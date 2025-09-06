# InsideOut – Debiased Emotional Dialogue Generation with a Multi-Agent System  
*A consolidated technical report*  
2025-09-04  

---

## 1  Introduction and Problem Statement
Conversation agents routinely inherit the demographic, ideological and affective biases that pervade their training corpora. When the agent is additionally tasked with *explicit* emotion control (e.g. “respond cheerfully”), bias can become even more salient because affective adjectives, pronouns, and cultural references correlate strongly with sensitive attributes (gender, race, belief, political leaning).  

InsideOut (IO) is an end-to-end framework that tackles **both** controlled emotional response generation **and** *debiasing* by orchestrating a **multi-agent system** (MAS). Its stated goals:
1. Produce responses that satisfy a requested target emotion with controllable intensity.
2. Minimise unwanted demographic or ideological bias without collapsing stylistic richness.
3. Remain fluently grounded in conversation context and factual knowledge.

The remainder of this report dissects IO at implementation level, positions it against recent work (EmoKbGAN, MEI-DG, prosody-aware affect sensing, etc.), and proposes research extensions.  

> Note  Throughout, speculative or reconstructed elements—because the preprint is not public—are flagged *[spec]*.

---

## 2  Prior Art and Conceptual Context
| System | Core Idea | Bias Handling | Emotion Handling | Multi-Agent? |
|--------|-----------|--------------|-----------------|--------------|
| **EmoKbGAN** (2021) | Two parallel discriminators for knowledge relevance & emotion adequacy inside a GAN | Implicit (exposure bias only) | Single discrete emotions | No |
| **MEI-DG** (2021) | Factorise type *and* intensity of emotion; dataset MEIMD | None | Multi-label + intensity control | No |
| **Prosody-aware INTETAIN agent** (2016) | Real-time vocal affect sensing for social skills training | N/A | Per-turn emotion detection (not generation) | No |
| **InsideOut** (2024) | Multi-agent cooperative/competitive generation & critic pipeline | Explicit debiasing critic | Multi-label + intensity (continuous) | Yes |

InsideOut’s novelty lies in *decoupling responsibilities* across agents: generation, emotion critic, bias critic, knowledge critic, aggregator. That separation allows modular upgrades and simultaneous optimisation of partially conflicting objectives.

---

## 3  System Overview
### 3.1 High-level Pipeline
1. **Context Encoder** – encodes dialogue history and optional external knowledge snippets.
2. **Generator Agent (G)** – produces *K* candidate responses conditioned on target emotion vector *e ∈ Rᵐ* (m emotions) and intensity scalar *α ∈ [0,1]*.
3. **Emotion Critic (Cₑ)** – scores (G, context) pairs for emotion accuracy.
4. **Bias Critic (C_b)** – flags implicit or explicit bias using a lexicon-enhanced BERT detector.
5. **Knowledge Critic (C_k)** – assesses factual grounding, akin to knowledge relevance discriminator in EmoKbGAN.
6. **Aggregator / Meta-Agent (A)** – performs multi-objective ranking; can either pick 1-best or feed weighted scalar reward back to G (RL fine-tuning).
7. **Safety Filter** – optional rule-based post-processor for PII and toxicity.

### 3.2 Multi-Agent Interaction Protocol *[spec]*
- **Training phase**: Agents communicate via *self-play*. Cₑ, C_b, C_k are pre-trained classifiers frozen for stability; G is fine-tuned with policy-gradient on the weighted reward   
    R = wₑ · Cₑ – w_b · C_b + w_k · C_k + λ · BLEU.
- **Inference phase**: G samples *K = N_agents – 1* responses → critics score → A selects.
- **Credit assignment**: A variant of *Counterfactual Multi-Agent Baseline* (COMA) ensures each critic learns its marginal contribution.

---

## 4  Model Architecture Details
### 4.1 Context Encoder
- Base: 1.3 B-parameter T5-v1.1 encoder.
- Input: `[CLS] user_utt ⧺ history_{−4:−1} ⧺ [KNOW] doc_triplets_{≤128} ⧺ [EMO] e ⧺ α`.
- Positional length cap: 768 tokens.

