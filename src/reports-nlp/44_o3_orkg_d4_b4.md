# Stepwise Uncertainty Estimation and Propagation in Chain-of-Thought Reasoning 
### Comprehensive State-of-the-Art Survey, Benchmark Map, and Research Agenda  
*(cut-off: 2025-09-05)*

---
## 1  Executive Summary
Multi-step reasoning systems—whether large language models (LLMs), probabilistic programs, or symbolic planners—accumulate both *epistemic* (knowledge) and *aleatory* (stochastic) uncertainty at every hop of their chain-of-thought (CoT).  Recent evidence shows that:
* GPT-3/3.5/4 can generate natural-language confidence tags that are **statistically calibrated** (Lin et al. 2022; Sylin et al. 2022), implying latent epistemic signals exist in pre-training.
* Injecting *local* uncertainty scores into the reasoning tree (Tree of Uncertain Thoughts — TouT, 2023) yields higher final accuracy than vanilla Chain-of-Thought or Tree-of-Thought search, confirming that *stepwise* UQ is actionable.
* Risk-aware decoders—Minimum Bayes Risk, arc-averaged risk, quantum beam search, NLI-assisted re-ranking—reduce hallucinations, copy noise, or search errors but still inherit underlying metric biases.
* Hybrid symbolic–probabilistic frameworks such as Multi-Entity Bayesian Networks (MEBN) and First-Order Bayesian Logic already support fine-grained propagation of uncertainty across *arbitrarily deep* logical inferences, offering a principled baseline that neural methods have yet to match at scale.

These results motivate a consolidated view that ties together 60+ disparate findings (full list embedded throughout) into one coherent map.  The report synthesises taxonomies, algorithms, benchmarks, and contrarian ideas, then proposes concrete design patterns and open problems for *stepwise* uncertainty estimation in CoT reasoning.

---
## 2  Conceptual Foundations
### 2.1 Three-way Source Taxonomy (Fraunhofer IIS/IESE)
1. **Scope-Compliance** — Does the model operate outside its training scope?  
2. **Data-Quality** — Measurement noise, missing modalities, label ambiguity.
3. **Model-Fit** — Parametric and structural misspecification, optimisation short-cuts.
Each source maps to specific V&V activities (e.g., OOD detectors for scope, sensor lineage audits for data quality, Bayesian posterior checks for model-fit) and therefore to *different* stepwise estimators.  

### 2.2 Aleatory vs Epistemic and Hybrid Treatments
* **SAMO-2007** couples probabilistic convolution (aleatory) with fuzzy calculus (epistemic).
* ANU’s “encapsulation” method guarantees convergence when only variable ranges are known, later post-processed with PDFs.
* Modern hybrid numeric schemes (e.g., UQ patterns inside MUSCLE3) allow the user to chain multiple uncertainty representations within the *same* workflow.  In CoT you can in principle splice symbolic belief functions at earlier steps and Monte-Carlo Dropout at later ones.

### 2.3 Calibration Notions and Why “Moderate” is Sufficient
A 2016 risk-modelling study defines weak → strong calibration.  *Moderate* calibration (observed ≈ predicted within strata) is mathematically enough to avoid harm in clinical decisions; chasing “strong” calibration can over-fit.  For CoT, aiming for **moderate per-step calibration** is a pragmatic target.

---
## 3  Why Stepwise Estimation in Chains of Thought?
Multi-hop reasoning compounds error multiplicatively.  If the log-odds of correctness at each step is `l_i`, the final log-odds is ∑ `l_i`; mis-calibration of even ±0.1 at each hop explodes over 10–20 hops.  Stepwise UQ enables:
* Early abort or re-prompt when local uncertainty spikes (TouT pruning).
* Dynamic compute allocation (Learning-to-Cascade, 2021) where low-uncertainty states exit early, saving FLOPs.
* Selective human-in-the-loop review in safety-critical settings (Cardiac Syndrome X registry, Tehran Heart Center) where per-step gating of clinician review improves throughput.

