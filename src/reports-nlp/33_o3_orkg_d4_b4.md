# Fishing in an LLM
## Theoretically Quantifying Uncertainty with Fisher Information in Large Language Models  
*A synthetic but exhaustive synthesis of the current research landscape (as of Sept 2025).*  

---

### Executive‐level take-aways
* Fisher-information–based theory yields **tight, interpretable uncertainty guarantees** that unify frequentist Cramér-Rao, Bayesian Jeffreys priors, MDL complexity penalties, and modern PAC-Bayes C-bounds.  
* **Scalable approximations now exist**—Kronecker factorizations, low-rank inverses, SWAG weightposteriors, and non-parametric score-sampling—that bring 7 B→70 B LLMs within reach on multi-GPU clusters.  
* **Empirical evidence** (e.g.\, SWAG on SNLI/MNLI, GPT-3 verbal probabilities) shows Fisher-aligned posteriors track *subjective* ambiguity better than deterministic fine-tuning, translating directly into gains for rejection sampling, safety filters, value-of-information (VoI) decision systems and risk-aware active learning.  
* **Numerical conditioning** is the hidden blocker: 70 B-parameter FIMs are rank-deficient and ill-conditioned; regularisation, mixed precision, and block-banded Einstein summations are mandatory.  

---

## 1  Problem framing
The “Fishing in an LLM” agenda asks:  
> *Can we quantify the predictive uncertainty of a large language model directly from its Fisher Information Matrix (FIM), and can that signal drive downstream decisions (AL, rejection, safety) at modern parameter counts?*

Fisher information enters at least three levels:
1. **Local curvature** of the negative log-likelihood gives the frequentist Cramér-Rao lower bound (CRB).
2. In the Bayesian view the *Jeffreys prior* ∝ √det F acts as an Occam penalty.
3. In MDL it re-appears as the parametric complexity term.

Thus a single geometric quantity controls *variance, prior regularisation and code length*, making it a natural uncertainty proxy for LLMs.

---

## 2  Theoretical building blocks
### 2.1  Classical bounds and their modern extensions
* **Vector UCRLB & biased estimators**: Recent work generalises CRB to rank-deficient FIMs and biased estimators via Tikhonov regularisation or shrinkage [Eldar et al.; Tun 2013].  
* **Sub-matrix bounds**: Quadratic-programming methods yield fast sub-matrix CRBs for ≥10⁵-D models (iterative non-monotone CG).
* **Uniform CRB recursions**: Geometric-series (GS) and CG algorithms compute selected columns of F⁻¹ without forming F, key for 7 B-params.
* **PAC-Bayes C-bounds**: Risk of a weighted majority vote can be bounded by the first two moments of the Gibbs margin; new variance-dependent C-bounds tighten as unlabeled data grow, relevant for adapter-fusion or prompt-ensemble LLMs.
* **Information-theoretic generalisation**: Sibson mutual information and maximal leakage tail bounds complement Fisher-based variance terms, yielding non-vacuous guarantees even under heavy distribution shift.

### 2.2  Epistemic vs Aleatoric decomposition
Cross-study evidence shows that decomposing total uncertainty improves active-learning efficiency by 25–40 %; Fisher-information variance or Laplace approximations give one tractable split, Input-Clarification Ensembling another.

---

## 3  Computing the Fisher signal at scale
### 3.1  Exact gradients are impossible
70 B-param FIMs are 70 B² entries; *approximation is mandatory*.

### 3.2  Kronecker-factored curvature family
| Variant | Key idea | Extra cost vs K-FAC | Empirical outcome |
|---|---|---|---|
| K-FAC (Martens & Grosse, 2015) | Layer-wise covariances≈Kronecker | — | baseline |
| Trace-restricted K-FAC (TKFAC, AAAI-21) | Match block trace + new damping | negligible | faster CNN convergence |
| KPSVD (2023 HAL) | SVD minimises \|F − Â\|_F | < 5 % | beats K-FAC on DAEs |
| Kronecker-Factor *Optimal* Curvature (K-FOC 2023) | Rank-1 Kronecker-sum via power iter. | ≈1 extra matvec | tighter curvature |
| 3D-Shampoo / DeepSpeed | Second-order preconditioner across 3-D parallel grid | amortised | throughput ≈ SGD |

