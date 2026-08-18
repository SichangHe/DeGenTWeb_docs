# Model equivalence framing

Checked 2026-08-18 against current official provider pages.

## Rule

Use an alternative model as a proxy only when the provider documents
comparable or better performance on the task family we are studying.
Write that as a DW inference from scoped provider evidence, not as
provider-endorsed blanket equivalence.

This does not replace the headline model-era cutoff in
`llm_dominant_generation_evaluation_plan.md`. A 2025 small model is not a
documented stand-in for a 2023 model unless the provider actually compares
those two.

## Anthropic

Claude Haiku 4.5 vs Claude Sonnet 4. The Oct 15, 2025 launch says Haiku 4.5
gives "similar levels of coding performance" to Sonnet 4 "at one-third the
cost and more than twice the speed", and "even surpasses Claude Sonnet 4 at
certain tasks, like using computers". The same post says it "serves as a
drop-in replacement for both Haiku 3.5 and Sonnet 4" on the API, Amazon
Bedrock, and Vertex AI.

https://www.anthropic.com/news/claude-haiku-4-5

The current Haiku product page is stronger on scope: "matching Sonnet 4's
performance on coding, computer use, and agent tasks".

https://www.anthropic.com/claude/haiku

The current models overview calls Haiku 4.5 "The fastest model with
near-frontier intelligence". It does not repeat the drop-in-replacement
sentence.

https://platform.claude.com/docs/en/about-claude/models/overview

Claude 3.5 Haiku vs Claude 3 Opus. The Oct 22, 2024 post says 3.5 Haiku
"matches the performance of Claude 3 Opus, our prior largest model, on many
evaluations" and "surpasses even Claude 3 Opus ... on many intelligence
benchmarks". The same post says it scores 40.6% on SWE-bench Verified,
"outperforming many agents using publicly available state-of-the-art
models—including the original Claude 3.5 Sonnet and GPT-4o".

https://www.anthropic.com/news/3-5-models-and-computer-use

Claude 3 Sonnet vs Claude 2. The Mar 4, 2024 family post says "For the vast
majority of workloads, Sonnet is 2x faster than Claude 2 and Claude 2.1 with
higher levels of intelligence."

https://www.anthropic.com/news/claude-3-family

Same-tier upgrades. Sonnet 4.5 is "a drop-in replacement that provides much
improved performance for the same price" versus prior Sonnet, not a
smaller-as-larger claim.

https://www.anthropic.com/news/claude-sonnet-4-5

Sonnet 5 "narrows the gap: its performance is close to that of Opus 4.8",
and "its higher-effort performance can match Opus 4.8 on some tasks". Useful
same-family precedent; it does not make Sonnet 4.6 a documented proxy for
Sonnet 4.

https://www.anthropic.com/news/claude-sonnet-5

## OpenAI

GPT-4.1 mini vs GPT-4o. The GPT-4.1 API post says GPT-4.1 mini is "even
beating GPT-4o in many benchmarks" and "matches or exceeds GPT-4o in
intelligence evals while reducing latency by nearly half and reducing cost
by 83%". The same page's SWE-bench Verified table reports GPT-4.1 mini at
23.6% versus GPT-4o at 33.2%, so this is not a coding-equivalence claim.

https://openai.com/index/gpt-4-1/

GPT-4o mini vs GPT-3.5 Turbo. The GPT-4o mini post says it "surpasses
GPT-3.5 Turbo and other small models on academic benchmarks across both
textual intelligence and multimodal reasoning", with "improved long-context
performance compared to GPT-3.5 Turbo".

https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/

gpt-oss-120b vs o4-mini. The gpt-oss post says gpt-oss-120b "achieves
near-parity with OpenAI o4-mini on core reasoning benchmarks" and "matches
or exceeds OpenAI o4-mini on competition coding (Codeforces), general
problem solving (MMLU and HLE) and tool calling (TauBench)". gpt-oss-20b
"delivers similar results to OpenAI o3-mini on common benchmarks". These
are not GPT-4o claims.

