normal selector offline diagnosis

The live `deferred_dolma_cleaned` query first materializes latest rows across the full crawl and classification tables. Its no-execution production plan estimates scans of about 108 million crawls, 103 million crawl/classification links, 103 million classifications, 43 million filtered Dolma rows, and 20 million detector rows, followed by a large sort. This explains the prolonged `DataFileRead` wait without proving a deadlock.

`EXPLAIN` without `ANALYZE` gives the live query a total cost above 30 million. The bounded candidate query has startup/512-row cost `97.51..1162.66`; a two-ID batch has cost `4.97..24.06` and uses the existing latest-crawl and latest-classification indexes. `normal_selector_offline_evidence.json` freezes these observations and the schema/query identities used to make them; the validator fails closed if any identity changes. No new production index is required.

The offline replacement in `scripts/normal_selector_offline_plan.py` uses two phases:

- fetch at most 512 candidate `clasf_id` values by the existing pending-score predicates and the indexed primary-key order
- fetch those IDs and recheck both exact latest-row conditions before scoring

The second phase preserves the exact live semantics: latest crawl per `(page_id, crawl_src_id)`, including PostgreSQL's `DESC NULLS FIRST` timestamp ordering and the crawl-ID tie break; latest classification per crawl; Dolma/basic filters; and the live pending condition (`score_set_id IS NULL` or `bino_score = -1`). It does not alter production indexes, processes, or data. A read-only `dw_test` regression compares the replacement directly with the legacy `DISTINCT ON` result for null, tied, and ordinary timestamps. The `dw_test` candidate plan uses a bounded sort and point lookup into `detector_score_sets`; no production execution was used.

The exact-34 path stays separate because this artifact neither ingests its missing pages nor launches or modifies a scorer. The integrated runtime binds the reviewed URL manifest and excludes those 34 URLs at the selector boundary before creating score tasks; a deployment owner must revalidate that manifest identity and its source handoff, rather than relying on a broad crawl-source exclusion.

Deployment remains blocked on explicit authority and a clean committed staging revision, not on an index change. The integrated paged implementation uses the current six-field `UsefulScoreSet`, binds the exact-34 URL manifest, and requires the shared supervisor lease across normal launch paths. The supervisor executes the frozen plan/schema/evidence validator during preflight and pins that validator, evidence, migrations, and recursive runtime closure. A deployment owner must still prove one supervisor owns the scorer/Bino pair and current backends and obtain permission before replacing the live scorer. Scoring missing `implicit_reward_model` values remains separate work; adding that predicate without a writer would create an endless rescore loop.
