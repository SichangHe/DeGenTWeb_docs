# Ad Extraction

extracting&counting ad may help identify content farm

## Options for methods

- (currently implemented) apply [EasyList](https://easylist.to/)
    CSS selectors on HTML (browser, JS enabled) using `lxml` or similar
    - [UW use this](literature.html#content-farm)
    - [x] only count elements w/ content → `n_non_empty_ads`
    - use bounding box?
- Huanchen idea: turn Ad blocker on/off in browser & diff visual element
- use uBlock Origin logger when running browser
- use uBlock-Origin-compatible rule parser (e.g.,
    [adblock-rust](https://github.com/brave/adblock-rust)) & somehow

## Browser operation

to load all ad, scroll to the bottom and top, 20 time combined,
each time wait for `networkidle` (in `degentweb.browser.save_page`)

- some ad load slowly
- some ad load after a timeout
- some ad load after user interaction

re-crawled all 0-ad page after adjusting browser interaction w/
`degentweb.browser.recrawl_no_ads`

## Ad classification

see [Analyzing the (In)Accessibility of
Online Advertisements](literature.html#content-farm)

most should be Google Ads

## Case study

- extreme page w/ 443 ads:
    <https://www.minimizemymess.com/blog/types-of-dresses>
    - long; scrollable ad banner at the top; different sidebar ads when
        scrolling