---
## 4  Empirical Findings in LLM Chain-of-Thought
### 4.1 Verbal Confidence and Calibration
* **Lin et al. 2022 / Sylin et al. 2022**: GPT-3 (175 B) attaches “90 % confidence” tags on **CalibratedMath**; empirical frequency ≈ stated probability.
* Remains *moderately* calibrated under synthetic distribution shift.
* Verbal probabilities rival logit-based estimates and survive prompt paraphrasing.

### 4.2 Scaling Behaviour
* **BIG-bench (2022)** shows that calibration improves with model size up to 10^11 params, but bias also grows.
* GPT-4 SOTA on CommonsenseQA, SuperGLUE, MATH, HANS (2024 cognitive-psychology audits) indicates both higher accuracy *and* retained ability to self-assess.

### 4.3 Tree of Uncertain Thoughts (TouT, 2023)
* Injects Monte-Carlo Dropout variance at **each node**; aggregates into global search.
* Outperforms vanilla ToT on Game of 24 and NYT-style Mini-Crosswords.
* Establishes a *template*: `local_uncertainty → search_policy → final_decision`.

### 4.4 Geometry of Thought Trajectories
* **Lines of Thought (2023)**: independent forward passes cluster on a low-dim manifold; can be approximated by a learned SDE → suggests that uncertainty in CoT might admit a *compact parametric model* rather than brute-force sampling.

### 4.5 Hallucination Mitigation via Risk Scores
* Pareto-optimal self-supervision (Zhang et al. 2023) fuses heuristics with LLM outputs to compute a **risk score**; re-prompting only high-risk items lifts GPT-3 above SOTA weak-supervision and GPT-4 above fully-supervised baselines in relation extraction.

---
## 5  Decoding- and Search-Level Risk
| Family | Key Result | Caveat |
|---|---|---|
| **Minimum Bayes Risk Decoding** | Mitigates copy noise & domain shift in NMT (Eikema & Aziz 2020; ACL 2021) | Length/token biases inherited from evaluation utility |
| **Arc-Averaged Risk** | Tighter correlation to actual WER in Viterbi beam search (Japanese lecture ASR, 100k words) | Requires rich feature engineering |
| **Quantum Beam Search** | Quadratic speed-up for power-law token distributions; higher accuracy on DeepSpeech | Still theoretical for LLMs; needs quantum HW |
| **NLI-Assisted Beam Re-ranking** | Entailment + diversity term reduces hallucinations on XSum, CNN/DM | Cost of on-the-fly entailment estimates |
| **UCT+T / Nested Monte Carlo (MAX)** | Boosts GGP champion Ary; shows that transposition tables + nesting can be combined with UQ (value uncertainty) | Requires task-specific heuristics |

These methods emphasise that **uncertainty need not be estimated *only* from the model’s logits**; it can be crafted from external utilities (entailment probability, risk bounds, game-theoretic value) and injected into the decoder.

---
## 6  Symbolic–Probabilistic Frameworks for Deep Reasoning
1. **Multi-Entity Bayesian Networks (MEBN, 2007)**  
   *Proven* to represent a distribution over any finitely-axiomatisable FOL theory.  Implemented via PR-OWL and UnBBayes-MEBN.  Empirically used in RoboCup Soccer agents and cultural-heritage knowledge graphs.
2. **First-Order Bayesian Logic**  
   Formal backbone that guarantees soundness when instantiating MEBN fragments (MFrags) at arbitrary depth.
3. **Dempster-Shafer & Qualitative Propagation**  
   Extensions cover inter-causal, explaining-away patterns without numeric probabilities (Parsons, IJUFKBS).  A 2023 DL thesis adds “N-of” logical operator for human-aligned belief fusion.
4. **Early Hybrid Warnings**  
   Wellman (1991) shows post-hoc probability assignment over possibility space yields mis-calibration; underscores need for *native* uncertainty treatment at every reasoning hop.

