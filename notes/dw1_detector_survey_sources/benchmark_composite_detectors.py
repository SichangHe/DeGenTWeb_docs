"""Bounded public-checkpoint screen for detectors surfaced by composite sources.

This research harness reads DW1's trial corpus without modifying it. It evaluates
three immutable public model revisions that were hidden behind benchmark,
evaluation, or training-study coverage rows. Each artifact is run at its released
maximum input length; the different length limits are reported and are not treated
as a like-for-like 2,048-token comparison.
"""

from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import math
import platform
import random
import statistics
import subprocess
import time
from collections.abc import Callable, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import torch
import torch.nn as nn
import transformers
from safetensors.torch import load_file
from sklearn.metrics import roc_auc_score
from transformers import AutoConfig, AutoModel, AutoModelForSequenceClassification
from transformers import AutoTokenizer
from transformers.modeling_utils import PreTrainedModel
from transformers.tokenization_utils_base import PreTrainedTokenizerBase


REPO_ROOT = Path(__file__).resolve().parents[3]
TRIAL_DATA = REPO_ROOT / "data/classify/cc10k/fdgpt_trial_all_df1"
BATCH_SIZE = 8
REPEATS = 5
DIRECT_SCREEN_SAMPLES_PER_CLASS = 500
DIRECT_SCREEN_SEED = 42
CALIBRATION_HUMAN_N = 1_000
CALIBRATION_SEED = 20_260_808
MIN_WORDS = 100
DW1_BINOCULARS_MEDIAN_BATCH_SECONDS = 7.732507459819317
type TensorEncoding = dict[str, torch.Tensor]


@dataclass(frozen=True)
class Candidate:
    key: str
    display_name: str
    revision: str
    weight_sha256: str
    max_length: int
    score_semantics: str
    execution_note: str


CANDIDATES = (
    Candidate(
        key="detectrlx_xlm",
        display_name="DetectRL-X X-Rob-Classifier",
        revision="76649a0257a812a81cf36b5de9cc5f2430aeaa7f",
        weight_sha256=(
            "c43079dafc0d33f815b6a1ba594a94cb67c58aa470061e322c00c4038e14fb88"
        ),
        max_length=512,
        score_semantics=(
            "logit[1]-logit[0]; paper orders binary labels HWT then LGT, but the "
            "released config omits id2label"
        ),
        execution_note="immutable released model and tokenizer path",
    ),
    Candidate(
        key="desklib",
        display_name="Desklib AI text detector v1.01",
        revision="5fdea974cd4287c61674951ec78803aa274e2fb7",
        weight_sha256=(
            "c024a1704c65f5a4bffeda58745c58fc0ed67d6ca07b158b068a257238815265"
        ),
        max_length=768,
        score_semantics="single released classifier logit; higher means AI",
        execution_note="exact custom architecture and max_len=768 card path",
    ),
    Candidate(
        key="modernbert",
        display_name="ModernBERT AI detector",
        revision="08f218f1d05791ad99c26ede421f69c781a50360",
        weight_sha256=(
            "880d16944505698bf8366a0c888161fc155902ec8f0ce68744401e04a5ff6e20"
        ),
        max_length=2_048,
        score_semantics=(
            "logit[1]-logit[0]; immutable model card identifies class 1 as AI"
        ),
        execution_note=(
            "reference_compile disabled because transformers 4.57.3 cannot run "
            "that optimization concurrently on two replicas; math and weights unchanged"
        ),
    ),
)


@dataclass(frozen=True)
class TrialRecord:
    row_index: int
    path: str
    n_tokens: int
    is_generated: int
    binoculars: float
    fast_detect_gpt: float


@dataclass(frozen=True)
class CandidateScore:
    row_index: int
    word_count: int
    token_count: int
    score: float


@dataclass(frozen=True)
class Timing:
    method: str
    max_length: int
    batch_size: int
    sequence_lengths: tuple[int, ...]
    seconds_per_batch: tuple[float, ...]
    median_seconds_per_batch: float
    median_seconds_per_document: float
    peak_allocated_mib_by_gpu: tuple[float, ...]
    peak_reserved_mib_by_gpu: tuple[float, ...]
    ratio_to_dw1_binoculars_batch: float


