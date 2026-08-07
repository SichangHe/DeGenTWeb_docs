"""Read-only, like-for-like detector timing study on DW1's cached models.

This research harness does not modify DW1 data or configuration. It times the
existing Binoculars path and faithful one-model implementations of DetectLLM-
LRR and SpecDetect on the same eight 2,048-token documents.
"""

from __future__ import annotations

import csv
import gc
import statistics
import time
from copy import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import scipy
import torch
import torch.nn.functional as F
import transformers
from transformers.tokenization_utils_base import BatchEncoding

from degentweb.classifying import BATCH_SIZE, CONTEXT_WINDOW
from degentweb.classifying.binoculars import Binoculars
from degentweb.classifying.detectors import detect_binoculars, detect_lrr


REPO_ROOT = Path(__file__).resolve().parents[3]
TRIAL_DATA = REPO_ROOT / "data/classify/cc10k/fdgpt_trial_all_df1"
REPEATS = 3


@dataclass(frozen=True)
class Timing:
    method: str
    seconds_per_batch: tuple[float, ...]
    median_seconds_per_batch: float
    median_seconds_per_document: float
    peak_allocated_mib_by_gpu: tuple[float, ...]


def _synchronize() -> None:
    for index in range(torch.cuda.device_count()):
        torch.cuda.synchronize(index)


def _reset_peak_memory() -> None:
    for index in range(torch.cuda.device_count()):
        torch.cuda.reset_peak_memory_stats(index)


def _peak_memory_mib() -> tuple[float, ...]:
    mib = 1024 * 1024
    return tuple(
        torch.cuda.max_memory_allocated(index) / mib
        for index in range(torch.cuda.device_count())
    )


def _read_longest_documents() -> tuple[list[str], list[str]]:
    records: list[tuple[int, str]] = []
    with TRIAL_DATA.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            records.append((int(row["n_tokens"]), row["extraction_path"]))
    records.sort(reverse=True)
    selected = records[:BATCH_SIZE]
    paths = [path for _, path in selected]
    texts = [(REPO_ROOT / path).read_text(encoding="utf-8") for path in paths]
    return texts, paths


def _measure(method: str, operation: Callable[[], list[float]]) -> Timing:
    operation()
    _synchronize()
    elapsed: list[float] = []
    peaks: list[tuple[float, ...]] = []
    for _ in range(REPEATS):
        _reset_peak_memory()
        started = time.perf_counter()
        scores = operation()
        _synchronize()
        elapsed.append(time.perf_counter() - started)
        peaks.append(_peak_memory_mib())
        if len(scores) != BATCH_SIZE:
            raise SystemExit(locals())
    median = statistics.median(elapsed)
    return Timing(
        method=method,
        seconds_per_batch=tuple(elapsed),
        median_seconds_per_batch=median,
        median_seconds_per_document=median / BATCH_SIZE,
        peak_allocated_mib_by_gpu=tuple(max(values) for values in zip(*peaks)),
    )


def _tokenize(tokenizer: transformers.PreTrainedTokenizerBase, texts: list[str]) -> BatchEncoding:
    return tokenizer(
        texts,
        return_tensors="pt",
        padding="longest",
        truncation=True,
        max_length=CONTEXT_WINDOW,
        return_token_type_ids=False,
    )


def _binoculars_scores(
    binoculars: Binoculars,
    encoding_observer: BatchEncoding,
    encoding_performer: BatchEncoding,
) -> list[float]:
    observer_logits, performer_logits = binoculars._get_logits(
        encoding_observer, encoding_performer
    )
    return detect_binoculars(
        observer_logits,
        performer_logits.to(binoculars.observer_model.device),
        encoding_observer,
        binoculars.tokenizer.pad_token_id,
    )


