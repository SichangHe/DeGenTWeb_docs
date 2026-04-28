# LLM Site Kinds — Takeaways, Evidence, and Paper Arguments

This doc structures the findings from
`src/degentweb/classifying/llm_site_kinds_analysis.py` for the paper writeup
(IMC 2026 "Evaluation in the Wild" section).
Script output blocks are referenced by their `w("<tag>")` heredoc tag and plot
paths under `data/classify/llm_site_kinds/`.

## Scope and cohort

- Latest `search_result` `site_analysis_runs` snapshot, `selected_for_deep`
    subdomains with non-null `svm_distance`, restricted to sites with at
    least one successful latest `site_feature_live` crawl. Tag:
    `site_summary`. Numbers drift slightly as new snapshots land — at the
    time of this writing the cohort is roughly 3,600 subdomains (2,243
    llm\_like, 1,353 human\_like); re-read the current `site_summary`
    heredoc for the authoritative count.
- Label = sign of the site-level SVM distance; subdomains with near-zero
    distances are treated the same as confidently-LLM ones.
- The analysis is deliberately search-result-only.
- Monetization signals are HTML substring checks run on the live-fetched
    page content (see `codebase_index/llm_site_kinds_analysis.md` and
    `docs/llm_site_kinds_tech_ref.md`).
    They detect presence at a point in time only and under-count
    server-injected / consent-gated ads.

### Balanced cohort for incentive-coarse paper plots

#### Why `selected_for_deep` gates sampled pages

`selected_for_deep=TRUE` in `site_analysis_subdomains` is the hard gate
for two things:
1. **`site_analysis_sampled_pages`**: The page-sampling step only collects
    pages for `selected_for_deep=TRUE` subdomains.  Without these pages
    the LLM categorization prompt has no text to work with → the site
    cannot be categorized.
2. **`site_feature_live` crawls**: The live-fetch enqueue query
    (`selected_site_analysis_sample_pages_without_fetch` in
    `src/degentweb/sql/queries/site_features.sql`, line ≈364) filters
    `WHERE selected_for_deep = true`.

Subdomains with `selected_for_deep=FALSE` therefore have neither
analysis pages nor live-fetch data and must be excluded from the cohort.
A previous balanced-cohort SQL (commit `edde835`, reverted in `d1852bd`)
dropped this filter and sourced sites purely from live-fetch success.
That was wrong: it included sites that had live-fetch data from older
crawls but no `site_analysis_sampled_pages`, so 146 Search human-like
sites ended up uncategorized in the session and were silently bucketed as
"Other" in the plots.

#### Current cohort procedure (as of 2026-04-27+)

The `incentive_coarse` paper plots and the macros
`SiteKindsTotalCount`, `SiteKindsAiCount`, `SiteKindsHumanCount`
(and `Cc*` siblings) come from a **balanced, fully-categorized** cohort
built by `scripts/rebuild_balanced_search_cohort.py` (Search) and
`src/degentweb/classifying/cc_llm_site_kinds_paper_artifacts.py` (CC).

Procedure for the Search side:

1. **`raw_cohort`**: latest `site_analysis_runs.analysis_run_id` for
    `search_result`; join `site_analysis_sampled_pages` and `pages`;
    filter `selected_for_deep=TRUE` AND `svm_distance IS NOT NULL`.
    This guarantees every subdomain has analysis pages and is thus
    categorizable.
2. **`live_ok`**: for each page in `raw_cohort`, take the latest
    successful `site_feature_live` crawl and join `htmls` for HTML
    content.  Only rows with `crawl_ok=TRUE` survive.
3. **`signal_subs`**: distinct `(subdomain_id, label, subdomain64blake3)`
    from `live_ok`.
4. **`balanced_sids`**: for each label, rank subdomains by
    `(subdomain64blake3, subdomain_id)` (deterministic, reproducible)
    and keep top `MIN(n_llm, n_human)`.
5. Filter `live_ok` to `balanced_sids` → `page_html_signals`.
6. Fetch `page_categorizations` from PG for the balanced set.
7. **Exclude uncategorized** subdomains (NULL `category_slug`) from
    `page_html_signals`; these are NOT bucketed as "Other".
8. **Re-balance** to `MIN(LLM, human)` after exclusion using the same
    blake3 order.  The tiny imbalance from excluded sites (typically
    0–10) is corrected here.

The CC pipeline (`cc_llm_site_kinds_paper_artifacts.py`) already used
`selected_for_deep=TRUE` throughout, so step 7–8 are no-ops for CC
(≤3 NULL sites out of 6,732).

**Cohort counts** (as of 2026-04-27):

