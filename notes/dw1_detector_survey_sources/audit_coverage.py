#!/usr/bin/env python3
"""Validate row and embedded-result coverage for frozen 2025–2026 exports."""

from __future__ import annotations

import argparse
import csv
import hashlib
import platform
import re
import sys
import xml.etree.ElementTree as ET
from collections.abc import Callable
from dataclasses import dataclass, replace
from pathlib import Path

ATOM_NS = "{http://www.w3.org/2005/Atom}"
EXPORT_NAMES = (
    "coverage_query_ai_generated.atom",
    "coverage_query_llm_generated.atom",
    "coverage_query_machine_generated.atom",
)
MAP_FIELDS = (
    "arxiv_id",
    "mapping_kind",
    "disposition_code",
    "flag_resolution",
    "reason",
    "source",
)
COMPOSITE_SOURCE_FIELDS = (
    "parent_id",
    "composite_kind",
    "resolution",
    "expected_result_count",
    "inspected_scope",
    "evidence_source",
    "reason",
)
EMBEDDED_RESULT_FIELDS = (
    "parent_id",
    "result_id",
    "system",
    "version",
    "claim",
    "metric_scope",
    "qualifying_basis",
    "primary_source",
    "artifact_status",
    "disposition_code",
    "disposition",
    "source_card",
)
EXPECTED_RESULT_FIELDS = ("parent_id", "result_id")
ALLOWED_FLAG_RESOLUTIONS = {"candidate_disposition", "false_positive", "not_flagged"}
ALLOWED_COMPOSITE_RESOLUTIONS = {
    "expanded_results",
    "no_qualifying_result",
    "parent_disposition_only",
}
COMPOSITE_DISPOSITION_CODES = {
    "attack_evaluation",
    "attack_study",
    "benchmark_study",
    "bias_evaluation",
    "dataset_only",
    "domain_augmentation",
    "evaluation_study",
    "evaluation_suite",
    "language_benchmark",
    "language_dataset",
    "language_shared_task",
    "shared_task_overview",
    "shared_task_system",
    "survey",
    "training_study",
}
COMPOSITE_TITLE_PATTERN = re.compile(
    r"\b(?:benchmark|shared[-\s]task|comparative|comparison|evaluating|evaluation|"
    r"findings|survey|systematic\s+(?:review|analysis)|case\s+study|dataset)\b",
    re.I,
)
RESULT_CODE_DEFINITIONS = {
    "commercial_closed": "closed service cannot supply a frozen public detector state",
    "exclude_multi_perturbation": "inference aggregates multiple target perturbations",
    "exclude_regeneration": "inference constructs a replacement sequence",
    "exclude_retrieval": "inference retrieves or looks up retained training/reference material",
    "exclude_rewriting": "inference rewrites or normalizes the target text",
    "existing_control": "already assessed public method retained only as a control",
    "parent_disposition": "the parent publication already gives the individual disposition",
    "primary_absent": "no separate public primary system paper or state was found",
    "reconstruction_only": "only a non-paper-state reconstruction can be built",
    "reject_scope": "result is restricted to a language, domain, task, or metric outside DW1",
    "released_watchlist": "public frozen detector merits a bounded screen but is not promoted",
    "retain_reject": "individually reviewed result fails one or more fixed evidence gates",
    "runnable_control": "public detector is runnable but fails the accuracy-first gate",
}
EXPECTED_RESULT_IDS_SHA256 = (
    "b7fbe5addd85685392ac7cd617ef9bfea6410bf7d5be2482057605ac5589cd8a"
)
SOURCE_CARDS_SHA256 = "1a240efcf1c8441eb94e5726716db4967cb8f074f910490923b6071076842387"
SOURCE_CARD_HEADING_PATTERN = re.compile(
    r"^## (?P<label>E\d+) — .+, arXiv (?P<parent>\d{4}\.\d{5})$"
)
SOURCE_CARD_MARKER_PATTERN = re.compile(
    r"^<!-- coverage-card (?P<label>E\d+) parent=(?P<parent>\d{4}\.\d{5}) "
    r"results=(?P<results>[^ ]+) -->$"
)
ANCHOR_RESULT_IDS = {
    "2501.08913": {
        "2501.08913:leidos-v1.0.3",
        "2501.08913:leidos-v1.0.2",
        "2501.08913:leidos-v1.0.4",
        "2501.08913:leidos-v1.0.1",
        "2501.08913:pangram",
        "2501.08913:ustc-bupt-r-l-focal-loss",
        "2501.08913:alert-v1.1",
        "2501.08913:cnlp-nits-distilbert",
        "2501.08913:alert-v1.2",
        "2501.08913:lux-rb-roai",
        "2501.08913:lux-roai-bert",
        "2501.08913:lux-finetuned-rb",
        "2501.08913:lux-radar-r-l",
        "2501.08913:cnlp-adv-submission-3",
        "2501.08913:cnlp-adv-new-detector",
        "2501.08913:ustc-roberta-dataaug",
        "2501.08913:binoculars",
        "2501.08913:mosaic-5",
        "2501.08913:gltr",
        "2501.08913:openai-roberta-large",
    },
    "2605.20761": {
        "2605.20761:sarang",
        "2605.20761:dakiet",
        "2605.20761:tesla",
        "2605.20761:skdu",
        "2605.20761:drocks",
        "2605.20761:llama-mamba",
        "2605.20761:ai-blues",
        "2605.20761:nlp-great",
    },
}
REQUIRED_SOURCE_CARDS = {
    "2501.08913": "Embedded source card E1",
    "2605.20761": "Embedded source card E2",
    "2605.15518": "Embedded source card E3",
    "2606.04906": "Embedded source card E4",
    "2604.11796": "Embedded source card E5",
    "2603.27949": "Embedded source card E6",
    "2603.18750": "Embedded source card E7",
    "2512.21709": "Embedded source card E8",
    "2512.09292": "Embedded source card E9",
    "2510.19492": "Embedded source card E10",
    "2510.16573": "Embedded source card E11",
    "2510.03502": "Embedded source card E12",
    "2509.26051": "Embedded source card E13",
    "2509.21269": "Embedded source card E14",
    "2507.15286": "Embedded source card E15",
    "2504.11369": "Embedded source card E16",
    "2503.15044": "Embedded source card E17",
    "2502.15654": "Embedded source card E18",
    "2502.12611": "Embedded source card E19",
    "2604.16607": "Embedded source card E20",
    "2510.12476": "Embedded source card E21",
    "2505.24523": "Embedded source card E22",
    "2501.11012": "Embedded source card E23",
    "2501.09813": "Embedded source card E24",
    "2603.23146": "Embedded source card E25",
    "2606.04177": "Embedded source card E26",
}
CODE_DEFINITIONS = {
    "explicit_disposition": {
        "advance_blocker": "actionable lead blocked by a named evidence or version gap",
        "calibration_watchlist": "calibration method retained without a qualifying detector state",
        "exclude_generation": "inference generates new content",
        "exclude_multi_perturbation": "inference aggregates multiple target perturbations",
        "exclude_perturbation": "inference transforms the target before classification",
        "exclude_regeneration": "inference constructs a replacement sequence",
        "exclude_retrieval": "inference retrieves a retained example or nearest neighbor",
        "exclude_rewriting": "inference rewrites the target text",
        "reconstruction_only": "released material permits only a non-paper-state reconstruction",
        "reject_scope": "individually reviewed result addresses a narrower task than DW1",
        "released_watchlist": "public detector retained pending fixed-screen evidence",
        "retain_reject": "individually reviewed detector fails one or more fixed gates",
        "runnable_control": "public detector retained as a non-qualifying control",
    },
    "non_candidate_class": {
        "analysis_only": "analysis or feature study without a proposed detector result",
        "attack_evaluation": "evaluation of detector vulnerability rather than a detector proposal",
        "attack_only": "attack contribution rather than a detector proposal",
        "attack_study": "attack-generation study rather than a detector proposal",
        "authorship_attribution": "author or generator attribution rather than binary detection",
        "benchmark_study": "benchmark contribution rather than a detector proposal",
        "bias_evaluation": "audit of existing detector bias rather than a detector proposal",
        "dataset_only": "dataset contribution rather than a detector proposal",
        "different_task": "classification target differs from human-versus-machine documents",
        "different_unit": "prediction unit differs from general document-level detection",
        "domain_augmentation": "detector is incidental to a training-data augmentation study",
        "domain_specific": "result is restricted to a specialist domain outside general DW1 use",
        "evaluation_study": "comparison of existing detectors rather than a detector proposal",
        "evaluation_suite": "evaluation framework rather than a detector proposal",
        "language_benchmark": "non-English benchmark rather than a general DW1 detector",
        "language_dataset": "non-English dataset contribution rather than a detector proposal",
        "language_shared_task": "non-English shared-task result outside general DW1 use",
        "language_specific": "non-English detector outside general DW1 use",
        "language_toolkit": "non-English analysis toolkit rather than a general DW1 detector",
        "no_threshold_evidence": "generic comparative wording without a high metric or strong claim",
        "shared_task_overview": "task inventory reporting other systems rather than a detector proposal",
        "shared_task_system": "general shared-task score below the 0.90 inclusion threshold",
        "survey": "secondary literature review rather than a detector proposal",
        "training_study": "detector is incidental to a model-training study",
    },
}
FLAG_PATTERNS = (
    ("sota", re.compile(r"\b(?:state[-\s]of[-\s]the[-\s]art|sota)\b", re.I)),
    (
        "best",
        re.compile(
            r"\b(?:best(?:[-\s](?:performing|performance))?|most\s+performant|"
            r"(?:first|1st)\s+(?:place|rank(?:ed)?)|top[-\s]rank(?:ed|ing)?)\b",
            re.I,
        ),
    ),
    (
        "comparative",
        re.compile(
            r"\b(?:outperform(?:s|ed|ing)?|surpass(?:es|ed|ing)?|"
            r"exceed(?:s|ed|ing)?|improv(?:e|es|ed|ing|ement|ements)|"
            r"superior|better than)\b",
            re.I,
        ),
    ),
    (
        "high_performance",
        re.compile(
            r"\b(?:high|strong|robust|competitive|remarkable|exceptional|optimal|"
            r"near(?:ly)?[-\s]perfect)\s+(?:accuracy|performance|results?|"
            r"precision|recall|f[\s_-]?1|f[-\s]?score|auc|auroc|detection)\b",
            re.I,
        ),
    ),
    (
        "accuracy_claim",
        re.compile(
            r"\b(?:accurate|highly[-\s]accurate)\s+"
            r"(?:detection|detector|classification)\b",
            re.I,
        ),
    ),
    (
        "metric",
        re.compile(
            r"\b(?:roc(?:[-\s]?auc)?|auroc|auc|accurac(?:y|ies)|f[\s_-]?1|"
            r"f[-\s]?score|precision|recall|tpr|fpr|true[-\s]positive(?: rate)?|"
            r"false[-\s]positive(?: rate)?|sensitivity|specificity)\b",
            re.I,
        ),
    ),
    (
        "high_percent",
        re.compile(
            r"(?<![\d.])(?:9\d(?:\.\d+)?|100(?:\.0+)?)\s*"
            r"(?:\\?%|percent(?:age)?)(?!\w)",
            re.I,
        ),
    ),
)


