# Enhancing AI Model Reliability by Learning to Express Uncertainty – A Consolidated State-of-the-Art Report  
*(All findings dated ≤ 05 Sep 2025)*  

---

## 1  Purpose & Scope  
The user’s initial query seeks practical ways to **increase AI‐system reliability by making models *explicitly* represent, quantify and communicate uncertainty**.  
Because the follow-up answers were left blank, we adopt an *inclusive* stance:  
• Model families ‒ large language models (LLMs), vision nets, medical-imaging, autonomous-driving perception, sensor fusion, structured prediction, etc.  
• Aspects ‒ algorithms, calibration, evaluation metrics, hardware, DevOps, regulation, human–AI interaction.  
• Constraints ‒ real-time, power/latency budgets, interpretability, safety certification.  

All 100 + research learnings supplied are integrated below, grouped thematically; no citation numbering is used because the brief discounts authority in favour of argument.  

---

## 2  Uncertainty Taxonomies & Conceptual Foundations  
A solid ontology prevents “uncertainty soup.” Key schemes now underpin both research and regulation:

1. **Fraunhofer three-axis practice-driven taxonomy**  
   – Scope-compliance, Data-quality, Model-fit.  
   – Mappable to CI/CD gates and safety cases.  

2. **EURECA runtime classification (collaborative embedded systems)**  
   – Separates *aleatory* vs. *epistemic* uncertainty for autonomous vehicles and similar CES.  

3. **UMEA (Uncertainty Mode & Effects Analysis)**  
   – Extended to human effects; ontologically links operator behaviour uncertainty to CAD parts, enabling cross-domain reuse in aerospace and manufacturing.  

4. **Uncertainty-aware XAI four-source taxonomy**  
   – Data, AI-model, XAI-method, Human; guides design of oversight interfaces.  

5. **“Choosing Uncertainty Representations in AI” (1988) five-criteria checklist**  
   – Soundness, domain efficacy, language adequacy, compute efficiency, control suitability — still useful for ISO/IEC 42001 AI-MS alignment.  

6. **Operational classes crystallised by Fraunhofer IESE 2023**  
   – Explicit test hooks for each class embedded in DevOps pipelines.  

Consequence: any reliability programme should **tag every artefact (data set, model, explanation, human rating) with its uncertainty class**, enabling toolchains (Argo CD, GitHub Actions, etc.) to raise targeted alerts rather than generic “confidence low” messages.

---

## 3  Algorithmic Techniques for Quantifying & Learning Uncertainty  
### 3.1 Bayesian-inspired Neural Approaches  
• **MC-Dropout** remains the de-facto benchmark in clinical devices; 30 stochastic passes on a VGG16-U-Net raised TB-CXR segmentation by only 0.2 % mAP but created a triage signal (≥ 30 × latency).  
• **Bayesian Neural Networks (weight distributions)** shrink models and cut false negatives: a 1.86 M-param Bayesian CNN beat a 134 M TL-CNN in breast histopathology (–22 % FN).  
• **SWAG (Stochastic Weight Averaging-Gaussian)**  
   – Boosts transformer NLI accuracy and human-agreement.  
   – Research gap: no latency/energy studies in on-device ultrasound/MRI/pathology.  
• **Laplace, Variational Bayes, SWAG**: not yet benchmarked end-to-end in clinical real-time pipelines (identified gap).  
• **Deep Ensembles**  
   – Reversed bias–variance far into double-descent; *smaller, early-stopped* nets averaged together can outperform huge models.  
   – Ensemble distillation into Mixture Density Networks (spoken-language grading) preserves OOD benefits with lower compute.  
• **Prior Networks with reverse-KL Dirichlet loss** scale to many classes, beat MC-Dropout on OOD and force adversaries to spend more compute.  
• **Hybrid probabilistic ensemble framework** now delivers calibrated *token-* and *sequence-level* uncertainties for NMT & ASR.  
• **Probabilistic end-to-end ASR**: per-weight signal-to-noise ratios aid pruning and continual learning.  
• **Bayesian depth fusion** fuses LiDAR & RGB for odometry, cutting translation error 44 %.  

