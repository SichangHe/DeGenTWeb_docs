#!/usr/bin/env python3
"""Validate row and embedded-result coverage for frozen 2025–2026 exports."""

from __future__ import annotations

import argparse
import csv
import hashlib
import platform
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections.abc import Callable
from dataclasses import dataclass, replace
from pathlib import Path

import discover_table_accounts as table_discovery

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
FULLTEXT_SOURCE_FIELDS = (
    "parent_id",
    "title",
    "paper_path",
    "pdf_sha256",
    "text_sha256",
    "mapping_kind",
    "publication_role",
    "resolution",
    "expected_account_count",
    "inspected_scope",
    "reason",
)
FULLTEXT_ACCOUNT_FIELDS = (
    "parent_id",
    "account_id",
    "system",
    "account_kind",
    "evidence_locator",
    "qualifying_evidence",
)
FULLTEXT_ACCOUNT_MAP_FIELDS = (
    "parent_id",
    "account_id",
    "resolution_kind",
    "target_id",
)
ALLOWED_FULLTEXT_RESOLUTIONS = {
    "embedded_result",
    "embedded_result+primary_result",
    "no_qualifying_account",
    "primary_result",
}
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
RESULT_CODE_TEXT_PATTERNS = {
    "exclude_generation": re.compile(r"generat|autoregress|summar|simplif", re.I),
    "exclude_multi_perturbation": re.compile(r"perturb|shuffl|auxiliary|sampl", re.I),
    "exclude_perturbation": re.compile(r"perturb|sanitiz|transform", re.I),
    "exclude_regeneration": re.compile(
        r"generat|continuation|ideal|replacement|repair", re.I
    ),
    "exclude_retrieval": re.compile(
        r"retriev|nearest|datastore|lookup|vocabular|retained reference|dictionary",
        re.I,
    ),
    "exclude_rewriting": re.compile(
        r"rewrit|normaliz|canonical|replace|transform|paraphras", re.I
    ),
}
EXPECTED_RESULT_IDS_SHA256 = (
    "d1c505385cfeaaf01582bbc972ace563a12e0b756199d10c99f47736b66a864f"
)
SOURCE_CARDS_SHA256 = "0ee5e13d9d053987153953525641b1ed45f4d614043efc4960d7b4ad30c61775"
FULLTEXT_SOURCES_SHA256 = (
    "541eded2fc1de41fd3ca845035c8b704b96fd19b1fc82210079fdd1f054fedee"
)
FULLTEXT_ACCOUNTS_SHA256 = (
    "78cf40ef5daa64712a926d2c1d822b145beb4635a924b9a2e3c8b93e9cc4c846"
)
FULLTEXT_ACCOUNT_MAP_SHA256 = (
    "459832035eb67b51630ddbe0bfb92355afb18f9485e6c4bef7f0cd64274e04ff"
)
PRIMARY_RESULTS_SHA256 = (
    "9bd6434060456233794f7d5d9b1b7e6c22d7bb9ea1689df3b7f3c7ddc00a0aec"
)
TABLE_CANDIDATES_SHA256 = (
    "0460babd82a2aba738e83d53b978f464f0e546305037e92d03a565ab47e045dd"
)
TABLE_DISCOVERY_SHA256 = (
    "296a40b62dd17c828f9dc959a1667a5465803a333efd9d3bf03b086c24033a48"
)
FULLTEXT_ACCOUNT_SET_SHA256 = (
    "1647ac46547ecab7adb0e96f09785e2b06d46a8ae7bb3fc66b3dd4168a6657db"
)
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
CONTENT_ANCHOR_ACCOUNTS = {
    "2501.03940": {
        "2501.03940:radar-ft",
        "2501.03940:m4-roberta-base",
        "2501.03940:gpt2",
        "2501.03940:llama31-1b",
        "2501.03940:hsff-gpt2",
        "2501.03940:hsff-llama31-1b",
        "2501.03940:mpn-gpt2",
        "2501.03940:mpn-llama31-1b",
        "2501.03940:ens-gpt2-llama",
        "2501.03940:ens-2gpt2-2llama",
        "2501.03940:ens-2gpt2",
        "2501.03940:ens-2llama",
        "2501.03940:ens-gpt2-llama-qwen",
    },
    "2607.03680": {
        "2607.03680:vanilla-intellabs-base",
        "2607.03680:vanilla-mage-large",
        "2607.03680:vanilla-faid-base",
        "2607.03680:vanilla-mirage-large",
        "2607.03680:fomaml-lora",
        "2607.03680:confidence-ensemble",
    },
    "2605.25281": {
        "2605.25281:imbd-read",
        "2605.25281:imbd-target-adapted",
        "2605.25281:grpo-noncot",
        "2605.25281:grpo-cot",
    },
    "2509.00623": {
        "2509.00623:roberta-base",
        "2509.00623:tfidf-svm",
        "2509.00623:candace",
    },
    "2503.22338": {
        f"2503.22338:{learner}-{feature}"
        for learner in ("svc", "rf", "xgb")
        for feature in ("raidar", "nela", "combined")
    },
    "2502.16857": {
        "2502.16857:original-xsmall",
        "2502.16857:original-small",
        "2502.16857:original-base",
        "2502.16857:noised-xsmall",
        "2502.16857:noised-small",
        "2502.16857:noised-base",
        "2502.16857:double-small",
        "2502.16857:ensemble-small",
    },
    "2507.05157": {
        "2507.05157:gpt4o-mini",
        "2507.05157:bert",
        "2507.05157:llama3-8b",
    },
    "2607.23805": set(),
    "2605.14240": set(),
    "2604.19768": set(),
    "2510.22874": set(),
    "2505.15422": set(),
    "2503.23622": set(),
    "2606.18946": {
        "2606.18946:poger",
        "2606.18946:seqxgpt",
        "2606.18946:sendetex",
        "2606.18946:senflow",
        "2606.18946:senflow-no-gcn",
        "2606.18946:senflow-no-crf",
        "2606.18946:senflow-no-cl",
        "2606.18946:senflow-no-tcn",
    },
    "2509.00731": {
        "2509.00731:roberta",
        "2509.00731:bert",
        "2509.00731:fasttext",
        "2509.00731:qwen-r4",
        "2509.00731:qwen-r8",
        "2509.00731:qwen-r16",
        "2509.00731:deepseek-r4",
        "2509.00731:deepseek-r8",
        "2509.00731:deepseek-r16",
    },
    "2501.14288": {
        "2501.14288:deberta",
        "2501.14288:deberta-lstm",
        "2501.14288:deberta-lstm-attention",
        "2501.14288:target-shuffling",
        "2501.14288:ensemble",
    },
    "2501.11914": {
        "2501.11914:inverse-perplexity-en",
        "2501.11914:inverse-perplexity-multi",
    },
    "2511.21744": {
        "2511.21744:cnn",
        "2511.21744:random-forest",
    },
    "2505.12507": {
        "2505.12507:npr",
        "2505.12507:lrr",
        "2505.12507:rank",
        "2505.12507:entropy",
        "2505.12507:logrank",
        "2505.12507:likelihood",
        "2505.12507:glimpse",
        "2505.12507:binoculars",
        "2505.12507:dnagpt",
        "2505.12507:fastdetectgpt",
        "2505.12507:roberta-qa",
        "2505.12507:radar",
        "2505.12507:gptzero",
        "2505.12507:detective",
        "2505.12507:lm2",
        "2505.12507:lm2-gpt2-tokenizer",
        "2505.12507:lm2-u",
        "2505.12507:lm2-w",
        "2505.12507:lm2-uw",
        "2505.12507:lm2-no-bert",
    },
    "2605.27921": {
        "2605.27921:tell",
        "2605.27921:mage",
        "2605.27921:pangram-editlens",
        "2605.27921:fastdetectgpt",
        "2605.27921:argugpt",
        "2605.27921:t5-sentinel",
        "2605.27921:detectllm-npr",
        "2605.27921:openai-roberta",
        "2605.27921:aigc-mpu",
        "2605.27921:detectllm-lrr",
        "2605.27921:logrank-gpt2-medium",
        "2605.27921:radar",
        "2605.27921:chatgpt-d",
    },
    "2604.16923": {
        "2604.16923:entropy",
        "2604.16923:likelihood",
        "2604.16923:logrank",
        "2604.16923:fastdetectgpt",
        "2604.16923:lastde-plus",
        "2604.16923:binoculars",
        "2604.16923:dna-detectllm",
        "2604.16923:remodetect",
        "2604.16923:imbd",
        "2604.16923:rai",
        "2604.16923:s-score",
        "2604.16923:lapd-llama2",
        "2604.16923:lapd-falcon",
        "2604.16923:lapd-gptj",
        "2604.16923:lapd-llama31",
    },
    "2601.04833": {
        "2601.04833:likelihood",
        "2601.04833:logrank",
        "2601.04833:fastdetectgpt",
        "2601.04833:lastde",
        "2601.04833:diveye",
        "2601.04833:dd",
        "2601.04833:lv",
        "2601.04833:tsd",
        "2601.04833:tsd-plus",
    },
    "2509.15550": {
        "2509.15550:biscope",
        "2509.15550:entropy",
        "2509.15550:likelihood",
        "2509.15550:logrank",
        "2509.15550:detectgpt",
        "2509.15550:fastdetectgpt",
        "2509.15550:binoculars",
        "2509.15550:lastde-plus",
        "2509.15550:dna-default",
        "2509.15550:dna-low-high",
        "2509.15550:dna-high-low",
        "2509.15550:dna-sequential",
        "2509.15550:dna-mistral",
        "2509.15550:dna-llama2",
        "2509.15550:dna-llama3",
    },
    "2504.21019": {
        "2504.21019:uniform",
        "2504.21019:gaussian",
    },
}
CONTENT_ANCHOR_TEXT = {
    "2501.03940": ("RADAR-FT", "five epochs", "RoBERTa", "0.970"),
    "2607.03680": (
        "IntelLabs (base)",
        "MAGE (large)",
        "FAID (base)",
        "MIRAGE (large)",
    ),
    "2605.25281": ("I M BD", "I M BD∗", "0.920", "0.929"),
    "2509.00623": ("TF-IDF + SVM", "Candace", "99.95"),
    "2503.22338": ("RAIDAR + NELA", "Random Forest", "0.9945"),
    "2502.16857": ("Double Finetune", "Ensemble", "0.9531"),
    "2507.05157": ("GPT-4o-mini", "BERT", "Llama", "93%"),
    "2607.23805": ("Fraudulent AI-Generated", "Software Engineering Surveys"),
    "2605.14240": ("Paraphrasing Attack Resilience", "0.8061"),
    "2604.19768": ("rhetorical intensity", "miscalibration"),
    "2510.22874": ("A Comprehensive Dataset", "0.53"),
    "2505.15422": ("studies conducted from 2015 to 2024", "accuracy of 98%"),
    "2503.23622": ("AI-Resilient Assessments", "automated feedback"),
    "2606.18946": ("SenFlow", "0.940"),
    "2509.00731": ("Qwen2.5-7B", "0.9594", "0.9008"),
    "2501.14288": ("DeBERTa-v3-large", "94.7"),
    "2501.11914": ("Inverse Perplexity", "0.7513"),
    "2511.21744": ("Random Forest", "0.9951"),
    "2505.12507": ("LM2 OTIFS", "Table 18", "0.97"),
    "2605.27921": ("T5Sentinel", "ChatGPT-D", "1.000"),
    "2604.16923": ("ReMoDetect", "ImBD", "92.18", "92.12"),
    "2601.04833": ("Likelihood", "Diveye", "92.96", "93.80"),
    "2509.15550": ("Biscope", "Mutation Repair", "98.30"),
    "2504.21019": ("training phase", "Gaussian noise", "86.10"),
}
RESULT_CODE_ANCHORS = {
    "2511.21744:detective-comparator": "exclude_retrieval",
    "2501.03940:radar-ft": "retain_reject",
    "2501.03940:m4-roberta-base": "retain_reject",
    "2607.03680:vanilla-intellabs-base": "retain_reject",
    "2607.03680:vanilla-mage-large": "retain_reject",
    "2607.03680:vanilla-faid-base": "retain_reject",
    "2607.03680:vanilla-mirage-large": "retain_reject",
    "2605.25281:imbd-read": "retain_reject",
    "2605.25281:imbd-target-adapted": "retain_reject",
    "2509.15550:biscope": "retain_reject",
    "2509.15550:entropy": "retain_reject",
    "2509.15550:likelihood": "retain_reject",
    "2509.15550:logrank": "retain_reject",
    "2509.15550:detectgpt": "exclude_multi_perturbation",
    "2509.15550:fastdetectgpt": "retain_reject",
    "2509.15550:binoculars": "retain_reject",
    "2509.15550:lastde-plus": "retain_reject",
    "2509.15550:dna-default": "exclude_regeneration",
    "2509.15550:dna-low-high": "exclude_regeneration",
    "2509.15550:dna-high-low": "exclude_regeneration",
    "2509.15550:dna-sequential": "exclude_regeneration",
    "2509.15550:dna-mistral": "exclude_regeneration",
    "2509.15550:dna-llama2": "exclude_regeneration",
    "2509.15550:dna-llama3": "exclude_regeneration",
    "2504.21019:uniform": "retain_reject",
    "2504.21019:gaussian": "retain_reject",
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


@dataclass(frozen=True)
class FulltextSource:
    parent_id: str
    title: str
    paper_path: str
    pdf_sha256: str
    text_sha256: str
    mapping_kind: str
    publication_role: str
    resolution: str
    expected_account_count: str
    inspected_scope: str
    reason: str


@dataclass(frozen=True)
class FulltextAccount:
    parent_id: str
    account_id: str
    system: str
    account_kind: str
    evidence_locator: str
    qualifying_evidence: str


@dataclass(frozen=True)
class FulltextAccountMap:
    parent_id: str
    account_id: str
    resolution_kind: str
    target_id: str


def validate_result_disposition(result: EmbeddedResult) -> None:
    if result.disposition_code == "retain_reject" and re.search(
        r"\bviolat(?:e|es|ing)\b.{0,100}\b(?:boundary|constraint)\b",
        result.disposition,
        re.I,
    ):
        raise ValueError(
            f"retained result inherits an exclusion blocker: {result.result_id}"
        )
    pattern = RESULT_CODE_TEXT_PATTERNS.get(result.disposition_code)
    if pattern is not None and pattern.search(result.disposition) is None:
        raise ValueError(
            "excluded result lacks mechanism-specific disposition evidence: "
            f"{result.result_id}"
        )


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


def _require_hash(path: Path, expected: str, label: str) -> None:
    actual = sha256(path)
    if actual != expected:
        raise ValueError(f"{label} hash mismatch: expected {expected}, found {actual}")


def load_fulltext_sources(path: Path) -> dict[str, FulltextSource]:
    _require_hash(path, FULLTEXT_SOURCES_SHA256, "full-text source inventory")
    sources: dict[str, FulltextSource] = {}
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if reader.fieldnames != list(FULLTEXT_SOURCE_FIELDS):
            raise ValueError(
                f"full-text-source header must be: {' | '.join(FULLTEXT_SOURCE_FIELDS)}"
            )
        for raw in reader:
            item = FulltextSource(
                **{field: raw[field].strip() for field in FULLTEXT_SOURCE_FIELDS}
            )
            if item.parent_id in sources:
                raise ValueError(f"duplicate full-text source: {item.parent_id}")
            sources[item.parent_id] = item
    return sources


def load_fulltext_accounts(path: Path) -> list[FulltextAccount]:
    _require_hash(path, FULLTEXT_ACCOUNTS_SHA256, "full-text account inventory")
    accounts: list[FulltextAccount] = []
    seen: set[str] = set()
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if reader.fieldnames != list(FULLTEXT_ACCOUNT_FIELDS):
            raise ValueError(
                "full-text-account header must be: "
                f"{' | '.join(FULLTEXT_ACCOUNT_FIELDS)}"
            )
        for raw in reader:
            item = FulltextAccount(
                **{field: raw[field].strip() for field in FULLTEXT_ACCOUNT_FIELDS}
            )
            if item.account_id in seen:
                raise ValueError(f"duplicate full-text account: {item.account_id}")
            seen.add(item.account_id)
            accounts.append(item)
    return accounts


def load_fulltext_account_map(path: Path) -> list[FulltextAccountMap]:
    _require_hash(path, FULLTEXT_ACCOUNT_MAP_SHA256, "full-text account map")
    account_map: list[FulltextAccountMap] = []
    seen: set[str] = set()
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if reader.fieldnames != list(FULLTEXT_ACCOUNT_MAP_FIELDS):
            raise ValueError(
                "full-text-account-map header must be: "
                f"{' | '.join(FULLTEXT_ACCOUNT_MAP_FIELDS)}"
            )
        for raw in reader:
            item = FulltextAccountMap(
                **{field: raw[field].strip() for field in FULLTEXT_ACCOUNT_MAP_FIELDS}
            )
            if item.account_id in seen:
                raise ValueError(f"duplicate full-text account map: {item.account_id}")
            seen.add(item.account_id)
            account_map.append(item)
    return account_map


def load_primary_results(path: Path) -> list[EmbeddedResult]:
    _require_hash(path, PRIMARY_RESULTS_SHA256, "primary-result inventory")
    return load_embedded_results(path)


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
        validate_result_disposition(result)
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


def _fulltext_account_digest(accounts: list[FulltextAccount]) -> str:
    inventory = "".join(
        f"{item.parent_id}\t{item.account_id}\n"
        for item in sorted(accounts, key=lambda item: (item.parent_id, item.account_id))
    )
    return hashlib.sha256(inventory.encode()).hexdigest()


def _read_fulltext_artifact(
    paper_root: Path, source: FulltextSource
) -> tuple[str, str, str]:
    relative = Path(source.paper_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe paper path for {source.parent_id}: {relative}")
    root = paper_root.resolve()
    paper = (root / relative).resolve()
    if not paper.is_relative_to(root) or not paper.is_file():
        raise ValueError(f"missing preserved primary PDF for {source.parent_id}")
    completed = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(paper), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return (
        sha256(paper),
        hashlib.sha256(completed.stdout).hexdigest(),
        compact(completed.stdout.decode("utf-8", errors="replace")),
    )


def validate_table_discovery(
    fulltext_sources_path: Path,
    fulltext_accounts_path: Path,
    candidates_path: Path,
    discovery_path: Path,
    paper_root: Path,
) -> tuple[list[table_discovery.Candidate], list[table_discovery.Resolution]]:
    """Replay PDF-table discovery independently of the curated generator."""
    if sha256(candidates_path) != TABLE_CANDIDATES_SHA256:
        raise ValueError("table-candidate snapshot hash mismatch")
    if sha256(discovery_path) != TABLE_DISCOVERY_SHA256:
        raise ValueError("table-discovery snapshot hash mismatch")
    sources = table_discovery.load_sources(fulltext_sources_path)
    candidates = table_discovery.discover_all(sources, paper_root)
    if table_discovery.serialize(candidates) != candidates_path.read_text(
        encoding="utf-8"
    ):
        raise ValueError("table-candidate snapshot does not reproduce from PDFs")
    accounts = table_discovery.load_accounts(fulltext_accounts_path)
    resolutions = table_discovery.resolve_all(candidates, accounts)
    table_discovery.validate_resolutions(candidates, resolutions, accounts)
    if table_discovery.serialize_resolutions(resolutions) != discovery_path.read_text(
        encoding="utf-8"
    ):
        raise ValueError("table-discovery account matches do not reproduce")
    return candidates, resolutions


def validate_fulltext(
    rows: list[ExportRow],
    mappings: dict[str, Mapping],
    fulltext_sources: dict[str, FulltextSource],
    accounts: list[FulltextAccount],
    account_map: list[FulltextAccountMap],
    embedded_results: list[EmbeddedResult],
    primary_results: list[EmbeddedResult],
    paper_root: Path,
    *,
    artifacts: dict[str, tuple[str, str, str]] | None = None,
    table_resolutions: list[table_discovery.Resolution] | None = None,
) -> dict[str, tuple[str, str, str]]:
    row_by_id = {row.arxiv_id: row for row in rows}
    row_ids = set(row_by_id)
    if set(fulltext_sources) != row_ids:
        missing = sorted(row_ids - set(fulltext_sources))
        unknown = sorted(set(fulltext_sources) - row_ids)
        raise ValueError(
            "full-text source inventory mismatch: "
            f"missing={','.join(missing) or 'none'}; "
            f"unknown={','.join(unknown) or 'none'}"
        )

    if _fulltext_account_digest(accounts) != FULLTEXT_ACCOUNT_SET_SHA256:
        raise ValueError("immutable full-text account set mismatch")
    account_by_id = {item.account_id: item for item in accounts}
    map_by_id = {item.account_id: item for item in account_map}
    if len(account_by_id) != len(accounts) or len(map_by_id) != len(account_map):
        raise ValueError("duplicate account IDs escaped a full-text loader")
    if set(account_by_id) != set(map_by_id):
        raise ValueError("full-text accounts and disposition map differ")

    embedded_by_id = {item.result_id: item for item in embedded_results}
    primary_by_id = {item.result_id: item for item in primary_results}
    if set(embedded_by_id) & set(primary_by_id):
        raise ValueError("embedded and primary result IDs overlap")
    for result_id, expected_code in RESULT_CODE_ANCHORS.items():
        result = primary_by_id.get(result_id)
        if result is None or result.disposition_code != expected_code:
            raise ValueError(
                "result-specific method disposition mismatch: "
                f"{result_id} expected {expected_code}"
            )

    by_parent: dict[str, list[FulltextAccount]] = {
        parent_id: [] for parent_id in fulltext_sources
    }
    for account in accounts:
        if not all(getattr(account, field) for field in FULLTEXT_ACCOUNT_FIELDS):
            raise ValueError(f"incomplete full-text account: {account.account_id}")
        if account.parent_id not in fulltext_sources:
            raise ValueError(
                f"full-text account has unknown parent: {account.account_id}"
            )
        if not (
            account.account_id == account.parent_id
            or account.account_id.startswith(f"{account.parent_id}:")
        ):
            raise ValueError(
                f"full-text account has wrong parent: {account.account_id}"
            )
        if len(account.evidence_locator) < 8 or len(account.qualifying_evidence) < 12:
            raise ValueError(f"underspecified full-text account: {account.account_id}")
        resolution = map_by_id[account.account_id]
        if (
            resolution.parent_id != account.parent_id
            or resolution.resolution_kind != account.account_kind
        ):
            raise ValueError(f"misbound full-text account map: {account.account_id}")
        if resolution.resolution_kind == "embedded_result":
            target = embedded_by_id.get(resolution.target_id)
            if target is None or target.parent_id != account.parent_id:
                raise ValueError(f"missing embedded target: {account.account_id}")
        elif resolution.resolution_kind == "primary_result":
            target = primary_by_id.get(resolution.target_id)
            if target is None or target.parent_id != account.parent_id:
                raise ValueError(f"missing primary target: {account.account_id}")
        else:
            raise ValueError(
                f"invalid full-text resolution for {account.account_id}: "
                f"{resolution.resolution_kind}"
            )
        by_parent[account.parent_id].append(account)

    embedded_account_ids = {
        item.account_id for item in accounts if item.account_kind == "embedded_result"
    }
    primary_account_ids = {
        item.account_id for item in accounts if item.account_kind == "primary_result"
    }
    if embedded_account_ids != set(embedded_by_id):
        raise ValueError("full-text inventory does not exactly carry embedded results")
    if primary_account_ids != set(primary_by_id):
        raise ValueError("full-text inventory does not exactly carry primary results")

    for result in primary_results:
        if not all(getattr(result, field) for field in EMBEDDED_RESULT_FIELDS):
            raise ValueError(f"incomplete primary result: {result.result_id}")
        if result.disposition_code not in (
            RESULT_CODE_DEFINITIONS.keys()
            | CODE_DEFINITIONS["explicit_disposition"].keys()
        ):
            raise ValueError(
                f"unknown primary-result disposition for {result.result_id}"
            )
        if result.primary_source != f"https://arxiv.org/abs/{result.parent_id}":
            raise ValueError(f"primary result has wrong source: {result.result_id}")
        if result.source_card != f"Full-text source {result.parent_id}":
            raise ValueError(
                f"primary result has wrong source binding: {result.result_id}"
            )
        if len(result.disposition) < 40 or len(result.artifact_status) < 20:
            raise ValueError(f"underspecified primary result: {result.result_id}")
        validate_result_disposition(result)

    leidos = embedded_by_id.get("2501.08913:leidos-v1.0.4")
    if leidos is None:
        raise ValueError("Leidos v1.0.4 result is missing")
    leidos_mechanism = leidos.disposition.lower()
    if (
        "unweighted multiclass distilroberta" not in leidos_mechanism
        or "ensemble" in leidos_mechanism
    ):
        raise ValueError("Leidos v1.0.4 mechanism contradicts its primary paper")

    artifact_state: dict[str, tuple[str, str, str]] = {}
    paper_paths: set[str] = set()
    for parent_id, source in fulltext_sources.items():
        row = row_by_id[parent_id]
        if (
            source.title != row.title
            or source.mapping_kind != mappings[parent_id].mapping_kind
        ):
            raise ValueError(f"full-text source metadata mismatch for {parent_id}")
        if not all(getattr(source, field) for field in FULLTEXT_SOURCE_FIELDS):
            raise ValueError(f"incomplete full-text source: {parent_id}")
        if len(source.inspected_scope) < 40 or len(source.reason) < 40:
            raise ValueError(f"underspecified full-text source: {parent_id}")
        try:
            expected_count = int(source.expected_account_count)
        except ValueError as error:
            raise ValueError(f"non-integer account count for {parent_id}") from error
        found_accounts = by_parent[parent_id]
        if expected_count != len(found_accounts):
            raise ValueError(
                f"full-text account count mismatch for {parent_id}: "
                f"expected {expected_count}, found {len(found_accounts)}"
            )
        expected_resolution = (
            "+".join(sorted({item.account_kind for item in found_accounts}))
            if found_accounts
            else "no_qualifying_account"
        )
        if (
            source.resolution != expected_resolution
            or source.resolution not in ALLOWED_FULLTEXT_RESOLUTIONS
        ):
            raise ValueError(f"invalid full-text resolution for {parent_id}")
        if source.paper_path in paper_paths:
            raise ValueError(f"primary PDF reused across sources: {source.paper_path}")
        paper_paths.add(source.paper_path)
        state = (
            _read_fulltext_artifact(paper_root, source)
            if artifacts is None
            else artifacts[parent_id]
        )
        if state[0] != source.pdf_sha256 or state[1] != source.text_sha256:
            raise ValueError(f"preserved full-text artifact mismatch for {parent_id}")
        artifact_state[parent_id] = state

    if set(CONTENT_ANCHOR_ACCOUNTS) != set(CONTENT_ANCHOR_TEXT):
        raise ValueError("content-derived account and text controls differ")
    for parent_id, expected_ids in CONTENT_ANCHOR_ACCOUNTS.items():
        found_ids = {item.account_id for item in by_parent[parent_id]}
        if not expected_ids <= found_ids:
            raise ValueError(
                f"content-derived anchor accounts missing for {parent_id}"
            )
        text = artifact_state[parent_id][2].lower()
        missing_tokens = [
            token
            for token in CONTENT_ANCHOR_TEXT[parent_id]
            if token.lower() not in text
        ]
        if missing_tokens:
            raise ValueError(
                f"content anchors absent from {parent_id}: {', '.join(missing_tokens)}"
            )
    if table_resolutions is not None:
        requirements = table_discovery.content_requirements(table_resolutions)
        for parent_id, expected_ids in requirements.items():
            found_ids = {item.account_id for item in by_parent[parent_id]}
            if not expected_ids <= found_ids:
                missing_ids = sorted(expected_ids - found_ids)
                raise ValueError(
                    "independently discovered table accounts missing for "
                    f"{parent_id}: {', '.join(missing_ids)}"
                )
    return artifact_state


def run_regression_tests(
    rows: list[ExportRow],
    mappings: dict[str, Mapping],
    sources: dict[str, CompositeSource],
    results: list[EmbeddedResult],
    expected_result_ids: dict[str, set[str]],
    source_cards: dict[str, SourceCard],
) -> int:
    tests = 0

    def expect_failure(operation: Callable[[], object], label: str) -> None:
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


def run_fulltext_regression_tests(
    rows: list[ExportRow],
    mappings: dict[str, Mapping],
    fulltext_sources: dict[str, FulltextSource],
    accounts: list[FulltextAccount],
    account_map: list[FulltextAccountMap],
    embedded_results: list[EmbeddedResult],
    primary_results: list[EmbeddedResult],
    paper_root: Path,
    artifacts: dict[str, tuple[str, str, str]],
    table_candidates: list[table_discovery.Candidate],
    table_resolutions: list[table_discovery.Resolution],
) -> int:
    tests = 0

    def expect_failure(operation: Callable[[], object], label: str) -> None:
        nonlocal tests
        try:
            operation()
        except ValueError:
            tests += 1
            return
        raise ValueError(f"full-text negative control unexpectedly passed: {label}")

    expect_failure(
        lambda: table_discovery.validate_resolutions(
            table_candidates, table_resolutions[:-1], accounts
        ),
        "one PDF-derived candidate resolution removed",
    )

    target_index = next(
        index
        for index, item in enumerate(table_resolutions)
        if item.target_account_ids
    )
    unknown_target_resolutions = list(table_resolutions)
    unknown_target_resolutions[target_index] = replace(
        table_resolutions[target_index],
        target_account_ids=("0000.00000:invented",),
    )
    expect_failure(
        lambda: table_discovery.validate_resolutions(
            table_candidates, unknown_target_resolutions, accounts
        ),
        "PDF-derived resolution redirected to an unknown account",
    )

    required_index = next(
        index
        for index, item in enumerate(table_resolutions)
        if "2510.12476:detective-m4" in item.target_account_ids
    )
    hidden_required_resolutions = list(table_resolutions)
    hidden_required_resolutions[required_index] = replace(
        table_resolutions[required_index],
        resolution_kind="nonqualifying_metric_context",
        target_account_ids=(),
        reason=(
            "Negative control falsely suppresses the grouped DeTeCtive M4 "
            "table state despite its directly extracted high cells."
        ),
    )
    expect_failure(
        lambda: table_discovery.validate_resolutions(
            table_candidates, hidden_required_resolutions, accounts
        ),
        "content-required grouped table state reclassified as a false positive",
    )

    mutated_candidates = list(table_candidates)
    mutated_candidates[required_index] = replace(
        table_candidates[required_index], row_label="mutated PDF row"
    )
    expect_failure(
        lambda: table_discovery.validate_resolutions(
            mutated_candidates, table_resolutions, accounts
        ),
        "raw PDF candidate content mutated without updating its resolution",
    )

    row_by_id = {row.arxiv_id: row for row in rows}
    if is_composite_source(row_by_id["2509.00623"], mappings["2509.00623"]):
        raise ValueError(
            "ordinary-title content fixture unexpectedly matches old selector"
        )
    tests += 1

    missing_candace_accounts = [
        item for item in accounts if item.account_id != "2509.00623:candace"
    ]
    missing_candace_map = [
        item for item in account_map if item.account_id != "2509.00623:candace"
    ]
    missing_candace_results = [
        item for item in primary_results if item.result_id != "2509.00623:candace"
    ]
    lowered_candace_sources = dict(fulltext_sources)
    lowered_candace_sources["2509.00623"] = replace(
        fulltext_sources["2509.00623"], expected_account_count="2"
    )
    expect_failure(
        lambda: validate_fulltext(
            rows,
            mappings,
            lowered_candace_sources,
            missing_candace_accounts,
            missing_candace_map,
            embedded_results,
            missing_candace_results,
            paper_root,
            artifacts=artifacts,
        ),
        "ordinary-title Candace result omitted with lowered mutable count",
    )

    non_anchor_id = "2501.03940:ens-gpt2-llama-qwen"
    missing_non_anchor_accounts = [
        item for item in accounts if item.account_id != non_anchor_id
    ]
    missing_non_anchor_map = [
        item for item in account_map if item.account_id != non_anchor_id
    ]
    missing_non_anchor_results = [
        item for item in primary_results if item.result_id != non_anchor_id
    ]
    lowered_non_anchor_sources = dict(fulltext_sources)
    lowered_non_anchor_sources["2501.03940"] = replace(
        fulltext_sources["2501.03940"], expected_account_count="10"
    )
    expect_failure(
        lambda: validate_fulltext(
            rows,
            mappings,
            lowered_non_anchor_sources,
            missing_non_anchor_accounts,
            missing_non_anchor_map,
            embedded_results,
            missing_non_anchor_results,
            paper_root,
            artifacts=artifacts,
        ),
        "non-anchor primary result omitted with lowered mutable count",
    )

    fitted_baseline_id = "2501.03940:m4-roberta-base"
    missing_fitted_baseline_accounts = [
        item for item in accounts if item.account_id != fitted_baseline_id
    ]
    missing_fitted_baseline_map = [
        item for item in account_map if item.account_id != fitted_baseline_id
    ]
    missing_fitted_baseline_results = [
        item for item in primary_results if item.result_id != fitted_baseline_id
    ]
    lowered_fitted_baseline_sources = dict(fulltext_sources)
    lowered_fitted_baseline_sources["2501.03940"] = replace(
        fulltext_sources["2501.03940"], expected_account_count="12"
    )
    expect_failure(
        lambda: validate_fulltext(
            rows,
            mappings,
            lowered_fitted_baseline_sources,
            missing_fitted_baseline_accounts,
            missing_fitted_baseline_map,
            embedded_results,
            missing_fitted_baseline_results,
            paper_root,
            artifacts=artifacts,
            table_resolutions=table_resolutions,
        ),
        "PDF-discovered fitted RoBERTa baseline omitted with lowered count",
    )

    collapsed_state_id = "2607.03680:vanilla-mirage-large"
    collapsed_state_accounts = [
        item for item in accounts if item.account_id != collapsed_state_id
    ]
    collapsed_state_map = [
        item for item in account_map if item.account_id != collapsed_state_id
    ]
    collapsed_state_results = [
        item for item in primary_results if item.result_id != collapsed_state_id
    ]
    collapsed_state_sources = dict(fulltext_sources)
    collapsed_state_sources["2607.03680"] = replace(
        fulltext_sources["2607.03680"], expected_account_count="5"
    )
    expect_failure(
        lambda: validate_fulltext(
            rows,
            mappings,
            collapsed_state_sources,
            collapsed_state_accounts,
            collapsed_state_map,
            embedded_results,
            collapsed_state_results,
            paper_root,
            artifacts=artifacts,
            table_resolutions=table_resolutions,
        ),
        "PDF-discovered MIRAGE training state collapsed with lowered count",
    )

    inherited_reader_blocker = [
        replace(
            item,
            disposition_code="exclude_generation",
            disposition=(
                "The ImBD baseline inherits READER's autoregressive generation "
                "boundary and is therefore excluded."
            ),
        )
        if item.result_id == "2605.25281:imbd-read"
        else item
        for item in primary_results
    ]
    expect_failure(
        lambda: validate_fulltext(
            rows,
            mappings,
            fulltext_sources,
            accounts,
            account_map,
            embedded_results,
            inherited_reader_blocker,
            paper_root,
            artifacts=artifacts,
            table_resolutions=table_resolutions,
        ),
        "ImBD baseline falsely inherits READER generation exclusion",
    )

    non_english_id = "2509.00731:qwen-r16"
    missing_non_english_accounts = [
        item for item in accounts if item.account_id != non_english_id
    ]
    missing_non_english_map = [
        item for item in account_map if item.account_id != non_english_id
    ]
    missing_non_english_results = [
        item for item in primary_results if item.result_id != non_english_id
    ]
    lowered_non_english_sources = dict(fulltext_sources)
    lowered_non_english_sources["2509.00731"] = replace(
        fulltext_sources["2509.00731"], expected_account_count="8"
    )
    expect_failure(
        lambda: validate_fulltext(
            rows,
            mappings,
            lowered_non_english_sources,
            missing_non_english_accounts,
            missing_non_english_map,
            embedded_results,
            missing_non_english_results,
            paper_root,
            artifacts=artifacts,
        ),
        "non-English Qwen LoRA state omitted with lowered mutable count",
    )

    detached_content_artifacts = dict(artifacts)
    original = artifacts["2509.00731"]
    detached_content_artifacts["2509.00731"] = (
        original[0],
        original[1],
        original[2].replace("0.9594", "omitted metric"),
    )
    expect_failure(
        lambda: validate_fulltext(
            rows,
            mappings,
            fulltext_sources,
            accounts,
            account_map,
            embedded_results,
            primary_results,
            paper_root,
            artifacts=detached_content_artifacts,
        ),
        "non-English account inventory detached from table content",
    )

    narrow_domain_id = "2605.27921:chatgpt-d"
    missing_narrow_domain_accounts = [
        item for item in accounts if item.account_id != narrow_domain_id
    ]
    missing_narrow_domain_map = [
        item for item in account_map if item.account_id != narrow_domain_id
    ]
    missing_narrow_domain_results = [
        item for item in primary_results if item.result_id != narrow_domain_id
    ]
    lowered_narrow_domain_sources = dict(fulltext_sources)
    lowered_narrow_domain_sources["2605.27921"] = replace(
        fulltext_sources["2605.27921"], expected_account_count="12"
    )
    expect_failure(
        lambda: validate_fulltext(
            rows,
            mappings,
            lowered_narrow_domain_sources,
            missing_narrow_domain_accounts,
            missing_narrow_domain_map,
            embedded_results,
            missing_narrow_domain_results,
            paper_root,
            artifacts=artifacts,
        ),
        "narrow-domain ChatGPT-D result omitted with lowered mutable count",
    )

    detached_narrow_domain_artifacts = dict(artifacts)
    original = artifacts["2605.27921"]
    detached_narrow_domain_artifacts["2605.27921"] = (
        original[0],
        original[1],
        original[2].replace("ChatGPT-D", "omitted result"),
    )
    expect_failure(
        lambda: validate_fulltext(
            rows,
            mappings,
            fulltext_sources,
            accounts,
            account_map,
            embedded_results,
            primary_results,
            paper_root,
            artifacts=detached_narrow_domain_artifacts,
        ),
        "narrow-domain account inventory detached from table content",
    )

    detached_zero_artifacts = dict(artifacts)
    original = artifacts["2605.14240"]
    detached_zero_artifacts["2605.14240"] = (
        original[0],
        original[1],
        original[2].replace("0.8061", "omitted metric"),
    )
    expect_failure(
        lambda: validate_fulltext(
            rows,
            mappings,
            fulltext_sources,
            accounts,
            account_map,
            embedded_results,
            primary_results,
            paper_root,
            artifacts=detached_zero_artifacts,
        ),
        "no-account decision detached from sub-threshold table evidence",
    )

    wrong_text_sources = dict(fulltext_sources)
    wrong_text_sources["2503.22338"] = replace(
        fulltext_sources["2503.22338"], text_sha256="0" * 64
    )
    expect_failure(
        lambda: validate_fulltext(
            rows,
            mappings,
            wrong_text_sources,
            accounts,
            account_map,
            embedded_results,
            primary_results,
            paper_root,
            artifacts=artifacts,
        ),
        "full-text extraction hash detached from preserved PDF",
    )

    inherited_lapd_blocker = [
        replace(
            item,
            disposition=(
                "The Binoculars comparator inherits LAPD's auxiliary sampling, "
                "violating the multi-perturbation constraint."
            ),
        )
        if item.result_id == "2604.16923:binoculars"
        else item
        for item in primary_results
    ]
    expect_failure(
        lambda: validate_fulltext(
            rows,
            mappings,
            fulltext_sources,
            accounts,
            account_map,
            embedded_results,
            inherited_lapd_blocker,
            paper_root,
            artifacts=artifacts,
        ),
        "retained comparator falsely inherits the parent method exclusion",
    )

    inherited_dna_blocker = [
        replace(
            item,
            disposition_code="exclude_regeneration",
            disposition=(
                "The Binoculars comparator constructs DNA-DetectLLM's ideal "
                "sequence, violating the no-regeneration boundary."
            ),
        )
        if item.result_id == "2509.15550:binoculars"
        else item
        for item in primary_results
    ]
    expect_failure(
        lambda: validate_fulltext(
            rows,
            mappings,
            fulltext_sources,
            accounts,
            account_map,
            embedded_results,
            inherited_dna_blocker,
            paper_root,
            artifacts=artifacts,
        ),
        "retained baseline falsely inherits DNA-DetectLLM regeneration",
    )

    ensemble_leidos = [
        replace(
            item,
            disposition=(
                "A separately submitted ensemble variant has no distinct public "
                "state and therefore remains only a reported shared-task result."
            ),
        )
        if item.result_id == "2501.08913:leidos-v1.0.4"
        else item
        for item in embedded_results
    ]
    expect_failure(
        lambda: validate_fulltext(
            rows,
            mappings,
            fulltext_sources,
            accounts,
            account_map,
            ensemble_leidos,
            primary_results,
            paper_root,
            artifacts=artifacts,
        ),
        "Leidos v1.0.4 falsely described as an ensemble",
    )

    missing_source = dict(fulltext_sources)
    missing_source.pop("2608.03859")
    expect_failure(
        lambda: validate_fulltext(
            rows,
            mappings,
            missing_source,
            accounts,
            account_map,
            embedded_results,
            primary_results,
            paper_root,
            artifacts=artifacts,
        ),
        "one of 119 full-text source audits removed",
    )
    return tests


def write_audit(
    path: Path,
    rows: list[ExportRow],
    mappings: dict[str, Mapping],
    sources: dict[str, CompositeSource],
    results: list[EmbeddedResult],
    fulltext_sources: dict[str, FulltextSource],
    accounts: list[FulltextAccount],
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
        "fulltext_resolution",
        "fulltext_account_count",
        "fulltext_paper_path",
        "fulltext_pdf_sha256",
        "fulltext_text_sha256",
        "fulltext_reason",
    )
    result_counts: dict[str, int] = {}
    for result in results:
        result_counts[result.parent_id] = result_counts.get(result.parent_id, 0) + 1
    account_counts: dict[str, int] = {}
    for account in accounts:
        account_counts[account.parent_id] = account_counts.get(account.parent_id, 0) + 1
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(
            target, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        for row in rows:
            flags, evidence = semantic_flags(row)
            mapping = mappings[row.arxiv_id]
            source = sources.get(row.arxiv_id)
            fulltext = fulltext_sources[row.arxiv_id]
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
                    "fulltext_resolution": fulltext.resolution,
                    "fulltext_account_count": account_counts.get(row.arxiv_id, 0),
                    "fulltext_paper_path": fulltext.paper_path,
                    "fulltext_pdf_sha256": fulltext.pdf_sha256,
                    "fulltext_text_sha256": fulltext.text_sha256,
                    "fulltext_reason": fulltext.reason,
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


def write_fulltext_account_audit(
    path: Path,
    rows: list[ExportRow],
    mappings: dict[str, Mapping],
    fulltext_sources: dict[str, FulltextSource],
    accounts: list[FulltextAccount],
    account_map: list[FulltextAccountMap],
    embedded_results: list[EmbeddedResult],
    primary_results: list[EmbeddedResult],
) -> None:
    row_by_id = {row.arxiv_id: row for row in rows}
    resolution_by_id = {item.account_id: item for item in account_map}
    result_by_id = {
        item.result_id: item for item in (*embedded_results, *primary_results)
    }
    fields = (
        *FULLTEXT_ACCOUNT_FIELDS,
        "parent_title",
        "paper_path",
        "pdf_sha256",
        "text_sha256",
        "resolution_kind",
        "target_id",
        "target_disposition_code",
        "target_disposition",
        "target_artifact_status",
    )
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(
            target, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        for account in sorted(
            accounts, key=lambda item: (item.parent_id, item.account_id)
        ):
            resolution = resolution_by_id[account.account_id]
            result = result_by_id.get(resolution.target_id)
            mapping = mappings[account.parent_id]
            source = fulltext_sources[account.parent_id]
            writer.writerow(
                {
                    **{
                        field: getattr(account, field)
                        for field in FULLTEXT_ACCOUNT_FIELDS
                    },
                    "parent_title": row_by_id[account.parent_id].title,
                    "paper_path": source.paper_path,
                    "pdf_sha256": source.pdf_sha256,
                    "text_sha256": source.text_sha256,
                    "resolution_kind": resolution.resolution_kind,
                    "target_id": resolution.target_id,
                    "target_disposition_code": (
                        result.disposition_code
                        if result is not None
                        else mapping.disposition_code
                    ),
                    "target_disposition": (
                        result.disposition if result is not None else mapping.reason
                    ),
                    "target_artifact_status": (
                        result.artifact_status if result is not None else mapping.reason
                    ),
                }
            )


def write_environment(path: Path) -> None:
    completed = subprocess.run(
        ["pdftotext", "-v"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    pdftotext_version = (completed.stderr or completed.stdout).splitlines()[0]
    path.write_text(
        f"python={sys.version.replace(chr(10), ' ')}\n"
        f"implementation={platform.python_implementation()}\n"
        f"platform={platform.platform()}\n"
        f"pdftotext={pdftotext_version}\n"
        "extraction_command=pdftotext -layout -enc UTF-8 PAPER -\n"
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
    fulltext_sources_path: Path,
    fulltext_accounts_path: Path,
    account_map_path: Path,
    primary_results_path: Path,
    table_candidates_path: Path,
    table_discovery_path: Path,
    paper_root: Path,
    audit_path: Path,
    embedded_audit_path: Path,
    fulltext_audit_path: Path,
    environment_path: Path,
    rows: list[ExportRow],
    raw_rows: int,
    mappings: dict[str, Mapping],
    sources: dict[str, CompositeSource],
    results: list[EmbeddedResult],
    fulltext_sources: dict[str, FulltextSource],
    accounts: list[FulltextAccount],
    primary_results: list[EmbeddedResult],
    table_candidates: list[table_discovery.Candidate],
    composite_regression_tests: int,
    fulltext_regression_tests: int,
) -> str:
    n_flagged = sum(bool(semantic_flags(row)[0]) for row in rows)
    n_explicit = sum(
        mapping.mapping_kind == "explicit_disposition" for mapping in mappings.values()
    )
    n_non_candidate = len(mappings) - n_explicit
    n_composite_required = sum(
        is_composite_source(row, mappings[row.arxiv_id]) for row in rows
    )
    command = (
        "uv run --isolated --no-project --python 3.13 python audit_coverage.py "
        "--map coverage_row_dispositions.tsv "
        "--composite-sources coverage_composite_sources.tsv "
        "--embedded-results coverage_embedded_results.tsv "
        "--expected-results coverage_expected_result_ids.tsv "
        "--source-cards coverage_composite_dispositions.md "
        "--fulltext-sources coverage_fulltext_sources.tsv "
        "--fulltext-accounts coverage_fulltext_expected_accounts.tsv "
        "--account-map coverage_fulltext_account_map.tsv "
        "--primary-results coverage_primary_results.tsv "
        "--table-candidates coverage_table_candidates.tsv "
        "--table-discovery coverage_table_discovery.tsv "
        f"--paper-root {paper_root} "
        "--output coverage_semantic_audit.tsv "
        "--embedded-output coverage_embedded_result_audit.tsv "
        "--fulltext-output coverage_fulltext_account_audit.tsv "
        "--report coverage_semantic_audit_report.txt "
        "--environment coverage_semantic_audit_environment.txt"
    )
    lines = [
        f"command={command}",
        f"raw_export_rows={raw_rows}",
        f"unique_2025_2026_rows={len(rows)}",
        f"semantically_flagged_rows={n_flagged}",
        f"explicit_dispositions={n_explicit}",
        f"non_candidate_classes={n_non_candidate}",
        f"mapping_rows={len(mappings)}",
        f"composite_required_rows={n_composite_required}",
        f"composite_review_rows={len(sources)}",
        f"embedded_result_rows={len(results)}",
        f"fulltext_source_rows={len(fulltext_sources)}",
        f"fulltext_account_rows={len(accounts)}",
        f"primary_result_rows={len(primary_results)}",
        f"independent_table_candidates={len(table_candidates)}",
        f"composite_regression_controls={composite_regression_tests}",
        f"fulltext_regression_controls={fulltext_regression_tests}",
        "regression_and_negative_controls="
        f"{composite_regression_tests + fulltext_regression_tests}",
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
            f"sha256 {fulltext_sources_path.name}={sha256(fulltext_sources_path)}",
            f"sha256 {fulltext_accounts_path.name}={sha256(fulltext_accounts_path)}",
            f"sha256 {account_map_path.name}={sha256(account_map_path)}",
            f"sha256 {primary_results_path.name}={sha256(primary_results_path)}",
            f"sha256 {table_candidates_path.name}={sha256(table_candidates_path)}",
            f"sha256 {table_discovery_path.name}={sha256(table_discovery_path)}",
            f"sha256 {audit_path.name}={sha256(audit_path)}",
            f"sha256 {embedded_audit_path.name}={sha256(embedded_audit_path)}",
            f"sha256 {fulltext_audit_path.name}={sha256(fulltext_audit_path)}",
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
    parser.add_argument("--fulltext-sources", type=Path)
    parser.add_argument("--fulltext-accounts", type=Path)
    parser.add_argument("--account-map", type=Path)
    parser.add_argument("--primary-results", type=Path)
    parser.add_argument("--table-candidates", type=Path)
    parser.add_argument("--table-discovery", type=Path)
    parser.add_argument("--paper-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--embedded-output", type=Path)
    parser.add_argument("--fulltext-output", type=Path)
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
        args.fulltext_sources,
        args.fulltext_accounts,
        args.account_map,
        args.primary_results,
        args.table_candidates,
        args.table_discovery,
        args.paper_root,
        args.output,
        args.embedded_output,
        args.fulltext_output,
        args.report,
        args.environment,
    )
    if any(path is None for path in required):
        raise ValueError(
            "--map, --composite-sources, --embedded-results, --expected-results, "
            "--source-cards, --fulltext-sources, --fulltext-accounts, "
            "--account-map, --primary-results, --paper-root, --output, "
            "--table-candidates, --table-discovery, "
            "--embedded-output, --fulltext-output, --report, and --environment "
            "are required"
        )
    (
        map_path,
        composite_sources_path,
        embedded_results_path,
        expected_results_path,
        source_cards_path,
        fulltext_sources_path,
        fulltext_accounts_path,
        account_map_path,
        primary_results_path,
        table_candidates_path,
        table_discovery_path,
        paper_root,
        output_path,
        embedded_output_path,
        fulltext_output_path,
        report_path,
        environment_path,
    ) = required
    mappings = load_mappings(map_path)
    sources = load_composite_sources(composite_sources_path)
    results = load_embedded_results(embedded_results_path)
    expected_result_ids = load_expected_result_ids(expected_results_path)
    source_cards = load_source_cards(source_cards_path)
    fulltext_sources = load_fulltext_sources(fulltext_sources_path)
    fulltext_accounts = load_fulltext_accounts(fulltext_accounts_path)
    fulltext_account_map = load_fulltext_account_map(account_map_path)
    primary_results = load_primary_results(primary_results_path)
    validate(rows, mappings)
    validate_composites(
        rows, mappings, sources, results, expected_result_ids, source_cards
    )
    table_candidates, table_resolutions = validate_table_discovery(
        fulltext_sources_path,
        fulltext_accounts_path,
        table_candidates_path,
        table_discovery_path,
        paper_root,
    )
    artifacts = validate_fulltext(
        rows,
        mappings,
        fulltext_sources,
        fulltext_accounts,
        fulltext_account_map,
        results,
        primary_results,
        paper_root,
        table_resolutions=table_resolutions,
    )
    composite_regression_tests = run_regression_tests(
        rows, mappings, sources, results, expected_result_ids, source_cards
    )
    fulltext_regression_tests = run_fulltext_regression_tests(
        rows,
        mappings,
        fulltext_sources,
        fulltext_accounts,
        fulltext_account_map,
        results,
        primary_results,
        paper_root,
        artifacts,
        table_candidates,
        table_resolutions,
    )
    write_audit(
        output_path,
        rows,
        mappings,
        sources,
        results,
        fulltext_sources,
        fulltext_accounts,
    )
    write_embedded_audit(embedded_output_path, rows, results)
    write_fulltext_account_audit(
        fulltext_output_path,
        rows,
        mappings,
        fulltext_sources,
        fulltext_accounts,
        fulltext_account_map,
        results,
        primary_results,
    )
    write_environment(environment_path)
    report = write_report(
        report_path,
        source_dir,
        map_path,
        composite_sources_path,
        embedded_results_path,
        expected_results_path,
        source_cards_path,
        fulltext_sources_path,
        fulltext_accounts_path,
        account_map_path,
        primary_results_path,
        table_candidates_path,
        table_discovery_path,
        paper_root,
        output_path,
        embedded_output_path,
        fulltext_output_path,
        environment_path,
        rows,
        raw_rows,
        mappings,
        sources,
        results,
        fulltext_sources,
        fulltext_accounts,
        primary_results,
        table_candidates,
        composite_regression_tests,
        fulltext_regression_tests,
    )
    print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
