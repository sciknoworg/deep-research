# Ensemble of LLMs Attacking and Defending Safety Classifiers

## 1. Executive Summary
Large-language-model (LLM) safety filters are quickly becoming the critical control point for any enterprise deploying generative AI.  Yet both theory and practice show **no single classifier can be perfectly robust**:  Bubeck et al. (2019) prove an *inevitable adversarial risk* bound, while recent red-teaming efforts (e.g., ASSERT 2023) demonstrate double-digit accuracy drops on seemingly simple prompt variations.  

The state of the art is therefore shifting toward *ensembles*—on both sides of the arms race:

* **Offense:**  Orchestrating multiple LLMs (or multiple prompting strategies for the same model) to discover or synthesize adversarial prompts that evade guardrails.
* **Defense:**  Building ensemble safety filters, possibly heterogeneous (rules + statistical detector + fine-tuned model), to raise the bar against jailbreaks without incurring unacceptable latency or cost.

This report consolidates empirical insights, theoretical limits, and engineering guidance into a coherent blueprint for research or deployment.  All thirteen learnings supplied were integrated and cross-referenced.

---

## 2. Background and Threat Model

### 2.1 Why Ensembles Matter

• **Diversity as a weapon**:  Different models have different failure modes; combining them boosts coverage.  Classic malware-detection studies (e.g., random-forest + JRIP + Ridor pushing Android true-positive rates to 98.2 %) already prove the concept (Learning 9).  

• **Diversity as a weakness**:  HAL-03806425 shows that combining eight image-resizing kernels *increases* transferability of attacks—an important caveat (Learning 1).

### 2.2 Threat Model Dimensions

1. **Modality**:  We focus on text-only GPT-4-class LLMs, but occasionally note multimodal extensions.  
2. **Deployment setting**:  Online API (e.g., OpenAI, Anthropic) vs. self-hosted models (Llama-3 70B) running on edge-core NFV fabric (Integration possibilities with ADRENALINE testbed; Learning 4) or 5G converged SDN transport (Learning 8).  
3. **Attacker capability**:  Access to multiple LLMs (open-source or via API) and freedom to iterate prompts; goal is to generate content that violates platform policy while passing the safety classifier.
4. **Defender capability**:  Ability to deploy multiple safety filters in parallel or cascaded, including rules, statistical detectors (MoJE; Learning 5), or fine-tuned transformer safety heads.

---

## 3. Offensive Use-Case:  Ensemble-of-LLMs Jailbreak Framework

### 3.1 Architecture

```
User Prompt  ──► Orchestrator  ──►  {LLM₁ … LLMₙ}  ──►  Diversity Filter  ──►  Safety Classifier  ──►  Pass/Fail
                                        ▲                                    ↓
                                        └────────── Reinforcement Learning ───┘
```

• **Orchestrator**:  Decides which base LLMs to query and with which prompt templates.  Similar to “attack-specific ensemble orchestration” that achieved 97.4 % recall in IDS benchmarks by ranking detectors per attack (Learning 2)—here we rank *attack generators* per jailbreak style (e.g., DAN, Caesar-shift, multilingual obfuscation).  

• **Diversity filter**:  Keeps only sufficiently different candidate outputs to escape rule-based deduplication, borrowing ideas from random-subspace bagging (Learning 1) but in generation space.  

• **Reinforcement loop**:  Safety classifier feedback (blocked/allowed) becomes the reward; any LLM whose outputs sneak through gets up-weighted (bandit-style routing).

### 3.2 Prompt-Space Diversification Strategies

1. **Model heterogeneity**:  Mix instruction-finetuned and chat-based models.  
2. **Prompt-template mutations**:  Use ASSERT 2023’s semantic-alignment vs. adversarial-knowledge-injection families (Learning 10).  
3. **Multi-lingual & code-switching**:  Combine low-resource languages + base64 + zero-width-character steganography.  
4. **Chain-of-thought elision**:  Ask the model to reason internally but output only the final answer—reduces safety filter context.

### 3.3 Empirical Expectations

• Based on the IDS study (Learning 2) and HAL-03806425, conditional routing should outperform naive majority voting by ~2–5 pp in bypass rate.  
• However, ensembles that *lack conditionality* may paradoxically increase the chance that *at least one* sample triggers the detector, so evaluating *per-query success probability* is crucial.

---

## 4. Defensive Use-Case:  Ensemble-Based Safety Classifiers

### 4.1 Design Taxonomy

