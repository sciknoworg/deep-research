# Final Report: Interactions Between Climate Change, Land Use, and Grassland Biodiversity

This comprehensive report synthesizes decades of research and recent advances in the understanding of how climate change and land use interact to alter grassland biodiversity. The integration of high-resolution remote sensing, advanced machine learning, and diverse experimental designs has refined our predictions of grassland ecosystem processes. In what follows, we detail the principal findings and methodologies that have shaped our current view, discuss case studies from various grassland ecosystems, and outline future research directions.

---

## 1. Introduction

Grasslands worldwide are under increasing threat from a combination of anthropogenic land-use changes and climate change. While each of these factors alone has a profound impact on biodiversity, their interaction creates a complex and dynamic system that poses significant challenges for conservation and management. The central question addressed in this report is: **Is there evidence that climate change and land use interact to alter biodiversity in grassland ecosystems?**

Drawing on extensive empirical studies, remote sensing innovations, and advanced modeling approaches, this report collates learnings from controlled experiments, observational analyses, and model-based projections. The review underscores not only the direct impacts (e.g., changes in temperature, precipitation, and disturbance regimes such as grazing, fire, and urbanization) but also secondary and interactive effects that drive non-linear responses at landscape scales.

---

## 2. Methodological Innovations and Data Integration

### 2.1 Advanced Remote Sensing and Process-Based Modeling

Recent research has seen a paradigm shift through the integration of high-resolution remote sensing data (e.g., Landsat, MODIS, Hyperspectral, Formosat-2, and SENTINEL products) with process-based ecosystem models. The use of spectral indices such as LAI, NDVI, SIF, NIRv, red edge, and SWIR bands has proved essential for mapping vegetation state, phenology, and functional dynamics. For instance, studies indicated SIF’s superior performance in capturing gross primary productivity (GPP) phenology in drylands, while LAI metrics have been crucial in distinguishing between different grassland management practices such as mowing and grazing.

These remote sensing products are integrated with dynamic vegetation global models (DGVMs), like the LPJmL, and simulation models (e.g., DLEM-Ag, PaSim) to refine spatial predictions of carbon fluxes, water budgets, and aboveground biomass. High-performance computing and digital twin frameworks have further accelerated these efforts by enabling pixel-level analyses and real-time spatio-temporal monitoring.

### 2.2 Ensemble and Hybrid Machine Learning Frameworks

Hybrid modeling techniques that blend mechanistic, statistical, and machine learning approaches have significantly enhanced the predictability of grassland ecosystem responses. Advanced methods, including Random Forest, Gradient Boosting machines, Support Vector Machines, and convolutional neural networks (CNNs) have been applied to species distribution modeling. In competitions like GeoLifeCLEF, models trained with multi-million species observations achieved high accuracy, sometimes demonstrating R² values of up to 0.60 and RMSEs as low as 1245.85 kg DW/ha.

Furthermore, ensemble modeling approaches—incorporating outputs from over a dozen grassland simulation models across numerous climate scenarios—have demonstrated how elevated atmospheric CO2, in combination with warming and altered precipitation, expands the thermal and hydric ranges of grasslands. Such studies also reveal trade-offs in greenhouse gas (GHG) emissions, providing crucial insights for mitigation strategies.

### 2.3 Sensitivity Analysis and Nonlinear Dynamics

A notable advancement is the application of functional data analysis-based sensitivity assessments and global sensitivity analysis (GSA) techniques (e.g., Sobol’ variance decomposition). These approaches have largely superseded traditional one-factor-at-a-time (OAT) methods, enabling the evaluation of non-linear and cumulative interactions among climate variables, land use intensities, and biotic interactions. Innovative strategies, such as bootstrap-based grouping and metafunction benchmarking, have allowed robust sensitivity measures to be obtained with a minimal number of model runs, balancing computational efficiency with predictive accuracy.

---

## 3. Empirical Insights and Case Studies

### 3.1 Field Experiments and Long-Term Manipulative Studies

Long-term experiments, some spanning over 25 to 50+ years, provide compelling evidence on how mesic and arid grassland ecosystems respond to varying disturbance regimes. For example, studies at the Konza Prairie Biological Station (USA) and analogous systems in South Africa and Europe have shown that grasslands often exhibit nonlinear, ridge-shaped responses when exposed to warming, precipitation shifts, and altered grazing pressures. Specifically, threshold metrics (e.g., a 4°C warming or 50% precipitation reduction) trigger significant declines in ANPP, BNPP, and species richness—especially under high grazing intensities.

