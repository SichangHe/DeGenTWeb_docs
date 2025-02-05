# Ad Extraction

extracting&counting ad may help identify content farm

## Options for methods

- apply [EasyList](https://easylist.to/) CSS selectors on HTML (browser,
    JS enabled) using `lxml` or similar
    - [UW use this](literature.html#content-farm)
- Huanchen idea: turn Ad blocker on/off in browser & diff visual element
- use uBlock Origin logger when running browser
- use uBlock-Origin-compatible rule parser (e.g.,
    [adblock-rust](https://github.com/brave/adblock-rust)) & somehow

## ad classification

see [Analyzing the (In)Accessibility of
Online Advertisements](literature.html#content-farm)

most should be Google Ads
