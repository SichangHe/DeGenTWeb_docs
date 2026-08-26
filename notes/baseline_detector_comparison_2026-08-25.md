# Baseline detector comparison and recommendation

## Result

The duplicate-cutoff sensitivity uses a shared, score-complete
Binoculars/FastDetectGPT population. At the historical 50% cutoff it retains
6,403 eligible pages from 144 sites before the per-site cap and samples 2,010
pages from 134 sites. Both site SVM directions converged.

| Detector | Cross-cohort site errors | Oriented page AUROC | Post-hoc page errors |
| --- | ---: | ---: | ---: |
| Binoculars | 5 / 156 directional predictions | 0.9378 after reversing its raw 0.0622 lower-is-generated score | 225 / 2,010 |
| FastDetectGPT | 3 / 156 directional predictions | 0.9413 | 207 / 2,010 |

The site errors are held-out cross-cohort results: Company sites train the first
classifier and Personal plus Other sites test it; Personal sites train the
second classifier and Company plus Other sites test it. Other sites occur in
both directions. Because Company generated sites are Wix and Personal generated
sites are B12, builder and site type change together. This is not a clean
builder-only estimate.

The page error counts are in-sample, label-selected, post-hoc descriptions, not
held-out estimates. The complete protocol and field definitions are in
[`duplicate_threshold_sensitivity.md`](duplicate_threshold_sensitivity.md).

Across the nearby 40%, 50%, 60%, and 75% duplicate cutoffs, Binoculars makes
5/156 site errors at every cutoff and FastDetectGPT makes 3/156 at every cutoff.
Binoculars oriented page AUROC stays between 0.9377 and 0.9382; FastDetectGPT
raw AUROC stays between 0.9409 and 0.9414. Thus the conclusion is insensitive
over this tested neighborhood. This supports retaining 50% as the historical
configuration; it does not establish 50% as uniquely optimal or literature
standard.

## Runtime and cost evidence

DW1's controlled Binoculars screen measured 7.7325 seconds per eight-document
batch, or 0.9666 seconds per document, on two RTX A6000 GPUs, with about 35 GB
peak allocation on each. The same boundary has not been rerun for the current
baseline sensitivity, and the stored FastDetectGPT scores are historical. The
canonical FastDetectGPT paper implies about 0.093 seconds per document from its
reported aggregate, but its A100 hardware, models, lengths, and unspecified
batching make that a scientific context point rather than a direct runtime
comparison. See the fixed comparison screen in
[`dw1_detector_survey.md`](dw1_detector_survey.md).

Pangram 4 currently lists $0.05 per 100 words and a 20% Bulk API discount. On
the reviewed active-baseline preflight, 3,116 filtered pages use an estimated
26,869 rounded credits: about $1,343 realtime or $1,075 bulk. This is a local
projection, not a vendor quote, and must be recomputed on the frozen purchase
manifest. Pangram says API access is separate from seat plans and academic
research credits may be available. See Pangram's
[pricing](https://www.pangram.com/pricing),
[credit definition](https://www.pangram.com/knowledge-hub/what-is-an-ai-detection-credit),
and [API page](https://www.pangram.com/solutions/api).

## Rewrite-detector feasibility

Pangram 4 is not rewrite-at-inference: its technical report describes classifier
inference, while rewriting and mirroring help create training data. The current
baseline has not been scored because no API credential or approved credit cap is
available. No Pangram accuracy comparison is claimed.

[RAIDAR](https://openreview.net/forum?id=bQWE2UqXmf) is the canonical simple
rewrite comparison: it rewrites once and learns from edit-distance features.
Its official repository uses an expired GPT-3.5-Turbo configuration, so a new
run requires an explicitly chosen and frozen substitute rewrite model and prompt.
Changing that model without disclosure would not reproduce the published state.

[L2D](https://openreview.net/forum?id=2ZUPeEM3FH) is the strongest recent
runnable rewrite candidate found. Its public detector checkpoint uses four
rewrites from manually gated `google/gemma-2-9b-it`; the model is about 18.55 GB,
and the paper reports 96 GB H20 experiments. The current environment has no
Hugging Face token and had about 11.3 GB free on each A6000 during preflight, so
no valid runtime or accuracy run was possible.

## Include/defer recommendation

Scoped status: no deployable Pangram scorer, approved price cap, or local
baseline comparison is currently available. The cost figures below are planning
estimates, not deployable pricing authorization. Rewrite alternatives remain
literature-only and gated on an explicit method/model choice or access and
compute. Third-builder and newer-human cohorts remain uncollected and
unevaluated pending provenance, complete detector-score coverage, and a frozen
held-out site-level protocol.

Include now:

- the paired Binoculars/FastDetectGPT baseline result
- the reviewed duplicate-cutoff sensitivity
- the measured Binoculars runtime/GPU footprint and the projected Pangram budget
- the accuracy-versus-runtime/cost rationale for retaining Binoculars

Defer pending explicit access or design decisions:

- Pangram accuracy claims until research credits or an approved capped pilot and
  API credential exist
- RAIDAR until the substitute rewrite model and prompt are prespecified
- L2D until Gemma access and sufficient GPU memory are available
- a third builder until it forms a provenance-documented, adequately sized,
  builder-level holdout with a matched negative/site-type cohort
- genuinely recent human negatives until authorship has direct provenance; a
  low-cost intermediate control is current text proven unchanged from a
  pre-ChatGPT archive snapshot

Wix-to-B12/B12-to-Wix transfer and body swapping address the immediate template
concern, but the former remains builder/site-type-confounded and neither replaces
a later third-builder external-validity test.
