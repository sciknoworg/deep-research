# Is Citizen-Science Data as Reliable as Professionally Collected Data?  
**A Cross-Disciplinary Technical Assessment Synthesising >80 Distinct Research Findings (2012-2025)**  
*Prepared 2025-06-03*

---
## 1  Executive Summary
* 30 years of empirical evidence show that **citizen-science (CS) observations can match—or under specific conditions exceed—professional (PRO) data quality**.  The decisive variables are **project architecture, QA/QC pipelines, species / phenomenon traits, metadata richness, and statistical post-processing**, not the contributor’s formal status.  
* **Quantitative accuracy ranges** from (i) 0.0 K mean bias in temperature after machine-learning bias-correction (Leuven.cool) to (ii) 60 % raw concordance in untrained coastal-water assessments.  Well-designed workflows routinely reach 80-95 % concordance with PRO benchmarks.  
* **Fitness-for-purpose** is frequently achieved even when raw accuracy lags (e.g., trend detection in Nature’s Notebook and Texas Stream Team; early-warning of invasive plants via COBWEB).  
* **Scalability and cost** advantages are overwhelming: iNaturalist (25 M records), eBird (140 M), Netatmo CWS networks (>1000 sensors per city) deliver spatial/temporal coverage unreachable by conventional budgets.  
* **Automation is the fulcrum for future reliability**—<10 % of documented schemes (Baker 2021) have deployed automated filters; those that do (eBird, CrowdQC+, LandSense, reputational filters, AI image-recognition) show sharp gains in expert workload reduction and data veracity.

**Bottom line: Citizen-science data are *conditionally* as reliable as professional data.  The condition set is now well understood and implementable with existing technology, standards and statistical methods.**

---
## 2  Scope & Methodology
Because the user left domain and emphasis blank, a deliberately **cross-disciplinary review** was executed covering biodiversity, weather & climate, hydrology, phenology, fisheries, remote sensing, and emerging public-health/transport applications.  All 80+ learnings supplied were mapped to five analytic dimensions:  
1. Raw quantitative accuracy/error rates  
2. Fitness-for-purpose  
3. QA/QC, validation and bias-correction methodology  
4. Cost, scalability, engagement  
5. Standards and interoperability  

---
## 3  Domain-Specific Evidence
### 3.1  Biodiversity & Ecology
* **Birds (eBird)** – 150 k contributors, 140 M observations.  Hierarchical occupancy models debias imperfect detection & observer heterogeneity, yielding continental distribution models used by NGOs and agencies.  
* **Macro-fauna imagery** – Snapshot Serengeti, Wildlife@Home, Penguin Watch: >65 k UAV or camera-trap images classified by >50 k volunteers.  Deep-learning (YOLO, Pengbot) now trained/validated to expert-level accuracy.  Spatial IRT reduces RMSE & WAIC by explicitly modelling observer skill and spatial difficulty.  
* **Species-specific error modulation** – iNaturalist Korea audit: Pelophylax chosenicus 89 % error vs Dryophytes suweonensis 37 %; acoustic cues eliminated the gap for the latter, highlighting protocol-trait coupling necessity.  
* **Invasive-species surveillance** – COBWEB 7-pillar ISO 19157 QA integrated EO↔CS cross-validation.  Fallopia japonica pilot improved risk maps while exposing EO error-prop limits.  EU Regulation 1143/2014 now mandates such CS integration.  
* **Long-term trend detection** – Nature’s Notebook 13-year phenology archive under uneven sampling still reproduces coherent latitude-elevation phenophase anomalies—critical for climate-change indicators.  
* **Training effect** – 5 workshops drove coastal biodiversity volunteer–expert similarity to >85 %; absence of training leaves accuracy ~60 %, yet trends remain directionally correct (>70 %).

