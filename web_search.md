# Web Search

## Google

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
