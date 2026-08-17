# Public Qwen IRM detector-agreement follow-up

Run date: 14 August 2026, America/Los_Angeles.

## Decision and scope

The public `Qwen/Qwen2-0.5B` base/instruction pair is now implemented as an
isolated DW1 comparison sidecar. It does not change the production detector
schema or deployed classifier. The implementation follows Equation 5 of the
[NeurIPS 2025 IRM paper](https://proceedings.neurips.cc/paper_files/paper/2025/hash/f50258b34f1c5080e43281e05050034e-Abstract-Conference.html): the primary score
is instruction-model sequence log likelihood minus base-model sequence log
likelihood, summed over scored tokens. Higher is more AI-like. A mean-per-token
score is preserved only as a sensitivity and is not used for votes.

This follow-up supports the human's request to add IRM as a comparison. It does
not establish a production replacement: the available corpus is a convenience
set rather than a new stratified current-generator test, stored Binoculars and
FastDetectGPT scores are historical rather than fresh same-process forwards,
and the primary row split is not content-disjoint.

## Bound inputs and outputs

The score source is
[`benchmark_composite_detectors_scores.csv`](benchmark_composite_detectors_scores.csv),
with 8,022 rows and SHA-256
`c635d2b98583f9f9bcf3917f7ecb18469185550ab66d46ff60021a977195e786`.
The 4,907 eligible texts have at least 100 words. The schema-v2
[`run manifest`](qwen_irm_agreement_score_manifest.json) binds their ordered
row index, lexical path, byte length, and raw-text SHA-256 into aggregate digest
`4acd86ebcea12aceb129b88566318fcb32e62f8cd49350525b57d8edbf790612`.

The pinned models are:

- `Qwen/Qwen2-0.5B`, revision
  `91d2aff3f957f99e4c74c962f2f408dcc88a18d8`, on `cuda:1`;
- `Qwen/Qwen2-0.5B-Instruct`, revision
  `c540970f9e29518b1d8f06ab8b24cba66ad77b6d`, on `cuda:0`.

The run used float32, maximum 2,048 tokens, and batch 8. The immutable
[`completion manifest`](qwen_irm_agreement_completion_manifest.json) seals the
4,907-row [`score sidecar`](qwen_irm_agreement_scores.csv), whose SHA-256 is
`2e3556fb41397ad61700da0325fcd9d905ab3073a86a6be590e40cdb196beb10`.
Plotting refuses changed inputs, an edited sidecar, an incomplete checkpoint, or
an incompatible manifest.

All copied outputs and raw run logs are bound by
[`qwen_irm_agreement_artifacts.sha256`](qwen_irm_agreement_artifacts.sha256).
The machine-readable result is
[`qwen_irm_agreement_stats.json`](qwen_irm_agreement_stats.json); the two
validated vector diagrams are the
[`held-out-human SVG`](qwen_irm_agreement_held_out_human.svg) and
[`held-out-generated SVG`](qwen_irm_agreement_held_out_generated.svg).

## A6000 feasibility and timing

The clean bound run completed on two 49,140 MiB NVIDIA RTX A6000 cards with
driver 580.173.02. `/usr/bin/time -v` measured 7 minutes 51.43 seconds for the
full 4,907-page command, or about 10.4 pages per wall-clock second. This broad
boundary includes input validation and two complete text-hash passes,
tokenizer/model loading, tokenization, host/device transfer, scoring,
per-batch durable checkpoints, and the completion seal. The one-second
`nvidia-smi dmon` record observed peak framebuffer use of 35,309 MiB on GPU 0
and 35,307 MiB on GPU 1, with 100-percent sampled SM utilization on both.

This is a full-corpus wall-clock result, not the controlled inference-only
Binoculars comparator boundary. The earlier M4 screen measured the same public
pair at 1.833742 seconds per batch versus M1 Binoculars at 7.732507 seconds per
batch, with both boundaries beginning at device-resident tokens and ending at
CPU scores. M4 therefore remains the direct near-Binoculars-speed evidence;
this run independently confirms capacity and sustained execution.

## Established row-level comparison

The established split has 1,000 human calibration rows and a disjoint-by-row
evaluation of 2,315 human and 1,592 generated rows. No generated row selects a
threshold. Each detector independently uses `score > threshold` with at most
one percent of calibration humans flagged; ties are conservative.

| Detector | Evaluation AUROC | Human false positives | Generated detections |
| --- | ---: | ---: | ---: |
| Binoculars | 0.977899 | 27 / 2,315 (1.166%) | 1,052 / 1,592 (66.080%) |
| FastDetectGPT | 0.968952 | 24 / 2,315 (1.037%) | 1,202 / 1,592 (75.503%) |
| Qwen IRM sum | 0.974840 | 15 / 2,315 (0.648%) | 1,154 / 1,592 (72.487%) |
| At-least-two-of-three consensus | not applicable | 16 / 2,315 (0.691%) | 1,186 / 1,592 (74.497%) |

AUROC ranks scores over all thresholds; the one-percent operating point is one
selected cutoff. Binoculars can therefore have the best row-weighted AUROC
while Qwen has fewer false positives and more detections at these independently
calibrated cutoffs. No paired uncertainty or significance result is claimed.
The vote is detector consensus, not ground truth.

Because independently calibrated cutoffs realize different evaluation FPRs, the
statistics also preserve a post-hoc held-out ROC comparison at no more than one
percent human FPR. Qwen detects 1,231/1,592 generated rows (77.324%) at
20/2,315 human false positives (0.864%); FastDetectGPT detects 1,198 (75.251%)
at 23 false positives (0.994%); and Binoculars detects 933 (58.606%) at 17 false
positives (0.734%). Evaluation labels select these descriptive ROC points, so
their thresholds are not deployable and never affect the calibrated votes or
Venn regions. The comparison answers like-for-like tail discrimination, not
threshold transfer.

For held-out humans, the seven exclusive flag regions are Binoculars only 13,
FastDetectGPT only 9, IRM only 10, Binoculars/FastDetectGPT only 11,
Binoculars/IRM only 1, FastDetectGPT/IRM only 2, and all three 2; 2,267 are
unflagged by all three. For held-out generated pages, the corresponding counts
are 80, 27, 113, 145, 11, 214, and 816; 186 are unflagged. Thus 816 generated
rows are flagged by all three, 370 by exactly two, and 220 by exactly one.

## Content-overlap audit and sensitivity

The primary split is row-disjoint but not content-disjoint. Its 1,000
calibration rows contain 938 unique raw-text hashes; its 3,907 evaluation rows
contain 3,624. Sixteen text hashes cross the split, covering 77 calibration rows
and 137 evaluation rows, all human. Evaluation also has 283 duplicate rows by
raw-text hash. These repetitions can change row-weighted metrics and weaken the
meaning of “held out.”

The predeclared secondary sensitivity keeps the lowest row index per raw-text
hash, removes every evaluation hash seen in calibration, recalibrates on 938
unique human texts, and evaluates 2,159 unique human plus 1,449 unique generated
texts:

| Detector | Evaluation AUROC | Human false positives | Generated detections |
| --- | ---: | ---: | ---: |
| Binoculars | 0.981654 | 21 / 2,159 (0.973%) | 939 / 1,449 (64.803%) |
| FastDetectGPT | 0.974616 | 18 / 2,159 (0.834%) | 1,101 / 1,449 (75.983%) |
| Qwen IRM sum | 0.983949 | 15 / 2,159 (0.695%) | 1,082 / 1,449 (74.672%) |
| At-least-two-of-three consensus | not applicable | 14 / 2,159 (0.648%) | 1,081 / 1,449 (74.603%) |

The near-equal Qwen and consensus totals conceal substantial row-level
substitution. On unique human texts, consensus removes 11 Qwen-only flags and
adds 10 Binoculars/FastDetectGPT-only flags, so it differs from Qwen on 21 rows.
On unique generated texts, it removes 137 Qwen-only flags and adds 136
Binoculars/FastDetectGPT-only flags, differing on 273 rows. Thus the one-row
aggregate trade in each class is not evidence that the two decision rules agree.

This sensitivity reverses the small aggregate AUROC ordering: Qwen is 0.002295
above Binoculars rather than 0.003059 below it, and it also has the better
selected low-FPR operating point. The difference is descriptive, not evidence
of statistical superiority. The disagreement between row-weighted and
content-unique results is itself a reason to require a new content-disjoint,
stratified current-generator evaluation before any production change.

At the separate post-hoc held-out ROC point, all three content-unique detectors
use 21/2,159 false positives (0.973%). Qwen detects 1,172/1,449 generated texts
(80.883%), FastDetectGPT 1,122 (77.433%), and Binoculars 939 (64.803%). This
same-FPR view strengthens the descriptive low-tail result for Qwen but remains
non-deployable because evaluation labels choose the thresholds.

The two-of-three rule is not a demonstrated deployment improvement: it adds
three detector dependencies, trails FastDetectGPT's detection rate on the
primary view, and slightly trails Qwen on the content-unique view. Its value here
is agreement diagnosis.
