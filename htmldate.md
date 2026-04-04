# `htmldate`

This repo uses [`htmldate`](https://github.com/adbar/htmldate) to
extract page dates from HTML.

- direct wrapper: `degentweb_core/src/degentweb_core/dates.py`
- `trafilatura` integration: `trafilatura/trafilatura/metadata.py`
- pinned version in this workspace: `1.9.4` (`uv.lock`, installed package)

## What we use it for

Our wrapper parses HTML with `lxml` and calls `find_dates()` once.
It returns a `DateExtractionResult` with:

- `original` → publication-date candidate
- `modified` → last-modified candidate

Each side is a `DateProvenance(date, source, detail)` object, and
`DateSource` is now an int-backed public enum.

The compatibility wrapper `find_date()` still exists and returns a single
string date or `None`.

## What `find_dates()` actually does

At a high level, `find_dates()` loads HTML, builds extraction options, and then
tries a fixed sequence of increasingly loose signals.
`find_date()` is now a compatibility wrapper over that structured API.

### Input handling

- accepts HTML bytes, HTML string, an `lxml.html.HtmlElement`, or
    a URL string
- if given a URL string as the main input, it may download the page itself
- if `url=` is not passed, it also checks `<link rel="canonical">` and
    may use that URL for URL-based extraction
- validates the requested output format
- validates all candidates against `min_date` and `max_date`
    - default `min_date`: `1995-01-01`
    - default `max_date`: current time

## Extraction order in `htmldate` 1.9.4

This is the verified control flow in `find_dates()`.

1. **URL fast path.**
    - `extract_url_date(url, options)` looks for `YYYY/MM/DD`, `YYYY-MM-DD`,
        or `YYYY_MM_DD`-style dates in the URL.
    - by default, a valid URL date returns immediately
    - if `deferred_url_extractor=True`, this early return is disabled and
        the URL date is retried later as a fallback
1. **Header metadata first, then JSON only if header failed.**
    - `examine_header(tree, options)` scans `<meta>` tags,
        including common `name=`, `property=`, `itemprop=`, `pubdate`, and
        `http-equiv` date fields
    - examples include Open Graph, Dublin Core, `datePublished`,
        `dateModified`, `published_time`, `last-modified`, and related names
    - it keeps a lower-confidence reserve date in some cases, e.g.
        modified-vs- original mismatch or `copyrightYear`
    - only if header extraction returns nothing, `json_search()`
        checks `application/ld+json` or `application/settings+json` for
        `datePublished` or `dateModified`
1. **Deferred URL fallback.**
    - if URL extraction was deferred and a valid URL date exists,
        it is returned here
1. **`<abbr>` scan.**
    - checks `data-utime` Unix timestamps
    - checks `<abbr class="date-published">`, `published`, or
        `time published` and their `title`/text content
1. **Targeted DOM scan after pruning.**
    - removes some non-text-heavy elements such as `iframe`, `svg`, `video`,
        etc., and strips archive.org banner inserts
    - then searches elements whose `id`, `class`, or `itemprop`
        look date-like (`date`, `time`, `publish`, `footer`, `byline`,
        `submitted`, `fecha`, `parution`, ...)
    - then checks `.//title|.//h1`
    - then checks `<time>` elements, especially `datetime=`, `pubdate`,
        `entry-date`, `entry-time`, and `updated`
1. **Serialized-HTML rescue pass.**
    - looks for full timestamp strings like `YYYY-MM-DD hh:mm:ss`
    - tries `og:image` URL dates
    - tries language-specific prose patterns such as `published`, `updated`,
        `Veröffentlicht am`, and Turkish equivalents
1. **Late fallback only when `extensive_search=True`.**
    - scans short text segments from common text containers and
        keeps a best reference date across them
    - if that still fails, `search_page()` runs broader regex heuristics on
        the whole serialized HTML in this order:
        1. copyright year
        1. multiple 3-part numeric date patterns
        1. compact `YYYYMMDD`
        1. slash/dot numeric patterns
        1. `YYYY-MM`
        1. `MM-YYYY`
        1. multilingual month-name regex
        1. copyright year fallback
        1. year-only fallback

If none of these stages finds a valid date, the corresponding
`DateProvenance` is empty; `find_date()` therefore returns `None` for that
slot.

## How candidates are parsed and validated

- `htmldate` first tries cheap custom parsing for ISO-like and
    numeric formats
- only if needed, and only when `extensive_search=True`, it falls back to
    a slower external parser (`dateparser`) for text-like date strings
- all accepted candidates are validated against bounds before being returned
- when several candidates compete, selection is heuristic:
    - `original_date=True` prefers older validated candidates
    - `original_date=False` prefers newer validated candidates
    - frequency and plausibility filters are also used

This is why `original_date` should be read as a selection preference, not as
a completely separate extraction algorithm.

## What “fallback” means here

`htmldate` fallback is entirely internal to the same HTML/URL input.
It does not call outside services or use a separate network-based backup.

The main fallback layers are:

- defer from strong structured signals to weaker ones
- move from URL/meta/JSON to HTML elements and text
- when `extensive_search=True`, expand from targeted nodes to
    broader regex and free-text heuristics
- fall back from full dates to lower-granularity dates like `YYYY-MM` or
    even `YYYY-01-01`

Lower-granularity fallbacks can reduce precision.
For example, `YYYY-MM` becomes the first day of that month, and
year-only fallback becomes January 1 of that year.

## Repo-specific notes

- `degentweb_core/src/degentweb_core/dates.py`
    always passes `extensive_search=True` and the page URL, so
    we opt into the broad fallback path on every call.
- `src/degentweb/sql/migrations/v12.sql` stores
    `publication_date_source` and `last_modified_date_source` as `SMALLINT`.
- `trafilatura/trafilatura/settings.py:set_date_params()` defaults to:
    - `original_date=True`
    - `extensive_search=<config>`
    - `max_date=today`
- `trafilatura/trafilatura/meta.py` exposes `reset_caches()` support for
    `htmldate`'s internal LRU caches.

## Practical takeaways

- Passing the real page URL matters because URL extraction runs very early by
    default.
- `extensive_search=True` improves recall, but it is explicitly a looser,
    more heuristic fallback mode.
- A returned date is only “best validated candidate”, not proof that
    the page declared publication and modification dates cleanly.
