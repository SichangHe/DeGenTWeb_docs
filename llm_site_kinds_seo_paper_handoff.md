# LLM Site Kinds — SEO Argument Paper-Integration Handoff

Complete handoff for the *"LLM SEO lead is a thin-site selection effect,
not content quality"* argument pushed into the IMC 2026 paper on
2026-04-21. Everything needed to verify, reproduce, extend, or
withdraw the numbers is reachable from this doc in at most one hop.

**Read this doc in layers.** §1 is the argument. §2 is the pipeline.
§3 is every file that matters. §4 is "how do I rerun this". §5 is
"how do I change the numbers". §6 is pointers to every related doc.
§7 is caveats. §8 is follow-ups.

## §1 Argument (one paragraph)

The cohort-wide Lighthouse SEO-score advantage of LLM-dominant
live-fetch sites (median 1.00 vs 0.92; perfect-SEO share
**51.4 %** vs **39.9 %** of 2,237 vs 1,342 sites) is driven entirely
by thin, un-optimized LLM sub-groups. On sites with no dedicated SEO
plugin the gap is **54.1 % vs 38.8 %** (+15.3 pp); on
Yoast-SEO-using sites the two sides are tied at **43.3 %** vs
**41.8 %**; on professionally-operated categories the humans lead
modestly (retail e-commerce **35.0 % vs 37.5 %**, SaaS **46.9 %
vs 49.1 %**, affiliate-SEO blogs **40.8 % vs 42.2 %**). Lighthouse
SEO measures template basics that a default CMS install satisfies
for free, so the cohort-wide lead is a footprint of rapid
deployment, not superior on-page optimization.

Numbers and their framing are persisted in
[`llm_site_kinds_paper_findings.md`](../llm_site_kinds_paper_findings.md)
§F4 (headline + tables + caveats).

## §2 End-to-end data flow

Five stages. Each arrow is a single script invocation.

```
DuckDB session
  data/classify/llm_site_kinds/duckdb_session/20260418_112640.duckdb
        │  (tables: page_html_signals, page_lighthouse,
        │   page_wappalyzer, page_categorizations)
        ▼
src/degentweb/classifying/llm_site_kinds_paper_plots.py  [DW1 repo]
  _write_seo_by_group_stats() runs SQL, writes KEY=VALUE
        ▼
data/classify/llm_site_kinds/llm_site_kinds_seo_by_group_stats.txt
  16 lines:  LH_SEO_PERFECT_{AI,HUMAN}_COUNT / _TOTAL / _PCT
             LH_SEO_PERFECT_{NOPLUGIN,YOAST,RETAIL,SAAS,AFFSEO}_{AI,HUMAN}_PCT
        ▼
imc2026stats/report_imc2026_stats.py  [DW1 repo]
  _extract_llm_site_kinds_seo_stats() reads the file, prints to stdout
        ▼
sync_dw1_paper_figures.py  [writeup repo]
  TEX_STAT_VARS entries map stat keys → \LhSeoPerfect* macros;
  rewrites placeholders in degentweb_imc2026.tex in place.
        ▼
degentweb_imc2026.tex  [writeup repo]
  \newcommand{\LhSeoPerfectAiPct}{51.4}   (etc.)
  §"SEO Signals" paragraph uses the macros.
```

Staging is deliberate: upstream stats are full-precision floats;
the writeup controls formatting (`.1f` for percentages) via
`FloatStatVar(format_spec=...)`, so changing the rendered
precision does not require a re-run of the DW1 analysis.

## §3 Every file involved

Two repos are in play. `DW1` is the code repo
(`/ssd1/sichanghe/dw_agent0` or any sibling clone). `writeup` is
Overleaf-synced paper repo (`/ssd1/sichangheagent/DeGenTWeb_writeup`).

### §3.1 DW1 repo

