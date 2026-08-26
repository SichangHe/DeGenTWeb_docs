# Expanded Baseline Cohort Protocol

Status: corrected protocol specification (`expanded-baseline-v2`). No cohort,
body-swap output, fitted model, or result is claimed here.

This version supersedes the withdrawn `expanded-baseline-v1` reciprocal-swap
design, which did not implement the intended negative-sample transformation.

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
- each human type: attempt 160 body-swapped negative sites
    - 25 pages per site, or 4,000 attempted transformed OOD pages
    - usable totals may be lower and must be reported as attrition

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
3. Freeze the body-swap prompt and generation configuration specified below,
   but do not generate text. This prevents cohort outcomes from influencing the
   configuration and generation outcomes from influencing natural cohorts.
4. Build two lists of matched site families. Each Wix/company family contains
   one Wix site and its company-human source; each B12/personal family contains
   one B12 site and its personal-human source. Redirects, aliases, mirrors, and
   derivatives retain the same canonical family ID.
5. Apply one frozen page-eligibility pipeline to natural human and generated
   sites. For every candidate site with at least 25 passing pages, order its
   pages by the
   128-bit BLAKE2b digest of the UTF-8 canonical JSON array
   `["expanded-baseline-v2", <canonical-site-id>, <canonical-page-id>]` and
   provisionally retain the first 25. Body-swap generation and validation are
   not natural-cohort eligibility conditions. A family is eligible when both
   natural sites have 25 provisional pages. The cohort manifest
   must record the Git commit and code path implementing every extraction and
   filter step, the exact serialized configuration and its SHA-256 digest, the
   dependency-lock digest, and all exclusion reasons. The prose overview is in
   [`filter_non_article.md`](filter_non_article.md).
6. Order every eligible family by the 128-bit BLAKE2b digest of the UTF-8
   canonical JSON array
   `["expanded-baseline-v2", <direction>, <canonical-family-id>]`, where
   `<direction>` is exactly `wix-company` or `b12-personal`. Break a digest tie
   by canonical family ID. Select the first 200; do not inspect outcomes or
   hand-pick among eligible families. Assign both sites in the first 40
   selected families to development and both sites in the remaining 160 to
   evaluation-reserved. Within development, assign the first 32 to fitting and
   the next 8 to validation.
7. Promote each selected natural site's 25 provisional pages into the frozen
   page manifest. Discard provisional artifacts for unselected families.
8. Persist the candidate, cohort, and page manifests with canonical IDs,
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
body-swap-OOD cohorts; do not pool them into one headline metric. Body-swap-OOD
metrics use reference label `1` because the evaluated main-body text is LLM-
generated; they remain OOD metrics, not in-distribution accuracy.

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

## Body-swapped negative OOD cohort

A body-swapped negative starts from an eligible human negative page. Replace
that page's main body with LLM-generated text while preserving its human shell.
The transformed derivative is OOD. It is never training data, never part of a
same-generator test, and never part of the 400 generated-site or 10,000 natural-
negative targets. Do not place a human body in a generated shell, construct a
reciprocal orientation, or define this cohort by Wix or B12 provenance.

For each frozen page of every selected evaluation-reserved human site, submit
its frozen title and main body to the text-generation configuration. The exact
prompt template is:

```text
Rewrite the source text below into a standalone web-page main body. Preserve
its factual claims and language. Return only the replacement body text, with no
commentary.

Title: {{title}}
Source text:
{{main_body}}
```

Before natural-family selection, freeze the provider, immutable model
identifier, model revision when the provider exposes one, all request
parameters including any supported seed, a maximum of three attempts per page,
prompt bytes, implementation Git commit and code path, serialized configuration
and its SHA-256 digest, and dependency-lock digest. Record the complete request
and response bytes, provider request ID, attempt number, and retrieval time. If
the provider cannot identify the served model sufficiently for audit, report
that limitation; do not silently substitute a model. A remote provider may not
reproduce identical bytes, so accepted response bytes are frozen inputs to all
later steps.

Do not generate until natural cohorts, both directional models, and both
thresholds are frozen. Then generate only the 25 frozen pages of each selected
evaluation-reserved human site, in ascending site-selection and page-selection
rank. No development page is a generation input.

Construct each attempt canonically:

1. Decode the frozen source response with the frozen extractor's recorded
   charset decision. Parse and serialize it with the frozen HTML implementation
   as UTF-8. Record the implementation version, decoded-text hash, serialized-
   HTML hash, selected main-body element's selector, and its unique serialized
   inner-byte range. A missing, non-unique, or non-contiguous range fails the
   attempt.
2. Normalize the LLM response's line endings to LF and Unicode to NFC. Split on
   one or more blank lines, discard empty parts, HTML-escape `&`, `<`, and `>`
   in each part, wrap each part in `<p>` and `</p>`, and join paragraphs with a
   single LF. The resulting UTF-8 bytes are the replacement fragment.
3. Replace exactly the selected element's serialized inner-byte range. Every
   other serialized HTML byte remains unchanged. Preserve the effective URL and
   response headers, except remove `Content-Encoding` and `Transfer-Encoding`,
   set `Content-Type` to `text/html; charset=utf-8`, and recompute
   `Content-Length` from the constructed bytes. Record original and derivative
   URL/header/HTML bytes and their SHA-256 digests.
4. Run the complete frozen page-eligibility pipeline on the constructed full
   derivative with that URL and those headers. For duplicate comparison, treat
   the 25 derivatives as one synthetic site ordered by frozen page-selection
   rank; rank `r` is compared only with accepted derivatives at ranks below
   `r`, in ascending rank. Record the ordered comparison IDs, extracted-text
   hash, predicate results, and rejection reason for every attempt.

Accept the first passing attempt among at most three attempts for a page. If a
page has no passing attempt, record it as OOD attrition and continue attempting
later ranks. Do not redraw a family, substitute a page or site, change any
natural cohort, or revise the prompt, model, threshold, or generation settings.
These are protocol instructions, not a claim that generation or validation has
occurred.

Create one derivative page per accepted attempt. Its reference label is `1`
because its evaluated body is the recorded LLM response; `negative` describes
the natural source, not the derivative label. The derivative ID is the 128-bit
BLAKE2b digest of the UTF-8 canonical JSON array
`["expanded-baseline-v2", "body-swapped-negative",
<canonical-human-page-id>, <generation-response-sha256>]`. It inherits the
source site's partition but cannot replace or modify the source identity.

Attempt derivatives for the 160 evaluation-reserved human sites of each type:
4,000 pages per human type and 8,000 total. A site enters site-level scoring
only if all 25 derivatives pass; otherwise report its accepted-page count and
exclude it from nine-percentile aggregation. The body-swap manifest records the
source site and page IDs, page rank, partition, reference label, every original
and constructed artifact named above, generation request and response hashes,
provider receipt, attempt number, output hash, derivative ID, duplicate-
comparison order, every predicate result, and page/site attrition reason.
Canonicalize and hash it by the same rule as the cohort manifests. Report both
attempted and accepted page and complete-site counts; 4,000 pages and 160 sites
per human type are attempted maxima, not claimed completed totals.

Apply each frozen directional model and its already selected threshold to both
human-shell OOD cohorts. Report every model/cohort combination separately as an
OOD stress test. Because the transformation changes a natural negative's body
to generated text, `negative` describes the source sample, not a class label of
`0`; the derivative's reference label is `1`. Do not report these derivatives
as natural negatives or use them to estimate in-distribution accuracy.
