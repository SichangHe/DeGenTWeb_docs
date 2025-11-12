# Filter out Non-Article

Binoculars, and presumably other generated text detectors,
can only perform well when detecting articles such as blog posts.
Non-articles, include lists of links on a homepage, login pages, dashboards of
sports scores, and spec charts of products,
may cause high false positive rates.

Current method to filter out non-articles (`visit_subdomains.py`):

- use how-to search results.
    most of them are articles and forum threads, except for
    occasional product sales page
- discard pages w/ \< 200 tokens
- discard pages w/ \> 20% text in link/code
    - Trafilatura sometimes extract wrong thing
        - extract many link following main text, e.g.
            <https://entrance-exam.net/annamalai-university-pg-diploma-in-automobile-maintenance-auto-garage-management-papers/>
        - extract only code block, e.g.
            for <https://plaid.com/institutions/mos/>
    - ⇒ try Trafilatura w/ `favor_precision` instead of `favor_recall` if
        too much text in link/code
- discard pages w/o any "block" \> 250 characters long
    - blocks are separated by newline, line break, separator; boundaries of
        block elements: header, paragraph, div, body, table cell, list item,
        code, quote
    - likely not consist of paragraph
- discard pages w/ \< 75% text in "large blocks"
    - large block need ≥200 characters
- discard pages w/ \> 20% text in list/table
    - do not count long list item/ table cell: need ≤ 100 characters long
- discard pages w/ \> 50% text duplicated relative to previous pages of
    the same subdomain
    - calculate %duplication based on byte chunks from
        Rabin fingerprint content-defined chunking (CDC)
        - 32 byte window, 96 byte target block size (1/64 probability for
            splitting)

Method used by DOLMa dataset:

- C4 nopunc: remove paragraphs not ending in punctuation
- Gopher rules
    - fraction of characters in most common n-gram greater than threshold
        - bigram > 0.20
        - trigram > 0.18
        - 4-gram > 0.16
    - fraction of characters in duplicate n-grams greater than threshold
    - fewer than 50 or more than 100 000 words
    - median word length < 3 or > 10
    - symbol / word ratio > 0.10
    - fraction of words with alphabetic characters < 0.80
    - contains fewer than 2 required words
    - fraction of lines starting with bullet > 0.90
    - fraction of lines ending with ellipsis > 0.30
    - fraction of duplicated lines > 0.30
    - fraction of characters in duplicated lines > 0.30
    - more than half of lines not ending with . ? ! "
    - contains token or token sequence repeated > 100 times

Ideas for filtering:

- discard pages based on HTML structure
    - but HTML structure is extremely flexible and
        behave differently based on CSS
    - perhaps study how Trafilatura filter out non-main-body text
- feed extracted text to classifier
    - BERT-based classifier for article/non-article

Unreliable ideas:

- filter by `og:type` = `article`.
    unreliable because not every article has this tag and
    content farm may have this tag be `website`

## Deduplication

- [Finding Similar Files in a Large File
    System](https://www.usenix.org/legacy/publications/library/proceedings/sf94/full_papers/manber.finding),
    Udi Manber, USENIX Winter, 1994
    - use Rabin fingerprint (polynomial fingerprint) to
        randomly determine "anchor" for chunking
        - polynomial fingerprint bc can efficiently compute next n-byte hash
            after shifting 1 byte
    - find identical chunks
- Simhash

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
    - webpage class: index, image, forum, product, research result, blog,
        download, news, video, other
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
- [Web Page Segmentation Revisited: Evaluation Framework and
    Dataset](https://dl.acm.org/doi/abs/10.1145/3340531.3412782),
    Johannes Kiesel, Florian Kneist, Lars Meyer, Kristof Komlossy, Benno Stein,
    Martin Potthast, CIKM, 2020
    - ⭐ Webis-WebSeg-20 dataset for WPS benchmark
- [WebSAM-Adapter: Adapting Segment Anything Model for Web Page
    Segmentation](https://github.com/pennmlr/WebSAM-Adapter/blob/main/WebSAM-Adapter.pdf),
    Bowen Ren, Zefeng Qian, Yuchen Sun, Chao Gao, Chongyang Zhang, Advances in
    Information Retrieval, Springer ECIR, 2024
    - segment any model vision-based SoTA webpage segmentation
    - use Webis-WebSeg-20 dataset for eval
    - did not cite Multimodal Web Page Segmentation
- [A DOM-structural cohesion analysis approach for segmentation of
    modern web
    pages](https://link.springer.com/article/10.1007/s11280-025-01333-3),
    Hieu Huynh, Quoc-Tri Le, Vu Nguyen, Tien Nguyen, Springer World Wide Web,
    2025
    - use DOM structure analysis
    - use Webis-WebSeg-20 dataset for eval
    - did not cite WebSAM-Adapter