- Search: 2,393 + 2,393 = **4,786** (all categorized; 5 excluded). Session:
    `data/classify/llm_site_kinds/duckdb_session/20260427_135715.duckdb`.
    The "any-run" expansion (sites `selected_for_deep=TRUE` in any analysis run,
    not just the latest) yielded 2,456 human × 2,503 LLM; balanced at 2,398 per
    label; 5 truly uncategorized excluded; final 2,393 per label.
- CC: 3,366 + 3,366 = 6,732 (unchanged). Session:
    `data/classify/llm_site_kinds_cc/duckdb_session/20260427_001614.duckdb`.

`llm_site_kinds_paper_plots._DEFAULT_SEARCH_DB_PATH` defaults to the
latest balanced search session.  Override via
`DEGENTWEB_SITE_KINDS_SEARCH_DB_PATH`.

**Re-building the Search balanced session from scratch:**

```bash
# 1. (one-time, if needed) fetch live HTML for new selected_for_deep=TRUE human sites
DEGENTWEB_LIVE_FETCH_COHORT_CRAWL_SRCS=search_result \
  python -m degentweb.post_processing.fetch_live_page_features

# 2. Rebuild the balanced DuckDB session (excludes uncategorized automatically)
python -m scripts.rebuild_balanced_search_cohort

# 3. If the script reports uncategorized sites remaining, run:
python -m scripts.categorize_balanced_search_cohort
python -m scripts.refresh_balanced_search_categorizations
python -m scripts.rebuild_balanced_search_cohort   # re-run after categorization

# 4. Regenerate combined plot (uses both Search and CC sessions)
python -m scripts.regen_incentive_coarse_plots
```

**Re-rendering plots without a fresh PG fetch.**

**Re-rendering plots without a fresh PG fetch.**
`scripts/regen_incentive_coarse_plots.py` opens the latest balanced
session for both Search and CC, monkey-patches
`llm_site_kinds_paper_plots.OUT_DIR` per side, calls
`_write_incentive_stats`, `_plot_incentive_coarse_by_label`
(WIDE + NARROW), and `_plot_incentive_coarse_combined` against the
NARROW style, and writes the PDFs/PNGs and stats files in place.
This is the script to run when only the plot styling changed — it
is much faster than rebuilding the cohort from Postgres.

## Paper arguments

Each argument is stated as Claim → Evidence → Caveat and points to the
relevant heredoc tag and plot.
Only effect sizes that are practically meaningful (≥ ~15 percentage points,
or ≥ 2× odds ratio) are used.

### Arg 1: LLM-dominant search results concentrate in a small number of distinctive "kinds"

- Claim: LLM-dominant sites are not an even sprinkle across the Web;
    they concentrate into a few well-defined archetypes based on
    monetization architecture and technology stack. Most kinds sit
    near the cohort LLM base rate (~62%); the signal is driven by a
    short list of kinds that skew strongly one way or the other.
- Evidence:
    - Mixed-cohort KMeans over ~160 features (binary tech buckets,
        binary monetization signals, counts, Lighthouse medians,
        category one-hot) with k∈{10..20}, the selector picks k=20;
        after the ≥20-site floor we publish 13 kinds in
        `paper_ready_kind_table`.
    - Cluster sizes and label-mix in `all_kind_label_mix`.
    - Plot: `llm_site_kinds_all_kind_monetization_share.{png,pdf}`
        (stacked monetization-bucket share per kind).
- Caveat: silhouette is low (~0.05 on the mixed-cohort fit). Kinds are
    a reading lens; their boundaries are soft. The story rests on the
    few kinds whose share deviates clearly from the cohort prior, not
    on every cluster separately.

### Arg 2: The "AI content farm" archetype is observable and has a specific stack

- Claim: A single kind accounts for the most extreme LLM prevalence
    and corresponds to the stereotype: maximum ad density through an
    ad-management platform plus affiliate links, low-quality page
    experience, low custom tech surface.
- Evidence (the top row of `paper_ready_kind_table` at the Ezoic
    content-farm kind; current `all_kind_summary` heredoc for feature
    lifts):
    - ~160 sites (≈4% of cohort); **~88% llm\_like** (≈ +26 pp over
        baseline).
    - 100% Ezoic, ~99% Sharethrough, ~99% Criteo, ~100% Index
        Exchange, ~97% Amazon Advertising; mean ≈9.2 ad networks per
        site.
    - ~59% of sites carry both ads and affiliate links.
    - Dominant CDN column = `cdn_jsdelivr` at ~99% — a fingerprint of
        Ezoic's managed-ad delivery rather than a publisher choice.
    - Representative subdomains have been spot-checked: each of
        `susanhomecare.com`, `sipsscene.com`, `homescale.net`,
        `stevenfitspot.com`, `cookgeeks.net` carries Ezoic on every
        sampled page (direct PG query, Apr 2026).
