"""Read-only WaveDetect feasibility study using its public official artifact.

Run with the downloaded Hugging Face snapshot on ``PYTHONPATH``. The script
does not modify DW1 data or configuration.
"""

from __future__ import annotations

import csv
import importlib
import platform
import random
import statistics
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import torch
import torch.nn as nn
import transformers
from sklearn.metrics import roc_auc_score
from transformers.tokenization_utils_base import BatchEncoding, PreTrainedTokenizerBase


REPO_ROOT = Path(__file__).resolve().parents[3]
TRIAL_DATA = REPO_ROOT / "data/classify/cc10k/fdgpt_trial_all_df1"
BATCH_SIZE = 8
REPEATS = 3
EVALUATION_SAMPLES_PER_CLASS = 500
SEED = 42


class WaveDetectPredictor(Protocol):
    device: torch.device
    model: nn.Module
    tokenizer: PreTrainedTokenizerBase


@dataclass(frozen=True)
class TrialRecord:
    path: str
    n_tokens: int
    is_generated: int
    binoculars: float
    fast_detect_gpt: float
    lrr: float
    roberta: float
    radar: float


@dataclass(frozen=True)
class Timing:
    max_length: int
    seconds_per_batch: tuple[float, ...]
    median_seconds_per_batch: float
    median_seconds_per_document: float
    peak_allocated_mib: float


def _load_predictor() -> WaveDetectPredictor:
    module = importlib.import_module("wavedetect_hf")
    predictor_type = module.WaveDetectPredictor
    return predictor_type(device="cuda:0")


def _read_records() -> list[TrialRecord]:
    records: list[TrialRecord] = []
    with TRIAL_DATA.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            records.append(
                TrialRecord(
                    path=row["extraction_path"],
                    n_tokens=int(row["n_tokens"]),
                    is_generated=int(row["is_generated"]),
                    binoculars=float(row["binoculars"]),
                    fast_detect_gpt=float(row["fast_detect_gpt"]),
                    lrr=float(row["lrr"]),
                    roberta=float(row["roberta"]),
                    radar=float(row["radar"]),
                )
            )
    return records


def _read_texts(records: list[TrialRecord]) -> list[str]:
    return [
        (REPO_ROOT / record.path).read_text(encoding="utf-8") for record in records
    ]


def _has_local_text(record: TrialRecord) -> bool:
    return (REPO_ROOT / record.path).is_file()


