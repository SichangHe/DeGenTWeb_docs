# source-1103 B12 crawl

- input
  - accepted 120-page ledger at the hash embedded in `crawl_source1103_b12_ledger.py`
  - four B12 sites with 30 unique canonical URLs each
- execution
  - uses `browser_crawl_results` with forced current browser visits
  - records every ledger URL as usable, unusable, or failed
  - does not call the scorer or AWS
- usable
  - the browser visit succeeded
  - the returned HTML has a nonempty body
- output
  - create-only JSON binds the ledger hash, crawl interval, crawl IDs, and exact URL outcomes