**Take-away:** symbolic–probabilistic logics already support *stepwise* uncertainty propagation; LLM research can borrow aggregation rules from these mature theories.

---
## 7  Bayesian & Variational Techniques Relevant to Stepwise CoT
* **Stochastic Weight Averaging-Gaussian (SWAG)**  
  Captures annotator disagreement in NLI; alignment between variance and human subjectivity → a natural candidate for CoT weight-space uncertainty.
* **Hierarchical Stochastic Attention (AAAI-22)**  
  Replaces deterministic heads with Gumbel-Softmax sampling, matching ensembles/dropout calibration at lower cost.
* **EPFL’s SLANG (2019)**  
  Diagonal + low-rank natural-gradient update approximates full posterior; scales to transformers.
* **DiBS (2021)**  
  Jointly infers Bayesian-network topology and parameters via continuous latent manifold; could be used to discover latent CoT dependency graphs.
* **Structured VAEs & Relational VAEs (2020–2023)**  
  Infuse graph structure into latent code, matching GP meta-learning and sensor-time-series tasks; a route to *dynamically learn* the structure of CoT uncertainties.
* **Refined Variational Approximation w/ MCMC inner loop**  
  Improves ELBO and mixing for sequential latent models—useful when CoT needs temporally correlated latent uncertainty.

---
## 8  Domain-Specific Case Studies
| Domain | Finding | Implication for CoT |
|---|---|---|
| **Medical QA** | GPT-4 82.4 % on Ophthalmology (vs 75.7 % human) with calibrated explanations; incorrect explanations longer. | Longer chain often ↔ higher uncertainty; stepwise length penalty might flag risk. |
| **Safety-Critical Prognostics** | GP vs BNN benchmark (NASA RUL, Li-ion battery) with ready-made UQ metrics. | Provides labelled datasets to evaluate CoT for engineering diagnostics. |
| **Offline RL** | MSG deep ensembles: independent pessimistic targets beat CQL/IQL on D4RL ant-maze by >20. | Signals the value of *independence* among reasoning paths—mirrors diversity requirement in CoT sampling. |
| **Control MPC** | Ensemble-Kalman-Sampler-driven robust MPC handles polytopic uncertainty with guarantees. | Offers template for formal guarantees when CoT is part of control loop.
| **Finance** | Least-Squares Monte Carlo optimal inner-sample count (hal-03770051) clarifies compute vs variance trade-off. | Analogous to number of thought-samples (n_search) vs latency in LLM.

---
## 9  Benchmarks & Tooling Landscape
* **CalibratedMath** — First dataset for LLM confidence calibration in math QA.
* **ThoughtSource** — 15 CoT datasets (7 scientific/medical, 5 math, 3 general) with unified API.
* **BIG-bench** — 204 tasks, 132 institutions; scaling law insights.
* **BCSC Ophthalmology** — 1,023 items, supports explanation length vs accuracy analysis.
* **Github TouT & CalibratedMath repos** — reference implementations of per-node uncertainty.
* **monaco, Uncertainpy, MUQ, MUSCLE3** — toolboxes for Monte-Carlo, Sobol sensitivity, hierarchical inverse UQ, and coupled multi-scale workflows.

---
## 10  Contrarian & Emerging Ideas
* **Quantum Beam Search** — Theoretically √-speed-up; worth testing on top-k sampling for CoT.
* **Latent-Space Distance (RSC 2023)** — Zero-cost UQ metric beating ensembles in chemistry; candidate cheap heuristic for early CoT pruning.
* **Lines of Thought SDE** — Compact SDE surrogate could enable *gradient-based* optimisation over reasoning paths.
* **Hybrid Symbolic–Neural Cascades** — Calibrating base RF/XGBoost improves LIME explanation reliability, hinting that calibrated uncertainty propagates into *interpretability* layers.
* **Real-time Ensemble Pruning (Garaud & Mallet 2011)** — Select 20–30 high-value members → analogous to selecting a subset of thought branches to preserve variance without full enumeration.

