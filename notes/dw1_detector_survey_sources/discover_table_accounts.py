#!/usr/bin/env python3
"""Extract and resolve high-metric content from the frozen PDF corpus."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import re
import subprocess
import unicodedata
from dataclasses import dataclass
from pathlib import Path


CAPTION_NUMBER = r"(?:[A-Z]?\d+[A-Za-z]?|[IVXLCDM]+)"
TABLE_PATTERN = re.compile(
    rf"(?:^|\s{{2,}})(?:table|tab\.?)\s+{CAPTION_NUMBER}\b",
    re.IGNORECASE,
)
ROMAN_TABLE_PATTERN = re.compile(
    r"(?:^|\s{2,})(?:table|tab\.?)\s+[IVXLCDM]+\b",
    re.IGNORECASE,
)
FIGURE_PATTERN = re.compile(
    rf"(?:^|\s{{2,}})(?:figure|fig\.?)\s+{CAPTION_NUMBER}\b",
    re.IGNORECASE,
)
CAPTION_PATTERN = re.compile(
    rf"(?:^|\s{{2,}})(?:(?:table|tab\.?)|(?:figure|fig\.?))\s+{CAPTION_NUMBER}\b",
    re.IGNORECASE,
)
SECTION_PATTERN = re.compile(
    r"(?:no training on RAID|\d+\s+epoch(?:s)?\s+fine[- ]tun(?:e|ing)|"
    r"without fine[- ]tuning|with fine[- ]tuning)",
    re.IGNORECASE,
)
METRIC_HEADER_PATTERN = re.compile(
    r"\b(?:auc|auroc|roc[- ]auc|accuracy|balanced accuracy|bacc|"
    r"macro[- ]?f\s*1|f\s*1|precision|recall|tpr|true positive rate|"
    r"humanrec|machinerec|avgrec)\b",
    re.IGNORECASE,
)
DECIMAL_METRIC_PATTERN = re.compile(r"(?<![\d.])(?:0?\.9\d*|1\.0+)(?![\d.%])")
PERCENT_METRIC_PATTERN = re.compile(
    r"(?<![\d.])(?:9\d(?:\.\d+)?|100(?:\.0+)?)\s*%(?!\d)"
)
WIDE_METRIC_PATTERN = re.compile(r"(?<![\d.])(?:9\d(?:\.\d+)?|100(?:\.0+)?)(?![\d.])")
HIGH_CLAIM_PATTERN = re.compile(
    r"\b(?:state[- ]of[- ]the[- ]art|sota|best performance|highest performance|"
    r"outperforms?\s+(?:all|the best|the strongest)|superior performance)\b",
    re.IGNORECASE,
)
STRONG_CLAIM_METHOD_PATTERN = re.compile(
    r"\b(?:Luminol-AIDetect|Fast(?:-\s*)?DetectGPT|Binoculars|"
    r"DeTeCtive|DetectAIve|PAWN|MELD|NEULIF|LM2otifs)\b",
    re.IGNORECASE,
)
FIGURE_LABEL_PATTERN = re.compile(
    r"(?:detect|gpt|llama|gemini|deepseek|claude|mistral|qwen|roberta|deberta|"
    r"binoculars|radar|raidar|glimpse|camf|pawn|faid|biscope|longformer|"
    r"ensemble|classifier|baseline)",
    re.IGNORECASE,
)
FIGURE_LEGEND_TOKEN_PATTERN = re.compile(
    r"^(?:GPT(?:-[A-Za-z0-9.]+)+|Llama[A-Za-z0-9. ._-]*|"
    r"Gemini-[A-Za-z0-9.]+(?:\s+Pro)?|DeepSeek-[A-Za-z0-9.]+|"
    r"Claude[A-Za-z0-9. ._-]*|Mistral[A-Za-z0-9. ._-]*|"
    r"Qwen[A-Za-z0-9. ._-]*)$",
    re.IGNORECASE,
)
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
WITNESS_FIELDS = (
    "parent_id",
    "account_id",
    "witness_id",
    "join_kind",
    "join_key",
    "identity_page",
    "identity_line",
    "identity_locator",
    "identity_text",
    "metric_page",
    "metric_line",
    "metric_locator",
    "metric_text",
    "metric_value",
    "raw_candidate_id",
    "source_text_sha256",
)
ALLOWED_RESOLUTIONS = {
    "account_evidence",
    "targeted_carry_forward",
    "duplicate_operating_point",
    "source_scope_summary",
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
2501.03940:radar-ft 2501.03940:mage-longformer 2501.03940:gltr
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
2607.22026:equal-hard 2607.22026:equal-soft
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
    "2605.16107": _ids("""
2605.16107:likelihood 2605.16107:logrank 2605.16107:entropy
2605.16107:detectgpt 2605.16107:fastgpt 2605.16107:binoculars
2605.16107:fouriergpt 2605.16107:adagpt
"""),
    "2604.02008": _ids("""
2604.02008:likelihood 2604.02008:logrank
2604.02008:fastdetectgpt 2604.02008:binoculars
2604.02008:fastdetectgpt-dald
2604.02008:fastdetectgpt-glimpse-gpt4-geometric
2604.02008:fastdetectgpt-glimpse-gpt4-zipfian
2604.02008:fastdetectgpt-glimpse-gpt4-mlp
2604.02008:fastdetectgpt-glimpse-davinci-geometric
2604.02008:binoculars-dald
"""),
    "2510.02319": _ids("""
2510.02319:fastdetectgpt 2510.02319:glimpse
2510.02319:binoculars 2510.02319:logrank
"""),
    "2508.11933": _ids("""
2508.11933:raidar 2508.11933:gpt4o-direct
2508.11933:gpt-cot 2508.11933:gpt-react
2508.11933:gpt4o-mini 2508.11933:gemini15-pro
2508.11933:deepseek-v3
"""),
    "2602.11871": _ids("""
2602.11871:fdgpt-llama 2602.11871:fdgpt-mistral
2602.11871:fdgpt-qwen 2602.11871:binoculars-llama
2602.11871:binoculars-mistral 2602.11871:binoculars-qwen
"""),
    "2505.11550": _ids("""
