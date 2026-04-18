# LLM Site Kinds — Technology and Signal Reference

Short, citable descriptions for every technology/monetization signal the
kinds analysis (`src/degentweb/classifying/llm_site_kinds_analysis.py`)
detects. Use this doc when writing the paper so each technology claim has a
verifiable source. Prefer the vendor's own page as the primary source and
an independent page (Wikipedia, Crunchbase, press coverage) as corroboration.

URLs are canonical vendor or Wikipedia pages as of 2026-04; resolve before
citing in the final paper.

## Ad networks and ad-management platforms

| Detector name | Vendor / product | What it does | Primary URL | Secondary URL |
| --- | --- | --- | --- | --- |
| `ad_google_adsense` | Google AdSense | Self-serve display-ad network operated by Google; the default monetization path for small/independent publishers. | https://adsense.google.com/ | https://en.wikipedia.org/wiki/Google_AdSense |
| `ad_google_doubleclick` | Google Ad Manager (formerly DoubleClick) | Google's publisher-side ad server and Ad Exchange (AdX). Serves and auctions display ads for larger publishers. | https://admanager.google.com/ | https://en.wikipedia.org/wiki/DoubleClick |
| `ad_amazon` | Amazon Advertising / a9 / OpenX | Amazon's publisher-side ad sales and Transparent Ad Marketplace (TAM) header bidding wrapper. | https://advertising.amazon.com/ | https://en.wikipedia.org/wiki/Amazon_Advertising |
| `ad_mediavine` | Mediavine | Full-service ad-management company for lifestyle publishers; requires a minimum traffic threshold for membership. | https://www.mediavine.com/ | https://en.wikipedia.org/wiki/Mediavine |
| `ad_ezoic` | Ezoic | AI-driven ad-management and site-acceleration layer; explicitly markets to small/new publishers (entry-level tier). | https://www.ezoic.com/ | https://en.wikipedia.org/wiki/Ezoic |
| `ad_raptive_adthrive` | Raptive (formerly AdThrive) | Premium full-service ad-management company for established publishers; acquired CafeMedia / AdThrive. | https://raptive.com/ | https://en.wikipedia.org/wiki/Raptive |
| `ad_taboola` | Taboola | Native-advertising / content-recommendation network ("you may also like" widgets). | https://www.taboola.com/ | https://en.wikipedia.org/wiki/Taboola |
| `ad_outbrain` | Outbrain | Native-advertising competitor to Taboola. | https://www.outbrain.com/ | https://en.wikipedia.org/wiki/Outbrain |
| `ad_criteo` | Criteo | Performance advertising / retargeting; publisher-side Commerce Media platform. | https://www.criteo.com/ | https://en.wikipedia.org/wiki/Criteo |
| `ad_sovrn` | Sovrn | Publisher-focused header bidding / ad exchange. Acquired Viglink. | https://www.sovrn.com/ | https://en.wikipedia.org/wiki/Sovrn |
| `ad_index_exchange` | Index Exchange | Independent ad exchange widely used in header bidding. | https://www.indexexchange.com/ | https://en.wikipedia.org/wiki/Index_Exchange |
| `ad_pubmatic` | PubMatic | Supply-side platform (SSP) used in header bidding. | https://pubmatic.com/ | https://en.wikipedia.org/wiki/PubMatic |
| `ad_yandex` | Yandex Advertising Network / Metrika | Russian search engine's ad network + analytics pixel. | https://yandex.com/adv/ | https://en.wikipedia.org/wiki/Yandex |
| `ad_microsoft` | Microsoft Advertising (formerly Bing Ads) | Microsoft's search-and-display ad network; UET pixel on publisher pages. | https://about.ads.microsoft.com/ | https://en.wikipedia.org/wiki/Microsoft_Advertising |
| `ad_facebook` | Meta Pixel | Facebook/Meta's conversion-tracking pixel used by advertisers, not an ad network per se but a near-universal marker of ads/retargeting. | https://www.facebook.com/business/tools/meta-pixel | https://en.wikipedia.org/wiki/Facebook_Pixel |
| `ad_propellerads` | PropellerAds | Performance/pop/push ad network known for lower-tier inventory. | https://propellerads.com/ | (no widely-cited Wikipedia page) |
| `ad_revcontent` | RevContent | Native-ads competitor to Taboola/Outbrain. | https://www.revcontent.com/ | (no widely-cited Wikipedia page) |
| `ad_monumetric` | Monumetric | Managed ad tier just above Ezoic, below Mediavine. | https://www.monumetric.com/ | (no widely-cited Wikipedia page) |
| `ad_shareathrough` | Sharethrough | Ad exchange focused on native/omnichannel supply. | https://www.sharethrough.com/ | https://en.wikipedia.org/wiki/Sharethrough |