@dataclass(frozen=True)
class ExportRow:
    arxiv_id: str
    published: str
    title: str
    abstract: str
    exports: tuple[str, ...]


@dataclass(frozen=True)
class Mapping:
    arxiv_id: str
    mapping_kind: str
    disposition_code: str
    flag_resolution: str
    reason: str
    source: str


@dataclass(frozen=True)
class CompositeSource:
    parent_id: str
    composite_kind: str
    resolution: str
    expected_result_count: str
    inspected_scope: str
    evidence_source: str
    reason: str


@dataclass(frozen=True)
class EmbeddedResult:
    parent_id: str
    result_id: str
    system: str
    version: str
    claim: str
    metric_scope: str
    qualifying_basis: str
    primary_source: str
    artifact_status: str
    disposition_code: str
    disposition: str
    source_card: str


@dataclass(frozen=True)
class SourceCard:
    label: str
    parent_id: str
    result_ids: frozenset[str]


def compact(text: str) -> str:
    return " ".join(text.split())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def arxiv_id(entry_id: str) -> str:
    match = re.search(r"/(\d{4}\.\d{4,5})(?:v\d+)?$", entry_id)
    if match is None:
        raise ValueError(f"unrecognized arXiv entry id: {entry_id}")
    return match.group(1)


def load_exports(source_dir: Path) -> tuple[list[ExportRow], int]:
    by_id: dict[str, ExportRow] = {}
    raw_rows = 0
    for export_name in EXPORT_NAMES:
        root = ET.parse(source_dir / export_name).getroot()
        for entry in root.findall(f"{ATOM_NS}entry"):
            raw_rows += 1
            identifier = arxiv_id(entry.findtext(f"{ATOM_NS}id", default=""))
            published = entry.findtext(f"{ATOM_NS}published", default="")[:10]
            if not published.startswith(("2025-", "2026-")):
                continue
            title = compact(entry.findtext(f"{ATOM_NS}title", default=""))
            abstract = compact(entry.findtext(f"{ATOM_NS}summary", default=""))
            prior = by_id.get(identifier)
            if prior is None:
                by_id[identifier] = ExportRow(
                    arxiv_id=identifier,
                    published=published,
                    title=title,
                    abstract=abstract,
                    exports=(export_name,),
                )
                continue
            if (prior.published, prior.title, prior.abstract) != (
                published,
                title,
                abstract,
            ):
                raise ValueError(f"conflicting frozen metadata for {identifier}")
            by_id[identifier] = ExportRow(
                arxiv_id=identifier,
                published=published,
                title=title,
                abstract=abstract,
                exports=(*prior.exports, export_name),
            )
    return sorted(
        by_id.values(), key=lambda row: (row.published, row.arxiv_id), reverse=True
    ), raw_rows


