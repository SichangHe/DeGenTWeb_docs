# Temporal Transition v2: Cohort + Tiered Evidence

Replaces the cutoff-based `complete_switch` claim
(`docs/temporal_transition.md`, approach 2) for the IMC 2026 paper.
The prior approach is fragile under reviewer scrutiny:
per-page threshold + purity rule + shuffle null model is a staircase,
and the paper section currently has two competing draft paragraphs that
both lean on it. The new design replaces the staircase with one cohort
filter and two simple per-site stats.

## Goal

Claim the form: "X% of CC sites that existed before ChatGPT show
LLM-shifted content after launch." Cohort restriction does the noise
control; per-site evidence comes in two tiers (strict + looser).
Drop the shuffle null model.

## Cohort definition (CC dataset only)

A subdomain qualifies iff:
1. It has ≥ 15 sampled pages total in the cc10k DuckDB session
   (the standard pipeline inclusion bar; matches
   `\BingResultSiteWfifteenCount` framing used elsewhere in the paper).
2. ≥ `K_PRE` of its sampled pages have htmldate publication date
   `< 2022-11-30` (ChatGPT launch).
3. ≥ `K_POST` of its sampled pages have htmldate `>= 2022-11-30`.

All three gates apply independently. Use `cleaned_bino_score` (cc10k) as
the score column, matching `report_imc2026_cutoff_switch_stats.py`.
Default `K_PRE = K_POST = 4`. Sensitivity sweep `{4, 5, 8, 10}` for the
per-side floors; the 15-page total floor is fixed.

`COHORT_N` = number of qualifying sites. This is the denominator for
all prevalence claims and is comparable across paper sections that use
the same 15-page-qualified population.

## Cohort and tier breakdown by site-level LLM classification

For `COHORT_N`, `TIER_A_N`, `TIER_B_N`, and `TIER_AB_N`, additionally
report the split between site-level LLM-dominant and non-LLM-dominant
sites (the SVM-based site classification used elsewhere in the paper).
Emit:
- `*_LLM_N`: count of sites within the cohort/tier classified as
  LLM-dominant.
- `*_NON_LLM_N`: count classified as non-LLM-dominant.

(SVM distance / sureness is intentionally NOT reported — paper has no
space for it.)