## Affiliate networks

| Detector name | Vendor / product | What it does | Primary URL | Secondary URL |
| --- | --- | --- | --- | --- |
| `aff_amazon` | Amazon Associates | Amazon's affiliate program; `amzn.to/` and `amazon.com/dp/...` tagged URLs. | https://affiliate-program.amazon.com/ | https://en.wikipedia.org/wiki/Amazon_Associates |
| `aff_skimlinks` | Skimlinks (Connexity) | Content-to-commerce affiliate platform that rewrites outbound links to earn commission on purchases. | https://www.skimlinks.com/ | https://en.wikipedia.org/wiki/Skimlinks |
| `aff_viglink` | VigLink (legacy) | Predecessor to Sovrn //Commerce. Still detectable on older sites. | (redirected) | https://en.wikipedia.org/wiki/VigLink |
| `aff_sovrn_commerce` | Sovrn //Commerce | Sovrn's replacement for VigLink. Same "auto-affiliate" pattern. | https://www.sovrn.com/affiliate/ | https://en.wikipedia.org/wiki/Sovrn |
| `aff_impact` | Impact (formerly Impact Radius) | Affiliate management SaaS for brands. | https://impact.com/ | (no widely-cited Wikipedia page) |
| `aff_cj` | Commission Junction (CJ Affiliate) | One of the longest-running affiliate networks; detection uses its legacy tracking hostnames (qksrv.net, dpbolvw.net, etc.). | https://www.cj.com/ | https://en.wikipedia.org/wiki/CJ_Affiliate |
| `aff_shareasale` | ShareASale | Mid-tier affiliate network, owned by Awin. | https://www.shareasale.com/ | https://en.wikipedia.org/wiki/ShareASale |
| `aff_awin` | Awin (Affiliate Window) | Large international affiliate network. | https://www.awin.com/ | https://en.wikipedia.org/wiki/Awin |
| `aff_rakuten` | Rakuten Advertising / LinkSynergy | Rakuten's affiliate platform. | https://rakutenadvertising.com/ | https://en.wikipedia.org/wiki/Rakuten_Marketing |
| `aff_clickbank` | ClickBank | Digital-product affiliate marketplace (info-products, courses, health supplements). | https://www.clickbank.com/ | https://en.wikipedia.org/wiki/ClickBank |
| `aff_ltk` | LTK / liketoknow.it / rstyle.me | Creator-focused affiliate platform, predominantly fashion/lifestyle. | https://company.shopltk.com/ | https://en.wikipedia.org/wiki/LTK_(company) |
| `aff_partnerstack` | PartnerStack | B2B/SaaS affiliate management. | https://partnerstack.com/ | (no widely-cited Wikipedia page) |
| `aff_avantlink` | AvantLink | Mid-tier affiliate network; outdoor/technical niches. | https://www.avantlink.com/ | (no widely-cited Wikipedia page) |
| `aff_shopstyle` | ShopStyle / RewardStyle | Fashion-affiliate marketplace. | https://www.shopstyle.com/ | https://en.wikipedia.org/wiki/ShopStyle |
| `aff_rel_sponsored` | `rel="sponsored"` link attribute | Google-recommended HTML attribute for paid / sponsored outbound links. Not a vendor; a signal of declared paid links. | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | https://en.wikipedia.org/wiki/Nofollow |

## Audience cultivation (newsletter / membership / donation)

