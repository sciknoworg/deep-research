# Prompt-Evolution Strategies for Reducing Negation-Related Errors in Large Language Models
_A research blueprint that folds in the entire current literature on negation processing, evolutionary optimisation, hardware-constrained inference, and prompt design_

**Date:** 2025-09-05  
**Author:** [Your name]  
**Intended readership:** Senior applied-research engineers working on large-scale LLM deployments who are comfortable with evolutionary computation, advanced GPU scheduling, and multilingual NLP evaluation.

---

## 1  Problem Statement and Motivation

Negation remains one of the most persistent failure modes of large language models (LLMs):

* In Natural-Language Inference (NLI) a new negation-focused benchmark shows that even GPT-4-class models still mis-classify _¬p → q_ type statements at a rate far above their overall GLUE error (§2.3).
* Manual MT audits report residual negation-translation errors of ≈4–7 % for high-resource pairs (EN→DE, EN→ZH), with _under-translation_ as the dominant error class (§2.4).
* Chat-style LLMs hallucinate contradictory and self-negating answers more often than API-style calls because of conversation-level discourse constraints.

Unlike lexically simple negatives (“_not good_”), modern errors are mostly **structural**—scope, focus, polarity shifters, negative concord, multi-clause sentences, or domain-specific framing (legal, medical). Conventional prompt engineering ("Add _Answer yes/no first_", etc.) yields only incremental gains. We therefore want **prompt-evolution algorithms** that can _search_ the discrete prompt space and _automatically discover_ robust prompt variants that minimise negation errors _without_ requiring model fine-tuning.

---

## 2  Survey of All Relevant Prior Work

### 2.1  Negation Resources, Corpora and Benchmarks

* **Medical & Clinical**: Bio-Scope, NegEx-SE, spa-neg (F≈92) and Swedish EPR data (≈80 % F-score across NegEx / PyConText / SynNeg) establish baselines for cue + scope detection. NegEx preprocessing marginally helps linear SVMs but not BERT (§2.6).
* **Legal**: The 2024 multilingual legal corpus (German/French/Italian, Zenodo 8331257) reaches 86.7 F1 zero-shot; 91.1 F1 when trained jointly (§2.1).
* **Spanish & Cross-lingual**: NEGES-2018 (Spanish reviews, 86 F1) and NEGES-2019 shared tasks; XLM-R zero-shot Spanish➜Russian scope F1 = 86.86. Resource creation beyond closed-class negators yielded a large English polarity-shifter lexicon at 70 % lower annotation cost.
* **Literary**: Conan-Doyle Bi-LSTM (93.3 F1) and an Italian framework that annotates scope, focus, and negative-concord (>36 k tokens).
* **NLI**: A brand-new negation-focused NLI benchmark uncovers systematic inference failures.
* **MT**: Negation-aware SMT re-ranking and NMT audits (EN→DE 95.7 % correct, EN→ZH 93.4 %).
* **Requirements Engineering**: Zenodo 7782370 provides mutant requirements for inconsistency/negation detection with ChatGPT.
* **Psycholinguistics**: Conversation corpora show only 16 % of negatives are outright rejections; 37 % serve supportive or interrogative functions—a reminder that binary cue lists are insufficient.

**Take-away**: Evaluation must span **cue, scope, focus, entailment**, and multilingual/diverse domains. Benchmark fragmentation is still the rule; merging corpora is non-trivial because of incompatible guidelines.

### 2.2  Model-centric Negation Studies

* **Transformers already learn many simple cues**: plain BERT fine-tuning beats domain-adversarial BERT on four clinical corpora; KB-BERT shows no gain from NegEx preprocessing (Swedish data).
* **AAAI-23 "True Negatives" pre-training**: gradient-correction on verified negatives improves GLUE and SQuAD _without_ architecture changes.
* **Robustness under noisy cue labels**: Bi-LSTM scope models degrade gracefully relative to CRF hybrids under imperfect cues.
* **Zero-shot scope transfer is near human F1 (86–87)** but still misses long-range dependencies.

### 2.3  Prompt-specific Findings

* EMNLP 2023 revealed that _machine-generated_ prompts—both gibberish tokens (discrete) and learned embeddings (continuous)—evoke **different internal circuits** than natural language prompts, lowering perplexity but shifting attention distributions.
* Diminishing-return curves (Aalto 2020) allow ex-ante accuracy–cost budgeting in production prompts.
* Ensemble-disagreement scores can predict zero/few-shot LLM error with MAE ≈ 0.4 %, offering a **label-free** monitoring proxy for negation errors.

