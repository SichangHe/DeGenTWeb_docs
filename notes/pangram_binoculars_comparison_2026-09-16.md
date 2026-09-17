# Pangram and Binoculars comparison

(authored by agents unless marked 🧑)

## Bottom line

The local data strongly support saying that Pangram has higher generated-page
sensitivity on the observed Claude body-swap pages. They do not support saying
that Pangram has better accuracy: the comparison has no human pages, Pangram's
false-positive rate is unknown, and the two detectors do not use matched
false-positive-rate thresholds.

Keep Binoculars as the reproducible baseline. Say that current detectors show
promising replacement paths, not that the local data establish a drop-in
replacement.

## Selected figure and matched comparison

Use [`pangram-vs-binoculars-all-available.pdf`](../data/pangram_binoculars_comparison_2026-09-16/pangram-vs-binoculars-all-available.pdf).
It is a completed direct same-page Pangram/Binoculars comparison. Do not use it as
an accuracy plot.

| call rule | generated pages detected | observed sensitivity |
|---|---:|---:|
| Pangram label is `AI` | 594/605 | 98.2% |
| Pangram AI percentage is at least 50% | 597/605 | 98.7% |
| Binoculars score is at or below max-F1 threshold | 470/605 | 77.7% |
| Binoculars score is at or below 0.01%-FPR threshold | 116/605 | 19.2% |

Suggested caption:

> Generated-page sensitivity on 605 of 780 accepted Claude Sonnet 4 and
> Sonnet 4.6 body-swapped pages. Each point compares Pangram's AI percentage
> with the Binoculars score; the vertical lines are Binoculars thresholds
> calibrated elsewhere. Pangram labeled 594/605 pages AI, while 470/605 fell
> below Binoculars' max-F1 threshold and 116/605 fell below its 0.01%-FPR
> threshold. This generated-only, incompletely observed cohort does not
> estimate either detector's accuracy or Pangram's false-positive rate, and
> the thresholds do not represent matched false-positive rates.

Coverage is 605/780 pages. It differs by model: 289/435 Sonnet 4 pages and
316/345 Sonnet 4.6 pages. All 52 sites have observations, but individual sites
have only 4--15 observed pages. The completed subset is not a random sample;
the submission process reused prior labels and prioritized texts under a credit
budget. The exact aggregate counts and site rows used here are in
[`all-available-analysis-summary.json`](../data/pangram_binoculars_comparison_2026-09-16/all-available-analysis-summary.json)
and
[`site-percentage-summary.csv`](../data/pangram_binoculars_comparison_2026-09-16/site-percentage-summary.csv).

