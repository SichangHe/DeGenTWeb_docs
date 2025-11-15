# Common Crawl Dataset

## Common Crawl index

### Formats

path file e.g.:
https://data.commoncrawl.org/crawl-data/CC-MAIN-2025-18/cc-index.paths.gz

line in path file e.g.:

```
cc-index/collections/CC-MAIN-2025-21/indexes/cdx-00022.gz
```

index file e.g.:
https://data.commoncrawl.org/cc-index/collections/CC-MAIN-2025-21/indexes/cdx-00002.gz

line in index file e.g. Languages are `,`-separated, English is `eng`:

```json
ar,com,fusionbikes)/producto/luz-knog-blinder-mini-niner 20250512054001 {"url": "https://fusionbikes.com.ar/producto/luz-knog-blinder-mini-niner/", "mime": "text/html", "mime-detected": "text/html", "status": "200", "digest": "ZA6MPPJEFGZ53KWFSLWMF7NDO7RKOWR4", "length": "78501", "offset": "243658810", "filename": "crawl-data/CC-MAIN-2025-21/segments/1746990412231.65/warc/CC-MAIN-20250512042640-20250512072640-00410.warc.gz", "charset": "UTF-8", "languages": "spa"}
```
line in index file with redirect:

```json
ar,com,futbolinterior)/component/mailto?link=b2449dac9dd9dbc27fe2d9f8c9dfc250a10eb664&template=shaper_helix3&tmpl=component 20250516140105 {"url": "http://futbolinterior.com.ar/component/mailto/?tmpl=component&template=shaper_helix3&link=b2449dac9dd9dbc27fe2d9f8c9dfc250a10eb664", "mime": "text/html", "mime-detected": "text/html", "status": "301", "digest": "OQ3OBNFR7DBCFQ4ANGEQW5P2FOXZZJRA", "length": "1103", "offset": "391196", "filename": "crawl-data/CC-MAIN-2025-21/segments/1746990412530.66/crawldiagnostics/CC-MAIN-20250516130253-20250516160253-00626.warc.gz", "redirect": "https://futbolinterior.com.ar/component/mailto/?tmpl=component&template=shaper_helix3&link=b2449dac9dd9dbc27fe2d9f8c9dfc250a10eb664"}
```

**filtering:** `mime` is `text/html`, `status` is `2xx`, `languages` is `eng`.

**ideal compression** (468B → \~80B for this file, \~17%):

```csv
subdomain,path,length,offset,filename
fusionbikes.com.ar,producto/luz-knog-blinder-mini-niner/,20250512054001,78501,243658810,CC-MAIN-2025-21/segments/1746990412231.65/warc/CC-MAIN-20250512042640-20250512072640-00410.warc.gz
# after storing subdomain and filename in other tables, 68 bytes for this entry
4B, producto/luz-knog-blinder-mini-niner/,20250512054001,4B, 4B,  4B
```

### Size and storage estimate

- 44 path files from 2020 to May 2025 (very small)
- \~301 index files per path, \~783MB per file, \~5.8GB uncompressed
    - \~13244 index files
- \~230GB of index files under each path file, \~10.1TB total (too much)
- assume 5% entries left after filtering, 17% compression rate after index
    - ⇒ \~14.9GB per path file, \~657GB total (managable)
- only keep 2000 entries per subdomain, ⇒ est. \<10% size, \<66GB (very fine)
    - throw away existing entries w/ largest BLAKE3 signed 64bit hash number
    - wrong estimate; actually much larger
- only sample index files w/ 1/32 probability
    - 589 index files
        - 166 from `cc-index/collections/CC-MAIN-2025-21/` because
            did not filter that path file when started crawling
    - only sample index files w/ 0-based line number (in path file) that
        is fully divided by 32
- 36192326 subdomains
    - only 153233 have 2000 records

### Implementation

- Common Crawl use blocked gzip
- batch insertion to avoid slow
- SSL errors; Common Crawl 1MiB/s rate limiting

## Sampling & classification

`common_crawl/classify10k.py`

- sample 10,000 subdomain from all index files
- 2.16%~4.30%~9.30% subdomains classified as AI-dominant,
    much lower compared to search results
- increasing %AI if segment by starting `crawled_at` year
- 10 concurrent downloads, CPU-bound by extraction
