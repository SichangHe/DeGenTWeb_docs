# LLM Site Features

## page features to extract

- prioritize top to bottom
- avoid features needing extra requests beyond the page crawl

### trivially computable now (single HTML, no extra requests)

- [x] #ads
- [x] #HTML bytes
- [x] #extracted text characters
- [x] #extracted text tokens
- [x] publication & last-modified date on page
- [ ] #outgoing links
- [ ] #domains in outgoing links
- [ ] external-link ratio
- [ ] #affiliate links
- [ ] affiliate-link ratio
- [ ] #CSS classes used
- [ ] #unique CSS classes
- [ ] whether HTML minified
- [ ] #forms
- [ ] #inputs
- [ ] #images in HTML
- [ ] image alt coverage
- [ ] canonical tag present
- [ ] #hreflang tags
- [ ] meta generator tag present
- [ ] #JSON-LD scripts
- [ ] schema.org type flags (Article/Product/FAQ/Breadcrumb)
- [ ] privacy/terms/contact link flags

### simple recrawl (single browser visit, still no extra requests)

- [ ] #total bytes
- [ ] #total requests
- [ ] #JS bytes
- [ ] #JS scripts fetched
- [ ] #CSS bytes
- [ ] #font bytes
- [ ] #font requests
- [ ] image stats: #requests, #bytes
- [ ] #third-party domains
- [ ] #third-party requests
- [ ] failed-request ratio
- [ ] redirect count
- [ ] #console errors
- [ ] #page errors

### later, more complicated (single browser visit)

- [ ] loading speed metrics: TTFB, DOMContentLoaded, onLoad, FCP, LCP, CLS,
    INP, TBT
    - implement: collect Navigation Timing + PerformanceObserver metrics in
        Playwright and save per crawl
- [ ] lighthouse metrics: performance, accessibility, best-practices, SEO
    - implement: run Lighthouse once after page load and
        persist category scores + key audits
- [ ] JS/CSS unused-byte ratio
    - implement: use Chrome DevTools Protocol coverage in Playwright;
        store used vs shipped bytes
- [ ] accessibility violation counts
    - implement: run axe-core or Lighthouse accessibility audits and
        store total + top rule counts

## site feature

### trivially computable now

- [ ] per-site median/IQR/deciles of each page feature
- [ ] per-site ad density metrics (ads per 1k tokens, ads per 100KB HTML)
- [ ] per-site affiliate/outgoing-link density
- [ ] per-site third-party footprint metrics
- [ ] per-site publication cadence (pages/week, median inter-publish gap,
    burstiness)

### later, more complicated

- [ ] intra-site template similarity score
    - implement: DOM skeleton hash per page, then median pairwise similarity
- [ ] #ad farm sites
    - [ ] define ad-farm programmatic signature
    - implement:
        rule score combining ad density + affiliate density + publication
        burstiness + low content diversity
