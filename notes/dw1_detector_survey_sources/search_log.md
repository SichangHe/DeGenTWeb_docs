# DW1 detector survey search log

## Focus and fixed screen

Research date: 2026-08-07, America/Los_Angeles.

The focus was alternative LLM-text detectors for DW1 that can run on exactly two
NVIDIA RTX A6000 GPUs and are supported by traceable evidence showing that they
are not slower than the relevant Binoculars comparison. No numerical meaning was
invented for “not much slower.” RAG, retrieval, text rewriting, regeneration, and
multi-perturbation methods were excluded. Public browsing was read-only; no PB,
authenticated, human, or persistent browser session was used or changed.

The canonical paper comparators were fixed before screening candidates:

- Binoculars: Falcon-7B plus Falcon-7B-Instruct, BF16, first 512 tokens, with the
  observer and performer assigned to separate devices in the official code.
- FastDetectGPT black-box: GPT-J-6B sampling/reference plus GPT-Neo-2.7B scoring.
  Its paper runtime is 233 seconds for XSum generations from five source models,
  with 500 samples per dataset, on one Tesla A100; model initialization is excluded.
- DW1 operational Binoculars: batch 8, 2,048-token maximum,
  `SichangHe/falcon-7b-FP8-Dynamic` plus
  `SichangHe/falcon-7b-instruct-FP8-Dynamic`, one model per A6000 and concurrent
  forward passes.

## Google Scholar attempt

Exact public, unauthenticated query attempted:

> "LLM-generated text detection" fast zero-shot runtime

Google Scholar returned HTTP 403. Its response used Google's robot error image
and stated that the client did not have permission to fetch the Scholar URL. The
challenge was recorded and was not retried or bypassed. Consequently, Scholar
could not contribute result ranking, citation counts, or coverage confirmation.
Discovery continued through the public arXiv API, Crossref, official venue pages,
official repositories, and public Hugging Face artifacts. This means the survey is
a focused primary-source study, not a claim of exhaustive Scholar coverage.

The raw response was captured only in an ephemeral workspace. The durable fact
needed for the study—the exact query, status, and handling—is preserved here.

## Public discovery routes

The broad arXiv API query was:

> all:"LLM-generated text detection" OR all:"machine-generated text detection"

It was sorted by submitted date descending with a maximum of 100 results. Title
queries were also used to resolve PAWN as arXiv 2501.03940 and WaveDetect as
arXiv 2606.23336. Crossref resolved SpecDetect to DOI
10.1609/aaai.v40i38.40510, DetectAnyLLM to DOI 10.1145/3746027.3754862, and
WaveDetect to DOI 10.18653/v1/2026.findings-acl.424. Official OpenReview and
venue records were preferred to preprints when available.

The candidate set retained for full feasibility cards was WaveDetect,
DetectLLM-LRR, SpecDetect and SpecDetect++, Lastde and Lastde++, PAWN, and RADAR.
OpenAI RoBERTa was kept as a local control. DetectAnyLLM was initially screened,
then excluded when primary-paper review showed that its Reference Clustering step
does nearest-reference lookup over retained human and generated reference sets.
Ghostbuster was screened but rejected because its defining feature computation
uses the closed ada and davinci models and the paper links a data repository, not
a public runnable detector. FourierGPT was screened independently. It uses one
likelihood estimator forward plus a Fourier transform, but the paper supplies no
inference timing, its supervised path needs labeled training, and its heuristic path predicts
only which member of a prompt-matched human/generated pair is machine-written. It
was therefore not ranked as a deployable single-document DW1 alternative; no claim
is made that SpecDetect compared against or superseded it.

DetectGPT, DetectNPR, DNA-GPT, TOCSIN, RAIDAR and other rewrite, regeneration,
or multi-perturbation methods were excluded by the fixed method constraint.
Retrieval defenses, RAG detectors, k-nearest-neighbor proxy methods, and
in-context example-retrieval detectors were excluded by the fixed retrieval
constraint.

## Official implementation snapshots inspected

- Binoculars, `ahans30/Binoculars`, commit
  `c8ae2f90d50ee696418bc71d8d9e5020e5f9d7b8`.
- FastDetectGPT, `baoguangsheng/fast-detect-gpt`, commit
  `971b05202bac2bb504d60c0ac0812fea7a8f7c82`.
- DetectLLM, `mbzuai-nlp/DetectLLM`, commit
  `1db7935ae8c6f68cb3ed36f97c207e14b622366d`.
- Lastde, `TrustMedia-zju/Lastde_Detector`, commit
  `ead6939e0e9382f9ce5aa1b33b936ee6c4e0605d`.
- SpecDetect, `luohaitong/SpecDetect`, commit
  `4fadfad3d4c38590909f19adceac0ac9ecae9547`.
- PAWN, `pablomiralles22/ai-gen-detection`, commit
  `675e6859fce24fd8e5dafd079c89770f2a4aea18`.
- DetectAnyLLM, `fjc2005/DetectAnyLLM`, commit
  `ea82e853b23077474b1fb82b498ae888c8e69ada`.
- RADAR, `IBM/RADAR`, commit
  `3a9acf6d3d9b1766f5c6497af96601dea1ead868`.
- FourierGPT, `CLCS-SUSTech/FourierGPT`, commit
  `ec84e8fad1767cf166210d6981d6bb4b1b2ede24`.

