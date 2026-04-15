# Bhaskar dataset note

## Source

- User-provided author message in chat:
  - "these are 3 more datasets created by changing prompts and some extra post processing."
  - "The latest one, dataset-4 seems the best out of 3 because some earlier ones have few issues"
  - issue note: "models are leaking their thoughts in the final output"
  - issue note: "the final html usually gets cut-off from the end"
  - concern note: "before moving to Bedrock, maybe we should spend some time on finalizing the pipeline"

## Structured summary of what the author said

- Claim: there were three additional dataset variants made by changing prompts and adding some post-processing.
- Claim: among those three variants, the one the author called `dataset-4` looked best.
- Claim: earlier variants had quality issues.
  - Some models leaked chain-of-thought-style text into final HTML.
  - Some generations spent too many tokens on reasoning, so final HTML was truncated.
  - The author changed prompts and parameters to improve the pipeline, but still expected unknown issues.
- Claim: the JSON files contain prompts and token counts and can be used to inspect generation cost/behavior.
- Opinion/question from author: they were considering Bedrock later, wanted help finalizing the pipeline first, and wondered whether Codex with a strong `AGENTS.md` might generate better template sites.

## What the current ZIP actually contains

- Fact: `data/bhaskar_llm_sites20260412.zip` contains nine timestamped generation runs under `dataset/<run_id>/...`.
- Fact: each run has one `generation_run_*.json` file plus generated HTML files.
- Fact: the archive metadata uses run timestamps like `20260410_192044` and `20260412_055748`; it does not carry an internal label such as `dataset-3` or `dataset-4`.
- Fact: the run-level JSON schema includes fields like `output_root`, `initial_seeds`, `generated_categories`, `category_generation_request`, and `websites`.
- Fact: the site-level JSON schema includes `site_name`, `category`, `theme`, `persona_description`, `simulated_prompt`, and page-level prompts/requests.

## Dataset numbering: what is known vs inferred

- Fact: I found no string like `dataset-3` or `dataset-4` inside the ZIP JSON metadata.
- Fact: the current archive path and internal folder names do not explain the numbering in the author message.
- Inference: the `dataset-3` / `dataset-4` labels were probably external filenames or conversation-level names, not preserved inside the archive.
- Inference: when the author said `dataset-4` was "the best out of 3," they were likely referring to a later variant not explicitly labeled inside this ZIP, or to a renamed successor of an earlier external bundle.
- Conclusion: from local artifacts alone, the numbering mismatch cannot be resolved with certainty; only the author message provides those labels.

## Provenance note relevant to classification

- Fact: the ZIP metadata shows synthetic-generation fields such as `persona_description`, `simulated_prompt`, `site_plan_request`, and per-page generation prompts.
- Fact: I did not find metadata fields indicating source-site provenance, paraphrase provenance, or a note that these were rewritten human sites.
- Conclusion: based on the JSON alone, these should be treated as directly generated synthetic sites, not documented paraphrases of human originals.

## Current scope decision

- User instruction: do not spend time on the author's speculative pipeline worries here.
- For this task, the useful parts of the author message are: dataset lineage is messy, prompt/post-processing changed across variants, and the JSON files are the ground truth for prompts/requests/tokens.