- Caveat: ~160 sites is small; the finding is specific to
    Ezoic-managed sites and does not automatically generalize to all
    ad-managed content farms.

### Arg 3: Established/premium monetization is human-dominated; LLM bias runs in the entry-level stack

- Claim: Among ad-tech vendors, LLM sites over-represent the simplest
    monetization on-ramps (AdSense, Ezoic) and strongly under-represent
    the premium/managed stacks (Raptive/AdThrive, Sovrn, header-bidding
    supply stacks such as Pubmatic / Mediavine / Amazon Advertising,
    Taboola / Outbrain native, ConvertKit / Mailchimp / Substack
    newsletter tooling). Tag: `signal_llm_vs_human_enrichment` (the
    rendered version already drops p/q columns and restricts to effect
    sizes of at least 1.5× with BH q ≤ 0.01).
- Evidence (share of cohort carrying each network; LLM vs human):
    - Ezoic: **~8.5% LLM vs ~2.4% human** (≈3.5× ratio).
    - Google AdSense: **~31% LLM vs ~23% human** (≈1.4× ratio).
    - Raptive/AdThrive: ~4% LLM vs **~13% human** (≈0.3× ratio).
    - Sovrn: ~5% LLM vs **~12% human**.
    - Amazon Advertising (display): ~14% LLM vs **~22% human**.
    - Mediavine: ~10% LLM vs **~13% human** (smaller gap).
    - ConvertKit newsletter: **~1% LLM vs ~4% human** (≈4× gap).
    - Mailchimp: **~1% LLM vs ~4% human**.
    - Substack: ~0.3% LLM vs ~1% human.
    - Taboola native: ~1% LLM vs ~3% human.
    - Skimlinks: ~0.6% LLM vs ~2% human.
- Paper reading: LLM content reaches for the cheapest-to-deploy
    monetization layer (drop AdSense tag / Ezoic site-wrap) and skips
    the audience-cultivation layer (newsletter signups) that defines
    durable publishing. The numbers above are per-site prevalences.
    Vendor descriptions and citable URLs live in
    `docs/llm_site_kinds_tech_ref.md`, including the monetization
    "ladder" framing (AdSense at the bottom, Raptive at the top).
- Caveat: HTML-substring detection under-counts some networks.
    It does not track revenue; a 3.5× prevalence ratio for Ezoic does
    not imply a revenue ratio.

### Arg 4: Institutional and established-affiliate web are largely LLM-free

- Claim: LLM content is sparse in clearly-bounded human-built
    regions: institutional sites (.edu/.org/.gov/Drupal-heavy), and
    established Skimlinks-managed affiliate sites. Newsletter/creator
    monetization is not dominant enough within a single cluster to
    appear in the current mixed-cohort fit, but on the per-signal
    level (Arg 3) ConvertKit/Mailchimp/Substack all skew human.
- Evidence (`paper_ready_kind_table`, using the current cluster IDs
    — the precise `kind_NN` names drift between runs, read the
    heredoc for the current mapping):
    - Drupal-institutional kind (≈120 sites): **~17% llm\_like**
        (lift −45 pp). ~80% of sites fall in the `institutional`
        category. Tech skews Drupal + Fastly / Apache.
    - Skimlinks-affiliate kind (≈30 sites): **~29% llm\_like**
        (lift −33 pp). 100% carry Skimlinks; mean affiliate-network
        count ≈1.9; the heaviest affiliate concentration in the
        cohort.
- Caveat: these clusters are small (30–130 sites); the directional
    effect is reliable, but the precise percentages are noisy.

### Arg 5: LLM-detection confidence is decoupled from monetization aggressiveness

- Claim: A site that the detector flags as very confidently LLM
    is no more and no less likely to be heavily monetized than a
    borderline-LLM site. The relationship between "how confident are
    we this is LLM content" and "how aggressively is the site
    monetized" is roughly flat.
- Evidence (tag `svm_distance_gradient`):
    - SVM-distance bucket (0, 0.5]: 62% has\_ads, 18% has\_affiliate,
        mean 2.2 ad networks.
    - (0.5, 1.0]: 63% / 16% / 2.1.
    - (1.0, 2.0]: 58% / 18% / 2.0.
    - (2.0, +inf): 59% / 16% / 2.0.
- Paper reading: "more confident LLM" ≠ "more spammy". A confidently-LLM
    site can be a SaaS copy page or a generated FAQ just as easily as a
    content-farm page. Be careful when the paper implies the two are
    aligned.
