# Negative Questioning for Alignment Models to Reduce Hallucinations

*Prepared 2025-09-04*

---

## Table of Contents
1. Executive Summary  
2. Problem Statement  
3. Taxonomy of “Negative Questioning” Paradigms  
   3.1 Stage I – RL-style Alignment Fine-Tuning  
   3.2 Stage II – Adversarial Evaluation Protocols  
   3.3 Stage III – Inference-Time Prompting  
4. Survey of Pertinent Prior Work  
   4.1 AutoDebug  
   4.2 MixCL  
   4.3 Med-HALT  
5. Benchmarking & Metrics  
   5.1 Canonical Public Benchmarks  
   5.2 Domain-Specific Extensions  
   5.3 New Metrics We Propose  
6. System Design Recommendations  
   6.1 Data Pipeline  
   6.2 Model Family & Compute Envelope  
   6.3 Training Objectives & Loss Functions  
7. Experimental Roadmap  
   7.1 MVP Schedule  
   7.2 Ablation Grid  
8. Risk Analysis & Mitigations  
9. Forward-Looking and Contrarian Ideas (Flagged ‑– Speculative)  
10. Concluding Remarks  

---

## 1  Executive Summary
Hallucinations—unfaithful assertions produced by large language models (LLMs)—remain the blocking safety flaw limiting industrial deployment in high-stakes contexts. The user proposes **Negative Questioning**: proactively injecting adversarial or contradiction-seeking prompts so the model learns or is forced to verify its knowledge. We synthesize three lines of recent research—AutoDebug, MixCL, and Med-HALT—with established alignment techniques (RLHF, RLAIF, constitutional AI) and with contemporary hallucination benchmarks (TruthfulQA, FaithDial, synthetic counterfactual suites). We articulate a full blueprint for:

1. **Fine-tuning with negative questions as hard negatives** (training-time alignment).  
2. **Automated adversarial evaluation loops** that continuously mine new failure modes.  
3. **Runtime negative elicitation strategies** that modulate the model’s epistemic state (inference-time).

Empirical targets are ≥40 % reduction in hallucination rates on open-domain datasets and ≥60 % on domain-specialized tasks (e.g., clinical Q-A), while capping compute at <250 GPU-days for 7–13 B models.

---

## 2  Problem Statement

Given an LLM *F* with parameters θ that is already roughly instruction-follow tuned, we want to produce a new model *F′* = *F*(θ′) with dramatically lower factual error *without* sacrificing creativity or latency. Hallucinations are challenging because:
• Ground-truth references are sparse, especially for open-ended tasks.  
• The loss landscape often fails to penalize plausible-sounding but wrong generations (Positivity Bias).  
• Existing RLHF reward models are themselves prone to hallucinate assessments.

Negative questioning reframes the issue: instead of merely maximizing reward for correct answers, the training or prompting pipeline dedicates capacity to answering **negative (counterfactual, adversarial, or contradiction-seeking) queries** such that hallucination modes are surfaced and punished.

---

## 3  Taxonomy of “Negative Questioning” Paradigms

### 3.1  Stage I – RL-Style Alignment Fine-Tuning (Training-Time)

1. **Curriculum of Adversarial Prompts**: Begin with mild negatives (“State something the Eiffel Tower is *not* made of”) and escalate to subtle disinformation (“Explain why Van Gogh became a Cubist in 1905”).
2. **Mixed Contrastive Objectives**: Combine positive factual pairs (q, a*) and hard negatives (q, â) in a combined reward *R* = α·R_pos – β·R_neg (cf. MixCL).  
3. **Reward Model Re-Weighting**: The RM is co-trained on both correctness and *counter-knowledge rejection* labels, encouraging a monotone decrease in log-probability of hallucinations.
4. **Policy Self-Consistency Check**: Penalize variance across independently sampled generations for the same question (self-consistency metric).

### 3.2  Stage II – Adversarial Evaluation Protocols (Post-Training)

