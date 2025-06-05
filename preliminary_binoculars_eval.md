# Preliminary Binoculars Evaluation

- [x] dump English HTTP response from random Common Crawl WARC file
- [x] extract main text; if longer than 2000 character, feed into Binoculars
- ~~[ ] split long page down to Falcon-7B context window 2048 token~~
    just truncate
    - currently, simply truncate
    - ~~[ ] average score weighted on token count~~

script: `degentweb.common_crawl.classify_english `

result dumped to `data/common_crawl/prelim_test/`; 5961 page; used 1h 20m

## Manual inspection of low-score page among 1010 Common Crawl page

low-score page:

- ~19 seem indeed generate article, mostly blog & product
- 3 simply table-like listing
- 7 short listing/interaction page (scoreboard, links;
    only 2 are > 2000 character)
- boilerplate text: 7 cookie banner (< 2000 character); 1 legal notice
- 1 seem false positive
    <https://catalyticconvertersolutions.com/writer/nicolas-will/>

lower-score page (above FPR-threshold but around F1-threshold):

- many also seem generated, some not
    - 1 page error message (MySQL)
    - boilerplate text (legal)

## Case studies

- short listing/interaction page
    - site search result
        <https://newsroom.courts.ca.gov/search?t=Napa&sort=created&order=desc&keywords=&facets_query=&f%5B0%5D=content:event&f%5B1%5D=event_type:132&f%5B2%5D=event_type:202>
    - event listing
        <https://www.montananaturalist.org/events/list/page/20/?tribe-bar-date=2023-09-14>
- boilerplate text:
    - cookie banner from Trafilatura extraction issue
        - very short content
            <https://myscholarshipbaze.com/play-alphabet-earn-cet-vol-25/>;
        - non-English content
            <https://www.neske.hu/webshop/ekszerek/medalok/turkiz-levelkes-medal-nagy/>,
            <https://traczer.pl/fr/suplement_vet/>
- clearly generated
    - AI refusing to write article
        <https://educacion-especial.com/2023/03/12/a-beginners-guide-to-home-schooling-tips-and-resources/>
    - BS Ad <http://aloeecopark.com/kajabi-themes-for-sale/>

## Problem

- `filter_non_article.md` ~~listing/interaction page should not be in
    this study~~
    - cannot simply filter by markup ratio (link, button, etc.)
        bc some attach large description block
    - ❓ ML model to distinguish article
        - can base on BERT or BART
        - cannot ask LLM bc unreliable (tested)
    - ~~❓ `<meta property="og:type" content="article">` but
        not every article has this~~ tested, unreliable

## ~~Google~~ Bing 500 WikiHow articles

script: `degentweb.browser.bing_search` `degentweb.classifying.google_prelim`
`degentweb.classifying.prelim_data_analysis`

- ~~not running browser;~~ 20 Bing search result per query; ~~\~133 Google query~~
- some domain has many result w/ Binoculars score \< FPR threshold
    - [x] ~~tend to have `og:type` be `article`~~ seem not reliable
    - include many ad (business model: content farm + ad?)
        - e.g.,
            <https://www.solveyourtech.com> <https://gbtimes.com>
            <https://robots.net> <https://www.supportyourtech.com>
            <https://www.thetechedvocate.org> <https://citizenside.com>
            <https://www.live2tech.com> <https://www.madpenguin.org>
            <https://accountinginsights.org> <https://umatechnology.org>
            <https://www.clrn.org> <https://www.costumerealm.com>
            <https://www.neuralword.com> <https://www.simplymac.com>
            <https://www.gameslearningsociety.org/> <https://thetechylife.com/>
            <https://elevationvibe.com/>
            <https://ebestcourses.com/language/accent-reduction/>
        - [x] detect&count ad
    - seller/scam website boosting site rank in search engine w/ AI blog
        - e.g.,
            <http://www.androidphonesoft.com/> <https://dashboardsexcel.com/>
        - [ ] detect seller/scam website
    - clearly generated but unclear how they profit
        - e.g., wiki <https://freemwiki.com/wiki/%E9%A6%96%E9%A1%B5>,
            blog <https://www.thegadgetgazette.com/>
        - 💡 we are 100% sure a website is generated w/ ChatGPT w/o human
            review if they include something like `As an AI`
        - sitemap show they post too often:
            <https://bankbingo.com/> <https://accountingjournalentries.com/>
    - explicitly generated
        - sell solution for generating article <https://eulogygenerator.com/>
        - AI search <https://www.neuralword.com/>
    - spammy but unclear if generated (from late 2022)
        <https://sheetsland.com/>
    - [x] how are they ranked in search result?
        - some appear in multiple search. double count or take median?
        - stats show they rank similar to non-AI sites
- some clear false positive on some forum&support page
    - no `og:type` or have it be `webpage`
    - for false positive article, perhaps can filter by searching
        [training
        data](https://huggingface.co/datasets/tiiuae/falcon-refinedweb)
        - too much data (2TB) to search online, need local DB
    - 🤔 some like <https://www.geeksforgeeks.org/> are somewhere between
        content farm and educational site, w/ variable quality

## Site crawling

script: `degentweb.browser.visit_subdomains`

1. for each subdomain shown in search result, if \< 20 page crawled, then
    try finding sitemap w/ ultimate-sitemap-parser
1. if no sitemap, then query Wayback Machine (WM) Content Index API for
    last 2000 ok HTML response in the last 4 year
1. if found any page, then crawl (20 – \#already_crawled) page