| Path | Role |
| --- | --- |
| `src/degentweb/classifying/llm_site_kinds_paper_plots.py` | Writes the stats file and the three F-section paper figures. Function `_write_seo_by_group_stats()` is the only piece that contributes to the SEO argument; it runs one SQL query and writes KEY=VALUE to `SEO_STATS_PATH`. |
| `data/classify/llm_site_kinds/duckdb_session/20260418_112640.duckdb` | Persistent DuckDB session with the four raw tables used by the SQL. Captured on 2026-04-18 and pinned into the script by path. |
| `data/classify/llm_site_kinds/llm_site_kinds_seo_by_group_stats.txt` | 16-line KEY=VALUE output of `_write_seo_by_group_stats()`. Committed as an artifact so downstream does not need the DuckDB session. |
| `imc2026stats/report_imc2026_stats.py` | Defines `LLM_SITE_KINDS_SEO_STATS` path and the `_extract_llm_site_kinds_seo_stats()` extractor. Invoked by the writeup's sync script. |
| `llm_site_kinds_paper_findings.md` (at PWD) | Paper-ready findings for all of F1–F4. §F4 contains the full SEO discussion with tables that mirror the macros in this handoff's §1. |
| `docs/llm_site_kinds.md` | Long-form cluster-by-cluster discussion. Arg 4.4 context lives here. |
| `docs/llm_site_kinds_tech_ref.md` | Vendor / product citations for every ad-tech / SEO-plugin / CMS name mentioned (Yoast, Rank Math, Ezoic, etc.). Cite from here when writing prose. |
| `codebase_index/llm_site_kinds_analysis.md` | Index of the upstream analysis script and its DuckDB session contents; start here if you need to understand how `page_html_signals` etc. were built. |

### §3.2 Writeup repo

| Path | Role |
| --- | --- |
| `sync_dw1_paper_figures.py` | Calls `report_imc2026_stats.py` and rewrites TeX placeholders. The 16 `LhSeoPerfect*` entries in `TEX_STAT_VARS` are the mapping stat-key → macro name + format. |
| `degentweb_imc2026.tex` | Declares `\newcommand{\LhSeoPerfect*}{placeholder}` at the preamble; the SEO-Signals subsection body contains the filler paragraph that uses them. |
| `docs/notes/dw1_sources.md` | Where each paper number comes from in DW1 (tag or stats file). |
| `docs/notes/tex_stat_vars_formatting.md` | Macro naming rules (letters-only, no embedded digits), formatting conventions (`.1f` for abstract percentages), and instructions for adding new stats. |
| `AGENTS.md` | Cross-repo workflow rules; "pull autostash rebase before editing; push after editing, for both this repo and the code repo". |

## §4 How to reproduce the numbers

### §4.1 Fastest path — trust the stats file

```sh
# From writeup repo, with DW1 clone at ../dw1:
python3 sync_dw1_paper_figures.py
# Produces: updated \newcommand{\LhSeoPerfect...}{...} lines in
# degentweb_imc2026.tex; confirm via `grep LhSeoPerfect *.tex`.
```

This path reads only the committed stats file; it does not touch the
DuckDB session. Use it when you pulled new DW1 numbers or changed
formatting and want to re-render the TeX.

### §4.2 Full path — regenerate the stats file from DuckDB

```sh
# From DW1 repo root:
source .venv/bin/activate
uv run python src/degentweb/classifying/llm_site_kinds_paper_plots.py
# Prints: "Wrote 3 plots and 1 stats file under data/classify/llm_site_kinds/"
# Also regenerates the three F-section PNG/PDF figures.
```

Confirm the stats file:

```sh
cat data/classify/llm_site_kinds/llm_site_kinds_seo_by_group_stats.txt
```

Then rerun §4.1.

### §4.3 Reading the raw DuckDB

If someone challenges a number, the underlying SQL is
inlined in `_write_seo_by_group_stats()` and uses only these
tables (all persisted in the DuckDB session):

- `page_html_signals` — per page, per-detector HTML-substring
  boolean flags + the site's label (`llm_like` / `human_like`).
- `page_lighthouse` — per page, Lighthouse scores.
- `page_wappalyzer` — per page, detected technologies.
- `page_categorizations` — per subdomain, latest category slug.

The SQL partitions on three axes: SEO-plugin presence
(Yoast-or-premium / Rank Math), `n_ads` (via the bucketed view), and
category slug. Counts and perfect-SEO shares are computed per label.

