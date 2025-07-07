# Execution

(code and discussion are taken private; please ask Steven for repo access)

see also `arguments.md` and `literature.md`

for development, see `development.md`

## Overall steps

- [ ] improve ground truth & get robust classifier
    - ~~[ ] find additional topics beyond blog posts to
        generate websites/ find tools to generates similar to existing~~
        - [x] \~100 human/AI websites baseline and still do well
    - limitations of Binoculars
    - [x] apply to 10,000 websites in the wild
        - [ ] check if doing well
- [ ] apply broadly to websites in the wild?
    - ways to discover them
- [ ] determine why they do this (money/misinformation)?

## Preliminary

- [x] run Binoculars over Common Crawl; see if
    result make sense (`preliminary_binoculars_eval.md`) *edit*: …
    and WikiHow search result

## Keyword acquisition

- WikiHow article titles (`wikihow.md`)
- ~~[ ] from Google Trends (`google_trends.md`)~~
    - Google completion?
- ~~get topic class from Google Trends~~
- ~~[ ] human brainstorm related keywords~~

## Web searching and crawling

`web_search.md`

- [ ] search Google/Bing/Brave/Perplexity/ChatGPT/ChatNoir
- [x] crawl top 20 results/reference
- [x] extract body text
    - ~~DOM Distiller Reading Mode~~
    - [Trafilatura](https://github.com/adbar/trafilatura)

## Generated text detection

- ~~[ ] filter out non-article (`filter_non_article.md`)~~
    rely on \#tokens filtering & low probability of getting many title pages
- ~~[ ] text cleaning~~ cleaned by Trafilatura
- Binoculars
    - [x] speed enhancement for large scale
- [ ] get powerful processor

## Case studies

- [ ] what are those website w/ many "positive" page
    - content farm w/ many ad (`ad_extraction.md`)
    - content farm selling product
        - [ ] identify scam seller
            - ~~perhaps use
                [blacklist](https://dsi.ut-capitole.fr/blacklists/index_en.php)
                used [by RefinedWeb](literature.html#training-data-curation)~~
                few matches
    - false positive: forum/support
- [ ] what are those "positive" page
    - [x] manual inspection
    - [ ] clustering