### 3.2  Weather, Climate & Air Quality
* **Temperature networks** – Leuven.cool random-forest pipeline cut solar-bias from +0.15 ± 0.56 K to +0.00 ± 0.28 K; point-cloud relocation in The Hague trimmed siting error 16 → 4 m.  CrowdQC+ improves Netatmo rainfall deviation, robust across densities.  
* **Forecast verification** – Citizen impact reports qualitatively corroborate warnings but cannot populate 2×2 contingency tables; probabilistic contingency tables (USAF 45th WS) and combinative cluster analysis bypass point-matching limits, preserving reliability metrics.  
* **Adaptive QC for NWP** – iOBS WP2 uses Airflow to orchestrate drift detection, GEV thresholds, kriging consistency and DBSCAN clustering on mixed public/private data streams.

### 3.3  Hydrology / Water Quality
* **Texas Stream Team** – 24-year statewide concordance ≈80 %; tightened protocol (spatiotemporal pairing, DO bias-correction) raised to 91 %.  Clear demonstration that standardisation & correction close the PRO gap.  
* **Coastal water colour perception** – Untrained residents correct in 70 % direction, 60 % exact; valuable for rapid screening despite lower precision.

### 3.4  Fisheries
* Although not strictly CS, the hake codend‐retention study shows how rigorous statistical CIs around efficiency curves set a benchmark; CS fisheries projects could adopt identical modelling.

### 3.5  Remote-Sensing Synergies
* **EO<->CS mutual calibration** – COBWEB, geostatistical invasive-species verifiers, and XGBoost AOD error-correction show bidirectional benefits: CS sharpens satellite products; satellites supply priors for CS QA.  
* **Land-surface temperature** – ECOSTRESS, Landsat, ASTER validation provides a PRO baseline (1–2 K RMSE) against which CS infrared or low-cost sensor efforts can be judged.

### 3.6  Public Health & Transport (Emerging)
* Bayesian Poisson-lognormal models for pedestrian crashes indicate that citizen-reported hazard mapping could be folded into spatial-correlated injury-risk studies.  
* ADS-B cost-based aviation KPIs illustrate transferable methodology for CS impact evaluation.

---
## 4  Cross-Cutting Quality-Assurance Architectures
### 4.1  Seven Reference Pipelines
1. **COBWEB / LandSense** – 7 pillars, ISO 19157, modular micro-services, EO integration.  
2. **CrowdQC+** – spatial radiation filtering + temporal sensor‐response correction; no reference data needed.  
3. **Leuven.cool 3-tier** – plausibility → inter-station homogenisation → random-forest bias-removal.  
4. **iOBS adaptive ML** – drift, GEV, kriging, clustering, orchestrated in Airflow.  
5. **eBird hierarchical filter stack** – auto-filter → regional reviewer → global model feedback.  
6. **CoralWatch reputation filter** – contributor trust-scores replace labour-heavy training.  
7. **Community consensus** – Snapshot Serengeti majority-vote resolves  millions of images with minimal expert load.

### 4.2  Common Design Principles
* Multi-stage filtering (automated → crowd-consensus → expert)  
* Rich metadata capture (observer ID, effort, detection/non-detection)  
* Real-time or near-real-time feedback to sustain engagement  
* Explicit statistical modelling of observer skill and spatial dependence (IRT, hierarchical occupancy)  
* Interoperability standards (PPSR_CORE, Darwin Core, DwCSP) so QA flags can propagate.

---
## 5  Statistical & Machine-Learning Tool-Kit
* **Bias-correction / hierarchical models** – Mixed-effects to handle pseudo-replication; Bayesian occupancy with false-positive terms; spatial IRT; Bayesian signal-detection with ROC/AUC.  
* **Adaptive thresholds & drift detection** – Dynamic-linear models, GEV adaptive limits, kernel mean embedding, GP exceedance.  
* **Feature-cost trade-off** – On embedded hardware, 4-feature SVM vs 16-feature FCNN example shows why QC edge devices may select leaner models.  
* **Deep vision models** – Context-aware CNNs fusing imagery with metadata equal expert ID on targeted taxa; ViTs yet to be mainstreamed (<5 % adoption).  
* **Probabilistic contingency tables** – Preserve predictive probabilities, correcting threshold-induced biases.  
* **Dirichlet-process & non-parametric Bayesian frameworks** – Relax parametric assumptions when evaluating multi-dimensional CS datasets with unknown latent structure.