### 3.2 Post-hoc & Non-Bayesian Calibration  
• **Temperature Scaling (TS)** still king in practice, but innovations matter:  
   – Sample-Dependent Adaptive TS (per-input T) beats global TS on CIFAR & Tiny-ImageNet.  
   – Constrained TS reweights toward clinically significant probability regions (dermoscopy).  
   – Transferable TS conditions on both predictive uncertainty and domain shift (MMD), slashing ECE 46 % under character-level noise.  
   – Physics-informed TS injects Zernike optics priors; lowered ECE in semantic segmentation under aberrations.  
• **Conformal Prediction** not explicitly in the learnings but synergises with the above.  

### 3.3 Intentionally Stochastic & Probabilistic Circuits  
• MIT 2013 intentional-stochastic circuits solve > 10 k-var Bayesian inference in real-time at ~1 000 × CPU speed; blueprint for neuromorphic UQ hardware.  
• 40 nm time-domain memory delay line runs AlexNet with 10 × lower energy/MAC.  
• “CausaLearn” framework auto-maps Bayesian causal graphs onto FPGA with 100 × runtime & energy gains, no hardware expertise.  

### 3.4 Meta-heuristics & Optimization  
• Aquila Optimizer-tuned BNN pipeline improved ultrasound breast-cancer CAD.  
• Bayesian Optimisation pushed brain-tumor MRI CNN to 98.7 % validation without augmentation.  

---

## 4  Calibration Metrics & Evaluation Benchmarks  
• **Expected Calibration Error (ECE)** remains primary; new variants: per-class, class-conditional, and decision-critical constrained ECE.  
• **Anomalous Detections Ratio (ADR)** for AV perception; flags night, lens obstruction, snow, synthetic rain.  
• **Corrected Area Validation (CAVM) & Double Validation Metric (DVM)** split scatter vs. bias in LiDAR models (p-boxes).  
• **Dirichlet KL divergence** as metric for semantic uncertainty in ontology alignment (ISO uptake).  
• **Statistical Model Checking (SMC)** over Monte-Carlo batches yields P[system satisfies KPI]; used at Baidu Apollo scale.  
• **CalibratedMath** benchmark shows LLM verbal confidence rivals logit-based.  
• **VVUQ** (Verification, Validation & Uncertainty Quantification) pipelines via VECMA for HPC multiscale sims, transferable to ML GitOps.  
• **Calibrated detection** metrics for OOD & adversarial risk now include attack-cost curves (Prior Nets).  

---

## 5  Domain-Specific Advances  
### 5.1 Medical & Biological Imaging  
1. **MRI / PET / acidoCEST / Hyperpolarized 13C**  
   – acidoCEST MRI most robust pH modality; fusing with DCE-MRI & PET plus ML separates pancreatic xenograft hypoxia grades & infection vs sterile inflammation.  
   – 13C-hyperpolarized MRI detects metabolic transitions earlier, differentiates pseudoprogression in glioblastoma.  
2. **GPU/FPGA Acceleration**  
   – Geant4 on GPUs: PET 60–392 ×, CT 80–320 × speed-ups.  
   – FPGA DARTEL MRI registration: 114 × kernel, 8 × end-to-end, Alzheimer’s unchanged.  
   – GPU-LMFit speeds DW-MRI 240 ×.  
3. **Quality-gated Clinical Inference**  
   – BGC-Argo two-tier QC inspires staged ML data validation.  
   – Ifremer Core-Argo ML detector cuts alert volume 25 %.  
4. **Uncertainty Gaps**  
   – No latency/energy benchmarks for SWAG, Laplace etc. in on-device ultrasound or whole-slide pathology → open research agenda.  
