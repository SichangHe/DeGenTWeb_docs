# CC Pre-ChatGPT False Positives

## Summary

The full-pipeline SVM incorrectly classifies 103 CC sites as LLM-dominant even though
all their archived pages predate ChatGPT's launch (before 2022-11-30). These sites are
definitively human-written, so every "LLM-dominant" prediction is a false positive.
The dominant pattern is **highly uniform, templated human prose**: local business service
pages (dental, auto repair, dealerships), product/e-commerce listings, real-estate landing
pages, and affiliate/SEO articles all share low perplexity and lexical predictability that
the Binoculars scorer mistakes for LLM output. A smaller cluster of scripture/liturgical
text and technical documentation contributes the same signal via domain-specific formulaic
language. All 103 subdomains have categorization data from `subdomain_categorizations`.

---

## Category breakdown

### Local business service operators — dental/medical practices (18 sites)

Multi-page sites describing procedures, staff bios, FAQs, and appointment CTAs.
Professionally written, jargon-rich, tight clinic-page templates produce low Binoculars
perplexity.

- www.arlingtontxdentists.com — dental practice lead-gen, templated procedure pages
- www.bakersmiles.com — orthodontic practice, repeated treatment descriptions
- www.drstewarddds.net — dental procedures info with contact forms
- www.kumarorthodontics.com — orthodontic/dentofacial services
- www.lajolladentistry.com — dental FAQs and financing content
- www.larrabee.samsesame.com — dental practice (SamSesame subdomain)
- www.lathroportho.com — local orthodontic practice
- www.leddenandbradleydental.com — multi-service dental practice
- www.ligsny.com — gastroenterology practice patient-education pages
- www.madison.samsesame.com — dental services (SamSesame subdomain)
- www.manhattanoasisdentistry.com — dental practice, patient-facing info
- www.rampartdental.com — dental practice lead-gen
- www.sandiegohearing.com — hearing health services
- www.sh-dentist.com — dental procedures and appointment CTAs
- elswickchiropractic.com — chiropractic/health services, multi-topic pages
- locations.amedisys.com — multi-location home health and hospice (business operator)
- www.liberationinmind.com — paid hypnotherapy audio sessions (own service)
- coastalmedical.applicantpro.com — job listing subdomain (ATS) for medical group

### Local business service operators — auto repair, home services (12 sites)

Auto repair shops with per-make service pages ("BMW repair", "Toyota service"),
customer review snippets, and appointment CTAs; also appliance/plumbing/fence services.
Per-service template pages are highly predictable, lowering Binoculars perplexity.

- apopkaappliancerepairmen.com — appliance repair services lead-gen
- autoonejackson.com — multi-brand auto repair shop
- www.elportalappliancerepairmen.com — appliance repair lead-gen
- essexdrainage.services — drainage repair business, service pages
- fenceinstallersjax.com — fence installation services
- maidattendants.com — residential/commercial cleaning services
- www.leonardiauto.com — auto repair, multi-make pages
- www.rickyjordansautorepair.com — auto repair, multi-make pages
- www.rissisauto.com — automotive repair/maintenance
- www.rpmautomotiveinc.com — automotive repair shop
- www.seydesign.com — location-specific emergency plumbing lead-gen pages
- www.waltsautoservice.com — automotive service shop

### Auto dealerships (12 sites)

Vehicle inventory pages with model descriptions, certifications, dealer contact CTAs,
and occasional blog posts. Inventory descriptions are formulaic and co-produced with
manufacturer content, lowering perplexity significantly.

- www.antrimhonda.com — Honda dealership inventory
- www.laddhanford.com — used car dealership vehicle listings
- www.lexusofmilwaukee.com — Lexus dealer inventory
- www.libertyford.com — Ford dealership
- www.rmlauto.com — used truck dealership
- www.rockcountyhonda.com — Honda dealership
- www.romanovw.com — VW dealership inventory
- www.volvocarscharlottesville.com — Volvo dealership
- www.volvocarsdemontrond.com — Volvo dealership
- www.volvocarssandiego.com — Volvo dealership
- www.volvooflouisville.com — Volvo dealership
- www.volvowinterpark.com — Volvo dealership blog/inventory

### Real estate agents and brokers (7 sites)

Real-estate agent personal sites with IDX listings, market-advice editorial articles,
and contact-form CTAs. Lead-gen prose is formal, repetitive across agents, and produced
from shared marketing templates.

- www.leodesjardins.com — RE agent editorial articles for lead-gen
- www.ryanhunchak.com — RE agent real-estate advice articles
- www.sallynicholasrealtor.com — RE agent listings and contact
- www.shaneownby.com — RE brokerage with IDX listings
- www.wendyrye.com — RE agent personal site
- www.westsuburbanrealestate.com — RE editorial lead-gen articles
- www.yesirealestate.com — RE agent self-promotional articles

### E-commerce and product listings (13 sites)

Product catalog pages with SKUs, specs, pricing, and purchase CTAs. Structured
product descriptions have low variance and low perplexity due to template reuse
and schema.org markup patterns.

- 24pharma.pk — pharmaceutical product pages (schema.org markup)
- eviraldeal.com — direct-to-consumer product listings
- mbparts.mbusa.com — OEM Mercedes-Benz parts (official subdomain)
- riddhika.com — handmade jewelry product listings
- ruggable.com — rug product listings with detailed descriptions
- www.365inflatable.co.uk — inflatable product pages with schema.org
- www.croma.org.es — bearing product pages, B2B lead-gen
- www.ellentonflorist.com — floral/gift product sales
- www.embellishyourwedding.com — wedding stationery product listings
- www.eschaussinhandball.com — bearing products with pricing
- www.libertyandjasminevintage.com — vintage clothing product pages
- www.rollsbearing.com — bearing product listings with specs
- www.ropeservicesuk.com — rope product pages with schema.org