2505.11550:full 2505.11550:optimized 2505.11550:simple
"""),
}

PREDECESSOR_ZERO_YIELD_PARENT_IDS = {
    "2607.23805",
    "2605.16107",
    "2604.25860",
    "2604.02008",
    "2604.19768",
    "2601.03812",
    "2512.21709",
    "2510.22874",
    "2510.16573",
    "2510.16549",
    "2510.12608",
    "2510.02319",
    "2508.11933",
    "2501.14288",
}
SPLIT_COLUMN_PARENT_IDS = {"2501.14288"}
EXPANDED_GROUP_PARENT_IDS = {"2510.02319"}
STRONG_CLAIM_PARENT_IDS = {"2604.25860"}
DECLARED_STATE_PATTERNS: dict[str, tuple[re.Pattern[str], ...]] = {
    "2605.16107": (re.compile(r"\bDetectLLM-M\b(?!ult)", re.I),),
    "2604.02008": (re.compile(r"♠\s*\+\s*MoP\s*\(Ours\)", re.I),),
}
DECLARED_STATE_LOCATORS = {
    "2605.16107": re.compile(r"Table (?:II|III)", re.I),
    "2604.02008": re.compile(r"Table V", re.I),
}

ROMAN_CONTENT_ACCOUNT_IDS = set().union(
    CONTENT_REQUIRED_ACCOUNT_IDS["2605.16107"],
    CONTENT_REQUIRED_ACCOUNT_IDS["2604.02008"],
    CONTENT_REQUIRED_ACCOUNT_IDS["2510.02319"],
    {
        "2508.11933:raidar",
        "2508.11933:gpt4o-direct",
        "2508.11933:gpt-cot",
        "2508.11933:gpt-react",
    },
)
FIGURE_CONTENT_ACCOUNT_IDS = {
    "2508.11933:gpt35",
    "2508.11933:gpt4o",
    "2508.11933:llama3-70b",
    "2508.11933:gpt4o-mini",
    "2508.11933:gemini15-pro",
    "2508.11933:deepseek-v3",
}
FIGURE_SERIES_ACCOUNTS = {
    "2508.11933:gpt35": ("GPT-3.5-Turbo", "95.18", 1),
    "2508.11933:gpt4o": ("GPT-4o", "98.49", 2),
    "2508.11933:gpt4o-mini": ("GPT-4o-mini", "96.89", 3),
    "2508.11933:llama3-70b": ("Llama3-70B", "96.64", 4),
    "2508.11933:gemini15-pro": ("Gemini-1.5 Pro", "96.45", 5),
    "2508.11933:deepseek-v3": ("DeepSeek-V3", "95.60", 6),
}
OFFPAGE_METRIC_ACCOUNT_IDS = CONTENT_REQUIRED_ACCOUNT_IDS["2602.11871"]

SHARED_TASK_RANKS = {
    "2501.11012:english-advacheck": ("English", "1"),
    "2501.11012:english-unibuc-nlp": ("English", "2"),
    "2501.11012:english-fraunhofer-sit": ("English", "3"),
    "2501.11012:english-grape": ("English", "4"),
    "2501.11012:english-techexperts-ipn": ("English", "5"),
    "2501.11012:english-turquaz": ("English", "6"),
    "2501.11012:english-szegedai": ("English", "7"),
    "2501.11012:english-aaig": ("English", "8"),
    "2501.11012:english-dcbu": ("English", "9"),
    "2501.11012:english-alfa": ("English", "10"),
    "2501.11012:english-l3i-plus-plus": ("English", "11"),
    "2501.11012:english-luxveri": ("English", "12"),
    "2501.11012:english-azlearning": ("English", "13"),
    "2501.11012:english-honghanhh": ("English", "14"),
    "2501.11012:english-baseline": ("English", "BL"),
    "2501.11012:english-vx1291": ("English", "15"),
    "2501.11012:english-rockstart": ("English", "16"),
    "2501.11012:multilingual-grape": ("Multilingual", "1"),
    "2501.11012:multilingual-rockstart": ("Multilingual", "2"),
    "2501.11012:multilingual-nota-ai": ("Multilingual", "3"),
    "2501.11012:multilingual-luxveri": ("Multilingual", "4"),
    "2501.11012:multilingual-techexperts-ipn": ("Multilingual", "5"),
    "2501.11012:multilingual-azlearning": ("Multilingual", "6"),
    "2501.11012:multilingual-nampfiev1995": ("Multilingual", "7"),
    "2501.11012:multilingual-baseline": ("Multilingual", "BL"),
    "2501.11012:multilingual-starlight1": ("Multilingual", "8"),
    "2501.11012:multilingual-abit7431": ("Multilingual", "9"),
    "2501.11012:multilingual-fraunhofer-sit": ("Multilingual", "10"),
    "2501.11012:multilingual-mail6djj": ("Multilingual", "11"),
    "2501.11012:multilingual-saehyunma": ("Multilingual", "12"),
    "2501.11012:multilingual-seven": ("Multilingual", "13"),
    "2501.11012:multilingual-jojoc": ("Multilingual", "14"),
    "2501.11012:multilingual-yaoxy": ("Multilingual", "16"),
    "2501.11012:multilingual-bennben": ("Multilingual", "18"),
    "2501.11012:multilingual-fangsifan": ("Multilingual", "19"),
    "2501.11012:multilingual-yuwert777": ("Multilingual", "20"),
    "2501.11012:multilingual-honghanhh": ("Multilingual", "21"),
    "2501.11012:multilingual-tmarchitan": ("Multilingual", "22"),
    "2501.11012:multilingual-sohailwaleed2": ("Multilingual", "24"),
}

LOW_ERROR_ACCOUNT_IDS = {
    "2604.25860:binoculars",
    "2604.25860:fastdetectgpt",
}

TABLE_COLUMN_ACCOUNTS = {
    "2501.03940:m4-roberta-base": (
        "RoBERTa",
        "Average",
        "0.970",
        3,
    ),
    "2501.03940:m4-xlm-roberta": (
        "XLM-RoBERTa",
        "Arabic",
        "92.18",
        3,
    ),
}

# These configurations share a printed row but own distinct result columns.  The
# tuple is (table token, row label, metric, ordered result columns, zero-based
# result-column index, expected value).  Witness generation re-parses the bound
# PDF header and row from scratch; the curated account inventory supplies only
# the identity to be checked, never a substitute metric.
TABLE_METRIC_COLUMN_ACCOUNTS: dict[
    str, tuple[str, str, str, tuple[str, ...], int, str]
] = {
    "2608.03859:pan12-ngram": (
        "table1",
        "PAN12-style n-gram overlap",
        "recall",
        ("Prec.", "Rec.", "F1", "FPR", "BAcc.", "MCC", "AUROC", "AP"),
        1,
        "0.9602",
    ),
    "2607.03680:vanilla-faid-extra-domain": (
        "table4",
        "Vanilla + extra",
        "accuracy",
        (
            "FAIDSet (in-dom)",
            "Unseen Domain",
            "Unseen Generator",
            "Unseen Domain+Generator",
        ),
        1,
        "91.5",
    ),
    "2607.03680:vanilla-faid-extra-domain-generator": (
        "table4",
        "Vanilla + extra",
        "accuracy",
        (
            "FAIDSet (in-dom)",
            "Unseen Domain",
            "Unseen Generator",
            "Unseen Domain+Generator",
        ),
        3,
        "88.2",
    ),
    "2607.03680:pooled-four-way": (
        "table11",
        "IntelLabs",
        "AUROC",
        ("4-way Mixed", "Strat base", "Strat large", "Best Single"),
        0,
        "0.968",
    ),
    "2607.03680:pooled-stratified-base": (
        "table11",
        "IntelLabs",
        "AUROC",
        ("4-way Mixed", "Strat base", "Strat large", "Best Single"),
        1,
        "0.970",
    ),
    "2607.03680:pooled-stratified-large": (
        "table11",
        "IntelLabs",
        "AUROC",
        ("4-way Mixed", "Strat base", "Strat large", "Best Single"),
        2,
        "0.997",
    ),
}


# These named architectures qualify through the paper's explicit robustness and
# generalisation claim, while their architecture-owned Table 2 cells are below
# 0.90.  Each witness must therefore join the common claim candidate to one
# literal architecture/configuration row and one declared result column; a
# nearby Longformer cell is never an admissible substitute.
TABLE_CONFIGURATION_CLAIM_ACCOUNTS: dict[
    str, tuple[str, str, str, tuple[str, ...], int, str]
] = {
    "2607.14905:gcn": (
        "table2",
        "GCN argmax none",
        "macro F1",
        (
            "Orig.",
            "Paraphr.",
            "BT-FR",
            "BT-TR",
            "Orig.",
            "Paraphr.",
            "BT-FR",
            "BT-TR",
        ),
        4,
        "0.68",
    ),
    "2607.14905:gat": (
        "table2",
        "GAT argmax none",
        "macro F1",
        (
            "Orig.",
            "Paraphr.",
            "BT-FR",
            "BT-TR",
            "Orig.",
            "Paraphr.",
            "BT-FR",
            "BT-TR",
        ),
        4,
        "0.75",
    ),
    "2607.14905:graph-transformer": (
        "table2",
        "Graph Transformer argmax none",
        "macro F1",
        (
            "Orig.",
            "Paraphr.",
            "BT-FR",
            "BT-TR",
            "Orig.",
            "Paraphr.",
            "BT-FR",
            "BT-TR",
        ),
        4,
        "0.78",
    ),
    "2607.14905:gps": (
        "table2",
        "GPS argmax none",
        "macro F1",
        (
            "Orig.",
            "Paraphr.",
            "BT-FR",
            "BT-TR",
            "Orig.",
            "Paraphr.",
            "BT-FR",
            "BT-TR",
        ),
        4,
        "0.78",
    ),
}

WEAK_STATE_ACCOUNTS = {
    "2607.22026:window-std": (
        "window_std",
        "0.7137",
        "table7",
        "window-std",
    ),
    "2605.02712:qwen3-32b-st-07": (
        "Qwen3-32B_ST_th0.7",
        "0.78",
        "table1",
        "selected-task10-submission",
    ),
    "2502.12734:greater-a-zero-query": (
        "GREATER-A",
        "69.11",
        "table2",
        "zero-query",
    ),
    "2502.12064:english-gpt2-small": (
        "gpt2-small",
        "0.8019",
        "table4",
        "english",
    ),
    "2502.12064:multilingual-gpt2-xl": (
        "gpt2-xl",
        "0.6620",
        "table6",
        "multilingual",
    ),
    "2501.11914:inverse-perplexity-en": (
        "Inverse Perplexity",
        "0.7458",
        "table5",
        "english",
    ),
    "2501.11914:inverse-perplexity-multi": (
        "Inverse Perplexity",
        "0.7513",
        "table5",
        "multilingual",
    ),
}

SOURCE_TABLE_COLUMN_ACCOUNTS = {
    "2502.12734:greater-d": (
        "GREATER-D",
        "Avg.",
        "1.78",
        "table1",
        12,
    ),
}

DEER_ROUTING_FIGURE_ACCOUNTS = {
    "2511.01192:domain-f1": ("Domain-Matching (F1)", "91.4", "f1", 1),
    "2511.01192:domain-entropy": (
        "Domain-Matching (Entropy)",
        "1.05",
        "entropy",
        2,
    ),
    "2511.01192:reward-f1": ("Reward-Driven (F1)", "94.1", "f1", 3),
    "2511.01192:reward-entropy": (
        "Reward-Driven (Entropy)",
        "0.39",
        "entropy",
        4,
    ),
}

FIGURE_CLASSIFIER_ACCOUNTS = {
    "2502.12611:xgb-classifier": "0.99",
    "2502.12611:extra-trees": "0.99",
    "2502.12611:mlp-classifier": "0.99",
    "2502.12611:linear-svc": "0.98",
    "2502.12611:random-forest": "0.98",
    "2502.12611:linear-discriminant-analysis": "0.98",
    "2502.12611:logistic-regression": "0.97",
    "2502.12611:bagging-classifier": "0.97",
    "2502.12611:voting-classifier": "0.97",
    "2502.12611:decision-tree": "0.96",
    "2502.12611:gradient-boosting": "0.95",
    "2502.12611:adaboost": "0.94",
    "2502.12611:extra-tree": "0.91",
    "2502.12611:bernoulli-nb": "0.90",
}
VISUAL_FIGURE_ACCOUNT_IDS = set(FIGURE_CLASSIFIER_ACCOUNTS)

VERTICAL_GROUP_ACCOUNTS = {
    "2510.16549:qwen3-rs": ("Qwen 3-8B", "Precision", "0.9034", "tablevi"),
}

REACT_SHOT_ACCOUNTS = {
    "2605.02374:react-32shot": "32",
    "2605.02374:react-64shot": "64",
    "2605.02374:react-128shot": "128",
    "2605.02374:react-256shot": "256",
}

ACCOUNT_IDENTITY_ALIASES: dict[str, tuple[str, ...]] = {
    "2606.31074:triospect-fastdetectgpt": ("Triospect (Fast-Detect)",),
    "2605.06903:paper-era": ("MELD (ours)",),
    "2601.04833:dd": ("DD",),
    "2601.04833:lv": ("LV",),
    "2601.04833:tsd": ("TSD",),
    "2505.12507:lm2": ("LM2 OTIFS",),
    "2505.11550:full": ("Full Architecture",),
    "2505.11550:optimized": ("Optimized Architecture",),
    "2505.11550:simple": ("Simple Architecture",),
    "2504.11369:lm-d": ("LM-D",),
    "2501.18998:fastdetectgpt-baseline": ("Fast-DetectGPT",),
    "2507.23577:ct-tdetect": ("CT (Framework)",),
    "2502.12734:greater-d": ("GREATER-D",),
    "2502.12734:greater-a-query": ("GREATER-A",),
    "2502.12734:greater-a-zero-query": ("GREATER-A",),
    "2501.03940:ens-2gpt2": ("2 GPT2",),
    "2501.03940:m4-roberta-base": ("RoBERTa",),
    "2501.03940:m4-xlm-roberta": ("XLM-RoBERTa",),
    "2501.11914:inverse-perplexity-en": ("Inverse Perplexity",),
    "2501.11914:inverse-perplexity-multi": ("Inverse Perplexity",),
    "2511.01192:domain-f1": ("Domain-Matching (F1)",),
    "2511.01192:domain-entropy": ("Domain-Matching (Entropy)",),
    "2511.01192:reward-f1": ("Reward-Driven (F1)",),
    "2511.01192:reward-entropy": ("Reward-Driven (Entropy)",),
}
ACCOUNT_IDENTITY_ALIASES.update(
    {account_id: ("REACT (Ours)",) for account_id in REACT_SHOT_ACCOUNTS}
)


# Parent-local content aliases handle typography and distinguish repeated fitted
# states whose printed names are identical.  Generic account matching handles all
# remaining inventory rows.
LOCAL_RULES: tuple[
    tuple[str, re.Pattern[str], re.Pattern[str], tuple[str, ...]], ...
] = (
    (
        "2608.03859",
        re.compile(r"^PAN12-style n-gram overlap", re.I),
        re.compile(r"Table 1", re.I),
        ("2608.03859:pan12-ngram",),
    ),
    (
        "2607.14905",
        re.compile(r"^baseline\. In the S AME", re.I),
        re.compile(r"Table 3", re.I),
        (
            "2607.14905:gcn",
            "2607.14905:gat",
            "2607.14905:graph-transformer",
            "2607.14905:gps",
        ),
    ),
    (
        "2505.11550",
        re.compile(r"^Full Architecture$", re.I),
        re.compile(r"Table 2", re.I),
        ("2505.11550:full",),
    ),
    (
        "2505.11550",
        re.compile(r"^Optimized Architecture$", re.I),
        re.compile(r"Table 2", re.I),
        ("2505.11550:optimized",),
    ),
    (
        "2505.11550",
        re.compile(r"^Simple Architecture$", re.I),
        re.compile(r"Table 2", re.I),
        ("2505.11550:simple",),
    ),
    (
        "2501.03940",
        re.compile(r"^XLM[- ]?RoBERTa", re.I),
        re.compile(r"Table 9", re.I),
        ("2501.03940:m4-xlm-roberta",),
    ),
    (
        "2501.03940",
        re.compile(r"^R-B GPT2", re.I),
        re.compile(r"Table 10", re.I),
        ("2501.03940:raid-rb-gpt2",),
    ),
    (
        "2501.03940",
        re.compile(r"^R-L GPT2", re.I),
        re.compile(r"Table 10", re.I),
        ("2501.03940:raid-rl-gpt2",),
    ),
    (
        "2501.03940",
        re.compile(r"^R-B CGPT", re.I),
        re.compile(r"Table 10", re.I),
        ("2501.03940:raid-rb-cgpt",),
    ),
    (
        "2501.03940",
        re.compile(r"^F-DetectGPT", re.I),
        re.compile(r"Table 10", re.I),
        ("2501.03940:raid-fastdetectgpt",),
    ),
    (
        "2501.03940",
        re.compile(r"^GPTZero", re.I),
        re.compile(r"Table 10", re.I),
        ("2501.03940:raid-gptzero",),
    ),
    (
        "2501.03940",
        re.compile(r"^Originality", re.I),
        re.compile(r"Table 10", re.I),
        ("2501.03940:raid-originality",),
    ),
    (
        "2501.03940",
        re.compile(r"^Winston", re.I),
        re.compile(r"Table 10", re.I),
        ("2501.03940:raid-winston",),
    ),
    (
        "2501.03940",
        re.compile(r"^ZeroGPT", re.I),
        re.compile(r"Table 10", re.I),
        ("2501.03940:raid-zerogpt",),
    ),
    (
        "2501.03940",
        re.compile(r"^PAWN\s*\(GPT2\)", re.I),
        re.compile(r"Table 10.*1 epoch", re.I),
        ("2501.03940:raidft-pawn-gpt2",),
    ),
    (
        "2501.03940",
        re.compile(r"^PAWN\s*\(Llama", re.I),
        re.compile(r"Table 10.*1 epoch", re.I),
        ("2501.03940:raidft-pawn-llama",),
    ),
    (
        "2501.03940",
        re.compile(r"^Longformer", re.I),
        re.compile(r"Table 10.*1 epoch", re.I),
        ("2501.03940:raidft-longformer",),
    ),
    (
        "2501.03940",
        re.compile(r"^RoBERTa", re.I),
        re.compile(r"Table 10.*1 epoch", re.I),
        ("2501.03940:raidft-roberta",),
    ),
    (
        "2501.03940",
        re.compile(r"^RADAR-PTM", re.I),
        re.compile(r"Table 10.*1 epoch", re.I),
        ("2501.03940:raidft-radar-ptm",),
    ),
    (
        "2501.03940",
        re.compile(r"^RADAR(?:\s|$)", re.I),
        re.compile(r"Table 10.*1 epoch", re.I),
        ("2501.03940:raidft-radar",),
    ),
    (
        "2501.03940",
        re.compile(r"^Longformer", re.I),
        re.compile(r"Table 10", re.I),
        ("2501.03940:mage-longformer",),
    ),
    (
        "2501.03940",
        re.compile(r"^RoBERTa", re.I),
        re.compile(r"Table 10", re.I),
        ("2501.03940:mage-roberta-base",),
    ),
    (
        "2501.03940",
        re.compile(r"^RADAR-PTM", re.I),
        re.compile(r"Table 10", re.I),
        ("2501.03940:mage-radar-ptm",),
    ),
    (
        "2501.03940",
        re.compile(r"^RADAR(?:\s|$)", re.I),
        re.compile(r"Table 10", re.I),
        ("2501.03940:raid-radar",),
    ),
    (
        "2501.03940",
        re.compile(r"^Binoculars", re.I),
        re.compile(r"Table 10", re.I),
        ("2501.03940:raid-binoculars",),
    ),
    (
        "2501.03940",
        re.compile(r"^GLTR", re.I),
        re.compile(r"Table (?:4|5|10)", re.I),
        ("2501.03940:gltr",),
    ),
    (
        "2607.03680",
        re.compile(r"^Longformer", re.I),
        re.compile(r"Table 3", re.I),
        ("2607.03680:mage-longformer",),
    ),
    (
        "2607.03680",
        re.compile(r"^Vanilla\s*\+\s*extra", re.I),
        re.compile(r"Table 4", re.I),
        (
            "2607.03680:vanilla-faid-extra-domain",
            "2607.03680:vanilla-faid-extra-domain-generator",
        ),
    ),
    (
        "2607.03680",
        re.compile(r"^Vanilla\s*\(base\)", re.I),
        re.compile(r"Table 8", re.I),
        ("2607.03680:vanilla-mirage-base",),
    ),
    (
        "2605.25281",
        re.compile(r"^NPR", re.I),
        re.compile(r"Table (?:8|9|14)", re.I),
        ("2605.25281:npr-gemma",),
    ),
    (
        "2605.25281",
        re.compile(r"^NPR", re.I),
        re.compile(r"Table (?:10|11|15)", re.I),
        ("2605.25281:npr-qwen",),
    ),
    (
        "2605.25281",
        re.compile(r"^D\s*ETECT\s*GPT|^DetectGPT", re.I),
        re.compile(r"Table (?:8|9|14)", re.I),
        ("2605.25281:detectgpt-gemma",),
    ),
    (
        "2605.25281",
        re.compile(r"^D\s*ETECT\s*GPT|^DetectGPT", re.I),
        re.compile(r"Table (?:10|11|15)", re.I),
        ("2605.25281:detectgpt-qwen",),
    ),
    (
        "2605.25281",
        re.compile(r"^B\s*INOCULARS|^Binoculars", re.I),
        re.compile(r"Table (?:8|9|14)", re.I),
        ("2605.25281:binoculars-gemma",),
    ),
    (
        "2605.25281",
        re.compile(r"^B\s*I\s*SCOPE\s*[∗*]", re.I),
        re.compile(r"Table (?:3|14)", re.I),
        ("2605.25281:biscope-target-adapted",),
    ),
    (
        "2605.25281",
        re.compile(r"^B\s*I\s*SCOPE", re.I),
        re.compile(r"Table (?:2|3|14|15)", re.I),
        ("2605.25281:biscope-read",),
    ),
    (
        "2605.25281",
        re.compile(r"^A\s*DA\s*D\s*ETECT\s*GPT\s*[∗*]", re.I),
        re.compile(r"Table 14", re.I),
        ("2605.25281:adadetectgpt-gemma-target",),
    ),
    (
        "2605.25281",
        re.compile(r"^A\s*DA\s*D\s*ETECT\s*GPT", re.I),
        re.compile(r"Table (?:8|9|14)", re.I),
        ("2605.25281:adadetectgpt-gemma",),
    ),
    (
        "2501.03940",
        re.compile(r"XLM[- ]?RoBERTa", re.I),
        re.compile(r"Table 9", re.I),
        ("2501.03940:m4-xlm-roberta",),
    ),
    (
        "2501.03940",
        re.compile(r"^RoBERTa", re.I),
        re.compile(r"Table 9", re.I),
        ("2501.03940:m4-roberta-base",),
    ),
    (
        "2501.03940",
        re.compile(r"^Longformer", re.I),
        re.compile(r"Table (?:4|5)", re.I),
        ("2501.03940:mage-longformer",),
    ),
    (
        "2501.03940",
        re.compile(r"^None", re.I),
        re.compile(r"Table 12", re.I),
        ("2501.03940:raid-rb-cgpt",),
    ),
    (
        "2607.03680",
        re.compile(r"^FAID(?:\s|$)", re.I),
        re.compile(r"Table 4", re.I),
        ("2607.03680:faid",),
    ),
    (
        "2607.03680",
        re.compile(r"^IntelLabs\s*\(base\)", re.I),
        re.compile(r"Table 5", re.I),
        ("2607.03680:vanilla-intellabs-base",),
    ),
    (
        "2607.03680",
        re.compile(r"^MAGE\s*\(large\)", re.I),
        re.compile(r"Table 5", re.I),
        ("2607.03680:vanilla-mage-large",),
    ),
    (
        "2607.03680",
        re.compile(r"^FAID\s*\(base\)", re.I),
        re.compile(r"Table 5", re.I),
        ("2607.03680:vanilla-faid-base",),
    ),
    (
        "2607.03680",
        re.compile(r"^MIRAGE\s*\(large\)", re.I),
        re.compile(r"Table 5", re.I),
        ("2607.03680:vanilla-mirage-large",),
    ),
    (
        "2607.03680",
        re.compile(r"^Vanilla\s*\(base\)", re.I),
        re.compile(r"Table (?:8|9)", re.I),
        ("2607.03680:vanilla-mirage-base",),
    ),
    (
        "2607.03680",
        re.compile(r"^Vanilla\s*\(large\)$", re.I),
        re.compile(r"Table 8", re.I),
        ("2607.03680:vanilla-mirage-large",),
    ),
    (
        "2607.03680",
        re.compile(r"^Vanilla\s*\(large\)\s*\(ours", re.I),
        re.compile(r"Table 9", re.I),
        ("2607.03680:vanilla-mage-large",),
    ),
    (
        "2607.03680",
        re.compile(r"^Longformer\s*\(paper", re.I),
        re.compile(r"Table 9", re.I),
        ("2607.03680:mage-longformer",),
    ),
    (
        "2607.03680",
        re.compile(r"^numeric configuration 5$", re.I),
        re.compile(r"Table 10", re.I),
        ("2607.03680:fomaml-hc3-k5",),
    ),
    (
        "2607.03680",
        re.compile(r"^numeric configuration 10$", re.I),
        re.compile(r"Table 10", re.I),
        ("2607.03680:fomaml-lora",),
    ),
    (
        "2607.03680",
        re.compile(r"^numeric configuration 20$", re.I),
        re.compile(r"Table 10", re.I),
        ("2607.03680:fomaml-hc3-k20",),
    ),
    (
        "2607.03680",
        re.compile(r"^numeric configuration 50$", re.I),
        re.compile(r"Table 10", re.I),
        ("2607.03680:fomaml-hc3-k50",),
    ),
    (
        "2607.03680",
        re.compile(r"^(?:IntelLabs|MAGE|FAID|MIRAGE)$", re.I),
        re.compile(r"Table 11", re.I),
        (
            "2607.03680:pooled-four-way",
            "2607.03680:pooled-stratified-base",
            "2607.03680:pooled-stratified-large",
        ),
    ),
    (
        "2607.03680",
        re.compile(r"^w\s*·\s*pvanilla", re.I),
        re.compile(r"Table 13", re.I),
        ("2607.03680:confidence-ensemble",),
    ),
    (
        "2607.03680",
        re.compile(r"^w\s*·\s*pFOMAML", re.I),
        re.compile(r"Table 13", re.I),
        ("2607.03680:reverse-confidence-ensemble",),
    ),
    (
        "2606.02158",
        re.compile(r"^w/o low-probability", re.I),
        re.compile(r"Table 3", re.I),
        ("2606.02158:without-low-probability",),
    ),
    (
        "2606.02158",
        re.compile(r"^w/o entropy", re.I),
        re.compile(r"Table 3", re.I),
        ("2606.02158:without-entropy",),
    ),
    (
        "2506.06705",
        re.compile(r"^RoB-base", re.I),
        re.compile(r"Table (?:1|2)", re.I),
        ("2506.06705:roberta-base",),
    ),
    (
        "2506.06705",
        re.compile(r"^RoB-large", re.I),
        re.compile(r"Table (?:1|2)", re.I),
        ("2506.06705:roberta-large",),
    ),
    (
        "2606.07313",
        re.compile(r"^SV-Detect\s*\(polish-only\)", re.I),
        re.compile(r"Table (?:8|9)", re.I),
        ("2606.07313:polish-only",),
    ),
    (
        "2606.07313",
        re.compile(r"^SV-Detect\s*\(3-task\)", re.I),
        re.compile(r"Table (?:8|9)", re.I),
        ("2606.07313:three-task",),
    ),
    (
        "2506.01702",
        re.compile(r"^TF-IDF baseline", re.I),
        re.compile(r"Table 1", re.I),
        ("2506.01702:tfidf-baseline",),
    ),
    (
        "2509.15550",
        re.compile(r"^Revise-Detect", re.I),
        re.compile(r"Table 5", re.I),
        ("2509.15550:revise-detect",),
    ),
    (
        "2606.04177",
        re.compile(r"SVM w/ Ling\. Feats", re.I),
        re.compile(r"Table (?:1|3|9)", re.I),
        ("2606.04177:linguistic-svm",),
    ),
    (
        "2606.18946",
        re.compile(r"^Full Model", re.I),
        re.compile(r"Table (?:4|5)", re.I),
        ("2606.18946:senflow",),
    ),
    (
        "2606.18946",
        re.compile(r"^w/o GCN", re.I),
        re.compile(r"Table 5", re.I),
        ("2606.18946:senflow-no-gcn",),
    ),
    (
        "2606.18946",
        re.compile(r"^w/o CRF", re.I),
        re.compile(r"Table 5", re.I),
        ("2606.18946:senflow-no-crf",),
    ),
    (
        "2606.18946",
        re.compile(r"^w/o CL", re.I),
        re.compile(r"Table 5", re.I),
        ("2606.18946:senflow-no-cl",),
    ),
    (
        "2606.18946",
        re.compile(r"^w/o TCN", re.I),
        re.compile(r"Table 5", re.I),
        ("2606.18946:senflow-no-tcn",),
    ),
    (
        "2604.04932",
        re.compile(r"^w/o CL", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.04932:race-no-cl",),
    ),
    (
        "2604.04932",
        re.compile(r"^w/o Relation", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.04932:race-no-relation",),
    ),
    (
        "2604.04932",
        re.compile(r"^w/o RGCN", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.04932:race-no-rgcn",),
    ),
    (
        "2604.04932",
        re.compile(r"^w/o Bottleneck", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.04932:race-no-bottleneck",),
    ),
    (
        "2604.04932",
        re.compile(r"^w/o Basis", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.04932:race-no-basis",),
    ),
    (
        "2505.15261",
        re.compile(r"^w/o Multi-Agent", re.I),
        re.compile(r"Table 3", re.I),
        ("2505.15261:without-multi-agent",),
    ),
    (
        "2505.15261",
        re.compile(r"^w/o Guidelines", re.I),
        re.compile(r"Table 3", re.I),
        ("2505.15261:without-guidelines",),
    ),
    (
        "2505.15261",
        re.compile(r"^w/o Adaptive Routing", re.I),
        re.compile(r"Table 3", re.I),
        ("2505.15261:without-adaptive-routing",),
    ),
    (
        "2505.15261",
        re.compile(r"^w/o Steer Calibration", re.I),
        re.compile(r"Table 3", re.I),
        ("2505.15261:without-steer-calibration",),
    ),
    (
        "2506.15683",
        re.compile(r"^w/o BFE", re.I),
        re.compile(r"Table 3", re.I),
        ("2506.15683:without-bfe",),
    ),
    (
        "2506.15683",
        re.compile(r"^w/o CL", re.I),
        re.compile(r"Table 3", re.I),
        ("2506.15683:without-cl",),
    ),
    (
        "2506.15683",
        re.compile(r"^w/o MoE", re.I),
        re.compile(r"Table 3", re.I),
        ("2506.15683:without-moe",),
    ),
    (
        "2501.08913",
        re.compile(r"R-Oai\s*&\s*BERT", re.I),
        re.compile(r"Table 4", re.I),
        ("2501.08913:lux-roai-bert",),
    ),
    (
        "2501.08913",
        re.compile(r"Radar\s*&\s*R-L", re.I),
        re.compile(r"Table (?:4|5)", re.I),
        ("2501.08913:lux-radar-r-l",),
    ),
    (
        "2501.08913",
        re.compile(r"Adv\.-New-Detector", re.I),
        re.compile(r"Table 4", re.I),
        ("2501.08913:cnlp-adv-new-detector",),
    ),
    (
        "2501.08913",
        re.compile(r"\bGLTR", re.I),
        re.compile(r"Table 5", re.I),
        ("2501.08913:gltr",),
    ),
    (
        "2505.05084",
        re.compile(r"^vanilla vanilla", re.I),
        re.compile(r"Table 3", re.I),
        ("2505.05084:binoculars-vanilla",),
    ),
    (
        "2603.18750",
        re.compile(r"MLP(?:\s*\(dtEN\))?$", re.I),
        re.compile(r"Table (?:3|5|6)", re.I),
        ("2603.18750:mlp-artmh",),
    ),
    (
        "2606.00016",
        re.compile(r"^text \(baseline\)", re.I),
        re.compile(r"Table 2", re.I),
        ("2606.00016:cnn-text",),
    ),
    (
        "2601.04641",
        re.compile(r"^DistillBert-F", re.I),
        re.compile(r"Table 2", re.I),
        ("2601.04641:distilbert-f",),
    ),
    (
        "2505.12507",
        re.compile(r"LM2\s*OTIFS-Bert", re.I),
        re.compile(r"Table 18", re.I),
        ("2505.12507:lm2-no-bert",),
    ),
    (
        "2502.16857",
        re.compile(r"Noised train/val Double Finetune", re.I),
        re.compile(r"Table 4", re.I),
        ("2502.16857:double-small",),
    ),
    (
        "2505.13855",
        re.compile(r"^Equal Vt\.", re.I),
        re.compile(r"Table 14", re.I),
        ("2505.13855:equal-vote",),
    ),
    (
        "2505.13855",
        re.compile(r"^Weight Vt\.", re.I),
        re.compile(r"Table 14", re.I),
        ("2505.13855:weighted-vote",),
    ),
)

LOCAL_RULES += (
    (
        "2608.01046",
        re.compile(r"^DeBERTa-Sentinel", re.I),
        re.compile(r"Table (?:3|4|5)", re.I),
        ("2608.01046:deberta-finetuned",),
    ),
    (
        "2608.01046",
        re.compile(r"^RoBERTa-Sentinel", re.I),
        re.compile(r"Table 5", re.I),
        ("2608.01046:roberta-finetuned",),
    ),
    (
        "2607.22026",
        re.compile(r"^HC3 Ensemble Calibration-weighted hard voting", re.I),
        re.compile(r"Table (?:4|5|6)", re.I),
        ("2607.22026:calibrated-hard",),
    ),
    (
        "2607.22026",
        re.compile(r"^HC3 Ensemble Equal-weight hard voting", re.I),
        re.compile(r"Table (?:4|5|6)", re.I),
        ("2607.22026:equal-hard",),
    ),
    (
        "2607.22026",
        re.compile(r"^HC3 Ensemble Calibration-weighted soft voting", re.I),
        re.compile(r"Table (?:4|5|6)", re.I),
        ("2607.22026:calibrated-soft",),
    ),
    (
        "2607.22026",
        re.compile(r"^HC3 Ensemble Equal-weight soft voting", re.I),
        re.compile(r"Table (?:4|5|6)", re.I),
        ("2607.22026:equal-soft",),
    ),
    (
        "2607.22026",
        re.compile(r"^HC3 Wavelet multilevel_energy", re.I),
        re.compile(r"Table (?:4|5|6)", re.I),
        ("2607.22026:multilevel-energy",),
    ),
    (
        "2607.22026",
        re.compile(r"^HC3 Wavelet energy_norm", re.I),
        re.compile(r"Table (?:4|5|6)", re.I),
        ("2607.22026:energy-norm",),
    ),
    (
        "2607.22026",
        re.compile(r"^(?:HC3|MAGE) Wavelet window_std", re.I),
        re.compile(r"Table (?:4|5|6)", re.I),
        ("2607.22026:window-std",),
    ),
    (
        "2607.14967",
        re.compile(r"(?:^|\s)DeTeCtive$", re.I),
        re.compile(r"Table 3", re.I),
        ("2607.14967:detective",),
    ),
    (
        "2606.31074",
        re.compile(r"^Fast-Detect \(Bao et al\.", re.I),
        re.compile(r"Table 3", re.I),
        ("2606.31074:fastdetectgpt",),
    ),
    (
        "2606.04177",
        re.compile(r"^TB[47] Longformer", re.I),
        re.compile(r"Table 3", re.I),
        ("2606.04177:mage-longformer",),
    ),
    (
        "2606.00016",
        re.compile(r"^RoBERTa$", re.I),
        re.compile(r"Table (?:2|3|4|5|6|7|8|9)", re.I),
        ("2606.00016:superannotate-roberta",),
    ),
    (
        "2606.00016",
        re.compile(r"^AEyeDE\(CNN\)$", re.I),
        re.compile(r"Table 1", re.I),
        ("2606.00016:cnn",),
    ),
    (
        "2505.14271",
        re.compile(r"^UnSup-SimCSE-XLM-RoBERTa-base", re.I),
        re.compile(r"Table 12", re.I),
        ("2505.14271:faid-unsup-simcse-xlmr",),
    ),
    (
        "2604.21223",
        re.compile(r"^RM-Deberta-v3-large-v2", re.I),
        re.compile(r"Table 8", re.I),
        ("2604.21223:reward-model-deberta",),
    ),
    (
        "2511.21744",
        re.compile(r"^AI-generated Text Detection", re.I),
        re.compile(r"Table 3", re.I),
        ("2511.21744:ai-generated-text-detection",),
    ),
    (
        "2511.21744",
        re.compile(r"^DeTeCtive", re.I),
        re.compile(r"Table 3", re.I),
        ("2511.21744:detective-comparator",),
    ),
    (
        "2511.21744",
        re.compile(r"^Restricted Embeddings", re.I),
        re.compile(r"Table 3", re.I),
        ("2511.21744:restricted-embeddings",),
    ),
    (
        "2511.21744",
        re.compile(r"^ChatGPT Detector", re.I),
        re.compile(r"Table 3", re.I),
        ("2511.21744:chatgpt-detector",),
    ),
    (
        "2511.21744",
        re.compile(r"^RoBERTa \+ BiLSTM", re.I),
        re.compile(r"Table 3", re.I),
        ("2511.21744:roberta-bilstm",),
    ),
    (
        "2509.18880",
        re.compile(r"^(?:\S+\s+)?e5-small-lora", re.I),
        re.compile(r"Table (?:2|13)", re.I),
        ("2509.18880:e5-small-lora",),
    ),
    (
        "2509.18880",
        re.compile(r"^(?:\S+\s+)?Desklib AI", re.I),
        re.compile(r"Table (?:2|13)", re.I),
        ("2509.18880:desklib",),
    ),
    (
        "2509.18880",
        re.compile(r"^SuperAnnotate", re.I),
        re.compile(r"Table 2", re.I),
        ("2509.18880:superannotate",),
    ),
    (
        "2509.18880",
        re.compile(r"^DivEye \(Ours\)", re.I),
        re.compile(r"Table (?:2|13)", re.I),
        ("2509.18880:gpt2",),
    ),
    (
        "2506.15683",
        re.compile(r"^RoBERTa$", re.I),
        re.compile(r"Table 3", re.I),
        ("2506.15683:roberta-baseline",),
    ),
    (
        "2506.15683",
        re.compile(r"^T5-Sentinel$", re.I),
        re.compile(r"Table 3", re.I),
        ("2506.15683:t5-sentinel-baseline",),
    ),
    (
        "2506.15683",
        re.compile(r"^DeTeCtive$", re.I),
        re.compile(r"Table 3", re.I),
        ("2506.15683:detective-baseline",),
    ),
    (
        "2506.15683",
        re.compile(r"^SeqXGPT$", re.I),
        re.compile(r"Table 3", re.I),
        ("2506.15683:seqxgpt-baseline",),
    ),
    (
        "2506.15683",
        re.compile(r"^DNA-GPT$", re.I),
        re.compile(r"Table 3", re.I),
        ("2506.15683:dna-gpt-baseline",),
    ),
    (
        "2506.15683",
        re.compile(r"^DetectGPT$", re.I),
        re.compile(r"Table 3", re.I),
        ("2506.15683:detectgpt-baseline",),
    ),
    (
        "2506.15683",
        re.compile(r"^Fast-DetectGPT$", re.I),
        re.compile(r"Table 3", re.I),
        ("2506.15683:fastdetectgpt-baseline",),
    ),
    (
        "2506.15683",
        re.compile(r"^PhantomHunter$", re.I),
        re.compile(r"Table (?:3|5)", re.I),
        ("2506.15683:full",),
    ),
    (
        "2506.15683",
        re.compile(r"^HasteWire$", re.I),
        re.compile(r"Table 5", re.I),
        ("2506.15683:hastewire",),
    ),
    (
        "2506.06705",
        re.compile(r"^w/o Adaption", re.I),
        re.compile(r"Table (?:3|4)", re.I),
        ("2506.06705:without-adaptation",),
    ),
    (
        "2506.06705",
        re.compile(r"^DivScore \(Mistral\)", re.I),
        re.compile(r"Table 4", re.I),
        ("2506.06705:divscore-mistral",),
    ),
    (
        "2506.06705",
        re.compile(r"^DivScore \(Falcon\)", re.I),
        re.compile(r"Table 4", re.I),
        ("2506.06705:divscore-falcon",),
    ),
    (
        "2506.06705",
        re.compile(r"^DivScore \(Qwen\)", re.I),
        re.compile(r"Table 4", re.I),
        ("2506.06705:divscore-qwen",),
    ),
    (
        "2506.06705",
        re.compile(r"^DivScore \(Llama\)", re.I),
        re.compile(r"Table 4", re.I),
        ("2506.06705:divscore-llama",),
    ),
    (
        "2506.06705",
        re.compile(r"^Entropy \(Mistral\)", re.I),
        re.compile(r"Table 4", re.I),
        ("2506.06705:entropy-mistral",),
    ),
    (
        "2506.06705",
        re.compile(r"^Entropy \(Falcon\)", re.I),
        re.compile(r"Table 4", re.I),
        ("2506.06705:entropy-falcon",),
    ),
    (
        "2506.06705",
        re.compile(r"^Entropy \(Qwen\)", re.I),
        re.compile(r"Table 4", re.I),
        ("2506.06705:entropy-qwen",),
    ),
    (
        "2506.06705",
        re.compile(r"^Entropy \(Llama\)", re.I),
        re.compile(r"Table 4", re.I),
        ("2506.06705:entropy-llama",),
    ),
    (
        "2506.06705",
        re.compile(r"^Cross-Entropy \(Qwen\)", re.I),
        re.compile(r"Table 4", re.I),
        ("2506.06705:cross-entropy-qwen",),
    ),
    (
        "2505.13855",
        re.compile(r"^baseline \(", re.I),
        re.compile(r"Table 2", re.I),
        ("2505.13855:qwen32b",),
    ),
    (
        "2503.00032",
        re.compile(r"^Essay POS Combinations Random Forest", re.I),
        re.compile(r"Table 9", re.I),
        ("2503.00032:pos-rf",),
    ),
    (
        "2503.00032",
        re.compile(r"^Punctuation Random Forest", re.I),
        re.compile(r"Table 9", re.I),
        ("2503.00032:punctuation-rf",),
    ),
    (
        "2502.16857",
        re.compile(r"^Ensemble \(deberta-v3-small \+ Double Finetune\)", re.I),
        re.compile(r"Table 4", re.I),
        ("2502.16857:ensemble-small",),
    ),
    (
        "2603.05617",
        re.compile(r"^N OTAI\.AI Ensemble", re.I),
        re.compile(r"Table 1", re.I),
        ("2603.05617:ensemble",),
    ),
    (
        "2601.20006",
        re.compile(r"^Per LLM Family Ensemble", re.I),
        re.compile(r"Table 15", re.I),
        ("2601.20006:ensemble-per-family",),
    ),
    (
        "2509.25154",
        re.compile(r"^XGB$", re.I),
        re.compile(r"Table 1", re.I),
        ("2509.25154:jdetector-xgb",),
    ),
    (
        "2509.00731",
        re.compile(r"^BERT Train$", re.I),
        re.compile(r"Table 1", re.I),
        ("2509.00731:bert",),
    ),
    (
        "2603.23146",
        re.compile(r"^Random Forest$", re.I),
        re.compile(r"Table (?:5|6|8)", re.I),
        ("2603.23146:optimized-random-forest",),
    ),
    (
        "2603.23146",
        re.compile(r"^SVM$", re.I),
        re.compile(r"Table (?:5|6)", re.I),
        ("2603.23146:optimized-svc",),
    ),
    (
        "2603.23146",
        re.compile(r"^XGBoost$", re.I),
        re.compile(r"Table (?:5|6|8)", re.I),
        ("2603.23146:optimized-xgboost",),
    ),
    (
        "2508.18715",
        re.compile(r"^MLP$", re.I),
        re.compile(r"Table 1", re.I),
        ("2508.18715:mlp",),
    ),
    (
        "2509.26051",
        re.compile(r"^F mDeBERTa-v3-base \(de-pl-hr-cs\)", re.I),
        re.compile(r"Table 3", re.I),
        ("2509.26051:mdeberta-v3-base",),
    ),
    (
        "2509.26051",
        re.compile(r"^F Llama$", re.I),
        re.compile(r"Table 3", re.I),
        ("2509.26051:llama-3.2-3b",),
    ),
    (
        "2509.26051",
        re.compile(r"^F Gemma$", re.I),
        re.compile(r"Table 3", re.I),
        ("2509.26051:gemma-2-2b",),
    ),
    (
        "2509.26051",
        re.compile(r"^F XLM-RoBERTa-base \(de-pl-hr-hu-cs\)", re.I),
        re.compile(r"Table (?:3|4)", re.I),
        ("2509.26051:xlm-roberta-base",),
    ),
    (
        "2509.26051",
        re.compile(r"^F mDeBERTa-v3-base \(de-pl-hr-hu-cs\)", re.I),
        re.compile(r"Table 4", re.I),
        ("2509.26051:mdeberta-generator-de-pl-hr-hu-cs",),
    ),
    (
        "2509.26051",
        re.compile(r"Llama-3\.2-3B \(hr-hu-cs\)", re.I),
        re.compile(r"Table 5", re.I),
        ("2509.26051:llama-news-hr-hu-cs",),
    ),
    (
        "2509.26051",
        re.compile(r"Llama-3\.2-3B \(de-pl-hu\)", re.I),
        re.compile(r"Table 5", re.I),
        ("2509.26051:llama-3.2-3b",),
    ),
    (
        "2509.26051",
        re.compile(r"Llama-3\.2-3B paraphrased", re.I),
        re.compile(r"Table (?:5|6|12)", re.I),
        ("2509.26051:llama-3.2-3b",),
    ),
    (
        "2509.26051",
        re.compile(r"^mDeBERTa-v3-base \(de\)$", re.I),
        re.compile(r"Table 5", re.I),
        ("2509.26051:mdeberta-social-de",),
    ),
    (
        "2509.26051",
        re.compile(r"Gemma-2-2B \(de-pl-hr-hu-cs\)", re.I),
        re.compile(r"Table 5", re.I),
        ("2509.26051:gemma-social-de-pl-hr-hu-cs",),
    ),
    (
        "2509.26051",
        re.compile(r"Gemma-2-2B \(de-pl-cs\)", re.I),
        re.compile(r"Table 5", re.I),
        ("2509.26051:gemma-2-2b",),
    ),
    (
        "2509.26051",
        re.compile(r"Gemma-2-2B paraphrased", re.I),
        re.compile(r"Table (?:5|6|12)", re.I),
        ("2509.26051:gemma-2-2b",),
    ),
    (
        "2509.26051",
        re.compile(r"^XLM-RoBERTa-base \(de-pl\)$", re.I),
        re.compile(r"Table 5", re.I),
        ("2509.26051:xlm-social-de-pl",),
    ),
    (
        "2509.26051",
        re.compile(r"^F Llama$", re.I),
        re.compile(r"Table 11", re.I),
        ("2509.26051:llama-tpr-pl",),
    ),
    (
        "2509.26051",
        re.compile(r"^F Gemma$", re.I),
        re.compile(r"Table 11", re.I),
        ("2509.26051:gemma-tpr-de-pl-hr-hu",),
    ),
    (
        "2509.26051",
        re.compile(r"^F mDeBERTa-v3-base \(de-pl-hr-hu\)", re.I),
        re.compile(r"Table 11", re.I),
        ("2509.26051:mdeberta-tpr-de-pl-hr-hu",),
    ),
    (
        "2509.26051",
        re.compile(r"^F XLM-RoBERTa-base \(de-cs\)", re.I),
        re.compile(r"Table 11", re.I),
        ("2509.26051:xlm-tpr-de-cs",),
    ),
    (
        "2509.26051",
        re.compile(r"^S Fast-DetectGPT", re.I),
        re.compile(r"Table 4", re.I),
        ("2509.26051:fastdetectgpt",),
    ),
    (
        "2509.26051",
        re.compile(r"^S Binoculars", re.I),
        re.compile(r"Table 4", re.I),
        ("2509.26051:binoculars",),
    ),
    (
        "2604.16607",
        re.compile(r"BiScope[- ]Arxiv", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.16607:biscope-arxiv",),
    ),
    (
        "2604.16607",
        re.compile(r"DeTeCtive \(M4GT\)", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.16607:detective-m4gt",),
    ),
    (
        "2604.16607",
        re.compile(r"DeTeCtive \(OUTFOX\)", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.16607:detective-outfox",),
    ),
    (
        "2604.16607",
        re.compile(r"DeTeCtive \(TuringBench\)", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.16607:detective-turingbench",),
    ),
    (
        "2604.16607",
        re.compile(r"Zippy \(Ensemble\)", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.16607:zippy-ensemble",),
    ),
    (
        "2604.16607",
        re.compile(r"RoBERTa \(H3C\+\)", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.16607:roberta-h3c-plus",),
    ),
    (
        "2604.16607",
        re.compile(r"RoBERTa \(M4GT\)", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.16607:roberta-m4gt",),
    ),
    (
        "2604.16607",
        re.compile(r"stylo \(H3C\+\)", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.16607:stylo-h3c-plus",),
    ),
    (
        "2604.16607",
        re.compile(r"mcgovern \(H3C\+\)", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.16607:mcgovern-h3c-plus",),
    ),
    (
        "2604.16607",
        re.compile(r"mcgovern \(M4GT\)", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.16607:mcgovern-m4gt",),
    ),
    (
        "2604.16607",
        re.compile(r"mcgovern \(MAGE\)", re.I),
        re.compile(r"Table 3", re.I),
        ("2604.16607:mcgovern-mage",),
    ),
    (
        "2510.12476",
        re.compile(r"^Lastde$", re.I),
        re.compile(r"Table (?:2|10|11)", re.I),
        ("2510.12476:lastde",),
    ),
    (
        "2510.12476",
        re.compile(r"^Lastde\+\+$", re.I),
        re.compile(r"Table (?:2|10|11)", re.I),
        ("2510.12476:lastde-plus-plus",),
    ),
    (
        "2501.03940",
        re.compile(r"RADAR-FT$", re.I),
        re.compile(r"Table (?:4|5)", re.I),
        ("2501.03940:radar-ft",),
    ),
    (
        "2501.03940",
        re.compile(r"PAWN \(GPT2\) PAWN \(LLaMA3-1b\) RoBERTa", re.I),
        re.compile(r"Table 9", re.I),
        ("2501.03940:m4-roberta-base",),
    ),
    (
        "2502.16857",
        re.compile(r"^deberta-v3-xsmall$", re.I),
        re.compile(r"Table 1", re.I),
        ("2502.16857:original-xsmall",),
    ),
    (
        "2502.16857",
        re.compile(r"^Original train/val deberta-v3-small$", re.I),
        re.compile(r"Table 1", re.I),
        ("2502.16857:original-small",),
    ),
    (
        "2502.16857",
        re.compile(r"^deberta-v3-base$", re.I),
        re.compile(r"Table 1", re.I),
        ("2502.16857:original-base",),
    ),
    (
        "2502.16857",
        re.compile(r"^deberta-v3-xsmall$", re.I),
        re.compile(r"Table 3", re.I),
        ("2502.16857:noised-xsmall",),
    ),
    (
        "2502.16857",
        re.compile(r"^deberta-v3-small$", re.I),
        re.compile(r"Table 3", re.I),
        ("2502.16857:noised-small",),
    ),
    (
        "2502.16857",
        re.compile(r"^deberta-v3-base$", re.I),
        re.compile(r"Table 3", re.I),
        ("2502.16857:noised-base",),
    ),
    (
        "2501.08913",
        re.compile(r"\[Cn\] (?:CNLP )?DistilBERT-NITS$", re.I),
        re.compile(r"Table (?:4|9)", re.I),
        ("2501.08913:cnlp-nits-distilbert",),
    ),
    (
        "2501.08913",
        re.compile(r"\[Us\] Roberta_dataaug\.$", re.I),
        re.compile(r"Table 4", re.I),
        ("2501.08913:ustc-roberta-dataaug",),
    ),
    (
        "2501.08913",
        re.compile(r"\[Ba\] Binoculars$", re.I),
        re.compile(r"Table 5", re.I),
        ("2501.08913:binoculars",),
    ),
    (
        "2501.08913",
        re.compile(r"\[Ba\] openai-roberta-L$", re.I),
        re.compile(r"Table 5", re.I),
        ("2501.08913:openai-roberta-large",),
    ),
    (
        "2504.11369",
        re.compile(r"Fast-DetectGPT \(Bao et al\.$|FastDetect$", re.I),
        re.compile(r"Table (?:1|9|10)", re.I),
        ("2504.11369:fastdetectgpt",),
    ),
    (
        "2504.11369",
        re.compile(r"LRR$", re.I),
        re.compile(r"Table (?:9|10)", re.I),
        ("2504.11369:lrr",),
    ),
    (
        "2504.11369",
        re.compile(r"GPT-D$", re.I),
        re.compile(r"Table (?:2|3)", re.I),
        ("2504.11369:chatgpt-detector",),
    ),
    (
        "2505.12507",
        re.compile(r"RADAR$", re.I),
        re.compile(r"Table 1", re.I),
        ("2505.12507:radar",),
    ),
    (
        "2505.12507",
        re.compile(r"Entropy$", re.I),
        re.compile(r"Table 1", re.I),
        ("2505.12507:entropy",),
    ),
    (
        "2604.11796",
        re.compile(r"Entropy$", re.I),
        re.compile(r"Table 2", re.I),
        ("2604.11796:entropy",),
    ),
    (
        "2604.11796",
        re.compile(r"Log-Rank$", re.I),
        re.compile(r"Table 2", re.I),
        ("2604.11796:log-rank",),
    ),
    (
        "2604.11796",
        re.compile(r"ReMoDetect$", re.I),
        re.compile(r"Table 2", re.I),
        ("2604.11796:remodetect",),
    ),
    (
        "2603.18750",
        re.compile(r"MobileNet CNN$|\bCNN$", re.I),
        re.compile(r"Table (?:3|4)", re.I),
        ("2603.18750:mobilenet-cnn",),
    ),
    (
        "2603.18750",
        re.compile(r"ZeroGPT$", re.I),
        re.compile(r"Table 3", re.I),
        ("2603.18750:zerogpt-artmh",),
    ),
    (
        "2603.18750",
        re.compile(r"Sapling$", re.I),
        re.compile(r"Table 6", re.I),
        ("2603.18750:sapling-artmh",),
    ),
    (
        "2603.18750",
        re.compile(r"GPTZero$", re.I),
        re.compile(r"Table 6", re.I),
        ("2603.18750:gptzero-artmh",),
    ),
    (
        "2510.12476",
        re.compile(r"Lastde drops from$", re.I),
        re.compile(r"Table 2", re.I),
        ("2510.12476:lastde",),
    ),
)

LOCAL_FALSE_RULES: tuple[
    tuple[str, re.Pattern[str], re.Pattern[str], str, str], ...
] = (
    (
        "2511.17402",
        re.compile(r".*", re.S),
        re.compile(r"Table (?:2|3|4)", re.I),
        "non_detector_row",
        "This row belongs to the toolkit's readability/complexity auxiliary task, not its machine-text detector evaluation.",
    ),
    (
        "2509.22147",
        re.compile(r".*", re.S),
        re.compile(r"Table (?:5|6|9)", re.I),
        "diagnostic_or_component",
        "This row belongs to the paper's segmentation, source-attribution, or expert-count auxiliary task, not the binary human-versus-machine deployment account.",
    ),
    (
        "2606.04177",
        re.compile(r"^CNN$", re.I),
        re.compile(r"Table 10", re.I),
        "non_detector_row",
        "`CNN` is the CNN/DailyMail text-domain label in this table, not a convolutional detector.",
    ),
    (
        "2606.04177",
        re.compile(r"^Baseline", re.I),
        re.compile(r"Table 15", re.I),
        "diagnostic_or_component",
        "This plotted baseline value is a feature-ablation reference line, not a separately named fitted detector.",
    ),
    (
        "2606.07313",
        re.compile(r"^\s*(?:DetectRL|Baseline)", re.I),
        re.compile(r"Table (?:3|6)", re.I),
        "non_detector_row",
        "This is a DetectRL attack/slice or leaderboard-heading row, not a separately named detector.",
    ),
    (
        "2607.17382",
        re.compile(r"^DetectRL", re.I),
        re.compile(r"Table (?:4|5|8|9|10)", re.I),
        "non_detector_row",
        "DetectRL is the evaluated benchmark row, not a DACTYL detector state.",
    ),
    (
        "2505.05084",
        re.compile(
            r"^(?:Detector Algorithm|w/o q̂M|detectors and supervised detectors)", re.I
        ),
        re.compile(r"Table (?:2|3|8|9)", re.I),
        "diagnostic_or_component",
        "This is a table heading, prose fragment, or component-only MCP ablation rather than a separately deployable detector state.",
    ),
    (
        "2605.06903",
        re.compile(r"^(?:Detector AUROC|MELD w/o)", re.I),
        re.compile(r"Table (?:1|5)", re.I),
        "diagnostic_or_component",
        "This is a leaderboard heading or loss-component ablation, not a separately released MELD detector state.",
    ),
    (
        "2511.01192",
        re.compile(r"^(?:w/o|DMoE)", re.I),
        re.compile(r"Table 2", re.I),
        "diagnostic_or_component",
        "This is a routing/component ablation within DEER, not a separately deployable detector account.",
    ),
    (
        "2506.01702",
        re.compile(r"^Detector ROC-AUC", re.I),
        re.compile(r"Table (?:1|2)", re.I),
        "table_heading_or_prose",
        "This is the metric header of the mdok comparison table, not a detector row.",
    ),
    (
        "2505.24523",
        re.compile(r"^DetectAIve", re.I),
        re.compile(r"Table 2", re.I),
        "nonqualifying_metric_context",
        "DetectAIve's own row remains below 0.90; the adjacent 0.93 in the two-column extraction belongs to prose describing RADAR.",
    ),
    (
        "2603.18750",
        re.compile(r"^CNN", re.I),
        re.compile(r"Table (?:4|5)", re.I),
        "nonqualifying_metric_context",
        "This is a one-class cross-domain diagnostic, not a new fitted state beyond the already disposed CNN1D account.",
    ),
    (
        "2602.01240",
        re.compile(r"^Full w/o", re.I),
        re.compile(r"Table 3", re.I),
        "diagnostic_or_component",
        "This is a component-removal ablation of DetectRouter, not a separately deployable scoring detector.",
    ),
    (
        "2502.15654",
        re.compile(r"^SmolLM2 baseline", re.I),
        re.compile(r"Table S2", re.I),
        "non_detector_row",
        "SmolLM2 is the evaluated generator in a data-quality experiment, not an AI-text detector.",
    ),
)

LOCAL_RULES += (
    (
        "2603.18750",
        re.compile(r"Rephrase$", re.I),
        re.compile(r"Table 3", re.I),
        ("2603.18750:rephrase",),
    ),
)

LOCAL_FALSE_RULES += (
    (
        "2607.03680",
        re.compile(r"^fine-tuned RoBERTa detector, we implement", re.I),
        re.compile(r"Table 6", re.I),
        "table_heading_or_prose",
        "This is implementation prose adjacent to the transfer table, not another fitted RoBERTa result row beyond the explicitly inventoried training states.",
    ),
    (
        "2501.09813",
        re.compile(r"^cross entropy function in order to make the model F1$", re.I),
        re.compile(r"Table (?:2|3)", re.I),
        "table_heading_or_prose",
        "This is training-description prose fused with a nearly one-hundred-percent dataset result in the adjacent PDF column, not a Cross-Entropy detector row.",
    ),
    (
        "2606.07313",
        re.compile(r"^SV-Detect Fast-DetectGPT RoBERTa-Base$", re.I),
        re.compile(r"Table 9", re.I),
        "table_heading_or_prose",
        "This is the three-detector column header above generator rows, not an additional fitted SV-Detect, Fast-DetectGPT, or RoBERTa state.",
    ),
    (
        "2605.06903",
        re.compile(r"^vs\. Binoculars$", re.I),
        re.compile(r"Table 8", re.I),
        "diagnostic_or_component",
        "This is the comparator heading for MELD-minus-Binoculars confidence intervals, not another fitted Binoculars or MELD detector state.",
    ),
    (
        "2601.20006",
        re.compile(
            r"^in the ensembles evaluated in the subsequent experiments\.$", re.I
        ),
        re.compile(r"Table 10", re.I),
        "table_heading_or_prose",
        "This is prose introducing the already inventoried fine-tuned family models, not a separately named ensemble or fitted state.",
    ),
    (
        "2510.12476",
        re.compile(
            r"^Detector Generator arXiv PeerRead Reddit WikiHow Wikipedia Avg\.$", re.I
        ),
        re.compile(r"Table 14", re.I),
        "table_heading_or_prose",
        "This is the Table 14 column header; the following grouped RoBERTa and DeTeCtive method identities are discovered and bound separately.",
    ),
    (
        "2509.18880",
        re.compile(
            r"^Backbone Model DivEye Binoculars BiScope LogRank DetectLLM FastDetectGPT$",
            re.I,
        ),
        re.compile(r"Table 6", re.I),
        "table_heading_or_prose",
        "This is the backbone-by-detector column header, not a new compound detector or separately fitted result state.",
    ),
    (
        "2501.08913",
        re.compile(r"^iterations are reached", re.I),
        re.compile(r"Table 3", re.I),
        "table_heading_or_prose",
        "This is threshold-calibration prose split across the two PDF columns, not a detector-result row.",
    ),
    (
        "2501.11012",
        re.compile(
            r"^(?:tems by comparing|and training-aligned|important, MGT detection|complexities to prevent)",
            re.I,
        ),
        re.compile(r"Table (?:8|9|11)", re.I),
        "table_heading_or_prose",
        "This is shared-task discussion or bibliography prose captured beside a percentage, not an individually named submitted system row.",
    ),
    (
        "2501.11914",
        re.compile(r"^For the English-only task", re.I),
        re.compile(r"Table (?:4|5)", re.I),
        "table_heading_or_prose",
        "This sentence narrates the already inventoried English and multilingual ensemble results; it is not another fitted state.",
    ),
    (
        "2502.11336",
        re.compile(r"^For each detector", re.I),
        re.compile(r"Table 1", re.I),
        "table_heading_or_prose",
        "This is experiment-protocol prose adjacent to a sample count, not a detector row or threshold result.",
    ),
    (
        "2502.12611",
        re.compile(r"^(?:statistically significant|SVC, DecisionTreeClassifier)", re.I),
        re.compile(r"Table (?:4|32)", re.I),
        "table_heading_or_prose",
        "This is statistical-analysis or model-summary prose containing a confidence percentage, not a named AI-text detector result.",
    ),
    (
        "2502.15654",
        re.compile(r"^B Machine-generated text detection hyperparameter sweep", re.I),
        re.compile(r"Table 3", re.I),
        "diagnostic_or_component",
        "This is a learning-rate hyperparameter range, not an additional fitted detector or evaluation result.",
    ),
    (
        "2504.11369",
        re.compile(
            r"^(?:• Model-based detection methods|ing\. Nonetheless, OTBDetector)", re.I
        ),
        re.compile(r"Table (?:1|3)", re.I),
        "table_heading_or_prose",
        "This is method-list or result-discussion prose captured across columns; every named table detector is dispositioned separately.",
    ),
    (
        "2504.21019",
        re.compile(
            r"^(?:box AIGT detection|a detection accuracy of|age detection accuracy of)",
            re.I,
        ),
        re.compile(r"Table (?:1|3)", re.I),
        "table_heading_or_prose",
        "This is DP-Net baseline or robustness narrative whose reported values are already bound to the uniform and Gaussian accounts, not a third state.",
    ),
    (
        "2505.14271",
        re.compile(r"^texts with the same models", re.I),
        re.compile(r"Table 1", re.I),
        "table_heading_or_prose",
        "This is FAIDSet construction/evaluation prose beside Table 1, not a separately named detector configuration.",
    ),
    (
        "2505.24523",
        re.compile(r"^detection\. Pre-trained detectors", re.I),
        re.compile(r"Table 2", re.I),
        "table_heading_or_prose",
        "This is prose describing existing MAGE and RADAR rows; the percentage is not a new named detector state.",
    ),
    (
        "2508.06913",
        re.compile(r"^where SentiDetect leads", re.I),
        re.compile(r"Table (?:2|3)", re.I),
        "table_heading_or_prose",
        "This is a relative-gain sentence about the already inventoried SentiDetect states, not an additional configuration.",
    ),
    (
        "2508.18715",
        re.compile(
            r"^(?:feature attribution|Datasets Binoculars|the only benchmark|PLM for turn-level)",
            re.I,
        ),
        re.compile(r"Table (?:1|5|6)", re.I),
        "table_heading_or_prose",
        "This is dialogue-benchmark, threshold, or attribution-method prose fused across PDF columns, not another detector row.",
    ),
    (
        "2509.00623",
        re.compile(r"^provided a very strong baseline", re.I),
        re.compile(r"Table 1", re.I),
        "table_heading_or_prose",
        "This sentence discusses the already inventoried TF-IDF+SVM submission and does not define another fitted state.",
    ),
    (
        "2509.00731",
        re.compile(
            r"^(?:are trained jointly|clearly, it overfit|degradation under distribution shift)",
            re.I,
        ),
        re.compile(r"Table (?:1|2)", re.I),
        "table_heading_or_prose",
        "This is training or result-discussion prose; the named BERT, RoBERTa, and LoRA states have separate accounts.",
    ),
    (
        "2509.26051",
        re.compile(r"^lingual baselines\), Llama", re.I),
        re.compile(r"Table 1", re.I),
        "table_heading_or_prose",
        "This is baseline-selection prose beside the dataset-count table, not a fitted language-combination result row.",
    ),
    (
        "2510.00890",
        re.compile(r"^Roberta$", re.I),
        re.compile(r"Table (?:1|2)", re.I),
        "nonqualifying_metric_context",
        "The RoBERTa row itself reports only 55.46 F1 and 72.30 AUROC; the adjacent >=0.90 values belong to Sci-SpanDet ablations.",
    ),
    (
        "2510.00890",
        re.compile(
            r"^(?:tics, zero-shot|RoBERTa and GLTR|perform paragraph-level)", re.I
        ),
        re.compile(r"Table (?:1|3)", re.I),
        "table_heading_or_prose",
        "This is comparison discussion whose high number belongs to an already inventoried Sci-SpanDet state, not a new detector row.",
    ),
    (
        "2510.03502",
        re.compile(r"^BERT$", re.I),
        re.compile(r"Table 9", re.I),
        "non_detector_row",
        "BERT appears in the LLM specification/reference context, not as an evaluated ALHD detector result.",
    ),
    (
        "2510.12476",
        re.compile(r"^based detectors: RoBERTa", re.I),
        re.compile(r"Table (?:5|6)", re.I),
        "table_heading_or_prose",
        "This is setup prose for the already inventoried RoBERTa and DeTeCtive M4 fits, not a third training state.",
    ),
    (
        "2511.00988",
        re.compile(r"^detector$", re.I),
        re.compile(r"Table 3", re.I),
        "table_heading_or_prose",
        "This is a malformed running-time diagram label with no system identity; named detector timing rows are dispositioned elsewhere.",
    ),
    (
        "2511.01192",
        re.compile(r"^Metric-based detectors make predictions", re.I),
        re.compile(r"Table 5", re.I),
        "table_heading_or_prose",
        "This is detector-family methodology prose beside dataset-length statistics, not a fitted DEER routing state.",
    ),
    (
        "2512.09292",
        re.compile(r"^datasets\. We use BiScope", re.I),
        re.compile(r"Table (?:1|2)", re.I),
        "table_heading_or_prose",
        "This is benchmark setup prose naming an already dispositioned comparator, not a distinct fitted result.",
    ),
    (
        "2601.04833",
        re.compile(r"^free detection of GPT-generated text", re.I),
        re.compile(r"Table (?:5|6)", re.I),
        "table_heading_or_prose",
        "This is a split bibliography citation to DNA-GPT, not a TSD detector row or new result.",
    ),
    (
        "2602.01240",
        re.compile(r"^tion overlooks model idiosyncrasies", re.I),
        re.compile(r"Table 1", re.I),
        "table_heading_or_prose",
        "This is source-surrogate discussion containing an illustrative AUC bound, not a named routing criterion.",
    ),
    (
        "2602.15514",
        re.compile(r"^Detector Test Prec Recall F1 Acc", re.I),
        re.compile(r"Table 2", re.I),
        "table_heading_or_prose",
        "This is the detector-table header, not an additional DependencyAI or XLM-RoBERTa state.",
    ),
    (
        "2603.23146",
        re.compile(r"^Detection$", re.I),
        re.compile(r"Table 2", re.I),
        "table_heading_or_prose",
        "This is a benchmark-description column heading, not a machine-learning detector result.",
    ),
    (
        "2604.16923",
        re.compile(r"^DetectGPT♣$", re.I),
        re.compile(r"Table 10", re.I),
        "nonqualifying_metric_context",
        "This DetectGPT row is at most 1.00% TPR in the cited low-FPR table; adjacent larger values belong to other methods.",
    ),
    (
        "2605.02374",
        re.compile(r"^ial rewrites\. Disabling retrieval guidance", re.I),
        re.compile(r"Table 3", re.I),
        "table_heading_or_prose",
        "This is REACT ablation discussion captured across columns, not a separately reported fitted detector row.",
    ),
    (
        "2605.02374",
        re.compile(r"^DetectRL$", re.I),
        re.compile(r"Table (?:4|5)", re.I),
        "non_detector_row",
        "DetectRL is the dataset block label in Table 5; detector systems occupy the table columns and are not represented by this row label.",
    ),
    (
        "2605.14240",
        re.compile(r"^cation using ensemble llm approaches", re.I),
        re.compile(r"Table 1", re.I),
        "table_heading_or_prose",
        "This is a bibliography entry containing a journal volume number, not an evaluated detector row.",
    ),
    (
        "2605.15518",
        re.compile(
            r"^(?:Classifier remains above|based detectors a|statistical-based detectors)",
            re.I,
        ),
        re.compile(r"Table 2", re.I),
        "table_heading_or_prose",
        "This is DetectRL-X aggregate discussion, not a separately named classifier beyond the exact leaderboard accounts.",
    ),
    (
        "2605.25281",
        re.compile(r"^detectors\. Acta neurochirurgica", re.I),
        re.compile(r"Table (?:4|5)", re.I),
        "table_heading_or_prose",
        "This is a bibliography fragment beside the READER table, not an evaluated detector state.",
    ),
    (
        "2606.02158",
        re.compile(
            r"^(?:budget, Uncertainty\+\+|ter sensitivity of Uncertainty\+\+)", re.I
        ),
        re.compile(r"Table 2", re.I),
        "diagnostic_or_component",
        "This is hyperparameter-sensitivity prose for the already inventoried Uncertainty++ account, not another fitted state.",
    ),
    (
        "2606.04177",
        re.compile(
            r"^(?:TB6 \(Unseen text domains\)|achieves the highest average detectability)",
            re.I,
        ),
        re.compile(r"Table 7", re.I),
        "table_heading_or_prose",
        "This is held-out-domain narrative about the existing Longformer/SVM evaluations, not a new classifier row.",
    ),
    (
        "2606.23336",
        re.compile(r"^RoBERTa$", re.I),
        re.compile(r"Table (?:5|6)", re.I),
        "diagnostic_or_component",
        "This RoBERTa entry is a computational-complexity row; its 1-forward notation is not a >=0.90 detector metric.",
    ),
    (
        "2606.23336",
        re.compile(r"^comparison across different detectors", re.I),
        re.compile(r"Table (?:6|8)", re.I),
        "table_heading_or_prose",
        "This is a two-column caption fragment naming evaluated generators, not a detector result row.",
    ),
    (
        "2606.31074",
        re.compile(
            r"^(?:detectors outperform the baselines|Detect\), which is even slightly better)",
            re.I,
        ),
        re.compile(r"Table (?:5|7)", re.I),
        "table_heading_or_prose",
        "This is Triospect result discussion captured beside a high number, not another detector or fitted proxy state.",
    ),
    (
        "2607.03680",
        re.compile(
            r"^(?:bution shift|proves over the vanilla baseline|and FOMAML\+LoRA performs|Vanilla detector\. All vanilla detectors|Ensemble AUROC TPR @|Held-out domain Ensemble TPR)",
            re.I,
        ),
        re.compile(r"Table (?:5|7|13|14)", re.I),
        "table_heading_or_prose",
        "This is transfer/adaptation prose or an ensemble-table header; exact Vanilla, FOMAML, pooled, and ensemble states are separately bound.",
    ),
    (
        "2608.01046",
        re.compile(r"^models\. DeBERTa-v3-small achieves", re.I),
        re.compile(r"Table 2", re.I),
        "table_heading_or_prose",
        "This is narrative describing the already inventoried fine-tuned DeBERTa-Sentinel, not another model state.",
    ),
    (
        "2608.01046",
        re.compile(r"^models\. DeBERTa-v3-small achieves", re.I),
        re.compile(r"Figure 4", re.I),
        "table_heading_or_prose",
        "This is two-column narrative describing the already inventoried fine-tuned DeBERTa-Sentinel beside a figure value, not another fitted state.",
    ),
    (
        "2607.03680",
        re.compile(r"^bution shift\. \(pvanilla", re.I),
        re.compile(r"Figure 2", re.I),
        "table_heading_or_prose",
        "This is distribution-shift discussion of the already inventoried vanilla detector probability, not a distinct fitted detector state or result row.",
    ),
    (
        "2606.02158",
        re.compile(r"^budget, Uncertainty\+\+ nearly converges", re.I),
        re.compile(r"Figure 3", re.I),
        "diagnostic_or_component",
        "This is sample-budget sensitivity prose for the already inventoried Uncertainty++ account, not another fitted state.",
    ),
    (
        "2605.16107",
        re.compile(r"^• DNA-DetectLLM \(DetectLLM\) \[$", re.I),
        re.compile(r"Table II", re.I),
        "table_heading_or_prose",
        "This is a method-list citation whose bracketed reference number triggered percentage discovery; the DetectLLM-M and DetectLLM-Mult result states are bound separately.",
    ),
    (
        "2605.16107",
        re.compile(r"^token-level scores for metric-based baselines\. Here, GPT", re.I),
        re.compile(r"Table II", re.I),
        "table_heading_or_prose",
        "This is proxy-model setup prose beside the result table; its model name and percentages do not define another detector result state.",
    ),
    (
        "2512.21709",
        re.compile(r"^detailed comparison\. Joint Conference on Neural Networks", re.I),
        re.compile(r"Table VI", re.I),
        "table_heading_or_prose",
        "This is a bibliography fragment whose page range was fused with the adjacent comparison table, not an evaluated detector row.",
    ),
    (
        "2511.00988",
        re.compile(r"^detector$", re.I),
        re.compile(r"Figure 6", re.I),
        "table_heading_or_prose",
        "This is an anonymous repeated plot label in the performance diagram, not a named detector identity; all named enhanced states are bound separately.",
    ),
    (
        "2510.16573",
        re.compile(r"^v3-base DistilBERT$", re.I),
        re.compile(r"Table IV", re.I),
        "table_heading_or_prose",
        "This is a line-wrap merge between the mDeBERTa-v3-base and DistilBERT rows; each complete model row has its own direct account evidence.",
    ),
    (
        "2510.16549",
        re.compile(r"^state-of-the-art Binoculars \[$", re.I),
        re.compile(r"Table I", re.I),
        "nonqualifying_metric_context",
        "This is dataset-preparation prose naming Binoculars; the adjacent numbers are LoRA and sequence-length settings, not a Binoculars evaluation metric.",
    ),
    (
        "2510.16549",
        re.compile(
            r"^a reliable safeguard against undetected academic impropriety", re.I
        ),
        re.compile(r"Table I", re.I),
        "table_heading_or_prose",
        "This is narrative about the dataset curation safeguard, not a detector identity or a separately reported fitted result.",
    ),
    (
        "2510.00890",
        re.compile(
            r"^perform paragraph-level baselines, reaching F1\(AI\) up to", re.I
        ),
        re.compile(r"Fig\. 6", re.I),
        "table_heading_or_prose",
        "This is result discussion summarizing the already inventoried Sci-SpanDet span detector; it does not name another fitted state.",
    ),
    (
        "2510.02319",
        re.compile(r"^mine detection accuracy\. \[$", re.I),
        re.compile(r"Fig\. 1", re.I),
        "table_heading_or_prose",
        "This is related-work prose whose citation number was mistaken for a metric; it does not identify a detector result row.",
    ),
    (
        "2510.02319",
        re.compile(r"^robust detector architectures have been explored\. \[$", re.I),
        re.compile(r"Fig\. 1", re.I),
        "table_heading_or_prose",
        "This is related-work prose whose citation number was mistaken for a metric; the paper's fitted ModernBERT and PIFE states are bound separately.",
    ),
    (
        "2508.11933",
        re.compile(r"^Best Baseline \(RQ1\)$", re.I),
        re.compile(r"Table II", re.I),
        "diagnostic_or_component",
        "This is a plot annotation repeating the best Table I baseline value, not a separately named system or fitted state.",
    ),
    (
        "2505.05084",
        re.compile(r"^vanilla vanilla$", re.I),
        re.compile(r"Figure 5", re.I),
        "diagnostic_or_component",
        "These are duplicated plot-style legend tokens under the already named Fast-DetectGPT and Binoculars curves, not an additional detector state.",
    ),
    (
        "2502.11336",
        re.compile(r"^For each detector, we evaluate$", re.I),
        re.compile(r"Figure 3", re.I),
        "table_heading_or_prose",
        "This is experiment-protocol prose whose sample count triggered discovery, not a named detector row or threshold result.",
    ),
    (
        "2501.09813",
        re.compile(r"^cross entropy function in order to make the model F1$", re.I),
        re.compile(r"Figure 3", re.I),
        "table_heading_or_prose",
        "This is training-description prose fused across columns with a dataset result approaching 100%, not a Cross-Entropy detector result.",
    ),
)

for _learner, _slug in (
    ("LR", "lr"),
    ("RF", "rf"),
    ("XGB", "xgb"),
    ("LDA", "lda"),
    ("SVM", "svm"),
):
    LOCAL_RULES += (
        (
            "2509.22147",
            re.compile(rf"^{_learner}$", re.I),
            re.compile(r"Table 3", re.I),
            (f"2509.22147:word2vec-{_slug}", f"2509.22147:tfidf-{_slug}"),
        ),
    )
for _name, _slug in (
    ("CNN", "cnn"),
    ("RNN", "rnn"),
    ("LSTM", "lstm"),
    ("BiLSTM", "bilstm"),
    ("BiGRU", "bigru"),
    ("CNN-LSTM", "cnn-lstm"),
    ("CNN-BiLSTM", "cnn-bilstm"),
    ("CNN-BiGRU", "cnn-bigru"),
    ("BERT", "bert"),
    ("DistilBERT", "distilbert"),
    ("RoBERTa", "roberta"),
    ("DeBERTa", "deberta"),
    ("ModernBERT", "modernbert"),
):
    LOCAL_RULES += (
        (
            "2509.22147",
            re.compile(rf"^{re.escape(_name)}$", re.I),
            re.compile(r"Table 3", re.I),
            (f"2509.22147:binary-{_slug}",),
        ),
    )
for _name, _slug in (
    ("BERT", "bert"),
    ("DistilBERT", "distilbert"),
    ("RoBERTa", "roberta"),
    ("DeBERTa", "deberta"),
    ("ModernBERT", "modernbert"),
):
    LOCAL_RULES += (
        (
            "2509.22147",
            re.compile(rf"^{re.escape(_name)}$", re.I),
            re.compile(r"Table 4", re.I),
            (f"2509.22147:implicit-{_slug}",),
        ),
    )
LOCAL_RULES += (
    (
        "2509.22147",
        re.compile(r"^ModernBERT \(Best\)", re.I),
        re.compile(r"Table 7", re.I),
        ("2509.22147:binary-modernbert",),
    ),
    (
        "2509.22147",
        re.compile(r"^BERT \(Best\)", re.I),
        re.compile(r"Table 8", re.I),
        ("2509.22147:implicit-bert",),
    ),
    (
        "2503.15044",
        re.compile(r"RF", re.I),
        re.compile(r"Table 3", re.I),
        ("2503.15044:random-forest",),
    ),
)

LOCAL_RULES += (
    (
        "2605.16107",
        re.compile(r"^Likelihood$", re.I),
        re.compile(r"Table III", re.I),
        ("2605.16107:likelihood",),
    ),
    (
        "2605.16107",
        re.compile(r"^Log-?Rank$", re.I),
        re.compile(r"Table III", re.I),
        ("2605.16107:logrank",),
    ),
    (
        "2605.16107",
        re.compile(r"^Entropy$", re.I),
        re.compile(r"Table III", re.I),
        ("2605.16107:entropy",),
    ),
    (
        "2605.16107",
        re.compile(r"^DetectGPT$", re.I),
        re.compile(r"Table III", re.I),
        ("2605.16107:detectgpt",),
    ),
    (
        "2605.16107",
        re.compile(r"^FastGPT$", re.I),
        re.compile(r"Table III", re.I),
        ("2605.16107:fastgpt",),
    ),
    (
        "2605.16107",
        re.compile(r"^Binoculars$", re.I),
        re.compile(r"Table III", re.I),
        ("2605.16107:binoculars",),
    ),
    (
        "2605.16107",
        re.compile(r"^FourierGPT$", re.I),
        re.compile(r"Table III", re.I),
        ("2605.16107:fouriergpt",),
    ),
    (
        "2605.16107",
        re.compile(r"^AdaGPT$", re.I),
        re.compile(r"Table III", re.I),
        ("2605.16107:adagpt",),
    ),
    (
        "2604.02008",
        re.compile(r"^Likelihood(?:\s|\[|$)", re.I),
        re.compile(r"Table III", re.I),
        ("2604.02008:likelihood",),
    ),
    (
        "2604.02008",
        re.compile(r"^LogRank(?:\s|\[|$)", re.I),
        re.compile(r"Table III", re.I),
        ("2604.02008:logrank",),
    ),
    (
        "2604.02008",
        re.compile(r"^(?:♠\s*)?Fast-DetectGPT(?:\s|\[|$)", re.I),
        re.compile(r"Table III", re.I),
        ("2604.02008:fastdetectgpt",),
    ),
    (
        "2604.02008",
        re.compile(r"^(?:♢\s*)?Binoculars(?:\s|\[|$)", re.I),
        re.compile(r"Table III", re.I),
        ("2604.02008:binoculars",),
    ),
    (
        "2604.02008",
        re.compile(r"^♠\s*\+\s*DALD", re.I),
        re.compile(r"Table III", re.I),
        ("2604.02008:fastdetectgpt-dald",),
    ),
    (
        "2604.02008",
        re.compile(r"^♠\s*\+\s*Glimpse-Geometric.*GPT-4", re.I),
        re.compile(r"Table III", re.I),
        ("2604.02008:fastdetectgpt-glimpse-gpt4-geometric",),
    ),
    (
        "2604.02008",
        re.compile(r"^♠\s*\+\s*Glimpse-Zipfian.*GPT-4", re.I),
        re.compile(r"Table III", re.I),
        ("2604.02008:fastdetectgpt-glimpse-gpt4-zipfian",),
    ),
    (
        "2604.02008",
        re.compile(r"^♠\s*\+\s*Glimpse-MLP.*GPT-4", re.I),
        re.compile(r"Table III", re.I),
        ("2604.02008:fastdetectgpt-glimpse-gpt4-mlp",),
    ),
    (
        "2604.02008",
        re.compile(r"^♠\s*\+\s*Glimpse-Geometric.*DaVinci-002", re.I),
        re.compile(r"Table III", re.I),
        ("2604.02008:fastdetectgpt-glimpse-davinci-geometric",),
    ),
    (
        "2604.02008",
        re.compile(r"^♢\s*\+\s*DALD", re.I),
        re.compile(r"Table III", re.I),
        ("2604.02008:binoculars-dald",),
    ),
    (
        "2510.02319",
        re.compile(r"^FastDetectGPT$", re.I),
        re.compile(r"Table VIII", re.I),
        ("2510.02319:fastdetectgpt",),
    ),
    (
        "2510.02319",
        re.compile(r"^Glimpse$", re.I),
        re.compile(r"Table VIII", re.I),
        ("2510.02319:glimpse",),
    ),
    (
        "2510.02319",
        re.compile(r"^Binoculars$", re.I),
        re.compile(r"Table VIII", re.I),
        ("2510.02319:binoculars",),
    ),
    (
        "2510.02319",
        re.compile(r"^LogRank$", re.I),
        re.compile(r"Table VIII", re.I),
        ("2510.02319:logrank",),
    ),
    (
        "2508.11933",
        re.compile(r"^Raidar$", re.I),
        re.compile(r"Table I", re.I),
        ("2508.11933:raidar",),
    ),
    (
        "2508.11933",
        re.compile(r"^GPT4o$", re.I),
        re.compile(r"Table I", re.I),
        ("2508.11933:gpt4o-direct",),
    ),
    (
        "2508.11933",
        re.compile(r"^GPT\+CoT$", re.I),
        re.compile(r"Table I", re.I),
        ("2508.11933:gpt-cot",),
    ),
    (
        "2508.11933",
        re.compile(r"^GPT\+React$", re.I),
        re.compile(r"Table I", re.I),
        ("2508.11933:gpt-react",),
    ),
    (
        "2508.11933",
        re.compile(r"^GPT-4o-mini$", re.I),
        re.compile(r"Fig(?:ure)?\.? 4", re.I),
        ("2508.11933:gpt4o-mini",),
    ),
    (
        "2508.11933",
        re.compile(r"^Gemini-1\.5 Pro$", re.I),
        re.compile(r"Fig(?:ure)?\.? 4", re.I),
        ("2508.11933:gemini15-pro",),
    ),
    (
        "2508.11933",
        re.compile(r"^DeepSeek-V3$", re.I),
        re.compile(r"Fig(?:ure)?\.? 4", re.I),
        ("2508.11933:deepseek-v3",),
    ),
    (
        "2508.11933",
        re.compile(r"^GPT-3\.5-Turbo$", re.I),
        re.compile(r"Fig(?:ure)?\.? 4", re.I),
        ("2508.11933:gpt35",),
    ),
    (
        "2508.11933",
        re.compile(r"^GPT-4o$", re.I),
        re.compile(r"Fig(?:ure)?\.? 4", re.I),
        ("2508.11933:gpt4o",),
    ),
    (
        "2508.11933",
        re.compile(r"^Llama3-70B$", re.I),
        re.compile(r"Fig(?:ure)?\.? 4", re.I),
        ("2508.11933:llama3-70b",),
    ),
    (
        "2604.25860",
        re.compile(r"^Luminol-AIDetect$", re.I),
        re.compile(r"explicit full-text", re.I),
        ("2604.25860:luminol",),
    ),
    (
        "2604.25860",
        re.compile(r"^Binoculars$", re.I),
        re.compile(r"explicit full-text", re.I),
        ("2604.25860:binoculars",),
    ),
    (
        "2604.25860",
        re.compile(r"^Fast-?DetectGPT$", re.I),
        re.compile(r"explicit full-text", re.I),
        ("2604.25860:fastdetectgpt",),
    ),
    (
        "2604.02008",
        re.compile(r"^♡\s*\+\s*kNNProxy", re.I),
        re.compile(r"Table (?:IV|V)", re.I),
        ("2604.02008:likelihood-knnproxy",),
    ),
    (
        "2604.02008",
        re.compile(r"^♠\s*\+\s*kNNProxy", re.I),
        re.compile(r"Table (?:III|IV|V)", re.I),
        ("2604.02008:fastdetectgpt-knnproxy",),
    ),
    (
        "2604.02008",
        re.compile(r"^♢\s*\+\s*kNNProxy", re.I),
        re.compile(r"Table (?:III|IV|V)", re.I),
        ("2604.02008:binoculars-knnproxy",),
    ),
    (
        "2604.02008",
        re.compile(r"^♠\s*\+\s*MoP", re.I),
        re.compile(r"Table V", re.I),
        ("2604.02008:fastdetectgpt-mop",),
    ),
    (
        "2604.02008",
        re.compile(r"^♢\s*\+\s*MoP", re.I),
        re.compile(r"Table V", re.I),
        ("2604.02008:binoculars-mop",),
    ),
    (
        "2510.16573",
        re.compile(r"^microsoft/mdeberta", re.I),
        re.compile(r"Table IV", re.I),
        ("2510.16573:mdeberta-v3-base",),
    ),
    (
        "2510.16573",
        re.compile(r"^distilbert/distilbert", re.I),
        re.compile(r"Table IV", re.I),
        ("2510.16573:distilbert-multilingual",),
    ),
    (
        "2510.16573",
        re.compile(r"^FacebookAI/xlm", re.I),
        re.compile(r"Table IV", re.I),
        ("2510.16573:xlm-roberta-base",),
    ),
    (
        "2510.16549",
        re.compile(r"^BERT(?:\s+Recall)?$", re.I),
        re.compile(r"Table VI", re.I),
        ("2510.16549:bert-rs",),
    ),
    (
        "2510.16549",
        re.compile(r"^SciBERT(?:\s+Recall)?$", re.I),
        re.compile(r"Table VI", re.I),
        ("2510.16549:scibert-rs",),
    ),
    (
        "2510.16549",
        re.compile(r"^RoBERTa(?:\s+Recall)?$", re.I),
        re.compile(r"Table VI", re.I),
        ("2510.16549:roberta-rs",),
    ),
    (
        "2510.16549",
        re.compile(r"^LLaMa$", re.I),
        re.compile(r"Table VI", re.I),
        ("2510.16549:llama31-rs",),
    ),
    (
        "2510.16549",
        re.compile(r"^Qwen$", re.I),
        re.compile(r"Table VI", re.I),
        ("2510.16549:qwen3-rs",),
    ),
    (
        "2510.12608",
        re.compile(r"^TF-IDF$", re.I),
        re.compile(r"Table III", re.I),
        ("2510.12608:style-tfidf",),
    ),
    (
        "2510.12608",
        re.compile(r"^Word2Vec/GloVe$", re.I),
        re.compile(r"Table III", re.I),
        ("2510.12608:style-word2vec",),
    ),
    (
        "2510.12608",
        re.compile(r"^BERT$", re.I),
        re.compile(r"Table III", re.I),
        ("2510.12608:style-bert",),
    ),
    (
        "2510.12608",
        re.compile(r"^SBERT$", re.I),
        re.compile(r"Table III", re.I),
        ("2510.12608:style-sbert",),
    ),
    (
        "2510.02319",
        re.compile(r"^Adversarially Trained ModernBERT Detector$", re.I),
        re.compile(r"Table VI", re.I),
        ("2510.02319:adv-modernbert",),
    ),
    (
        "2510.02319",
        re.compile(r"^PIFE-Augmented with ModernBERT$", re.I),
        re.compile(r"Table VII", re.I),
        ("2510.02319:pife-modernbert",),
    ),
    (
        "2501.14288",
        re.compile(r"^DeBERTa-v3-large$", re.I),
        re.compile(r"Table I", re.I),
        ("2501.14288:deberta",),
    ),
    (
        "2501.14288",
        re.compile(r"^DeBERTa \+ LSTM$", re.I),
        re.compile(r"Table I", re.I),
        ("2501.14288:deberta-lstm",),
    ),
    (
        "2501.14288",
        re.compile(r"^\+ Linear Attention Pooling$", re.I),
        re.compile(r"Table I", re.I),
        ("2501.14288:deberta-lstm-attention",),
    ),
    (
        "2501.14288",
        re.compile(r"^\+ Target Shuffling$", re.I),
        re.compile(r"Table I", re.I),
        ("2501.14288:target-shuffling",),
    ),
    (
        "2501.14288",
        re.compile(r"^Ensemble Model$", re.I),
        re.compile(r"Table I", re.I),
        ("2501.14288:ensemble",),
    ),
    (
        "2512.21709",
        re.compile(r"^Base, IndicBERT-Base and MultilingualBERT-Base", re.I),
        re.compile(r"Fig\. 1", re.I),
        (
            "2512.21709:zeroshot-banglabert",
            "2512.21709:zeroshot-indicbert",
            "2512.21709:zeroshot-multilingualbert",
        ),
    ),
    (
        "2512.21709",
        re.compile(r"^B\. Fine-Tuned Classification MultilingualBERT-Base", re.I),
        re.compile(r"Table V", re.I),
        ("2512.21709:multilingual-bert",),
    ),
    (
        "2510.02319",
        re.compile(
            r"^to ModernBERT, and our novel PIFE-augmented model\. Char Insertion", re.I
        ),
        re.compile(r"Table VII", re.I),
        ("2510.02319:pife-modernbert",),
    ),
    (
        "2508.11933",
        re.compile(r"^CAMF \(Ours\)$", re.I),
        re.compile(r"Table I", re.I),
        ("2508.11933:gpt35",),
    ),
    (
        "2506.06705",
        re.compile(r"^w/o Adaption .*Entropy \(Qwen\)$", re.I),
        re.compile(r"Figure 4", re.I),
        ("2506.06705:without-adaptation", "2506.06705:entropy-qwen"),
    ),
    (
        "2506.06705",
        re.compile(r"^Entropy$", re.I),
        re.compile(r"Table (?:1|2)", re.I),
        ("2506.06705:entropy",),
    ),
    (
        "2503.22338",
        re.compile(r"^RAIDAR \[$", re.I),
        re.compile(r"Table 2", re.I),
        ("2503.22338:svc-raidar", "2503.22338:rf-raidar", "2503.22338:xgb-raidar"),
    ),
    (
        "2503.22338",
        re.compile(r"^RAIDAR \+ NELA$", re.I),
        re.compile(r"Table 2", re.I),
        (
            "2503.22338:svc-combined",
            "2503.22338:rf-combined",
            "2503.22338:xgb-combined",
        ),
    ),
    (
        "2503.22338",
        re.compile(r"^RAIDAR \[$", re.I),
        re.compile(r"Table 3", re.I),
        ("2503.22338:xgb-raidar",),
    ),
    (
        "2503.22338",
        re.compile(r"RAIDAR \+ NELA$", re.I),
        re.compile(r"Table 3", re.I),
        ("2503.22338:xgb-combined",),
    ),
    (
        "2501.14288",
        re.compile(r"This metric captures .* Ensemble Model$", re.I),
        re.compile(r"Table I", re.I),
        ("2501.14288:ensemble",),
    ),
    (
        "2602.11871",
        re.compile(r"^FAST-D\s*ETECT\s*GPT$", re.I),
        re.compile(r"Table 1", re.I),
        (
            "2602.11871:fdgpt-llama",
            "2602.11871:fdgpt-mistral",
            "2602.11871:fdgpt-qwen",
        ),
    ),
    (
        "2602.11871",
        re.compile(r"^B\s*INOCULARS$", re.I),
        re.compile(r"Table 1", re.I),
        (
            "2602.11871:binoculars-llama",
            "2602.11871:binoculars-mistral",
            "2602.11871:binoculars-qwen",
        ),
    ),
)

LOCAL_RULES += (
    (
        "2510.16549",
        re.compile(r"^Precision.*0\.9034", re.I),
        re.compile(r"TABLE VI", re.I),
        ("2510.16549:qwen3-rs",),
    ),
)

for _base_label, _base_slug in (
    ("Likelihood", "likelihood"),
    ("Log-Rank", "logrank"),
    ("Entropy", "entropy"),
    ("DetectGPT", "detectgpt"),
    ("FastGPT", "fastgpt"),
    ("Binoculars", "binoculars"),
    ("FourierGPT", "fouriergpt"),
    ("AdaGPT", "adagpt"),
    ("DetectLLM", "detectllm"),
):
    LOCAL_RULES += (
        (
            "2605.16107",
            re.compile(rf"^{re.escape(_base_label)}-M$", re.I),
            re.compile(r"Table (?:II|III)", re.I),
            (f"2605.16107:{_base_slug}-m",),
        ),
    )

LOCAL_RULES += (
    (
        "2605.15518",
        re.compile(r"^based detector, Biscope", re.I),
        re.compile(r"Table 2", re.I),
        ("2605.15518:biscope",),
    ),
    (
        "2505.12507",
        re.compile(r"^Experiments F-DetectGPT$", re.I),
        re.compile(r"Table 1", re.I),
        ("2505.12507:fastdetectgpt",),
    ),
    (
        "2601.04833",
        re.compile(r"^DD$", re.I),
        re.compile(r"Table (?:3|6)", re.I),
        ("2601.04833:dd",),
    ),
    (
        "2601.04833",
        re.compile(r"^LV$", re.I),
        re.compile(r"Table (?:3|6)", re.I),
        ("2601.04833:lv",),
    ),
    (
        "2601.04833",
        re.compile(r"^TSD$", re.I),
        re.compile(r"Table (?:3|6)", re.I),
        ("2601.04833:tsd",),
    ),
)

LOCAL_FALSE_RULES += (
    (
        "2606.07313",
        re.compile(r"^SV-Detect \(ours\)$", re.I),
        re.compile(r"Table 1", re.I),
        "diagnostic_or_component",
        "This is the family-level inference-cost row; the separately fitted SV-Detect backbone and training states have individual account bindings.",
    ),
    (
        "2605.15518",
        re.compile(r"^DetectRL(?:-X)?(?: \(Wu et al\.)?", re.I),
        re.compile(r"Table 1", re.I),
        "non_detector_row",
        "DetectRL-X is the benchmark/evaluation suite in this comparison, not a separately deployable detector state.",
    ),
    (
        "2604.21300",
        re.compile(r"^improvement over baselines across most domains", re.I),
        re.compile(r"Table 3", re.I),
        "table_heading_or_prose",
        "This is result-discussion prose fused across PDF columns, not a named authorship-attribution detector row.",
    ),
    (
        "2601.04833",
        re.compile(r"^(?:shot detection|Zero-Shot Detection Metrics)", re.I),
        re.compile(r"Table 1", re.I),
        "table_heading_or_prose",
        "This is section or method-family prose adjacent to the slope table, not a separately named fitted detector configuration.",
    ),
    (
        "2510.03502",
        re.compile(r"^aubmindlab/bert-base-arabertv2$", re.I),
        re.compile(r"Table 8", re.I),
        "diagnostic_or_component",
        "This is a pretrained-model identifier in the architecture-specification table, not a threshold result row; the fitted AraBERTv2 account is bound to its result table separately.",
    ),
    (
        "2509.21269",
        re.compile(r"^(?:DetectRL|Peer Review Detection|TriBERT)", re.I),
        re.compile(r"Table (?:1|2)", re.I),
        "non_detector_row",
        "This is a source-dataset or prior-work label in the corpus-statistics tables, not one of the paper's three fitted Mistral classifier states.",
    ),
    (
        "2509.00731",
        re.compile(r"^Experimental Setup almost perfectly", re.I),
        re.compile(r"Table 1", re.I),
        "table_heading_or_prose",
        "This is two-column experiment prose merged with a RoBERTa result, not an additional encoder or LoRA state.",
    ),
    (
        "2505.15422",
        re.compile(r"^(?:Barlas and Stamatatos|W\. Huang)", re.I),
        re.compile(r"Table (?:5|6)", re.I),
        "nonqualifying_metric_context",
        "This is a bibliographic summary row in an authorship-analysis survey; the adjacent numbers are publication/task metadata rather than a qualifying AI-text detector metric.",
    ),
)

LOCAL_CARRY_RULES: tuple[
    tuple[str, re.Pattern[str], re.Pattern[str], tuple[str, ...]], ...
] = (
    (
        "2607.22026",
        re.compile(r"lrr_score", re.I),
        re.compile(r"Table (?:4|5|6)", re.I),
        ("2505.12507:lrr",),
    ),
    (
        "2607.22026",
        re.compile(r"mean_rank", re.I),
        re.compile(r"Table (?:4|5|6)", re.I),
        ("2505.12507:rank",),
    ),
    (
        "2607.17382",
        re.compile(r"Baseline mdok", re.I),
        re.compile(r"Table 11", re.I),
        ("2506.01702:mdok-binary",),
    ),
    (
        "2607.22026",
        re.compile(r"^HC3 Baseline mean_logrank", re.I),
        re.compile(r"Table (?:4|5|6)", re.I),
        ("2505.12507:logrank",),
    ),
    (
        "2607.22026",
        re.compile(r"^HC3 Baseline mean_log_likelihood", re.I),
        re.compile(r"Table (?:4|5|6)", re.I),
        ("2505.12507:likelihood",),
    ),
    (
        "2607.22026",
        re.compile(r"^HC3 Baseline mean_entropy", re.I),
        re.compile(r"Table (?:4|5|6)", re.I),
        ("2505.12507:entropy",),
    ),
    (
        "2505.15261",
        re.compile(r"^Fast-Detect", re.I),
        re.compile(r"Table (?:1|2|4|5|6)", re.I),
        ("2505.12507:fastdetectgpt",),
    ),
    (
        "2509.18880",
        re.compile(r"FastDetectGPT$", re.I),
        re.compile(r"Table 1", re.I),
        ("2505.12507:fastdetectgpt",),
    ),
    (
        "2604.02008",
        re.compile(r"^Stream Query Proxy Glimpse \[$", re.I),
        re.compile(r"Table I", re.I),
        ("2505.12507:glimpse",),
    ),
    (
        "2509.22147",
        re.compile(r"^Glimpse \((?:davinci|babbage)\)$", re.I),
        re.compile(r"Table 7", re.I),
        ("2505.12507:glimpse",),
    ),
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
    (
        re.compile(r"^(?:Log[- ]?Likelihood|Likelihood)(?:\s|\[|\(|$)", re.I),
        "2505.12507:likelihood",
    ),
    (re.compile(r"^Log[- ]?Rank(?:\s|\[|\(|$)", re.I), "2505.12507:logrank"),
    (re.compile(r"^Entropy(?:\s|\[|\(|$)", re.I), "2505.12507:entropy"),
    (re.compile(r"^Rank(?:\s|\[|\(|$)", re.I), "2505.12507:rank"),
    (re.compile(r"^(?:Detect)?LRR(?:\s|\[|\(|$)", re.I), "2505.12507:lrr"),
    (re.compile(r"^(?:Detect)?NPR(?:\s|\[|\(|$)", re.I), "2505.12507:npr"),
    (re.compile(r"^DetectGPT(?:\s|\[|\(|\*|$)", re.I), "2509.15550:detectgpt"),
    (re.compile(r"^DNA[- ]?GPT(?:\s|\[|\(|$)", re.I), "2505.12507:dnagpt"),
    (
        re.compile(
            r"^(?:Fast[- ]?DetectGPT|F[- ]DetectGPT|FastDetect)(?:\s|\[|\(|$)", re.I
        ),
        "2505.12507:fastdetectgpt",
    ),
    (re.compile(r"^Binoculars(?:\s|\[|\(|\*|$)", re.I), "2505.12507:binoculars"),
    (re.compile(r"^RADAR(?:\s|\[|\(|\*|$)", re.I), "2505.12507:radar"),
    (re.compile(r"^GLTR(?:\s|\[|\(|\*|$)", re.I), "2501.08913:gltr"),
    (re.compile(r"^GPTZero(?:\s|\[|\(|\*|$)", re.I), "2505.12507:gptzero"),
    (re.compile(r"^Lastde\+\+(?:\s|\[|\(|$)", re.I), "2604.16923:lastde-plus"),
    (re.compile(r"^Lastde(?:\s|\[|\(|$)", re.I), "2601.04833:lastde"),
    (re.compile(r"^ReMoDetect(?:\s|\[|\(|$)", re.I), "2604.16923:remodetect"),
    (re.compile(r"^BiScope(?:\s|\[|\(|-|$)", re.I), "2603.24981:biscope"),
    (
        re.compile(r"^(?:LLM-)?DetectAIve(?:\s|\[|\(|$)", re.I),
        "2505.14271:llmdetectaive",
    ),
    (re.compile(r"^DeTeCtive(?:\s|\[|\(|$)", re.I), "2505.12507:detective"),
    (re.compile(r"^Longformer(?:\s|\[|\(|$)", re.I), "2607.14905:longformer"),
    (re.compile(r"^RoBERTa-Base(?:\s|\[|\(|$)", re.I), "2506.06705:roberta-base"),
    (re.compile(r"^RoBERTa-Large(?:\s|\[|\(|$)", re.I), "2506.06705:roberta-large"),
    (
        re.compile(r"^XLM-RoBERTa-Base(?:\s|\[|\(|$)", re.I),
        "2509.26051:xlm-roberta-base",
    ),
    (
        re.compile(r"^XLM-RoBERTa-Large(?:\s|\[|\(|$)", re.I),
        "2512.21709:xlm-roberta-large",
    ),
    (re.compile(r"^ModernBERT-Detect(?:\s|\[|\(|$)", re.I), "2502.15654:modernbert"),
    (
        re.compile(r"^RoBERTa-ChatGPT(?:\s|\[|\(|$)", re.I),
        "2504.11369:chatgpt-detector",
    ),
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
    r"uncertainty|divscore|specdetect|fourier|repreguard|glimpse|dald|adagpt|"
    r"camf|raidar|gpt\+cot|gpt\+react|attention pooling|target shuffling|"
    r"w/o|without|full model)",
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
    evidence_locator: str
    qualifying_evidence: str


@dataclass(frozen=True)
class Resolution:
    candidate: Candidate
    resolution_kind: str
    target_account_ids: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class AccountWitness:
    parent_id: str
    account_id: str
    witness_id: str
    join_kind: str
    join_key: str
    identity_page: int
    identity_line: int
    identity_locator: str
    identity_text: str
    metric_page: int
    metric_line: int
    metric_locator: str
    metric_text: str
    metric_value: str
    raw_candidate_id: str
    source_text_sha256: str


def compact(value: str) -> str:
    return SPACE_PATTERN.sub(" ", CONTROL_PATTERN.sub("", value)).strip()


def searchable(value: str) -> str:
    """Normalize mathematical Unicode glyphs before semantic pattern matching."""
    return unicodedata.normalize("NFKC", value)


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def identity_normalized(value: str) -> str:
    """Normalize a printed method identity without collapsing `++` variants."""
    return normalized(value.replace("++", " plus ").replace("+", " plus "))


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
    accounts = [
        Account(
            row["parent_id"],
            row["account_id"],
            row["system"],
            row["evidence_locator"],
            row["qualifying_evidence"],
        )
        for row in rows
    ]
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
        # Leaderboards often begin with a numeric rank, followed by the system
        # name and then the first metric.  Preserve the name between the first
        # two numbers instead of collapsing every such result to an opaque
        # ``numeric configuration`` label.
        label = compact(line[match.end() : matches[1].start()]).strip("|:;,-–—")
    if not label and len(matches) >= 2:
        label = f"numeric configuration {match.group()}"
    n_words = len(re.findall(r"[A-Za-z][A-Za-z-]*", label))
    if not label or not 1 <= n_words <= 20 or len(label) > 180:
        return None
    return label


def _locator(lines: list[str], index: int, previous_caption: str, section: str) -> str:
    captions = [
        (candidate_index, compact(line[match.start() :]))
        for candidate_index, line in enumerate(lines)
        if (match := CAPTION_PATTERN.search(line)) is not None
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
        parts.append("caption continuation")
    if section:
        parts.append(section)
    return compact(" | ".join(parts))


def discover(
    source: Source,
    paper_root: Path,
    *,
    source_text: str | None = None,
) -> list[Candidate]:
    text = (
        source_text
        if source_text is not None
        else extract_text(paper_root / source.paper_path)
    )
    document_metric_witness = next(
        (
            f"document metric context line {line_number}: {compact(line)}"
            for line_number, line in enumerate(text.splitlines(), start=1)
            if METRIC_HEADER_PATTERN.search(searchable(line))
            and re.search(
                r"\b(?:report|evaluation|metric|score|performance|result)\w*\b",
                line,
                re.IGNORECASE,
            )
        ),
        "",
    )
    found: list[Candidate] = []
    absolute_line = 0
    previous_caption = ""
    active_section = ""
    emitted_claim_labels: set[str] = set()
    pages = text.split("\f")
    table_caption_count = sum(
        len(TABLE_PATTERN.findall(line)) for line in text.splitlines()
    )
    roman_table_caption_count = sum(
        len(ROMAN_TABLE_PATTERN.findall(line)) for line in text.splitlines()
    )
    figure_caption_count = sum(
        len(FIGURE_PATTERN.findall(line)) for line in text.splitlines()
    )
    for page_number, page in enumerate(pages, start=1):
        lines = page.splitlines()
        page_start_line = absolute_line
        page_has_figure = any(FIGURE_PATTERN.search(line) for line in lines)
        current_page_has_table = any(TABLE_PATTERN.search(line) for line in lines)
        page_has_table = current_page_has_table or bool(
            previous_caption
            and TABLE_PATTERN.search(previous_caption)
            and not page_has_figure
        )
        page_has_metric = any(
            METRIC_HEADER_PATTERN.search(searchable(line)) for line in lines
        )
        metric_context = page_has_metric or bool(document_metric_witness)
        page_has_high_metric = any(
            metric_trigger(compact(line), page_has_metric) is not None for line in lines
        )
        for index, raw_line in enumerate(lines):
            absolute_line += 1
            normalized_line = compact(raw_line)
            if (caption_match := CAPTION_PATTERN.search(raw_line)) is not None:
                previous_caption = compact(raw_line[caption_match.start() :])
            if SECTION_PATTERN.search(normalized_line):
                active_section = normalized_line
            if (
                not page_has_table
                or not metric_context
                or (
                    not page_has_metric
                    and (
                        not current_page_has_table
                        or len(NUMBER_PATTERN.findall(normalized_line)) < 2
                    )
                )
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
            trigger = metric_trigger(normalized_line, metric_context)
            label = row_label(normalized_line) if trigger else None
            if trigger is None or label is None:
                continue
            start = max(0, index - 2)
            context = compact(" || ".join(lines[start : index + 1]))
            locator = _locator(lines, index, previous_caption, active_section)
            if not page_has_metric:
                trigger = f"offpage_metric_{trigger}"
                context = compact(f"{context} || {document_metric_witness}")
                locator = compact(f"{locator} | off-page metric definition")
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

        # A two-column PDF can place an equation or prose fragment before a
        # complete detector row on the same physical line.  Scan each layout
        # column independently so the first number in the unrelated column
        # cannot erase the method label.
        if (
            source.parent_id in SPLIT_COLUMN_PARENT_IDS
            and page_has_table
            and page_has_metric
        ):
            for index, raw_line in enumerate(lines):
                segments = [
                    compact(segment)
                    for segment in re.split(r"\s{2,}", raw_line.strip())
                    if compact(segment)
                ]
                if len(segments) < 2:
                    continue
                for segment_index, segment in enumerate(segments):
                    if not METHOD_LIKE_PATTERN.search(segment):
                        continue
                    joined_segment = compact(" ".join(segments[segment_index:]))
                    joined_segment = re.sub(r"^\(\d+\)\s*", "", joined_segment)
                    trigger = metric_trigger(joined_segment, True)
                    label = row_label(joined_segment) if trigger else None
                    if (
                        trigger is None
                        or label is None
                        or not METHOD_LIKE_PATTERN.search(label)
                        or joined_segment == compact(raw_line)
                    ):
                        continue
                    locator = _locator(lines, index, previous_caption, active_section)
                    context = compact(" || ".join(lines[max(0, index - 2) : index + 1]))
                    line_number = page_start_line + index + 1
                    digest = hashlib.sha256(
                        f"{source.parent_id}\t{page_number}\t{line_number}\tsplit-column\t{joined_segment}".encode()
                    ).hexdigest()[:16]
                    found.append(
                        Candidate(
                            source.parent_id,
                            f"{source.parent_id}:{digest}",
                            page_number,
                            line_number,
                            locator,
                            f"split_column_{trigger}",
                            label,
                            context,
                        )
                    )

        # A table can define its evaluation metric in surrounding prose or an
        # appendix instead of repeating the header on the physical table page.
        # For multirow detector blocks, the detector identity is printed once
        # beside the middle model row.  Bind that literal method cell, all three
        # adjacent model rows, and the exact document-level metric witness.
        # This path is content-derived and runs for every such table; account
        # identities enter only later during resolution.
        if current_page_has_table and not page_has_metric and document_metric_witness:
            for index, raw_line in enumerate(lines):
                segments = [
                    compact(segment)
                    for segment in re.split(r"\s{2,}", raw_line.strip())
                    if compact(segment)
                ]
                if len(segments) < 2:
                    continue
                method_label = segments[0].strip("|:;,-–—")
                method_words = re.findall(r"[A-Za-z][A-Za-z0-9+_.-]*", method_label)
                if (
                    NUMBER_PATTERN.search(method_label)
                    or not 1 <= len(method_words) <= 8
                    or method_label.endswith(".")
                    or normalized(method_label) in {"detector", "detectors"}
                    or re.search(
                        r"\b(?:arxiv|proceedings|workshop|pages?|preprint|"
                        r"generated text detection)\b",
                        method_label,
                        re.IGNORECASE,
                    )
                    or not re.search(
                        r"(?:detect|binocular|radar|roberta|deberta|longformer|"
                        r"classifier|ensemble|baseline)",
                        normalized(method_label),
                    )
                ):
                    continue
                block = lines[max(0, index - 1) : min(len(lines), index + 2)]
                if (
                    not any(metric_trigger(compact(line), True) for line in block)
                    or sum(len(NUMBER_PATTERN.findall(line)) for line in block) < 4
                ):
                    continue
                locator = compact(
                    f"{_locator(lines, index, previous_caption, active_section)} "
                    "| off-page metric definition"
                )
                context = compact(f"{' || '.join(block)} || {document_metric_witness}")
                line_number = page_start_line + index + 1
                digest = hashlib.sha256(
                    f"{source.parent_id}\t{page_number}\t{line_number}\t"
                    f"offpage-grouped\t{method_label}\t{context}".encode()
                ).hexdigest()[:16]
                found.append(
                    Candidate(
                        source.parent_id,
                        f"{source.parent_id}:{digest}",
                        page_number,
                        line_number,
                        locator,
                        "offpage_metric_grouped_threshold_rows",
                        method_label,
                        context,
                    )
                )

        for state_pattern in DECLARED_STATE_PATTERNS.get(source.parent_id, ()):
            for index, raw_line in enumerate(lines):
                if (state_match := state_pattern.search(raw_line)) is None:
                    continue
                label = compact(state_match.group())
                locator = _locator(lines, index, previous_caption, active_section)
                if not DECLARED_STATE_LOCATORS[source.parent_id].search(locator):
                    continue
                context = compact(
                    " || ".join(lines[max(0, index - 2) : min(len(lines), index + 3)])
                )
                line_number = page_start_line + index + 1
                digest = hashlib.sha256(
                    f"{source.parent_id}\t{page_number}\t{line_number}\tnamed-state\t{label}\t{context}".encode()
                ).hexdigest()[:16]
                found.append(
                    Candidate(
                        source.parent_id,
                        f"{source.parent_id}:{digest}",
                        page_number,
                        line_number,
                        locator,
                        "named_fitted_state_row",
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
                    or normalized(label)
                    in {"detector", "detectors", "method", "model", "baseline"}
                ):
                    continue
                grouped_window = (
                    21 if source.parent_id in EXPANDED_GROUP_PARENT_IDS else 7
                )
                following = [
                    compact(line) for line in lines[index + 1 : index + grouped_window]
                ]
                threshold_rows = [
                    line
                    for line in following
                    if metric_trigger(line, True) is not None
                    and (
                        source.parent_id in EXPANDED_GROUP_PARENT_IDS
                        or GENERATOR_PATTERN.search(line)
                    )
                ]
                if len(threshold_rows) < 2:
                    continue
                locator = _locator(lines, index, previous_caption, active_section)
                context = compact(
                    " || ".join([raw_line, *lines[index + 1 : index + grouped_window]])
                )
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

        # Plot legends frequently carry the method identity on one line and
        # threshold-scale values on separate graphical text lines.  On a page
        # with a figure caption, metric header, and high value, split a genuine
        # multi-label legend into content-derived candidates.  This preserves
        # the literal label and surrounding plotted numbers instead of relying
        # on the hand-curated account inventory to seed discovery.
        if page_has_figure and page_has_metric and page_has_high_metric:
            for index, raw_line in enumerate(lines):
                segments = [
                    compact(segment).strip("|:;,-–—")
                    for segment in re.split(r"\s{2,}", raw_line.strip())
                ]
                eligible = [
                    segment
                    for segment in segments
                    if segment
                    and len(segment) <= 60
                    and 1 <= len(re.findall(r"[A-Za-z][A-Za-z0-9+_.-]*", segment)) <= 8
                    and FIGURE_LABEL_PATTERN.search(segment)
                    and FIGURE_LEGEND_TOKEN_PATTERN.fullmatch(segment)
                ]
                if len(set(eligible)) < 2:
                    continue
                locator = _locator(lines, index, previous_caption, active_section)
                context = compact(
                    " || ".join(lines[max(0, index - 3) : min(len(lines), index + 50)])
                )[:3000].rstrip()
                line_number = page_start_line + index + 1
                for label in dict.fromkeys(eligible):
                    digest = hashlib.sha256(
                        f"{source.parent_id}\t{page_number}\t{line_number}\tfigure-legend\t{label}\t{context}".encode()
                    ).hexdigest()[:16]
                    found.append(
                        Candidate(
                            source.parent_id,
                            f"{source.parent_id}:{digest}",
                            page_number,
                            line_number,
                            locator,
                            "figure_legend_threshold",
                            label,
                            context,
                        )
                    )

        # Some legitimate high-performance accounts use error rates where
        # smaller is better and therefore contain no >=0.90 row.  Preserve a
        # named method when the frozen text itself makes an explicit SOTA/best
        # claim, binding the exact nearby wording rather than inventing a
        # threshold surrogate.
        for index, raw_line in enumerate(lines):
            if source.parent_id not in STRONG_CLAIM_PARENT_IDS:
                break
            window = compact(
                " || ".join(lines[max(0, index - 3) : min(len(lines), index + 4)])
            )
            if not HIGH_CLAIM_PATTERN.search(window):
                continue
            for method_match in STRONG_CLAIM_METHOD_PATTERN.finditer(window):
                label = compact(method_match.group()).replace("- ", "-")
                label_key = normalized(label)
                if label_key in emitted_claim_labels:
                    continue
                emitted_claim_labels.add(label_key)
                line_number = page_start_line + index + 1
                digest = hashlib.sha256(
                    f"{source.parent_id}\t{page_number}\t{line_number}\tstrong-claim\t{label}\t{window}".encode()
                ).hexdigest()[:16]
                found.append(
                    Candidate(
                        source.parent_id,
                        f"{source.parent_id}:{digest}",
                        page_number,
                        line_number,
                        "explicit full-text high-performance claim",
                        "explicit_high_performance_claim",
                        label,
                        window[:3000].rstrip(),
                    )
                )

    content_candidate_count = len(found)
    source_text_sha256 = hashlib.sha256(text.encode()).hexdigest()
    page_count = sum(bool(page.strip()) for page in pages)
    summary_context = (
        f"source_text_sha256={source_text_sha256}; pages={page_count}; "
        f"table_captions={table_caption_count}; "
        f"roman_table_captions={roman_table_caption_count}; "
        f"figure_captions={figure_caption_count}; "
        f"content_candidates={content_candidate_count}"
    )
    summary_digest = hashlib.sha256(
        f"{source.parent_id}\tsource_scope_summary\t{source_text_sha256}\t{summary_context}".encode()
    ).hexdigest()[:16]
    found.append(
        Candidate(
            source.parent_id,
            f"{source.parent_id}:{summary_digest}",
            0,
            0,
            "entire bound PDF",
            "source_scope_summary",
            f"source {source.parent_id}",
            summary_context,
        )
    )
    return found


def discover_all(
    sources: list[Source],
    paper_root: Path,
    *,
    source_texts: dict[str, str] | None = None,
) -> list[Candidate]:
    return [
        candidate
        for source in sources
        for candidate in discover(
            source,
            paper_root,
            source_text=(
                None if source_texts is None else source_texts[source.parent_id]
            ),
        )
    ]


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


def load_candidates(path: Path) -> list[Candidate]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    return [
        Candidate(
            row["parent_id"],
            row["candidate_id"],
            int(row["page"]),
            int(row["line"]),
            row["table_locator"],
            row["trigger"],
            row["row_label"],
            row["context"],
        )
        for row in rows
    ]


def _account_aliases(account: Account) -> set[str]:
    slug = account.account_id.split(":", 1)[-1]
    system = re.split(
        r"\b(?:comparator|baseline|detector|trained on|target-adapted|with|using|after)\b",
        account.system,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]
    aliases = {
        identity_normalized(slug),
        identity_normalized(system),
        identity_normalized(account.system),
    }
    return {alias for alias in aliases if len(alias) >= 4}


def _local_resolution(item: Candidate) -> tuple[str, tuple[str, ...]] | None:
    locator = item.table_locator
    current_line = item.context.rsplit(" || ", 1)[-1]
    for parent_id, label_pattern, locator_pattern, targets in LOCAL_RULES:
        if (
            item.parent_id == parent_id
            and (
                label_pattern.search(item.row_label)
                or label_pattern.search(current_line)
            )
            and locator_pattern.search(locator)
        ):
            return "account_evidence", targets
    for parent_id, label_pattern, locator_pattern, targets in LOCAL_CARRY_RULES:
        if (
            item.parent_id == parent_id
            and (
                label_pattern.search(item.row_label)
                or label_pattern.search(current_line)
            )
            and locator_pattern.search(locator)
        ):
            return "targeted_carry_forward", targets
    return None


def _local_false_resolution(item: Candidate) -> tuple[str, str] | None:
    current_line = item.context.rsplit(" || ", 1)[-1]
    for parent_id, label_pattern, locator_pattern, kind, reason in LOCAL_FALSE_RULES:
        if (
            item.parent_id == parent_id
            and (
                label_pattern.search(item.row_label)
                or label_pattern.search(current_line)
            )
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
    label = identity_normalized(item.row_label)
    same_parent: list[tuple[int, int, str]] = []
    for alias, account_id in by_parent.get(item.parent_id, []):
        if label == alias:
            same_parent.append((2, len(alias), account_id))
        elif (len(alias) >= 6 and label.startswith(alias)) or (
            len(label) >= 6 and alias.startswith(label)
        ):
            same_parent.append((1, min(len(label), len(alias)), account_id))
    if same_parent:
        best = max((quality, length) for quality, length, _ in same_parent)
        return "account_evidence", tuple(
            sorted(
                {
                    target
                    for quality, length, target in same_parent
                    if (quality, length) == best
                }
            )
        )
    # Grouped PDF layouts can put the account identity on a preceding physical
    # row and the qualifying value on the current row.  Use only long exact
    # normalized aliases in the frozen local context so short/generic detector
    # names cannot capture unrelated neighboring results.
    context = identity_normalized(item.context)
    contextual = [
        (len(alias), account_id)
        for alias, account_id in by_parent.get(item.parent_id, [])
        if len(alias) >= 8 and alias in context
    ]
    if contextual:
        best = max(length for length, _ in contextual)
        return "account_evidence", tuple(
            sorted({target for length, target in contextual if length == best})
        )
    for pattern, target_id in CANONICAL_CARRY_RULES:
        if pattern.search(item.row_label):
            return "targeted_carry_forward", (target_id,)
    return None


def resolve_all(rows: list[Candidate], accounts: list[Account]) -> list[Resolution]:
    by_parent: dict[str, list[tuple[str, str]]] = {}
    for account in accounts:
        aliases = [(alias, account.account_id) for alias in _account_aliases(account)]
        by_parent.setdefault(account.parent_id, []).extend(aliases)
    resolutions: list[Resolution] = []
    for item in rows:
        if item.trigger == "source_scope_summary":
            kind, targets = "source_scope_summary", ()
            reason = (
                "This content-hash-bound row records the complete PDF discovery scope and "
                "candidate yield; it is not itself a detector-result claim."
            )
            resolutions.append(Resolution(item, kind, targets, reason))
            continue
        explicit_resolution = _local_resolution(item)
        false_resolution = (
            None if explicit_resolution is not None else _local_false_resolution(item)
        )
        matched = (
            explicit_resolution
            if explicit_resolution is not None
            else (
                None
                if false_resolution is not None
                else _matched_accounts(item, by_parent)
            )
        )
        if false_resolution is not None:
            kind, reason = false_resolution
            targets = ()
        elif matched is not None:
            kind, targets = matched
            reason = (
                f"The exact row label and {item.table_locator} bind this high-metric row to "
                f"{', '.join(targets)}."
            )
        elif NONDETECTOR_PATTERN.search(item.row_label) or GENERATOR_PATTERN.search(
            item.row_label
        ):
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


def load_resolutions(path: Path) -> list[Resolution]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    return [
        Resolution(
            Candidate(
                row["parent_id"],
                row["candidate_id"],
                int(row["page"]),
                int(row["line"]),
                row["table_locator"],
                row["trigger"],
                row["row_label"],
                row["context"],
            ),
            row["resolution_kind"],
            tuple(filter(None, row["target_account_ids"].split(","))),
            row["reason"],
        )
        for row in rows
    ]


WITNESS_TOKEN_STOPWORDS = {
    "account",
    "architecture",
    "baseline",
    "classifier",
    "default",
    "detector",
    "detection",
    "fine",
    "fitted",
    "method",
    "model",
    "paper",
    "primary",
    "result",
    "state",
    "submitted",
    "system",
    "trained",
    "using",
    "with",
}


def _witness_tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if len(token) >= 2 and token not in WITNESS_TOKEN_STOPWORDS
    }


def _identity_aliases(account: Account) -> set[str]:
    slug = account.account_id.split(":", 1)[-1]
    aliases = _account_aliases(account) | {
        identity_normalized(slug),
        identity_normalized(account.system),
    }
    aliases.update(
        identity_normalized(part)
        for part in re.split(r"\s+(?:with|using|after|on|for)\s+", account.system)
    )
    aliases.update(
        identity_normalized(alias)
        for alias in ACCOUNT_IDENTITY_ALIASES.get(account.account_id, ())
    )
    aliases.add(
        identity_normalized(
            re.sub(
                r"^(?:Master-test|GPT-4\.1-nano validation|Per-LLM|Per-family)\s+",
                "",
                account.system,
                flags=re.IGNORECASE,
            )
        )
    )
    for alias in tuple(aliases):
        if "fastdetectgpt" in alias:
            aliases.update(
                {
                    alias.replace("fastdetectgpt", "fastdetect"),
                    alias.replace("fastdetectgpt", "fdetectgpt"),
                }
            )
    return {alias for alias in aliases if len(alias) >= 3}


def _identity_score(
    account: Account,
    text: str,
    sibling_token_counts: dict[str, int],
) -> int:
    compact_text = identity_normalized(text)
    exact = 0
    boundary_exact = 0
    for alias in _identity_aliases(account):
        start = compact_text.find(alias)
        if start < 0:
            continue
        exact = max(exact, len(alias))
        end = start + len(alias)
        if end == len(compact_text) or not compact_text[end].isalpha():
            boundary_exact = max(boundary_exact, len(alias))
    account_tokens = _witness_tokens(
        f"{account.account_id.split(':', 1)[-1]} {account.system}"
    )
    overlap = account_tokens & _witness_tokens(text)
    unique = {token for token in overlap if sibling_token_counts.get(token, 0) == 1}
    if boundary_exact >= 3:
        return 2000 + boundary_exact
    if exact >= 3:
        return 1000 + exact
    if len(overlap) >= 2:
        return 100 + 10 * len(overlap)
    if unique and max(map(len, unique)) >= 3:
        return 50 + max(map(len, unique))
    return 0


def _metric_values(value: str, *, allow_wide: bool) -> tuple[str, ...]:
    matches = list(DECIMAL_METRIC_PATTERN.finditer(value))
    matches.extend(PERCENT_METRIC_PATTERN.finditer(value))
    if allow_wide:
        matches.extend(WIDE_METRIC_PATTERN.finditer(value))
    return tuple(
        dict.fromkeys(match.group().strip().removesuffix("%") for match in matches)
    )


def _expected_metric_values(account: Account) -> set[str]:
    evidence = re.sub(
        rf"\b(?:tables?|figures?|fig\.?)\s+{CAPTION_NUMBER}"
        rf"(?:\s*[-–—]\s*{CAPTION_NUMBER})?"
        rf"(?:\s*(?:,|and)\s*{CAPTION_NUMBER})*",
        " ",
        account.qualifying_evidence,
        flags=re.IGNORECASE,
    )
    evidence = re.sub(
        r"TPR\s*@\s*\d+(?:\.\d+)?\s*%\s*FPR", " ", evidence, flags=re.IGNORECASE
    )
    return set(_metric_values(evidence, allow_wide=True))


def _locator_tokens(value: str) -> set[str]:
    tokens = set()
    for match in re.finditer(
        rf"\b(?P<kind>tables?|figures?|fig\.?)\s+(?P<number>{CAPTION_NUMBER})\b",
        value,
        re.IGNORECASE,
    ):
        kind = "table" if match.group("kind").lower().startswith("table") else "figure"
        tokens.add(normalized(f"{kind}{match.group('number')}"))
    return tokens


def _witness_values_without_id(item: AccountWitness) -> tuple[str, ...]:
    return (
        item.parent_id,
        item.account_id,
        item.join_kind,
        item.join_key,
        str(item.identity_page),
        str(item.identity_line),
        item.identity_locator,
        item.identity_text,
        str(item.metric_page),
        str(item.metric_line),
        item.metric_locator,
        item.metric_text,
        item.metric_value,
        item.raw_candidate_id,
        item.source_text_sha256,
    )


def rekey_witness(item: AccountWitness) -> AccountWitness:
    digest = hashlib.sha256(
        "\t".join(_witness_values_without_id(item)).encode()
    ).hexdigest()[:16]
    return AccountWitness(
        item.parent_id,
        item.account_id,
        f"{item.account_id}@{digest}",
        item.join_kind,
        item.join_key,
        item.identity_page,
        item.identity_line,
        item.identity_locator,
        item.identity_text,
        item.metric_page,
        item.metric_line,
        item.metric_locator,
        item.metric_text,
        item.metric_value,
        item.raw_candidate_id,
        item.source_text_sha256,
    )


def _new_witness(
    account: Account,
    join_kind: str,
    join_key: str,
    identity_page: int,
    identity_line: int,
    identity_locator: str,
    identity_text: str,
    metric_page: int,
    metric_line: int,
    metric_locator: str,
    metric_text: str,
    metric_value: str,
    raw_candidate_id: str,
    source_text_sha256: str,
) -> AccountWitness:
    return rekey_witness(
        AccountWitness(
            account.parent_id,
            account.account_id,
            "",
            join_kind,
            join_key,
            identity_page,
            identity_line,
            identity_locator,
            identity_text,
            metric_page,
            metric_line,
            metric_locator,
            metric_text,
            metric_value,
            raw_candidate_id,
            source_text_sha256,
        )
    )


def witness_values(item: AccountWitness) -> tuple[str, ...]:
    values = _witness_values_without_id(item)
    return values[:2] + (item.witness_id,) + values[2:]


def serialize_witnesses(rows: list[AccountWitness]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(WITNESS_FIELDS)
    writer.writerows(witness_values(item) for item in rows)
    return stream.getvalue()


def write_witnesses(path: Path, rows: list[AccountWitness]) -> None:
    path.write_text(serialize_witnesses(rows), encoding="utf-8")


def load_witnesses(path: Path) -> list[AccountWitness]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    return [
        AccountWitness(
            row["parent_id"],
            row["account_id"],
            row["witness_id"],
            row["join_kind"],
            row["join_key"],
            int(row["identity_page"]),
            int(row["identity_line"]),
            row["identity_locator"],
            row["identity_text"],
            int(row["metric_page"]),
            int(row["metric_line"]),
            row["metric_locator"],
            row["metric_text"],
            row["metric_value"],
            row["raw_candidate_id"],
            row["source_text_sha256"],
        )
        for row in rows
    ]


def _page_records(text: str) -> list[tuple[int, int, int, str, list[str]]]:
    records: list[tuple[int, int, int, str, list[str]]] = []
    absolute_line = 0
    for page_number, page in enumerate(text.split("\f"), start=1):
        lines = page.splitlines()
        for index, line in enumerate(lines):
            absolute_line += 1
            records.append((page_number, absolute_line, index, line, lines))
    return records


def _candidate_metric_value(metric_text: str, account: Account) -> str:
    values = _metric_values(metric_text, allow_wide=True)
    expected = _expected_metric_values(account)
    return next(
        (value for value in values if value in expected),
        values[0] if values else "explicit high-performance claim",
    )


def _row_identity_forms(raw_label: str) -> set[str]:
    forms = {identity_normalized(raw_label)}
    without_attribution = re.sub(
        r"\s*(?:\[[^]]*]|\((?:ours|[^)]*et al\.?)[^)]*\)|[†‡*♣]+).*$",
        "",
        raw_label,
        flags=re.IGNORECASE,
    )
    forms.add(identity_normalized(without_attribution))
    if raw_label.lower().startswith("numeric configuration "):
        forms.add(identity_normalized(raw_label.removeprefix("numeric configuration ")))
    return {form for form in forms if form}


def _candidate_exact_row(candidate: Candidate, text: str) -> str:
    forms = _row_identity_forms(candidate.row_label)
    context_rows = [compact(part) for part in candidate.context.split(" || ")]
    source_rows = [
        compact(line)
        for page, _, _, line, _ in _page_records(text)
        if page == candidate.page
    ]
    for rows in (context_rows, source_rows):
        matches = []
        for row in rows:
            row_key = identity_normalized(row)
            identity_lengths = [
                len(form)
                for form in forms
                if row_key == form or row_key.startswith(form)
            ]
            if identity_lengths:
                matches.append((max(identity_lengths), -len(row), row))
        if matches:
            return max(matches)[2]
    return candidate.context


def _direct_witness(
    account: Account,
    resolution: Resolution,
    text: str,
    source_text_sha256: str,
) -> AccountWitness:
    candidate = resolution.candidate
    metric_text = _candidate_exact_row(candidate, text)
    return _new_witness(
        account,
        "direct_candidate",
        f"candidate={candidate.candidate_id}",
        candidate.page,
        candidate.line,
        candidate.table_locator,
        candidate.row_label,
        candidate.page,
        candidate.line,
        candidate.table_locator,
        metric_text,
        _candidate_metric_value(metric_text, account),
        candidate.candidate_id,
        source_text_sha256,
    )


def _direct_binding_score(
    account: Account,
    resolution: Resolution,
    sibling_token_counts: dict[str, int],
) -> int:
    local = _local_resolution(resolution.candidate)
    if local is not None:
        return 2000 if local == ("account_evidence", (account.account_id,)) else 0
    forms = _row_identity_forms(resolution.candidate.row_label)
    exact = max(
        (len(alias) for alias in _identity_aliases(account) if alias in forms),
        default=0,
    )
    score = 1000 + exact if exact else 0
    return score


def _direct_evidence_score(
    account: Account, resolution: Resolution, text: str
) -> tuple[int, int, int]:
    if (
        resolution.candidate.trigger == "explicit_high_performance_claim"
        and account.account_id != "2604.25860:luminol"
    ):
        # The other two claim candidates merely name comparison methods in
        # adjacent prose. Their qualifying evidence is in the result tables,
        # so they must receive a row-level witness rather than inheriting the
        # proposed method's SOTA wording.
        return (0, 0, 0)
    metric_text = _candidate_exact_row(resolution.candidate, text)
    values = _metric_values(metric_text, allow_wide=True)
    expected = _expected_metric_values(account)
    return (
        int(any(value in expected for value in values)),
        int(
            bool(values)
            or resolution.candidate.trigger == "explicit_high_performance_claim"
        ),
        len(values),
    )


def _sibling_token_counts(accounts: list[Account]) -> dict[str, dict[str, int]]:
    by_parent: dict[str, dict[str, int]] = {}
    for account in accounts:
        tokens = _witness_tokens(
            f"{account.account_id.split(':', 1)[-1]} {account.system}"
        )
        counts = by_parent.setdefault(account.parent_id, {})
        for token in tokens:
            counts[token] = counts.get(token, 0) + 1
    return by_parent


def _candidate_near_line(
    candidates: list[Candidate],
    page: int,
    line: int,
    metric_text: str,
) -> Candidate | None:
    same_page = [item for item in candidates if item.page == page]
    if not same_page:
        return None
    exact_context = [
        item
        for item in same_page
        if normalized(metric_text) in normalized(item.context)
    ]
    pool = exact_context or [item for item in same_page if abs(item.line - line) <= 6]
    return min(pool, key=lambda item: abs(item.line - line), default=None)


def _same_window_witness(
    account: Account,
    text: str,
    candidates: list[Candidate],
    sibling_token_counts: dict[str, int],
    source_text_sha256: str,
) -> AccountWitness | None:
    expected = _expected_metric_values(account)
    requested_locators = _locator_tokens(
        f"{account.evidence_locator} {account.qualifying_evidence}"
    )
    best: tuple[tuple[int, ...], AccountWitness] | None = None
    for page, absolute_line, index, line, lines in _page_records(text):
        identity_text = compact(line)
        identity_score = _identity_score(account, identity_text, sibling_token_counts)
        if identity_score == 0:
            continue
        page_has_metric = any(
            METRIC_HEADER_PATTERN.search(searchable(line)) for line in lines
        )
        for metric_index in range(max(0, index - 3), min(len(lines), index + 4)):
            metric_text = compact(lines[metric_index])
            values = _metric_values(metric_text, allow_wide=page_has_metric)
            if not values:
                continue
            metric_line = absolute_line + metric_index - index
            raw_candidate = _candidate_near_line(
                candidates, page, metric_line, metric_text
            )
            if raw_candidate is None:
                continue
            if len(
                requested_locators
            ) == 1 and not requested_locators & _locator_tokens(
                raw_candidate.table_locator
            ):
                continue
            if _identity_score(
                account, raw_candidate.context, sibling_token_counts
            ) == 0 or normalized(metric_text) not in normalized(raw_candidate.context):
                continue
            metric_value = next(
                (value for value in values if value in expected),
                max(values, key=lambda value: float(value)),
            )
            identity_locator = _locator(lines, index, "", "")
            metric_locator = _locator(lines, metric_index, "", "")
            witness = _new_witness(
                account,
                "same_window",
                f"page={page};identity_line={absolute_line};metric_line={metric_line}",
                page,
                absolute_line,
                identity_locator,
                identity_text,
                page,
                metric_line,
                metric_locator,
                metric_text,
                metric_value,
                raw_candidate.candidate_id,
                source_text_sha256,
            )
            score = (
                int(metric_value in expected),
                int(metric_index == index),
                _identity_score(
                    account,
                    f"{identity_text} {metric_text}",
                    sibling_token_counts,
                ),
                _identity_score(account, metric_text, sibling_token_counts),
                int(raw_candidate.line == metric_line),
                -abs(metric_index - index),
                identity_score,
                -absolute_line,
            )
            if best is None or score > best[0]:
                best = score, witness
    return None if best is None else best[1]


def _ordered_header_matches(header: str, columns: tuple[str, ...]) -> bool:
    """Require each declared result column to occur once in source order."""
    searchable_header = normalized(header)
    offset = 0
    for column in columns:
        token = normalized(column)
        index = searchable_header.find(token, offset)
        if index < 0:
            return False
        offset = index + len(token)
    return True


def _table_result_cells(row_text: str, row_label: str) -> tuple[str | None, ...]:
    """Parse ordered means/dashes from one compact result row."""
    match = re.match(
        rf"^{re.escape(row_label)}(?:\s+|$)(?P<cells>.*)$",
        row_text,
        re.IGNORECASE,
    )
    if match is None:
        return ()
    cells: list[str | None] = []
    for cell in re.finditer(
        r"—|(?<![\d.])(?P<mean>\d+(?:\.\d+)?)"
        r"(?:\s*±\s*\d+(?:\.\d+)?)?(?:[†‡*])?",
        match.group("cells"),
    ):
        cells.append(cell.group("mean"))
    return tuple(cells)


def _table_metric_column_witness(
    account: Account,
    text: str,
    candidates: list[Candidate],
    resolutions: list[Resolution],
    source_text_sha256: str,
) -> AccountWitness:
    """Bind a shared table row to the exact metric column owned by an account."""
    specification = TABLE_METRIC_COLUMN_ACCOUNTS.get(account.account_id)
    if specification is None:
        raise ValueError(f"unknown table-metric account: {account.account_id}")
    table_token, row_label, metric, columns, column_index, expected_value = (
        specification
    )
    resolution_by_id = {item.candidate.candidate_id: item for item in resolutions}
    matches: list[tuple[Candidate, int, int, str, str]] = []
    for page, absolute_line, index, line, lines in _page_records(text):
        row_text = compact(line)
        if not row_text or not identity_normalized(row_text).startswith(
            identity_normalized(row_label)
        ):
            continue
        cells = _table_result_cells(row_text, row_label)
        if len(cells) != len(columns) or cells[column_index] != expected_value:
            continue
        header_rows = [
            (header_index, compact(header_line))
            for header_index, header_line in enumerate(lines[:index])
            if _ordered_header_matches(compact(header_line), columns)
        ]
        if not header_rows:
            continue
        header_index, header_text = max(header_rows)
        if index - header_index > 12:
            continue
        row_candidates = [
            candidate
            for candidate in candidates
            if candidate.page == page
            and candidate.line == absolute_line
            and table_token in _locator_tokens(candidate.table_locator)
            and normalized(row_text) in normalized(candidate.context)
            and (
                (resolution := resolution_by_id.get(candidate.candidate_id)) is not None
            )
            and resolution.resolution_kind == "account_evidence"
            and account.account_id in resolution.target_account_ids
        ]
        for candidate in row_candidates:
            matches.append((candidate, page, absolute_line, header_text, row_text))
    if len(matches) != 1:
        raise ValueError(
            f"table-metric account must resolve to one exact PDF row: "
            f"{account.account_id} ({len(matches)} found)"
        )
    candidate, page, absolute_line, header_text, row_text = matches[0]
    table_number = table_token.removeprefix("table")
    column = columns[column_index]
    join_key = (
        f"table={table_number};row={row_label};metric={metric};column={column};"
        f"column_position={column_index + 1};value={expected_value}"
    )
    metric_locator = (
        f"{candidate.table_locator} | metric={metric}; column={column}; "
        f"header={header_text}"
    )
    return _new_witness(
        account,
        "table_metric_column_join",
        join_key,
        page,
        absolute_line,
        candidate.table_locator,
        row_text,
        page,
        absolute_line,
        metric_locator,
        f"{header_text} || {row_text}",
        expected_value,
        candidate.candidate_id,
        source_text_sha256,
    )


def _table_configuration_claim_witness(
    account: Account,
    text: str,
    candidates: list[Candidate],
    resolutions: list[Resolution],
    source_text_sha256: str,
) -> AccountWitness:
    """Join a shared performance claim to one account-owned table cell."""
    specification = TABLE_CONFIGURATION_CLAIM_ACCOUNTS.get(account.account_id)
    if specification is None:
        raise ValueError(f"unknown table-claim account: {account.account_id}")
    table_token, row_label, metric, columns, column_index, expected_value = (
        specification
    )
    row_matches: list[tuple[int, int, int, list[str], str, str]] = []
    for page, absolute_line, index, line, lines in _page_records(text):
        row_text = compact(line)
        if not identity_normalized(row_text).startswith(identity_normalized(row_label)):
            continue
        cells = _table_result_cells(row_text, row_label)
        if len(cells) != len(columns) or cells[column_index] != expected_value:
            continue
        header_rows = [
            (header_index, compact(header_line))
            for header_index, header_line in enumerate(lines[:index])
            if _ordered_header_matches(compact(header_line), columns)
        ]
        if not header_rows:
            continue
        header_index, header_text = max(header_rows)
        if index - header_index > 24:
            continue
        locator = _locator(lines, index, "", "")
        if table_token not in _locator_tokens(locator):
            continue
        row_matches.append((page, absolute_line, index, lines, header_text, row_text))
    if len(row_matches) != 1:
        raise ValueError(
            f"table-claim account must resolve to one exact PDF row: "
            f"{account.account_id} ({len(row_matches)} found)"
        )

    support = [
        item
        for item in resolutions
        if item.candidate in candidates
        and item.resolution_kind == "account_evidence"
        and account.account_id in item.target_account_ids
        and item.candidate.parent_id == account.parent_id
        and item.candidate.trigger != "source_scope_summary"
    ]
    if len(support) != 1:
        raise ValueError(
            f"table-claim account must have one account-owned claim candidate: "
            f"{account.account_id} ({len(support)} found)"
        )
    claim = support[0].candidate
    page, absolute_line, index, lines, header_text, row_text = row_matches[0]
    table_number = table_token.removeprefix("table")
    column = columns[column_index]
    join_key = (
        f"table={table_number};row={row_label};metric={metric};column={column};"
        f"column_position={column_index + 1};value={expected_value};"
        f"claim_candidate={claim.candidate_id}"
    )
    row_locator = _locator(lines, index, "", "")
    metric_locator = (
        f"{row_locator} | metric={metric}; column={column}; header={header_text}; "
        f"claim={claim.table_locator}"
    )
    return _new_witness(
        account,
        "table_configuration_claim_join",
        join_key,
        page,
        absolute_line,
        row_locator,
        row_text,
        page,
        absolute_line,
        metric_locator,
        f"{header_text} || {row_text}",
        expected_value,
        claim.candidate_id,
        source_text_sha256,
    )


def _table_join_witness(
    account: Account,
    text: str,
    candidates: list[Candidate],
    sibling_token_counts: dict[str, int],
    source_text_sha256: str,
) -> AccountWitness | None:
    records = _page_records(text)
    identities = []
    for page, absolute_line, index, _, lines in records:
        identity_text = compact(
            " || ".join(lines[max(0, index - 1) : min(len(lines), index + 2)])
        )
        score = _identity_score(account, identity_text, sibling_token_counts)
        if score:
            identities.append((score, page, absolute_line, index, identity_text, lines))
    requested_locators = _locator_tokens(
        f"{account.evidence_locator} {account.qualifying_evidence}"
    )
    metric_candidates = [
        item
        for item in candidates
        if item.trigger != "source_scope_summary"
        and (
            not requested_locators
            or requested_locators & _locator_tokens(item.table_locator)
        )
    ]
    expected = _expected_metric_values(account)
    best: tuple[tuple[int, ...], AccountWitness] | None = None
    for identity_score, page, absolute_line, index, identity_text, lines in identities:
        for candidate in metric_candidates:
            if abs(candidate.page - page) > 2:
                continue
            values = _metric_values(candidate.context, allow_wide=True)
            if not values and candidate.trigger != "explicit_high_performance_claim":
                continue
            metric_value = next(
                (value for value in values if value in expected),
                values[0] if values else "explicit high-performance claim",
            )
            shared_locators = requested_locators & _locator_tokens(
                candidate.table_locator
            )
            join_locator = ",".join(sorted(shared_locators)) or normalized(
                candidate.table_locator
            )
            witness = _new_witness(
                account,
                "table_configuration_join",
                f"locator={join_locator};identity_line={absolute_line}",
                page,
                absolute_line,
                _locator(lines, index, "", ""),
                identity_text,
                candidate.page,
                candidate.line,
                candidate.table_locator,
                candidate.context,
                metric_value,
                candidate.candidate_id,
                source_text_sha256,
            )
            score = (
                int(metric_value in expected),
                int(bool(shared_locators)),
                -abs(candidate.page - page),
                -abs(candidate.line - absolute_line),
                identity_score,
            )
            if best is None or score > best[0]:
                best = score, witness
    return None if best is None else best[1]


def _same_line_text_witness(
    account: Account,
    text: str,
    sibling_token_counts: dict[str, int],
    source_text_sha256: str,
) -> AccountWitness | None:
    expected = _expected_metric_values(account)
    if not expected:
        return None
    best: tuple[tuple[int, int], AccountWitness] | None = None
    for page, absolute_line, index, line, lines in _page_records(text):
        row = compact(line)
        identity_score = _identity_score(account, row, sibling_token_counts)
        values = _metric_values(row, allow_wide=True)
        matching = [value for value in values if value in expected]
        if identity_score == 0 or not matching:
            continue
        locator = _locator(lines, index, "", "")
        witness = _new_witness(
            account,
            "same_line_text",
            f"page={page};line={absolute_line}",
            page,
            absolute_line,
            locator,
            row,
            page,
            absolute_line,
            locator,
            row,
            matching[0],
            "",
            source_text_sha256,
        )
        score = (identity_score, -absolute_line)
        if best is None or score > best[0]:
            best = score, witness
    return None if best is None else best[1]


def _same_line_error_witness(
    account: Account,
    text: str,
    sibling_token_counts: dict[str, int],
    source_text_sha256: str,
) -> AccountWitness | None:
    """Bind the two accepted low-error comparator results to their table rows."""
    if account.account_id not in LOW_ERROR_ACCOUNT_IDS:
        return None
    requested = _locator_tokens(
        f"{account.evidence_locator} {account.qualifying_evidence}"
    )
    best: tuple[tuple[int, int, int], AccountWitness] | None = None
    for page, absolute_line, index, line, lines in _page_records(text):
        row = compact(line)
        identity_score = _identity_score(account, row, sibling_token_counts)
        if identity_score == 0:
            continue
        locator = _locator(lines, index, "", "")
        if not requested & _locator_tokens(locator):
            continue
        values = [
            match.group()
            for match in re.finditer(r"(?<![\d.])(?:0?\.\d{3}|0)(?![\d.])", row)
            if float(match.group()) <= 0.01
        ]
        if not values:
            continue
        metric_value = min(values, key=float)
        witness = _new_witness(
            account,
            "same_line_error_rate",
            f"page={page};line={absolute_line};metric=error_rate",
            page,
            absolute_line,
            locator,
            row,
            page,
            absolute_line,
            locator,
            row,
            metric_value,
            "",
            source_text_sha256,
        )
        score = (identity_score, -int(float(metric_value) * 1000), -absolute_line)
        if best is None or score > best[0]:
            best = score, witness
    return None if best is None else best[1]


def _same_page_configuration_witness(
    account: Account,
    text: str,
    sibling_token_counts: dict[str, int],
    source_text_sha256: str,
) -> AccountWitness | None:
    expected = _expected_metric_values(account)
    requested = _locator_tokens(
        f"{account.evidence_locator} {account.qualifying_evidence}"
    )
    if not expected or not requested:
        return None
    records = _page_records(text)
    identities = [
        (
            _identity_score(account, compact(line), sibling_token_counts),
            page,
            absolute_line,
            index,
            compact(line),
            lines,
        )
        for page, absolute_line, index, line, lines in records
        if _identity_score(account, compact(line), sibling_token_counts)
    ]
    best: tuple[tuple[int, int, int], AccountWitness] | None = None
    for (
        identity_score,
        page,
        identity_line,
        identity_index,
        identity_text,
        lines,
    ) in identities:
        for metric_page, metric_line, metric_index, line, metric_lines in records:
            if metric_page != page:
                continue
            metric_text = compact(line)
            matching = [
                value
                for value in _metric_values(metric_text, allow_wide=True)
                if value in expected
            ]
            if not matching:
                continue
            metric_locator = _locator(metric_lines, metric_index, "", "")
            shared = requested & _locator_tokens(metric_locator)
            if not shared:
                continue
            witness = _new_witness(
                account,
                "same_page_configuration",
                "locator=" + ",".join(sorted(shared)),
                page,
                identity_line,
                _locator(lines, identity_index, "", ""),
                identity_text,
                metric_page,
                metric_line,
                metric_locator,
                metric_text,
                matching[0],
                "",
                source_text_sha256,
            )
            score = (identity_score, -abs(metric_line - identity_line), -metric_line)
            if best is None or score > best[0]:
                best = score, witness
    return None if best is None else best[1]


def _rank_pattern(rank: str, *, identity: bool) -> re.Pattern[str]:
    token = r"(?:BL|Baseline|[–—-])" if rank == "BL" else re.escape(rank)
    prefix = r"(?:^|\s{2,})" if identity else r"^\s*"
    return re.compile(rf"{prefix}{token}(?!\d)\s+", re.IGNORECASE)


def _caption_page(
    records: list[tuple[int, int, int, str, list[str]]], table_number: str
) -> tuple[int, str] | None:
    pattern = re.compile(rf"\bTable\s+{re.escape(table_number)}\s*:", re.IGNORECASE)
    return next(
        (
            (page, compact(line))
            for page, _, _, line, _ in records
            if pattern.search(line)
        ),
        None,
    )


def _shared_task_rank_witness(
    account: Account,
    text: str,
    candidates: list[Candidate],
    sibling_token_counts: dict[str, int],
    source_text_sha256: str,
) -> AccountWitness:
    track, rank = SHARED_TASK_RANKS[account.account_id]
    identity_table = "4" if track == "English" else "6"
    metric_tables = ("8",) if track == "English" else ("9", "10", "11")
    records = _page_records(text)
    identity_caption = _caption_page(records, identity_table)
    if identity_caption is None:
        raise ValueError(f"shared-task identity table absent: {account.account_id}")
    identity_page, identity_caption_text = identity_caption
    identity_rows = []
    for page, absolute_line, _, line, _ in records:
        if page != identity_page or not _rank_pattern(rank, identity=True).search(line):
            continue
        identity_text = compact(line)
        score = _identity_score(account, identity_text, sibling_token_counts)
        if account.account_id.endswith(
            ":english-baseline"
        ) or account.account_id.endswith(":multilingual-baseline"):
            score = max(score, 1000 if re.search(r"\bBaseline\b", line) else 0)
        if score:
            identity_rows.append((score, absolute_line, identity_text))
    if not identity_rows:
        raise ValueError(f"shared-task rank identity absent: {account.account_id}")
    _, identity_line, identity_text = max(identity_rows)

    expected = _expected_metric_values(account)
    metric_rows = []
    for table_number in metric_tables:
        caption = _caption_page(records, table_number)
        if caption is None:
            continue
        metric_page, caption_text = caption
        for page, absolute_line, _, line, lines in records:
            if page != metric_page or not _rank_pattern(rank, identity=False).search(
                line
            ):
                continue
            metric_text = compact(line)
            values = _metric_values(metric_text, allow_wide=True)
            matching = [value for value in values if value in expected]
            if not matching:
                continue
            raw_candidate = _candidate_near_line(
                candidates, metric_page, absolute_line, metric_text
            )
            if raw_candidate is None:
                continue
            metric_rows.append(
                (
                    len(matching),
                    table_number,
                    metric_page,
                    absolute_line,
                    caption_text,
                    metric_text,
                    matching[-1],
                    raw_candidate,
                    lines,
                )
            )
    if not metric_rows:
        raise ValueError(
            f"shared-task qualifying rank row absent: {account.account_id}"
        )
    (
        _,
        metric_table,
        metric_page,
        metric_line,
        metric_caption_text,
        metric_text,
        metric_value,
        raw_candidate,
        _,
    ) = max(metric_rows)
    return _new_witness(
        account,
        "shared_task_rank_join",
        f"track={track};rank={rank}",
        identity_page,
        identity_line,
        identity_caption_text,
        identity_text,
        metric_page,
        metric_line,
        metric_caption_text,
        metric_text,
        metric_value,
        raw_candidate.candidate_id,
        source_text_sha256,
    )


def _visual_figure_witness(
    account: Account,
    text: str,
    sibling_token_counts: dict[str, int],
    source_text_sha256: str,
    source_pdf_sha256: str,
) -> AccountWitness:
    value = FIGURE_CLASSIFIER_ACCOUNTS[account.account_id]
    records = _page_records(text)
    identities = [
        (
            _identity_score(account, compact(line), sibling_token_counts),
            page,
            absolute_line,
            compact(line),
        )
        for page, absolute_line, _, line, _ in records
        if _identity_score(account, compact(line), sibling_token_counts)
    ]
    if not identities:
        raise ValueError(f"visual-account identity absent: {account.account_id}")
    _, identity_page, identity_line, identity_text = max(identities)
    metric_rows = [
        (page, absolute_line, compact(line))
        for page, absolute_line, _, line, _ in records
        if re.search(r"models approaching\s+0\.99", line, re.IGNORECASE)
    ]
    if not metric_rows or "Figure 42" not in text or "Figure 43" not in text:
        raise ValueError(f"visual-account figure evidence absent: {account.account_id}")
    metric_page, metric_line, metric_text = metric_rows[0]
    return _new_witness(
        account,
        "visual_figure_carry",
        (
            f"figures=42,43;metric=accuracy;plot_value={value};"
            f"pdf_sha256={source_pdf_sha256}"
        ),
        identity_page,
        identity_line,
        "exact detector identity in the bound PDF",
        identity_text,
        metric_page,
        metric_line,
        "HC3 Figure 42 and ICNALE-plus-LLM Figure 43",
        metric_text,
        value,
        "",
        source_text_sha256,
    )


def _figure_series_witness(
    account: Account,
    text: str,
    candidates: list[Candidate],
    source_text_sha256: str,
) -> AccountWitness:
    label, value, series_index = FIGURE_SERIES_ACCOUNTS[account.account_id]
    matching_candidates = [
        item
        for item in candidates
        if item.trigger == "figure_legend_threshold"
        and identity_normalized(item.row_label) == identity_normalized(label)
        and "figure4" in _locator_tokens(item.table_locator)
        and value in item.context
    ]
    if len(matching_candidates) != 1:
        raise ValueError(f"Figure 4 legend candidate absent: {account.account_id}")
    candidate = matching_candidates[0]
    records = _page_records(text)
    page_records = [item for item in records if item[0] == candidate.page]
    legend = next(
        (
            (absolute_line, compact(line))
            for _, absolute_line, _, line, _ in page_records
            if all(
                identity_normalized(series_label) in identity_normalized(line)
                for series_label, _, _ in FIGURE_SERIES_ACCOUNTS.values()
            )
        ),
        None,
    )
    caption = next(
        (
            (absolute_line, compact(line))
            for _, absolute_line, _, line, _ in page_records
            if re.search(r"\bFig\.\s*4\.", line, re.IGNORECASE)
        ),
        None,
    )
    if legend is None or caption is None:
        raise ValueError(f"Figure 4 legend/caption absent: {account.account_id}")
    identity_line, identity_text = legend
    caption_line, caption_text = caption
    metric = next(
        (
            (absolute_line, compact(line), lines, index)
            for _, absolute_line, index, line, lines in page_records
            if identity_line < absolute_line < caption_line
            if re.search(rf"(?<![\d.]){re.escape(value)}(?![\d.])", line)
        ),
        None,
    )
    if metric is None:
        raise ValueError(f"Figure 4 series evidence absent: {account.account_id}")
    metric_line, metric_text, metric_lines, metric_index = metric
    return _new_witness(
        account,
        "figure_series_join",
        f"figure=4;domain=Code;series={series_index}",
        candidate.page,
        identity_line,
        caption_text,
        identity_text,
        candidate.page,
        metric_line,
        _locator(metric_lines, metric_index, "", ""),
        metric_text,
        value,
        candidate.candidate_id,
        source_text_sha256,
    )


def _table_column_witness(
    account: Account,
    text: str,
    candidates: list[Candidate],
    source_text_sha256: str,
) -> AccountWitness:
    label, row_label, value, series_index = TABLE_COLUMN_ACCOUNTS[account.account_id]
    matching_candidates = [
        item
        for item in candidates
        if identity_normalized(item.row_label) == identity_normalized(row_label)
        and "table9" in _locator_tokens(item.table_locator)
        and value in _candidate_exact_row(item, text)
    ]
    if len(matching_candidates) != 1:
        raise ValueError(f"Table 9 column candidate absent: {account.account_id}")
    candidate = matching_candidates[0]
    records = _page_records(text)
    page_records = [item for item in records if item[0] == candidate.page]
    headers = [
        (absolute_line, compact(line))
        for _, absolute_line, _, line, _ in page_records
        if identity_normalized(label) in identity_normalized(line)
        and "pawn" in identity_normalized(line)
        and absolute_line < candidate.line
    ]
    if not headers:
        raise ValueError(f"Table 9 column header absent: {account.account_id}")
    identity_line, identity_text = max(headers)
    metric_text = _candidate_exact_row(candidate, text)
    if value not in metric_text:
        raise ValueError(f"Table 9 column value absent: {account.account_id}")
    return _new_witness(
        account,
        "table_column_join",
        f"table=9;row={row_label};series={series_index}",
        candidate.page,
        identity_line,
        candidate.table_locator,
        identity_text,
        candidate.page,
        candidate.line,
        candidate.table_locator,
        metric_text,
        value,
        candidate.candidate_id,
        source_text_sha256,
    )


def _weak_state_witness(
    account: Account,
    text: str,
    sibling_token_counts: dict[str, int],
    source_text_sha256: str,
) -> AccountWitness:
    label, value, locator_token, state_key = WEAK_STATE_ACCOUNTS[account.account_id]
    matches = []
    for page, absolute_line, index, line, lines in _page_records(text):
        row = compact(line)
        locator = _locator(lines, index, "", "")
        if (
            identity_normalized(label) in identity_normalized(row)
            and re.search(rf"(?<![\d.]){re.escape(value)}(?![\d.])", row)
            and locator_token in _locator_tokens(locator)
            and _identity_score(account, row, sibling_token_counts)
        ):
            matches.append((page, absolute_line, locator, row))
    if len(matches) != 1:
        raise ValueError(f"weak-state row absent: {account.account_id}")
    page, absolute_line, locator, row = matches[0]
    return _new_witness(
        account,
        "same_line_weak_state",
        f"locator={locator_token};state={state_key};classification=nonqualifying_named_state",
        page,
        absolute_line,
        locator,
        row,
        page,
        absolute_line,
        locator,
        row,
        value,
        "",
        source_text_sha256,
    )


def _vertical_group_witness(
    account: Account,
    text: str,
    candidates: list[Candidate],
    source_text_sha256: str,
) -> AccountWitness:
    label, metric_label, value, locator_token = VERTICAL_GROUP_ACCOUNTS[
        account.account_id
    ]
    matching_candidates = [
        item
        for item in candidates
        if identity_normalized(item.row_label) == identity_normalized(metric_label)
        and locator_token in _locator_tokens(item.table_locator)
        and value in _candidate_exact_row(item, text)
    ]
    if len(matching_candidates) != 1:
        raise ValueError(f"vertical metric row absent: {account.account_id}")
    candidate = matching_candidates[0]
    records = _page_records(text)
    identity = next(
        (
            (absolute_line, compact(line))
            for page, absolute_line, _, line, _ in records
            if page == candidate.page
            and candidate.line < absolute_line <= candidate.line + 2
            and identity_normalized(label) in identity_normalized(line)
        ),
        None,
    )
    if identity is None:
        raise ValueError(f"vertical method identity absent: {account.account_id}")
    identity_line, identity_text = identity
    metric_text = _candidate_exact_row(candidate, text)
    return _new_witness(
        account,
        "vertical_model_group_join",
        f"locator={locator_token};model={identity_normalized(label)};metric=precision",
        candidate.page,
        identity_line,
        candidate.table_locator,
        identity_text,
        candidate.page,
        candidate.line,
        candidate.table_locator,
        metric_text,
        value,
        candidate.candidate_id,
        source_text_sha256,
    )


def _source_table_column_witness(
    account: Account,
    text: str,
    sibling_token_counts: dict[str, int],
    source_text_sha256: str,
) -> AccountWitness:
    label, row_label, value, locator_token, series_index = SOURCE_TABLE_COLUMN_ACCOUNTS[
        account.account_id
    ]
    records = _page_records(text)
    metric_rows = [
        (page, absolute_line, index, compact(line), lines)
        for page, absolute_line, index, line, lines in records
        if identity_normalized(row_label) in identity_normalized(line)
        and re.search(rf"(?<![\d.]){re.escape(value)}(?![\d.])", line)
        and locator_token in _locator_tokens(_locator(lines, index, "", ""))
    ]
    if len(metric_rows) != 1:
        raise ValueError(f"source table metric row absent: {account.account_id}")
    metric_page, metric_line, metric_index, metric_text, metric_lines = metric_rows[0]
    headers = [
        (absolute_line, compact(line))
        for page, absolute_line, _, line, _ in records
        if page == metric_page
        and absolute_line < metric_line
        and identity_normalized(label) in identity_normalized(line)
    ]
    if not headers:
        raise ValueError(f"source table column header absent: {account.account_id}")
    identity_line, identity_text = max(headers)
    if _identity_score(account, identity_text, sibling_token_counts) == 0:
        raise ValueError(f"source table column identity mismatch: {account.account_id}")
    locator = _locator(metric_lines, metric_index, "", "")
    return _new_witness(
        account,
        "source_table_column_join",
        f"locator={locator_token};row={identity_normalized(row_label)};series={series_index}",
        metric_page,
        identity_line,
        locator,
        identity_text,
        metric_page,
        metric_line,
        locator,
        metric_text,
        value,
        "",
        source_text_sha256,
    )


def _deer_routing_figure_witness(
    account: Account,
    text: str,
    source_text_sha256: str,
) -> AccountWitness:
    label, value, metric_kind, series_index = DEER_ROUTING_FIGURE_ACCOUNTS[
        account.account_id
    ]
    records = _page_records(text)
    identity_rows = [
        (page, absolute_line, compact(line))
        for page, absolute_line, _, line, _ in records
        if identity_normalized(label) in identity_normalized(line)
    ]
    if len(identity_rows) != 1:
        raise ValueError(f"DEER Figure 4 legend absent: {account.account_id}")
    identity_page, identity_line, identity_text = identity_rows[0]
    caption = next(
        (
            (absolute_line, compact(line))
            for page, absolute_line, _, line, _ in records
            if page == identity_page
            and re.search(r"\bFigure\s+4:", line, re.IGNORECASE)
        ),
        None,
    )
    if caption is None:
        raise ValueError(f"DEER Figure 4 caption absent: {account.account_id}")
    caption_line, caption_text = caption
    metric_rows = [
        (absolute_line, compact(line))
        for page, absolute_line, _, line, _ in records
        if page == identity_page
        and identity_line < absolute_line < caption_line
        and re.search(rf"(?<![\d.]){re.escape(value)}(?![\d.])", line)
    ]
    if not metric_rows:
        raise ValueError(f"DEER Figure 4 value absent: {account.account_id}")
    metric_line, metric_text = metric_rows[0]
    return _new_witness(
        account,
        "deer_figure_series_join",
        f"figure=4;series={series_index};metric={metric_kind}",
        identity_page,
        identity_line,
        caption_text,
        identity_text,
        identity_page,
        metric_line,
        caption_text,
        metric_text,
        value,
        "",
        source_text_sha256,
    )


def _react_shot_witness(
    account: Account,
    text: str,
    candidates: list[Candidate],
    source_text_sha256: str,
) -> AccountWitness:
    shot = REACT_SHOT_ACCOUNTS[account.account_id]
    records = _page_records(text)
    caption = _caption_page(records, "1")
    if caption is None:
        raise ValueError(f"REACT Table 1 absent: {account.account_id}")
    table_page, _ = caption
    header_rows = [
        (absolute_line, compact(line))
        for page, absolute_line, _, line, _ in records
        if page == table_page and re.search(r"R\s*EACT\s*\(Ours\)", line, re.IGNORECASE)
    ]
    if not header_rows:
        raise ValueError(f"REACT Table 1 column absent: {account.account_id}")
    identity_line, identity_text = header_rows[0]
    page_records = [item for item in records if item[0] == table_page]
    metric_rows: list[tuple[int, str, str, Candidate]] = []
    for index, (_, _, _, line, _) in enumerate(page_records):
        if not re.search(rf"(?:^|\s){re.escape(shot)}\s*$", line):
            continue
        previous = next(
            (item for item in reversed(page_records[:index]) if compact(item[3])),
            None,
        )
        if previous is None or not re.search(r"\bAcc\s*↑", previous[3]):
            continue
        _, metric_line, _, metric_raw, _ = previous
        metric_text = compact(metric_raw)
        means = re.findall(r"(?<![\d.])(\d{1,3}\.\d+)(?=±)", metric_text)
        if not means or float(means[-1]) < 90:
            continue
        raw_candidate = _candidate_near_line(
            candidates, table_page, metric_line, metric_text
        )
        if raw_candidate is None:
            continue
        metric_rows.append((metric_line, metric_text, means[-1], raw_candidate))
    if not metric_rows:
        raise ValueError(f"REACT shot row absent: {account.account_id}")
    metric_line, metric_text, metric_value, raw_candidate = metric_rows[0]
    return _new_witness(
        account,
        "column_configuration_join",
        f"table=1;column=REACT;shot={shot}",
        table_page,
        identity_line,
        "Table 1 column header",
        identity_text,
        table_page,
        metric_line,
        raw_candidate.table_locator,
        metric_text,
        metric_value,
        raw_candidate.candidate_id,
        source_text_sha256,
    )


def build_account_witnesses(
    sources: list[Source],
    paper_root: Path,
    accounts: list[Account],
    candidates: list[Candidate],
    resolutions: list[Resolution],
    *,
    source_texts: dict[str, str] | None = None,
    run_validation: bool = True,
) -> list[AccountWitness]:
    source_by_parent = {item.parent_id: item for item in sources}
    candidates_by_parent: dict[str, list[Candidate]] = {}
    for candidate in candidates:
        if candidate.trigger != "source_scope_summary":
            candidates_by_parent.setdefault(candidate.parent_id, []).append(candidate)
    direct_by_target: dict[str, list[Resolution]] = {}
    for resolution in resolutions:
        if resolution.resolution_kind != "account_evidence":
            continue
        for target in resolution.target_account_ids:
            direct_by_target.setdefault(target, []).append(resolution)
    sibling_counts = _sibling_token_counts(accounts)
    texts = {} if source_texts is None else source_texts
    witnesses = []
    missing_witnesses = []
    for account in accounts:
        source = source_by_parent[account.parent_id]
        if account.parent_id not in texts:
            text = extract_text(paper_root / source.paper_path)
            texts[account.parent_id] = text
        text = texts[account.parent_id]
        source_hash = hashlib.sha256(text.encode()).hexdigest()
        parent_candidates = candidates_by_parent.get(account.parent_id, [])
        if account.account_id in TABLE_METRIC_COLUMN_ACCOUNTS:
            witness = _table_metric_column_witness(
                account,
                text,
                parent_candidates,
                resolutions,
                source_hash,
            )
        elif account.account_id in TABLE_CONFIGURATION_CLAIM_ACCOUNTS:
            witness = _table_configuration_claim_witness(
                account,
                text,
                parent_candidates,
                resolutions,
                source_hash,
            )
        elif account.account_id in REACT_SHOT_ACCOUNTS:
            witness = _react_shot_witness(account, text, parent_candidates, source_hash)
        elif account.account_id in SHARED_TASK_RANKS:
            witness = _shared_task_rank_witness(
                account,
                text,
                parent_candidates,
                sibling_counts[account.parent_id],
                source_hash,
            )
        elif account.account_id in FIGURE_SERIES_ACCOUNTS:
            witness = _figure_series_witness(
                account, text, parent_candidates, source_hash
            )
        elif account.account_id in TABLE_COLUMN_ACCOUNTS:
            witness = _table_column_witness(
                account, text, parent_candidates, source_hash
            )
        elif account.account_id in SOURCE_TABLE_COLUMN_ACCOUNTS:
            witness = _source_table_column_witness(
                account,
                text,
                sibling_counts[account.parent_id],
                source_hash,
            )
        elif account.account_id in DEER_ROUTING_FIGURE_ACCOUNTS:
            witness = _deer_routing_figure_witness(
                account,
                text,
                source_hash,
            )
        elif account.account_id in WEAK_STATE_ACCOUNTS:
            witness = _weak_state_witness(
                account,
                text,
                sibling_counts[account.parent_id],
                source_hash,
            )
        elif account.account_id in VERTICAL_GROUP_ACCOUNTS:
            witness = _vertical_group_witness(
                account, text, parent_candidates, source_hash
            )
        elif account.account_id in VISUAL_FIGURE_ACCOUNT_IDS:
            witness = _visual_figure_witness(
                account,
                text,
                sibling_counts[account.parent_id],
                source_hash,
                file_sha256(paper_root / source.paper_path),
            )
        elif direct_matches := [
            (evidence_score, binding_score, item)
            for item in direct_by_target.get(account.account_id, [])
            if (
                binding_score := _direct_binding_score(
                    account, item, sibling_counts[account.parent_id]
                )
            )
            and (evidence_score := _direct_evidence_score(account, item, text))[1]
        ]:
            _, _, resolution = max(
                direct_matches,
                key=lambda item: (
                    item[0],
                    item[1],
                    item[2].candidate.candidate_id,
                ),
            )
            witness = _direct_witness(account, resolution, text, source_hash)
        else:
            witness = _same_line_error_witness(
                account, text, sibling_counts[account.parent_id], source_hash
            )
            if witness is None:
                witness = _same_window_witness(
                    account,
                    text,
                    parent_candidates,
                    sibling_counts[account.parent_id],
                    source_hash,
                )
            if witness is None:
                witness = _table_join_witness(
                    account,
                    text,
                    parent_candidates,
                    sibling_counts[account.parent_id],
                    source_hash,
                )
            if witness is None:
                witness = _same_line_text_witness(
                    account,
                    text,
                    sibling_counts[account.parent_id],
                    source_hash,
                )
            if witness is None:
                witness = _same_page_configuration_witness(
                    account,
                    text,
                    sibling_counts[account.parent_id],
                    source_hash,
                )
            if witness is None:
                missing_witnesses.append(account.account_id)
                continue
        witnesses.append(witness)
    if missing_witnesses:
        raise ValueError(
            "accounts lack source-derived witnesses: " + ",".join(missing_witnesses)
        )
    if run_validation:
        validate_account_witnesses(
            witnesses,
            sources,
            paper_root,
            accounts,
            candidates,
            resolutions,
            source_texts=texts,
        )
    return witnesses


def extract_source_texts(sources: list[Source], paper_root: Path) -> dict[str, str]:
    return {
        source.parent_id: extract_text(paper_root / source.paper_path)
        for source in sources
    }


def file_sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


_CANONICAL_WITNESS_CACHE: dict[tuple[object, ...], tuple[AccountWitness, ...]] = {}


def _same_number(left: str, right: str) -> bool:
    try:
        return abs(float(left) - float(right)) < 1e-9
    except ValueError:
        return left == right


def validate_account_witnesses(
    witnesses: list[AccountWitness],
    sources: list[Source],
    paper_root: Path,
    accounts: list[Account],
    candidates: list[Candidate],
    resolutions: list[Resolution],
    *,
    source_texts: dict[str, str] | None = None,
) -> None:
    account_by_id = {item.account_id: item for item in accounts}
    if len(witnesses) != len(accounts) or {
        item.account_id for item in witnesses
    } != set(account_by_id):
        raise ValueError(
            "account witness ledger must contain every account exactly once"
        )
    if len({item.account_id for item in witnesses}) != len(witnesses):
        raise ValueError("duplicate account witness")
    source_by_parent = {item.parent_id: item for item in sources}
    texts = source_texts or extract_source_texts(sources, paper_root)
    account_parent_ids = {item.parent_id for item in accounts}
    if not account_parent_ids <= set(texts) or not set(texts) <= set(source_by_parent):
        raise ValueError("account witness source-text set mismatch")
    source_hashes = {
        parent_id: hashlib.sha256(text.encode()).hexdigest()
        for parent_id, text in texts.items()
    }
    visual_parent_ids = {
        account_by_id[account_id].parent_id for account_id in VISUAL_FIGURE_ACCOUNT_IDS
    }
    source_pdf_hashes = {
        parent_id: file_sha256(paper_root / source_by_parent[parent_id].paper_path)
        for parent_id in visual_parent_ids
    }
    page_texts = {
        parent_id: {
            page: compact(page_text)
            for page, page_text in enumerate(text.split("\f"), start=1)
        }
        for parent_id, text in texts.items()
    }
    candidate_by_id = {item.candidate_id: item for item in candidates}
    resolution_by_id = {item.candidate.candidate_id: item for item in resolutions}
    sibling_counts = _sibling_token_counts(accounts)
    canonical_key = (
        tuple(accounts),
        tuple(candidates),
        tuple(resolutions),
        tuple(sorted(source_hashes.items())),
    )
    canonical_witnesses = _CANONICAL_WITNESS_CACHE.get(canonical_key)
    if canonical_witnesses is None:
        canonical_witnesses = tuple(
            build_account_witnesses(
                sources,
                paper_root,
                accounts,
                candidates,
                resolutions,
                source_texts=dict(texts),
                run_validation=False,
            )
        )
        _CANONICAL_WITNESS_CACHE[canonical_key] = canonical_witnesses
    if tuple(witnesses) != canonical_witnesses:
        supplied_by_id = {item.account_id: item for item in witnesses}
        mismatch = next(
            (
                item.account_id
                for item in canonical_witnesses
                if supplied_by_id.get(item.account_id) != item
            ),
            "unknown",
        )
        raise ValueError(
            f"account witness differs from canonical PDF derivation: {mismatch}"
        )
    allowed_kinds = {
        "direct_candidate",
        "same_window",
        "table_configuration_join",
        "table_configuration_claim_join",
        "table_metric_column_join",
        "column_configuration_join",
        "same_line_text",
        "same_line_error_rate",
        "same_page_configuration",
        "shared_task_rank_join",
        "visual_figure_carry",
        "figure_series_join",
        "table_column_join",
        "same_line_weak_state",
        "vertical_model_group_join",
        "source_table_column_join",
        "deer_figure_series_join",
    }
    for witness in witnesses:
        account = account_by_id[witness.account_id]
        if witness.parent_id != account.parent_id:
            raise ValueError(f"cross-parent account witness: {witness.account_id}")
        if witness.join_kind not in allowed_kinds:
            raise ValueError(f"unknown account witness kind: {witness.join_kind}")
        if witness != rekey_witness(witness):
            raise ValueError(f"account witness digest mismatch: {witness.account_id}")
        if witness.source_text_sha256 != source_hashes[witness.parent_id]:
            raise ValueError(
                f"account witness source hash mismatch: {witness.account_id}"
            )
        for page, label in (
            (witness.identity_page, "identity"),
            (witness.metric_page, "metric"),
        ):
            if page not in page_texts[witness.parent_id]:
                raise ValueError(
                    f"account witness {label} page absent: {witness.account_id}"
                )

        if witness.join_kind == "table_metric_column_join":
            parent_candidates = [
                item
                for item in candidates
                if item.parent_id == witness.parent_id
                and item.trigger != "source_scope_summary"
            ]
            expected_witness = _table_metric_column_witness(
                account,
                texts[witness.parent_id],
                parent_candidates,
                resolutions,
                source_hashes[witness.parent_id],
            )
            resolution = resolution_by_id.get(witness.raw_candidate_id)
            if (
                witness != expected_witness
                or resolution is None
                or resolution.resolution_kind != "account_evidence"
                or witness.account_id not in resolution.target_account_ids
            ):
                raise ValueError(
                    f"table-metric column witness detached: {witness.account_id}"
                )
            continue

        if witness.join_kind == "table_configuration_claim_join":
            parent_candidates = [
                item
                for item in candidates
                if item.parent_id == witness.parent_id
                and item.trigger != "source_scope_summary"
            ]
            expected_witness = _table_configuration_claim_witness(
                account,
                texts[witness.parent_id],
                parent_candidates,
                resolutions,
                source_hashes[witness.parent_id],
            )
            resolution = resolution_by_id.get(witness.raw_candidate_id)
            if (
                witness != expected_witness
                or resolution is None
                or resolution.resolution_kind != "account_evidence"
                or witness.account_id not in resolution.target_account_ids
            ):
                raise ValueError(
                    f"table-claim configuration witness detached: {witness.account_id}"
                )
            continue

        if witness.join_kind == "direct_candidate":
            candidate = candidate_by_id.get(witness.raw_candidate_id)
            resolution = resolution_by_id.get(witness.raw_candidate_id)
            if (
                candidate is None
                or resolution is None
                or resolution.resolution_kind != "account_evidence"
                or witness.account_id not in resolution.target_account_ids
                or witness.identity_text != candidate.row_label
                or witness.metric_locator != candidate.table_locator
                or witness.identity_page != candidate.page
                or witness.metric_page != candidate.page
                or witness.identity_line != candidate.line
                or witness.metric_line != candidate.line
                or (
                    candidate.trigger != "explicit_high_performance_claim"
                    and normalized(witness.metric_text)
                    not in normalized(page_texts[witness.parent_id][candidate.page])
                )
                or (
                    candidate.trigger == "explicit_high_performance_claim"
                    and witness.metric_text != candidate.context
                )
                or (
                    normalized(witness.metric_text) not in normalized(candidate.context)
                    and normalized(candidate.context)
                    not in normalized(witness.metric_text)
                )
                or (
                    candidate.trigger != "explicit_high_performance_claim"
                    and not any(
                        _same_number(witness.metric_value, value)
                        for value in _metric_values(
                            witness.metric_text, allow_wide=True
                        )
                    )
                )
                or _direct_binding_score(
                    account,
                    resolution,
                    sibling_counts[witness.parent_id],
                )
                == 0
            ):
                raise ValueError(
                    f"direct candidate witness detached: {witness.account_id}"
                )
            continue

        identity_page_text = page_texts[witness.parent_id][witness.identity_page]
        if normalized(witness.identity_text) not in normalized(identity_page_text):
            raise ValueError(f"witness identity text absent: {witness.account_id}")
        identity_score = _identity_score(
            account,
            witness.identity_text,
            sibling_counts[witness.parent_id],
        )
        shared_baseline = (
            witness.join_kind == "shared_task_rank_join"
            and witness.account_id.endswith(
                (":english-baseline", ":multilingual-baseline")
            )
            and re.search(r"\bBaseline\b", witness.identity_text, re.IGNORECASE)
        )
        if (
            identity_score == 0
            and witness.join_kind != "visual_figure_carry"
            and not shared_baseline
        ):
            raise ValueError(f"witness identity mismatch: {witness.account_id}")

        if witness.join_kind == "visual_figure_carry":
            value = FIGURE_CLASSIFIER_ACCOUNTS.get(witness.account_id)
            if (
                value is None
                or witness.raw_candidate_id
                or "Figure 42" not in texts[witness.parent_id]
                or "Figure 43" not in texts[witness.parent_id]
                or witness.join_key
                != (
                    f"figures=42,43;metric=accuracy;plot_value={value};"
                    f"pdf_sha256={source_pdf_hashes[witness.parent_id]}"
                )
                or normalized(witness.metric_text)
                not in normalized(page_texts[witness.parent_id][witness.metric_page])
                or not _same_number(witness.metric_value, value)
                or value not in account.qualifying_evidence
                or normalized("models approaching 0.99")
                not in normalized(witness.metric_text)
            ):
                raise ValueError(
                    f"visual figure witness detached: {witness.account_id}"
                )
            continue

        if witness.join_kind == "figure_series_join":
            series = FIGURE_SERIES_ACCOUNTS.get(witness.account_id)
            candidate = candidate_by_id.get(witness.raw_candidate_id)
            if series is None or candidate is None:
                raise ValueError(
                    f"Figure 4 series witness unknown: {witness.account_id}"
                )
            label, value, series_index = series
            legend_key = identity_normalized(witness.identity_text)
            positions = [
                legend_key.find(identity_normalized(series_label))
                for series_label, _, _ in FIGURE_SERIES_ACCOUNTS.values()
            ]
            if (
                candidate.trigger != "figure_legend_threshold"
                or candidate.parent_id != witness.parent_id
                or candidate.page != witness.identity_page
                or candidate.line != witness.identity_line
                or identity_normalized(candidate.row_label)
                != identity_normalized(label)
                or "figure4" not in _locator_tokens(candidate.table_locator)
                or witness.join_key != f"figure=4;domain=Code;series={series_index}"
                or "figure4" not in _locator_tokens(witness.identity_locator)
                or any(position < 0 for position in positions)
                or positions != sorted(positions)
                or normalized(witness.identity_text)
                not in normalized(page_texts[witness.parent_id][witness.identity_page])
                or normalized(witness.metric_text)
                not in normalized(page_texts[witness.parent_id][witness.metric_page])
                or not _same_number(witness.metric_value, value)
                or not any(
                    _same_number(witness.metric_value, item)
                    for item in _metric_values(witness.metric_text, allow_wide=True)
                )
                or value not in candidate.context
                or normalized(label) not in normalized(candidate.context)
                or "Fig. 4" not in candidate.context
            ):
                raise ValueError(
                    f"Figure 4 series witness detached: {witness.account_id}"
                )
            continue

        if witness.join_kind == "table_column_join":
            specification = TABLE_COLUMN_ACCOUNTS.get(witness.account_id)
            candidate = candidate_by_id.get(witness.raw_candidate_id)
            if specification is None or candidate is None:
                raise ValueError(f"table-column witness unknown: {witness.account_id}")
            label, row_label, value, series_index = specification
            header_labels = (
                "PAWN (GPT2)",
                "PAWN (LLaMA3-1b)",
                label,
            )
            header_key = identity_normalized(witness.identity_text)
            positions = [
                header_key.find(identity_normalized(item)) for item in header_labels
            ]
            if (
                witness.join_key != f"table=9;row={row_label};series={series_index}"
                or candidate.page != witness.identity_page
                or candidate.page != witness.metric_page
                or candidate.line != witness.metric_line
                or identity_normalized(candidate.row_label)
                != identity_normalized(row_label)
                or "table9" not in _locator_tokens(candidate.table_locator)
                or any(position < 0 for position in positions)
                or positions != sorted(positions)
                or series_index != 3
                or normalized(witness.identity_text)
                not in normalized(page_texts[witness.parent_id][witness.identity_page])
                or normalized(witness.metric_text)
                not in normalized(page_texts[witness.parent_id][witness.metric_page])
                or not _same_number(witness.metric_value, value)
                or not any(
                    _same_number(witness.metric_value, item)
                    for item in _metric_values(witness.metric_text, allow_wide=True)
                )
                or value not in candidate.context
            ):
                raise ValueError(f"table-column witness detached: {witness.account_id}")
            continue

        if witness.join_kind == "same_line_weak_state":
            specification = WEAK_STATE_ACCOUNTS.get(witness.account_id)
            if specification is None:
                raise ValueError(f"weak-state witness unknown: {witness.account_id}")
            label, value, locator_token, state_key = specification
            numeric_value = float(value)
            below_threshold = (
                numeric_value < 0.90 if numeric_value <= 1 else numeric_value < 90
            )
            if (
                witness.join_key
                != f"locator={locator_token};state={state_key};classification=nonqualifying_named_state"
                or witness.raw_candidate_id
                or witness.identity_page != witness.metric_page
                or witness.identity_line != witness.metric_line
                or witness.identity_text != witness.metric_text
                or identity_normalized(label)
                not in identity_normalized(witness.metric_text)
                or locator_token not in _locator_tokens(witness.metric_locator)
                or normalized(witness.metric_text)
                not in normalized(page_texts[witness.parent_id][witness.metric_page])
                or not _same_number(witness.metric_value, value)
                or not below_threshold
            ):
                raise ValueError(f"weak-state witness detached: {witness.account_id}")
            continue

        if witness.join_kind == "source_table_column_join":
            specification = SOURCE_TABLE_COLUMN_ACCOUNTS.get(witness.account_id)
            if specification is None:
                raise ValueError(
                    f"source-table-column witness unknown: {witness.account_id}"
                )
            label, row_label, value, locator_token, series_index = specification
            page_text = page_texts[witness.parent_id][witness.metric_page]
            if (
                witness.join_key
                != f"locator={locator_token};row={identity_normalized(row_label)};series={series_index}"
                or witness.raw_candidate_id
                or witness.identity_page != witness.metric_page
                or witness.identity_line >= witness.metric_line
                or identity_normalized(label)
                not in identity_normalized(witness.identity_text)
                or identity_normalized(row_label)
                not in identity_normalized(witness.metric_text)
                or locator_token not in _locator_tokens(witness.metric_locator)
                or normalized(witness.identity_text) not in normalized(page_text)
                or normalized(witness.metric_text) not in normalized(page_text)
                or not _same_number(witness.metric_value, value)
                or not re.search(
                    rf"(?<![\d.]){re.escape(value)}(?![\d.])",
                    witness.metric_text,
                )
                or value not in account.qualifying_evidence
            ):
                raise ValueError(
                    f"source-table-column witness detached: {witness.account_id}"
                )
            continue

        if witness.join_kind == "deer_figure_series_join":
            specification = DEER_ROUTING_FIGURE_ACCOUNTS.get(witness.account_id)
            if specification is None:
                raise ValueError(f"DEER figure witness unknown: {witness.account_id}")
            label, value, metric_kind, series_index = specification
            page_text = page_texts[witness.parent_id][witness.metric_page]
            if (
                witness.join_key
                != f"figure=4;series={series_index};metric={metric_kind}"
                or witness.raw_candidate_id
                or witness.identity_page != witness.metric_page
                or witness.identity_line >= witness.metric_line
                or identity_normalized(label)
                not in identity_normalized(witness.identity_text)
                or "figure4" not in normalized(witness.identity_locator)
                or "figure4" not in normalized(witness.metric_locator)
                or normalized(witness.identity_text) not in normalized(page_text)
                or normalized(witness.metric_text) not in normalized(page_text)
                or not _same_number(witness.metric_value, value)
                or not re.search(
                    rf"(?<![\d.]){re.escape(value)}(?![\d.])",
                    witness.metric_text,
                )
                or value not in account.qualifying_evidence
            ):
                raise ValueError(f"DEER figure witness detached: {witness.account_id}")
            continue

        if witness.join_kind == "vertical_model_group_join":
            specification = VERTICAL_GROUP_ACCOUNTS.get(witness.account_id)
            candidate = candidate_by_id.get(witness.raw_candidate_id)
            if specification is None or candidate is None:
                raise ValueError(
                    f"vertical-group witness unknown: {witness.account_id}"
                )
            label, metric_label, value, locator_token = specification
            if (
                witness.join_key
                != f"locator={locator_token};model={identity_normalized(label)};metric=precision"
                or candidate.page != witness.identity_page
                or candidate.page != witness.metric_page
                or candidate.line != witness.metric_line
                or not 0 < witness.identity_line - witness.metric_line <= 2
                or identity_normalized(candidate.row_label)
                != identity_normalized(metric_label)
                or locator_token not in _locator_tokens(candidate.table_locator)
                or identity_normalized(label)
                not in identity_normalized(witness.identity_text)
                or normalized(witness.identity_text)
                not in normalized(page_texts[witness.parent_id][witness.identity_page])
                or normalized(witness.metric_text)
                not in normalized(page_texts[witness.parent_id][witness.metric_page])
                or not _same_number(witness.metric_value, value)
                or not any(
                    _same_number(witness.metric_value, item)
                    for item in _metric_values(witness.metric_text, allow_wide=True)
                )
            ):
                raise ValueError(
                    f"vertical-group witness detached: {witness.account_id}"
                )
            continue

        if witness.join_kind in {"same_line_text", "same_page_configuration"}:
            if witness.raw_candidate_id:
                raise ValueError(
                    f"text witness has raw candidate: {witness.account_id}"
                )
            metric_page_text = page_texts[witness.parent_id][witness.metric_page]
            expected = _expected_metric_values(account)
            if (
                normalized(witness.metric_text) not in normalized(metric_page_text)
                or witness.metric_value not in expected
                or not any(
                    _same_number(witness.metric_value, value)
                    for value in _metric_values(witness.metric_text, allow_wide=True)
                )
            ):
                raise ValueError(f"text witness detached: {witness.account_id}")
            if witness.join_kind == "same_line_text":
                if (
                    witness.identity_page != witness.metric_page
                    or witness.identity_line != witness.metric_line
                    or witness.identity_text != witness.metric_text
                ):
                    raise ValueError(
                        f"same-line text witness detached: {witness.account_id}"
                    )
            else:
                requested = _locator_tokens(
                    f"{account.evidence_locator} {account.qualifying_evidence}"
                )
                if (
                    witness.identity_page != witness.metric_page
                    or not requested & _locator_tokens(witness.metric_locator)
                ):
                    raise ValueError(
                        f"same-page configuration detached: {witness.account_id}"
                    )
            continue

        if witness.join_kind == "same_line_error_rate":
            requested = _locator_tokens(
                f"{account.evidence_locator} {account.qualifying_evidence}"
            )
            values = [
                match.group()
                for match in re.finditer(
                    r"(?<![\d.])(?:0?\.\d{3}|0)(?![\d.])", witness.metric_text
                )
                if float(match.group()) <= 0.01
            ]
            if (
                witness.account_id not in LOW_ERROR_ACCOUNT_IDS
                or witness.raw_candidate_id
                or witness.identity_page != witness.metric_page
                or witness.identity_line != witness.metric_line
                or witness.identity_text != witness.metric_text
                or normalized(witness.metric_text)
                not in normalized(page_texts[witness.parent_id][witness.metric_page])
                or not requested & _locator_tokens(witness.metric_locator)
                or not any(
                    _same_number(witness.metric_value, value) for value in values
                )
            ):
                raise ValueError(
                    f"same-line error witness detached: {witness.account_id}"
                )
            continue

        candidate = candidate_by_id.get(witness.raw_candidate_id)
        if (
            candidate is None
            or candidate.parent_id != witness.parent_id
            or candidate.page != witness.metric_page
            or abs(candidate.line - witness.metric_line) > 6
        ):
            raise ValueError(f"witness metric candidate detached: {witness.account_id}")
        if not any(
            _same_number(witness.metric_value, value)
            for value in _metric_values(witness.metric_text, allow_wide=True)
        ):
            raise ValueError(f"witness metric value absent: {witness.account_id}")

        if witness.join_kind == "column_configuration_join":
            shot = REACT_SHOT_ACCOUNTS.get(witness.account_id, "")
            records = _page_records(texts[witness.parent_id])
            record_index = next(
                (
                    index
                    for index, item in enumerate(records)
                    if item[1] == witness.metric_line
                ),
                -1,
            )
            next_nonempty = next(
                (
                    compact(item[3])
                    for item in records[record_index + 1 :]
                    if item[0] == witness.metric_page and compact(item[3])
                ),
                "",
            )
            means = re.findall(r"(?<![\d.])(\d{1,3}\.\d+)(?=±)", witness.metric_text)
            if (
                not shot
                or witness.join_key != f"table=1;column=REACT;shot={shot}"
                or normalized("REACT (Ours)") not in normalized(witness.identity_text)
                or normalized(witness.metric_text)
                not in normalized(page_texts[witness.parent_id][witness.metric_page])
                or not re.search(rf"(?:^|\s){re.escape(shot)}\s*$", next_nonempty)
                or not means
                or not _same_number(witness.metric_value, means[-1])
                or float(witness.metric_value) < 90
                or witness.metric_text not in candidate.context
            ):
                raise ValueError(
                    f"column-configuration witness detached: {witness.account_id}"
                )
        elif witness.join_kind == "same_window":
            if (
                witness.identity_page != witness.metric_page
                or abs(witness.identity_line - witness.metric_line) > 5
                or normalized(witness.metric_text)
                not in normalized(page_texts[witness.parent_id][witness.metric_page])
            ):
                raise ValueError(f"same-window witness detached: {witness.account_id}")
        elif witness.join_kind == "table_configuration_join":
            requested = _locator_tokens(
                f"{account.evidence_locator} {account.qualifying_evidence}"
            )
            shared_locators = requested & _locator_tokens(witness.metric_locator)
            join_locator = ",".join(sorted(shared_locators)) or normalized(
                candidate.table_locator
            )
            if (
                witness.account_id in TABLE_METRIC_COLUMN_ACCOUNTS
                or witness.account_id in TABLE_CONFIGURATION_CLAIM_ACCOUNTS
                or abs(witness.identity_page - witness.metric_page) > 2
                or (
                    requested
                    and not requested & _locator_tokens(witness.metric_locator)
                )
                or witness.metric_text != candidate.context
                or witness.join_key
                != f"locator={join_locator};identity_line={witness.identity_line}"
                or normalized(witness.identity_text)
                not in normalized(page_texts[witness.parent_id][witness.identity_page])
                or _identity_score(
                    account,
                    witness.identity_text,
                    sibling_counts[witness.parent_id],
                )
                == 0
            ):
                raise ValueError(
                    f"table-configuration witness detached: {witness.account_id}"
                )
        else:
            track, rank = SHARED_TASK_RANKS.get(witness.account_id, ("", ""))
            identity_table = "4" if track == "English" else "6"
            metric_tables = {"8"} if track == "English" else {"9", "10", "11"}
            metric_locator_tokens = _locator_tokens(witness.metric_locator)
            if (
                witness.join_key != f"track={track};rank={rank}"
                or normalized(f"Table {identity_table}")
                not in _locator_tokens(witness.identity_locator)
                or not {
                    normalized(f"Table {table_number}")
                    for table_number in metric_tables
                }
                & metric_locator_tokens
                or not re.search(
                    rf"(?:^|\s){'(?:BL|Baseline|[–—-])' if rank == 'BL' else re.escape(rank)}(?!\d)\s+",
                    witness.identity_text,
                    re.IGNORECASE,
                )
                or not _rank_pattern(rank, identity=False).search(witness.metric_text)
                or not any(
                    _same_number(witness.metric_value, value)
                    for value in _expected_metric_values(account)
                )
            ):
                raise ValueError(
                    f"shared-task rank witness detached: {witness.account_id}"
                )


def content_requirements(resolutions: list[Resolution]) -> dict[str, set[str]]:
    discovered: dict[str, set[str]] = {}
    for item in resolutions:
        if item.resolution_kind == "account_evidence":
            discovered.setdefault(item.candidate.parent_id, set()).update(
                item.target_account_ids
            )
    missing = {
        parent_id: sorted(required - discovered.get(parent_id, set()))
        for parent_id, required in CONTENT_REQUIRED_ACCOUNT_IDS.items()
        if required - discovered.get(parent_id, set())
    }
    if missing:
        detail = "; ".join(
            f"{parent}: {','.join(ids)}" for parent, ids in missing.items()
        )
        raise ValueError(
            f"content-required table accounts were not independently resolved: {detail}"
        )
    return CONTENT_REQUIRED_ACCOUNT_IDS


def validate_source_coverage(
    candidates: list[Candidate],
    resolutions: list[Resolution],
    accounts: list[Account],
) -> None:
    summaries = [item for item in candidates if item.trigger == "source_scope_summary"]
    if len(summaries) != 119 or len({item.parent_id for item in summaries}) != 119:
        raise ValueError(
            "discovery must retain one content-hash scope summary for each of 119 PDFs"
        )
    content_count_by_parent: dict[str, int] = {}
    for summary in summaries:
        match = re.fullmatch(
            r"source_text_sha256=([0-9a-f]{64}); pages=(\d+); "
            r"table_captions=(\d+); roman_table_captions=(\d+); "
            r"figure_captions=(\d+); content_candidates=(\d+)",
            summary.context,
        )
        if match is None or int(match.group(2)) < 1:
            raise ValueError(f"malformed source-scope summary: {summary.parent_id}")
        actual_content = sum(
            item.parent_id == summary.parent_id
            and item.trigger != "source_scope_summary"
            for item in candidates
        )
        if actual_content != int(match.group(6)):
            raise ValueError(
                f"source-scope candidate count mismatch: {summary.parent_id}"
            )
        content_count_by_parent[summary.parent_id] = actual_content

    accounts_by_parent: dict[str, set[str]] = {}
    for account in accounts:
        accounts_by_parent.setdefault(account.parent_id, set()).add(account.account_id)
    unsupported_zero_yield = {
        parent_id: sorted(account_ids - set(WEAK_STATE_ACCOUNTS))
        for parent_id, account_ids in accounts_by_parent.items()
        if content_count_by_parent[parent_id] == 0
        and account_ids - set(WEAK_STATE_ACCOUNTS)
    }
    if unsupported_zero_yield:
        detail = "; ".join(
            f"{parent}: {','.join(ids)}"
            for parent, ids in sorted(unsupported_zero_yield.items())
        )
        raise ValueError(
            "account-bearing PDF has zero independent content candidates outside "
            "the exact below-threshold state class: " + detail
        )

    discovered_by_parent: dict[str, set[str]] = {}
    evidence_by_target: dict[str, list[Resolution]] = {}
    for item in resolutions:
        if item.resolution_kind != "account_evidence":
            continue
        discovered_by_parent.setdefault(item.candidate.parent_id, set()).update(
            item.target_account_ids
        )
        for target_id in item.target_account_ids:
            evidence_by_target.setdefault(target_id, []).append(item)

    required_zero_yield: dict[str, set[str]] = {}
    for account in accounts:
        if account.parent_id in PREDECESSOR_ZERO_YIELD_PARENT_IDS:
            required_zero_yield.setdefault(account.parent_id, set()).add(
                account.account_id
            )
    missing_zero_yield = {
        parent_id: sorted(required - discovered_by_parent.get(parent_id, set()))
        for parent_id, required in required_zero_yield.items()
        if required - discovered_by_parent.get(parent_id, set())
    }
    if missing_zero_yield:
        detail = "; ".join(
            f"{parent}: {','.join(ids)}"
            for parent, ids in sorted(missing_zero_yield.items())
        )
        raise ValueError(
            "predecessor zero-yield account lacks direct PDF discovery evidence: "
            + detail
        )

    wrong_roman_form = sorted(
        target_id
        for target_id in ROMAN_CONTENT_ACCOUNT_IDS
        if not any(
            re.search(
                r"\b(?:TABLE|Table)\s+[IVXLCDM]+\b",
                item.candidate.table_locator,
            )
            for item in evidence_by_target.get(target_id, [])
        )
    )
    if wrong_roman_form:
        raise ValueError(
            "Roman-caption account lacks Roman-table evidence: "
            + ",".join(wrong_roman_form)
        )
    wrong_figure_form = sorted(
        target_id
        for target_id in FIGURE_CONTENT_ACCOUNT_IDS
        if not any(
            item.candidate.trigger == "figure_legend_threshold"
            and re.search(
                r"\b(?:Figure|Fig\.?)\s+4\b",
                item.candidate.table_locator,
                re.IGNORECASE,
            )
            for item in evidence_by_target.get(target_id, [])
        )
    )
    if wrong_figure_form:
        raise ValueError(
            "figure account lacks direct legend/figure evidence: "
            + ",".join(wrong_figure_form)
        )
    wrong_offpage_form = sorted(
        target_id
        for target_id in OFFPAGE_METRIC_ACCOUNT_IDS
        if not any(
            item.candidate.trigger.startswith("offpage_metric_")
            and "document metric context line " in item.candidate.context
            and "off-page metric definition" in item.candidate.table_locator
            for item in evidence_by_target.get(target_id, [])
        )
    )
    if wrong_offpage_form:
        raise ValueError(
            "off-page metric account lacks table-to-definition evidence: "
            + ",".join(wrong_offpage_form)
        )


def validate_resolutions(
    candidates: list[Candidate],
    resolutions: list[Resolution],
    accounts: list[Account],
) -> None:
    if len(candidates) != len(resolutions):
        raise ValueError("every PDF-derived candidate must have exactly one resolution")
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
            raise ValueError(
                f"unresolved table candidate: {item.candidate.candidate_id}"
            )
        if len(item.reason) < 40:
            raise ValueError(
                f"underspecified table resolution: {item.candidate.candidate_id}"
            )
        if item.resolution_kind in {
            "account_evidence",
            "targeted_carry_forward",
            "duplicate_operating_point",
        }:
            if not item.target_account_ids:
                raise ValueError(
                    f"targetless table resolution: {item.candidate.candidate_id}"
                )
            for target_id in item.target_account_ids:
                target = account_by_id.get(target_id)
                if target is None:
                    raise ValueError(f"unknown table-resolution target: {target_id}")
                if (
                    item.resolution_kind == "account_evidence"
                    and target.parent_id != item.candidate.parent_id
                ):
                    raise ValueError(
                        f"cross-parent account evidence: {item.candidate.candidate_id}"
                    )
        elif item.target_account_ids:
            raise ValueError(
                f"false-positive resolution has a target: {item.candidate.candidate_id}"
            )
    content_requirements(resolutions)
    validate_source_coverage(candidates, resolutions, accounts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--paper-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--accounts", type=Path)
    parser.add_argument("--match-output", type=Path)
    parser.add_argument("--witness-output", type=Path)
    args = parser.parse_args()
    sources = load_sources(args.sources)
    candidates = discover_all(sources, args.paper_root)
    write(args.output, candidates)
    supplied_account_outputs = (
        args.accounts is not None,
        args.match_output is not None,
        args.witness_output is not None,
    )
    if any(supplied_account_outputs) and not all(supplied_account_outputs):
        raise ValueError(
            "--accounts, --match-output, and --witness-output must be supplied together"
        )
    unresolved = 0
    witness_count = 0
    if args.accounts is not None and args.match_output is not None:
        assert args.witness_output is not None
        accounts = load_accounts(args.accounts)
        resolutions = resolve_all(candidates, accounts)
        unresolved = sum(item.resolution_kind == "UNRESOLVED" for item in resolutions)
        if unresolved == 0:
            validate_resolutions(candidates, resolutions, accounts)
        args.match_output.write_text(
            serialize_resolutions(resolutions), encoding="utf-8"
        )
        witnesses = build_account_witnesses(
            sources, args.paper_root, accounts, candidates, resolutions
        )
        args.witness_output.write_text(serialize_witnesses(witnesses), encoding="utf-8")
        witness_count = len(witnesses)
    print(
        f"sources={len(sources)} content_candidates="
        f"{sum(item.trigger != 'source_scope_summary' for item in candidates)} "
        f"scope_summaries={sum(item.trigger == 'source_scope_summary' for item in candidates)} "
        f"unresolved={unresolved} account_witnesses={witness_count}"
    )


if __name__ == "__main__":
    main()
