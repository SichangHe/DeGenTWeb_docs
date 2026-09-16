# fixed-frame 2014 filter-effect evaluation
(authored by agents unless marked 🧑)

- purpose
  - measure page-filter survival on one fixed 10,000-site 2014 Common Crawl frame
  - retain sites that later fail a stage
- fixed frame
  - first 10,000 sites with at least 15 successful latest old-source pages
  - ordered by `subdomain64blake3`, then `subdomain_id`
  - fail closed if live pages no longer reproduce the 15-page prerequisite
- filter stages
  - extraction
  - Dolma record
  - Dolma pass
  - token minimum
  - duplicate limit
  - real Binoculars score
- outcomes
  - report survival and abstention separately
  - report filtered-pipeline FPR only among sites with 15 filtered scored pages
  - mark a no-filter outcome comparison unavailable when raw scores exist only for filtered pages
- test limitation
  - `tests/test_expand_old_cc_2014.py` cannot collect without optional `types_aiobotocore_s3`
- implementation
  - SQL: `src/degentweb/sql/queries/old_cc_2014_filter_effect.sql`
  - runner: `src/degentweb/classifying/evaluate_old_cc_2014_filter_effect.py`
