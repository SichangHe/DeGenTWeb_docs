#!/usr/bin/env python3
"""Replace heuristic predecessor witnesses with exact source-owned joins.

The raw table scanner remains independent of this module.  This layer starts
from its canonical 987-account witness output, proves the exact 225
``same_window`` and 95 generic ``table_configuration_join`` predecessor rows,
and replaces them with reviewed source/row/column/state bindings.  A direct
fine-tuned DeBERTa companion is included so training-state swaps are bilateral.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from collections import Counter
from dataclasses import dataclass, replace
from pathlib import Path

import discover_table_accounts as discovery


OWNERSHIP_FIELDS = (
    "parent_id",
    "account_id",
    "predecessor_witness_id",
    "predecessor_join_kind",
    "predecessor_join_key",
    "predecessor_metric_value",
    "predecessor_raw_candidate_id",
    "successor_join_kind",
    "evidence_kind",
    "method_state",
    "source_identity_label",
    "identity_page",
    "identity_line",
    "identity_locator",
    "identity_text",
    "metric_page",
    "metric_line",
    "metric_locator",
    "metric_text",
    "metric_name",
    "metric_column",
    "metric_column_index",
    "evaluation_scope",
    "metric_value",
    "raw_candidate_id",
    "evidence_source_kind",
    "evidence_source_path",
    "source_text_sha256",
    "evidence_span_sha256",
    "negative_kind",
    "header_page",
    "header_line",
    "header_locator",
    "header_text",
    "header_sha256",
    "negative_page",
    "negative_line",
    "negative_locator",
    "negative_text",
    "negative_value",
    "negative_reason",
)
EXPECTED_OWNERSHIP_ROWS = 321
EXPECTED_PREDECESSOR_COUNTS = {
    "same_window": 225,
    "table_configuration_join": 95,
    "direct_companion": 1,
}
EXPECTED_ACCOUNT_SET_SHA256 = (
    "e501508d1cb3aa1dddaaa472673a5ad53276396cf92527cfe8fbf26b9c9eb7eb"
)
EXPECTED_PREDECESSOR_BINDING_SHA256 = (
    "8e391693afcc5173ad70ca69698e4744c8ccef2a5e1b147a5497c3aea29af895"
)
EXPECTED_CELL_BINDING_SHA256 = (
    "44474a89a16c15a4d1750a362b31bc6daf2c69f39935d0442f33684e2746cc22"
)
TARGET_PREDECESSOR_KINDS = {"same_window", "table_configuration_join"}
SUCCESSOR_KINDS = {
    "source_owned_row_join",
    "source_owned_state_join",
    "source_owned_figure_join",
    "source_owned_artifact_state_join",
}
NEGATIVE_KINDS = {
    "wrong_row",
    "wrong_column",
    "wrong_training_state",
    "wrong_method_state",
}
COMPANION_ACCOUNT_ID = "2608.01046:deberta-finetuned"
LEGACY_PREDECESSOR_ACCOUNT = "2604.21223:qwen25-pair"
LEGACY_PREDECESSOR_SYSTEM = "IRM Qwen2.5 model pair"
LEGACY_PREDECESSOR_EVIDENCE = (
    "paper model-pair tables, Appendix Table 8, and frozen IRM screen; both pair "
    "families and the RM-DeBERTa comparator have a paper AUROC >=0.90 slice, "
    "while the best downloadable IRM pair measured 0.9436 versus Binoculars 0.9595"
)
NAMED_COUNTEREXAMPLES = {
    "2608.01046:tfidf-logreg": (
        "source_owned_figure_join",
        412,
        412,
        1,
        "93.6",
    ),
    "2608.01046:deberta-zeroshot": (
        "source_owned_state_join",
        447,
        447,
        4,
        "100.00",
    ),
    "2608.01046:deberta-finetuned": (
        "source_owned_state_join",
        448,
        448,
        2,
        "0.976",
    ),
    "2607.17382:modernbert-large": (
        "source_owned_state_join",
        366,
        368,
        2,
        "0.9329",
    ),
    "2607.17382:modernbert-large-mcgrad": (
        "source_owned_state_join",
        386,
        388,
        2,
        "0.9337",
    ),
}
REQUIRED_SOURCE_BINDINGS = {
    "2511.21744:cnn": (
        "source_owned_state_join",
        "prose_ordered_pair",
        20,
        23,
        1,
        "99.5",
        "cnn",
    ),
    "2511.21744:random-forest": (
        "source_owned_state_join",
        "prose_ordered_pair",
        20,
        23,
        2,
        "95",
        "randomforest",
    ),
    "2506.06705:without-adaptation": (
        "source_owned_figure_join",
        "figure_series",
        532,
        543,
        1,
        "92.63",
        "baseline DivScore without domain",
    ),
    "2507.23577:tdetect": (
        "source_owned_state_join",
        "prose_or_figure_claim",
        35,
        39,
        1,
        "0.926",
        "tdetect",
    ),
    "2509.14268:qwen2-0.5b": (
        "source_owned_row_join",
        "table_row",
        539,
        539,
        5,
        "0.8570",
        "Qwen2-0.5B [56]",
    ),
    "2509.14268:gpt-neo-2.7b": (
        "source_owned_row_join",
        "table_row",
        540,
        540,
        4,
        "0.7694",
        "GPT-Neo-2.7B [8]",
    ),
    "2509.14268:gpt-j-6b": (
        "source_owned_row_join",
        "table_row",
        541,
        541,
        6,
        "0.8367",
        "GPT-J-6B [51]",
    ),
    "2509.18880:falcon7b": (
        "source_owned_row_join",
        "table_row",
        1775,
        1775,
        2,
        "0.90",
        "Falcon-7B",
    ),
    "2509.18880:llama31-8b": (
        "source_owned_row_join",
        "table_row",
        1777,
        1777,
        3,
        "0.91",
        "Llama-3.1-8B",
    ),
    "2509.18880:mistral7b": (
        "source_owned_row_join",
        "table_row",
        1778,
        1778,
        3,
        "0.90",
        "Mistral-7B-v0.3",
    ),
    "2509.25154:jdetector-no-llm": (
        "source_owned_figure_join",
        "prose_or_figure_claim",
        433,
        433,
        2,
        "-2.7",
        "w/o LLM-enhanced Feature",
    ),
    "2509.25154:jdetector-no-linguistic": (
        "source_owned_figure_join",
        "prose_or_figure_claim",
        432,
        449,
        1,
        "5.3",
        "w/o Linguistic Feature",
    ),
    "2602.08031:detectgpt": (
        "source_owned_row_join",
        "table_row",
        2474,
        2474,
        5,
        "92.84",
        "AUROC DetectGPT",
    ),
    "2604.16923:lapd-llama2": (
        "source_owned_row_join",
        "table_row",
        518,
        518,
        3,
        "99.42",
        "Llama2-7B Pair",
    ),
    "2604.21223:qwen25-pair": (
        "source_owned_state_join",
        "table_row",
        477,
        481,
        2,
        "90.14",
        "Qwen2-0.5B",
    ),
    "2606.31074:binoculars": (
        "source_owned_row_join",
        "table_row",
        563,
        563,
        2,
        "0.916",
        "Binoculars (Hans et al., 2024)",
    ),
    "2606.31074:imbd": (
        "source_owned_row_join",
        "table_row",
        565,
        565,
        2,
        "0.962",
        "ImBD (Chen et al., 2025)",
    ),
    "2607.17382:modernbert-large": (
        "source_owned_state_join",
        "table_row",
        366,
        368,
        2,
        "0.9329",
        "modernbertlarge",
    ),
    "2607.17382:modernbert-large-mcgrad": (
        "source_owned_state_join",
        "table_row",
        386,
        388,
        2,
        "0.9337",
        "mcgrad",
    ),
    "2608.01046:tfidf-logreg": (
        "source_owned_figure_join",
        "figure_series",
        412,
        412,
        1,
        "93.6",
        "lines including TF-IDF + LogReg (",
    ),
    "2608.01046:deberta-zeroshot": (
        "source_owned_state_join",
        "table_row",
        447,
        447,
        4,
        "100.00",
        "DeBERTa-v3 (zero-shot)",
    ),
    "2608.01046:deberta-finetuned": (
        "source_owned_state_join",
        "table_row",
        448,
        448,
        2,
        "0.976",
        "DeBERTa-Sentinel (fine-tuned)",
    ),
}


@dataclass(frozen=True)
class Ownership:
    parent_id: str
    account_id: str
    predecessor_witness_id: str
    predecessor_join_kind: str
    predecessor_join_key: str
    predecessor_metric_value: str
    predecessor_raw_candidate_id: str
    successor_join_kind: str
    evidence_kind: str
    method_state: str
    source_identity_label: str
    identity_page: int
    identity_line: int
    identity_locator: str
    identity_text: str
    metric_page: int
    metric_line: int
    metric_locator: str
    metric_text: str
    metric_name: str
    metric_column: str
    metric_column_index: int
    evaluation_scope: str
    metric_value: str
    raw_candidate_id: str
    evidence_source_kind: str
    evidence_source_path: str
    source_text_sha256: str
    evidence_span_sha256: str
    negative_kind: str
    header_page: int
    header_line: int
    header_locator: str
    header_text: str
    header_sha256: str
    negative_page: int
    negative_line: int
    negative_locator: str
    negative_text: str
    negative_value: str
    negative_reason: str


def _digest(rows: list[Ownership], fields: tuple[str, ...]) -> str:
    payload = "".join(
        "\t".join(str(getattr(row, field)) for field in fields) + "\n"
        for row in sorted(rows, key=lambda item: item.account_id)
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def _validate_immutable_digests(rows: list[Ownership]) -> None:
    if (
        _digest(rows, ("account_id",)) != EXPECTED_ACCOUNT_SET_SHA256
        or _digest(
            rows,
            (
                "account_id",
                "predecessor_witness_id",
                "predecessor_join_kind",
                "predecessor_join_key",
                "predecessor_metric_value",
                "predecessor_raw_candidate_id",
            ),
        )
        != EXPECTED_PREDECESSOR_BINDING_SHA256
        or _digest(
            rows,
            (
                "account_id",
                "evidence_source_kind",
                "evidence_source_path",
                "identity_line",
                "metric_line",
                "metric_column_index",
                "metric_value",
            ),
        )
        != EXPECTED_CELL_BINDING_SHA256
    ):
        raise ValueError(
            "ownership ledger immutable account/predecessor/cell set changed"
        )


def load_ownership(path: Path) -> list[Ownership]:
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if tuple(reader.fieldnames or ()) != OWNERSHIP_FIELDS:
            raise ValueError("predecessor ownership ledger header mismatch")
        raw_rows = list(reader)
    integer_fields = {
        "identity_page",
        "identity_line",
        "metric_page",
        "metric_line",
        "metric_column_index",
        "header_page",
        "header_line",
        "negative_page",
        "negative_line",
    }
    rows = [
        Ownership(
            **{
                field: int(row[field]) if field in integer_fields else row[field]
                for field in OWNERSHIP_FIELDS
            }
        )
        for row in raw_rows
    ]
    if (
        len(rows) != EXPECTED_OWNERSHIP_ROWS
        or len({row.account_id for row in rows}) != EXPECTED_OWNERSHIP_ROWS
    ):
        raise ValueError("ownership ledger must contain 321 unique account rows")
    counts = Counter(row.predecessor_join_kind for row in rows)
    if counts != Counter(EXPECTED_PREDECESSOR_COUNTS):
        raise ValueError(f"ownership predecessor counts changed: {dict(counts)}")
    _validate_immutable_digests(rows)
    return rows


def _numeric_values(text: str) -> tuple[str, ...]:
    return tuple(
        match.group().strip().removesuffix("%")
        for match in discovery.NUMBER_PATTERN.finditer(text)
    )


def _normalized_positions(text: str) -> tuple[str, tuple[int, ...]]:
    chars: list[str] = []
    positions: list[int] = []
    for position, char in enumerate(text.casefold()):
        if char.isalnum():
            chars.append(char)
            positions.append(position)
    return "".join(chars), tuple(positions)


def _label_end(text: str, label: str) -> int | None:
    literal_offset = text.casefold().find(label.casefold())
    if literal_offset >= 0:
        return literal_offset + len(label)
    normalized_text, positions = _normalized_positions(text)
    normalized_label = discovery.identity_normalized(label)
    offset = normalized_text.find(normalized_label)
    if not normalized_label or offset < 0:
        return None
    return positions[offset + len(normalized_label) - 1] + 1


def _selected_number(row: Ownership) -> re.Match[str]:
    matches = tuple(discovery.NUMBER_PATTERN.finditer(row.metric_text))
    if not 1 <= row.metric_column_index <= len(matches):
        raise ValueError(f"ownership metric column absent: {row.account_id}")
    return matches[row.metric_column_index - 1]


def _inside_uncertainty_group(text: str, position: int) -> bool:
    for opening, closing in (("(", ")"), ("[", "]")):
        opening_index = text.rfind(opening, 0, position)
        if (
            opening_index > text.rfind(closing, 0, position)
            and text.find(closing, position) >= 0
            and not re.search(r"[A-Za-z=]", text[opening_index + 1 : position])
        ):
            return True
    return False


def _non_result_number(
    text: str,
    match: re.Match[str],
    label_end: int | None,
    *,
    reject_uncertainty_group: bool = True,
) -> bool:
    before = text[match.start() - 1 : match.start()]
    after = text[match.end() : match.end() + 1]
    before_two = text[match.start() - 2 : match.start() - 1]
    after_two = text[match.end() + 1 : match.end() + 2]
    value = float(match.group().strip().removesuffix("%"))
    return (
        (label_end is not None and match.start() < label_end)
        or abs(value) > 100
        or 1900 <= abs(value) <= 2100
        or before.isalpha()
        or after.isalpha()
        or (before == "-" and before_two.isalnum())
        or (after == "-" and after_two.isalnum())
        or before == "±"
        or (reject_uncertainty_group and _inside_uncertainty_group(text, match.start()))
        or (before == "." and before_two.isdigit())
        or (after == "." and after_two.isdigit())
        or (match.start() == 0 and value.is_integer() and 1 <= abs(value) < 50)
    )


def _expected_wrong_column_donor(row: Ownership) -> str:
    matches = tuple(discovery.NUMBER_PATTERN.finditer(row.metric_text))
    selected_index = row.metric_column_index - 1
    selected_value = float(row.metric_value)
    label_end = _label_end(row.metric_text, row.source_identity_label)
    candidates = []
    for index, match in enumerate(matches):
        value = match.group().strip().removesuffix("%")
        if (
            index == selected_index
            or discovery._same_number(value, row.metric_value)
            or _non_result_number(row.metric_text, match, label_end)
        ):
            continue
        same_scale = (abs(float(value)) <= 1) == (abs(selected_value) <= 1)
        candidates.append((not same_scale, abs(index - selected_index), index, value))
    if not candidates:
        raise ValueError(
            f"ownership row lacks a distinct result donor: {row.account_id}"
        )
    return min(candidates)[-1]


def _validate_negative_donor(row: Ownership) -> None:
    if row.negative_kind == "wrong_column":
        if row.negative_text != row.metric_text or not discovery._same_number(
            row.negative_value, _expected_wrong_column_donor(row)
        ):
            raise ValueError(
                f"ownership wrong-column donor is not the derived result cell: "
                f"{row.account_id}"
            )
        return
    if not any(
        discovery._same_number(
            match.group().strip().removesuffix("%"), row.negative_value
        )
        and not _non_result_number(
            row.negative_text,
            match,
            None,
            reject_uncertainty_group=False,
        )
        for match in discovery.NUMBER_PATTERN.finditer(row.negative_text)
    ):
        raise ValueError(f"ownership negative donor is not a result: {row.account_id}")


def _validate_required_binding(row: Ownership) -> None:
    expected = REQUIRED_SOURCE_BINDINGS.get(row.account_id)
    if expected is None:
        return
    actual = (
        row.successor_join_kind,
        row.evidence_kind,
        row.identity_line,
        row.metric_line,
        row.metric_column_index,
        row.metric_value,
        row.source_identity_label,
    )
    if actual != expected:
        raise ValueError(
            f"required source-owned row/column/state changed: {row.account_id}"
        )


def _validate_semantic_relation(row: Ownership, evidence_span: str) -> None:
    selected = _selected_number(row)
    if row.evidence_kind == "table_row":
        before = row.metric_text[max(0, selected.start() - 1) : selected.start()]
        after = row.metric_text[selected.end() : selected.end() + 1]
        before_two = row.metric_text[
            max(0, selected.start() - 2) : max(0, selected.start() - 1)
        ]
        after_two = row.metric_text[selected.end() + 1 : selected.end() + 2]
        selected_value = abs(float(selected.group().strip().removesuffix("%")))
        if before == "±":
            raise ValueError(
                f"ownership selected an uncertainty, not a result: {row.account_id}"
            )
        if (
            selected_value > 100
            or 1900 <= selected_value <= 2100
            or before.isalpha()
            or after.isalpha()
            or (before == "-" and before_two.isalnum())
            or (after == "-" and after_two.isalnum())
        ):
            raise ValueError(
                f"ownership selected a model-name numeral: {row.account_id}"
            )
    if row.successor_join_kind == "source_owned_row_join":
        label_end = _label_end(row.metric_text, row.source_identity_label)
        if label_end is None or selected.start() < label_end:
            raise ValueError(
                f"ownership result is not after its exact source row: {row.account_id}"
            )
    if row.evidence_kind in {
        "prose_or_figure_claim",
        "prose_ordered_pair",
        "figure_series",
    }:
        normalized_span = discovery.identity_normalized(
            f"{evidence_span} {row.header_text}"
        )
        metric_token = re.sub(r"[^a-z0-9]", "", row.metric_name.casefold())
        metric_tokens = {metric_token}
        if metric_token.startswith("f1"):
            metric_tokens = {"f1"}
        elif metric_token in {"auroc", "rocauc"}:
            metric_tokens = {"auc", "auroc", "rocauc"}
        elif metric_token.startswith("thresholdmetric"):
            metric_tokens = set()
        if metric_tokens and not any(
            token in normalized_span for token in metric_tokens
        ):
            raise ValueError(
                f"ownership claim lacks its declared metric: {row.account_id}"
            )
    _validate_required_binding(row)


def _record(
    records: list[tuple[int, int, int, str, list[str]]], line: int
) -> tuple[int, int, int, str, list[str]]:
    matches = [item for item in records if item[1] == line]
    if len(matches) != 1:
        raise ValueError(f"source line is not unique or is absent: {line}")
    return matches[0]


def _span(
    records: list[tuple[int, int, int, str, list[str]]], start: int, end: int
) -> str:
    return "\n".join(
        discovery.compact(item[3])
        for item in records
        if min(start, end) <= item[1] <= max(start, end)
    )


def _source_text(
    row: Ownership,
    source_by_parent: dict[str, discovery.Source],
    source_texts: dict[str, str],
    ownership_root: Path,
) -> str:
    if row.evidence_source_kind == "extracted_primary_pdf_text":
        source = source_by_parent[row.parent_id]
        if row.evidence_source_path != source.paper_path:
            raise ValueError(f"ownership PDF path mismatch: {row.account_id}")
        return source_texts[row.parent_id]
    if row.evidence_source_kind == "local_benchmark_artifact":
        relative = Path(row.evidence_source_path)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"unsafe ownership artifact path: {row.account_id}")
        return (ownership_root / relative).read_text(encoding="utf-8")
    raise ValueError(f"unknown ownership evidence source: {row.account_id}")


def _owned_witness(
    row: Ownership, account: discovery.Account
) -> discovery.AccountWitness:
    join_key = (
        f"source={row.evidence_source_kind}:{row.evidence_source_path};"
        f"identity_line={row.identity_line};metric_line={row.metric_line};"
        f"metric_column={row.metric_column_index};state="
        f"{discovery.identity_normalized(row.method_state)};"
        f"header_sha256={row.header_sha256};"
        f"evidence_span_sha256={row.evidence_span_sha256}"
    )
    return discovery._new_witness(
        account,
        row.successor_join_kind,
        join_key,
        row.identity_page,
        row.identity_line,
        row.identity_locator,
        row.identity_text,
        row.metric_page,
        row.metric_line,
        row.metric_locator,
        row.metric_text,
        row.metric_value,
        row.raw_candidate_id,
        row.source_text_sha256,
    )


def validate_ownership_sources(
    rows: list[Ownership],
    sources: list[discovery.Source],
    accounts: list[discovery.Account],
    candidates: list[discovery.Candidate],
    source_texts: dict[str, str],
    ownership_root: Path,
    *,
    check_immutable_digests: bool = True,
) -> None:
    if check_immutable_digests:
        _validate_immutable_digests(rows)
    source_by_parent = {item.parent_id: item for item in sources}
    account_by_id = {item.account_id: item for item in accounts}
    candidate_by_id = {item.candidate_id: item for item in candidates}
    cell_owners: dict[tuple[object, ...], str] = {}
    for row in rows:
        account = account_by_id.get(row.account_id)
        if account is None or account.parent_id != row.parent_id:
            raise ValueError(f"ownership account/parent mismatch: {row.account_id}")
        if row.method_state != account.system:
            raise ValueError(f"ownership method state mismatch: {row.account_id}")
        if row.successor_join_kind not in SUCCESSOR_KINDS:
            raise ValueError(f"unknown ownership successor kind: {row.account_id}")
        if row.negative_kind not in NEGATIVE_KINDS:
            raise ValueError(f"unknown ownership negative kind: {row.account_id}")
        if len(row.evaluation_scope) < 24 or len(row.negative_reason) < 40:
            raise ValueError(f"underspecified ownership adjudication: {row.account_id}")
        _validate_negative_donor(row)

        text = _source_text(row, source_by_parent, source_texts, ownership_root)
        if hashlib.sha256(text.encode()).hexdigest() != row.source_text_sha256:
            raise ValueError(f"ownership source hash mismatch: {row.account_id}")
        records = discovery._page_records(text)
        identity = _record(records, row.identity_line)
        metric = _record(records, row.metric_line)
        header = _record(records, row.header_line)
        negative = _record(records, row.negative_line)
        exact_records = (
            (identity, row.identity_page, row.identity_locator, row.identity_text),
            (metric, row.metric_page, row.metric_locator, row.metric_text),
            (header, row.header_page, row.header_locator, row.header_text),
            (negative, row.negative_page, row.negative_locator, row.negative_text),
        )
        for record, page, locator, recorded_text in exact_records:
            expected_locator = discovery._locator(record[4], record[2], "", "")
            if (
                record[0] != page
                or discovery.compact(record[3]) != recorded_text
                or expected_locator != locator
            ):
                raise ValueError(f"ownership source row detached: {row.account_id}")
        if hashlib.sha256(row.header_text.encode()).hexdigest() != row.header_sha256:
            raise ValueError(f"ownership header hash mismatch: {row.account_id}")
        evidence_span = _span(records, row.identity_line, row.metric_line)
        if (
            hashlib.sha256(evidence_span.encode()).hexdigest()
            != row.evidence_span_sha256
        ):
            raise ValueError(f"ownership evidence span mismatch: {row.account_id}")
        _validate_semantic_relation(row, evidence_span)

        metric_values = _numeric_values(row.metric_text)
        if not 1 <= row.metric_column_index <= len(metric_values):
            raise ValueError(f"ownership metric column absent: {row.account_id}")
        owned_value = metric_values[row.metric_column_index - 1]
        if not discovery._same_number(owned_value, row.metric_value):
            raise ValueError(f"ownership metric cell mismatch: {row.account_id}")
        if not row.metric_name or not row.metric_column:
            raise ValueError(f"ownership metric semantics absent: {row.account_id}")

        combined = f"{row.identity_text} {row.metric_text}"
        if len(
            discovery.identity_normalized(row.source_identity_label)
        ) < 2 or discovery.identity_normalized(
            row.source_identity_label
        ) not in discovery.identity_normalized(combined):
            raise ValueError(f"ownership source identity absent: {row.account_id}")

        cell_key = (
            row.evidence_source_kind,
            row.evidence_source_path,
            row.identity_line,
            row.metric_line,
            row.metric_column_index,
        )
        if previous := cell_owners.get(cell_key):
            raise ValueError(
                f"ownership cell shared by {previous} and {row.account_id}"
            )
        cell_owners[cell_key] = row.account_id

        negative_values = _numeric_values(row.negative_text)
        if not any(
            discovery._same_number(row.negative_value, value)
            for value in negative_values
        ):
            raise ValueError(f"ownership negative value absent: {row.account_id}")
        if discovery._same_number(row.negative_value, row.metric_value):
            raise ValueError(
                f"ownership negative duplicates owned value: {row.account_id}"
            )
        if row.negative_kind == "wrong_column" and (
            row.negative_page != row.metric_page or row.negative_line != row.metric_line
        ):
            raise ValueError(f"wrong-column donor changed row: {row.account_id}")
        if row.negative_kind == "wrong_row" and (row.negative_line == row.metric_line):
            raise ValueError(f"wrong-row donor kept owned row: {row.account_id}")
        if row.raw_candidate_id:
            candidate = candidate_by_id.get(row.raw_candidate_id)
            if (
                candidate is None
                or candidate.parent_id != row.parent_id
                or candidate.page != row.metric_page
                or candidate.line != row.metric_line
                or (
                    discovery.normalized(row.metric_text)
                    not in discovery.normalized(candidate.context)
                    and discovery.normalized(candidate.context)
                    not in discovery.normalized(row.metric_text)
                )
            ):
                raise ValueError(f"ownership raw candidate detached: {row.account_id}")

    by_id = {row.account_id: row for row in rows}
    for account_id, expected in NAMED_COUNTEREXAMPLES.items():
        row = by_id[account_id]
        actual = (
            row.successor_join_kind,
            row.identity_line,
            row.metric_line,
            row.metric_column_index,
            row.metric_value,
        )
        if actual != expected or row.negative_kind != "wrong_training_state":
            raise ValueError(f"named ownership counterexample regressed: {account_id}")


def validate_owned_witnesses(
    witnesses: list[discovery.AccountWitness],
    predecessors: list[discovery.AccountWitness],
    ownership: list[Ownership],
    sources: list[discovery.Source],
    accounts: list[discovery.Account],
    candidates: list[discovery.Candidate],
    source_texts: dict[str, str],
    ownership_root: Path,
) -> None:
    validate_ownership_sources(
        ownership, sources, accounts, candidates, source_texts, ownership_root
    )
    account_by_id = {item.account_id: item for item in accounts}
    predecessor_by_id = {item.account_id: item for item in predecessors}
    witness_by_id = {item.account_id: item for item in witnesses}
    ownership_by_id = {item.account_id: item for item in ownership}
    if (
        len(predecessor_by_id) != len(accounts)
        or len(witness_by_id) != len(accounts)
        or set(predecessor_by_id) != set(account_by_id)
        or set(witness_by_id) != set(account_by_id)
    ):
        raise ValueError("owned witness ledgers must cover all 987 accounts exactly")

    actual_targets = {
        item.account_id
        for item in predecessors
        if item.join_kind in TARGET_PREDECESSOR_KINDS
    }
    expected_targets = set(ownership_by_id) - {COMPANION_ACCOUNT_ID}
    if actual_targets != expected_targets:
        raise ValueError("ownership target set differs from predecessor heuristics")
    actual_counts = Counter(
        item.join_kind
        for item in predecessors
        if item.join_kind in TARGET_PREDECESSOR_KINDS
    )
    if actual_counts != Counter({"same_window": 225, "table_configuration_join": 95}):
        raise ValueError(f"predecessor heuristic counts changed: {dict(actual_counts)}")

    for account_id, predecessor in predecessor_by_id.items():
        row = ownership_by_id.get(account_id)
        witness = witness_by_id[account_id]
        if row is None:
            if witness != predecessor:
                raise ValueError(f"non-target witness changed: {account_id}")
            continue
        expected_predecessor_kind = (
            predecessor.join_kind
            if account_id != COMPANION_ACCOUNT_ID
            else "direct_companion"
        )
        if (
            row.predecessor_witness_id != predecessor.witness_id
            or row.predecessor_join_kind != expected_predecessor_kind
            or row.predecessor_join_key != predecessor.join_key
            or not discovery._same_number(
                row.predecessor_metric_value, predecessor.metric_value
            )
            or row.predecessor_raw_candidate_id != predecessor.raw_candidate_id
        ):
            raise ValueError(f"ownership predecessor detached: {account_id}")
        expected = _owned_witness(row, account_by_id[account_id])
        if witness != expected:
            raise ValueError(f"owned witness differs from exact join: {account_id}")

    forbidden = [
        item.account_id
        for item in witnesses
        if item.join_kind in TARGET_PREDECESSOR_KINDS
    ]
    if forbidden:
        raise ValueError(
            "heuristic predecessor witnesses survived replacement: "
            + ",".join(forbidden)
        )


def build_owned_account_witnesses(
    sources: list[discovery.Source],
    paper_root: Path,
    accounts: list[discovery.Account],
    candidates: list[discovery.Candidate],
    resolutions: list[discovery.Resolution],
    ownership_path: Path,
    *,
    source_texts: dict[str, str] | None = None,
) -> tuple[
    list[discovery.AccountWitness],
    list[discovery.AccountWitness],
    list[Ownership],
    dict[str, str],
]:
    texts = source_texts or discovery.extract_source_texts(sources, paper_root)
    predecessor_accounts = [
        replace(
            item,
            system=LEGACY_PREDECESSOR_SYSTEM,
            qualifying_evidence=LEGACY_PREDECESSOR_EVIDENCE,
        )
        if item.account_id == LEGACY_PREDECESSOR_ACCOUNT
        else item
        for item in accounts
    ]
    predecessors = discovery.build_account_witnesses(
        sources,
        paper_root,
        predecessor_accounts,
        candidates,
        resolutions,
        source_texts=texts,
        run_validation=False,
    )
    ownership = load_ownership(ownership_path)
    ownership_by_id = {item.account_id: item for item in ownership}
    account_by_id = {item.account_id: item for item in accounts}
    witnesses = [
        _owned_witness(ownership_by_id[item.account_id], account_by_id[item.account_id])
        if item.account_id in ownership_by_id
        else item
        for item in predecessors
    ]
    validate_owned_witnesses(
        witnesses,
        predecessors,
        ownership,
        sources,
        accounts,
        candidates,
        texts,
        ownership_path.parent,
    )
    return witnesses, predecessors, ownership, texts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--paper-root", type=Path, required=True)
    parser.add_argument("--accounts", type=Path, required=True)
    parser.add_argument("--table-candidates", type=Path, required=True)
    parser.add_argument("--table-discovery", type=Path, required=True)
    parser.add_argument("--predecessor-ownership", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sources = discovery.load_sources(args.sources)
    accounts = discovery.load_accounts(args.accounts)
    candidates = discovery.load_candidates(args.table_candidates)
    resolutions = discovery.load_resolutions(args.table_discovery)
    discovery.validate_resolutions(candidates, resolutions, accounts)
    witnesses, predecessors, ownership, _ = build_owned_account_witnesses(
        sources,
        args.paper_root,
        accounts,
        candidates,
        resolutions,
        args.predecessor_ownership,
    )
    discovery.write_witnesses(args.output, witnesses)
    print(
        f"predecessor_witnesses={len(predecessors)} "
        f"ownership_replacements={len(ownership)} "
        f"final_witnesses={len(witnesses)}"
    )


if __name__ == "__main__":
    main()
