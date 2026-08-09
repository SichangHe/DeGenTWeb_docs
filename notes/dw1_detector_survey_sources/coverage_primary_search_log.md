# Bounded public primary-system searches

Run date: 2026-08-08, America/Los_Angeles.

These searches resolve systems named by composite overview rows when the
overview bibliography does not supply a public primary paper. They are bounded
negative evidence, not a claim of universal absence. Requests were anonymous,
read-only, and made only to public OpenAlex, DBLP, and GitHub endpoints. No
authenticated state, persistent browser profile, robot-challenge bypass, or PB
resource was used.

The four exact queries were:

- `USTC-BUPT R-L Focal Loss AI generated text`;
- `Tesla Defactify AI generated text`;
- `Llama_Mamba Counter Turing Test`; and
- `NLP_great Counter Turing Test`.

For each query the run requested at most ten OpenAlex works, ten DBLP
publications, and ten GitHub repositories. The exact public commands were
equivalent to:

```text
curl -fsSLG --data-urlencode "search=QUERY" --data-urlencode "per-page=10" \
  https://api.openalex.org/works
curl -fsSLG --data-urlencode "q=QUERY" --data-urlencode "h=10" \
  --data-urlencode "format=json" https://dblp.org/search/publ/api
curl -fsSLG -H "Accept: application/vnd.github+json" \
  -H "User-Agent: dw1-public-research" --data-urlencode "q=QUERY" \
  --data-urlencode "per_page=10" https://api.github.com/search/repositories
```

Results:

- USTC-BUPT: DBLP and GitHub returned zero. OpenAlex returned the Task 3
  overview plus an unrelated table-of-contents record, not a system paper.
- Tesla: DBLP and GitHub returned zero. OpenAlex returned the Counter Turing
  overview plus an unrelated 2023 multimodal benchmark, not a system paper.
- Llama_Mamba: OpenAlex and GitHub returned zero; the DBLP request returned an
  HTTP 500 and is not treated as positive or negative evidence.
- NLP_great: OpenAlex, DBLP, and GitHub returned zero.

The official Task 3 overview cites primary papers for Leidos, Pangram, ALERT,
and CNLP-NITS but not USTC-BUPT. The official Counter Turing overview cites
primary papers for Sarang, Dakiet, SKDU, Drocks, and AI_Blues, but not Tesla,
Llama_Mamba, or NLP_great. The exact returned JSON bodies and repository-search
responses are preserved in the external integrity collection.

## Task 1 overview resolution after high-cell review

The official public ACL volume index was fetched anonymously with:

```text
curl -fsSL https://aclanthology.org/volumes/2025.genaidetect-1/
```

It supplies exact primary papers for DCBU (`.12`), L3i++ (`.13`), TechExperts
(`.14`), SzegedAI (`.15`), Unibuc/tmarchitan (`.16`), Fraunhofer SIT (`.17`),
Nota AI (`.19`), LuxVeri (`.21`), Grape (`.22`), AAIG (`.23`), TurQUaz (`.24`),
and Advacheck (`.26`). Each PDF was downloaded from its public
`https://aclanthology.org/2025.genaidetect-1.ID.pdf` endpoint, validated as a
PDF, hashed, and retained in the external collection.

For Alfa, azlearning, honghanhh, VX1291, rockstart, nampfiev1995, starlight1,
abit7431, mail6djj, saehyunma, seven, jojoc, yaoxy, bennben, fangsifan,
yuwert777, and sohailwaleed2, the official overview provides the primary-absence
evidence directly: its system-description footnote states that teams without a
description did not submit a manuscript and did not provide a short system
description. Their result rows use `NONE_AFTER_BOUNDED_PUBLIC_SEARCH` as the
machine sentinel while spelling out that overview-bounded absence; it is not a
claim that no later or differently named artifact could exist anywhere.

The two official baselines map to the overview's own training description, not
to a nonexistent separate paper. The Unibuc system paper links public source at
`https://github.com/ClaudiuCreanga/coling-2025-task-1`, but anonymous repository
inspection found code/configuration rather than submitted detector weights.

## Closing Task 3 and benchmark-source resolution

A second complete read of Task 3 Tables 4–5 exposed additional submitted
versions and official baselines. The overview bibliography and public ACL volume
map LuxVeri to `2025.genaidetect-1.41` and MOSAIC to
`2025.genaidetect-1.44`; both PDFs were downloaded anonymously and retained.
GLTR maps to official ACL paper `P19-3019`. The OpenAI RoBERTa-large baseline
maps to its public Hugging Face model page, not to a new Task 3 state.
USTC-BUPT's additional `Roberta_dataaug.` row retains the same bounded primary-
paper absence as its earlier submission.

The newly explicit benchmark methods were resolved from the parent papers'
bibliographies rather than guessed from names. Neighborhood is Mattern et al.,
official ACL paper `2023.findings-acl.719`; ReCaLL is Xie et al., official ACL
paper `2024.emnlp-main.493`; DC-PDD is arXiv `2409.14781` and official GitHub
repository `zhang-wei-chao/DC-PDD`; HC3 is arXiv `2301.07597`; and DetectGPT is
arXiv `2301.11305`. LLM-Deviation/MFD maps to public Research Square DOI
`10.21203/rs.3.rs-3226684/v1`. All primary PDFs and an immutable DC-PDD archive
are retained in the external collection.

This identity check corrected two provisional URL matches before freezing:
arXiv `2307.03819` is an algebraic-geometry paper, and arXiv `2405.05131` is a
radar paper. Neither unrelated PDF is in the final collection or used as
evidence.