def _specdetect_scores(
    performer: transformers.PreTrainedModel,
    encoding: BatchEncoding,
) -> list[float]:
    with torch.inference_mode():
        logits = performer(**encoding).logits[:, :-1]
        labels = encoding.input_ids[:, 1:]
        mask = encoding.attention_mask[:, 1:].bool()
        log_probs = F.log_softmax(logits, dim=-1)
        token_log_likelihoods = log_probs.gather(
            dim=-1, index=labels.unsqueeze(-1)
        ).squeeze(-1)

    scores: list[float] = []
    for values, valid in zip(token_log_likelihoods, mask):
        sequence = values[valid].float().cpu().numpy()
        centered = sequence - np.mean(sequence)
        length = centered.shape[0]
        spectrum = np.fft.fft(centered)
        half_power = (np.abs(spectrum) / length) ** 2
        scores.append(float(-np.sum(half_power[: length // 2])))
    return scores


def _lrr_scores(
    performer: transformers.PreTrainedModel,
    encoding: BatchEncoding,
) -> list[float]:
    with torch.inference_mode():
        logits = performer(**encoding).logits[:, :-1]
        return detect_lrr(logits, encoding)


def main() -> None:
    if torch.cuda.device_count() != 2:
        raise SystemExit(locals())

    texts, paths = _read_longest_documents()
    binoculars = Binoculars(
        check_tokenizer_consistency=False,
        observer_kwargs={"local_files_only": True},
        performer_kwargs={"local_files_only": True},
    )
    encoded_cpu = _tokenize(binoculars.tokenizer, texts)
    token_lengths = encoded_cpu.attention_mask.sum(dim=1).tolist()
    if token_lengths != [CONTEXT_WINDOW] * BATCH_SIZE:
        raise SystemExit(locals())

    print(
        {
            "torch": torch.__version__,
            "transformers": transformers.__version__,
            "scipy": scipy.__version__,
            "gpu_names": tuple(
                torch.cuda.get_device_name(index)
                for index in range(torch.cuda.device_count())
            ),
            "batch_size": BATCH_SIZE,
            "sequence_lengths": token_lengths,
            "documents": paths,
            "observer": binoculars.observer_model.config._name_or_path,
            "performer": binoculars.performer_model.config._name_or_path,
            "observer_dtype": str(binoculars.observer_model.dtype),
            "performer_dtype": str(binoculars.performer_model.dtype),
        }
    )

    # Use the same boundary for every method: device-resident token IDs enter the
    # timed operation, while detector scores on the CPU leave it. Model loading,
    # tokenization, and host-to-device input transfer are excluded.
    encoding_observer = copy(encoded_cpu).to(binoculars.observer_model.device)
    encoding_performer = copy(encoded_cpu).to(binoculars.performer_model.device)
    binoculars_timing = _measure(
        "DW1 Binoculars, two concurrent Falcon forwards",
        lambda: _binoculars_scores(
            binoculars,
            encoding_observer,
            encoding_performer,
        ),
    )
    print(binoculars_timing)

    performer = binoculars.performer_model
    del binoculars.observer_model
    gc.collect()
    torch.cuda.empty_cache()
    candidate_encoding = copy(encoded_cpu).to(performer.device)

    specdetect_timing = _measure(
        "SpecDetect formula, one DW1 performer forward",
        lambda: _specdetect_scores(performer, candidate_encoding),
    )
    print(specdetect_timing)

    lrr_timing = _measure(
        "DetectLLM-LRR, one DW1 performer forward",
        lambda: _lrr_scores(performer, candidate_encoding),
    )
    print(lrr_timing)

    print(
        {
            "specdetect_to_binoculars_median_ratio": (
                specdetect_timing.median_seconds_per_batch
                / binoculars_timing.median_seconds_per_batch
            ),
            "lrr_to_binoculars_median_ratio": (
                lrr_timing.median_seconds_per_batch
                / binoculars_timing.median_seconds_per_batch
            ),
            "scope": (
                "Measured scoring latency and allocated CUDA memory only; model loading, "
                "tokenization, and input transfer excluded for every method. Accuracy, "
                "threshold calibration, sustained throughput, and multi-worker contention "
                "were not measured."
            ),
        }
    )


if __name__ == "__main__":
    main()
