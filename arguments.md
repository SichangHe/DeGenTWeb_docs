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

## Content farm

- moral issue: some site like GeeksforGeeks look like content farm but
    may be useful; what is our stance?
