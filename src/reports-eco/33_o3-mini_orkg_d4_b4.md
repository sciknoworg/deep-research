# Final Report: Key Challenges for Biodiversity

This report synthesizes recent advances and research findings on biodiversity challenges from multiple perspectives. The discussion spans global as well as region-specific issues and integrates ecological, socio-economic, policy, and technological dimensions. In what follows, we detail the multifaceted challenges facing biodiversity today, the methodological advances needed to address these challenges, and recommendations for integrating these insights into effective conservation strategies.

---

## 1. Introduction

Global biodiversity is under unprecedented strain due to a complex web of anthropogenic and natural pressures. Climate change, habitat fragmentation, invasive species, and additional stressors continue to undermine ecosystem stability. Alongside these drivers, socio-economic factors and policy inefficiencies complicate conservation planning. Emerging interdisciplinary frameworks, powered by remote sensing, artificial intelligence (AI), and integrative modeling approaches, are essential avenues to counter these challenges. This report brings together the latest research learnings, including integrated biodiversity models, early-warning signal methodologies, policy integration, uncertainty quantification, and socio-economic valuation methods.

## 2. Ecological Modeling and Data Integration

### 2.1. Integrated Biodiversity Models

Recent work in biodiversity modeling emphasizes the necessity of integrating empirical, mechanistic, and remote sensing data to capture the dynamic interactions between climate and land use. This integration seeks to account for both direct climate impacts and indirect effects mediated by climate-driven land-use changes. Key challenges include:

- **Harmonizing spatial–temporal scales:** Models must bridge fine-scale local observations (e.g., plot-level biodiversity data) with global climate and land-use trends.
- **Disentangling bidirectional feedbacks:** Both climate and land-use change often produce nonlinear interactions and cascading feedback loops that complicate predictions.
- **Empirical-socioeconomic data bridges:** Incorporating socio-economic variables, such as the effects of urban expansion and economic development, into ecological models is essential to understand comprehensive biodiversity shifts.

Middleware frameworks that use APIs and containerized workflow environments (for example, extensions to GEMINI-E3, TIAM-WORLD, MAGICC6, and LPJmL) have emerged as promising tools to enhance data interoperability and longevity of integrated models.

### 2.2. Advances in Early Warning Signal Detection

The emergence of sophisticated early warning signal methodologies has transformed our ability to detect abrupt transitions in ecosystems. Techniques such as the Ratio of Spectra (ROSA) and critical slowing down indicators, often coupled with remote sensing data, have provided evidence for impending events like Amazon rainforest dieback or ENSO anomalies.

- **Spatial and temporal indicators:** Approaches that quantify spatial standard deviations and patch structure (often characterized using power law distributions) assist in forecasting regime shifts well in advance.
- **Probabilistic modeling:** Bayesian neural networks and Monte Carlo dropout methods enhance uncertainty calibration across datasets, which is particularly useful for complex and noisy time-series observations.

When incorporating these early warning signals into dynamic biodiversity models, researchers have observed improved lead times and robustness in predictions, even in ecosystems prone to nonlinear or abrupt shifts.

## 3. Interdisciplinary Approaches in Biodiversity Conservation

### 3.1. Integrating Socio-Economic and Policy Challenges

Biodiversity conservation is inextricably linked to socio-economic and policy frameworks. Notably, current research calls for:

- **Dynamic policy frameworks:** Policies that incorporate scenario planning, real-time monitoring, and simulation modeling are needed. Examples include integrated conservation planning recognized by UN SDGs and frameworks from COP15 and COP26.
- **Stakeholder engagement:** Broad participation of local communities, NGOs, international bodies, and scientific institutions is vital to balance ecological objectives with practical governance realities.
- **Fiscal innovations:** Models that integrate ecological feedback with economic instruments—such as biodiversity offsets, green fiscal policies, local future tax credits, and property tax shifting—offer promising solutions. Evidence from case studies in Canada and across Europe illustrate that even marginal tax increases on non-priority lands can yield significant conservation benefits.

### 3.2. Social–Ecological Systems and Dynamic Governance Models

Research underscores the importance of aligning conservation strategies with the underlying socio-economic determinants of biodiversity loss:

- **Multi-scale governance:** Effective conservation requires transboundary and coordinated governance that aligns global policy targets with local implementation. For example, agent-based models of farmer decision-making in the UK emphasize the need for participatory, localized conservation practices.
- **Adaptive conservation planning:** Scientific evidence from the UK, Iberian Peninsula, and tropical regions suggests that flexible, adaptive approaches are critical for meeting biodiversity targets in the face of shifting climates. Strategies such as creating dynamic wildlife corridors, assisted migration, and community-level management have been shown to be particularly effective.