- Caveat: we only bucketed LLM-like sites; the analysis does not
    say anything about monetization changes across the sign boundary
    (human vs LLM).

### Arg 6: Aggressive monetization correlates with user-hostile page experience

- Claim: LLM-dominant content-farm-style sites provide the worst
    Web Vitals in our cohort. The cluster with the most ad networks
    also has the worst median performance score and total blocking
    time.
- Evidence (tag `all_kind_lighthouse`):
    - Ezoic content-farm kind: median performance ~0.45, total
        blocking time on the order of 10 seconds, mean ≈9 ad
        networks per site.
    - WordPress publisher (light) kind: median performance ~0.8,
        total blocking time well under 100 ms, mean <0.5 ad networks
        per site.
- Paper framing: the monetization-aggressiveness gradient (ad-network
    count per site) is also a user-experience gradient.
- Caveat: Lighthouse is a single-run synthetic benchmark, not a real
    user measurement. Run-to-run Lighthouse numbers vary with ad
    auction fills. The claim should be framed as "relative ordering",
    not an exact headline number.

### Arg 7: Skimlinks affiliate is a counter-example of an LLM-rare *but* heavily-monetized cluster

- Claim: Heavy monetization ≠ LLM. Skimlinks-managed affiliate sites
    are among the most intensely monetized in the cohort (mean ~2
    affiliate networks per site, near-100% `ads_and_affiliate`) yet
    they are only ≈29% LLM.
- Evidence: the Skimlinks-affiliate kind in `paper_ready_kind_table`.
- Paper reading: the paper's monetization-driven framing should not
    oversell the claim "aggressive monetization = LLM". The direction
    of the correlation is weak and depends on which monetization
    layer.

### Arg 8: Within a kind, LLM sites still under-use affiliate and newsletter signals

- Claim: Even within a single kind (i.e. holding the stack rough
    constant), LLM sites carry noticeably fewer affiliate links and
    newsletter signals than the human sites that landed in the same
    kind. The LLM-vs-human gap on monetization is not only between
    kinds but also within kinds.
- Evidence (tag `all_kind_llm_vs_human_within_kind`, filtered to
    ≥10 pp within-kind gap and ≥15 sites in each label):
    - In the "WordPress premium publisher" kind (a mixed LLM-human
        cluster): LLM sites are ~17 pp less likely to carry affiliate
        links and ~14 pp less likely to carry newsletter signups than
        human sites in the same kind.
    - In the "heavy ad + affiliate" kind: LLM sites are ~11 pp less
        likely to carry affiliate links, but ~10 pp more likely to
        carry newsletter signups (reverse of the usual direction;
        small n, read as suggestive).
- Caveat: the filter requires a within-kind gap of at least 10 pp
    AND at least 15 sites on each side. Kinds that are nearly
    pure-LLM or pure-human do not contribute rows to this table
    because the human (or LLM) cell is too small.

## Extra findings from CDF and spot-check evidence

These are supporting observations surfaced by the LLM-vs-human CDFs and
by direct HTML-content spot-checking.

- **Whole-cohort LLM vs human CDFs do not look dramatically different.**
    The `llm_site_kinds_llm_vs_human_cdf_n_ads_networks.png` plot
    shows the LLM cohort has slightly *more* zero-ad-network sites
    (≈41% vs ≈35%) than the human cohort, and the same shape in the
    tail; the LLM-vs-human picture is not "LLM sites are monetized
    more aggressively on average" — it is "a small LLM-dominated
    subset (the content-farm kind) drags up the average, while the
    long tail of LLM sites is at worst mildly monetized and often
    not at all". Same pattern in
    `llm_site_kinds_llm_vs_human_cdf_median_performance_score.png`:
    overall LLM performance CDF sits slightly *above* the human one;
    the poor-Vitals story of Arg 6 is driven by a specific cluster,
    not the whole label.
- **`llm_site_kinds_signal_llm_vs_human_gap.png`** is a single bar
    chart of the per-signal LLM-minus-human percentage-point gap.
    Two blue bars (LLM-enriched: AdSense and Ezoic) vs a long tail
    of orange bars (human-enriched): Raptive/AdThrive, Amazon
    Advertising, Sovrn, Facebook Pixel, PubMatic, ConvertKit,
    Mediavine, Amazon Associates, Mailchimp, Criteo,
    Google Ad Manager, Index Exchange, Taboola. Good paper figure
    for Arg 3; the asymmetry is striking.