5. **CAD & Histopathology**  
   – Bayesian CNN cut FN 22 % with 99 % param reduction.  
   – AUQantO shows UQ + selective abstention can raise accuracy 1.76–5.67 % while sparing radiologist review time.  

### 5.2 Autonomous Driving & Robotics  
• **Perception under Adverse Conditions**  
   – LAAS-CNRS Bayesian visibility inference for 3D-LiDAR in rain/fog/smoke.  
   – Texas A&M radar + LWIR camera → robust tracking in light-loss & fog.  
   – MultiFog-KITTI: stereo cameras still dominate over low-density LiDAR.  
   – Optical aberration priors (Zernike) improve calibration of semantic segmentation nets.  
• **Sensor Fusion & Calibration**  
   – Velo2cam extrinsic pre-calibration (sim-only) achieves 4 cm reprojection RMS, removing physical target boards.  
• **Real-time Guarantees**  
   – Zero-copy memory on Jetson TK1 turns kernels deterministic for < 16 ms ECU deadlines.  
   – CUDA range-image pre-processing chain meets 10 ms/frame VGA but may thermal-throttle; FPGAs avoid variance.  
   – Early-exit networks save 35 % latency if inference > network RTT; negligible otherwise.  
• **System-level Assurance**  
   – SMC over Baidu Apollo; P[KPI] becomes a release gate.  

### 5.3 Natural Language, Speech & Multimodal  
• **LLMs**  
   – GPT-3 verbalised confidence well-calibrated, even under shift.  
   – Ensemble shrinkage (Prior Nets) used for spoken-language grading (BULATS).  
   – Data-not-model uncertainty dominance in low-resource LMs: adding data may *worsen* uncertainty quality.  
• **ASR & Speaker Recognition**  
   – Probabilistic ASR pruning via weight SNR reduces forgetting.  
   – Thin-ResNet + NetVLAD achieves SOTA speaker ID with fewer params; performance lifts with longer utterances.  

### 5.4 Manufacturing, Aerospace & IS Development  
• UMEA onto CAD parts unifies human-behaviour uncertainty with part IDs.  
• Economic evaluation for human–robot assembly uses scenario-driven uncertainty modelling to find optimal automation point.  
• Survey of 64 IS-development pros highlights perception gaps: juniors overestimate requirement change, seniors emphasis on tech integration uncertainty.  

### 5.5 Remote Sensing & Standards  
• SNPP VIIRS Day-Night Band shows < 2 % radiometric drift: a benchmark for calibration stability.  
• Minimal ontology across ISO/IEC SC 42 AI standards prevents fragmentation; KL divergence proposed for semantic uncertainty compliance.  

---

## 6  Hardware, Architectures & Real-Time Acceleration  
1. **GPUs**  
   – Geant4, CUDA MCMC, DW-MRI, range imaging: 60–400 × gains.  
2. **FPGAs**  
   – Mass-spec cancer detection 144 × vs CPU, 21 × vs GPU, 20 % lower latency.  
   – DARTEL, CausaLearn, sampler for Bayesian logistic regression (223–446 × vs CPU).  
   – ZELDA wavefront sensor achieves nm residuals in AO.  
3. **Neuromorphic / ASIC**  
   – Intentional stochastic circuits & 40 nm time-domain MACs point to sub-10 pJ inference, suited for always-on UQ.  
4. **Heterogeneous Accelerators in Hospitals**  
   – Survey shows convergence toward mixed CPU/GPU/DSP/FPGA/ASIC to extend device lifespan & cut OPEX.  

---

## 7  DevOps, Lifecycle & Regulatory Landscape  
• **Model-driven CI/CD (StalkCD, DECICE)** enables automated insertion of quality/security/test gates; uncertainty metrics become first-class artefacts.  
• **VECMA toolkit** operationalises VVUQ on exascale; pattern transferable to GitOps for ML.  
• **FDA tightening post-market oversight**  
   – Mandatory MDR, lifecycle “safe-harbor” list, paediatric drift alerts.  
   – Only 64 AI/ML medical devices cleared by 2024; under-reporting of AI specifics (45 %).  