def load_mappings(path: Path) -> dict[str, Mapping]:
    mappings: dict[str, Mapping] = {}
    with path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source, delimiter="\t")
        if reader.fieldnames != list(MAP_FIELDS):
            raise ValueError(f"mapping header must be: {' | '.join(MAP_FIELDS)}")
        for raw in reader:
            mapping = Mapping(**{field: raw[field].strip() for field in MAP_FIELDS})
            if mapping.arxiv_id in mappings:
                raise ValueError(f"duplicate mapping for {mapping.arxiv_id}")
            mappings[mapping.arxiv_id] = mapping
    return mappings


def load_composite_sources(path: Path) -> dict[str, CompositeSource]:
    sources: dict[str, CompositeSource] = {}
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if reader.fieldnames != list(COMPOSITE_SOURCE_FIELDS):
            raise ValueError(
                "composite-source header must be: "
                f"{' | '.join(COMPOSITE_SOURCE_FIELDS)}"
            )
        for raw in reader:
            item = CompositeSource(
                **{field: raw[field].strip() for field in COMPOSITE_SOURCE_FIELDS}
            )
            if item.parent_id in sources:
                raise ValueError(f"duplicate composite source for {item.parent_id}")
            sources[item.parent_id] = item
    return sources


def load_embedded_results(path: Path) -> list[EmbeddedResult]:
    results: list[EmbeddedResult] = []
    seen: set[str] = set()
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if reader.fieldnames != list(EMBEDDED_RESULT_FIELDS):
            raise ValueError(
                f"embedded-result header must be: {' | '.join(EMBEDDED_RESULT_FIELDS)}"
            )
        for raw in reader:
            item = EmbeddedResult(
                **{field: raw[field].strip() for field in EMBEDDED_RESULT_FIELDS}
            )
            if item.result_id in seen:
                raise ValueError(f"duplicate embedded result: {item.result_id}")
            seen.add(item.result_id)
            results.append(item)
    return results


def load_expected_result_ids(path: Path) -> dict[str, set[str]]:
    actual_hash = sha256(path)
    if actual_hash != EXPECTED_RESULT_IDS_SHA256:
        raise ValueError(
            "expected-result inventory hash mismatch: "
            f"expected {EXPECTED_RESULT_IDS_SHA256}, found {actual_hash}"
        )
    expected: dict[str, set[str]] = {}
    seen: set[str] = set()
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if reader.fieldnames != list(EXPECTED_RESULT_FIELDS):
            raise ValueError(
                f"expected-result header must be: {' | '.join(EXPECTED_RESULT_FIELDS)}"
            )
        for raw in reader:
            parent_id = raw["parent_id"].strip()
            result_id = raw["result_id"].strip()
            if not parent_id or not result_id:
                raise ValueError("blank expected-result inventory row")
            if result_id in seen:
                raise ValueError(f"duplicate expected result: {result_id}")
            if not result_id.startswith(f"{parent_id}:"):
                raise ValueError(f"expected result does not bind parent: {result_id}")
            seen.add(result_id)
            expected.setdefault(parent_id, set()).add(result_id)
    return expected