@dataclass(frozen=True)
class OperatingPoint:
    method: str
    target_calibration_fpr: float
    threshold: float
    calibration_fpr: float
    evaluation_human_n: int
    evaluation_generated_n: int
    evaluation_fpr: float
    evaluation_tpr: float


class Detector(nn.Module):
    """Common raw-score interface for the three immutable detector states."""

    @torch.inference_mode()
    def score_encoding(self, encoding: TensorEncoding) -> list[float]:
        raise NotImplementedError


class SequenceClassifierDetector(Detector):
    def __init__(self, model_dir: Path) -> None:
        super().__init__()
        self.model: PreTrainedModel = (
            AutoModelForSequenceClassification.from_pretrained(
                model_dir,
                local_files_only=True,
            )
        )
        self.model.eval()

    @torch.inference_mode()
    def score_encoding(self, encoding: TensorEncoding) -> list[float]:
        logits = self.model(**encoding).logits.float()
        if logits.ndim != 2 or logits.shape[1] != 2:
            raise SystemExit(locals())
        return (logits[:, 1] - logits[:, 0]).cpu().tolist()


class DesklibDetector(Detector):
    """Exact mean-pooling/single-logit architecture in the immutable card."""

    def __init__(self, model_dir: Path) -> None:
        super().__init__()
        config = AutoConfig.from_pretrained(model_dir, local_files_only=True)
        self.model: PreTrainedModel = AutoModel.from_config(config)
        self.classifier = nn.Linear(config.hidden_size, 1)
        self.load_state_dict(load_file(model_dir / "model.safetensors"), strict=True)
        self.eval()

    @torch.inference_mode()
    def score_encoding(self, encoding: TensorEncoding) -> list[float]:
        attention_mask = encoding["attention_mask"]
        hidden = self.model(**encoding).last_hidden_state.float()
        expanded = attention_mask.unsqueeze(-1).expand(hidden.size()).float()
        pooled = (hidden * expanded).sum(1) / expanded.sum(1).clamp(min=1e-9)
        return self.classifier(pooled).squeeze(-1).cpu().tolist()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-root", required=True, type=Path)
    parser.add_argument("--scores-out", required=True, type=Path)
    return parser.parse_args()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_records() -> list[TrialRecord]:
    records: list[TrialRecord] = []
    with TRIAL_DATA.open(newline="", encoding="utf-8") as stream:
        for row_index, row in enumerate(csv.DictReader(stream)):
            records.append(
                TrialRecord(
                    row_index=row_index,
                    path=row["extraction_path"],
                    n_tokens=int(row["n_tokens"]),
                    is_generated=int(row["is_generated"]),
                    binoculars=float(row["binoculars"]),
                    fast_detect_gpt=float(row["fast_detect_gpt"]),
                )
            )
    return records


def _has_local_text(record: TrialRecord) -> bool:
    return (REPO_ROOT / record.path).is_file()


def _read_text(record: TrialRecord) -> str:
    return (REPO_ROOT / record.path).read_text(encoding="utf-8")


def _model_dir(model_root: Path, candidate: Candidate) -> Path:
    return model_root / candidate.key


def _load_detector(
    model_dir: Path, candidate: Candidate, device: torch.device
) -> Detector:
    if candidate.key == "desklib":
        model: Detector = DesklibDetector(model_dir)
    else:
        model = SequenceClassifierDetector(model_dir)
        if candidate.key == "modernbert":
            model.model.config.reference_compile = False
    model.to(device)
    model.eval()
    return model


def _load_tokenizer(model_dir: Path, candidate: Candidate) -> PreTrainedTokenizerBase:
    return AutoTokenizer.from_pretrained(
        model_dir,
        local_files_only=True,
        use_fast=candidate.key != "detectrlx_xlm",
    )


def _tokenize(
    tokenizer: PreTrainedTokenizerBase,
    texts: Sequence[str],
    max_length: int,
    device: torch.device,
) -> TensorEncoding:
    raw = tokenizer(
        list(texts),
        return_tensors="pt",
        return_token_type_ids=False,
        padding=True,
        truncation=True,
        max_length=max_length,
    )
    return {
        key: value.to(device)
        for key, value in raw.items()
        if isinstance(value, torch.Tensor)
    }


