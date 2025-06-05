# Common Crawl Dataset

## Common Crawl index

### Formats

path file e.g.:
https://data.commoncrawl.org/crawl-data/CC-MAIN-2025-18/cc-index.paths.gz

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

**filtering:** `mime` is `text/html`, `status` is `200`, `languages`
contains `eng`.

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
- \~230GB of index files under each path file, \~10.1TB total (too much)
- assume 5% entries left after filtering, 17% compression rate after index
    - ⇒ \~14.9GB per path file, \~657GB total (managable)
- only keep 2000 entries per subdomain, ⇒ est. \<10% size, \<66GB (very fine)
    - throw away existing entries w/ largest BLAKE3 64bit hash number
