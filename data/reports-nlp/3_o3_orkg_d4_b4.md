# Probabilistic Opinion Pooling for Open-Domain Question Answering – State of the Art, Lessons Across Domains, and Research Agenda (2025)

## 1. Motivation and Scope  
Open-domain question answering (OD-QA) systems increasingly rely on *ensembles* of heterogeneous agents: retrieval-augmented LLMs, knowledge-graph reasoners, vision–language models, speech recognisers, etc.  Each agent emits a probability distribution \(p_k(a\mid q)\) over candidate answers \(a\).  *Probabilistic opinion pooling* asks: **how should these distributions be combined into a single, calibrated posterior?**  

The report integrates five strands of evidence:

1. **Aggregation theory** — linear, log, geometric, multiplicative and Rényi pools; Bayesian model averaging (BMA); copula and fuzzy extensions; calibration theory.
2. **Practical architectures** — MoE LLMs, judge–specialist QA, RL-weighted knowledge distillation, quadratic-mean fusion, MinCq, sequence-level and stochastic KD, divide-and-conquer BMA for large Bayesian networks, lightweight multimodal fusion.
3. **Empirical lessons** — 2002–2024 experiments across NLP, vision, remote sensing, forecasting, finance, nuclear safety, radar, speaker verification and political science.
4. **Multimodal generalisation** — image–text VQA, audio-text MTL-QA, LF disparity fusion, TimeSpec4LULC, scale-consistent LF fusion, multimodal hierarchical Dirichlet processes (mmHDPs).
5. **Tooling & benchmarks** — NQ, MuMuQA, MTL-QA, INTERSPEECH judge–specialist set-ups, S2ORC metadata caveats, Bayesian-UQ software (BMS, Pi4U, UQLab, cira_uq4ml).

All 80+ learnings supplied are cited in-line.  Speculative claims are marked *[Spec]*.

## 2. Historical Trajectory of Opinion Pooling  

### 2.1 Early Ensemble Models (≈2000-2010)
* **High-dimensional sparse QA** was already amenable to probabilistic model averaging: a 2002 study cut binary query error by 50 % using convex-optimised weights across *thousands* of dimensions.  
* *Bayesian Model Averaging* (BMA) became the statistical workhorse: Hjort & Claeskens (2003-04) built frequentist risk bounds, while the **BMS R package** (2013) operationalised hyper-g priors, MCMC sampling and full diagnostics; tooling was otherwise scarce until ≈2011.
* In language technology, **Vaswani et al.** embedded a neural probabilistic LM directly into MT decoders and k-best re-ranking (+1.1 BLEU).  Google’s trillion-token n-gram LM embraced the “**Stupid Backoff**” smoother for scalable probability assignment.
* In nuclear engineering, **ANSWERS®** linked reactor codes with Bayesian updating against >2 000 criticality experiments – early evidence that domain-specific pools can outperform single-model workflows.

### 2.2 Axiomatic Diversification (2010-2020)
* **Dietrich & List** clarified that linear pools are only *procedurally* rational; geometric or multiplicative pools are *epistemically* defensible when agents use shared vs. private data.  
* **Rényi mixtures** (Storkey–Zhu–Hu, 2014) introduced a one-parameter interpolation \(\alpha\) between linear (\(\alpha=0\)) and log pools (\(\alpha\to\infty\)); Kaggle experiments showed the log limit is optimal when agents are unbiased and share evidence.  
* Finance adopted **copula opinion pooling** (Meucci 2005; NB working paper 2010; sentiment-driven trading 2018) to fuse non-Gaussian views, beating both linear and log pools on KL (KLIC) and risk metrics.
* **Quadratic-mean fusion** (Arandjelović 2016) overturned the community’s linear-weight baseline in object recognition, ECG and traffic fatality prediction – O(d) cost, interpretability retained.
* **Empirical recalibration pipelines**: two-parameter recalibration followed by log-odds averaging (26.7 % mean Brier gain), Smirnov-transformed linear pools for inflation nowcasts (10-30 % CRPS lift), and weighted-median updating grounded in cognitive dissonance for human forecasts.
* **General-agenda & premise-based extensions** bridge binary judgment aggregation and probabilistic pooling – directly relevant to modular QA where each sub-question can be pooled then constrained.

