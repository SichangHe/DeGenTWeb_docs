# Dolma Deduplication Study

Scope: source-995 asks whether to remove DeGenTWeb's CDC 50% duplicate-rate
gate and wholesale adopt Dolma cleaning and deduplication, apart from the
separate token-repetition choice. This is a read-only study, not a design or
implementation decision.

## Recommendation

Do not remove the CDC gate or wholesale copy Dolma now. Dolma is useful prior
art and a good source of candidate components, but its public pipeline is for
static language-model pretraining. DeGenTWeb selects page text for a
generated-text detector. Its outcome is detector false-positive behaviour,
not language-model training quality.

Copying a named recipe would make the method easier to describe, but would not
eliminate the need to state the recipe, its corpus scope, and its observed
effect on this detector. It would also replace a site-local incremental method
with a global, probabilistic corpus method. That is a material methodological
change, not merely a better explanation of the same method.

Keep the current gate until a measured replacement is available. If the goal
is a simpler, externally specified policy, evaluate an adapted Dolma-style
deduplication policy alongside the current gate before choosing one. Treat
token repetition separately: it is an intra-document quality rule, not
cross-document deduplication. The phrase "except for token repetition" is
ambiguous about retaining or omitting that rule; either choice needs its own
evidence.

## What the current rule does

`MAX_PCENT_DUPE` is 50%, documented as "At most 50% of text should be
duplicate from other pages" in
[`classifying/__init__.py`](../src/degentweb/classifying/__init__.py). For each
content-defined byte chunk, the active code checks membership in a mutable set
for the subdomain, adds unseen chunks immediately, and divides seen chunk bytes
by the raw extraction length in
[`run_all_client.py`](../src/degentweb/classifying/run_all_client.py). Thus it
is a page-rejection rule, scoped to a subdomain and processing order. It also
counts a chunk repeated later in the same page after its first occurrence.

The normal current scoring path calculates that rate on the raw extraction,
then runs the in-project Dolma-derived quality cleaner and applies both the
cleaned-token threshold and the 50% rate. See
[`run_all_client.py`](../src/degentweb/classifying/run_all_client.py) and
[`dolma_filter.py`](../src/degentweb/classifying/dolma_filter.py). The project
therefore already adopts C4 NoPunc and Gopher-style rules in part; it does not
use the Dolma toolkit's deduper.

The historical recalculation orders pages by subdomain and crawl time, then
resets its chunk set per subdomain in
[`classifying.sql`](../src/degentweb/sql/queries/classifying.sql) and
[`all_dupe_rate.py`](../src/degentweb/classifying/all_dupe_rate.py). A project
binding describes these chunks as "sized around 64 bytes" in
[`degentweb_rs2`](../DeGenTWeb_rs2/python/degentweb_rs2/__init__.py). This
conflicts with the old 96-byte target statement in
[`filter_non_article.md`](filter_non_article.md), so the current implementation
rather than that prose should govern any future comparison.

## What Dolma does

The cloned primary source is `/ssd1/sichanghe/allenai--dolma` at commit
`669f534823b08d266a8fff01f8a1c916a5a56576`. Its toolkit describes separate
tagging, optional deduplication, mixing, and tokenization in
[`docs/README.md`](/ssd1/sichanghe/allenai--dolma/docs/README.md).

Its deduper uses an in-memory Bloom filter and writes attributes rather than
immediately discarding text. It can mark an entire document duplicate from a
specified key, or mark duplicate newline-delimited paragraph spans. The docs
explicitly warn that the Bloom filter can have false positives:
[`docs/deduplication.md`](/ssd1/sichanghe/allenai--dolma/docs/deduplication.md).
The v1.6 Common Crawl recipe deduplicates exact `$.text` documents with a
configured estimated corpus size and `1e-06` desired false-positive rate in
[`doc_dedupe/cc_en_head.yaml`](/ssd1/sichanghe/allenai--dolma/configs/dolma-v1_6/doc_dedupe/cc_en_head.yaml).
Its mixer removes duplicate documents but replaces duplicate paragraph spans
with empty text in
[`mixing/cc-head.yaml`](/ssd1/sichanghe/allenai--dolma/configs/dolma-v1_6/mixing/cc-head.yaml).

That production recipe also carries Gopher rules, PII and toxicity handling,
and a 100-or-more-token-repetition exclusion. Those are distinct selection
rules, not "deduplication." The same recipe lists all of them explicitly in
[`mixing/cc-head.yaml`](/ssd1/sichanghe/allenai--dolma/configs/dolma-v1_6/mixing/cc-head.yaml).

## Why one is not a substitute for the other

CDC asks whether this page's input is mostly repeated at this site. Dolma's
exact-document and paragraph policies seek corpus diversity while retaining
the nonduplicate remainder of a document. Neither source establishes that
switching between those policies improves a generated-text detector. A global
Bloom-filter job also requires a frozen corpus and a decision about retention
and ordering, whereas current crawling is incremental and database-backed.

## Evidence needed before a change

On a fixed, source-balanced extraction sample, compare:

1. the current default
2. the current default without CDC
3. adapted exact-document plus paragraph deduplication without CDC
4. adapted deduplication plus CDC

For every arm, retain page, bytes, subdomain, and unique-text coverage; manually
review only disagreement pages for article suitability; and measure the
detector's false-positive rate and calibration on existing labelled material.
Run the CDC arms in chronological and shuffled orders so any order dependence
is measured rather than mistaken for noise. A replacement is justified only if
it improves the detector-specific endpoint without unacceptable loss of
eligible-page or site coverage.

No implementation, scoring, crawling, or data change was made for this study.
