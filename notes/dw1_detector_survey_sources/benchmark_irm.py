"""Read-only A6000 feasibility screen for the released IRM detector.

The NeurIPS 2025 supplemental artifact evaluates Implicit Reward Model (IRM)
detection by subtracting a base model's sequence log likelihood from its
instruction-tuned counterpart's sequence log likelihood.  This harness applies
that exact score to the strongest model family in the paper that can be
downloaded anonymously: Qwen2-0.5B.  It does not modify DW1 data or settings.
"""

from __future__ import annotations

import csv
import hashlib
import platform
import random
import statistics
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

import torch
import torch.nn.functional as F
import transformers
from sklearn.metrics import roc_auc_score
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.modeling_utils import PreTrainedModel
from transformers.tokenization_utils_base import BatchEncoding, PreTrainedTokenizerBase


REPO_ROOT = Path(__file__).resolve().parents[3]
TRIAL_DATA = REPO_ROOT / "data/classify/cc10k/fdgpt_trial_all_df1"
MODEL_CACHE = Path.home() / ".cache/huggingface/hub"
BASE_REVISION = "91d2aff3f957f99e4c74c962f2f408dcc88a18d8"
INSTRUCTION_REVISION = "c540970f9e29518b1d8f06ab8b24cba66ad77b6d"
BASE_PATH = MODEL_CACHE / "models--Qwen--Qwen2-0.5B" / "snapshots" / BASE_REVISION
INSTRUCTION_PATH = (
    MODEL_CACHE
    / "models--Qwen--Qwen2-0.5B-Instruct"
    / "snapshots"
    / INSTRUCTION_REVISION
)
BASE_WEIGHTS_SHA256 = "9cd8fc8c85a197b8c551d6b931b5709fe2611889d6b44945876472fecdf77cad"
INSTRUCTION_WEIGHTS_SHA256 = (
    "130282af0dfa9fe5840737cc49a0d339d06075f83c5a315c3372c9a0740d0b96"
)
SUPPLEMENTAL_ZIP_SHA256 = (
    "831062de6a10566594c072f43ea8b770dfdf73d1b1193dc32c3a4c76fb56c8fa"
)
BATCH_SIZE = 8
CONTEXT_WINDOW = 2_048
REPEATS = 3
EVALUATION_SAMPLES_PER_CLASS = 500
SEED = 42
DW1_BINOCULARS_MEDIAN_BATCH_SECONDS = 7.732507459819317


@dataclass(frozen=True)
class TrialRecord:
    path: str
    n_tokens: int
    is_generated: int
    binoculars: float
    fast_detect_gpt: float


@dataclass(frozen=True)
class Timing:
    method: str
    batch_size: int
    sequence_lengths: tuple[int, ...]
    seconds_per_batch: tuple[float, ...]
    median_seconds_per_batch: float
    median_seconds_per_document: float
    peak_allocated_mib_by_gpu: tuple[float, ...]
    ratio_to_dw1_binoculars_batch: float


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
                )
            )
    return records


def _has_local_text(record: TrialRecord) -> bool:
    return (REPO_ROOT / record.path).is_file()


def _read_texts(records: list[TrialRecord]) -> list[str]:
    return [(REPO_ROOT / record.path).read_text(encoding="utf-8") for record in records]


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


def _load_model(path: Path, device: torch.device) -> PreTrainedModel:
    if not (path / "model.safetensors").is_file():
        raise SystemExit(locals())
    model: PreTrainedModel = AutoModelForCausalLM.from_pretrained(
        path,
        dtype=torch.float32,
        device_map=str(device),
        local_files_only=True,
    )
    model.eval()
    return model


def _load_tokenizer(path: Path) -> PreTrainedTokenizerBase:
    tokenizer = AutoTokenizer.from_pretrained(
        path,
        local_files_only=True,
    )
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    return tokenizer


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _record_manifest_sha256(records: list[TrialRecord]) -> str:
    digest = hashlib.sha256()
    for record in records:
        line = (
            f"{record.path}\t{record.n_tokens}\t{record.is_generated}\t"
            f"{record.binoculars!r}\t{record.fast_detect_gpt!r}\n"
        )
        digest.update(line.encode())
    return digest.hexdigest()


def _selected_text_sha256(records: list[TrialRecord]) -> str:
    digest = hashlib.sha256()
    for record in records:
        digest.update(record.path.encode())
        digest.update(b"\0")
        with (REPO_ROOT / record.path).open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


