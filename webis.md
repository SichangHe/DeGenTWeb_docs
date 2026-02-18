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