### 2.3 Scaling Era & LLM Renaissance (2021-2025)
* **Sparse MoE LLMs** achieve dense-model quality with ≈ ¼ pre-training FLOPs; cross-expert KD (RWTH 2020) and *Stochastic KD* (SKDBERT) retain 99.5 % GLUE while halving latency.
* **Judge–Specialist monotonic aggregation** (INTERSPEECH 2023) guarantees that adding sources never hurts accuracy on *Natural Questions* and stays robust to ASR noise – a direct instantiation of constrained pooling.
* **Large-scale Bayesian network averaging**: Bristol’s ε-optimal enumeration pushes credible-set averaging to >30 variables; LSBN’s divide-and-conquer pipeline adds Markov-blanket isolation and merge heuristics.
* **RL-weighted multi-teacher KD (RMT-KD)**, **Semantic Calibration KD (SemCKD)** and **Vocabulary-Aware Distillation (VIPI)** demonstrate dynamic, instance-specific weights rather than static pools.
* **Non-parametric calibration tests** revealed that many deep ensembles are *not* epistemically calibrated; post-hoc recalibration or training-time constraints are required.

## 3. Theoretical Foundations Relevant to OD-QA  

### 3.1 Pooling Families and Properties
| Family | Formula (aggregation of K agents) | Key properties | QA implications |
|---|---|---|---|
| Linear \(p\_\text{agg}(a)=\sum w_k p_k(a)\) | Preserves unanimity, may violate independence | Simple, differentiable; prone to *over-dispersion*; baseline for majority of LLM ensembles |
| Log (Product) \(\propto\prod p_k(a)^{w_k}\) | Likelihood equivalence; yields sharper posteriors | Sensitive to mis-calibration; good when agents share evidence |
| Geometric | Normalised \(\sum w_k \log p_k\) then exp | Axiomatic justification under shared data | Useful for multi-retriever setups where passages overlap |
| Multiplicative | Variant of log pool with private info axiom | De-emphasises overlapping evidence | Fits retrieval + KG hybrid pipelines |
| Rényi (α-mixture) | Interpolates linear↔log | Choose α by cross-val or bias priors | Allows *continuous control* over sharpness |
| Quadratic Mean | \(\sqrt{\sum w_k p_k(a)^2}\) | Empirically higher accuracy in vision | Offers robust alternative with same O(K) cost |
| Copula Pool | Aggregates via joint CDF, decoupling marginals | Handles non-Gaussian / heavy-tail | Candidate for answer calibration when probabilities heavy-tailed |
| Fuzzy / Hesitant | Linguistic, q-rung, 2-tuple | Outlier-robust, attribute correlation | Useful when confidence expressed linguistically (human-in-the-loop) |

### 3.2 Weight-Setting Principles
1. **Bayesian posterior weights** (BMA, model evidence).  
2. **Score-based weights** – maximise KL skill (Norges Bank 2010), MinCq’s voter-diversity QP, reinforcement-learned (RMT-KD), policy-gradient (deep).  
3. **Dynamic or time-weighted** – as deadline approaches, decay older beliefs (CSU 2024).  
4. **Normative Linear Pooling** – filter ‘dominant’ but uncompetitive models before assigning weights (corporate default 2023).  
5. **Instance-adaptive** – per-query RL policy, or per-token gating in Mixture-of-Experts.

### 3.3 Calibration & Verification Metrics
* **Brier decomposition** (Murphy, Ferro extensions) – reliability, resolution, uncertainty; weighted and latitude-weighted variants matter (seasonal climate).  
* **KL / Log-Loss decomposition** – exact split into entropy, reliability, resolution (Benedetti 2010); aligns with optimisation of log pools.  
* *Averaging logits vs. probabilities* – logits tighten ECE for under-confident nets but *explode* over-confident false-positives; probability space remains safer for high-stakes QA.
* **Non-parametric calibration test** – an ensemble is calibrated only if *some* convex combination is; many modern QA ensembles fail.

## 4. Practical Architectures for OD-QA Opinion Pooling  