| Detector name | Vendor / product | What it does | Primary URL | Secondary URL |
| --- | --- | --- | --- | --- |
| `subscribe_substack` | Substack | Email-newsletter platform with built-in paywall/subscription. | https://substack.com/ | https://en.wikipedia.org/wiki/Substack |
| `subscribe_convertkit` | Kit (formerly ConvertKit) | Creator-focused email-marketing platform. Strongly associated with professional blogger/creator workflows. | https://kit.com/ | https://en.wikipedia.org/wiki/ConvertKit |
| `subscribe_mailchimp` | Mailchimp | Email-marketing/automation platform; `list-manage.com` signup-form domain. | https://mailchimp.com/ | https://en.wikipedia.org/wiki/Mailchimp |
| `subscribe_beehiiv` | beehiiv | Newsletter platform (Substack alternative founded by ex-Morning Brew). | https://www.beehiiv.com/ | (no widely-cited Wikipedia page) |
| `subscribe_ghost` | Ghost Members | Paid-membership layer on the Ghost CMS. | https://ghost.org/members/ | https://en.wikipedia.org/wiki/Ghost_(blogging_platform) |
| `subscribe_memberful` | Memberful | Paid membership and paywall SaaS; often paired with Ghost/WordPress. | https://memberful.com/ | (no widely-cited Wikipedia page) |
| `subscribe_circle` | Circle | Paid community / cohort platform. | https://circle.so/ | (no widely-cited Wikipedia page) |
| `donate_patreon` | Patreon | Recurring membership/donation platform. | https://www.patreon.com/ | https://en.wikipedia.org/wiki/Patreon |
| `donate_buymeacoffee` | Buy Me a Coffee | One-off and recurring creator tip jar. | https://buymeacoffee.com/ | https://en.wikipedia.org/wiki/Buy_Me_a_Coffee |
| `donate_kofi` | Ko-fi | Creator tip jar with memberships and shops. | https://ko-fi.com/ | https://en.wikipedia.org/wiki/Ko-fi |
| `donate_paypal` | PayPal (donate) | `paypal.me/` and `paypal.com/donate` links. | https://www.paypal.com/ | https://en.wikipedia.org/wiki/PayPal |

## Commerce / digital-product checkout

These cover the monetization gap for SaaS, creator storefronts, and
digital downloads that were not visible through ad-network / affiliate
detection alone.

| Detector name | Vendor / product | What it does | Primary URL | Secondary URL |
| --- | --- | --- | --- | --- |
| `commerce_stripe_checkout` | Stripe Checkout / Elements | Dominant payment-processing API; marks a site that accepts card payments directly. | https://stripe.com/payments/checkout | https://en.wikipedia.org/wiki/Stripe,_Inc. |
| `commerce_paddle` | Paddle | SaaS-focused merchant of record; popular with developer tools. | https://www.paddle.com/ | (no widely-cited Wikipedia page) |
| `commerce_lemonsqueezy` | Lemon Squeezy | Merchant of record for digital products (now part of Stripe). | https://www.lemonsqueezy.com/ | (news coverage exists; limited Wikipedia) |
| `commerce_gumroad` | Gumroad | Creator storefront for digital downloads, courses, memberships. | https://gumroad.com/ | https://en.wikipedia.org/wiki/Gumroad |
| `commerce_podia` | Podia | Creator storefront and course platform. | https://www.podia.com/ | (no widely-cited Wikipedia page) |
| `commerce_sellfy` | Sellfy | Creator storefront for digital products and print-on-demand. | https://sellfy.com/ | (no widely-cited Wikipedia page) |
| `commerce_payhip` | Payhip | UK-based creator-commerce platform. | https://payhip.com/ | (no widely-cited Wikipedia page) |
| `commerce_shopify_buy` | Shopify Buy Button | Shopify's embeddable storefront widget injected into third-party sites. | https://www.shopify.com/buy-button | (Shopify Wikipedia covers the parent) |

## Lead generation / engagement

Lead-generation widgets monetize through sign-ups, not ad views or
checkouts; including them closes part of the "none detected" gap for
SaaS and services sites.

