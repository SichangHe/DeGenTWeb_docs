## 2026-03-31

- site-level comments not yet recorded elsewhere:
    - `firsttimedogmom.com`: appears AI-like, has 2023 comments, modified 2025
    - `tips.simplygoodstuff.com`: published 2007, modified 2024
    - `www.greenemath.com`: possible false positive; generic math-teaching pages with YouTube-style descriptions
- after removing no-H1 pages, little H1-level separation remained between Bing LLM and human sites
- feature ideas not yet tracked in feature files:
    - heading-count distribution by level and markup ratio
    - word-frequency features for explainability
- ops/dev incidents not previously logged:
    - missing logging for failures before HTTP request starts
    - year-long bug where forked subprocesses did not share memory correctly
    - CC local-fetch bottleneck from EC2 workers stealing work
    - EC2 clients crashing on disconnect

## 2026-03-23

- TODO: revisit older spam-account literature for framing:
    - UCSD Click Trajectory email-spam work
    - SybilGuard-style spam-account work
- corrected assumption that 100k crawl had completed; rerun initiated
- data-analysis incidents not previously documented:
    - OOM in Pandas path -> DuckDB switch -> DuckDB segfault -> fix
    - cached DuckDB tables on disk for faster reloads
- page-feature release references:
    - `https://github.com/SichangHe/DeGenTWeb_docs/releases/tag/data-20260323-cc-page-feat`
    - `https://github.com/SichangHe/DeGenTWeb_docs/releases/tag/data-20260323-search-page-feat`
- implementation workflow details:
    - LLM categorization seed categories/descriptions created
    - workflow: sample page -> LLM picks/proposes category -> pause for human review when category is new
- pending analysis TODOs:
    - inspect most-different plots/pages
    - compare Webis first vs last tar slices

## 2026-03-03

- Exxact outage impact details:
    - no DB access prevented analysis work
    - about 3TB estimated for another DB instance from backup
- follow-up TODOs:
    - CDFs for all metric pairs
    - write 6-page version and literature review update
    - create dump of all surely-LLM sites for Calvin

## 2026-02-24

- sampling-scale details:
    - about 70k total sampled subdomains at this point
    - some search terms appeared to trigger more LLM-site results
- review-process note:
    - manual review of selected boundary sites was pending
- infra/task detail not yet in execution notes:
    - TODO: run Binoculars with NVFP4 on AWS 6000 Blackwell (half done)

## 2026-02-17

- experimentation/cost notes:
    - OpenCode/OpenClaw required heavy token budgets
    - AWS Bedrock experiment incurred immediate cost (~$40)
    - OpenClaw failed to launch headless browser; Browser Use CLI worked

## 2026-02-10

- trend detail:
    - AI rate in 10k Bing-search-result sites rose from 11.9% to 15.5%

## 2026-01-27

- reliability work details:
    - process pool kills timed-out workers to avoid repeated stdlib pooling bugs
    - AWS CC S3 service used trained zstd dictionary

## 2026-01-20

- infrastructure details:
    - Postgres killed by EarlyOOM
    - smaller Postgres tables moved to SSD because HDD writes were too slow
    - Exxact OOM and CPU saturation tied to malfunctioning colmap

## 2026-01-13

- dev details:
    - automatic GPU-selection logic added
    - CC over-crawling fixed
    - review UI improved
- TODOs:
    - investigate free-trial-generated sites and social-media promotion patterns
    - add CC sites to baseline anyway
    - crawl more pages from non-unimodal sites for bimodal checks

## 2026-01-06

- filter-calibration detail:
    - dropping 50% no-punctuation filter kept baseline acceptable
    - approximately 9 pre-ChatGPT false-positive subdomains supported keeping the change
- architecture detail:
    - moved HTTP client/browser controller/CC downloader to actor-model style

## 2025-12-16

- crawl-data consistency details:
    - subdomain/URL mismatch bug tracked in some crawls
    - sitemap links crossing subdomains were dropped as a temporary rule

## 2025-12-02

- baseline-size calibration detail:
    - around 14 pages/site converged, with 12 pages very close

## 2025-11-24

- poster-feedback details:
    - gpt-neo-2.7B may outperform Falcon-7B in one reproduction slide deck
    - sampling decoding plus repetition penalty can break detector behavior

## Existing canonical coverage (not duplicated here)

- date-cue examples (`galaxy.ai`, `cs2.kinguin.net`) are in `baseline_sites.md`
- image/video/lighthouse TODOs are in `execution.md` and `llm_site_features.md`
- many bimodal site examples are in `bimodal.md`
- Bing 500 WikiHow examples are in `preliminary_binoculars_eval.md`
- Google layout parsing, WikiHow dataset, and Google Trends notes are in
  `web_search.md`, `wikihow.md`, and `google_trends.md`

- elsewhere
    - caveat: some AI-heavy sites use fake old publication years;
        prefer `last-modified` when available (e.g., `galaxy.ai`,
        `cs2.kinguin.net`)
