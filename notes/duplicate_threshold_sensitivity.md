# Baseline duplicate-threshold sensitivity

## Purpose

This report tests whether the baseline detector result depends materially on the
rule that removes a page when more than 50% of its extracted text duplicates
earlier pages from the same subdomain. It measures cutoffs of 10%, 25%, 40%,
50%, 60%, 75%, and 100%. The sweep tests robustness around 50%; it does not
claim that 50% is uniquely optimal.

## Evaluated population

[`report_duplicate_threshold_sensitivity.py`](../../imc2026stats/report_duplicate_threshold_sensitivity.py)
uses the current labeled baseline sites and the full cleaned-page filters. A page
must have both stored Binoculars and FastDetectGPT scores. The two detectors are
therefore compared on exactly the same pages and sites at each cutoff. Other
detectors are omitted because their incomplete score coverage would make their
errors incomparable without another shared-population analysis.

For each subdomain, pages have one cutoff-independent order by URL hash, URL,
and classification ID. At each cutoff, the report keeps the first 15 eligible
pages from sites with at least 15 eligible pages. A looser cutoff can add an
earlier-priority page but cannot randomly reshuffle the sample. The output also
reports all eligible page and site counts before the 15-page cap.

## Metrics

The site-level comparison preserves the existing two held-out-builder
directions: train on Company sites and test on Personal plus Other sites; then
train on Personal sites and test on Company plus Other sites. Other sites occur
in both test directions, so `n_site_directional_predictions` is not a unique-site
count. If a direction cannot be fit, its evaluability and accuracy are reported
separately. If either linear SVM fit is not evaluable or emits a convergence
warning, its accuracy is blank and the combined site accuracy and error count
are also blank. The output retains evaluability and convergence fields for each
direction.

Page AUROC uses every sampled baseline page, including Other sites. Its raw
value and whether higher or lower scores indicate generated text are explicit.
The best page accuracy/error and TPR at no more than 1% page FPR use the same
sample labels to select their operating point. They are in-sample, label-selected,
post-hoc descriptions, not held-out error estimates or deployable thresholds.

## Output

The CSV is written to
`data/classify/baselines/duplicate_threshold_sensitivity.csv`. Interpret stable
results over nearby cutoffs as evidence that the conclusion is not specific to
50%. Do not compare nonconverged rows or extend this sensitivity result to a
detector whose scores were not part of the paired population.
