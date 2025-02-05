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

## Search Engine Optimization (SEO)

See
<https://sichanghe.github.io/notes/research/web_user_facing.html#search-engine-optimization-seo>.

## Generative AI (GenAI)

See <https://sichanghe.github.io/notes/research/gen_ai.html>.

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
    - use Trafilatura for main content extraction
    - [Quality at a glance: An audit of web-crawled multilingual
        datasets](https://watermark.silverchair.com/tacl_a_00447.pdf?token=AQECAHi208BE49Ooan9kkhW_Ercy7Dm3ZL_9Cf3qfKAc485ysgAAA0kwggNFBgkqhkiG9w0BBwagggM2MIIDMgIBADCCAysGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMYDsuqH9y69stXtfIAgEQgIIC_NpNFUq9XwBVhA1GuuhBYIPM2rR1yaHpq0n-bsnXNpOZXebbOTNYclgulKb11kmkZC-vjIjmwX-KrceujuXg5DtWoNKKSazVZ2wdi579s04VCzdNHhIyjGdoQtcKPnBvVL5lvYq4Brsi18jPkNekQGKdp4t3OrmvsTSayJ-m8P_4FPvE8LA9At7VukzIaj3EJ-EYJtNUvGOJ8j7HU-UAqIbxl-Of4Ulfa4gndWd_c-IKyvHNgXUlBTxa5ocFpR5j39MrSIYZ2jX8xUQzYcRoZW2w3mvXeETbOhHH2J4BzdkGLSQmZLGJtsYRKCI737LYKrN_iICcJvItUH0mzdr-0MA5cVEaKzqwD_2A7rq63XZL7pinxTQuvucrD3q76nE4NSo_bTyJtL7Pj2XNw4oD2F7N6Blb0D96nz0y92JzTy_WCXr--xY5PSEQIacyDQ99U7TH-_epctu0nxgFcQwfMYpQd7kmpW0dfx3r9eYDRnTExA4aGNr8a6R0405Xk_GCfiSltsGcAhTmcX7B5DaXMhtMvZgKppyqtZmqllraKWzFUQjuBrRLw--daMIYngX9I_mbh0_qwtmb_wEWXEKLmTyLA3VnGDFm8o941eQRb4ZM1apSBgq1ymdVXGjsk-Alc0tlwhQbpuavNaJyWDTCoT2-mgqVCeaaqPbYyhsWudRIQ6cCnJIzTyiAkSLZHLq-9HqmRB2AM-g4BhQwnPlOWcJq373OBXp8AhXH-o6Yjp6v7rcTmx475d84NLISae6gw2SuDuVhDb_sJY88bhbHQlr6OAToNnJQAZDT_Y1po1QKuExz9slSvbacDrkVdj9MspgXZkjYcknKOAV39jMVANRbC0QnX6OLHDs0vaAZSBvNajeZ1A_2t3qJnvZncdK9958K8enIb1Pqk-xEL9-aeim94JRNqUd_f3-K2VY_0G3lYs3LIPi_EbIbiCQOXn5t3v7DLAXfwi6lYsaLISHHUYAdCpOo9Srb8Naw2PbhirzWQZm9bFc9wlcvr3Zh),
        Julia Kreutzer, Isaac Caswell, Lisa Wang, Ahsan Wahab, Daan van Esch,
        Nasanbayar Ulzii-Orshikh, Allahsera Tapo, Nishant Subramani,
        Artem Sokolov, Claytone Sikasote, et al., ACL, 2022
        - Common Crawl include large portion of machine spam & porn
