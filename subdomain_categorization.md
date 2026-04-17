# Subdomain categorization

(generated following discussion)

## Current decisions

- Keep one primary category plus optional tags.
- Do not use a separate unclear category; use workflow states such as
    `needs_more_evidence` and `needs_human_review`.
- Start from approved categories only; show only approved categories to the
    model, and save new category proposals for human approval before reuse.
- Approved taxonomy can be refined by introducing a new canonical category and
    marking narrower overlapping labels as `superseded`; superseded labels stay
    in history but disappear from future prompts because prompts read only
    approved categories.
- Current canonical merge plan:
  - `software_repository` is the superset replacement for
    `android_app_repository`, `ios_app_repository`,
    `open_source_software_repository`, and
    `software_download_repository`.
  - `asset_boilerplate_resources` is the superset replacement for
    `form_repository`, `free_template_repository`,
    `product_manual_repository`, `free_design_asset_repository`,
    `free_map_repository`, and `genealogy_repository`.
  - `personal` is the superset replacement for
    `personal_knowledge_base`.
- Keep the current category set for now and adjust it as we learn; likely
    future pressure point is splitting `malicious_deceptive`, possibly making
    `phishing` its own category.
- Current MVP uses stored extracted pages from site-analysis snapshots only.
- Candidate subdomains come from `site_analysis_subdomains.selected_for_deep`,
    not raw `subdomains`, because LLM site categorization only makes sense once
    the site-analysis pipeline has already established there are enough usable
    pages to judge the site as a whole.
- By default, categorization uses the latest site-analysis run for each crawl
    source automatically, and prompt pages come from the corresponding latest
    `site_analysis_sampled_pages` snapshot so the evidence matches the same
    site-analysis selection pass.
- When a categorization run starts, the chosen `analysis_run_id` is pinned into
    `run_notes`, so resume stays on the same site-analysis snapshot without
    needing a separate schema column.
- Current categorization loop prompt version is `2`.
- Prompt version `1` is preserved for replay/backward compatibility.
- Current prompt uses XML samples first, includes existing site tags and
    selected per-page features, warns about extraction artifacts, and requires
    evidence to cite URLs.
- Store exact prompt text plus structured prompt inputs so each categorization
    can be replayed exactly.
- Current schema changes are in `src/degentweb/sql/migrations/v11.sql`.

## Goal

- Assign each subdomain one coarse category that is easy to analyze.
- Keep extra detail in separate tags instead of
    putting everything into the main category.
- Use LLM output to speed up categorization, then measure quality with
    blinded human review.
- Reuse existing crawl, extraction, and review data as much as possible.

## Main idea

- Give each subdomain exactly one primary category.
- Give each subdomain zero or more tags.
- Treat category as the main answer to "what kind of site is this mostly?"
- Treat tags as extra facts such as "has blog", "ad heavy", "affiliate",
    "ugc", or "docs".
- Keep page-level authorship judgement separate from
    site-level category because they answer different questions.

## Why use one category plus tags

- One category per subdomain makes counting, grouping, error analysis, and
    trend analysis simple.
- Multiple category tags per subdomain would make basic analysis ambiguous
    and messy.
- Separate tags keep nuance without breaking mutual exclusivity.
- This lets us say a site is `business_using_blog_for_seo` and then
    add tags like `healthcare`, `local_service`, or `affiliate`.
- This keeps the category list short enough that humans and
    LLMs can apply it consistently.

## Category design

- Use a coarse category list based on recurring patterns already seen in
    `docs/bimodal.md`.
- Pick one category even if the site has multiple parts, based on
    what the site is mainly for.
- Keep a catch-all category for real sites that
    do not match the main repeated patterns.
- Keep an insufficient-evidence category for cases where
    the available pages do not support a reliable decision.

## Suggested categories

- business_using_blog_for_seo
- ecommerce_and_directories
- seo_and_affiliate_blogs
- free_online_tools
- spam_content_farms_and_scam_sites
- other_legit_sites
- insufficient_evidence

## New categories

- The model may emit a category name that is not yet in the current list if
    the current list is clearly not a good fit.
- There is no need for a separate special workflow for this.
- We will review such cases manually anyway.
- New category names can be saved as proposals in the database and then
    reviewed by a human in the normal review flow.

## Why these categories are coarse

- They describe the site's main job rather than its topic.
- They are broad enough that one subdomain usually has one dominant answer.
- They leave room for tags to capture the details that matter later.
- They are easier to compare across datasets than narrow content labels.
- Broader taxonomy labels such as institutional, product company, publisher,
    or community are often more useful here as tags or loose mappings than as
    the main project category.