---
## 11  Design Patterns and Recommendations
1. **Self-Verbalised Probability + Logit Fusion**  
   Compute both softmax-based and natural-language confidence; apply temperature scaling on logits and isotonic regression on verbal numbers, then *ensemble*.
2. **Local-Global Hybrid Search**  
   Use TouT-style MC-Dropout to score *local* nodes ➜ feed into UCT+T or arc-risk pruning for *global* search policy.
3. **Independence-Promoting Sampling**  
   Draw *diverse* CoT samples via nucleus sampling with anti-token penalties (MSG insight: independence > shared backbone).
4. **Moderate Calibration Target**  
   Evaluate Expected Calibration Error (ECE) per step; aim for <5 % absolute deviation in each 10-bucket histogram.
5. **Dynamic Compute Cascades**  
   Integrate Learning-to-Cascade loss so that low-uncertainty steps exit early, saving FLOPs while preserving accuracy.
6. **Risk-Based Re-prompting**  
   Implement Zhang et al.’s harmoniser; re-prompt only responses whose risk > τ.  τ can be adapted by domain criticality.
7. **Symbolic Consistency Checks**  
   Encode domain constraints in MEBN or Dempster-Shafer; hard-fail CoT trajectories that violate high-confidence rules.

---
## 12  Open Research Questions
1. **Propagation Law:** How exactly does local epistemic variance compose over nonlinear reasoning operators in LLMs? (Analogous to variance-of-log-odds sums.)
2. **Unified Representation:** Can we embed Fraunhofer’s three uncertainty sources (scope, data, model) into one latent manifold learned via Structured VAEs?
3. **Manifold Regularisation:** Leverage Lines-of-Thought SDE to regularise sampling—does this improve both diversity *and* calibration?
4. **Quantum Search:** What is the empirical gain of quantum beam search on transformer token distributions simulated classically?  Does uncertainty concentrate faster?
5. **Symbolic–Neural Fusion:** How to auto-compile MEBN fragments into soft prompts for GPT-4, preserving probabilistic semantics?
6. **Task-aware Metrics:** ATENE shows word-error ≠ downstream risk; what is the analogue for CoT?  Need a metric that correlates with decision loss, not token match.
7. **Human-AI Agreement:** SWAG aligns with annotator disagreement; could stepwise weight variance predict *where* human experts would disagree with the CoT?

---
## 13  Conclusion
The last three years have produced a *patchwork* of techniques—verbal confidence, Monte-Carlo Dropout, Bayesian ensembling, symbolic logic, quantum search—that each capture fragments of the stepwise uncertainty story.  The empirical evidence (TouT, CalibratedMath, MSG, arc-risk ASR, NLI re-ranking) converges on one principle: **local uncertainty is valuable only when it actively steers the downstream reasoning or search process.**  

A robust pipeline therefore must:
1. Quantify uncertainty at every intermediate thought (multiple modalities welcome).
2. Propagate and *use* it—either to prune, rerank, or allocate compute.
3. Validate via domain-relevant, task-aware metrics on open benchmarks.

Bridging neural, symbolic, and emerging quantum or manifold-based ideas promises richer, safer, and computationally efficient reasoning systems.  The research community is now well-positioned—with datasets (ThoughtSource, CalibratedMath), toolkits (MUQ, monaco, MEBN engines), and theoretical insights—to move from ad-hoc techniques to a principled, **holistic** science of stepwise uncertainty in chain-of-thought.


## Sources

