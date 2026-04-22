# Detecting Potential Fraudulent / Scam Sites in the Search-Result Cohort

Analysis date: 2026-04-22. Cohort: 3,596 sites from `site_full_mg` (2,243
LLM-like, 1,353 human-like), the `selected_for_deep` search-result snapshot.

Script: `scripts/detect_scam_sites.py`.
Output: `data/classify/scam_detection/scam_flagged_sites.csv`.

---

## ⚠ Top Takeaway: Most Flagged Sites Are Not Financial Fraud

The sites identified in this analysis are predominantly **piracy/copyright
violations** and **spam content farms**, not sites that defraud users of
money or deliver malware. Specifically:

- Piracy sites (`pirated_software_distribution`, `pirated_book_distribution`,
  etc.) distribute copyrighted content without authorization. Users get what
  they come for (the file); there is no deception about the product or financial
  theft. These are illegal but not "scams."
- Spam/content farms (`spam_parked_content_farm`) waste users' time with thin
  content but do not steal money or install malware.
- No malware-distributing sites were found in the search-result cohort.
- No current `malicious_deceptive` or `online_gambling_casino` sites were found
  in the search-result cohort.

**True financial fraud / scam sites** — fake shops, fake service operators,
phishing pages, investment scams — are largely absent from the search-result
cohort because search engines filter them. The Common Crawl dataset, which
crawls the open web without search-engine filtering, is a better source for
finding these. See the CC analysis in `docs/scam_site_detection_cc.md`.

---

## TL;DR Findings (Search-Result Cohort)

- **0.3% of the search-result cohort** (11/3,596) are in explicitly bad categories.
- **0.75% more** (27 additional) were ever assigned a bad category in a prior
  categorization run but currently carry a "legit" label — model disagreement across
  runs is the most useful novel signal for borderline fraud.
- **Keyword scanning adds no extra true positives**: 3 sites have keyword hits, but
  2 are already covered by category signals and the only keyword-only site is a
  known false positive (security publisher writing about malware).
- Total: 39 flagged sites (1.1% of cohort). The cohort is relatively clean: search
  engines filter out most egregious fraud.

---

## Which buckets fraudulent sites would be in

### Tier 1 — Explicit bad categories

These category slugs directly encode harmful or illegal intent:

| Slug | Description | n (cohort) |
|---|---|---:|
| `malicious_deceptive` | Phishing, counterfeit docs, malware, identity theft | 0 |
| `spam_parked_content_farm` | Thin/mass-gen SEO farms, expired-domain repurposing | 7 |
| `illegal_child_exploitation` | CSAM | 0 |
| `pirated_software_distribution` | Cracked/unauthorized software | 1 |
| `pirated_book_distribution` | Free copyrighted ebooks/PDFs | 0 |
| `pirated_educational_content` | Free copyrighted course/study material | 1 |
| `pirated_media_distribution` | Unauthorized movie/TV | 0 |
| `pirated_music_distribution` | Unauthorized music | 1 |
| `unauthorized_media_streaming` | Illegal streaming portals | 0 |
| `adult_pornography` | Explicit adult content | 1 |
| `online_gambling_casino` | Real-money online casino/gambling | 0 |

The current-cohort counts confirm that the search-result snapshot contains spam,
piracy, and a small amount of adult content, but no currently labeled financial-fraud
or online-gambling sites.

### Tier 2 — Fraud hidden inside "legitimate" categories

Even in the cohort, some sites in ostensibly legit categories exhibit deceptive
behavior that was caught by the categorization model in at least one run:

| Current category | Hidden fraud type | Example |
|---|---|---|
| `retail_ecommerce` | Pirated software sold as "cheap" copies | `sadesign.ai` |
| `publisher_editorial` | Distributes unauthorized APKs alongside tutorials | `androidcure.com` |
| `community_ugc` | Forum that primarily facilitates sharing copyrighted PDFs | `www.studynama.com` |
| `publisher_editorial` | Borderline explicit adult content (BDSM fetish guides) | `emmalovesadress.com` |
| `publisher_editorial` / `affiliate_seo_content` | Low-value content farms misclassified | 22 sites |

---

## Detection methodology

### Signal 1 — Explicit bad category (highest precision)

Check `site_full_mg.category_slug ∈ EXPLICIT_BAD_SLUGS`.
Zero false positives; recall limited to sites whose current categorization
reflects the bad intent.

### Signal 2 — Cross-run category disagreement (highest novelty)

Query all historical `subdomain_categorizations` rows for each cohort site and
check whether any approved category was ever in the bad set. A mismatch between
the latest run (legit category) and a prior run (bad category) means the model
observed different page samples and judged the site differently at least once.

This catches:
- Sites that cleaned up their content between crawls but retain some bad pages.
- Sites that mixed legitimate content with a bad intent (e.g., `sadesign.ai`
  mixes design tutorials with pirated Adobe software for sale).
- Sites where the bad-category run sampled the "wrong" pages, producing a
  reliable fraud signal that the latest run missed.

In the cohort: 27 sites (23 spam-only, 1 mixed spam+pirated software,
1 pirated software only, 1 pirated educational, 1 adult).

### Signal 3 — Why_text keyword scanning (broadest coverage, needs care)