| Detector name | Vendor / product | What it does | Primary URL | Secondary URL |
| --- | --- | --- | --- | --- |
| `lead_hubspot_forms` | HubSpot Forms | HubSpot's embedded form / pop-up script; typical of marketing landing pages. | https://www.hubspot.com/products/marketing/forms | https://en.wikipedia.org/wiki/HubSpot |
| `lead_mktoforms` | Marketo Forms | Adobe-owned B2B marketing-automation platform's forms. | https://nation.marketo.com/ | https://en.wikipedia.org/wiki/Marketo |
| `lead_calendly` | Calendly | Meeting-booking widget; strong signal for B2B sales pipelines. | https://calendly.com/ | https://en.wikipedia.org/wiki/Calendly |
| `lead_typeform` | Typeform | Interactive form / survey widget. | https://www.typeform.com/ | https://en.wikipedia.org/wiki/Typeform |
| `engage_intercom` | Intercom | Business-messenger / live-chat SaaS; signals a sales/support team. | https://www.intercom.com/ | https://en.wikipedia.org/wiki/Intercom_(company) |
| `engage_tawkto` | tawk.to | Free live-chat widget; common on small-business sites. | https://www.tawk.to/ | (no widely-cited Wikipedia page) |

## CMS, site builders, page builders

| Detector name | Vendor / product | What it does | Primary URL | Secondary URL |
| --- | --- | --- | --- | --- |
| `cms_wordpress` | WordPress | Dominant open-source CMS; ~40% of the Web runs on it. | https://wordpress.org/ | https://en.wikipedia.org/wiki/WordPress |
| `cms_shopify` | Shopify | Hosted e-commerce platform. | https://www.shopify.com/ | https://en.wikipedia.org/wiki/Shopify |
| `cms_wix` | Wix | Hosted drag-and-drop site builder. | https://www.wix.com/ | https://en.wikipedia.org/wiki/Wix_(website) |
| `cms_squarespace` | Squarespace | Hosted site-builder aimed at creators and small businesses. | https://www.squarespace.com/ | https://en.wikipedia.org/wiki/Squarespace |
| `cms_webflow` | Webflow | Design-oriented hosted site builder. | https://webflow.com/ | https://en.wikipedia.org/wiki/Webflow |
| `cms_ghost` | Ghost | Open-source blog and newsletter platform. | https://ghost.org/ | https://en.wikipedia.org/wiki/Ghost_(blogging_platform) |
| `cms_drupal` | Drupal | Open-source CMS commonly used by institutional sites. | https://www.drupal.org/ | https://en.wikipedia.org/wiki/Drupal |
| `cms_joomla` | Joomla | Open-source CMS. | https://www.joomla.org/ | https://en.wikipedia.org/wiki/Joomla |
| `ecommerce_woocommerce` | WooCommerce | WordPress plugin turning WordPress into an e-commerce site; owned by Automattic. | https://woocommerce.com/ | https://en.wikipedia.org/wiki/WooCommerce |
| `ecommerce_magento` | Magento (Adobe Commerce) | Enterprise open-source e-commerce. | https://business.adobe.com/products/magento/magento-commerce.html | https://en.wikipedia.org/wiki/Magento |
| `ecommerce_bigcommerce` | BigCommerce | Hosted e-commerce competitor to Shopify. | https://www.bigcommerce.com/ | https://en.wikipedia.org/wiki/BigCommerce |
| `page_builder_elementor` | Elementor | Most-installed WordPress page builder. | https://elementor.com/ | https://en.wikipedia.org/wiki/Elementor |
| `page_builder_divi` | Divi (Elegant Themes) | Popular WordPress page-builder theme. | https://www.elegantthemes.com/gallery/divi/ | (no widely-cited Wikipedia page) |

## Frameworks and static-site generators