## §5 How to change the numbers

### §5.1 Change the threshold or the groups

Edit `_write_seo_by_group_stats()` in
`src/degentweb/classifying/llm_site_kinds_paper_plots.py`:

- The perfect-SEO cutoff is hard-coded at `seo >= 0.995`. Move it if
  the paper argues a different cutoff.
- The sub-groups are hard-coded in the CTE (Yoast-or-premium,
  Rank Math, three category slugs, plus no-plugin derived by
  negation). Add new groups by adding new `SUM(CASE WHEN ...)`
  columns and emitting matching `LH_SEO_PERFECT_<NAME>_{AI,HUMAN}_PCT`
  lines.

### §5.2 Add a new macro

Three edits in lock-step:

1. **DW1 extractor:** ensure the key appears in the stats file AND
   `_extract_llm_site_kinds_seo_stats()` returns it (it does; the
   extractor just parses KEY=VALUE).
2. **Writeup sync:** add a `FloatStatVar("LhSeoPerfect<Name>AiPct",
   "LH_SEO_PERFECT_<NAME>_AI_PCT", ".1f")` (and the human twin) to
   `TEX_STAT_VARS` in `sync_dw1_paper_figures.py`. Follow the
   letters-only / no-digits macro naming rule from
   `docs/notes/tex_stat_vars_formatting.md`.
3. **Paper:** add a `\newcommand{\LhSeoPerfect<Name>...}{0.0}`
   placeholder at the preamble of `degentweb_imc2026.tex` and use
   the macro where needed.

Run `sync_dw1_paper_figures.py` after each edit.

### §5.3 Change formatting only

If the paper needs (say) 2-decimal precision instead of 1, flip the
`format_spec` argument on the relevant `FloatStatVar` in the sync
script and re-run. No DW1 recomputation needed.

## §6 Cross-reference map

Walk this tree when you need context beyond what this handoff shows.

### §6.1 For "what does the argument say"

- **[`llm_site_kinds_paper_findings.md`](../llm_site_kinds_paper_findings.md)** §F4 — headline, per-group tables, paper-framing paragraph, caveats. Authoritative for the argument.
- **[`docs/llm_site_kinds.md`](llm_site_kinds.md)** — long-form cluster story; older framing that §F4 supersedes but that is still useful context on what "kinds" mean and how the KMeans fit was done.

### §6.2 For "where do the vendor names come from"

- **[`docs/llm_site_kinds_tech_ref.md`](llm_site_kinds_tech_ref.md)** — primary/secondary URLs for every tech name in §F2 and §F4 (Yoast, Rank Math, Ezoic, Mediavine, Raptive, ConvertKit, etc.). Cite from here rather than writing in the paper.

### §6.3 For "how was the DuckDB session built"

- **[`codebase_index/llm_site_kinds_analysis.md`](../codebase_index/llm_site_kinds_analysis.md)** — schema of `page_html_signals` / `page_lighthouse` / `page_wappalyzer` / `page_categorizations`; how `llm_site_kinds_analysis.py` fills the session (tags, detection logic, bucket rules).

### §6.4 For "how the writeup repo absorbs DW1 numbers"

- **`../DeGenTWeb_writeup/docs/notes/dw1_sources.md`** — source-of-truth map; what each paper claim cites. This handoff's §3.2 entries should eventually land there as a new line under "SEO / live fetch".
- **`../DeGenTWeb_writeup/docs/notes/tex_stat_vars_formatting.md`** — macro-naming and formatting conventions. Consult before adding new macros.

## §7 Caveats and limitations

The argument is defensible at the 0.995 threshold on site-level
median SEO. The following caveats apply:

- **Binarization threshold.** The 0.995 cutoff rounds *any* score
  of 1.00 into "perfect". Alternative cutoffs (0.95, 0.90)
  preserve the direction of every gap but change magnitudes. The
  raw per-site medians stay in `page_lighthouse`; recompute if a
  reviewer challenges the threshold.
