"""Read-only A6000 feature-cost screen for the released SV-Detect pipeline.

SV-Detect does not publish trained steering vectors or its final logistic model.
This harness therefore does not claim an end-to-end detector result.  It measures
an optimized batched reconstruction of the feature mathematics: one frozen
GPT-Neo-2.7B forward, per-layer mean pooling, and cosine projection.  Unlike the
release's one-text-at-a-time FP32 extraction to CPU, this screen uses FP16, four
texts per card, and projection in GPU hooks.  Fixed unit directions stand in for
the absent trained vectors without changing operation shapes.
"""

from __future__ import annotations

import csv
import platform
import statistics
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Any, Self

import torch
import torch.nn.functional as F
import transformers
from torch.utils.hooks import RemovableHandle
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.modeling_utils import PreTrainedModel
from transformers.tokenization_utils_base import BatchEncoding, PreTrainedTokenizerBase


REPO_ROOT = Path(__file__).resolve().parents[3]
TRIAL_DATA = REPO_ROOT / "data/classify/cc10k/fdgpt_trial_all_df1"
MODEL_REVISION = "e24fa291132763e59f4a5422741b424fb5d59056"
MODEL_PATH = (
    Path.home()
    / ".cache/huggingface/hub/models--EleutherAI--gpt-neo-2.7B/snapshots"
    / MODEL_REVISION
)
MODEL_WEIGHTS_SHA256 = (
    "ac75c6bf3e242ed5df22c1d9eb4a5fa563d201c0beab16711bd3fbb7448b1699"
)
OFFICIAL_REPOSITORY_COMMIT = "a25469ba6a1fa2adcf644338db6fef712511da66"
BATCH_SIZE = 8
CONTEXT_WINDOW = 2_048
REPEATS = 3
DW1_BINOCULARS_MEDIAN_BATCH_SECONDS = 7.732507459819317


@dataclass(frozen=True)
class Timing:
    method: str
    total_batch_size: int
    sequence_lengths: tuple[int, ...]
    seconds_per_batch: tuple[float, ...]
    median_seconds_per_batch: float
    median_seconds_per_document: float
    peak_allocated_mib_by_gpu: tuple[float, ...]
    ratio_to_dw1_binoculars_batch: float


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


def _load_model(device: torch.device) -> PreTrainedModel:
    if not (MODEL_PATH / "model.safetensors").is_file():
        raise SystemExit(locals())
    model: PreTrainedModel = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        dtype=torch.float16,
        device_map=str(device),
        local_files_only=True,
    )
    model.eval()
    return model


def _load_tokenizer() -> PreTrainedTokenizerBase:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    return tokenizer


def _decoder_blocks(model: PreTrainedModel) -> list[torch.nn.Module]:
    transformer = getattr(model, "transformer", None)
    blocks = getattr(transformer, "h", None)
    if blocks is None:
        raise SystemExit(locals())
    return list(blocks)


def _tokenize(
    tokenizer: PreTrainedTokenizerBase,
    texts: list[str],
    device: torch.device,
) -> BatchEncoding:
    return tokenizer(
        texts,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=CONTEXT_WINDOW,
        return_token_type_ids=False,
    ).to(device)


class ProjectionRecorder:
    """Batched form of the official release's per-block forward hooks."""

    def __init__(self, blocks: list[torch.nn.Module], hidden_size: int) -> None:
        self.blocks = blocks
        self.directions = tuple(
            F.normalize(
                torch.ones(
                    hidden_size,
                    dtype=torch.float32,
                    device=next(block.parameters()).device,
                ),
                dim=0,
            )
            for block in blocks
        )
        self.handles: list[RemovableHandle] = []
        self.projections: list[torch.Tensor | None] = [None] * len(blocks)

    def __enter__(self) -> Self:
        self.projections = [None] * len(self.blocks)

        def make_hook(index: int) -> Any:
            def hook(
                _module: torch.nn.Module,
                _inputs: tuple[Any, ...],
                output: Any,
            ) -> None:
                hidden = output[0] if isinstance(output, tuple) else output
                pooled = hidden.mean(dim=1).float()
                self.projections[index] = F.cosine_similarity(
                    pooled,
                    self.directions[index].unsqueeze(0),
                    dim=-1,
                )

            return hook

        self.handles = [
            block.register_forward_hook(make_hook(index))
            for index, block in enumerate(self.blocks)
        ]
        return self

    def __exit__(
        self,
        _exception_type: type[BaseException] | None,
        _exception: BaseException | None,
        _traceback: TracebackType | None,
    ) -> None:
        for handle in self.handles:
            handle.remove()
        self.handles = []

    def scores(self) -> list[float]:
        if any(value is None for value in self.projections):
            raise SystemExit(locals())
        projections = torch.stack(
            [value for value in self.projections if value is not None],
            dim=-1,
        )
        return projections.mean(dim=-1).cpu().tolist()


