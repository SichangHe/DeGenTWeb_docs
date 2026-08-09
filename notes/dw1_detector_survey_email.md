Subject: Correction: dw1_detector_survey.md evidence

Beginning of memo.

I need to correct my earlier detector summary. It missed MELD, a public detector
released in May 2026 with unusually strong accuracy claims. The corrected result
is more promising, but it still does not support replacing DW1 Binoculars today.

MELD's paper reports 99.85 percent area under the receiver operating
characteristic curve on clean RAID data, versus 84.40 percent for Binoculars. At
a one-percent false-positive rate, its reported true-positive rate is 99.40
percent, versus 69.54 percent for Binoculars. MELD was trained on RAID data, so
this is a shared test-set comparison, not an equal training comparison.

The public artifact has a critical version gap. The paper-era checkpoint depends
on companion code that is no longer anonymously available. The current runnable
version says it replaced the earlier checkpoints and that their scores are not
comparable. I therefore cannot assign the paper's accuracy to the version I
tested.

The current version fits easily on the two NVIDIA A6000 graphics processors. At
2,048 tokens and batch eight, two concurrent replicas processed a batch in about
zero point six three seconds, compared with about seven point seven three seconds
for DW1 Binoculars under the same scoring boundary. On the available
length-eligible DW1 screen, however, MELD's area-under-curve score was zero point
nine five five. Stored Binoculars scored zero point nine seven eight, and stored
FastDetectGPT scored zero point nine six nine.

MELD's locally calibrated low-false-positive recall was promising, but its
shipped one-percent threshold produced about eight point six percent false
positives on separate local human texts. The corpus was not a new frozen,
stratified evaluation, and the comparator scores were historical. Those gaps make
MELD the first candidate for a proper follow-up, not a deployment recommendation.

I also checked other omitted recent releases. DACTYL has a public ModernBERT
checkpoint and strong 2026 challenge results, but no matching Binoculars
low-false-positive or A6000 comparison. The International Conference on Learning
Representations Markov calibration code needs a new supervised state.
Exons-Detect has strong paper results, but its essential generated replacement
sequence violates the no-regeneration constraint.

The row-by-row audit also found two high claims that the earlier correction had
still grouped too loosely. LM squared motifs beats Binoculars in an in-domain
table, but trails it in the paper's cross-domain average, uses nearest-neighbor
lookup, and no public detector release was found. NEULIF reports ninety-nine
point five percent area under the curve for a small classifier, but only on one
in-domain Kaggle split. No public model was found, and the paper supplies no
matched Binoculars result, generator provenance, or reproducible timing. Neither
qualifies under the fixed screen.

The expanded audit also preserved seven other strong shared-task or small-test
claims. Their results include perfect F one on one shared task and ninety-eight
point three percent accuracy on a sixty-text test. The three public source
releases do not include trained checkpoints, and none reports a matched
low-false-positive and speed comparison. They do not change the recommendation.

A broader audit first found that overview, benchmark, and shared-task papers hid
named systems. The final repair then read the full text and result tables of all
one hundred nineteen frozen papers, including ordinary detector papers whose
titles did not signal a comparison. A fresh adversarial mutation found that the
first table inventory still omitted named configurations in papers it had
labeled as non-candidates. The corrected ledger now accounts separately for
eight hundred five qualifying detector accounts: two hundred forty-one
previously expanded systems and five hundred sixty-four primary-paper
configurations. No single parent-level account remains. Six papers have a
table-specific reason that no result qualifies. High validation or narrow
scores remain beside weak official, transfer, attack, or cross-domain results.

This pass recovered all three M-DAIGT systems, nine classical-classifier feature
combinations, eight DeBERTa training and ensemble states, three Defactify
systems, all nine Chinese encoder and LoRA states in paper 2509.00731, eight
SenFlow-related states, five semantic-similarity DeBERTa stages, and both
LuxVeri inverse-perplexity ensembles. It also recovered ten narrow-domain TELL
comparators, five late-stage stability baselines, and the ReMoDetect and ImBD
rows reported inside the LAPD paper. The result-specific pass also stopped
DNA-DetectLLM's regeneration blocker from being applied to its ordinary
baselines. It corrected DP-Net in the other direction: its noise is added only
during training, so the two states are evidence-rejected rather than excluded
as inference perturbation pipelines. Their best seven-domain average accuracy
is eighty-six point one percent, with no frozen state or fixed low-false-positive
and A6000 evidence. It also corrected one mechanism: Leidos
version one point zero point four is the paper's unweighted multiclass
DistilRoBERTa classifier, not an ensemble. None of the recovered configurations
adds the matched low-false-positive, public artifact, two-A6000, and
near-Binoculars evidence needed to change the recommendation.

Three complete public checkpoints warranted direct testing. DetectRL-X and
ModernBERT were fast but substantially less accurate than the stored controls.
Desklib was also fast. Its area-under-curve score was zero point nine seven five,
just below Binoculars at zero point nine seven eight. At a locally calibrated
one-percent false-positive rate, Desklib detected about eighty-nine point six
percent of generated texts, versus about sixty-six point one percent for stored
Binoculars. That tail result is promising, but the corpus was not frozen, the
comparators were historical, and Desklib used a shorter input limit. It is a
runnable follow-up, not a replacement recommendation.

For now, keep Binoculars. Before reconsidering MELD, resolve the checkpoint used
for the paper and run MELD, Desklib, Binoculars, and FastDetectGPT together on one
frozen, stratified, current-generator test with separate human calibration.

End of memo.