- **Category boundaries.** Category slugs are assigned by the
  Bedrock categorization pipeline; they are not perfectly
  reliable. `retail_ecommerce` excludes sites that Bedrock classed
  as `business_service_operator` that happen to have a shop; the
  §F4 "humans lead in retail e-commerce" claim uses the
  Bedrock-defined boundary.
- **Yoast + Rank Math coverage.** Wappalyzer-side detection misses
  self-hosted or proxied copies of these plugins. The "no-plugin"
  sub-group over-counts sites whose plugin we failed to detect.
- **Cohort size.** The smaller category rows (SaaS n=64 LLM / 55
  human, retail 140/80, affiliate-SEO 250/109) are enough for a
  direction-of-effect claim, not for a precise magnitude.
- **Metric is on-page only.** Lighthouse SEO does not include
  ranking signals. Actual search ranking / click-through is out of
  scope; the argument only says *"the Lighthouse lead is a
  template effect."*

## §8 Open follow-ups

Listed in descending priority. Each could be done as its own
short PR.

1. **Paper figure for F4.4.** Horizontal bar of
   (LLM − human perfect-SEO share, pp) across ~8 thin-side and
   ~6 cultivated-side groups, sorted by gap. Would turn the
   current paragraph into a one-figure finding. Mechanism:
   extend `llm_site_kinds_paper_plots.py` with
   `_plot_seo_gap_by_group()` following the existing
   `_plot_tech_bias` pattern; add a `CopySpec` in the writeup
   sync. No new macros needed.
2. **Add SEO handoff entry to writeup's `dw1_sources.md`.** Currently
   the only "SEO / live fetch" line in that doc points at the older
   p50/min ECDF artifacts. Add a line pointing at
   `llm_site_kinds_seo_by_group_stats.txt` and this handoff.
3. **Robustness check on the 0.995 threshold.** Emit three stats
   files at 0.995 / 0.95 / 0.90 thresholds and document that the
   direction is stable. Low effort; high defensibility.
4. **Persist the full by-group table as a DuckDB table** (so the
   stats file becomes `SELECT * FROM seo_by_group`). Not strictly
   needed while the pipeline is a single script; would matter if a
   second consumer appears.
5. **Cross-reference §F4 with §F1 clusters.** Does the Ezoic
   content-farm kind from F3 fall on the thin or cultivated side of
   §F4? Currently ambiguous in the doc.

## §9 Commit record (2026-04-21)

Two repos pushed:

- **DW1 `main`:**
  - `3c5c369` *feat(stats): emit llm_site_kinds SEO-by-group stats file*
    — adds `_write_seo_by_group_stats()` and extractor.
  - `71dc981` *docs(llm_site_kinds): replace F4 SEO hand-wave with
    per-group breakdown* — rewrites F4.4 in the findings doc.
  - `4394f4a` *docs(llm_site_kinds): explain SEO score gap in F4*
    — superseded by 71dc981.
- **Writeup `master`:**
  - `cd5cf79` *paper: qualify SEO lead as a thin-site selection
    effect* — adds the 16 `LhSeoPerfect*` macros, the filler
    paragraph in SEO Signals, and the sync registrations.

Both branches are up to date with their remotes. The working trees
are clean except for linter-reformat ripples on unrelated files;
none are owned by this task.

## §10 What this handoff doc is *not*

- Not the paper argument — that is
  [`llm_site_kinds_paper_findings.md`](../llm_site_kinds_paper_findings.md)
  §F4. If the numbers differ between the two, trust §F4.
- Not the script documentation — that is
  [`codebase_index/llm_site_kinds_analysis.md`](../codebase_index/llm_site_kinds_analysis.md)
  for the upstream analysis and the docstring of
  `_write_seo_by_group_stats()` for this pipeline's specific SQL.
- Not the vendor citation reference — that is
  [`docs/llm_site_kinds_tech_ref.md`](llm_site_kinds_tech_ref.md).
- Not the writeup-repo conventions — those are in
  `../DeGenTWeb_writeup/docs/notes/tex_stat_vars_formatting.md`
  and `../DeGenTWeb_writeup/docs/notes/dw1_sources.md`.

This doc glues the above into a single reproducible pipeline.