- **Content-farm sites pass naive AI-disclosure checks.** Direct PG
    grep on the representative Ezoic content-farm subdomains
    (`susanhomecare.com`, `sipsscene.com`, `homescale.net`,
    `stevenfitspot.com`, `cookgeeks.net`, `homebathtub.com`,
    `liftmanual.com`) found zero occurrences of obvious AI-giveaway
    phrases like "as an AI language model" or "in conclusion,", and
    zero pages with AI-generation disclosures. Every sampled page
    carries a schema.org Person / author markup. In other words,
    these sites would not be caught by surface-level manual review;
    the SVM / Binoculars detector is doing work a human reader
    typically would not.
- **Content-farm pages are heavy.** Average HTML byte size for the
    seven representative subdomains above ranges from ~170 KB to
    ~1.16 MB, with multiple sites at 800 KB+. This corroborates the
    Lighthouse-perf claim (Arg 6): the poor Web Vitals are rooted in
    actual page weight, not just synthetic-benchmark variance.

## Supporting tables and plots

- `site_summary` — cohort sizes and coverage.
- `monetization_family_summary` — site-level `has_ads` /
    `has_affiliate` / `has_subscribe` / `has_donate` / `has_commerce`
    / `has_lead` prevalence for LLM vs human.
- `monetization_bucket_summary` — LLM vs human cross-tab over the
    seven-way monetization bucket (`ads_and_affiliate` /
    `ads_only` / `affiliate_only` / `subscribe_or_donate` /
    `commerce_checkout` / `lead_gen_only` / `none_detected`).
- `monetization_signal_summary` — per-network site counts and
    percentages, LLM vs human.
- `signal_llm_vs_human_enrichment` — rendered version already filters
    to ≥1.5× ratio and BH q ≤ 0.01 and drops raw p/q columns. Full
    table with p/q is kept in DuckDB (`signal_llm_vs_human`).
- `ads_category_enrichment` / `affiliate_category_enrichment` —
    per-category prevalence of `has_ads` / `has_affiliate` among LLM
    sites, rendered with p/q stripped and small categories filtered
    out (the full tables with p/q stay in DuckDB).
- `feature_pair_cramers_v_top` — top pairwise Cramer's V over binary
    features (LLM cohort); trivial "X-html-detector vs
    X-Wappalyzer-detector" pairs are filtered out; rendered list
    drops raw p/q.
- `all_kind_summary` / `all_kind_label_mix` / `all_kind_lighthouse` /
    `paper_ready_kind_table` — the main per-kind tables.
- `all_kind_llm_vs_human_within_kind` — within-kind LLM vs human gaps
    on `has_ads`, `has_affiliate`, `has_subscribe`, `has_commerce`,
    `has_lead`. Filtered to gap ≥ 10 pp with ≥ 15 sites per label.
- `all_kind_modality_breakdown` — cross-ref with the
    score-distribution bimodal analysis: how many sites in each kind
    are flagged `bimodal` or `other` modality by
    `score_distribution.py`. In practice most sites are `unknown`
    (not eligible for the score-distribution classifier or
    single-gaussian); the table is mainly useful for spotting kinds
    where bimodal concentration is unusually high.
- `kind_summary` / `kind_label_mix` — LLM-only clustering for
    completeness; the mixed-cohort view is the primary one for the
    paper.
- Plots (paths relative to `data/classify/llm_site_kinds/`):
    - `llm_site_kinds_all_kind_monetization_share.{png,pdf}` — per-kind
        stacked bar of monetization buckets.
    - `llm_site_kinds_signal_llm_vs_human_gap.{png,pdf}` — horizontal
        bar of LLM-minus-human percentage-point gap per signal (the
        single best paper figure for Arg 3).
    - `llm_site_kinds_llm_vs_human_cdf_*.png` — LLM-vs-human CDFs
        for `n_ads_networks`, `n_affiliate_networks`,
        `n_base_technologies`, `median_performance_score`,
        `median_seo_score`, `median_accessibility_score`,
        `median_lcp_ms` (log-x), `median_tbt_ms`. Tag:
        `llm_vs_human_cdf_plot_paths`.
    - `llm_site_kinds_cluster_label_mix.{png,pdf}` — per-LLM-kind
        count bar (LLM-only clustering).
    - `llm_site_kinds_affiliate_by_category.{png,pdf}` — per-category
        affiliate prevalence among LLM sites, with a cohort baseline
        line.
    - `llm_site_kinds_ads_by_category.{png,pdf}` — same for ads.
    - `llm_site_kinds_pair_cramers_v_top.{png,pdf}` — strongest
        pairwise Cramer's V over binary features (LLM cohort).

## Known limitations of this analysis

