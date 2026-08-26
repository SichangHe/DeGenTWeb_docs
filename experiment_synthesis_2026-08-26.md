# Experiment synthesis for the DeGenTWeb detector study

This note integrates the reviewed learning-curve, body-swap, duplicate-threshold,
and detector-comparison results. It separates measured results from planned or
blocked work.

## Supported results

### Learning curve

The frozen dataset has 132 eligible sites: 67 generated and 65 human, with 15
pages per site. The primary mixed-domain curve uses the same balanced 20-site
held-out test set for 30 nested repeats at 10, 20, 30, and 40 training sites per
class. Mean balanced accuracy increases from 98.8% to 99.8% across those
checkpoints.

This is ceiling-like performance on one frozen baseline holdout. It does not
show that more data cannot improve transfer to new builders or site types.
Checkpoints at 80, 120, 160, and 200 sites per class are unsupported because the
smaller training class is short by 25, 65, 105, and 145 sites, respectively.

The directional curves use different test cohorts. Training on company sites
and testing on a distinct balanced 50-site personal cohort gives 95.8% balanced
accuracy at 20 training sites per class. Training on personal sites and testing
on a distinct balanced 54-site company cohort gives 100.0%. Builder and site
type change together, so these numbers are directional transfer checks, not
clean builder-generalization estimates.

The reviewed [protocol](https://github.com/SichangHe/DeGenTWeb/blob/15907e96946f4d12dece58189ce5882ada822cb3/imc2026stats/docs/learning_curve_protocol.md),
[results](https://github.com/SichangHe/DeGenTWeb/blob/15907e96946f4d12dece58189ce5882ada822cb3/imc2026stats/docs/learning_curve_results.md),
[site manifest](https://github.com/SichangHe/DeGenTWeb/blob/15907e96946f4d12dece58189ce5882ada822cb3/imc2026stats/learning_curve/site_manifest.csv),
and [plot](https://github.com/SichangHe/DeGenTWeb/blob/15907e96946f4d12dece58189ce5882ada822cb3/imc2026stats/learning_curve/learning_curve.pdf),
plus the page manifest, nested order, repeated-run table, and summary are bound
to DeGenTWeb commit `15907e9`. The corresponding Methods change is bound to
paper commit `0c3c91d`.

### Body-swap control

The reviewed control contains 24 current-original and reciprocal-swap page
records: one trusted Wix-human pair and one trusted B12-human pair, with three
pages per condition. Every record meets a 200-token minimum and was freshly
scored through one recorded scorer boundary.

All 24 page predictions match the text donor's label, no matched original/swap
pair crosses the page threshold, and descriptive median score differences range
from -0.023 to 0.000. This is a bounded page-level end-to-end
extraction-plus-detector control. It does not establish template invariance,
shell causality, site-level performance, or a population effect. See
[the body-swap protocol and limits](template_control.md).

### Detector and duplicate-threshold comparison

At the historical 50% duplicate cutoff, the shared Binoculars/FastDetectGPT
population contains 2,010 pages from 134 sites. Across 156 directional
held-out-builder site predictions, Binoculars makes 5 errors and FastDetectGPT
makes 3. The 156 prediction rows are not distinct sites because `Other` sites
occur in both test directions. Oriented page AUROC is 0.9378 and 0.9413,
respectively. The results are stable at 40%, 50%, 60%, and 75% cutoffs. This
supports robustness near 50%, not the claim that 50% is uniquely correct or
established by prior literature. See
[the reviewed sensitivity protocol](notes/duplicate_threshold_sensitivity.md).

Only Binoculars has a measured local runtime/GPU record in this comparison.
Pangram has a cost projection but no deployable local scorer or baseline result.
A historical 2026-08-25 preflight over 3,116 capped-input pages estimates a
same-input Pangram 4 full run at $1,180.75 realtime or $944.60 bulk before
research credits. It is not a reproducible frozen common cohort; recreate the
page manifest and price estimate before purchase. A one-page-per-site
feasibility run on that historical snapshot is estimated at $52.15 realtime or
$41.72 bulk, but cannot measure site-level accuracy. Pangram should therefore be
deferred until access, research credits or a fixed cap, and a frozen
scoring/adoption protocol exist. Pangram is not a rewrite detector.

RAIDAR and L2D remain literature-only and method-gated. A third builder and a
newer human cohort also remain deferred: neither has a provenance-qualified,
fully scored, matched-negative, frozen site-level holdout. Current hosting alone
does not establish human authorship. See the
[external detector review](external_detector_literature.md).

## Paper integration diff

The learning-curve Methods text is already present in paper commit `0c3c91d`.
The following bounded additions are ready for the paper owner. They should not
replace the explicit limitations.

### Add to detector evaluation

> We evaluated Binoculars and FastDetectGPT on a shared population after the
> historical 50% within-subdomain duplicate filter. The population contains
> 2,010 pages from 134 sites. Across 156 directional held-out-builder site
> predictions, Binoculars made 5 errors and FastDetectGPT made 3; oriented
> page-level AUROC was 0.9378 and 0.9413, respectively. Results were unchanged
> in direction and nearly unchanged in magnitude at 40%, 60%, and 75% cutoffs,
> so we treat 50% as a historical design choice rather than a literature-derived
> optimum. The 156 rows are directional predictions rather than distinct sites;
> `Other` sites occur in both test directions.

### Add to learning-curve results

> In the primary mixed-domain curve, one fixed balanced 20-site test set and 30
> nested repeats at 10, 20, 30, and 40 training sites per class increased mean
> balanced accuracy from 98.8% to 99.8%. The result indicates ceiling-like
> performance on this baseline holdout, not a general plateau. Larger
> checkpoints were not executable from the frozen pool: the smaller training
> class was short by 25, 65, 105, and 145 sites for 80, 120, 160, and 200 sites
> per class.

### Add to controls and limitations

> In a bounded body-swap control spanning one Wix-human pair and one B12-human
> pair, all 24 freshly scored page predictions followed the text donor's label,
> and no matched original/swap crossed the page threshold. Because this control
> covers only two site pairs and end-to-end extraction may include shell text,
> it does not establish template invariance, shell causality, or site-level
> generalization. Separate directional curves test a balanced 50-site personal
> cohort and a balanced 54-site company cohort; those results confound builder
> and site type. Pangram and rewrite-based alternatives remain unevaluated
> locally; their cost, access, method, and cohort gates are reported separately.
