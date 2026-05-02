# Fraud-Only Sites in the Common Crawl 2 Scam CSV

Analysis date: 2026-04-22.
Input: `data/classify/scam_detection/scam_flagged_cc2.csv`.
Related artifacts: `scripts/detect_scam_sites_cc2.py`, `docs/scam_site_detection_cc.md`.

---

## Top Takeaways

- The CC2 scam CSV is **much broader than fraud-only**: it has 16,033 rows total,
  but only **30** rows in the script's broad `financial_harm` slice and only **3**
  sites that are defensibly fraudulent in the narrow sense used here.
- That narrow fraud-only subset is **3 / 16,033 = 0.0187%** of the CC2 cohort,
  about **10× smaller** than the broader 0.19% financial-harm figure in
  `docs/scam_site_detection_cc.md`.
- The main reason the CSV feels too large is that the broad Tier A result is mostly
  **gambling, not clear fraud**: **26 / 30 = 86.7%** of Tier A is current online
  gambling, plus one historical gambling borderline case.
- The clearest current hard-fraud sites are **human-like**, not LLM-like. The only
  clear LLM-associated fraud site is a **historical relabel case**:
  `allinonedocument.com`.

---

## Narrow Definition Used Here

This note uses a **fraud-only** definition narrower than the script's
`financial_harm` tier.

Included:

- sites whose core purpose is to **deceive victims for value**;
- sites selling clearly fraudulent products or services;
- sites whose primary purpose is to **enable fraud directly**.

Excluded:

- real-money gambling sites whose notes describe gambling operations but do not by
  themselves show rigged outcomes or fake services;
- piracy, spam, adult content, and other harmful-but-not-fraud categories.

Operationally, that leaves **two direct fraud services** plus **one fraud-enabling
site**.

---

## Fraud-Only Hierarchical Grouping

### 1. Direct monetized fraud services

These sites appear to sell illegal or deceptive products/services directly.

#### 1.1 Identity-theft data sale

| Site | Current label | Evidence |
|---|---|---|
| `findsomeonessocialsecuritynumber.com` | `human_like`, `malicious_deceptive` | `why_text`: "sell or provide access to stolen Social Security Numbers and related personal data"; signals: `credential_theft`, `deceptive_general` |

Why it belongs here:

- the site's stated product is stolen personal data;
- the harm is direct and transactional, not merely promotional;
- this is the cleanest identity-theft service in the CC2 fraud slice.

#### 1.2 Counterfeit-document sale

| Site | Current label | Evidence |
|---|---|---|
| `allinonedocument.com` | `llm_like`, now `business_service_operator`, historically `malicious_deceptive` | `why_text`: repeatedly promotes buying passports, visas, and other travel documents directly from the operator |

Why it belongs here:

- earlier categorizations labeled it `malicious_deceptive`;
- the latest run softened it to `business_service_operator`, but the note still
  describes direct sale of illegal documents;
- this is the **one clear LLM-like fraud seller** in the narrow subset.

Important nuance:

- this is **not** a current `malicious_deceptive` row in the CSV;
- it survives in the fraud-only subset only because the historical label and the
  latest `why_text` agree on counterfeit-document sales.

---

### 2. Fraud-enablement / scam-infrastructure content

These sites do not primarily sell a fake product to the visitor, but their core
purpose is to support fraud or related abuse.

#### 2.1 Instructional fraud-enablement hub

| Site | Current label | Evidence |
|---|---|---|
| `smartlazyhustler.com` | `human_like`, `malicious_deceptive` | `why_text`: provides instructions and encouragement for shoplifting, phishing, bank-log spamming, scams, and fraud; signals: `phishing`, `deceptive_general` |

Why it belongs here:

- the site is not just discussing scams; the note says its primary purpose is to
  encourage and explain them;
- this makes it fraud-enabling infrastructure rather than a neutral publisher.

Important nuance:

- this is the weakest member of the fraud-only subset if one insists on
  victim-facing commercial fraud only;
- it is still much closer to fraud than the gambling rows, because the content is
  explicitly about conducting scams rather than participating in gambling.

---

### 3. What is **not** in the fraud-only subset

#### 3.1 Online gambling cluster (excluded)

Excluded sites: the **26 current** `online_gambling_casino` rows plus the
historical borderline `wulkan-bet.org` case.

Why excluded:

- the notes describe real-money casino or betting operations;
- the notes do **not** by themselves establish fake services, rigged outcomes, or
  direct deception of users;
- several notes explicitly mention licensing or operator policies.

Why this matters:

- this cluster is the main reason the CC2 scam CSV looks much larger than the true
  fraud-only subset;
- **27 / 30** rows in the broad Tier A slice are gambling or gambling-adjacent,
  leaving only **3** fraud-only sites under the narrower definition here.

#### 3.2 Other non-fraud harmful categories (excluded)

Also excluded from this note:

- piracy / unauthorized distribution (`piracy` tier);
- spam / parked-content farms and adult-content rows (`vice` tier);
- keyword-only hits that are really security writing about fraud rather than
  committing it.

---

## Site List for the Narrow Fraud-Only Subset

| Group | Site | LLM-like? | Why included |
|---|---|---:|---|
| Direct fraud service | `findsomeonessocialsecuritynumber.com` | No | sells stolen SSNs / personal data |
| Direct fraud service | `allinonedocument.com` | Yes | sells counterfeit passports / visas / IDs |
| Fraud-enablement content | `smartlazyhustler.com` | No | publishes instructions for phishing / scam activity |

Summary numbers:

- Narrow fraud-only subset: **3 sites**.
- LLM-like within that subset: **1 / 3 = 33.3%**.
- Current `malicious_deceptive`: **2 / 3**, both human-like.
- Historical relabel case: **1 / 3**, the only LLM-like fraud site.

---

## New Takeaways from the Narrower Cut

1. **The CC2 fraud story is mostly a false impression caused by label scope.** The
   CSV is useful for finding fraud candidates, but most of the broad Tier A slice
   is not fraud under a narrow deception-based definition.
2. **Hard fraud remains rare even in Common Crawl.** The fraud-only slice is only
   **0.0187%** of the full 16,033-row cohort.
3. **Current hard fraud is human-like; LLM shows up mainly in presentation.** The
   strongest LLM-linked fraud case is the counterfeit-document seller that now
   presents itself as an ordinary business-service operator.
4. **If the paper wants "fraud" rather than "financial harm," it should use 3
   sites, not 30.** The 30-site number is valid only for the broader financial-harm
   framing.

---

## Recommendation for downstream use

- Use this note when the claim must be strictly about **fraudulent sites only**.
- Use `docs/scam_site_detection_cc.md` when the claim is about the broader
  **financial-harm / fraud-adjacent** slice.
- Do not mix the 3-site fraud-only subset with the 30-site financial-harm count in
  the same sentence without stating the scope difference explicitly.