1. **HTML substring detection is a lower bound on monetization.**
    Server-side ads, consent-wall-gated scripts, and dynamically-
    injected affiliate rewrites are missed.
    The EasyList parent-element ad counter (`ads_counts`) has never
    been run on `site_feature_live` crawls, so we cannot cross-check
    against it for this cohort. Wiring up an EasyList-based count on
    this cohort is an obvious follow-up.
2. **"Kind" is a KMeans artifact, not a ground truth.** Clusters are
    a reading lens, not a taxonomy.
3. **Detection of Amazon Associates is URL-pattern-based.** We match
    `amzn.to/`, `amazon.com/dp/`, `amazon.com/gp/product/`,
    `amazon.com/exec/obidos`, and `amzn.com/`. We intentionally
    dropped the loose `?tag=` / `&tag=` patterns after noticing they
    match WordPress-style tag-page URLs.
4. **We do not know when a site was created.** The DB has a
    `first_crawled_at` per subdomain but it records when DeGenTWeb
    first crawled the domain, not when the domain existed on the
    Web. For a cohort whose crawls are mostly in 2025, nearly every
    `first_crawled_at` is 2025; this column should not be used to
    argue site age.
5. **SVM label is a single-threshold classification.** A subdomain is
    `llm_like` iff `svm_distance > 0`. Near-zero distances are
    counted as LLM with the same weight as confidently-LLM ones.
6. **No revenue data.** We can see monetization *surface area* but
    not dollars.

## Open follow-ups

- Cross-reference with the bimodal-mode analysis from
    `search_result_dolma_data_analysis.py`: do subdomains that the
    score-distribution classifier flags as `bimodal_gaussian` land
    disproportionately in the content-farm kind?
- Close the `none_detected` bucket: 35.9% of LLM sites have no
    monetization signal. Adding patterns for Stripe checkout,
    Paddle, Lemon Squeezy, Gumroad, SaaS-membership flows, lead-gen
    forms (HubSpot, Marketo), and dropshipping should shrink this.
- EasyList ad count on the live-fetch cohort, to cross-check the
    substring detection and provide a second view of ad density.
- Run the same pipeline against Webis / Common Crawl cohorts if
    (when) we extend live-fetch there.
- Named-kind labels in the paper writeup — currently kinds are
    `kind_06`, `kind_07`, etc. For writing, use the one-line
    descriptions in `paper_ready_kind_table` to give them readable
    names (e.g. "Ezoic content farm", "Drupal institutional").

## Pointer to the tech reference

Vendor and product descriptions with citable sources are in
`docs/llm_site_kinds_tech_ref.md`. Use that doc when writing the
paper to back up technology claims.

## Pointer to the what-they-do breakdown

A hierarchical breakdown of what all 2,243 LLM-like sites are actually
doing — by category and monetization sub-type, with examples and
percentages — is in
[`docs/llm_site_kinds_what_they_do.md`](llm_site_kinds_what_they_do.md).
Analysis methodology and reproduction steps are in
[`codebase_index/llm_site_kinds_what_they_do_analysis.md`](../codebase_index/llm_site_kinds_what_they_do_analysis.md).

---

## CC vs Search composition differences — analysis (2026-04-27)

### Category distributions (balanced cohorts, all categorized)

**Search** (2,393 LLM + 2,393 human):

| Category | LLM% | Human% | Δ |
|---|---|---|---|
| publisher_editorial | 54.0 | 40.9 | +13.1 |
| business_service_operator | 18.0 | 19.2 | −1.2 |
| affiliate_seo_content | 11.4 | 10.6 | +0.8 |
| retail_ecommerce | 6.1 | 6.4 | −0.3 |
| product_saas_company | 3.0 | 4.7 | −1.8 |
| institutional | 0.8 | 7.1 | **−6.3** |
| personal | 1.8 | 5.0 | −3.3 |

→ Distributions are **nearly identical**. The search-ranking filter pre-selects
for traffic-seeking commercial sites on both sides. The main LLM edge is in
`publisher_editorial` (+13pp): LLM content farms masquerade as editorial sites and
outcompete human editorial in SERPs.

**CC** (3,366 LLM + 3,366 human):

| Category | LLM% | Human% | Δ |
|---|---|---|---|
| business_service_operator | 42.6 | 31.0 | **+11.6** |
| retail_ecommerce | 16.8 | 9.6 | **+7.2** |
| publisher_editorial | 23.8 | 26.3 | −2.5 |
| affiliate_seo_content | 5.0 | 2.0 | +2.9 |
| product_saas_company | 4.8 | 2.0 | +2.8 |
| institutional | 1.2 | 15.7 | **−14.5** |
| personal | 0.7 | 5.6 | **−4.8** |

→ Distributions are **structurally different**. Two mechanisms:

