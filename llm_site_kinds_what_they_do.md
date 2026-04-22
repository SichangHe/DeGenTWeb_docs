# What LLM-Dominant Search-Result Sites Are Actually Doing

Hierarchical breakdown of 2,243 LLM-like search-result sites based on their
`subdomain_categorizations.why_text` notes (one note per site, latest
categorization run), cross-referenced with the site-level monetization
features in the DuckDB session (`site_full_mg` table).

**Cohort.** 3,596 sites total (2,243 LLM-like, 1,353 human-like). Label =
sign of SVM distance. The 2,243 LLM sites all have a categorization note;
this doc covers all of them.

**Methodology.** Four subagents read all 2,243 notes in parallel, one per
major category. Topic-frequency keyword counts (regex, word-boundary) were
run independently to cross-check estimates. Percentages at each level are
rounded to the nearest integer and sum to ~100% within each grouping.

---

## Overview

| Category | n | % of LLM cohort |
| --- | ---: | ---: |
| Publisher / editorial | 1217 | 54.3% |
| Business / service operator | 408 | 18.2% |
| Affiliate / SEO content | 250 | 11.1% |
| Retail e-commerce | 140 | 6.2% |
| Product / SaaS company | 64 | 2.9% |
| Personal | 42 | 1.9% |
| Tool / utility | 40 | 1.8% |
| Asset / boilerplate resources | 20 | 0.9% |
| Institutional | 18 | 0.8% |
| Marketplace / directory | 15 | 0.7% |
| Support / knowledge base | 13 | 0.6% |
| Fringe (spam, piracy, adult, etc.) | 16 | 0.7% |

**Top-line monetization (all 2,243 LLM sites):**

| Monetization bucket | n | % |
| --- | ---: | ---: |
| ads\_only | 1060 | 47.3% |
| none\_detected | 767 | 34.2% |
| ads\_and\_affiliate | 269 | 12.0% |
| affiliate\_only | 98 | 4.4% |
| lead\_gen\_only | 22 | 1.0% |
| subscribe\_or\_donate | 15 | 0.7% |
| commerce\_checkout | 12 | 0.5% |

---

## 1. Publisher / Editorial Sites (1217 sites, 54.3%)

Sites whose primary product is original staff-written or AI-generated
informational articles. The content spans practical how-tos, explainers,
listicles, product overviews, recipes, niche-expertise pieces, and news.
Revenue comes almost entirely from display ads and, secondarily, affiliate
commissions. The editorial voice ranges from personal (single author,
first-person) to multi-author publications with a professional but generic
style. Monetization is overwhelmingly ad-supported; fewer than 3% of
editorial LLM sites use newsletter subscriptions.

**Topic distribution across all 1,217 editorial LLM sites** (keyword match,
many sites match more than one topic; ordered by frequency):

| Topic niche | ~% of editorial |
| --- | ---: |
| General how-to / listicle (no dominant niche) | 16% |
| Health / medical | 13% |
| Recipe / food / cooking | 10% |
| Pets / animal care | 7% |
| Relationships / lifestyle / self-help | 6% |
| Career / business | 6% |
| Home improvement / DIY / gardening | 5% |
| Technology / AI | 3% |
| Fitness / exercise | 3% |
| Travel / outdoor | 3% |
| Crafts / hobbies (drawing, music, etc.) | 3% |
| Education / academic | 3% |
| Beauty / hair / makeup | 3% |
| Spirituality / religion | 2% |
| Gaming / entertainment | 2% |
| Sports | 1% |
| Legal / law | 1% |
| Personal finance / investing | 1% |
| Environment / sustainability | 1% |
| Other / mixed niche | 11% |

### 1.1 ads\_only (612 sites, 50.3% of editorial)

Pure CPM/CPC display advertising. Sites publish SEO-targeted informational
content and earn revenue from impressions. This is the "paste an AdSense
tag and publish" model. Affiliate programs are absent or not detected.

**Sub-types:**

- **Generic multi-topic how-to blogs** (~25%): Wide-topic articles on home,
  lifestyle, pets, and relationships with no dominant subject. Content is
  broad enough to capture any search query. Typically 30–200 articles with
  high keyword-density titles ("How to X", "What is Y", "Best Z in 2025").
  Examples: `sharksmind.com` (broad advisory content on diverse topics),
  `smallpetjournal.com` (pet care across many species), `g15tools.com`
  (gambling psychology, telemedicine, sports betting — random topic mix).

- **Health / wellness / medical explainer blogs** (~13%): Non-clinical
  articles explaining conditions, symptoms, treatments, and wellness
  practices. Written to rank on health queries without medical credentials.
  Often include disclaimer boilerplate. Examples: `healthendure.com` (health
  and wellness articles), `psychology.tips` (psychology topics — ADHD,
  therapy, relationships), `know-the-ada.com` (ADA healthcare accessibility
  guides), `medicalhubnews.com` (drug interactions, health topics).

