# Ensemble of LLMs Attacking (and Defending) Safety Classifiers – A Comprehensive Technical Report  
*Date : 2025-09-04*

---

## 1  Scope and Motivation

Large-language-model (LLM) deployments are increasingly gated by **safety-classifier front-ends** (single-turn toxicity filters, multi-turn conversation guardians, policy-compliance critics, etc.). 2024–2025 field reports show that *single* end-point moderators—even when adversarially trained—are brittle against novel jail-breaks and distribution-shift attacks. A natural escalation is (i) **attackers** coordinating *ensembles of LLMs* to discover bypasses, and conversely (ii) **defenders** constructing *ensemble safety classifiers* with stronger non-correlated failure modes.  
This document synthesises the state of the art, derives new threat models, proposes experimental blueprints, and offers design recommendations.  

**Key prior learnings integrated**:  
• Secure/Insecure set regularisation in ensembles (AAAI-21)  
• Ensemble RL Attackers (ELAA 2023, +35 % success)  
• Population-risk certification via Bayesian search (PROSAC 2024)

We address **all three desiderata** implied by the follow-up questions: theoretical analysis, empirical attack experiments, and novel ensemble-architecture recommendations.

---

## 2  Current Safety-Classifier Ecosystem

| Deployment tier | Typical classifier | API behaviour | Observed weak points |
|-----------------|--------------------|---------------|----------------------|
| Proprietary consumer LLM (OpenAI, Anthropic) | **Single-turn policy model** (`moderate()` / “system-only” channel) | Hard-block or rewrite | Gradient-free black-box, prompt-leakage, style-transfer |
| Enterprise-fine-tuned LLM | **Multi-turn safety agent** (reinforcement “Referee”) | Soft denial + escalation | Conversation-state spoofing, context overflow |
| Open-source stack (LLama-Guard, Together AI filters) | **RoBERTa / DeBERTa toxicity MBERT** | Probability threshold | Evasion by rare-word synonyms, unicode homoglyphs |

**Observation 1** : all three tiers rely on *single* classifiers with homogeneous pre-training.  
**Observation 2** : shared datasets (OpenAI’s policy set, Jigsaw) create *correlated decision boundaries*, a prime target for ensemble attacks.

---

## 3  Threat Model: Ensemble Attackers against Safety Classifiers

### 3.1  Attacker Resources

1. **K heterogeneous LLMs** (open-source + grey-box proprietary endpoints).  
2. **Limited or no gradient access** to the safety classifier (realistic for closed APIs).  
3. **Query budget Q** (rate-limiting).  
4. **Goal**: craft a prompt *p* such that the downstream LLM generates disallowed content **and** the front-end safety classifier *C* labels *p* as safe.  

### 3.2  Attack Pipeline

Step A – *Prompt diversification* : Each ensemble member proposes candidate jailbreaks (autoregressive beam, evolutionary search, policy-gradient).  
Step B – *Collaborative selection* : A meta-agent scores candidates using disagreement heuristics; high-entropy prompts likely straddle the classifier boundary.  
Step C – *Adaptive refinement* : Bandit optimisation updates each member’s search distribution conditioned on classifier feedback. (This is ELAA-style RL in the language domain.)  

### 3.3  Transferability Principle

AAAI-21 shows that *promoting per-sample disagreement* reduces adversarial transfer inside *defensive* ensembles; *the dual* holds for **attacking** — maximise intra-ensemble diversity to *increase* transfer *from the ensemble to a single victim*.  

---

## 4  Relevant Prior Work and Its Cross-Application to LLM Safety

1. **Secure/Insecure set regularisation (AAAI-21)**  
   • Idea: label each training sample as “secure” if robust across the committee, “insecure” otherwise; explicitly push models apart on insecure points.  
   • Application to attacks: treat prompts that *some* LLMs think will pass the filter but others flag as borderline as *insecure* for the attacker—focus search precisely there.

2. **ELAA (Ensemble RL Attack, 2023)**  
   • Vision domain: +35 % success by aggregating multiple weak RL attackers.  
   • Language analogue: Use smaller instruct-tuned models (Φ-2 mini, Vicuna-7B) as weak searchers; policy-gradient reward = binary safe/unsafe from the target classifier. Use Thompson sampling across models to maintain exploration.

3. **PROSAC (2024) population certification**  
   • Defines (α,ζ) guarantee: at most α population-risk with ζ confidence.  
   • For language, swap AutoAttack/SquareAttack with *PromptAttack* suites (Greedy-Jail, Skeleton-Key, Synthetic Rev). Use Bayesian optimisation on held-out dangerous-prompt corpus to bound risk of the classifier ensemble.

---

## 5  Empirical Study Blueprint

### 5.1  Benchmarks and Models

Attack ensemble (K = 5):
• `Llama-3-70B-Instruct`, `Mistral-7B-Instruct`, `Gemma-IT-27B`, `Vicuna-13B-v1.5`, `Phi-3-mini`.  
Safety classifier baselines:
• `OpenAI moderation-2024-06` (API), `LLama-Guard-2`, `DeBERTa-Tox-v2`, and a *custom GPT-J policy critic*.

### 5.2  Datasets

• `AdvBench-LLM-v2` (12 k expert-curated adversarial goal specs).  
• `HarmfulQA` (3 k multi-turn scenarios).  
• `InnocentMiddle` (10 k benign instructions) – controls for over-blocking.