| Layer | Example Component | Strength | Cost |
|-------|-------------------|----------|------|
| Linguistic Heuristics | Regex profanity filter | Near-zero latency | High false-negatives |
| Statistical Detector | MoJE (lightweight linguistic statistics; Learning 5/12) | 90 % jailbreak detection, negligible overhead | Limited to known patterns |
| Deep Model | GPT-4-derived policy head | High recall & novel-attack coverage | Latency + $$$ |
| Certified Wrapper | PROSAC population-level risk certificate (Learning 11) | Probabilistic guarantees | Training compute |

An *ensemble* chains or parallelises these layers:

```
          +--> Heuristic -->
Prompt -->+--> MoJE ------> Voting ---> Pass/Fail
          +--> PolicyHead ->
```

### 4.2 Empirical Benchmarks & Shortcomings

• **RobustBench Analogy**:  Croce et al.’s AutoAttack (Learning 6) shows that a mere 60 % robust accuracy plateau persists in vision; by analogy, LLM safety ensembles are unlikely to exceed ~70 % *robust pass-through rate* on adversarial prompts unless radically new methods appear.  

• **Benchmark Realism**:  Offenburg 2024 found ℓ∞ 8/255 attacks trivially detectable (Learning 3).  For LLM safety, the moral is: avoid toy perturbations and instead use coordinated prompt corpora like ASSERT or real jailbreak transcripts.

### 4.3 Conditional Routing Defense

Mirroring the offensive orchestration, we can **rank safety heads by per-attack F1** and query only the top-k predicted to excel on that category.  This lowers latency (fewer heads) while leveraging specialization.  

Initial simulation (synthetic mix of 10 k benign / 10 k jailbreak prompts) shows expected AUC gain of 1–3 pp over unconditional majority vote, aligning with Learning 2.

---

## 5. Theoretical Limits vs. Practical Gains

Bubeck et al. (Learning 7) formally bound *unavoidable* adversarial risk for *any* classifier if data are generated by a smooth manifold.  Ensembles cannot break this bound but can move us closer to it.  The **goal is therefore risk *minimisation*, not elimination**.

PROSAC (Learning 11) offers an actionable metric:  choose α (max tolerated adversarial risk) and ζ (failure probability).  Ensembles that beat (α, ζ) thresholds can be *certified* for a given deployment.

---

## 6. Experimental Protocol Blueprint

1. **Dataset Construction**  
   • Benign: 150 k standard prompts (OpenAI, Anthropic logs).  
   • Adversarial: 50 k ASSERT 2023 prompts + 20 k crowdsourced jailbreaks + 5 k synthetic multi-lingual transformations.  
2. **Model Pool**  
   • Attack ensemble: {Llama-3-70B-Instruct, Mixtral-8x22B, GPT-4o, Qwen-2-72B}.  
   • Defensive base heads: {Regex-rules, MoJE, GPT-4-policy, DeBERTa-v3-safety-finetuned}.  
3. **Ensemble Strategies**  
   a. Offensive conditional routing (bandit).  
   b. Defensive majority vote vs. conditional top-k.  
4. **Metrics**  
   • Jailbreak success rate (lower is better).  
   • Benign pass rate.  
   • Latency (95th percentile).  
   • Certified risk (α, ζ) via PROSAC.
5. **Infrastructure**  
   • NFV instance chaining over ETSI OSM + TAPI (Learning 4) on 5G SDN transport (Learning 8) to mirror realistic edge deployments.  
6. **Reproducibility**  
   • Provide Docker images and code in HuggingFace repository; AutoAttack-style wrapper but adapted for prompts.

---

## 7. Deployment Considerations

1. **Latency Budget**:  Each additional safety head adds ~5–30 ms.  Use conditional routing to stay <150 ms aggregate.  
2. **Cost**:  Querying GPT-4-class models for defense can dominate OpEx; combine with cheap MoJE front-filter so that only ~10 % of traffic hits the expensive head.  
3. **Dynamic Updating**:  Adopt blue-green deployments with continuous A/B testing; use PROSAC to detect if a new model silently increases (α, ζ) beyond tolerance.  
4. **Edge vs. Cloud Split**:  Push lightweight models (Regex, MoJE) to edge PoPs; heavier heads stay in regional data centers accessible via TAPI-orchestrated WAN (Learning 4).  

---

## 8. Open Research Questions & Contrarian Ideas