Apply regex patterns to the LLM-generated `why_text` rationale for each site.
The categorization model uses specific language to describe fraud:

| Pattern type | Example model language |
|---|---|
| Piracy | "offers free downloadable PDFs without indication of licensing" |
| Piracy software | "distributes modified APK files... not authorized by original developers" |
| Malicious | "provides detailed instructions for shoplifting, phishing, bank-log spamming" |
| Counterfeit goods | "sells cheap copyrighted software" / "counterfeit travel documents" |
| Identity theft | "sell or provide access to stolen Social Security Numbers" |
| CSAM | "explicit sexual descriptions... involving minors" |
| Spam | "thin, auto-generated articles" / "expired-domain repurposed to host SEO content" |
| Fake health claims | "miracle cure", "guaranteed heal", "unproven claims" |

**Known limitations:**
- The model often explicitly affirms legitimacy by stating the absence of fraud
  ("no downloadable pirated content", "no malicious intent"). Because "pirated"
  appears in the negation, naive keyword matching produces false positives.
  The script uses a negation-prefix check (60-char look-behind) to mitigate this,
  but long-range list-style negations ("no X, Y, or Z") can still leak through.
- Sites that write *about* fraud (e.g., `macsecurity.net` writing about malware
  removal) trigger keyword patterns. Sentence-level context is needed to
  distinguish "distributes malware" from "explains how to remove malware."
- The why_text is generated by the categorization model itself; sites that present
  only their legitimate front page to the model will not have their fraud described.

In the cohort: 3 total keyword-hit sites, but 2 are already covered by category
signals and the only keyword-only site is a false positive, so keyword scanning
adds no extra true positives here.

### Signal 4 — YMYL + LLM + monetization cross-signal (not yet implemented)

**Your Money or Your Life (YMYL)** categories (health, finance, legal advice) carry
elevated fraud risk when combined with LLM-generated content and strong monetization.
Potential future signals:

- `category_slug = publisher_editorial` + why_text mentions `health|medical|pharma`
  + `label = llm_like` + `has_ads = true` → AI-generated health misinformation for ad revenue.
- `business_service_operator` + why_text mentions `invest|forex|crypto|recovery`
  + `monetization_bucket = none_detected` → lead-gen fraud (fake recovery service).
- `retail_ecommerce` + why_text mentions `software|license|Adobe|Photoshop`
  + `monetization_bucket ≠ commerce_checkout` → pirated software sales.

These would require a second-pass query that joins `site_full_mg` feature columns
with the why_text content.

---

## Specific flagged sites in cohort

| Site | Current cat | Risk | Evidence |
|---|---|---|---|
| `filecr.com` | pirated_software_distribution | Confirmed | Current category + piracy in why_text |
| `4d4m.com` | pirated_music_distribution | Confirmed | Current category + piracy in why_text (free MP3s without license) |
| `saifetech.org` | pirated_educational_content | Confirmed | Distributes copyrighted textbook PDFs |
| `gopakuteeram.com` | adult_pornography | Confirmed | Adult category |
| `k2digitizers.com` | spam_parked_content_farm | Confirmed | Auto-generated gaming articles |
| `englishsunglish.com` | spam_parked_content_farm | Confirmed | Thin unrelated articles |
| `realfarmacy.com` | spam_parked_content_farm | Confirmed | Expired-domain SEO farm |
| `premiumbusinesshub.com` | spam_parked_content_farm | Confirmed | Content farm |
| `volleyballblaze.com` | spam_parked_content_farm | Confirmed | Content farm |
| `www.aquariumpharm.com` | spam_parked_content_farm | Confirmed | Content farm |
| `programminginsider.com` | spam_parked_content_farm | Confirmed | Content farm (human-like) |
| `sadesign.ai` | retail_ecommerce | **Suspected** | Ever `pirated_software_distribution`; why_text: "cheap copyrighted software", "Adobe... pirated" in one run |
| `androidcure.com` | publisher_editorial | **Suspected** | Ever `pirated_software_distribution`; distributes modified APKs (GBWhatsapp) without authorization |
| `www.studynama.com` | community_ugc | **Suspected** | Ever `pirated_educational_content`; forum for sharing copyrighted PDF notes |
| `emmalovesadress.com` | publisher_editorial | **Borderline** | Ever `adult_pornography`; explicit BDSM/sissification guides |

---

## Methodology limitations and gaps

1. **Coverage gap**: Why_text only covers sites with `decision_state = 'categorized'`.
   8 cohort sites (all human-like with `NULL` category in DuckDB) have no category.

2. **Single-snapshot bias**: The DuckDB cohort uses the latest categorization run.
   Sites that changed behavior after the categorization date are missed.

3. **No live-crawl validation**: Fraud detection here is based on categorization
   notes, not direct re-crawling of the flagged sites. Ground truth requires
   manual verification or a live re-crawl of the flagged list.

4. **Structural signals unused**: The `site_full_mg` table has 60+ tech/monetization
   features. YMYL-topic × LLM-label × monetization cross-signals (Signal 4 above)
   could surface additional borderline sites without requiring keyword scan.

5. **Search-result selection bias**: The cohort is drawn from search results. The
   most egregious fraud (CSAM, fake SSN shops, illegal streaming portals) rarely
   appears in search results and is therefore absent from the cohort even when
   present in the broader DB.