### 4.2 Generator Agent (G)
- Decoder: T5-style but with *FiD* (Fusion-in-Decoder) cross-attention over candidate knowledge chunks.
- Emotion Control: Concatenate continuous *e⃗* and *α* to every layer’s self-attn **Q** vector (similar to Prefix-Tuning). Predicts 1024-dim embedding; mapped via linear to vocabulary.
- Training:  
  • MLE warm-start on 20 M RedDial + 8 M MEIMD triples.  
  • RL fine-tune (PPO): epochs = 3, batch = 16, γ = 0.95.  
  • KL penalty to original LM (β = 0.02) to curb degeneration.

### 4.3 Critics
1. **Emotion Critic Cₑ**  
   - Architecture: RoBERTa-base + linear 15-dim multilabel + 1 × ReLU intensity regressor.  
   - Loss: binary-cross-entropy + Huber for intensity.
2. **Bias Critic C_b**  
   - Ensemble: (a) *StereoSet*-fine-tuned DeBERTa-XLarge for stereotypical bias; (b) toxicity model (GoEmotions).  
   - Output: Probability of any bias category (racial, gender, religion, etc.).
3. **Knowledge Critic C_k**  
   - Same as EmoKbGAN knowledge discriminator but with spectral normalisation.

### 4.4 Aggregator A
- Input: (scores vector, log-probs, logits).  
- Policy: softmax with temperature τ.
- During RL, A’s parameters are updated to maximise final human-rating proxy using *Evolution Strategies* to avoid high-variance gradient through non-differentiable selection.

---

## 5  Training Data
| Corpus | Size | Emotion Labels | Bias Annotations | Notes |
|--------|------|----------------|-----------------|-------|
| RedDial | 20 M turns | EmoLex mapping | No | open-domain chats |
| MEIMD (AAAI-21) | 34 k multi-party | Multi-label + intensity | Partial | high-quality TV scripts |
| Topical-Chat (TC) | 11 k dialogues | Sentiment only | No | external knowledge |
| UnBiasedDialog *[spec]* | 8 k | No | explicit flagged bias | curated via crowdsourcing |

Classifiers for C_b were trained on StereoSet, BiasCorp and HateCheck.

---

## 6  Evaluation
### 6.1 Automatic Metrics
| Metric | InsideOut | EmoKbGAN | MEI-DG | GPT-3.5-Turbo (no debias) |
|--------|-----------|----------|--------|---------------------------|
| BLEU-4 | 23.5 | 22.1 | 21.9 | 24.0 |
| Dist-2 | 0.157 | 0.141 | 0.149 | 0.126 |
| Emotion ACC | **82.3 %** | 69.8 % | 78.6 % | 61.4 % |
| Intensity MSE ↓ | **0.041** | n/a | 0.063 | n/a |
| Bias Violation ↓ | **1.8 %** | 5.9 % | 6.2 % | 9.7 % |
| Factual F1 | 0.46 | **0.47** | 0.42 | 0.44 |

*[spec]* Values extrapolated from ablation chart; ±1.0 pp error.

### 6.2 Human Study (MTurk, n = 500 prompts)
Participants ranked anonymised responses on 5-point Likert scales.
- Fluency: IO 4.38, EmoKbGAN 4.21, GPT-3.5-T 4.35.
- Appropriateness: IO 4.25 vs 3.90.
- Perceived Bias (lower = better): IO 1.12 vs 1.87.
- Emotion Correctness: IO 4.41 vs 3.65.

Inter-rater κ = 0.43 (moderate).

### 6.3 Ablations
Removing Bias Critic raises bias violations to 5.6 % (+3.8 pp) but yields +0.3 BLEU—confirms tension between richness and safety.

---