### 4.1 Multi-Reader / Multi-Retriever Pipelines
1. **Judge–Specialist** (2023) – K specialised retriever-reader stacks feed distributions to a separate LM judge that outputs pooled probabilities under monotonicity constraints.  
2. **Rényi-weighted retrievers** *[Spec]* – estimate agent bias via validation; choose α-mixture per question.  
3. **General-agenda pooling** – treat sub-questions (entities, types, supporting facts) as ‘basic events’, pool their probabilities line-by-line, then solve global constraints (truth-functional closure).  

### 4.2 LLM Mixture-of-Experts & Distillation
* **Sparse MoE LLMs** – token-wise router softmax ≈ multiplicative pooling over expert posteriors.  Cross-expert KD acts as *student* linear pool with additional regularisation.
* **Stochastic KD** – random teacher sampling implicitly approximates an unweighted linear pool over time, but with variance reduction.
* **RMT-KD** – RL assigns per-instance teacher weights ≈ dynamic linear pool; outperforms uniform weights on GLUE and OD-QA (*[Spec]* extension pending).  
* **SemCKD** – per-layer soft assignment; analogous to hierarchical pooling.

### 4.3 Bayesian Ensembles & Credible Sets
* **Approx-guaranteed BMA** for Bayesian networks (AAAI 2019; Bristol 2023/24) makes it feasible to model-average thousands of candidate belief graphs for entity linking or multi-hop reasoning.  
* **Warped Bayesian Quadrature** can replace MCMC evidence estimation inside BMA, accelerating weight computation.
* **Two-level BMA for control** (Darwen 2023) hints at *action-aware pooling*: first average world models, then answer-policy distributions – relevant for interactive QA agents.

### 4.4 Lightweight & Multimodal Fusion Modules
* **High-order tensor fusion** (MFH, BLOCK) compress tri-linear interactions; remained SOTA for VQA until larger VL-LLMs.  
* **Scale-consistent LF fusion** aligns disparity volumes before attention-guided residual fusion; conceptually similar to aligning answer logits from systems with different calibration scales.  
* **Lightweight Data Fusion (LDF)** and **mmHDP** extend Bayesian pooling to unaligned modalities – usable when text answers need evidence from images or audio segments in MTL-QA.
* **ArithFusion** shows that *single arithmetic operation* can beat heavy transformers for image pair fusion – evidence that quadratic-mean or RMS pools may win over deep modules in QA.

### 4.5 Specialist Non-Text Channels
* **Speaker-verification Bayesian weighting** – uncertainty-aware logistic regression cuts EER by 37 %; analogy: weight speech-transcribed answers lower when ASR uncertainty high.  
* **Deep Density Network ensembles** for spoken-language scoring illustrate benefit of distilling mixture-density ensembles into single MDN – blueprint for compressing OD-QA ensembles while keeping calibrated uncertainty.
* **Information-geometry radar pooling** formalises resolution as a detection-tracking trade-off; similar geometry could guide *answer-span resolution* in span-based QA.

## 5. Empirical Benchmarks & Datasets  
| Dataset / Task | Relevance to pooling | Notes |
|---|---|---|
| Natural Questions (NQ) | Multi-passage, single gold | Used by Judge–Specialist monotonic pool |
| MuMuQA | Cross-media, multi-hop | Baselines still far from human; highlight multimodal fusion gap |
| MTL-QA | KG + Wikipedia + audio | Enables multitask open-domain & KGQA pooling |
| INTERSPEECH 2023 configs | Speech-noise robustness | Tests multisource ASR+text pooling |
| S2ORC | 200 M papers metacorpus | Caveat: 0.91–0.99 metadata accuracy; pooled retrievers must account for noise |
| TimeSpec4LULC | MODIS 7-band >200 time-steps | Good sandbox for spatio-temporal pooling strategies |

## 6. Lessons Transferrable to OD-QA  

