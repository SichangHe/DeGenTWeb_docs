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
repository or checkpoint for EchoPrompt or Steer-to-Detect. Exact-title searches
for DWT-Fusion found only an unrelated 2020 repository. Repository absence is
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
