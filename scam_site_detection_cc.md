# Fraudulent / Scam Sites in the Common Crawl 2 Cohort

Analysis date: 2026-04-22.
Cohort: CC2 `analysis_run_id=7`, `selected_for_deep=true`, `svm_distance IS NOT NULL`
→ 16,033 subdomains (5,857 LLM-like 36.5%, 10,176 human-like 63.5%).
Categorized: 11,594 (72%).

Script: `scripts/detect_scam_sites_cc2.py`.
Output: `data/classify/scam_detection/scam_flagged_cc2.csv`.

---

## ⚠ Scope Correction from Search-Result Analysis

Most sites flagged in the search-result analysis were **piracy and spam content
farms**, not financial fraud. Those are copyright violations / nuisance sites;
users are not defrauded of money and no malware is delivered. This CC2 analysis
narrows the target to potentially fraudulent or financially harmful sites:

| Target | Included? |
|---|---|
| Phishing, credential theft, identity fraud | ✓ |
| Fake shops (takes money, delivers nothing) | ✓ |
| Counterfeit / fake goods sold for real money | ✓ |
| Investment / crypto scams | ✓ |
| Real-money gambling operators (especially clearly predatory cases) | ✓ |
| Malware delivery | ✓ |
| Piracy (user gets the file, no monetary loss) | ✗ |
| Spam / content farms (nuisance, not fraud) | ✗ |

---

## Summary Findings

### Tier A — Potential fraud / financial harm (primary target): 30 sites (0.19% of cohort)

| Category / evidence | n | LLM-like | LLM share |
|---|---:|---:|---:|
| `malicious_deceptive` (current) | 2 | 0 | 0% |
| `online_gambling_casino` (current) | 26 | 21 | **81%** |
| Ever `malicious_deceptive`, now `business_service_operator` | 1 | 1 | LLM |
| Ever `online_gambling_casino`, now `business_service_operator` | 1 | 0 | human |

### Tier B — Non-financial harmful / illegal content: 83 sites

79 of these sites are piracy / unauthorized-distribution categories, plus 4
`illegal_child_exploitation` sites. 39.8% LLM-like overall — near baseline.

### Tier C — Vice / Spam: 268 sites

32.1% LLM-like — slightly below baseline.

---

## Confirmed Hard-Fraud Sites and Financial-Harm Clusters

### `malicious_deceptive` (2 sites, both human-like)

| Site | Nature |
|---|---|
| `findsomeonessocialsecuritynumber.com` | Sells stolen Social Security Numbers / personal data (identity theft service) |
| `smartlazyhustler.com` | Publishes instructions for shoplifting, phishing, bank-log spamming, scams |

Both are `human_like`; neither uses LLM-generated content. In this cohort, the
clearest hard-fraud pages are not LLM-dominant.

### `malicious_deceptive` in prior run, now `business_service_operator`

| Site | Nature | LLM |
|---|---|---|
| `allinonedocument.com` | Sells counterfeit passports, visas, and ID documents | LLM-like |

The most recent categorization run saw the site's "commercial service" framing and
assigned `business_service_operator`. Earlier runs correctly identified the
product as fraudulent. **This is the one clearly LLM-assisted fraud operation
found**: the site uses AI-generated content to present its document-fraud service
as a legitimate business.

### Online gambling (26 sites, 81% LLM-like)

A cluster of real-money online gambling platforms, predominantly Philippine-based
(`.com.ph`, `.net.ph`, `GCash` payment integration):

- `www.fb777-login.com.ph` (SVM=8.96), `online-sport-ph.net` (6.78),
  `mobile.casino4win.net` (5.56), `jiliasia7.com.ph` (5.01), `mwcashcasino.ph`
  (4.88), `www.bingoballs.net` (4.67), `app.lotoplus.net` (4.54) — Peraplay/BingoPlus
  operator network.
- Additional: `peraplay.fun`, `damanonline.games`, `slotvip-casino.com.ph`,
  `37jl.org.ph`, `metabets.ph`, `momobet.com.ph`, `m99-kh.com`, `hehe555.net`,
  `123jili.net.ph`, `200jili.com.ph`, `w500.net.ph`, `bingoballs.net`,
  `app.bingoplus-ph.net`.
- Non-Philippine: `www.luckstarscasino.com`, `www.spinzwin.com`.

**The 81% LLM-like rate (vs 36.5% baseline, 2.2× lift) is the strongest
financial-harm signal in the data.** These sites use LLM-generated promotional
and game-description content. The category captures real-money gambling
operators; the evidence here does not prove that every site is fake or unlicensed,
but it does identify a cluster of financially risky / predatory services largely
absent from search results.

The `wulkan-bet.org` case (now `business_service_operator`) is a similar
gambling platform that the model reclassified when it sampled pages showing
licensing disclaimers — a known model disagreement pattern.

---

## LLM-Share Analysis by Category

The most striking pattern is the LLM concentration in gambling:

| Tier | n | LLM-like | LLM% | vs baseline |
|---|---:|---:|---:|---:|
| `malicious_deceptive` | 2 | 0 | 0% | −36.5 pp |
| `online_gambling_casino` | 26 | 21 | 81% | **+44.5 pp** |
| Non-financial harmful / illegal total | 83 | 33 | 39.8% | +3.3 pp |
| `pirated_software_distribution` | 36 | 16 | 44% | +7.5 pp |
| `illegal_child_exploitation` | 4 | 0 | 0% | −36.5 pp |
| `adult_pornography` | 51 | 17 | 33% | −3.5 pp |
| `spam_parked_content_farm` | 217 | 69 | 32% | −4.5 pp |
| Baseline (all CC2 selected) | 16,033 | 5,857 | 36.5% | — |

