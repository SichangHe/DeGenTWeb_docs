# Interpreting CDC-Based Site Exclusions

Scope: source-999 asks how to justify removing sites whose crawled pages have
more than 50% CDC-measured duplication. This is an interpretation and
reporting note. It does not change the filter or any cohort.

## Defensible claim

Do not claim that a removed site is low quality, generated, useless, or
entirely boilerplate. The present filter does not establish any of those
claims.

The defensible statement is:

> We restricted the site-level analysis to sites with enough pages whose raw
> extracted text was not mostly already present in the same subdomain under the
> pre-specified CDC procedure. Sites with too few such pages were not eligible
> for a multi-page, site-level estimate. This is an eligibility restriction,
> not a finding about authorship, value, or the whole site.

This follows directly from the code. `MAX_PCENT_DUPE` is 50% and is documented
as "At most 50% of text should be duplicate from other pages" in
[`classifying/__init__.py`](../src/degentweb/classifying/__init__.py). The
filter applies that condition to each classification in
[`pg/db.py`](../src/degentweb/pg/db.py), while site selection counts only pages
that pass it in
[`classifying.sql`](../src/degentweb/sql/queries/classifying.sql).

The motivation is measurement independence, not a moral or authorship
judgment. The project documents that generated-text detectors can have high
false-positive rates on non-article material such as link lists, dashboards,
and product charts in [`filter_non_article.md`](filter_non_article.md). A
site-level distribution made mostly of repeated templates would overweight one
text layer and provide too little independent evidence about the site.

## Required limits

The current metric is not a direct boilerplate measurement. It iterates
content-defined byte chunks, adds an unseen chunk to a mutable subdomain set,
and counts a seen chunk's bytes in the duplicate numerator in
[`run_all_client.py`](../src/degentweb/classifying/run_all_client.py). Therefore
the result is:

- relative to other processed text in that subdomain, rather than to the web
- dependent on the existing chunk set and processing order
- able to count repeated text within the current extraction after its first
  occurrence
- calculated before Dolma cleaning in the normal path

Consequently, do not say that a specific percentage is the template share of a
site, that all pages are templated, or that removed sites would bias results in
a known direction. The threshold is a heuristic eligibility rule. The current
implementation gives no universal empirical calibration for 50%.

## How to report a removed site

For each cohort, publish or retain an exclusion table with the exact site
identity, number of crawled pages, number passing the other filters, number
failing only the CDC condition, number retained, and the frozen crawl/order
used. State whether the site missed the cohort's required number of eligible
pages. Do not collapse these into a qualitative label such as "templated."

The companion sensitivity analysis should rerun the same frozen cohort with:

1. the current CDC rule
2. no CDC rule
3. an adapted exact-document plus paragraph deduplication policy

Report site retention, page retention, unique-text retention, and the
detector's relevant false-positive/calibration outcome. Only this analysis can
support a claim that excluding these sites improves the intended measurement.

## Implication for the proposed Dolma change

Removing CDC merely to avoid explaining exclusions is not defensible. Every
deduplication policy creates an inclusion boundary that must be specified. The
right simplification is to use a clearly defined and evaluated policy, then
describe it accurately. The study in
[`dolma_dedup_study_20260824.md`](dolma_dedup_study_20260824.md) explains why
Dolma's global document/paragraph deduplication is not automatically an
equivalent replacement.

The low-prominence decision record
[`notes/rejected_dedup_alternatives.md`](notes/rejected_dedup_alternatives.md)
briefly records why MinHash, embedding, and DCLM/BFF-style alternatives were
considered but not adopted.

No filter, data, scoring, crawling, or cohort was changed.