- If too many sites end up in `other_legit_sites` or `insufficient_evidence`,
    the rubric is too vague or the list is still too fine-grained.

## Tags

- Tags are optional and many-to-many.
- Tags should capture extra structure that is useful but not suitable as
    the main category.
- Good tag examples are local_service, healthcare, B2B, education, directory,
    affiliate, casino, crack_software, generated_seo, health_wellness,
    ecommerce, catalog, multilingual, parked_repurposed, dating_spam,
    celebrity_spam, and scam_site.
- Useful broader-archetype tags are institutional, product_saas,
    community_ugc, retail_ecommerce, marketplace, listings, and
    publisher_editorial.
- Useful monetization and risk tags are lead_gen, display_ads, subscription,
    thin_content, parked_domain, malicious_deceptive, phishing, malware, adult,
    gambling, and warez.
- Tags can support graph-like analysis later through relational tables and
    SQL views.
- Tags should not be used as the main site type label.

## Assignment rule

- Ask: what is the dominant purpose of this subdomain?
- A good tie-breaker is: what is the operator trying to get the user to do if
    supporting pages are ignored?
- Choose the one category that best answers that question.
- Use tags for the important secondary traits.
- If a site is a real business with SEO blog content, keep it in
    `business_using_blog_for_seo` rather than `seo_and_affiliate_blogs`.
- Clear business identity signals such as company branding, service pages,
    address, phone number, contact forms, or
    service-area language are strong evidence for
    `business_using_blog_for_seo`.
- If the economic engine is traffic monetization through affiliate links,
    search capture, or template-like informational pages,
    prefer `seo_and_affiliate_blogs`.
- If the economic engine is an interactive function such as a converter,
    checker, generator, or calculator, prefer `free_online_tools`.
- If the main pattern is e-commerce, catalog, marketplace, or discovery,
    prefer `ecommerce_and_directories` and use tags like `retail_ecommerce`,
    `marketplace`, `directory`, or `listings` for the subtype.
- If fraud, abuse, or spam is the core purpose, keep the site in
    `spam_content_farms_and_scam_sites` and use tags such as
    `malicious_deceptive`, `phishing`, `malware`, `parked_domain`, `gambling`,
    or `warez` for the subtype.
- If the evidence is conflicting and no dominant purpose is clear,
    use `other_legit_sites` only for clearly real sites and
    `insufficient_evidence` for weak or missing evidence.

## Inputs to the LLM

- Use up to 5 pages per subdomain from the database.
- Include extracted main text and lightweight metadata for each page.
- Metadata can include page URL, crawl source, bytes, chars, ad counts,
    dates, and filter flags.
- Use metadata as supporting context, not as the main evidence.
- The main evidence should still be quoted text from the page extractions.

## Why only a few pages

- A small fixed number keeps cost and latency predictable.
- A few diverse pages are usually enough for a coarse site-level category.
- Too many pages increase prompt size and noise.
- The goal is not to summarize the whole site perfectly, but to
    identify its dominant pattern reliably.

## Page selection

- Prefer pages with usable extracted text.
- Prefer diversity across URLs rather than 5 near-duplicate pages.
- Avoid over-weighting boilerplate, login pages, tag pages, and empty pages.
- If a subdomain has fewer than enough usable pages, keep going with
    what is available and allow insufficient_evidence.
- Record which pages were shown to the model so results are auditable.

## Homepage fetch

- First use stored pages from the database.
- If the stored evidence is weak or sparse, try fetching the homepage live.
- Use the live homepage as extra evidence, not as a silent replacement for
    the stored sample.
- Record whether live fetch was used.

## Why homepage fetch is only a fallback

- Stored pages are cheaper and faster because they already exist in
    the database.
- Stored pages are also closer to the rest of the pipeline and easier to
    reproduce.
- Live fetch can fail, change over time, or disagree with
    stored crawl snapshots.
- Using it only when
    needed gives more coverage without making every categorization slow and
    fragile.

## Common Crawl pages missing HTML

- If a Common Crawl page is selected but its HTML is not yet stored,
    fetch it on the fly.
- Reuse the existing Common Crawl path.
- If extracted text already exists, use it and only fetch HTML for review or
    debugging.
- If extracted text does not exist, fetch HTML, run extraction, and
    save both.

## LLM task

- Build the prompt in a script instead of writing it ad hoc.
- Show the sampled pages and metadata.
- Ask the model to decide the single best category.
- Ask the model to add optional tags.
- Ask the model to quote exact evidence from the provided pages.
- Ask the model to explain uncertainty when
    the category is `insufficient_evidence`.
