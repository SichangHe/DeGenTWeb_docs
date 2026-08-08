"""Read-only A6000 timing screen for the released LAPD score.

The harness uses the official LAPD score and its ten-thousand conditional
token samples with DW1's cached Falcon base/instruction pair.  The pair's two
forwards are batched and concurrent; the released score, which requires batch
one, is then applied to each document.  Base logits are reused as sampling
logits, matching the release's cached path and avoiding a redundant forward.
"""

from __future__ import annotations

import csv
import statistics
import time
from copy import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import torch
import torch.nn.functional as F
from transformers.tokenization_utils_base import BatchEncoding

from degentweb.classifying import BATCH_SIZE, CONTEXT_WINDOW
from degentweb.classifying.binoculars import Binoculars
from degentweb.classifying.detectors import detect_binoculars


REPO_ROOT = Path(__file__).resolve().parents[3]
TRIAL_DATA = REPO_ROOT / "data/classify/cc10k/fdgpt_trial_all_df1"
REPEATS = 3
N_CONDITIONAL_SAMPLES = 10_000
SEED = 42
OFFICIAL_REPOSITORY_COMMIT = "1988eb68b70205d471c1924b6bbf1e199452662d"
OFFICIAL_COMPUTE_SHA256 = (
    "b1fa1fc8380b69f9f1acab980ebd8117d9708cf3af18174f3720687c35eebe4e"
)
OBSERVER_REVISION = "0ad33730b9d0911d6586670a661f04adaaf2c850"
PERFORMER_REVISION = "40d43a5d6ac55026c5a471d908c9d3bf6623dbb1"


@dataclass(frozen=True)
class Timing:
    method: str
    seconds_per_batch: tuple[float, ...]
    median_seconds_per_batch: float
    median_seconds_per_document: float
    peak_allocated_mib_by_gpu: tuple[float, ...]


def _read_longest_documents() -> tuple[list[str], list[str]]:
    records: list[tuple[int, str]] = []
    with TRIAL_DATA.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            path = row["extraction_path"]
            if (REPO_ROOT / path).is_file():
                records.append((int(row["n_tokens"]), path))
    records.sort(reverse=True)
    selected = records[:BATCH_SIZE]
    if len(selected) != BATCH_SIZE:
        raise SystemExit(locals())
    paths = [path for _, path in selected]
    texts = [(REPO_ROOT / path).read_text(encoding="utf-8") for path in paths]
    return texts, paths


def _assert_cached_revision(repository: str, expected: str) -> None:
    cache_name = f"models--{repository.replace('/', '--')}"
    reference = Path.home() / ".cache/huggingface/hub" / cache_name / "refs/main"
    if (
        not reference.is_file()
        or reference.read_text(encoding="utf-8").strip() != expected
    ):
        raise SystemExit(locals())


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


def _measure(method: str, operation: Callable[[], list[float]]) -> Timing:
    operation()
    _synchronize()
    elapsed: list[float] = []
    peaks: list[tuple[float, ...]] = []
    for _ in range(REPEATS):
        _reset_peak_memory()
        torch.manual_seed(SEED)
        torch.cuda.manual_seed_all(SEED)
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


def _conditional_samples(logits: torch.Tensor) -> torch.Tensor:
    log_probs = F.log_softmax(logits, dim=-1)
    distribution = torch.distributions.Categorical(logits=log_probs)
    return distribution.sample((N_CONDITIONAL_SAMPLES,)).permute(1, 2, 0)


