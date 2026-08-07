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