| Detector name | Vendor / product | What it does | Primary URL | Secondary URL |
| --- | --- | --- | --- | --- |
| `framework_react` | React | JS UI library maintained by Meta. | https://react.dev/ | https://en.wikipedia.org/wiki/React_(software) |
| `framework_vue` | Vue.js / Nuxt | JS UI framework and its SSR framework Nuxt. | https://vuejs.org/ | https://en.wikipedia.org/wiki/Vue.js |
| `framework_angular` | Angular | Google-backed JS framework. | https://angular.dev/ | https://en.wikipedia.org/wiki/Angular_(web_framework) |
| `framework_nextjs` | Next.js | React framework with SSR / static export; by Vercel. | https://nextjs.org/ | https://en.wikipedia.org/wiki/Next.js |
| `framework_gatsby` | Gatsby | Static-site generator built on React. | https://www.gatsbyjs.com/ | https://en.wikipedia.org/wiki/Gatsby.js |
| `framework_astro` | Astro | Static-first multi-framework site builder. | https://astro.build/ | (Wikipedia page limited) |
| `framework_svelte` | Svelte / SvelteKit | Compile-time JS framework. | https://svelte.dev/ | https://en.wikipedia.org/wiki/Svelte |

## Analytics

| Detector name | Vendor / product | What it does | Primary URL | Secondary URL |
| --- | --- | --- | --- | --- |
| `analytics_google` | Google Analytics / Tag Manager | Dominant free analytics platform. | https://marketingplatform.google.com/about/analytics/ | https://en.wikipedia.org/wiki/Google_Analytics |
| `analytics_snowplow` | Snowplow Analytics | Self-hosted / warehouse-native event analytics; a marker of larger data teams. | https://snowplow.io/ | https://en.wikipedia.org/wiki/Snowplow_(software) |
| `analytics_hotjar` | Hotjar | Session recording and heatmap analytics. | https://www.hotjar.com/ | https://en.wikipedia.org/wiki/Hotjar |
| `analytics_plausible` | Plausible Analytics | Privacy-focused open-source analytics alternative. | https://plausible.io/ | (no widely-cited Wikipedia page) |
| `analytics_matomo` | Matomo (Piwik) | Open-source, self-hostable analytics. | https://matomo.org/ | https://en.wikipedia.org/wiki/Matomo_(software) |
| `analytics_clarity` | Microsoft Clarity | Free Microsoft heatmap/session-recording analytics. | https://clarity.microsoft.com/ | https://en.wikipedia.org/wiki/Microsoft_Clarity |
| `analytics_amplitude` | Amplitude | Product analytics platform. | https://amplitude.com/ | https://en.wikipedia.org/wiki/Amplitude_(company) |
| `analytics_segment` | Segment (Twilio) | Customer data platform and event forwarder. | https://segment.com/ | https://en.wikipedia.org/wiki/Segment.com |
| `analytics_fathom` | Fathom Analytics | Privacy-focused analytics alternative. | https://usefathom.com/ | (no widely-cited Wikipedia page) |
| `analytics_hubspot` | HubSpot | Marketing-automation / CRM with embedded analytics. | https://www.hubspot.com/ | https://en.wikipedia.org/wiki/HubSpot |

## CDN / hosting / infrastructure