1. **Non-commercial floor disappears for LLM.** CC human is ~21% institutional
   + personal (universities, .gov, .org NGOs, churches, hobbyist blogs) that have
   no AI adoption pressure. CC LLM is <2% of these. Because LLM sites are nearly
   all commercial, BSO/retail/SaaS inflate as a share of the LLM pie.

2. **CC captures a commercial tier invisible in Search.** CC indexes small
   businesses building their first web presence with AI, which never rank in
   search. The .ae/.pk/.ph/.africa TLD patterns (see TLD section below) show
   this is concentrated in emerging markets.

### TLD analysis (CC dataset)

**Most LLM-enriched TLDs** (by LLM%/human% ratio, n≥5):

| TLD | LLM n | Human n | Ratio | Interpretation |
|---|---|---|---|---|
| .guide | 11 | 1 | 11x | How-to guide content farms |
| **.ai** | **223** | **36** | **6.2x** | AI startups using LLM for own content (see below) |
| .pk | 70 | 12 | 5.8x | Pakistan SMBs: e-commerce, real estate, local services |
| .ae | 138 | 26 | 5.3x | UAE businesses: real estate Dubai, marketing agencies |
| .agency | 31 | 6 | 5.2x | Marketing/design agencies with AI-generated content |
| .africa | 12 | 5 | 2.4x | African emerging market businesses |
| .app | 64 | 46 | 1.4x | App product pages (mild enrichment) |

**Most human-enriched TLDs**:

| TLD | LLM n | Human n | Ratio | Interpretation |
|---|---|---|---|---|
| .gov | 1 | 42 | 0.02x | Government — zero LLM adoption |
| .ac.uk | 0 | 23 | 0.00x | UK academia — zero LLM adoption |
| .sg | 0 | 18 | 0.00x | Singapore institutions |
| .org | 101 | 424 | 0.24x | Non-profits/NGOs strongly human-dominated |
| .co.uk | 2 | 40 | 0.05x | UK commercial (often established businesses) |
| .me | 3 | 14 | 0.21x | Personal portfolios/blogs |

### .ai domain deep dive

CC: **223 LLM .ai** (6.63% of all CC LLM) vs **36 human .ai** (1.07%) → **6.2x ratio**.
.ai is the **#3 TLD** for CC LLM (after .com and .net). For CC human it is #7.

Search: 37 LLM .ai (1.5%) vs 16 human .ai (0.7%) → 2.1x ratio. The lower Search
enrichment confirms these sites mostly don't rank well.

**Two distinct populations of .ai sites:**

*Human .ai* — legitimate established AI/tech product companies:
`arthur.ai`, `vast.ai` (GPU cloud), `fundgpt.ai`, `hypernatural.ai`, `invoicer.ai`,
`metatable.ai`, `ocelot.ai`. Categories: product_saas_company (dominant),
support_knowledge_base (docs). These have real products and human-written copy.

*LLM .ai* — AI startups / AI-themed services using LLM for their own marketing/blog content:
`autoblogging.ai` (product_saas: AI writing tool itself), `essayai.ai`,
`blog.forexhero.ai`, `bestinai.ai`, `generativeaidatascientist.ai`,
`marketinghero.ai`, `sociallab.ai`, `blog.cryptohero.ai`. Categories: mix of
product_saas_company (~40%), business_service_operator (~30%),
publisher_editorial (~20%).

Key .ai observations:
- **Self-referential**: many are AI-product companies using AI to write their
  own blog/marketing content. The LLM detection is catching AI companies' own
  marketing material.
- **"blog.*" subdomain pattern**: `blog.forexhero.ai`, `blog.alphashots.ai`,
  `blog.clientconnect.ai`, `blog.brainify.ai`, `blog.wowto.ai` — these are
  AI startups with LLM-generated blog sections specifically.
- **docs.*.ai pattern**: `docs.allpass.ai`, `docs.swarmzero.ai`, `docs.trieve.ai` —
  auto-generated or LLM-assisted technical documentation.
- Some problematic content: `undressaiapp.ai`, `www.cybeauty.ai`, `thotchat.ai`
  (adult/NSFW) using AI for content generation.

### Emerging-market business pattern (.ae, .pk examples)

**CC LLM .ae examples** (real estate, marketing, local services Dubai):
`neorealtydubai.ae`, `busrentaldubai.ae`, `danceanddazzledubai.ae`,
`www.reemmall.ae` (mall retail), `jaipurnationaluniversity.ae`,
`www.twoguys.ae`, `stratedge.ae`, `kabamba.aero`.

