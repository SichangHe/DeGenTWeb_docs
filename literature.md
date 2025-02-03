# Literature

## Content farm

- [An examination of content farms in
    web search using
    crowdsourcing](https://dl.acm.org/doi/10.1145/2396761.2398689)
    An examination of content farms in web search using crowdsourcing,
    Richard McCreadie, Craig Macdonald, Iadh Ounis, Jim Giles, Ferris Jabr,
    CIKM, 2012
    - Mechanical Turk to label search result
    - found content farm decrease
- [Polls, clickbait, and commemorative $2 bills:
    problematic political advertising on news and
    media websites around the 2020 U.S.
    elections](https://dl.acm.org/doi/abs/10.1145/3487552.3487850), Eric Zeng,
    Miranda Wei, Theo Gregersen, Tadayoshi Kohno, Franziska Roesner, IMC, 2021
    - content farm served political ad
    - extract ad w/ [EasyList](https://easylist.to/) CSS selector
        - 💡 can use uBlock Origin logger
    - qualitative coding & BERT classifier to analyze
    - [Analyzing the (In)Accessibility of
        Online
        Advertisements](https://dl.acm.org/doi/abs/10.1145/3646547.3688427),
        Christina Yeung, Tadayoshi Kohno, Franziska Roesner, IMC, 2024
        - use UWCSESecurityLab adscraper to extract ad, which [in turn use
            EsayList](https://github.com/UWCSESecurityLab/adscraper/blob/main/crawler/src/ads/ad-detection.ts#L10)
- [Funding the Next Generation of Content Farms: Some of
    the World’s Largest Blue Chip Brands Unintentionally Support the Spread of
    Unreliable AI-Generated News
    Websites](https://www.newsguardtech.com/misinformation-monitor/june-2023/)
    - NewsGuard found 141 brand have ad on AI-driven site
        - unreliable AI-generated news website (UAIN)
    - mainly use Google Ads
    - publish large volume, sometimes 1000 per day
    - [Junk websites filled with AI-generated text are pulling in money from
        programmatic
        ads](https://www.technologyreview.com/2023/06/26/1075504/junk-websites-filled-with-ai-generated-text-are-pulling-in-money-from-programmatic-ads/)
        - number for ad revenue
    - [People Are Spinning Up Low-Effort Content Farms Using
        AI](https://futurism.com/content-farms-ai)
        - content farm low quality, misinformation, profit from Google Ads
        - 💡 maybe we report them to Google bc against their ad policy
- [AI ‘News’ Content Farms Are Easy to Make and Hard to Detect:
    A Case Study in Italian](https://aclanthology.org/2024.acl-long.817/),
    Giovanni Puccetti, Anna Rogers, Chiara Alzetta, Felice Dell’Orletta,
    Andrea Esuli, ACL, 2024
    - easy to fine-tune free model into Italian content farm model (CFM)
    - literature review on NewsGuard report & detector
    - human&DetectGPT low accuracy—infeasible to detect
        - fine-tuning of detector help a lot, but need to know base LLM used

## Training data curation

- [The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with
    Web Data, and Web Data Only](https://arxiv.org/abs/2306.01116),
    Guilherme Penedo, Quentin Malartic, Daniel Hesslow, Ruxandra Cojocaru,
    Alessandro Cappelli, Hamza Alobeidli, Baptiste Pannier, Ebtesam Almazrouei,
    Julien Launay, arXiv, 2023
    - heuristic-based URL filtering; no ML filtering to avoid bias
        - [4.6M site
            list](https://dsi.ut-capitole.fr/blacklists/index_en.php)
            💡 useful for spotting spam/scam, etc.
    - use Trafilatura  for main content extraction
    - Quality at a glance: An audit of web-crawled multilingual datasets
        - Common Crawl include large portion of machine spam & porn
