# Lighthouse SEO score

**Human summary**: checks if the pages

- blocks bot crawling per metadata, response header, or robots.txt;
- has `<title>` element;
- has `<meta name="description">` with non-empty content;
- returns successful HTTP status;
- has descriptive link text;
- has crawlable anchor `href`s;
- has valid robots.txt (if present);
- has `alt` attributes on images;
- has valid `hreflang` links (if any);
- properly declares canonical URL (if any).

Then, weighted average of applicable checks

---

(generated according to lighthouse@13.0.3 code)

`lhr.categories.seo.score` is a weighted arithmetic mean of 10 binary audits.
Each audit scores either 0 or 1; no partial credit.
The final score is rounded to 2 decimal places.

## Weighted mean formula

```
score = sum(audit_score * weight) / sum(weight)
```

Only audits with `weight > 0` contribute.
An audit's weight is zeroed out at runtime if it is `notApplicable`,
`informative`, or `manual`; it is then excluded from both numerator and
denominator.

## Audit weights (from `core/config/default-config.js`)

```
is-crawlable       93/23 ≈ 4.04   (≥31% of total by design)
document-title         1
meta-description       1
http-status-code       1
link-text              1
crawlable-anchors      1
robots-txt             1
image-alt              1
hreflang               1
canonical              1
structured-data        0   (manual, never counts)
```

Total weight when all applicable: 93/23 + 9 = 300/23 ≈ 13.04.
The `is-crawlable` weight was chosen so that
failing it alone pushes the category below 0.69 (i.e.,
guarantees an overall "failing" category score).

## Individual audit pass/fail conditions

All audits below return 1 (pass) or 0 (fail) unless noted.

`is-crawlable` — navigation mode only.
Fails (score=0) only if *all* of the following user-agents are blocked from
crawling the page: generic (`*`/`robots`), `Googlebot`, `bingbot`,
`DuckDuckBot`, `archive.org_bot`. Blocking sources checked:
- `<meta name="robots">` or `<meta name="<agent>">` containing `noindex`,
    `none`, or a past-dated `unavailable_after:<date>`.
- `X-Robots-Tag` HTTP response header with the same directives.
- `/robots.txt` disallowing the URL for that user-agent.

Passes (score=1) if any one of the five user-agents remains unblocked.
Warns (but still passes) if some bots are blocked while others are allowed.

`document-title` — axe-core rule. Fails if the page has no `<title>` element.
`notApplicable` if axe found no nodes matching the rule (weight zeroed).

`meta-description` — Fails if `<meta name="description">` is absent or
its `content` is empty/whitespace-only.

`http-status-code` — navigation mode only.
Fails if the main document HTTP status is 400–599.

`link-text` — Fails if any `<a href>` link (excluding `nofollow`,
`javascript:`, `mailto:`, and same-page fragment links)
has text matching a hardcoded non-descriptive-phrase list (e.g., "click here",
"read more") in one of 8 supported languages (en, ja, es, pt, ko, sv, de, ta,
fa).

`crawlable-anchors` — Fails if any anchor element has an uncrawlable `href`:
`javascript:void(0)`, empty string, `file:` URLs, or an `href` that
cannot be resolved to a valid URL.
Anchors acting as id-only targets (`<a id="x">`) and `mailto:`
links are exempt.

`robots-txt` — Fetches `/robots.txt`.
- Returns `notApplicable` (weight=0) if status is 4xx or content is empty
    (no robots.txt is not an error).
- Fails (score=0) if fetch completely failed (no status) or status is 5xx.
- Parses the file and fails if any line has a syntax error:
    unknown directive, `allow`/`disallow` before a `user-agent`,
    bad sitemap URL, missing user-agent value, or patterns not starting with
    `/` or `*` (unless empty).

`image-alt` — axe-core rule. Fails if any `<img>` lacks an `alt` attribute.
`notApplicable` if the page has no images.

`hreflang` — navigation mode only.
Checks all in-head/HTTP-header `<link rel="alternate" hreflang="...">`
elements. Fails if any has:
- an invalid language code (not a valid BCP-47 language subtag or
    `x-default`), or
- a non-fully-qualified (relative) `href`.

Passes if there are no such links at all (score=1, not `notApplicable`).

`canonical` — navigation mode only.
Checks `<link rel="canonical">` in `<head>` and HTTP `Link:` headers. Fails if:
- any canonical `href` is not a valid absolute URL,
- any canonical `href` is relative (resolves but raw value is not absolute),
- multiple differing canonical URLs are declared,
- the canonical points to a different URL listed in `hreflang`
    alternates (cross-language canonical mistake), or
- the canonical points to the site root (`/`) while the page is not the root.

Returns `notApplicable` (weight=0) if no canonical link is present at all.

`structured-data` — always weight=0 (manual). Never affects the score.