def _tokenize(
    tokenizer: PreTrainedTokenizerBase,
    texts: list[str],
    device: torch.device,
) -> BatchEncoding:
    return tokenizer(
        texts,
        return_tensors="pt",
        return_token_type_ids=False,
        padding=True,
        truncation=True,
        max_length=CONTEXT_WINDOW,
    ).to(device)


@torch.inference_mode()
def _sequence_log_likelihood(
    model: PreTrainedModel,
    encoding: BatchEncoding,
) -> torch.Tensor:
    logits = model(
        input_ids=encoding.input_ids,
        attention_mask=encoding.attention_mask,
        use_cache=False,
    ).logits[:, :-1]
    labels = encoding.input_ids[:, 1:]
    valid = encoding.attention_mask[:, 1:].bool()
    log_probs = F.log_softmax(logits, dim=-1)
    token_log_likelihood = log_probs.gather(
        dim=-1,
        index=labels.unsqueeze(-1),
    ).squeeze(-1)
    return (token_log_likelihood * valid).sum(dim=-1).float().cpu()


def _score_sequential(
    instruction_model: PreTrainedModel,
    base_model: PreTrainedModel,
    instruction_encoding: BatchEncoding,
    base_encoding: BatchEncoding,
) -> list[float]:
    instruction_likelihood = _sequence_log_likelihood(
        instruction_model,
        instruction_encoding,
    )
    base_likelihood = _sequence_log_likelihood(base_model, base_encoding)
    return (instruction_likelihood - base_likelihood).tolist()


def _score_concurrent(
    instruction_model: PreTrainedModel,
    base_model: PreTrainedModel,
    instruction_encoding: BatchEncoding,
    base_encoding: BatchEncoding,
) -> list[float]:
    with ThreadPoolExecutor(max_workers=2) as executor:
        instruction_future = executor.submit(
            _sequence_log_likelihood,
            instruction_model,
            instruction_encoding,
        )
        base_future = executor.submit(
            _sequence_log_likelihood,
            base_model,
            base_encoding,
        )
        instruction_likelihood = instruction_future.result()
        base_likelihood = base_future.result()
    return (instruction_likelihood - base_likelihood).tolist()


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


def _measure(
    method: str,
    instruction_model: PreTrainedModel,
    base_model: PreTrainedModel,
    instruction_encoding: BatchEncoding,
    base_encoding: BatchEncoding,
    *,
    concurrent: bool,
) -> Timing:
    operation = _score_concurrent if concurrent else _score_sequential
    operation(
        instruction_model,
        base_model,
        instruction_encoding,
        base_encoding,
    )
    _synchronize()
    elapsed: list[float] = []
    peaks: list[tuple[float, ...]] = []
    for _ in range(REPEATS):
        _reset_peak_memory()
        started = time.perf_counter()
        scores = operation(
            instruction_model,
            base_model,
            instruction_encoding,
            base_encoding,
        )
        _synchronize()
        elapsed.append(time.perf_counter() - started)
        peaks.append(_peak_memory_mib())
        if len(scores) != len(instruction_encoding.input_ids):
            raise SystemExit(locals())
    median = statistics.median(elapsed)
    batch_size = len(instruction_encoding.input_ids)
    lengths = tuple(int(value) for value in instruction_encoding.attention_mask.sum(1))
    return Timing(
        method=method,
        batch_size=batch_size,
        sequence_lengths=lengths,
        seconds_per_batch=tuple(elapsed),
        median_seconds_per_batch=median,
        median_seconds_per_document=median / batch_size,
        peak_allocated_mib_by_gpu=tuple(max(values) for values in zip(*peaks)),
        ratio_to_dw1_binoculars_batch=(median / DW1_BINOCULARS_MEDIAN_BATCH_SECONDS),
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
    records: list[TrialRecord],
    instruction_tokenizer: PreTrainedTokenizerBase,
    base_tokenizer: PreTrainedTokenizerBase,
    instruction_model: PreTrainedModel,
    base_model: PreTrainedModel,
) -> None:
    labels = [record.is_generated for record in records]
    irm_scores: list[float] = []
    started = time.perf_counter()
    for start in range(0, len(records), BATCH_SIZE):
        batch = records[start : start + BATCH_SIZE]
        texts = _read_texts(batch)
        instruction_encoding = _tokenize(
            instruction_tokenizer,
            texts,
            torch.device("cuda:0"),
        )
        base_encoding = _tokenize(base_tokenizer, texts, torch.device("cuda:1"))
        if not torch.equal(
            instruction_encoding.input_ids.cpu(),
            base_encoding.input_ids.cpu(),
        ) or not torch.equal(
            instruction_encoding.attention_mask.cpu(),
            base_encoding.attention_mask.cpu(),
        ):
            raise SystemExit(locals())
        irm_scores.extend(
            _score_concurrent(
                instruction_model,
                base_model,
                instruction_encoding,
                base_encoding,
            )
        )
    _synchronize()
    elapsed = time.perf_counter() - started
    print(
        {
            "evaluation_n": len(records),
            "human_n": labels.count(0),
            "generated_n": labels.count(1),
            "selection_seed": SEED,
            "max_length": CONTEXT_WINDOW,
            "batch_size": BATCH_SIZE,
            "elapsed_seconds_including_text_reads_and_tokenization": elapsed,
            "seconds_per_document": elapsed / len(records),
            "irm_raw_auc": float(roc_auc_score(labels, irm_scores)),
            "irm_orientation_free_auc": _orientation_free_auc(labels, irm_scores),
            "binoculars_orientation_free_auc": _orientation_free_auc(
                labels,
                [-record.binoculars for record in records],
            ),
            "fast_detect_gpt_orientation_free_auc": _orientation_free_auc(
                labels,
                [record.fast_detect_gpt for record in records],
            ),
        }
    )