- **Recipe and food content** (~11%): Recipe articles with structured data
  (schema.org Recipe), ingredient lists, and step-by-step instructions.
  Often personal-voice blogs. Ads are sidebar or in-content. Examples:
  `tastepursuits.com` (staff-written food articles), `elianarecipes.com`
  (recipe collections), `grillstory.net` (grilling techniques).

- **Pet and animal care guides** (~6%): Breed profiles, care instructions,
  health guides, and behavioral tips across dogs, cats, fish, reptiles. High
  search volume per species/breed. Examples: `likeablepets.com` (pet care
  advice), `bettafishworld.com` (aquarium fish guides), `www.dog-breeds.net`
  (breed profiles).

- **Home improvement / gardening / DIY** (~4%): How-to articles on home
  maintenance, gardening, and consumer-electronics setup. Examples:
  `automatelife.net` (smart-home how-tos), `toagriculture.com` (agriculture
  and horticulture guides), `busyyard.com` (gardening), `pooltipsusa.com`
  (pool maintenance).

- **Technology / programming tutorials** (~4%): Code walkthroughs, software
  guides, and app how-tos. Often targets developer-adjacent queries.
  Examples: `idroot.us` (technical how-to tutorials), `www.sparkcodehub.com`
  (programming and data engineering), `www.solveyourtech.com` (tech how-tos),
  `www.appcracy.com` (app reviews and info).

- **Niche-topic single-subject blogs** (~12%): Sites with one well-defined
  topic — drawing tutorials, Bible study, board game rules, astrology,
  Lean Six Sigma, running/triathlon, card-game rules. Examples:
  `sketchok.com` (step-by-step drawing tutorials), `faithinthedivine.com`
  (biblical/spiritual articles), `officialgamerules.org` (board/card game
  rules), `www.learnleansigma.com` (Lean Six Sigma guides).

- **Spiritual / religious content** (~4%): Christian devotionals, Bible
  commentary, pastoral writing, astrology, crystal healing. Examples:
  `biblicalchronology.com` (biblical history), `osrsmoneymaking.guide`
  (RuneScape guides).

- **AI / LLM tool commentary and review** (~3%): Blogs covering AI tool
  releases, tutorials for ChatGPT, Midjourney, and similar. Often
  self-referential — AI tools writing about AI. Examples:
  `www.yeschat.ai` (AI tool roundups and tutorials).

### 1.2 none\_detected (416 sites, 34.2% of editorial)

No ads, no affiliate, no lead-gen detected. Two populations: (a)
enthusiast/passion-project blogs with very low traffic that have not yet
deployed or qualified for monetization; (b) sites that have recently
launched and not yet enrolled in ad programs. Content quality appears
similar to ads\_only but traffic is likely substantially lower.

**Sub-types:**

- **Health and wellness education (no revenue)** (~18%): Wellness, nutrition,
  mental health, and personal development articles with no monetization.
  Likely low-traffic or recently launched. Examples: `crystalhappiness.com`
  (crystal properties and uses), `www.edailyworkout.com` (health and fitness
  articles), `embodiedmoments.com` (mental wellness), `petlifeblog.com` (pet
  care with zero ads).

- **General hobby / how-to (no revenue)** (~20%): How-to and tutorial
  content across diverse niches — photography, gardening, tire care, Word
  tutorials, VPN guides — with zero monetization. Examples:
  `www.artisticphotographyguide.com` (photography tips),
  `aggressivelyorganic.com` (organic gardening), `tirethink.com` (tire
  info), `learnword.io` (Microsoft Word how-tos).

- **Niche single-subject enthusiast sites** (~15%): Sites about very narrow
  topics with no revenue (crystals, birds, gemstones, card games, astronomy).
  Examples: `birdswave.com` (bird articles), `stongle.com` (gemstones and
  diamond guides), `fossilnest.com` (gemstone and geode collecting).

- **AI / tech education (non-commercial)** (~7%): AI explainer sites and
  tech educational blogs with no revenue. May be early-stage or bootstrapped.
  Examples: `truthordare.ai` (AI application examples), `aicompetence.org`
  (AI education).

- **Brand blog / content marketing without visible monetization** (~10%):
  Company blogs that publish content to drive awareness or leads but have no
  external ads or affiliate. Revenue is indirect (product/service promotion
  on same domain). Examples: `www.nestinsights.com` (property market news
  + platform promotion), `blog.tracespend.com` (personal finance articles
  promoting TraceSpend product).

### 1.3 ads\_and\_affiliate (143 sites, 11.7% of editorial)

