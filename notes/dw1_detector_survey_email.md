Subject: dw1_detector_survey.md: recent detector update

Beginning of memo.

No qualifying recent detector is demonstrated as a replacement for DW1 Binoculars. I screened nineteen public papers from 2025 and 2026, checked official artifacts, and tested the strongest feasible paths on the two NVIDIA A6000 GPUs. The impressive reported numbers all fail at least one required accuracy, artifact, speed, or method constraint.

The implicit reward model, or I R M, is the only recent fully executable public control that stays in scope. Its best paper configuration beats Binoculars on three matched DetectRL tasks, but those Meta checkpoints require license acceptance. The public Qwen configuration ran more than four times faster than Binoculars locally. Its local area-under-curve score was zero point nine four four, below Binoculars at zero point nine five nine. It is a useful control, not an improved recommendation.

SV-Detect reports near-perfect in-domain results, but the authors did not release the trained steering directions or classifier. An optimized feature reconstruction fit easily on the A6000s, but that is not the released path, end-to-end detector throughput, or an accuracy reproduction. SV-Detect remains reconstruction-only evidence.

LAPD has the strongest matched zero-shot paper comparison and added only about half a percent to the same-process Binoculars batch time. However, it uses ten thousand categorical auxiliary samples, and its paper groups the method with approaches that perturb or generate auxiliary sequences. Under the strict no-multi-perturbation constraint, LAPD is excluded unless you explicitly permit that sampling.

EchoPrompt and Steer-to-Detect report impressive 2026 results, but neither has a released implementation or detector state, and their length, batch, and hardware evidence is insufficient. The previous WaveDetect recommendation is also superseded because its local area-under-curve score was only zero point eight nine one.

Keep Binoculars. A future candidate should advance only after it matches both Binoculars area-under-curve and low-false-positive behavior on the same frozen, stratified DW1 test, while retaining the measured A6000 speed boundary.

End of memo.