Additional HPC advances:
* **Cost-optimal Kronecker ⊗-vector kernels**: 2012 SMP algorithm uses virtual broadcast → hits communication lower bound.
* **GPU batched Kronecker kernels (<16×16)**: 285 GFLOP/s, beating cuBLAS GEMMs.
* **Spiral FFT & CFD block-tridiagonal solvers**: Kronecker remapping yields 3.6–6.5× speed-ups; lessons transfer to FIM matvecs.
* **FPGA 3D-FFT clusters**: show bandwidth-bound nature; relevant for large Kronecker matmuls.

### 3.3  Low-rank & iterative inverses
* **Tyrtyshnikov “superfast” Newton**: sub-linear inversion for two-level Toeplitz ≈ low-rank transformer FIM blocks.
* **Block-banded inverse uniqueness**: v-block band gives ≈100× faster inversions and underpins Kalman-Bucy style updates.
* **Bayesian Conjugate Gradient (BayesCG)**: interprets each CG iterate probabilistically → free covariance estimate.
* **Geometric-series / non-monotone CG recursion**: Uniform CRB without full inversion; faster convergence observed in SPECT.

### 3.4  Non-parametric & black-box estimation
Gaussian KDE + field-theory density estimator can recover FIM rows from score-function samples without back-prop access—critical for black-box closed-source models.

### 3.5  Numerical conditioning & mixed precision
Renne 2020 shows 2× step-size in 2 × 2 cosmology FIM explodes error; for 70 B LLMs we must:
* inject *sub-FP32* jitter,
* use Clark/Taufer style mixed-precision Krylov solvers (retain single-precision throughput, double-precision accuracy),
* stabilise with “matrix vibration” or trace-matching.

---

## 4  Empirical Bayesian & ensemble surrogates
* **SWAG**: On SNLI/MNLI posterior uncertainty tracks human disagreement; repeated evidence across multiple bullets.
* **Stochastic Weight Averaging–Gaussian for LLMs**: Promising but memory heavy; can be combined with K-FOC preconditioner.
* **FisherNet**: VAE variant where latent-space covariance *is* the FIM → cuts reconstruction error.
* **GPT-3 verbal probabilities**: Calibrated “90 % confident” statements show latent epistemic info is already encoded.
* **Ensemble methods** outperform single-model calibration in low-resource NLP but degrade with more data—signalling rising aleatoric share.

---

## 5  Calibration & evaluation metrics
* **Error-based calibration plots (Levi 2022)** outperform NLL / ECE on chem-ML → strong baseline for any new Fisher metric.
* **Transferable Temperature Scaling (TTS)** reduces ECE by 46 % on noisy QNLI/AG-News.
* **Variational-Bayes calibration** shrinks gap to 0.02–0.04 on patent data.
* **Max-Entropy LMs**: 32–39 % perplexity drop; ME constraints can regularise logits akin to Fisher-information penalties.
* **Posterior-calibration audits for coreference**: emphasise evaluating the *uncertainty itself*, not just accuracy.

---

## 6  Downstream decision systems
### 6.1  Active learning & rejection
* **Risk-based AL via EVPI/AL-MI**: 25–40 % fewer labels; but watch late-stage sampling bias → discriminative switch solves it.
* **Classification with rejection**: provable risk bounds; natural fit because Fisher variance gives rejection score.
* **Input-Clarification Ensembling** decomposes LLM uncertainty without retraining, mirroring Fisher epistemic/aleatoric split.

### 6.2  Value-of-Information (VoI) pipelines
* Simulation-regression VOI (reservoir Utsira CO₂) shows ML surrogates scale VoI to large domains.
* Normalised Expected Reward Ratio & mutual-information indices extend classical VOI to cost-aware sensor placement.
* Genetic algorithms optimise multi-sensor moves under asymmetric Type I/II costs → blueprint for adaptive RLHF data collection.

### 6.3  Safety filters & selective prediction
Fisher-based variance can trigger a *rejection* or a *clarification prompt*; PAC-Bayes C-bounds provide the theoretical guarantee; GPT-3 verbal confidence hints at interfacing via natural language.

---