def _nvidia_smi_environment() -> tuple[str, ...]:
    result = subprocess.run(
        [
            "nvidia-smi",
            "--query-gpu=index,name,driver_version,memory.total",
            "--format=csv,noheader,nounits",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    if len(rows) != torch.cuda.device_count():
        raise SystemExit(locals())
    return rows


def _tokenize(
    predictor: WaveDetectPredictor,
    texts: list[str],
    max_length: int,
) -> BatchEncoding:
    return predictor.tokenizer(
        texts,
        return_tensors="pt",
        truncation=True,
        max_length=max_length,
        padding=True,
    ).to(predictor.device)


@torch.no_grad()
def _score_encoding(
    predictor: WaveDetectPredictor,
    encoding: BatchEncoding,
) -> list[float]:
    logits = predictor.model(encoding["input_ids"], encoding["attention_mask"])
    return torch.softmax(logits, dim=-1)[:, 1].float().cpu().tolist()


def _measure(
    predictor: WaveDetectPredictor,
    texts: list[str],
    max_length: int,
) -> Timing:
    encoding = _tokenize(predictor, texts, max_length)
    token_lengths = encoding.attention_mask.sum(dim=1).tolist()
    if token_lengths != [max_length] * BATCH_SIZE:
        raise SystemExit(locals())
    _score_encoding(predictor, encoding)
    torch.cuda.synchronize()
    elapsed: list[float] = []
    peaks: list[float] = []
    for _ in range(REPEATS):
        torch.cuda.reset_peak_memory_stats(predictor.device)
        started = time.perf_counter()
        scores = _score_encoding(predictor, encoding)
        torch.cuda.synchronize()
        elapsed.append(time.perf_counter() - started)
        peaks.append(torch.cuda.max_memory_allocated(predictor.device) / (1024 * 1024))
        if len(scores) != BATCH_SIZE:
            raise SystemExit(locals())
    median = statistics.median(elapsed)
    return Timing(
        max_length=max_length,
        seconds_per_batch=tuple(elapsed),
        median_seconds_per_batch=median,
        median_seconds_per_document=median / BATCH_SIZE,
        peak_allocated_mib=max(peaks),
    )


def _balanced_evaluation_records(records: list[TrialRecord]) -> list[TrialRecord]:
    rng = random.Random(SEED)
    human = [record for record in records if record.is_generated == 0]
    generated = [record for record in records if record.is_generated == 1]
    selected = rng.sample(human, EVALUATION_SAMPLES_PER_CLASS)
    selected.extend(rng.sample(generated, EVALUATION_SAMPLES_PER_CLASS))
    rng.shuffle(selected)
    return selected


def _orientation_free_auc(labels: list[int], scores: list[float]) -> float:
    auc = float(roc_auc_score(labels, scores))
    return max(auc, 1 - auc)


def _evaluate(
    predictor: WaveDetectPredictor,
    records: list[TrialRecord],
) -> None:
    labels = [record.is_generated for record in records]
    wave_scores: list[float] = []
    started = time.perf_counter()
    for start in range(0, len(records), BATCH_SIZE):
        batch_records = records[start : start + BATCH_SIZE]
        encoding = _tokenize(predictor, _read_texts(batch_records), 1024)
        wave_scores.extend(_score_encoding(predictor, encoding))
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - started

    print(
        {
            "evaluation_n": len(records),
            "human_n": labels.count(0),
            "generated_n": labels.count(1),
            "selection_seed": SEED,
            "max_length": 1024,
            "batch_size": BATCH_SIZE,
            "elapsed_seconds": elapsed,
            "seconds_per_document": elapsed / len(records),
            "wave_detect_raw_auc": float(roc_auc_score(labels, wave_scores)),
            "wave_detect_orientation_free_auc": _orientation_free_auc(
                labels, wave_scores
            ),
            "binoculars_orientation_free_auc": _orientation_free_auc(
                labels, [-record.binoculars for record in records]
            ),
            "fast_detect_gpt_orientation_free_auc": _orientation_free_auc(
                labels, [record.fast_detect_gpt for record in records]
            ),
            "lrr_orientation_free_auc": _orientation_free_auc(
                labels, [record.lrr for record in records]
            ),
            "roberta_orientation_free_auc": _orientation_free_auc(
                labels, [record.roberta for record in records]
            ),
            "radar_orientation_free_auc": _orientation_free_auc(
                labels, [record.radar for record in records]
            ),
        }
    )


def main() -> None:
    if torch.cuda.device_count() != 2:
        raise SystemExit(locals())
    all_records = _read_records()
    records = [record for record in all_records if _has_local_text(record)]
    if not records:
        raise SystemExit(locals())
    longest = sorted(records, key=lambda record: record.n_tokens, reverse=True)[
        :BATCH_SIZE
    ]
    texts = _read_texts(longest)
    predictor = _load_predictor()

    print(
        {
            "artifact": "KaitongQin/WaveDetect",
            "artifact_revision": "c4d72102938842de531990b3e961d3b41aaa4f05",
            "checkpoint_sha256": (
                "68d100bfa9f7a9081627b55e988963bd230628f8cc62e1913ef85d44fdbab096"
            ),
            "python": platform.python_version(),
            "torch": torch.__version__,
            "torch_cuda_build": torch.version.cuda,
            "transformers": transformers.__version__,
            "nvidia_smi_gpus": _nvidia_smi_environment(),
            "batch_size": BATCH_SIZE,
            "score_rows": len(all_records),
            "rows_with_local_text": len(records),
            "missing_text_rows": len(all_records) - len(records),
            "documents": [record.path for record in longest],
        }
    )
    print(_measure(predictor, texts, 1024))
    print(_measure(predictor, texts, 2048))
    _evaluate(predictor, _balanced_evaluation_records(records))


if __name__ == "__main__":
    main()