**CC LLM .pk examples** (e-commerce, fashion, pharmacy):
`trendify.pk`, `vegasvapor.pk`, `www.marhampharmacy.pk`,
`shreepramukhjewellery.in.ua` (Indian jewelry), `floristella.com.ph` (Philippines florist).

Pattern: these are real businesses in markets where professional web writing is
expensive relative to local wages, and where AI writing tools have reached high
adoption. They build a web presence primarily for credibility/legitimacy (not search
ranking), so they appear in CC but not in Search.

### What actually drives the CC LLM BSO bulk (2026-04-28)

**Short answer**: Not emerging-market businesses — those are only ~200 of the
1,435 CC LLM BSO sites. The bulk is **Anglophone small/local offline service
businesses** (US, Canada, UK, Australia) that used AI tools to generate their
website content cheaply.

**Monetization fingerprint is the diagnostic**: CC LLM BSO has **75% no-signal**
(no ads, no affiliate links, no subscribe forms) — identical to CC human BSO (74%).
Compare to CC LLM editorial (69% no-signal) or affiliate/SEO (75% no-signal but
higher affiliate rate). This proves these are not content farms: they have no
interest in monetizing web traffic. Their website is a **digital business card and
lead-generation contact page**.

**Industry breakdown (keyword-approximated, 1,435 CC LLM BSO sites):**

| Industry | n | % |
|---|---|---|
| Medical / dental / health clinic | 132 | 9.2% |
| Home / trade services (HVAC, plumbing, roofing, cleaning…) | 128 | 8.9% |
| Marketing / media / creative agencies | 91 | 6.3% |
| Tech / IT / digital services | 78 | 5.4% |
| Auto / transport / logistics | 52 | 3.6% |
| Travel / events / hospitality | 44 | 3.1% |
| Legal / finance / accounting | 33 | 2.3% |
| Wellness / beauty / personal care | 28 | 2.0% |
| Real estate / construction | 27 | 1.9% |
| Emerging-market geo TLDs (.ae+.pk+.ph+.africa) | ~230 | ~16% |
| Other / unclassified (same pattern, opaque domain names) | 762 | 53% |

The "other-unclassified" 53% breaks the same way when eyeballed:
`affordableheatingcooling.com`, `ajrheatingandactx.com`,
`aliefheatingandairconditioning.com`, `agapebhc.com` (behavioral health),
`airportassistme.com`, `allphaserestore.com` (restoration) — all local services
using domain names that don't contain readable industry keywords.

**The mechanism**:
- A dentist / HVAC company / law firm / marketing agency wants a website.
- They use an AI-assisted website builder (Wix AI, Squarespace AI, or ChatGPT)
  to generate "About Us", service descriptions, FAQ copy.
- Cost: nearly zero. Time: minutes.
- This site appears in Common Crawl (broadly indexed), but **never ranks in search**
  (no SEO investment, no backlinks, no content scale).
- Result: shows up in CC as LLM-dominant, absent from Search cohort.

The emerging-market pattern (.ae, .pk, .ph) is the most **visible** because the TLD
ratio is large (5–6x), but those ~230 sites are just a more exotic instance of the
same universal phenomenon. The dominant driver is the much larger pool of
**English-language small businesses in the US/Canada/UK** doing the same thing.

**Comparison: CC vs Search LLM BSO monetization**:
- CC LLM BSO: ads=24.7%, aff=0.4%, neither=75.1% — **no-monetization mode**
- Search LLM BSO: ads=31.2%, aff=3.0%, neither=66.7% — slightly more monetized

Search LLM BSO (430 sites) has higher ad/affiliate rates because ranking in search
selects for sites with active traffic strategies, including those that monetize
that traffic. CC LLM BSO has no such filter.

### One-sentence explanations

**Search** (LLM ≈ human): The ranking filter selects for traffic-seeking commercial
sites on both sides, making category mixes similar. The LLM edge is narrowly in
editorial content farming.

**CC** (LLM >> BSO/retail, human >> institutional/personal): No filter, so the full
web shows through. Human web includes a large non-commercial sector with zero LLM
adoption pressure. LLM BSO is dominated by **offline service businesses** (medical,
HVAC, legal, etc.) that used AI to generate their website copy as a digital business
card — not content farms. Emerging-market businesses (.ae, .pk) are a visible
minority (~16%) of the same phenomenon, not the bulk driver.

Reproduction: `data/classify/llm_site_kinds/duckdb_session/20260427_135715.duckdb`
(Search) and `data/classify/llm_site_kinds_cc/duckdb_session/20260427_001614.duckdb`
(CC). The analysis code used to derive these figures is the inline Python block at
the bottom of `PLAN-cc-search-category-analysis.md`.
