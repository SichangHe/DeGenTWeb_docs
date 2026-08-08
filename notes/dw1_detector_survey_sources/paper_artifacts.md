# Preserved primary paper artifacts

The following PDFs are retained in the established external paper collection.
Hashes are SHA-256. Long author-bearing filenames follow the existing collection
convention.

- Binoculars: `Spotting LLMs With Binoculars- Zero-Shot Detection of
  Machine-Generated Text, Abhimanyu Hans, Avi Schwarzschild, Valeriia
  Cherepanova, Hamid Kazemi, Aniruddha Saha, Micah Goldblum, Jonas Geiping, Tom
  Goldstein, ICML, 2024.pdf`; SHA-256
  `ac5915c5b2bd275da288e439cb2047213a09e59e94ec451faf8e027bd709f404`.
- FastDetectGPT: `Fast-DetectGPT- Efficient Zero-Shot Detection of
  Machine-Generated Text via Conditional Probability Curvature, Guangsheng Bao,
  Yanbin Zhao, Zhiyang Teng, Linyi Yang, Yue Zhang, ICLR, 2024.pdf`; SHA-256
  `4cb2f768f8b815cdce2bf2ceba61722d015cd6b7644ca147177270f5e6a42415`.
- DetectLLM: `DetectLLM- Leveraging Log Rank Information for Zero-Shot Detection
  of Machine-Generated Text, Jinyan Su, Terry Yue Zhuo, Di Wang, Preslav Nakov,
  arXiv, 2023.pdf`; SHA-256
  `8236109913f1e9bbb3c8fa6f8df998cedb8a9f39eb494a9380c4153a9c028466`.
- Lastde: `Training-free LLM-generated Text Detection by Mining Token Probability
  Sequences, Yihuai Xu, Yongwei Wang, Yifei Bi, et al., ICLR, 2025.pdf`; SHA-256
  `b775fb10c5dfae152552107b5b283a85cf175195191c47932c3fec39702a1cdb`.
- SpecDetect: `SpecDetect- Simple, Fast, and Training-Free Detection of
  LLM-Generated Text via Spectral Analysis, Haitong Luo, Weiyao Zhang, Suhang
  Wang, et al., AAAI, 2026.pdf`; SHA-256
  `0909a40e83540372defe5dce9bc54240054e2ec71400405ab884758956e99c66`.
- WaveDetect: `WaveDetect- Robust Framework for Machine-Generated Text Detection
  via Wavelet Transform, Zhichen Liu, Kaitong Qin, Linhan He, Yang Xu, ACL
  Findings, 2026.pdf`; SHA-256
  `e86bd0986fd30a7c7bfc5532a30178515d185f3b92e221b16635ec9052bb12d2`.
- PAWN: `Not all tokens are created equal- Perplexity Attention Weighted Networks
  for AI generated text detection, Pablo Miralles-González, Javier Huertas-Tato,
  Alejandro Martín, David Camacho, arXiv, 2025.pdf`; SHA-256
  `ff91c1168e705d1111d0ce32f5c12ac80461eb9c5dd2b64c96befd4738e8f50a`.
- DetectAnyLLM: `DetectAnyLLM- Towards Generalizable and Robust Detection of
  Machine-Generated Text Across Domains and Models, Jiachen Fu, Chun-Le Guo,
  Chongyi Li, ACM MM, 2025.pdf`; SHA-256
  `4cdeb806579c5f6e4053a746e380d7c67890cde939ddea828a32fe83b9e09877`.
- FourierGPT: `FourierGPT- Detecting Subtle Differences between Human and Model
  Languages Using Spectrum of Relative Likelihood, Yang Xu, Yu Wang, Hao An,
  Zhichen Liu, Yongyuan Li, EMNLP, 2024.pdf`; SHA-256
  `b6bb36ee3e0750722d6a80e8e7a21ef58f72af468f2a1604d3a0a66fb0f9fc11`.
- RADAR: `RADAR- Robust AI-Text Detection via Adversarial Learning, Xiaomeng Hu,
  Pin-Yu Chen, Tsung-Yi Ho, NeurIPS, 2023.pdf`; SHA-256
  `e84b2fc44bd9915c4d592cc2a038495fa7c89da8b2c6b8ed51d9a46ff37fbfb7`.
