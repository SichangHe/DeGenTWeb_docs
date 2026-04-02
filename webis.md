# Webis-PSERP-24 S3 Dataset

- Set access key & secret under AWS CLI `webis` profile
- Needed `aws configure set profile.webis.s3.addressing_style virtual`

## Metadata index

96 top-level prefixes contain delimited by date & search engine, e.g.
`2022-08-24-startpage/`:

```sh
aws s3api list-objects-v2 \
  --profile webis \
  --endpoint-url https://s3.data.webis.de \
  --bucket corpus-webis-pserp-full-24 \
  --delimiter "/" \
  --query "CommonPrefixes[].Prefix" \
  --output json > data/webis/top-prefixes.json
```

Per-prefix JSONL files (96 total) in `data/webis/prefix-index/` from
running `src/degentweb/webis/data_index.py`, each w/ something like:

```json
{"Key": "2022-08-24-startpage/gpc/results-crawl/part-0/query-0.tar.xz", "LastModified": "2026-01-20T16:08:43.101000+00:00", "ETag": "\"56dc2ba638449ab2c285481ffa89e7e5\"", "Size": 95760708, "StorageClass": "STANDARD"}
{"Key": "2022-08-24-startpage/gpt/results.jsonl", "LastModified": "2026-01-20T22:27:19.315000+00:00", "ETag": "\"d997b2630237a73837b0b5590c9a78f9\"", "Size": 36128966, "StorageClass": "STANDARD"}
```

- `gpc` (GS1 Global Product Classification), or `gpt`
    (Google Product Taxonomy)
- `LastModified` is useless bc it's just upload time
- `StorageClass` is always `STANDARD`

## Example content

Each line of `results.jsonl` contains:

```json
{"query": "string", "results": [{"title": "string", "url": "full_url_string", "snippet": "string"}, …]}
```

Each `query-N.tar.xz` contains `query-N/`, which contains `hit-0` thru `hit-19`
(may not be exactly 19?) and `query.txt`

- `query.txt` contains the query string, which should match the `query` of
    a `results.jsonl` line
- `hit-N` contains `browser.json` `config.json` `id.txt` `snapshot/`
- (useless) `browser.json`: `{"viewport":{"width":1280,"height":720}}`
- (useless) `config.json`:
    `{"viewportAdjust":{},"snapshot":{"screenshot":{"timeout":120000}},"url":"…"}`
- (useless) `id.txt`: 28-byte hash string
- `snapshot/` contains `archive.warc.gz` `dom.html` `nodes.jsonl`
    `screenshot.png` `viewport.json`
- `archive.warc.gz`: WARC archive
- `dom.html`: rendered HTML
- `nodes.jsonl`: all DOM nodes, each line like
    `{"xPath":"/HTML[1]/BODY[1]","visible":true,"classes":[…],"position":{…},"text":"…","attributes":{…},"css":{…}}`
- `screenshot.png`: rendered page whole-page screenshot
- `viewport.json`:
    indicate page dimensions `{"x":0,"y":0,"width":1280,"height":10851}`

## Current decisions

- Keep Webis downloads on normal file paths via AWS CLI `s3 cp`;
    fd/stdout variants triggered 403/throughput regressions.
- Download all `results.jsonl`; they are cheap and
    give full query/result metadata.
- Do not download all crawl tars; choose tars from `results.jsonl` by
    subdomain page deficit.
- Target about 15 pages per subdomain; use existing stored pages first to
    avoid imbalance.
- `query-N.tar.xz` is matched to line `N` of
    the corresponding `results.jsonl`; use that to map pages/subdomains to
    tar keys.
- Some `results.jsonl` objects listed in prefix-index currently 403;
    selective mode continues with accessible metadata only.
- New Webis crawls should use crawl source `webis`, not `search_result`.
- Live DB still has historical Webis rows labeled `search_result`;
    migrate/backfill that data source separately.

## ChatNoir timestamp caveat

ChatNoir rows can look like they have "wrong" timestamps compared to
`startpage`/`ddg`/`bing`.

- Author note "ChatNoir is based on ClueWeb22"
- ClueWeb22 is a dataset released on 2022.
    The 10 billion web pages were sampled from
    the Bing search index during the first half of 2022

Current project rule:

- Hardcode ChatNoir `search_results.search_timestamp` to `2022-07-01`.
- Do not use S3 `LastModified` or WARC-derived timestamps for
    ChatNoir search timestamp semantics.

## Reliable query-source split: WikiHow vs Webis/non-WikiHow

Do not treat `search_query_hashes` as WikiHow-only.
It is shared by both WikiHow and Webis ingest paths.

Canonical distinction:

- **WikiHow query**: matching row exists in `wikihow_articles` for the same
    `search_query_id`.
- **Non-WikiHow query**: no matching `wikihow_articles` row.

Reference SQL pattern:

```sql
SELECT
  sr.search_result_id,
  se.search_engine_name,
  CASE
    WHEN EXISTS (
      SELECT 1
      FROM wikihow_articles wa
      WHERE wa.search_query_id = sr.search_query_id
    ) THEN 'wikihow'
    ELSE 'non_wikihow'
  END AS query_source
FROM search_results sr
JOIN search_engines se USING (search_engine_id);
```

If you specifically want **Webis-like** rows, combine non-WikiHow with
engine and crawl-source checks (for example `crawl_src_name='webis'` via
`search_results -> links -> crawls -> crawl_sources`).