## 4. Technological Advances and Solutions

### 4.1. Role of Remote Sensing and AI

Advances in remote sensing technology—such as the application of high-resolution Sentinel imagery, LiDAR, and continuous spatiotemporal datasets—are transforming biodiversity monitoring by providing near-real-time ecological assessments. The integration of these datasets with explainable AI methods (encompassing deep learning, NLP, and reinforcement learning) enhances model accuracy and provides actionable insights at multiple scales.

- **Automated species identification:** Citizen science platforms (e.g., eBird’s Human-Computer Learning Network) combined with deep learning models enable scalable and cost-efficient data collection.
- **Multi-domain data fusion:** Systems that merge satellite imagery with socio-economic data help quantify trends like urban sprawl, light pollution, and land-use change—critical indices to forecast biodiversity impacts.

### 4.2. Advanced Aggregation and Uncertainty Quantification

Given the complexity of biodiversity metrics, various aggregation methodologies (e.g., PCA, Local PCA, GWPCA) have been developed to capture spatial heterogeneity and interrelated variables. These methods attempt to address issues of substitutability among dimensions in composite indices, which are critical when integrating environmental, economic, and health data.

- **Uncertainty management:** Modern models increasingly utilize Bayesian frameworks and Monte Carlo techniques to manage epistemic and aleatoric uncertainties. These approaches enhance reliability when predicting the timing and magnitude of ecosystem tipping points.
- **Hybrid downscaling:** The creation of hybrid models that merge empirical data with deep learning emulators offers a pathway for rapid, computationally efficient predictions, thereby refining traditional species distribution models.

## 5. Ecosystem Connectivity and Conservation Strategies

### 5.1. Dynamic Wildlife Corridors and Dispersal Dynamics

Maintaining dispersal connectivity is crucial for species survival, particularly under climate change. Simulation studies and empirical field validations have advanced our understanding of:

- **Corridor efficacy:** Models that account for species-specific dispersal capabilities and habitat connectivity (e.g., cellular lattice and colonization–extinction models) suggest that optimal corridors are achieved when the scale of patch heterogeneity aligns with species’ dispersal thresholds.
- **Partial dispersal scenarios:** Recognizing that species often experience intermediate levels of dispersal, recent models now incorporate full, partial, and no-dispersal conditions. This refinement addresses limitations in simple assumptions and provides more realistic projections for conservation planning.

### 5.2. Nature-based Solutions and Ecosystem Credit Systems

Convergence of biodiversity and climate agendas is encouraging the adoption of Nature-based Solutions, which integrate financial incentives with ecological benefits. In practice, ecosystem credit systems—a method that combines ecological feedback loops with monetized incentives—are emerging as potent policy tools. Case studies in fishery management and water quality trading underscore their effectiveness at multiple scales.

- **Credit stacking and fiscal instruments:** By stacking ecosystem credits and employing designs such as cap-and-trade schemes, decision makers can achieve measurable service improvements and social-welfare gains. These market-based interventions can complement traditional regulatory policies.

## 6. Future Directions and Recommendations

### 6.1. Advancing Integrated Frameworks

Future research must focus on further merging ecological and evolutionary processes with modern computational advances. Approaches to consider include:

- Building multi-scale models that explicitly incorporate feedback loops between climate, land use, and biodiversity.
- Enhancing interoperability between disparate datasets through standardized metadata frameworks (e.g., I-ADOPT) and FAIR data principles.
- Investing in middleware and plugin frameworks that facilitate the seamless integration of socio-economic models with biophysical data.

### 6.2. Research-Driven Policy Design

Robust scientific input demands that policy frameworks become more dynamic and evidence-based:

- **Scenario planning and real-time monitoring:** Authorities should embed data-rich, predictive models into adaptive management practices, ensuring that policy targets remain congruent with ecological realities. This can be accomplished using advanced early warning systems and AI-driven analytics.
- **Stakeholder co-production:** Involving local communities and international bodies in both data collection (through citizen science) and the decision-making process ensures that conservation strategies are tailored to regional nuances and social realities.
- **Economic integrations:** Models linking fiscal policies with conservation outcomes (e.g., Local Future Tax Credits and dynamic conservation surcharges) provide a proactive pathway to blend economic growth with sustainable biodiversity management.