Display ads plus affiliate links. These sites layer affiliate product
recommendations on top of an editorial foundation. The affiliate layer is
secondary to editorial content — articles are not purely review/buying-guide
content but include product links where relevant.

**Sub-types:**

- **Recipe / food with kitchen-equipment affiliate** (~24%): Cooking articles
  with embedded links to kitchen tools, ingredients, or appliances. Amazon
  Associates is the primary affiliate program. Examples:
  `cookerdiary.com` (recipes with tool affiliate links), `familytablevibes.com`
  (recipes with product links), `thenailsnation.com` (beauty and nail art
  with product links).

- **Home / DIY / smart-home with product affiliate** (~7%): Home improvement
  and smart-device articles with product recommendations and affiliate links.
  Examples: `homescale.net` (home appliance how-tos), `dreamoutdoorliving.com`
  (outdoor living articles).

- **Health / wellness with supplement affiliate** (~14%): Wellness articles
  linking to supplements, fitness equipment, or wellness products. Examples:
  `theherbprof.com` (herbal medicine reviews), `www.mensfitclub.com` (men's
  fitness with product links).

- **General product review + listicle** (~15%): "Best X" articles with
  affiliate product links, not purely affiliate-SEO-category content.
  Examples: `robots.net` (product review listicles), `thetirereviews.com`
  (tire reviews with links), `smartwatchinsight.com` (smartwatch comparisons).

- **Tech / software review with affiliate** (~5%): Software tool comparisons
  and AI tool reviews with affiliate or referral links. Examples:
  `webhostinggeeks.com` (web hosting articles), `sysadminsage.com` (sysadmin
  tech articles).

- **Niche lifestyle / hobby with incidental affiliate** (~20%): Sports, pets,
  travel, spirituality content with occasional product links. Examples:
  `turtlepetguide.com` (turtle care and products), `christpulse.com`
  (Christian content), `safeskateboard.com` (skateboard guides).

### 1.4 affiliate\_only (32 sites, 2.6% of editorial)

Affiliate links are the sole detected monetization. These sites are on the
cusp of being `affiliate_seo_content`; the editorial framing is more
prominent than in the pure affiliate-SEO cohort but the revenue model is
the same. Generally lower editorial quality than ads\_only.

**Sub-types:**

- **Pet product guides presented as editorial** (~35%): Breed or care
  articles with embedded product recommendations. Examples:
  `iheartdogs.com` (dog articles with product recommendations),
  `dachshundsplanet.com` (breed-specific product guides).

- **Health / wellness product recommendations** (~20%): Wellness or medical
  topic articles with supplement or device affiliate links.

- **Home improvement product guides** (~15%): DIY / home content with
  hardware and materials affiliate links.

### 1.5 subscribe\_or\_donate / lead\_gen (12 sites, 1.0% of editorial)

Very small cohort. Subscribe/donate sites (~8) are niche passion projects:
piano learning guides (`pianoers.com`), art-education magazines
(`serenademagazine.art`), massage education (`massageforbody.com`). Lead-gen
editorial sites (~4) use content to drive conversions: career-mentoring
leads (`blog.mentoria.com`), lab-testing service leads (`www.getlabtest.com`).

---

## 2. Business / Service Operators (408 sites, 18.2%)

Real-world, often offline-first service businesses using LLM-generated blog
content as an SEO and trust-building layer. Revenue flows from service
delivery (appointments, labor, professional fees, custom products), not from
ads. LLM content answers common customer questions, explains services and
procedures, and drives organic search traffic to appointment or contact forms.

**Industry breakdown across all 408 BSO sites:**

| Industry | ~% of BSO |
| --- | ---: |
| Healthcare / medical / therapy | 20% |
| Local home services (plumbing, pest, cleaning, construction) | 15% |
| Professional services (law, accounting, marketing, HR, consulting) | 18% |
| Education / training / coaching | 10% |
| Digital / IT services and SaaS | 8% |
| B2B manufacturing, printing, materials | 8% |
| Beauty / esthetics / wellness | 7% |
| Other / specialty services | 14% |

### 2.1 none\_detected (194 sites, 47.5% of BSO)

No display ads. The business earns via service delivery; ads would distract
from conversion. These are pure lead-generation machines using LLM content
as SEO infrastructure.

**Sub-types:**

- **Healthcare providers and medical practices** (~20%): Dental practices,
  ENT, psychiatry, pediatrics, physical therapy, veterinary clinics, ABA
  therapy, telehealth. Content educates patients on conditions and treatments;
  every article ends with an appointment CTA. Examples: `www.enttx.com` (ENT
  / allergy clinic), `www.allstarimplants.com` (dental implants),
  `zoelifepsychiatricservices.com` (telepsychiatry), `swallergy.com`
  (allergy and asthma practice), `cvhsaratoga.com` (veterinary hospital).

