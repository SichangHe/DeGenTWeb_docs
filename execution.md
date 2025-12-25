# Execution

(code and discussion are taken private; please ask Steven for repo access)

- see also `arguments.md` and `literature.md`
- development: `development.md`
- web search and crawling: `web_search.md`

## Overall steps

- [ ] improve ground truth & get robust classifier
    - [x] \~100 human/AI websites baseline and still do well
    - [ ] check if doing well
        - [x] apply to 10,000 websites in the wild
- [ ] apply broadly to websites in the wild?
    - ways to discover them
- [ ] determine why they do this (money/misinformation)?

## By order

want:

- how much need to crawl
    - [ ] compute CDF of per-subdomain filter pass portions
    - [ ] estimate expectation of crawl-to-sample ratio
- [ ] sampling sensitivity in the wild
    - [ ] retune filter thresholds after restat showed over-filtering
        - [ ] confirm Dolma filter works well against non-prose false
            positives on Common Crawl data
            - [x] apply Dolma filter
- [ ] inspect near-border sites
    - [ ] inspect filtered-out sites to confirm they are non-AI pages
- [ ] expand baseline dataset per reviewer feedback
    - [ ] collect additional true positive and true negative scenarios
    - [ ] broaden beyond Wix-style generators
    - [ ] measure accuracy on larger baseline with pre-GPT sites and
        Playwright-generated AI pages
    - [ ] characterize known generated versus self-generated websites
- [ ] cluster pages into two Gaussians per site for bimodal Binoculars score
- [ ] historical trend shift from Common Crawl windows
- [ ] monitor search-result trends
    - [ ] schedule periodic query sampling
    - [ ] run time series analysis on website changes
- [ ] measure impact of "humanizer" tools on Binoculars scores
- [ ] what are those website w/ many "positive" page
    - [ ] finish review UI for manual inspection
    - content farm w/ many ad (`ad_extraction.md`)
        - [ ] infer search queries targeted by content farms
            - [ ] inspect outgoing links for clusters of AI-dominant content
    - content farm selling product
        - [ ] identify scam seller
            - ~~perhaps use
                [blacklist](https://dsi.ut-capitole.fr/blacklists/index_en.php)
                used [by RefinedWeb](literature.html#training-data-curation)~~
                few matches
        - [ ] detect affiliate links
    - false positive: forum/support
    - [ ] find zero-ad zero-affiliate link site and study it
    - [ ] clustering
        - [ ] check existing clustering approaches
        - [ ] find comment about similar AI sites
        - keywords: DOM structure, JS frameworks, structural similarity,
            technology stack, template identification, website fingerprinting,
            layout similarity, homology detection
        - most literature targets traffic-based attacks
    - [ ] analyze Binoculars score versus publication timing
        - [ ] study burst versus gradual ramps of AI content
        - [ ] examine whether AI enables faster publication speed
        - hard to quantify publication speed without sitemap coverage
        - no correlation observed between score and date so far
        - [ ] derive sitemap-based publication speed signal
    - [ ] distinguish sites appearing across multiple search results
    - [ ] inspect site source code for tooling clues
        - [ ] identify website technologies via Wappalyzergo and
            correlate findings
    - [ ] measure similarity among pages within the same site
    - [ ] investigate middle-ground websites between obvious AI and
        human content
    - [ ] investigate get-rich-quick scheme hypothesis
        - attempted archiving Reddit posts but originals missing;
            have related passive income post
        - [ ] continue evidence gathering
- [ ] search Google/Bing/Brave/Perplexity/ChatGPT/ChatNoir
- [ ] fetch deeper than 20 results when queries yield many AI hits

nice-to-have:

- [ ] reduce text extraction overhead (CPU-bound)
- [ ] fix browser controller memory leak
- [ ] verify whether modem.tools is generated
- [ ] catalog ways to use LLMs to write content
- [ ] study HTML and JS feature dependencies
    - [ ] ask Yacin Alhamwy & Adrian Kunz to crawl dependency for sites
- crawling improvements
    - [ ] click cookie banner
    - [ ] SSO sign in
- [ ] training data memorization risks
- [ ] segment non-single-text pages
- [ ] explore non-website detection applications
    - [ ] Reddit LLM user detection
    - [ ] OpenReview detection similar to ICML study
    - [ ] student cheating detection
    - [ ] Amazon fake reviewer detection
    - [ ] fake news, resume, and bot detection scenarios
- [ ] build SearXNG plugin to filter AI-generated sites
    - posted on r/Searx; received upvotes but no responses

done:

- [x] preliminary: run Binoculars over Common Crawl; see if
    result make sense (`preliminary_binoculars_eval.md`) *edit*: …
    and WikiHow search result
- [x] crawl top 20 results/reference
- [x] extract body text
    - ~~DOM Distiller Reading Mode~~
    - [Trafilatura](https://github.com/adbar/trafilatura)
- Binoculars
    - [x] speed enhancement for large scale

## Meta question

- [ ] decide which web subsets to sample
    - [ ] study domain registration recency
        - [ ] evaluate RDAP creation-date reliability (thanks Xiao & Wes)
        - DNS registration records proved unreliable
        - [ ] review WhoisXML API data availability and pricing
- [ ] analyze why existing page reviews yield few insights
- [ ] examine ad network bottlenecks for AI sites
    - focus on Google Ads limiting revenue for LLM ad farms while
        profiting off reduced search quality
    - [ ] evaluate how hard it is to create AI websites that rank high
        - [ ] quantify SEO effort versus generation effort versus ranking
- [ ] gather evidence that adversarial perplexity inflation hurts quality
- [ ] assess economic viability versus human writing
    - [ ] consider signing up to work for a content farm
- [ ] evaluate harms from AI sites
    - [ ] quantify misinformation impact
    - [ ] measure scam prevalence
    - [ ] test search or RAG quality improvements after filtering
        - [ ] assess degradation of search or LLM results
- [ ] assess whether text detection alone suffices
    - [ ] examine generated imagery on detected sites such as
        <https://burstofstyle.com/messi-blonde-hair/>
    - [ ] survey openly available detectors of AI-generated images
- [ ] design deterministic confirmation steps after detector pre-filtering

## Reading backlog

- [ ] review phishing detection papers
- [ ] review genre detection papers
- [ ] review AI text detection papers
- [ ] review EU AI disclosure compliance research
- [ ] review synthetic data impact on LLM performance
    <https://sichanghe.github.io/notes/research/web_user_facing.html#search-engine-optimization-seo>.

## Cancelled

- filtering
    - try other ML model on Common Crawl derived labels
        - gather more ground truth
        - revisit decision-tree-based filter tuning to replace heuristics