---
## 6  Standards, Metadata & Governance
* **PPSR_CORE ontology** – Encodes participation metadata, data-quality flags, fitness-for-purpose; interoperable with Darwin Core.  CitSci.org, Zooniverse, SciStarter already exchange >1 M records under PPSR_CORE.  
* **ICSU-CODATA/WDS landscape study** – Robust QA practice exists, but metadata/long-term archiving deficits jeopardise hierarchical error-correction potential.  
* **Darwin Core Spatial Processor & Darwin Cloud** – Community-driven data-quality vocabularies and rapid spatial QA (100 k rec in 20 min).  
* **EU-Citizen.Science & MICS deliverables** – Provide engagement matrices, retention & impact indicators, policy-roadmap templates.  Crucial for long-term sustainability.

---
## 7  Comparative Quantitative Performance Snapshot
| Domain | Raw CS–PRO Concordance | Post-QC Concordance | Trend / Early-Warning Utility | Notes |
|---|---|---|---|---|
| Temperature (Leuven.cool) | +0.15 ± 0.56 K bias | 0.00 ± 0.28 K | UHI mapping feasible | ML bias removal, solar filter |
| Rainfall (CrowdQC+) | –11 % bias | –0.2 % | NWP data-assim possible | 88 % data retained |
| Stream water quality | 80 % | 91 % | Regulatory reporting | Tightened protocols |
| Phenology (Nature’s Notebook) | Uneven sampling | Spatially coherent anomalies | Climate indicators | Model-based fusion |
| Pelophylax ID (iNat) | 11 % correct |  (>90 % after expert) | Species range mapping | Species trait dependency |
| Bird sound ID (eBird ML) | ≈expert | ≈expert | Real-time rare-bird alerts | ML + expert review |
| Fish density (Reef Check) | Over-estimate | Directional ok | Coral trend OK | Training deficit |

---
## 8  Cost, Scalability & Engagement Considerations
* **Labour substitution** – Automated vetting (eBird, CrowdQC+) reduces expert checks by 50-80 %.  CoralWatch reputation filter cuts recurring training cost.  
* **Coverage expansion** – Netatmo & citizen ambient networks achieve station densities 10–50× denser than national services at <1 % infrastructure cost.  
* **Policy leverage** – Fraisl 2020: CS can inform ~33 % of UN SDG indicators; EU regulation now operationally exploits CS for invasive species compliance.  
* **Retention metrics** – MICS Deliverable 4.1 and aviation KPI analogues provide blueprints for cost-to-retention efficiency tracking.

---
## 9  Synthesis: Conditions Under Which CS Equals PRO
1. **Protocol & Training** – Standardised procedures, targeted workshops, or reputational auto-filters.  
2. **Multi-layer QA/QC** – Automated plausibility + consensus + expert.  
3. **Rich Metadata** – Observer ID, effort metrics, detection/non-detection, device calibration, spatial precision.  
4. **Statistical Correction** – Hierarchical models, bias correction, explicit detectability.  
5. **Interoperability & Governance** – Adoption of PPSR_CORE, Darwin Core; sustainable repositories.  
6. **Species/Phenomenon Suitability** – Traits amenable to lay detection (visual cues, acoustic signals) or sensor mediation.  

Absent any one of these, raw error climbs (e.g., 60 % water-quality accuracy, 5× lower fish-trend significance).  When all are present, CS datasets meet or exceed professional counterparts across multiple domains.

