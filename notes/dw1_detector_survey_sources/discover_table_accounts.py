#!/usr/bin/env python3
"""Extract and resolve high-metric table rows from the frozen PDF corpus."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


TABLE_PATTERN = re.compile(r"(?:^|\s{2,})table\s+[a-z]?[0-9]+\b", re.IGNORECASE)
SECTION_PATTERN = re.compile(
    r"(?:no training on RAID|\d+\s+epoch(?:s)?\s+fine[- ]tun(?:e|ing)|"
    r"without fine[- ]tuning|with fine[- ]tuning)",
    re.IGNORECASE,
)
METRIC_HEADER_PATTERN = re.compile(
    r"\b(?:auc|auroc|roc[- ]auc|accuracy|balanced accuracy|bacc|macro[- ]?f1|"
    r"f1|precision|recall|tpr|true positive rate|humanrec|machinerec|avgrec)\b",
    re.IGNORECASE,
)
DECIMAL_METRIC_PATTERN = re.compile(r"(?<![\d.])(?:0?\.9\d*|1(?:\.0+)?)(?![\d.])")
PERCENT_METRIC_PATTERN = re.compile(
    r"(?<![\d.])(?:9\d(?:\.\d+)?|100(?:\.0+)?)\s*%(?!\d)"
)
WIDE_METRIC_PATTERN = re.compile(r"(?<![\d.])(?:9\d(?:\.\d+)?|100(?:\.0+)?)(?![\d.])")
NUMBER_PATTERN = re.compile(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?%?")
SPACE_PATTERN = re.compile(r"\s+")
CONTROL_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
FIELDS = (
    "parent_id",
    "candidate_id",
    "page",
    "line",
    "table_locator",
    "trigger",
    "row_label",
    "context",
)
RESOLUTION_FIELDS = FIELDS + (
    "resolution_kind",
    "target_account_ids",
    "reason",
)
ALLOWED_RESOLUTIONS = {
    "account_evidence",
    "targeted_carry_forward",
    "duplicate_operating_point",
    "non_detector_row",
    "diagnostic_or_component",
    "table_heading_or_prose",
    "nonqualifying_metric_context",
}


def _ids(value: str) -> set[str]:
    return {item for item in value.split() if item}


# These are the exact states added after the evaluator's full-table challenge.  Each
# must be rediscovered from PDF table content and bound to its own account.
CONTENT_REQUIRED_ACCOUNT_IDS = {
    "2501.03940": _ids("""
2501.03940:radar-ft 2501.03940:m4-roberta-base
2501.03940:m4-xlm-roberta 2501.03940:mage-longformer 2501.03940:gltr
2501.03940:raid-rb-gpt2 2501.03940:raid-rl-gpt2 2501.03940:raid-rb-cgpt
2501.03940:raid-radar 2501.03940:raid-fastdetectgpt 2501.03940:raid-binoculars
2501.03940:raid-gptzero 2501.03940:raid-originality 2501.03940:raid-winston
2501.03940:raid-zerogpt 2501.03940:mage-roberta-base 2501.03940:mage-radar-ptm
2501.03940:raidft-pawn-gpt2 2501.03940:raidft-pawn-llama
2501.03940:raidft-longformer 2501.03940:raidft-roberta
2501.03940:raidft-radar-ptm 2501.03940:raidft-radar
"""),
    "2607.22026": _ids("""
2607.22026:multilevel-energy 2607.22026:energy-norm
2607.22026:window-std 2607.22026:equal-hard 2607.22026:equal-soft
2607.22026:calibrated-hard 2607.22026:calibrated-soft
"""),
    "2607.03680": _ids("""
2607.03680:anchor 2607.03680:mage-longformer 2607.03680:llmdetectaive
2607.03680:faid 2607.03680:vanilla-faid-extra-domain
2607.03680:vanilla-faid-extra-domain-generator 2607.03680:detectanyllm
2607.03680:vanilla-mirage-base 2607.03680:fomaml-hc3-k5
2607.03680:fomaml-hc3-k20 2607.03680:fomaml-hc3-k50
2607.03680:reverse-confidence-ensemble 2607.03680:pooled-four-way
2607.03680:pooled-stratified-base 2607.03680:pooled-stratified-large
"""),
    "2606.02158": _ids("""
2606.02158:likelihood 2606.02158:logrank 2606.02158:detectlrr
2606.02158:lastde 2606.02158:detectgpt 2606.02158:detectnpr
2606.02158:dnagpt 2606.02158:fastdetectgpt 2606.02158:lastde-plus
2606.02158:without-low-probability 2606.02158:without-entropy
"""),
    "2605.25281": _ids("""
2605.25281:biscope-read 2605.25281:biscope-target-adapted
2605.25281:npr-gemma 2605.25281:npr-qwen
2605.25281:detectgpt-gemma 2605.25281:detectgpt-qwen
2605.25281:binoculars-gemma 2605.25281:radar
2605.25281:fastdetectgpt-gemma 2605.25281:adadetectgpt-gemma
2605.25281:adadetectgpt-gemma-target
"""),
    "2602.08031": _ids("""
2602.08031:likelihood 2602.08031:logrank 2602.08031:entropy
2602.08031:detectgpt 2602.08031:fastgpt 2602.08031:dnagpt
2602.08031:repreguard 2602.08031:lastde 2602.08031:fouriergpt
2602.08031:binoculars
"""),
    "2508.11343": _ids("""
2508.11343:likelihood 2508.11343:logrank 2508.11343:entropy
2508.11343:detectlrr 2508.11343:lastde 2508.11343:detectgpt
2508.11343:detectnpr 2508.11343:dnagpt 2508.11343:fastdetectgpt
2508.11343:lastde-plus
"""),
    "2606.07313": _ids("""
2606.07313:polish-only 2606.07313:three-task
"""),
    "2506.01702": _ids("""
2506.01702:tfidf-baseline
"""),
    "2509.15550": _ids("""
2509.15550:revise-detect
"""),
    "2605.06903": _ids("""
2605.06903:roberta-chatgpt-meld 2605.06903:modernbert-detect-meld
2605.06903:repreguard-meld
"""),
    "2604.21223": _ids("""
2604.21223:reward-model-deberta
"""),
    "2606.00016": _ids("""
2606.00016:superannotate-roberta
"""),
    "2505.14271": _ids("""
2505.14271:faid-unsup-simcse-xlmr
"""),
    "2511.21744": _ids("""
2511.21744:ai-generated-text-detection 2511.21744:detective-comparator
2511.21744:restricted-embeddings 2511.21744:chatgpt-detector
2511.21744:roberta-bilstm
"""),
    "2509.18880": _ids("""
2509.18880:e5-small-lora 2509.18880:desklib 2509.18880:superannotate
"""),
    "2506.15683": _ids("""
2506.15683:full 2506.15683:roberta-baseline
2506.15683:t5-sentinel-baseline 2506.15683:detective-baseline
2506.15683:seqxgpt-baseline 2506.15683:dna-gpt-baseline
2506.15683:detectgpt-baseline 2506.15683:fastdetectgpt-baseline
2506.15683:hastewire
"""),
    "2506.06705": _ids("""
2506.06705:roberta-base 2506.06705:roberta-large 2506.06705:entropy
2506.06705:rank 2506.06705:logrank 2506.06705:likelihood
2506.06705:detectgpt 2506.06705:fastdetectgpt 2506.06705:binoculars
2506.06705:without-adaptation 2506.06705:divscore-mistral
2506.06705:divscore-falcon 2506.06705:divscore-qwen
2506.06705:divscore-llama 2506.06705:entropy-mistral
2506.06705:entropy-falcon 2506.06705:entropy-qwen
2506.06705:entropy-llama 2506.06705:cross-entropy-qwen
"""),
    "2509.26051": _ids("""
2509.26051:llama-3.2-3b 2509.26051:mdeberta-v3-base
2509.26051:gemma-2-2b 2509.26051:xlm-roberta-base
2509.26051:llama-news-hr-hu-cs 2509.26051:llama-tpr-pl
2509.26051:mdeberta-generator-de-pl-hr-hu-cs
2509.26051:mdeberta-news-cs 2509.26051:mdeberta-social-de
2509.26051:mdeberta-tpr-de-pl-hr-hu
2509.26051:gemma-social-de-pl-hr-hu-cs
2509.26051:gemma-tpr-de-pl-hr-hu
2509.26051:xlm-social-de-pl 2509.26051:xlm-tpr-de-cs
2509.26051:fastdetectgpt 2509.26051:binoculars
2509.26051:llm-deviation
"""),
    "2604.16607": _ids("""
2604.16607:binoculars 2604.16607:fdg-gpt-neo 2604.16607:fdg-gpt-j
2604.16607:fdg-falcon-7b 2604.16607:zippy-lzma
2604.16607:zippy-ensemble 2604.16607:biscope-arxiv
2604.16607:biscope-yelp 2604.16607:biscope-essay
2604.16607:biscope-creative 2604.16607:detective-mage
2604.16607:detective-m4gt 2604.16607:detective-outfox
2604.16607:detective-turingbench 2604.16607:roberta-h3c-plus
2604.16607:roberta-m4gt 2604.16607:roberta-mage
2604.16607:roberta-raid 2604.16607:stylo-h3c-plus
2604.16607:mcgovern-h3c-plus 2604.16607:mcgovern-m4gt
2604.16607:mcgovern-mage
"""),
    "2510.12476": _ids("""
