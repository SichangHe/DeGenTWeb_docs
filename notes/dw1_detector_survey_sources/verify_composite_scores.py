"""Independently recompute the frozen composite-detector score CSV results."""

from __future__ import annotations

import csv
import hashlib
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path

from sklearn.metrics import roc_auc_score


DIRECT_SEED = 42
CALIBRATION_SEED = 20_260_808
MIN_WORDS = 100
EXPECTED_CSV_SHA256 = "c635d2b98583f9f9bcf3917f7ecb18469185550ab66d46ff60021a977195e786"


@dataclass(frozen=True)
class Row:
    row_index: int
    label: int
    word_count: int
    split: str
    scores: dict[str, float]


EXPECTED_AUCS = {
    "detectrlx_xlm_score": (0.918836, 0.9532527649044359),
    "desklib_score": (0.939764, 0.9750795011775941),
    "modernbert_score": (0.809716, 0.8337289850982775),
    "binoculars_ai_score": (0.9594860000000001, 0.9778986726288027),
    "fast_detect_gpt_score": (0.95362, 0.9689516697960645),
}

EXPECTED_OPERATING_POINTS = {
    "detectrlx_xlm_score": (
        (0.009071274298056155, 0.271356783919598),
        (0.05658747300215983, 0.8203517587939698),
    ),
    "desklib_score": (
        (0.009071274298056155, 0.8963567839195979),
        (0.056155507559395246, 0.9428391959798995),
    ),
    "modernbert_score": (
        (0.010367170626349892, 0.00628140703517588),
        (0.05701943844492441, 0.04020100502512563),
    ),
    "binoculars_ai_score": (
        (0.011663066954643628, 0.6608040201005025),
        (0.03628509719222462, 0.8574120603015075),
    ),
    "fast_detect_gpt_score": (
        (0.010367170626349892, 0.7550251256281407),
        (0.058315334773218146, 0.8624371859296482),
    ),
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read(path: Path) -> list[Row]:
    score_names = list(EXPECTED_AUCS)
    rows: list[Row] = []
    with path.open(newline="", encoding="utf-8") as stream:
        for raw in csv.DictReader(stream):
            rows.append(
                Row(
                    row_index=int(raw["row_index"]),
                    label=int(raw["is_generated"]),
                    word_count=int(raw["word_count"]),
                    split=raw["split"],
                    scores={name: float(raw[name]) for name in score_names},
                )
            )
    return rows


def _auc(rows: list[Row], score_name: str) -> float:
    return float(
        roc_auc_score(
            [row.label for row in rows],
            [row.scores[score_name] for row in rows],
        )
    )


def _assert_close(actual: float, expected: float) -> None:
    if not math.isclose(actual, expected, rel_tol=0.0, abs_tol=1e-12):
        raise SystemExit(f"mismatch: {actual!r} != {expected!r}")


def _threshold(human_scores: list[float], target_fpr: float) -> float:
    descending = sorted(human_scores, reverse=True)
    return descending[math.floor(target_fpr * len(descending))]


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_composite_scores.py SCORE_CSV")
    path = Path(sys.argv[1])
    actual_sha256 = _sha256(path)
    if actual_sha256 != EXPECTED_CSV_SHA256:
        raise SystemExit(f"unexpected CSV SHA-256: {actual_sha256}")

    rows = _read(path)
    if len(rows) != 8_022 or [row.row_index for row in rows] != sorted(
        row.row_index for row in rows
    ):
        raise SystemExit("row count or order mismatch")

    rng = random.Random(DIRECT_SEED)
    human = [row for row in rows if row.label == 0]
    generated = [row for row in rows if row.label == 1]
    direct = rng.sample(human, 500) + rng.sample(generated, 500)
    rng.shuffle(direct)

    eligible_human = [
        row for row in rows if row.label == 0 and row.word_count >= MIN_WORDS
    ]
    calibration = random.Random(CALIBRATION_SEED).sample(eligible_human, 1_000)
    calibration_ids = {row.row_index for row in calibration}
    evaluation = [
        row
        for row in rows
        if row.word_count >= MIN_WORDS and row.row_index not in calibration_ids
    ]
    evaluation_human = [row for row in evaluation if row.label == 0]
    evaluation_generated = [row for row in evaluation if row.label == 1]

    expected_splits = {
        row.row_index: (
            "excluded_under_100_words"
            if row.word_count < MIN_WORDS
            else "calibration_human"
            if row.row_index in calibration_ids
            else "evaluation"
        )
        for row in rows
    }
    if any(row.split != expected_splits[row.row_index] for row in rows):
        raise SystemExit("frozen split column disagrees with independent selection")
    if (len(calibration), len(evaluation_human), len(evaluation_generated)) != (
        1_000,
        2_315,
        1_592,
    ):
        raise SystemExit("split counts mismatch")

    for score_name, (
        expected_direct_auc,
        expected_evaluation_auc,
    ) in EXPECTED_AUCS.items():
        _assert_close(_auc(direct, score_name), expected_direct_auc)
        _assert_close(_auc(evaluation, score_name), expected_evaluation_auc)
        calibration_scores = [row.scores[score_name] for row in calibration]
        for target_fpr, expected in zip(
            (0.01, 0.05),
            EXPECTED_OPERATING_POINTS[score_name],
            strict=True,
        ):
            threshold = _threshold(calibration_scores, target_fpr)
            fpr = sum(
                row.scores[score_name] > threshold for row in evaluation_human
            ) / len(evaluation_human)
            tpr = sum(
                row.scores[score_name] > threshold for row in evaluation_generated
            ) / len(evaluation_generated)
            _assert_close(fpr, expected[0])
            _assert_close(tpr, expected[1])

    print(
        {
            "csv_sha256": actual_sha256,
            "rows": len(rows),
            "direct_rows": len(direct),
            "calibration_human": len(calibration),
            "evaluation_human": len(evaluation_human),
            "evaluation_generated": len(evaluation_generated),
            "auc_and_operating_point_checks": len(EXPECTED_AUCS) * 4,
            "result": "PASS",
        }
    )


if __name__ == "__main__":
    main()