1. **Baseline choice matters** – quadratic-mean or Rényi pools can *strictly dominate* weighted averages at the same computational cost.
2. **Calibration is as important as accuracy** – log pools sharpen but magnify mis-calibration; for LLM ensembles with over-confident answers, probability-space linear or RMS pools are safer.
3. **Dynamic weighting outperforms static** – RL, time-weighted, or normative linear pools adapt to question difficulty and deadline pressure.
4. **Structure matters** – pooling at fine-grained ‘basic events’ (entities, hops) then constraining globally improves logical consistency and mitigates doctrinal paradox analogues.
5. **Cross-modal alignment first, pooling second** – scale-consistent LF methods, mmHDPs and ArithFusion show that unaligned feature spaces corrupt pool quality.
6. **Compression is achievable without losing uncertainty** – sequence-level KD, ensemble-to-single MDN distillation, and VIPI vocab transfer all retain or even improve accuracy while shrinking size & latency.
7. **Tool support is mature** – BMS, Pi4U, UQLab, cira_uq4ml, MUCalc provide plug-and-play Bayesian UQ and pooling primitives; LSBN, ε-optimal enumeration, and Bristol’s libraries extend to structure learning.

## 7. Open Research Questions & Contrarian Ideas  
1. **α-Adaptive Rényi Pools for LLMs** – Estimate per-question α via gradient descent on held-out calibration error. *[Spec]*
2. **Quadratic-Mean Gating in MoE Routers** – Replace softmax with RMS aggregator; test if expert diversity acts like Arandjelović’s quadratic fusion.
3. **Copula Pooling for Overlapping Passages** – Fit a Gaussian/Student copula over top-k answer logits from retrievers to model dependency explicitly.
4. **Forecast-style Decomposition as Loss** – Optimise LLM ensembles directly on KL-based reliability & resolution terms (Benedetti 2010) rather than CE loss.
5. **Warped Bayesian Quadrature for Evidence Integration** – Use active quadrature to estimate evidence of answer sets quickly during retrieval-generation loops.
6. **Hopf-instability Analysis for Latency** – Apply dynamic-systems insight (7–15 month lag) to multi-agent dialog; predict when delayed pooling updates destabilise answer consensus. *[Spec]*
7. **Fuzzy q-Rung Dual Hesitant Pooling for Human-LLM Hybrid Teams** – When analysts provide linguistic confidence (‘likely’, ‘almost certain’), combine with model probabilities via PDMSM or H2TLCG operators.

## 8. Recommended Design Pattern for Future OD-QA Systems  
```
Retrieve K evidence sets ➔ K reader/LLM answer dists p_k
│
├─ Calibration module (per-agent two-param + temperature)
│
├─ Dependency assessment
│   ├─ Overlap score O_kl  (shared passages, shared data)
│   └─ Use O_kl to choose pool family: geometric if high overlap, multiplicative if low
│
├─ Weight assignment
│   ├─ Prior weight ∝ inverse agent entropy (MinCq diversity)
│   ├─ RL refinement per question (RMT-KD policy)
│   └─ Deadline decay if real-time (CSU 2024)
│
├─ Pool aggregator
│   ├─ Default: α-Rényi with α tuned by validation
│   ├─ Fallback: quadratic-mean when calibration uncertain
│   └─ Safety: probability-space averaging when ECE > β
│
└─ Post-hoc hierarchical consistency checks
    ├─ Entity-type compatibility
    └─ Premise-based closure (general-agenda pooling)
```
This blueprint is implementable with open-source tooling: BMS for weight optimisation, cira_uq4ml for calibration metrics, Bristol ε-optimal libraries for structure averaging, BLOCK for high-order vision-text fusion, and VIPI for efficient vocabulary transfer in the distilled final model.

## 9. Conclusion  
The last two decades provide *convergent evidence* that intelligent weight selection, calibration and family choice can yield 10–50 % error reductions across domains – from Norwegian GDP forecasts to object recognition and nuclear safety.  In OD-QA, the nascent Judge–Specialist and MoE/KD lines echo these findings but do **not yet exploit the full palette**: quadratic-mean fusion, copula pools, dynamic RL weighting, and fine-grained agenda pooling remain under-explored.  

With mature Bayesian-UQ toolchains, scalable α-Rényi mixtures, and data-efficient KD methods, the field is poised to replace ad-hoc majority vote with theory-grounded, empirically validated pooling that is *both* sharper and better calibrated.  The roadmap above—rooted in all 80+ cross-domain learnings—offers concrete steps toward next-generation, uncertainty-aware, multimodal OD-QA systems.


## Sources

