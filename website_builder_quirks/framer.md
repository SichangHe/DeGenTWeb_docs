# Framer restrictions and quirks

(authored by agents unless marked 🧑)

## Pricing, account, and payment restrictions

- **restriction:** [pricing](https://www.framer.com/pricing/) lists Free at `$0`.
  Basic is `$10/month` on yearly billing, so the minimum year costs `$120`.
  Tax may be added at checkout.
- **restriction:** the [pricing FAQ](https://www.framer.com/pricing/#faq-payment-methods)
  says paid plans accept card and, in some regions, PayPal.
- **restriction:** the [pricing FAQ](https://www.framer.com/pricing/#faq-refunds)
  says EU or Turkish buyers are legally eligible for a refund within 14 days.

## Free tier, sites, pages, and publishing restrictions

- **restriction:** [pricing](https://www.framer.com/pricing/) says Free includes
  1 GB bandwidth, 10 CMS collections, 1,000
  pages, 5 MB uploads, one locale, and up to three editors. A custom domain
  requires a paid site plan.
- **restriction:** publishing assigns a `framer.app` domain. Staging is Pro or
  higher, per the [publishing guide](https://www.framer.com/help/articles/publishing-your-framer-website/).

## Content-generation restrictions

- **restriction:** a Free workspace with no active subscriptions receives a
  one-time 500-credit allowance. Prompt cost varies with complexity and
  credit-using features stop at zero, according to the [credit guide](https://www.framer.com/help/articles/how-ai-credits-and-agents-pricing-work/).

## Branding, domain, and persistence restrictions

- **restriction:** Free sites use a Framer subdomain and show “Made in Framer.”
  The [badge guide](https://www.framer.com/help/articles/how-do-i-remove-the-made-in-framer-badge-from-my-website/)
  requires a paid plan or connected custom domain, followed by republishing.
- **restriction:** each paid site plan applies to a project; [pricing](https://www.framer.com/pricing/)
  presents Basic as a per-project site plan.
- **restriction:** permanent project deletion immediately unpublishes the site,
  cannot be undone, and does not automatically detach a custom domain, per the
  [deletion guide](https://www.framer.com/help/articles/deleting-a-project-in-framer/).

## Export, crawl, robots, and login restrictions

- **restriction—provider conflict:** Framer's [HTML export article](https://www.framer.com/help/articles/can-i-export-my-website-to-html-and-self-host-it/)
  says HTML export is unavailable, while its [data-portability article](https://www.framer.com/help/articles/porting-your-data-from-framer/)
  says a full site can be downloaded and hosted elsewhere. Both were updated
  August 7, 2026. Whole-site export is therefore unresolved. CMS data can be
  exported through plugins as CSV or JSON.
- **crawl fact:** Framer pre-renders published pages, generates `robots.txt` and
  `sitemap.xml`, and allows major search and AI crawlers by default. Optimized
  pages also support Markdown content negotiation, per its [crawler guide](https://www.framer.com/help/articles/make-site-readable-by-ai-agents/).
- **restriction:** Markdown may be absent for unoptimized or rate-limited pages.
  A custom robots file requires Pro or Enterprise, according to the
  [robots guide](https://www.framer.com/help/articles/how-can-i-access-the-robots-txt-file/).

## Automation and bulk restrictions

- **restriction:** Framer's [acceptable-use policy](https://www.framer.com/legal/acceptable-use-policy)
  prohibits robots, page scraping, and manual processes that acquire or monitor
  platform or hosted content by means Framer did not purposely provide.
- **restriction:** external Agents are a product feature, but the one-time 500
  variable-cost Free credits bound Framer AI features that consume credits in
  an eligible Free workspace; editor helpers continue at zero credits.

## Verified unknowns

- **verified unknown:** no cited provider source states how many separate Free
  projects may be published concurrently, how deletion affects that allowance,
  or how long an inactive Free project or URL persists.
- **verified unknown:** the cited provider material does not state whether Free
  requires billing details.
- **verified unknown:** Framer promises no number of finished sites or pages
  from the 500-credit allowance.
- **verified unknown:** the cited provider material does not establish a new
  Free site's signed-out response or persistence.
- **verified unknown:** no cited provider source permits a research workflow
  that automatically generates and publishes many Free sites. Obtain written
  permission before bulk use.
- **verified unknown:** the pricing FAQ does not state whether buyers outside the
  EU and Turkey have a general refund option.
- **verified unknown:** whole-site export remains unresolved because the two
  current provider articles conflict, as documented above.
