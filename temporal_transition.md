# Temporal Transition: Did Sites Switch to LLM Content?

## Question

Did existing sites produce non-LLM content before ChatGPT's launch and switch
to LLM content afterward, or did the LLM-dominant share grow mainly through
new sites? This doc records what we tried, why we moved to each approach, and
where the current evidence stands.

## Approaches tried (chronological)

### 1. GMM-based switch test (bimodality stats)

Script: `imc2026stats/report_imc2026_bimodality_stats.py`.

For bimodally-distributed sites (two Gaussian components in their Binoculars
score distribution), we fitted a GMM and assigned each page to a component.
Sites with strong negative correlation between publication date and Gaussian
component were candidate "switchers". Strict gates: ≥90% purity per segment,
≥0.6 delta, ≤365-day window, ≥8 pages per segment.

**Results:** 90 strict-switch sites (all datasets combined), 80 post-GPT, null
expected ≈ 0 (200:1+ ratio).

**Limitation:** Requires bimodal score distribution, so it misses sites that
adopted LLM content gradually or where scores are unimodal. Also complex to explain.

### 2. Cutoff-based complete-switch (current primary)

Script: `imc2026stats/report_imc2026_cutoff_switch_stats.py`.
Doc: `imc2026stats/report_imc2026_cutoff_switch_stats.md`.

Simple, threshold-free criterion: classify each page as LLM (bino < 0.9015)
or non-LLM, then check whether all non-LLM pages predate the first LLM page
(`complete_switch`). Minimum 4 pages per group.

**Results (all datasets):**
- 851 complete-switch sites, 801 post-GPT.
- Null expected: 4.32 (200:1 ratio, 0.03% null rate).
- CC-only: 619 total, 579 post-GPT, null expected 2.62, median cutoff 2023-08-20.

**Why this is used in the paper:** Simplest criterion, strongest signal,
easy to explain. The 0.03% null rate makes the paper claim robust.

**Limitation:** Strict — misses sites that adopted LLM content but still
published occasional non-LLM pages after the transition (hybrid). The
`hybrid` sub-class (≥4 non-LLM after cutoff) has a 57.6% null rate,
too high for strong claims.

### 3. SVM prediction-shift (exploratory, not primary)

Script: `imc2026stats/report_imc2026_prediction_shift_stats.py`.
Doc: `imc2026stats/report_imc2026_prediction_shift_stats.md`.

Uses the DeGenTWeb SVM applied to temporal page groups rather than per-page
threshold. Brute-force searches for the best split where pre-group is
SVM-classified as non-LLM-dominant and post-group as LLM-dominant,
maximizing `post_svm - pre_svm`.

Sub-classes:
- `pure_to_llm`: ≥80% LLM pages in post-group → 3,322 sites (18:1 over null 184).
- `pure_to_hybrid`: <80% but SVM says LLM-dominant → 9,961 sites (2.1:1, 35.1% null).

**Why not primary:** The 18:1 ratio is solid, but explaining an SVM applied to
temporal deciles is more complex than the threshold criterion. The earlier
"earliest valid split" variant had a 36.5% null rate (marginal splits near
decision boundary fired even pre-GPT); the "best split" variant is better.
The pure_to_hybrid result is too noisy for paper claims.

## Decision for IMC 2026 paper

Use **cutoff-based complete_switch** (CC dataset) as the primary claim:

> We find 579 CC sites where every non-LLM page predates the first LLM page
> (≥4 pages per group), with transition on or after ChatGPT's launch.
> Shuffling page dates produces ~2.6 such patterns by chance (null rate 0.03%).
> Median transition date: 2023-08-20.

TeX macros in `sync_dw1_figures/tex_stats_switching.py`: `CutoffCc*`.
Paper prose in `sections/wild.tex` (second `\agentadd{}` block after the GMM-based block).

## Open question

The GMM-based and cutoff-based methods agree on the direction but not magnitude
(90 vs 619 sites). The GMM result is more conservative because it requires
bimodal score distributions and tight purity gates. Whether to present both
or consolidate into one is an open editorial decision (`docs/notes/open_decisions.md`).