def main() -> None:
    if torch.cuda.device_count() != 2:
        raise SystemExit(locals())
    all_records = _read_records()
    available_records = [record for record in all_records if _has_local_text(record)]
    if len(available_records) < EVALUATION_SAMPLES_PER_CLASS * 2:
        raise SystemExit(locals())
    longest = sorted(
        available_records,
        key=lambda record: record.n_tokens,
        reverse=True,
    )[:BATCH_SIZE]
    texts = _read_texts(longest)
    evaluation_records = _balanced_evaluation_records(available_records)

    instruction_device = torch.device("cuda:0")
    base_device = torch.device("cuda:1")
    instruction_tokenizer = _load_tokenizer(INSTRUCTION_PATH)
    base_tokenizer = _load_tokenizer(BASE_PATH)
    instruction_model = _load_model(INSTRUCTION_PATH, instruction_device)
    base_model = _load_model(BASE_PATH, base_device)
    instruction_encoding = _tokenize(
        instruction_tokenizer,
        texts,
        instruction_device,
    )
    base_encoding = _tokenize(base_tokenizer, texts, base_device)
    single_instruction_encoding = _tokenize(
        instruction_tokenizer,
        texts[:1],
        instruction_device,
    )
    single_base_encoding = _tokenize(base_tokenizer, texts[:1], base_device)
    if not torch.equal(
        instruction_encoding.input_ids.cpu(), base_encoding.input_ids.cpu()
    ) or not torch.equal(
        instruction_encoding.attention_mask.cpu(),
        base_encoding.attention_mask.cpu(),
    ):
        raise SystemExit(locals())

    print(
        {
            "artifact": "NeurIPS 2025 IRM supplemental",
            "artifact_sha256": SUPPLEMENTAL_ZIP_SHA256,
            "instruction_model": "Qwen/Qwen2-0.5B-Instruct",
            "instruction_revision": INSTRUCTION_REVISION,
            "instruction_weights_sha256": INSTRUCTION_WEIGHTS_SHA256,
            "base_model": "Qwen/Qwen2-0.5B",
            "base_revision": BASE_REVISION,
            "base_weights_sha256": BASE_WEIGHTS_SHA256,
            "dtype": str(instruction_model.dtype),
            "python": platform.python_version(),
            "torch": torch.__version__,
            "torch_cuda_build": torch.version.cuda,
            "transformers": transformers.__version__,
            "nvidia_smi_gpus": _nvidia_smi_environment(),
            "score_rows": len(all_records),
            "rows_with_local_text": len(available_records),
            "missing_text_rows": len(all_records) - len(available_records),
            "trial_csv_sha256": _file_sha256(TRIAL_DATA),
            "evaluation_manifest_sha256": _record_manifest_sha256(evaluation_records),
            "evaluation_text_sha256": _selected_text_sha256(evaluation_records),
            "documents": [record.path for record in longest],
        }
    )
    print(
        _measure(
            "IRM Qwen2-0.5B pair, sequential forwards",
            instruction_model,
            base_model,
            single_instruction_encoding,
            single_base_encoding,
            concurrent=False,
        )
    )
    print(
        _measure(
            "IRM Qwen2-0.5B pair, concurrent forwards",
            instruction_model,
            base_model,
            instruction_encoding,
            base_encoding,
            concurrent=True,
        )
    )
    _evaluate(
        evaluation_records,
        instruction_tokenizer,
        base_tokenizer,
        instruction_model,
        base_model,
    )


if __name__ == "__main__":
    main()