def _token_likelihoods(logits: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
    if labels.ndim == logits.ndim - 1:
        labels = labels.unsqueeze(-1)
    log_probs = F.log_softmax(logits, dim=-1)
    return log_probs.gather(dim=-1, index=labels)


def _lapd_score(
    base_logits: torch.Tensor,
    instruction_logits: torch.Tensor,
    labels: torch.Tensor,
) -> float:
    if base_logits.shape[0] != 1 or instruction_logits.shape[0] != 1:
        raise SystemExit(locals())
    samples = _conditional_samples(base_logits)
    base_observed = _token_likelihoods(base_logits, labels)
    instruction_observed = _token_likelihoods(instruction_logits, labels)
    base_sampled = _token_likelihoods(base_logits, samples)
    instruction_sampled = _token_likelihoods(instruction_logits, samples)
    observed = (instruction_observed * (base_observed - instruction_observed)).mean(
        dim=1
    )
    sampled = (instruction_sampled * (base_sampled - instruction_sampled)).mean(dim=1)
    discrepancy = (observed.squeeze(-1) - sampled.mean(dim=-1)) / sampled.std(dim=-1)
    return discrepancy.item()


def _binoculars_scores(
    binoculars: Binoculars,
    observer_encoding: BatchEncoding,
    performer_encoding: BatchEncoding,
) -> list[float]:
    observer_logits, performer_logits = binoculars._get_logits(
        observer_encoding,
        performer_encoding,
    )
    return detect_binoculars(
        observer_logits,
        performer_logits.to(observer_logits.device),
        observer_encoding,
        binoculars.tokenizer.pad_token_id,
    )


def _lapd_scores(
    binoculars: Binoculars,
    observer_encoding: BatchEncoding,
    performer_encoding: BatchEncoding,
) -> list[float]:
    observer_logits, performer_logits = binoculars._get_logits(
        observer_encoding,
        performer_encoding,
    )
    base_logits = observer_logits[:, :-1]
    labels = observer_encoding.input_ids[:, 1:]
    scores: list[float] = []
    for index in range(BATCH_SIZE):
        instruction_logits = performer_logits[index : index + 1, :-1].to(
            base_logits.device
        )
        scores.append(
            _lapd_score(
                base_logits[index : index + 1],
                instruction_logits,
                labels[index : index + 1],
            )
        )
    return scores


def main() -> None:
    if torch.cuda.device_count() != 2:
        raise SystemExit(locals())
    _assert_cached_revision("SichangHe/falcon-7b-FP8-Dynamic", OBSERVER_REVISION)
    _assert_cached_revision(
        "SichangHe/falcon-7b-instruct-FP8-Dynamic",
        PERFORMER_REVISION,
    )
    texts, paths = _read_longest_documents()
    binoculars = Binoculars(
        check_tokenizer_consistency=False,
        observer_kwargs={"local_files_only": True},
        performer_kwargs={"local_files_only": True},
    )
    encoded_cpu = binoculars.tokenizer(
        texts,
        return_tensors="pt",
        padding="longest",
        truncation=True,
        max_length=CONTEXT_WINDOW,
        return_token_type_ids=False,
    )
    lengths = tuple(int(value) for value in encoded_cpu.attention_mask.sum(dim=1))
    if lengths != (CONTEXT_WINDOW,) * BATCH_SIZE:
        raise SystemExit(locals())
    observer_encoding = copy(encoded_cpu).to(binoculars.observer_model.device)
    performer_encoding = copy(encoded_cpu).to(binoculars.performer_model.device)

    print(
        {
            "artifact": "creator-xi/LAPD",
            "artifact_commit": OFFICIAL_REPOSITORY_COMMIT,
            "official_compute_sha256": OFFICIAL_COMPUTE_SHA256,
            "observer": binoculars.observer_model.config._name_or_path,
            "observer_revision": OBSERVER_REVISION,
            "performer": binoculars.performer_model.config._name_or_path,
            "performer_revision": PERFORMER_REVISION,
            "observer_dtype": str(binoculars.observer_model.dtype),
            "performer_dtype": str(binoculars.performer_model.dtype),
            "gpu_names": tuple(
                torch.cuda.get_device_name(index)
                for index in range(torch.cuda.device_count())
            ),
            "gpu_total_memory_mib": tuple(
                torch.cuda.get_device_properties(index).total_memory / (1024 * 1024)
                for index in range(torch.cuda.device_count())
            ),
            "batch_size": BATCH_SIZE,
            "sequence_lengths": lengths,
            "conditional_samples_per_token": N_CONDITIONAL_SAMPLES,
            "documents": paths,
        }
    )
    binoculars_timing = _measure(
        "DW1 Binoculars, two concurrent Falcon forwards",
        lambda: _binoculars_scores(
            binoculars,
            observer_encoding,
            performer_encoding,
        ),
    )
    print(binoculars_timing)
    lapd_timing = _measure(
        "LAPD, same concurrent Falcon forwards plus released score",
        lambda: _lapd_scores(
            binoculars,
            observer_encoding,
            performer_encoding,
        ),
    )
    print(lapd_timing)
    print(
        {
            "lapd_to_binoculars_median_batch_ratio": (
                lapd_timing.median_seconds_per_batch
                / binoculars_timing.median_seconds_per_batch
            ),
            "scope": (
                "Same hardware, models, token IDs, batch, documents, and timing boundary. "
                "This validates cost only; paper accuracy used full-precision Llama-2 or "
                "Falcon pairs and does not transfer to DW1's dynamic Falcon checkpoints."
            ),
        }
    )


if __name__ == "__main__":
    main()