### Other lead-gen and B2B service operators (9 sites)

Varied business service sites (insurance, finance, industrial equipment, corporate IR)
with uniform landing-page prose aimed at lead capture.

- www.americansforthefamily.com — insurance lead-gen (funeral/life/annuity)
- www.aprpayday.com — payday/business loan origination
- www.aercap.com — corporate press releases, investor relations
- www.buena-rajstopy.pl — mining equipment manufacturer, B2B
- dpsmakowpodhalanski.pl — heavy equipment manufacturer, product catalog
- evdanco-energy.com — industrial brake-block manufacturer with inquiry form
- www.elite-taxes.com — tax/accounting/elder-care professional services
- www.sambhavmetal.com — metal product catalog, B2B lead-gen
- paydayloansnearme.me — payday loan lead-gen (own service)

### Publisher/editorial sites (10 sites)

Original editorial content (travel guides, personal blogs, fashion articles, ESL
lessons, podcast episode descriptions). Fluent, readable prose scores low in
perplexity and overlaps with the LLM-dominant SVM region.

- annedennish.com — personal author blog (books, personal reflections)
- everytravelguide.com — travel-guide editorial articles
- flickereffect.libsyn.com — podcast episode descriptions (movies/TV)
- outsidetheloopradio.libsyn.com — podcast episode descriptions (Chicago)
- rong-chang.com — ESL reading passages and grammar lessons
- voguestateofmind.com — personal fashion/beauty blog
- www.fancyfashioncastleblog.com — travel/fashion/lifestyle editorial
- www.silverlakemomsclub.org — beauty/hair advice editorial
- www.ymcaktub.org — beauty/fashion/lifestyle editorial
- www.sandrinesgallery.com — artist personal blog, tutorials, artwork

### Religious and scripture sites (5 sites)

Daily liturgical readings, lectionaries, and full Bible chapters. Formal, highly
repetitive, syntactically regular, clean text produces Binoculars scores in the
LLM range despite being centuries-old human writing.

- nycathedral.org — daily Orthodox liturgical readings and saint commemorations
- stpatricklutheran.org — daily lectionary readings and collects
- whitepaperbible.org — Christian devotional papers (publisher/editorial)
- www.northsidebaptistgso.org — church ministries and worship-service info
- www.studybible.me — full Bible chapters presented for reading

### Technical documentation and support (3 sites)

API references, XAMPP install guides, and network-graph tool documentation.
Technical writing is precise, low-variance, and formulaic, mimicking LLM output style.

- docs.scriptable.app — Scriptable app API reference (class/method/property docs)
- fiscaliamorc.net — XAMPP installation/configuration documentation
- longstay.fr — XAMPP setup tutorials and troubleshooting guides

### Affiliate/SEO content farms (8 sites)

Thin articles designed to capture search traffic and monetize via referral links.
Formulaic "best X" and comparison articles naturally score as LLM-like due to
low lexical variance.

- adult-hookup.co.uk — affiliate reviews of adult dating platforms
- autopartslife.com — keyword-rich automotive how-to articles
- avaimobile.com — thin "best X" product-review articles with affiliate notices
- bluebracket.net — thin mattress-review affiliate articles
- cbmnetnibb.net — templated IRA company reviews with affiliate CTAs
- world-power-plugs.com — location-specific travel adapter affiliate articles
- www.ezyhotelbooking.com — boilerplate Kartra-feature articles (SEO only)
- www.jobdescription.ai — ready-made job description templates (resource farm)

### Spam/parked content farms (3 sites)

Pages with no real content or service; exist purely to capture search traffic.
Auto-generated or very sparse text may coincidentally land in the LLM score range.

- worldclick.org — thin boilerplate app-description pages (content farm)
- www.evimitasi.com — autogenerated domain-analysis ad pages (parked)
- www.masteringsharepoint.com — low-quality template articles, no functionality

### Miscellaneous (3 sites)

- aonlinetitanpoker.com — poker strategy guides (publisher/editorial, formal instructional tone)
- destinia.com.pa — thin SEO hotel-destination booking pages for own travel service
- www.nodexlgraphgallery.org — autogenerated network-graph display pages (tool/utility)

---

## Sites without categorization data (0 sites)

All 103 subdomains have `why_text` populated in `subdomain_categorizations`.

---

## Implications for pipeline

The false positives cluster into three root causes:

1. **Template/boilerplate human prose** (roughly 65 of 103 FPs): local business service
   pages, dealership inventory descriptions, product listings, and real-estate landing
   pages are written by copywriters following tight templates. Their low lexical variance
   produces Binoculars scores indistinguishable from LLM output. This is the dominant
   failure mode and is structural — such text is genuinely hard to distinguish from
   LLM-generated content on perplexity alone.

2. **Formally written or domain-specific text** (~18 FPs): scripture readings,
   liturgical calendars, technical documentation, and B2B product catalogs use precise,
   repetitive language that also scores as LLM-like. These FPs are essentially impossible
   to separate from LLM output using a score-only approach without domain-aware heuristics
   (e.g., date of first publication, detected scripture markup).

3. **Thin/low-value pages** (~11 FPs): affiliate thin articles and spam content farms
   contain sparse text whose score distribution may land in the LLM range by coincidence,
   or whose per-page variance is so low that the decile vector maps to the LLM region.

These FPs confirm that the Binoculars scorer has a known weakness on professionally
templated or formally structured text, and that the SVM trained on baseline decile
distributions inherits this weakness. The overall FPR of ~0.29% (103/35856 before-GPT
sites) is low enough that the pipeline is reliable at scale for detecting widespread
LLM adoption. However, individual site-level verdicts for heavily templated service
sites should be treated with caution.