Moreover, manipulative experiments incorporating factorial designs have elucidated the role of plant community composition and functional traits (e.g., specific leaf area, leaf nitrogen content) in buffering ecosystem responses. Experimental designs that incorporate herbivore exclusion and herbivory feedback, as seen in the Konza-Kruger Fire-Grazing Project, have emphasized the importance of accounting for edge or halo effects, where disturbances at ecosystem boundaries significantly alter species dispersal and colonization dynamics.

### 3.2 Urban Grasslands and Regional Variability

Observational studies in urban contexts (e.g., Berlin) have illustrated that urban abiotic factors such as sky view factor, impervious surface percentage, and human population density affect functional biodiversity metrics. Alien forbs, contributing approximately 13.1% to aboveground biomass, underscore the nuanced interplay between native and non-native species. Regional studies, whether in urbanized environments or semi-natural grasslands like those in the Netherlands, have documented differential strengths in resistance and resilience: intensively managed systems tend to recover more quickly whereas species-rich, semi-natural systems exhibit higher resistance to climatic anomalies.

### 3.3 Global Meta-Analysis and Synthesis

Meta-analytical approaches have allowed researchers to quantitatively synthesize results across multiple studies. By incorporating long-term records (e.g., a 14-year NDVI time series) and cumulative meta-analyses that dynamically update with new data, these assessments reveal that global mean temperature increases are robust predictors of biodiversity decline. Studies integrating Essential Biodiversity Variables (EBVs) and frameworks like the Convention on Biological Diversity have underscored the importance of considering both direct climate drivers and indirect land-use effects (e.g., urban expansion and agricultural encroachment) when evaluating beta-diversity dynamics.

---

## 4. Modeling Interactions: Climate Change and Land Use

### 4.1 Integrated Assessment Models and Socio-Ecological Systems

The integration of multi-spatial socioeconomic statistics with dynamic climate and ecological datasets (as demonstrated by the Inner Mongolia study) significantly enhances model accuracy. In these studies, panel regressions with quadratic, lagged, and non-linear effects have captured the interplay between climate variables and socioeconomic indicators, yielding more accurate spatial predictions of grassland productivity and species shifts. Such hybrid models clarify the feedback loops between land-use practices (e.g., grazing management, nutrient addition) and climate change drivers. 

### 4.2 Mechanistic and State-and-Transition Models

Mechanistic simulation models that incorporate explicit above–belowground feedbacks and state-and-transition frameworks have advanced our understanding of regime shifts in grasslands. These models account for important processes such as intraspecific vs. interspecific competition, density-dependent dispersal, and lagged responses to climatic perturbations. The identification of critical thresholds, such as a transition near 68% vegetation cover in Kruger National Park, elucidates how combined disturbances (fire, grazing, drought) precipitate shifts from sedgedominated to forb-dominated communities.

### 4.3 Role of Climate-Driven Land Use Scenarios

Coupling climate-driven land-use models with ecological frameworks has proven vital in distinguishing between direct climate impacts and indirect urbanization effects. Advanced approaches using remote sensing indices and machine learning classifiers have achieved high classification accuracies (e.g., up to 94.23% in Natura 2000 habitats), providing a robust method to forecast future changes in species richness and ecosystem services. These projections, typically derived from ensembles of multiple simulation models, support the formulation of climate‐smart management strategies that integrate altered species compositions, such as the adoption of C4 grasses and grass–legume mixtures.

---

## 5. Implications for Management and Conservation

### 5.1 Adaptive Management Strategies

Building on model-based projections and case-study insights, adaptive management practices have been increasingly adopted to enhance ecosystem resilience. For instance, rotational grazing, reduced mowing frequencies, and the incorporation of native warm-season species have shown promise in mitigating the adverse impacts of projected climatic shifts. In semi‐arid rangelands, flexible stocking strategies and localized management frameworks—supported by real-time sensor monitoring and digital twin models—have optimized forage production while preserving biodiversity.

### 5.2 Policy and Interdisciplinary Collaboration

The complexity of grassland responses to climate change and land use underscores the need for robust, interdisciplinary collaboration among ecologists, remote sensing experts, and policy makers. Recent NSF-funded initiatives and collaborative frameworks have advanced harmonized parameterization protocols and standardized data transformation methods. These efforts are essential for refining species distribution models and improving the implementation of international conservation frameworks (e.g., Agenda 2030, SDGs 14 & 15).

