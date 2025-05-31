# Web Search

## Google

(following are deprecated, from web-based crawling)

- main result: `a:has(h3)` w/ `jsname`, `href`, `data-ved`, `ping` and
    no other attribute
    - main result may be video, then it has additional `a:has(svg)`
        w/ same `href`
    - 💡 can filter video result by rm `href` from `a:has(svg)`
- `Discussions and forums`: same as main result except has `class` and
    does not contain `h3`
- related result under a main result (e.g., Reddit): has only `class`,
    `href`, `ping`
- `Videos`: same as main result except has `class`, `aria-label`, etc.
    and does not contain `h3`
- `What people are saying` (TikTok, etc.): same as main result except
    has `class` and does not contain `h3`
- ❓ Google sometimes also display time of publish; useful?

- ~~[ ] ❓ Google blocked our IPv6 address; why are we on IPv6?~~

## Bing

just use API

## [SearXNG](https://docs.searxng.org/) (SearX successor)

- privacy-focused meta search engine to aggregate search results
- [subreddit](https://www.reddit.com/r/Searx)
    [instances](https://searx.space/)
- evidence people don't want AI result
    - [Integrating LLMs into search (link prediction, top-site summarization,
        stable diffusion images, academic articles)
        #2163](https://github.com/searxng/searxng/issues/2163#issuecomment-1752087912)
    - [\[Feature\] exclude / filter domains from results (client side)
        #2351](https://github.com/searxng/searxng/issues/2351)
- plugin to filter website: [Filter URLs
    example](https://docs.searxng.org/dev/plugins/development.html#filter-urls-example)
