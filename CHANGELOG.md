# Changelog

## 2025-11-11

- finished DB migration & bulk Git history cleanup
- re-statted search result sites and observed filtering too strict

## 2025-10-07

- tried decision tree/forest for filtering; default settings high FPR;
    tree uninterpretable

## 2025-09-29

- removed TimescaleDB after confirming PostgreSQL handled compression

## 2025-09-18

- re-crawling Common Crawl 10k subdomains; many rejected as non-articles

## 2025-09-09

- DB migration blocked by TimescaleDB slowness until adding index and
    fixing chunking
- re-crawling Common Crawl 10k subdomains remains slow after filter
    adjustments but likely correct

## 2025-07-23

- recomputed incorrect Binoculars scores
- re-downloaded Common Crawl index for uniform sampling and
    filtered IP hostnames

## 2025-07-08

- analyzed Common Crawl 10k subdomains: lower %AI overall, more when
    crawled later
- quantized Falcon-7B to fp8 and improved dynamic batching for Binoculars
- SVMs need only 15 pages per site; Binoculars SVMs highly confident on
    baseline
- enabled CDC-based dedup per site, removed unused Common Crawl downloads

## 2025-06-24

- NLP researchers hinted worse Binocular results from new models are due to
    model being less similar to ChatGPT-3.5
- removed Playwright thread bottleneck and scaled task spawning by
    available resources
- set up SQLite concurrent writes and Rust+Python codebase for maintenance
- building Common Crawl index DB faced gzip issues, SSL errors, and
    rate limiting
- sampled subdomains with 10 concurrent downloads;
    observed CPU-bound extraction and subdomain completion stats
- filtered by duplication rate using CDC

## 2025-06-03

- fixed low-hanging non-article filtering issues
- sampled subdomains from Common Crawl for classification

## 2025-05-06

- completed per-site deduplication and additional filtering tweaks
- decided against moving extraction and ad counting into the browser

## 2025-04-29

- improved ad counting by counting only elements with content and
    considered ads-per-token metric
- debugged asyncio crawler issues; noted resource balancing contribution
- fixed false positive on www.w3docs.com by filtering code text

## 2025-04-15

- settled on decile-based feature vectors
- sampled subdomains via how-to queries to broaden coverage
- generated positive websites for baseline
- built website feature vector SVM with train/test split

## 2025-04-08

- surveyed website generator capabilities

## 2025-03-25

- expanded AI and human website datasets, including IndieWeb sources

## 2025-02-24

- confirmed high-score pages in low-score sites rarely good
- subdomain SVMs for statistical scoring
- reviewed blacklist matching, sites near threshold, and WHOIS checks

## 2025-02-11

- switched to Wayback Machine prefix search instead of recursive crawling
