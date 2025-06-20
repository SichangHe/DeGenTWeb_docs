# Execution

(code and discussion are taken private; please ask Steven for repo access)

see also `arguments.md` and `literature.md`

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

## Development

- clone w/ `--recurse-submodules` and remember to update submodules on pull
    - automatically do these w/
        [these Git
        config](https://sichanghe.github.io/notes/programming/git.html#config)
- use [Rye](https://rye.astral.sh/) to manage Python dependencies
    (`rye sync`, `rye add`)
    - note: some dependency like `nvidia-cuda-runtime-cu12` version for
        Binoculars are unfortunately hardcoded for Exxact; need to change if
        used on other machine
- install `uv` and `maturin[patchelf]`:

    ```sh
    rye install uv
    rye install maturin
    rye install patchelf
    ```
- [install Rust](https://www.rust-lang.org/tools/install)
- register [Pre-commit Hook](https://pre-commit.com/) to run linters and
    formatters automatically before Git commit:

    ```sh
    . venv/bin/activate # if not in Rye's virtual env
    pre-commit install
    ```
- run `. static_checks.sh` before making pull request