The public WaveDetect Hugging Face artifact was inspected and executed at
revision `c4d72102938842de531990b3e961d3b41aaa4f05`. The public DetectAnyLLM
adapter was inspected at revision `c1bcbefd92919ea27317ebf4e1868ab65bb40eda`.
The public RADAR artifact was inspected at revision
`4ff1f23a69a36aa1df47b0933be6279f1b896c9b`.

## Collection and extraction limits

Primary PDFs were retained in the established paper collection. Existing Marker
Markdown was reused where present. DetectAnyLLM's Marker extraction expanded to
thousands of OCR blocks and was stopped after a bounded timeout; its primary PDF
remains intact and searchable evidence was extracted with `pdftotext`. WaveDetect
and FourierGPT were handled from their primary ACL PDFs with `pdftotext`. No
paper-collection index or unrelated file was changed.

The public web-search connector returned a gateway error during this study, so it
did not provide discovery evidence. Public primary endpoints remained reachable.
This, together with the Scholar 403, is why the result should be read as a bounded,
reproducible primary-source synthesis rather than an exhaustive web census.

## Accuracy-first follow-up: 2026-08-08

The renewed focus was explicitly recency and high accuracy: public 2025–2026
detectors that could plausibly match or improve Binoculars while retaining the
two-A6000, near-DW1-Binoculars-speed, and method-family constraints. Evidence
collected before the routing pause was preserved, then verified after the manager
returned the task to running. No authenticated endpoint, PB state, browser profile,
persistent browser session, or human-owned tmux state was accessed.

### Public discovery

The public arXiv API was queried by recent submission date with combinations of:

> "AI-generated text detection" OR "LLM-generated text detection"

> detector Binoculars AUROC inference speed

Exact-title and author-linked resolution produced these primary manuscripts:
2608.05741, 2608.01046, 2607.22026, 2607.14967, 2607.03680, 2606.31074,
2606.07313, 2606.02158, 2605.23190, 2605.16107, 2605.12890, 2604.21223,
2604.16923, 2602.13042, 2601.04833, 2511.01192, 2508.13152, 2506.15683,
and 2506.06705. All 19 PDFs were downloaded from public arXiv endpoints and
preserved in the established external paper collection with hashes recorded in
`paper_artifacts.md`.

Google Scholar exact-title and related-work discovery was attempted through its
public unauthenticated endpoint. It returned HTTP 403 with a robot challenge.
The challenge was not retried, solved, or bypassed. OpenReview returned a similar
challenge for IRM; the official NeurIPS proceedings page, paper, and supplemental
archive were used instead. The general web-search connector returned HTTP 404, so
it contributed no evidence.

### Official repositories inspected

- LAPD, `creator-xi/LAPD`, commit
  `1988eb68b70205d471c1924b6bbf1e199452662d`.
- SV-Detect, `Atmyre/SV-Detect`, commit
  `a25469ba6a1fa2adcf644338db6fef712511da66`.
- RepreGuard, `NLP2CT/RepreGuard`, commit
  `53677be4efc4a494d083b76f91dccc50d8bb4400`.
- Uncertainty-AIGT, `guoyikai2000/Uncertainty-AIGT`, commit
  `2e06a3d91ed1121c25b3fd7e6380238e04517086`.
- GTCL-AIDetection, `christopherburatti/GTCL-AIDetection`, commit
  `c9094d66bd0f6a888d3490ac04b3b3c68d2d2b64`.
- Triospect, `baoguangsheng/triospect`, commit
  `7599d456a667e3db0261ffe35da1c1bc37b641a9`.
- DeBERTa-Sentinel, `Galileo-Galili/HUMAN-VS-AI-TEXT-DETECTION`, commit
  `cd8b1a46cc98eb353ef2eb6e70bfc751f6eece16`.
- Multi-Level Contextual Detection, `Daftstone/Multi-level-MGT-Detection`, commit
  `c108289ea8595da780471ed1ce034773a571b364`.

GitHub's public API exact-title searches on 8 August 2026 found no official
repository or checkpoint for EchoPrompt or Steer-to-Detect. That historical
result is preserved as of that date. Exact-title searches for DWT-Fusion found
only an unrelated 2020 repository.

