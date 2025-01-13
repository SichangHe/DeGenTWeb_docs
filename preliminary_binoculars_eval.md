# Preliminary Binoculars Evaluation

- [x] dump English HTTP response from random Common Crawl WARC file
- [x] extract main text; if longer than 2000 character, feed into Binoculars
- [ ] split long page down to Falcon-7B context window 2048 token
    - currently, simply truncate
    - [ ] average score weighted on token count

script: `degentweb.common_crawl.classify_english `

result dumped to `data/common_crawl/prelim_test/`; 5961 page; used 1h 20m

## Manual inspection of 1010 page

low-score page:

- ~19 seem indeed generate article, mostly blog & product
- 3 simply table-like listing
- 7 short listing/interaction page (scoreboard, links;
    only 2 are > 2000 character)
- boilerplate text: 7 cookie banner (< 2000 character); 1 legal notice
- 1 seem false positive
    <https://catalyticconvertersolutions.com/writer/nicolas-will/>

lower-score page (above FPR-threshold but around F1-threshold):

- many also seem generated, some not
    - 1 page error message (MySQL)
    - boilerplate text (legal)

## Case studies

- short listing/interaction page
    - site search result
        <https://newsroom.courts.ca.gov/search?t=Napa&sort=created&order=desc&keywords=&facets_query=&f%5B0%5D=content:event&f%5B1%5D=event_type:132&f%5B2%5D=event_type:202>
- boilerplate text:
    - cookie banner from Trafilatura extraction issue
        - very short content
            <https://myscholarshipbaze.com/play-alphabet-earn-cet-vol-25/>;
        - non-English content
            <https://www.neske.hu/webshop/ekszerek/medalok/turkiz-levelkes-medal-nagy/>,
            <https://traczer.pl/fr/suplement_vet/>
