# Expanded Baseline Cohort Protocol

Status: frozen before model training or evaluation (`expanded-baseline-v1`).

This protocol covers the source-1067 baseline expansion. The separate primary
mixed-domain holdout of 10 AI-generated and 10 human sites is outside this
protocol: remove those sites first, and do not count them or their pages toward
any target below.

## Requirements and protocol decisions

Source-1067 requires 200 Wix and 200 B12 sites, approximately 10,000 human
negative samples, training on only one generator at a time, tests on unseen
samples from that generator, OOD tests, and OOD treatment of body swaps. It
also requires most sites of each type to be held out.

The following numbers are protocol decisions needed to make those requirements
executable; they were not independently observed facts:

- company-human target: 200 sites and 5,000 eligible pages
- personal-human target: 200 sites and 5,000 eligible pages
- each human or generated site: 25 eligible pages
- each type: 40 development sites and 160 evaluation-reserved sites
- each 40-site development cohort: 32 fit sites and 8 validation sites
- each generator family: 160 negative and 160 positive body-swap sites
    - 25 pages per site, or 4,000 pages per label

Each 200-site target includes its 160 evaluation-reserved sites. The 5,000-page
target likewise includes 1,000 development and 4,000 evaluation-reserved pages.
Neither target includes any site or page from the primary mixed-domain holdout.

The resulting frozen inventory is:

- Wix/company: 200 sites and 5,000 generated pages
    - 40 development sites = 32 fit + 8 validation
    - 160 evaluation-reserved sites
- company-human: 200 sites and 5,000 natural negative pages
    - 40 development sites = 32 fit + 8 validation
    - 160 evaluation-reserved sites
- B12/personal: 200 sites and 5,000 generated pages
    - 40 development sites = 32 fit + 8 validation
    - 160 evaluation-reserved sites
- personal-human: 200 sites and 5,000 natural negative pages
    - 40 development sites = 32 fit + 8 validation
    - 160 evaluation-reserved sites

For this protocol, the 10,000-negative-sample target means natural human class-0
pages: 5,000 company-human plus 5,000 personal-human. This interpretation is a
protocol decision because source-1067 does not define the negative-sample unit.
Body-swapped negatives are additional OOD samples and do not count toward it.

## Freeze procedure

Freeze sites before selecting pages or running experiments.

1. Remove every primary mixed-domain holdout site and all of its derivatives.
2. Snapshot the complete candidate inventory before applying eligibility rules.
   Record its content digest, retrieval time, source identity, canonical IDs,
   and generator-to-human-source mapping. This immutable snapshot is the only
   candidate universe for this protocol version.
3. Build two lists of matched site families. Each Wix/company family contains
   one Wix site and its company-human source; each B12/personal family contains
   one B12 site and its personal-human source. Redirects, aliases, mirrors, and
   derivatives retain the same canonical family ID.
4. Apply one frozen page-eligibility pipeline to human and generated sites. For
   every candidate site with at least 25 passing pages, order its pages by the
   128-bit BLAKE2b digest of the UTF-8 canonical JSON array
   `["expanded-baseline-v1", <canonical-site-id>, <canonical-page-id>]` and
   provisionally retain the first 25. Before family selection, rank-pair those
   provisional pages and run the frozen validation for all 50 reciprocal swap
   outputs defined below. A family is eligible only if both sites have 25
   provisional pages and every swap passes. The cohort manifest must record the
   Git commit and code path implementing every extraction and filter step, the
   exact serialized configuration and its SHA-256 digest, the dependency-lock
   digest, and all exclusion reasons. The prose overview is in
   [`filter_non_article.md`](filter_non_article.md).
5. Order every eligible family by the 128-bit BLAKE2b digest of the UTF-8
   canonical JSON array
   `["expanded-baseline-v1", <direction>, <canonical-family-id>]`, where
   `<direction>` is exactly `wix-company` or `b12-personal`. Break a digest tie
   by canonical family ID. Select the first 200; do not inspect outcomes or
   hand-pick among eligible families. Assign both sites in the first 40
   selected families to development and both sites in the remaining 160 to
   evaluation-reserved. Within development, assign the first 32 to fitting and
   the next 8 to validation.
6. Promote each selected site's 25 provisional pages into the frozen page
   manifest. Every page, reciprocal swap, and derivative inherits its site
   family's partition. Discard provisional artifacts for unselected families.