def load_source_cards(path: Path) -> dict[str, SourceCard]:
    actual_hash = sha256(path)
    if actual_hash != SOURCE_CARDS_SHA256:
        raise ValueError(
            "source-card file hash mismatch: "
            f"expected {SOURCE_CARDS_SHA256}, found {actual_hash}"
        )
    lines = path.read_text(encoding="utf-8").splitlines()
    cards: dict[str, SourceCard] = {}
    labels: set[str] = set()
    result_ids: set[str] = set()
    marker_indexes: set[int] = set()
    heading_indexes = [
        index
        for index, line in enumerate(lines)
        if SOURCE_CARD_HEADING_PATTERN.fullmatch(line)
    ]
    for position, heading_index in enumerate(heading_indexes):
        heading = SOURCE_CARD_HEADING_PATTERN.fullmatch(lines[heading_index])
        if heading is None:
            raise AssertionError("source-card heading selection drift")
        marker_index = heading_index + 2
        if marker_index >= len(lines) or lines[heading_index + 1] != "":
            raise ValueError(f"source-card marker missing after {heading['label']}")
        marker = SOURCE_CARD_MARKER_PATTERN.fullmatch(lines[marker_index])
        if marker is None:
            raise ValueError(f"invalid source-card marker for {heading['label']}")
        if (heading["label"], heading["parent"]) != (
            marker["label"],
            marker["parent"],
        ):
            raise ValueError(
                f"source-card heading/marker mismatch for {heading['label']}"
            )
        if heading["label"] in labels or heading["parent"] in cards:
            raise ValueError(f"duplicate source card for {heading['label']}")
        raw_result_ids = marker["results"].split(";")
        card_result_ids = frozenset(raw_result_ids)
        if len(card_result_ids) != len(raw_result_ids):
            raise ValueError(f"duplicate result ID in source card {heading['label']}")
        if any(
            not result_id.startswith(f"{heading['parent']}:")
            for result_id in card_result_ids
        ):
            raise ValueError(
                f"source-card result has wrong parent for {heading['label']}"
            )
        overlap = result_ids & card_result_ids
        if overlap:
            raise ValueError(
                "result IDs appear in multiple source cards: "
                f"{', '.join(sorted(overlap))}"
            )
        next_heading = (
            heading_indexes[position + 1]
            if position + 1 < len(heading_indexes)
            else len(lines)
        )
        if len(compact("\n".join(lines[marker_index + 1 : next_heading]))) < 150:
            raise ValueError(f"source-card evidence missing for {heading['label']}")
        label = f"Embedded source card {heading['label']}"
        cards[heading["parent"]] = SourceCard(
            label=label,
            parent_id=heading["parent"],
            result_ids=card_result_ids,
        )
        labels.add(heading["label"])
        result_ids.update(card_result_ids)
        marker_indexes.add(marker_index)
    stray_markers = [
        index
        for index, line in enumerate(lines)
        if SOURCE_CARD_MARKER_PATTERN.fullmatch(line) and index not in marker_indexes
    ]
    if stray_markers:
        raise ValueError("source-card marker lacks a matching heading")
    return cards


def is_composite_source(row: ExportRow, mapping: Mapping) -> bool:
    return bool(
        mapping.disposition_code in COMPOSITE_DISPOSITION_CODES
        or COMPOSITE_TITLE_PATTERN.search(row.title)
    )


def semantic_flags(row: ExportRow) -> tuple[tuple[str, ...], tuple[str, ...]]:
    text = f"{row.title}. {row.abstract}"
    flags: list[str] = []
    evidence: list[str] = []
    for name, pattern in FLAG_PATTERNS:
        match = pattern.search(text)
        if match is None:
            continue
        flags.append(name)
        start = max(0, match.start() - 70)
        end = min(len(text), match.end() + 110)
        evidence.append(compact(text[start:end]))
    return tuple(flags), tuple(evidence)


def validate(rows: list[ExportRow], mappings: dict[str, Mapping]) -> None:
    row_ids = {row.arxiv_id for row in rows}
    missing = sorted(row_ids - mappings.keys())
    unknown = sorted(mappings.keys() - row_ids)
    if missing:
        raise ValueError(f"missing mappings: {', '.join(missing)}")
    if unknown:
        raise ValueError(f"mapping rows absent from exports: {', '.join(unknown)}")
    for row in rows:
        mapping = mappings[row.arxiv_id]
        flags, _ = semantic_flags(row)
        if mapping.mapping_kind not in CODE_DEFINITIONS:
            raise ValueError(
                f"invalid mapping kind for {row.arxiv_id}: {mapping.mapping_kind}"
            )
        if mapping.disposition_code not in CODE_DEFINITIONS[mapping.mapping_kind]:
            raise ValueError(
                f"invalid {mapping.mapping_kind} code for {row.arxiv_id}: "
                f"{mapping.disposition_code}"
            )
        if mapping.flag_resolution not in ALLOWED_FLAG_RESOLUTIONS:
            raise ValueError(
                f"invalid flag resolution for {row.arxiv_id}: {mapping.flag_resolution}"
            )
        if not all((mapping.disposition_code, mapping.reason, mapping.source)):
            raise ValueError(f"incomplete mapping for {row.arxiv_id}")
        if mapping.source != f"https://arxiv.org/abs/{row.arxiv_id}":
            raise ValueError(
                f"mapping must cite its frozen primary row for {row.arxiv_id}"
            )
        if flags and mapping.flag_resolution == "not_flagged":
            raise ValueError(f"unresolved semantic flag for {row.arxiv_id}")
        if not flags and mapping.flag_resolution != "not_flagged":
            raise ValueError(
                f"flag resolution without a mechanical flag for {row.arxiv_id}"
            )
        if (
            mapping.mapping_kind == "non_candidate_class"
            and flags
            and mapping.flag_resolution != "false_positive"
        ):
            raise ValueError(
                f"flagged non-candidate lacks false-positive resolution for {row.arxiv_id}"
            )
        if (
            mapping.mapping_kind == "explicit_disposition"
            and flags
            and mapping.flag_resolution != "candidate_disposition"
        ):
            raise ValueError(
                f"flagged candidate lacks an individual disposition for {row.arxiv_id}"
            )