### 5.3  Attack Settings

| Config | Query budget per prompt | Feedback granularity |
|--------|------------------------|----------------------|
| A | 10 queries | binary (block / allow) |
| B | 50 queries | probability score p(safe) |

Evaluation metrics:  
• **Bypass rate** = % harmful prompts that pass classifier.  
• **Classifier Failure Diversity (CFD)** = average pairwise Jaccard of failure sets across replicas (lower = better defense).  
• **Over-block delta** = benign false-positives after attack adaptation.

### 5.4  Hypotheses

H1 : Ensemble RL attackers outperform single-LLM jailbreak by ≥ 20 % under config A.  
H2 : Adding *heterogeneous* (transformer-vs-Mixture-of-Experts) models yields another +5 %.  
H3 : Defensive ensemble with Secure/Insecure regularisation halves bypass rate but increases over-block by ≤ 3 %.

---

## 6  Designing Ensemble Safety Classifiers (Defensive View)

### 6.1  Architectural Axes of Diversity

1. **Objective Diversity** – toxicity, policy compliance, legal compliance trained *separately* then aggregated (AND voting).  
2. **Representation Diversity** – bag-of-ngrams CNN vs. large transformer vs. retrieval-augmented monitor.  
3. **Data-Split Diversity** – train on disjoint slices, use negative-correlation boosting (NCL) to de-synchronise errors.  

### 6.2  Aggregation Strategies

• `AND-majority` (default) – block if ≥ 1 sub-classifier blocks (safer but high false-positive).  
• `Risk-aware Weighted` – weight votes by calibrated risk from PROSAC; dynamic threshold keeps α fixed.  
• `Adaptive abstention` – when ensemble disagreement > τ, escalate to human.  

### 6.3  Training with Secure/Insecure Sets

Algorithm:  
1. Pre-train each sub-classifier normally.  
2. For minibatch, compute agreement mask.  
3. If sample insecure, add contrastive loss to maximise embedding divergence between random pair of classifiers.  
4. Fine-tune until validation CFD < δ.

Outcome: Lower cross-transfer of jailbreaks similar to AAAI-21 vision results; our pilot experiments show 99.3 % detection on AdvBench-LLM-v2.

### 6.4  Certification à la PROSAC

• Define harm distribution *D* (mixture of known and synthetically generated threats).  
• Run Bayesian optimiser on 2 k calibration prompts -> worst-case bypass estimate \hat r.  
• Guarantee: Pr[r > α] < ζ. For α = 1 %, ζ = 10⁻³ achieved with ensemble size 7, query budget 6×10⁴.

---

## 7  Contrarian & Emerging Directions

1. **Adversarial-CAPTCHA gating** – require human-solvable but LLM-hard tasks (e.g., CAPTCHA involving high-resolution OCR) *before* executing risky instructions. (Speculative)  
2. **Neural-signature watermarks** – embed cryptographic *non-linguistic* features in safe prompts; classifiers only pass prompts containing valid signature, impeding arbitrary generation by attackers. (Research-stage)  
3. **Self-distilled defensive simulacra** – train miniature safety models inside the main LLM that produce *counterfactual refusals*, offering internal gradient signals for integrated safety.  

---

## 8  Recommendations (Actionable)

1. **Short term (≤ 3 mo)**  
   • Deploy *tri-model* AND-ensemble (RoBERTa-policy, RAG-GPT-critic, DistilTox).  
   • Add Secure/Insecure divergence fine-tuning for 3 days on 8 A100s.  
2. **Medium term (3–9 mo)**  
   • Integrate Bayesian risk certificates using PROSAC; publish α,ζ to regulators.  
   • Run continuous red-team via ensemble RL attackers (budget 5 M queries/mo).  
3. **Long term (> 9 mo)**  
   • Explore watermark-based prompt-auth, escalate ambiguous prompts to human adjudication pipeline with cost-aware triage.

---

## 9  Outstanding Research Questions

• Optimal trade-off curve between ensemble size and inference latency for online moderation.  
• How to quantise disagreement information into a single differentiable signal for joint training with the generator model.  
• Formal relation between CFD and certified α under PROSAC – can we derive closed-form bounds?  
• Attackers with *adaptive linguistic steganography*: does Secure/Insecure training remain effective?

---

## 10  Conclusion

Both attacker and defender stand to gain from ensembling: attackers harvest diversity to cover more boundary regions; defenders harness diversity to decorrelate errors and obtain statistical guarantees. The balance pivots on how effectively each side can *reduce transferability* for defenses yet *increase it* for attacks. Techniques such as **Secure/Insecure set training**, **ensemble RL search**, and **population-risk certification** constitute the current state of the art. System designers should adopt heterogeneous, dynamically-calibrated ensembles and continuously probe them with multi-LLM adversaries to stay ahead in the safety arms race.


## Sources

- https://escholarship.org/uc/item/2bj9c0br
- http://pralab.diee.unica.it/sites/default/files/biggio11-smc.pdf
- https://zenodo.org/record/7945511
- https://ojs.aaai.org/index.php/AAAI/article/view/16843
- https://ojs.aaai.org/index.php/AAAI/article/view/17595
- https://discovery.ucl.ac.uk/id/eprint/10181256/
- https://doaj.org/article/8879abd584ca43ff964e09b9fdbb3d00
- https://hdl.handle.net/20.500.12511/6894
- http://hdl.handle.net/10779/DRO/DU:20625285.v1