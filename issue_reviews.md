# Issue reviews

Periodic notes from GitHub issue review, focused on analysis findings that still matter. Skip paper-writing, pure infra/tooling, and stale directions.

- Last full issue+comment review: `2026-04-16T02:37:02Z`
- Scope of latest pass: all repository issues plus comments updated through that timestamp.

## 2026-04-16

### Main takeaways

- **Detector output only became useful after page-quality controls.** Early issue work showed many extreme Binoculars scores on short, non-article, or boilerplate-heavy pages, so manual review, browser crawling, and article filtering were necessary before trusting the detector ([#1](https://github.com/SichangHe/DeGenTWeb/issues/1), [#2](https://github.com/SichangHe/DeGenTWeb/issues/2), [#3](https://github.com/SichangHe/DeGenTWeb/issues/3), [#8](https://github.com/SichangHe/DeGenTWeb/issues/8), [#13](https://github.com/SichangHe/DeGenTWeb/issues/13)).
- **Filtering and dedup mattered as much as the detector.** Later fixes focused on long-enough text blocks, list/table ratios, hidden boilerplate removal, and CDC-style duplicate-block removal; together they reduced false positives from cookie banners, listings, and repeated template text ([#6](https://github.com/SichangHe/DeGenTWeb/issues/6), [#13](https://github.com/SichangHe/DeGenTWeb/issues/13), [#26](https://github.com/SichangHe/DeGenTWeb/issues/26)).
- **Website-level baseline separation stayed strong.** The baseline-site experiments reported a clear gap between generated and human-written sites even after more filtering and dedup, which supports the decile-feature SVM framing more than raw per-page thresholding does ([#18](https://github.com/SichangHe/DeGenTWeb/issues/18), [#30](https://github.com/SichangHe/DeGenTWeb/issues/30)).
- **Search-result analysis produced a meaningful AI-like slice.** The Bing/WikiHow crawl grew from preliminary spot checks into site-level classification; one later pass reported 68 subdomains with at least 20 samples predicted as generated, and a follow-up sensitivity study found very few human predictions flipped under re-sampling ([#3](https://github.com/SichangHe/DeGenTWeb/issues/3), [#23](https://github.com/SichangHe/DeGenTWeb/issues/23), [#40](https://github.com/SichangHe/DeGenTWeb/issues/40)).
- **Auxiliary signals were mixed rather than decisive.** Ad counts are better treated as ad-element or monetization intent than literal visible ads, UT1 blacklist matching produced few scam hits, and publication-date signals are noisy because modified pages and `htmldate` fallback behavior can distort them ([#6](https://github.com/SichangHe/DeGenTWeb/issues/6), [#14](https://github.com/SichangHe/DeGenTWeb/issues/14), [#58](https://github.com/SichangHe/DeGenTWeb/issues/58)).
- **Scaling the datasets is currently constrained by coverage and storage.** Common Crawl work suggested enough scale to surface many AI-like sites, but practical bottlenecks moved to index download speed and local HTML storage; Webis selective downloads also looked too sparse for the current 15-page-per-site pipeline ([#27](https://github.com/SichangHe/DeGenTWeb/issues/27), [#53](https://github.com/SichangHe/DeGenTWeb/issues/53)).
- **Some hypotheses gained support, others stayed secondary.** There is direct external evidence that people build AI-content sites for monetization, while prompt-engineered LLM article filtering and similar side paths looked lower-value than improving the main text-analysis pipeline ([#13](https://github.com/SichangHe/DeGenTWeb/issues/13), [#37](https://github.com/SichangHe/DeGenTWeb/issues/37)).

### Unresolved relevant issues

- [#18](https://github.com/SichangHe/DeGenTWeb/issues/18) — Keep broadening baseline sites and generated-site examples without weakening the currently strong separation.
- [#14](https://github.com/SichangHe/DeGenTWeb/issues/14) — Decide whether blacklist matching is useful enough to keep, given the weak scam-signal yield so far.
- [#23](https://github.com/SichangHe/DeGenTWeb/issues/23) — Finish interpreting the Bing/WikiHow search-result crawl and calibrate confidence on site-level predictions.
- [#27](https://github.com/SichangHe/DeGenTWeb/issues/27) — Continue Common Crawl sampling once storage and throughput are less constraining.
- [#29](https://github.com/SichangHe/DeGenTWeb/issues/29) — Decide whether extra detectors add real independent signal or mostly correlated confidence with Binoculars.
- [#30](https://github.com/SichangHe/DeGenTWeb/issues/30) — Finish the real-world, class-imbalanced ablation story instead of leaning on AUROC.
- [#40](https://github.com/SichangHe/DeGenTWeb/issues/40) — Re-run page-sampling sensitivity after the latest filtering stack settles.
- [#53](https://github.com/SichangHe/DeGenTWeb/issues/53) — Determine whether Webis-PSERP-24 can be made dense enough for this pipeline or should stay a side experiment.
- [#54](https://github.com/SichangHe/DeGenTWeb/issues/54) — Check whether image-generation signals add anything beyond text-based signals.
- [#56](https://github.com/SichangHe/DeGenTWeb/issues/56) — Validate whether LLM-based site categorization produces stable categories worth keeping.
- [#57](https://github.com/SichangHe/DeGenTWeb/issues/57) — Turn live-fetch response/header/Lighthouse/Wappalyzer outputs into usable comparative signals.
- [#58](https://github.com/SichangHe/DeGenTWeb/issues/58) — Decide how publication dates should be interpreted given modified pages and `htmldate` fallback artifacts.

### Explicitly skipped this pass

- Paper-writing and figure issues such as [#60](https://github.com/SichangHe/DeGenTWeb/issues/60) and [#61](https://github.com/SichangHe/DeGenTWeb/issues/61).
- Pure infrastructure, refactor, migration, and one-off bug-fix threads unless they changed analysis conclusions.
- Open but stale directions whose comments already showed low value for this review pass.