### 6.3. Addressing Uncertainties and Long-Term Sustainability

Alternative and underutilized approaches—such as translocation experiments, gene expression studies, and environmental gradient analysis—should be expanded to validate model predictions and measure short-term ecological resilience. Multi-disciplinary research that fuses insights from ecology, economics, and social sciences will be instrumental in designing more resilient conservation strategies.

## 7. Conclusion

The challenges facing global biodiversity are both complex and intertwined. Addressing these requires:

- A concerted integration of ecological, climatic, socio-economic, and technological data streams.
- Adaptive and dynamic governance that can respond to rapid and often nonlinear changes in ecosystems.
- Deployment of innovative analytical techniques—including early warning systems, deep learning, and uncertainty quantification—to better predict and manage abrupt transitions in biodiversity.

In summary, advancing the field of biodiversity conservation depends on proactive, interdisciplinary frameworks that foster both scientific discovery and practical policy implementation. The learnings synthesized in this report highlight key areas for future research and present a roadmap for integrating state-of-the-art models with real-time conservation actions, ensuring that biodiversity is preserved for generations to come.

---

*This report leverages extensive recent research findings and speculative future pathways to offer a detailed and comprehensive perspective on current biodiversity challenges. Continued refinement of integrated models and policy frameworks will be essential in responding to the accelerating pressures of global change.*

## Sources