def _expected_count(source: CompositeSource) -> int:
    try:
        count = int(source.expected_result_count)
    except ValueError as error:
        raise ValueError(
            f"non-integer expected result count for {source.parent_id}"
        ) from error
    if count < 0:
        raise ValueError(f"negative expected result count for {source.parent_id}")
    return count


def _validate_source_shape(
    source: CompositeSource,
    results: list[EmbeddedResult],
    mapping: Mapping,
) -> None:
    if source.resolution not in ALLOWED_COMPOSITE_RESOLUTIONS:
        raise ValueError(
            f"invalid composite resolution for {source.parent_id}: {source.resolution}"
        )
    if not all(
        (
            source.composite_kind,
            source.inspected_scope,
            source.evidence_source,
            source.reason,
        )
    ):
        raise ValueError(f"incomplete composite source for {source.parent_id}")
    if len(source.inspected_scope) < 40 or len(source.reason) < 40:
        raise ValueError(f"underspecified composite review for {source.parent_id}")
    if source.evidence_source != f"https://arxiv.org/abs/{source.parent_id}":
        raise ValueError(
            f"composite source must cite its primary parent for {source.parent_id}"
        )
    expected = _expected_count(source)
    if len(results) != expected:
        raise ValueError(
            f"embedded-result count mismatch for {source.parent_id}: "
            f"expected {expected}, found {len(results)}"
        )
    if source.resolution == "expanded_results" and expected == 0:
        raise ValueError(f"empty expanded composite source for {source.parent_id}")
    if source.resolution != "expanded_results" and expected != 0:
        raise ValueError(
            f"non-expanded source has embedded results for {source.parent_id}"
        )
    if (
        source.resolution == "parent_disposition_only"
        and mapping.mapping_kind != "explicit_disposition"
    ):
        raise ValueError(
            f"parent-only resolution lacks explicit disposition for {source.parent_id}"
        )


def validate_composites(
    rows: list[ExportRow],
    mappings: dict[str, Mapping],
    sources: dict[str, CompositeSource],
    results: list[EmbeddedResult],
    expected_result_ids: dict[str, set[str]],
    source_cards: dict[str, SourceCard],
    *,
    enforce_known_results: bool = True,
) -> None:
    row_by_id = {row.arxiv_id: row for row in rows}
    required = {
        row.arxiv_id for row in rows if is_composite_source(row, mappings[row.arxiv_id])
    }
    missing = sorted(required - sources.keys())
    unknown = sorted(sources.keys() - row_by_id.keys())
    if missing:
        raise ValueError(f"missing composite-source audits: {', '.join(missing)}")
    if unknown:
        raise ValueError(f"composite sources absent from exports: {', '.join(unknown)}")

    expanded_parents = {
        parent_id
        for parent_id, source in sources.items()
        if source.resolution == "expanded_results"
    }
    missing_expectations = sorted(expanded_parents - expected_result_ids.keys())
    unknown_expectations = sorted(expected_result_ids.keys() - expanded_parents)
    if missing_expectations:
        raise ValueError(
            "expanded sources missing exact result inventories: "
            f"{', '.join(missing_expectations)}"
        )
    if unknown_expectations:
        raise ValueError(
            "exact result inventories lack expanded sources: "
            f"{', '.join(unknown_expectations)}"
        )
    if set(REQUIRED_SOURCE_CARDS) != expanded_parents:
        raise ValueError("source-card map does not exactly match expanded sources")
    if set(source_cards) != expanded_parents:
        raise ValueError("parsed source cards do not exactly match expanded sources")
    for parent_id, card in source_cards.items():
        if card.parent_id != parent_id:
            raise ValueError(f"source card has wrong parent binding for {parent_id}")
        if card.label != REQUIRED_SOURCE_CARDS[parent_id]:
            raise ValueError(f"source card has wrong label binding for {parent_id}")
        if card.result_ids != expected_result_ids[parent_id]:
            raise ValueError(f"source card has wrong result-ID binding for {parent_id}")

    by_parent: dict[str, list[EmbeddedResult]] = {
        identifier: [] for identifier in sources
    }
    seen_result_ids: set[str] = set()
    for result in results:
        if not all(getattr(result, field) for field in EMBEDDED_RESULT_FIELDS):
            raise ValueError(
                f"incomplete embedded result: {result.result_id or '<blank>'}"
            )
        if result.result_id in seen_result_ids:
            raise ValueError(f"duplicate embedded result: {result.result_id}")
        seen_result_ids.add(result.result_id)
        if result.parent_id not in sources:
            raise ValueError(
                f"embedded result has unaudited parent: {result.result_id}"
            )
        if not result.result_id.startswith(f"{result.parent_id}:"):
            raise ValueError(f"result id does not bind parent: {result.result_id}")
        if result.disposition_code not in RESULT_CODE_DEFINITIONS:
            raise ValueError(
                f"unknown result disposition for {result.result_id}: "
                f"{result.disposition_code}"
            )
        if not (
            result.primary_source.startswith("https://")
            or result.primary_source == "NONE_AFTER_BOUNDED_PUBLIC_SEARCH"
        ):
            raise ValueError(
                f"invalid primary-source resolution for {result.result_id}"
            )
        if len(result.disposition) < 40 or len(result.artifact_status) < 20:
            raise ValueError(f"underspecified embedded result: {result.result_id}")
        expected_card = source_cards[result.parent_id].label
        if result.source_card != expected_card:
            raise ValueError(
                f"invalid source card for {result.result_id}: "
                f"expected {expected_card!r}, found {result.source_card!r}"
            )
        by_parent[result.parent_id].append(result)

    for parent_id, source in sources.items():
        _validate_source_shape(source, by_parent[parent_id], mappings[parent_id])
        if source.resolution != "expanded_results":
            continue
        expected_ids = expected_result_ids[parent_id]
        if _expected_count(source) != len(expected_ids):
            raise ValueError(
                f"declared count disagrees with exact inventory for {parent_id}: "
                f"declared {_expected_count(source)}, inventoried {len(expected_ids)}"
            )
        found_ids = {result.result_id for result in by_parent[parent_id]}
        if found_ids != expected_ids:
            missing_ids = sorted(expected_ids - found_ids)
            unexpected_ids = sorted(found_ids - expected_ids)
            raise ValueError(
                f"exact embedded-result mismatch for {parent_id}: "
                f"missing={','.join(missing_ids) or 'none'}; "
                f"unexpected={','.join(unexpected_ids) or 'none'}"
            )

    if enforce_known_results:
        for parent_id, expected_ids in ANCHOR_RESULT_IDS.items():
            if expected_result_ids.get(parent_id) != expected_ids:
                raise ValueError(f"anchor inventory mismatch for {parent_id}")
            found_ids = {result.result_id for result in by_parent.get(parent_id, [])}
            missing_ids = sorted(expected_ids - found_ids)
            if missing_ids:
                raise ValueError(
                    f"known embedded results missing for {parent_id}: "
                    f"{', '.join(missing_ids)}"
                )


