Subject: dw1_detector_survey.md: detector shortlist

Below is the recommendation memo for dw1_detector_survey.md.

I found one new method worth advancing to a bounded DW1 evaluation: WaveDetect. I preserved the exact constraint of two NVIDIA A6000 GPUs and did not assign a numerical meaning to “not much slower than Binoculars.” I excluded retrieval, RAG, rewriting, regeneration, and multi-perturbation methods.

The official public WaveDetect checkpoint ran on one A6000 at batch eight and two thousand forty-eight tokens. It used about fifteen point one gibibytes of allocated GPU memory and took about zero point zero three nine seconds of scoring time per document. The controlled DW1 Binoculars run used both A6000s, about thirty-four point three gibibytes on each, and took about zero point nine seven seconds per document under the same timing boundary. On a fixed one-thousand-document DW1 triage screen, WaveDetect at one thousand twenty-four tokens reached zero point eight nine one AUROC. Stored historical Binoculars and FastDetectGPT scores on the same rows reached zero point nine five nine and zero point nine five four, but their software and truncation basis may differ. This makes WaveDetect a viable fast pilot, not an accuracy-equivalent replacement or a controlled accuracy win.

DetectLLM-LRR also passed the direct hardware and speed screen, and DW1 already computes it. Its local AUROC was only zero point seven nine nine, so I recommend keeping it as a cheap baseline or ensemble feature, not replacing Binoculars with it. Base SpecDetect was slightly faster than Binoculars in the controlled test and is the next-best formula to investigate, but its official initial code release has concrete runtime defects and no DW1 accuracy or threshold evidence.

Lastde and PAWN fit the reported memory envelope, but neither has the required like-for-like speed evidence at DW1 length and batch settings. DetectAnyLLM is excluded because it searches retained human and generated reference sets at detection time. RADAR and OpenAI RoBERTa are inexpensive but performed too poorly on the existing DW1 scores. I did not call any of these viable.

Before adoption, WaveDetect needs a held-out, stratified DW1 evaluation, low-false-positive calibration on separate human data, recent-generator and attack coverage, and sustained service-throughput testing. I made no DW1 implementation or configuration changes.

Secondary references for reading follow. The durable study is at docs slash notes slash dw1 underscore detector underscore survey dot markdown. The controlled results are in its companion source directory, in benchmark underscore results dot text and benchmark underscore wavedetect underscore results dot text. The primary sources are the [WaveDetect paper](https://aclanthology.org/2026.findings-acl.424/), the [DetectLLM paper](https://aclanthology.org/2023.findings-emnlp.827/), the [SpecDetect paper](https://ojs.aaai.org/index.php/AAAI/article/view/40510), the [Binoculars paper](https://proceedings.mlr.press/v235/hans24a.html), and the [FastDetectGPT paper](https://openreview.net/forum?id=Bpcgcr8E8Z).

Above was the recommendation memo for dw1_detector_survey.md.