Rationale: a Tier A site that is also classified as LLM-dominant is
the strongest claim ("transitioned, and now site-level dominated by
LLM content"). A Tier A site classified as non-LLM-dominant means the
site shifted but is not yet majority-LLM. Both are interesting; the
paper may pick whichever subset.

## Tier A — Non-overlap (strict, threshold-free)

For each cohort site:

- `pre_scores`  = Binoculars scores of pages with date `< 2022-11-30`
- `post_scores` = Binoculars scores of pages with date `>= 2022-11-30`

Tier A iff `min(pre_scores) > max(post_scores)`
(Binoculars convention: lower score ⇒ more LLM-like).
Every pre-launch page on the site scores higher than every post-launch
page. No threshold; the score scale is the site's own.

Outputs:
- `TIER_A_N`
- `TIER_A_SHARE_PCT` = `TIER_A_N / COHORT_N × 100`
- `TIER_A_MEDIAN_FIRST_POST_DATE`
  (median across Tier A sites of the first post-launch page's date).

## Tier B — Mean-shift (looser, captures noise-eaten transitions)

Tier B iff a site is in cohort, **not** in Tier A, and
`mean(pre_scores) - mean(post_scores) >= DELTA`.

`DELTA` calibrated by sensitivity sweep `{0.0, 0.25, 0.5, 0.75, 1.0, 1.5}`.
Pick the `DELTA` where the count vs. `DELTA` curve plateaus before noise
dominates; if no clear plateau, default to `0.5` (≈ half a Binoculars
score unit).

Outputs:
- `TIER_B_N` (at default `DELTA`)
- `TIER_B_SHARE_PCT`
- `TIER_AB_N` = `TIER_A_N + TIER_B_N` (disjoint by construction)
- `TIER_AB_SHARE_PCT`
- Sensitivity table TSV: rows `K`, columns `DELTA`, cells `(TIER_A_N, TIER_B_N)`.

## Sanity checks

- `TIER_A_N` should be `<` prior `CUTOFF_CC10K_COMPLETE_N` (619).
  Non-overlap is strictly stricter than "all pre-non-LLM pages predate
  first LLM page". The 619 baseline already used the 15-page-qualified
  population, so apples-to-apples once the floor is added.
- `TIER_A_LLM_N + TIER_A_NON_LLM_N` should equal `TIER_A_N`
  (every cohort site has a site-level classification).
- `TIER_A_MEDIAN_FIRST_POST_DATE` should fall in 2023 (consistent with
  prior median 2023-08-20).
- For 3 random Tier A sites, manually inspect 2 pre-launch pages and 2
  post-launch pages to confirm the score gap reflects visible writing-style
  difference, not classifier artifact. Spot-check only; not the headline
  validation (humans can't reliably label LLM text, so no bulk labeling).

## Visual: 3-site scatter

Pick 3 sites that span the rigor spectrum:
- Site 1: Tier A, large gap `min(pre) − max(post)`.
- Site 2: Tier A, narrow gap.
- Site 3: Tier B-only.

Plot:
- X = page publication date (htmldate)
- Y = raw Binoculars score
- 3 marker shapes (circle / square / triangle), one per site
- Site names in the legend
- Horizontal line at `0.9015` (max-F1 threshold);
  region above labeled "Human-like", below labeled "LLM-like"
- Vertical line at 2022-11-30 labeled "ChatGPT launch"

Save to `data/classify/imc2026_temporal_transition_v2/transition_3site.pdf`
and copy to the paper figure path used by `sync_dw1_paper_figures.py`.

## TeX macros to emit (via stats.txt KEY=VALUE)

Mirror the existing `CUTOFF_*` macro pattern in
`sync_dw1_paper_figures.py`:
- `TIER_COHORT_N`, `TIER_COHORT_LLM_N`, `TIER_COHORT_NON_LLM_N`
- `TIER_A_N`, `TIER_A_SHARE_PCT`,
  `TIER_A_LLM_N`, `TIER_A_NON_LLM_N`,
  `TIER_A_MEDIAN_FIRST_POST_DATE`
- `TIER_B_N`, `TIER_B_SHARE_PCT`,
  `TIER_B_LLM_N`, `TIER_B_NON_LLM_N`
- `TIER_AB_N`, `TIER_AB_SHARE_PCT`,
  `TIER_AB_LLM_N`, `TIER_AB_NON_LLM_N`
- `TIER_K_PRE`, `TIER_K_POST`, `TIER_DELTA`,
  `TIER_N_PAGES_MIN` (= 15)

## Implementation notes

- Reference: `imc2026stats/report_imc2026_cutoff_switch_stats.py` for
  DuckDB session pattern and stats.txt emission. Drop the null-model
  block.
- Output dir: `data/classify/imc2026_temporal_transition_v2/`.
- New script: `imc2026stats/report_imc2026_temporal_transition_v2.py`.
- Companion doc: `imc2026stats/report_imc2026_temporal_transition_v2.md`
  describing what the script does, key decisions, control flow, output
  keys (style of existing report_*.md files in that directory).

## Out of scope

- Site1000 / Webis datasets. Paper claim is CC-only.
- Shuffle null model.
- GMM (approach 1) and SVM-shift (approach 3) revisits.
- Multiple-testing correction (no per-site p-values in this design).
- Bulk human labeling of pages (humans can't reliably label LLM text).

## Decisions to flag back to user

- If `COHORT_N` is too small (e.g., < 1,000), the prevalence claim
  weakens; surface this for re-scoping.
- If `TIER_A_N` is much smaller than expected (e.g., < 50), report and
  ask whether to relax `K_PRE/K_POST` or accept the lower number.
- If `DELTA` sensitivity has no clear plateau, report and ask.