def _synchronize() -> None:
    for device_index in range(torch.cuda.device_count()):
        torch.cuda.synchronize(device_index)


def _reset_peak_memory() -> None:
    for device_index in range(torch.cuda.device_count()):
        torch.cuda.reset_peak_memory_stats(device_index)


def _peak_memory_mib() -> tuple[tuple[float, ...], tuple[float, ...]]:
    divisor = 1024 * 1024
    allocated = tuple(
        torch.cuda.max_memory_allocated(device_index) / divisor
        for device_index in range(torch.cuda.device_count())
    )
    reserved = tuple(
        torch.cuda.max_memory_reserved(device_index) / divisor
        for device_index in range(torch.cuda.device_count())
    )
    return allocated, reserved


def _score_concurrently(
    models: tuple[Detector, Detector],
    encodings: tuple[TensorEncoding, TensorEncoding],
) -> list[float]:
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(model.score_encoding, encoding)
            for model, encoding in zip(models, encodings, strict=True)
        ]
        results = [future.result() for future in futures]
    return results[0] + results[1]


def _measure(
    candidate: Candidate,
    method: str,
    batch_size: int,
    sequence_lengths: tuple[int, ...],
    operation: Callable[[], object],
) -> Timing:
    operation()
    _synchronize()
    elapsed_s: list[float] = []
    allocated_peaks: list[tuple[float, ...]] = []
    reserved_peaks: list[tuple[float, ...]] = []
    for _ in range(REPEATS):
        _reset_peak_memory()
        _synchronize()
        started = time.perf_counter()
        operation()
        _synchronize()
        elapsed_s.append(time.perf_counter() - started)
        allocated, reserved = _peak_memory_mib()
        allocated_peaks.append(allocated)
        reserved_peaks.append(reserved)
    median_s = statistics.median(elapsed_s)
    return Timing(
        method=method,
        max_length=candidate.max_length,
        batch_size=batch_size,
        sequence_lengths=sequence_lengths,
        seconds_per_batch=tuple(elapsed_s),
        median_seconds_per_batch=median_s,
        median_seconds_per_document=median_s / batch_size,
        peak_allocated_mib_by_gpu=tuple(
            max(values) for values in zip(*allocated_peaks)
        ),
        peak_reserved_mib_by_gpu=tuple(max(values) for values in zip(*reserved_peaks)),
        ratio_to_dw1_binoculars_batch=median_s / DW1_BINOCULARS_MEDIAN_BATCH_SECONDS,
    )


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
    return tuple(line.strip() for line in result.stdout.splitlines() if line.strip())


def _manifest_sha256(records: Sequence[TrialRecord]) -> str:
    digest = hashlib.sha256()
    for record in records:
        digest.update(
            (
                f"{record.row_index}\t{record.path}\t{record.n_tokens}\t"
                f"{record.is_generated}\t{record.binoculars!r}\t"
                f"{record.fast_detect_gpt!r}\n"
            ).encode()
        )
    return digest.hexdigest()


def _text_sha256(records: Sequence[TrialRecord]) -> str:
    digest = hashlib.sha256()
    for record in records:
        digest.update(record.path.encode())
        digest.update(b"\0")
        with (REPO_ROOT / record.path).open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


def _direct_screen_records(records: Sequence[TrialRecord]) -> list[TrialRecord]:
    rng = random.Random(DIRECT_SCREEN_SEED)
    human = [record for record in records if record.is_generated == 0]
    generated = [record for record in records if record.is_generated == 1]
    selected = rng.sample(human, DIRECT_SCREEN_SAMPLES_PER_CLASS)
    selected.extend(rng.sample(generated, DIRECT_SCREEN_SAMPLES_PER_CLASS))
    rng.shuffle(selected)
    return selected