@torch.inference_mode()
def _feature_scores(
    model: PreTrainedModel,
    blocks: list[torch.nn.Module],
    encoding: BatchEncoding,
) -> list[float]:
    recorder = ProjectionRecorder(blocks, int(model.config.hidden_size))
    with recorder:
        output = model(
            input_ids=encoding.input_ids,
            attention_mask=encoding.attention_mask,
            use_cache=False,
        )
        del output
    return recorder.scores()


def _score_concurrent(
    first_model: PreTrainedModel,
    second_model: PreTrainedModel,
    first_blocks: list[torch.nn.Module],
    second_blocks: list[torch.nn.Module],
    first_encoding: BatchEncoding,
    second_encoding: BatchEncoding,
) -> list[float]:
    with ThreadPoolExecutor(max_workers=2) as executor:
        first_future = executor.submit(
            _feature_scores,
            first_model,
            first_blocks,
            first_encoding,
        )
        second_future = executor.submit(
            _feature_scores,
            second_model,
            second_blocks,
            second_encoding,
        )
        return first_future.result() + second_future.result()


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
    operation: Any,
    sequence_lengths: tuple[int, ...],
) -> Timing:
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
        if len(scores) != len(sequence_lengths):
            raise SystemExit(locals())
    median = statistics.median(elapsed)
    return Timing(
        method=method,
        total_batch_size=len(sequence_lengths),
        sequence_lengths=sequence_lengths,
        seconds_per_batch=tuple(elapsed),
        median_seconds_per_batch=median,
        median_seconds_per_document=median / len(sequence_lengths),
        peak_allocated_mib_by_gpu=tuple(max(values) for values in zip(*peaks)),
        ratio_to_dw1_binoculars_batch=(median / DW1_BINOCULARS_MEDIAN_BATCH_SECONDS),
    )


def main() -> None:
    if torch.cuda.device_count() != 2:
        raise SystemExit(locals())
    texts, paths = _read_longest_documents()
    tokenizer = _load_tokenizer()
    first_device = torch.device("cuda:0")
    second_device = torch.device("cuda:1")
    first_model = _load_model(first_device)
    second_model = _load_model(second_device)
    first_blocks = _decoder_blocks(first_model)
    second_blocks = _decoder_blocks(second_model)

    single_encoding = _tokenize(tokenizer, texts[:1], first_device)
    midpoint = BATCH_SIZE // 2
    first_encoding = _tokenize(tokenizer, texts[:midpoint], first_device)
    second_encoding = _tokenize(tokenizer, texts[midpoint:], second_device)
    sequence_lengths = tuple(
        int(value)
        for value in torch.cat(
            (
                first_encoding.attention_mask.sum(dim=1).cpu(),
                second_encoding.attention_mask.sum(dim=1).cpu(),
            )
        )
    )
    if sequence_lengths != (CONTEXT_WINDOW,) * BATCH_SIZE:
        raise SystemExit(locals())

    print(
        {
            "artifact": "Atmyre/sv-detect",
            "artifact_commit": OFFICIAL_REPOSITORY_COMMIT,
            "model": "EleutherAI/gpt-neo-2.7B",
            "model_revision": MODEL_REVISION,
            "model_weights_sha256": MODEL_WEIGHTS_SHA256,
            "dtype": str(first_model.dtype),
            "python": platform.python_version(),
            "torch": torch.__version__,
            "torch_cuda_build": torch.version.cuda,
            "transformers": transformers.__version__,
            "nvidia_smi_gpus": _nvidia_smi_environment(),
            "documents": paths,
            "released_detector_state": False,
            "timed_operations": (
                "one frozen model forward, per-layer mean pooling, cosine projection, "
                "and CPU scores"
            ),
        }
    )
    print(
        _measure(
            "SV-Detect feature path, one A6000",
            lambda: _feature_scores(first_model, first_blocks, single_encoding),
            (CONTEXT_WINDOW,),
        )
    )
    print(
        _measure(
            "SV-Detect feature path, two-A6000 data parallel",
            lambda: _score_concurrent(
                first_model,
                second_model,
                first_blocks,
                second_blocks,
                first_encoding,
                second_encoding,
            ),
            sequence_lengths,
        )
    )


if __name__ == "__main__":
    main()