def run_regression_tests(
    rows: list[ExportRow],
    mappings: dict[str, Mapping],
    sources: dict[str, CompositeSource],
    results: list[EmbeddedResult],
    expected_result_ids: dict[str, set[str]],
    source_cards: dict[str, SourceCard],
) -> int:
    tests = 0

    def expect_failure(operation: Callable[[], None], label: str) -> None:
        nonlocal tests
        try:
            operation()
        except ValueError:
            tests += 1
            return
        raise ValueError(f"negative control unexpectedly passed: {label}")

    predecessor_sources = dict(sources)
    predecessor_sources.pop("2501.08913", None)
    expect_failure(
        lambda: validate_composites(
            rows,
            mappings,
            predecessor_sources,
            results,
            expected_result_ids,
            source_cards,
        ),
        "predecessor Task 3 catch-all",
    )

    missing_task3_result = [
        result
        for result in results
        if result.result_id != "2501.08913:cnlp-nits-distilbert"
    ]
    expect_failure(
        lambda: validate_composites(
            rows,
            mappings,
            sources,
            missing_task3_result,
            expected_result_ids,
            source_cards,
        ),
        "named Task 3 result omitted",
    )

    mutable_count_sources = dict(sources)
    mutable_count_sources["2605.15518"] = replace(
        sources["2605.15518"], expected_result_count="1"
    )
    missing_non_anchor_result = [
        result
        for result in results
        if result.result_id != "2605.15518:mdeberta-classifier"
    ]
    expect_failure(
        lambda: validate_composites(
            rows,
            mappings,
            mutable_count_sources,
            missing_non_anchor_result,
            expected_result_ids,
            source_cards,
        ),
        "non-anchor result omitted with lowered mutable count",
    )

    hidden_high_cell_sources = dict(sources)
    hidden_high_cell_sources["2604.16607"] = replace(
        sources["2604.16607"],
        resolution="no_qualifying_result",
        expected_result_count="0",
        reason=(
            "All mean values are below 0.90, so the named high per-dataset "
            "results are incorrectly suppressed in this negative control."
        ),
    )
    hidden_high_cell_results = [
        result for result in results if result.parent_id != "2604.16607"
    ]
    expect_failure(
        lambda: validate_composites(
            rows,
            mappings,
            hidden_high_cell_sources,
            hidden_high_cell_results,
            expected_result_ids,
            source_cards,
        ),
        "formerly hidden high-cell parent reclassified as no-qualifier",
    )

    wrong_card_results = [
        replace(result, source_card="does-not-exist")
        if result.result_id == "2605.15518:mdeberta-classifier"
        else result
        for result in results
    ]
    expect_failure(
        lambda: validate_composites(
            rows,
            mappings,
            sources,
            wrong_card_results,
            expected_result_ids,
            source_cards,
        ),
        "unbound source-card label",
    )

    missing_source_cards = dict(source_cards)
    missing_source_cards.pop("2605.15518")
    expect_failure(
        lambda: validate_composites(
            rows,
            mappings,
            sources,
            results,
            expected_result_ids,
            missing_source_cards,
        ),
        "real source card removed",
    )

    wrong_parent_cards = dict(source_cards)
    wrong_parent_cards["2605.15518"] = replace(
        source_cards["2605.15518"], parent_id="2606.04906"
    )
    expect_failure(
        lambda: validate_composites(
            rows,
            mappings,
            sources,
            results,
            expected_result_ids,
            wrong_parent_cards,
        ),
        "real source card bound to wrong parent",
    )

    wrong_result_cards = dict(source_cards)
    wrong_result_cards["2605.15518"] = replace(
        source_cards["2605.15518"],
        result_ids=(
            source_cards["2605.15518"].result_ids - {"2605.15518:mdeberta-classifier"}
        ),
    )
    expect_failure(
        lambda: validate_composites(
            rows,
            mappings,
            sources,
            results,
            expected_result_ids,
            wrong_result_cards,
        ),
        "real source card missing a cited result ID",
    )

    synthetic_source = CompositeSource(
        parent_id="synthetic",
        composite_kind="benchmark",
        resolution="expanded_results",
        expected_result_count="2",
        inspected_scope="Synthetic table inspected across every named system and metric column.",
        evidence_source="https://arxiv.org/abs/synthetic",
        reason="Two qualifying systems are declared so one child row must not pass validation.",
    )
    synthetic_mapping = Mapping(
        arxiv_id="synthetic",
        mapping_kind="non_candidate_class",
        disposition_code="benchmark_study",
        flag_resolution="false_positive",
        reason="synthetic",
        source="https://arxiv.org/abs/synthetic",
    )
    one_synthetic_result = EmbeddedResult(
        parent_id="synthetic",
        result_id="synthetic:one",
        system="one",
        version="v1",
        claim="0.99 AUROC",
        metric_scope="synthetic aggregate",
        qualifying_basis="metric at least 0.90",
        primary_source="NONE_AFTER_BOUNDED_PUBLIC_SEARCH",
        artifact_status="No public state in this synthetic control.",
        disposition_code="primary_absent",
        disposition="Synthetic disposition long enough to exercise the shape validator.",
        source_card="synthetic-control",
    )
    expect_failure(
        lambda: _validate_source_shape(
            synthetic_source,
            [one_synthetic_result],
            synthetic_mapping,
        ),
        "analogous missing benchmark result",
    )

    weak_negative = CompositeSource(
        parent_id="synthetic",
        composite_kind="benchmark",
        resolution="no_qualifying_result",
        expected_result_count="0",
        inspected_scope="short",
        evidence_source="https://arxiv.org/abs/synthetic",
        reason="short",
    )
    expect_failure(
        lambda: _validate_source_shape(weak_negative, [], synthetic_mapping),
        "undocumented no-qualifying assertion",
    )

    complete_negative = CompositeSource(
        parent_id="synthetic",
        composite_kind="benchmark",
        resolution="no_qualifying_result",
        expected_result_count="0",
        inspected_scope=(
            "All aggregate rows in synthetic Tables 1 through 3 were inspected."
        ),
        evidence_source="https://arxiv.org/abs/synthetic",
        reason=(
            "The largest aggregate threshold metric is 0.81, so no system meets "
            "the frozen 0.90 or strong-claim rule."
        ),
    )
    _validate_source_shape(complete_negative, [], synthetic_mapping)
    tests += 1
    return tests