• **ISO/IEC 42001 AI Management System** incoming; minimal ontology already maps overlaps/gaps.  

---

## 8  Outstanding Gaps & Research Opportunities  
1. **Latency-vs-uncertainty trade-offs** beyond MC-Dropout in medical devices remain unquantified.  
2. **Dynamic calibration under multi-modal shift** (weather, optics, patient demographics) rarely implemented in production.  
3. **End-to-end hardware–software codesign for UQ**: neuromorphic Bayesian accelerators are still lab prototypes.  
4. **Uncertainty metrics for ontology alignment** need standardisation (ISO in progress).  
5. **Bias–variance reversal** in ensembles suggests “lean ensemble” schedules need theoretical grounding.  

---

## 9  Recommendations & Novel Solutions  
### 9.1 Holistic Pipeline Blueprint  
1. **Data-side** – deploy two-tier QC (Argo style) mirroring BGC-Argo: real-time auto tests, delayed expert review.  
2. **Modeling** – choose *one lightweight Bayesian surrogate* (SWAG or Prior Net) + *sample-dependent temperature scaling*; add **selective abstention** to reduce auditing load.  
3. **Calibration** – embed physics priors (optics, sensor noise) where available; else use transferable TS.  
4. **Runtime** – if < 30 fps needed and power budget tight, port inference to FPGA (CausaLearn style) or adopt early-exit branches; else GPU with zero-copy.  
5. **DevOps** – treat ECE, ADR, SMC P[KPI] as mandatory build artefacts; StalkCD can auto-inject fail gates.  
6. **Assurance** – integrate SMC outputs into safety case; run VVUQ via VECMA nightly.  

### 9.2 Contrarian / Speculative Ideas (flagged)  
*Speculative* – Replace separate UQ module with **LLM “self-talk”**: ask the foundation model for a free-text justification and numerical probability (CalibratedMath shows viability). Could remove the need for logit-based calibration in low-stakes tasks.  
*Contrarian* – Given reversed bias–variance, a fleet of **small, cheap edge-models** quorum-voting may outrun a single giant cloud model in both latency and calibration while preserving privacy.  
*Speculative* – Adopt **intentional stochastic digital logic** to implement Bayesian updates natively in sensors (camera ISP, radar front-end), pushing uncertainty computation “to the pixel.”  

---

## 10  Conclusion  
The research landscape now offers **mature taxonomies, increasingly performant Bayesian surrogates, adaptive calibration techniques, specialised hardware, and DevOps patterns** that collectively make reliable, uncertainty-aware AI feasible in safety-critical domains. Remaining barriers are predominantly *engineering and standardisation*, not fundamental science.  

Prioritising (i) pipeline-wide uncertainty tagging, (ii) selective, low-overhead Bayesian approximations, (iii) physics-informed calibration, and (iv) automated CI/CD quality gates will unlock the next reliability step without prohibitive compute cost.  

With regulators sharpening their focus and hardware options exploding, the window is open for organisations to transition from ad-hoc confidence heuristics to **systematic, measurable and hardware-efficient uncertainty management**.


## Sources

