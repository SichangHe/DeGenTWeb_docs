#!/usr/bin/env python3
"""Build the frozen full-text/configuration inventory for the 119-paper export."""

from __future__ import annotations

import argparse
import csv
import hashlib
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _pairs(value: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for line in value.strip().splitlines():
        slug, display = line.split("|", 1)
        pairs.append((slug, display))
    return pairs


# Curated only after reading each primary paper's full text and result tables.  A row
# is a separately named submitted/proposed/fitted configuration with a qualifying
# threshold metric or explicit high-performance claim.  Repeated datasets and
# operating points remain evidence on one row; component-only hyperparameter sweeps
# are not deployment accounts.
PRIMARY_GROUPS: dict[str, list[tuple[str, str]]] = {
    "2607.22026": _pairs("""
multilevel-energy|DWT multilevel detail energy
energy-norm|DWT normalized energy
window-std|DWT windowed coefficient standard deviation
equal-hard|DWT equal-weight hard voting
equal-soft|DWT equal-weight soft voting
calibrated-hard|DWT calibration-weighted hard voting
calibrated-soft|DWT calibration-weighted soft voting
"""),
    "2607.17382": _pairs("""
modernbert-large|DACTYL ModernBERT-large
modernbert-large-mcgrad|DACTYL ModernBERT-large with MCGrad
deberta-v3-large|DACTYL DeBERTa-v3-large
"""),
    "2607.03680": _pairs("""
vanilla-intellabs-base|IntelLabs-trained Vanilla RoBERTa-base
vanilla-mage-large|MAGE-trained Vanilla RoBERTa-large
vanilla-faid-base|FAID-trained Vanilla RoBERTa-base
vanilla-mirage-large|MIRAGE-trained Vanilla RoBERTa-large
anchor|Anchor peer-review detector
mage-longformer|MAGE Longformer comparator
llmdetectaive|LLM-DetectAIve comparator
faid|FAID comparator
vanilla-faid-extra-domain|FAID Vanilla+extra adapted to the unseen-domain validation set
vanilla-faid-extra-domain-generator|FAID Vanilla+extra adapted to the unseen-domain-plus-generator validation set
detectanyllm|DetectAnyLLM comparator
vanilla-mirage-base|MIRAGE-trained Vanilla RoBERTa-base
fomaml-lora|FOMAML+LoRA K=10 target-adapted detector
fomaml-hc3-k5|FOMAML+LoRA MAGE-to-HC3 K=5 adaptation
fomaml-hc3-k20|FOMAML+LoRA MAGE-to-HC3 K=20 adaptation
fomaml-hc3-k50|FOMAML+LoRA MAGE-to-HC3 K=50 adaptation
confidence-ensemble|Confidence-weighted vanilla/FOMAML ensemble
reverse-confidence-ensemble|Reverse-confidence FOMAML/vanilla ensemble
pooled-four-way|Four-way mixed pooled Vanilla detector
pooled-stratified-base|Stratified pooled Vanilla RoBERTa-base
pooled-stratified-large|Stratified pooled Vanilla RoBERTa-large
"""),
    "2606.23336": _pairs("""
base|WaveDetect-base
all|WaveDetect-all
"""),
    "2606.07313": _pairs("""
gpt-neo-logreg-all|SV-Detect GPT-Neo-2.7B LogReg/all
gpt-neo-logreg-trimmed|SV-Detect GPT-Neo-2.7B LogReg/trimmed
qwen3-1.7b|SV-Detect Qwen3-1.7B
qwen3-1.7b-base|SV-Detect Qwen3-1.7B-Base
gemma3-1b-pt|SV-Detect Gemma3-1B pretrained
gemma3-1b-it|SV-Detect Gemma3-1B instruction-tuned
llama2-mean-all|SV-Detect Llama-2-7B Mean/all
llama2-mean-trimmed|SV-Detect Llama-2-7B Mean/trimmed
llama2-logreg-all|SV-Detect Llama-2-7B LogReg/all
llama2-logreg-trimmed|SV-Detect Llama-2-7B LogReg/trimmed
polish-only|SV-Detect MIRAGE polish-only fitted state
three-task|SV-Detect MIRAGE three-task fitted state
"""),
    "2606.02158": _pairs("""
uncertainty|Uncertainty
uncertainty-plus|Uncertainty++
likelihood|Likelihood comparator
logrank|LogRank comparator
detectlrr|DetectLRR comparator
lastde|Lastde comparator
detectgpt|DetectGPT comparator
detectnpr|DetectNPR comparator
dnagpt|DNA-GPT comparator
fastdetectgpt|Fast-DetectGPT comparator
lastde-plus|Lastde++ comparator
without-low-probability|Uncertainty without low-probability feature
without-entropy|Uncertainty without entropy feature
"""),
    "2606.00402": _pairs("""
l2d-knockoff|Knockoff-calibrated L2D
imbd-knockoff|Knockoff-calibrated ImBD
"""),
    "2605.25281": _pairs("""
imbd-read|ImBD trained on READ
imbd-target-adapted|ImBD target-adapted
biscope-read|BiScope trained on READ
biscope-target-adapted|BiScope target-adapted
npr-gemma|NPR with Gemma surrogate
npr-qwen|NPR with Qwen surrogate
detectgpt-gemma|DetectGPT with Gemma surrogate
detectgpt-qwen|DetectGPT with Qwen surrogate
binoculars-gemma|Binoculars with Gemma model pair
radar|RADAR released comparator
fastdetectgpt-gemma|FastDetectGPT with Gemma sampling/scoring models
adadetectgpt-gemma|AdaDetectGPT with Gemma sampling/scoring models
adadetectgpt-gemma-target|Target-adapted AdaDetectGPT with Gemma sampling/scoring models
grpo-noncot|READER GRPO non-CoT
grpo-cot|READER GRPO CoT
"""),
    "2605.16107": _pairs("""
likelihood|Likelihood baseline
logrank|Log-Rank baseline
entropy|Entropy baseline
detectgpt|DetectGPT baseline
fastgpt|FastGPT baseline
binoculars|Binoculars baseline
fouriergpt|FourierGPT baseline
adagpt|AdaGPT baseline
likelihood-m|Likelihood-M
likelihood-mult|Likelihood-Mult
logrank-m|Log-Rank-M
logrank-mult|Log-Rank-Mult
entropy-m|Entropy-M
entropy-mult|Entropy-Mult
detectgpt-m|DetectGPT-M
detectgpt-mult|DetectGPT-Mult
fastgpt-m|FastGPT-M
fastgpt-mult|FastGPT-Mult
binoculars-m|Binoculars-M
binoculars-mult|Binoculars-Mult
fouriergpt-m|FourierGPT-M
fouriergpt-mult|FourierGPT-Mult
adagpt-m|AdaGPT-M
adagpt-mult|AdaGPT-Mult
detectllm-m|DetectLLM-M
detectllm-mult|DetectLLM-Mult
"""),
    "2605.06903": _pairs("""
paper-era|MELD paper-era model
public-v5|MELD public v5 checkpoint
roberta-chatgpt-meld|RoBERTa-ChatGPT retrained on MELD data
modernbert-detect-meld|ModernBERT-Detect retrained on MELD data
repreguard-meld|RepreGuard retrained on MELD data
"""),
    "2605.02374": _pairs("""
react-32shot|REACT 32-shot
react-64shot|REACT 64-shot
react-128shot|REACT 128-shot
react-256shot|REACT 256-shot
"""),
    "2604.21223": _pairs("""
llama32-pair|IRM Llama-3.2 model pair
qwen25-pair|IRM Qwen2.5 model pair
reward-model-deberta|OpenAssistant RM-DeBERTa-v3-large-v2 comparator
"""),
    "2606.00016": _pairs("""
cnn|AEyeDE CNN
cnn-text|AEyeDE CNN+text
individual|AEyeDE individual-generator arrangement
unified|AEyeDE unified-generator arrangement
superannotate-roberta|SuperAnnotate RoBERTa comparator
"""),
    "2604.02008": _pairs("""
likelihood|Likelihood comparator
logrank|LogRank comparator
fastdetectgpt|FastDetectGPT comparator
binoculars|Binoculars comparator
fastdetectgpt-dald|FastDetectGPT+DALD
fastdetectgpt-glimpse-gpt4-geometric|FastDetectGPT+Glimpse GPT-4 geometric
fastdetectgpt-glimpse-gpt4-zipfian|FastDetectGPT+Glimpse GPT-4 Zipfian
fastdetectgpt-glimpse-gpt4-mlp|FastDetectGPT+Glimpse GPT-4 MLP
fastdetectgpt-glimpse-davinci-geometric|FastDetectGPT+Glimpse DaVinci-002 geometric
binoculars-dald|Binoculars+DALD
likelihood-knnproxy|Likelihood+kNNProxy
fastdetectgpt-knnproxy|FastDetectGPT+kNNProxy
binoculars-knnproxy|Binoculars+kNNProxy
fastdetectgpt-mop|FastDetectGPT+MoP
binoculars-mop|Binoculars+MoP
"""),
    "2602.08031": _pairs("""
likelihood|Likelihood baseline
likelihood-m|Likelihood-M
logrank|Log-Rank baseline
logrank-m|Log-Rank-M
entropy|Entropy baseline
entropy-m|Entropy-M
detectgpt|DetectGPT baseline
detectgpt-m|DetectGPT-M
fastgpt|FastGPT baseline
fastgpt-m|FastGPT-M
dnagpt|DNA-GPT baseline
dnagpt-m|DNA-GPT-M
repreguard|RepreGuard baseline
repreguard-m|RepreGuard-M
lastde|Lastde baseline
lastde-m|Lastde-M
fouriergpt|FourierGPT baseline
fouriergpt-m|FourierGPT-M
binoculars|Binoculars baseline
binoculars-m|Binoculars-M
"""),
    "2602.01240": _pairs("""
likelihood|DetectRouter-Likelihood
entropy|DetectRouter-Entropy
rank|DetectRouter-Rank
logrank|DetectRouter-LogRank
llr|DetectRouter-LLR
fastdetectgpt|DetectRouter-FastDetectGPT
"""),
    "2602.13226": _pairs("""
varybalance|VaryBalance
varybalance-expansion|VaryBalance with expansion
"""),
    "2601.04833": _pairs("""
likelihood|Likelihood
logrank|Log-Rank
fastdetectgpt|FastDetectGPT
lastde|Lastde
diveye|DivEye
dd|DD
lv|LV
tsd|TSD
tsd-plus|TSD+
"""),
    "2601.04641": _pairs("""
likelihood|DP-MGTD Likelihood
rank|DP-MGTD Rank
rank-gltr|DP-MGTD Rank-GLTR
entropy|DP-MGTD Entropy
logrank|DP-MGTD Log-Rank
binoculars|DP-MGTD Binoculars
distilbert-f|DP-MGTD DistilBERT-F
roberta-f|DP-MGTD RoBERTa-F
"""),
    "2601.03812": _pairs("""
bilstm|BiLSTM detector
distilbert|DistilBERT detector
"""),
    "2511.21744": _pairs("""
cnn|NEULIF CNN
random-forest|NEULIF Random Forest
ai-generated-text-detection|AI-generated Text Detection transformer ensemble comparator
detective-comparator|DeTeCtive literature comparator
restricted-embeddings|Restricted Embeddings literature comparator
chatgpt-detector|ChatGPT Detector literature comparator
roberta-bilstm|RoBERTa plus BiLSTM literature comparator
styloai-education|StyloAI Education-dataset result
"""),
    "2511.01192": _pairs("""
domain-f1|DEER domain-matching/F1 routing
domain-entropy|DEER domain-matching/entropy routing
reward-f1|DEER reward-driven/F1 routing
reward-entropy|DEER reward-driven/entropy routing
"""),
    "2511.00988": _pairs("""
chatgpt-e|ChatGPT-E
mpu-e|MPU-E
radar-e|RADAR-E
ours-kd|Ours-KD
"""),
    "2509.18880": _pairs("""
gpt2|DivEye GPT-2
falcon7b|DivEye Falcon-7B
llama31-8b|DivEye Llama-3.1-8B
mistral7b|DivEye Mistral-7B-v0.3
e5-small-lora|e5-small-lora fitted comparator
desklib|Desklib AI fitted comparator
superannotate|SuperAnnotate fitted comparator
boost-radar|DivEye+RADAR
boost-detectllm|DivEye+DetectLLM
boost-fastdetectgpt|DivEye+FastDetectGPT
boost-biscope|DivEye+BiScope
"""),
    "2510.02319": _pairs("""
bert|Fine-tuned BERT
distilbert|Fine-tuned DistilBERT
roberta|Fine-tuned RoBERTa
xlnet|Fine-tuned XLNet
albert|Fine-tuned ALBERT
deberta|Fine-tuned DeBERTa
modernbert|Fine-tuned ModernBERT
adv-modernbert|Adversarially trained ModernBERT
pife-modernbert|PIFE-augmented ModernBERT
fastdetectgpt|FastDetectGPT comparator
glimpse|Glimpse comparator
binoculars|Binoculars comparator
logrank|LogRank comparator
"""),
    "2509.14268": _pairs("""
qwen2-0.5b|DetectAnyLLM Qwen2-0.5B scoring model
gpt-j-6b|DetectAnyLLM GPT-J-6B scoring model
gpt-neo-2.7b|DetectAnyLLM GPT-Neo-2.7B scoring model
"""),
    "2509.02499": _pairs("""
lr-roberta|MoSEs-lr + RoBERTa
lr-fastdetectgpt|MoSEs-lr + FastDetectGPT
lr-lastde|MoSEs-lr + Lastde
xg-roberta|MoSEs-xg + RoBERTa
xg-fastdetectgpt|MoSEs-xg + FastDetectGPT
xg-lastde|MoSEs-xg + Lastde
"""),
    "2509.00623": _pairs("""
roberta-base|M-DAIGT RoBERTa-base
tfidf-svm|M-DAIGT TF-IDF+LinearSVC
candace|M-DAIGT Candace
"""),
    "2508.13768": _pairs("""
roberta-base|MGT-Prism RoBERTa-base
roberta-large|MGT-Prism RoBERTa-large
"""),
    "2508.11933": _pairs("""
raidar|RAIDAR direct baseline
gpt4o-direct|GPT-4o direct baseline
gpt-cot|GPT+CoT baseline
gpt-react|GPT+ReAct baseline
gpt35|CAMF GPT-3.5-Turbo agents
gpt4o|CAMF GPT-4o agents
llama3-70b|CAMF Llama-3-70B agents
gpt4o-mini|CAMF GPT-4o-mini agents
gemini15-pro|CAMF Gemini-1.5 Pro agents
deepseek-v3|CAMF DeepSeek-V3 agents
"""),
    "2508.11343": _pairs("""
specdetect|SpecDetect
specdetect-plus|SpecDetect++
likelihood|Likelihood comparator
logrank|LogRank comparator
entropy|Entropy comparator
detectlrr|DetectLRR comparator
lastde|Lastde comparator
detectgpt|DetectGPT comparator
detectnpr|DetectNPR comparator
dnagpt|DNA-GPT comparator
fastdetectgpt|Fast-DetectGPT comparator
lastde-plus|Lastde++ comparator
"""),
    "2508.06913": _pairs("""
sdc|SentiDetect-SDC
sdp|SentiDetect-SDP
"""),
    "2507.23577": _pairs("""
tdetect|T-Detect
ct-tdetect|CT(T-Detect)
"""),
    "2507.05157": _pairs("""
gpt4o-mini|Defactify GPT-4o-mini fine-tune
bert|Defactify BERT fine-tune
llama3-8b|Defactify Llama-3-8B fine-tune
"""),
    "2506.15683": _pairs("""
full|PhantomHunter
without-bfe|PhantomHunter without BFE
without-cl|PhantomHunter without contrastive learning
without-moe|PhantomHunter without mixture-of-experts
roberta-baseline|RoBERTa comparison state
t5-sentinel-baseline|T5-Sentinel comparison state
detective-baseline|DeTeCtive comparison state
seqxgpt-baseline|SeqXGPT comparison state
dna-gpt-baseline|DNA-GPT comparison state
detectgpt-baseline|DetectGPT comparison state
fastdetectgpt-baseline|Fast-DetectGPT comparison state
hastewire|HasteWire commercial comparison service
"""),
    "2506.06705": _pairs("""
general|DivScore
medical|DivScore-medical
legal|DivScore-legal
without-adaptation|DivScore without domain adaptation
divscore-mistral|DivScore with Mistral detector LM
divscore-falcon|DivScore with Falcon detector LM
divscore-qwen|DivScore with Qwen detector LM
divscore-llama|DivScore with Llama detector LM
entropy-mistral|Entropy with Mistral detector LM
entropy-falcon|Entropy with Falcon detector LM
entropy-qwen|Entropy with Qwen detector LM
entropy-llama|Entropy with Llama detector LM
cross-entropy-qwen|Cross-Entropy with Qwen detector LM
roberta-base|RoBERTa-base comparator
roberta-large|RoBERTa-large comparator
entropy|Entropy comparator
rank|Rank comparator
logrank|Log-Rank comparator
likelihood|Log-Likelihood comparator
detectgpt|DetectGPT comparator
fastdetectgpt|Fast-DetectGPT comparator
binoculars|Binoculars comparator
"""),
    "2506.01702": _pairs("""
gemma2-2b|Gemma-2-2B submitted detector
gemma2-9b-it|Gemma-2-9B-IT submitted detector
qwen3-4b|Qwen3-4B-Base submitted detector
qwen3-8b|Qwen3-8B-Base submitted detector
qwen3-14b|Qwen3-14B-Base submitted detector
mdok-binary|mdok binary detector
tfidf-baseline|TF-IDF validation baseline
"""),
    "2505.15261": _pairs("""
full|Full AGENT-X
without-multi-agent|AGENT-X without multi-agent
without-guidelines|AGENT-X without guidelines
without-adaptive-routing|AGENT-X without adaptive routing
without-steer-calibration|AGENT-X without steer calibration
"""),
    "2505.13855": _pairs("""
qwen18b|Qwen1.5-1.8B
qwen32b|Qwen1.5-32B
qwen-moe|Qwen MoE
equal-vote|Equal Vote
weighted-vote|Weighted Vote
jt-domain|JT-Domain
jt-scratch|JT-Scratch
dogen|DoGEN
"""),
    "2505.11550": _pairs("""
full|Full multifaceted architecture
optimized|Optimized multifaceted architecture
simple|Simple E5+stylometry architecture
"""),
    "2504.21019": _pairs("""
uniform|DP-Net+uniform noise
gaussian|DP-Net+Gaussian noise
"""),
    "2503.22338": _pairs("""
svc-raidar|SVC with RAIDAR features
svc-nela|SVC with NELA features
svc-combined|SVC with RAIDAR+NELA features
rf-raidar|Random Forest with RAIDAR features
rf-nela|Random Forest with NELA features
rf-combined|Random Forest with RAIDAR+NELA features
xgb-raidar|XGBoost with RAIDAR features
xgb-nela|XGBoost with NELA features
xgb-combined|XGBoost with RAIDAR+NELA features
"""),
    "2502.16857": _pairs("""
original-xsmall|Original-data DeBERTa-v3-xsmall
original-small|Original-data DeBERTa-v3-small
original-base|Original-data DeBERTa-v3-base
noised-xsmall|Noised-data DeBERTa-v3-xsmall
noised-small|Noised-data DeBERTa-v3-small
noised-base|Noised-data DeBERTa-v3-base
double-small|Double-finetuned DeBERTa-v3-small
ensemble-small|Weighted small/double-finetune ensemble
"""),
    "2501.03940": _pairs("""
radar-ft|RADAR-FT comparator
m4-roberta-base|Five-epoch RoBERTa-base M4 baseline
m4-xlm-roberta|M4 XLM-RoBERTa comparator
mage-longformer|MAGE Longformer comparator
gltr|GLTR comparator
raid-rb-gpt2|RAID RoBERTa-base GPT-2-output detector
raid-rl-gpt2|RAID RoBERTa-large GPT-2-output detector
raid-rb-cgpt|RAID RoBERTa-base HC3 detector
raid-radar|RAID RADAR comparator
raid-fastdetectgpt|RAID FastDetectGPT comparator
raid-binoculars|RAID Binoculars comparator
raid-gptzero|RAID GPTZero service
raid-originality|RAID Originality service
raid-winston|RAID Winston service
raid-zerogpt|RAID ZeroGPT service
mage-roberta-base|MAGE-pretrained RoBERTa-base
mage-radar-ptm|MAGE-pretrained RADAR-PTM
raidft-pawn-gpt2|PAWN GPT-2 after one-epoch RAID fine-tuning
raidft-pawn-llama|PAWN Llama-3.1-1B after one-epoch RAID fine-tuning
raidft-longformer|Longformer after one-epoch RAID fine-tuning
raidft-roberta|RoBERTa after one-epoch RAID fine-tuning
raidft-radar-ptm|RADAR-PTM after one-epoch RAID fine-tuning
raidft-radar|RADAR after one-epoch RAID fine-tuning
gpt2|PAWN GPT-2
llama31-1b|PAWN Llama-3.1-1B
hsff-gpt2|HSFF GPT-2 ablation
hsff-llama31-1b|HSFF Llama-3.1-1B ablation
mpn-gpt2|MPN GPT-2 ablation
mpn-llama31-1b|MPN Llama-3.1-1B ablation
ens-gpt2-llama|PAWN ensemble 1 GPT-2 + 1 Llama
ens-2gpt2-2llama|PAWN ensemble 2 GPT-2 + 2 Llama
ens-2gpt2|PAWN ensemble 2 GPT-2
ens-2llama|PAWN ensemble 2 Llama
ens-gpt2-llama-qwen|PAWN ensemble GPT-2 + Llama + Qwen
"""),
}


MODEL16 = _pairs("""
llama31-8b|Llama-3.1-8B
llama32-3b|Llama-3.2-3B
phi3-mini|Phi-3-mini
phi3-small|Phi-3-small
phi3-medium|Phi-3-medium
phi35-mini|Phi-3.5-mini
phi4-mini|Phi-4-mini
phi4|Phi-4
ministral8b|Ministral-8B-2410
mistral-nemo|Mistral-Nemo-2407
qwen2-7b|Qwen2-7B
qwen25-3b|Qwen2.5-3B
qwen25-7b|Qwen2.5-7B
qwen25-14b|Qwen2.5-14B
falcon3-3b|Falcon3-3B
falcon3-7b|Falcon3-7B
""")
PRIMARY_GROUPS["2601.20006"] = (
    [("external-deberta", "External DeBERTa detector")]
    + [(f"master-{slug}", f"Master-test {name}") for slug, name in MODEL16]
    + [
        (f"gpt41nano-{slug}", f"GPT-4.1-nano validation {name}")
        for slug, name in MODEL16
    ]
    + _pairs("""
self-phi35-mini|Per-LLM Phi-3.5-mini
self-mistral-nemo|Per-LLM Mistral-Nemo-2407
family-llama31-8b|Per-family Llama-3.1-8B
ensemble-per-llm|Per-LLM ensemble
ensemble-per-family|Per-family ensemble
""")
)

MIXTURE_CONFIGS: list[tuple[str, str]] = []
for feature, display in (("word2vec", "Word2Vec"), ("tfidf", "TF-IDF")):
    for learner in ("LR", "RF", "XGB", "LDA", "SVM"):
        MIXTURE_CONFIGS.append((f"{feature}-{learner.lower()}", f"{display} {learner}"))
for slug, name in _pairs("""
cnn|CNN
rnn|RNN
lstm|LSTM
bilstm|BiLSTM
bigru|BiGRU
cnn-lstm|CNN-LSTM
cnn-bilstm|CNN-BiLSTM
cnn-bigru|CNN-BiGRU
bert|BERT
distilbert|DistilBERT
roberta|RoBERTa
deberta|DeBERTa
modernbert|ModernBERT
"""):
    MIXTURE_CONFIGS.append((f"binary-{slug}", f"Binary {name}"))
for slug, name in _pairs("""
bert|BERT
distilbert|DistilBERT
roberta|RoBERTa
deberta|DeBERTa
modernbert|ModernBERT
"""):
    MIXTURE_CONFIGS.append((f"implicit-{slug}", f"Implicit-method {name}"))
PRIMARY_GROUPS["2509.22147"] = MIXTURE_CONFIGS

PRIMARY_GROUPS.update(
    {
        "2608.03859": _pairs("""
pan12-ngram|PAN12 character n-gram plagiarism detector
bm25-pair|BM25 pair classifier
linq-cosine|Linq cosine similarity
plagbench-zero|PlagBench zero-shot vanilla
plagbench-zero-cot|PlagBench zero-shot chain-of-thought
plagbench-few|PlagBench few-shot vanilla
plagbench-few-cot|PlagBench few-shot chain-of-thought
scdg-qwen-avg|SCDG Qwen3-8B average aggregation
scdg-qwen-topq|SCDG Qwen3-8B top-q aggregation
scdg-ministral-avg|SCDG Ministral-8B average aggregation
scdg-ministral-topq|SCDG Ministral-8B top-q aggregation
scdg-llama-avg|SCDG Llama-3.1-8B average aggregation
scdg-llama-topq|SCDG Llama-3.1-8B top-q aggregation
bm25-full|BM25 full-document retrieval
bm25-sentence|BM25 sentence retrieval
bge-m3-full|BGE-M3 full-document retrieval
bge-m3-sentence|BGE-M3 sentence retrieval
four-way-combsum|Four-way CombSUM retrieval
linq-sentence-chunk|Linq sentence-to-chunk retrieval
three-route-rrf|Three-route reciprocal-rank fusion
rrf-scdg|Reciprocal-rank fusion plus SCDG
daac|DAAC retrieval
daac-scdg|DAAC plus SCDG
"""),
        "2608.01046": _pairs("""
deberta-finetuned|Fine-tuned DeBERTa-Sentinel
roberta-finetuned|Fine-tuned RoBERTa-Sentinel
tfidf-logreg|TF-IDF logistic regression
deberta-zeroshot|Zero-shot DeBERTa-Sentinel
"""),
        "2607.14967": _pairs("""
gtcl-nomic|GTCL with Nomic embeddings
gtcl-jina|GTCL with Jina embeddings
detective|DeTeCtive
desklib|Desklib
tmr|TMR
"""),
        "2607.14905": _pairs("""
longformer|Longformer text-only baseline
gcn|Reasoning-graph GCN
gat|Reasoning-graph GAT
graph-transformer|Reasoning-graph Transformer
gps|Reasoning-graph GPS
"""),
        "2606.31074": _pairs("""
raidar|RAIDAR
binoculars|Binoculars
triospect-binoculars|Triospect-Binoculars
imbd|ImBD
triospect-imbd|Triospect-ImBD
fastdetectgpt|FastDetectGPT
triospect-fastdetectgpt|Triospect-FastDetectGPT
triospect-fd-qwen200|Triospect-FastDetectGPT Qwen max-tokens 200
triospect-fd-gpt4o200|Triospect-FastDetectGPT GPT-4o max-tokens 200
"""),
        "2606.18946": _pairs("""
poger|POGER
seqxgpt|SeqXGPT
sendetex|SenDetEX
senflow|SenFlow
senflow-no-gcn|SenFlow without GCN
senflow-no-crf|SenFlow without CRF
senflow-no-cl|SenFlow without contrastive learning
senflow-no-tcn|SenFlow without TCN
"""),
        "2605.27921": _pairs("""
tell|TELL
mage|MAGE classifier
pangram-editlens|Pangram EditLens
fastdetectgpt|FastDetectGPT
argugpt|ArguGPT
t5-sentinel|T5-Sentinel
detectllm-npr|DetectLLM-NPR
openai-roberta|OpenAI RoBERTa
aigc-mpu|AIGC MPU
detectllm-lrr|DetectLLM-LRR
logrank-gpt2-medium|LogRank GPT-2-medium
radar|RADAR
chatgpt-d|ChatGPT-D
"""),
        "2605.03723": _pairs("""
vcp|VCP change-point detector
wcp|WCP change-point detector
"""),
        "2605.02712": _pairs("""
qwen3-32b-st-07|Qwen3-32B_ST threshold 0.7
"""),
        "2604.25860": _pairs("""
luminol|Luminol-AIDetect
binoculars|Binoculars
fastdetectgpt|FastDetectGPT
"""),
        "2604.21365": _pairs("""
gemma3-task-a|Gemma-3-27B Task A submission
codegemma-task-b|CodeGemma-7B Task B submission
qwen-coder-task-c|Qwen2.5-Coder-14B Task C submission
"""),
        "2604.21300": _pairs("""
luar|LUAR
man-nguyen|Man and Nguyen baseline
contrastive-pretraining|Contrastive pretraining baseline
eavae|EAVAE
"""),
        "2604.16923": _pairs("""
entropy|Entropy
likelihood|Likelihood
logrank|LogRank
fastdetectgpt|FastDetectGPT
lastde-plus|Lastde++
binoculars|Binoculars
dna-detectllm|DNA-DetectLLM
remodetect|ReMoDetect
imbd|ImBD
rai|RAI preference-discrepancy score
s-score|Alignment-imprint S score
lapd-llama2|LAPD Llama-2 model pair
lapd-falcon|LAPD Falcon model pair
lapd-gptj|LAPD GPT-J model pair
lapd-llama31|LAPD Llama-3.1 model pair
"""),
        "2604.04932": _pairs("""
roberta|RoBERTa
roberta-dann|RoBERTa-DANN
coco|CoCo
seqxgpt|SeqXGPT
detective|DeTeCtive
lf-motifs|LF-Motifs
race|RACE with IsaNLP parser
race-no-cl|RACE without contrastive learning
race-no-relation|RACE without relations
race-no-rgcn|RACE without RGCN
race-no-bottleneck|RACE without bottleneck
race-no-basis|RACE without basis decomposition
race-dmrst|RACE with DMRST parser
"""),
        "2603.24981": _pairs("""
biscope|BiScope
fastdetectgpt|FastDetectGPT
binoculars|Binoculars
lastde-plus|Lastde++
irm|IRM
dna-detectllm|DNA-DetectLLM
exons-falcon|Exons-Detect Falcon model pair
exons-no-repair|Exons-Detect without log-perplexity repair
exons-no-g|Exons-Detect without exonic-token amplification
exons-llama7b|Exons-Detect Llama-7B model pair
exons-mistral|Exons-Detect Mistral model pair
exons-llama32|Exons-Detect Llama-3.2 model pair
"""),
        "2603.05617": _pairs("""
stylometric|NOTAI stylometric classifier
curvature|NOTAI curvature classifier
ensemble|NOTAI full ensemble
"""),
        "2602.15514": _pairs("""
xlmr|XLM-RoBERTa baseline
dependencyai|DependencyAI
"""),
        "2602.11871": _pairs("""
fdgpt-llama|FastDetectGPT with Llama scorer
fdgpt-mistral|FastDetectGPT with Mistral scorer
fdgpt-qwen|FastDetectGPT with Qwen scorer
binoculars-llama|Binoculars with Llama pair
binoculars-mistral|Binoculars with Mistral pair
binoculars-qwen|Binoculars with Qwen pair
    """),
    }
)

PRIMARY_GROUPS.update(
    {
        "2511.17402": _pairs("""
roberta-bne|RoBERTa-BNE machine-text classifier
pucp-xgb|PUCP-Metrix XGBoost classifier
"""),
        "2510.20610": _pairs("""
xlm-roberta|BUSTED XLM-RoBERTa submission
"""),
        "2510.16549": _pairs("""
bert-rs|BERT trained on real plus synthetic reviews
scibert-rs|SciBERT trained on real plus synthetic reviews
roberta-rs|RoBERTa trained on real plus synthetic reviews
llama31-rs|Llama-3.1-8B trained on real plus synthetic reviews
qwen3-rs|Qwen3-8B trained on real plus synthetic reviews
"""),
        "2510.12608": _pairs("""
fastdetectgpt|FastDetectGPT
raidar|RAIDAR
r-detect|R-Detect
style-tfidf|StyleDecipher TF-IDF representation
style-word2vec|StyleDecipher Word2Vec/GloVe representation
style-bert|StyleDecipher BERT representation
style-sbert|StyleDecipher SBERT representation
"""),
        "2510.00890": _pairs("""
scispandet|Sci-SpanDet
no-sd|Sci-SpanDet without semantic discrepancy
no-graphenc|Sci-SpanDet without graph encoder
no-mc|Sci-SpanDet without metric contrast
no-sl|Sci-SpanDet without structural learning
no-calibration|Sci-SpanDet without calibration
no-pc|Sci-SpanDet without probability correction
"""),
        "2509.25154": _pairs("""
roberta|RoBERTa
roberta-candidates|RoBERTa with candidate texts
longformer|Longformer
longformer-candidates|Longformer with candidate texts
jdetector-lgbm|J-Detector LGBM
jdetector-rf|J-Detector Random Forest
jdetector-xgb|J-Detector XGBoost
jdetector-no-llm|J-Detector without LLM-enhanced features
jdetector-no-linguistic|J-Detector without linguistic features
"""),
        "2509.15550": _pairs("""
biscope|BiScope
entropy|Entropy
likelihood|Likelihood
logrank|LogRank
detectgpt|DetectGPT
fastdetectgpt|FastDetectGPT
binoculars|Binoculars
lastde-plus|Lastde++
revise-detect|Revise-Detect comparator
dna-default|DNA-DetectLLM default repair
dna-low-high|DNA-DetectLLM low-to-high repair
dna-high-low|DNA-DetectLLM high-to-low repair
dna-sequential|DNA-DetectLLM sequential repair
dna-mistral|DNA-DetectLLM Mistral model pair
dna-llama2|DNA-DetectLLM Llama-2 model pair
dna-llama3|DNA-DetectLLM Llama-3 model pair
"""),
        "2509.00731": _pairs("""
roberta|RoBERTa encoder
bert|BERT encoder
fasttext|FastText classifier
qwen-r4|Qwen2.5-7B LoRA rank 4
qwen-r8|Qwen2.5-7B LoRA rank 8
qwen-r16|Qwen2.5-7B LoRA rank 16
deepseek-r4|DeepSeek-R1-Distill-Qwen-7B LoRA rank 4
deepseek-r8|DeepSeek-R1-Distill-Qwen-7B LoRA rank 8
deepseek-r16|DeepSeek-R1-Distill-Qwen-7B LoRA rank 16
"""),
        "2508.18715": _pairs("""
random-forest|Random Forest dialogue detector
mlp|MLP dialogue detector
faithshap-1|EMMM Faith-SHAP 1-act/1-token
faithshap-3|EMMM Faith-SHAP 3-act/3-token
stii-1|EMMM STII 1-act/1-token
stii-3|EMMM STII 3-act/3-token
ig-1|EMMM Integrated Gradients 1-act/1-token
ig-3|EMMM Integrated Gradients 3-act/3-token
distilgpt2|EMMM DistilGPT-2 utterance detector
distilroberta|EMMM DistilRoBERTa utterance detector
roberta|EMMM RoBERTa utterance detector
"""),
        "2508.01754": _pairs("""
radar|RADAR
tdt|Temporal Tomography Detector
"""),
        "2506.02959": _pairs("""
deberta|HACo-Det DeBERTa
seqxgpt|SeqXGPT
detectgpt|DetectGPT
npr|NPR
fastdetectgpt|FastDetectGPT
logprob|Log-probability
rank|Rank
logrank|LogRank
entropy|Entropy
lrr|LRR
xlnet|HACo-Det XLNet
roberta|HACo-Det RoBERTa
"""),
        "2505.14271": _pairs("""
llmdetectaive|LLM-DetectAIve
t5-sentinel|T5-Sentinel
faid|FAID default
faid-multilingual-e5|FAID multilingual-e5 encoder
faid-xlmr|FAID XLM-RoBERTa encoder
faid-unsup-simcse-xlmr|FAID UnSup-SimCSE-XLM-RoBERTa encoder
faid-knn|FAID k-nearest-neighbors clustering
faid-fuzzy-cmeans|FAID fuzzy C-means clustering
"""),
        "2505.12507": _pairs("""
npr|NPR
lrr|LRR
rank|Rank
entropy|Entropy
logrank|LogRank
likelihood|Likelihood
glimpse|Glimpse
binoculars|Binoculars
dnagpt|DNA-GPT
fastdetectgpt|FastDetectGPT
roberta-qa|RoBERTa-QA
radar|RADAR
gptzero|GPTZero
detective|DeTeCtive
lm2|LM2otifs default
lm2-gpt2-tokenizer|LM2otifs GPT-2 tokenizer
lm2-u|LM2otifs undirected-graph ablation
lm2-w|LM2otifs weighted-graph ablation
lm2-uw|LM2otifs undirected weighted-graph ablation
lm2-no-bert|LM2otifs without BERT token initialization
"""),
        "2505.05084": _pairs("""
binoculars-vanilla|Binoculars default threshold
binoculars-max-f1|Binoculars F1-maximizing threshold
binoculars-platt|Binoculars Platt calibration
binoculars-isotonic|Binoculars isotonic calibration
binoculars-mcp|Binoculars multiscaled conformal prediction
"""),
        "2504.02873": _pairs("""
short-phd|Short-PHD
"""),
        "2503.00032": _pairs("""
exaone-paraphrase|Exaone paraphrase detector
pos-lr|KatFishNet POS logistic regression
punctuation-lr|KatFishNet punctuation logistic regression
pos-rf|KatFishNet POS Random Forest
punctuation-rf|KatFishNet punctuation Random Forest
punctuation-svm|KatFishNet punctuation SVM
all-lr|KatFishNet all-feature logistic regression
pos-punctuation-lr|KatFishNet POS plus punctuation logistic regression
pos-spacing-lr|KatFishNet POS plus spacing logistic regression
punctuation-spacing-lr|KatFishNet punctuation plus spacing logistic regression
"""),
        "2502.12734": _pairs("""
greater-d|GREATER-D defended detector
greater-a-query|GREATER-A query attack
greater-a-zero-query|GREATER-A zero-query attack
"""),
        "2502.12064": _pairs("""
english-gpt2-small|English GPT-2-small GLTR threshold ensemble
multilingual-gpt2-xl|Multilingual GPT-2-XL GLTR threshold ensemble
"""),
        "2502.11336": _pairs("""
roberta|RoBERTa
lr-gltr|Logistic-regression GLTR
dna-gpt|DNA-GPT
exagpt-2000|ExaGPT 2,000-example datastore
exagpt-500|ExaGPT 500-example datastore
exagpt-500-ivfpq|ExaGPT 500-example IVFPQ datastore
"""),
        "2502.04528": _pairs("""
fairopt|FairOPT group-adaptive thresholding
desklib-fairopt|Desklib with FairOPT thresholds
desklib-static|Desklib with static threshold
"""),
        "2501.18998": _pairs("""
fastdetectgpt-baseline|FastDetectGPT unperturbed baseline
fastdetectgpt-bert|FastDetectGPT after BERT embedding attack
fastdetectgpt-elmo|FastDetectGPT after ELMo embedding attack
fastdetectgpt-fasttext|FastDetectGPT after FastText embedding attack
fastdetectgpt-glove|FastDetectGPT after GloVe embedding attack
fastdetectgpt-tmae|FastDetectGPT after TM-AE embedding attack
fastdetectgpt-word2vec|FastDetectGPT after Word2Vec embedding attack
"""),
        "2501.14288": _pairs("""
deberta|DeBERTa-v3-large
deberta-lstm|DeBERTa plus bidirectional LSTM
deberta-lstm-attention|DeBERTa plus LSTM and linear attention
target-shuffling|DeBERTa plus LSTM, attention, and target shuffling
ensemble|Semantic-similarity ensemble
"""),
        "2501.11914": _pairs("""
inverse-perplexity-en|LuxVeri English inverse-perplexity ensemble
inverse-perplexity-multi|LuxVeri multilingual inverse-perplexity ensemble
"""),
        "2606.04177": _pairs("""
linguistic-svm|Linguistic-feature SVM
"""),
    }
)


# Table/figure scopes were recorded independently of the disposition mapping.
# These strings bind every configuration above to the exact portion of its source
# used for the semantic decision; the full extracted-text hash binds all pages.
EVIDENCE: dict[str, str] = {
    "2607.22026": "main scalar-score and voting tables plus proxy/wavelet sensitivity; HC3 best individual 0.9876 AUROC and calibrated hard vote 0.9919, with much weaker M4/MAGE rows",
    "2607.17382": "Tables 8-11 and PAN leaderboard; each named classifier/calibration state has at least one AUROC >=0.93, but calibration and OOD metrics vary",
    "2607.03680": "Tables 2-14; the four separately trained Vanilla states, Anchor, Longformer, LLM-DetectAIve, FAID, extra-fitted FAID states, DetectAnyLLM, MIRAGE-base state, K-shot FOMAML states, pooled-training states, and both ensemble directions have an explicit >=0.90 slice or material fitted-state result; cross-corpus and low-FPR transfer are weaker, and the binned LR rows are target-label oracle diagnostics rather than detector accounts",
    "2606.23336": "Tables 1-3; both WaveDetect states exceed 0.90 on paper rows, while the separately frozen public-state screen is 0.8906 AUROC",
    "2606.07313": "backbone Table 2, COLING Tables 5-6, and MIRAGE Table 9; every backbone or separately fitted polish-only/three-task state has a development, test, or DetectRL AUROC >=0.90, while official COLING F1 can be 0.740",
    "2606.02158": "Tables 1-5 and 12-16; both proposed scores, nine named comparison detectors, and the two named feature ablations have an AUROC/TPR >=0.90 on at least one model/domain cell, with lower paraphrase/cross-domain averages",
    "2606.00402": "Table 2; L2D and ImBD knockoff variants have detection power >=0.90 on at least one generator/q cell; power is not document AUROC",
    "2605.25281": "Tables 2-3, 8-15, and 17-18; READ- and target-adapted supervised states, qualifying Gemma/Qwen proxy configurations, RADAR, and both GRPO prompting states exceed 0.90 on a reported per-domain, target-generator, in-domain, or OOD slice; base/SFT READER rows and rationale-prediction diagnostics are not detector accounts",
    "2605.16107": "Tables II-III and transfer/attack figures; each -M or -Mult state has at least one AUROC or TPR@1%FPR >=0.90, with sharply varying averages",
    "2605.06903": "paper result tables, official checkpoint history, preserved two-A6000 v5 screen, and Appendix Table 9; paper-era, public-v5, and the three same-data baseline retrains are deliberately separate",
    "2605.02374": "main Table 1 and OOD Table 4; every REACT shot-size state exceeds 0.90 accuracy in-domain, while OOD HC3 averages are about 0.86-0.87",
    "2604.21223": "paper model-pair tables, Appendix Table 8, and frozen IRM screen; both pair families and the RM-DeBERTa comparator have a paper AUROC >=0.90 slice, while the best downloadable IRM pair measured 0.9436 versus Binoculars 0.9595",
    "2606.00016": "Tables 1-4 and attack/external Tables 5-9; every named architecture/arrangement and the released SuperAnnotate RoBERTa comparator exceed 0.90 F1 or AUC on at least one cell, with weaker unified/transfer results",
    "2604.02008": "Tables III-V; every aligned/routed detector has AUROC or F1 >=0.90 on a Mix8/DetectRL cell and uses retained proxy/reference material",
    "2602.08031": "Table 2 and Appendix Tables 18-24; each unmodified baseline and corresponding -M detector is separately reported and crosses 0.90 AUROC on a dataset/generator cell, with variable transfer and low-FPR behavior",
    "2602.01240": "Tables 2 and 6-7; each routed criterion crosses 0.90 AUROC on an EvoBench/MAGE family cell although aggregates can be much lower",
    "2602.13226": "main comparison and expansion ablation; both rewrite configurations have a qualifying high cell and require target rewrites",
    "2601.20006": "Tables 8-14; every listed state has accuracy, F1, AUC, or recall >=0.90; most are token-level/validation-only and ensemble precision is weak",
    "2601.04833": "Tables 3 and 6; Likelihood, Log-Rank, FastDetectGPT, Lastde, DivEye, DD, LV, TSD, and TSD+ each have AUROC >=0.90 on at least one generator slice, while aggregate performance is substantially lower",
    "2601.04641": "main DP-MGTD tables; every named detector instantiation has a qualifying high sanitized-text cell and depends on privacy-budget target sanitization",
    "2601.03812": "main classifier table; BiLSTM ROC-AUC 0.94 and DistilBERT 0.96, with lower accuracy/topic-transfer evidence",
    "2511.21744": "Tables 2-3 and the Table 3 discussion; CNN and Random Forest are separately fitted, while six named literature comparison states expose a >=0.90 claim on at least one in-domain or small-dataset slice; NEULIF's best balanced-split ROC-AUC is 0.9951 without cross-domain evidence",
    "2511.01192": "Figure 4 routing-objective series and Tables 3, 6, 8; the four named routing states are separately plotted, and the F1-routed states reach 91.4 and 94.1 while entropy-routed states reach 1.05 and 0.39 entropy on the plotted series; downstream F1 is >=0.90 on a domain/length cell, with weaker OOD/attack averages",
    "2511.00988": "main/appendix AUROC tables and KD table; every enhanced state crosses 0.90 on at least one LLM/domain cell, with variable low-FPR transfer",
    "2509.22147": "binary Tables 3-4; every listed feature/learner or implicit transformer has accuracy/F1 >=0.90; segmentation and multiclass tables are excluded tasks",
    "2509.18880": "Tables 1-4, 6, and 13; each listed backbone/boosted state or fitted e5-small-lora, Desklib, and SuperAnnotate comparator reaches AUROC, accuracy, or a reported attack-slice percentage >=0.90 somewhere; boosted Binoculars stays below 0.90 and is not an account",
    "2510.02319": "Tables IV-VII; seven base fine-tunes, adversarial ModernBERT, and PIFE all have AUC >0.90; only PIFE remains strong on most semantic attacks",
    "2509.14268": "main DDL/reference-clustering tables and scoring-model ablation; each named proxy configuration has a qualifying high cell",
    "2509.02499": "main MoSEs-lr/MoSEs-xg tables; all six learner/base-detector pairings cross 0.90 and depend on the stylistics reference repository",
    "2509.00623": "Table 1: RoBERTa news/academic accuracy-F1 99.99/99.99 and 100/100; TF-IDF+SVM 97.90/97.91 and 99.85/99.85; Candace 99.75/99.75 and 99.95/99.95",
    "2508.13768": "Tables 3, 7, 14; both RoBERTa backbone states exceed 0.90 F1 on a generator/domain cell, with weaker scientific-writing/OOD rows",
    "2508.11933": "main results and backbone analysis; every named multi-agent backbone exceeds 0.90 on at least one domain/generator metric",
    "2508.11343": "Table 1 and appendix result/variant tables; SpecDetect, SpecDetect++, and ten named comparison detectors each cross 0.90 on a dataset/model cell, with incomplete artifact reproduction",
    "2508.06913": "Tables 1-3; SDC and SDP each exceed 0.90 F1 on a domain/generator cell, while averages are about 0.70-0.85 and attacks degrade them",
    "2507.23577": "Tables 1-2; standalone T-Detect has Books AUROC 0.926 and CT(T-Detect) has named high domain cells despite 0.876/0.881 aggregates",
    "2507.05157": "validation/test tables: GPT-4o-mini 0.97 validation and 0.9547 test; BERT 1.00 validation but 0.767 test; Llama Task-B validation macro F1 0.93 but 0.14 test",
    "2506.15683": "Tables 3 and 5; every full/ablation or named experimental comparison row has a class F1 >0.90 somewhere; full PhantomHunter macro F1 is 0.9624-0.9714, comparison and ablation balance is weaker, and HasteWire is a closed service",
    "2506.06705": "Tables 1-2, Figure 4, and appendix Table 4; general, medical, legal, no-adaptation, detector-LM, score-ablation, RoBERTa, and named score-baseline states each exceed 0.90 AUROC on a relevant domain/generator cell",
    "2506.01702": "Tables 1-2 and official Table 4; the TF-IDF validation baseline and all six submitted binary states exceed 0.99 on a validation metric, but OOD AUROC is 0.592-0.700 and official mdok AUROC/F1 0.853/0.898",
    "2505.15261": "Tables 1-3; every listed full/ablation state has a domain AUROC >=0.90, while only full AGENT-X averages 0.9007",
    "2505.13855": "Tables 1-2; every fitted/ensemble configuration crosses 0.90 on MAGE or RAID; DoGEN aggregates are 0.9760 and 0.9581 AUROC",
    "2505.11550": "Table 2; Task-A F1 is 0.949 full, 0.994 optimized, and 0.974 simple, while Task-B is 0.190-0.627",
    "2504.21019": "Tables 2-4; uniform and Gaussian DP-Net states each cross 0.90 accuracy/AUROC on a target domain, with lower averages/paraphrase robustness",
    "2503.22338": "Tables 2-3; all nine classifier-feature states have development F1 >=0.9205; XGBoost test F1 is 0.9454 RAIDAR, 0.9945 NELA, 0.9917 combined",
    "2502.16857": "Tables 2 and 4; three original Task-A states 0.9515-0.9985; three noised Task-A states 0.9985-1.000; double Task-B 0.9167; ensemble Task-B 0.9531",
    "2501.03940": "Tables 4-12; the fitted and prior comparator states, M4 baselines, every PAWN/branch/ensemble, the MAGE-pretrained states, and the separately one-epoch RAID-fitted states have a threshold metric >=0.90 on a reported slice; PAWN paraphrase AUROC is 0.528-0.755 and RAID uses per-domain 5% FPR thresholds",
}

EVIDENCE.update(
    {
        "2608.03859": "Tables 1-2; every listed plagiarism detector, source-conditioned description-gain state, or retrieval/reranking state has a reported score >=0.90 on a plagiarism or source-retrieval metric, not general AI-text detection",
        "2608.01046": "main comparison and class tables; fine-tuned DeBERTa AUC 0.9953/F1 0.976, RoBERTa F1 0.953, TF-IDF+LogReg AUC 0.936, and zero-shot DeBERTa machine recall above 0.90 despite poor balance",
        "2607.14967": "Tables 3 and 10; GTCL with both named embedding backbones and the DeTeCtive, Desklib, and TMR comparison rows each have a threshold metric >=0.90 on a reported slice",
        "2607.14905": "Tables 2-3 and 7-8; Longformer reaches 0.97/0.96 F1 in same-version original text, while each named reasoning-graph architecture is separately evaluated and claimed more robust/better across obfuscation or cross-version slices",
        "2606.31074": "Tables 3 and 5; every listed baseline, Triospect/base pairing, or named proxy/token-budget state has AUROC >=0.90 on at least one reported pre-attack, attacked, or efficiency slice",
        "2606.18946": "Tables 2 and 5; POGER AUC 0.938, SeqXGPT up to 0.950, SenDetEX macro F1 0.924, SenFlow 0.940, and each named SenFlow ablation has macro F1 0.922-0.935",
        "2605.27921": "Tables 5 and 7; TELL, MAGE, and Pangram EditLens exceed 0.90 aggregate AUROC, while ten additional named comparators cross 0.90 only on a domain slice and remain much weaker in aggregate",
        "2605.03723": "main segmentation comparisons; VCP and WCP are the separately named best change-point states under the paper's window-deviation criterion",
        "2605.02712": "official Task-10 result discussion; Qwen3-32B_ST at threshold 0.7 is the selected/best submission even though its macro result is below 0.90",
        "2604.25860": "Tables 1-3 and 6; Luminol-AIDetect is the claimed fast best/near-best method and the Binoculars and FastDetectGPT competitors have near-zero error on at least one RAID/domain cell",
        "2604.21365": "official task result tables; the named Gemma, CodeGemma, and Qwen-Coder submissions are the paper's best systems for Tasks A, B, and C respectively, all on machine-generated code rather than prose",
        "2604.21300": "Table 3; LUAR, Man-Nguyen, contrastive pretraining, and EAVAE each have pAUC@10 or pAUC@5 >=0.90 on at least one authorship-attribution slice",
        "2604.16923": "Tables 1-2, 5, 6, and 14; every listed baseline, alignment score, LAPD model-pair state, or qualifying supervised comparator has AUROC >=0.90 on a dataset/generator cell, while averages and low-FPR evidence vary",
        "2604.04932": "Tables 2-4; every listed baseline, RACE state, ablation, or parser configuration has AUROC, accuracy, or class F1 >=0.90 on a creator/editor slice of the four-way task",
        "2603.24981": "Tables 1-2; every listed baseline, Exons repair/amplification state, and model pair reaches AUROC >=0.90 on an M4, RAID, or RealDet cell",
        "2603.05617": "main classifier table; stylometric-only is explicitly competitive, curvature-only machine precision is 0.9417, and the full NOTAI ensemble reaches 0.9634 accuracy",
        "2602.15514": "Table 2; both XLM-RoBERTa and DependencyAI cross 0.90 on a language/domain accuracy or F1 cell, with weaker multilingual transfer",
        "2602.11871": "Table 1; FastDetectGPT and Binoculars with each Llama, Mistral, or Qwen scoring configuration cross 0.90 AUROC on a top-k/document-domain slice",
        "2511.17402": "machine-text classification table; RoBERTa-BNE has machine recall 0.9407 and PUCP-Metrix XGBoost is the toolkit's selected/best classifier despite lower aggregate performance",
        "2510.20610": "official Arabic shared-task table; XLM-RoBERTa is the paper's best submission at 0.7701 macro F1, below the general-detector threshold",
        "2510.16549": "Table VI; every named real-plus-synthetic trained backbone has precision, recall, or F1 >=0.90 on at least one real/synthetic peer-review test cell",
        "2510.12608": "Tables 2-3; the three comparison detectors and each named StyleDecipher representation cross 0.90 on a domain accuracy/F1 cell, with weaker transfer",
        "2510.00890": "Table 2; full Sci-SpanDet and all six component ablations report AUROC 0.9008-0.9263 on the span-level scientific-text task",
        "2509.25154": "Table 1 and Figure 4; four SLM states, three J-Detector learners, and two feature-removal states reach F1 or AUROC >=0.90 on a judgment dataset/group-size slice",
        "2509.15550": "main and appendix tables; every listed baseline, Revise-Detect comparator, repair order, and DNA-DetectLLM model pair has AUC/accuracy >=0.90 on a dataset/generator cell",
        "2509.00731": "Tables 2-4; RoBERTa/BERT/FastText development metrics exceed 0.90, Qwen LoRA ranks 4/8/16 score 0.9431/0.9376/0.9594 accuracy, and DeepSeek ranks 4/8/16 qualify by 0.9079 accuracy, 0.9008 AI F1, and 0.9293 accuracy",
        "2508.18715": "Tables 1-2 and 5; Random Forest/MLP, all six attribution-budget states, and all three utterance PLM states exceed 0.90 macro F1 on a dialogue dataset/task slice",
        "2508.01754": "main comparison; RADAR reaches 0.912 on Books and TDT reaches 0.900-0.919 on a level-3 nonstationarity slice",
        "2506.02959": "main and Appendix Table 16; each listed detector/statistic/backbone has a human- or machine-class F1 >=0.90 on at least one fine-grained coauthorship slice",
        "2505.14271": "Tables 1, 12, and 13; two baselines, FAID, three alternate encoders, and two alternate clusterers have accuracy/F1 >=0.90 on a known or unseen-generator slice",
        "2505.12507": "Tables 1, 7-18; every listed detector, LM2otifs tokenizer state, or graph ablation has AUC/accuracy >=0.90 on a domain/generator slice; DetectGPT alone never qualifies",
        "2505.05084": "Tables 2 and 7; vanilla, F1-maximized, Platt, isotonic, and MCP Binoculars thresholds each exceed 0.90 F1 on a reported calibration/evaluation slice",
        "2504.02873": "main comparisons; Short-PHD is the paper's explicitly best short-text state although its reported aggregate values stay below 0.90",
        "2503.00032": "main feature/classifier tables; the Exaone paraphrase detector and nine named KatFishNet feature-learner states cross 0.90 accuracy/F1 on a Korean corpus/domain cell",
        "2502.12734": "Tables 1-2; GREATER-D is the explicitly best defense, while query and zero-query GREATER-A are separately reported best/second-best attack states",
        "2502.12064": "Tables 4 and 6; the English GPT-2-small and multilingual GPT-2-XL threshold ensembles are the separately selected best GLTR configurations at 0.8019 and 0.6620 macro F1, below the high-accuracy threshold",
        "2502.11336": "Table 2 and datastore ablation; RoBERTa, LR-GLTR, DNA-GPT, and all three named ExaGPT datastore states cross 0.90 AUROC on a source/domain cell",
        "2502.04528": "Tables 3 and 8; FairOPT preserves about 0.90 dataset accuracy while reducing disparity, and Desklib with FairOPT or static thresholds crosses 0.90 accuracy/F1 on RAID/MAGE/SemEval slices",
        "2501.18998": "Table 1 and Appendix Table 5; unperturbed FastDetectGPT and each named embedding-attack state retain AUROC >=0.90 on at least one source/model black-box or white-box cell",
        "2501.14288": "Table I; DeBERTa, its three staged architecture/training states, and the final ensemble report AUC 91.2%-94.7%, while F1/Pearson are lower",
        "2501.11914": "Tables 4-5; the English and multilingual inverse-perplexity ensembles are the paper's separately selected best systems at 0.7458 and 0.7513 macro F1",
        "2606.04177": "Tables 2-15; the proposed linguistic-feature SVM reaches AUROC 0.968 in-domain and 0.907-0.945 in held-out settings, while the distinct MAGE baseline remains separately embedded",
    }
)

MECHANISM: dict[str, str] = {
    "2607.22026": "wavelet statistic or named hard/soft fusion over proxy-wavelet configurations",
    "2607.17382": "supervised large encoder classifier, with MCGrad calibration where named",
    "2607.03680": "supervised RoBERTa, few-shot FOMAML+LoRA adaptation, or confidence-weighted two-detector fusion",
    "2606.23336": "small-LM surprisal sequence transformed to spectral/wavelet features and classified by a CNN",
    "2606.07313": "steering-vector representation from the named probe LM, pool, and downstream rule",
    "2606.02158": "selective low-probability-token local/global uncertainty statistic",
    "2606.00402": "distribution-free knockoff filter applied to the named rewrite detector's target/rewrite score",
    "2605.25281": "Qwen2.5-1.5B SFT+GRPO detector queried in the named autoregressive prompting mode",
    "2605.16107": "named base detector enhanced by Markov calibration (-M) or multi-level contextual rule-support reasoning (-Mult)",
    "2605.06903": "supervised MELD detector under the paper-era or current-v5 recipe",
    "2605.02374": "few-shot RoBERTa trained with retrieval-guided adversarial generation and pairwise boundary contrastive loss",
    "2604.21223": "information-ratio metric from the named observer/performer model pair",
    "2606.00016": "CNN over proxy attention-attribution maps, optionally concatenated with text, under the named training arrangement",
    "2604.02008": "named detector aligned by nearest-neighbor proxy lookup or routed among retained proxy corpora",
    "2602.08031": "named score detector plus a fitted Markov-random-field calibration layer",
    "2602.01240": "learned prototype router selects a surrogate before applying the named zero-shot criterion",
    "2602.13226": "variation score over LLM rewrites, with optional rewrite-set expansion",
    "2601.20006": "named LM fine-tuned for token-level detection, or the named any-positive ensemble",
    "2601.04833": "named late-stage stability detector/statistic",
    "2601.04641": "named detector after differentially private entity sanitization of the target",
    "2601.03812": "supervised sequence classifier with the named architecture",
    "2511.21744": "supervised NEULIF linguistic-feature classifier with the named learner",
    "2511.01192": "supervised mixture-of-experts using the named routing objective/statistic",
    "2511.00988": "easy-to-hard supervised enhancement of the named detector, or its distilled student",
    "2509.22147": "supervised binary classifier using the named representation and learner/backbone",
    "2509.18880": "XGBoost over diversity features from the named proxy, optionally concatenated with a detector score",
    "2510.02319": "named supervised transformer; adversarial state adds augmented pairs; PIFE scores a canonicalized target discrepancy",
    "2509.14268": "DDL score with the named proxy plus reference clustering over retained examples",
    "2509.02499": "conditional threshold estimator using the named learner/base detector and retrieved stylistic references",
    "2509.00623": "row-specific RoBERTa fine-tune, TF-IDF LinearSVC, or custom Transformer over four Llama token-feature streams",
    "2508.13768": "supervised multi-scale spectral alignment with the named RoBERTa backbone",
    "2508.11933": "multi-agent LLM collaboration, routing, and confidence aggregation with the named backbone",
    "2508.11343": "spectral likelihood statistic, with the enhanced normalization/features in SpecDetect++",
    "2508.06913": "sentiment-distribution statistic over multiple sentiment-altering/semantic-preserving target rewrites",
    "2507.23577": "heavy-tailed score normalization, optionally combined in the two-dimensional CT framework",
    "2507.05157": "instruction-augmented fine-tuning of the named hosted or local model",
    "2506.15683": "family-aware probability features, contrastive learning, and mixture-of-experts with the named component removed",
    "2506.06705": "divergence score from the general or knowledge-distilled domain proxy",
    "2506.01702": "named supervised LM classifier, with the mdok robust fine-tuning recipe where named",
    "2505.15261": "multi-LLM-agent routing/guidelines/voting with the named component removed",
    "2505.13855": "named dense/MoE baseline or ensemble of domain experts; DoGEN uses learned top-2 domain routing",
    "2505.11550": "named supervised multi-encoder/stylometry architecture",
    "2504.21019": "RoBERTa trained with dynamically selected uniform or Gaussian perturbation noise",
    "2503.22338": "named classical classifier over seven-rewrite RAIDAR, NELA, or concatenated features",
    "2502.16857": "named DeBERTa size/data recipe, sequential fine-tune, or 60:40 ensemble",
    "2501.03940": "PAWN with the named backbone, branch-only ablation, or averaged-logit ensemble",
}

MECHANISM.update(
    {
        "2608.03859": "named plagiarism classifier, source-conditioned description-gain scorer, or source-retrieval/reranking pipeline",
        "2608.01046": "named directly supervised or zero-shot encoder/classical sequence classifier",
        "2607.14967": "named latent-trajectory, embedding-retrieval, or supervised comparison detector",
        "2607.14905": "Longformer text classifier or named graph neural network over extracted argumentative reasoning graphs",
        "2606.31074": "named zero-shot baseline or Triospect aggregation over target rewrites from multiple generation perspectives",
        "2606.18946": "named sentence-level sequential/graph detector or SenFlow component-ablation state",
        "2605.27921": "named supervised/explainable encoder classifier",
        "2605.03723": "named change-point segmentation method over a mixed human-machine document",
        "2605.02712": "supervised Qwen conspiracy classifier at the selected operating threshold",
        "2604.25860": "named zero-shot statistic; Luminol repeatedly shuffles the target before fitting perplexity-feature distributions",
        "2604.21365": "fine-tuned code-language model for the named shared-task code-detection subtask",
        "2604.21300": "named supervised/few-shot authorship representation evaluated on attribution pairs",
        "2604.16923": "named score baseline or alignment-preference discrepancy with the stated observer/performer pair",
        "2604.04932": "named supervised four-way creator/editor classifier or RACE graph/parser ablation",
        "2603.24981": "named baseline or Exons hidden-state discrepancy with the specified repair/amplification/model-pair state",
        "2603.05617": "stylometric classifier, conditional-curvature classifier, or their NOTAI probability ensemble",
        "2602.15514": "named supervised multilingual encoder with or without dependency-parse features",
        "2602.11871": "named zero-shot detector with the stated scorer/model pair, evaluated by the DMAP analysis",
        "2511.17402": "named Spanish machine-text classifier in the PUCP-Metrix toolkit",
        "2510.20610": "fine-tuned XLM-RoBERTa Arabic shared-task classifier",
        "2510.16549": "named supervised peer-review classifier trained on real plus LLM-augmented examples",
        "2510.12608": "named baseline or classical classifier over the stated StyleDecipher representation",
        "2510.00890": "Sci-SpanDet span classifier with the named structural/calibration component removed where specified",
        "2509.25154": "named judgment classifier or J-Detector learner/feature-ablation over judgment-group statistics",
        "2509.15550": "named baseline or DNA-inspired target mutation-and-LLM-repair configuration",
        "2509.00731": "named Chinese encoder/classical classifier or decoder fine-tuned with the stated LoRA rank",
        "2508.18715": "named dialogue classifier or EMMM selector-predictor with the stated attribution budget/backbone",
        "2508.01754": "named baseline or temporal-tomography statistic over ordered text windows",
        "2506.02959": "named fine-grained human/AI span or sentence classifier/statistic",
        "2505.14271": "named supervised baseline or FAID contrastive encoder plus vector-database clusterer configuration",
        "2505.12507": "named baseline or LM2otifs graph-motif classifier with the stated tokenizer/graph initialization",
        "2505.05084": "Binoculars with the named fixed, fitted, or conformal calibration rule",
        "2504.02873": "persistent-homology distance after inserting multiple off-topic generated continuations into the target",
        "2503.00032": "named Korean paraphrase detector or classical learner over the stated linguistic feature set",
        "2502.12734": "GREATER adversarially trained defense or its query/zero-query target-rewriting attack",
        "2502.12064": "GLTR rank-bin features combined by the selected GPT-2 threshold ensemble",
        "2502.11336": "named baseline or nearest-example detector using the stated datastore/index state",
        "2502.04528": "named base detector with static, ROC-derived, or group-adaptive FairOPT thresholds",
        "2501.18998": "FastDetectGPT before or after the stated token-replacement embedding attack",
        "2501.14288": "DeBERTa semantic-similarity architecture with the stated LSTM, attention, target-shuffling, or ensemble stage",
        "2501.11914": "inverse-perplexity soft-voting over the named English or multilingual encoder ensemble",
        "2606.04177": "support-vector machine over the paper's fixed linguistic feature representation",
    }
)

NO_ACCOUNT_REASONS: dict[str, str] = {
    "2607.23805": "Tables report survey-response distributions and downstream statistical effects, not a validated detector system, threshold metric, or claimed best detector.",
    "2605.14240": "The seven evaluated detectors peak at 0.8061 F1 before paraphrase and 0.6716 after attack; the paper claims attack degradation, not a new high-performing detector.",
    "2604.19768": "The experiments measure epistemic-rhetorical miscalibration in LLM outputs; no human-versus-machine detector, fitted detection state, or detector performance table is present.",
    "2510.22874": "The dataset paper's reported baseline is approximately 0.53 and no named detector configuration has a >=0.90 threshold metric or explicit best/high-performance claim.",
    "2505.15422": "Every tabulated study is from 2015-2024 and concerns author attribution/verification; tables are bibliographic taxonomies without result metrics, while isolated 92%-98% narratives concern older, differently scoped authorship tasks.",
    "2503.23622": "The paper evaluates assessment design and feedback rather than an AI-text detector; it contains no named detector result or threshold-performance table.",
}

# Result-specific evidence is required where one paper's configurations differ in
# metric boundary, mechanism, artifact status, or method-gate disposition.
RESULT_EVIDENCE: dict[str, str] = {
    "2501.03940:radar-ft": "Table 4 reproduces the RADAR-FT comparator at AUROC 0.99 in-domain, 0.97 out-of-domain, and 0.98 overall; these are prior-work comparison values rather than a PAWN artifact.",
    "2501.03940:m4-roberta-base": "Table 9 reports the authors' RoBERTa-base baseline after five training epochs on M4: mean out-of-domain AUROC 0.970, with individual domain cells as high as 1.000.",
    "2607.03680:vanilla-intellabs-base": "Table 5 reports the separately trained IntelLabs/base Vanilla state at 1.000 AUROC on its IntelLabs diagonal; several cross-corpus cells are much weaker.",
    "2607.03680:vanilla-mage-large": "Table 5 reports the separately trained MAGE/large Vanilla state at 0.982 AUROC on its MAGE diagonal; cross-corpus cells vary substantially.",
    "2607.03680:vanilla-faid-base": "Table 5 reports the separately trained FAID/base Vanilla state at 0.997 AUROC on its FAID diagonal; cross-corpus cells vary substantially.",
    "2607.03680:vanilla-mirage-large": "Table 5 reports the separately trained MIRAGE/large Vanilla state at 0.976 AUROC on its MIRAGE diagonal; cross-corpus cells vary substantially.",
    "2605.25281:imbd-read": "Table 2 reports ImBD trained on READ at 0.920 AUROC on the per-domain Gemma-2-9B slice but only 0.728 under one global threshold; per-domain and global thresholds are test-label oracle settings.",
    "2605.25281:imbd-target-adapted": "Table 14 reports target-adapted ImBD* at 0.929 mean AUROC across GPT-4o domains, with individual domain cells up to 0.980; adaptation uses labeled outputs from the same target generator in other domains.",
    "2605.06903:roberta-chatgpt-meld": "Appendix Table 9 reports the RoBERTa-ChatGPT same-data retrain at 99.93% MELD-eval AUROC and 99.85% Ghostbuster AUROC, but only 73.96% on M4GT.",
    "2605.06903:modernbert-detect-meld": "Appendix Table 9 reports the ModernBERT-Detect same-data retrain at 99.89% MELD-eval AUROC and 99.70% Ghostbuster AUROC, but only 76.30% on M4GT.",
    "2605.06903:repreguard-meld": "Appendix Table 9 reports the RepreGuard same-data retrain at 91.35% Ghostbuster AUROC, while MAGE, M4GT, DetectRL, and MELD-eval remain 56.09%-88.67%.",
    "2604.21223:reward-model-deberta": "Appendix Table 8 reports OpenAssistant RM-DeBERTa-v3-large-v2 at 95.49% AUROC on the Writing domain but only 73.08% average AUROC and 65.01% average F1.",
    "2606.00016:superannotate-roberta": "Tables 2 and 4 report the released SuperAnnotate RoBERTa detector at 98.35% AUC on the RAID Llama slice and 99.57% on HC3, while several unified, attacked, and external-transfer cells are much weaker.",
    "2505.14271:faid-unsup-simcse-xlmr": "Table 12 reports the UnSup-SimCSE-XLM-RoBERTa FAID encoder at 92.12% accuracy and 91.75% macro F1 on known generators, falling to 87.45%/86.90% on unseen generators.",
    "2511.21744:ai-generated-text-detection": "Table 3 reproduces a 99% result (F1 0.994) for the cited optimized transformer ensemble; NEULIF does not provide the primary experiment, dataset split, low-FPR result, or artifact.",
    "2511.21744:detective-comparator": "Table 3 reproduces 96% average recall for DeTeCtive and the discussion describes roughly 96%-99% cross-domain recall; these are literature values rather than a NEULIF-run comparison.",
    "2511.21744:restricted-embeddings": "Table 3 reproduces 91%-95% for Restricted Embeddings and describes in-domain performance plus OOD gains without a common dataset, split, or metric denominator.",
    "2511.21744:chatgpt-detector": "Table 3 reproduces 98%-99% for a fine-tuned CamemBERTa/XLM-R ChatGPT detector and immediately notes substantial degradation on novel or adversarial text.",
    "2511.21744:roberta-bilstm": "Table 3 reproduces 97% open-set performance for a fine-tuned RoBERTa+BiLSTM system; no common NEULIF dataset, low-FPR comparison, artifact, or timing is supplied.",
    "2511.21744:styloai-education": "The Table 3 footnote and adjacent discussion report 98% for StyloAI on fewer than 200 Education examples but only 81% on the 55,677-example AuTextification dataset, explicitly warning of overfitting.",
    "2509.18880:e5-small-lora": "Table 2 reports the fitted e5-small-lora classifier at 93.9% accuracy and 0.986 AUROC on RAID; Table 13 reports high attack-table percentages but no matched low-FPR transfer result.",
    "2509.18880:desklib": "Table 2 reports Desklib AI at 94.9% accuracy and 0.973 AUROC on RAID; appendix attack rows vary and this paper supplies no new frozen Desklib state.",
    "2509.18880:superannotate": "Table 2 reports SuperAnnotate at 70.3% accuracy but 0.910 AUROC on RAID; the high threshold-independent value is accompanied by weak fixed-threshold balance.",
    "2506.15683:roberta-baseline": "Table 3 reports RoBERTa machine-class F1 of 98.47%-97.67% on arXiv but macro F1 of only 79.67%-82.83; Q&A balance is also below 0.90 macro F1.",
    "2506.15683:t5-sentinel-baseline": "Table 3 reports T5-Sentinel machine-class F1 of 98.95%-99.19% on arXiv while every macro F1 remains below 0.90.",
    "2506.15683:detective-baseline": "Table 3 reports DeTeCtive machine-class F1 up to 99.39% and macro F1 up to 94.19; the implementation selects K from validation examples with a KNN retrieval rule.",
    "2506.15683:seqxgpt-baseline": "Table 3 reports SeqXGPT machine-class F1 up to 99.46% and macro F1 up to 93.47, using three white-box proxy probability streams.",
    "2506.15683:dna-gpt-baseline": "Table 3 reports a 99.00% machine-class F1 slice for DNA-GPT but macro F1 of at most 86.04; the experiment uses ten target continuations.",
    "2506.15683:detectgpt-baseline": "Table 3 reports DetectGPT machine-class F1 up to 98.31% but macro F1 of at most 78.38; the experiment uses 100 perturbations per target.",
    "2506.15683:fastdetectgpt-baseline": "Table 3 reports Fast-DetectGPT machine-class F1 up to 99.68% and macro F1 up to 95.25, with lower balance on other slices.",
    "2506.15683:hastewire": "Table 5 reports HasteWire machine-class F1 of 97.50% but human-class F1 of 65.01%, macro F1 of 81.26%, and TPR at 1% FPR of 69.90%.",
    "2506.06705:without-adaptation": "Figure 4 reports the named no-domain-adaptation DivScore baseline with a qualifying averaged AUROC cell but materially weaker medical/legal/combined adaptation results.",
    "2506.06705:divscore-mistral": "Appendix Table 4 reports DivScore with Mistral at 99.04%-99.96% AUROC across the four source-LLM columns and 99.72% average.",
    "2506.06705:divscore-falcon": "Appendix Table 4 reports DivScore with Falcon at 95.87%-99.70% AUROC and 98.46% average.",
    "2506.06705:divscore-qwen": "Appendix Table 4 reports DivScore with Qwen at 94.43%-99.96% AUROC and 97.79% average.",
    "2506.06705:divscore-llama": "Appendix Table 4 reports DivScore with Llama at 99.03%-99.91% AUROC and 99.67% average.",
    "2506.06705:entropy-mistral": "Appendix Table 4 reports Entropy with Mistral at 85.43%-99.78% AUROC and 95.95% average.",
    "2506.06705:entropy-falcon": "Appendix Table 4 reports Entropy with Falcon at 89.34%-99.49% AUROC and 95.41% average.",
    "2506.06705:entropy-qwen": "Appendix Table 4 reports Entropy with Qwen at 89.03%-99.88% AUROC and 96.78% average.",
    "2506.06705:entropy-llama": "Appendix Table 4 reports Entropy with Llama at 86.75%-99.89% AUROC and 95.94% average.",
    "2506.06705:cross-entropy-qwen": "Appendix Table 4 reports Cross-Entropy with Qwen at 94.97% on one source-LLM column but only 49.23% average.",
    "2509.00623:roberta-base": "Table 1 test: RoBERTa-base accuracy/F1 is 99.99%/99.99% on news and 100.00%/100.00% on academic abstracts; it is the selected primary submission.",
    "2509.00623:tfidf-svm": "Table 1 test: TF-IDF+SVM accuracy/F1 is 97.90%/97.91% on news and 99.85%/99.85% on academic abstracts.",
    "2509.00623:candace": "Table 1 test: Candace accuracy/F1 is 99.75%/99.75% on news and 99.95%/99.95% on academic abstracts; the paper says its multiple-Llama feature pass is slower.",
    "2503.22338:svc-raidar": "Table 2 development F1 is 0.9573 Task A and 0.5403 Task B for SVC with seven-rewrite RAIDAR features; no SVC test row is reported.",
    "2503.22338:svc-nela": "Table 2 development F1 is 0.9205 Task A and 0.4585 Task B for SVC with NELA features; no SVC test row is reported.",
    "2503.22338:svc-combined": "Table 2 development F1 is 0.9268 Task A and 0.4337 Task B for SVC with RAIDAR+NELA features; no SVC test row is reported.",
    "2503.22338:rf-raidar": "Table 2 development F1 is 0.9548 Task A and 0.5283 Task B for Random Forest with seven-rewrite RAIDAR features; no Random Forest test row is reported.",
    "2503.22338:rf-nela": "Table 2 development F1 is 0.9942 Task A and 0.8061 Task B for Random Forest with NELA features; no Random Forest test row is reported.",
    "2503.22338:rf-combined": "Table 2 development F1 is 0.9933 Task A and 0.7754 Task B for Random Forest with RAIDAR+NELA features; no Random Forest test row is reported.",
    "2503.22338:xgb-raidar": "Tables 2-3: XGBoost+RAIDAR F1 is 0.9652/0.5719 on development and 0.9454/0.4410 on test for Tasks A/B.",
    "2503.22338:xgb-nela": "Tables 2-3: XGBoost+NELA F1 is 0.9979/0.8489 on development and 0.9945/0.7615 on test for Tasks A/B.",
    "2503.22338:xgb-combined": "Tables 2-3: XGBoost+RAIDAR+NELA F1 is 0.9968/0.8430 on development and 0.9917/0.7443 on test for Tasks A/B.",
    "2502.16857:original-xsmall": "Table 2 test: original-data DeBERTa-v3-xsmall F1 is 0.9521 Task A and 0.2418 Task B.",
    "2502.16857:original-small": "Table 2 test: original-data DeBERTa-v3-small F1 is 0.9985 Task A and 0.2885 Task B.",
    "2502.16857:original-base": "Table 2 test: original-data DeBERTa-v3-base F1 is 0.9515 Task A and 0.4322 Task B.",
    "2502.16857:noised-xsmall": "Table 4 test: noised-data DeBERTa-v3-xsmall F1 is 0.9985 Task A and 0.6382 Task B.",
    "2502.16857:noised-small": "Table 4 test: noised-data DeBERTa-v3-small F1 is 1.0000 Task A and 0.9454 Task B.",
    "2502.16857:noised-base": "Table 4 test: noised-data DeBERTa-v3-base F1 is 0.9989 Task A and 0.6570 Task B.",
    "2502.16857:double-small": "Table 4 test: sequentially double-finetuned DeBERTa-v3-small reports 0.9167 Task-B F1; Task-A is not reported for this row.",
    "2502.16857:ensemble-small": "Table 4 test: the 60:40 noised-small/double-finetuned ensemble reports 0.9531 Task-B F1; Task-A is reported only for the best-submission combination.",
    "2507.05157:gpt4o-mini": "Tables 4 and 6: GPT-4o-mini Task-A macro F1 is 0.97 on validation and 0.9547 on the unseen test; about 200 test calls were content-filtered.",
    "2507.05157:bert": "Tables 4-6: BERT validation F1 is 1.00 on Task A and about 0.98 macro on Task B, but unseen-test F1 falls to 0.7670 and 0.4698.",
    "2507.05157:llama3-8b": "Tables 4-6: Llama-3-8B validation macro F1 is 0.89 on Task A and 0.93 on Task B, while unseen-test Task-B F1 is 0.14.",
    "2605.27921:fastdetectgpt": "Tables 5 and 7: aggregate AUROC is 0.8609, but per-domain AUROC reaches 0.965 on educational web, 0.919 on email, 0.986 on finance, and 0.914 on student essays.",
    "2605.27921:argugpt": "Tables 5 and 7: aggregate AUROC is 0.8281, but per-domain AUROC reaches 0.926 on educational web, 0.989 on email, 0.997 on finance, and 0.990 on student essays.",
    "2605.27921:t5-sentinel": "Tables 5 and 7: aggregate AUROC is 0.8020, but per-domain AUROC reaches 1.000 on web text and 0.948 on student essays.",
    "2605.27921:detectllm-npr": "Tables 5 and 7: aggregate AUROC is 0.7824, but per-domain AUROC reaches 0.956 on email, 0.987 on finance, and 0.967 on student essays.",
    "2605.27921:openai-roberta": "Tables 5 and 7: aggregate AUROC is 0.7770, but per-domain AUROC reaches 0.986 on finance and 0.945 on student essays.",
    "2605.27921:aigc-mpu": "Tables 5 and 7: aggregate AUROC is 0.7741, but per-domain AUROC reaches 0.947 on educational web, 0.991 on email, and 0.979 on student essays.",
    "2605.27921:detectllm-lrr": "Tables 5 and 7: aggregate AUROC is 0.7627, but per-domain AUROC reaches 0.931 on email, 0.976 on finance, and 0.909 on student essays.",
    "2605.27921:logrank-gpt2-medium": "Tables 5 and 7: aggregate AUROC is 0.7573, but per-domain AUROC reaches 0.943 on email, 0.981 on finance, and 0.941 on student essays.",
    "2605.27921:radar": "Tables 5 and 7: aggregate AUROC is 0.7441, but per-domain AUROC reaches 0.956 on educational web, 0.913 on encyclopedic reference, and 0.919 on student essays.",
    "2605.27921:chatgpt-d": "Tables 5 and 7: aggregate AUROC is 0.6972, but the finance-domain AUROC is 1.000.",
    "2604.16923:remodetect": "Table 14: ReMoDetect reaches 92.18% AUROC on RealDet but only 80.82% on average over the five benchmark columns.",
    "2604.16923:imbd": "Table 14: ImBD reaches 92.12% AUROC on RealDet but only 83.27% on average over the five benchmark columns.",
    "2601.04833:likelihood": "Tables 3 and 6: Likelihood reaches 91.30% AUROC on GLM and 92.96% on LLaMA within MAGE, but averages 56.81% on MAGE and 77.44% on EvoBench.",
    "2601.04833:logrank": "Tables 3 and 6: Log-Rank reaches 90.28% AUROC on GLM and 91.69% on LLaMA within MAGE, but averages 55.91% on MAGE and 75.37% on EvoBench.",
    "2601.04833:fastdetectgpt": "Table 3: FastDetectGPT reaches 94.17% AUROC on the EvoBench LLaMA-3 slice but averages 79.85% on EvoBench and 69.69% on MAGE.",
    "2601.04833:lastde": "Table 3: Lastde reaches 90.80% AUROC on the EvoBench LLaMA-3 slice but averages 76.66% on EvoBench and 70.71% on MAGE.",
    "2601.04833:diveye": "Table 6: DivEye reaches 92.61% AUROC on GLM and 93.80% on LLaMA within MAGE but averages 69.60% on MAGE and 74.40% on EvoBench.",
    "2509.15550:biscope": "Tables 1-2: BiScope reaches 99.74% AUROC on the Arxiv/Gemini cell but averages 91.17% over nine in-domain cells and 82.28% over four public benchmarks.",
    "2509.15550:entropy": "Tables 1-2: Entropy reaches 91.17% AUROC on one WritingPrompts cell but averages 75.26% over nine in-domain cells and 67.82% over four public benchmarks.",
    "2509.15550:likelihood": "Tables 1-2: Likelihood reaches 95.52% AUROC on one WritingPrompts cell but averages 78.87% over nine in-domain cells and 71.73% over four public benchmarks.",
    "2509.15550:logrank": "Tables 1-2: LogRank reaches 94.53% AUROC on one WritingPrompts cell but averages 78.26% over nine in-domain cells and 72.91% over four public benchmarks.",
    "2509.15550:detectgpt": "Tables 1-2: DetectGPT reaches 92.18% AUROC on one Arxiv cell but averages 74.42% over nine in-domain cells and 59.02% over four public benchmarks.",
    "2509.15550:fastdetectgpt": "Tables 1-2: FastDetectGPT averages 96.20% AUROC over nine in-domain cells but only 85.07% over four public benchmarks.",
    "2509.15550:binoculars": "Tables 1-2: Binoculars averages 97.39% AUROC over nine in-domain cells and 86.08% over four public benchmarks.",
    "2509.15550:lastde-plus": "Tables 1-2: Lastde++ averages 94.90% AUROC over nine in-domain cells but only 82.00% over four public benchmarks.",
    "2509.15550:dna-default": "Tables 1-2: default DNA-DetectLLM averages 98.30% AUROC over nine in-domain cells and 90.86% over four public benchmarks.",
    "2509.15550:dna-low-high": "Table 1: the DNA-DetectLLM low-to-high repair order averages 97.43% AUROC over nine dataset/generator cells.",
    "2509.15550:dna-high-low": "Table 1: the DNA-DetectLLM high-to-low repair order averages 98.16% AUROC over nine dataset/generator cells.",
    "2509.15550:dna-sequential": "Table 1: the DNA-DetectLLM sequential repair order averages 98.23% AUROC over nine dataset/generator cells.",
    "2509.15550:dna-mistral": "Figure 6 evaluates the Mistral DNA-DetectLLM observer/reference pair; the text says all four pairs beat the baselines and the best plotted pair reaches 92.4% and 90.7% AUROC on the plotted tasks.",
    "2509.15550:dna-llama2": "Figure 6 evaluates the Llama-2 DNA-DetectLLM observer/reference pair; the text says all four pairs beat the baselines and the best plotted pair reaches 92.4% and 90.7% AUROC on the plotted tasks.",
    "2509.15550:dna-llama3": "Figure 6 evaluates the Llama-3 DNA-DetectLLM observer/reference pair; the text says all four pairs beat the baselines and the best plotted pair reaches 92.4% and 90.7% AUROC on the plotted tasks.",
    "2504.21019:uniform": "Table 2: training-time uniform-noise DP-Net reaches 96.88% accuracy on Wikipedia/ChatGPT but averages 85.48% over seven unseen domains.",
    "2504.21019:gaussian": "Table 2: training-time Gaussian-noise DP-Net reaches 96.04% accuracy on Wikipedia/ChatGPT but averages 86.10% over seven unseen domains.",
}

RESULT_EVIDENCE.update(
    {
        "2511.01192:domain-f1": "Figure 4 plots the Domain-Matching (F1) routing series and labels its selected value 91.4; Tables 3, 6, and 8 give the downstream domain/length evidence.",
        "2511.01192:domain-entropy": "Figure 4 plots the Domain-Matching (Entropy) routing series and labels its selected value 1.05; Tables 3, 6, and 8 give the downstream domain/length evidence.",
        "2511.01192:reward-f1": "Figure 4 plots the Reward-Driven (F1) routing series and labels its selected value 94.1; Tables 3, 6, and 8 give the downstream domain/length evidence.",
        "2511.01192:reward-entropy": "Figure 4 plots the Reward-Driven (Entropy) routing series and labels its selected value 0.39; Tables 3, 6, and 8 give the downstream domain/length evidence.",
        "2605.02712:qwen3-32b-st-07": "Table 1 reports Qwen3-32B_ST_th0.7 at macro F1 0.78; it is the separately selected Task-10 submission but does not qualify as a high-accuracy result.",
        "2605.02374:react-32shot": "Table 1, DetectRL 32-shot row: REACT accuracy is 99.46% (99.46% F1).",
        "2605.02374:react-64shot": "Table 1, DetectRL 64-shot row: REACT accuracy is 99.82% (99.82% F1).",
        "2605.02374:react-128shot": "Table 1, DetectRL 128-shot row: REACT accuracy is 99.74% (99.74% F1).",
        "2605.02374:react-256shot": "Table 1, DetectRL 256-shot row: REACT accuracy is 99.79% (99.79% F1).",
        "2502.12734:greater-d": "Table 1: GREATER-D has 1.78% average ASR under text perturbations and 12.42% under adversarial attacks, both best among the compared defenses.",
        "2502.12734:greater-a-query": "Table 2 query-based row: GREATER-A reaches 96.58% ASR with 62.63 average queries.",
        "2502.12734:greater-a-zero-query": "Table 2 zero-query row: GREATER-A reaches 69.11% ASR.",
        "2502.12064:english-gpt2-small": "Table 4 reports the selected English GPT-2-small GLTR threshold ensemble at 0.8019 macro F1; it is separately disposed but below the high-accuracy threshold.",
        "2502.12064:multilingual-gpt2-xl": "Table 6 reports the selected multilingual GPT-2-XL GLTR threshold ensemble at 0.6620 macro F1; it is separately disposed but below the high-accuracy threshold.",
        "2501.11914:inverse-perplexity-en": "Table 5 reports the selected English Inverse Perplexity ensemble at 0.7458 macro F1; it is separately disposed but below the high-accuracy threshold.",
        "2501.11914:inverse-perplexity-multi": "Table 5 reports the selected multilingual Inverse Perplexity ensemble at 0.7513 macro F1; it is separately disposed but below the high-accuracy threshold.",
        "2501.03940:ens-2gpt2": "Table 8: the two-GPT-2 PAWN ensemble reports 0.983 AUROC in-distribution and 0.943 on the wilderness testbeds.",
        "2501.03940:m4-xlm-roberta": "Table 9 reports the fitted XLM-RoBERTa M4 comparator at 92.18% accuracy and 92.12% macro F1 on Arabic, and 94.39% on both metrics for Urdu; AUROC is not reported for this column.",
        "2607.22026:window-std": "Table 7 reports the strongest window_std state on HC3 at 0.7137 AUROC, 0.5835 AUPRC, 0.7640 F1, and 0.0000 TPR at 1% FPR. It is retained as an individually disposed proposed state, not as a threshold-qualifying high-accuracy result.",
        "2510.16549:qwen3-rs": "Table VI reports the Qwen 3-8B real-plus-synthetic state with 0.9034 precision on the Multi-DR R+S test column; its recall and F1 on that cell are 0.8504 and 0.8738, and its binary-task F1 peaks at 0.8068.",
        "2605.16107:likelihood": "Table III reports the unmodified Likelihood baseline at 95.58% average AUROC on Essay and 90.17% on TruthfulQA.",
        "2605.16107:logrank": "Table III reports the unmodified Log-Rank baseline at 95.39% average AUROC on Essay; its TruthfulQA average is 89.37%.",
        "2605.16107:entropy": "Table III reports the unmodified Entropy baseline with 96.02% AUROC on the TruthfulQA/ChatGLM slice, while the two benchmark averages are 81.53% and 88.23%.",
        "2605.16107:detectgpt": "Table III reports the unmodified DetectGPT baseline at 92.84% AUROC on two TruthfulQA generator slices, while the Essay and TruthfulQA averages are 49.33% and 84.07%.",
        "2605.16107:fastgpt": "Table III reports the unmodified FastGPT baseline at 96.26% AUROC on TruthfulQA/ChatGLM, while the Essay and TruthfulQA averages are 65.17% and 89.34%.",
        "2605.16107:binoculars": "Table III reports the unmodified Binoculars baseline at 97.36% average AUROC on Essay and 86.97% on TruthfulQA.",
        "2605.16107:fouriergpt": "Table III reports the unmodified FourierGPT baseline at 90.23% average AUROC on Essay and 92.68% on TruthfulQA, with one Essay generator cell at 52.38%.",
        "2605.16107:adagpt": "Table III reports the unmodified AdaGPT baseline at 92.69% AUROC on Essay/ChatGLM and 96.67% on TruthfulQA/ChatGLM, while the averages are 82.81% and 88.19%.",
        "2604.02008:likelihood": "Table III reports the unaligned Likelihood comparator at 0.907 AUROC on the GPT-3.5 slice but only 0.808 average on Mix8.",
        "2604.02008:logrank": "Table III reports the unaligned LogRank comparator at 0.906 AUROC on GPT-3.5 and 0.904 on Gemini-1.5 Pro but only 0.808 average on Mix8.",
        "2604.02008:fastdetectgpt": "Table III reports unaligned FastDetectGPT at 0.900-0.955 on four Mix8 source slices and 0.893 average.",
        "2604.02008:binoculars": "Table III reports unaligned Binoculars at 0.920-0.994 across the eight Mix8 source slices and 0.974 average.",
        "2604.02008:fastdetectgpt-dald": "Table III reports FastDetectGPT+DALD at 0.923 average AUROC on Mix8, with source-specific values from 0.811 to 0.981.",
        "2604.02008:fastdetectgpt-glimpse-gpt4-geometric": "Table III reports FastDetectGPT+Glimpse with the GPT-4 API and geometric reconstruction at 0.895-0.982 AUROC on the five available Mix8 source slices; three cells are unavailable.",
        "2604.02008:fastdetectgpt-glimpse-gpt4-zipfian": "Table III reports FastDetectGPT+Glimpse with the GPT-4 API and Zipfian reconstruction at 0.899-0.979 AUROC on the five available Mix8 source slices; three cells are unavailable.",
        "2604.02008:fastdetectgpt-glimpse-gpt4-mlp": "Table III reports FastDetectGPT+Glimpse with the GPT-4 API and MLP reconstruction at 0.900-0.981 AUROC on the five available Mix8 source slices; three cells are unavailable.",
        "2604.02008:fastdetectgpt-glimpse-davinci-geometric": "Table III reports FastDetectGPT+Glimpse with the DaVinci-002 API and geometric reconstruction at 0.930 average AUROC on Mix8.",
        "2604.02008:binoculars-dald": "Table III reports Binoculars+DALD at 0.866 average AUROC on Mix8 despite individual source cells up to 0.960.",
        "2510.02319:fastdetectgpt": "Table VIII reports FastDetectGPT at 0.972 AUROC and 0.813 TPR at 1% FPR on the non-adversarial split, falling to 0.492-0.635 AUROC on the attack mixes.",
        "2510.02319:glimpse": "Table VIII reports Glimpse at 0.965 AUROC and 0.790 TPR at 1% FPR on the non-adversarial split, falling to 0.474-0.618 AUROC on the attack mixes.",
        "2510.02319:binoculars": "Table VIII reports Binoculars at 0.985 AUROC and 0.857 TPR at 1% FPR on the non-adversarial split, falling to 0.553-0.662 AUROC on the attack mixes.",
        "2510.02319:logrank": "Table VIII reports LogRank at 0.921 AUROC and 0.682 TPR at 1% FPR on the non-adversarial split, falling to 0.396-0.534 AUROC on the attack mixes.",
        "2508.11933:raidar": "Table I reports the RAIDAR baseline at 90.11% F1 and 90.46% accuracy on Code, while its four other domain F1 values are 63.18%-82.56%.",
        "2508.11933:gpt4o-direct": "Table I reports direct GPT-4o prompting at 93.05% F1 and 93.21% accuracy on Code, while its four other domain F1 values are 70.53%-86.81%.",
        "2508.11933:gpt-cot": "Table I reports GPT+CoT at 93.64% F1 and 93.88% accuracy on Code, while its four other domain F1 values are 71.89%-87.44%.",
        "2508.11933:gpt-react": "Table I reports GPT+ReAct at 94.27% F1 and 94.51% accuracy on Code, while its four other domain F1 values are 72.52%-88.07%.",
        "2508.11933:gpt35": "Figure 4 reports the CAMF GPT-3.5-Turbo backbone at 95.18% F1 on Code; the figure provides no low-FPR result or uncertainty interval.",
        "2508.11933:gpt4o": "Figure 4 reports the CAMF GPT-4o backbone at 98.49% F1 on Code; the figure provides no low-FPR result or uncertainty interval.",
        "2508.11933:llama3-70b": "Figure 4 reports the CAMF Llama3-70B backbone at 96.64% F1 on Code; the figure provides no low-FPR result or uncertainty interval.",
        "2508.11933:gpt4o-mini": "Figure 4 reports the CAMF GPT-4o-mini backbone at 96.89% F1 on Code; the figure provides no low-FPR result or uncertainty interval.",
        "2508.11933:gemini15-pro": "Figure 4 reports the CAMF Gemini-1.5 Pro backbone at 96.45% F1 on Code; the figure provides no low-FPR result or uncertainty interval.",
        "2508.11933:deepseek-v3": "Figure 4 reports the CAMF DeepSeek-V3 backbone at 95.60% F1 on Code; the figure provides no low-FPR result or uncertainty interval.",
    }
)

for slug, system in PRIMARY_GROUPS["2601.20006"]:
    account_id = f"2601.20006:{slug}"
    if slug == "external-deberta":
        table = "8"
    elif slug.startswith("master-"):
        table = "9"
    elif slug.startswith("gpt41nano-"):
        table = "10"
    elif slug.startswith("self-"):
        table = "11"
    elif slug == "ensemble-per-llm":
        table = "12"
    elif slug.startswith("family-"):
        table = "13"
    elif slug == "ensemble-per-family":
        table = "14"
    else:
        raise ValueError(f"unmapped 2601.20006 account: {account_id}")
    RESULT_EVIDENCE[account_id] = (
        f"Table {table} reports the {system} row with accuracy, F1, AUC, or recall "
        ">=0.90 on its named master, validation, self-model, family, or ensemble "
        "evaluation; this is not a shared disposition inherited from another row."
    )

RESULT_MECHANISM: dict[str, str] = {
    "2501.03940:radar-ft": "the prior RADAR adversarially trained RoBERTa detector after the paper's named fine-tuning setting",
    "2501.03940:m4-roberta-base": "a directly supervised RoBERTa-base sequence classifier trained by the PAWN authors on M4 for five epochs",
    "2607.03680:vanilla-intellabs-base": "a RoBERTa-base sequence classifier fitted separately on IntelLabs",
    "2607.03680:vanilla-mage-large": "a RoBERTa-large sequence classifier fitted separately on MAGE",
    "2607.03680:vanilla-faid-base": "a RoBERTa-base sequence classifier fitted separately on FAID",
    "2607.03680:vanilla-mirage-large": "a RoBERTa-large sequence classifier fitted separately on MIRAGE",
    "2605.25281:imbd-read": "the ImBD proxy language model fine-tuned toward machine-text preference on the READ training split",
    "2605.25281:imbd-target-adapted": "the ImBD proxy language model fine-tuned with labeled samples from the target generator on other READ domains",
    "2605.06903:roberta-chatgpt-meld": "the official RoBERTa-ChatGPT architecture and training recipe refitted on MELD's training mixture",
    "2605.06903:modernbert-detect-meld": "the official ModernBERT-Detect architecture and training recipe refitted on MELD's training mixture",
    "2605.06903:repreguard-meld": "the official RepreGuard architecture and training recipe refitted on MELD's training mixture",
    "2604.21223:reward-model-deberta": "the public OpenAssistant DeBERTa-v3-large reward model used directly as a machine-text score",
    "2606.00016:superannotate-roberta": "the released SuperAnnotate RoBERTa sequence classifier",
    "2505.14271:faid-unsup-simcse-xlmr": "the FAID multi-task contrastive detector using an UnSup-SimCSE-XLM-RoBERTa encoder and its retained vector database",
    "2511.21744:ai-generated-text-detection": "the cited optimized neural transformer ensemble, as described only by NEULIF's secondary comparison",
    "2511.21744:detective-comparator": "the cited DeTeCtive contrastive encoder followed by KNN lookup over retained training embeddings; NEULIF supplies only a secondary comparison value",
    "2511.21744:restricted-embeddings": "the cited transformer detector after embedding-subspace pruning, as described only by NEULIF's secondary comparison",
    "2511.21744:chatgpt-detector": "the cited fine-tuned CamemBERTa/XLM-R transformer classifier, as described only by NEULIF's secondary comparison",
    "2511.21744:roberta-bilstm": "the cited fine-tuned RoBERTa representation followed by a bidirectional LSTM classifier",
    "2511.21744:styloai-education": "the cited StyloAI Random Forest over stylometric features on its small Education split",
    "2509.18880:e5-small-lora": "the released or cited e5-small representation with a fitted low-rank classification head",
    "2509.18880:desklib": "the cited Desklib AI directly supervised sequence classifier",
    "2509.18880:superannotate": "the cited SuperAnnotate directly supervised RoBERTa sequence classifier",
    "2506.15683:roberta-baseline": "the paper's directly supervised RoBERTa black-box comparison classifier",
    "2506.15683:t5-sentinel-baseline": "the paper's supervised T5-Sentinel text-to-text comparison classifier",
    "2506.15683:detective-baseline": "the paper's DeTeCtive contrastive encoder followed by validation-set KNN retrieval",
    "2506.15683:seqxgpt-baseline": "the SeqXGPT CNN/attention detector over white-box token-probability streams from three named proxy LMs",
    "2506.15683:dna-gpt-baseline": "DNA-GPT scoring over ten generated continuations of each target",
    "2506.15683:detectgpt-baseline": "DetectGPT curvature estimated from 100 perturbed versions of each target",
    "2506.15683:fastdetectgpt-baseline": "Fast-DetectGPT conditional-probability curvature with GPT-Neo-2.7B as sampling and scoring model",
    "2506.15683:hastewire": "the closed HasteWire API detector service",
    "2506.06705:without-adaptation": "the DivScore scoring architecture before medical/legal domain-knowledge distillation",
    "2506.06705:divscore-mistral": "the DivScore divergence score computed with the Mistral detector LM",
    "2506.06705:divscore-falcon": "the DivScore divergence score computed with the Falcon detector LM",
    "2506.06705:divscore-qwen": "the DivScore divergence score computed with the Qwen detector LM",
    "2506.06705:divscore-llama": "the DivScore divergence score computed with the Llama detector LM",
    "2506.06705:entropy-mistral": "mean token entropy computed with the Mistral detector LM",
    "2506.06705:entropy-falcon": "mean token entropy computed with the Falcon detector LM",
    "2506.06705:entropy-qwen": "mean token entropy computed with the Qwen detector LM",
    "2506.06705:entropy-llama": "mean token entropy computed with the Llama detector LM",
    "2506.06705:cross-entropy-qwen": "the paper's cross-entropy scoring ablation computed with the Qwen detector LM",
    "2509.00623:roberta-base": "a directly fine-tuned RoBERTa-base sequence classifier",
    "2509.00623:tfidf-svm": "a TF-IDF representation classified by a linear support-vector machine",
    "2509.00623:candace": "a custom Transformer over token features extracted from four Llama models",
    "2507.05157:gpt4o-mini": "instruction fine-tuning of hosted GPT-4o-mini version 2024-08-01-preview",
    "2507.05157:bert": "direct supervised BERT fine-tuning with a 512-token maximum",
    "2507.05157:llama3-8b": "four-bit low-rank fine-tuning of Llama-3-8B with an 8,000-token configured sequence length",
    "2605.27921:fastdetectgpt": "the FastDetectGPT conditional-probability-curvature statistic",
    "2605.27921:argugpt": "the named supervised argumentative-essay classifier",
    "2605.27921:t5-sentinel": "the named supervised T5 text-to-text detector",
    "2605.27921:detectllm-npr": "DetectLLM normalized perturbed log-rank over multiple target-text perturbations",
    "2605.27921:openai-roberta": "the named directly supervised OpenAI RoBERTa detector",
    "2605.27921:aigc-mpu": "the named multi-scale positive-unlabeled classifier",
    "2605.27921:detectllm-lrr": "the DetectLLM log-likelihood/log-rank-ratio statistic",
    "2605.27921:logrank-gpt2-medium": "average token log-rank under GPT-2-medium",
    "2605.27921:radar": "the named adversarially trained supervised RADAR detector",
    "2605.27921:chatgpt-d": "the named supervised ChatGPT text detector",
    "2604.16923:remodetect": "the training-dependent ReMoDetect reward-model detector for aligned-model generations",
    "2604.16923:imbd": "the ImBD proxy language model fine-tuned toward machine-text preference",
    "2601.04833:likelihood": "mean token likelihood under the common surrogate language model",
    "2601.04833:logrank": "mean token log-rank under the common surrogate language model",
    "2601.04833:fastdetectgpt": "the FastDetectGPT conditional-probability-curvature statistic",
    "2601.04833:lastde": "the Lastde detector over discriminative local subsequences in token-probability series",
    "2601.04833:diveye": "the DivEye statistic over diversity patterns in surprisal fluctuations",
}
for _result_id in (
    "2503.22338:svc-raidar",
    "2503.22338:svc-combined",
    "2503.22338:rf-raidar",
    "2503.22338:rf-combined",
    "2503.22338:xgb-raidar",
    "2503.22338:xgb-combined",
):
    RESULT_MECHANISM[_result_id] = (
        "the named classical classifier over RAIDAR features produced by seven target-text rewrites, optionally concatenated with NELA"
    )
for _result_id in (
    "2503.22338:svc-nela",
    "2503.22338:rf-nela",
    "2503.22338:xgb-nela",
):
    RESULT_MECHANISM[_result_id] = (
        "the named classical classifier over the non-rewrite NELA feature set"
    )
for _slug in (
    "original-xsmall",
    "original-small",
    "original-base",
    "noised-xsmall",
    "noised-small",
    "noised-base",
    "double-small",
    "ensemble-small",
):
    RESULT_MECHANISM[f"2502.16857:{_slug}"] = (
        "the row-specific DeBERTa size and original/noised training recipe, sequential fine-tune, or 60:40 logit ensemble"
    )

RESULT_OUTCOME: dict[str, str] = {
    "2501.03940:radar-ft": "This is a prior-work comparator; the bound paper provides no exact released RADAR-FT revision or checkpoint and no matched low-FPR, cross-distribution, or fixed two-A6000 near-Binoculars timing basis.",
    "2501.03940:m4-roberta-base": "The high score is the authors' M4-fitted baseline. No fitted state, transferable low-FPR calibration, or fixed A6000 timing is released; the paper's convenience timing uses one RTX 3090 rather than the required matched two-A6000 screen.",
    "2607.03680:vanilla-intellabs-base": "The diagonal result does not transfer reliably across the four corpora, and no separately frozen fitted state, transferable low-FPR calibration, or fixed two-A6000 near-Binoculars timing is available.",
    "2607.03680:vanilla-mage-large": "The diagonal result does not transfer reliably across the four corpora, and no separately frozen fitted state, transferable low-FPR calibration, or fixed two-A6000 near-Binoculars timing is available.",
    "2607.03680:vanilla-faid-base": "The diagonal result does not transfer reliably across the four corpora, and no separately frozen fitted state, transferable low-FPR calibration, or fixed two-A6000 near-Binoculars timing is available.",
    "2607.03680:vanilla-mirage-large": "The diagonal result does not transfer reliably across the four corpora, and no separately frozen fitted state, transferable low-FPR calibration, or fixed two-A6000 near-Binoculars timing is available.",
    "2605.25281:imbd-read": "The qualifying per-domain value depends on an infeasible test-label oracle threshold while the global result is much weaker; no frozen READ-fitted state, transferable low-FPR calibration, or fixed A6000 timing is released.",
    "2605.25281:imbd-target-adapted": "This slice-specific result requires labeled target-generator adaptation, and the paper releases no exact adapted state, general deployment calibration, low-FPR transfer result, or fixed A6000 timing.",
    "2605.06903:roberta-chatgpt-meld": "This is a separately fitted appendix state, not the public RoBERTa-ChatGPT checkpoint. No immutable MELD-data retrain, portable calibration, or fixed near-Binoculars timing is released.",
    "2605.06903:modernbert-detect-meld": "This is a separately fitted appendix state, not the public ModernBERT-Detect checkpoint. No immutable MELD-data retrain, portable calibration, or fixed near-Binoculars timing is released.",
    "2605.06903:repreguard-meld": "This is a separately fitted appendix state, not a Markov-enhanced or public RepreGuard version. Its weak transfer and missing immutable retrain, calibration, and timing block promotion.",
    "2604.21223:reward-model-deberta": "The public reward-model checkpoint is runnable, but one high specialist-domain cell beside a weak aggregate supplies no general low-FPR calibration, matched Binoculars/FastDetectGPT comparison, or fixed A6000 timing.",
    "2606.00016:superannotate-roberta": "The public classifier has a high aligned slice but HC3 was in its training data and transfer/attack cells are much weaker; the paper supplies no portable low-FPR calibration or fixed near-Binoculars timing.",
    "2505.14271:faid-unsup-simcse-xlmr": "The known-generator high score falls below 0.90 on unseen generators, and the retained vector-database lookup violates the no-retrieval boundary; no exact fitted detector or comparable timing is released.",
    "2511.21744:ai-generated-text-detection": "This is a secondary, incomparable literature claim: NEULIF preserves neither the primary evaluation split nor an official checkpoint, low-FPR evidence, or timing basis, so it cannot support promotion.",
    "2511.21744:detective-comparator": "This is a secondary literature value without a like-for-like NEULIF evaluation, immutable state, transferable calibration, or fixed two-A6000 timing basis.",
    "2511.21744:restricted-embeddings": "The 91%-95% range combines unspecified in-domain and OOD contexts from another paper; no common split, exact state, low-FPR calibration, or timing supports promotion.",
    "2511.21744:chatgpt-detector": "The cited in-domain score is explicitly reported to degrade on novel or adversarial text, and NEULIF supplies no exact comparator state, common evaluation, or A6000 timing.",
    "2511.21744:roberta-bilstm": "This is a secondary open-set claim without a bound primary experiment, exact fitted state, portable low-FPR calibration, or matched timing.",
    "2511.21744:styloai-education": "The paper itself attributes the 98% result to a tiny split and reports only 81% on the much larger corpus; no exact state or matched deployment evidence supports promotion.",
    "2509.18880:e5-small-lora": "The high RAID score is a separately fitted benchmark comparator; this paper supplies no immutable fitted state, transferable calibration, cross-distribution low-FPR evidence, or fixed A6000 timing.",
    "2509.18880:desklib": "The high RAID score is a reproduced comparator result rather than a new Desklib artifact; no matched low-FPR transfer or fixed two-A6000 timing is supplied.",
    "2509.18880:superannotate": "The high AUROC coexists with weak fixed-threshold accuracy, and this paper supplies no new fitted checkpoint, portable threshold, or matched cross-distribution timing.",
    "2506.15683:roberta-baseline": "A high machine-class F1 beside weak human-class balance does not establish deployable high accuracy; no exact fitted state, low-FPR calibration, or fixed A6000 timing is released.",
    "2506.15683:t5-sentinel-baseline": "A high machine-class F1 beside sub-0.90 macro F1 does not establish deployable high accuracy; no exact fitted state or matched low-FPR/timing evidence is released.",
    "2506.15683:detective-baseline": "This experiment retrieves validation examples at inference and therefore violates the no-retrieval boundary; the paper also releases no exact comparator state or matched timing.",
    "2506.15683:seqxgpt-baseline": "The high slice requires three white-box proxy probability streams and has weaker transfer elsewhere; no exact fitted state, portable calibration, or near-Binoculars timing is released.",
    "2506.15683:dna-gpt-baseline": "Inference regenerates ten continuations from each target, violating the no-regeneration boundary; the high class-specific value is also poorly balanced.",
    "2506.15683:detectgpt-baseline": "Inference aggregates 100 perturbed versions of each target, violating the no-multi-perturbation boundary; the high class-specific value is also poorly balanced.",
    "2506.15683:fastdetectgpt-baseline": "This is an individually visible FastDetectGPT comparison, but the paper supplies no new frozen state, transferable calibration, or fixed matched A6000 timing.",
    "2506.15683:hastewire": "The high machine-class F1 is paired with weak human-class and low-FPR results, and the closed service has no reproducible public state or A6000 timing basis.",
    "2506.06705:without-adaptation": "The qualifying cell is a weaker no-adaptation ablation, not a released general detector; no exact fitted state, portable calibration, or fixed near-Binoculars timing is supplied.",
    "2506.06705:divscore-mistral": "This proxy-specific appendix state is not separately released and lacks matched cross-distribution low-FPR calibration and fixed two-A6000 timing.",
    "2506.06705:divscore-falcon": "This proxy-specific appendix state is not separately released and lacks matched cross-distribution low-FPR calibration and fixed two-A6000 timing.",
    "2506.06705:divscore-qwen": "This proxy-specific appendix state is not separately released and lacks matched cross-distribution low-FPR calibration and fixed two-A6000 timing.",
    "2506.06705:divscore-llama": "This proxy-specific appendix state is not separately released and lacks matched cross-distribution low-FPR calibration and fixed two-A6000 timing.",
    "2506.06705:entropy-mistral": "The high appendix cells are proxy- and generator-specific; no new frozen state, portable threshold, or fixed matched timing is supplied.",
    "2506.06705:entropy-falcon": "The high appendix cells are proxy- and generator-specific; no new frozen state, portable threshold, or fixed matched timing is supplied.",
    "2506.06705:entropy-qwen": "The high appendix cells are proxy- and generator-specific; no new frozen state, portable threshold, or fixed matched timing is supplied.",
    "2506.06705:entropy-llama": "The high appendix cells are proxy- and generator-specific; no new frozen state, portable threshold, or fixed matched timing is supplied.",
    "2506.06705:cross-entropy-qwen": "One high source-LLM cell beside a 49.23% average does not establish a general detector, and no exact state, portable calibration, or timing is released.",
    "2509.00623:roberta-base": "The near-perfect score is confined to the M-DAIGT news/academic task; no released trained state, cross-distribution test, low-FPR result, or fixed A6000 timing exists.",
    "2509.00623:tfidf-svm": "The high score is confined to the M-DAIGT news/academic task; no fitted SVM, exact vectorizer, cross-distribution test, low-FPR result, or fixed A6000 timing is released.",
    "2509.00623:candace": "The high score is confined to the M-DAIGT news/academic task; no trained state, exact four-Llama deployment recipe, low-FPR result, or reproducible timing is released, and the paper calls it slower than RoBERTa.",
    "2507.05157:gpt4o-mini": "This is a closed hosted fine-tune with content-filtered test failures, no released state, no low-FPR result, and no fixed two-A6000 or near-Binoculars deployment basis.",
    "2507.05157:bert": "The perfect validation score collapses on the official unseen test; no trained state, low-FPR result, or fixed A6000 timing is released.",
    "2507.05157:llama3-8b": "The high validation Task-B score collapses to 0.14 on the official unseen test; no trained state, low-FPR result, or fixed A6000 timing is released.",
}
for _slug in (
    "fastdetectgpt",
    "argugpt",
    "t5-sentinel",
    "detectllm-npr",
    "openai-roberta",
    "aigc-mpu",
    "detectllm-lrr",
    "logrank-gpt2-medium",
    "radar",
    "chatgpt-d",
):
    RESULT_OUTCOME[f"2605.27921:{_slug}"] = (
        "The qualifying value is a narrow domain cell; the same frozen table reports a much weaker aggregate, and this comparator contributes no new released state or fixed low-FPR, cross-distribution, and A6000 timing basis."
    )
for _slug in ("remodetect", "imbd"):
    RESULT_OUTCOME[f"2604.16923:{_slug}"] = (
        "Only the RealDet cell crosses 0.90; the five-column average is much lower and the LAPD paper supplies no new frozen comparator state or like-for-like two-A6000 timing evidence."
    )
for _slug in (
    "entropy",
    "likelihood",
    "logrank",
    "fastdetectgpt",
    "lastde-plus",
):
    RESULT_OUTCOME[f"2604.16923:{_slug}"] = (
        "This is an existing comparator rather than a new detector state; the LAPD paper supplies no new released artifact or fixed low-FPR, cross-distribution, and two-A6000 superiority evidence for it."
    )
RESULT_OUTCOME["2604.16923:binoculars"] = (
    "This is the existing DW1 incumbent used as a paper comparator, not a newly promoted candidate."
)
RESULT_OUTCOME["2604.16923:dna-detectllm"] = (
    "Inference constructs a generated ideal sequence, so it violates the no-regeneration boundary."
)
for _slug in ("rai", "s-score"):
    RESULT_OUTCOME[f"2604.16923:{_slug}"] = (
        "This paper-specific ablation supplies no frozen low-FPR and two-A6000 evidence showing an accuracy improvement over the incumbent."
    )
for _slug in ("lapd-llama2", "lapd-falcon", "lapd-gptj", "lapd-llama31"):
    RESULT_OUTCOME[f"2604.16923:{_slug}"] = (
        "Its standardization draws 10,000 categorical auxiliary samples per token, violating the strict multi-perturbation constraint."
    )
for _slug in ("likelihood", "logrank", "fastdetectgpt", "lastde", "diveye"):
    RESULT_OUTCOME[f"2601.04833:{_slug}"] = (
        "Only a generator-specific cell crosses 0.90; the same tables report substantially weaker benchmark averages and do not establish a new frozen low-FPR state or fixed A6000 comparison."
    )
for _slug in ("detective", "tmr"):
    RESULT_OUTCOME[f"2607.14967:{_slug}"] = (
        "This reported comparator supplies no new released state or matched low-FPR, cross-distribution, and two-A6000 evidence sufficient for promotion."
    )
RESULT_OUTCOME["2607.14967:desklib"] = (
    "This table row adds no new matched low-FPR or speed evidence; the separately preserved public Desklib state remains only the bounded runnable follow-up described in M8."
)
for _slug in ("binoculars", "imbd", "fastdetectgpt"):
    RESULT_OUTCOME[f"2606.31074:{_slug}"] = (
        "This is an existing comparator rather than the Triospect transformation pipeline; this paper adds no new released state or fixed low-FPR and two-A6000 superiority evidence for it."
    )
RESULT_OUTCOME["2606.31074:raidar"] = (
    "Inference derives features from multiple rewrites of the target text, violating the no-rewriting boundary."
)
for _slug in ("biscope", "fastdetectgpt", "lastde-plus", "irm"):
    RESULT_OUTCOME[f"2603.24981:{_slug}"] = (
        "This is an existing comparison detector, not the Exons mutation-repair pipeline; the paper supplies no new frozen low-FPR state or fixed two-A6000 superiority evidence for it."
    )
RESULT_OUTCOME["2603.24981:binoculars"] = (
    "This is the existing DW1 incumbent used as a paper comparator, not a newly promoted candidate."
)
RESULT_OUTCOME["2502.11336:roberta"] = (
    "This supervised baseline is confined to the paper's example-detection evaluation and adds no new released state or fixed cross-distribution, low-FPR, and two-A6000 evidence."
)
RESULT_OUTCOME["2502.11336:lr-gltr"] = (
    "This fitted GLTR-feature baseline adds no released state or fixed cross-distribution, low-FPR, and two-A6000 evidence."
)
RESULT_OUTCOME["2502.11336:dna-gpt"] = (
    "Inference generates continuations before scoring divergence, violating the no-regeneration boundary."
)
RESULT_OUTCOME["2505.12507:npr"] = (
    "Inference aggregates normalized log-rank over multiple perturbed versions of the target, violating the strict multi-perturbation boundary."
)
RESULT_OUTCOME["2505.12507:dnagpt"] = (
    "Inference generates continuations before scoring divergence, violating the no-regeneration boundary."
)
for _slug in (
    "biscope",
    "entropy",
    "likelihood",
    "logrank",
    "fastdetectgpt",
    "lastde-plus",
):
    RESULT_OUTCOME[f"2509.15550:{_slug}"] = (
        "This is a comparison detector rather than the DNA mutation-repair pipeline; its high in-domain or generator-specific result does not add a new frozen low-FPR state or fixed two-A6000 superiority evidence."
    )
RESULT_OUTCOME["2509.15550:binoculars"] = (
    "This is the existing DW1 incumbent used as a paper comparator, not a newly promoted candidate."
)
RESULT_OUTCOME["2509.15550:detectgpt"] = (
    "Inference evaluates numerous perturbed contrast samples of the target, violating the strict multi-perturbation boundary."
)
RESULT_OUTCOME["2504.21019:uniform"] = (
    "Uniform noise is applied to embeddings during training, not inference. The seven-domain average accuracy is 85.48%, and no frozen state, low-FPR result, or fixed A6000 timing supports promotion."
)
RESULT_OUTCOME["2504.21019:gaussian"] = (
    "Gaussian noise is applied to embeddings during training, not inference. The seven-domain average accuracy is 86.10%, and no frozen state, low-FPR result, or fixed A6000 timing supports promotion."
)
for _slug in ("binoculars", "fastdetectgpt"):
    RESULT_OUTCOME[f"2604.25860:{_slug}"] = (
        "This is an existing comparator rather than the Luminol target-shuffling pipeline; the paper adds no new candidate state or fixed low-FPR and two-A6000 superiority evidence."
    )
for _result_id in RESULT_EVIDENCE:
    if _result_id.startswith("2503.22338:"):
        RESULT_OUTCOME[_result_id] = (
            "The result is confined to Defactify development/test data; public feature code ships no fitted classifier, transferable low-FPR calibration, cross-distribution comparison, or fixed A6000 timing."
        )
    elif _result_id.startswith("2502.16857:"):
        RESULT_OUTCOME[_result_id] = (
            "The result is confined to one Defactify task split; no trained state, cross-distribution test, transferable low-FPR calibration, or fixed A6000 timing is released."
        )

RESULT_CODE: dict[str, str] = {
    result_id: "exclude_rewriting"
    for result_id in RESULT_MECHANISM
    if result_id.startswith("2503.22338:")
    and ("-raidar" in result_id or "-combined" in result_id)
}
for _result_id in (
    "2501.03940:radar-ft",
    "2501.03940:m4-roberta-base",
    "2607.03680:vanilla-intellabs-base",
    "2607.03680:vanilla-mage-large",
    "2607.03680:vanilla-faid-base",
    "2607.03680:vanilla-mirage-large",
    "2605.25281:imbd-read",
    "2605.25281:imbd-target-adapted",
):
    RESULT_CODE[_result_id] = "retain_reject"
RESULT_CODE["2507.05157:gpt4o-mini"] = "commercial_closed"
for _slug in (
    "bert",
    "distilbert",
    "roberta",
    "xlnet",
    "albert",
    "deberta",
    "modernbert",
    "adv-modernbert",
):
    _result_id = f"2510.02319:{_slug}"
    RESULT_CODE[_result_id] = "retain_reject"
    RESULT_MECHANISM[_result_id] = (
        "a direct supervised transformer classifier, with training-time augmented pairs only for the adversarial ModernBERT state"
    )
    RESULT_OUTCOME[_result_id] = (
        "This direct classifier is not the PIFE target-transformation path, but its high in-domain AUC degrades on semantic attacks and no qualifying frozen cross-distribution state, low-FPR calibration, or fixed A6000 comparison is established."
    )

for _slug in ("qwen-r4", "qwen-r8", "qwen-r16"):
    RESULT_MECHANISM[f"2509.00731:{_slug}"] = (
        f"Qwen2.5-7B decoder fine-tuned for Chinese binary classification with LoRA rank {_slug[6:]}"
    )
for _slug in ("deepseek-r4", "deepseek-r8", "deepseek-r16"):
    RESULT_MECHANISM[f"2509.00731:{_slug}"] = (
        f"DeepSeek-R1-Distill-Qwen-7B fine-tuned for Chinese binary classification with LoRA rank {_slug[10:]}"
    )
for _slug in ("roberta", "bert", "fasttext"):
    RESULT_MECHANISM[f"2509.00731:{_slug}"] = (
        "the named directly fitted Chinese encoder or FastText classifier"
    )

RESULT_MECHANISM.update(
    {
        "2604.16923:entropy": "mean token entropy under the paper's scoring model",
        "2604.16923:likelihood": "mean token log-likelihood under the paper's scoring model",
        "2604.16923:logrank": "mean token log-rank under the paper's scoring model",
        "2604.16923:fastdetectgpt": "the FastDetectGPT conditional-probability-curvature statistic",
        "2604.16923:lastde-plus": "the Lastde++ local-subsequence statistic over token-probability series",
        "2604.16923:binoculars": "the Binoculars cross-model perplexity-ratio statistic",
        "2604.16923:dna-detectllm": "DNA-DetectLLM discrepancy scoring against a generated ideal sequence",
        "2604.16923:rai": "the raw log-likelihood ratio between aligned and base models before LAPD standardization",
        "2604.16923:s-score": "the information-weighted alignment-imprint sum before LAPD standardization",
        "2604.16923:lapd-llama2": "LAPD standardized information-weighted alignment imprint with the Llama-2 observer/performer pair",
        "2604.16923:lapd-falcon": "LAPD standardized information-weighted alignment imprint with the Falcon observer/performer pair",
        "2604.16923:lapd-gptj": "LAPD standardized information-weighted alignment imprint with the GPT-J observer/performer pair",
        "2604.16923:lapd-llama31": "LAPD standardized information-weighted alignment imprint with the Llama-3.1 observer/performer pair",
        "2607.14967:detective": "the named directly supervised DeTeCtive comparator",
        "2607.14967:desklib": "the named directly supervised Desklib comparator",
        "2607.14967:tmr": "the named TMR comparison detector",
        "2606.31074:raidar": "RAIDAR features derived from multiple target-text rewrites",
        "2606.31074:binoculars": "the Binoculars cross-model perplexity-ratio statistic",
        "2606.31074:imbd": "the ImBD preference-divergence comparator",
        "2606.31074:fastdetectgpt": "the FastDetectGPT conditional-probability-curvature statistic",
        "2603.24981:biscope": "the BiScope zero-shot comparison statistic",
        "2603.24981:fastdetectgpt": "the FastDetectGPT conditional-probability-curvature statistic",
        "2603.24981:binoculars": "the Binoculars cross-model perplexity-ratio statistic",
        "2603.24981:lastde-plus": "the Lastde++ local-subsequence statistic over token-probability series",
        "2603.24981:irm": "the IRM comparison detector with its stated model pair",
        "2603.24981:dna-detectllm": "DNA-DetectLLM discrepancy scoring against a generated ideal sequence",
        "2502.11336:roberta": "the directly supervised RoBERTa comparison classifier",
        "2502.11336:lr-gltr": "logistic regression over GLTR token-rank features",
        "2502.11336:dna-gpt": "DNA-GPT scoring over generated continuations",
        "2505.12507:npr": "DetectLLM normalized perturbed log-rank over multiple target-text perturbations",
        "2505.12507:dnagpt": "DNA-GPT scoring over generated continuations",
        "2509.15550:biscope": "the directly supervised BiScope bidirectional cross-entropy classifier",
        "2509.15550:entropy": "mean token entropy under the scoring model",
        "2509.15550:likelihood": "mean token likelihood under the scoring model",
        "2509.15550:logrank": "mean token log-rank under the scoring model",
        "2509.15550:detectgpt": "DetectGPT scoring over numerous target-text perturbations",
        "2509.15550:fastdetectgpt": "the FastDetectGPT conditional-probability-curvature statistic",
        "2509.15550:binoculars": "the Binoculars cross-model perplexity-ratio statistic",
        "2509.15550:lastde-plus": "the Lastde++ local-subsequence statistic over token-probability series",
        "2509.15550:dna-default": "DNA-DetectLLM iterative token mutation-repair with the default simplified repair score",
        "2509.15550:dna-low-high": "DNA-DetectLLM iterative token mutation-repair in low-to-high score order",
        "2509.15550:dna-high-low": "DNA-DetectLLM iterative token mutation-repair in high-to-low score order",
        "2509.15550:dna-sequential": "DNA-DetectLLM sequential iterative token mutation-repair",
        "2509.15550:dna-mistral": "DNA-DetectLLM iterative token mutation-repair with the Mistral observer/reference pair",
        "2509.15550:dna-llama2": "DNA-DetectLLM iterative token mutation-repair with the Llama-2 observer/reference pair",
        "2509.15550:dna-llama3": "DNA-DetectLLM iterative token mutation-repair with the Llama-3 observer/reference pair",
        "2504.21019:uniform": "RoBERTa trained with dynamically selected uniform embedding noise",
        "2504.21019:gaussian": "RoBERTa trained with dynamically selected Gaussian embedding noise",
        "2604.25860:binoculars": "the Binoculars cross-model perplexity-ratio statistic",
        "2604.25860:fastdetectgpt": "the FastDetectGPT conditional-probability-curvature statistic",
    }
)

_BASELINE_MECHANISMS = {
    "likelihood": "mean token likelihood under the scoring language model",
    "logrank": "mean token log-rank under the scoring language model",
    "entropy": "mean token entropy under the scoring language model",
    "detectlrr": "the DetectLLM likelihood-to-log-rank-ratio statistic",
    "lastde": "the Lastde local-subsequence statistic over token-probability series",
    "detectgpt": "DetectGPT scoring over multiple masked-and-filled perturbations of the target text",
    "detectnpr": "DetectLLM normalized perturbed log-rank over multiple target-text perturbations",
    "dnagpt": "DNA-GPT scoring over generated continuations",
    "fastdetectgpt": "the FastDetectGPT conditional-probability-curvature statistic",
    "lastde-plus": "the Lastde++ local-subsequence statistic over token-probability series",
    "binoculars": "the Binoculars cross-model perplexity-ratio statistic",
}

for _parent_id, _slugs in {
    "2606.02158": (
        "likelihood",
        "logrank",
        "detectlrr",
        "lastde",
        "detectgpt",
        "detectnpr",
        "dnagpt",
        "fastdetectgpt",
        "lastde-plus",
    ),
    "2508.11343": (
        "likelihood",
        "logrank",
        "entropy",
        "detectlrr",
        "lastde",
        "detectgpt",
        "detectnpr",
        "dnagpt",
        "fastdetectgpt",
        "lastde-plus",
    ),
}.items():
    for _slug in _slugs:
        RESULT_MECHANISM[f"{_parent_id}:{_slug}"] = _BASELINE_MECHANISMS[_slug]

RESULT_MECHANISM.update(
    {
        "2606.02158:without-low-probability": "the proposed local/global uncertainty statistic with its low-probability-token feature removed",
        "2606.02158:without-entropy": "the proposed local/global uncertainty statistic with its entropy feature removed",
        "2506.06705:roberta-base": "a directly supervised RoBERTa-base sequence classifier",
        "2506.06705:roberta-large": "a directly supervised RoBERTa-large sequence classifier",
        "2506.06705:entropy": _BASELINE_MECHANISMS["entropy"],
        "2506.06705:rank": "mean token rank under the scoring language model",
        "2506.06705:logrank": _BASELINE_MECHANISMS["logrank"],
        "2506.06705:likelihood": _BASELINE_MECHANISMS["likelihood"],
        "2506.06705:detectgpt": _BASELINE_MECHANISMS["detectgpt"],
        "2506.06705:fastdetectgpt": _BASELINE_MECHANISMS["fastdetectgpt"],
        "2506.06705:binoculars": _BASELINE_MECHANISMS["binoculars"],
        "2501.03940:m4-xlm-roberta": "a directly supervised XLM-RoBERTa comparison classifier fitted on M4",
        "2501.03940:mage-longformer": "the directly supervised 4,096-token Longformer detector fitted on MAGE",
        "2501.03940:gltr": "the GLTR token-rank-bin heuristic detector",
        "2501.03940:raid-rb-gpt2": "the published RoBERTa-base GPT-2 detector evaluated on RAID without RAID fitting",
        "2501.03940:raid-rl-gpt2": "the published RoBERTa-large GPT-2 detector evaluated on RAID without RAID fitting",
        "2501.03940:raid-rb-cgpt": "the published RoBERTa-base ChatGPT detector evaluated on RAID without RAID fitting",
        "2501.03940:raid-radar": "the published adversarially trained RADAR detector evaluated on RAID without RAID fitting",
        "2501.03940:raid-fastdetectgpt": _BASELINE_MECHANISMS["fastdetectgpt"],
        "2501.03940:raid-binoculars": _BASELINE_MECHANISMS["binoculars"],
        "2501.03940:raid-gptzero": "the closed GPTZero detector evaluated through its public service",
        "2501.03940:raid-originality": "the closed Originality.ai detector evaluated through its public service",
        "2501.03940:raid-winston": "the closed Winston AI detector evaluated through its public service",
        "2501.03940:raid-zerogpt": "the closed ZeroGPT detector evaluated through its public service",
        "2501.03940:mage-roberta-base": "the directly supervised RoBERTa-base detector fitted on MAGE",
        "2501.03940:mage-radar-ptm": "the RADAR pretrained-transformer state fitted on MAGE",
        "2501.03940:raidft-pawn-gpt2": "PAWN with the GPT-2 backbone after one epoch of supervised RAID fitting",
        "2501.03940:raidft-pawn-llama": "PAWN with the Llama backbone after one epoch of supervised RAID fitting",
        "2501.03940:raidft-longformer": "the Longformer detector after one epoch of supervised RAID fitting",
        "2501.03940:raidft-roberta": "the RoBERTa detector after one epoch of supervised RAID fitting",
        "2501.03940:raidft-radar-ptm": "the RADAR pretrained-transformer detector after one epoch of supervised RAID fitting",
        "2501.03940:raidft-radar": "the RADAR detector after one epoch of supervised RAID fitting",
        "2607.03680:anchor": "the Anchor peer-review score with per-source-LLM thresholds calibrated from reference reviews",
        "2607.03680:mage-longformer": "the directly supervised 4,096-token Longformer detector fitted on MAGE",
        "2607.03680:llmdetectaive": "the published directly supervised LLM-DetectAIve comparison classifier",
        "2607.03680:faid": "the published FAID multi-task contrastive detector with vector-database augmentation",
        "2607.03680:vanilla-faid-extra-domain": "a RoBERTa-base classifier additionally fitted on the released unseen-domain validation set",
        "2607.03680:vanilla-faid-extra-domain-generator": "a RoBERTa-base classifier additionally fitted on the released unseen-domain-plus-generator validation set",
        "2607.03680:detectanyllm": "the published DetectAnyLLM detector trained on 500 paired GPT-3.5-polish examples",
        "2607.03680:vanilla-mirage-base": "a RoBERTa-base sequence classifier fitted separately on MIRAGE",
        "2607.03680:fomaml-lora": "a RoBERTa-large detector adapted with FOMAML and LoRA on ten labeled target examples",
        "2607.03680:fomaml-hc3-k5": "a MAGE-meta-trained RoBERTa-large detector adapted with FOMAML and LoRA on five labeled HC3 examples",
        "2607.03680:fomaml-hc3-k20": "a MAGE-meta-trained RoBERTa-large detector adapted with FOMAML and LoRA on twenty labeled HC3 examples",
        "2607.03680:fomaml-hc3-k50": "a MAGE-meta-trained RoBERTa-large detector adapted with FOMAML and LoRA on fifty labeled HC3 examples",
        "2607.03680:confidence-ensemble": "confidence-weighted score fusion of the Vanilla and target-adapted FOMAML detectors",
        "2607.03680:reverse-confidence-ensemble": "confidence-weighted score fusion using the FOMAML detector as the confidence source",
        "2607.03680:pooled-four-way": "a directly supervised RoBERTa detector fitted on a four-benchmark pooled training set",
        "2607.03680:pooled-stratified-base": "a directly supervised RoBERTa-base detector fitted on the paper's stratified pooled training set",
        "2607.03680:pooled-stratified-large": "a directly supervised RoBERTa-large detector fitted on the paper's stratified pooled training set",
        "2605.25281:biscope-read": "the directly supervised BiScope bidirectional cross-entropy classifier fitted on READ",
        "2605.25281:biscope-target-adapted": "the BiScope classifier additionally fitted with labeled target-generator examples from other READ domains",
        "2605.25281:npr-gemma": "DetectLLM normalized perturbed log-rank using the Gemma surrogate",
        "2605.25281:npr-qwen": "DetectLLM normalized perturbed log-rank using the Qwen surrogate",
        "2605.25281:detectgpt-gemma": "DetectGPT perturbation scoring using Gemma as the surrogate language model",
        "2605.25281:detectgpt-qwen": "DetectGPT perturbation scoring using Qwen as the surrogate language model",
        "2605.25281:binoculars-gemma": "the Binoculars cross-model perplexity-ratio statistic with the paper's Gemma model pair",
        "2605.25281:radar": "the released adversarially trained RADAR-Vicuna-7B classifier",
        "2605.25281:fastdetectgpt-gemma": "FastDetectGPT conditional-probability curvature with the paper's Gemma scoring and sampling models",
        "2605.25281:adadetectgpt-gemma": "AdaDetectGPT with the paper's Gemma scoring and sampling models",
        "2605.25281:adadetectgpt-gemma-target": "AdaDetectGPT with the paper's Gemma models and labeled target-generator adaptation",
        "2606.07313:polish-only": "the SV-Detect steering-vector classifier separately fitted on MIRAGE polish examples only",
        "2606.07313:three-task": "the SV-Detect steering-vector classifier separately fitted on MIRAGE generate, polish, and rewrite examples",
        "2506.01702:tfidf-baseline": "a directly supervised linear classifier over TF-IDF text features",
        "2509.15550:revise-detect": "Revise-Detect scoring after an LLM rewrites or revises the target text",
    }
)

for _slug in (
    "likelihood",
    "logrank",
    "entropy",
    "detectgpt",
    "fastgpt",
    "dnagpt",
    "repreguard",
    "lastde",
    "fouriergpt",
    "binoculars",
):
    _mechanism = {
        "likelihood": _BASELINE_MECHANISMS["likelihood"],
        "logrank": _BASELINE_MECHANISMS["logrank"],
        "entropy": _BASELINE_MECHANISMS["entropy"],
        "detectgpt": _BASELINE_MECHANISMS["detectgpt"],
        "fastgpt": _BASELINE_MECHANISMS["fastdetectgpt"],
        "dnagpt": _BASELINE_MECHANISMS["dnagpt"],
        "repreguard": "the published RepreGuard representation-based detector without Markov calibration",
        "lastde": _BASELINE_MECHANISMS["lastde"],
        "fouriergpt": "the FourierGPT frequency-domain token-probability statistic without Markov calibration",
        "binoculars": _BASELINE_MECHANISMS["binoculars"],
    }[_slug]
    RESULT_MECHANISM[f"2602.08031:{_slug}"] = _mechanism

_NEW_PARENT_OUTCOMES = {
    "2606.02158": "This named table state has a qualifying slice, but the paper supplies no separately frozen state, transferable low-FPR and cross-distribution calibration, or fixed two-A6000 near-Binoculars timing basis.",
    "2508.11343": "This named Table 1 comparator has a qualifying dataset/model slice, but the SpecDetect paper supplies no new frozen comparator state or matched low-FPR, cross-distribution, and two-A6000 timing evidence.",
    "2506.06705": "This named comparison state has a qualifying domain/model slice, but the DivScore paper supplies no new frozen comparator state or matched low-FPR, cross-distribution, and two-A6000 timing evidence.",
    "2602.08031": "This unmodified comparison detector is distinct from its Markov-calibrated counterpart, but the paper supplies no new frozen baseline state or matched low-FPR, cross-distribution, and two-A6000 timing evidence.",
}
for _parent_id, _outcome in _NEW_PARENT_OUTCOMES.items():
    for _slug, _display in PRIMARY_GROUPS[_parent_id]:
        _result_id = f"{_parent_id}:{_slug}"
        if _result_id in RESULT_MECHANISM and _result_id not in RESULT_OUTCOME:
            RESULT_OUTCOME[_result_id] = _outcome

for _slug, _display in PRIMARY_GROUPS["2501.03940"]:
    _result_id = f"2501.03940:{_slug}"
    if _result_id in RESULT_MECHANISM and _result_id not in RESULT_OUTCOME:
        RESULT_OUTCOME[_result_id] = (
            "This separately named PAWN-table state crosses 0.90 on at least one reported slice, but the paper supplies no exact frozen state with transferable low-FPR, cross-distribution, and fixed two-A6000 near-Binoculars evidence."
        )
for _slug in ("raid-gptzero", "raid-originality", "raid-winston", "raid-zerogpt"):
    RESULT_OUTCOME[f"2501.03940:{_slug}"] = (
        "This closed commercial detector crosses 0.90 on a RAID slice, but no reproducible state, portable calibration, or fixed two-A6000 timing basis is publicly available."
    )

for _slug, _display in PRIMARY_GROUPS["2607.03680"]:
    _result_id = f"2607.03680:{_slug}"
    if _result_id in RESULT_MECHANISM and _result_id not in RESULT_OUTCOME:
        RESULT_OUTCOME[_result_id] = (
            "This table state has a qualifying in-domain, adapted, or pooled slice, but transfer or low-FPR performance is materially weaker and no exact frozen state with fixed two-A6000 near-Binoculars timing is released."
        )
RESULT_OUTCOME["2607.03680:faid"] = (
    "The published FAID detector uses vector-database augmentation at inference, violating the no-retrieval boundary; this comparison paper also supplies no frozen FAID state or fixed A6000 timing."
)

for _slug, _display in PRIMARY_GROUPS["2605.25281"]:
    _result_id = f"2605.25281:{_slug}"
    if _result_id in RESULT_MECHANISM and _result_id not in RESULT_OUTCOME:
        RESULT_OUTCOME[_result_id] = (
            "This named READ or OOD table state crosses 0.90 only under a per-domain oracle threshold, a narrow slice, or target adaptation; it adds no exact frozen state with transferable low-FPR calibration and fixed A6000 timing."
        )
for _slug in ("npr-gemma", "npr-qwen", "detectgpt-gemma", "detectgpt-qwen"):
    RESULT_OUTCOME[f"2605.25281:{_slug}"] = (
        "Inference aggregates multiple perturbed versions of the target, violating the strict multi-perturbation boundary."
    )

for _slug in ("polish-only", "three-task"):
    RESULT_OUTCOME[f"2606.07313:{_slug}"] = (
        "This separately fitted MIRAGE state has high in-task AUROC, but no exact frozen fitted state, transferable low-FPR calibration, or fixed two-A6000 near-Binoculars timing is released."
    )
RESULT_OUTCOME["2506.01702:tfidf-baseline"] = (
    "The near-perfect value is validation-only and does not survive the paper's OOD evaluation basis; no fitted vectorizer/classifier, transferable low-FPR calibration, or fixed A6000 timing is released."
)
RESULT_OUTCOME["2509.15550:revise-detect"] = (
    "Inference rewrites or revises the target before scoring, violating the no-rewriting boundary."
)

for _parent_id in (
    "2606.02158",
    "2508.11343",
    "2506.06705",
    "2602.08031",
    "2501.03940",
    "2607.03680",
    "2605.25281",
    "2606.07313",
    "2506.01702",
    "2509.15550",
):
    for _slug, _display in PRIMARY_GROUPS[_parent_id]:
        _result_id = f"{_parent_id}:{_slug}"
        if _result_id in RESULT_MECHANISM:
            RESULT_CODE.setdefault(_result_id, "retain_reject")

for _result_id in (
    "2606.02158:detectgpt",
    "2606.02158:detectnpr",
    "2508.11343:detectgpt",
    "2602.08031:detectgpt",
    "2506.06705:detectgpt",
    "2605.25281:npr-gemma",
    "2605.25281:npr-qwen",
    "2605.25281:detectgpt-gemma",
    "2605.25281:detectgpt-qwen",
):
    RESULT_CODE[_result_id] = "exclude_multi_perturbation"
for _result_id in (
    "2606.02158:dnagpt",
    "2508.11343:dnagpt",
    "2602.08031:dnagpt",
    "2509.15550:dna-default",
    "2509.15550:dna-low-high",
    "2509.15550:dna-high-low",
    "2509.15550:dna-sequential",
    "2509.15550:dna-mistral",
    "2509.15550:dna-llama2",
    "2509.15550:dna-llama3",
):
    RESULT_CODE[_result_id] = "exclude_regeneration"
RESULT_CODE["2607.03680:faid"] = "exclude_retrieval"
RESULT_CODE["2509.15550:revise-detect"] = "exclude_rewriting"
for _result_id in (
    "2605.06903:roberta-chatgpt-meld",
    "2605.06903:modernbert-detect-meld",
    "2605.06903:repreguard-meld",
    "2604.21223:reward-model-deberta",
    "2606.00016:superannotate-roberta",
):
    RESULT_CODE[_result_id] = "retain_reject"
RESULT_CODE["2505.14271:faid-unsup-simcse-xlmr"] = "exclude_retrieval"
for _slug in (
    "ai-generated-text-detection",
    "detective-comparator",
    "restricted-embeddings",
    "chatgpt-detector",
    "roberta-bilstm",
    "styloai-education",
):
    RESULT_CODE[f"2511.21744:{_slug}"] = "retain_reject"
RESULT_CODE["2511.21744:detective-comparator"] = "exclude_retrieval"
for _slug in ("e5-small-lora", "desklib", "superannotate"):
    RESULT_CODE[f"2509.18880:{_slug}"] = "retain_reject"
for _slug in (
    "roberta-baseline",
    "t5-sentinel-baseline",
    "seqxgpt-baseline",
    "fastdetectgpt-baseline",
):
    RESULT_CODE[f"2506.15683:{_slug}"] = "retain_reject"
RESULT_CODE["2506.15683:detective-baseline"] = "exclude_retrieval"
RESULT_CODE["2506.15683:dna-gpt-baseline"] = "exclude_regeneration"
RESULT_CODE["2506.15683:detectgpt-baseline"] = "exclude_multi_perturbation"
RESULT_CODE["2506.15683:hastewire"] = "commercial_closed"
for _slug in (
    "without-adaptation",
    "divscore-mistral",
    "divscore-falcon",
    "divscore-qwen",
    "divscore-llama",
    "entropy-mistral",
    "entropy-falcon",
    "entropy-qwen",
    "entropy-llama",
    "cross-entropy-qwen",
):
    RESULT_CODE[f"2506.06705:{_slug}"] = "retain_reject"
for _slug in ("raid-gptzero", "raid-originality", "raid-winston", "raid-zerogpt"):
    RESULT_CODE[f"2501.03940:{_slug}"] = "commercial_closed"

for _slug in ("detective", "desklib", "tmr"):
    RESULT_CODE[f"2607.14967:{_slug}"] = "retain_reject"
RESULT_CODE["2605.27921:detectllm-npr"] = "exclude_multi_perturbation"
for _slug in ("binoculars", "imbd", "fastdetectgpt"):
    RESULT_CODE[f"2606.31074:{_slug}"] = "retain_reject"
RESULT_CODE["2606.31074:raidar"] = "exclude_rewriting"
for _slug in ("binoculars", "fastdetectgpt"):
    RESULT_CODE[f"2604.25860:{_slug}"] = "retain_reject"
for _slug in (
    "entropy",
    "likelihood",
    "logrank",
    "fastdetectgpt",
    "lastde-plus",
    "binoculars",
    "remodetect",
    "imbd",
):
    RESULT_CODE[f"2604.16923:{_slug}"] = "retain_reject"
RESULT_CODE["2604.16923:dna-detectllm"] = "exclude_regeneration"
for _slug in ("rai", "s-score"):
    RESULT_CODE[f"2604.16923:{_slug}"] = "retain_reject"
for _slug in (
    "biscope",
    "entropy",
    "likelihood",
    "logrank",
    "fastdetectgpt",
    "binoculars",
    "lastde-plus",
):
    RESULT_CODE[f"2509.15550:{_slug}"] = "retain_reject"
RESULT_CODE["2509.15550:detectgpt"] = "exclude_multi_perturbation"
for _slug in ("uniform", "gaussian"):
    RESULT_CODE[f"2504.21019:{_slug}"] = "retain_reject"
for _slug in (
    "biscope",
    "fastdetectgpt",
    "binoculars",
    "lastde-plus",
    "irm",
):
    RESULT_CODE[f"2603.24981:{_slug}"] = "retain_reject"
RESULT_CODE["2603.24981:dna-detectllm"] = "exclude_regeneration"
for _slug in (
    "fdgpt-llama",
    "fdgpt-mistral",
    "fdgpt-qwen",
    "binoculars-llama",
    "binoculars-mistral",
    "binoculars-qwen",
):
    RESULT_CODE[f"2602.11871:{_slug}"] = "retain_reject"
for _slug in ("llmdetectaive", "t5-sentinel"):
    RESULT_CODE[f"2505.14271:{_slug}"] = "retain_reject"
for _slug in (
    "npr",
    "lrr",
    "rank",
    "entropy",
    "logrank",
    "likelihood",
    "glimpse",
    "binoculars",
    "fastdetectgpt",
    "roberta-qa",
    "radar",
    "gptzero",
    "detective",
):
    RESULT_CODE[f"2505.12507:{_slug}"] = "retain_reject"
RESULT_CODE["2505.12507:npr"] = "exclude_multi_perturbation"
RESULT_CODE["2505.12507:dnagpt"] = "exclude_regeneration"
for _slug in ("roberta", "lr-gltr"):
    RESULT_CODE[f"2502.11336:{_slug}"] = "retain_reject"
RESULT_CODE["2502.11336:dna-gpt"] = "exclude_regeneration"
RESULT_CODE["2502.12734:greater-d"] = "retain_reject"
for _slug in ("greater-a-query", "greater-a-zero-query"):
    RESULT_CODE[f"2502.12734:{_slug}"] = "exclude_rewriting"
RESULT_CODE["2501.18998:fastdetectgpt-baseline"] = "retain_reject"
for _slug in ("bert", "elmo", "fasttext", "glove", "tmae", "word2vec"):
    RESULT_CODE[f"2501.18998:fastdetectgpt-{_slug}"] = "exclude_rewriting"

for _slug in ("llmdetectaive", "t5-sentinel"):
    RESULT_OUTCOME[f"2505.14271:{_slug}"] = (
        "This direct comparison classifier is individually retained, but the paper supplies no frozen transferable state, low-FPR cross-distribution evidence, or fixed A6000 timing sufficient for promotion."
    )
for _slug in (
    "npr",
    "lrr",
    "rank",
    "entropy",
    "logrank",
    "likelihood",
    "glimpse",
    "binoculars",
    "dnagpt",
    "fastdetectgpt",
    "roberta-qa",
    "radar",
    "gptzero",
    "detective",
):
    RESULT_OUTCOME[f"2505.12507:{_slug}"] = (
        "This is an individually visible comparison result, not LM2otifs itself; the cited table does not establish a new frozen state with like-for-like low-FPR, two-A6000, and near-Binoculars timing evidence."
    )


# Eval7's independent Roman-caption/figure challenge exposed 29 exact states
# that the preceding Arabic-table scanner could not see.  Keep their method
# identities and dispositions local: none may inherit the parent paper's
# proposed-method exclusion.
RESULT_MECHANISM.update(
    {
        "2605.16107:likelihood": _BASELINE_MECHANISMS["likelihood"],
        "2605.16107:logrank": _BASELINE_MECHANISMS["logrank"],
        "2605.16107:entropy": _BASELINE_MECHANISMS["entropy"],
        "2605.16107:detectgpt": _BASELINE_MECHANISMS["detectgpt"],
        "2605.16107:fastgpt": _BASELINE_MECHANISMS["fastdetectgpt"],
        "2605.16107:binoculars": _BASELINE_MECHANISMS["binoculars"],
        "2605.16107:fouriergpt": "the unmodified FourierGPT likelihood-spectrum statistic",
        "2605.16107:adagpt": "the unmodified AdaDetectGPT classifier that learns witness functions from training data",
        "2604.02008:likelihood": _BASELINE_MECHANISMS["likelihood"],
        "2604.02008:logrank": _BASELINE_MECHANISMS["logrank"],
        "2604.02008:fastdetectgpt": _BASELINE_MECHANISMS["fastdetectgpt"],
        "2604.02008:binoculars": _BASELINE_MECHANISMS["binoculars"],
        "2604.02008:fastdetectgpt-dald": "FastDetectGPT after DALD supervised fine-tuning aligns the proxy on proprietary-LLM outputs before inference",
        "2604.02008:fastdetectgpt-glimpse-gpt4-geometric": "FastDetectGPT after geometric full-distribution reconstruction from GPT-4 API top-k probabilities",
        "2604.02008:fastdetectgpt-glimpse-gpt4-zipfian": "FastDetectGPT after Zipfian full-distribution reconstruction from GPT-4 API top-k probabilities",
        "2604.02008:fastdetectgpt-glimpse-gpt4-mlp": "FastDetectGPT after learned-MLP full-distribution reconstruction from GPT-4 API top-k probabilities",
        "2604.02008:fastdetectgpt-glimpse-davinci-geometric": "FastDetectGPT after geometric full-distribution reconstruction from DaVinci-002 API top-k probabilities",
        "2604.02008:binoculars-dald": "Binoculars using a DALD proxy fine-tuned on proprietary-LLM outputs before inference",
        "2510.02319:fastdetectgpt": _BASELINE_MECHANISMS["fastdetectgpt"],
        "2510.02319:glimpse": "Glimpse reconstructs a source-model token distribution from commercial API top-k probabilities before zero-shot scoring",
        "2510.02319:binoculars": _BASELINE_MECHANISMS["binoculars"],
        "2510.02319:logrank": _BASELINE_MECHANISMS["logrank"],
        "2508.11933:raidar": "RAIDAR reasoning features derived from multiple target-text rewrites",
        "2508.11933:gpt4o-direct": "direct binary prompting of the hosted GPT-4o model",
        "2508.11933:gpt-cot": "chain-of-thought binary prompting of the hosted GPT-4o model",
        "2508.11933:gpt-react": "a ReAct-inspired multi-agent GPT-4o inference setup",
        "2508.11933:gpt4o-mini": "CAMF's multi-stage, multi-agent adversarial-probing and judgment pipeline using GPT-4o-mini",
        "2508.11933:gemini15-pro": "CAMF's multi-stage, multi-agent adversarial-probing and judgment pipeline using Gemini-1.5 Pro",
        "2508.11933:deepseek-v3": "CAMF's multi-stage, multi-agent adversarial-probing and judgment pipeline using DeepSeek-V3",
    }
)

for _result_id in (
    "2605.16107:likelihood",
    "2605.16107:logrank",
    "2605.16107:entropy",
    "2605.16107:fastgpt",
    "2605.16107:fouriergpt",
    "2605.16107:adagpt",
):
    RESULT_OUTCOME[_result_id] = (
        "The high value is confined to the paper's source/generator slices; the paper releases no runnable detector state, transferable low-FPR calibration, or fixed two-A6000 near-Binoculars timing for this baseline."
    )
RESULT_OUTCOME["2605.16107:detectgpt"] = (
    "Inference scores multiple masked-and-filled perturbations of every target, violating the strict multi-perturbation boundary."
)
RESULT_OUTCOME["2605.16107:binoculars"] = (
    "This is the existing DW1 incumbent used as a paper comparator, not a newly promoted candidate."
)

for _result_id in (
    "2604.02008:likelihood",
    "2604.02008:logrank",
    "2604.02008:fastdetectgpt",
    "2604.02008:fastdetectgpt-dald",
    "2604.02008:binoculars-dald",
):
    RESULT_OUTCOME[_result_id] = (
        "This individually reported comparator or training-time proxy alignment supplies no new frozen detector state, transferable low-FPR calibration, or fixed two-A6000 near-Binoculars timing sufficient for promotion."
    )
RESULT_OUTCOME["2604.02008:binoculars"] = (
    "This is the existing DW1 incumbent used as a paper comparator, not a newly promoted candidate."
)
for _result_id in (
    "2604.02008:fastdetectgpt-glimpse-gpt4-geometric",
    "2604.02008:fastdetectgpt-glimpse-gpt4-zipfian",
    "2604.02008:fastdetectgpt-glimpse-gpt4-mlp",
    "2604.02008:fastdetectgpt-glimpse-davinci-geometric",
):
    RESULT_OUTCOME[_result_id] = (
        "This state depends on a proprietary model's hosted top-k probability API; the paper says GPT-4 no longer exposes those probabilities, and no frozen service state, portable calibration, or A6000 deployment exists."
    )

for _result_id in (
    "2510.02319:fastdetectgpt",
    "2510.02319:logrank",
):
    RESULT_OUTCOME[_result_id] = (
        "The high value is confined to the non-adversarial split and collapses on all attack mixes; this paper supplies no new frozen state, transferable low-FPR calibration, or fixed A6000 timing."
    )
RESULT_OUTCOME["2510.02319:glimpse"] = (
    "The high non-adversarial result depends on proprietary source-model top-k probability access, collapses on the attack mixes, and supplies no reproducible frozen service or two-A6000 state."
)
RESULT_OUTCOME["2510.02319:binoculars"] = (
    "This is the existing DW1 incumbent used as a paper comparator; the attack-mix collapse is evidence against treating the narrow high cell as a new candidate."
)

RESULT_OUTCOME["2508.11933:raidar"] = (
    "Inference derives features from multiple rewrites of the target text, violating the no-rewriting boundary."
)
for _result_id in (
    "2508.11933:gpt4o-direct",
    "2508.11933:gpt-cot",
    "2508.11933:gpt-react",
):
    RESULT_OUTCOME[_result_id] = (
        "This is a closed hosted GPT-4o configuration with no reproducible public state, low-FPR calibration, or two-A6000 deployment basis; only the Code-domain result crosses 0.90 F1."
    )
for _result_id in (
    "2508.11933:gpt4o-mini",
    "2508.11933:gemini15-pro",
):
    RESULT_OUTCOME[_result_id] = (
        "This CAMF state requires repeated calls to a closed hosted backbone in a multi-agent pipeline; no public frozen state, low-FPR result, or two-A6000 deployment exists, and the paper's default CAMF timing is 22.5 seconds per sample."
    )
RESULT_OUTCOME["2508.11933:deepseek-v3"] = (
    "The figure's high Code-domain value has no released CAMF implementation or exact fitted state, low-FPR result, fixed two-A6000 timing, or plausible near-Binoculars multi-agent deployment basis."
)

for _result_id in (
    "2605.16107:likelihood",
    "2605.16107:logrank",
    "2605.16107:entropy",
    "2605.16107:fastgpt",
    "2605.16107:binoculars",
    "2605.16107:fouriergpt",
    "2605.16107:adagpt",
    "2604.02008:likelihood",
    "2604.02008:logrank",
    "2604.02008:fastdetectgpt",
    "2604.02008:binoculars",
    "2604.02008:fastdetectgpt-dald",
    "2604.02008:binoculars-dald",
    "2510.02319:fastdetectgpt",
    "2510.02319:binoculars",
    "2510.02319:logrank",
    "2508.11933:deepseek-v3",
):
    RESULT_CODE[_result_id] = "retain_reject"
RESULT_CODE["2605.16107:detectgpt"] = "exclude_multi_perturbation"
for _result_id in (
    "2605.16107:detectgpt-m",
    "2605.16107:detectgpt-mult",
):
    RESULT_MECHANISM[_result_id] = (
        "DetectGPT scoring over multiple masked-and-filled target perturbations, followed by the paper's named Markov or multi-level contextual layer"
    )
    RESULT_OUTCOME[_result_id] = (
        "The underlying detector still scores multiple target perturbations, violating the strict multi-perturbation boundary."
    )
    RESULT_CODE[_result_id] = "exclude_multi_perturbation"
for _result_id in (
    "2605.16107:detectllm-m",
    "2605.16107:detectllm-mult",
):
    RESULT_MECHANISM[_result_id] = (
        "DNA-DetectLLM scoring against a regenerated ideal sequence, followed by the paper's named Markov or multi-level contextual layer"
    )
    RESULT_OUTCOME[_result_id] = (
        "The underlying detector constructs a regenerated ideal sequence, violating the no-regeneration boundary."
    )
    RESULT_CODE[_result_id] = "exclude_regeneration"
for _result_id in (
    "2604.02008:fastdetectgpt-glimpse-gpt4-geometric",
    "2604.02008:fastdetectgpt-glimpse-gpt4-zipfian",
    "2604.02008:fastdetectgpt-glimpse-gpt4-mlp",
    "2604.02008:fastdetectgpt-glimpse-davinci-geometric",
    "2510.02319:glimpse",
    "2508.11933:gpt4o-direct",
    "2508.11933:gpt-cot",
    "2508.11933:gpt-react",
    "2508.11933:gpt4o-mini",
    "2508.11933:gemini15-pro",
):
    RESULT_CODE[_result_id] = "commercial_closed"
RESULT_CODE["2508.11933:raidar"] = "exclude_rewriting"


CANONICAL_PAPERS = {
    "2606.23336": "papers/canonical_wavedetect_2606.23336.pdf",
    "2509.14268": "papers/canonical_detectanyllm_2509.14268.pdf",
    "2508.11343": "papers/canonical_specdetect_2508.11343.pdf",
    "2501.03940": "papers/canonical_pawn_2501.03940.pdf",
}

EXPECTED_FIELDS = (
    "parent_id",
    "account_id",
    "system",
    "account_kind",
    "evidence_locator",
    "qualifying_evidence",
)
ACCOUNT_MAP_FIELDS = (
    "parent_id",
    "account_id",
    "resolution_kind",
    "target_id",
)
SOURCE_FIELDS = (
    "parent_id",
    "title",
    "paper_path",
    "pdf_sha256",
    "text_sha256",
    "mapping_kind",
    "publication_role",
    "resolution",
    "expected_account_count",
    "inspected_scope",
    "reason",
)
RESULT_FIELDS = (
    "parent_id",
    "result_id",
    "system",
    "version",
    "claim",
    "metric_scope",
    "qualifying_basis",
    "primary_source",
    "artifact_status",
    "disposition_code",
    "disposition",
    "source_card",
)


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _paper_path(external_root: Path, parent_id: str) -> Path:
    preferred = CANONICAL_PAPERS.get(parent_id, f"papers/{parent_id}.pdf")
    path = external_root / preferred
    if path.is_file():
        return path
    versioned = sorted((external_root / "papers").glob(f"{parent_id}v*.pdf"))
    if len(versioned) == 1:
        return versioned[0]
    raise FileNotFoundError(f"no unique preserved primary PDF for {parent_id}")


def _extract_text(path: Path) -> bytes:
    completed = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def _write_tsv(path: Path, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def build(external_root: Path) -> tuple[int, int, int]:
    import audit_coverage as audit

    exports, _ = audit.load_exports(HERE)
    mappings = audit.load_mappings(HERE / "coverage_row_dispositions.tsv")
    composite_sources = audit.load_composite_sources(
        HERE / "coverage_composite_sources.tsv"
    )
    embedded_results = audit.load_embedded_results(
        HERE / "coverage_embedded_results.tsv"
    )
    embedded_by_parent: dict[str, list[audit.EmbeddedResult]] = {}
    for result in embedded_results:
        embedded_by_parent.setdefault(result.parent_id, []).append(result)

    export_ids = {export.arxiv_id for export in exports}
    decision_ids = (
        set(PRIMARY_GROUPS) | set(embedded_by_parent) | set(NO_ACCOUNT_REASONS)
    )
    if decision_ids != export_ids:
        raise ValueError(
            "paper-level full-text decision partition mismatch: "
            f"missing={','.join(sorted(export_ids - decision_ids)) or 'none'}; "
            f"unknown={','.join(sorted(decision_ids - export_ids)) or 'none'}"
        )
    if set(NO_ACCOUNT_REASONS) & (set(PRIMARY_GROUPS) | set(embedded_by_parent)):
        raise ValueError("no-account paper also has an expected result account")

    if set(EVIDENCE) != set(PRIMARY_GROUPS) or set(MECHANISM) != set(PRIMARY_GROUPS):
        raise ValueError("primary inventory metadata does not match its parent set")
    primary_ids = {
        f"{parent_id}:{slug}"
        for parent_id, configurations in PRIMARY_GROUPS.items()
        for slug, _ in configurations
    }
    override_ids = (
        RESULT_EVIDENCE.keys()
        | RESULT_MECHANISM.keys()
        | RESULT_OUTCOME.keys()
        | RESULT_CODE.keys()
    )
    if not override_ids <= primary_ids:
        raise ValueError("result-specific override lacks a primary inventory row")

    primary_result_rows: list[dict[str, str]] = []
    for parent_id in sorted(PRIMARY_GROUPS, reverse=True):
        mapping = mappings[parent_id]
        for slug, system in PRIMARY_GROUPS[parent_id]:
            result_id = f"{parent_id}:{slug}"
            evidence = RESULT_EVIDENCE.get(result_id, EVIDENCE[parent_id])
            mechanism = RESULT_MECHANISM.get(result_id, MECHANISM[parent_id])
            outcome = RESULT_OUTCOME.get(result_id, mapping.reason)
            default_code = (
                "reject_scope"
                if mapping.mapping_kind == "non_candidate_class"
                else mapping.disposition_code
            )
            disposition_code = RESULT_CODE.get(result_id, default_code)
            primary_result_rows.append(
                {
                    "parent_id": parent_id,
                    "result_id": result_id,
                    "system": system,
                    "version": system,
                    "claim": evidence,
                    "metric_scope": evidence,
                    "qualifying_basis": "Named submitted/proposed/fitted configuration with a threshold metric or explicit high-performance result in the cited full-text table scope.",
                    "primary_source": f"https://arxiv.org/abs/{parent_id}",
                    "artifact_status": outcome,
                    "disposition_code": disposition_code,
                    "disposition": f"{mechanism}. {outcome}",
                    "source_card": f"Full-text source {parent_id}",
                }
            )

    expected_rows: list[dict[str, str]] = []
    map_rows: list[dict[str, str]] = []
    source_rows: list[dict[str, str]] = []
    seen_accounts: set[str] = set()

    for export in exports:
        parent_id = export.arxiv_id
        mapping = mappings[parent_id]
        accounts: list[tuple[str, str, str, str, str, str]] = []

        for result in embedded_by_parent.get(parent_id, []):
            accounts.append(
                (
                    result.result_id,
                    result.system,
                    "embedded_result",
                    result.metric_scope,
                    result.claim,
                    result.result_id,
                )
            )

        if parent_id in PRIMARY_GROUPS:
            for slug, system in PRIMARY_GROUPS[parent_id]:
                result_id = f"{parent_id}:{slug}"
                accounts.append(
                    (
                        result_id,
                        system,
                        "primary_result",
                        "Primary PDF full text and all main/appendix result tables",
                        RESULT_EVIDENCE.get(result_id, EVIDENCE[parent_id]),
                        result_id,
                    )
                )

        for account_id, system, kind, locator, evidence, target_id in accounts:
            if account_id in seen_accounts:
                raise ValueError(f"duplicate full-text account {account_id}")
            seen_accounts.add(account_id)
            expected_rows.append(
                {
                    "parent_id": parent_id,
                    "account_id": account_id,
                    "system": system,
                    "account_kind": kind,
                    "evidence_locator": locator,
                    "qualifying_evidence": evidence,
                }
            )
            map_rows.append(
                {
                    "parent_id": parent_id,
                    "account_id": account_id,
                    "resolution_kind": kind,
                    "target_id": target_id,
                }
            )

        composite = composite_sources.get(parent_id)
        if accounts:
            kinds = {item[2] for item in accounts}
            resolution = "+".join(sorted(kinds))
            reason = f"Full text yields {len(accounts)} exact account(s); the immutable account inventory is compared with distinct disposition targets."
        else:
            resolution = "no_qualifying_account"
            reason = NO_ACCOUNT_REASONS[parent_id]

        if parent_id in PRIMARY_GROUPS:
            inspected_scope = "Full text; every main and appendix result table; separately named submitted/proposed/fitted configurations; dataset, generator, domain, length, validation/test, mechanism, artifact, and timing statements."
        elif composite is not None:
            inspected_scope = composite.inspected_scope
        else:
            inspected_scope = "Full text and every result table; proposed/submitted system identities, versions, variants, datasets, operating points, mechanisms, artifact statements, and timing claims."

        paper = _paper_path(external_root, parent_id)
        extracted = _extract_text(paper)
        source_rows.append(
            {
                "parent_id": parent_id,
                "title": export.title,
                "paper_path": paper.relative_to(external_root).as_posix(),
                "pdf_sha256": _sha256_path(paper),
                "text_sha256": _sha256_bytes(extracted),
                "mapping_kind": mapping.mapping_kind,
                "publication_role": (
                    composite.composite_kind
                    if composite is not None
                    else "primary_or_noncandidate_publication"
                ),
                "resolution": resolution,
                "expected_account_count": str(len(accounts)),
                "inspected_scope": inspected_scope,
                "reason": reason,
            }
        )

    _write_tsv(
        HERE / "coverage_primary_results.tsv", RESULT_FIELDS, primary_result_rows
    )
    _write_tsv(
        HERE / "coverage_fulltext_expected_accounts.tsv", EXPECTED_FIELDS, expected_rows
    )
    _write_tsv(HERE / "coverage_fulltext_account_map.tsv", ACCOUNT_MAP_FIELDS, map_rows)
    _write_tsv(HERE / "coverage_fulltext_sources.tsv", SOURCE_FIELDS, source_rows)
    return len(source_rows), len(expected_rows), len(primary_result_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--external-root", type=Path, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    counts = build(arguments.external_root.resolve())
    print(f"sources={counts[0]} accounts={counts[1]} primary_results={counts[2]}")
