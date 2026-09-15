# Hostinger restrictions and quirks

(authored by agents unless marked 🧑)

## Pricing, account, and payment restrictions

- **restriction:** the [AI Builder page](https://www.hostinger.com/ai-website-builder)
  advertises Premium at `$2.99/month`, but requires `$143.52` prepaid for 48
  months and renews at `$10.99/month`. All plans are paid upfront; tax can vary.
  The advertised deal exceeds a `$12` total budget.
- **restriction:** refunds immediately terminate the service and erase its data.
  Disabling renewal keeps service only to expiry, according to
  the [cancellation guide](https://www.hostinger.com/support/1583775-how-to-cancel-a-hosting-plan-at-hostinger/).

## Trial, sites, pages, and publishing restrictions

- **restriction:** the [trial guide](https://www.hostinger.com/support/11131062-hostinger-ai-builder-how-to-try-it-for-free/)
  provides a seven-day draft. Trial sites cannot publish, stores cannot
  connect payment methods, Agentic mode gets five credits, and publishing,
  exporting, more credits, or more sites requires payment.
- **restriction:** Premium allows three sites. The higher Unlimited and Cloud
  plans advertise unlimited sites on the [AI Builder page](https://www.hostinger.com/ai-website-builder),
  subject to its linked [Fair Usage Policy](https://www.hostinger.com/legal/hosting-agreement).
- **restriction:** Manual mode has no numerical limit on pages, sections, or
  elements, according to the [page guide](https://www.hostinger.com/support/6456705-hostinger-ai-builder-manual-mode-how-to-add-more-pages/).

## Content-generation restrictions

- **restriction:** paid Premium includes five creation credits. Agentic requests
  consume variable credits based on compute, including questions and manual
  edits; top-ups expire after three months, per the [credit guide](https://www.hostinger.com/support/11136677-hostinger-ai-builder-agentic-mode-ai-credits/).
- **restriction:** outside the trial, the [Agentic creation guide](https://www.hostinger.com/support/how-to-create-a-web-app-using-hostinger-ai-builder-agentic-mode/)
  directs users to buy a plan before creating and publishing a project; AI
  creation and follow-up prompts consume the plan's credits.

## Branding, domain, and persistence restrictions

- **restriction:** Manual mode's [publishing guide](https://www.hostinger.com/support/6475340-hostinger-ai-builder-manual-mode-how-to-publish-a-website/)
  says an auto-generated preview domain remains usable while a connected custom
  domain propagates. The [AI Builder page](https://www.hostinger.com/ai-website-builder)
  advertises a custom domain free only for the first year. Hostinger does not
  promise that either URL persists after hosting expires.
- **restriction:** expired sites stop working. A plan canceled for non-payment
  may be restorable for less than 30 days; after 30 days it is permanently
  deleted, according to the [inactive-plan guide](https://www.hostinger.com/support/4146981-what-to-do-if-your-hosting-plan-becomes-inactive-at-hostinger/).
- **restriction:** duplicating Manual sites does not copy the store, products,
  or store settings. Moving a duplicate between shared plans costs a fee; Cloud
  plans are exempt, per the [duplicate guide](https://www.hostinger.com/support/8439478-hostinger-ai-builder-how-to-duplicate-a-website/).

## Export, crawl, robots, and login restrictions

- **restriction:** Agentic export is a React/Vite Node.js zip containing
  frontend and logic files, not integrated-backend data. Edited exports cannot
  be imported back for prompting, per the [code-export guide](https://www.hostinger.com/support/10771345-hostinger-ai-builder-agentic-mode-how-to-export-code/).
- **restriction:** Manual mode cannot download a whole-site backup, according to
  the [cancellation guide](https://www.hostinger.com/support/1583775-how-to-cancel-a-hosting-plan-at-hostinger/).
  Its WordPress export omits styles, layout, store, integrations, forms,
  submissions, and SEO settings, per the [content-export guide](https://www.hostinger.com/support/6572573-hostinger-ai-builder-manual-mode-how-to-export-content-to-wordpress/).
- **crawl fact:** published Manual sites automatically expose and update
  `/sitemap.xml`, per the [sitemap guide](https://www.hostinger.com/support/6491673-hostinger-ai-builder-website-s-sitemap/).
- **restriction:** Hostinger applies non-disableable server-level rate limits to
  automated traffic from network ranges including AWS and Microsoft. Affected
  clients may receive HTTP 429 for hours, per the [rate-limit guide](https://www.hostinger.com/support/429-errors-on-automated-integrations-and-link-previews/).

## Automation and bulk restrictions

- **restriction:** the seven-day trial cannot publish or create more sites, and
  the paid Premium site cap is three.
- **restriction:** AWS-origin automation may be rate-limited as described above.
  Hostinger recommends exponential backoff where supported and does not allow
  this server-level limit to be disabled per site.

## Verified unknowns

- **verified unknown:** Hostinger promises no number of complete sites or pages
  from five credits and gives no replacement-generation count.
- **verified unknown:** the cited provider pages do not establish a required
  visible Hostinger badge on published customer sites.
- **verified unknown:** the cited provider material does not establish
  customer-site robots, signed-out crawl results, or preview-domain lifetime.
- **verified unknown:** the cited provider material does not promise that a
  custom or preview URL persists after hosting expires.
- **verified unknown:** no cited public bulk-generation API or express browser-
  automation permission exists for this consumer builder. Do not infer bulk
  permission from the advertised “Unlimited” hosting plan.
