"""Reproduce the public MELD v5 inference path on the DW1 A6000 host.

The paper-era checkpoint cannot be executed faithfully from anonymous public
artifacts because its linked code endpoint is unavailable. This harness therefore
loads only the immutable, self-contained v5 revision and keeps its results separate
from the paper's claims. It reads DW1 trial data without modifying it.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import platform
import random
import statistics
import subprocess
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import torch
import torch.nn as nn
import transformers
from pydantic import BaseModel, Field
from safetensors.torch import load_file
from sklearn.metrics import roc_auc_score
from transformers import AutoConfig, AutoModel, AutoTokenizer
from transformers.modeling_utils import PreTrainedModel
from transformers.tokenization_utils_base import PreTrainedTokenizerBase


REPO_ROOT = Path(__file__).resolve().parents[3]
TRIAL_DATA = REPO_ROOT / "data/classify/cc10k/fdgpt_trial_all_df1"
CURRENT_REVISION = "453acf594d48f8c55c3a38bde396f9178516d817"
PAPER_REVISION = "51f3ac2d4ce8de9f6f3a1eba9ca4276b077bb808"
CURRENT_WEIGHT_SHA256 = (
    "32b0fbf6a5bd2083b53d41db24dcd5b6756fa82c688b7396552da9fbcaf8bb91"
)
PAPER_WEIGHT_SHA256 = "b829b8f9482df9cbd5bc287baa484cceae0f5d0b9af77528fda42da12f06660e"
CONTEXT_WINDOW = 2_048
BATCH_SIZE = 8
REPEATS = 5
DIRECT_SCREEN_SAMPLES_PER_CLASS = 500
CALIBRATION_HUMAN_N = 1_000
DIRECT_SCREEN_SEED = 42
CALIBRATION_SEED = 20_260_808
MIN_WORDS = 100
DW1_BINOCULARS_MEDIAN_BATCH_SECONDS = 7.732507459819317
type TensorEncoding = dict[str, torch.Tensor]


class Thresholds(BaseModel):
    fpr_001: float = Field(alias="fpr_0.01")
    fpr_005: float = Field(alias="fpr_0.05")
    fpr_01: float = Field(alias="fpr_0.1")


class ScoreOffsets(BaseModel):
    overall: Thresholds
    n_human: int


class MeldConfig(BaseModel):
    model_type: str
    architecture: str
    version: str
    backbone_hidden_size: int
    style_rank: int
    n_human_anchors: int
    n_families: int
    n_ops: int
    rho: float
    tau_agg: float
    max_length: int
    score_offsets: ScoreOffsets
    released_step: int


@dataclass(frozen=True)
class TrialRecord:
    row_index: int
    path: str
    n_tokens: int
    is_generated: int
    binoculars: float
    fast_detect_gpt: float


@dataclass(frozen=True)
class ScoredRecord:
    record: TrialRecord
    word_count: int
    meld_token_count: int
    meld_probability: float
    meld_score: float


@dataclass(frozen=True)
class Timing:
    method: str
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


class Meld(nn.Module):
    """Exact v5 architecture published in the immutable model card."""

    def __init__(self, model_dir: Path, cfg: MeldConfig) -> None:
        super().__init__()
        self.cfg = cfg
        self.backbone: PreTrainedModel = AutoModel.from_config(
            AutoConfig.from_pretrained(model_dir, local_files_only=True),
            attn_implementation="sdpa",
        )
        self.style_proj = nn.Linear(
            cfg.backbone_hidden_size, cfg.style_rank, bias=False
        )
        self.style_ln = nn.LayerNorm(cfg.style_rank)
        self.human_anchors = nn.Parameter(
            torch.zeros(cfg.n_human_anchors, cfg.style_rank)
        )
        self.family_protos = nn.Parameter(torch.zeros(cfg.n_families, cfg.style_rank))
        self.family_bias = nn.Parameter(torch.zeros(cfg.n_families))
        self.log_tau = nn.Parameter(torch.zeros(()))
        self.op_protos = nn.Parameter(torch.zeros(cfg.n_ops, cfg.style_rank))
        self.op_bias = nn.Parameter(torch.zeros(cfg.n_ops))
        self.load_state_dict(load_file(model_dir / "model.safetensors"), strict=True)
        self.eval()

    @torch.inference_mode()
    def score_encoding(
        self, encoding: TensorEncoding
    ) -> tuple[list[float], list[float]]:
        valid = (
            encoding["attention_mask"].bool() & ~encoding["special_tokens_mask"].bool()
        )
        hidden = self.backbone(
            input_ids=encoding["input_ids"],
            attention_mask=encoding["attention_mask"],
        ).last_hidden_state.float()
        style = self.style_ln(self.style_proj(hidden))
        tau = self.log_tau.clamp(-4.0, 4.0).exp()

        def squared_distance(
            points: torch.Tensor, prototypes: torch.Tensor
        ) -> torch.Tensor:
            return (
                (points * points).sum(-1, keepdim=True)
                - 2.0 * points @ prototypes.t()
                + (prototypes * prototypes).sum(-1).view(1, 1, -1)
            )

        human = torch.logsumexp(
            -tau * squared_distance(style, self.human_anchors),
            -1,
            keepdim=True,
        )
        family = -tau * squared_distance(
            style, self.family_protos
        ) + self.family_bias.view(1, 1, -1)
        per_token = self.cfg.tau_agg * torch.logsumexp(
            (family - human).clamp(-30.0, 30.0) / self.cfg.tau_agg,
            dim=-1,
        )
        ordered = (
            per_token.masked_fill(
                ~valid,
                torch.finfo(per_token.dtype).min,
            )
            .sort(dim=1, descending=True)
            .values
        )
        n_keep = (valid.sum(1).clamp(min=1) * self.cfg.rho).ceil().clamp(min=1).long()
        keep = torch.arange(ordered.shape[1], device=ordered.device).unsqueeze(
            0
        ) < n_keep.unsqueeze(1)
        scores = (
            torch.where(keep, ordered, torch.zeros_like(ordered)).sum(1)
            / n_keep.float()
        )
        return torch.sigmoid(scores).cpu().tolist(), scores.cpu().tolist()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", required=True, type=Path)
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


def _load_cfg(model_dir: Path) -> MeldConfig:
    return MeldConfig.model_validate_json((model_dir / "meld_config.json").read_text())


def _load_model(model_dir: Path, cfg: MeldConfig, device: torch.device) -> Meld:
    model = Meld(model_dir, cfg).to(device)
    model.eval()
    return model


def _load_tokenizer(model_dir: Path) -> PreTrainedTokenizerBase:
    return AutoTokenizer.from_pretrained(model_dir, local_files_only=True)


def _tokenize(
    tokenizer: PreTrainedTokenizerBase,
    texts: list[str],
    device: torch.device,
) -> TensorEncoding:
    raw = tokenizer(
        texts,
        return_tensors="pt",
        return_token_type_ids=False,
        return_special_tokens_mask=True,
        padding=True,
        truncation=True,
        max_length=CONTEXT_WINDOW,
    )
    encoding: TensorEncoding = {}
    for key in ("input_ids", "attention_mask", "special_tokens_mask"):
        value = raw[key]
        if not isinstance(value, torch.Tensor):
            raise SystemExit(locals())
        encoding[key] = value.to(device)
    return encoding


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
    models: tuple[Meld, Meld],
    encodings: tuple[TensorEncoding, TensorEncoding],
) -> tuple[list[float], list[float]]:
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(model.score_encoding, encoding)
            for model, encoding in zip(models, encodings, strict=True)
        ]
        results = [future.result() for future in futures]
    return results[0][0] + results[1][0], results[0][1] + results[1][1]


def _measure(
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


def _direct_screen_records(records: list[TrialRecord]) -> list[TrialRecord]:
    rng = random.Random(DIRECT_SCREEN_SEED)
    human = [record for record in records if record.is_generated == 0]
    generated = [record for record in records if record.is_generated == 1]
    selected = rng.sample(human, DIRECT_SCREEN_SAMPLES_PER_CLASS)
    selected.extend(rng.sample(generated, DIRECT_SCREEN_SAMPLES_PER_CLASS))
    rng.shuffle(selected)
    return selected


def _manifest_sha256(records: list[TrialRecord]) -> str:
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


def _text_sha256(records: list[TrialRecord]) -> str:
    digest = hashlib.sha256()
    for record in records:
        digest.update(record.path.encode())
        digest.update(b"\0")
        with (REPO_ROOT / record.path).open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


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
    calibration_fpr = sum(score > threshold for score in calibration_scores) / len(
        calibration_scores
    )
    evaluation_fpr = sum(score > threshold for score in evaluation_human_scores) / len(
        evaluation_human_scores
    )
    evaluation_tpr = sum(
        score > threshold for score in evaluation_generated_scores
    ) / len(evaluation_generated_scores)
    return OperatingPoint(
        method=method,
        target_calibration_fpr=target_fpr,
        threshold=threshold,
        calibration_fpr=calibration_fpr,
        evaluation_human_n=len(evaluation_human_scores),
        evaluation_generated_n=len(evaluation_generated_scores),
        evaluation_fpr=evaluation_fpr,
        evaluation_tpr=evaluation_tpr,
    )


def _auc(labels: list[int], scores: list[float]) -> float:
    return float(roc_auc_score(labels, scores))


def _evaluate_all(
    records: list[TrialRecord],
    tokenizer: PreTrainedTokenizerBase,
    models: tuple[Meld, Meld],
) -> list[ScoredRecord]:
    scored: list[ScoredRecord] = []
    started = time.perf_counter()
    for start in range(0, len(records), BATCH_SIZE):
        batch = records[start : start + BATCH_SIZE]
        texts = [_read_text(record) for record in batch]
        midpoint = max(1, len(batch) // 2)
        first_texts, second_texts = texts[:midpoint], texts[midpoint:]
        first_encoding = _tokenize(tokenizer, first_texts, torch.device("cuda:0"))
        if second_texts:
            second_encoding = _tokenize(tokenizer, second_texts, torch.device("cuda:1"))
            probabilities, scores = _score_concurrently(
                models,
                (first_encoding, second_encoding),
            )
            token_counts = first_encoding["attention_mask"].sum(1).cpu().tolist()
            token_counts.extend(second_encoding["attention_mask"].sum(1).cpu().tolist())
        else:
            probabilities, scores = models[0].score_encoding(first_encoding)
            token_counts = first_encoding["attention_mask"].sum(1).cpu().tolist()
        scored.extend(
            ScoredRecord(
                record=record,
                word_count=len(text.split()),
                meld_token_count=int(token_count),
                meld_probability=probability,
                meld_score=score,
            )
            for record, text, token_count, probability, score in zip(
                batch,
                texts,
                token_counts,
                probabilities,
                scores,
                strict=True,
            )
        )
    _synchronize()
    elapsed_s = time.perf_counter() - started
    print(
        {
            "evaluation_rows": len(records),
            "elapsed_seconds_including_text_reads_tokenization_and_transfer": elapsed_s,
            "seconds_per_document": elapsed_s / len(records),
        }
    )
    return scored


def _write_scores(
    scored: list[ScoredRecord],
    calibration_rows: set[int],
    output_path: Path,
) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(
            [
                "row_index",
                "path",
                "is_generated",
                "word_count",
                "meld_token_count",
                "split",
                "meld_probability",
                "meld_score",
                "binoculars_ai_score",
                "fast_detect_gpt_score",
            ]
        )
        for item in scored:
            split = "evaluation"
            if item.word_count < MIN_WORDS:
                split = "excluded_under_100_words"
            elif item.record.row_index in calibration_rows:
                split = "calibration_human"
            writer.writerow(
                [
                    item.record.row_index,
                    item.record.path,
                    item.record.is_generated,
                    item.word_count,
                    item.meld_token_count,
                    split,
                    repr(item.meld_probability),
                    repr(item.meld_score),
                    repr(-item.record.binoculars),
                    repr(item.record.fast_detect_gpt),
                ]
            )


def _report_accuracy(
    scored: list[ScoredRecord], cfg: MeldConfig, scores_out: Path
) -> None:
    by_index = {item.record.row_index: item for item in scored}
    direct_records = _direct_screen_records([item.record for item in scored])
    direct = [by_index[record.row_index] for record in direct_records]
    direct_labels = [item.record.is_generated for item in direct]
    print(
        {
            "direct_screen_n": len(direct),
            "direct_screen_seed": DIRECT_SCREEN_SEED,
            "direct_screen_manifest_sha256": _manifest_sha256(direct_records),
            "direct_screen_text_sha256": _text_sha256(direct_records),
            "direct_screen_under_100_words_n": sum(
                item.word_count < MIN_WORDS for item in direct
            ),
            "meld_auc": _auc(direct_labels, [item.meld_score for item in direct]),
            "binoculars_auc": _auc(
                direct_labels,
                [-item.record.binoculars for item in direct],
            ),
            "fast_detect_gpt_auc": _auc(
                direct_labels,
                [item.record.fast_detect_gpt for item in direct],
            ),
        }
    )

    eligible = [item for item in scored if item.word_count >= MIN_WORDS]
    eligible_human = [item for item in eligible if item.record.is_generated == 0]
    rng = random.Random(CALIBRATION_SEED)
    calibration = rng.sample(eligible_human, CALIBRATION_HUMAN_N)
    calibration_rows = {item.record.row_index for item in calibration}
    evaluation = [
        item for item in eligible if item.record.row_index not in calibration_rows
    ]
    evaluation_human = [item for item in evaluation if item.record.is_generated == 0]
    evaluation_generated = [
        item for item in evaluation if item.record.is_generated == 1
    ]
    labels = [item.record.is_generated for item in evaluation]
    methods: dict[str, Callable[[ScoredRecord], float]] = {
        "MELD v5 raw score": lambda item: item.meld_score,
        "stored DW1 Binoculars, sign-normalized": lambda item: -item.record.binoculars,
        "stored DW1 FastDetectGPT": lambda item: item.record.fast_detect_gpt,
    }
    print(
        {
            "eligible_min_words": MIN_WORDS,
            "eligible_n": len(eligible),
            "excluded_under_100_words_n": len(scored) - len(eligible),
            "calibration_seed": CALIBRATION_SEED,
            "calibration_human_n": len(calibration),
            "calibration_manifest_sha256": _manifest_sha256(
                [item.record for item in calibration]
            ),
            "evaluation_n": len(evaluation),
            "evaluation_human_n": len(evaluation_human),
            "evaluation_generated_n": len(evaluation_generated),
            "evaluation_manifest_sha256": _manifest_sha256(
                [item.record for item in evaluation]
            ),
            "evaluation_text_sha256": _text_sha256(
                [item.record for item in evaluation]
            ),
        }
    )
    for method, score_of in methods.items():
        print(
            {
                "method": method,
                "evaluation_auc": _auc(labels, [score_of(item) for item in evaluation]),
            }
        )
        for target_fpr in (0.01, 0.05):
            print(
                _operating_point(
                    method,
                    [score_of(item) for item in calibration],
                    [score_of(item) for item in evaluation_human],
                    [score_of(item) for item in evaluation_generated],
                    target_fpr,
                )
            )
    for name, threshold in (
        ("v5 shipped overall FPR 1% threshold", cfg.score_offsets.overall.fpr_001),
        ("v5 shipped overall FPR 5% threshold", cfg.score_offsets.overall.fpr_005),
    ):
        print(
            OperatingPoint(
                method=name,
                target_calibration_fpr=float("nan"),
                threshold=threshold,
                calibration_fpr=sum(item.meld_score > threshold for item in calibration)
                / len(calibration),
                evaluation_human_n=len(evaluation_human),
                evaluation_generated_n=len(evaluation_generated),
                evaluation_fpr=sum(
                    item.meld_score > threshold for item in evaluation_human
                )
                / len(evaluation_human),
                evaluation_tpr=sum(
                    item.meld_score > threshold for item in evaluation_generated
                )
                / len(evaluation_generated),
            )
        )
    _write_scores(scored, calibration_rows, scores_out)
    print({"scores_path": str(scores_out), "scores_sha256": _file_sha256(scores_out)})


def main() -> None:
    args = _parse_args()
    if torch.cuda.device_count() != 2:
        raise SystemExit(locals())
    model_dir = args.artifact_root / "snapshots" / "meld" / CURRENT_REVISION
    paper_model_dir = args.artifact_root / "snapshots" / "meld" / PAPER_REVISION
    if _file_sha256(model_dir / "model.safetensors") != CURRENT_WEIGHT_SHA256:
        raise SystemExit(locals())
    if _file_sha256(paper_model_dir / "model.safetensors") != PAPER_WEIGHT_SHA256:
        raise SystemExit(locals())
    cfg = _load_cfg(model_dir)
    if cfg.max_length != CONTEXT_WINDOW:
        raise SystemExit(locals())
    tokenizer = _load_tokenizer(model_dir)
    models = (
        _load_model(model_dir, cfg, torch.device("cuda:0")),
        _load_model(model_dir, cfg, torch.device("cuda:1")),
    )
    records = _read_records()
    available = [record for record in records if _has_local_text(record)]
    longest = sorted(available, key=lambda record: record.n_tokens, reverse=True)[
        :BATCH_SIZE
    ]
    texts = [_read_text(record) for record in longest]
    one_encoding = _tokenize(tokenizer, texts[:1], torch.device("cuda:0"))
    batch_encoding = _tokenize(tokenizer, texts, torch.device("cuda:0"))
    first_encoding = _tokenize(tokenizer, texts[:4], torch.device("cuda:0"))
    second_encoding = _tokenize(tokenizer, texts[4:], torch.device("cuda:1"))
    sequence_lengths = tuple(
        int(value) for value in batch_encoding["attention_mask"].sum(1).tolist()
    )
    if sequence_lengths != (CONTEXT_WINDOW,) * BATCH_SIZE:
        raise SystemExit(locals())

    print(
        {
            "run_at": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(),
            "artifact": "MELD v5 immutable public Hugging Face revision",
            "current_revision": CURRENT_REVISION,
            "current_weight_sha256": CURRENT_WEIGHT_SHA256,
            "paper_revision_preserved_not_executed": PAPER_REVISION,
            "paper_weight_sha256": PAPER_WEIGHT_SHA256,
            "model_config_sha256": _file_sha256(model_dir / "meld_config.json"),
            "backbone_config_sha256": _file_sha256(model_dir / "config.json"),
            "tokenizer_sha256": _file_sha256(model_dir / "tokenizer.json"),
            "parameter_count": sum(
                parameter.numel() for parameter in models[0].parameters()
            ),
            "dtype": str(next(models[0].parameters()).dtype),
            "python": platform.python_version(),
            "torch": torch.__version__,
            "torch_cuda_build": torch.version.cuda,
            "transformers": transformers.__version__,
            "nvidia_smi_gpus": _nvidia_smi_environment(),
            "trial_rows": len(records),
            "rows_with_local_text": len(available),
            "trial_csv_sha256": _file_sha256(TRIAL_DATA),
            "longest_documents": [record.path for record in longest],
            "timing_boundary": "device-resident token tensors entered scoring and CPU scores left it",
            "timing_repetitions": REPEATS,
        }
    )
    print(
        _measure(
            "MELD v5, one GPU, batch 1",
            1,
            (int(one_encoding["attention_mask"].sum()),),
            lambda: models[0].score_encoding(one_encoding),
        )
    )
    print(
        _measure(
            "MELD v5, one GPU, batch 8",
            BATCH_SIZE,
            sequence_lengths,
            lambda: models[0].score_encoding(batch_encoding),
        )
    )
    print(
        _measure(
            "MELD v5, two replica GPUs, concurrent batch 4+4",
            BATCH_SIZE,
            sequence_lengths,
            lambda: _score_concurrently(models, (first_encoding, second_encoding)),
        )
    )
    scored = _evaluate_all(available, tokenizer, models)
    _report_accuracy(scored, cfg, args.scores_out)


if __name__ == "__main__":
    main()
