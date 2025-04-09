# Baseline Websites

- assume webpage before ChatGPT (Nov 30, 2022) likely human-written
    - publication date extraction: [htmldate: A Python package to
        extract publication dates from web
        pages](https://www.theoj.org/joss-papers/joss.02439/10.21105.joss.02439.pdf),
        Adrien Barbaresi, JOSS, 2020

## Human-written

- credible source
    - Wikihow <https://www.wikihow.com/>
- personal website
    - [IndieWeb Wiki](https://indieweb.org/): registry of personal website
        - after filtering by having sitemap, most are tech blog
    - WordPress directory?
- company website
    - ~~[EDGAR database](https://www.edgarcompany.sec.gov/servlet/CompanyDBSearch?page=main)
        → company name → search for website~~ many of them do not have website
    - ~~US Business Database?~~ no website link
    - ~~LinkedIn?~~ forbit crawling
    - Russell 2000
        - many do not have blog; many are after ChatGPT; many have no sitemap
        - after filtering by having sitemap, most are tech company
        - content: most are blog/ company statement (news);
            some are service/product description; few functional page e.g. form

- find `.*/blog/.*` URL in CommonCrawl?

## Machine-generated

- self-claim generated
    - sell solution for generating article <https://eulogygenerator.com/>
    - AI search <https://www.neuralword.com/>
- clear cue (e.g., "as an AI")
    - <https://educacion-especial.com/2023/03/12/a-beginners-guide-to-home-schooling-tips-and-resources/>
    - <https://freemwiki.com/wiki/%E9%A6%96%E9%A1%B5>

## AI website generator

- [10Web](https://10web.io/) claim to generate&host website on
    name&description
    - landing page & 1-paragraph sample article
    - claim to have generated 1.5M+ websites
    - from \$13/month; need \$28/month "pro" to edit&multi-site; WordPress,
        Cloudflare CDN
        - ❌ need \$49/month for each additional website
    - ❌ extremely slow when generating, e.g., \>10min/page
- [Wix AI Website Builder](https://www.wix.com/ai-website-builder)
    - landing page & short/long blog article on demand
    - allow multiple site, sell domain&service instead of generator
    - for arbitrary page, "Generate Full Page Text" produce poor result
        - ❌ only generate 1 very short text block & no layout generation
- [ContentBot.ai](https://contentbot.ai/) automate AI-driven content creation
    - claim to be used on ABCNews, Contagious, PR Week, etc.
    - no free trial; from \$0.5/1000 word, \$29/month for full plan
- [Copy.ai](https://www.copy.ai/) go-to market AI for marketing, sales, etc.
    - claim to be used by SIEMENS, Rubrik, etc.
    - no free trial; \$49/month for starter individual plan;
        mainly target business
- [WebWave AI](https://webwave.me/ai-website-builder)
    - landing page & manually written blog
    - ❌ very slow; had bug of not publishing blog
    - from \$3.5/month; \$5/month for blog&SEO
- [B12](https://www.b12.io/)
    - landing page/ medium-length blog/ service/project description/ team
        member, on demand
        - or any page given name+description
    - from \$42/month
    - very fast generation
- [Contentful AI Content
    Generator](https://www.contentful.com/marketplace/ai-content-generator/)
    use OpenAI API to write content
- [HubSpot AI Website
    Generator](https://www.hubspot.com/products/cms/ai-website-generator)
    optimize existing company website
    - only generate landing page
- [Relume](https://www.relume.io/) only generate mockup/HTML
- [Webflow](https://webflow.com/) only generate layout
- [GoDaddy Airo](https://www.godaddy.com/en-ca/offers/airo) focus on
    marketing & selling
    - ❌ need GoDaddy domain
- [Dorik AI](https://dorik.com/)
    - ❌ need \$39/month for unlimited \#page, else limit to 5 (free) or
        25 (\$18/month) per site
- [Vzy](https://vzy.co/)
    - \$10/month/site for 100 page
- Wegic, Tilda, Shopify Magic?

### Provided example generated sites

- hand-picked; probably not purely generated
- some not text-heavy (mainly image, etc.)
- commonly business w/ `/blog`; unlike most content farm found

each generator:

- 10Web
    <https://help.10web.io/hc/en-us/articles/360031026572-Can-You-Provide-Examples-of-Websites-Hosted-on-10Web>
    - seem not purely generated
- Wix <https://www.wix.com/blog/wix-artificial-design-intelligence> Examples
    of sites created with Wix’s ADI-powered website builder
    - most down
- B12
    <https://www.commoninja.com/blog/b12-ai-website-builder#Examples-of-Websites-Designed-with-B12%23Examples-of-Websites-Designed-with-B12>

### Website generator capability

- [Examining the Accessibility of Generative AI Website Builder Tools for
    Blind and Low Vision Users: 21 Best Practices for Designers and
    Developers](https://ieeexplore.ieee.org/abstract/document/10609588),
    Sushil K. Oswal, Hitender K. Oswal, ProComm, 2024
    - dorik.com, relume.io, wix.com capability
        - generate landing page, sitemap, wireframe on description
        - customize layout, style
        - generate text&image w/ prompt
- most tutorial/comparison only showcase landing page generation
- product description/ event description/ tech doc/ blog
- marketing email/ social media post/ SEO
- not content: AI chat support, analytics report
- not AI functionality
    - boilerplate page: FAQ/ privacy policy/ terms of service/ 404
    - selling product/service/ booking/ form

## What category to cover

- can only cover what AI website generator can generate

covering:

- personal/company/organization blog

want:

- personal/team project description
- news
- products
