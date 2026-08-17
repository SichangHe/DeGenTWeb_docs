# Synthetic site generation

`agent/site_generation.py` drives Wix or B12 with Playwright, not a vision
agent. Run it with a dedicated, already-authenticated Chrome profile; never
put credentials in the command line, checkpoint, or log.

```sh
uv run python -m degentweb.agent.gen_wix \
  --profile-dir data/browser/wix-generation-profile \
  --manifest data/wix-site-manifest.jsonl \
  --output-dir data/generation-checkpoints
uv run python -m degentweb.agent.gen_b12 \
  --profile-dir data/browser/b12-generation-profile \
  --manifest data/b12-site-manifest.jsonl \
  --output-dir data/generation-checkpoints
```

For the authorized one-site personal-browser pilot, use a desktop
Chrome/Chromium process that has been started with remote debugging bound to
the local machine (for example, `--remote-debugging-address=127.0.0.1` and
`--remote-debugging-port=9222`). It must use the existing persistent profile,
be visibly open, and already be authenticated by its human owner. Keep one
query-free Wix dashboard (`manage.wix.com`) for profile mode, or a B12
`/client/<id>/site_builder/` tab for the personal-browser pilot; do not share
an everyday browsing window. The supplied endpoint must be a literal loopback
HTTP(S) address, and the runner never starts or closes the browser in CDP mode. `--profile-dir` launches the fixed
`/usr/bin/google-chrome` executable; use CDP mode for Chromium or another
Chrome installation.

CDP mode is limited to B12 and refuses to run unless exactly one `--site-name`
and exact target id are given; it does not open, close, or mutate another tab.
It examines only page-target metadata to identify the human-authorized provider
tab, binds that target id to its exact provider URL, and validates the current
URL before every navigation or DOM action. Listing output exposes only the
provider, opaque target id, path class, eligibility, and query/fragment flags;
it never prints an URL or page content. The site remains in draft form unless
`--publish` is explicitly supplied.

When no exact authorized tab handoff has been recorded, list eligible provider
tabs without changing them, then obtain the human-approved eligible target id
before starting generation. It does not inspect tab content or create, close,
or navigate a tab.

```sh
uv run python -m degentweb.agent.persistent_browser_tabs b12 \
  --cdp-endpoint http://127.0.0.1:9279
```

```sh
uv run python -m degentweb.agent.gen_b12 \
  --cdp-endpoint http://127.0.0.1:9222 \
  --tab-target-id exact-target-id-from-listing \
  --manifest data/reviewed-one-site-manifest.jsonl \
  --site-name 'exact reviewed manifest name' \
  --output-dir data/generation-checkpoints
```

The runner persists a JSON checkpoint after creation of the site and every
post. It waits after actions and requires each expected visible UI label. It
raises a `needs_intervention` checkpoint for login, CAPTCHA, or an unmatched
provider state. A walkthrough can refine the label selectors, but never turns
the production path back into agent-directed browsing.

With `--publish`, Wix first creates all required blog posts as drafts, then
publishes each checkpointed post, then publishes the site. It refuses duplicate
post titles because the provider editor cannot select those drafts unambiguously.
Both providers must show their provider-specific publication success state before
the checkpoint is marked complete.

After a `needs_intervention` result, inspect the provider tab first. Use
`--retry-needs-intervention` only if the interrupted action did not complete;
the runner records that human confirmation, clears the in-flight marker, and
retries it. If its outcome is uncertain or it completed, leave the checkpoint
unchanged and obtain a new reviewed handoff rather than risking a duplicate.

Each manifest line must contain `site_key`, `category`, `name`, `description`,
and `posts`; every post has `title` and `description`. The same frozen manifest
supplies both the split and audit site list. Audit input must have unique page
identities and only manifest site keys.

The pre-runner reviewed JSON-array manifest is also accepted. Give its matching
schema-v1 state file through `--legacy-state`; the runner accepts only a pending
job with zero attempts, carries its source-site and digest into the new
checkpoint, and never edits the old shared state file. For the reviewed B12
pilot, select only `Circuit & Culture`, keep publication disabled, and use its
three reviewed posts; that is a smoke pilot, not a 15-page eligible site.

```sh
uv run python -m degentweb.agent.gen_b12 \
  --cdp-endpoint http://127.0.0.1:9279 \
  --tab-target-id exact-target-id-from-listing \
  --manifest data/site_creation/manifests/unmatched_candidates_20260816.json \
  --legacy-state data/site_creation/states/b12_unmatched_20260816.json \
  --site-name 'Circuit & Culture' --minimum-pages 3 \
  --output-dir data/generation-checkpoints
```

The page loop stops only after 15 candidate pages. If the input runs out of
posts, or the provider cannot complete the path, the checkpoint is
`unclassifiable` or `needs_intervention` respectively. Crawl and extract main
text before calling `audit_extracted_page`; the audit only rejects pages with
fewer than 50 words or obvious prompt/AI meta-text. A site with fewer than 15
remaining pages is unclassifiable.

Use `split_by_category` to freeze the conventional random train/test split
within every category. It rejects duplicate site keys to prevent train/test
leakage and categories with fewer than two sites. Store that output with the
extraction/audit artifacts.

```sh
uv run python -m degentweb.agent.generation_dataset split \
  --input data/site-manifest.jsonl --output data/site-split.jsonl --seed 20260817
uv run python -m degentweb.agent.generation_dataset audit \
  --input data/extracted-pages.jsonl --page-output data/page-audits.jsonl \
  --site-output data/site-audits.jsonl --sites-input data/site-manifest.jsonl
```

## HTML and historic-model choice

Keep the existing fixed HTML shell wherever possible: it is deterministic and
does not require a text model. This implementation does not make Bedrock
generation requests. If that separate future arm is approved, the live `aws
bedrock list-foundation-models --region us-east-1` probe on 2026-08-17 found
`mistral.mixtral-8x7b-instruct-v0:1` `ACTIVE`; it is the practical
period-appropriate templating fallback with frozen request settings.

The same live probe found no GPT-4, Claude 2.x, Claude 3 Sonnet, Claude 3.5
Sonnet, or Claude 3.7 Sonnet IDs. It did find legacy Claude 3 Haiku and active
Mixtral. Anthropic's own API documentation says Claude Sonnet 3.5 was retired
on 2026-01-05 and Claude 2/2.1 plus Claude Sonnet 3 were retired on 2024-11-06,
so changing providers does not restore those exact Claude models. For a
non-Bedrock paid comparison, OpenAI currently documents the frozen
`gpt-4.1-2025-04-14` snapshot; this is a practical GPT-family substitute but
not historical GPT-4 and must be funded outside Bedrock.

Sources: [AWS Bedrock model lifecycle](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html), [Anthropic model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations), [OpenAI GPT-4.1 model documentation](https://developers.openai.com/api/docs/models/gpt-4.1).
