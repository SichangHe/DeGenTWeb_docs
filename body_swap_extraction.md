# BodySwap extraction behavior and decision
(authored by agents unless marked 🧑)

BodySwap can replace the originally extracted post on a page containing
multiple posts, while subsequent extraction selects another, untouched post.
The October 6, 2026 investigation recorded this behavior. The human decided
to preserve extraction failures rather than force extraction to return the
injected body, and to document the details here rather than in the paper.

## Recorded evidence

The prior investigator wrote in “Re: [dw_bodyswap_text_check] BodySwap English
text extraction check”, preserved in
`/ssd1/sichangheagent/work_logs/human_deferred_reading.md` under that subject
(the explanation beginning “WTF? Why do we have swap sites pages that are
untouched human texts?”):

> Because the source page holds many posts, the swap replaces only the one the extractor returned, and after the swap the extractor returns a different, untouched post. Nothing checks for this.

The same explanation records the construction and acceptance behavior:

> 3. The swap replaced exactly that part with LLM text. This step worked: on 494 of the 522 pages, at most 5% of the originally extracted text is left on the swapped page.
> 4. The other posts on the page stayed, as designed: the swap keeps everything outside the extracted part.
> 5. On the swapped page, the extractor no longer picks the replaced part. It picks other posts. On 516 of the 522 pages the scored text shares almost no 5-word phrase with the originally extracted text, so it is human text we never scored on the original page either.
> 6. The acceptance filter only tests language, 200 tokens, Dolma and duplication. It never compares the scored text with the LLM text, so these pages passed.

The investigation's earlier report gives the size and scope of its findings:

> That is 2.6% of the 20,412 qualified pages, on 262 sites. On these pages more than half of the scored words do not appear in the generated body. For 515 of the 522, over 80% of the scored words are found in the old 2014 page around the generated body.

> I could not check 273 other qualified pages: they come from the older and the recovery runs, which do not save the generated body in the same place.

These are the prior investigator's recorded measurements, not a new replay.
Word or phrase overlap measures similarity; it does not by itself establish
the authorship of every word. In `origin.py`, the original-text comparisons
count overlapping five-word spans, despite the explanation's use of “text”
and “words”; `origin.json` stores their shares rounded to two decimal places.

The saved evidence is under
[`data/classify/dw_bodyswap_text_check_20261006/`](../data/classify/dw_bodyswap_text_check_20261006/):

- `report.md`: original findings and investigation limits
- `qualified_pages_mostly_old_text.csv`: the 522 flagged page identities,
  word counts, overlap shares, and starts of scored text
- `origin.json` and `origin.py`: source-text overlap evidence and its analysis
- `purity.py`, `cover.py`, and `verify.py`: generated-body and extraction checks

The replacement pipeline is indexed in
[`codebase_index/body_swap_ood.md`](../codebase_index/body_swap_ood.md).
Its removal of duplicate copies of the originally extracted body is distinct
from deleting unrelated posts until extraction matches the injected body.

## Unconfirmed cause and effect

The investigator explicitly left the reason for switching posts unresolved:

> What I do not know: why the extractor switches posts. One clue: on these pages the LLM body is short, median 329 words against 506 on normal pages, while the human posts it picked instead have a median of about 630 words. I have not confirmed that length is the cause.

The effect on classifier error rates was not measured by rerunning without
the flagged pages. The earlier recommendation to remove them was an agent
proposal, not an approved change.

## 🧑 Human decision

The human's reply in
`/ssd1/sichangheagent/work_logs/manager_mail/85c5dff58359-2645.txt`,
subject “Re: [dw_bodyswap_text_check] BodySwap English text extraction check”,
states:

> It sounds like what's wrong was that we needed to check if the extracted text is similar to the body we injected. And then if the extracted body does not match what we injected. We should delete that element and we should do this in a loop until we get almost what we injected back. However, I am against doing that because we may test our ability to handle boilerplate, for example, by sometimes having extraction being wrong. In the wild extraction is wrong all the time. I guess we don't need to mention these in the paper and just need to document it in the doc tree of the cold repo.

The decision rejects that deletion loop because extraction errors can be part
of testing the handling of boilerplate. This documentation update changes
neither the extraction pipeline nor the dataset and adds nothing to the paper.