Interpretations:
- **Gambling sites (81% LLM)**: LLM content is used to produce promotional copy,
  game descriptions, and FAQ pages at scale. Many of these are likely
  programmatically generated landing pages for the same operator network.
- **`malicious_deceptive` sites (0% LLM)**: Hard-fraud operations are human-run.
  SSN theft and shoplifting instruction sites do not use AI content generation.
- **Outside gambling, bad categories are near or below baseline** — piracy,
  adult, spam, and other severe-illegal categories do not show a distinctive
  LLM signal.

---

## Keyword Detection on why_text: One False Positive

The only keyword-only hit is `www.evntec.com` (`publisher_editorial`) — a
**security publisher** writing *about* phishing scams. "Phishing" in the why_text
means the site explains phishing, not that it commits it. Pattern `r"\bphish..."`:
see the `malware_content` false positive from the search-result analysis for the
same structural issue.

**Conclusion**: For the CC2 cohort, why_text keyword scanning adds no true
positives beyond explicit category assignment. Category disagreement across runs
(`allinonedocument.com`, `wulkan-bet.org`) remains the best supplementary signal.

---

## General Methodology for Our Data

Three-signal framework (in descending reliability):

1. **Explicit bad category** (precision ~100%, limited recall):
   - Financial harm: `malicious_deceptive`, `online_gambling_casino`.
   - Non-financial harmful / illegal: piracy slugs, `illegal_child_exploitation`.
   - Vice: `adult_pornography`, `spam_parked_content_farm`.

2. **Cross-run category disagreement** (catches borderline cases):
   - A site that was ever `malicious_deceptive` but is now `business_service_operator`
     is the canonical borderline fraud example (`allinonedocument.com`).
   - Query: all historical `subdomain_categorizations` rows per site, check if any
     approved category is in the bad set.

3. **Why_text keyword patterns** (limited utility in practice):
   - Works when the model explicitly names the fraud mechanism.
   - Fails for security publishers, negation in why_text list phrases.
   - Use only as a tie-breaker; do not rely on it as primary signal.

**What remains undetectable without live re-crawl:**
- Fake shops that look like legitimate retailers (fraud only becomes apparent at
  checkout / post-purchase).
- Investment scam sites that look like financial advisory publishers.
- Phishing pages that mimic legitimate brand pages (not yet in the crawl).

---

## Comparison: Search Result vs Common Crawl

| Signal | Search-result cohort (3,596) | CC2 cohort (16,033) |
|---|---|---|
| `malicious_deceptive` in cohort | 0 | 2 |
| `online_gambling_casino` in cohort | 0 | 26 |
| `spam_parked_content_farm` | 7 (0.2%) | 217 (1.4%) |
| All piracy slugs | 3 | 83 |
| `adult_pornography` | 1 | 51 |
| Financial-harm tier total | 0 | 30 |
| Financial-harm rate | 0% | 0.19% |

The CC2 dataset exposes a small set of potentially fraudulent or financially
harmful sites that search engines exclude from results. Even so, the rate is low
(0.19%): the CC2 crawler also selects
"interesting" (LLM-scored) pages rather than uniformly sampling the web, so
unambiguously fraudulent domains may still be underrepresented.

---

## Paper Integration

Best fit in the outline: `findings in the wild` → `LLM exacerbate existing Web
problems`, immediately after the category-breakdown discussion and as the concrete
resolution of the TODOs for fake ecommerce / potentially fraudulent sites.

**1-sentence RQ:** Where do potentially fraudulent sites appear in our website
categories, and does LLM-dominant content concentrate in those categories once we
look beyond search-engine-filtered results?

**1-sentence answer:** In our data, potentially fraudulent or financially harmful
sites are rare and mostly absent from search results, but the Common Crawl cohort reveals a small
0.19% financial-harm slice dominated by online gambling, where 81% of currently labeled
gambling sites are LLM-like, while the clearest hard-fraud sites are human-run
except for one LLM-assisted fake-document seller.

### Numbers to foreground

- Search-result cohort: 0 current `malicious_deceptive`, 0 current
  `online_gambling_casino`, and the top takeaway is that most flagged sites there
  are piracy/spam rather than monetary fraud.
- Common Crawl 2 cohort: 30 potentially fraudulent / financially harmful sites out
  of 16,033 (0.19%).
- Composition of that slice: 26 current `online_gambling_casino`, 2 current
  `malicious_deceptive`, plus 2 historically flagged borderline cases.
- LLM concentration: 21/26 current gambling sites are LLM-like (81%) versus a
  36.5% CC2 baseline (+44.5 percentage points, 2.2× lift).
- Hard-fraud counterexample: both current `malicious_deceptive` sites are
  human-like; only `allinonedocument.com` is a clearly LLM-assisted fraud site.

### How to write it in the paper

- Use this as a short quantitative subsection, not as a gallery of anecdotes.
- Give 1 short example sentence for `allinonedocument.com` as the clearest
  LLM-assisted fraud case, and 1 short sentence that the dominant pattern is a
  gambling-site cluster using LLM-written promotional copy.
- Avoid detailed site descriptions unless needed for a single illustrative
  example; the main contribution here is the category-level prevalence contrast
  between search results and Common Crawl, not case-study depth.
