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