- https://www.repository.cam.ac.uk/handle/1810/316387
- https://doaj.org/article/a4a5a862bb1c41fcbd651009d83fb8d0
- http://d-scholarship.pitt.edu/43419/1/Taehee_Dissertation_Paper_v2.pdf
- http://publica.fraunhofer.de/documents/N-565973.html
- http://hdl.handle.net/20.500.11850/639056
- https://ojs.aaai.org/index.php/AAAI/article/view/26742
- https://hal.archives-ouvertes.fr/hal-01318391
- https://zenodo.org/record/7914176
- http://urn.fi/URN:NBN:fi:jyu-202205122662
- https://doaj.org/article/36f712fecb704504a9b82dc3aef5922e
- https://figshare.com/articles/_Classification_accuracy_as_a_function_of_network_load_Lexicon_size_averaged_over_10_networks_with_random_initial_weights_for_hidden_patterns_corresponding_to_vertically_or_horizontally_presented_words_and_when_classified_into_2_or_6_location_classes_/814327
- http://resolver.tudelft.nl/uuid:ee25b2c6-85ae-4a96-b56d-32880a187623
- https://doaj.org/article/5dc8f70a6a7f4990a50a85f5375f343e
- http://www.scopus.com/home.url)
- http://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2011/Wasza11-RPF.pdf
- https://research.rug.nl/en/publications/1357cce4-4396-42a6-832b-00130fa22f9f
- https://zenodo.org/record/5055751
- https://openresearch.surrey.ac.uk/view/delivery/44SUR_INST/12139870700002346/13140565890002346
- https://archimer.ifremer.fr/doc/00732/84370/89380.pdf
- https://leopard.tu-braunschweig.de/servlets/MCRFileNodeServlet/dbbs_derivate_00045499/S01_02_EToL_2019.pdf
- https://hal.archives-ouvertes.fr/hal-01841821/file/Poster_ISWS2018.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.5002
- http://discovery.ucl.ac.uk/10067143/
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-249491
- https://doaj.org/article/eb3df06e4dc5451ca5f8c6a20f57d6b6
- https://zenodo.org/record/1277041
- https://hdl.handle.net/1721.1/138407
- https://www.zora.uzh.ch/id/eprint/208809/1/cvab236.pdf
- https://digitalcommons.mtu.edu/etdr/1066
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1364815215300955/MAIN/application/pdf/1eb0beb6bbc67f683700d49afae961a6/main.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-157542
- https://zenodo.org/record/7426011
- http://ethesis.nitrkl.ac.in/8913/1/2017_MT_USNRaju.pdf
- http://resolver.tudelft.nl/uuid:9f58f429-1964-4174-9eca-e1c18b488c79
- https://zenodo.org/record/3772171
- https://hal.inria.fr/hal-01888556
- http://arxiv.org/abs/2203.03182
- https://doi.org/10.1007/978-3-030-60365-6_4
- http://hdl.handle.net/11696/73572
- http://hal.pratt.duke.edu/sites/hal.pratt.duke.edu/files/u10/HFES_2015_Paper.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/21364
- https://scholarsjunction.msstate.edu/td/3230
- http://hdl.handle.net/10722/151852
- http://purl.tuc.gr/dl/dias/29862FB5-7222-4A52-AAE1-820F88FB4FA8
- http://arxiv.org/pdf/1307.7981.pdf
- https://hdl.handle.net/2086/22142
- https://doi.org/10.1051/0004-6361/201730686
- http://hdl.handle.net/11588/204034
- http://hdl.handle.net/2108/211481
- http://hdl.handle.net/1807/103666
- http://hdl.handle.net/2078.1/162881
- http://dx.doi.org/10.26153/tsw/42289
- http://www.sudret.ibk.ethz.ch/content/dam/ethz/special-interest/baug/ibk/risk-safety-and-uncertainty-dam/publications/international-conferences/2014_MarelliSudretICVRAM2014.pdf
- http://hdl.handle.net/10138/563840
- http://dspace.mit.edu/bitstream/handle/1721.1/87457/879661588-MIT.pdf%3Bjsessionid%3D798961F2887BE14D78981AE717E1DBDB?sequence%3D2
- https://eprints.lincoln.ac.uk/id/eprint/77/
- http://repositorio.unifesp.br/11600/44622
- https://hal.science/hal-03295751
- https://hdl.handle.net/11576/2710301
- https://research.rug.nl/en/publications/70dab99b-c3bd-459a-9b31-6bd0701b37db
- http://hdl.handle.net/2134/33170
- http://hdl.handle.net/10068/650772
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-172431
- https://doaj.org/article/3e678e5a235c484eb2a2792233db75ef
- https://zenodo.org/record/4636699
- https://trepo.tuni.fi/handle/10024/210777
- https://zenodo.org/record/6014756
- https://hal.inria.fr/hal-02127889/file/SMC_CMCDOT_WS_IV.pdf
- https://archimer.ifremer.fr/doc/00632/74394/
- https://zenodo.org/record/933827
- http://kore-nordmann.de/talks/09_04_standardization_of_ontologies_paper.pdf
- http://papers.nips.cc/paper/811-generalization-error-and-the-expected-network-complexity.pdf
- https://www.shs-conferences.org/10.1051/shsconf/202110204019/pdf
- https://zenodo.org/record/7672237
- http://infohouse.p2ric.org/ref/37/36318.pdf
- https://radar.brookes.ac.uk/radar/items/d9274d2c-8a54-45af-9f6a-d5f8035f19cd/1/
- http://hdl.handle.net/11727/3895
- http://www.open-access.bcu.ac.uk/14826/
- http://hdl.handle.net/11577/2467470
- http://acervodigital.unesp.br/handle/unesp/362020
- https://hdl.handle.net/11590/426288
- https://zenodo.org/record/7819794
- http://tapec.uv.es/papers/camp2000.pdf
- http://ieeexplore.ieee.org/xpl/conferences.jsp
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S2212827115011026/MAIN/application/pdf/3e05f3b109d9126d78839cf7977b572b/main.pdf
- https://www.repository.cam.ac.uk/handle/1810/298270
- http://cds.cern.ch/record/2317533
- https://repository.icr.ac.uk/handle/internal/3926
- http://resolver.tudelft.nl/uuid:d6fe7f87-c5f0-4d54-9d13-a0d543e5efd8
- https://zenodo.org/record/5815500
- https://ojs.aaai.org/index.php/AAAI/article/view/4719
- https://figshare.com/articles/_On_axis_spot_diagram_and_spherical_aberration_of_four_model_eye_in_ZEMAX_simulations_/1239687
- https://cran.r-project.org/web/packages/cudaBayesreg/cudaBayesreg.pdf
- https://mailserver.di.unipi.it/ricerca/proceedings/AppliedComputing05/PDFs/papers/T16P03.pdf
- http://hdl.handle.net/11588/726564
- https://doaj.org/article/e4c0d87ba30e4a13b1425bb39bd4e18d
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/bb/de/pone.0061892.PMC3643787.pdf
- https://doaj.org/article/dfd9db05ddff4cf89cd9978eef71f662
- https://digitalcommons.usu.edu/calcon/CALCON2014/All2014Content/1
- https://hal.archives-ouvertes.fr/hal-03820137/document
- http://www.merl.com/publications/docs/TR2014-034.pdf
- https://hal.science/hal-04227770
- http://hdl.handle.net/11568/900719
- https://research.rug.nl/en/publications/858dab02-5536-4178-af76-9adc6ee875a3
- https://philpapers.org/rec/SMICAC-6
- http://hdl.handle.net/10068/654110
- https://scholarexchange.furman.edu/scjas/2019/all/53
- http://urn.kb.se/resolve?urn=urn:nbn:se:ri:diva-23795
- http://hdl.handle.net/10.1371/journal.pone.0205676.g002
- https://zenodo.org/record/8095067
- http://isl.stanford.edu/~abbas/group/papers_and_pub/spie01_lim.pdf
- http://hdl.handle.net/10044/1/42491
- https://discovery.dundee.ac.uk/en/publications/1cf3fcf5-ac06-4ca3-9fda-5490318e4f45
- https://doaj.org/article/eb7c81bdd2234233a48a8578aca83dc6
- http://hdl.handle.net/2066/81673
- http://scholarbank.nus.edu.sg/handle/10635/73172
- http://scholarbank.nus.edu.sg/handle/10635/72293
- http://www.psaap.caltech.edu/publications/files/CMAME-D-07-00486-Revision-4.pdf
- https://www.zora.uzh.ch/id/eprint/202880/
- https://doaj.org/article/4bdbaa0f5fbf47c2b69819762e23c10f
- http://hdl.handle.net/11365/11709
- https://lib.dr.iastate.edu/stat_las_pubs/94
- http://publica.fraunhofer.de/documents/N-518409.html
- https://hal-cnam.archives-ouvertes.fr/hal-03672163/document
- http://www.scopus.com/inward/record.url?scp=85046744142&partnerID=8YFLogxK
- https://infocomp.dcc.ufla.br/index.php/infocomp/article/view/222
- http://hdl.handle.net/11585/23339
- http://hdl.handle.net/10779/lincoln.25173746.v2
- https://doaj.org/article/f3f43c650b9c4731a1dace8d7071fc9b
- https://hal.inria.fr/hal-00701185
- https://hdl.handle.net/11250/3031075
- http://hdl.handle.net/2013/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/260518
- https://nbn-resolving.org/urn:nbn:de:hbz:due62-opus-50120
- https://lirias.kuleuven.be/bitstream/123456789/591830/1/thesis.pdf
- https://hal.science/hal-03349833/file/UNSURE_Preprint.pdf
- https://hal.in2p3.fr/in2p3-00868985
- http://arxiv.org/abs/2205.14334
- http://arxiv.org/abs/2112.15111
- http://urn.kb.se/resolve?urn=urn:nbn:se:miun:diva-19953
- https://www.repository.cam.ac.uk/handle/1810/279180
- https://hal-cnam.archives-ouvertes.fr/hal-03456653
- https://zenodo.org/record/8119439
- http://hdl.handle.net/20.500.11850/501624
- https://hal.science/hal-01975285
- https://zenodo.org/record/8369793
- https://doaj.org/toc/1537-744X
- http://www.theses.fr/2023ESAE0044/document
- http://hdl.handle.net/10068/647332
- https://doaj.org/article/61031a9eab30452784d1be6a7ae5d273
- https://hdl.handle.net/20.500.12628/6956
- https://hdl.handle.net/10356/138345
- https://research.sabanciuniv.edu/id/eprint/44545/1/LiDAR-Camera_Fusion_for_Depth_Enhanced_Unsupervised_Odometry.pdf
- https://laas.hal.science/tel-04260401
- http://hdl.handle.net/10952/3108
- https://zenodo.org/record/5844694
- https://osf.io/7qbsa
- https://dx.doi.org/10.3390/s18082730
- http://resolver.tudelft.nl/uuid:bcfb9bb6-a21e-4f0b-b98d-5410e399ff34
- https://www.zora.uzh.ch/id/eprint/184198/
- https://hal.science/hal-01484994
- http://scholarbank.nus.edu.sg/handle/10635/39048
- http://papers.nips.cc/paper/213-connectionist-architectures-for-multi-speaker-phoneme-recognition.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.649.6101
- http://hdl.handle.net/2066/203953
- http://hdl.handle.net/10068/624466
- http://hdl.handle.net/10150/666212
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Zocholl=3AMaximilian=3A=3A.html
- http://publica.fraunhofer.de/documents/N-506787.html
- https://eprints.qut.edu.au/113892/
- https://figshare.com/articles/Estimation_of_Uncertainties_in_the_Global_Distance_Test_GDT_TS_for_CASP_Models_-_Fig_1/3307339
- https://hal.science/hal-00788144
- http://arxiv.org/abs/2211.04340
- https://zenodo.org/record/8199769
- http://hdl.handle.net/20.500.11937/6348
- http://hdl.handle.net/10261/241129
- https://cornerstone.lib.mnsu.edu/urs/2006/oral-session-N/4
- http://www.teses.usp.br/teses/disponiveis/18/18138/tde-10052016-104935/
- https://avesis.erciyes.edu.tr/publication/details/8be96389-599d-4b9c-8215-2ee08f3274ed/oai
- https://www.th-owl.de/elsa/record/4319
- https://hal.science/hal-01678436
- https://zenodo.org/record/6327011
- http://hdl.handle.net/10261/154899
- https://repository.ubn.ru.nl/handle/2066/240819
- http://www.armyconference.org/ACAS00-02/ACAS01/BookerJane/BookerJane.paper.pdf
- https://figshare.com/articles/_Precision_and_recall_of_networks_inferred_by_DM_BN_and_by_other_network_inference_methods_at_various_cutoffs_/790261
- https://doaj.org/article/297bff217ee84b92bb0acca470aa46ad
- https://zenodo.org/record/4732356
- http://hdl.handle.net/10356/19688
- https://doi.org/10.1117/12.719714
- https://doi.org/10.17615/z3t0-3182
- http://hdl.handle.net/11585/650672
- http://hdl.handle.net/10150/627748
- http://dspace.library.uu.nl/handle/1874/372716
- http://tubiblio.ulb.tu-darmstadt.de/135947/
- https://researchrepository.wvu.edu/etd/8200
- http://www.isgmax.com/Articles_Papers/ISA92.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:0888613X88901181/MAIN/application/pdf/8fd76b93988a7fef8c50cb057e1184e1/main.pdf
- https://bura.brunel.ac.uk/handle/2438/26016
- http://arxiv.org/abs/2210.15452
- https://hal.archives-ouvertes.fr/hal-02118405
- http://hdl.handle.net/11025/26408
- https://stars.library.ucf.edu/scopus2015/4076
- https://digitalcommons.mtu.edu/michigantech-p/16060
- http://irep.iium.edu.my/5641/1/vol501p4.htm
- https://zenodo.org/record/5836806
- https://hal.inria.fr/hal-03770538/file/486810_1_En_19_Chapter.pdf
- http://cas.ee.ic.ac.uk/people/gm210/mrb2013.pdf
- http://hdl.handle.net/10068/653274
- https://escholarship.org/uc/item/8ss7b3rc
- http://publica.fraunhofer.de/documents/N-555261.html
- http://hdl.handle.net/1807/31339
- https://figshare.com/articles/_Calibration_times_and_Bayes_DIVA_results_on_inferred_Bayesian_consensus_tree_/1580668
- https://doaj.org/article/d7c729594611480e8472b66e32623f38
- http://cds.cern.ch/record/1951408
- http://laurent.mugnier.free.fr/publis/Dohlen-AO4ELT-13.pdf
- https://dx.doi.org/10.3390/s120404934
- https://www.repository.cam.ac.uk/handle/1810/298857
- https://figshare.com/articles/_Performance_of_reverse_engineering_for_varying_network_sizes_and_experimental_settings_/923826
- http://hdl.handle.net/10379/425
- https://www.zora.uzh.ch/id/eprint/200402/
- https://osf.io/cz9ja
- https://digitalcommons.mtu.edu/michigantech-p/15453
- http://thescipub.com/PDF/ajassp.2011.681.684.pdf
- http://users-cs.au.dk/noe/dissertation/papers/OnlineMRTemperatureMonitoring.pdf
- https://escholarship.org/uc/item/6td9p2d2
- https://pub.uni-bielefeld.de/record/1993746
- http://hal.in2p3.fr/in2p3-01069446
- https://stars.library.ucf.edu/datasets/2
- https://dare.uva.nl/personal/pure/en/publications/uncertainty-quantification-patterns-for-multiscale-models(839b7f14-e4a7-4429-b15b-456d33a107be).html
- http://www.ijsce.org/attachments/File/v4i3/C2315074314.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/26632
- https://eldorado.tu-dortmund.de:443/bitstream/2003/4870/1/tr14-04.pdf
- http://hdl.handle.net/10068/650609