def _empirical_threshold(human_scores: list[float], target_fpr: float) -> float:
    descending = sorted(human_scores, reverse=True)
    n_allowed = math.floor(target_fpr * len(descending))
    if n_allowed >= len(descending):
        raise SystemExit(locals())
    return descending[n_allowed]


def _operating_point(
    method: str,
    calibration_scores: list[float],
    evaluation_human_scores: list[float],
    evaluation_generated_scores: list[float],
    target_fpr: float,
) -> OperatingPoint:
    threshold = _empirical_threshold(calibration_scores, target_fpr)
    return OperatingPoint(
        method=method,
        target_calibration_fpr=target_fpr,
        threshold=threshold,
        calibration_fpr=sum(score > threshold for score in calibration_scores)
        / len(calibration_scores),
        evaluation_human_n=len(evaluation_human_scores),
        evaluation_generated_n=len(evaluation_generated_scores),
        evaluation_fpr=sum(score > threshold for score in evaluation_human_scores)
        / len(evaluation_human_scores),
        evaluation_tpr=sum(score > threshold for score in evaluation_generated_scores)
        / len(evaluation_generated_scores),
    )


def _auc(labels: Sequence[int], scores: Sequence[float]) -> float:
    return float(roc_auc_score(labels, scores))


def _evaluate_candidate(
    records: Sequence[TrialRecord],
    tokenizer: PreTrainedTokenizerBase,
    models: tuple[Detector, Detector],
    candidate: Candidate,
) -> dict[int, CandidateScore]:
    scored: dict[int, CandidateScore] = {}
    started = time.perf_counter()
    for start in range(0, len(records), BATCH_SIZE):
        batch = records[start : start + BATCH_SIZE]
        texts = [_read_text(record) for record in batch]
        midpoint = max(1, len(batch) // 2)
        first_encoding = _tokenize(
            tokenizer,
            texts[:midpoint],
            candidate.max_length,
            torch.device("cuda:0"),
        )
        second_texts = texts[midpoint:]
        if second_texts:
            second_encoding = _tokenize(
                tokenizer,
                second_texts,
                candidate.max_length,
                torch.device("cuda:1"),
            )
            scores = _score_concurrently(models, (first_encoding, second_encoding))
            token_counts = first_encoding["attention_mask"].sum(1).cpu().tolist()
            token_counts.extend(second_encoding["attention_mask"].sum(1).cpu().tolist())
        else:
            scores = models[0].score_encoding(first_encoding)
            token_counts = first_encoding["attention_mask"].sum(1).cpu().tolist()
        for record, text, token_count, score in zip(
            batch,
            texts,
            token_counts,
            scores,
            strict=True,
        ):
            scored[record.row_index] = CandidateScore(
                row_index=record.row_index,
                word_count=len(text.split()),
                token_count=int(token_count),
                score=score,
            )
    _synchronize()
    elapsed_s = time.perf_counter() - started
    print(
        {
            "candidate": candidate.display_name,
            "evaluation_rows": len(records),
            "elapsed_seconds_including_text_reads_tokenization_and_transfer": elapsed_s,
            "seconds_per_document": elapsed_s / len(records),
        }
    )
    return scored


def _report_accuracy(
    candidate: Candidate,
    records: Sequence[TrialRecord],
    scored: dict[int, CandidateScore],
) -> None:
    direct_records = _direct_screen_records(records)
    direct_labels = [record.is_generated for record in direct_records]
    direct_scores = [scored[record.row_index].score for record in direct_records]
    direct_human = [
        scored[record.row_index].score
        for record in direct_records
        if record.is_generated == 0
    ]
    direct_generated = [
        scored[record.row_index].score
        for record in direct_records
        if record.is_generated == 1
    ]
    print(
        {
            "candidate": candidate.display_name,
            "direct_screen_n": len(direct_records),
            "direct_screen_seed": DIRECT_SCREEN_SEED,
            "direct_screen_manifest_sha256": _manifest_sha256(direct_records),
            "direct_screen_text_sha256": _text_sha256(direct_records),
            "direct_screen_under_100_words_n": sum(
                scored[record.row_index].word_count < MIN_WORDS
                for record in direct_records
            ),
            "candidate_auc": _auc(direct_labels, direct_scores),
            "candidate_human_mean_score": statistics.fmean(direct_human),
            "candidate_generated_mean_score": statistics.fmean(direct_generated),
            "binoculars_auc": _auc(
                direct_labels, [-record.binoculars for record in direct_records]
            ),
            "fast_detect_gpt_auc": _auc(
                direct_labels, [record.fast_detect_gpt for record in direct_records]
            ),
        }
    )

    eligible = [
        record for record in records if scored[record.row_index].word_count >= MIN_WORDS
    ]
    eligible_human = [record for record in eligible if record.is_generated == 0]
    rng = random.Random(CALIBRATION_SEED)
    calibration = rng.sample(eligible_human, CALIBRATION_HUMAN_N)
    calibration_rows = {record.row_index for record in calibration}
    evaluation = [
        record for record in eligible if record.row_index not in calibration_rows
    ]
    evaluation_human = [record for record in evaluation if record.is_generated == 0]
    evaluation_generated = [record for record in evaluation if record.is_generated == 1]
    labels = [record.is_generated for record in evaluation]
    methods: dict[str, Callable[[TrialRecord], float]] = {
        candidate.display_name: lambda record: scored[record.row_index].score,
        "stored DW1 Binoculars, sign-normalized": lambda record: -record.binoculars,
        "stored DW1 FastDetectGPT": lambda record: record.fast_detect_gpt,
    }
    print(
        {
            "candidate": candidate.display_name,
            "eligible_min_words": MIN_WORDS,
            "eligible_n": len(eligible),
            "excluded_under_100_words_n": len(records) - len(eligible),
            "calibration_seed": CALIBRATION_SEED,
            "calibration_human_n": len(calibration),
            "calibration_manifest_sha256": _manifest_sha256(calibration),
            "evaluation_n": len(evaluation),
            "evaluation_human_n": len(evaluation_human),
            "evaluation_generated_n": len(evaluation_generated),
            "evaluation_manifest_sha256": _manifest_sha256(evaluation),
            "evaluation_text_sha256": _text_sha256(evaluation),
        }
    )
    for method, score_of in methods.items():
        print(
            {
                "candidate_context": candidate.display_name,
                "method": method,
                "evaluation_auc": _auc(
                    labels, [score_of(record) for record in evaluation]
                ),
            }
        )
        for target_fpr in (0.01, 0.05):
            print(
                _operating_point(
                    method,
                    [score_of(record) for record in calibration],
                    [score_of(record) for record in evaluation_human],
                    [score_of(record) for record in evaluation_generated],
                    target_fpr,
                )
            )


def _write_scores(
    records: Sequence[TrialRecord],
    all_scores: dict[str, dict[int, CandidateScore]],
    output_path: Path,
) -> None:
    first = all_scores[CANDIDATES[0].key]
    eligible_human = [
        record
        for record in records
        if record.is_generated == 0 and first[record.row_index].word_count >= MIN_WORDS
    ]
    calibration_rows = {
        record.row_index
        for record in random.Random(CALIBRATION_SEED).sample(
            eligible_human, CALIBRATION_HUMAN_N
        )
    }
    fields = [
        "row_index",
        "path",
        "is_generated",
        "word_count",
        "split",
        "binoculars_ai_score",
        "fast_detect_gpt_score",
    ]
    for candidate in CANDIDATES:
        fields.extend((f"{candidate.key}_token_count", f"{candidate.key}_score"))
    with output_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(fields)
        for record in records:
            split = "evaluation"
            if first[record.row_index].word_count < MIN_WORDS:
                split = "excluded_under_100_words"
            elif record.row_index in calibration_rows:
                split = "calibration_human"
            row: list[object] = [
                record.row_index,
                record.path,
                record.is_generated,
                first[record.row_index].word_count,
                split,
                repr(-record.binoculars),
                repr(record.fast_detect_gpt),
            ]
            for candidate in CANDIDATES:
                score = all_scores[candidate.key][record.row_index]
                row.extend((score.token_count, repr(score.score)))
            writer.writerow(row)


def main() -> None:
    args = _parse_args()
    if torch.cuda.device_count() != 2:
        raise SystemExit(locals())
    records = _read_records()
    available = [record for record in records if _has_local_text(record)]
    longest = sorted(available, key=lambda record: record.n_tokens, reverse=True)[
        :BATCH_SIZE
    ]
    longest_texts = [_read_text(record) for record in longest]
    print(
        {
            "run_at": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(),
            "python": platform.python_version(),
            "torch": torch.__version__,
            "torch_cuda_build": torch.version.cuda,
            "transformers": transformers.__version__,
            "nvidia_smi_gpus": _nvidia_smi_environment(),
            "trial_rows": len(records),
            "rows_with_local_text": len(available),
            "trial_csv_sha256": _file_sha256(TRIAL_DATA),
            "longest_documents": [record.path for record in longest],
            "timing_boundary": (
                "device-resident token tensors entered scoring and CPU scores left it"
            ),
            "timing_repetitions": REPEATS,
        }
    )

    all_scores: dict[str, dict[int, CandidateScore]] = {}
    for candidate in CANDIDATES:
        model_dir = _model_dir(args.model_root, candidate)
        if _file_sha256(model_dir / "model.safetensors") != candidate.weight_sha256:
            raise SystemExit(locals())
        tokenizer = _load_tokenizer(model_dir, candidate)
        models = (
            _load_detector(model_dir, candidate, torch.device("cuda:0")),
            _load_detector(model_dir, candidate, torch.device("cuda:1")),
        )
        one_encoding = _tokenize(
            tokenizer,
            longest_texts[:1],
            candidate.max_length,
            torch.device("cuda:0"),
        )
        batch_encoding = _tokenize(
            tokenizer,
            longest_texts,
            candidate.max_length,
            torch.device("cuda:0"),
        )
        first_encoding = _tokenize(
            tokenizer,
            longest_texts[:4],
            candidate.max_length,
            torch.device("cuda:0"),
        )
        second_encoding = _tokenize(
            tokenizer,
            longest_texts[4:],
            candidate.max_length,
            torch.device("cuda:1"),
        )
        sequence_lengths = tuple(
            int(value) for value in batch_encoding["attention_mask"].sum(1).tolist()
        )
        if sequence_lengths != (candidate.max_length,) * BATCH_SIZE:
            raise SystemExit(locals())
        print(
            {
                "candidate": candidate.display_name,
                "revision": candidate.revision,
                "weight_sha256": candidate.weight_sha256,
                "max_length": candidate.max_length,
                "score_semantics": candidate.score_semantics,
                "execution_note": candidate.execution_note,
                "parameter_count": sum(
                    parameter.numel() for parameter in models[0].parameters()
                ),
                "dtype": str(next(models[0].parameters()).dtype),
                "model_files": {
                    path.name: _file_sha256(path)
                    for path in sorted(model_dir.iterdir())
                    if path.is_file()
                },
            }
        )
        print(
            _measure(
                candidate,
                f"{candidate.display_name}, one GPU, batch 1",
                1,
                (int(one_encoding["attention_mask"].sum()),),
                lambda: models[0].score_encoding(one_encoding),
            )
        )
        print(
            _measure(
                candidate,
                f"{candidate.display_name}, one GPU, batch 8",
                BATCH_SIZE,
                sequence_lengths,
                lambda: models[0].score_encoding(batch_encoding),
            )
        )
        print(
            _measure(
                candidate,
                f"{candidate.display_name}, two replica GPUs, concurrent batch 4+4",
                BATCH_SIZE,
                sequence_lengths,
                lambda: _score_concurrently(models, (first_encoding, second_encoding)),
            )
        )
        scored = _evaluate_candidate(available, tokenizer, models, candidate)
        all_scores[candidate.key] = scored
        _report_accuracy(candidate, available, scored)
        models[0].to(torch.device("cpu"))
        models[1].to(torch.device("cpu"))
        gc.collect()
        torch.cuda.empty_cache()

    _write_scores(available, all_scores, args.scores_out)
    print(
        {
            "scores_path": str(args.scores_out),
            "scores_sha256": _file_sha256(args.scores_out),
        }
    )


if __name__ == "__main__":
    main()
