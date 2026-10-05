# Frozen public evidence collection: DW1 detector survey

Collection date: 2026-08-08, America/Los_Angeles.

This directory is the discoverable external evidence collection for the renewed
DW1 detector survey. Its canonical absolute path is:

`/ssd1/sichangheagent/dw1_detector_survey_public_artifacts/2026-08-08`

The collection contains public primary-paper PDFs, raw public arXiv Atom query
exports, pages returned by anonymous public Google Scholar requests, sanitized
response headers, immutable official repository archives, both relevant
immutable MELD Hugging Face snapshots, three composite-source detector
checkpoints, and public artifact metadata.
The sibling survey source directory in the documentation repository preserves
the benchmark source, raw stdout and stderr, score-level output, and execution
environment manifests.

No PB state, credential, authenticated endpoint, browser profile, cookie jar,
persistent browser session, robot-challenge bypass, or human-owned tmux session
was used. The MELD paper-era companion endpoint returned HTTP 401; its response
and sanitized headers are retained under `http/`, and the endpoint was not
bypassed. The Google Scholar response headers were sanitized to remove
`Set-Cookie`; no returned cookie was stored or sent.

## Layout

- `papers/`: exact public arXiv PDFs used or screened. A few version-suffixed
  copies are deliberately retained when collection work addressed an explicit
  version.
- `queries/`: raw date-sorted arXiv Atom responses, the mechanically extracted
  first-page Google Scholar result list, and bounded public artifact searches.
- `http/`: the raw Scholar response body, sanitized response headers, and the
  inaccessible MELD companion-code response.
- `snapshots/meld/`: the immutable paper-era and current v5 official Hugging Face
  repositories, including exact weights.
- `snapshots/detectrlx-*`, `snapshots/desklib-*`, and `snapshots/modernbert-*`:
  complete immutable public checkpoint snapshots used by the composite repair.
- `snapshots/*.tar.gz`: immutable official GitHub source archives for the
  reviewed releases, including Markov calibration, Exons-Detect, DetectRL-X,
  Desklib, C-ReD, ALHD, model collapse, and ELFEN.
- `snapshots/metadata/`: anonymous official API metadata used to pin revisions.
- `MANIFEST.sha256`: SHA-256 integrity ledger for every retained file other than
  the ledger itself.

## Reproduction boundary

The paper-era MELD state is preserved but is not executed: the model card depends
on companion code that is no longer anonymously available, and substituting the
current self-contained v5 architecture would not be faithful. The current v5
state is executed separately and is never used to validate the paper-era accuracy
tables. The survey documents this artifact-version and benchmark-comparability
gap as a blocker.

LM²otifs and NEULIF are preserved as primary PDFs. Neither paper links an
official repository or checkpoint. Anonymous GitHub repository searches by exact
method name, exact title, and arXiv identifier found no matching LM²otifs release;
the corresponding NEULIF title and identifier searches found none, while its
name search returned unrelated repositories. Anonymous Hugging Face model and
Space searches by method name found no result for either method. The raw JSON
responses and combined public Scholar result page are retained. This is a bounded
artifact-status observation, not proof that no release can exist elsewhere.
The anonymous Kaggle API resolves the likely NEULIF corpus to
`shanegerami/ai-vs-human-text`; its public description says only that roughly
500,000 essays were combined from multiple sources. The retained search and
metadata responses do not identify generator families, source domains, or text
lengths.

The semantic repair first promoted thirteen export rows from catch-alls to
explicit dispositions. Adversarial review then promoted six high-scoring shared-
task systems and one comparative detector paper. The generalized repair adds the
previously hidden linguistic-feature SVM as the sixty-ninth explicit publication
row, then reviews 33 composite overview, benchmark, comparative, evaluation, and
shared-task sources. Successive high-cell repairs expand 26 of them to 263
qualifying named system/version results, including per-dataset, generator,
domain, prompt-group, language, and validation results paired with their weak
mean or official aggregate; the remaining seven sources have specific
no-qualifier reasons. Their public primary PDFs are retained. The
frozen export references DP-MGTD
revision 2, whose abstract page remains public but whose revision-2 PDF returned
HTTP 404 during preservation; the still-public revision-1 PDF is kept as
`papers/2601.04641v1.pdf`. That version limit is explicit rather than silently
substituted.