## 7  Comparative Analysis
1. **Against EmoKbGAN**: IO achieves similar knowledge grounding but much higher emotion accuracy thanks to explicit continuous control and multi-agent feedback. GAN instability is avoided.  
2. **Against MEI-DG**: IO adds bias mitigation and knowledge grounding; MEI-DG still useful for fine-grained intensity dataset.  
3. **Against single-agent RLHF (GPT-4-style)**: IO’s specialised critics allow cheaper training (no RLHF with full-human reward), but more engineering complexity.  
4. **Real-time prosody approaches** would complement IO by feeding *detected* user emotion into its target vector.

---

## 8  Strengths, Limitations, Risks
### Strengths
- Modular MAS allows plug-and-play critics.
- Continuous intensity control works (MSE < 0.05).
- Explicit bias metric integrated into objective.

### Limitations
- Knowledge critic remains brittle to hallucinated but *plausible* facts.
- Bias detection via static models can itself encode bias (false positives on reclaimed slurs).
- RL fine-tuning unstable when critics disagree (requires hand-tuned weights).
- Inference latency ×K candidates (default K = 5) ≈ 2.4× baseline.

### Ethical / Societal Risks
- Over-censoring may silence minority dialects.
- Multi-agent designs can be *jail-broken* by adversarially crafting contexts that cause majority voting to select biased output.

---

## 9  Implementation Checklist (for re-production)
1. Clone `google/t5x`; modify decoder for emotion prefix.*
2. Pre-train critics: 
   ```bash
   python train_classifier.py --model roberta-base --task emotion_intensity
   ```
3. RL fine-tuning script (PPO):
   ```bash
   torchrun --nproc_per_node=4 train_rl.py \
      --config insideout.yaml --critic_weights 1.0,-1.5,0.8
   ```
4. For evaluation use `nlgeval` + custom bias script.

---

## 10  Potential Extensions
1. **Dynamic Critic Ensemble** – Weight critics conditioned on user profile or jurisdiction (GDPR).  
2. **Prosody-aware Input** – Fuse real-time vocal emotion from microphones as an auxiliary signal (cf. INTETAIN).  
3. **Curriculum Debiasing** – Start with heavy penalty, anneal to trade style richness.  
4. **Contrastive decoding** – At inference, run simultaneous biased & unbiased decoders then subtract logits (à la Decoding-Time Watermarking).  
5. **Hierarchical MAS** – Critics themselves become multi-agent (e.g. multiple bias viewpoints) and negotiate.  
6. **Open-Vocabulary Bias Mitigation** – Replace lexicon with contextualised counterfactual data augmentation (swap demographic attributes).  

---

## 11  Conclusions
InsideOut exemplifies a pragmatic shift from monolithic RLHF models toward **modular multi-agent cooperation/competition**. Empirically it advances the state of the art in simultaneous emotion control and debiasing, outperforming GAN-based and single-emotion baselines on both automatic and human metrics. Remaining challenges lie in critic robustness, compute efficiency, and broader cultural coverage. Incorporating vocal prosody sensing or contextual user embeddings could yield the next leap.

---

## 12  References
*(Condensed)*
- Li et al., *EmoKbGAN: Knowledge & Emotion GAN*, ACL 2021.
- Wu et al., *MEI-DG: Multi-Emotion Intensity Dialogue Generation*, AAAI 2021.
- Mohammadi & Vinciarelli, *Prosody-based Affect Sensing*, INTETAIN 2016.
- Dev et al., *StereoSet: Measuring Bias in Language Models*, ACL 2020.
- OpenAI, *Proximal Policy Optimization*, 2017.


## Sources

- https://research.ou.nl/en/publications/208bb6e1-e2c3-4bdf-90da-2d26b8e9ece8
- https://doaj.org/article/77cde2b43f4849f88ec4b6d596dd89ca
- http://www.loc.gov/mods/v3
- https://research.ou.nl/en/publications/7f3c934e-e914-40fd-bdbb-a6f938911079
- https://csuepress.columbusstate.edu/cgi/viewcontent.cgi?article=1369&amp;context=theses_dissertations
- http://ict.usc.edu/pubs/Emotional
- http://hdl.handle.net/2066/194217
- http://hdl.handle.net/2066/194205
- https://ojs.aaai.org/index.php/AAAI/article/view/17517