1. **AutoDebug-Style Chain Generation**: Use a smaller, cheaper LLM to generate candidate adversarial questions that aim to trick or confuse *F′*.  
2. **Transferability Filter**: Only keep those adversaries that cause F′ to fail with probability ≥p but are answered correctly by an oracle (human or GPT-4o).  
3. **Rolling Benchmark Augmentation**: Append surviving adversaries back into the evaluation set to continuously raise the bar.

### 3.3  Stage III – Inference-Time Prompting (Runtime)

1. **Implicit Negative Prompting**: Wrap user queries with an internal prelude: “List any assumptions you are uncertain about and explicitly say ‘I’m not sure’ when knowledge is missing.”
2. **Self-Critique Re-asking**: After an answer A, automatically pose a mirrored negative question: “Why might A be wrong?” and check for contradictions.
3. **Dynamic Retrieval Fallback**: If the model’s internal uncertainty above a threshold δ, switch to retrieval-augmented generation (RAG) or escalate to human assistance.

---

## 4  Survey of Pertinent Prior Work

### 4.1  AutoDebug (Huang et al., 2023)
• Chains of prompts were crafted to elicit knowledge conflicts, leading to **34–58 pp** accuracy drops even in GPT-4.  
• Crucially, adversarial sets *transfer* across model sizes, implying we can mine negatives with a 3-B model and use them to align a 70-B model.  
• Lesson: **Negative questioning is inexpensive to scale**; small models discover patterns large models still fall for.

### 4.2  MixCL (Xu et al., AAAI-24)
• Introduces a **mixed contrastive loss**: L = λ·L_pos + (1–λ)·L_neg, where hard negatives come from (i) retrieval over KB, (ii) model-generated counterfactuals.  
• On Wizard-of-Wikipedia, MixCL LLaMA-13 B hit **0.46 F1 fact score**—competitive with retrieval-augmented systems but w/o retrieval overhead.  
• Lesson: Hard negatives + contrastive signal reduce hallucination **without external KB latency**—useful when RAG is infeasible.

### 4.3  Med-HALT (Moore et al., 2023)
• Multilingual, 26k Q-A pairs from medical licensing exams.  
• Separates **reasoning hallucinations** (chain-of-thought deviates) from **memory hallucinations** (named entities wrong).  
• GPT-3.5 scored 54 %, Llama-2-70 B 37 %—gap shows domain-fine-tuning needs aggressive hallucination control.  
• Lesson: **Domain safety** (e.g., healthcare) requires specialized negative questioning; cross-lingual considerations apply.

---

## 5  Benchmarking & Metrics

### 5.1  Canonical Public Benchmarks
• TruthfulQA (MC + Gen): score ↘ indicates truthfulness errors.  
• FaithDial: dialogue-centric factual alignment.  
• CounterFact & FACTA: entity-consistent counterfactual edits.  
• AGIEval adversarial subset (complex multi-step reasoning).

### 5.2  Domain-Specific Extensions
• Med-HALT (healthcare)  
• FinQA (finance)  
• GovReport-Hall (public policy summarization; hallucination annotations)  
• MultiModal: HallusionBench-MM pairs text + image negatives.

### 5.3  New Metrics We Propose
1. **Negative Agreement Rate (NAR)**: % of adversarial negatives where model answers “unknown/unverifiable”.  
2. **Counter-Assertion Consistency (CAC)**: KL divergence between answer distributions when question is stated vs negated (“X is not Y”).  
3. **Self-Critique Recall (SCR)**: fraction of hallucinations subsequently caught by model’s own critique.

---

## 6  System Design Recommendations

### 6.1  Data Pipeline
1. **Source Pools**: (i) Wikipedia + wikidata triples, (ii) newswire (knowledge volatile), (iii) synthetic counterfactual generator (via AutoDebug-lite).  
2. **On-the-Fly Adversaries**: During RL rollouts, sample k = 2–4 negatives per positive by entity swapping or tense reversal.  
3. **Dedup & Leakage Control**: Keep validation questions unseen (use MinHash + semantic hashing with threshold 0.85).

