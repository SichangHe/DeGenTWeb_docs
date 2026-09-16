# fixed-frame 2014 filter-effect evaluation
(authored by agents unless marked 🧑)

- purpose
  - measure page-filter survival on one fixed 10,000-site 2014 Common Crawl frame
  - retain sites that later fail a stage
- fixed frame
  - original deterministic pre-filter 10,000-site cohort
  - reconstructed with its audit and site-identity hash
  - sites are never replaced, including sites now below 15 current pages
- filter stages
  - extraction
  - Dolma record
  - Dolma pass
  - token minimum
  - duplicate limit
  - real Binoculars score
- outcomes
  - report current-snapshot survival and abstention separately at every stage
  - report filtered-pipeline FPR only among sites with 15 filtered scored pages
  - report sites with fewer than 15 current successful pages as source-stage abstentions
  - mark an exact same-page no-filter comparison unavailable: the old artifact has a page-key hash but not page identities, and current real scores exist only for filtered pages
  - do not interpret the conditional FPR as a causal effect of filtering
- test limitation
  - `tests/test_expand_old_cc_2014.py` cannot collect without optional `types_aiobotocore_s3`
- implementation
  - SQL: `src/degentweb/sql/queries/old_cc_2014_filter_effect.sql`
  - runner: `src/degentweb/classifying/evaluate_old_cc_2014_filter_effect.py`