7. Persist the candidate, cohort, and page manifests with canonical IDs,
   exclusion reasons, digests, labels, partitions, and content snapshot IDs.
   Serialize each manifest with RFC 8785 JSON canonicalization and record its
   SHA-256 digest. Do not redraw a cohort after seeing results.

If an inventory cannot meet a frozen target, report the shortfall. Do not move
primary-holdout sites, substitute across types, or silently change the split.
Any amendment needs a new protocol version and a rationale recorded before
affected results are computed.

## Directional experiments

The split is global, but `same-generator` and `OOD` are relative to the model
being evaluated.

The natural OOD tests intentionally change generator and site type together.
They measure the requested Wix/company-to-B12/personal shift and its reverse;
they do not isolate generator shift from domain shift.

### Wix/company direction

- development: 40 Wix/company and 40 company-human sites
    - fitting: the first 32 matched families
    - validation: the next 8 matched families
- same-generator test: the 160 evaluation-reserved Wix/company sites against
  the 160 evaluation-reserved company-human sites
- natural OOD test: the 160 evaluation-reserved B12/personal sites against the
  160 evaluation-reserved personal-human sites
- transformed OOD test: every body-swap cohort, reported separately

### B12/personal direction

- development: 40 B12/personal and 40 personal-human sites
    - fitting: the first 32 matched families
    - validation: the next 8 matched families
- same-generator test: the 160 evaluation-reserved B12/personal sites against
  the 160 evaluation-reserved personal-human sites
- natural OOD test: the 160 evaluation-reserved Wix/company sites against the
  160 evaluation-reserved company-human sites
- transformed OOD test: every body-swap cohort, reported separately

The scoring unit is one site. Score each of its 25 frozen pages, then represent
the site by the nine page-score percentiles from 10% through 90%. The site model
emits one binary prediction from that vector. Report site-level confusion
counts and metrics separately for same-generator, natural-OOD, and
body-swap-OOD cohorts; do not pool them into one headline metric.

The feature vector and selection rule are frozen as follows:

1. Do not select or transform features beyond the nine percentiles above.
2. On the 32 fit families, fit one linear `sklearn.svm.SVC` per
   `C` in `[0.01, 0.1, 1, 10, 100, 1000, 1000000]`, with `kernel="linear"`,
   `class_weight=None`, `probability=False`, and `random_state=42`. Record the
   exact scikit-learn and dependency-lock versions.
3. For each fitted model, score the 16 validation sites. Its threshold
   candidates are negative infinity, positive infinity, and every distinct
   validation decision score. Predict label `1` exactly when score is greater
   than or equal to the threshold.
4. Select the `(C, threshold)` pair with greatest validation balanced accuracy,
   defined as the unweighted mean of label-0 and label-1 recall. Break a tie by
   smaller `C`, then smaller absolute threshold, then smaller threshold.
5. Freeze the selected model fitted only on the 32 fit families and its selected
   threshold. Do not refit on validation families or change any choice after
   opening an evaluation cohort.

No evaluation-reserved site may be used for fitting, threshold selection,
feature selection, prompt revision, early stopping, or model selection.

## Body swaps

Every body swap is OOD, regardless of which generator, human source, body, or
site shell supplied its components. Body swaps are never training data, never
part of a same-generator test, and never part of the 400 generated-site or
10,000 human-negative targets.

The body-swap population and labels are protocol decisions, not source-1067
facts. For each of the 160 evaluation-reserved families in each direction,
pair the human and generated pages by their frozen page-selection rank from 1
through 25. Build exactly two reciprocal swap sites:

- negative swap, label `0`: human page bodies in the matched generated shell
- positive swap, label `1`: generated page bodies in the matched human shell

This yields, separately for Wix/company and B12/personal, 160 negative swap
sites and 160 positive swap sites, with 4,000 pages per label. Do not construct
cross-family swaps or use development components. A compatible swap must
preserve the donor's frozen main-body bytes and replace the recipient's main
body without retaining recipient-body text; reject the entire candidate family
if any of its 50 reciprocal pages cannot satisfy those checks.

Before cohort selection, freeze the swap implementation's Git commit, code
path, serialized configuration, configuration SHA-256 digest, and dependency-
lock digest. The body-swap manifest records every direction, family, page rank,
donor page and body hash, shell page and shell hash, output page hash, label,
and validation result. Canonicalize and hash it by the same rule as the cohort
manifests. Apply the same 25-page site aggregation and report each generator
family and swap orientation separately.