- **Local service contractors** (~20%): Plumbing, pest control, cleaning,
  painting, HVAC, pool installation, fencing, wildlife removal, auto repair.
  LLM writes service-specific guides ("how to prevent pests", "types of
  roofing") to rank for local keywords. Examples: `zipzappestcontrol.com`
  (pest control), `agvinylfencing.com` (vinyl fencing), `www.lawnlab.com`
  (lawn care), `www.virginiawildlifepros.com` (wildlife removal),
  `apxconstructiongroup.com` (construction and remodeling).

- **Professional service firms** (~18%): Law firms, CPA/accounting, marketing
  agencies, recruiting, staffing, immigration consulting, digital marketing.
  LLM creates practice-area explainers and how-to guides that establish
  expertise. Examples: `zakfisherlaw.com` (criminal defense / bankruptcy),
  `masseyandcompanycpa.com` (CPA and tax), `earthrelocation.com` (moving
  and relocation), `networkcablingirvine.com` (network cabling services),
  `marketwiz.ai` (digital marketing for niche industries).

- **Education and training schools** (~13%): Coding bootcamps, martial arts,
  acting schools, modeling, CPR training, surfing, speech therapy, online
  courses. LLM content explains curriculum, learning methods, and career
  paths. Examples: `pinecone.academy` (coding for kids), `silverdragondojo.com`
  (martial arts), `nirgunaactingschool.com` (acting school), `solidsurfhouse.com`
  (surf coaching retreats).

- **B2B manufacturing and materials suppliers** (~10%): CNC machining, custom
  packaging, garment manufacturing, foam products, industrial supplies. LLM
  blog showcases production capabilities; targets procurement and B2B buyers.
  Examples: `mechforce.com` (CNC machining), `www.epackprinting.com` (custom
  packaging), `uwinfoam.com` (foam manufacturing).

- **Health/wellness alternative practitioners** (~10%): Holistic healing,
  ABA therapy, hypnosis, CPR training, mental health counseling. Similar to
  medical but without clinical credentials. Examples:
  `www.auroraholistichealing.com` (holistic healing), `lgbtqiacounseling.com`
  (LGBTQ+ therapy), `moveupaba.com` (ABA therapy).

### 2.2 ads\_only (185 sites, 45.3% of BSO)

Same business types as none\_detected but running display ads on
lower-conversion content pages. The ads monetize browsing traffic that
doesn't convert to service leads. This suggests a slightly higher-traffic
profile than the no-ads BSO sites.

**Sub-types (same industry mix):**

- **Healthcare and medical practices** (~16%): Similar composition to
  none\_detected — dental, ENT, pediatrics, physical therapy, veterinary,
  telehealth. Examples: `www.entdoctoroc.com` (ENT), `medicalhousecalls.com`
  (concierge primary care), `www.ewmotiontherapy.com` (physical therapy),
  `animaloutpatientsurgery.com` (veterinary surgery).

- **Local service contractors** (~15%): Cleaning, painting, appliance repair,
  pest control. Examples: `www.crownclassiccleaners.net` (commercial
  cleaning), `www.mgppainting.com` (painting contractor), `drgreenservices.com`
  (lawn and pest).

- **Professional services** (~20%): Marketing agencies, CPA services,
  staffing, immigration consulting, personal injury law. Examples:
  `sbgfunding.com` (business financing), `www.superfastcpa.com` (CPA exam
  prep), `markbandylaw.com` (bankruptcy / foreclosure).

- **Education and training programs** (~15%): Coding bootcamps, CPR/EMT
  certification, real estate licensing, nursing assistant training. Examples:
  `truthhealthacademy.com` (nursing assistant training), `lset.uk` (DevOps
  training), `www.americanrealtyacademy.com` (real estate licensing).

- **Digital services and SaaS** (~12%): Web development, content agencies,
  app development, custom hiring platforms. Examples: `www.sinelogix.com`
  (developer hiring), `headspace.media` (marketing/video production),
  `twinsunsolutions.com` (app development).

- **B2B manufacturing and B2B services** (~10%): Machinery, construction
  materials, garment manufacturing, data services. Examples:
  `www.mangoprocess.com` (mango processing machinery), `datacluster.com`
  (B2B data services), `ernestmaier.com` (construction materials).

### 2.3 lead\_gen\_only (10 sites, 2.5% of BSO)

Service businesses where lead capture is the sole visible revenue path —
no ads, no affiliate. Highly specific B2B or niche consumer services.
Examples: `marketwiz.ai` (marketing agency for niche industries),
`majorimpact.com` (local SEO services), `collegeessay.org` (essay writing
service), `boardsi.com` (executive recruitment).

---

## 3. Affiliate / SEO Content Sites (250 sites, 11.1%)

Sites built primarily to capture search traffic and earn commissions by
recommending products. Content is thinner than editorial sites and more
explicitly commercial — "best X" articles, buying guides, product
comparisons, and review listicles. The monetization model is the primary
design constraint; content exists to enable conversions.

### 3.1 ads\_and\_affiliate (99 sites, 39.6% of affiliate-SEO)

The most common affiliate-SEO model: both ad impressions and affiliate
commissions. Sites have high content volume to maximize both revenue
streams.

**Sub-types:**

- **Product review and buying guides** (~35%): Long-form "best [product]"
  articles with Amazon or merchant affiliate links embedded throughout.
  Typically covers 5–15 products per article with specs, pros/cons, and
  verdict. Examples: `slumberhabit.com` (mattress and pest reviews),
  `tiregrades.com` (tire guides), `toolsgearlab.com` (multi-category tools
  and gear), `robots.net` (product review listicles).

- **Lifestyle and wellness with product recommendations** (~25%): Health,
  beauty, home décor, and spirituality articles containing affiliate product
  links. Examples: `awakemindful.com` (meditation and health products),
  `frenchgirlbeauty.com` (beauty recommendations), `homedecorbliss.com`
  (home décor), `giftguideideas.com` (gift guides).

- **Niche hobby and craft content** (~20%): Deep editorial on specialized
  hobbies (gardening, fishing, music, knitting, coffee) with embedded
  product affiliate links. Examples: `livetoplant.com` (plant care and
  products), `reelrapture.com` (fishing gear), `grindthosebeans.com`
  (coffee equipment), `yarnfulcreations.com` (knitting supplies).

- **Food and recipe with ingredient affiliate** (~12%): Cooking guides and
  recipes with affiliate links to kitchen tools and ingredients. Examples:
  `www.simplycookingrecipes.com` (recipes with product links),
  `doughnutlounge.com` (baking articles), `greenplatepursuits.com` (food
  articles with tools).

- **Thin content farms** (~8%): Generic how-to and list articles with
  minimal original value, heavy ad density, and numerous affiliate links.
  Examples: `taratq.com` (consumer Q&A), `smallusefultips.com` (generic
  DIY tips), `ihowlist.com` (mixed-topic list articles).

### 3.2 ads\_only (67 sites, 26.8% of affiliate-SEO)

Pure ad-supported SEO content — high keyword density, no affiliate. These
sites rely entirely on CPM/CPC revenue from high-traffic informational
queries. Examples: `fluentslang.com` (slang definitions), `fishyfeatures.com`
(fish articles), `worldsoccerreader.com` (soccer topics),
`www.adamkempfitness.com` (fitness guides).

### 3.3 affiliate\_only (53 sites, 21.2% of affiliate-SEO)

Affiliate links are the sole monetization. High affiliate-link density.
These are pure comparison and recommendation sites without the ad layer.

**Sub-types:**

- **Product-focused buying guides** (~40%): High-ratio affiliate links in
  product comparison articles with no ad monetization. Examples:
  `toptenreviewed.com` (multi-category product lists), `goprocamerasreview.com`
  (GoPro gear), `helmetslab.com` (helmet reviews).

- **Specialized equipment and gear** (~30%): Fishing, outdoor, sports, and
  niche equipment reviews with dense affiliate links. Examples:
  `aguapulse.com` (kayaks and fishing gear), `spinningpole.com` (fishing
  gear), `bikeforgeeks.com` (bikes).

- **Fashion, beauty, and lifestyle** (~15%): Clothing, beauty, and wellness
  recommendations with affiliate links. Examples: `hairingcaring.com` (hair
  care), `designeraffair.com` (home décor), `www.myglowjourney.com` (beauty
  products).

- **Food and cooking affiliate** (~10%): Recipe and cooking content with
  affiliate links to ingredients or cookware. Examples:
  `heartyhomecook.com` (cooking guides with links),
  `ilikechocolates.com` (chocolate product recommendations).

### 3.4 none\_detected (29 sites, 11.6% of affiliate-SEO)

Affiliate-SEO sites with no detected monetization. Likely thin sites not
yet monetized, or using undetected affiliate mechanisms. Examples:
`backtothegoodlife.com`, `www.espressomuse.com` (likely early-stage or
using referral programs not caught by substring detection).

---

## 4. Retail E-commerce (140 sites, 6.2%)

Direct-to-consumer storefronts selling branded physical or digital products.
Sites feature product pages with pricing, purchase calls-to-action, and
schema.org Product markup. Editorial blog content supports brand sales
rather than serving as primary monetization.

### 4.1 ads\_only (73 sites, 52.1% of retail)

D2C retailers running display ads alongside their storefronts — likely
low ad revenue but ads fill dead space on informational pages.

**Product categories:**

- **Beauty, skincare, and hair** (~25%): Branded cosmetics, skincare,
  hair extensions, wigs. Examples: `elizabethobeauty.com` (skincare
  products), `lfactorcosmetics.com` (makeup), `www.sishair.com` (hair
  extensions), `yoghair.com` (hair extensions).

- **Health, wellness, and supplements** (~15%): Nutrition supplements,
  medical mobility aids, essential oils, wellness goods. Examples:
  `essentialsportsnutrition.com` (supplements), `bioma.health` (supplement
  pills), `apriahome.com` (medical mobility aids).

- **Food and beverage** (~12%): Specialty foods, meal kits, chocolates,
  natural skincare/food products. Examples: `www.factor75.com` (ready-made
  meals), `www.chocovira.in` (custom chocolates), `oldworldtruffles.com`
  (truffle foods).

- **Hobby, crafts, and specialty goods** (~12%): Cosplay products, minerals,
  mechanical pencils, lightsaber replicas, novelty items. Examples:
  `tokyo-cosplay.com` (cosplay), `izzyminerals.com` (gemstone/mineral sales),
  `astromx-sabers.com` (lightsaber replicas).

- **Home and garden products** (~10%): Furniture, live plants, custom badges,
  outdoor gear. Examples: `www.blueflowerco.com` (linen home goods),
  `tropicflow.com` (live fish and plants), `www.growjoy.com` (live plants).

- **Specialized industrial and equipment** (~10%): Monitor mounts, fishing
  tackle, forklifts, firearms. Examples: `www.mount-it.com` (desk mounts),
  `www.ltmgforklift.com` (forklifts), `proarmory.com` (firearms).

- **Digital products** (~10%): Study guides, Windows software keys, business
  templates, digital beats. Examples: `distilleryuniversity.com` (workshops),
  `wholsalekeys.com` (software licenses), `businessplan-templates.com`
  (templates), `beats4lyricists.com` (digital beats).

- **Fashion and apparel** (~8%): Footwear, costumes, accessories, press-on
  nails. Examples: `tonefootwear.com`, `www.costume-shop.com`, `daringlily.com`.

### 4.2 none\_detected (45 sites, 32.1% of retail)

E-commerce stores with no detected ads or affiliate. These are pure
product-sale revenue models.

**Sub-types:**

- **Niche physical goods retailers** (~40%): Tactical products, crystals,
  firewood, gemstones and jewelry. Examples: `crateclub.com` (tactical
  gear), `crescentcast.com` (crystals), `stackedwood.com` (firewood),
  `www.thenaturalsapphirecompany.com` (gemstones).

- **Professional and B2B goods/services** (~35%): Concrete delivery, RV
  awnings, medical equipment, cinema equipment. Examples:
  `supreme-concrete.com`, `www.natureawning.com`, `risenmedical.com`.

- **Plants, seeds, and agriculture** (~15%): Nurseries, seed suppliers,
  farm products, oak furniture. Examples: `www.stclareseeds.com` (seeds),
  `www.houseofoak.co.uk` (oak furniture).

- **Digital and content products** (~10%): E-books, guides, silicone molds.
  Examples: `www.guidetoprofitablelivestock.com` (digital guides),
  `candlesmolds.com` (molds and kits).

### 4.3 ads\_and\_affiliate (12 sites, 8.6%) and affiliate\_only (4 sites)

Hybrid retailers that also promote external products. Examples:
`enjoyandhavefun.com` (shop + affiliate content), `farmerflints.com`
(seeds + garden articles), `www.countrychicpaint.com` (paint + DIY
tutorials).

---

## 5. Product / SaaS Companies (64 sites, 2.9%)

Commercially operated software platforms. The site's primary product is the
software itself (often a freemium or subscription SaaS). LLM content on
these sites is marketing collateral — product blog posts, feature explainers,
use-case articles — rather than the primary value delivered to the user.

### 5.1 ads\_only (37 sites, 57.8% of SaaS)

**Sub-types:**

- **AI writing and productivity tools** (~40%): Essay writers, copywriting
  platforms, AI tutors, image/video editors, presentation builders.
  Examples: `perfectessaywriter.ai` (AI essay writing), `copy.ai`
  (AI copywriting), `maxstudio.ai` (AI image editing), `studymonkey.ai`
  (AI tutoring), `clickup.com` (project management).

- **Specialized software and APIs** (~30%): Browser extensions, API-driven
  design tools, video platforms, niche vertical SaaS. Examples:
  `bardeen.ai` (workflow automation), `tactiq.io` (meeting transcription),
  `stockimg.ai` (AI image generation), `bocalive.ai` (live streaming).

- **Financial and productivity SaaS** (~20%): Tax software, financial
  planning, workforce management. Examples: `keepertax.com` (tax), various
  business intelligence tools.

### 5.2 none\_detected (19 sites, 29.7% of SaaS)

Early-stage or pure-freemium SaaS with no detectable monetization on
crawled pages. Examples: niche API tools, browser extensions in beta,
vertical SaaS for specific industries.

### 5.3 lead\_gen\_only (5 sites, 7.8% of SaaS)

B2B SaaS using trial or demo requests as the primary conversion. Examples:
test-automation tools, business management platforms. Examples:
`10web.io` (website builder), `Tweetlio` (social media tool).

---

## 6. Smaller Categories (206 sites, 9.2%)

### 6.1 Personal sites (42 sites, 1.9%)

Individual bloggers and personal brands publishing self-authored content.
Often first-person voice and community-oriented around niche interests.

- **Personal lifestyle blogs with ads** (~48%): Recipe collections, hobby
  documentation. Examples: `cookwithbrendagantt.com` (personal cooking),
  `myhomemaderecipe.com`, `thetrashcanturkey.com` (hunting tips).

- **Pure personal editorial (no ads)** (~36%): Tech tutorials, author blogs,
  spirituality. Examples: `sebhastian.com` (tech articles),
  `emilyegarrison.com` (author blog), `paulvangelder.com` (spirituality).

- **Minimal hybrid monetization** (~19%): Light sponsorships or affiliate
  mentions alongside personal blog. Examples: `tobiasholm.com` (personal
  tech blog with a sheet-music shop), `livingplanetfriendly.com`
  (sustainability guides).

### 6.2 Tool / Utility sites (40 sites, 1.8%)

Interactive web utilities where users access the tool directly on the site.

- **Calculators and converters** (~70%): Financial calculators, unit
  converters, domain-specific calculators (caffeine content, diaper sizing,
  BMI). Examples: `calculator.academy`, `a2zcalculators.com`,
  `madecalculators.com`, `mathbz.com`.

- **AI-powered generators** (~20%): Story generators, name generators, AI
  writing assistants, code generators. Examples: `generatestory.io`,
  `writerbuddy.ai`, `codepal.ai`.

- **Specialized interactive tools** (~10%): File converters, travel planners,
  résumé builders. Examples: `convert.guru`, `picflow.com`, `1map.com`.

### 6.3 Asset / Boilerplate Resources (20 sites, 0.9%)

Downloadable and reusable templates, blueprints, and design assets.

- **Letter templates and legal documents** (~50%): Letter templates,
  certificate templates, legal contracts. Examples: `requestletters.com`,
  `sample-resignation-letters.com`, `creativecounsel.io`.

- **Technical blueprints** (~40%): Circuit diagrams, wiring diagrams, floor
  plans, financial models. Examples: `circuitdiagram.co`, `wiredraw.co`,
  `houseplanstory.com`, `10xsheets.com`.

- **Printable creative assets** (~15%): Coloring pages, worksheets for kids.
  Examples: `mimi-panda.com`, `freshcoloring.com`.

### 6.4 Institutional sites (18 sites, 0.8%)

Educational institutions, nonprofits, and professional associations.
Notably low LLM prevalence in the overall cohort (~17% LLM vs ~80% human
in this category), so these 18 are the minority that show LLM signals.

- **Educational institutions** (~50%): Universities, private schools,
  conservatories, online schools. Examples: `theglobalcollege.com`
  (international IB college), `101.school` (structured online courses).

- **Nonprofit and charitable organizations** (~33%): Healthcare nonprofits,
  disability advocacy, faith-based organizations. Examples:
  `smilesmovement.org` (oral health outreach), `disabilityhelp.org`
  (rights education).

- **Government and professional associations** (~17%): Government consulates,
  professional associations. Examples: `kenyaconsulatela.go.ke`,
  `ncacia.org` (crime investigators association).

### 6.5 Marketplace / Directory / Listings (15 sites, 0.7%)

Platforms aggregating third-party listings. Users browse and match with
services rather than purchasing from the platform.

- **Professional service directories** (~27%): Financial advisors, medical
  professionals, web design agencies. Examples: `financestrategists.com`,
  `medappz.com`.

- **Real estate and accommodation** (~20%): Apartment listings, assisted
  living, school finders. Examples: `apartmentadvisor.com`,
  `world-schools.com`.

- **Job boards** (~20%): Public-sector and sports-industry job listings.
  Examples: `workforgov.co.za`, `soccerjobs.io`.

- **Software comparison and pet marketplaces** (~20%): SaaS comparison
  tools, pet sale/adoption listings. Examples: `selecthub.com`,
  `petmeetly.com`.

### 6.6 Support / Knowledge Base (13 sites, 0.6%)

Self-service documentation and help hubs.

- **Product-specific help centers** (~77%): Samsung Galaxy manual,
  CloudHQ extension support, Typing.com instructional guides. Examples:
  `galaxys24manual.com`, `typingcom.helpscoutdocs.com`.

- **General technical and software tutorials** (~23%): Microsoft Word
  guides, IT support how-tos, device troubleshooting. Examples:
  `mswtutor.com`, `androidreset.org`.

### 6.7 Fringe / Other (16 sites, 0.7%)

Spam and parked content farms (6), software repositories (4), piracy
(3), adult content (1), online gaming portal (1), community UGC (1).
All very small in the LLM cohort and not analyzed in detail.

---

## 7. Key Patterns Summary

### The hierarchy

```
2,243 LLM search-result sites
│
├── Publisher / editorial (54.3%)
│   ├── ads_only (50% of editorial = 27% of all LLM sites)
│   │   Topics: how-to/listicle (16%), health (13%), recipe (10%), pets (7%)
│   ├── none_detected (34% of editorial = 18% of all LLM sites)
│   │   Same topic mix; lower traffic; many recently launched or non-monetized
│   ├── ads_and_affiliate (12% of editorial = 6% of all LLM sites)
│   │   Topic emphasis: recipe/food (24%), health (14%), general how-to (15%)
│   └── affiliate_only (3% of editorial = 1.5% of all LLM sites)
│       Mostly pet, health, home product guides
│
├── Business / service operator (18.2%)
│   ├── none_detected: pure lead-gen (48%)
│   │   Healthcare 20%, contractors 20%, professional services 18%
│   ├── ads_only: lead-gen + residual ad revenue (45%)
│   │   Same industry mix
│   └── lead_gen_only, ads+affiliate, etc. (7%)
│
├── Affiliate / SEO content (11.1%)
│   ├── ads_and_affiliate (40%)
│   │   Product reviews, lifestyle, niche hobby, food
│   ├── ads_only (27%)
│   │   Pure traffic sites, no affiliate
│   └── affiliate_only (21%)
│       Specialized gear, fashion/lifestyle, food affiliate
│
├── Retail e-commerce (6.2%)
│   ├── ads_only (52%): beauty/hair, supplements, food, specialty goods
│   └── none_detected (32%): pure product-sale retailers
│
├── Product / SaaS company (2.9%)
│   Mostly ads_only (58%); AI writing tools, productivity SaaS dominant
│
└── Other (7.3%)
    Personal (2%), tool/utility (2%), assets (1%), institutional (1%), etc.
```

### What LLM content is being used for

| Use case | Primary category | Approximate share |
| --- | --- | ---: |
| Ad-supported informational content farming | publisher\_editorial / ads\_only | ~27% |
| Pre-monetization or low-traffic informational blogs | publisher\_editorial / none\_detected | ~18% |
| SEO + service-lead generation for local/professional services | business\_service\_operator | ~18% |
| Affiliate product recommendation farming | affiliate\_seo\_content | ~11% |
| Ad+affiliate hybrid editorial | publisher\_editorial / ads\_and\_affiliate | ~6% |
| D2C e-commerce brand blogging | retail\_ecommerce | ~6% |
| SaaS marketing / product blog | product\_saas\_company | ~3% |
| Other | — | ~11% |

### What is conspicuously absent

Consistent with the paper's broader argument:

- **Newsletter/audience cultivation**: Only 15 LLM sites (0.7%) are
  classified `subscribe_or_donate`. Human sites carry this at 3.4× the LLM
  rate.
- **Premium managed ads (Raptive/AdThrive, Mediavine)**: LLM sites reach
  for AdSense/Ezoic; premium networks require traffic and content-quality
  thresholds that most LLM sites do not meet.
- **Established affiliate networks (Skimlinks)**: LLM sites vastly
  under-represent Skimlinks-managed affiliate (the institutionalized affiliate
  layer); they favor direct Amazon Associates or unmanaged affiliate links.
- **Deep lead-cultivation content marketing**: Business operators use LLM
  for shallow SEO blog posts, not the deep thought-leadership content
  (white papers, case studies, webinars) that characterizes high-ticket
  B2B buyers' journey content.

---

*Generated 2026-04-21. Source: `why_text` from `subdomain_categorizations`
(latest per site) joined with `site_full_mg` from
`data/classify/llm_site_kinds/duckdb_session/20260418_112640.duckdb`.
Analysis code: inline Python in the conversation session that produced this
doc.*