- RAID: `RAID- A Shared Benchmark for Robust Evaluation of Machine-Generated Text
  Detectors, Liam Dugan, Alyssa Hwang, Filip Trhlik, Josh Magnus Ludan, Andrew
  Zhu, Hainiu Xu, Daphne Ippolito, Chris Callison-Burch, ACL, 2024.pdf`; SHA-256
  `291b3e73ebc087dfd432789fcc2f9b55f97b174aea6092d2f5999501182b806c`.

The public WaveDetect artifact was downloaded without credentials into an
ephemeral snapshot and executed there. Its checkpoint, `wavedetect_all.bin`, is
1,010,614,711 bytes and has SHA-256
`68d100bfa9f7a9081627b55e988963bd230628f8cc62e1913ef85d44fdbab096`.
Its official loader has SHA-256
`c78d135864ee3a6a4699e609c735e6cf85de19f0870b8882983b5be1cf6828be`.
The temporary download is reproducible from the immutable Hugging Face revision
recorded in `search_log.md`; the durable benchmark records both hashes.

## Accuracy-first follow-up artifacts, 2026-08-08

The following additional primary PDFs were retained in the same external paper
collection. Each entry gives the public arXiv identifier, exact collection
filename, and SHA-256.

- 2608.05741: `Once a Response, Always a Response- Detecting LLM-generated Text
  via Latent Prompt Restoration, Hongrui Bao et al., arXiv, 2026.pdf`;
  `8c1153cd3ad45560456236c309089481cc794a96e0d57a35d1244a37426fba00`.
- 2608.01046: `DeBERTa-Sentinel- Toward Transparent and Trustworthy Detection of
  AI-Generated Text, Muhammad Yousaf Rehman, Muhammad Islam, arXiv, 2026.pdf`;
  `5eac5dbc2876863413a0e16d4c308adce57903de65dc7bb5e125d3af27c6a850`.
- 2607.22026: `DWT-Fusion- A Signal-Based Framework for Training-Free
  LLM-Generated Text Detection, Mehmet Batuhan Ozdas, Murat Osmanoglu, arXiv,
  2026.pdf`;
  `ed489430b1093e3f9118c7ee63a7607900274ac71c1fca695a401cc864ab6bd6`.
- 2607.14967: `Latent Trajectory Discrimination for AI-Generated Text Detection,
  Gianluca Bonifazi et al., arXiv, 2026.pdf`;
  `e55aad9c55f4b35c89a44b329b32ab84fe4e3d91c2d5ab60090f010fb2ec5ae1`.
- 2607.03680: `Rethinking AI-Generated Text Detection- A Strong Baseline and the
  Distribution-Shift Problem That Remains, Zhuoer Shen et al., arXiv, 2026.pdf`;
  `94ae79a9fae11a16e84352b483c02fccd9dcfe670dc329b8796c1ee680d66cc2`.
- 2606.31074: `Triospect- A Three-Dimensional Framework for Robust Statistical
  AI-Generated Text Detection Against Diverse Attacks, Guangsheng Bao et al.,
  arXiv, 2026.pdf`;
  `421bba6e4fb73f25140e0b25eea89662007d1ea0e16bdd9496b581787dd9fc88`.
- 2606.07313: `SV-Detect- AI-generated Text Detection with Steering Vectors,
  Mikhail Vishnyakov, Tatiana Gaintseva, arXiv, 2026.pdf`;
  `e954de41cee6325d644f01d0f3249205a1af84455ed2a77c9b4b2e710509ffe4`.
- 2606.02158: `On the Salience of Low-Probability Tokens for AI-Generated Text
  Detection- A Multiscale Uncertainty Perspective, Yikai Guo et al., ICML,
  2026.pdf`;
  `88f56026bead9c967c88acc15d8a2eaedbb72ce93b3ddb163fa7f831c8be0962`.
- 2605.23190: `Hidden Human-Like Nature of Machine-Generated Texts- Theory and
  Detection Enhancement, Chenwang Wu et al., arXiv, 2026.pdf`;
  `88ba4b4aa22a6cb79ef3566c5dd85f5a172386ec22049b4809b5261ee982a8ac`.