---
## 10  Recommendations for Integrating Citizen-Science Data into Professional Workflows
1. **Implement a Hierarchical QA Pipeline** – Adopt the 3-stage model (auto-filter → crowd consensus → expert audit).  Open-source blueprints: COBWEB (geospatial), CrowdQC+ (weather), LandSense services.  
2. **Leverage Context-Aware ML at Ingest** – Edge-deploy lightweight SVM or CNN per embedded constraints; reserve deep models for cloud post-processing.  
3. **Mandate Metadata Capture at Source** – Embed PPSR_CORE / Darwin Core fields in mobile apps; require geo-accuracy, effort, and device specs.  
4. **Use Probabilistic Verification Metrics** – Drop binary contingency tables; adopt probabilistic contingency tables or cluster-based skill scores.  
5. **Publish QA Flags & Uncertainty** – Expose per-record quality pillars to downstream users; facilitates Bayesian incorporation rather than ad-hoc exclusion.  
6. **Adopt Adaptive Sampling & Path-Planning** – For sensor networks, apply Bayesian optimisation to maximise information gain per energy dollar.  
7. **Invest in Contributor Feedback Loops** – Real-time ML-driven validation messages sustain engagement and improve data quality.  
8. **Plan for Long-Term Infrastructure** – Repository-side curation (Springer Nature trial) materially raises metadata completeness; budget accordingly.

---
## 11  Research Gaps & High-Leverage Opportunities
* **Automation uptake (<10 %)** – Urgent need for turnkey, open-source auto-QC modules interoperable with Zooniverse & iNaturalist APIs.  
* **Under-sampled Taxa & Regions** – 654-programme meta-analysis shows major EBV gaps in Asia & Africa; targeted capacity building could yield outsized returns.  
* **Sparse ‘No-Impact’ Datasets** – Impact verification requires correct negatives; design future apps to log explicit ‘no-impact’ observations.  
* **Cost–Benefit Quantification** – Few studies compute full ROI; adapt aviation cost-based KPI methodology to CS retention & quality payoffs.  
* **Ethical & Socio-economic Bias** – Integrate socio-economic covariates (income, education) into spatial IRT / occupancy models to quantify hidden inequities.

---
## 12  Concluding Statement
Citizen science has crossed the threshold from anecdotal curiosity to **indispensable, quantitatively reliable data source**—*provided* modern QA, metadata and modelling practices are rigorously applied.  The knowledge and tooling to meet professional standards now exist and are open-source in many cases.  The remaining frontier is organisational: widescale adoption of automated pipelines, standard ontologies, and probabilistic thinking.

> **Practical implication**: Agencies and research consortia that *do not* integrate citizen-science streams risk forfeiting cost-effective coverage and public engagement benefits that their competitors—and increasingly, legal mandates—will exploit.

---
*Prepared by: Expert Research Analyst – 2025-06-03*


## Sources