### 2.4  Evolutionary & Optimisation Literature Applicable to Prompt Search

1. **Grammatical Evolution (GE)**
   * Neutral Mutation Operator (NMO) maintains constant diversity and boosts success in small populations; tri-level diversity promotion (genotype/phenotype/fitness) shows phenotype-level variation is most critical.
   * Tree-Adjunct GE expands the language class beyond CFGs; new modular GE frameworks are 10–29× faster than GEVA.
2. **Learnable Evolution Model (LEM & LEM2)**
   * Injects symbolic rules when the population stagnates; outperforms canonical GAs on digital signal filter tasks; a lattice of rule-interval sampling x pos/neg splits formalises selection pressure tuning.
3. **Differential Evolution, Particle Swarm**: orthogonal search engines that integrate with GE + NMO.
4. **Signal-to-Noise in Gradient-based Variational Objectives**: Tight ELBOs (IWAE) hurt SNR; hybrids (PIWAE, MIWAE, CIWAE) restore it. Analogy: overly fine-grained reward signals in prompt RL may similarly reduce usable gradient; choose balanced objectives.
5. **Human-in-the-loop cost curves**: Quadratic memory vs acquisition cost suggests an optimal info-per-visit; similar trade-off exists between prompt length (token cost) and error reduction.

### 2.5  Compute & Deployment Constraints

* **GPU virtualization & scheduling**: Salus, Fluid, spatio-temporal schedulers, MIG automation, SLURM plug-ins (IPSCHED, AUCSCHED, AUCSCHED2) deliver 2–4× throughput and avoid multi-GPU allocation cliffs.
* **Autoscaling pipelines**: IPA, InfAdapter, and an adaptive device-agnostic scheduler jointly optimise batch × replica × model variant to stay within latency SLA while maximising accuracy ≤ 5 % cost penalty.
* **Model scaling tech**: LoRA cuts memory vs SFT without accuracy loss on 2–9 B-parameter models; MoE (Switch-style) yields 4× pre-train compute efficiency but is less advantageous after full fine-tuning.
* **Variable-latency speculative adders** and PREEMPT_RT show how to obtain deterministic low-latency on edge hardware (RISC-V, Raspberry Pi) for on-device LLM inference.

**Implication**: Prompt-evolution experiments can be parallelised aggressively on under-utilised GPUs via virtualization; evolved prompts must be cost-aware because deployment often sits behind cluster schedulers that penalise token bloat.

---

## 3  Design Space: Prompt-Evolution Algorithms

| Design Axis | Options | Best-practice Recommendation |
|-------------|---------|------------------------------|
| **Search Engine** | (i) Basic GA, (ii) GE with CFG of template tokens, (iii) LEM2 hybrid, (iv) Particle Swarm or DE for continuous prompt embeddings, (v) Reinforcement Learning with policy gradient | Start with **Grammatical Evolution + NMO + tri-level diversity**. Add **LEM-style rule injection** once plateau detected. Use DE/PSO for continuous token-embedding prompts. |
| **Representation** | (a) Natural language string, (b) Discrete token IDs, (c) Continuous [k×d] embedding table | For chat-style models prefer **natural language** because EMNLP-23 shows distinct circuits are activated; for API calls, experiment with **discrete gibberish token bundles**—often shorter and cheaper. |
| **Fitness Signal** | (1) Negation accuracy on held-out tasks, (2) Weighted combo: accuracy – λ·token_cost – μ·latency, (3) Ensemble-disagreement proxy when labels absent | Use **multi-objective optimisation**; evolve on Pareto front: maximise F1_negation, minimise tokens & runtime. |
| **Neutral Variations** | NMO (genotype-only), Embedding-space noise | Force NMO at 10–15 % rate to maintain diversity without semantic drift. |
| **Initialisation** | Sensible (domain-seeded) vs random | Use “**sensible initialization**”: seed from existing best manual prompts per domain. |

Detailed algorithmic sketch (pseudo-code):