https://openai.com/index/introducing-gpt-oss/

GPT-5 mini is described as the ChatGPT fallback after GPT-5 usage limits,
"a smaller, faster, and highly capable model". No official benchmark
sentence was found that it matches GPT-4o.

https://openai.com/index/introducing-gpt-5/

## Other providers

DeepSeek-R1 vs OpenAI o1. DeepSeek's Jan 20, 2025 release says
"Performance on par with OpenAI-o1" and "Math, code, and reasoning tasks on
par with OpenAI-o1". Distilled "32B & 70B models on par with OpenAI-o1-mini".
This is DeepSeek's claim about o1-class reasoning, not about Claude or
GPT-4o.

https://www.deepseek.com/en/news/deepseek-r1/

Gemini 3 Flash vs prior Pro. Google says Flash "combining Gemini 3's
Pro-grade reasoning with Flash-level latency" and "significantly
outperforming even the best 2.5 model, Gemini 2.5 Pro, across a number of
benchmarks". MMMU Pro is "comparable to Gemini 3 Pro". SWE-bench Verified
78% "outperforming ... Gemini 3 Pro". External precedent; Gemini is not in
the current DW Bedrock matrix.

https://blog.google/products-and-platforms/products/gemini/gemini-3-flash/

Llama 3 vs Llama 2. Meta says the 8B and 70B Llama 3 models "are a major
leap over Llama 2 and establish a new state-of-the-art for LLM models at
those scales". That is a same-size successor claim, not Llama 3 8B as a
proxy for Llama 2 70B.

https://ai.meta.com/blog/meta-llama-3/

Amazon Nova pages describe Micro, Lite, Pro, and Premier as different
price-performance tiers. No official Micro-equals-Pro or Lite-equals-Pro
sentence was found on 2026-08-18.

## What DW can use

Current Bedrock recent-model stress test
(`codebase_index/bedrock_synth_site_eval.md`):

- Claude Haiku 4.5 as a scoped proxy for Claude Sonnet 4 on coding,
  computer-use, and agent tasks
- Claude Sonnet 4 as the referenced larger model when still available
- Claude Sonnet 4.6 as a distinct later Sonnet point, not as a
  provider-documented proxy for Sonnet 4
- GPT-OSS-120B as OpenAI's documented open-weight comparison to o4-mini on
  the cited reasoning and tool-use benchmarks
- DeepSeek R1 as DeepSeek's documented o1-class reasoning/code comparison,
  kept in the named recent-model stress test, not in the headline set

Headline era rule, if exact 2023 models are missing and the 2024-06-30
extension is used:

- Claude 3 Sonnet as Anthropic's documented faster, higher-intelligence
  successor to Claude 2 / 2.1 (March 2024, inside the extended cutoff)
- Llama 3 70B as Meta's documented same-scale successor to Llama 2 70B
  (April 2024)

GPT-4o mini is OpenAI's documented successor to GPT-3.5 Turbo on the cited
academic benchmarks, but it was released 2024-07-18, after the extended
cutoff, so it is not a headline-extension candidate.

If DW expands beyond Bedrock to the OpenAI API:

- GPT-4.1 mini as a scoped proxy for GPT-4o on OpenAI intelligence evals
- GPT-4.1 as OpenAI's documented GPT-4o successor that also improves coding
- not GPT-4.1 mini for SWE-bench-style coding
- GPT-4o mini as a scoped successor for GPT-3.5 Turbo on the cited academic
  benchmarks, only outside the headline set because it is after 2024-06-30

## Do not claim

- Haiku 4.5 is generally equivalent to Sonnet 4 on all tasks
- Haiku 4.5 is a documented proxy for Claude 2
- GPT-4.1 mini is equivalent to GPT-4o for coding
- GPT-OSS-120B is equivalent to GPT-4o
- Llama 3 8B is a documented proxy for Llama 2 70B
- Amazon Nova Micro or Lite equals Nova Pro
- DeepSeek R1 is equivalent to Claude or GPT-4o
- GPT-5 mini is a documented GPT-4o proxy