### 6.2  Model Family & Compute Envelope
• *Baseline*: Open-weights Llama-3 8 B (text) or Qwen-VL-7 B (multimodal).  
• 80 % of budget (200 GPU-days on A100) on RLHF with contrastive reward; 20 % on RM training + evaluation sweeps.  
• Mixed-precision (FP16/BF16) + sequence parallelism; memory cap 80 GB/GPU.

### 6.3  Training Objectives & Loss Functions
L_total = L_sft + γ·L_RL + η·L_contrastive + ζ·L_uncertainty, where:
• L_RL uses sparse reward: +1 correct, −2 hallucination, −0.5 uncertain but acceptable.  
• L_uncertainty penalizes over-confidence: cross-entropy vs calibrated temperature scaling target.

---

## 7  Experimental Roadmap

### 7.1  MVP Schedule (12 Weeks)
1. **Week 1–2**: Build negative generator (AutoDebug port) & ingest initial 50k adversaries.  
2. **Week 3–4**: Train reward model on composite (TruthfulQA + negatives).  
3. **Week 5–7**: RLHF + MixCL contrastive fine-tune.  
4. **Week 8**: Offline evaluation on benchmarks; calibrate thresholds.  
5. **Week 9–10**: Deploy to inference harness with self-critique plugin.  
6. **Week 11–12**: Red-teaming sprint; patch catastrophic failures.

### 7.2  Ablation Grid
• Toggle contrastive weight η ∈ {0, 0.3, 0.6}.  
• Compare negative sources: human vs synthetic vs retrieval.  
• Evaluate scaling law: 7 B vs 13 B vs 34 B; compute constant.

---

## 8  Risk Analysis & Mitigations
• **Mode Collapse**: Excess negative pressure causes the model to answer “I don’t know” universally. Mitigation: reward uncertainty only when warranted (calibrated via NLL threshold).
• **Spurious Negatives**: Poorly crafted negatives teach wrong facts. Use filtered pipeline with oracle verification.
• **Evaluation Overfitting**: Adversarial test set leaks; enforce strict data hygiene and periodic holdout refresh.

---

## 9  Forward-Looking & Contrarian Ideas (Speculative)
1. **Neural Differential Game**: Treat alignment as min-max; adversary and policy co-evolve every gradient step (GAN-like). May uncover deeper hallucination modes but risks instability.  
2. **Epistemic Memory Module**: Separate “belief” vectors and require negative questioning to update an explicit uncertainty tensor; akin to Bayesian posterior within transformer.  
3. **Agentic Negative Critic**: Spin up a secondary autonomous agent tasked only with refuting the main model; could run one or two inference steps per user query if latency budget allows.  
4. **Cross-Modal Negatives**: Supply contradictory images to text prompts (“This image shows a dog wearing a cat collar; describe the cat”). Test multimodal hallucination.

---

## 10  Concluding Remarks
Negative questioning provides a unifying lens over diverse anti-hallucination techniques: from adversarial data augmentation (AutoDebug) to mixed contrastive objectives (MixCL) and domain-specific safety suites (Med-HALT). By integrating these under a staged pipeline—training, evaluation, inference—we can create LLMs that not only answer correctly but *know when they can be wrong*. The proposed benchmarks (NAR, CAC, SCR) will quantify progress; the experimental roadmap constrains compute; and speculative routes signal further upside.

If executed, we anticipate halving hallucination rates on standard tasks, and—more importantly—gaining a scalable methodology for continuous improvement as model sizes and deployment domains grow.


## Sources

- http://arxiv.org/abs/2308.15126
- https://zenodo.org/record/8296440
- http://arxiv.org/abs/2202.03629
- http://arxiv.org/abs/2310.12516
- http://arxiv.org/abs/2308.11764
- https://research.rug.nl/en/publications/8e18419a-ed43-4be6-a0ca-7d55eb0d57df
- http://hdl.handle.net/10251/201319
- http://arxiv.org/abs/2307.15343
- https://zenodo.org/record/7137373
- https://ojs.aaai.org/index.php/AAAI/article/view/26596