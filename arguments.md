# Arguments

(citation in Quarto format w/ `reference.bib` for future writing)

## Significance

- The Web is the largest public corpus of knowledge for human consumption and
    machine learning training
- AI-generated text usually plagiarize prior content,
    often hallucinate misinformation, so it pollutes contents on the Web.
- Spammy content affects search engine user experience by
    disrupting search engine ranking
    - Users want accountable, reliable, and informative content, but
        AI-generated contents are often not so.
    - [Arguments from
        Perplexity.ai](https://www.perplexity.ai/hub/faq/how-does-perplexity-work):
        LLMs may have stale information, and do not cite their sources for
        verification purposes.
- Generated contents in training data may harm LLM performance
- Generated contents in RAG data may harm LLM search performance
- Laws like the [EU AI
    Act](https://www.europarl.europa.eu/topics/en/article/20230601STO93804/eu-ai-act-first-regulation-on-artificial-intelligence)
    mandate disclosure of AI-generated content, but
    many AI content websites do not comply and thus may be illegal.

## Crawling

- trying to see webpage users see although scraper see different results,
    search result differ based on location
- main body text extraction is difficult to do well, but
    we do best-effort w/ SoTA method
    - Trafilatura [@barbaresi2021trafilatura]
        is SoTA [@bevendorff2023empirical; @reeve2024evaluation]

## Generated text detection

- Binoculars score reflect information density (substance)
    - is calibrated perplexity
    - generated text is bad because provide less actual information
    - detect both generated and low-quality content
- statistical probability may give more info than
    binary classification using fixed threshold
- detection of individual webpage may yield error, but
    aggregate analysis per website should increase accuracy
- although NLP benchmarks evaluated individual detectors on texts,
    they do not reflect the results from our aggregate website analysis, so
    we need to run our pipeline over baseline websites
- when multiple detectors exhibit the same trend, the trend is evident

## Content farm

- moral issue: some site like GeeksforGeeks look like content farm but
    may be useful; what is our stance?

## Generalizing to non-article webpages

Text-based LLM detection cannot generalize to all webpages.
Types of webpages from the viewpoint of such detection (enumeration based on
Deepseek):

- **Single or cohesive narrative/text blocks.** Blog Posts, News Articles,
    Research Publications, Tutorials/Guides, E-books/Whitepapers,
    Podcast Transcripts, Recipes, Interactive Stories, Archived Content.

    👌 These can be treated as a single block of text and directly classified.

- **Multi-Section Text Pages.** Homepage, FAQ, Glossary,
    Forum (boards/posts), Directory, Wiki/Knowledge Base, Portfolio,
    Testimonials, Case Studies, Team Directory, Event Listings, Press Releases,
    User Profiles, Social Feeds, Q&A Platforms.

    😰 These, when treated as a single block of text, causes discontinuity in
    the text and degrade text detection performance.
    Segmenting them and classifying each segment separately may work.

- **Boilerplate/Legal/Standardized Content.** Privacy Policy, Terms of
    Service, Disclaimer, Product Pages (descriptions), Download Pages,
    Account Settings, Pricing Pages, Services Pages, Career Listings,
    API Documentation, Client Dashboards, Affiliate Pages.

    🤷 These have standardized forms, such that humans would write them in
    a similar way that LLMs do, so detection makes little sense.

- **Media/Non-Text Pages.** Image Galleries, Video Pages, Audio Streams,
    3D/Virtual Tours.

    ❌ Text detection is not applicable to these.

- **Interactive/Functional Interfaces.** Dashboards, Quizzes/Surveys,
    Calendars, Booking/Checkout Pages, Login/Registration Forms,
    Search Results, Advanced Filters, Live Chat, Calculators/Converters, Games,
    AR/VR Interfaces.
    Stock Tickers, Weather Forecasts, Order Tracking, Live Streams/Webinars,
    Auction/Bidding Pages, Real Estate Listings, Job Boards.
    Comparison Tools, Financial Calculators, Medical/Appointment Systems,
    Code Playgrounds, Maps.

    ❌ These are not really text-centric content, so
    text detection is not applicable.