- Ask the model to return JSON only.

## LLM output

- category
- tags
- confidence
- used_live_fetch
- uncertainty_reason
- evidence items with page reference and exact quote

## Why require quotes

- Quotes make the output auditable.
- Quotes let us detect hallucinated evidence.
- Quotes help humans review disagreements quickly.
- Quotes make it easier to debug the taxonomy and prompt.

## Script and parsing

- Put prompt construction and API calls in a script such as
    `scripts/subdomain_categorize.py`.
- Keep the prompt versioned in code so reruns are reproducible.
- Parse the JSON response with Pydantic.
- Fail if the JSON does not match the expected schema.
- Keep the existing category list in code, but
    allow category strings outside the current list because
    humans will review them manually.
- Store the raw API response as well as the parsed result for debugging.

## Storage shape

- Store one explicit site-level category per subdomain as
    a first-class field or table, not inside free-form tags.
- Store tags separately in a many-to-many table.
- Store evidence and model metadata separately if needed.
- Keep page-level review judgement separate from site-level category.
- Keep history if useful, but the latest category should be easy to
    query directly.

## Store categorizations by author

- Store LLM output and human review in the same schema.
- Give each categorization an author.
- For model output, set author to the model name, such as `gpt-oss-120b`.
- For human review later, set author to the person name, such as `steven`.
- This makes model-human comparison easy because both live in the same shape.

## Why not use only the current site_tags table

- The current many-to-many tag shape is good for optional attributes.
- It is not good for one mutually exclusive analytic label.
- A first-class category field avoids duplicate meanings, spelling drift, and
    awkward SQL.
- This makes dashboards, confusion matrices, and
    prevalence estimates much easier.

## Cost formula

- Input cost is input_tokens / 1,000,000 × $0.15.
- Output cost is output_tokens / 1,000,000 × $0.60.
- Total cost per API call is input cost plus output cost.

## Cost estimate example

- If the prompt uses about 8,000 input tokens and about 600 output tokens,
    cost is 8,000 / 1,000,000 × $0.15 plus 600 / 1,000,000 × $0.60.
- That is about $0.00156 per subdomain.
- If 100,000 subdomains are categorized at that rate,
    the API cost is about $156 before extra homepage-fetch cases.
- Cost scales almost linearly with the text cap and output length, which
    is why prompt caps matter.

## Human review

- Sample both predicted LLM-heavy and predicted human-heavy parts of
    the population.
- Because human-heavy sites are much more common, it is fine to
    review only a sample of them.
- Use stratified sampling rather than convenience sampling.
- Include model confidence and whether live fetch was used in
    the sampling strata.
- Keep human reviewers blinded to model output.

## Why stratified sampling matters

- It keeps the evaluation set informative even when
    the real population is imbalanced.
- It gives enough positive and negative cases for error analysis.
- It avoids wasting most of the review budget on the most common easy cases.
- If we want population-level estimates later, we can weight results back by
    sampling probability.

## What success looks like

- Most subdomains receive one clear category without human intervention.
- Tags add useful nuance without replacing the main category.
- Human reviewers can understand and correct model outputs quickly.
- Agreement is high on the coarse category list.
- SQL analysis of category counts, error rates, and
    trends is straightforward.

## Failure signs

- Reviewers often disagree because two categories both seem equally right.
- Too many sites fall into `other_legit_sites` or `insufficient_evidence`.
- Tags start carrying the real meaning while categories become shallow.
- The model cites evidence that is not present in the supplied pages.
- The pipeline repeatedly refetches the same missing Common Crawl pages.

## Practical first version

- Start with the category list above.
- Use stored pages first and homepage fetch only as fallback.
- Keep one primary category and separate tags.
- Save exact evidence quotes.
- Parse model JSON with Pydantic.
- Store each result with an author such as `gpt-oss-120b` or `steven`.
- Run blinded stratified human review on a sample.

## Operator flow

- Run `src/degentweb/classifying/subdomain_categorization_data_analysis.py` in
    IPython.
- The loop resumes the latest matching active run for each crawl source, or
    starts a new one if none exists.
- The loop stops when the current run creates proposed categories.
- It emails the pending-review summary and prints it locally.
- Approve or reject proposals with the helper functions in the script, then run
    the loop again.

## Environment

- Do not edit the committed `.env` in the repo.
- Set real SMTP credentials in your local `.env` for:
    - `EMAIL_ME_GMAIL_ADDRESS`
    - `EMAIL_ME_GMAIL_APP_PASSWORD`