### 5.3 Future Research Directions and Technological Innovations

While significant advances have been made, several challenges remain:

- **Data Integration and Calibration:** Continued efforts are needed to reconcile heterogeneous data sources—including satellite imagery corrections, registration issues, and differences in spatial-temporal resolutions.

- **Nonlinear and Cumulative Effects:** Emerging GSA methods and integrative approaches combining cumulative meta-analysis with clustering-based sensitivity analysis require further validation under diverse climate scenarios.

- **Real-Time Monitoring:** Enhancing real-time ecosystem monitoring via IoT-enabled sensor networks and cloud computing platforms will support dynamic adaptive management. 

- **Urban and Peri-Urban Dynamics:** More research is required to understand how urbanization, particularly its indirect effects (e.g., fragmentation and halo disturbances), modulates grassland biodiversity and ecosystem resilience.

- **Trait-Based and Mechanistic Models:** Incorporating explicit functional trait measurements (e.g., SLA, LNC) and mechanistic feedbacks (above–belowground interactions) remains a promising avenue to further integrate biotic interactions within predictive frameworks.

---

## 6. Synthesis and Concluding Remarks

Based on the extensive interdisciplinary research synthesized herein, there is compelling evidence that climate change and land use interact synergistically to alter the biodiversity of grasslands. The cumulative learnings illustrate that while isolated studies provide key insights, it is the integrated approach—merging observational data, experimental manipulations, hybrid machine learning, and sophisticated ecosystem modeling—that yields the most accurate predictions of ecosystem responses.

In summary, our findings highlight:

- The merit of high-resolution, multi-sensor remote sensing integrated with state-of-the-art process-based and machine learning models in capturing fine-scale and large-scale grassland dynamics.
- The necessity of considering nonlinear dynamics and threshold responses in both experimental and modeling frameworks to accurately predict ecosystem shifts.
- The critical importance of adaptive management strategies that are informed by real-time monitoring and dynamic, calibrated models, particularly in the face of escalating climate extremes and evolving land-use practices.

Addressing these challenges will require ongoing interdisciplinary collaboration and innovation, ensuring that future models can both predict and mediate the complex interdependencies between climate change, land use, and biodiversity. As we refine these integrated approaches, the resulting frameworks will not only advance our scientific understanding but also inform robust conservation and management policies essential for sustaining grassland ecosystems worldwide.

---

*This report integrates data and findings from diverse global research initiatives. Many of these studies highlight the need for adaptable methods to tackle emergent ecological complexities, underscoring the evolving nature of grassland ecology under the twin pressures of anthropogenic land-use change and climate change.*


## Sources

- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/18/d8/pone.0104672.PMC4128714.pdf
- https://scholars.unh.edu/faculty_pubs/208
- https://library.wur.nl/WebQuery/wurpubs/523131
- https://escholarship.org/uc/item/1b67s3rs
- https://doi.org/10.1016/j.envsoft.2014.05.001
- https://library.wur.nl/WebQuery/wurpubs/327314
- http://urn.kb.se/resolve?urn=urn:nbn:se:su:diva-205609
- http://hdl.handle.net/10150/631793
- http://hdl.handle.net/11585/722476
- https://hal.science/hal-01152055
- https://www.webofscience.com/api/gateway?GWVersion=2&SrcApp=PARTNER_APP&SrcAuth=LinksAMR&KeyUT=WOS:000396241600001&DestLinkType=FullRecord&DestApp=ALL_WOS&UsrCustomerID=42fe17854fe8be72a22db98beb5d2208
- http://publications.jrc.ec.europa.eu/repository/handle/JRC16303
- http://hdl.handle.net/10255/dryad.119302
- http://hdl.handle.net/10459.1/57170
- https://doi.org/10.3389/fpls.2017.00730
- https://doaj.org/article/0ada9567ecc246b49a983850900654e7
- https://zenodo.org/record/7504592
- http://science.sciencemag.org/content/sci/315/5812/640.full.pdf
- https://doaj.org/toc/2069-6469
- https://doaj.org/article/8fcbefb3d6434f8dac214ae83bd691a2
- http://infoscience.epfl.ch/record/201274
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:308049
- https://sajs.co.za/article/view/10343
- https://espace.library.uq.edu.au/view/UQ:64310
- https://lirias.kuleuven.be/bitstream/123456789/429652/1/Poster_PhDSymp2012.pdf
- https://uknowledge.uky.edu/igc/22/1/1
- https://hal.science/hal-02972041/document
- https://zenodo.org/record/4982568
- https://hdl.handle.net/11250/2756526
- https://elib.dlr.de/91190/
- http://digital.library.unt.edu/ark:/67531/metadc708355/
- https://espace.library.uq.edu.au/view/UQ:349257
- http://www.terrapub.co.jp/e-library/kawahata/pdf/375.pdf
- https://www.sciencedirect.com/science/article/pii/S0034425719306467?dgcid=coauthor
- http://prodinra.inra.fr/ft/7A6DF7AE-6F5E-4F1D-997A-76304E6D4142
- http://www.scopus.com/inward/record.url?scp=85065149854&partnerID=8YFLogxK
- https://doi.org/10.1111/j.0030-1299.2007.16047.x
- https://hdl.handle.net/10037/23067
- http://hdl.handle.net/1911/93744
- http://edepot.wur.nl/161421
- https://doaj.org/article/f2ebfaf7d3b242efbcad60c6cee8c812
- https://doaj.org/article/f8fcb12e932f49589e76d96112287fab
- http://publications.jrc.ec.europa.eu/repository/handle/JRC99401
- https://escholarship.org/uc/item/1cr7d6hc
- https://uknowledge.uky.edu/pss_etds/152
- http://hdl.handle.net/20.500.11850/510228
- https://figshare.com/articles/_Are_There_Consistent_Grazing_Indicators_in_Drylands_Testing_Plant_Functional_Types_of_Various_Complexity_in_South_Africa_8217_s_Grassland_and_Savanna_Biomes_/1134970
- https://hal.inrae.fr/hal-02623254
- http://hdl.handle.net/11311/1102920
- https://orbi.uliege.be/handle/2268/25121
- https://digitalcommons.unl.edu/ncfwrustaff/228
- https://dspace.library.uu.nl/handle/1874/394661
- https://elib.dlr.de/111343/
- https://lib.dr.iastate.edu/leopold_grantreports/538
- http://www.nonlin-processes-geophys.net/18/883/2011/npg-18-883-2011.pdf
- https://ams.confex.com/ams/30AgFBioGeo/webprogram/Paper207473.html
- http://hdl.handle.net/2066/157388
- https://doi.org/10.1111/nph.17269
- http://dx.doi.org/10.6073/pasta/248023bcad0d257eb579f577694f3bf4
- https://discovery.ucl.ac.uk/id/eprint/10143879/
- http://ir.ibcas.ac.cn/handle/2S10CLM1/19830
- http://www.planta.cn/forum/files_planta/1_123.pdf
- http://hdl.handle.net/2429/42269
- http://hdl.handle.net/11858/00-001M-0000-0015-3DCD-B
- http://www.sciencedirect.com/science/journal/01681699/98/supp/C
- http://hdl.handle.net/10261/46552
- http://dx.doi.org/10.1016/j.jenvman.2014.11.034
- https://ro.uow.edu.au/smhpapers1/1127
- http://www.iseis.org/jei/abstract.asp?no=201600337
- http://library.wur.nl/WebQuery/wurpubs/431258
- http://hdl.handle.net/11581/391700
- https://zenodo.org/record/3598595
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0190052816300293/MAIN/application/pdf/1fb9bb03022aaef0f5d8649f84148e8f/main.pdf
- https://figshare.com/articles/_Sensitivity_analysis_for_effects_of_diet_interventions_on_weight_using_frequentist_meta_analysis_method_/1581353
- https://ir.library.oregonstate.edu/concern/graduate_thesis_or_dissertations/hd76s773t
- https://zenodo.org/record/4439518
- https://digitalrepository.unm.edu/lter_sev_data/359
- https://hal.inrae.fr/hal-02608836
- http://prodinra.inra.fr/record/322577
- https://scholarworks.umt.edu/ntsg_pubs/143
- https://hal.inrae.fr/hal-03353487/document
- http://hdl.handle.net/10962/d1006017
- https://publications.jrc.ec.europa.eu/repository/handle/JRC119211
- http://agritrop.cirad.fr/581604/1/Volaire%2C%20Barkaoui%2C%20Norton%2C%202014%2C%20European%20Journal%20of%20Agronomy.pdf
- http://nora.nerc.ac.uk/id/eprint/533647/
- https://ojs.macsur.eu/index.php/Reports/article/view/D-C4.2.1
- https://doaj.org/toc/2073-4395
- https://doaj.org/article/1c5844406b1141c28b3e3571cbea578a
- https://serval.unil.ch/notice/serval:BIB_D16FD5B8CEF1
- https://doaj.org/article/1c449ba2fa4b4ea49ccdd0904add3ca7
- https://digitalrepository.unm.edu/lter_sev_data/360
- https://hal.inrae.fr/hal-02608839
- https://www.mdpi.com/2072-4292/15/8/2043/pdf?version=1681347101
- http://hdl.handle.net/10150/666147
- http://hdl.handle.net/1903/31359
- https://www.sciencedirect.com/science/article/abs/pii/S0169534718303045
- http://dx.doi.org/10.1007/s13280-015-0699-8
- https://digitalcommons.usu.edu/cgi/viewcontent.cgi?article=1012&amp;context=sagestep_articles
- https://hal.inrae.fr/hal-02640357
- http://ir.ibcas.ac.cn/handle/2S10CLM1/20698
- https://hal.inrae.fr/hal-02607910
- https://hal.inrae.fr/hal-02628929
- https://hal.archives-ouvertes.fr/hal-01571079
- https://digitalrepository.unm.edu/context/lter_sev_data/article/1321/type/native/viewcontent
- http://hdl.handle.net/10393/27867
- http://hdl.handle.net/1959.14/1045497
- https://hal.inrae.fr/hal-02751060/file/2009_Soussana_IOP_Conference_Series_Earth_Environ_Sci_242046_1.pdf
- https://dspace.library.uu.nl/handle/1874/423933
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/07/33/pone.0018581.PMC3080866.pdf
- https://hal.inrae.fr/hal-04208851
- https://repositorium.ub.uni-osnabrueck.de/bitstream/urn:nbn:de:gbv:700-201112078601/2/thesis_jakoby.pdf
- http://mysite.science.uottawa.ca/jkerr/pdf/tree2003.pdf
- https://research.vu.nl/en/publications/cdcdf65d-67be-4074-82cd-7f1401178057
- http://archiv.ub.uni-marburg.de/diss/z2019/0092
- https://doaj.org/article/f23a0090481445628c8a9216e387f6cd
- http://www.nfp54.ch/files/nxt_projects_80/06_12_2009_07_47_17-nobisetal.pdf
- https://ul.qucosa.de/api/qucosa%3A85744/attachment/ATT-0/
- https://orbi.uliege.be/handle/2268/204390
- https://doaj.org/article/ef5e9559f3734e6a8a67c294763ed87d
- https://doaj.org/toc/2194-9034
- https://uknowledge.uky.edu/igc/XXV_IGC_2023/Ecology/20
- https://mdpi.com/books/pdfview/book/3519
- https://dspace.library.uu.nl/handle/1874/408706
- https://hal-lirmm.ccsd.cnrs.fr/lirmm-03793595/document
- http://hdl.handle.net/20.500.11850/192195
- https://doaj.org/article/4e12bec1ec9f4dd1be4cbbf094da30b2
- https://ageconsearch.umn.edu/record/169952/files/PeterHHoward_AAEA2014_2.pdf
- https://ir.library.carleton.ca/pub/2760
- https://digitalrepository.unm.edu/context/lter_sev_data/article/1328/type/native/viewcontent
- https://research.wur.nl/en/publications/exploring-interaction-effects-from-mechanisms-between-climate-and
- http://hdl.handle.net/10092/5109
- https://open.uct.ac.za/bitstream/11427/36617/1/thesis_sci_2022_dabengwa%20abraham%20nqabutho.pdf
- http://hdl.handle.net/10179/2366
- http://www.thesai.org/Downloads/Volume4No2/Paper_1-Machine_Learning_for_Bioclimatic_Modelling.pdf?height%3D100%%26iframe%3Dtrue%26width%3D100%
- http://www.loc.gov/mods/v3
- https://www.repository.cam.ac.uk/handle/1810/262166
- https://research.wur.nl/en/publications/perspectives-in-machine-learning-for-wildlife-conservation
- http://publications.jrc.ec.europa.eu/repository/handle/JRC113132
- https://research.wur.nl/en/publications/contributions-of-machine-learning-to-remote-sensing-data-analysis
- https://openprairie.sdstate.edu/cgi/viewcontent.cgi?article=6021&amp;context=etd
- https://zenodo.org/record/8033473
- https://doaj.org/article/11f936b45256484ca62a15f3e8d5c4c5
- https://hdl.handle.net/1959.7/uws:67628
- http://dx.doi.org/10.1126/science.1213908
- http://www.zpok.zoldpok.hu/img_upload/cb39111eba7a31c9c0e48686fa8e3c87/Bartha_et_al_2008_Kiskun_LTER_37_40.pdf
- https://research.vu.nl/en/publications/de8bca68-60d8-4474-9a15-33fde13267ac
- http://hdl.handle.net/2078.1/35975
- https://engagedscholarship.csuohio.edu/cgi/viewcontent.cgi?article=1102&amp;context=scibges_facpub
- https://doi.org/10.48693/160
- https://figshare.com/articles/Dynamics_of_climate-mediated_fragmentation_of_suitable_patches_for_12_boreal-obligate_species_/5006717
- http://hdl.handle.net/11369/358965
- https://figshare.com/articles/_Sensitivity_analysis_examining_the_effects_of_multimorbidity_on_active_safety_incidents_and_precursors_of_safety_incidents_across_studies_with_superior_methodological_quality_scores_/1526986
- http://hdl.handle.net/10150/643046
- https://dspace.library.uu.nl/handle/1874/423752
- http://www.documentation.ird.fr/hor/fdi:010077371
- https://zenodo.org/record/8100303
- http://ir.igsnrr.ac.cn/handle/311030/42881
- http://hdl.handle.net/10.1371/journal.pone.0282210.s002
- https://figshare.com/articles/Anthropogenic_Halo_Disturbances_Alter_Landscape_and_Plant_Richness_A_Ripple_Effect__/156558
- http://hdl.handle.net/10388/8190
- https://elib.dlr.de/124482/
- http://hdl.handle.net/2108/282637
- http://159.226.115.200/handle/311030/24280
- https://research.wur.nl/en/publications/do-spatially-homogenising-and-heterogenising-processes-affect-tra
- http://publications.jrc.ec.europa.eu/repository/handle/JRC101127
- https://digitalcommons.unl.edu/dissertations/AAI27666971
- http://hdl.handle.net/10150/280167
- https://doi.org/10.3389/fsufs.2024.1507692
- https://uknowledge.uky.edu/igc/22/plenary/3
- https://figshare.com/articles/Dataset_for_Land_management_trumps_the_effects_of_climate_change_and_elevated_CO2_on_grassland_functioning/1112543
- https://hdl.handle.net/11386/4826953
- https://escholarship.org/uc/item/49m1s7tb
- http://159.226.115.200/handle/311030/23690
- https://escholarship.org/uc/item/6kc5524x
- https://zenodo.org/record/7579583
- https://hal.science/hal-01102955
- https://doaj.org/toc/1932-6203
- https://hal.science/hal-01779748/document
- https://hal.inrae.fr/hal-03203049
- https://www.zora.uzh.ch/id/eprint/133226/1/GilbertEtal_2017_AmNat.pdf
- https://www.sciencedirect.com/science/article/pii/S1364815218301464?via%3Dihub
- https://hal.science/hal-02904051
- http://hdl.handle.net/1773/23416
- https://scholarworks.boisestate.edu/td/1523
- https://hal.science/hal-01445170
- https://doi.org/10.1111/1365-2745.13552
- http://agritrop.cirad.fr/482252/
- https://hdl.handle.net/10568/106634
- https://zenodo.org/record/260396
- https://zenodo.org/record/3975829
- http://hdl.handle.net/1885/84010
- http://real.mtak.hu/67679/1/comec.9.2008.s.3.pdf
- https://figshare.com/articles/Sensitivity_analysis_Relative_and_absolute_frequency_of_meta-analyses_with_10_primary_studies_showing_nominally_statistically_significant_results_small-study_effect_and_excess_significance_by_research_area_/6590591
- http://hdl.handle.net/20.500.11850/417453
- https://espace.library.uq.edu.au/view/UQ:730921
- http://hdl.handle.net/10255/dryad.119008
- https://uknowledge.uky.edu/igc/20/themeB/21
- http://hdl.handle.net/1928/21049
- https://lirias.kuleuven.be/bitstream/123456789/514101/1/De%20Keersmaeker%20et%20al.%20JAE%202016.pdf
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/39/68/13280_2015_Article_699.PMC4709351.pdf
- https://digitalcommons.unl.edu/natrespapers/528
- https://lirias.kuleuven.be/bitstream/123456789/518359/1/CORP2015_141.pdf
- http://prodinra.inra.fr/record/403664
- https://datacompass.lshtm.ac.uk/id/eprint/2964/
- http://hdl.handle.net/1885/34872