"""Summarize the immutable detector scores already stored for the DW1 trial."""

from __future__ import annotations

import csv
from pathlib import Path

from sklearn.metrics import roc_auc_score


REPO_ROOT = Path(__file__).resolve().parents[3]
TRIAL_DATA = REPO_ROOT / "data/classify/cc10k/fdgpt_trial_all_df1"
SCORE_COLUMNS = (
    "binoculars",
    "fast_detect_gpt",
    "lrr",
    "log_p",
    "log_rank",
    "roberta",
    "radar",
)


def main() -> None:
    labels: list[int] = []
    scores = {column: [] for column in SCORE_COLUMNS}
    with TRIAL_DATA.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            labels.append(int(row["is_generated"]))
            for column in SCORE_COLUMNS:
                scores[column].append(float(row[column]))

    print({"rows": len(labels), "human": labels.count(0), "generated": labels.count(1)})
    for column in SCORE_COLUMNS:
        raw_auc = float(roc_auc_score(labels, scores[column]))
        print(
            {
                "score": column,
                "raw_auc": raw_auc,
                "orientation_free_auc": max(raw_auc, 1 - raw_auc),
            }
        )


if __name__ == "__main__":
    main()