| Detector name | Vendor / product | What it does | Primary URL | Secondary URL |
| --- | --- | --- | --- | --- |
| `cdn_cloudflare` | Cloudflare | Global CDN, DDoS protection, reverse proxy. Dominant in our cohort. | https://www.cloudflare.com/ | https://en.wikipedia.org/wiki/Cloudflare |
| `cdn_cloudfront` | Amazon CloudFront | AWS's CDN. | https://aws.amazon.com/cloudfront/ | https://en.wikipedia.org/wiki/Amazon_CloudFront |
| `cdn_fastly` | Fastly | Edge CDN popular with larger media properties. | https://www.fastly.com/ | https://en.wikipedia.org/wiki/Fastly |
| `cdn_akamai` | Akamai | Legacy enterprise CDN. | https://www.akamai.com/ | https://en.wikipedia.org/wiki/Akamai_Technologies |
| `cdn_vercel` | Vercel | Next.js-creator's hosting/edge platform. | https://vercel.com/ | https://en.wikipedia.org/wiki/Vercel |
| `cdn_netlify` | Netlify | Static-site and Jamstack hosting. | https://www.netlify.com/ | https://en.wikipedia.org/wiki/Netlify |
| `cdn_jsdelivr` | jsDelivr | Public open-source CDN for JS/CSS libraries; used by many wrapper scripts (including Ezoic's). | https://www.jsdelivr.com/ | (no widely-cited Wikipedia page) |
| `cdn_cdnjs` | cdnjs (Cloudflare) | Another public open-source CDN for JS libraries. | https://cdnjs.com/ | (no widely-cited Wikipedia page) |
| `cdn_hostinger` | Hostinger CDN | CDN bundled with the Hostinger shared-hosting product. | https://www.hostinger.com/ | (no widely-cited Wikipedia page) |
| `cdn_google` | Google Cloud CDN | Google's CDN product, often attached to Google-hosted Wix / GCP sites. | https://cloud.google.com/cdn | https://en.wikipedia.org/wiki/Google_Cloud_Platform |

## Web servers

| Detector name | Vendor / product | What it does | Primary URL | Secondary URL |
| --- | --- | --- | --- | --- |
| `server_nginx` | nginx | Dominant open-source reverse proxy / HTTP server. | https://nginx.org/ | https://en.wikipedia.org/wiki/Nginx |
| `server_apache` | Apache HTTP Server | Classic open-source HTTP server. | https://httpd.apache.org/ | https://en.wikipedia.org/wiki/Apache_HTTP_Server |
| `server_litespeed` | LiteSpeed Web Server | Commercial Apache-compatible server popular with shared hosts. | https://www.litespeedtech.com/products/litespeed-web-server | https://en.wikipedia.org/wiki/LiteSpeed_Web_Server |
| `server_iis` | Microsoft IIS | Windows-native HTTP server. | https://www.iis.net/ | https://en.wikipedia.org/wiki/Internet_Information_Services |
| `server_caddy` | Caddy | Go-based HTTP server with automatic HTTPS. | https://caddyserver.com/ | https://en.wikipedia.org/wiki/Caddy_(web_server) |

## SEO / engagement add-ons

| Detector name | Vendor / product | What it does | Primary URL | Secondary URL |
| --- | --- | --- | --- | --- |
| `seo_yoast` | Yoast SEO | Most-installed WordPress SEO plugin. | https://yoast.com/ | https://en.wikipedia.org/wiki/Yoast_SEO |
| `seo_rankmath` | Rank Math | Yoast competitor for WordPress SEO. | https://rankmath.com/ | (no widely-cited Wikipedia page) |
| `comments_disqus` | Disqus | Embedded comments platform. | https://disqus.com/ | https://en.wikipedia.org/wiki/Disqus |
| `payment_stripe` | Stripe | Payment-processing API / checkout. | https://stripe.com/ | https://en.wikipedia.org/wiki/Stripe,_Inc. |
| `payment_paypal` | PayPal Checkout | Payment-processing API. | https://www.paypal.com/ | https://en.wikipedia.org/wiki/PayPal |

## Monetization-ladder framing for the paper

Useful reading order when writing the paper: the ad-management tier
is itself a signal of where the site is in its monetization lifecycle.

1. **Entry-level**: Google AdSense (self-serve), Ezoic (AI-managed,
    minimal traffic floor).
2. **Managed mid-tier**: Monumetric, Mediavine.
3. **Managed premium**: Raptive (formerly AdThrive / CafeMedia).
4. **Header-bidding stack** (DIY premium): Pubmatic / Index Exchange /
    Criteo / Sharethrough / Sovrn / Mediavine wrapper, usually with
    Snowplow / Google Ad Manager at the publisher side.
5. **Audience cultivation** (not ad-tech): Substack, Kit
    (ConvertKit), Mailchimp, Ghost, Patreon.

Our cohort shows LLM enrichment at level 1 (AdSense, Ezoic) and human
enrichment at level 3, level 4, and level 5. This ladder is one
way to describe the gap.

Sources for the general monetization-tiering framing:
- Google AdSense eligibility: https://support.google.com/adsense/answer/12171608
- Ezoic "Access Now" program: https://pubgenius.com/resource-center/access-now/
- Monumetric minimum traffic: https://www.monumetric.com/pricing/
- Mediavine minimum traffic: https://www.mediavine.com/advertisers-programmatic-partners/
- Raptive application: https://raptive.com/publishers/apply/