## 7  Scaling strategy for 7 B→70 B LLMs
1. **Parallelism layout**: Use Pr×Pc grid blending model/domain & batch paral — analytic bounds show optimum is hybrid.
2. **DeepSpeed 3-D (data/pipeline/tensor) Shampoo**: matches SGD throughput; second-order is now viable.
3. **Communication minimisation**: virtual broadcast Kronecker matvec, Spiral-style tensor reordering.
4. **Numerical stability**: sub-FP32 perturbations, trace-restricted damping, mixed-precision CG.
5. **Low-rank blocks**: exploit v-block band uniqueness; integrate Tyrtyshnikov Newton for inverse updates.
6. **Black-box models**: fall back to KDE Fisher estimation; no gradients needed.

---

## 8  Research gaps & proposed contributions
1. **Tight Fisher-based selective-prediction bound for LLMs**: Combine vector UCRLB with variance C-bound; dataset-free guarantee.  
2. **K-FOC + SWAG hybrid**: Use higher-fidelity FIM approximation as SWAG prior; test on 7 B OPT-125m subset → escalate.  
3. **Non-parametric Fisher score sampler** for proprietary GPT-4: validate against verbal confidence calibration plots.  
4. **Active-learning benchmark**: Apply AL-MI vs entropy vs Fisher-trace on BEIR in retrieval-augmented LLM setting.  
5. **Mixed-precision block-band inverse kernel**: Inspired by Clark/Taufer; integrate into Triton.

---

## 9  Experimental roadmap
| Stage | Model | Data | Metric | Compute |
|---|---|---|---|---|
| POC | OPT-125 M | SNLI+small SQuAD | Levi error-calib, CRB width | 1×A100 |
| Scale-up | 7 B open-LLAMA | MNLI, BEIR | Rejection ROC, VoI gain | 8×H100 |
| Production | 70 B GPT-J derivative | Internal chat logs | Latency vs FISHER reject | 64×H100 + 3D-Shampoo |

---

## 10  Contrarian/speculative ideas
* **Hierarchical RIP compressive sensing**: Build block-sparse adapter matrices with deterministic recovery guarantees.  
* **Bayesian CG inside attention**: Treat KV retrieval as linear solve with uncertainty; propagate variance end-to-end.  
* **Energy-based Tweedie boosting for logits**: Direct loss on response; removes least-squares artefacts in low-count token regimes.  
* **Damage-sensitive actuation signals transfer**: Optimise prompt perturbations akin to SHM actuation to expose model weak spots.  
* **Kronecker-product SVD in FPGA inference** for on-device privacy-preserving Fisher analyses. *Marked speculative*.

---

## 11  Recommendations
1. **Adopt KPSVD or K-FOC as default curvature estimator**; pair with DeepSpeed Shampoo for scalability.  
2. **Use Levi error-based calibration plots** when benchmarking any Fisher-derived metric.  
3. **Integrate Fisher variance into selective-generation policy**: threshold for clarification or safe completion.  
4. **Plug VoI-style cost/benefit calculus** into data-collection loops to prioritise high-impact RLHF queries.  
5. **Maintain mixed-precision numerical hygiene**; pre-register tensors in BF16, accumulate curvature stats in FP32-dense chunks.  

---

## 12  Conclusion
All strands of modern learning theory—frequentist, Bayesian, MDL, PAC-Bayes—converge on Fisher information as the *universal currency* of parametric uncertainty.  Recent algorithmic breakthroughs (Kronecker factorizations, SWAG posteriors, mixed-precision Krylov solvers, non-parametric score sampling) dismantle the computational roadblocks that once confined Fisher analyses to small models.  When combined with principled calibration and value-of-information decision frameworks, Fisher-based signals can now drive practical workflows for active learning, safe LLM deployment, and cost-aware data acquisition at the tens-of-billion parameter scale.  The agenda is ripe: **go fishing**—the nets are finally big enough.


## Sources

