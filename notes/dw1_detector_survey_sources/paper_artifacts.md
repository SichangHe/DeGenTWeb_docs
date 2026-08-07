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