- http://aclweb.org/anthology/D/D15/D15-1182.pdf
- http://hdl.handle.net/10.17608/k6.auckland.24796683.v1
- https://ojs.aaai.org/index.php/AAAI/article/view/16865
- https://hal.sorbonne-universite.fr/hal-02073644/document
- http://hdl.handle.net/10.1371/journal.pone.0206478.g004
- https://zenodo.org/record/3951676
- https://scholarworks.unist.ac.kr/handle/201301/59819
- http://hdl.handle.net/10536/DRO/DU:30003064
- https://repository.upenn.edu/dissertations/AAI3015308
- https://researchbank.rmit.edu.au/view/rmit:32684
- http://repository.cmu.edu/cgi/viewcontent.cgi?article%3D2405%26context%3Dcompsci
- http://infoscience.epfl.ch/record/266638
- http://hdl.handle.net/2429/84333
- http://hdl.handle.net/10197/12574
- https://zenodo.org/record/4015102
- http://hdl.handle.net/10255/dryad.126971
- http://journalarticle.ukm.my/77/1/
- http://clair.si.umich.edu/clair/HLT-NAACL03/shorts/pdf/hlt_naacl_03_shortpaper_301.pdf
- http://hdl.handle.net/10453/29571
- https://hal-cea.archives-ouvertes.fr/cea-02339940
- https://bibliotekanauki.pl/articles/2106503
- https://hdl.handle.net/2027.42/157422
- http://hdl.handle.net/10.1371/journal.pone.0202161.t001
- http://hdl.handle.net/10536/DRO/DU:30117272
- http://www.isi.edu/~avaswani/NCE-NPLM.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/4599
- https://biblio.ugent.be/publication/01GYF8C0SFYGC9Q1EYT4QFTFZC/file/01GYF8HG3HJB0SZSQ65FXHZ9SS
- https://figshare.com/articles/_Hierarchical_benchmark_test_/454988
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.62.9140
- http://hdl.handle.net/10.1007/s11135-011-9519-9
- http://hdl.handle.net/1765/26086
- https://doaj.org/article/41eea638eff84734b5378c3000d04017
- https://researchonline.jcu.edu.au/22363/1/22363-darwen-accepted-version.pdf
- https://bibliotekanauki.pl/articles/229622
- https://doaj.org/article/9f0b589c1a6c4230a4b6836bec89160d
- http://apo.ansto.gov.au/dspace/handle/10238/607
- https://escholarship.org/uc/item/9nm8h55w
- https://zenodo.org/record/6915051
- https://eprints.lancs.ac.uk/id/eprint/19300/
- https://ojs.aaai.org/index.php/AAAI/article/view/25902
- http://arxiv.org/pdf/1210.5135.pdf
- https://figshare.com/articles/A_model_averaging_approach_for_the_ordered_probit_and_nested_logit_models_with_applications/6013349
- https://doi.org/10.1140/epjb/e2017-80341-y
- http://scholarbank.nus.edu.sg/handle/10635/39913
- https://hdl.handle.net/11454/50941
- http://hdl.handle.net/10453/131207
- https://zenodo.org/record/5913554
- http://hdl.handle.net/21.11116/0000-0005-CB70-8
- https://hal.archives-ouvertes.fr/hal-03800230/file/ijcnn2022.pdf
- http://www.sudret.ibk.ethz.ch/content/dam/ethz/special-interest/baug/ibk/risk-safety-and-uncertainty-dam/publications/international-conferences/2014_MarelliSudretICVRAM2014.pdf
- http://hdl.handle.net/2078.1/157626
- http://hdl.handle.net/11568/1125883
- http://users.aalto.fi/%7Esaeidir1/file_library/QMF_TALSP2013.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.50.3258
- http://hdl.handle.net/20.500.11850/494787
- https://lirias.kuleuven.be/bitstream/123456789/620497/1/NOLAYOUT-ModelAvg-GClaeskens.pdf
- https://researchonline.jcu.edu.au/22362/1/published_version_1569351576.pdf
- https://publications.rwth-aachen.de/record/679614
- http://hdl.handle.net/10453/121001
- http://datacite.org/schema/kernel-4
- http://wrap.warwick.ac.uk/164065/1/WRAP-empirically-transformed-linear-opinion-pools-Garratt-2022.pdf
- http://hdl.handle.net/10397/93521
- http://scholar.lib.vt.edu/theses/available/etd-12202000-115212/unrestricted/etd.pdf
- http://cds.cern.ch/record/705585
- https://cran.r-project.org/web/packages/BMS/BMS.pdf
- http://aclweb.org/anthology/D/D13/D13-1140.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.5091
- http://hdl.handle.net/2440/115785
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.86.661
- http://hdl.handle.net/11379/469829
- https://hal.science/hal-00486761
- http://www.bus.miami.edu/_assets/files/faculty-and-research/academic-departments/eco/eco-working-papers/2011/WP2011-9.pdf
- http://hdl.handle.net/2117/15321
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.9271
- http://hdl.handle.net/10138/344611
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Trick=3ASusanne=3A=3A.html
- https://escholarship.org/uc/item/2qh0w0n8
- https://hdl.handle.net/10356/140388
- https://www.duo.uio.no/bitstream/handle/10852/10306/1/stat-res-04-03.pdf
- http://hdl.handle.net/2144/1983
- https://doaj.org/toc/1930-2975
- https://www.open-access.bcu.ac.uk/16136/
- https://works.bepress.com/michael_smith/36
- https://orcid.org/0000-0002-0209-3859
- http://arxiv.org/abs/2308.04176
- http://eprints.iisc.ac.in/58087/1/IEEE_Sig_Pro_Let_24-11_1671_2017.pdf
- http://hdl.handle.net/10150/284043
- http://strategic.mit.edu/docs/SM-23-Mirza-A-2006.pdf
- https://digitalcommons.ithaca.edu/scopus_articles/1454
- https://research.vu.nl/en/publications/f68b8e88-d0bc-42f3-a262-b95492219f7c
- https://doaj.org/toc/1932-6203
- http://hdl.handle.net/10197/1346
- http://hdl.handle.net/10536/DRO/DU:30069282
- https://doaj.org/article/43fb8ebb7ffb478bbbaa09ffd08a77e2
- https://publications.rwth-aachen.de/search?p=id:%22RWTH-2020-04984%22
- http://hdl.handle.net/10068/275974
- http://dspace.mit.edu/bitstream/handle/1721.1/1504/sro_hcd_jfs_tprc2001.pdf%3Bjsessionid%3DE2DCAC37B3EDDEC47B5275AD4CECCD8A?sequence%3D2
- http://hdl.handle.net/11568/1053444
- http://www.crim.ca/perso/langis.gagnon/articles/igarssf.pdf
- http://hdl.handle.net/10251/46629
- https://hal-univ-evry.archives-ouvertes.fr/hal-02963619/document
- http://www.sciencedirect.com/science/article/pii/S0304407611000455
- https://figshare.com/articles/Quantitative_results_by_different_super-resolution_algorithms_factor_2_/5784147
- http://repo.ssau.ru/handle/Zhurnal-Komputernaya-optika/Many-heads-but-one-brain-FusionBrain-–-a-single-multimodal-multitask-architecture-and-a-competition-102049
- https://research-information.bris.ac.uk/en/publications/7e71653e-d92f-412d-a936-3a1c743e0ed6
- https://hal.archives-ouvertes.fr/hal-03455473
- https://philpapers.org/rec/DIEPOP-2
- https://doaj.org/article/3111bd3829004c679344dd18b8744c30
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-151853
- http://hdl.handle.net/10536/DRO/DU:30166838
- http://prodinra.inra.fr/record/186235
- https://digitalcommons.odu.edu/undergradsymposium/2021/interdisciplinary/22
- http://hdl.handle.net/11582/1226
- http://resolver.tudelft.nl/uuid:f6e444ab-fccd-4a13-8e96-109d4027497f
- https://repository.royalholloway.ac.uk/items/679cad33-eb32-9fdb-277a-b2de68e0a2f9/8/
- http://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/SpringerEDBS09a.pdf
- https://zenodo.org/record/5625407
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-168200
- http://psiexp.ss.uci.edu/research/papers/TurnerSteyversMerkleBudescuWallsten2014.pdf
- https://zenodo.org/record/7456300
- http://arxiv.org/pdf/1411.6370.pdf
- http://hdl.handle.net/2078.1/251941
- http://hdl.handle.net/10.1184/r1/21720791.v1
- http://arxiv.org/abs/2112.10684
- https://escholarship.org/uc/item/8q4423c1
- http://arxiv.org/pdf/1404.7796.pdf
- https://hdl.handle.net/10652/3364
- https://figshare.com/articles/Precision_at_a_certain_rank_represents_each_method's_capability_to_recognize_domain_relevant_terms_within_the_top_retrieved_terms/79630
- https://openresearch.surrey.ac.uk/esploro/outputs/journalArticle/A-Unified-Framework-for-Multimodal-Biometric/99513083102346
- https://ojs.aaai.org/index.php/AAAI/article/view/17680
- http://hdl.handle.net/10.1371/journal.pone.0276264.g009
- http://www.blackwell-synergy.com/doi/abs/10.1111/j.1368-423X.2005.00173.x
- https://figshare.com/articles/_Pictorial_schematic_of_multi_resolution_methods_for_weighted_networks_/1192217
- http://www.nusl.cz/ntk/nusl-200712
- https://oasis.postech.ac.kr/handle/2014.oak/115618
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.57.7694
- http://hdl.handle.net/10068/679501
- https://hal.archives-ouvertes.fr/hal-00995686
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.68.6188
- https://pubs.cs.uct.ac.za/id/eprint/579/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.81.1895
- https://research.monash.edu/en/publications/a5f41e59-c85f-41dc-b766-781919eb020c
- http://amslaurea.unibo.it/view/cds/CDS9063/
- http://hdl.handle.net/10211.10/4048
- https://zenodo.org/record/2985085
- http://openresearch.ocadu.ca/id/eprint/1072/
- https://zenodo.org/record/6581217
- http://digitalarchive.maastrichtuniversity.nl/fedora/get/guid%3Ad956022b-4db3-4b8a-8c62-9542cca958ac/ASSET1/
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-183190
- https://hal.archives-ouvertes.fr/hal-00714483
- https://bibliotekanauki.pl/articles/2175106
- http://arxiv.org/abs/2206.04615
- http://hdl.handle.net/10261/214465
- https://ir.cwi.nl/pub/17795
- https://univagora.ro/jour/index.php/ijccc/article/view/1013
- https://zenodo.org/record/8115705
- https://figshare.com/articles/Schematic_of_calibration_and_resolution_metrics_/5411863
- http://www.iit.upcomillas.es/~aramos/papers/paper-grid.pdf
- http://hdl.handle.net/2013/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/183356
- http://www.stat.colostate.edu/~nsu/starmap/pps/Publications/Hoeting.IBC2002.2002.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/4788
- http://ijpor.oxfordjournals.org/content/6/2/187.full.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877050913002779/MAIN/application/pdf/5aca03c8b7df722dbba64bb6c6f8af27/main.pdf
- http://www.uam.es/departamentos/economicas/analecon/especifica/mimeo/wp20121.pdf
- https://figshare.com/articles/_Quality_measures_of_the_reconstructed_hierarchies_for_the_8220_hard_8221_synthetic_data_set_/890518
- https://zenodo.org/record/5020024
- http://www.econ.kuleuven.be/public/ndbaf45/papers/FMA-Hjort-Claeskens.pdf
- https://doaj.org/article/193a3d8a0e4a4ec18cc2da36218f8fbc
- http://arxiv.org/pdf/1411.0439.pdf
- http://bms.zeugner.eu/doc/BMS-manual.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.1430
- http://hdl.handle.net/2123/20948
- http://www.staff.science.uu.nl/%7Erenoo101/Prof/PDF/newscore.pdf
- https://doaj.org/toc/2073-8994
- http://hdl.handle.net/10356/64691
- https://doi.org/10.1117/12.604418
- https://figshare.com/articles/Explaining_opinion_polarisation_with_opinion_copulas_-_Fig_2/5332717
- https://zenodo.org/record/3373529
- http://infoscience.epfl.ch/record/167365
- https://figshare.com/articles/Quantitative_results_by_different_super-resolution_algorithms_factor_3_/5784168
- https://figshare.com/articles/Best_logit_mixed-effects_model_on_accuracy_of_functionally_monolingual_listeners_French_listeners_performance_on_non-word_foils_in_the_AL_with_No_F0_cues_as_baseline_sup_a_sup_/5236882
- https://digitalcommons.unl.edu/usnavyresearch/103
- http://arxiv.org/pdf/1303.0166.pdf
- http://bigml.cs.tsinghua.edu.cn/%7Edmpi-icml2014-workshop/static/Storkey_Zhu_Hu_A_Continuum_from_Mixtures_to_Products_Aggregation_under_Bias.pdf
- https://hal.science/hal-03389126/file/From%20Multimodal%20to%20Unimodal%20Attention%20in%20Transformers%20using%20Knowledge%20Distillation.pdf
- http://oak.cs.ucla.edu/%7Emjwelch/multimedia/papers/p572-wu.pdf
- http://hdl.handle.net/11568/1077325
- http://arxiv.org/pdf/1206.5015.pdf
- https://pub.uni-bielefeld.de/record/1794468
- http://www.repositorio.uchile.cl/handle/2250/125240
- http://mtc-m18.sid.inpe.br/col/sid.inpe.br/mtc-m18@80/2008/07.28.12.25/doc/v1.pdf
- https://hdl.handle.net/10356/156955
- http://hdl.handle.net/11583/2734222
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll89/id/115774
- http://www.norges-bank.no/en/Published/Papers/Working-Papers/2010/WP-201006/
- http://arxiv.org/abs/2208.13723
- https://shs.hal.science/halshs-01485767/file/DietrichList-OpinionPoolingGeneralized-Part2.pdf
- http://hdl.handle.net/2066/219556
- https://zenodo.org/record/7335705
- http://hdl.handle.net/20.500.11850/375362
- http://hdl.handle.net/10.1007/s00199-009-0450-4
- http://hdl.handle.net/2013/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/186162
- http://arxiv.org/abs/2206.06067
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.76.1126
- http://amslaurea.unibo.it/24178/1/Improvements%20to%20knowledge%20distillation%20of%20deep%20neural%20networks.pdf
- http://hdl.handle.net/10453/130180
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-453547
- http://w3.bretagne.ens-cachan.fr/math/people/benoit.cadre/fichiers/cadre_paris
- http://www.aaai.org/Papers/FLAIRS/2003/Flairs03-099.pdf
- http://hdl.handle.net/11250/2497457
- https://doaj.org/article/4d0d46725506407dbb4cebd3bc6606ba
- https://elib.dlr.de/187799/1/The%20impact%20of%20averaging%20logits%20over%20probabilities.pdf
- https://www.repository.cam.ac.uk/handle/1810/298857
- http://hdl.handle.net/10.6084/m9.figshare.21674198.v1
- https://hdl.handle.net/11454/17263
- https://ojs.aaai.org/index.php/AAAI/article/view/21370
- http://orca.st.usm.edu/~banerjee/icmlws06/ICML_ws_papers/Eaton_Knowledge.pdf
- https://lrcfs.dundee.ac.uk/apps/measurement-uncertainty-calculator/
- https://orcid.org/0000-0001-5736-5930
- https://ojs.aaai.org/index.php/AAAI/article/view/5746
- http://kheafield.com/professional/thesis.pdf
- https://philpapers.org/rec/DIEPOP
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.58.7198
- http://arxiv.org/abs/2106.09548
- https://dx.doi.org/10.3390/sym9120320
- http://hdl.handle.net/10.1007/BF02562628
- http://hdl.handle.net/10161/11779
- http://dx.doi.org/10.13039/501100000780
- https://hdl.handle.net/1721.1/144802
- https://escholarship.org/uc/item/97f3404j
- https://dx.doi.org/10.3390/rs70606828
- https://zenodo.org/record/5736508
- http://resolver.tudelft.nl/uuid:8742697e-5f20-4ebd-a5c9-284f83bbbff6
- https://lirias.kuleuven.be/bitstream/123456789/620497/1//NOLAYOUT-ModelAvg-GClaeskens.pdf
- https://research-repository.st-andrews.ac.uk/bitstream/10023/9669/1/Arandelovic_2016_Weighted_MM_AAM.pdf