def write_audit(
    path: Path,
    rows: list[ExportRow],
    mappings: dict[str, Mapping],
    sources: dict[str, CompositeSource],
    results: list[EmbeddedResult],
) -> None:
    fields = (
        "arxiv_id",
        "published",
        "title",
        "exports",
        "semantic_flags",
        "flag_evidence",
        "mapping_kind",
        "disposition_code",
        "class_definition",
        "flag_resolution",
        "reason",
        "source",
        "composite_required",
        "composite_resolution",
        "embedded_result_count",
        "composite_reason",
    )
    result_counts: dict[str, int] = {}
    for result in results:
        result_counts[result.parent_id] = result_counts.get(result.parent_id, 0) + 1
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(
            target, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        for row in rows:
            flags, evidence = semantic_flags(row)
            mapping = mappings[row.arxiv_id]
            source = sources.get(row.arxiv_id)
            writer.writerow(
                {
                    "arxiv_id": row.arxiv_id,
                    "published": row.published,
                    "title": row.title,
                    "exports": ";".join(row.exports),
                    "semantic_flags": ";".join(flags) or "none",
                    "flag_evidence": " || ".join(evidence) or "none",
                    "mapping_kind": mapping.mapping_kind,
                    "disposition_code": mapping.disposition_code,
                    "class_definition": CODE_DEFINITIONS[mapping.mapping_kind][
                        mapping.disposition_code
                    ],
                    "flag_resolution": mapping.flag_resolution,
                    "reason": mapping.reason,
                    "source": mapping.source,
                    "composite_required": str(
                        is_composite_source(row, mapping)
                    ).lower(),
                    "composite_resolution": (
                        source.resolution if source is not None else "not_composite"
                    ),
                    "embedded_result_count": result_counts.get(row.arxiv_id, 0),
                    "composite_reason": (
                        source.reason if source is not None else "not_composite"
                    ),
                }
            )


def write_embedded_audit(
    path: Path,
    rows: list[ExportRow],
    results: list[EmbeddedResult],
) -> None:
    row_by_id = {row.arxiv_id: row for row in rows}
    fields = (
        "parent_id",
        "parent_published",
        "parent_title",
        *EMBEDDED_RESULT_FIELDS[1:],
        "class_definition",
    )
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(
            target,
            fieldnames=fields,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for result in sorted(
            results, key=lambda item: (item.parent_id, item.result_id)
        ):
            parent = row_by_id[result.parent_id]
            writer.writerow(
                {
                    "parent_id": result.parent_id,
                    "parent_published": parent.published,
                    "parent_title": parent.title,
                    **{
                        field: getattr(result, field)
                        for field in EMBEDDED_RESULT_FIELDS[1:]
                    },
                    "class_definition": RESULT_CODE_DEFINITIONS[
                        result.disposition_code
                    ],
                }
            )


def write_environment(path: Path) -> None:
    path.write_text(
        f"python={sys.version.replace(chr(10), ' ')}\n"
        f"implementation={platform.python_implementation()}\n"
        f"platform={platform.platform()}\n"
        "dependencies=Python standard library only\n",
        encoding="utf-8",
    )


def write_report(
    path: Path,
    source_dir: Path,
    map_path: Path,
    composite_sources_path: Path,
    embedded_results_path: Path,
    expected_results_path: Path,
    source_cards_path: Path,
    audit_path: Path,
    embedded_audit_path: Path,
    environment_path: Path,
    rows: list[ExportRow],
    raw_rows: int,
    mappings: dict[str, Mapping],
    sources: dict[str, CompositeSource],
    results: list[EmbeddedResult],
    regression_tests: int,
) -> str:
    n_flagged = sum(bool(semantic_flags(row)[0]) for row in rows)
    n_explicit = sum(
        mapping.mapping_kind == "explicit_disposition" for mapping in mappings.values()
    )
    n_non_candidate = len(mappings) - n_explicit
    n_composite_required = sum(
        is_composite_source(row, mappings[row.arxiv_id]) for row in rows
    )
    lines = [
        "command=uv run --isolated --no-project --python 3.13 python audit_coverage.py --map coverage_row_dispositions.tsv --composite-sources coverage_composite_sources.tsv --embedded-results coverage_embedded_results.tsv --expected-results coverage_expected_result_ids.tsv --source-cards coverage_composite_dispositions.md --output coverage_semantic_audit.tsv --embedded-output coverage_embedded_result_audit.tsv --report coverage_semantic_audit_report.txt --environment coverage_semantic_audit_environment.txt",
        f"raw_export_rows={raw_rows}",
        f"unique_2025_2026_rows={len(rows)}",
        f"semantically_flagged_rows={n_flagged}",
        f"explicit_dispositions={n_explicit}",
        f"non_candidate_classes={n_non_candidate}",
        f"mapping_rows={len(mappings)}",
        f"composite_required_rows={n_composite_required}",
        f"composite_review_rows={len(sources)}",
        f"embedded_result_rows={len(results)}",
        f"regression_and_negative_controls={regression_tests}",
    ]
    for export_name in EXPORT_NAMES:
        lines.append(f"sha256 {export_name}={sha256(source_dir / export_name)}")
    lines.extend(
        (
            f"sha256 {Path(__file__).name}={sha256(Path(__file__))}",
            f"sha256 {map_path.name}={sha256(map_path)}",
            f"sha256 {composite_sources_path.name}={sha256(composite_sources_path)}",
            f"sha256 {embedded_results_path.name}={sha256(embedded_results_path)}",
            f"sha256 {expected_results_path.name}={sha256(expected_results_path)}",
            f"sha256 {source_cards_path.name}={sha256(source_cards_path)}",
            f"sha256 {audit_path.name}={sha256(audit_path)}",
            f"sha256 {embedded_audit_path.name}={sha256(embedded_audit_path)}",
            f"sha256 {environment_path.name}={sha256(environment_path)}",
            "result=PASS",
        )
    )
    report = "\n".join(lines) + "\n"
    path.write_text(report, encoding="utf-8")
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", type=Path)
    parser.add_argument("--composite-sources", type=Path)
    parser.add_argument("--embedded-results", type=Path)
    parser.add_argument("--expected-results", type=Path)
    parser.add_argument("--source-cards", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--embedded-output", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--environment", type=Path)
    parser.add_argument("--inventory", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_dir = Path(__file__).resolve().parent
    rows, raw_rows = load_exports(source_dir)
    if args.inventory:
        writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
        writer.writerow(("arxiv_id", "published", "title", "semantic_flags"))
        for row in rows:
            writer.writerow(
                (
                    row.arxiv_id,
                    row.published,
                    row.title,
                    ";".join(semantic_flags(row)[0]) or "none",
                )
            )
        return 0
    required = (
        args.map,
        args.composite_sources,
        args.embedded_results,
        args.expected_results,
        args.source_cards,
        args.output,
        args.embedded_output,
        args.report,
        args.environment,
    )
    if any(path is None for path in required):
        raise ValueError(
            "--map, --composite-sources, --embedded-results, --expected-results, "
            "--source-cards, --output, --embedded-output, --report, and "
            "--environment are required"
        )
    (
        map_path,
        composite_sources_path,
        embedded_results_path,
        expected_results_path,
        source_cards_path,
        output_path,
        embedded_output_path,
        report_path,
        environment_path,
    ) = required
    mappings = load_mappings(map_path)
    sources = load_composite_sources(composite_sources_path)
    results = load_embedded_results(embedded_results_path)
    expected_result_ids = load_expected_result_ids(expected_results_path)
    source_cards = load_source_cards(source_cards_path)
    validate(rows, mappings)
    validate_composites(
        rows, mappings, sources, results, expected_result_ids, source_cards
    )
    regression_tests = run_regression_tests(
        rows, mappings, sources, results, expected_result_ids, source_cards
    )
    write_audit(output_path, rows, mappings, sources, results)
    write_embedded_audit(embedded_output_path, rows, results)
    write_environment(environment_path)
    report = write_report(
        report_path,
        source_dir,
        map_path,
        composite_sources_path,
        embedded_results_path,
        expected_results_path,
        source_cards_path,
        output_path,
        embedded_output_path,
        environment_path,
        rows,
        raw_rows,
        mappings,
        sources,
        results,
        regression_tests,
    )
    print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