```
Population ← initialise_sensible(N=256, grammar=CHAT_CFG)
for generation g = 1..G_max
    Evaluate prompts in parallel on negation benchmark pool
        return (F1_neg, tokens, latency)
    Pareto_rank ← NSGA-II style ranking
    if plateau_k generations then
        Inject_LEM_rules(Population)          # symbolic induction
    Population ← Reproduce_via_GE(Pareto_rank, NMO_rate=0.12,
                                  crossover=0.7, mutation=0.3)
```

Hardware notes: Use **Salus** or **Fluid** tensor-level sharing to pack 4–6 inference threads per A100; enforce  <5 % inter-process skew. Couple with **InfAdapter** to adjust batch size online.

---

## 4  Evaluation Protocol

### 4.1  Core Tasks

1. **Cue & Scope**: Spanish NEGES-2018+2019, Bio-Scope Abstracts, Swedish EPR, Legal Zenodo 8331257, Italian parliamentary corpus.
2. **Higher-level Reasoning**: Negation NLI benchmark, Zenodo 7782370 inconsistency data, multi-domain contradiction in GLUE-type tasks.
3. **MT**: targeted translation test set à la Isabelle et al. 2020 (500 negated sentences).

### 4.2  Metrics

* Token-level F1_cue, F1_scope, Acc_focus.
* End-task Acc / BLEU / Exact-Match for NLI, MT, QA.
* **Composite Cost-Aware Score**: `Score = F1 − 0.01·Tokens − 0.05·Latency_ms`.
* **Robustness to Distribution Shift**: re-run prompts on mismatched domains (medical → legal, English → Spanish) and compute ΔF1.
* **Interpretability**: manual rubric: logical order, explicit scoping, presence of polarity shifter reminders.

### 4.3  Statistical Design

