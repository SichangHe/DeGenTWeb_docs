# Pangram false-positive-rate samples

(authored by agents unless marked 🧑)

status

- 605 2014 Common Crawl negative pages sampled to match the 605 already-scored generated Pangram pages
- five sealed source-1093 pages plus 600 source-1249 pages, 200-word floor, training-baseline overlap 0
- index: `.runtime/pangram-fpr/negative-605.jsonl`
- trial credits used up; dashboard 0 left
- 🧑 no paid Pangram signup by the agent; human opened the trial

results

- 605 2014 negatives sized to the generated-page count: all Human, 0 AI, 0 Mixed
- 73 later 2014 pages scored with leftover trial credits: all Human
- 678 scored 2014 pages total: 0 AI-or-Mixed calls under Pangram's Human/AI/Mixed label
- capture date does not prove individual human authorship, so this is not a proven-human false-positive rate
- reserved ranks 170 and 432 had no captured label on the first try; both scored Human on retry
- 67 later unused generated body-swap pages, all AI
- earlier Claude body-swap cohort: 780 pages, 768 AI, 9 Human, 3 Mixed
- freeze roots: `.runtime/pangram-fpr/frozen-negatives-605`, `frozen-even-2102`, `frozen-leftover-12`, `frozen-leftover-3`

negative class

- 🧑 "five independently sealed pre-ChatGPT Common Crawl human sites"
  - from `source1093_pangram_research_quota_draft.md`
- freezer limitation, quoted from the sealed population:
  - "Capture date does not prove individual human authorship and cannot exclude older automated or templated text generation."
- not these
  - already-scored generated Claude body-swap pages
  - Wix or B12 generated sites
  - the old 144-site baseline
  - SVM pre-ChatGPT false-positive sites

points to test

- site `stacygail.blogspot.com`
  - page `old-cc-2014/01a53e05170c732b387b15ca020b8b94562d2392e915ace538e1d3d762d97b5f`
  - url `http://stacygail.blogspot.com/2011/07/titles-or-lack-thereof-blurb-and.html`
  - capture `2014-10-24`
  - 594 words
- site `taniakindersley.blogspot.com`
  - page `old-cc-2014/030375347e38001fdd80c25ab8d1a80896b96d31de49877bfdb61776d0a712ae`
  - url `http://taniakindersley.blogspot.com/2014/03/an-ordinary-monday.html?showComment=1393864923005`
  - capture `2014-10-31`
  - 590 words
- site `edtechdunny.blogspot.com.au`
  - page `old-cc-2014/2a7c8ca701c40e99fd18faf419d33588f4ba74254588f4427e08b743f8896927`
  - url `http://edtechdunny.blogspot.com.au/2012/11/launching-virtual-book-club.html`
  - capture `2014-11-01`
  - 625 words
- site `andrewhutchinson.com.au`
  - page `old-cc-2014/2e8748bd82a72c1d9c4ce621df4a09836be780dc4c3bf69a01b1bcae8846177f`
  - url `http://andrewhutchinson.com.au/2014/07/28/on-finding-your-literary-voice/`
  - capture `2014-10-21`
  - 1312 words
- site `meloukhia.net`
  - page `old-cc-2014/d783b91321c83c7127e309778bd3b0b9816f97864aa697bb056ab1cdb57f46ab`
  - url `http://meloukhia.net/2013/12/who_we_were_then_who_we_are_now/`
  - capture `2014-10-23`
  - 917 words

payloads

- bodies under `src/degentweb/agent/data/source1093_body_swap_receipts/source1093-human-negative-002/bodies/`
- population `source1093-old-cc-2014-body-swap-001`
- one page per site; the "at most 30 clean article bodies" cap cannot be filled from this freezer
- first-2,048-token truncation is not stored yet
- local whitespace units sum to 43; only Pangram can bill

browser

- proxied personal-browser stack on display `:83`, noVNC `6083`, CDP `9283`
- AWS SOCKS on `18183`; tag `degentweb-pangram-aws-proxy`
- view: `ssh -L 6083:127.0.0.1:6083 USER@SERVER` then `http://localhost:6083/vnc.html`
- Chrome starts blank; Pangram signup is for the human