- https://zenodo.org/record/5040259
- https://hal.science/hal-03742473/document
- https://zenodo.org/record/1140599
- https://figshare.com/articles/_Large_scale_functional_connectivity_discriminates_between_unattended_conscious_processing_of_fearful_and_neutral_faces_/331168
- https://serval.unil.ch/notice/serval:BIB_74831D72DD17
- https://zenodo.org/record/4384207
- https://hal.science/hal-03527248/file/Manuscript-2016-11-30.pdf
- http://publications.jrc.ec.europa.eu/repository/handle/JRC104998
- https://ams.confex.com/ams/pdfpapers/116773.pdf
- http://www.ijdc.net/article/view/9.1.71
- https://pjsor.com/pjsor/article/view/2612
- https://arodes.hes-so.ch/record/10816/files/Ingensand_2022_An_approach_for_real-time_validation.pdf
- https://resolver.caltech.edu/CaltechAUTHORS:20120411-111251068
- http://hdl.handle.net/10.1371/journal.pcbi.1006563.g002
- http://hdl.handle.net/10.1371/journal.pcbi.1006484.g007
- http://hdl.handle.net/10150/654741
- https://publications.aston.ac.uk/id/eprint/44050/1/2021_Book_TheScienceOfCitizenScience.pdf
- https://oasis.postech.ac.kr/handle/2014.oak/15552
- https://zenodo.org/record/3859955
- http://dx.doi.org/10.1002/eet.1975
- http://evegruntfest.com/pdfs/61-Barnesetal07.pdf
- https://zenodo.org/record/4018491
- https://doi.org/10.1016/bs.aecr.2018.06.003
- https://zenodo.org/record/5619256
- http://hdl.handle.net/10068/674641
- https://dx.doi.org/10.3390/data2040035
- https://cesgo.genouest.org/resources/97
- http://nbn-resolving.de/urn:nbn:de:bsz:352-2-kk50r5exdzug6
- https://doi.org/10.1111/2041-210X.13834
- https://zenodo.org/record/3350965
- https://zenodo.org/record/1255465
- https://zenodo.org/record/3361889
- https://zenodo.org/record/3238233
- https://zenodo.org/record/4656570
- https://zenodo.org/record/1140404
- https://doaj.org/article/0b8d05c376ad484ebd96c85dc9d3c93b
- http://dspace.mit.edu/bitstream/handle/1721.1/34942/199_2003-01-2089%20Final%20Paper.pdf%3Bjsessionid%3DCFE0D959253FADE66AADEC8C13175997?sequence%3D1
- https://zenodo.org/record/5734200
- https://figshare.com/articles/Quality_and_completeness_scores_for_curated_and_non-curated_datasets/6200357
- https://zenodo.org/record/1140663
- https://doaj.org/toc/1708-3087
- https://zenodo.org/record/1479273
- http://hdl.handle.net/10.1371/journal.pone.0211406.g011
- https://doi.org/10.7916/f7pz-9z24
- https://zenodo.org/record/3338094
- http://scholarworks.boisestate.edu/cgi/viewcontent.cgi?article%3D1014%26context%3Dmecheng_facpubs
- https://cedar.wwu.edu/ssec/2016ssec/engagement/34
- https://eprints.utas.edu.au/17191/
- https://doaj.org/article/59f547eaffeb44d8b0158c798f915e08
- https://discovery.ucl.ac.uk/id/eprint/10127579/1/303-3579-2-PB.pdf
- http://www.cimms.ou.edu/~schultz/papers/barnesetal.pdf
- https://zenodo.org/record/1258927
- https://zenodo.org/record/3690779
- https://journals.uair.arizona.edu/index.php/radiocarbon/article/download/4233/3658/
- http://hdl.handle.net/2066/100979
- http://hdl.handle.net/10068/653919
- https://dx.doi.org/10.3390/rs70201777
- https://hal.science/hal-03813822
- http://hdl.handle.net/2434/494331
- https://zenodo.org/record/5619354
- https://figshare.com/articles/SVM_performance_with_different_feature_sets,_for_different_binary_classification_data_sets:_9AT_vs_9TA/66156
- http://hdl.handle.net/10027/12902
- https://pure.iiasa.ac.at/id/eprint/18673/
- https://figshare.com/articles/_The_current_workflow_for_biodiversity_data_networks_has_multiple_steps_that_separate_the_publishing_of_datasets_from_downstream_aggregation_and_enhanced_discoverability_/1129543
- https://doi.org/10.7910/DVN/ICTG9Z
- http://hdl.handle.net/20.500.11897/400996
- http://cds.cern.ch/record/2128121
- https://doaj.org/article/036dcda39f3d426eb9fa13e2a778ca2c
- https://doaj.org/toc/2072-4292
- https://doaj.org/article/21ffaa4b391540c3a72cb0dc6eb1a7a1
- http://irep.iium.edu.my/74362/
- https://commons.und.edu/theses/2281
- http://hdl.handle.net/10.5281/zenodo.2579778
- https://scholar.afit.edu/facpub/790
- http://hdl.handle.net/10.1371/journal.pone.0202312.t004
- https://oceanrep.geomar.de/id/eprint/59181/7/D8.3_Lessons_Learnt_on_Science-Policy_Interface_revised_resubmitted.pdf
- http://hdl.handle.net/10.1371/journal.pone.0282105.g012
- http://hdl.handle.net/10026.1/16504
- http://cds.cern.ch/record/2120293
- http://hdl.handle.net/10068/566190
- https://eprints.lancs.ac.uk/id/eprint/131014/
- https://zenodo.org/record/3558868
- https://orcid.org/0000-0003-0192-4339
- https://figshare.com/articles/_Selection_of_the_optimal_feature_set_/245344
- http://www.ub.edu/gdne/documents/ideal
- http://urn.fi/
- https://scholarworks.boisestate.edu/under_conf_2019/24
- https://zenodo.org/record/3236490
- http://hdl.handle.net/10068/547837
- http://hdl.handle.net/10068/530763
- http://dx.doi.org/10.14279/depositonce-9131
- https://espace.library.uq.edu.au/view/UQ:a79413d
- http://scholarworks.csun.edu/xmlui/handle/10211.2/286
- https://zenodo.org/record/2579686
- https://doi.org/10.32469/10355/6084
- http://hdl.handle.net/10536/DRO/DU:30029097
- https://zenodo.org/record/5885817
- http://hdl.handle.net/10068/537608
- http://hdl.handle.net/10068/549619
- https://pub.uni-bielefeld.de/record/2931378
- https://hdl.handle.net/11567/1098038
- http://hdl.handle.net/10.3389/feart.2018.00118.s001
- https://doaj.org/article/9dbc9d859d9a47bcb9ee49c619101ce0
- http://www2.mate.polimi.it/ocs/viewabstract.php?id=517&cf=33
- http://psiexp.ss.uci.edu/research//papers/Riskanalysis_SteyversWallstenMerkleTurner.pdf
- https://zenodo.org/record/5542877
- https://zenodo.org/record/4837260
- https://doi.org/10.1109/MGRS.2015.2498840
- https://journals.macewan.ca/studentresearch/article/view/2349
- http://hdl.handle.net/10.1371/journal.pone.0210146.g005
- http://urn.kb.se/resolve?urn=urn:nbn:se:his:diva-17216
- http://hdl.handle.net/10179/17764
- http://arodes.hes-so.ch/record/12790
- http://dx.doi.org/10.5334/cstp.91
- http://hdl.handle.net/10.1371/journal.pone.0210146.g004
- https://ams.confex.com/ams/pdfpapers/72674.pdf
- https://figshare.com/articles/ICBR_Core_Zoo_Performance_Analysis/1491447
- http://handle.uws.edu.au:8081/1959.7/uws:35679
- http://orbi.ulg.ac.be/bitstream/2268/19188/1/Life%20and%20motion%20configuration%20-%20Hallot%20and%20Billen.pdf
- https://usir.salford.ac.uk/id/eprint/53211/1/Torija_et_al_ICSV2016.pdf
- http://pqdtopen.proquest.com/#viewpdf?dispub=13423764
- https://espace.library.uq.edu.au/view/UQ:237671
- http://hdl.handle.net/10068/388924
- https://doaj.org/article/4611459707d842e1a15c5fe6d1d8e80b
- https://stars.library.ucf.edu/scopus2010/5010
- https://zenodo.org/record/3661160
- https://hal.science/hal-03988322/file/remotesensing-12-04164.pdf
- https://zenodo.org/record/1140527
- https://escholarship.org/uc/item/0gp0d96f
- http://hdl.handle.net/1854/LU-8742674
- https://zenodo.org/record/3251323
- https://espace.library.uq.edu.au/view/UQ:684896
- https://figshare.com/articles/_Contingency_table_comparing_gauge_area_averages_and_satellite_rainfall_estimates_/979806
- http://internal.psychology.illinois.edu/%7Easbenjam/pubs/McCarleyBenjamin2013.pdf
- https://nottingham-repository.worktribe.com/file/1395082/1/Handling%20Uncertainty%20in%20Citizen%20Science%20Data
- https://escholarship.org/uc/item/0qr3185s
- https://zenodo.org/record/574575
- https://zenodo.org/record/7521705
- https://nbn-resolving.org/urn:nbn:de:hbz:294-87226
- https://dx.doi.org/10.3390/rs9010087
- http://hdl.handle.net/10068/500897
- https://dx.doi.org/10.3390/rs9040357
- http://hdl.handle.net/10.5281/zenodo.2579782
- https://zenodo.org/record/3690772
- https://doaj.org/article/a11a8f2d08f54273920a2b5da2806d90
- http://hw.oeaw.ac.at/8085-2
- http://hdl.handle.net/10.1371/journal.pone.0206044.g005
- https://zenodo.org/record/802703
- https://zenodo.org/record/3468699
- http://sgmeet.com/aslo/granada2015/viewabstract.asp?AbstractID=25788
- http://hdl.handle.net/10068/275974
- http://faculty.washington.edu/marzban/cluster2.pdf
- https://zenodo.org/record/7797546
- https://doaj.org/article/ba052f48bf75431c89d1ade5b561ad3c
- https://zenodo.org/record/4452819
- https://www.matec-conferences.org/10.1051/matecconf/201930406007/pdf
- http://hdl.handle.net/2013/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/198718
- http://eprints.nottingham.ac.uk/49665/
- http://doi.org/10.1371/journal.pone.0147152
- http://hdl.handle.net/10.1371/journal.pone.0214474.g006
- https://ams.confex.com/ams/pdfpapers/101629.pdf
- http://hdl.handle.net/10068/418036
- https://zenodo.org/record/6542154
- https://mural.maynoothuniversity.ie/7093/
- https://library.wur.nl/WebQuery/wurpubs/552657
- https://zenodo.org/record/5619366
- http://dx.doi.org/10.5194/isprsarchives-XL-1-W5-745-2015
- http://edoc.mpg.de/545005
- http://www.hathitrust.org/access_use#pd-google.
- https://doi.org/10.3897/biss.5.75506
- https://doaj.org/article/8ab5f6d09ac24ea1a23f18e7581a36f6
- https://figshare.com/articles/_Classification_results_degree_vs_activation_features_/175226
- http://hdl.handle.net/10068/654180
- https://hdl.handle.net/1813/39286
- http://arodes.hes-so.ch/record/4387
- https://zenodo.org/record/3476728
- https://repository.rudn.ru/records/article/record/71682/
- http://researchdata.gla.ac.uk/view/author/16855.html
- http://resolver.tudelft.nl/uuid:b9cd47d6-c54f-40f4-95f9-4e9624f1c859
- http://tubiblio.ulb.tu-darmstadt.de/140605/
- https://figshare.com/articles/Andrew_etal_PeerJ_InsectsCC/105599
- http://oa.upm.es/63561/
- https://escholarship.org/uc/item/0tc179sc
- https://eprints.lancs.ac.uk/id/eprint/127626/
- http://hdl.handle.net/10.1371/journal.pone.0210146.t005
- https://zenodo.org/record/3994455
- http://hdl.handle.net/10261/142581
- https://scholar.afit.edu/etd/2300
- https://doaj.org/article/0dae7d2f450f44a8a0308a47864a5e37
- http://hdl.handle.net/10150/665355
- http://hdl.handle.net/10197/10940
- https://doi.org/10.7910/DVN/DBRLV5
- http://istardb.org/1583/1/amateur_community_and_citizen_science.pdf
- https://escholarship.org/uc/item/4f89v0b5
- http://hdl.handle.net/10.1371/journal.pone.0282105.g014
- https://digitalcommons.uri.edu/nrs_facpubs/219
- https://escholarship.org/uc/item/54d938bd
- http://vcg.seas.harvard.edu/files/pfister/files/infovis_submission251-camera.pdf
- https://zenodo.org/record/7853217
- http://hdl.handle.net/11585/551087
- https://scholarworks.utep.edu/open_etd/2374
- https://zenodo.org/record/4409124
- https://pure.iiasa.ac.at/view/iiasa/2612.html
- http://myweb.fsu.edu/jelsner/PDF/Research/Imperfect.pdf
- https://pure.iiasa.ac.at/id/eprint/19147/
- http://researchspace.bathspa.ac.uk/11636/1/AS6823441386700801539694928196_content_1.pdf
- http://discovery.ucl.ac.uk/10058422/1/Citizen-Science.pdf
- https://doaj.org/article/3ad76478261f4fd5867b70a904b0c046
- https://zenodo.org/record/1140643
- https://mural.maynoothuniversity.ie/7093/1/12934_SEBASTIAN_DUQUE_JARAMILLO.pdf
- http://hdl.handle.net/10400.1/10650
- http://hdl.handle.net/2142/106442
- https://zenodo.org/record/6345452