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

## Segmentation for generalization

Instead of only filtering out what we cannot handle (non-article),
we can also try to generalize our method to *all* webpages.

If we could split a webpage into sections, we could apply Binoculars to
each section.
For example, we could segment a homepage full of links into each of
the links it contains, and subsequently filter them out based on length;
we could segment a forum page into each comment.

Importantly, we need to segment after main text extraction with Trafilatura.

### Webpage segmentation (WPS) tool

- [Web page segmentation with structured prediction and its application in
    web page
    classification](https://dl.acm.org/doi/abs/10.1145/2600428.2609630),
    Lidong Bing, Rui Guo, Wai Lam, Zheng-Yu Niu, Haifeng Wang, SIGIR, 2014
    - too old
- [Box clustering segmentation: A new method for vision-based web page
    preprocessing](https://www.sciencedirect.com/science/article/pii/S0306457316301169),
    Jan Zeleny, Radek Burget, Jaroslav Zendulka,
    Information Processing Management, Elsevier, 2017
    - vision-based
    - no code
- [Multimodal Web Page Segmentation Using Self-organized Multi-objective
    Clustering](https://dl.acm.org/doi/abs/10.1145/3480966),
    Srivatsa Ramesh Jayashree, Gaël Dias, Judith Jeyafreeda Andrew,
    Sriparna Saha, Fabrice Maurel, Stéphane Ferrari, TOIS, 2022
    - MCS: automatically choose \#segment using K-means
    - no code?
