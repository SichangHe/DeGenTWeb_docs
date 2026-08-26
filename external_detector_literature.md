# External AI-text detector and duplicate-filter evidence

Sources and prices were checked on 2026-08-25. This note contains public-source
findings and experiment-design recommendations only. Vendor accuracy numbers are
vendor-reported unless an independent study is named.

## Pangram pricing and method

Pangram's current Developer API prices are:

- Pangram 4: $0.05 per 100 words, or $0.04 with the Bulk API's 20% discount.
- Pangram 3: $0.05 per 1,000 words, or $0.04 with the Bulk API discount.
- Each Pangram 4 scan is billed in 100-word units. Pangram says, "One credit
  equals 100 words, rounded up to the next 100." Thus 101 words costs two
  credits, not 1.01 credits.
- The self-serve API limit is 5 queries per second. Pangram invites
  noncommercial academic projects to request research credits.
- Seat subscriptions are not a substitute for programmatic evaluation:
  Pangram says API access is not included in the Free, Individual,
  Professional, or Teams plans.

Authoritative sources: [pricing](https://www.pangram.com/pricing),
[credit rounding](https://www.pangram.com/knowledge-hub/what-is-an-ai-detection-credit),
[Developer plan](https://www.pangram.com/knowledge-hub/what-is-pangrams-developers-plan),
and [API limits, bulk discount, and research credits](https://www.pangram.com/solutions/api).

For Pangram 4, the reproducible preflight estimate for page-level scoring is:

```text
realtime dollars = 0.05 * sum_over_pages(ceil(page_words / 100))
bulk dollars     = 0.04 * sum_over_pages(ceil(page_words / 100))
```

The published Pangram 4 architecture is an open-weight mixture-of-experts
backbone with classification heads. It performs classifier inference on the
submitted text; it does not rewrite every submitted text. Pangram uses synthetic
mirroring and editing in training-data construction. This distinction matters
when comparing runtime and mechanism with rewrite-based detectors. See the
[Pangram 4 technical report](https://arxiv.org/abs/2607.27183) and the
[original Pangram report](https://arxiv.org/abs/2402.14873).

One independent, web-focused preprint compared Pangram v3 with Binoculars,
Desklib, and DivEye before using Pangram on Internet Archive samples. Its small
robustness study favored Pangram v3 for the authors' HTML, language, and model-
family tests, but it does not establish Pangram 4 performance on the DeGenTWeb
baseline. It supports doing a matched local comparison, not importing its
conclusion. See [The Impact of AI-Generated Text on the Internet](https://arxiv.org/abs/2604.26965).

## Detector families and suitability

| Method | What it does at inference | Calibration and main constraint | Suitability for the same baseline pages |
| --- | --- | --- | --- |
| Binoculars (ICML 2024) | Divides observer-model perplexity by observer/performer cross-perplexity; no generated rewrite | Zero-shot global thresholds, two related language models, and two forward evaluations. The paper's greater-than-90% TPR at 0.01% FPR is scoped to its benchmarks, and the paper cautions that it did not test deliberate bypass attacks. | Keep as the existing open reference, but report locally calibrated and fixed published thresholds separately. [Paper](https://proceedings.mlr.press/v235/hans24a.html) |
| RAIDAR (ICLR 2024) | Rewrites once, computes edit-distance features, then applies logistic regression or XGBoost | Needs labeled training data and a fixed rewrite model/prompt. The paper says, "There is no single prompt that performs best across all data sources." Its released GPT-3.5-Turbo setup now requires a documented model substitution. | Best simple, canonical rewrite baseline. Train only on training sites and freeze prompt, rewrite model, and classifier before evaluating held-out sites. [Paper](https://openreview.net/forum?id=bQWE2UqXmf), [code](https://github.com/cvlab-columbia/RaidarLLMDetect) |
| Learn-to-Distance, L2D (ICLR 2026) | Generates multiple rewrites, then uses a learned distance between original and rewritten text | Public checkpoint uses Gemma-2-9B-IT; experiments use four rewrites. The paper calls computational cost "relatively high" and reports experiments on a 96 GB H20 GPU. | Strongest newer rewrite candidate with public code and checkpoint, but use only if the GPU/runtime budget permits. Keep site-level training/test separation if adapting it. [Paper](https://openreview.net/forum?id=2ZUPeEM3FH), [code](https://github.com/Mamba413/L2D) |
| DNA-GPT (ICLR 2024) | Truncates the input and generates continuations, then compares n-gram overlap | The paper recommends 5-10 regenerations and notes that an unknown source model needs a proxy. This is regeneration-based rather than a full-text rewrite detector. | Useful optional stress test, but less natural for sites produced by unknown, mixed generators and much more generation-heavy than Binoculars. [Paper](https://openreview.net/forum?id=Xlayxj2fWp), [code](https://github.com/Xianjun-Yang/DNA-GPT) |
| Learning to Rewrite, L2R (ACL 2025) | Fine-tunes an 8B model to rewrite AI text less than human text | Requires QLoRA training and autoregressive generation. The public repository found in this review contains data, not a turnkey released detector. | Defer unless the model/checkpoint becomes reproducible; it adds implementation risk without a clean off-the-shelf comparison. [Paper](https://aclanthology.org/2025.acl-long.322/), [data](https://github.com/ranhli/l2r_data) |
| MAGRET (COLING 2025) | Combines model rewrites with learned semantic and statistical features | Needs closed-model API rewrites plus trained encoders/classifiers; the paper notes continuing API payments. No official runnable detector was located in this review. | Defer for the bounded baseline comparison. [Paper](https://aclanthology.org/2025.coling-main.557/) |

A minimum mechanism-diverse comparison is Binoculars, Pangram 4, and RAIDAR.
L2D is the best justified extension if compute permits. DNA-GPT should be labeled
as regeneration-based rather than rewrite-based.

For a fair comparison:

1. Use the same frozen page cohort and source extraction for every detector, and
   record the exact text each method scores. The current Binoculars path caps an
   input at 2,048 Binoculars tokens, while Pangram can score a longer document in
   windows. Therefore either send both methods the exact same Binoculars-capped
   text in a comparable-input analysis, or call a method-native full-page result
   non-identical. Prefer reporting the comparable-input result plus a clearly
   labeled method-native sensitivity result.
2. Freeze the site-level split before fitting any RAIDAR/L2D parameters or
   thresholds. Never split pages from one site across train and test.
3. Freeze rewrite prompts, model versions, sampling settings, and number of
   rewrites. Record generated tokens, wall time, GPU time, and API cost.
4. Report page-level and site-level metrics, including false-positive rate on
   human sites. Do not compare each method at a separately optimized test-set
   threshold.
5. Treat current Pangram claims, published detector benchmark claims, and local
   baseline measurements as three separate evidence classes.

The [DetectRL benchmark](https://proceedings.neurips.cc/paper_files/paper/2024/hash/b61bdf7e9f64c04ec75a26e781e2ad51-Abstract-Datasets_and_Benchmarks_Track.html)
is further reason to preserve this local evaluation: it documents substantial
degradation of several zero-shot detectors under real-world perturbations.

## The 50% same-subdomain duplicate cutoff

No direct published precedent was found for the project's exact rule after
bounded Google Scholar and web searches for combinations of `50%`, duplicate
text, same domain/subdomain, web pages, and content-defined chunks. Absence from
this bounded search is not proof that no precedent exists.

The closest numerical precedent located was the 2023 Finnish Internet Parsebank
preprint. It marks corpus-wide duplicate paragraphs, discards documents above
75%, and exposes D-25, D-50, and D-75 buckets. The authors explain that D-50
contains documents with "more than 25% duplicate text, but less than 50%."
That work supports studying duplication strata, but not adopting 50% for this
project: its paragraph-level, corpus-wide metric differs from sequential
same-subdomain content-defined-chunk overlap. See
[Finnish Internet Parsebank](https://doi.org/10.21203/rs.3.rs-3138153/v1).

The defensible response is therefore a sensitivity analysis, not a claim that
prior work validates the exact cutoff:

- Keep the existing 50% implementation as the historical primary rule, and
  freeze that designation and the sensitivity protocol before recomputing any
  outcomes. Recompute results at 25%, 40%, 60%, 75%, and no duplicate filter.
- At each setting, report retained pages and sites by label, builder, and site
  type; the number of sites still meeting the page-count eligibility rule; and
  performance on the frozen site-level holdout.
- Because sequential duplicate percentages depend on which page is seen first,
  repeat the calculation under the current chronological order and one stable
  URL-derived order. Report whether conclusions change.
- If conclusions do change, retain the full curve and describe 50% as a design
  choice. If they do not, state that the result is insensitive over the tested
  range.
