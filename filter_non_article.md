# Filter out Non-Article

Binoculars, and presumably other generated text detectors,
can only perform well when detecting articles such as blog posts.
Non-articles, include lists of links on a homepage, login pages, dashboards of
sports scores, and spec charts of products,
may cause high false positive rates.

Current method to filter out non-articles:

- use how-to search results.
    most of them are articles and forum threads, except for
    occasional product sales page
- discard pages w/ \< 200 tokens

Ideas for filtering:

- discard pages based on HTML structure
    - but HTML structure is extremely flexible and
        behave differently based on CSS
    - perhaps study how Trafilatura filter out non-main-body text
- feed extracted text to classifier
    - BERT-based classifier for article/non-article
- word count on extracted text to see if consist of paragraph

Unreliable ideas:

- filter by `og:type` = `article`.
    unreliable because not every article has this tag and
    content farm may have this tag be `website`