The analysis contract states, verbatim, that it "reports generated-site
sensitivity evidence only" and "does not estimate SVM accuracy without
human-site Pangram percentages"
([source excerpt and original repository path](pangram_binoculars_source_excerpts_2026-09-16.md#pangram-analysis-contract)).

## What the model results support

### Older studied generators

The current full-corpus body-swap test detected generated sites at median rates
of 95.2% for GPT-3.5 Turbo, 97.3% for GPT-4, 100.0% for Mixtral 8x22B, and
98.6% for Llama 3.3 70B. This supports high detection on those generators only
for the body-swap out-of-distribution stress test.

The same test also detected 99.3% of Sonnet 4 and 97.2% of Sonnet 4.6 sites.
That difference does not establish a general recency effect inside the body-swap
task. The source explicitly says: "Older whole-site results and the preliminary
eight-Wix-site page-body run are not directly comparable"
([source excerpt and original repository path](pangram_binoculars_source_excerpts_2026-09-16.md#full-corpus-result-packet)).

### Newer whole-site generators

The separate Bedrock whole-site stress test is evidence of uneven performance
on current generators. Because every test site was generated, the reported
`site_accuracy` field is a generated-site detection rate: 90% for Sonnet 4,
15% for Sonnet 4.6, 75% for Haiku 4.5, 0% for DeepSeek R1, and 100% for
GPT-OSS-120B. Across seven
model/configuration points, this rate had Spearman correlation -0.870 with the
AA Intelligence Index. Seven points and heterogeneous model results are not
enough to establish a general chronological trend.

Safe wording:

> Binoculars-based site classification worked well on the older generators in
> our body-swap stress test, but a separate current whole-site stress test
> exposed large model-dependent failures. Detection was 15% on Sonnet 4.6
> versus 90% on Sonnet 4 and was 0% on DeepSeek R1, although GPT-OSS-120B was
> detected perfectly. The result shows sensitivity to generator and generation
> setup, not universal degradation with model age.

The exact whole-site values are in
[`bedrock-model-summary.csv`](../data/pangram_binoculars_comparison_2026-09-16/bedrock-model-summary.csv)
and [`bedrock-paper-stats.txt`](../data/pangram_binoculars_comparison_2026-09-16/bedrock-paper-stats.txt).

## Why Sonnet body swaps score better

The data establish the immediate reason, not the cause. Across all 780 pages in
the accepted body-swap manifest, mean Binoculars scores were 0.859 for 435
Sonnet 4 pages from 29 sites and 0.877 for 345 Sonnet 4.6 pages from 23 sites.
Each site contributes 15 pages. Lower is more AI-like. The separate whole-site
analysis reported corresponding model-summary means of 0.891 and 0.955. The
much higher Sonnet 4.6 whole-site scores put more sites on the missed side of
the classifier boundary.

The experiment does not isolate why those score distributions differ. Body
swaps replace text inside selected existing sites. The whole-site protocol says
it generated "20-page synthetic sites from minimal prompts" with `plain` and
`quality` prompt styles plus thinking controls
([experiment-protocol excerpt and original repository path](pangram_binoculars_source_excerpts_2026-09-16.md#bedrock-experiment-protocol)).
The cohorts, prompts, reasoning settings, retained pages, and sample sizes
differ. The reviewed source warns: "Prompts, reasoning settings,
retained pages, and other generation conditions were not isolated"
([source excerpt and original repository path](pangram_binoculars_source_excerpts_2026-09-16.md#full-corpus-result-packet)).

Therefore describe the lower body-swap scores as an observed explanation of the
classifier outputs, not a causal explanation of model behavior.

## Replacement claim

Three local results make replacement plausible:

- Pangram has much higher generated-page sensitivity on the observed Sonnet
  body-swap pages
- on the content-unique convenience split, Qwen IRM had AUROC 0.9839 versus
  0.9817 for Binoculars and detected 74.7% versus 64.8% of generated texts at
  their independently calibrated cutoffs, with 15 versus 21 human false calls
- Desklib detected 89.6% versus 66.1% for stored Binoculars near a locally
  calibrated 1% false-positive operating point, but its AUROC was slightly
  lower, 0.9751 versus 0.9779

None establishes replacement. Pangram lacks a human negative cohort. The Qwen
and Desklib comparisons use convenience data and historical Binoculars scores,
not fresh same-process scoring on a frozen current-generator test. The Qwen
report says, verbatim, "It does not establish a production replacement"
([`qwen_irm_agreement_results.md`](dw1_detector_survey_sources/qwen_irm_agreement_results.md)).
The detector inventory concludes, "None of the three replaces Binoculars"
([`candidate_manifest.md`](dw1_detector_survey_sources/candidate_manifest.md)).

Safe wording:

> Newer detectors can recover many current-generator pages that Binoculars
> misses at selected operating points. Our present comparisons do not
> establish greater accuracy or a replacement because they lack one frozen,
> content-disjoint current-generator test with fresh scores and matched
> false-positive-rate calibration.

## Claim strength

- strong: Pangram has higher sensitivity on the 605 observed generated pages
- moderate: the whole-site stress test exposes serious failures on some current
  generators
- weak: model age or strength alone causes the degradation
- unsupported: Pangram has better overall accuracy
- unsupported: a newer detector is already a validated drop-in replacement

Body-swap results remain an out-of-distribution stress test. The repository's
framing is explicit: "Results on them must be reported as an OOD stress test,
not as in-distribution accuracy or evidence about Wix or B12"
([`docs/template_control.md`](../template_control.md)).