2510.12476:lastde 2510.12476:lastde-plus-plus
2510.12476:log-likelihood 2510.12476:logrank
2510.12476:detect-lrr 2510.12476:fastdetectgpt
2510.12476:roberta-m4 2510.12476:detective-m4
"""),
}


# Parent-local content aliases handle typography and distinguish repeated fitted
# states whose printed names are identical.  Generic account matching handles all
# remaining inventory rows.
LOCAL_RULES: tuple[tuple[str, re.Pattern[str], re.Pattern[str], tuple[str, ...]], ...] = (
    ("2501.03940", re.compile(r"^XLM[- ]?RoBERTa", re.I), re.compile(r"Table 9", re.I), ("2501.03940:m4-xlm-roberta",)),
    ("2501.03940", re.compile(r"^R-B GPT2", re.I), re.compile(r"Table 10", re.I), ("2501.03940:raid-rb-gpt2",)),
    ("2501.03940", re.compile(r"^R-L GPT2", re.I), re.compile(r"Table 10", re.I), ("2501.03940:raid-rl-gpt2",)),
    ("2501.03940", re.compile(r"^R-B CGPT", re.I), re.compile(r"Table 10", re.I), ("2501.03940:raid-rb-cgpt",)),
    ("2501.03940", re.compile(r"^F-DetectGPT", re.I), re.compile(r"Table 10", re.I), ("2501.03940:raid-fastdetectgpt",)),
    ("2501.03940", re.compile(r"^GPTZero", re.I), re.compile(r"Table 10", re.I), ("2501.03940:raid-gptzero",)),
    ("2501.03940", re.compile(r"^Originality", re.I), re.compile(r"Table 10", re.I), ("2501.03940:raid-originality",)),
    ("2501.03940", re.compile(r"^Winston", re.I), re.compile(r"Table 10", re.I), ("2501.03940:raid-winston",)),
    ("2501.03940", re.compile(r"^ZeroGPT", re.I), re.compile(r"Table 10", re.I), ("2501.03940:raid-zerogpt",)),
    ("2501.03940", re.compile(r"^PAWN\s*\(GPT2\)", re.I), re.compile(r"Table 10.*1 epoch", re.I), ("2501.03940:raidft-pawn-gpt2",)),
    ("2501.03940", re.compile(r"^PAWN\s*\(Llama", re.I), re.compile(r"Table 10.*1 epoch", re.I), ("2501.03940:raidft-pawn-llama",)),
    ("2501.03940", re.compile(r"^Longformer", re.I), re.compile(r"Table 10.*1 epoch", re.I), ("2501.03940:raidft-longformer",)),
    ("2501.03940", re.compile(r"^RoBERTa", re.I), re.compile(r"Table 10.*1 epoch", re.I), ("2501.03940:raidft-roberta",)),
    ("2501.03940", re.compile(r"^RADAR-PTM", re.I), re.compile(r"Table 10.*1 epoch", re.I), ("2501.03940:raidft-radar-ptm",)),
    ("2501.03940", re.compile(r"^RADAR(?:\s|$)", re.I), re.compile(r"Table 10.*1 epoch", re.I), ("2501.03940:raidft-radar",)),
    ("2501.03940", re.compile(r"^Longformer", re.I), re.compile(r"Table 10", re.I), ("2501.03940:mage-longformer",)),
    ("2501.03940", re.compile(r"^RoBERTa", re.I), re.compile(r"Table 10", re.I), ("2501.03940:mage-roberta-base",)),
    ("2501.03940", re.compile(r"^RADAR-PTM", re.I), re.compile(r"Table 10", re.I), ("2501.03940:mage-radar-ptm",)),
    ("2501.03940", re.compile(r"^RADAR(?:\s|$)", re.I), re.compile(r"Table 10", re.I), ("2501.03940:raid-radar",)),
    ("2501.03940", re.compile(r"^Binoculars", re.I), re.compile(r"Table 10", re.I), ("2501.03940:raid-binoculars",)),
    ("2501.03940", re.compile(r"^GLTR", re.I), re.compile(r"Table (?:4|5|10)", re.I), ("2501.03940:gltr",)),
    ("2607.03680", re.compile(r"^Longformer", re.I), re.compile(r"Table 3", re.I), ("2607.03680:mage-longformer",)),
    ("2607.03680", re.compile(r"^Vanilla\s*\+\s*extra", re.I), re.compile(r"Table 4", re.I), ("2607.03680:vanilla-faid-extra-domain", "2607.03680:vanilla-faid-extra-domain-generator")),
    ("2607.03680", re.compile(r"^Vanilla\s*\(base\)", re.I), re.compile(r"Table 8", re.I), ("2607.03680:vanilla-mirage-base",)),
    ("2605.25281", re.compile(r"^NPR", re.I), re.compile(r"Table (?:8|9|14)", re.I), ("2605.25281:npr-gemma",)),
    ("2605.25281", re.compile(r"^NPR", re.I), re.compile(r"Table (?:10|11|15)", re.I), ("2605.25281:npr-qwen",)),
    ("2605.25281", re.compile(r"^D\s*ETECT\s*GPT|^DetectGPT", re.I), re.compile(r"Table (?:8|9|14)", re.I), ("2605.25281:detectgpt-gemma",)),
    ("2605.25281", re.compile(r"^D\s*ETECT\s*GPT|^DetectGPT", re.I), re.compile(r"Table (?:10|11|15)", re.I), ("2605.25281:detectgpt-qwen",)),
    ("2605.25281", re.compile(r"^B\s*INOCULARS|^Binoculars", re.I), re.compile(r"Table (?:8|9|14)", re.I), ("2605.25281:binoculars-gemma",)),
    ("2605.25281", re.compile(r"^B\s*I\s*SCOPE\s*[∗*]", re.I), re.compile(r"Table (?:3|14)", re.I), ("2605.25281:biscope-target-adapted",)),
    ("2605.25281", re.compile(r"^B\s*I\s*SCOPE", re.I), re.compile(r"Table (?:2|3|14|15)", re.I), ("2605.25281:biscope-read",)),
    ("2605.25281", re.compile(r"^A\s*DA\s*D\s*ETECT\s*GPT\s*[∗*]", re.I), re.compile(r"Table 14", re.I), ("2605.25281:adadetectgpt-gemma-target",)),
    ("2605.25281", re.compile(r"^A\s*DA\s*D\s*ETECT\s*GPT", re.I), re.compile(r"Table (?:8|9|14)", re.I), ("2605.25281:adadetectgpt-gemma",)),
    ("2501.03940", re.compile(r"XLM[- ]?RoBERTa", re.I), re.compile(r"Table 9", re.I), ("2501.03940:m4-xlm-roberta",)),
    ("2501.03940", re.compile(r"^RoBERTa", re.I), re.compile(r"Table 9", re.I), ("2501.03940:m4-roberta-base",)),
    ("2501.03940", re.compile(r"^Longformer", re.I), re.compile(r"Table (?:4|5)", re.I), ("2501.03940:mage-longformer",)),
    ("2501.03940", re.compile(r"^None", re.I), re.compile(r"Table 12", re.I), ("2501.03940:raid-rb-cgpt",)),
    ("2607.03680", re.compile(r"^FAID(?:\s|$)", re.I), re.compile(r"Table 4", re.I), ("2607.03680:faid",)),
    ("2607.03680", re.compile(r"^IntelLabs\s*\(base\)", re.I), re.compile(r"Table 5", re.I), ("2607.03680:vanilla-intellabs-base",)),
    ("2607.03680", re.compile(r"^MAGE\s*\(large\)", re.I), re.compile(r"Table 5", re.I), ("2607.03680:vanilla-mage-large",)),
    ("2607.03680", re.compile(r"^FAID\s*\(base\)", re.I), re.compile(r"Table 5", re.I), ("2607.03680:vanilla-faid-base",)),
    ("2607.03680", re.compile(r"^MIRAGE\s*\(large\)", re.I), re.compile(r"Table 5", re.I), ("2607.03680:vanilla-mirage-large",)),
    ("2607.03680", re.compile(r"^Vanilla\s*\(base\)", re.I), re.compile(r"Table (?:8|9)", re.I), ("2607.03680:vanilla-mirage-base",)),
    ("2607.03680", re.compile(r"^Vanilla\s*\(large\)$", re.I), re.compile(r"Table 8", re.I), ("2607.03680:vanilla-mirage-large",)),
    ("2607.03680", re.compile(r"^Vanilla\s*\(large\)\s*\(ours", re.I), re.compile(r"Table 9", re.I), ("2607.03680:vanilla-mage-large",)),
    ("2607.03680", re.compile(r"^Longformer\s*\(paper", re.I), re.compile(r"Table 9", re.I), ("2607.03680:mage-longformer",)),
    ("2607.03680", re.compile(r"^numeric configuration 5$", re.I), re.compile(r"Table 10", re.I), ("2607.03680:fomaml-hc3-k5",)),
    ("2607.03680", re.compile(r"^numeric configuration 10$", re.I), re.compile(r"Table 10", re.I), ("2607.03680:fomaml-lora",)),
    ("2607.03680", re.compile(r"^numeric configuration 20$", re.I), re.compile(r"Table 10", re.I), ("2607.03680:fomaml-hc3-k20",)),
    ("2607.03680", re.compile(r"^numeric configuration 50$", re.I), re.compile(r"Table 10", re.I), ("2607.03680:fomaml-hc3-k50",)),
    ("2607.03680", re.compile(r"^(?:IntelLabs|MAGE|FAID|MIRAGE)$", re.I), re.compile(r"Table 11", re.I), ("2607.03680:pooled-four-way", "2607.03680:pooled-stratified-base", "2607.03680:pooled-stratified-large")),
    ("2607.03680", re.compile(r"^w\s*·\s*pvanilla", re.I), re.compile(r"Table 13", re.I), ("2607.03680:confidence-ensemble",)),
    ("2607.03680", re.compile(r"^w\s*·\s*pFOMAML", re.I), re.compile(r"Table 13", re.I), ("2607.03680:reverse-confidence-ensemble",)),
    ("2606.02158", re.compile(r"^w/o low-probability", re.I), re.compile(r"Table 3", re.I), ("2606.02158:without-low-probability",)),
    ("2606.02158", re.compile(r"^w/o entropy", re.I), re.compile(r"Table 3", re.I), ("2606.02158:without-entropy",)),
    ("2506.06705", re.compile(r"^RoB-base", re.I), re.compile(r"Table (?:1|2)", re.I), ("2506.06705:roberta-base",)),
    ("2506.06705", re.compile(r"^RoB-large", re.I), re.compile(r"Table (?:1|2)", re.I), ("2506.06705:roberta-large",)),
    ("2606.07313", re.compile(r"^SV-Detect\s*\(polish-only\)", re.I), re.compile(r"Table (?:8|9)", re.I), ("2606.07313:polish-only",)),
    ("2606.07313", re.compile(r"^SV-Detect\s*\(3-task\)", re.I), re.compile(r"Table (?:8|9)", re.I), ("2606.07313:three-task",)),
    ("2506.01702", re.compile(r"^TF-IDF baseline", re.I), re.compile(r"Table 1", re.I), ("2506.01702:tfidf-baseline",)),
    ("2509.15550", re.compile(r"^Revise-Detect", re.I), re.compile(r"Table 5", re.I), ("2509.15550:revise-detect",)),
    ("2606.04177", re.compile(r"SVM w/ Ling\. Feats", re.I), re.compile(r"Table (?:1|3|9)", re.I), ("2606.04177:linguistic-svm",)),
    ("2606.18946", re.compile(r"^Full Model", re.I), re.compile(r"Table (?:4|5)", re.I), ("2606.18946:senflow",)),
    ("2606.18946", re.compile(r"^w/o GCN", re.I), re.compile(r"Table 5", re.I), ("2606.18946:senflow-no-gcn",)),
    ("2606.18946", re.compile(r"^w/o CRF", re.I), re.compile(r"Table 5", re.I), ("2606.18946:senflow-no-crf",)),
    ("2606.18946", re.compile(r"^w/o CL", re.I), re.compile(r"Table 5", re.I), ("2606.18946:senflow-no-cl",)),
    ("2606.18946", re.compile(r"^w/o TCN", re.I), re.compile(r"Table 5", re.I), ("2606.18946:senflow-no-tcn",)),
    ("2604.04932", re.compile(r"^w/o CL", re.I), re.compile(r"Table 3", re.I), ("2604.04932:race-no-cl",)),
    ("2604.04932", re.compile(r"^w/o Relation", re.I), re.compile(r"Table 3", re.I), ("2604.04932:race-no-relation",)),
    ("2604.04932", re.compile(r"^w/o RGCN", re.I), re.compile(r"Table 3", re.I), ("2604.04932:race-no-rgcn",)),
    ("2604.04932", re.compile(r"^w/o Bottleneck", re.I), re.compile(r"Table 3", re.I), ("2604.04932:race-no-bottleneck",)),
    ("2604.04932", re.compile(r"^w/o Basis", re.I), re.compile(r"Table 3", re.I), ("2604.04932:race-no-basis",)),
    ("2505.15261", re.compile(r"^w/o Multi-Agent", re.I), re.compile(r"Table 3", re.I), ("2505.15261:without-multi-agent",)),
    ("2505.15261", re.compile(r"^w/o Guidelines", re.I), re.compile(r"Table 3", re.I), ("2505.15261:without-guidelines",)),
    ("2505.15261", re.compile(r"^w/o Adaptive Routing", re.I), re.compile(r"Table 3", re.I), ("2505.15261:without-adaptive-routing",)),
    ("2505.15261", re.compile(r"^w/o Steer Calibration", re.I), re.compile(r"Table 3", re.I), ("2505.15261:without-steer-calibration",)),
    ("2506.15683", re.compile(r"^w/o BFE", re.I), re.compile(r"Table 3", re.I), ("2506.15683:without-bfe",)),
    ("2506.15683", re.compile(r"^w/o CL", re.I), re.compile(r"Table 3", re.I), ("2506.15683:without-cl",)),
    ("2506.15683", re.compile(r"^w/o MoE", re.I), re.compile(r"Table 3", re.I), ("2506.15683:without-moe",)),
    ("2501.08913", re.compile(r"R-Oai\s*&\s*BERT", re.I), re.compile(r"Table 4", re.I), ("2501.08913:lux-roai-bert",)),
    ("2501.08913", re.compile(r"Radar\s*&\s*R-L", re.I), re.compile(r"Table (?:4|5)", re.I), ("2501.08913:lux-radar-r-l",)),
    ("2501.08913", re.compile(r"Adv\.-New-Detector", re.I), re.compile(r"Table 4", re.I), ("2501.08913:cnlp-adv-new-detector",)),
    ("2501.08913", re.compile(r"\bGLTR", re.I), re.compile(r"Table 5", re.I), ("2501.08913:gltr",)),
    ("2505.05084", re.compile(r"^vanilla vanilla", re.I), re.compile(r"Table 3", re.I), ("2505.05084:binoculars-vanilla",)),
    ("2603.18750", re.compile(r"MLP(?:\s*\(dtEN\))?$", re.I), re.compile(r"Table (?:3|5|6)", re.I), ("2603.18750:mlp-artmh",)),
    ("2606.00016", re.compile(r"^text \(baseline\)", re.I), re.compile(r"Table 2", re.I), ("2606.00016:cnn-text",)),
    ("2601.04641", re.compile(r"^DistillBert-F", re.I), re.compile(r"Table 2", re.I), ("2601.04641:distilbert-f",)),
    ("2505.12507", re.compile(r"LM2\s*OTIFS-Bert", re.I), re.compile(r"Table 18", re.I), ("2505.12507:lm2-no-bert",)),
    ("2502.16857", re.compile(r"Noised train/val Double Finetune", re.I), re.compile(r"Table 4", re.I), ("2502.16857:double-small",)),
    ("2505.13855", re.compile(r"^Equal Vt\.", re.I), re.compile(r"Table 14", re.I), ("2505.13855:equal-vote",)),
    ("2505.13855", re.compile(r"^Weight Vt\.", re.I), re.compile(r"Table 14", re.I), ("2505.13855:weighted-vote",)),
)

LOCAL_RULES += (
    ("2608.01046", re.compile(r"^DeBERTa-Sentinel", re.I), re.compile(r"Table (?:3|4|5)", re.I), ("2608.01046:deberta-finetuned",)),
    ("2608.01046", re.compile(r"^RoBERTa-Sentinel", re.I), re.compile(r"Table 5", re.I), ("2608.01046:roberta-finetuned",)),
    ("2607.22026", re.compile(r"^HC3 Ensemble Calibration-weighted hard voting", re.I), re.compile(r"Table (?:4|5|6)", re.I), ("2607.22026:calibrated-hard",)),
    ("2607.22026", re.compile(r"^HC3 Ensemble Equal-weight hard voting", re.I), re.compile(r"Table (?:4|5|6)", re.I), ("2607.22026:equal-hard",)),
    ("2607.22026", re.compile(r"^HC3 Ensemble Calibration-weighted soft voting", re.I), re.compile(r"Table (?:4|5|6)", re.I), ("2607.22026:calibrated-soft",)),
    ("2607.22026", re.compile(r"^HC3 Ensemble Equal-weight soft voting", re.I), re.compile(r"Table (?:4|5|6)", re.I), ("2607.22026:equal-soft",)),
    ("2607.22026", re.compile(r"^HC3 Wavelet multilevel_energy", re.I), re.compile(r"Table (?:4|5|6)", re.I), ("2607.22026:multilevel-energy",)),
    ("2607.22026", re.compile(r"^HC3 Wavelet energy_norm", re.I), re.compile(r"Table (?:4|5|6)", re.I), ("2607.22026:energy-norm",)),
    ("2607.22026", re.compile(r"^(?:HC3|MAGE) Wavelet window_std", re.I), re.compile(r"Table (?:4|5|6)", re.I), ("2607.22026:window-std",)),
    ("2607.14967", re.compile(r"(?:^|\s)DeTeCtive$", re.I), re.compile(r"Table 3", re.I), ("2607.14967:detective",)),
    ("2606.31074", re.compile(r"^Fast-Detect \(Bao et al\.", re.I), re.compile(r"Table 3", re.I), ("2606.31074:fastdetectgpt",)),
    ("2606.04177", re.compile(r"^TB[47] Longformer", re.I), re.compile(r"Table 3", re.I), ("2606.04177:mage-longformer",)),
    ("2606.00016", re.compile(r"^RoBERTa$", re.I), re.compile(r"Table (?:2|3|4|5|6|7|8|9)", re.I), ("2606.00016:superannotate-roberta",)),
    ("2606.00016", re.compile(r"^AEyeDE\(CNN\)$", re.I), re.compile(r"Table 1", re.I), ("2606.00016:cnn",)),
    ("2505.14271", re.compile(r"^UnSup-SimCSE-XLM-RoBERTa-base", re.I), re.compile(r"Table 12", re.I), ("2505.14271:faid-unsup-simcse-xlmr",)),
    ("2604.21223", re.compile(r"^RM-Deberta-v3-large-v2", re.I), re.compile(r"Table 8", re.I), ("2604.21223:reward-model-deberta",)),
    ("2511.21744", re.compile(r"^AI-generated Text Detection", re.I), re.compile(r"Table 3", re.I), ("2511.21744:ai-generated-text-detection",)),
    ("2511.21744", re.compile(r"^DeTeCtive", re.I), re.compile(r"Table 3", re.I), ("2511.21744:detective-comparator",)),
    ("2511.21744", re.compile(r"^Restricted Embeddings", re.I), re.compile(r"Table 3", re.I), ("2511.21744:restricted-embeddings",)),
    ("2511.21744", re.compile(r"^ChatGPT Detector", re.I), re.compile(r"Table 3", re.I), ("2511.21744:chatgpt-detector",)),
    ("2511.21744", re.compile(r"^RoBERTa \+ BiLSTM", re.I), re.compile(r"Table 3", re.I), ("2511.21744:roberta-bilstm",)),
    ("2509.18880", re.compile(r"^(?:\S+\s+)?e5-small-lora", re.I), re.compile(r"Table (?:2|13)", re.I), ("2509.18880:e5-small-lora",)),
    ("2509.18880", re.compile(r"^(?:\S+\s+)?Desklib AI", re.I), re.compile(r"Table (?:2|13)", re.I), ("2509.18880:desklib",)),
    ("2509.18880", re.compile(r"^SuperAnnotate", re.I), re.compile(r"Table 2", re.I), ("2509.18880:superannotate",)),
    ("2509.18880", re.compile(r"^DivEye \(Ours\)", re.I), re.compile(r"Table (?:2|13)", re.I), ("2509.18880:gpt2",)),
    ("2506.15683", re.compile(r"^RoBERTa$", re.I), re.compile(r"Table 3", re.I), ("2506.15683:roberta-baseline",)),
    ("2506.15683", re.compile(r"^T5-Sentinel$", re.I), re.compile(r"Table 3", re.I), ("2506.15683:t5-sentinel-baseline",)),
    ("2506.15683", re.compile(r"^DeTeCtive$", re.I), re.compile(r"Table 3", re.I), ("2506.15683:detective-baseline",)),
    ("2506.15683", re.compile(r"^SeqXGPT$", re.I), re.compile(r"Table 3", re.I), ("2506.15683:seqxgpt-baseline",)),
    ("2506.15683", re.compile(r"^DNA-GPT$", re.I), re.compile(r"Table 3", re.I), ("2506.15683:dna-gpt-baseline",)),
    ("2506.15683", re.compile(r"^DetectGPT$", re.I), re.compile(r"Table 3", re.I), ("2506.15683:detectgpt-baseline",)),
    ("2506.15683", re.compile(r"^Fast-DetectGPT$", re.I), re.compile(r"Table 3", re.I), ("2506.15683:fastdetectgpt-baseline",)),
    ("2506.15683", re.compile(r"^PhantomHunter$", re.I), re.compile(r"Table (?:3|5)", re.I), ("2506.15683:full",)),
    ("2506.15683", re.compile(r"^HasteWire$", re.I), re.compile(r"Table 5", re.I), ("2506.15683:hastewire",)),
    ("2506.06705", re.compile(r"^w/o Adaption", re.I), re.compile(r"Table (?:3|4)", re.I), ("2506.06705:without-adaptation",)),
    ("2506.06705", re.compile(r"^DivScore \(Mistral\)", re.I), re.compile(r"Table 4", re.I), ("2506.06705:divscore-mistral",)),
    ("2506.06705", re.compile(r"^DivScore \(Falcon\)", re.I), re.compile(r"Table 4", re.I), ("2506.06705:divscore-falcon",)),
    ("2506.06705", re.compile(r"^DivScore \(Qwen\)", re.I), re.compile(r"Table 4", re.I), ("2506.06705:divscore-qwen",)),
    ("2506.06705", re.compile(r"^DivScore \(Llama\)", re.I), re.compile(r"Table 4", re.I), ("2506.06705:divscore-llama",)),
    ("2506.06705", re.compile(r"^Entropy \(Mistral\)", re.I), re.compile(r"Table 4", re.I), ("2506.06705:entropy-mistral",)),
    ("2506.06705", re.compile(r"^Entropy \(Falcon\)", re.I), re.compile(r"Table 4", re.I), ("2506.06705:entropy-falcon",)),
    ("2506.06705", re.compile(r"^Entropy \(Qwen\)", re.I), re.compile(r"Table 4", re.I), ("2506.06705:entropy-qwen",)),
    ("2506.06705", re.compile(r"^Entropy \(Llama\)", re.I), re.compile(r"Table 4", re.I), ("2506.06705:entropy-llama",)),
    ("2506.06705", re.compile(r"^Cross-Entropy \(Qwen\)", re.I), re.compile(r"Table 4", re.I), ("2506.06705:cross-entropy-qwen",)),
    ("2505.13855", re.compile(r"^baseline \(", re.I), re.compile(r"Table 2", re.I), ("2505.13855:qwen32b",)),
    ("2503.00032", re.compile(r"^Essay POS Combinations Random Forest", re.I), re.compile(r"Table 9", re.I), ("2503.00032:pos-rf",)),
    ("2503.00032", re.compile(r"^Punctuation Random Forest", re.I), re.compile(r"Table 9", re.I), ("2503.00032:punctuation-rf",)),
    ("2502.16857", re.compile(r"^Ensemble \(deberta-v3-small \+ Double Finetune\)", re.I), re.compile(r"Table 4", re.I), ("2502.16857:ensemble-small",)),
    ("2603.05617", re.compile(r"^N OTAI\.AI Ensemble", re.I), re.compile(r"Table 1", re.I), ("2603.05617:ensemble",)),
    ("2601.20006", re.compile(r"^Per LLM Family Ensemble", re.I), re.compile(r"Table 15", re.I), ("2601.20006:ensemble-per-family",)),
    ("2509.25154", re.compile(r"^XGB$", re.I), re.compile(r"Table 1", re.I), ("2509.25154:jdetector-xgb",)),
    ("2509.00731", re.compile(r"^BERT Train$", re.I), re.compile(r"Table 1", re.I), ("2509.00731:bert",)),
    ("2603.23146", re.compile(r"^Random Forest$", re.I), re.compile(r"Table (?:5|6|8)", re.I), ("2603.23146:optimized-random-forest",)),
    ("2603.23146", re.compile(r"^SVM$", re.I), re.compile(r"Table (?:5|6)", re.I), ("2603.23146:optimized-svc",)),
    ("2603.23146", re.compile(r"^XGBoost$", re.I), re.compile(r"Table (?:5|6|8)", re.I), ("2603.23146:optimized-xgboost",)),
    ("2508.18715", re.compile(r"^MLP$", re.I), re.compile(r"Table 1", re.I), ("2508.18715:mlp",)),
    ("2509.26051", re.compile(r"^F mDeBERTa-v3-base \(de-pl-hr-cs\)", re.I), re.compile(r"Table 3", re.I), ("2509.26051:mdeberta-v3-base",)),
    ("2509.26051", re.compile(r"^F Llama$", re.I), re.compile(r"Table 3", re.I), ("2509.26051:llama-3.2-3b",)),
    ("2509.26051", re.compile(r"^F Gemma$", re.I), re.compile(r"Table 3", re.I), ("2509.26051:gemma-2-2b",)),
    ("2509.26051", re.compile(r"^F XLM-RoBERTa-base \(de-pl-hr-hu-cs\)", re.I), re.compile(r"Table (?:3|4)", re.I), ("2509.26051:xlm-roberta-base",)),
    ("2509.26051", re.compile(r"^F mDeBERTa-v3-base \(de-pl-hr-hu-cs\)", re.I), re.compile(r"Table 4", re.I), ("2509.26051:mdeberta-generator-de-pl-hr-hu-cs",)),
    ("2509.26051", re.compile(r"Llama-3\.2-3B \(hr-hu-cs\)", re.I), re.compile(r"Table 5", re.I), ("2509.26051:llama-news-hr-hu-cs",)),
    ("2509.26051", re.compile(r"Llama-3\.2-3B \(de-pl-hu\)", re.I), re.compile(r"Table 5", re.I), ("2509.26051:llama-3.2-3b",)),
    ("2509.26051", re.compile(r"Llama-3\.2-3B paraphrased", re.I), re.compile(r"Table (?:5|6|12)", re.I), ("2509.26051:llama-3.2-3b",)),
    ("2509.26051", re.compile(r"^mDeBERTa-v3-base \(de\)$", re.I), re.compile(r"Table 5", re.I), ("2509.26051:mdeberta-social-de",)),
    ("2509.26051", re.compile(r"Gemma-2-2B \(de-pl-hr-hu-cs\)", re.I), re.compile(r"Table 5", re.I), ("2509.26051:gemma-social-de-pl-hr-hu-cs",)),
    ("2509.26051", re.compile(r"Gemma-2-2B \(de-pl-cs\)", re.I), re.compile(r"Table 5", re.I), ("2509.26051:gemma-2-2b",)),
    ("2509.26051", re.compile(r"Gemma-2-2B paraphrased", re.I), re.compile(r"Table (?:5|6|12)", re.I), ("2509.26051:gemma-2-2b",)),
    ("2509.26051", re.compile(r"^XLM-RoBERTa-base \(de-pl\)$", re.I), re.compile(r"Table 5", re.I), ("2509.26051:xlm-social-de-pl",)),
    ("2509.26051", re.compile(r"^F Llama$", re.I), re.compile(r"Table 11", re.I), ("2509.26051:llama-tpr-pl",)),
    ("2509.26051", re.compile(r"^F Gemma$", re.I), re.compile(r"Table 11", re.I), ("2509.26051:gemma-tpr-de-pl-hr-hu",)),
    ("2509.26051", re.compile(r"^F mDeBERTa-v3-base \(de-pl-hr-hu\)", re.I), re.compile(r"Table 11", re.I), ("2509.26051:mdeberta-tpr-de-pl-hr-hu",)),
    ("2509.26051", re.compile(r"^F XLM-RoBERTa-base \(de-cs\)", re.I), re.compile(r"Table 11", re.I), ("2509.26051:xlm-tpr-de-cs",)),
    ("2509.26051", re.compile(r"^S Fast-DetectGPT", re.I), re.compile(r"Table 4", re.I), ("2509.26051:fastdetectgpt",)),
    ("2509.26051", re.compile(r"^S Binoculars", re.I), re.compile(r"Table 4", re.I), ("2509.26051:binoculars",)),
    ("2604.16607", re.compile(r"BiScope[- ]Arxiv", re.I), re.compile(r"Table 3", re.I), ("2604.16607:biscope-arxiv",)),
    ("2604.16607", re.compile(r"DeTeCtive \(M4GT\)", re.I), re.compile(r"Table 3", re.I), ("2604.16607:detective-m4gt",)),
    ("2604.16607", re.compile(r"DeTeCtive \(OUTFOX\)", re.I), re.compile(r"Table 3", re.I), ("2604.16607:detective-outfox",)),
    ("2604.16607", re.compile(r"DeTeCtive \(TuringBench\)", re.I), re.compile(r"Table 3", re.I), ("2604.16607:detective-turingbench",)),
    ("2604.16607", re.compile(r"Zippy \(Ensemble\)", re.I), re.compile(r"Table 3", re.I), ("2604.16607:zippy-ensemble",)),
    ("2604.16607", re.compile(r"RoBERTa \(H3C\+\)", re.I), re.compile(r"Table 3", re.I), ("2604.16607:roberta-h3c-plus",)),
    ("2604.16607", re.compile(r"RoBERTa \(M4GT\)", re.I), re.compile(r"Table 3", re.I), ("2604.16607:roberta-m4gt",)),
    ("2604.16607", re.compile(r"stylo \(H3C\+\)", re.I), re.compile(r"Table 3", re.I), ("2604.16607:stylo-h3c-plus",)),
    ("2604.16607", re.compile(r"mcgovern \(H3C\+\)", re.I), re.compile(r"Table 3", re.I), ("2604.16607:mcgovern-h3c-plus",)),
    ("2604.16607", re.compile(r"mcgovern \(M4GT\)", re.I), re.compile(r"Table 3", re.I), ("2604.16607:mcgovern-m4gt",)),
    ("2604.16607", re.compile(r"mcgovern \(MAGE\)", re.I), re.compile(r"Table 3", re.I), ("2604.16607:mcgovern-mage",)),
    ("2510.12476", re.compile(r"^Lastde$", re.I), re.compile(r"Table (?:2|10|11)", re.I), ("2510.12476:lastde",)),
    ("2510.12476", re.compile(r"^Lastde\+\+$", re.I), re.compile(r"Table (?:2|10|11)", re.I), ("2510.12476:lastde-plus-plus",)),
    ("2501.03940", re.compile(r"RADAR-FT$", re.I), re.compile(r"Table (?:4|5)", re.I), ("2501.03940:radar-ft",)),
    ("2501.03940", re.compile(r"PAWN \(GPT2\) PAWN \(LLaMA3-1b\) RoBERTa", re.I), re.compile(r"Table 9", re.I), ("2501.03940:m4-roberta-base",)),
    ("2502.16857", re.compile(r"^deberta-v3-xsmall$", re.I), re.compile(r"Table 1", re.I), ("2502.16857:original-xsmall",)),
    ("2502.16857", re.compile(r"^Original train/val deberta-v3-small$", re.I), re.compile(r"Table 1", re.I), ("2502.16857:original-small",)),
    ("2502.16857", re.compile(r"^deberta-v3-base$", re.I), re.compile(r"Table 1", re.I), ("2502.16857:original-base",)),
    ("2502.16857", re.compile(r"^deberta-v3-xsmall$", re.I), re.compile(r"Table 3", re.I), ("2502.16857:noised-xsmall",)),
    ("2502.16857", re.compile(r"^deberta-v3-small$", re.I), re.compile(r"Table 3", re.I), ("2502.16857:noised-small",)),
    ("2502.16857", re.compile(r"^deberta-v3-base$", re.I), re.compile(r"Table 3", re.I), ("2502.16857:noised-base",)),
    ("2501.08913", re.compile(r"\[Cn\] (?:CNLP )?DistilBERT-NITS$", re.I), re.compile(r"Table (?:4|9)", re.I), ("2501.08913:cnlp-nits-distilbert",)),
    ("2501.08913", re.compile(r"\[Us\] Roberta_dataaug\.$", re.I), re.compile(r"Table 4", re.I), ("2501.08913:ustc-roberta-dataaug",)),
    ("2501.08913", re.compile(r"\[Ba\] Binoculars$", re.I), re.compile(r"Table 5", re.I), ("2501.08913:binoculars",)),
    ("2501.08913", re.compile(r"\[Ba\] openai-roberta-L$", re.I), re.compile(r"Table 5", re.I), ("2501.08913:openai-roberta-large",)),
    ("2504.11369", re.compile(r"Fast-DetectGPT \(Bao et al\.$|FastDetect$", re.I), re.compile(r"Table (?:1|9|10)", re.I), ("2504.11369:fastdetectgpt",)),
    ("2504.11369", re.compile(r"LRR$", re.I), re.compile(r"Table (?:9|10)", re.I), ("2504.11369:lrr",)),
    ("2504.11369", re.compile(r"GPT-D$", re.I), re.compile(r"Table (?:2|3)", re.I), ("2504.11369:chatgpt-detector",)),
    ("2505.12507", re.compile(r"RADAR$", re.I), re.compile(r"Table 1", re.I), ("2505.12507:radar",)),
    ("2505.12507", re.compile(r"Entropy$", re.I), re.compile(r"Table 1", re.I), ("2505.12507:entropy",)),
    ("2604.11796", re.compile(r"Entropy$", re.I), re.compile(r"Table 2", re.I), ("2604.11796:entropy",)),
    ("2604.11796", re.compile(r"Log-Rank$", re.I), re.compile(r"Table 2", re.I), ("2604.11796:log-rank",)),
    ("2604.11796", re.compile(r"ReMoDetect$", re.I), re.compile(r"Table 2", re.I), ("2604.11796:remodetect",)),
    ("2603.18750", re.compile(r"MobileNet CNN$|\bCNN$", re.I), re.compile(r"Table (?:3|4)", re.I), ("2603.18750:mobilenet-cnn",)),
    ("2603.18750", re.compile(r"ZeroGPT$", re.I), re.compile(r"Table 3", re.I), ("2603.18750:zerogpt-artmh",)),
    ("2603.18750", re.compile(r"Sapling$", re.I), re.compile(r"Table 6", re.I), ("2603.18750:sapling-artmh",)),
    ("2603.18750", re.compile(r"GPTZero$", re.I), re.compile(r"Table 6", re.I), ("2603.18750:gptzero-artmh",)),
    ("2510.12476", re.compile(r"Lastde drops from$", re.I), re.compile(r"Table 2", re.I), ("2510.12476:lastde",)),
)

LOCAL_FALSE_RULES: tuple[tuple[str, re.Pattern[str], re.Pattern[str], str, str], ...] = (
    ("2511.17402", re.compile(r".*", re.S), re.compile(r"Table (?:2|3|4)", re.I), "non_detector_row", "This row belongs to the toolkit's readability/complexity auxiliary task, not its machine-text detector evaluation."),
    ("2509.22147", re.compile(r".*", re.S), re.compile(r"Table (?:5|6|9)", re.I), "diagnostic_or_component", "This row belongs to the paper's segmentation, source-attribution, or expert-count auxiliary task, not the binary human-versus-machine deployment account."),
    ("2606.04177", re.compile(r"^CNN$", re.I), re.compile(r"Table 10", re.I), "non_detector_row", "`CNN` is the CNN/DailyMail text-domain label in this table, not a convolutional detector."),
    ("2606.04177", re.compile(r"^Baseline", re.I), re.compile(r"Table 15", re.I), "diagnostic_or_component", "This plotted baseline value is a feature-ablation reference line, not a separately named fitted detector."),
    ("2606.07313", re.compile(r"^\s*(?:DetectRL|Baseline)", re.I), re.compile(r"Table (?:3|6)", re.I), "non_detector_row", "This is a DetectRL attack/slice or leaderboard-heading row, not a separately named detector."),
    ("2607.17382", re.compile(r"^DetectRL", re.I), re.compile(r"Table (?:4|5|8|9|10)", re.I), "non_detector_row", "DetectRL is the evaluated benchmark row, not a DACTYL detector state."),
    ("2505.05084", re.compile(r"^(?:Detector Algorithm|w/o q̂M|detectors and supervised detectors)", re.I), re.compile(r"Table (?:2|3|8|9)", re.I), "diagnostic_or_component", "This is a table heading, prose fragment, or component-only MCP ablation rather than a separately deployable detector state."),
    ("2605.06903", re.compile(r"^(?:Detector AUROC|MELD w/o)", re.I), re.compile(r"Table (?:1|5)", re.I), "diagnostic_or_component", "This is a leaderboard heading or loss-component ablation, not a separately released MELD detector state."),
    ("2511.01192", re.compile(r"^(?:w/o|DMoE)", re.I), re.compile(r"Table 2", re.I), "diagnostic_or_component", "This is a routing/component ablation within DEER, not a separately deployable detector account."),
    ("2506.01702", re.compile(r"^Detector ROC-AUC", re.I), re.compile(r"Table (?:1|2)", re.I), "table_heading_or_prose", "This is the metric header of the mdok comparison table, not a detector row."),
    ("2505.24523", re.compile(r"^DetectAIve", re.I), re.compile(r"Table 2", re.I), "nonqualifying_metric_context", "DetectAIve's own row remains below 0.90; the adjacent 0.93 in the two-column extraction belongs to prose describing RADAR."),
    ("2603.18750", re.compile(r"^CNN", re.I), re.compile(r"Table (?:4|5)", re.I), "nonqualifying_metric_context", "This is a one-class cross-domain diagnostic, not a new fitted state beyond the already disposed CNN1D account."),
    ("2602.01240", re.compile(r"^Full w/o", re.I), re.compile(r"Table 3", re.I), "diagnostic_or_component", "This is a component-removal ablation of DetectRouter, not a separately deployable scoring detector."),
    ("2502.15654", re.compile(r"^SmolLM2 baseline", re.I), re.compile(r"Table S2", re.I), "non_detector_row", "SmolLM2 is the evaluated generator in a data-quality experiment, not an AI-text detector."),
)

LOCAL_RULES += (
    ("2603.18750", re.compile(r"Rephrase$", re.I), re.compile(r"Table 3", re.I), ("2603.18750:rephrase",)),
)

LOCAL_FALSE_RULES += (
    ("2607.03680", re.compile(r"^fine-tuned RoBERTa detector, we implement", re.I), re.compile(r"Table 6", re.I), "table_heading_or_prose", "This is implementation prose adjacent to the transfer table, not another fitted RoBERTa result row beyond the explicitly inventoried training states."),
    ("2501.09813", re.compile(r"^cross entropy function in order to make the model F1$", re.I), re.compile(r"Table (?:2|3)", re.I), "table_heading_or_prose", "This is training-description prose fused with a nearly one-hundred-percent dataset result in the adjacent PDF column, not a Cross-Entropy detector row."),
    ("2606.07313", re.compile(r"^SV-Detect Fast-DetectGPT RoBERTa-Base$", re.I), re.compile(r"Table 9", re.I), "table_heading_or_prose", "This is the three-detector column header above generator rows, not an additional fitted SV-Detect, Fast-DetectGPT, or RoBERTa state."),
    ("2605.06903", re.compile(r"^vs\. Binoculars$", re.I), re.compile(r"Table 8", re.I), "diagnostic_or_component", "This is the comparator heading for MELD-minus-Binoculars confidence intervals, not another fitted Binoculars or MELD detector state."),
    ("2601.20006", re.compile(r"^in the ensembles evaluated in the subsequent experiments\.$", re.I), re.compile(r"Table 10", re.I), "table_heading_or_prose", "This is prose introducing the already inventoried fine-tuned family models, not a separately named ensemble or fitted state."),
    ("2510.12476", re.compile(r"^Detector Generator arXiv PeerRead Reddit WikiHow Wikipedia Avg\.$", re.I), re.compile(r"Table 14", re.I), "table_heading_or_prose", "This is the Table 14 column header; the following grouped RoBERTa and DeTeCtive method identities are discovered and bound separately."),
    ("2509.18880", re.compile(r"^Backbone Model DivEye Binoculars BiScope LogRank DetectLLM FastDetectGPT$", re.I), re.compile(r"Table 6", re.I), "table_heading_or_prose", "This is the backbone-by-detector column header, not a new compound detector or separately fitted result state."),
    ("2501.08913", re.compile(r"^iterations are reached", re.I), re.compile(r"Table 3", re.I), "table_heading_or_prose", "This is threshold-calibration prose split across the two PDF columns, not a detector-result row."),
    ("2501.11012", re.compile(r"^(?:tems by comparing|and training-aligned|important, MGT detection|complexities to prevent)", re.I), re.compile(r"Table (?:8|9|11)", re.I), "table_heading_or_prose", "This is shared-task discussion or bibliography prose captured beside a percentage, not an individually named submitted system row."),
    ("2501.11914", re.compile(r"^For the English-only task", re.I), re.compile(r"Table (?:4|5)", re.I), "table_heading_or_prose", "This sentence narrates the already inventoried English and multilingual ensemble results; it is not another fitted state."),
    ("2502.11336", re.compile(r"^For each detector", re.I), re.compile(r"Table 1", re.I), "table_heading_or_prose", "This is experiment-protocol prose adjacent to a sample count, not a detector row or threshold result."),
    ("2502.12611", re.compile(r"^(?:statistically significant|SVC, DecisionTreeClassifier)", re.I), re.compile(r"Table (?:4|32)", re.I), "table_heading_or_prose", "This is statistical-analysis or model-summary prose containing a confidence percentage, not a named AI-text detector result."),
    ("2502.15654", re.compile(r"^B Machine-generated text detection hyperparameter sweep", re.I), re.compile(r"Table 3", re.I), "diagnostic_or_component", "This is a learning-rate hyperparameter range, not an additional fitted detector or evaluation result."),
    ("2504.11369", re.compile(r"^(?:• Model-based detection methods|ing\. Nonetheless, OTBDetector)", re.I), re.compile(r"Table (?:1|3)", re.I), "table_heading_or_prose", "This is method-list or result-discussion prose captured across columns; every named table detector is dispositioned separately."),
    ("2504.21019", re.compile(r"^(?:box AIGT detection|a detection accuracy of|age detection accuracy of)", re.I), re.compile(r"Table (?:1|3)", re.I), "table_heading_or_prose", "This is DP-Net baseline or robustness narrative whose reported values are already bound to the uniform and Gaussian accounts, not a third state."),
    ("2505.14271", re.compile(r"^texts with the same models", re.I), re.compile(r"Table 1", re.I), "table_heading_or_prose", "This is FAIDSet construction/evaluation prose beside Table 1, not a separately named detector configuration."),
    ("2505.24523", re.compile(r"^detection\. Pre-trained detectors", re.I), re.compile(r"Table 2", re.I), "table_heading_or_prose", "This is prose describing existing MAGE and RADAR rows; the percentage is not a new named detector state."),
    ("2508.06913", re.compile(r"^where SentiDetect leads", re.I), re.compile(r"Table (?:2|3)", re.I), "table_heading_or_prose", "This is a relative-gain sentence about the already inventoried SentiDetect states, not an additional configuration."),
    ("2508.18715", re.compile(r"^(?:feature attribution|Datasets Binoculars|the only benchmark|PLM for turn-level)", re.I), re.compile(r"Table (?:1|5|6)", re.I), "table_heading_or_prose", "This is dialogue-benchmark, threshold, or attribution-method prose fused across PDF columns, not another detector row."),
    ("2509.00623", re.compile(r"^provided a very strong baseline", re.I), re.compile(r"Table 1", re.I), "table_heading_or_prose", "This sentence discusses the already inventoried TF-IDF+SVM submission and does not define another fitted state."),
    ("2509.00731", re.compile(r"^(?:are trained jointly|clearly, it overfit|degradation under distribution shift)", re.I), re.compile(r"Table (?:1|2)", re.I), "table_heading_or_prose", "This is training or result-discussion prose; the named BERT, RoBERTa, and LoRA states have separate accounts."),
    ("2509.26051", re.compile(r"^lingual baselines\), Llama", re.I), re.compile(r"Table 1", re.I), "table_heading_or_prose", "This is baseline-selection prose beside the dataset-count table, not a fitted language-combination result row."),
    ("2510.00890", re.compile(r"^Roberta$", re.I), re.compile(r"Table (?:1|2)", re.I), "nonqualifying_metric_context", "The RoBERTa row itself reports only 55.46 F1 and 72.30 AUROC; the adjacent >=0.90 values belong to Sci-SpanDet ablations."),
    ("2510.00890", re.compile(r"^(?:tics, zero-shot|RoBERTa and GLTR|perform paragraph-level)", re.I), re.compile(r"Table (?:1|3)", re.I), "table_heading_or_prose", "This is comparison discussion whose high number belongs to an already inventoried Sci-SpanDet state, not a new detector row."),
    ("2510.03502", re.compile(r"^BERT$", re.I), re.compile(r"Table 9", re.I), "non_detector_row", "BERT appears in the LLM specification/reference context, not as an evaluated ALHD detector result."),
    ("2510.12476", re.compile(r"^based detectors: RoBERTa", re.I), re.compile(r"Table (?:5|6)", re.I), "table_heading_or_prose", "This is setup prose for the already inventoried RoBERTa and DeTeCtive M4 fits, not a third training state."),
    ("2511.00988", re.compile(r"^detector$", re.I), re.compile(r"Table 3", re.I), "table_heading_or_prose", "This is a malformed running-time diagram label with no system identity; named detector timing rows are dispositioned elsewhere."),
    ("2511.01192", re.compile(r"^Metric-based detectors make predictions", re.I), re.compile(r"Table 5", re.I), "table_heading_or_prose", "This is detector-family methodology prose beside dataset-length statistics, not a fitted DEER routing state."),
    ("2512.09292", re.compile(r"^datasets\. We use BiScope", re.I), re.compile(r"Table (?:1|2)", re.I), "table_heading_or_prose", "This is benchmark setup prose naming an already dispositioned comparator, not a distinct fitted result."),
    ("2601.04833", re.compile(r"^free detection of GPT-generated text", re.I), re.compile(r"Table (?:5|6)", re.I), "table_heading_or_prose", "This is a split bibliography citation to DNA-GPT, not a TSD detector row or new result."),
    ("2602.01240", re.compile(r"^tion overlooks model idiosyncrasies", re.I), re.compile(r"Table 1", re.I), "table_heading_or_prose", "This is source-surrogate discussion containing an illustrative AUC bound, not a named routing criterion."),
    ("2602.15514", re.compile(r"^Detector Test Prec Recall F1 Acc", re.I), re.compile(r"Table 2", re.I), "table_heading_or_prose", "This is the detector-table header, not an additional DependencyAI or XLM-RoBERTa state."),
    ("2603.23146", re.compile(r"^Detection$", re.I), re.compile(r"Table 2", re.I), "table_heading_or_prose", "This is a benchmark-description column heading, not a machine-learning detector result."),
    ("2604.16923", re.compile(r"^DetectGPT♣$", re.I), re.compile(r"Table 10", re.I), "nonqualifying_metric_context", "This DetectGPT row is at most 1.00% TPR in the cited low-FPR table; adjacent larger values belong to other methods."),
    ("2605.02374", re.compile(r"^ial rewrites\. Disabling retrieval guidance", re.I), re.compile(r"Table 3", re.I), "table_heading_or_prose", "This is REACT ablation discussion captured across columns, not a separately reported fitted detector row."),
    ("2605.02374", re.compile(r"^DetectRL$", re.I), re.compile(r"Table (?:4|5)", re.I), "non_detector_row", "DetectRL is the dataset block label in Table 5; detector systems occupy the table columns and are not represented by this row label."),
    ("2605.14240", re.compile(r"^cation using ensemble llm approaches", re.I), re.compile(r"Table 1", re.I), "table_heading_or_prose", "This is a bibliography entry containing a journal volume number, not an evaluated detector row."),
    ("2605.15518", re.compile(r"^(?:Classifier remains above|based detectors a|statistical-based detectors)", re.I), re.compile(r"Table 2", re.I), "table_heading_or_prose", "This is DetectRL-X aggregate discussion, not a separately named classifier beyond the exact leaderboard accounts."),
    ("2605.25281", re.compile(r"^detectors\. Acta neurochirurgica", re.I), re.compile(r"Table (?:4|5)", re.I), "table_heading_or_prose", "This is a bibliography fragment beside the READER table, not an evaluated detector state."),
    ("2606.02158", re.compile(r"^(?:budget, Uncertainty\+\+|ter sensitivity of Uncertainty\+\+)", re.I), re.compile(r"Table 2", re.I), "diagnostic_or_component", "This is hyperparameter-sensitivity prose for the already inventoried Uncertainty++ account, not another fitted state."),
    ("2606.04177", re.compile(r"^(?:TB6 \(Unseen text domains\)|achieves the highest average detectability)", re.I), re.compile(r"Table 7", re.I), "table_heading_or_prose", "This is held-out-domain narrative about the existing Longformer/SVM evaluations, not a new classifier row."),
    ("2606.23336", re.compile(r"^RoBERTa$", re.I), re.compile(r"Table (?:5|6)", re.I), "diagnostic_or_component", "This RoBERTa entry is a computational-complexity row; its 1-forward notation is not a >=0.90 detector metric."),
    ("2606.23336", re.compile(r"^comparison across different detectors", re.I), re.compile(r"Table (?:6|8)", re.I), "table_heading_or_prose", "This is a two-column caption fragment naming evaluated generators, not a detector result row."),
    ("2606.31074", re.compile(r"^(?:detectors outperform the baselines|Detect\), which is even slightly better)", re.I), re.compile(r"Table (?:5|7)", re.I), "table_heading_or_prose", "This is Triospect result discussion captured beside a high number, not another detector or fitted proxy state."),
    ("2607.03680", re.compile(r"^(?:bution shift|proves over the vanilla baseline|and FOMAML\+LoRA performs|Vanilla detector\. All vanilla detectors|Ensemble AUROC TPR @|Held-out domain Ensemble TPR)", re.I), re.compile(r"Table (?:5|7|13|14)", re.I), "table_heading_or_prose", "This is transfer/adaptation prose or an ensemble-table header; exact Vanilla, FOMAML, pooled, and ensemble states are separately bound."),
    ("2607.14905", re.compile(r"^baseline\. In the S AME", re.I), re.compile(r"Table 3", re.I), "table_heading_or_prose", "This is same-version evaluation prose referring to the existing Longformer baseline, not a new graph architecture."),
    ("2608.01046", re.compile(r"^models\. DeBERTa-v3-small achieves", re.I), re.compile(r"Table 2", re.I), "table_heading_or_prose", "This is narrative describing the already inventoried fine-tuned DeBERTa-Sentinel, not another model state."),
)

for _learner, _slug in (("LR", "lr"), ("RF", "rf"), ("XGB", "xgb"), ("LDA", "lda"), ("SVM", "svm")):
    LOCAL_RULES += ((
        "2509.22147",
        re.compile(rf"^{_learner}$", re.I),
        re.compile(r"Table 3", re.I),
        (f"2509.22147:word2vec-{_slug}", f"2509.22147:tfidf-{_slug}"),
    ),)
for _name, _slug in (
    ("CNN", "cnn"), ("RNN", "rnn"), ("LSTM", "lstm"),
    ("BiLSTM", "bilstm"), ("BiGRU", "bigru"), ("CNN-LSTM", "cnn-lstm"),
    ("CNN-BiLSTM", "cnn-bilstm"), ("CNN-BiGRU", "cnn-bigru"),
    ("BERT", "bert"), ("DistilBERT", "distilbert"), ("RoBERTa", "roberta"),
    ("DeBERTa", "deberta"), ("ModernBERT", "modernbert"),
):
    LOCAL_RULES += ((
        "2509.22147",
        re.compile(rf"^{re.escape(_name)}$", re.I),
        re.compile(r"Table 3", re.I),
        (f"2509.22147:binary-{_slug}",),
    ),)
for _name, _slug in (
    ("BERT", "bert"), ("DistilBERT", "distilbert"), ("RoBERTa", "roberta"),
    ("DeBERTa", "deberta"), ("ModernBERT", "modernbert"),
):
    LOCAL_RULES += ((
        "2509.22147",
        re.compile(rf"^{re.escape(_name)}$", re.I),
        re.compile(r"Table 4", re.I),
        (f"2509.22147:implicit-{_slug}",),
    ),)
LOCAL_RULES += (
    ("2509.22147", re.compile(r"^ModernBERT \(Best\)", re.I), re.compile(r"Table 7", re.I), ("2509.22147:binary-modernbert",)),
    ("2509.22147", re.compile(r"^BERT \(Best\)", re.I), re.compile(r"Table 8", re.I), ("2509.22147:implicit-bert",)),
    ("2503.15044", re.compile(r"RF", re.I), re.compile(r"Table 3", re.I), ("2503.15044:random-forest",)),
)

LOCAL_CARRY_RULES: tuple[tuple[str, re.Pattern[str], re.Pattern[str], tuple[str, ...]], ...] = (
    ("2607.22026", re.compile(r"lrr_score", re.I), re.compile(r"Table (?:4|5|6)", re.I), ("2505.12507:lrr",)),
    ("2607.22026", re.compile(r"mean_rank", re.I), re.compile(r"Table (?:4|5|6)", re.I), ("2505.12507:rank",)),
    ("2607.17382", re.compile(r"Baseline mdok", re.I), re.compile(r"Table 11", re.I), ("2506.01702:mdok-binary",)),
    ("2607.22026", re.compile(r"^HC3 Baseline mean_logrank", re.I), re.compile(r"Table (?:4|5|6)", re.I), ("2505.12507:logrank",)),
    ("2607.22026", re.compile(r"^HC3 Baseline mean_log_likelihood", re.I), re.compile(r"Table (?:4|5|6)", re.I), ("2505.12507:likelihood",)),
    ("2607.22026", re.compile(r"^HC3 Baseline mean_entropy", re.I), re.compile(r"Table (?:4|5|6)", re.I), ("2505.12507:entropy",)),
    ("2505.15261", re.compile(r"^Fast-Detect", re.I), re.compile(r"Table (?:1|2|4|5|6)", re.I), ("2505.12507:fastdetectgpt",)),
    ("2509.18880", re.compile(r"FastDetectGPT$", re.I), re.compile(r"Table 1", re.I), ("2505.12507:fastdetectgpt",)),
)

CANONICAL_CARRY_RULES: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"^DeBERTa-v3 \(zero-shot\)$", re.I), "2502.15654:deberta-v3"),
    (re.compile(r"^OriginalityAI$", re.I), "2603.18750:originality-artmh"),
    (re.compile(r"^FourierGPT$", re.I), "2602.08031:fouriergpt"),
    (re.compile(r"^RepreGuard(?:\s|\[|\(|$)", re.I), "2602.08031:repreguard"),
    (re.compile(r"^DetectAnyLLM(?:\s|\[|\(|$)", re.I), "2607.03680:detectanyllm"),
    (re.compile(r"^Revise-?Detect(?:\s|\[|\(|$)", re.I), "2509.15550:revise-detect"),
    (re.compile(r"^AdaDetectGPT(?:\s|\[|\(|$)", re.I), "2605.25281:adadetectgpt-gemma"),
    (re.compile(r"^DetectLLM-LRR(?:\s|\[|\(|$)", re.I), "2605.27921:detectllm-lrr"),
    (re.compile(r"^DetectLLM(?:\s|\[|\(|$)", re.I), "2510.19492:detectllm"),
    (re.compile(r"^R-Detect(?:\s|\[|\(|$)", re.I), "2510.12608:r-detect"),
    (re.compile(r"^FastText(?:\s|\[|\(|\.|$)", re.I), "2509.00731:fasttext"),
    (re.compile(r"^QuillBot(?:\s|\[|\(|$)", re.I), "2603.18750:quillbot-artmh"),
    (re.compile(r"^Curvature(?:\s|\[|\(|$)", re.I), "2603.05617:curvature"),
    (re.compile(r"^FastGPT(?:\s|\[|\(|$)", re.I), "2602.08031:fastgpt"),
    (re.compile(r"^ChatGPT-D(?:\s|\[|\(|$)", re.I), "2605.27921:chatgpt-d"),
    (re.compile(r"^Sapling(?:\s|\[|\(|$)", re.I), "2603.18750:sapling-artmh"),
    (re.compile(r"^(?:Log[- ]?Likelihood|Likelihood)(?:\s|\[|\(|$)", re.I), "2505.12507:likelihood"),
    (re.compile(r"^Log[- ]?Rank(?:\s|\[|\(|$)", re.I), "2505.12507:logrank"),
    (re.compile(r"^Entropy(?:\s|\[|\(|$)", re.I), "2505.12507:entropy"),
    (re.compile(r"^Rank(?:\s|\[|\(|$)", re.I), "2505.12507:rank"),
    (re.compile(r"^(?:Detect)?LRR(?:\s|\[|\(|$)", re.I), "2505.12507:lrr"),
    (re.compile(r"^(?:Detect)?NPR(?:\s|\[|\(|$)", re.I), "2505.12507:npr"),
    (re.compile(r"^DetectGPT(?:\s|\[|\(|\*|$)", re.I), "2509.15550:detectgpt"),
    (re.compile(r"^DNA[- ]?GPT(?:\s|\[|\(|$)", re.I), "2505.12507:dnagpt"),
    (re.compile(r"^(?:Fast[- ]?DetectGPT|F[- ]DetectGPT|FastDetect)(?:\s|\[|\(|$)", re.I), "2505.12507:fastdetectgpt"),
    (re.compile(r"^Binoculars(?:\s|\[|\(|\*|$)", re.I), "2505.12507:binoculars"),
    (re.compile(r"^RADAR(?:\s|\[|\(|\*|$)", re.I), "2505.12507:radar"),
    (re.compile(r"^GLTR(?:\s|\[|\(|\*|$)", re.I), "2501.08913:gltr"),
    (re.compile(r"^GPTZero(?:\s|\[|\(|\*|$)", re.I), "2505.12507:gptzero"),
    (re.compile(r"^Lastde\+\+(?:\s|\[|\(|$)", re.I), "2604.16923:lastde-plus"),
    (re.compile(r"^Lastde(?:\s|\[|\(|$)", re.I), "2601.04833:lastde"),
    (re.compile(r"^ReMoDetect(?:\s|\[|\(|$)", re.I), "2604.16923:remodetect"),
    (re.compile(r"^BiScope(?:\s|\[|\(|-|$)", re.I), "2603.24981:biscope"),
    (re.compile(r"^(?:LLM-)?DetectAIve(?:\s|\[|\(|$)", re.I), "2505.14271:llmdetectaive"),
    (re.compile(r"^DeTeCtive(?:\s|\[|\(|$)", re.I), "2505.12507:detective"),
    (re.compile(r"^Longformer(?:\s|\[|\(|$)", re.I), "2607.14905:longformer"),
    (re.compile(r"^RoBERTa-Base(?:\s|\[|\(|$)", re.I), "2506.06705:roberta-base"),
    (re.compile(r"^RoBERTa-Large(?:\s|\[|\(|$)", re.I), "2506.06705:roberta-large"),
    (re.compile(r"^XLM-RoBERTa-Base(?:\s|\[|\(|$)", re.I), "2509.26051:xlm-roberta-base"),
    (re.compile(r"^XLM-RoBERTa-Large(?:\s|\[|\(|$)", re.I), "2512.21709:xlm-roberta-large"),
    (re.compile(r"^ModernBERT-Detect(?:\s|\[|\(|$)", re.I), "2502.15654:modernbert"),
    (re.compile(r"^RoBERTa-ChatGPT(?:\s|\[|\(|$)", re.I), "2504.11369:chatgpt-detector"),
)

NONDETECTOR_PATTERN = re.compile(
    r"^(?:average|avg\.?|all|total|human|machine|overall|macro|micro|mean|median|"
    r"english|russian|german|chinese|french|spanish|arabic|reviews?|arxiv|xsum|"
    r"reddit|finance|medicine|legal|news|wikipedia|wiki|yelp|squad|cmv|eli5|"
    r"open_qa|reddit_eli5|wiki_csai|hswag|roct|tldr|wp|dataset|domain|generator|"
    r"model|method|setting|rank team|test|train|validation|precision|recall|"
    r"detection accuracy|macro-f|auc|auroc|f1|tpr|fpr|accuracy|parameters?|"
    r"batch|length|time|memory|curvature|none|original|paraphr\.?|bt-fr|bt-tr)\b",
    re.IGNORECASE,
)
GENERATOR_PATTERN = re.compile(
    r"^(?:gpt(?:-|\s)?[2345]|chatgpt|claude|sonnet|haiku|gemini|llama|qwen|"
    r"deepseek|mistral|falcon|cohere|davinci|dolly|bloomz|glm|mercury|kimi|"
    r"minimax)(?:\b|[-_.])",
    re.IGNORECASE,
)
PROSE_PATTERN = re.compile(
    r"(?:\b(?:table|figure|equation|reports?|shows?|results?|performance|"
    r"increases?|producing|keeping|compared?|strongest|variants?|source|"
    r"samples?|steps?|learning rate|dilation rates?)\b|[=∼θ∆]|\{)",
    re.IGNORECASE,
)
METHOD_LIKE_PATTERN = re.compile(
    r"(?:detect|detector|gptzero|originality|winston|zerogpt|binoculars|radar|"
    r"gltr|likelihood|logrank|log-rank|entropy|lastde|biscope|reader|pawn|"
    r"roberta|deberta|longformer|bert|svm|xgb|random forest|\brf\b|\blr\b|"
    r"cnn|mlp|lstm|ensemble|classifier|baseline|vanilla|fomaml|faid|anchor|"
    r"uncertainty|divscore|specdetect|fourier|repreguard|w/o|without|full model)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Source:
    parent_id: str
    paper_path: str


@dataclass(frozen=True)
class Candidate:
    parent_id: str
    candidate_id: str
    page: int
    line: int
    table_locator: str
    trigger: str
    row_label: str
    context: str


@dataclass(frozen=True)
class Account:
    parent_id: str
    account_id: str
    system: str


@dataclass(frozen=True)
class Resolution:
    candidate: Candidate
    resolution_kind: str
    target_account_ids: tuple[str, ...]
    reason: str


def compact(value: str) -> str:
    return SPACE_PATTERN.sub(" ", CONTROL_PATTERN.sub("", value)).strip()


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def load_sources(path: Path) -> list[Source]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    sources = [Source(row["parent_id"], row["paper_path"]) for row in rows]
    if len(sources) != 119 or len({item.parent_id for item in sources}) != 119:
        raise ValueError("table discovery requires the exact 119-source corpus")
    return sources


def load_accounts(path: Path) -> list[Account]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    accounts = [Account(row["parent_id"], row["account_id"], row["system"]) for row in rows]
    if len(accounts) != len({item.account_id for item in accounts}):
        raise ValueError("duplicate account IDs")
    return accounts


def extract_text(path: Path) -> str:
    completed = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout.decode("utf-8", errors="replace")


def metric_trigger(line: str, metric_context: bool) -> str | None:
    if DECIMAL_METRIC_PATTERN.search(line):
        return "threshold_decimal"
    if PERCENT_METRIC_PATTERN.search(line):
        return "threshold_percent"
    if metric_context and WIDE_METRIC_PATTERN.search(line):
        return "threshold_wide"
    return None


def row_label(line: str) -> str | None:
    matches = list(NUMBER_PATTERN.finditer(line))
    match = matches[0] if matches else None
    if match is None:
        return None
    label = compact(line[: match.start()]).strip("|:;,-–—")
    if not label and len(matches) >= 2:
        label = f"numeric configuration {match.group()}"
    n_words = len(re.findall(r"[A-Za-z][A-Za-z-]*", label))
    if not label or not 1 <= n_words <= 20 or len(label) > 180:
        return None
    return label


def _locator(lines: list[str], index: int, previous_caption: str, section: str) -> str:
    captions = [
        (candidate_index, compact(line[match.start():]))
        for candidate_index, line in enumerate(lines)
        if (match := TABLE_PATTERN.search(line)) is not None
    ]
    before = [item for item in captions if item[0] <= index]
    after = [item for item in captions if item[0] > index]
    parts: list[str] = []
    if before:
        parts.append(f"preceding {max(before)[1][:180]}")
    elif previous_caption:
        parts.append(f"preceding {previous_caption[:180]}")
    if after:
        parts.append(f"following {min(after)[1][:180]}")
    if not parts:
        parts.append("table continuation")
    if section:
        parts.append(section)
    return compact(" | ".join(parts))


def discover(source: Source, paper_root: Path) -> list[Candidate]:
    text = extract_text(paper_root / source.paper_path)
    found: list[Candidate] = []
    absolute_line = 0
    previous_caption = ""
    active_section = ""
    for page_number, page in enumerate(text.split("\f"), start=1):
        lines = page.splitlines()
        page_start_line = absolute_line
        page_has_table = bool(previous_caption) or any(TABLE_PATTERN.search(line) for line in lines)
        page_has_metric = any(METRIC_HEADER_PATTERN.search(line) for line in lines)
        for index, raw_line in enumerate(lines):
            absolute_line += 1
            normalized_line = compact(raw_line)
            if (caption_match := TABLE_PATTERN.search(raw_line)) is not None:
                previous_caption = compact(raw_line[caption_match.start():])
            if SECTION_PATTERN.search(normalized_line):
                active_section = normalized_line
            if (
                not page_has_table
                or not page_has_metric
                or not re.search(r"\s{2,}", raw_line.strip())
                or not (
                    re.search(r"[A-Za-z]{2}", normalized_line)
                    or (
                        re.match(r"^\s*\d+(?:\.\d+)?\s{2,}", raw_line)
                        and len(NUMBER_PATTERN.findall(normalized_line)) >= 2
                    )
                )
            ):
                continue
            trigger = metric_trigger(normalized_line, page_has_metric)
            label = row_label(normalized_line) if trigger else None
            if trigger is None or label is None:
                continue
            start = max(0, index - 2)
            context = compact(" || ".join(lines[start : index + 1]))
            locator = _locator(lines, index, previous_caption, active_section)
            digest = hashlib.sha256(
                f"{source.parent_id}\t{page_number}\t{absolute_line}\t{normalized_line}".encode()
            ).hexdigest()[:16]
            found.append(
                Candidate(
                    source.parent_id,
                    f"{source.parent_id}:{digest}",
                    page_number,
                    absolute_line,
                    locator,
                    trigger,
                    label,
                    context,
                )
            )

        # Some PDFs print a detector name once as a multirow table heading and
        # put all numbers on the indented generator rows below it.  Those
        # headings would otherwise disappear because `row_label()` deliberately
        # requires a number on the same physical line.  Discover them directly
        # when at least two following rows contain threshold-scale values.  The
        # method identity, following numeric rows, and table locator are all
        # retained in the candidate ID/evidence so a curated account cannot
        # manufacture this state without matching frozen PDF content.
        if page_has_table:
            for index, raw_line in enumerate(lines):
                label = compact(raw_line).strip("|:;,-–—")
                words = re.findall(r"[A-Za-z][A-Za-z0-9+_.-]*", label)
                if (
                    not label
                    or NUMBER_PATTERN.search(label)
                    or not 1 <= len(words) <= 8
                    or len(label) > 100
                    or not METHOD_LIKE_PATTERN.search(label)
                    or normalized(label) in {"detector", "detectors", "method", "model", "baseline"}
                ):
                    continue
                following = [compact(line) for line in lines[index + 1 : index + 7]]
                threshold_rows = [
                    line
                    for line in following
                    if metric_trigger(line, True) is not None
                    and GENERATOR_PATTERN.search(line)
                ]
                if len(threshold_rows) < 2:
                    continue
                locator = _locator(lines, index, previous_caption, active_section)
                context = compact(" || ".join([raw_line, *lines[index + 1 : index + 7]]))
                line_number = page_start_line + index + 1
                digest = hashlib.sha256(
                    f"{source.parent_id}\t{page_number}\t{line_number}\tgrouped\t{label}\t{context}".encode()
                ).hexdigest()[:16]
                found.append(
                    Candidate(
                        source.parent_id,
                        f"{source.parent_id}:{digest}",
                        page_number,
                        line_number,
                        locator,
                        "grouped_threshold_rows",
                        label,
                        context,
                    )
                )
    return found


def discover_all(sources: list[Source], paper_root: Path) -> list[Candidate]:
    return [candidate for source in sources for candidate in discover(source, paper_root)]


def candidate_values(item: Candidate) -> tuple[str, ...]:
    return (
        item.parent_id,
        item.candidate_id,
        str(item.page),
        str(item.line),
        item.table_locator,
        item.trigger,
        item.row_label,
        item.context,
    )


def serialize(rows: list[Candidate]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(FIELDS)
    writer.writerows(candidate_values(item) for item in rows)
    return stream.getvalue()


def write(path: Path, rows: list[Candidate]) -> None:
    path.write_text(serialize(rows), encoding="utf-8")


def _account_aliases(account: Account) -> set[str]:
    slug = account.account_id.split(":", 1)[-1]
    system = re.split(
        r"\b(?:comparator|baseline|detector|trained on|target-adapted|with|using|after)\b",
        account.system,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]
    aliases = {normalized(slug), normalized(system), normalized(account.system)}
    return {alias for alias in aliases if len(alias) >= 4}


def _local_resolution(item: Candidate) -> tuple[str, tuple[str, ...]] | None:
    locator = item.table_locator
    current_line = item.context.rsplit(" || ", 1)[-1]
    for parent_id, label_pattern, locator_pattern, targets in LOCAL_RULES:
        if (
            item.parent_id == parent_id
            and (label_pattern.search(item.row_label) or label_pattern.search(current_line))
            and locator_pattern.search(locator)
        ):
            return "account_evidence", targets
    for parent_id, label_pattern, locator_pattern, targets in LOCAL_CARRY_RULES:
        if (
            item.parent_id == parent_id
            and (label_pattern.search(item.row_label) or label_pattern.search(current_line))
            and locator_pattern.search(locator)
        ):
            return "targeted_carry_forward", targets
    return None


def _local_false_resolution(item: Candidate) -> tuple[str, str] | None:
    current_line = item.context.rsplit(" || ", 1)[-1]
    for parent_id, label_pattern, locator_pattern, kind, reason in LOCAL_FALSE_RULES:
        if (
            item.parent_id == parent_id
            and (label_pattern.search(item.row_label) or label_pattern.search(current_line))
            and locator_pattern.search(item.table_locator)
        ):
            return kind, reason
    return None


def _matched_accounts(
    item: Candidate,
    by_parent: dict[str, list[tuple[str, str]]],
) -> tuple[str, tuple[str, ...]] | None:
    explicit = _local_resolution(item)
    if explicit is not None:
        return explicit
    label = normalized(item.row_label)
    same_parent: list[tuple[int, str]] = []
    for alias, account_id in by_parent.get(item.parent_id, []):
        if (
            label == alias
            or (len(alias) >= 6 and label.startswith(alias))
            or (len(label) >= 6 and alias.startswith(label))
        ):
            same_parent.append((len(alias), account_id))
    if same_parent:
        best = max(length for length, _ in same_parent)
        return "account_evidence", tuple(sorted({target for length, target in same_parent if length == best}))
    for pattern, target_id in CANONICAL_CARRY_RULES:
        if pattern.search(item.row_label):
            return "targeted_carry_forward", (target_id,)
    return None


def resolve_all(rows: list[Candidate], accounts: list[Account]) -> list[Resolution]:
    by_parent: dict[str, list[tuple[str, str]]] = {}
    for account in accounts:
        aliases = [
            (alias, account.account_id) for alias in _account_aliases(account)
        ]
        by_parent.setdefault(account.parent_id, []).extend(aliases)
    resolutions: list[Resolution] = []
    for item in rows:
        false_resolution = _local_false_resolution(item)
        matched = None if false_resolution is not None else _matched_accounts(item, by_parent)
        if false_resolution is not None:
            kind, reason = false_resolution
            targets = ()
        elif matched is not None:
            kind, targets = matched
            reason = (
                f"The exact row label and {item.table_locator} bind this high-metric row to "
                f"{', '.join(targets)}."
            )
        elif NONDETECTOR_PATTERN.search(item.row_label) or GENERATOR_PATTERN.search(item.row_label):
            kind, targets = "non_detector_row", ()
            reason = (
                f"The extracted label `{item.row_label}` is a dataset, domain, generator, "
                "aggregate, metric, or resource row rather than a detector system."
            )
        elif PROSE_PATTERN.search(item.row_label) or len(item.row_label.split()) > 10:
            kind, targets = "table_heading_or_prose", ()
            reason = (
                f"The extracted prefix `{item.row_label}` is a caption, equation, table "
                "heading, or prose fragment rather than a detector row."
            )
        elif not METHOD_LIKE_PATTERN.search(item.row_label):
            kind, targets = "nonqualifying_metric_context", ()
            reason = (
                f"The exact label `{item.row_label}` contains no detector identity; the "
                "high number belongs to table metadata, a corpus slice, or another reported quantity."
            )
        else:
            kind, targets = "UNRESOLVED", ()
            reason = (
                f"Method-like label `{item.row_label}` requires an account or a specific "
                "false-positive decision."
            )
        resolutions.append(Resolution(item, kind, targets, reason))
    return resolutions


def resolution_values(item: Resolution) -> tuple[str, ...]:
    return candidate_values(item.candidate) + (
        item.resolution_kind,
        ",".join(item.target_account_ids),
        item.reason,
    )


def serialize_resolutions(rows: list[Resolution]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(RESOLUTION_FIELDS)
    writer.writerows(resolution_values(item) for item in rows)
    return stream.getvalue()


def serialize_matches(rows: list[Candidate], accounts: list[Account]) -> str:
    return serialize_resolutions(resolve_all(rows, accounts))


def write_matches(path: Path, rows: list[Candidate], accounts: list[Account]) -> None:
    path.write_text(serialize_matches(rows, accounts), encoding="utf-8")


def content_requirements(resolutions: list[Resolution]) -> dict[str, set[str]]:
    discovered: dict[str, set[str]] = {}
    for item in resolutions:
        if item.resolution_kind == "account_evidence":
            discovered.setdefault(item.candidate.parent_id, set()).update(item.target_account_ids)
    missing = {
        parent_id: sorted(required - discovered.get(parent_id, set()))
        for parent_id, required in CONTENT_REQUIRED_ACCOUNT_IDS.items()
        if required - discovered.get(parent_id, set())
    }
    if missing:
        detail = "; ".join(f"{parent}: {','.join(ids)}" for parent, ids in missing.items())
        raise ValueError(f"content-required table accounts were not independently resolved: {detail}")
    return CONTENT_REQUIRED_ACCOUNT_IDS


def validate_resolutions(
    candidates: list[Candidate],
    resolutions: list[Resolution],
    accounts: list[Account],
) -> None:
    if len(candidates) != len(resolutions):
        raise ValueError("every table candidate must have exactly one resolution")
    candidate_ids = [item.candidate_id for item in candidates]
    resolved_candidates = [item.candidate for item in resolutions]
    if (
        len(candidate_ids) != len(set(candidate_ids))
        or candidates != resolved_candidates
    ):
        raise ValueError("table candidate/resolution identity mismatch")
    account_by_id = {item.account_id: item for item in accounts}
    for item in resolutions:
        if item.resolution_kind not in ALLOWED_RESOLUTIONS:
            raise ValueError(f"unresolved table candidate: {item.candidate.candidate_id}")
        if len(item.reason) < 40:
            raise ValueError(f"underspecified table resolution: {item.candidate.candidate_id}")
        if item.resolution_kind in {"account_evidence", "targeted_carry_forward", "duplicate_operating_point"}:
            if not item.target_account_ids:
                raise ValueError(f"targetless table resolution: {item.candidate.candidate_id}")
            for target_id in item.target_account_ids:
                target = account_by_id.get(target_id)
                if target is None:
                    raise ValueError(f"unknown table-resolution target: {target_id}")
                if item.resolution_kind == "account_evidence" and target.parent_id != item.candidate.parent_id:
                    raise ValueError(f"cross-parent account evidence: {item.candidate.candidate_id}")
        elif item.target_account_ids:
            raise ValueError(f"false-positive resolution has a target: {item.candidate.candidate_id}")
    content_requirements(resolutions)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--paper-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--accounts", type=Path)
    parser.add_argument("--match-output", type=Path)
    args = parser.parse_args()
    sources = load_sources(args.sources)
    candidates = discover_all(sources, args.paper_root)
    write(args.output, candidates)
    if (args.accounts is None) != (args.match_output is None):
        raise ValueError("--accounts and --match-output must be supplied together")
    unresolved = 0
    if args.accounts is not None and args.match_output is not None:
        accounts = load_accounts(args.accounts)
        resolutions = resolve_all(candidates, accounts)
        unresolved = sum(item.resolution_kind == "UNRESOLVED" for item in resolutions)
        if unresolved == 0:
            validate_resolutions(candidates, resolutions, accounts)
        args.match_output.write_text(
            serialize_resolutions(resolutions), encoding="utf-8"
        )
    print(
        f"sources={len(sources)} table_candidates={len(candidates)} "
        f"unresolved={unresolved}"
    )


if __name__ == "__main__":
    main()