The 14 August current-status audit corrected EchoPrompt's disposition. Its
original abstract calls it “a training-free detector”. The later author-overlap
[EVIL-Detect paper](https://arxiv.org/abs/2608.10698) says, “Our code is
available at” its linked [repository at the inspected
commit](https://github.com/bbbbhrrrr/evildetect/tree/597bc4f0dd3fc1cc39a3dcd495013bd4f323ffdd).
This post-review paper was inspected live for the status correction; it postdates
and is not included in the closed 8 August PDF ledger in `paper_artifacts.md`.
That commit contains `scripts/echoprompt/score_votes.py` and section 4 of
`docs/reproduction.md`: a method-faithful Chinese/NLPCC implementation that fits
thresholds on validation labels. It is not a trained EchoPrompt checkpoint or an
exact reproduction of the original DetectRL, RealDet, and RAID results. The same
bounded official-source, GitHub repository, and Hugging Face search still found
no Steer-to-Detect implementation or learned state. Negative search results are
reported as “not found in the bounded search,” never as proof that no artifact
can exist.

### Public checkpoint resolution

Anonymous Hugging Face API and immutable revision metadata were used. The IRM
paper's best Llama-3.2-1B base/instruct pair returned HTTP 401 because access
requires license acceptance; no credential was supplied and the gate was not
bypassed. The strongest anonymously downloadable paper-listed family was:

- `Qwen/Qwen2-0.5B`, revision
  `91d2aff3f957f99e4c74c962f2f408dcc88a18d8`.
- `Qwen/Qwen2-0.5B-Instruct`, revision
  `c540970f9e29518b1d8f06ab8b24cba66ad77b6d`.

SV-Detect's exact backbone was resolved as `EleutherAI/gpt-neo-2.7B`, revision
`e24fa291132763e59f4a5422741b424fb5d59056`. Model weight hashes are recorded in
the corresponding durable benchmark results.

### Feasibility protocol and exclusion audit

Three bounded harnesses were added only under the survey source directory. LAPD
was compared in the same process against current DW1 Binoculars using the same
dynamic Falcon models, token IDs, eight documents, batch 8, 2,048-token cap, and
timing boundary. IRM used the exact public Qwen paper family in float32. SV-Detect
used the exact public GPT-Neo backbone in an optimized batched FP16 reconstruction
of the published feature mathematics; because no trained detector state exists,
its run was explicitly cost-only and not the exact release path.

GTCL was rejected after its official inference code showed k-nearest-neighbor
classification over retained representations. Triospect was rejected after the
official method showed summary and simplification generation plus multi-view
aggregation. These method exclusions preceded accuracy ranking. LAPD's categorical
sampling does not decode, rescore, or add another model forward, but the paper
groups its 10,000 auxiliary samples with perturbing or generating auxiliary
sequences. The conservative final review therefore excluded LAPD under the strict
no-multi-perturbation constraint rather than inferring an exception.

The adversarial review questioned IRM's score sign because the Python source uses
misleading variable names. Reading the official command together with paper
Equation 5 resolved it: the command passes the instruction checkpoint as
`base_model` and the base checkpoint as `ref_model`, so the official score is
instruction likelihood minus base likelihood. The final harness and rerun preserve
that direction. Base and instruction tokenizers were loaded separately and
verified to produce identical token IDs on all 1,000 selected texts. Trial,
selected-record, and selected-text hashes were added to the durable result. The
review also caused the SV-Detect timing to be relabeled as an optimized
reconstruction rather than an exact release-path result.

## Evaluator-failure repair: frozen 2026-08-08 search

This repair preserves every earlier source and result above, but supersedes the
19-paper coverage boundary and the conclusion drawn from it. The fresh evaluator
correctly identified MELD and broader recent-result omissions.

### Date-sorted public exports

The public arXiv API was queried anonymously with `start=0`, `max_results=100`,
`sortBy=submittedDate`, and `sortOrder=descending` for each exact phrase:

> all:"AI-generated text detection"

> all:"LLM-generated text detection"

> all:"machine-generated text detection"

The server returned 93, 40, and 71 rows respectively. Raw Atom responses, server
update timestamps, query links, and hashes are preserved as
`coverage_query_ai_generated.atom`, `coverage_query_llm_generated.atom`, and
`coverage_query_machine_generated.atom`. Deduplication by arXiv identifier and a
2025–2026 date filter yield 119 results. A fourth targeted query,
`all:Markov AND all:"text detection"`, is retained as
`coverage_query_markov.atom`. The date-sorted disposition ledger is
`coverage_dispositions.md`; it gives a source-mapped reason for every plausible
high-accuracy row and accounts for every other exported identifier by scope.

The general web-search connector was invoked for relevant public discovery but
returned HTTP 404 from its search gateway. It contributed no substantive source.
Direct anonymous primary endpoints remained usable.

### Fresh public Google Scholar boundary

One anonymous request used the exact first-page query:

> https://scholar.google.com/scholar?as_ylo=2025&as_yhi=2026&scisbd=1&q=%22AI-generated+text+detection%22

It returned HTTP 200 and ten visible results without a robot challenge. No cookie
jar, stored cookie, browser profile, persistent session, second page, retry, or
challenge bypass was used. The complete HTML body and response headers with every
`Set-Cookie` field removed are retained in the external collection; the ten
mechanically extracted titles and target URLs are preserved in
`coverage_query_google_scholar.tsv`. This fresh result does not erase the earlier
403 attempt recorded above: both are true bounded observations from different
requests. Scholar is supplemental discovery evidence, not an exhaustive census.

### MELD public artifact resolution

The primary manuscript is arXiv 2605.06903. Anonymous Hugging Face API metadata
and commit history resolved two immutable official states:

- paper-era revision
  `51f3ac2d4ce8de9f6f3a1eba9ca4276b077bb808`, with a 1,584,091,048-byte FP32
  weight file and model card describing 396 million parameters; and
- current v5 revision
  `453acf594d48f8c55c3a38bde396f9178516d817`, whose model-release commit is
  `9b6379cdf62961a443d972fd27ff705ea9a07dd3` and whose exact executable state has
  394,833,461 parameters.

Both complete repositories were downloaded anonymously and preserved. The
paper-era model card's official companion URL redirected to a JSON HTTP 401
response, `{"error":"not_connected"}`. The response was recorded once and not
bypassed. The current card explicitly says v5 replaced earlier checkpoints and
that scores across eras are incomparable. Therefore the repair did not infer or
substitute missing paper-era code.

### Other omitted releases resolved

- Markov-informed calibration: ICLR 2026 manuscript arXiv 2602.08031 and official
  `tmlr-group/MRF_Calibration` commit
  `a21add14e162943907c1af01ddbd299db8b7faf8`; the immutable public source archive
  is preserved.
- Exons-Detect: manuscript arXiv 2603.24981 and official
  `Xiaoweizhu57/Exons-Detect` commit
  `239862c0a9bb580b7cf883b5efdfab1570bb0e8f`; the immutable public source archive
  is preserved. The repository states that its tests validate scoring math rather
  than end-to-end model downloads and does not ship the paper's complete
  mutation-repair path or detector state.
- DACTYL/Vanguard: manuscript arXiv 2607.17382; official public Hugging Face
  ModernBERT revision `82306100e5a8f1d31e495579d740ac7ff6f62336` and DeBERTa
  revision `c2e282cedc8d4ef8dd30d1cc1098d297b26ce258`. Their model-card claims are
  retained as released watchlist evidence, not treated as a DW1 reproduction.

No credential, authenticated model, PB state, persistent browser/session state,
or human-owned tmux session was accessed.

### MELD execution and preservation

`benchmark_meld.py` reproduces only the exact self-contained v5 model-card
architecture. It validates immutable current and paper-era weight hashes, tests
one-GPU batch 1, one-GPU batch 8, and two concurrent batch-4 replicas at exactly
2,048 tokens, then scores all 8,022 available trial texts. It preserves the prior
seed-42 direct screen and adds a disjoint human calibration/evaluation split over
the 4,907 texts meeting v5's 100-word minimum.

The first isolated run used Python 3.14 and failed before inference because the
third-party ModernBERT implementation decorates a function with `torch.compile`,
which rejects that interpreter. Its raw stdout and stderr are retained. The
successful run used Python 3.13; raw stdout, raw stderr, all 8,022 score rows,
package/interpreter/GPU manifests, and model-file hashes are retained without
curation. `benchmark_meld_design.md` fixes the question, sample selection, timing
boundary, metrics, command, and interpretation.

### Discoverable public evidence collection

Every new public paper, raw query, official snapshot, API metadata record, and
relevant HTTP response is preserved at:

`/ssd1/sichangheagent/dw1_detector_survey_public_artifacts/2026-08-08`

The collection has its own README and `MANIFEST.sha256` covering every retained
file other than the ledger itself. `paper_artifacts.md` records the path and key
identities. This replaces the earlier unverifiable phrase “established external
paper collection” with a discoverable, integrity-checkable location.

## Semantic-coverage repair: 2026-08-08

The next evaluator found that identifier accounting had hidden LM²otifs and
NEULIF inside a mixed catch-all. The three raw exact-phrase exports were not
refetched or edited. A new row-level audit treats their frozen title and abstract
text as the discovery surface and the arXiv identifier as the unique mapping key.

The initial row-level project's exact command was:

```text
uv run --isolated --no-project --python 3.13 python audit_coverage.py \
  --map coverage_row_dispositions.tsv \
  --output coverage_semantic_audit.tsv \
  --report coverage_semantic_audit_report.txt \
  --environment coverage_semantic_audit_environment.txt
```

It parsed 204 raw export entries into the unchanged 119 unique 2025–2026 rows.
Patterns conservatively flagged 106 rows for SOTA, best/first-rank,
comparative-improvement, high/robust/near-perfect performance, accuracy claims,
named accuracy/threshold metrics, or explicit percentages of at least 90. The
reviewed mapping assigns 68 rows explicit dispositions and 51 mechanically
allowlisted non-candidate classes. Every flagged non-candidate has a specific
false-positive explanation. Kind-specific code-to-definition allowlists reject
unknown, wrong-kind, and catch-all codes, and the generated audit emits the bound
definition beside each matched fragment and primary URL. The report binds the
command, script, mapping, exports, output, environment, and counts by SHA-256 and
returns PASS.

Four validation-negative controls used the recorded Python 3.13 interpreter,
process-substituted mappings, and `/dev/null` outputs: removing the last row,
duplicating the first data row, replacing a code with `catch_all`, and assigning
the non-candidate `analysis_only` code to an explicit disposition. Each exited
1; the unchanged mapping exited 0. A separate broader expression covering
accurate, near-perfect, first-rank, F-score, ROC, TPR/FPR, and high-percentage
forms found no matching unflagged row after the repair.

### LM²otifs and NEULIF primary and artifact checks

One anonymous arXiv metadata request for identifiers `2505.12507,2511.21744`
resolved both current revision-2 records. Their public PDFs were downloaded
directly and preserved. LM²otifs reports “state-of-the-art performance”; NEULIF
reports a 99.5 percent ROC-AUC. Those phrases triggered review rather than
promotion.

Neither paper links a repository or checkpoint. Anonymous GitHub repository
searches used each method name, exact title, and arXiv identifier. LM²otifs
returned no repository; NEULIF name-only matches were unrelated and its exact
title/identifier returned none. Anonymous Hugging Face model and Space searches
by method name returned none. The raw public JSON responses are retained. This
is a bounded artifact check, not a universal nonexistence claim.

One combined anonymous public Google Scholar first-page request for
`"LM2otifs" OR "NEULIF"` returned HTTP 200 without a robot challenge. It exposed
the primary arXiv record and unrelated lexical matches, not an official detector
release. No cookie jar or persistent session was used; response cookies were not
stored or sent. The raw body is retained. The general web-search connector again
returned HTTP 404 and supplied no evidence.

The anonymous Kaggle API's exact-title result matching NEULIF's roughly 500,000
essays was `shanegerami/ai-vs-human-text`. Its public metadata says the essays
were combined from multiple sources but does not name generators, domains, or
lengths. Search and metadata JSON are retained; because the paper itself does not
name the owner/reference, this match remains inferred rather than definitive.

No local A6000 run was performed. LM²otifs releases neither code nor its trained
graph, vocabulary, GCN state, or threshold; reconstructing it would not reproduce
the paper. NEULIF releases neither classifier, scaler, feature schema, split
indices, nor timing protocol; retraining a substitute would test a different
state. Their exact scientific blockers are recorded in source cards N13 and N14.

### Preservation after row promotion

The initial semantic review moved thirteen other results from catch-alls into explicit
dispositions. Their primary PDFs were downloaded from the exact frozen arXiv
revision and preserved. DP-MGTD revision 2 was the sole exception: its abstract
page returned HTTP 200 but its revision-2 PDF returned 404, so the public
revision-1 PDF is retained and labeled rather than silently substituted.

The first fresh semantic reviewer then found six high-scoring shared-task systems
whose missing artifact, low-FPR, or deployment evidence had been mislabeled as a
false-positive reason. A separate broader trigger check found the general
comparative detector 2603.18750. All seven were moved to individual dispositions;
their PDFs were preserved, and the three paper-linked GitHub repositories were
pinned and archived. Those repositories contain scripts or notebooks but no
trained checkpoints, so no scientifically comparable A6000 run was possible.

The public download pattern was:

```text
curl --fail --location --silent --show-error \
  --output /tmp/ARXIV_ID.pdf https://arxiv.org/pdf/ARXIV_ID
curl --fail --silent --show-error \
  https://api.github.com/repos/OWNER/REPO
curl --fail --silent --show-error \
  https://api.github.com/repos/OWNER/REPO/commits/DEFAULT_BRANCH
curl --fail --location --silent --show-error \
  https://github.com/OWNER/REPO/archive/COMMIT.tar.gz
```

The client was curl 7.81.0 with OpenSSL 3.0.2; PDF text checks used Poppler
`pdftotext` 22.02.0. All endpoints were anonymous and public. Exact PDF, archive,
repository-metadata, and commit-metadata hashes are in the external manifest;
primary and archive anchors are repeated in source card N15 and
`paper_artifacts.md`.

At that review stage, the explicit export table had 68 identifiers and the
targeted carry-forward table had three. A mechanical filename audit found a
retained primary PDF for all 71. That historical external ledger covered 150
files and had SHA-256
`1b92b652294562b6f1abbad3064c2c0f2b0fa2c49ff23e30b3937d5e9cdba67c`;
all entries verified before that candidate was restored to read-only.

## Generalized composite-source repair: 2026-08-08

The next evaluator showed that publication-level semantic flags still allowed an
overview or benchmark disposition to hide named high-score systems. The three
raw Atom exports remained unchanged. The generalized command is:

```text
uv run --isolated --no-project --python 3.13 python audit_coverage.py \
  --map coverage_row_dispositions.tsv \
  --composite-sources coverage_composite_sources.tsv \
  --embedded-results coverage_embedded_results.tsv \
  --expected-results coverage_expected_result_ids.tsv \
  --source-cards coverage_composite_dispositions.md \
  --output coverage_semantic_audit.tsv \
  --embedded-output coverage_embedded_result_audit.tsv \
  --report coverage_semantic_audit_report.txt \
  --environment coverage_semantic_audit_environment.txt
```

The unchanged exports contain 204 raw entries and 119 unique 2025–2026
publications. The row layer has 106 semantic flags, 70 explicit dispositions, and
49 allowlisted non-candidate classes. Title and publication-class rules select 33
composite sources. At that repair stage, 24 expanded to 180 named qualifying
system/version results and nine retained table/section-specific no-qualifier or
parent-only reasons. Eleven regression and negative controls pass, including removal of the
whole Task 3 review, removal of only CNLP-NITS, a missing non-anchor child with a
lowered mutable count, reclassification of a known high-cell parent as a
no-qualifier, an invalid source-card label, removal of a real E-card, wrong
parent/result bindings in a real E-card, an analogous count mismatch, and weak
and complete negative-source controls. The hand-reviewed exact-result inventory is
SHA-256-bound by the checker, so deleting an inventory row is not an accepted
way to make a source disappear.

The audit also parses the machine-readable marker under every E-card heading in
`coverage_composite_dispositions.md`. The Markdown file is checker-hash-bound;
each marker must bind its label and parent to exactly the same result-ID set as
the independent inventory and result ledger. A label-only string cannot stand
in for missing or misassociated source-card evidence.

A fresh adversarial reviewer found that the earlier aggregate-only rule still
hid Table 2 variants in arXiv 2604.16607 and 2510.12476. Removing that escape
hatch added their 18 named systems, then a full reread added five qualifying
attack-study detector states, 39 Task 1 English/multilingual submission states,
and the Unibuc system paper's high validation/source result. A final consistency
pass adds two Urdu training/precision crossings plus five public and fourteen
study-fitted systems from the author-role bias source. Each new row binds
the high slice to its weak mean, personalized, adversarial, or official aggregate
result. Twelve ACL Task 1 primary papers and official NeurIPS BiScope/DeTeCtive
PDFs were downloaded anonymously and preserved; overview-stated manuscript
absence remains explicit for teams without a primary paper.

A closing table-by-table pass applied the same rule without source-specific
exceptions. It added 61 configurations that the preceding repair still hid:
additional Task 3 versions and controls, high length/attack/domain/language
slices, older score baselines, the author-role-bias study's fitted classifiers
and ensembles, and its mdok comparison. The final inventory therefore contains
At that predecessor composite-only stage, the inventory contained 241 exact
result IDs from 26 expanded sources; seven sources remained
no-qualifier only after their inspected tables and non-candidate high values are
stated explicitly. Each isolated high cell retains its weaker mean, overall,
other-class, or official aggregate in the same row. The checker binds the exact
241-ID set rather than trusting per-parent counts. The later full-table repair
supersedes that count with the 263-ID inventory recorded below.

### Task 3 and primary-system resolution

The Task 3 overview was downloaded anonymously from arXiv 2501.08913. Its four
primary system papers were downloaded from the public ACL Anthology endpoints
`2025.genaidetect-1.38`, `.39`, `.40`, and `.42`. Tables 4–5 and the bibliography
were inspected together; four Leidos versions, Pangram, USTC-BUPT, ALERT, and
CNLP-NITS now have separate result rows. The Pangram paper describes preprocessing
before tokenization but does not specify whether deployed inference transforms
the target, so its closed-state gap—not a guessed method exclusion—governs its
disposition. CNLP's attack-conditioned target normalization/rewrite is an
inference-stage exclusion.

`coverage_primary_search_log.md` preserves the exact anonymous public OpenAlex,
DBLP, and GitHub commands and result summaries for USTC-BUPT and the three
Counter Turing systems without cited primary papers. The returned JSON is in the
external collection. A DBLP HTTP 500 for Llama_Mamba is explicitly not counted as
negative evidence. No Scholar challenge or authenticated source was used.

A post-freeze primary-source identity check found two narrow preservation errors
before commit. Composite parent 2505.24523 lacked its PDF; the exact public arXiv
PDF was added. Two embedded FastDetectGPT rows pointed to unrelated arXiv
2305.16783 and now cite the correct 2310.05130 primary paper. DetectLLM rows
already cited correct arXiv 2306.05540, but two inherited external filenames used
unrelated 2306.05594. The correct 2306.05540 PDF was added and the unrelated bytes
were retained only for ledger continuity, explicitly disclaimed in
`paper_artifacts.md`. These checks used anonymous arXiv API/PDF endpoints and did
not alter the accepted detector conclusions.

### Public composite-detector states and execution

Anonymous Hugging Face metadata and files fixed three complete revisions:

- `WUJUNCHAO/DetectRL-X-XLM-RoBERTa-Detector-All` at
  `76649a0257a812a81cf36b5de9cc5f2430aeaa7f`;
- `desklib/ai-text-detector-v1.01` at
  `5fdea974cd4287c61674951ec78803aa274e2fb7`; and
- `GeorgeDrayson/modernbert-ai-detection` at
  `08f218f1d05791ad99c26ede421f69c781a50360`.

Paper-linked official GitHub repositories were resolved through anonymous API
metadata and archived at exact commits for DetectRL-X, Desklib, C-ReD, ALHD,
model collapse, and ELFEN. Their identities and hashes are in
`paper_artifacts.md`; source is never substituted for a missing trained state.

The successful screen command was:

```text
cd /ssd1/sichangheagent/dw1/docs
/tmp/dw1-meld-venv/bin/python \
  notes/dw1_detector_survey_sources/benchmark_composite_detectors.py \
  --model-root /tmp/dw1-rev3-models \
  --scores-out /tmp/benchmark_composite_detectors_scores.csv
```

Raw stdout/stderr and the exact 8,022-row CSV are retained. The first attempt
completed DetectRL-X and Desklib but failed when ModernBERT's public
`reference_compile=true` optimization encountered a two-replica FX/Dynamo error
under Transformers 4.57.3. The successful run disables only that in-memory
optimization flag; weights, tokenizer, forward mathematics, and score semantics
remain unchanged. Both attempts are preserved. A separate verifier reconstructs
the seeded splits and recomputes all AUROCs and operating points from the score
CSV. Ruff, basedpyright, model-file checks, packages, interpreter, and GPU details
are durable beside the harness.

### Pre-eval5 external freeze

The predecessor external collection contained 274 files other than its ledger;
the later full-corpus freeze below supersedes this count with 288 files.
The post-review additions are the missing composite parent 2505.24523, the
correctly identified DetectLLM 2306.05540 PDF, twelve Task 1 primary system
papers, official BiScope and DeTeCtive PDFs, nine closing-pass primary PDFs,
and the immutable DC-PDD archive plus metadata; the README correction is
included within the same manifest. That predecessor `MANIFEST.sha256` had SHA-256
`6aeb1d786e1c91eb6c7e3f0723d129a6a562586c57024227c7082bbbdf5f4529`.
All 274 predecessor entries verified, and a permission audit found zero writable
collection files or directories. The collection contained only public anonymous evidence;
no PB, human, authenticated, persistent browser/session, robot-bypass, or
human-owned tmux state was accessed.

## 2026-08-09 eval5 full-corpus semantic repair

The completed eval5 verdict was read before this repair. Its SHA-256 is
`83a0ae2d665fda4e549cbb573c4845db685b54fc6880b4004dbb9ae6c4102165`;
the frozen next-evaluator prompt SHA-256 is
`ab0c2d2a7bddb41a7739012b18e48ce4aa2cbe6735b287c971045d3cbc30fd87`.
The repair did not open a new search lane. It completed the already bounded
119-publication corpus and replaced title/class discovery with primary-PDF
content review.

Fourteen missing corpus PDFs were fetched from anonymous public arXiv export
PDF endpoints and checked with `pdfinfo`: 2608.03859, 2607.14905, 2605.03723,
2605.02712, 2604.21365, 2604.21300, 2604.04932, 2511.17402, 2510.00890,
2509.25154, 2508.18715, 2503.23622, 2501.18998, and 2501.14288. The reproducible
request form was:

```text
curl --fail --location --silent --show-error \
  https://export.arxiv.org/pdf/ARXIV_ID \
  --output papers/ARXIV_ID.pdf
pdfinfo papers/ARXIV_ID.pdf
sha256sum papers/ARXIV_ID.pdf
```

No credentials, cookies, persistent browser profile, PB, robot-challenge bypass,
or human-owned tmux state was used. The resulting collection has 288 manifest
entries. `MANIFEST.sha256` has SHA-256
`e9ae35623cb3b808368cc9729d001bc33940b71148814199402c9d2b4149dd97`;
all entries and the exact path set verified, and no collection path is writable.

Every primary PDF was extracted with Poppler's `pdftotext -layout -enc UTF-8`.
`build_fulltext_inventory.py` then materialized the curated table-derived
inventory:

```text
uv run --isolated --no-project --python 3.13 python \
  build_fulltext_inventory.py \
  --external-root /ssd1/sichangheagent/dw1_detector_survey_public_artifacts/2026-08-08
```

The reproducible output is 119 source rows, 987 exact detector accounts, and 724
primary-result dispositions. No parent-only account remains; six sources have
table-derived no-account decisions. The immutable account-pair digest is
`3a2f45d49a5909e3e13cfd92876eca8656c5a03b478d250f77a1876c35b35cd4`.
The four generated input hashes and the exact audit replay command are preserved
in `coverage_semantic_audit_report.txt`; interpreter, platform, Poppler version,
and extraction command are in `coverage_semantic_audit_environment.txt`.

The official Leidos paper was re-read directly from
`papers/2025.genaidetect-1.39.pdf`. Its method and submission tables map
BC/v1.0.1 to unweighted binary DistilRoBERTa, BW/v1.0.3 to weighted binary,
MC/v1.0.4 to unweighted multiclass, and MW/v1.0.2 to weighted multiclass. The
prior v1.0.4 ensemble wording was false and was corrected in the result row and
E1 evidence card. A dedicated mutation control now rejects that wording.

A fresh adversarial mutation of the first full-text repair exposed two remaining
manual-list omissions: the nine Chinese encoder/LoRA states in 2509.00731 and
eight POGER/SeqXGPT/SenDetEX/SenFlow states in 2606.18946. Rechecking the entire
former zero/parent partition also made five 2501.14288 architecture stages, both
LuxVeri ensembles, and every other qualifying named configuration explicit. The
checker now binds these exact ID sets to table text and rejects a lowered-count
non-English omission plus positive- and zero-decision content detachment.

A final all-paper table pass caught 17 additional narrow-slice accounts that a
weak aggregate had suppressed: ten TELL comparators in arXiv 2605.27921, five
late-stage stability baselines in 2601.04833, and ReMoDetect plus ImBD in
2604.16923. Their exact table cells, weaker aggregate evidence, mechanisms,
artifact status, and dispositions are now separate rows. Content anchors bind
all three paper-specific ID sets to their extracted table text. Two additional
controls reject deletion of ChatGPT-D while lowering the mutable count and
detachment of that row from its table text.

The next fresh reviewer exposed a disposition-level version of the same
grouping defect in arXiv 2509.15550: DNA-DetectLLM's regeneration blocker had
been inherited by eight named baselines. The primary paper was re-read; every
baseline now has exact Table 1/Table 2 evidence and its actual mechanism.
DetectGPT retains a multi-perturbation exclusion, seven ordinary baselines are
evidence-rejected, and only the seven DNA repair/order/model-pair states remain
regeneration-excluded. A code anchor and mutation control protect this split.

The resulting all-exclusion-parent audit also corrected arXiv 2504.21019. Its
uniform and Gaussian perturbations alter embeddings during training only; the
paper explicitly describes direct target-domain inference. The states are now
evidence-rejected on their 85.48%/86.10% seven-domain average accuracy, absent
frozen state, absent low-FPR result, and absent fixed A6000 timing rather than
being falsely method-excluded.

The eval6 challenge found another account-identity defect in three bound PDFs.
PAWN now has separate RADAR-FT and five-epoch M4 RoBERTa-base rows. The generic
Vanilla row in arXiv 2607.03680 is replaced by its four IntelLabs/base,
MAGE/large, FAID/base, and MIRAGE/large fitted states. READER now separates ImBD
trained on READ from target-adapted ImBD*. These are eight explicit identities
and seven net new accounts. Their result-specific rows preserve diagonal,
oracle-threshold, and target-adaptation limits and do not promote them.

The generalized table-resolution repair then applied the same account rule to
every independently extracted row rather than only those eight fixtures. It
expanded the language/training states in arXiv 2509.26051; dataset-fitted
RoBERTa, DeTeCtive, stylo, and mcgovern states in 2604.16607; both M4
training-based states in 2510.12476; comparison states in NEULIF, DivEye, and
PhantomHunter; and method/backbone ablations in DivScore. Every added row keeps
its weaker aggregate, domain, artifact, method, calibration, and timing limits.
The complete result sets are 263 embedded rows plus 724 primary rows.

The eval7 challenge showed that the preceding scanner recognized only Arabic
table numbers and therefore missed Roman-caption tables, Figure 4 legends, and
all candidate evidence in fourteen predecessor zero-yield sources. Direct
inspection identified 29 omitted states: eight base rows in 2605.16107, ten
base/DALD/Glimpse rows in 2604.02008, four zero-shot comparators in 2510.02319,
and seven RAIDAR/hosted-prompt/CAMF rows in 2508.11933. Each now has exact strong
and weak evidence, mechanism, artifact status, method disposition, two-A6000
feasibility, and timing treatment. None passes the fixed promotion screen.

To separate discovery from the curator-authored inventory,
`discover_table_accounts.py` independently runs `pdftotext -layout` over all
119 source-ledger PDFs, recognizes Arabic and Roman tables plus compact figure
legends, carries explicit metric declarations across page boundaries, normalizes
mathematical Unicode metric glyphs and spaced F1 labels, and finds 4,812
high-threshold result candidates. It also emits one
content-hash-bound scope summary for each of the 119 PDFs, including every
former zero-yield source, and only then resolves every candidate against the
account ledger or a content-specific non-candidate class. A separate binding
phase emits one hash-bound source witness for every one of the 987 accounts,
without using those bindings to seed or suppress the raw queue. This
closes Review 16's concrete DMAP counterexample: Table 1's six
FastDetectGPT/Binoculars scorer configurations now bind to the AUROC definition
in Appendix K.

```text
uv run --isolated --no-project --python 3.13 python \
  discover_table_accounts.py \
  --sources coverage_fulltext_sources.tsv \
  --paper-root /ssd1/sichangheagent/dw1_detector_survey_public_artifacts/2026-08-08 \
  --output coverage_table_candidates.tsv \
  --accounts coverage_fulltext_expected_accounts.tsv \
  --match-output coverage_table_discovery.tsv \
  --witness-output /tmp/dw1_predecessor_witnesses.tsv

uv run --isolated --no-project --python 3.13 python \
  witness_ownership.py \
  --sources coverage_fulltext_sources.tsv \
  --paper-root /ssd1/sichangheagent/dw1_detector_survey_public_artifacts/2026-08-08 \
  --accounts coverage_fulltext_expected_accounts.tsv \
  --table-candidates coverage_table_candidates.tsv \
  --table-discovery coverage_table_discovery.tsv \
  --predecessor-ownership coverage_predecessor_witness_ownership.tsv \
  --output coverage_account_witnesses.tsv
```

The raw-candidate SHA-256 is
`08a293da9a3e6acc46b3f606939655a1c72b2494b10b7b9399ebe2073ddae2c1`;
the match-ledger SHA-256 is
`71d5274ba80c82b143a71c624459c53d873494b3eb4a75ef968a0ffcbae76fe5`.
The 987-row witness-ledger and 321-row predecessor-ownership-ledger SHA-256
values are recorded in the final candidate manifest. The second command
re-derives all 987 predecessor witnesses, proves the exact 225 `same_window` and
95 generic configuration rows, and replaces all 320 with exact source-owned
joins; a fine-tuned DeBERTa companion makes the reviewed ledger 321 rows. The
semantic audit regenerates the final witness output byte-for-byte and rejects an
unresolved, removed, mutated, or mis-targeted resolution or witness. Sixty-eight full-text controls include
the content-discovered fitted baseline, four separately trained states,
READER method inheritance, four direct resolution-ledger mutations, and four
source-form mutations covering scope summaries, Roman captions, figure legends,
and direct evidence under predecessor zero-yield sources, plus mutations of the
987-witness source, identity, metric, configuration, and join bindings and
detachment of an off-page metric definition, source-independent Unicode-F1
discovery with a metric-context guard, and direct candidate binding for the
recovered architecture row. They additionally derive the external README's
4,812-result plus 119-summary
total and reject the unrelated Anchor/Table 2 metric or a neighboring Table 4
or Table 11 column as evidence for any of the five repaired distribution-shift
accounts. They also reject a neighboring PAN12 metric, a Longformer-to-GCN
column substitution, and replacement of the complete GCN row by Longformer's
row. Six final mutations reject removal of an ownership row, restoration of a
heuristic witness, wrong-row and wrong-column substitutions, and
zero-shot/fine-tuned DeBERTa or base/MCGrad training-state swaps. Three further
controls swap the two J-Detector ablations, swap DetectAnyLLM scorer rows, and
select DetectGPT's uncertainty instead of its AUROC. The 321-row source audit
also corrected LAPD's model-size numeral, three neighboring DetectAnyLLM rows,
the two J-Detector decrease annotations, the public Qwen2-0.5B IRM label, base
Binoculars and ImBD rows, three DivEye backbones, and DetectGPT's AUROC cell.
Every wrong-column record now freezes its exact source-row semantic result
interval, all in-boundary result-cell indexes, and the selected alternate
result-cell index. This changed exactly the two PAWN component-count donors,
Exaone 3.5, and the Candace/TF-IDF System 3/System 2 identifiers to real
same-row result metrics. Nine controls also reject those five patterns plus a
CUDA version, numeric model-name fragment, slash-delimited identifier, and
text-length parameter. Wrong-row and wrong-state donors bind a different exact
source result rather than a rank, year, model-size numeral, axis tick, or
uncertainty. Sixty-eight full-text controls now pass. The content
mutations bypass the immutable-ledger digest gate while retaining exact source
validation. With the eleven composite controls, all 79 pass.
The audit was run by the exact recorded
`uv run --isolated --no-project --python 3.13` command; its environment record
now reports CPython 3.13.11 rather than bytes produced by a different interpreter.