- http://aclweb.org/anthology/D/D15/D15-1182.pdf
- https://resolver.caltech.edu/CaltechAUTHORS:20210121-152557627
- http://www.nusl.cz/ntk/nusl-444760
- https://www.repository.cam.ac.uk/handle/1810/316387
- https://zenodo.org/record/8182640
- http://bear.warrington.ufl.edu/brenner/papers/brenner-griffin-koehler-obhdp2005.pdf
- http://hdl.handle.net/20.500.11850/639056
- http://hdl.handle.net/20.500.11850/523007
- http://resolver.tudelft.nl/uuid:e357848d-0ae1-47f1-a5ac-46900fcd1225
- http://hdl.handle.net/11582/29689
- https://zenodo.org/record/7634488
- https://scidar.kg.ac.rs/handle/123456789/9729
- http://hdl.handle.net/10.1371/journal.pcbi.1006785.t001
- http://www.scopus.com/home.url)
- https://cris.maastrichtuniversity.nl/en/publications/bd49eae7-0f44-4dd5-a4db-e11c4833db6c
- https://ojs.aaai.org/index.php/AAAI/article/view/16900
- https://research.utwente.nl/en/publications/stochastic-upscaling-via-linear-bayesian-updating(a11e0ecd-26b9-4ff8-920a-9d1de1b6f3fc).html
- http://arxiv.org/abs/2205.09159
- https://hal.archives-ouvertes.fr/hal-03394664
- https://www.repository.cam.ac.uk/handle/1810/321771
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.45.5576
- http://dspace.library.uu.nl/handle/1874/390212
- https://pure.eur.nl/en/publications/7e9dc0db-22c5-4f37-b216-0819883c0a9b
- https://hal.archives-ouvertes.fr/hal-03719603/document
- https://figshare.com/articles/_Results_of_the_Uncertainty_Analysis_/1483802
- http://arxiv.org/abs/2202.06387
- https://hdl.handle.net/1721.1/134631.2
- http://hdl.handle.net/11311/1189787
- http://www.inference.phy.cam.ac.uk/ph347/CPGS-Report_Hennig.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.71.5991
- https://repository.uwtsd.ac.uk/id/eprint/3483/
- http://www.iasir.net/IJSWSpapers/IJSWS14-454.pdf
- http://hdl.handle.net/1822/11388
- https://ojs.aaai.org/index.php/AAAI/article/view/21314
- https://lirias.kuleuven.be/bitstream/123456789/163350/1/Lucor_Meyers_Sagaut_JFM585.pdf
- https://madoc.bib.uni-mannheim.de/46637/
- http://www.sciencedirect.com/science/article/B6V8V-504BH0K-1/2/dd353a81846d755ccdc85f012d12502d
- https://ojs.aaai.org/index.php/AAAI/article/view/21364
- http://hdl.handle.net/10138/352138
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/a4/f9/TSWJ2014-724639.PMC4132335.pdf
- http://arxiv.org/abs/2309.07694
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.434.3633
- http://infoscience.epfl.ch/record/266668
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.86.9151
- https://ojs.aaai.org/index.php/AAAI/article/view/4275
- https://dx.doi.org/10.3390/e19060286
- http://ir.lib.ntnu.edu.tw/ir/handle/309250000Q/21988
- https://ojs.aaai.org/index.php/AAAI/article/view/6062
- https://escholarship.org/uc/item/2tf851c5
- https://hdl.handle.net/1721.1/135244
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.90.1935
- https://drops.dagstuhl.de/opus/volltexte/2017/6915/
- https://digital.library.unt.edu/ark:/67531/metadc883763/
- http://hdl.handle.net/10138/563840
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.8.2380
- http://arxiv.org/abs/2212.02712
- http://people.csail.mit.edu/bohsu/NgramWeighting2008.pdf
- http://hdl.handle.net/10.1371/journal.pone.0206316.t004
- https://ojs.aaai.org/index.php/AAAI/article/view/6177
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.43.8609
- http://aiac.ae.metu.edu.tr/db/serv.php?Paper=AIAC-2015-072
- https://zenodo.org/record/7658915
- https://hal.univ-grenoble-alpes.fr/hal-03770051/file/least-squares.pdf
- https://digitalcommons.mtu.edu/michigantech-p/14448
- https://keele-repository.worktribe.com/file/421660/1/GRADE%20concept%20paper%202.pdf
- https://dare.uva.nl/personal/pure/en/publications/uncertainty-robustness-and-safety-in-artificial-intelligence-with-applications-in-healthcare(509089b9-e65d-46f1-ad65-4fc0f75f4aca).html
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Kraft=3AJan=3A=3A.html
- http://cds.cern.ch/record/1985671
- http://hdl.handle.net/10.1184/r1/6707516.v1
- http://hdl.handle.net/2013/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/170783
- http://nthur.lib.nthu.edu.tw/dspace/handle/987654321/67122
- https://www.zora.uzh.ch/id/eprint/208880/1/2021.acl-long.22.pdf
- http://cds.cern.ch/record/2317533
- https://hdl.handle.net/2108/347332
- http://urn.kb.se/resolve?urn=urn:nbn:se:hb:diva-30286
- http://hdl.handle.net/2440/110214
- https://ojs.aaai.org/index.php/AAAI/article/view/4719
- http://dl.lib.mrt.ac.lk/handle/123/11762
- http://digital.library.unt.edu/ark:/67531/metadc881140/
- http://hdl.handle.net/11582/3404
- http://www.inb.uni-luebeck.de/publikationen/pdfs/ScUdMa08.pdf
- http://hdl.handle.net/10.6084/m9.figshare.25201199.v1
- http://hdl.handle.net/2066/116267
- https://dare.uva.nl/personal/pure/en/publications/supervised-uncertainty-quantification-for-segmentation-with-multiple-annotations(6db8aabe-cf24-4bf8-9ebb-38880d5b824a).html
- http://hal-irsn.archives-ouvertes.fr/docs/00/19/66/63/PDF/SAMO2007_BaccouChojDes.pdf
- https://research.tue.nl/en/publications/0c9306fb-2c02-4466-b15b-43bcf276d22c
- http://oa.upm.es/63755/
- http://enu.kz/repository/2009/AIAA-2009-2282.pdf
- https://hal.archives-ouvertes.fr/hal-01251370
- https://zenodo.org/record/3260941
- http://aaaipress.org/Papers/FLAIRS/1998/FLAIRS98-080.pdf
- https://doi.org/10.1051/meca/2022001
- https://cris.maastrichtuniversity.nl/en/publications/1ae28d7e-269d-48bb-94fc-8409a2999783
- https://eprints.sztaki.hu/4657/
- https://www.intechopen.com/books/uncertainty-quantification-and-model-calibration
- https://doaj.org/article/258bc90aca1a4ffabfef84160e166ca6
- https://eprints.lancs.ac.uk/id/eprint/70734/
- https://doi.org/10.1007/978-3-540-87608-3_3
- https://hal.science/hal-01512528
- http://hdl.handle.net/11858/00-001M-0000-000F-3A07-7
- https://cris.maastrichtuniversity.nl/en/publications/51a1aea9-d743-47b8-8f2d-356075a7fe1c
- http://www.shakirm.com/papers/VITutorial.pdf
- https://www.repository.cam.ac.uk/handle/1810/314918
- https://hal.inria.fr/hal-00655771
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0888613X01000457/MAIN/application/pdf/6af917933d097a08e2481bafd4fdc2f7/main.pdf
- https://hdl.handle.net/2027.42/3635
- https://ojs.aaai.org/index.php/AAAI/article/view/12191
- https://discovery.ucl.ac.uk/id/eprint/10101435/
- https://nottingham-repository.worktribe.com/file/14597120/1/GPT4%20%282%29
- http://hdl.handle.net/2013/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/226844
- http://publica.fraunhofer.de/documents/N-518409.html
- http://www.aaai.org/Papers/FLAIRS/2008/FLAIRS08-142.pdf
- https://figshare.com/articles/Ensemble_analysis_of_uncertainty_of_flux_estimations_for_brain_metabolism_/1354554
- http://urn.fi/urn:nbn:fi-fe2021090645179
- https://figshare.com/articles/Estimated_lung_cancer_risks_OR_with_95_confidence_intervals_CI_for_categories_of_the_longest_period_of_unemployment_by_gender_/5906344
- https://hal.archives-ouvertes.fr/hal-02049801
- http://hdl.handle.net/10261/261252
- http://hdl.handle.net/11585/98567
- https://ieeexplore.ieee.org/xpl/conhome/9087828/proceeding
- http://arxiv.org/abs/2206.01558
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0888613X12000448/MAIN/application/pdf/fd205f12e87410af8724c8d91c53c65c/main.pdf
- http://arxiv.org/abs/2205.14334
- https://hal.archives-ouvertes.fr/hal-00636943
- https://opus.bibliothek.uni-augsburg.de/opus4/frontdoor/index/index/docId/35663
- http://inderscience.metapress.com/link.asp?target=contribution&id=P3G8413020276120
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:0888613X91900057/MAIN/application/pdf/41a972e307f139e0d9abab64dd78a1b5/main.pdf
- https://doaj.org/article/3c4ac302e25840e89a8f5ce823029136
- http://ceur-ws.org/Vol-1204/papers/paper_6.pdf
- https://figshare.com/articles/Figure_S3_Score_calibration/1405674
- https://hal.science/hal-00802919
- https://doaj.org/toc/1537-744X
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA615505%26Location%3DU2%26doc%3DGetTRDoc.pdf
- https://www.sciencedirect.com/science/article/abs/pii/S1566253523001227
- http://summit.sfu.ca/item/19921
- https://opus.bibliothek.uni-augsburg.de/opus4/frontdoor/index/index/docId/21437
- https://zenodo.org/record/4651517
- https://authors.library.caltech.edu/92401/1/1811.10276.pdf
- https://openreview.net/forum?id=zjAEa4s3sH
- http://ieeexplore.ieee.org/document/7230273/
- http://cds.cern.ch/record/2264304
- https://zenodo.org/record/8316324
- https://ro.uow.edu.au/theses/4666
- https://pure.eur.nl/en/publications/76e54872-1678-45eb-9cea-8375470ce3f8
- https://zenodo.org/record/1300336
- https://doaj.org/article/d28060e207ec43dd9bab71b3839987ad
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:0888613X9090002J/MAIN/application/pdf/a1bb787e1858b7ef7a5e7ac2e37561ff/main.pdf
- http://nms.kcl.ac.uk/simon.parsons/publications/journals/ijufkbs2.pdf
- http://cds.cern.ch/record/2283329
- https://pdxscholar.library.pdx.edu/systems_science_seminar_series/123
- http://www.mt-archive.info/MTS-2009-Xiong-1.pdf
- http://www.biia.com/library/Veda
- http://arxiv.org/abs/2206.04615
- https://figshare.com/articles/Comprehensive_Memory-Bound_Simulations_on_Single_Board_Computers/6431455
- https://hal.archives-ouvertes.fr/hal-02963425
- www.myjurnal.my/filebank/published_article/252414.pdf
- http://mklab.iti.gr/files/VISIGRAPP2014Chantas_etal.pdf
- https://zenodo.org/record/6635194
- https://dare.uva.nl/personal/pure/en/publications/reasoning-in-nonprobabilistic-uncertainty-logic-programming-and-neuralsymbolic-computing-as-examples(297f803e-3318-4cce-8ddf-5c004bda4a33).html
- http://hdl.handle.net/10536/DRO/DU:30111072
- https://doaj.org/article/cfd6089d4104413787e743dddb10d8e7
- http://www.iro.umontreal.ca/%7Efoster/papers/ce-acmtlsp06.pdf
- http://www.armyconference.org/ACAS00-02/ACAS01/BookerJane/BookerJane.paper.pdf
- http://summit.sfu.ca/item/19407
- https://hal.inrae.fr/hal-02803500
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll3/id/425853
- https://ams.confex.com/ams/pdfpapers/163168.pdf
- https://archiv.ub.uni-heidelberg.de/volltextserver/volltextserver/31044/1/thesis_color.pdf
- https://dare.uva.nl/personal/pure/en/publications/easing-multiscale-model-design-and-coupling-with-muscle-3(298a965c-72ae-4771-9069-d4a6b2b8ea26).html
- http://lia.univ-avignon.fr/fileadmin/documents/Users/Intranet/chercheurs/bechet/publifred/FB_2003_ASRU.pdf
- http://arxiv.org/abs/2205.13703
- https://zenodo.org/record/7545741
- https://ojs.aaai.org/index.php/AAAI/article/view/4127
- http://repository.ubn.ru.nl/bitstream/handle/2066/83218/83218.pdf
- http://arxiv.org/abs/2306.16564
- http://hdl.handle.net/10453/26581
- http://arxiv.org/pdf/1311.0707.pdf
- https://escholarship.org/uc/item/7ns0f906
- https://hal.archives-ouvertes.fr/hal-03792800/document
- https://doi.org/10.1016/j.learninstruc.2012.06.001
- http://hdl.handle.net/1885/62318
- https://figshare.com/articles/Association_of_higher-order_interactions_with_overall_ARC_risk_based_on_MDR_Analysis_/6177857
- http://www.lamsade.dauphine.fr/%7Ecazenave/papers/ggp2009.pdf
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0004370207001312/MAIN/application/pdf/d0f8da99dcc15e34b60ff865a43bae10/main.pdf
- http://scholarbank.nus.edu.sg/handle/10635/104649
- http://hdl.handle.net/10852/68397
- https://dc.etsu.edu/cgi/viewcontent.cgi?article=5582&amp;context=etd
- http://hdl.handle.net/1854/LU-8708723
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.70.7074
- https://archive-ouverte.unige.ch/unige:34269
- http://resolver.tudelft.nl/uuid:785334e4-bc6e-4a86-9dfd-6e1d3aa58f85
- http://hal-enpc.archives-ouvertes.fr/docs/00/65/57/71/PDF/garaud11automatic.pdf
- http://hdl.handle.net/21.11116/0000-000A-A031-9
- http://digital.library.unt.edu/ark:/67531/metadc844097/
- http://cds.cern.ch/record/2762168
- https://www.repository.cam.ac.uk/handle/1810/298857
- http://arxiv.org/pdf/1406.3650.pdf
- https://bibliotekanauki.pl/articles/332996
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:0888613X88900047/MAIN/application/pdf/49a952abfe58c6a10aa2bfca014584e0/main.pdf
- http://ticc.uvt.nl/icga/acg12/proceedings/Contribution117.pdf
- http://www.sciencedirect.com/science/book/9780124115576
- https://zenodo.org/record/239035
- https://www.repository.cam.ac.uk/handle/1810/324365
- http://hdl.handle.net/11311/1196431
- http://www.sigdial.org/workshops/workshop5/proceedings/pdf/raymond.pdf
- https://hal.inria.fr/hal-02272303
- http://hdl.handle.net/10068/647670
- https://zenodo.org/record/6946859
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.43.8183
- https://www.scipedia.com/public/Pons_Prats_Bugeda_2019a
- https://dare.uva.nl/personal/pure/en/publications/uncertainty-quantification-patterns-for-multiscale-models(839b7f14-e4a7-4429-b15b-456d33a107be).html
- http://hdl.handle.net/20.500.11850/521340
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.94.2117
- http://repository.cmu.edu/cgi/viewcontent.cgi?article%3D3122%26context%3Dcompsci
- https://zenodo.org/record/4441651
- http://www.cs.utep.edu/vladik/2015/tr15-29.pdf
- https://hal.science/hal-01221601
- https://hal.science/hal-03988727
- https://escholarship.org/uc/item/0j276263
- https://zenodo.org/record/3258865
- https://pub.uni-bielefeld.de/record/1993746