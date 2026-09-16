# Draft issue

This is a draft for the human to approve; it does not post an issue or alter the classifier. Exact five-site evidence is in [the advisor-requested website investigation](/ssd1/sichangheagent/work_logs/dw_advisor_sites_investigation.md).

## Title

Report AI-detector findings as findings about the webpage text tested

## Body

In our previous meeting, the advisor noted that our five-site “LLM-dominant” wording could be mistaken for a claim about an entire website. It is not. The software gives a number for the readable webpage text it can process; a more AI-like number means that wording shares patterns with the language-model comparison text used by the study. It does not show who made the whole site or whether its product is good.

The report uses two sets of pages:

- **Full scored set:** every captured page whose readable main text passed the study’s language and length checks. These page scores produce the current site label.
- **15-page reading set:** 15 pages automatically selected in a fixed, repeatable way from that full scored set. We read these pages to show examples. They do not calculate or change the site label.

Change the later evaluation to say what text was tested before describing a website. Name the page or page group, give an example, name the type of text, and say what was not tested. Use “this text resembles the study’s AI comparison text,” not “this website was made by AI.” Do not use these text scores to claim that a site is useful, valuable, or low quality.

Example completed row: **Manualzz** — tested text: 20 eligible manual-landing pages, including the webpage summary and FAQ around a downloadable Whirlpool manual; detector result: site margin +3.411, with weaker corroboration from the second detector; text type: page wrapper; narrow conclusion: that surrounding text looks AI-like; other possible explanation: a fixed template; not tested: the manual itself.

## Done when

- The five site findings say whether they concern the full scored set or a named text example.
- They keep the 15-page reading set separate from the full scored set.
- Each reviewed example states text type, another possible explanation, and the function or document not tested.

# August 25, 2026 advisor meeting plan

## Action before the meeting

The human decides whether the issue wording above is ready to post to the project tracker. Bring [the five-site evidence brief](/ssd1/sichangheagent/work_logs/dw_advisor_sites_investigation.md) plus **one single-page table with five rows**: Manualzz, FasterCapital, Brainly, E-Housing, and 1map.

For every row, include: page or page group tested; number of pages in the full scored set; current detector result; one example; text type; narrow conclusion; another possible explanation; and what the detector did not test. Use the same column definitions as the completed Manualzz row above.

## First question for the advisor

“Can we approve this rule: our detector result describes webpage text tested by the study, not the whole website, unless a separate study provides stronger authorship evidence?”

## Three follow-up decisions

1. Should the main result continue to include every page in the full scored set, while we also show a second robustness result with clearly defined wrapper/template text left out? A wrapper is page text around a document; a template is repeated, automatically filled text. The second result checks whether that defined text type changes the conclusion; it never replaces the main all-page result.
2. Before a future whole-site authorship claim, rank these evidence tasks from first to last. Each addresses a different uncertainty:
   - compare a tested page with an older archived copy, to see whether the same text was already present;
   - find author/edit information, to see who may have written or changed the text;
   - check the extraction, to see whether the software included document/tool text it should not have; or
   - test known human or fixed-template manuals, to see whether the detector wrongly calls them AI-like.

## After the meeting

The human records the claim-boundary decision and the two follow-up decisions in the meeting notes. The research team updates the five findings and the paper’s later evaluation before the next advisor review.