The final content-derived repair removes the title/class selection boundary. It
binds a primary PDF and reproducible full-text extraction for every one of the
119 frozen export publications, reads all main and appendix result tables, and
maps 987 qualifying detector accounts to explicit dispositions. Independent
content discovery recognizes Arabic and Roman table captions and figure legends,
records one hash-bound scope summary per paper, and resolves every raw row.
Mechanically derived discovery total: 4,812 result candidates + 119 source
summaries = 4,931 discovery rows. A second adjudication requires direct
same-parent content for all 987 accepted accounts, including six DMAP Table 1
scorer configurations whose
AUROC definition appears only in Appendix K, without using those bindings to
seed or suppress the independent candidate queue.
Fourteen public
arXiv PDFs that were absent from the preceding freeze were added solely to make
that 119-paper corpus complete: 2608.03859, 2607.14905, 2605.03723, 2605.02712,
2604.21365, 2604.21300, 2604.04932, 2511.17402, 2510.00890, 2509.25154,
2508.18715, 2503.23622, 2501.18998, and 2501.14288. Each was fetched through the
anonymous public arXiv export endpoint and is individually hash-bound below.
No authenticated or browser-session state was used.

The GenAI Detection Task 3 overview and primary system PDFs for Leidos, Pangram,
ALERT, and CNLP-NITS are preserved. USTC-BUPT has an explicit absence record:
the overview bibliography and bounded anonymous public OpenAlex, DBLP, and GitHub
exact searches found no separate primary paper, repository, or checkpoint. The
same exact-search records document primary-paper absence for the Counter Turing
Tesla, Llama_Mamba, and NLP_great systems. Absence claims are bounded to those
preserved public searches.

The official Leidos system paper also resolves a mechanism error in an earlier
supporting row: MC/v1.0.4 is an unweighted multiclass DistilRoBERTa classifier,
not an ensemble. BC/v1.0.1 is unweighted binary, BW/v1.0.3 weighted binary, and
MW/v1.0.2 weighted multiclass.

The closing Task 3 pass also preserves the official LuxVeri and MOSAIC system
PDFs. Older methods newly exposed by benchmark cells retain their public primary
papers for GLTR, HC3, DetectGPT, the Neighborhood membership attack, ReCaLL,
DC-PDD, and LLM-Deviation. The official DC-PDD repository metadata and
an immutable archive at commit `5d4220850da9a2c6ee1026029b2814b72a4dd581`
are preserved; source availability is not treated as a fitted cross-model
calibration artifact.

The Task 1 overview's 39 high-slice English/multilingual submission rows map to
official ACL system papers where they exist. This collection preserves papers
for DCBU (`.12`), L3i++ (`.13`), TechExperts (`.14`), SzegedAI (`.15`),
Unibuc/tmarchitan (`.16`), Fraunhofer SIT (`.17`), Nota AI (`.19`), LuxVeri
(`.21`), Grape (`.22`), AAIG (`.23`), TurQUaz (`.24`), and Advacheck (`.26`).
The overview explicitly says systems without a description submitted neither a
manuscript nor a short description; those result rows use a primary-absence
sentinel rather than an invented paper. Official NeurIPS PDFs for BiScope and
DeTeCtive are also retained for the cross-dataset high-cell dispositions.

Three of the seven later promotions link official public GitHub repositories:
mdok, the Defactify NELA-feature system, and the English/Italian comparative
framework. Their immutable source archives and anonymous repository/commit
metadata are retained under `snapshots/` and `snapshots/metadata/`. The archives
contain source or notebooks but no trained detector checkpoint; that distinction
is preserved in the individual dispositions rather than treating source code as
a runnable paper state.

DetectRL-X X-Rob, Desklib v1.01, and the model-collapse ModernBERT checkpoint are
complete anonymous public states and were screened. The repository-owned evidence
retains successful and failed raw logs, the score CSV, independent recomputation,
environment manifests, a separate exact model-file ledger, and a non-destructive
layout script that maps these revision-bearing snapshot names to the three short
harness keys. Only Desklib came close to stored Binoculars AUROC; it remains a
runnable follow-up rather than a replacement. No other embedded result was
reconstructed when its trained state was missing.

Two inherited files whose names contain `canonical_detectllm_2306.05594` are an
unrelated space-environment paper, not DetectLLM. They remain only to preserve
prior ledger continuity and are not evidence. The correctly identified
DetectLLM arXiv 2306.05540 PDF is separately retained as
`papers/canonical_detectllm_2306.05540.pdf`; FastDetectGPT is arXiv 2310.05130.

The collection is frozen by the candidate manifest and documentation commits
recorded in the survey package. Recompute the integrity ledger from this directory
with `sha256sum --check MANIFEST.sha256`.