- 2605.16107: `Multi-Level Contextual Token Relation Modeling for
  Machine-Generated Text Detection, Chenwang Wu et al., arXiv, 2026.pdf`;
  `9168190e61f316a3cf8d90da4954e411cc0f1d29c55d9267c8bb03fdfae5ae39`.
- 2605.12890: `Steer-to-Detect- Probing Hidden Representations for Detection of
  LLM-Generated Texts, Luxu Liang, Xiang Li, arXiv, 2026.pdf`;
  `c3bbcc1773f06ff2c8bf0ba954bb3580eb62dba10015656e5689de0956c3ccb7`.
- 2604.21223: `Zero-Shot Detection of LLM-Generated Text via Implicit Reward
  Model, Runheng Liu et al., NeurIPS, 2025.pdf`;
  `948798d933d73d437446080ec0b83aa9176b9ded9985825a10b30d4198b668fe`.
- 2604.16923: `Alignment Imprint- Zero-Shot AI-Generated Text Detection via
  Provable Preference Discrepancy, Junxi Wu et al., arXiv, 2026.pdf`;
  `620a0cf98fe5cabd0d266470d1cbd4a39b59b5ec0542de920a52ce1a5dae5f06`.
- 2602.13042: `GPTZero- Robust Detection of LLM-Generated Texts, George Alexandru
  Adam et al., arXiv, 2026.pdf`;
  `341332b450762857d140a934f9878c78db8bac561da5b5a1304182060617383d`.
- 2601.04833: `When AI Settles Down- Late-Stage Stability as a Signature of
  AI-Generated Text Detection, Ke Sun et al., arXiv, 2026.pdf`;
  `50bb8bb07148e7ef527bc9875987b7ea0b6c6cc3233778ae633941af4c8891f4`.
- 2511.01192: `DEER- Disentangled Mixture of Experts with Instance-Adaptive
  Routing for Generalizable Machine-Generated Text Detection, Guoxin Ma et al.,
  arXiv, 2025.pdf`;
  `2328603588d53dd95d2626a0eba9971de3680f395bf00eb97db648ff146655bb`.
- 2508.13152: `RepreGuard- Detecting LLM-Generated Text by Revealing Hidden
  Representation Patterns, Xin Chen et al., TACL, 2025.pdf`;
  `dfcfe768062a716d92356dc3e306444e62dd4cc9bac21641637be4e858f1ceef`.
- 2506.15683: `PhantomHunter- Detecting Unseen Privately-Tuned LLM-Generated Text
  via Family-Aware Learning, Yuhui Shi et al., arXiv, 2025.pdf`;
  `bc2cb679488a08a0a390b4e217eee53a44d0e715fec0dd807a29645056b61b5b`.
- 2506.06705: `DivScore- Zero-Shot Detection of LLM-Generated Text in Specialized
  Domains, Zhihui Chen et al., arXiv, 2025.pdf`;
  `6e896b807f0684520dc8b93d7241d4f91dac3fd0d92f43e087f206679f524557`.

Official artifact identities used for reproduction:

- IRM NeurIPS supplemental archive:
  `831062de6a10566594c072f43ea8b770dfdf73d1b1193dc32c3a4c76fb56c8fa`.
- LAPD `method/core/compute.py` at the recorded commit:
  `b1fa1fc8380b69f9f1acab980ebd8117d9708cf3af18174f3720687c35eebe4e`;
  `agg_strategy.py`:
  `961e9f6f79d257ee176f9cb32d390a3188de657de7ed59985cee558881573ce6`;
  multi-GPU runner:
  `f99e8de654e74ca7533113d205da12eecfd05fed68d60b6fd16210320674a490`.
- Public IRM Qwen2-0.5B base weight:
  `9cd8fc8c85a197b8c551d6b931b5709fe2611889d6b44945876472fecdf77cad`;
  instruction weight:
  `130282af0dfa9fe5840737cc49a0d339d06075f83c5a315c3372c9a0740d0b96`.
- Public SV-Detect GPT-Neo-2.7B weight:
  `ac75c6bf3e242ed5df22c1d9eb4a5fa563d201c0beab16711bd3fbb7448b1699`.

Repository snapshots and model downloads were inspected in ephemeral workspaces.
Their immutable commits, revisions, public URLs, relevant file hashes, and exact
execution outputs are durable here and in `search_log.md` and the benchmark result
files. No authenticated artifact was copied or accessed.