- http://aclweb.org/anthology/D/D15/D15-1182.pdf
- http://www.cs.ru.nl/personal/gdal/files/gdal2013thesis.pdf
- https://hdl.handle.net/1721.1/121552
- http://d-scholarship.pitt.edu/43419/1/Taehee_Dissertation_Paper_v2.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/5946
- http://udspace.udel.edu/handle/19716/5530
- https://eprints.whiterose.ac.uk/135422/1/1-s2.0-S0022460X18305479-main.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.65.4270
- https://hal.archives-ouvertes.fr/hal-01411044
- https://hal.science/hal-03541459v7/file/PAPER.pdf
- https://escholarship.org/uc/item/3b9012zs
- https://hal.science/hal-01774837/document
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:0024379580902475/MAIN/application/pdf/11613c97061289976fa5f33803ebf186/main.pdf
- https://zenodo.org/record/3831431
- https://eprints.whiterose.ac.uk/189928/1/1-s2.0-S0888327022006124-main.pdf
- https://dx.doi.org/10.3390/e19110617
- https://lirias.kuleuven.be/handle/123456789/657714
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:0024379587901108/MAIN/application/pdf/0ad8d00628852c07a1c03ca33f4ee262/main.pdf
- https://hdl.handle.net/11511/37423
- https://orcid.org/0000-0002-9038-1622
- https://hal.inria.fr/hal-01582197
- https://escholarship.org/uc/item/5rg4q3sb
- http://publications.imp.fu-berlin.de/2823/
- http://math.bnu.edu.cn/statprob/CSPS-IMS2005/Abstracts/RobertMnatsakanov.pdf
- http://hal.inria.fr/docs/01/05/43/37/PDF/main_Cborne_multi.pdf
- http://hdl.handle.net/10453/139375
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0024379503008917/MAIN/application/pdf/916111ab424f714c91452fcbbc4af760/main.pdf
- https://zenodo.org/record/7157724
- https://hal-mines-paristech.archives-ouvertes.fr/hal-03906232
- http://arxiv.org/pdf/1005.0047.pdf
- http://ijseat.com/index.php/ijseat/article/view/106
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.57.8466
- https://lib.dr.iastate.edu/qnde/2016/abstracts/191
- https://research.tue.nl/en/publications/4c458387-9335-49b8-9bb0-8a1d0e62d9dc
- http://www.ele.uri.edu/faculty/kay/New
- http://hdl.handle.net/10068/649670
- http://www.capsl.udel.edu/pub/doc/memos/memo081.pdf
- www.duo.uio.no:10852/70337
- http://nlp.nju.edu.cn/zhaoyg/Papers/ijcnlp2011.pdf
- http://eprints.lse.ac.uk/35495/
- https://digitalcommons.kean.edu/keanpublications/2343
- http://www.cs.iit.edu/~ml/pdfs/sharma-icdm13.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.72.8232
- https://juser.fz-juelich.de/record/860333
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0022247X11003192/MAIN/application/pdf/fe9fe82ee629a2fa507322031498eaa4/main.pdf
- http://hdl.handle.net/10138/563840
- https://doaj.org/toc/1875-9203
- https://figshare.com/articles/_Fisher_information_fit_for_one_object_/1293202
- https://hal.archives-ouvertes.fr/hal-03764630/document
- http://hdl.handle.net/2434/141718
- http://arxiv.org/abs/2311.08718
- https://hal.archives-ouvertes.fr/hal-01484994
- http://hdl.handle.net/10251/63537
- http://hdl.handle.net/11568/962595
- http://scholarbank.nus.edu.sg/handle/10635/84719
- https://lirias.kuleuven.be/bitstream/123456789/121090/1/KBI_0610.pdf
- http://homepages.vub.ac.be/%7Eimarkovs/mtns-special-session.pdf
- http://www.dmargineantu.net/workshop/BudgetedLearning_ICML-2010/blicml2010_AttenbergProvost_7.pdf
- https://ojs.aaai.org/index.php/aimagazine/article/view/4812
- http://static.googleusercontent.com/media/research.google.com/en/us/pubs/archive/41880.pdf
- http://webee.technion.ac.il/people/YoninaEldar/Info/sing-fim.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.67.3460
- https://doaj.org/article/bcaf88176072420fbac17385f082f6f6
- https://hal.archives-ouvertes.fr/hal-03784295
- https://zenodo.org/record/2611401
- http://hdl.handle.net/20.500.11850/615331
- http://hdl.handle.net/21.11116/0000-0004-CB68-3
- http://arxiv.org/abs/2008.03225
- http://www.ddm.org/dd24/home.html
- http://arxiv.org/pdf/1408.1336.pdf
- https://hdl.handle.net/11250/2680263
- http://www.math.uni-magdeburg.de/institute/imst/ag_schwabe/preprints/2009_28.pdf
- http://d-scholarship.pitt.edu/44738/
- http://hdl.handle.net/2117/334049
- http://nbn-resolving.de/urn:nbn:de:bsz:352-2-1bk1kceuhte259
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0024379503007237/MAIN/application/pdf/e736ed7d41274d8b0e6dade5cb1b2bfd/main.pdf
- https://zenodo.org/record/7766942
- http://repository.hanyang.ac.kr/handle/20.500.11754/81767
- http://www.cmpe.boun.edu.tr/~cemgil/papers/dikmen-cemgil-tr596.pdf
- http://hdl.handle.net/11392/1210207
- https://ojs.aaai.org/index.php/AAAI/article/view/4719
- http://www.eleceng.adelaide.edu.au/personal/dabbott/publications/PLO_duan2012.pdf
- http://hdl.handle.net/11562/342883
- https://lirias.kuleuven.be/handle/123456789/310163
- https://ojs.aaai.org/index.php/AAAI/article/view/16920
- https://hal.science/hal-04266143
- https://doi.org/10.24355/dbbs.084-200901220100-9
- https://escholarship.org/uc/item/8s02j324
- https://figshare.com/articles/_The_average_precision_for_active_learning_versus_most_confident_MC_prediction_selection_/1633563
- http://www.cnel.ufl.edu/files/1114101712.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-65855
- http://hdl.handle.net/2440/73883
- http://hdl.handle.net/2078.1/244222
- http://arxiv.org/abs/2202.07537
- http://hdl.handle.net/2142/106140
- http://hdl.handle.net/10068/650540
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0024379507002182/MAIN/application/pdf/676026fcea42bc067c1007254113223d/main.pdf
- http://dx.doi.org/10.1111/j.1365-2966.2011.20166.x
- https://escholarship.org/uc/item/1gw7j701
- https://hdl.handle.net/11250/3021029
- https://hal.science/hal-01258816/file/ml_sm_boost_rev.pdf
- https://zenodo.org/record/7611955
- http://informs-sim.org/wsc09papers/140.pdf
- http://infoscience.epfl.ch/record/279608
- http://hdl.handle.net/2108/216272
- https://resolver.caltech.edu/CaltechAUTHORS:20190328-113742589
- https://doaj.org/article/ed0651e907dd46c78f2bfbd9571ea303
- http://infoscience.epfl.ch/record/222443
- http://www.wseas.us/e-library/conferences/2005brazil/papers/494-180.pdf
- https://doaj.org/toc/2077-4303
- https://dare.uva.nl/personal/pure/en/publications/a-tutorial-on-fisher-information(d6d6b40d-d69f-4de4-88a9-dfc38f389e50).html
- http://arxiv.org/abs/2201.02555
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.51.446
- http://hdl.handle.net/11588/732806
- http://hdl.handle.net/1773/35582
- https://who.rocq.inria.fr/Laura.Grigori/Slides_teaching/lecture16_SparseIterativeSolvers_Grigori.pdf
- http://hdl.handle.net/21.11116/0000-0005-D558-8
- https://zenodo.org/record/3381524
- http://jim.sagepub.com/content/20/11/1307.full.pdf
- https://doaj.org/article/a7869c1781b14b37b9a1df4689b6a646
- http://www.eurasip.org/Proceedings/Eusipco/Eusipco2004/defevent/papers/cr1065.pdf
- https://hdl.handle.net/11311/1227355
- http://www.inm.ras.ru/library/Tyrtyshnikov/biblio/verynewtensor1.pdf
- http://arxiv.org/abs/2205.14334
- http://www.cs.toronto.edu/%7Ersalakhu/papers/FANG.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.55.7169
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.85.3807
- http://hdl.handle.net/10068/650029
- http://search.ieice.org/index.html
- https://ojs.aaai.org/index.php/AAAI/article/view/4514
- https://corescholar.libraries.wright.edu/knoesis/279
- http://hdl.handle.net/21.11116/0000-0009-CEFC-4
- http://hdl.handle.net/1807/33324
- https://doaj.org/article/dea10fae0f6a44f3b513b11cd37d7885
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.5.6158
- https://monarch.qucosa.de/api/qucosa%3A19727/attachment/ATT-1/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.87.5287
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.92.9504
- https://www.esaim-proc.org/10.1051/proc/202373218/pdf
- http://sumo.intec.ugent.be/sites/sumo/files/2013_09__IEEE_Africon.pdf
- http://hdl.handle.net/10068/649642
- https://hdl.handle.net/11250/3017317
- https://research.rug.nl/en/publications/active-learning-for-reducing-labeling-effort-in-text-classification-tasks(eb1680e7-3660-4f67-8bbc-c353df2757f2).html
- https://zenodo.org/record/8316324
- http://arxiv.org/pdf/1302.2686.pdf
- http://gateway.proquest.com/openurl?url_ver=Z39.88-2004&rft_val_fmt=info:ofi/fmt:kev:mtx:dissertation&res_dat=xri:pqm&rft_dat=xri:pqdiss:9513498
- https://biblio.ugent.be/publication/792704/file/1137969
- https://eprints.whiterose.ac.uk/id/eprint/180703/1/RBAL_JP.pdf
- https://hal.inria.fr/hal-03278470
- http://hdl.handle.net/10068/649256
- http://hdl.handle.net/10072/381813
- https://hal.science/hal-02905949
- http://www.cs.toronto.edu/%7Ecmaddis/pubs/nsc.pdf
- http://ir.lib.ntnu.edu.tw/ir/handle/309250000Q/17952
- https://zenodo.org/record/1300775
- http://lup.lub.lu.se/student-papers/record/8969562
- https://eprints.qut.edu.au/43936/
- http://www.iro.umontreal.ca/%7Efoster/papers/ce-acmtlsp06.pdf
- http://hdl.handle.net/2027.42/85950
- https://hal.archives-ouvertes.fr/hal-03654923/file/ECCOMAS_2022_Wackers_et_al.pdf
- http://infoscience.epfl.ch/record/287973
- http://hdl.handle.net/11393/291218
- http://www.scopus.com/inward/record.url?scp=61849185858&partnerID=8YFLogxK
- http://eprints.iisc.ac.in/45995/
- http://hdl.handle.net/2440/73114
- http://www.csie.ntu.edu.tw/%7Ehtlin/paper/doc/activehint.pdf
- https://hal.archives-ouvertes.fr/hal-00575979
- https://eprints.lancs.ac.uk/id/eprint/133042/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.72.4098
- https://figshare.com/articles/_Fisher_information_estimates_for_the_general_case_of_a_decoder_trained_and_tested_on_different_response_statistics_/1432553
- http://arxiv.org/pdf/1310.5438.pdf
- http://hal.in2p3.fr/in2p3-00702588
- https://hal.archives-ouvertes.fr/hal-01110393
- http://hdl.handle.net/11349/28724
- http://www.sciencedirect.com/science/article/B6V1D-47N61TW-6J/2/fed025c3c388f811d21786df398d5682
- http://hdl.handle.net/10.1371/journal.pone.0205355.t010
- http://arxiv.org/abs/2210.15452
- https://repository.upenn.edu/dissertations/AAI9840230
- http://dspace.wul.waseda.ac.jp/dspace/bitstream/2065/34465/1/20.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.76.1126
- http://hdl.handle.net/11585/787053
- https://hdl.handle.net/11250/2982079
- http://faculty.chicagobooth.edu/workshops/econometrics/past/pdf/Calvet.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:ri:diva-23722
- https://ieeexplore.ieee.org/abstract/document/8651970
- https://ojs.aaai.org/index.php/AAAI/article/view/16921
- https://escholarship.org/uc/item/9hv9327j
- http://hdl.handle.net/10.1184/r1/6603032.v1
- http://hdl.handle.net/10.6084/m9.figshare.7122788.v2
- https://elib.dlr.de/145806/1/Kronecker_Factored_Optimal_Curvature.pdf
- http://www.nvidia.com/content/gtc/posters/44_clark__mixed_precision_gpu_krylov_solver.pdf
- http://www-rohan.sdsu.edu/~gawron/mt_plus/readings/max_ent/me_smt_och_acl02.pdf
- https://figshare.com/articles/_Fisher_information_estimates_when_ignoring_correlations_/1432555
- https://escholarship.org/uc/item/6td9p2d2
- http://www.loc.gov/mods/v3
- https://doi.org/10.1023/A:1025785432765
- http://arxiv.org/pdf/1304.7054.pdf
- https://hal.archives-ouvertes.fr/hal-02311104
- https://figshare.com/articles/FFTS_with_near-optimal_memory_access_through_block_data_layouts/6468803
- https://figshare.com/articles/_Fisher_information_estimates_for_an_independent_population_/1432554
- https://ojs.aaai.org/index.php/AAAI/article/view/26632
- https://2021.ecmlpkdd.org/
- https://hal.inria.fr/hal-01581090
- http://ir.iscas.ac.cn/handle/311060/16959
- http://hdl.handle.net/11568/962621