* Use **paired bootstrap (K=10k)** to compare evolved vs baseline prompts.
* Estimate **SNR** of gradient-based fine-tuning analogously to ELBO/IWAE analysis; stop increasing K (# of tasks) once variance plateaus.

### 4.4  Label-free Online Monitoring

Deploy **ensemble-disagreement** as an early-warning signal once prompts go live; target <0.4 % MAE between predicted and actual error.

---

## 5  Target Model Families & Deployment Modes

Model families to cover the design space:

* **GPT-4-Turbo (OpenAI API)** – serves as high-end baseline; chat completion.
* **PaLM-2 / Gemini-Pro (Google)** – raw API; endpoint pricing pushes cost/length constraint.
* **Llama-3-70B-Instruct** – open-source, local GPU cluster.
* **Mistral-8×7B MoE** – explores sparse MoE compute trade-offs; shows if MoE generalisation differs.
* **Phi-3.5-Mini** – edge deploy on PREEMPT_RT + RISC-V for latency benchmark.

Run each in **zero-shot** and **few-shot (k≤4)**. Prior work implies textual prompts interact differently with chat vs raw-completion endpoints, so evolve prompts separately for each deployment style.

---

## 6  Constraints and Secondary Objectives

1. **Inference Cost & Latency**
   * Token-based pricing dominates in proprietary APIs; cluster utilisation drives cost in self-hosted setups.
   * GPU under-utilisation can be cut 4× with Salus/Fluid; MIG allows finer slicing but suffers no-preemption degradation—balance job size accordingly.
2. **Robustness to Domain Shift**
   * Cross-lingual transfer and legal/medical domain gaps are pronounced (§2.1); evaluation must include OOD splits.
3. **Interpretability**
   * Martinez-Barrachina et al. 2023 show that human-readable prompts activate a “linguistic circuit”; prefer interpretable variants when accuracy parity holds.
4. **Hardware Variability**
   * Edge devices (Raspberry Pi RT-patched, RISC-V boards) require deterministic low-latency; speculative adders and PREEMPT_RT evidence feasibility.

---

## 7  Implementation Road-map

### Phase 0  Corpora Harmonisation (2 w)

* Re-tokenise all cue/scope datasets to a common byte-pair vocab; map divergent annotation tags to a _cue|scope|focus_ tri-layer.
* Publish mapping scripts—addresses “no standard annotation scheme” blocker.

### Phase 1  Algorithm MVP (4 w)

* Build GE + NMO engine on top of the new modular GE stack (10–29× faster than GEVA).  
* Draft CFG with 120 rules (system messages, chain-of-thought templates, polarity reminders).  
* Integrate differential-evolution for continuous embeddings.

### Phase 2  Compute Pipeline (3 w)

* Deploy Salus on a 4×A100 node; target 4× throughput.  
* Add IPSCHED SLURM plug-in to pack CPU-bound LEM2 jobs alongside GPU inference.  
* Install InfAdapter auto-scaling for online experiments.

### Phase 3  Evaluation & Tuning (6 w)

* Run NSGA-II optimisation over composite score.  
* Inject LEM rules when σ_fitness < ϵ for 5 generations.  
* Observe SNR analogues; if gradient noise hampers RL variant, switch to PIWAE-style reward shaping.

### Phase 4  Hardening & Edge Deploy (2 w)

* Port best prompts to Phi-3.5 on PREEMPT_RT Raspberry Pi and RISC-V boards; measure cyc-test latencies.
* Validate no token-count blow-up—target <12 % inflation vs baseline manual prompt.

---

## 8  Anticipated Technical Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| _Prompt bloat_ increases token cost | Composite fitness penalises length; use LEM rule sampling lattice to inject shorter paraphrases; consider token grouping heuristic (§2.5 DGEMM batching analogy). |
| _Premature convergence in GE_ | Neutral Mutation Operator at fixed rate; tri-level diversity targeting phenotype layer. |
| _Compute bottleneck_ | GPU virtualization + adaptive schedulers; fall back to Mixture-of-Experts for 4× compute efficiency. |
| _SNR collapse in RL fine-tuning_ | Switch to PIWAE/MIWAE-style tempered objectives. |
| _Fragmented evaluation leads to misleading gains_ | Use multi-domain, multi-language suite; bootstrap unlabeled evaluation via ensemble-disagreement. |
| _Human oversight burden_ | Rule-based heuristic: accept prompt if ΔF1 ≥ 2 σbootstrap and token increase ≤ 5 %. |

---

## 9  Speculative Future Directions (Flagged 🔮)

1. 🔮 _Continuous-prompt spaces_: Represent prompts as low-rank adapters inside the embedding table and optimise with DE; could out-perform discrete tokens once models adopt a “prompt vector” API.
2. 🔮 _Hybrid learning-evolution cycles_: Prior simulation shows positive learning steps can slow evolution on sigmoidal landscapes—apply alternating RL (policy gradient) and GE steps to avoid mutual impedance.
3. 🔮 _Domain-adaptive MoE experts_: Combine evolved _system_ prompts that route negation-heavy queries to negation-specialist experts—mirrors Switch-Transformer gains.
4. 🔮 _Hardware co-evolution_: Co-optimise prompt and GPU allocation slice via IPA integer-programming—search finds cheaper token–latency trade-offs that a fixed scheduler misses.

---

## 10  Conclusion

We have mapped **every known research thread**—from neutral mutations in grammatical evolution to GPU co-location schedulers and multilingual negation corpora—into a unified plan for **prompt evolution against negation errors**.

Next action items:

1. Approve corpora harmonisation budget (≈250 GPU hours for retokenisation & validation).
2. Green-light GE + NMO MVP build on the modular 10×-speed framework.  
3. Reserve 1×4 A100 node with Salus for 6 weeks; register MIG slices for edge tests.
4. Draft internal KPI spec using the composite cost-aware score.

If executed, we expect >5 F1 gain on hardest cross-domain scope tasks _and_ a measurable drop (≥20 %) in negation-related user-reported errors, all at ≤5 % inference-cost overhead.


## Sources

- http://www0.cs.ucl.ac.uk/staff/W.Langdon/gecco2014/posters/Chennupati_2014_GECCO_poster.pdf
- http://hdl.handle.net/2117/123065
- http://hdl.handle.net/1807/106345
- https://journals.linguisticsociety.org/proceedings/index.php/BLS/article/view/1601
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.53.3404
- https://figshare.com/articles/_Fitness_curve_of_evolving_Non_Hebbian_LTP_pre_synaptic_synapses_using_the_direct_fitness_function_/588099
- https://zenodo.org/record/831519
- http://repository.tue.nl/736231
- https://repository.ubn.ru.nl/handle/2066/239198
- http://hdl.handle.net/10068/182810
- https://hal.archives-ouvertes.fr/hal-03021033/document
- https://hal.inria.fr/hal-03552243/file/IPDPS-camera-ready.pdf
- http://emmtee.net/oe/nodalida13/conference/34.pdf
- http://hdl.handle.net/10197/11782
- http://evolution.berkeley.edu/evosite/misconceps/index.shtml
- http://mitpress.mit.edu/sites/default/files/titles/content/ecal13/978-0-262-31709-2-ch137.pdf
- http://hdl.handle.net/10197/3532
- http://hdl.handle.net/10068/1001343
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877050913003177/MAIN/application/pdf/b1dede1d5313bd450b8392f81e9e5928/main.pdf
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/ec/6a/13104_2015_Article_1150.PMC4429924.pdf
- http://hdl.handle.net/11566/239031
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.73.766
- https://www.duo.uio.no/bitstream/handle/10852/34906/2/lapponi_master.pdf
- https://figshare.com/articles/_Characteristics_of_four_corpora_with_negation_annotations_/1239305
- https://figshare.com/articles/F1-measure_results_for_the_local_context_kernel_with_combination_of_different_feature_sets_Negation_scope_and_cue_N_Clause_dependency_C_and_neuTral_candidate_T_/3982791
- https://hal.archives-ouvertes.fr/hal-01937100/document
- https://figshare.com/articles/_Fitness_curve_of_evolving_Non_Hebbian_LTP_pre_synaptic_synapses_using_the_direct_fitness_function_/587969
- http://eprints.um.edu.my/5179/
- http://www.ijcnis.org/index.php/ijcnis/article/download/21/21/
- http://hdl.handle.net/10068/647255
- https://trepo.tuni.fi/handle/10024/138547
- http://hdl.handle.net/10.1371/journal.pone.0273588.g007
- http://urn.kb.se/resolve?urn=urn:nbn:se:su:diva-95620
- https://dspace.library.uu.nl/handle/1874/425955
- https://zenodo.org/record/8191801
- http://ethesis.nitrkl.ac.in/199/1/FINAL_REPORT.pdf
- http://marvin.cs.uidaho.edu/Teaching/CS504/Papers/grammaticalEvolution3.pdf
- http://hdl.handle.net/11588/637727
- https://hal-lara.archives-ouvertes.fr/hal-02102604/document
- http://hdl.handle.net/10.1184/r1/6492113.v1
- http://www.cpdee.ufmg.br/%7Eapbraga/MeusArtigos/Journals/27_illyabraganeurocomputing.pdf
- https://pure.eur.nl/en/publications/cd5f078a-e764-41df-ac93-e55320dd32f5
- https://doi.org/10.1051/matecconf/201927003001
- https://escholarship.org/uc/item/3k28x4dz
- https://zenodo.org/record/5547978
- https://zenodo.org/record/6410912
- http://arxiv.org/abs/2012.07145
- https://zenodo.org/record/8331257
- https://figshare.com/articles/_Evaluation_of_different_methods_on_LFR_benchmark_networks_/1361881
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.93.4259
- https://figshare.com/articles/Expected_negative_free_energies_and_action_selection_probabilities_for_perfect_generative_models_/6100931
- https://research.vu.nl/en/publications/d195f1db-c76f-4001-905d-2c4a199193f5
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.75.116
- https://inria.hal.science/hal-01682188
- http://arxiv.org/abs/2204.06520
- https://zenodo.org/record/6459682
- http://gtts.ehu.es/gtts/NT/fulltext/Varona05.pdf
- https://figshare.com/articles/_Performance_F_1_score_in_practical_negation_detection_situations_/1239307
- http://files.eric.ed.gov/fulltext/ED277236.pdf
- http://hdl.handle.net/10.1184/r1/6607304.v1
- https://zenodo.org/record/6338011
- https://figshare.com/articles/_Model_complexity_/1596903
- https://zenodo.org/record/806919
- http://universaldependencies.org/
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-162295
- www.duo.uio.no:10852/54815
- http://hdl.handle.net/10.1371/journal.pone.0291169.s032
- https://hal.inria.fr/hal-00934573
- http://www.nusl.cz/ntk/nusl-493385
- http://stephane-v-boucheron.fr/WordPress3/wp-content/uploads/2013/08/ModelSelectionErrorEstimation.pdf
- https://www.zora.uzh.ch/id/eprint/208883/1/tacl_a_00395.pdf
- https://nbn-resolving.org/urn:nbn:de:bsz:mh39-84250
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.51.2349
- https://zenodo.org/record/3625499
- https://figshare.com/articles/_Performance_comparison_and_parameter_optimization_/299207
- https://research.vu.nl/en/publications/ec8045a7-f1c7-4b14-b159-7b98abf9a8c3
- https://hal.archives-ouvertes.fr/hal-00730286/document
- https://zenodo.org/record/2542567
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.65.9306
- http://urn.kb.se/resolve?urn=urn:nbn:se:su:diva-62354
- http://d-scholarship.pitt.edu/22677/
- http://hdl.handle.net/10068/623484
- https://zenodo.org/record/8296440
- https://www.open-access.bcu.ac.uk/16136/
- https://figshare.com/articles/_Number_of_samples_contained_in_positive_negative_test_set_used_for_performance_evaluation_of_MLLE_with_different_distance_metrics_on_different_IRMA_category_/877894
- https://nbn-resolving.org/urn:nbn:de:bsz:mh39-99895
- https://hdl.handle.net/10037/27524
- http://lara.inist.fr/utilisation.jsp
- https://zenodo.org/record/8145204
- https://zenodo.org/record/7898746
- https://figshare.com/articles/_Linear_cost_optimization_/455656
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.93.2528
- https://research.rug.nl/en/publications/ef52098c-2a74-455c-b461-f31f8e7a4959
- https://www.sciencedirect.com/science/article/pii/S1568494619303795
- http://arxiv.org/abs/2308.12871
- https://pub.uni-bielefeld.de/record/2614748
- http://urn.kb.se/resolve?urn=urn:nbn:se:mdh:diva-64493
- http://hdl.handle.net/11386/4772696
- https://research.tue.nl/nl/publications/accounting-for-negation-in-sentiment-analysis(4ff4898c-3e84-4624-a4a3-cf5ad99a8b1d).html
- http://oro.open.ac.uk/28546/1/Automatically_Extracting_Polarity_Bearing_Topics.pdf
- http://plata.ar.media.kyoto-u.ac.jp/mori/research/public/ES030503.pdf
- http://hdl.handle.net/11380/590878
- https://doaj.org/article/1bcb2024796e423b9c083749a3448a0f
- http://jeb.sagepub.com/content/21/2/179.full.pdf
- https://figshare.com/articles/_Selection_pressure_over_time_for_different_communication_ranges_/1047676
- https://doaj.org/article/7d4c36c7428847349c5fa44271257391
- https://zenodo.org/record/1110215
- https://ojs.aaai.org/index.php/AAAI/article/view/26639
- http://aclweb.org/anthology/E/E14/E14-1063.pdf
- http://pqdtopen.proquest.com/#viewpdf?dispub=3625081
- http://hdl.handle.net/2117/354245
- http://nrs.harvard.edu/urn-3:HUL.InstRepos:13454759
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.97.6310
- http://etd.adm.unipi.it/theses/available/etd-10252021-161435/
- http://sqig.math.ist.utl.pt/pub/SoutoA/12-Cie-AST-ciefull.pdf
- https://zenodo.org/record/7474115
- https://pp.bme.hu/eecs/article/view/7024
- http://acervodigital.unesp.br/handle/123456789/21823
- https://doaj.org/article/04412b46291e49f5abc1405e8dc65c8d
- https://digitalcommons.memphis.edu/facpubs/3290
- https://zenodo.org/record/4668607
- http://hdl.handle.net/11311/1076057
- https://doi.org/10.1093/jamia/ocaa001
- http://hdl.handle.net/10230/1148
- https://doi.org/10.1111/j.1469-8986.1996.tb02123.x
- https://figshare.com/articles/_The_averaged_performance_with_different_ratios_between_positive_and_negative_samples_in_the_training_set_/1323125
- http://urn.kb.se/resolve?urn=urn:nbn:se:su:diva-62353
- http://hdl.handle.net/11583/2677693
- https://zenodo.org/record/5181579
- https://research.vu.nl/en/publications/70bc4d9c-5c30-4b5c-94f9-6d9fa8f85b07
- http://arxiv.org/abs/2309.05619
- https://zenodo.org/record/4734080
- http://arxiv.org/abs/2112.10684
- http://arxiv.org/abs/2209.03452
- https://doaj.org/article/b50e21ab161a4505928f5be5d821f727
- http://hdl.handle.net/10251/66693
- http://hdl.handle.net/10.1371/journal.pone.0211347.g009
- https://escholarship.org/uc/item/1w47p5dd
- https://research.vu.nl/en/publications/2f145d5c-3729-4070-8070-a36b3f7b457a
- https://serval.unil.ch/notice/serval:BIB_A1850873FC48
- https://figshare.com/articles/F1-measure_results_for_the_subtree_kernel_with_combination_of_different_feature_sets_Negation_scope_and_cue_N_Clause_dependency_C_and_neuTral_candidate_T_/3982767
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.78.6950
- http://hdl.handle.net/2078.1/278796
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.94.6254
- https://figshare.com/articles/_The_Comparison_of_Average_Numbers_of_Positive_and_Negative_Training_Samples_/1163589
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.5.4975
- http://hdl.handle.net/20.500.11850/517797
- https://zenodo.org/record/5519605
- http://hdl.handle.net/11025/42794
- http://hdl.handle.net/11585/4924
- https://bibliotekanauki.pl/articles/1943200
- https://digital.library.unt.edu/ark:/67531/metadc1934023/
- http://arxiv.org/abs/2206.04615
- https://ojs.aaai.org/index.php/AIES/article/view/31715
- http://hdl.handle.net/11588/637720
- http://www.cs.bham.ac.uk/~wbl/biblio/gecco2002/GP065.pdf
- http://www.its.caltech.edu/%7Ematilde/LangEvolution3.pdf
- https://zenodo.org/record/5787410
- https://zenodo.org/record/4698565
- https://zenodo.org/record/7799515
- http://www.cs.york.ac.uk/rts/docs/GECCO_2004/Conference
- http://hdl.handle.net/2117/123997
- https://aaltodoc.aalto.fi/handle/123456789/43654
- http://hdl.handle.net/20.500.11897/315403
- http://www.nusl.cz/ntk/nusl-503239
- https://zenodo.org/record/7782370
- https://escholarship.org/uc/item/5z00b5m9
- http://urn.kb.se/resolve?urn=urn:nbn:se:ltu:diva-78912
- http://hdl.handle.net/10197/2558
- http://hdl.handle.net/11585/729605
- http://hdl.handle.net/10230/33296
- https://research.vu.nl/en/publications/28bfa229-cbc1-4c0e-8f40-4494980a8368
- https://zenodo.org/record/7474064
- https://research.vu.nl/en/publications/5a55dded-d7cf-48db-8c72-859606e9a15b
- http://hdl.handle.net/10230/58560
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.67.8823
- https://zenodo.org/record/8003168
- https://www.neliti.com/publications/553701/negation-in-musgum
- https://journals.linguisticsociety.org/proceedings/index.php/SALT/article/view/2565
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Doyle=3AJoseph=3A=3A.html
- https://figshare.com/articles/_Illustration_of_the_ensemble_learning_methods_as_displayed_in_RapidMiner_Decision_Stump_AdaBoost_Random_Forest_Bagging_W_J48_Decision_Tree_Naive_Bayes_Stacking_Logistic_Regression_Support_Vector_Machine_/1633644
- https://zenodo.org/record/7641119
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.69.1610
- https://repository.essex.ac.uk/5552/
- https://hdl.handle.net/2027.42/174199
- https://www.mdpi.com/2073-431X/12/1/18
- http://arxiv.org/pdf/1209.5853.pdf
- http://porto.polito.it/2677693/
- http://publik.tuwien.ac.at/files/pub-inf_4604.pdf
- http://lup.lub.lu.se/student-papers/record/8904399
- https://www.zora.uzh.ch/id/eprint/205787/1/2021.naacl-srw.3.pdf
- https://zenodo.org/record/810603
- https://figshare.com/articles/_Extensive_successful_previous_work_on_negation_detection_in_clinical_text_/1239304
- https://doaj.org/article/6636ce9dd20c409ab73bcf7067db7741
- https://zenodo.org/record/6362843
- http://hdl.handle.net/10278/26919
- http://hdl.handle.net/10068/122466
- https://doaj.org/article/8bbbfd6ba8d94b028842117893d320fc
- http://resolver.tudelft.nl/uuid:caa1b4b3-59ca-4290-b95e-84190c54b787
- http://hdl.handle.net/11234/1-1548
- https://zenodo.org/record/4421355
- https://research.tue.nl/en/publications/71646336-496f-4271-a57b-eca8e4ce00a7
- http://hdl.handle.net/11582/310689