- http://resolver.tudelft.nl/uuid:4d7dfe78-b94d-485d-b0f6-ef73b33a8047
- http://arxiv.org/pdf/1403.0316.pdf
- http://hdl.handle.net/2429/65695
- https://research.wur.nl/en/publications/biodiversity-conservation-in-climate-change-driven-transient-comm
- http://handle.unsw.edu.au/1959.4/26796
- http://hdl.handle.net/10536/DRO/DU:30070597
- http://cascadesorte.org/wp-content/uploads/2013/04/Sorte2013_Oikos.pdf
- http://hdl.handle.net/10871/125229
- https://doaj.org/article/ff52582fe28f418884466216f9c0d99d
- http://edepot.wur.nl/264296
- https://doaj.org/article/46bc3792a75c4b1abd5b844d2fbb390a
- http://hdl.handle.net/2142/16442
- https://biblio.ugent.be/publication/4328172/file/4328191
- https://www.repository.cam.ac.uk/handle/1810/273519
- http://hdl.handle.net/1842/28081
- https://dspace.library.uu.nl/handle/1874/413225
- https://lirias.kuleuven.be/handle/123456789/343793
- https://hal.umontpellier.fr/hal-03415696/file/fmars-08-613279.pdf
- https://digitalcommons.usf.edu/msc_facpub/1004
- http://bioecon-network.org/pages/16th_2014/Liu.pdf
- http://hdl.handle.net/10261/221903
- https://doaj.org/article/f4fe313e23264e4488437e2e15aedf01
- https://hal.science/hal-01834227/document
- http://ageconsearch.umn.edu/record/18810
- https://www.ijai4s.org/index.php/journal/article/view/4
- http://hdl.handle.net/1885/209339
- https://dspace.library.uu.nl/handle/1874/281753
- http://digital.csic.es/bitstream/10261/67404/1/journal.pone.0041010-1.pdf
- https://doi.org/10.1016/j.ecoinf.2006.12.001
- http://journals.openedition.org/trajectoires/1312
- http://infoscience.epfl.ch/record/216989
- https://hal.inrae.fr/hal-02939133/document
- http://hdl.handle.net/10449/24390
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/26/32/pone.0081025.PMC3836997.pdf
- https://doi.org/10.1088/1748-9326/acbc8d
- https://hal.archives-ouvertes.fr/hal-01983410
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/78/32/ece30003-3334.PMC3797481.pdf
- www.myjurnal.my/filebank/published_article/470531.pdf
- https://doi.org/10.17352/ojps.000026
- http://www.icarus.info/wp-content/uploads/2011/06/Wright.pdf
- https://escholarship.org/uc/item/83r1097x
- https://escholarship.org/uc/item/43v1c827
- https://hal.science/hal-00362940
- http://hdl.handle.net/2060/20200001156
- https://espace.library.uq.edu.au/view/UQ:308094
- https://hal.sorbonne-universite.fr/hal-01465891/document
- http://www.geocomputation.org/2003/Papers/Carmel_Paper.pdf
- https://hal.inrae.fr/hal-02608839
- http://ageconsearch.umn.edu/record/305246
- https://hal.archives-ouvertes.fr/hal-02444463
- https://hdl.handle.net/2164/18923
- http://hdl.handle.net/10722/213230
- http://hdl.handle.net/11573/874621
- http://hdl.handle.net/10027/19852
- http://hdl.handle.net/10255/dryad.227888
- https://birmingham.elsevierpure.com/en/publications/98518a06-d842-4c29-95bf-6c572ae10cd7
- https://zenodo.org/record/7064254
- https://dx.doi.org/10.3390/d5010114
- https://boris.unibe.ch/139255/
- http://hdl.handle.net/10.6084/m9.figshare.7411688.v1
- http://tiikmpublishing.com/proceedings/index.php/globewarm/issue/archive
- https://cedar.wwu.edu/ssec/2018ssec/allsessions/5
- http://www.economics.hawaii.edu/research/workingpapers/WP_10-11.pdf
- https://doaj.org/article/c31c42b5f44f422aaf2e9728ac500309
- http://hdl.handle.net/10.1371/journal.pclm.0000320.g002
- https://hdl.handle.net/11311/1259408
- https://doi.org/10.1098/rspb.2002.2246
- https://dx.doi.org/10.3390/su10051369
- https://espace.library.uq.edu.au/view/UQ:263158
- http://hdl.handle.net/10138/567414
- https://serval.unil.ch/notice/serval:BIB_D16FD5B8CEF1
- https://doi.org/10.17615/bbjn-n855
- http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3962379/pdf/pone.0092097.pdf
- https://doaj.org/toc/1932-6203
- https://hal.science/hal-03769565/document
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0959378015000576/MAIN/application/pdf/dfb9b0be73c1545a5331e813f7ea272e/main.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S096098220702341X/MAIN/application/pdf/b2e29df97cfb1043ed02ca38018849d9/main.pdf
- https://espace.library.uq.edu.au/view/UQ:376214
- https://figshare.com/articles/Framework_for_Data_Informed_Science_Policy/157174
- https://escholarship.org/uc/item/378683cq
- https://insu.hal.science/insu-03863754
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/27647
- https://researchonline.jcu.edu.au/52025/1/52025_reside_et_al_2018.pdf
- https://hal.archives-ouvertes.fr/tel-01846283
- https://doaj.org/article/53a7d36739d54214b9708c19cc65c689
- https://discovery.dundee.ac.uk/en/publications/f5bad95c-1ec5-45cc-ade2-4ce562eb72aa
- https://escholarship.org/uc/item/54d938bd
- http://ageconsearch.umn.edu/record/280912
- https://shs.hal.science/halshs-01225980
- https://doi.org/10.1111/2041-210X.13834
- https://doi.org/10.1111/j.1600-0706.2013.00399.x
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0006320716303639/MAIN/application/pdf/08a9fb9c2bdd8c0dd4674df6d395ba18/main.pdf
- https://hal.archives-ouvertes.fr/hal-01444016
- https://zenodo.org/record/3350965
- https://pure.knaw.nl/portal/en/publications/e3bc8365-8457-41d8-869c-b21f63006744
- https://hal.archives-ouvertes.fr/hal-01565811
- https://doaj.org/article/028c8b448d58458aadd3a269fb75e5b5
- https://hal-ineris.archives-ouvertes.fr/ineris-01855135
- http://agritrop.cirad.fr/574270/
- http://hdl.handle.net/10072/398282
- https://espace.library.uq.edu.au/view/UQ:269547
- https://doi.org/10.1016/j.gecco.2019.e00601
- https://eprints.whiterose.ac.uk/88317/1/Hill%20et%20al%20%282015%29%20Aichi%20Targets.pdf
- http://hdl.handle.net/11858/00-001M-0000-000E-DC24-0
- https://ojs.aaai.org/index.php/AAAI/article/view/17728
- http://dx.doi.org/10.1111/geb.12555
- https://elib.dlr.de/191309/
- https://doaj.org/toc/1337-947X
- http://publications.ut-capitole.fr/21716/1/Froger_21716.pdf
- http://www.forestthreats.org/products/publications/Quantitative_metrics_for_assessing_predicted_climate_change_pressure.pdf
- https://library.wur.nl/WebQuery/wurpubs/531572
- https://eprints.whiterose.ac.uk/203883/1/Paper%20with%20authors%20details_final.pdf
- http://hdl.handle.net/11154/2121
- https://doaj.org/article/5454a09c084f4b058d1c9c85c6519754
- https://elib.dlr.de/186663/
- https://research.vu.nl/en/publications/de8bca68-60d8-4474-9a15-33fde13267ac
- https://eprints.whiterose.ac.uk/75927/1/pdf%20Anticipating%20and%20managing%20future%20trade-offs.pdf
- https://biblio.ugent.be/publication/3049827/file/3049857
- https://hal-univ-tlse2.archives-ouvertes.fr/hal-01631272
- http://www.gfy.ku.dk/%7Epditlev/papers/tipping_chapter_rev1.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.85.7382
- https://escholarship.org/uc/item/97d454fj
- http://web.gps.caltech.edu/~drf/misc/airs/maup_summary.pdf
- http://hdl.handle.net/10449/22034
- https://escholarship.org/uc/item/0ct4c4xb
- https://www.zora.uzh.ch/id/eprint/187981/
- https://www.zora.uzh.ch/id/eprint/150598/1/2017_08113128.pdf
- http://tud.qucosa.de/api/qucosa%3A26748/attachment/ATT-1/
- https://www.webofscience.com/api/gateway?GWVersion=2&SrcApp=PARTNER_APP&SrcAuth=LinksAMR&KeyUT=WOS:000388154100004&DestLinkType=FullRecord&DestApp=ALL_WOS&UsrCustomerID=42fe17854fe8be72a22db98beb5d2208
- https://zenodo.org/record/3776949
- https://research.wur.nl/en/publications/evidence-based-alignment-of-conservation-policies-with-remote-sen
- https://escholarship.org/uc/item/4151d3nj
- https://pure.iiasa.ac.at/view/iiasa/2612.html
- https://hal.archives-ouvertes.fr/hal-02195169/document
- https://lirias.kuleuven.be/bitstream/123456789/429652/1/Poster_PhDSymp2012.pdf
- http://science.sciencemag.org/content/sci/332/6025/53.full.pdf
- https://doi.org/10.1007/978-3-319-76445-0_10
- https://doaj.org/article/8073f8e7929843d0b02dc74d41fd4684
- https://escholarship.org/uc/item/1b67s3rs
- https://escholarship.org/uc/item/7m36291w
- https://figshare.com/articles/_Assessment_of_early_detection_methods_in_terms_of_i_the_potential_for_detecting_early_warnings_signals_in_the_selected_time_series_ii_how_far_in_advance_early_warning_signals_could_potentially_be_detected_i_e_in_number_of_years_before_the_regime_shift_ii/283058
- http://hdl.handle.net/11573/650036
- http://hdl.handle.net/10150/662901
- http://harvardforest.fas.harvard.edu/sites/harvardforest.fas.harvard.edu/files/publications/pdfs/Dakos_PLoS1_2012.pdf
- http://eprints.lse.ac.uk/46895/
- http://hdl.handle.net/11585/722476
- http://hdl.handle.net/2262/79065
- http://hdl.handle.net/11567/1070050
- http://hdl.handle.net/20.500.11850/557699
- http://hdl.handle.net/11858/00-001M-0000-0014-9A7E-B
- http://urn.kb.se/resolve?urn=urn:nbn:se:su:diva-179561
- http://hdl.handle.net/2440/93300
- https://scholarworks.umt.edu/ntsg_pubs/402
- http://hdl.handle.net/10261/149016
- https://hal.archives-ouvertes.fr/hal-00304508
- https://www.zora.uzh.ch/id/eprint/206213/1/2021_Schaepman_s41559-021-01451-x.pdf
- https://research.vu.nl/en/publications/c0b06de8-4104-4ea0-86f6-f58719d37e82
- https://research.utwente.nl/en/publications/0258d70f-e5ae-46d8-9898-c01a6f82adc3
- http://shdl.mmu.edu.my/9455/
- https://hal.archives-ouvertes.fr/hal-03249425/document
- https://hal.archives-ouvertes.fr/hal-02930052/file/Warszawski_2013_Environ._Res._Lett._8_044018.pdf
- http://eprints.iisc.ac.in/44963/
- https://doaj.org/article/68264f8842d64f4884adbe5255e4183d
- https://doi.org/10.1126/science.287.5459.1770
- https://research.monash.edu/en/publications/a2bac437-2b99-4d83-b297-b0ece8517e76
- http://www.loc.gov/mods/v3
- https://insight.cumbria.ac.uk/id/eprint/5467/1/IFLAS_OP_4_LFTCs.pdf
- http://nora.nerc.ac.uk/id/eprint/530313/
- http://hdl.handle.net/10.26180/5c6bfb381fe23
- https://www.zora.uzh.ch/id/eprint/216975/
- https://elib.dlr.de/111343/
- https://researchonline.jcu.edu.au/29015/1/29015_Bateman_etal_2013.pdf
- https://doaj.org/article/4dac3c2109d344a8879c050e38b674c5
- https://boris.unibe.ch/146566/
- https://ageconsearch.umn.edu/record/94826/files/EERH_RR26.pdf
- https://digitalcommons.uri.edu/nrs_facpubs/313
- http://arodes.hes-so.ch/record/9395
- https://archive-ouverte.unige.ch/unige:143505
- https://hdl.handle.net/2454/40483
- https://figshare.com/articles/Methods_for_Detecting_Early_Warnings_of_Critical_Transitions_in_Time_Series_Illustrated_Using_Simulated_Ecological_Data/122643
- https://dspace.library.uu.nl/handle/1874/429514
- https://doi.org/10.1098/rstb.2004.1589
- http://www.ias.unu.edu/binaries/IASWorkingPaper100.pdf
- http://researchspace.bathspa.ac.uk/11636/1/AS6823441386700801539694928196_content_1.pdf
- http://researchonline.jcu.edu.au/42703/
- http://urn.fi/URN:NBN:fi:jyu-202105042599
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/de/1a/12080_2012_Article_171.PMC4270430.pdf
- https://doi.org/10.13016/dspace/pqzx-581s
- https://researchonline.jcu.edu.au/61291/6/61291.pdf
- http://hdl.handle.net/1885/67039
- https://researchonline.jcu.edu.au/24830/1/24830_Hill_etal_2013.pdf
- http://j.boulangeat.free.fr/pdfs/Travis2013_Oikos.pdf
- http://www.fisica.edu.uy/%7Ehugo/early.pdf
- http://hdl.handle.net/10316/31247
- https://espace.library.uq.edu.au/view/UQ:678082
- https://eprints.lancs.ac.uk/id/eprint/160474/
- https://discovery.dundee.ac.uk/en/publications/8fbce3a9-ec90-470c-acc8-c9052ef5ef62
- http://dces.essex.ac.uk/Research/iieg/papers/WereTigersOfBelum%28Paper%29.pdf
- http://hdl.handle.net/2142/26362
- https://zenodo.org/record/4969734
- http://hdl.handle.net/2078.3/231192
- https://ojs.aaai.org/index.php/aimagazine/article/view/2431
- https://research-portal.st-andrews.ac.uk/en/researchoutput/modelling-wildlife-corridors(3375dcac-70ff-4c17-8c3b-dc485a4afa43).html
- https://pure.iiasa.ac.at/id/eprint/18059/
- http://hdl.handle.net/10174/28001
- http://hdl.handle.net/1885/34610
- https://opus.bibliothek.uni-wuerzburg.de/files/13186/129_Rinawati_Diversity.pdf
- http://hdl.handle.net/1959.14/142010
- http://hdl.handle.net/10.6084/m9.figshare.7506242.v1
- https://doaj.org/article/6c762f7db8ef4f7da887b6b58c6621db
- https://doaj.org/article/b4d8eca99c3e4bb782ed304a760d91db
- https://bradfordlab.files.wordpress.com/2011/10/bradford-warren-2012.pdf
- https://doi.pangaea.de/10.1594/PANGAEA.900207
- https://doaj.org/article/a88a82eb13cc486d8a8bbcffbf28279e
- http://hdl.handle.net/10.6084/m9.figshare.7472948.v1
- https://research.utwente.nl/en/publications/modelling-how-people-and-nature-are-intertwined(a9ab50c0-ad2d-489c-b7b1-ca710e24d5e4).html
- http://www.whoi.edu/cms/files/guisan_thuiller_2005_53452.pdf
- http://agritrop.cirad.fr/579039/7/579039.pdf
- https://www.intechopen.com/books/biodiversity-loss-in-a-changing-planet
- https://hdl.handle.net/11250/2653345
- https://escholarship.org/uc/item/4xv7j2qs
- https://escholarship.org/uc/item/8wm0n05n
- http://tubiblio.ulb.tu-darmstadt.de/138745/
- http://publications.jrc.ec.europa.eu/repository/handle/JRC92638
- http://hdl.handle.net/11588/820375