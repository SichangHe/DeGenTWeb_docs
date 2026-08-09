#!/usr/bin/env python3
"""Validate one semantic disposition for every frozen 2025–2026 export row."""

from __future__ import annotations

import argparse
import csv
import hashlib
import platform
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
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
ALLOWED_FLAG_RESOLUTIONS = {"candidate_disposition", "false_positive", "not_flagged"}
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


def write_audit(
    path: Path, rows: list[ExportRow], mappings: dict[str, Mapping]
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
    )
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(
            target, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        for row in rows:
            flags, evidence = semantic_flags(row)
            mapping = mappings[row.arxiv_id]
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
    audit_path: Path,
    environment_path: Path,
    rows: list[ExportRow],
    raw_rows: int,
    mappings: dict[str, Mapping],
) -> str:
    n_flagged = sum(bool(semantic_flags(row)[0]) for row in rows)
    n_explicit = sum(
        mapping.mapping_kind == "explicit_disposition" for mapping in mappings.values()
    )
    n_non_candidate = len(mappings) - n_explicit
    lines = [
        "command=uv run --isolated --no-project --python 3.13 python audit_coverage.py --map coverage_row_dispositions.tsv --output coverage_semantic_audit.tsv --report coverage_semantic_audit_report.txt --environment coverage_semantic_audit_environment.txt",
        f"raw_export_rows={raw_rows}",
        f"unique_2025_2026_rows={len(rows)}",
        f"semantically_flagged_rows={n_flagged}",
        f"explicit_dispositions={n_explicit}",
        f"non_candidate_classes={n_non_candidate}",
        f"mapping_rows={len(mappings)}",
    ]
    for export_name in EXPORT_NAMES:
        lines.append(f"sha256 {export_name}={sha256(source_dir / export_name)}")
    lines.extend(
        (
            f"sha256 {Path(__file__).name}={sha256(Path(__file__))}",
            f"sha256 {map_path.name}={sha256(map_path)}",
            f"sha256 {audit_path.name}={sha256(audit_path)}",
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
    parser.add_argument("--output", type=Path)
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
    required = (args.map, args.output, args.report, args.environment)
    if any(path is None for path in required):
        raise ValueError("--map, --output, --report, and --environment are required")
    map_path, output_path, report_path, environment_path = required
    mappings = load_mappings(map_path)
    validate(rows, mappings)
    write_audit(output_path, rows, mappings)
    write_environment(environment_path)
    report = write_report(
        report_path,
        source_dir,
        map_path,
        output_path,
        environment_path,
        rows,
        raw_rows,
        mappings,
    )
    print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
