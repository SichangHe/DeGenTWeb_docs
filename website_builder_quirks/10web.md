# 10Web restrictions and quirks

(authored by agents unless marked 🧑)

## Pricing, account, and payment restrictions

- **restriction:** the live [pricing page](https://10web.io/pricing-platform/)
  embeds AI Starter at `$20` for one monthly site. Its displayed `$10/month`
  rate requires `$120` prepaid for 12 months. Both exceed a `$12` total budget
  once the billing period is applied.
- **restriction:** Free generation requires an account. Full editing requires a
  seven-day Pro trial and card, according to [Get Started for Free](https://help.10web.io/hc/en-us/articles/360021420139-Get-Started-for-Free-on-10Web).
  Restricted actions, including disabling Site Lock, may trigger a charge.
- **restriction—provider conflict:** the [cancellation guide](https://help.10web.io/hc/en-us/articles/5315648905234-Canceling-Downgrading-or-Changing-10Web-Subscriptions)
  says paid access lasts through the billing period and then sites and data are
  permanently deleted unless backed up. The [recovery policy](https://help.10web.io/hc/en-us/articles/360030873572-How-to-Recover-10Web-Hosted-Websites-That-Were-Deleted-on-Plan-Expiration)
  instead says paid sites are deleted one month after expiration and their
  backups retained six more months. Post-cancellation deletion timing is
  therefore unresolved.

## Free tier, sites, pages, and publishing restrictions

- **restriction:** Free permits one generated website. Full editing is unavailable
  without the card-backed trial.
- **restriction:** the seven-day trial site has Site Lock, which shows visitors
  a username/password prompt. Pointing a custom domain or purchasing a plan
  removes it, according to the [Site Lock guide](https://help.10web.io/hc/en-us/articles/12191661456786-What-is-Site-Lock).
- **restriction:** a non-upgraded trial website is deleted after expiry. 10Web
  says trial sites are deleted one month after expiry and their backups retained
  three more months for support-assisted restoration in its
  [recovery policy](https://help.10web.io/hc/en-us/articles/360030873572-How-to-Recover-10Web-Hosted-Websites-That-Were-Deleted-on-Plan-Expiration).

## Content-generation restrictions

- **restriction:** AI Starter includes 100 credits/month, but the provider does
  not convert credits into a fixed site allowance. Website-generation prompts
  must contain 20–2,000 characters under the
  [prompt guide](https://help.10web.io/hc/en-us/articles/27778193894034-Prompt-and-Character-Limit-Guidelines-for-AI-Website-Generation-at-10Web).

## Branding, domain, and persistence restrictions

- **restriction:** every new site initially uses a 10Web subdomain. Changing it
  requires cloning and temporarily consumes another hosting slot, according to
  the [subdomain guide](https://help.10web.io/hc/en-us/articles/12191379602962-Can-I-Change-the-Temporary-Subdomain).

## Export, crawl, robots, and login restrictions

- **restriction:** 10Web does not provide a static HTML/CSS download. Paid users
  can download the WordPress backup or use SSH/SFTP, but those credentials are
  unavailable on Free, per [code access](https://help.10web.io/hc/en-us/articles/25664682627474-Can-I-Have-HTML-And-CSS-Code-Of-My-Website)
  and [Free access](https://help.10web.io/hc/en-us/articles/360021420139-Get-Started-for-Free-on-10Web).
- **restriction:** 10Web says AI-generated sites may not work correctly outside
  its hosting ecosystem in its [hosting article](https://help.10web.io/hc/en-us/articles/11594324041106-Can-I-Use-an-AI-Builder-Generated-Website-on-Other-Hostings).
- **restriction:** Site Lock is a login barrier, so a default trial result is not
  anonymously crawlable.

## Automation and bulk restrictions

- **restriction:** the consumer workflow has authentication, a one-site Free
  cap, per-plan hosting slots, and Site Lock.
- **restriction:** the official [Website Builder API](https://10web.io/website-builder-api/)
  is a separate volume product with custom pricing, not an included consumer
  bulk interface.

## Verified unknowns

- **verified unknown:** Free-generation lifetime, replacement-generation count,
  initial whole-site credit cost, finished-site yield from 100 monthly credits,
  and whether deletion restores the one-site allowance are not stated.
- **verified unknown:** an [older AI Builder guide](https://help.10web.io/hc/en-us/articles/7952757255186-AI-Website-Builder-Fully-Automated-WordPress-Website-Creation-in-a-Few-Minutes)
  describes recreation one source page at a time, a five-page Free cap, and
  unlimited paid pages; current provider material does not confirm those limits.
- **verified unknown:** a visible provider badge on public consumer-plan pages
  is not established by the cited sources; white labeling is an Agency feature.
- **verified unknown:** the cited provider material does not state the default
  customer-site robots rules, sitemap behavior, or crawlability after Site Lock
  is removed.
- **verified unknown:** the cited provider material does not state whether
  consumer browser automation is permitted or give a consumer bulk-generation
  rate.
- **verified unknown:** post-cancellation site and backup deletion timing remains
  unresolved because the cancellation and recovery articles conflict, as
  documented above.