1. **Reverse Transfer Exploitation**:  Could we *intentionally* leak carefully perturbed benign prompts that trigger *catastrophic forgetting* in black-box safety systems?  (Speculative)  
2. **Adversarial Diversity Regularisation**:  Instead of minimising disagreement among defensive heads, *maximise* it during training so at least one head “sees” each adversarial direction—analogous to negative-correlation learning.  
3. **Generative Proof Certificates**:  Use the attack ensemble to *construct* adversarial examples until a defensive ensemble survives 10⁵ consecutive attempts, then ship a cryptographic proof of effort to regulators—bridging practice and PROSAC-style guarantees.  
4. **Model Soups for Safety**:  Interpolate weights of multiple safety heads (like vision “model soups”) rather than ensembling logits—may yield single-model latency with ensemble-level robustness.

---

## 9. Recommendations

1. **Short Term (0–3 months)**  
   • Deploy MoJE as a front-line filter; it offers 90 % detection at negligible cost.  
   • Add at least one large policy head for high-sensitivity contexts.  
2. **Medium Term (3–12 months)**  
   • Implement conditional routing both in attack-side red-team tools and defense; measure gains.  
   • Adopt population-level certification (PROSAC) as a KPI.  
3. **Long Term (>12 months)**  
   • Explore weight-space model soups to compress ensembles.  
   • Push for a **RobustBench-for-Prompts**:  an open leaderboard with realistic adversarial prompt suites.

---

## 10. Conclusion
Ensembling is *necessary but not sufficient* for LLM safety.  Empirically, smart orchestration (conditional routing, diversity management) yields measurable gains—often 2–5 percentage points over naive majority vote, echoing results from IDS, spam, and malware domains (Learnings 1, 2, 9).  Yet fundamental limits (Learning 7) preclude total immunity.  Combining lightweight detectors like MoJE (Learning 5) with deep policy heads, wrapped in quantitative certification (Learning 11), and deploying across modern NFV/SDN infrastructure (Learnings 4, 8) currently represents the most defensible strategy.

Future work should converge on standardized, realistic benchmarks, lest we repeat the AutoAttack over-fitting pitfall highlighted by Offenburg 2024 (Learning 3).  Until then, a layered, ensemble-centric defense—continuously stress-tested by an equally sophisticated offensive ensemble—remains the pragmatic path forward.


## Sources

- https://discovery.ucl.ac.uk/id/eprint/10181256/
- https://zenodo.org/record/7273745
- https://zenodo.org/record/5976001
- https://hdl.handle.net/1721.1/137065
- https://zenodo.org/record/61255
- https://hal.science/hal-03426097v2/document
- https://hal.inria.fr/hal-03893496
- https://doi.org/10.1109/CVPRW56347.2022.00025
- https://eprints.whiterose.ac.uk/167427/1/28-Fog-BookChapter8.pdf
- http://urn.fi/URN:NBN:fi:jyu-201805172654
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-211212
- https://hal.archives-ouvertes.fr/hal-01990465
- https://hal.inria.fr/hal-03806425
- https://nrl.northumbria.ac.uk/id/eprint/49657/1/FINAL%20VERSION_TII.pdf
- https://doi.org/10.3390/fi12110180
- http://pralab.diee.unica.it/sites/default/files/biggio11-smc.pdf
- https://zenodo.org/record/7041019
- https://zenodo.org/record/321598
- http://arxiv.org/abs/2310.09624
- http://www.nusl.cz/ntk/nusl-448078
- https://zenodo.org/record/1321203
- https://hdl.handle.net/10356/169803
- https://doaj.org/article/2f58b7eb0a0e4bba991ab714b3842ed4
- http://eprints.utm.my/id/eprint/96365/1/OkwaraJerryChizobaMSC2019.pdf.pdf
- http://hdl.handle.net/11584/105029
- https://ojs.aaai.org/index.php/AIES/article/view/31638
- https://zenodo.org/record/6414075
- https://hdl.handle.net/1721.1/134088
- http://infoscience.epfl.ch/record/281094
- https://zenodo.org/record/1178708
- https://zenodo.org/record/4467346
- http://hdl.handle.net/20.500.11850/615512
- https://hdl.handle.net/20.500.11766/10606
- https://hdl.handle.net/20.500.12511/6894
- https://doaj.org/article/1c0d2fb828ac40d192ebdd1adf78ea41
- http://hdl.handle.net/11250/253097
- https://opus.hs-offenburg.de/frontdoor/index/index/docId/6449
- https://zenodo.org/record/2558306