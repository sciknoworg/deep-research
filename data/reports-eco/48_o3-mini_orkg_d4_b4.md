# Methodological Challenges in Measuring Seedling Functional Traits

This report offers an in-depth examination of the multifaceted methodological challenges encountered when measuring seedling functional traits. Drawing on a comprehensive review of recent studies, advanced imaging modalities, integration of machine learning, and sophisticated sampling designs, we elucidate both the technical and conceptual barriers that hinder accurate phenotyping. We discuss the balance between throughput and precision in various experimental settings, the intricacies introduced by ontogenetic shifts during seedling development, and the environmental heterogeneities between controlled and field conditions. In doing so, we propose avenues for methodological innovation and integrated frameworks for future research.

---

## 1. Introduction

Seedling functional traits serve as crucial indicators of plant performance, ecological adaptability, and restoration potential. While the measurement of these traits can provide insights into growth, survival, and ecosystem functioning, the methodological challenges are extensive and span instrumentation, sampling design, and data integration. This report synthesizes numerous research learnings—from the integration of machine learning (ML) techniques and advanced imaging systems to the critical role of intraspecific variability and ontogenetic changes—to provide an encompassing view on the obstacles and potential solutions in the field of seedling trait measurement.

## 2. Controlled Laboratory vs. Natural Field Environments

### 2.1 Heterogeneity in Environmental Conditions

The transition from controlled laboratory conditions to natural field environments represents one of the major methodological challenges. Controlled settings, such as glasshouse experiments with standardized protocols (e.g., randomized blocks in 10 cm pots with weekly repositioning), can minimize environmental variability and allow for reproducible measurements. However, extrapolating these results to heterogeneous field settings often involves increased uncertainties due to natural fluctuations in soil conditions, moisture, temperature, and biotic interactions. For example, studies in Mediterranean climates have shown that increases in seedling size and tissue nutrient concentration under controlled settings facilitate growth during the wet season, resulting in more extensive root systems—a phenomenon that may not be as clearly reproduced in field observations.

### 2.2 Trade-offs Between Throughput and Measurement Precision

High-throughput phenotyping systems are invaluable for generating large-scale datasets rapidly. Yet, inherent trade-offs exist: while throughput increases, precision often suffers due to the limitations in the sensitivity of available instrumentation. Controlled laboratory setups generally yield higher precision in quantifying morphological and biochemical traits, whereas field-based assessments must contend with variable signal-to-noise ratios and reduced instrumentation resolution.

## 3. Instrumentation and Measurement Techniques

### 3.1 Advanced Imaging Modalities

Modern phenotyping is propelled by advancements in imaging technologies. Techniques such as Magnetic Resonance Imaging (MRI), Positron Emission Tomography (PET), and hybrid systems like phenoPET (developed in collaboration with Philips Photon Counting and Forschungszentrum Jülich) allow for noninvasive, automated 3D reconstruction of plant architectures, including root system dynamics and carbon tracer transport. Such methods provide not only morphological data but also functional biochemical markers through the integration of luminescence reporters and PET tracers. These approaches are pivotal in both controlled and natural settings, yet the challenges lie in standardizing protocols across modalities and ensuring consistent data extraction.

### 3.2 2D vs. 3D Imaging Techniques

Traditional 2D imaging methods (e.g., visible light imaging in rhizotrons or high-resolution X-ray imaging) offer cost-effective and high-resolution data capture, but they inherently lack spatial depth. In contrast, 3D imaging modalities capture volumetric complexity and temporal dynamics that are critical for understanding the spatial configuration of root axes, lateral branching, and even dynamic responses under stress. The integration of 2D data with additional depth information—potentially using low-resolution 3D point clouds corrected through hyperspectral imaging techniques—presents a promising pathway for overcoming existing limitations.

### 3.3 Sensor-Specific Domain Shifts and Calibration

The use of sensors such as LiDAR in both laboratory and field settings introduces significant challenges related to domain shifts. Variations (e.g., differences in vertical scanning planes between 32 and 64 configurations) create input data distribution shifts that necessitate rigorous pre-training and deep domain adaptation. Calibration techniques and real-time adaptive optimization using ML frameworks are essential tools for aligning data distributions across different sensor configurations, thus ensuring that learned features from one setup can be transferred to another with minimal degradation in performance.

## 4. Sampling Design and Intraspecific Trait Variability (ITV)

### 4.1 Sampling Strategies and Trade-offs

Effective assessment of seedling functional traits requires careful sampling designs that capture both between- and within-individual variability. Hierarchical sampling approaches have been proposed, such as optimal schemes where 4 leaves from 10 individuals are sampled rather than a minimum of 5 leaves from 5 individuals. Such designs allow researchers to account for canopy stratification and local heterogeneities, ensuring that trait estimates are reflective of the true population variance. Studies on species such as Quercus ilex have successfully demonstrated that capturing canopy stratification is critical for accurately estimating trait variability.

### 4.2 Ontogenetic Changes and Developmental Shifts

Seedlings are not static entities: they undergo significant ontogenetic changes that can alter trait relationships and complicate measurement protocols. For traits like specific leaf area (SLA) or leaf nitrogen, the correspondence between laboratory-grown seedlings and field-grown adults can be relatively weak owing to developmental plasticity. This ontogenetic shift highlights the need for developmental stage-specific protocols that are integrated within trait-based models to accurately predict long-term plant performance and ecological outcomes.

### 4.3 Statistical Modelling and ML Integration

Numerous studies have integrated advanced statistical models and ML methods to deal with the variability inherent in seedling trait data. Models ranging from L1-regularized logistic regression, Random Forest, and Support Vector Machines (SVM) to ensemble approaches that combine Multi-Layer Perceptron (MLP), Radial Basis Function (RBF) networks, and genetic algorithm–optimized stacks have shown promise. The coupling of these models with high-quality imaging data and standardized protocols has enabled significant gains in prediction accuracy. However, achieving a balance between model complexity and computational efficiency remains a critical challenge.

## 5. Data Fusion and Integration Across Methodologies

### 5.1 Multi-sensor Data Fusion

The integration of multiple data sources is at the core of contemporary phenotyping efforts. Techniques for fusing hyperspectral imaging, LiDAR, and remote sensing data (e.g., from MODIS, Landsat, SPOT) have proven effective for generating trait maps that capture spatial and temporal variability at scales ranging from the cellular to the ecosystem level. Canonical correlation analysis and cross-modality representation learning are among the advanced techniques employed to reconcile differences in spectral, spatial, and structural variables. This fusion not only enhances the predictive power of individual sensors but also allows researchers to overcome localized data quality issues, particularly in heterogeneous field environments.

### 5.2 Real-Time Adaptive and Distributed Workflows

Large-scale experiments and phenotyping pipelines are increasingly utilizing distributed, real-time adaptive systems to manage petabyte-scale datasets. Tools such as FStream and Condor-based SWAMP platforms optimize communication and computational resources, thus enhancing throughput and reducing latency. These systems are essential for integrating high-throughput imaging with real-time calibration frameworks, as they enable dynamic adjustments based on online profiling and historical trends.

### 5.3 Integration of Biochemical and Morphological Data

Hybrid approaches that merge biochemical markers (e.g., luminescence reporters, PET tracers) with morphological measurements from imaging modalities enable more nuanced assessments of seedling performance. For instance, combining HPLC analysis for biochemical markers with 3D reconstructions of root architecture can provide insights into both the structural and functional aspects of seedling growth. This multimodal integration can resolve the trade-off between high-throughput measurements and the need for high-resolution, reproducible measurements, and it is especially promising for applications in restoration ecology and crop breeding.

## 6. Future Perspectives and Recommendations

### 6.1 Standardization and Protocol Harmonization

The push towards standardized protocols—as highlighted in recent handbooks for plant functional trait measurement—remains paramount. Despite progress in imaging and ML techniques, the reproducibility and resolution of trait quantification across labs and field sites require a concerted effort to harmonize methods. This includes integrating early-life stage measurements (seedling and germination traits) within existing frameworks used for mature plants.

### 6.2 Embracing Ontogenetic and Environmental Complexity

Any successful model for predicting seedling performance must account for both ontogenetic shifts and environmental filtering. Future research should focus on developing dynamic, multiscale models that explicitly incorporate the developmental trajectory of seedlings and the influence of local environmental conditions. Models such as Trait Driver Theory and hierarchical nonlinear growth models provide a starting point for such integration but require further refinement to capture the full breadth of variability observed in natural ecosystems.

### 6.3 Technology Integration and Advanced Analytics

The integration of cutting-edge technologies, including advanced imaging systems, ML-enhanced data fusion, and distributed computing, holds significant promise for overcoming many of the current methodological challenges. In particular, the expansion of ensemble ML methods and real-time adaptive pipeline frameworks will likely reduce the bottlenecks associated with high-throughput phenotyping. Researchers should continue to explore contrarian ideas such as incorporating remote sensing-derived trait maps and multi-trait deep learning models for genomic-enabled prediction, which can be particularly powerful when combined with classical measurement approaches.

### 6.4 Cross-Ecosystem Model Transferability

A persistent challenge is the cross-ecosystem transferability of controlled experimental results to varied field conditions. Targeting this gap demands extensive collaborations, integrated bioinformatics platforms, and the continuous calibration of models using both in situ and remote sensing data. Future studies should prioritize long-term field validations and multi-scale sampling designs that bridge the gap between controlled experiments and heterogeneous natural environments.

## 7. Conclusion

In summary, the methodological challenges in measuring seedling functional traits are manifold, encompassing issues from sensor calibration and 2D versus 3D imaging limitations to sampling design intricacies and ontogenetic variability. It is clear that integrated approaches—leveraging advanced ML techniques, adaptive imaging modalities, and robust statistical models—are essential for surmounting these obstacles. Establishing standardized protocols and dynamic data fusion frameworks will further enhance reproducibility and predictive power, thereby advancing our understanding of seedling ecophysiology. Moving forward, a synthesis of controlled experimentation and real-world validation stands as the cornerstone for future innovations in the field, with the ultimate goal of improving ecological restoration, crop performance prediction, and ecosystem management.

---

This comprehensive examination highlights both the current state of the art and the avenues for future development, underscoring the need for multi-disciplinary approaches and continuous methodological refinement in the study of seedling functional traits.


## Sources

- https://biblio.ugent.be/publication/8587837/file/8587936
- http://eprints.nottingham.ac.uk/35708/
- https://zenodo.org/record/7054485
- https://archives-publications.inrae.fr/398874.pdf
- http://hdl.handle.net/10255/dryad.130933
- https://doaj.org/toc/2095-7505
- https://hal.archives-ouvertes.fr/hal-01445186
- https://dx.doi.org/10.3390/s18041187
- https://doaj.org/article/97d94abb4e424abd8bff7aaea1aaa0b8
- http://home.mit.bme.hu/~eredics/documents/measurement09.pdf
- https://doaj.org/article/c08c5a7898f64a57af43de103f7548e9
- http://hdl.handle.net/11575/115191
- https://escholarship.org/uc/item/40v4x53m
- http://ezproxy.uws.edu.au/login?url=http://doi.org/10.5194/bg-10-5497-2013
- https://dx.doi.org/10.3390/s130912698
- http://hdl.handle.net/10255/dryad.220787
- https://hal.archives-ouvertes.fr/hal-00776389
- https://juser.fz-juelich.de/record/202330
- https://research.wur.nl/en/publications/close-range-hyperspectral-imaging-of-plants-a-review
- http://ir.iswc.ac.cn/handle/361005/4708
- http://repositorio.unicamp.br/jspui/handle/REPOSIP/320404
- http://hdl.handle.net/1957/10879
- https://doi.org/10.1023/B:PLSO.0000037029.82618.27
- https://doaj.org/article/5c52f2d6b83647c681ab4be26ef4ad75
- https://doaj.org/article/cacc739367374a5ea91db2d620181020
- http://limno.fcien.edu.uy/pdf/fito2008/clase4/Violle2007-LeT-
- http://apiolaza.net/uploads/Apiolaza_2009_ExploitingScales.pdf
- https://escholarship.org/uc/item/6kn9b59b
- https://ezproxy.uws.edu.au/login?url=https://doi.org/10.1071/BT12225
- https://hal.archives-ouvertes.fr/halsde-00288538
- https://dx.doi.org/10.3390/s16050641
- http://studentsrepo.um.edu.my/7761/1/thesis.pdf
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/42/b1/fpls-05-00770.PMC4299434.pdf
- https://doi.org/10.1038/s41598-017-18525-1
- http://scholar.ulethbridge.ca/chasmer/files/isrse_jajberni_final.pdf
- https://aaltodoc.aalto.fi/handle/123456789/47576
- https://juser.fz-juelich.de/search?p=id:%22FZJ-2022-00412%22
- https://biblio.ugent.be/publication/5776964/file/5776970
- http://era.daf.qld.gov.au/id/eprint/5056/
- http://hdl.handle.net/1957/42881
- https://biblio.ugent.be/publication/1978659/file/4168414
- https://research.vu.nl/en/publications/9d4c8a15-beac-4859-a16e-05bccd0e01ec
- https://doaj.org/article/93a4bf74faa44c3e9c6ceaa8631bc6fe
- https://researchonline.jcu.edu.au/63560/1/Engert%20et%20al%202020%20Functional%20trait%20representation%20differes%20between%20restoration%20plantings%20and%20mature%20tropical%20rainforest%20FEM.pdf
- https://hal.inrae.fr/hal-02738363/document
- https://researchrepository.murdoch.edu.au/view/author/Hu,
- http://geography.swan.ac.uk/silvilaser/papers/keynote_papers/Lucas.pdf
- http://hdl.handle.net/10255/dryad.49806
- http://library.wur.nl/WebQuery/wurpubs/398805
- https://digitalcommons.montclair.edu/compusci-facpubs/442
- http://hdl.handle.net/10255/dryad.222278
- http://hdl.handle.net/11858/00-001M-0000-000E-B985-F
- http://hdl.handle.net/2160/41280
- https://hal.archives-ouvertes.fr/hal-02324182
- https://www.frontiersin.org/research-topics/4419/phenomics
- https://hdl.handle.net/2027.42/155513
- http://hdl.handle.net/1807/109066
- https://eppn2020.plant-phenotyping.eu/index.php?index=121&event=PhenomicsWebinars
- https://hal-agrocampus-ouest.archives-ouvertes.fr/hal-01705938
- http://prodinra.inra.fr/record/430157
- http://hdl.handle.net/11343/194879
- http://prodinra.inra.fr/record/62970
- https://salford-repository.worktribe.com/file/1323200/1/Published%20Version
- http://hdl.handle.net/10255/dryad.100016
- https://research.wur.nl/en/publications/real-time-application-of-crop-transpiration-and-photosynthesis-mo
- https://doaj.org/article/012ed85d53604cb1b7d34299d3cdcd96
- https://figshare.com/articles/_Functional_knowledge_transfer_FKT_improves_prediction_accuracy_for_a_wide_range_of_state_of_the_art_classification_algorithms_/652956
- https://zenodo.org/record/6422463
- http://techreports.library.cornell.edu:8081/Dienst/UI/1.0/Display/cul.cs/TR98-1662
- http://www.nusl.cz/ntk/nusl-446251
- https://zenodo.org/record/8033473
- http://hdl.handle.net/10179/14853
- https://doaj.org/toc/1932-6203
- http://hdl.handle.net/10072/392021
- https://doi.org/10.1371/journal.pone.0176959.
- https://hal.inrae.fr/hal-03771427
- https://juser.fz-juelich.de/search?p=id:%22FZJ-2018-01164%22
- http://hdl.handle.net/10255/dryad.144090
- https://digitalcommons.unl.edu/dissertations/AAI29167763
- http://ir.ibcas.ac.cn/handle/2S10CLM1/20564
- http://scholar.ulethbridge.ca/chasmer/files/isrse_evavangorsel_la.pdf
- https://figshare.com/articles/The_effect_of_soil_origin_soil_type_and_their_interaction_on_the_number_of_seedlings_and_on_aboveground_and_belowground_biomass_of_different_dominant_species_in_feedback_experiment_/3460547
- http://hdl.handle.net/10.1184/r1/8175407.v1
- https://hdl.handle.net/10568/99155
- https://doaj.org/article/e05ce7c192e5480abbd49b406d13f829
- https://digitalcommons.unl.edu/dissertations/AAI28028389
- https://figshare.com/articles/Precision-mapping_and_statistical_validation_of_quantitative_trait_loci_by_machine_learning-3/82294
- https://hal.archives-ouvertes.fr/halsde-00377965
- https://juser.fz-juelich.de/search?p=id:%22FZJ-2022-02196%22
- https://zenodo.org/record/8322905
- https://doaj.org/article/8c81f25a835c47f9ace56ed7130e1105
- http://hdl.handle.net/1885/173141
- https://hal.archives-ouvertes.fr/hal-00684558
- http://resolver.tudelft.nl/uuid:cf2f814d-c954-49b8-b07e-dd436bed0992
- https://hal.science/hal-01606568/document
- http://edepot.wur.nl/40783
- http://resolver.tudelft.nl/uuid:618db181-4d0d-4384-a9b2-4c0a8925da4f
- https://escholarship.org/uc/item/32r2m9n5
- http://hdl.handle.net/10261/266596
- http://prodinra.inra.fr/ft/8E0A6E43-163B-42A3-BBA7-CE649F17C57B
- https://avesis.erciyes.edu.tr/publication/details/d3b2f41d-9136-40a1-a5d4-8121b497c84a/oai
- https://juser.fz-juelich.de/search?p=id:%22FZJ-2013-04090%22
- https://orgprints.org/id/eprint/41820/
- https://institut-agro-dijon.hal.science/hal-03279153
- http://repository.cshl.edu/id/eprint/30898/
- https://scholarworks.umt.edu/ntsg_pubs/176
- https://doaj.org/article/a997b97242c4463fbb40c9e657125853
- http://www.bucksch.nl/downloads/posterGRC.pdf
- https://figshare.com/articles/The_effects_of_soil_conditioning_by_each_dominant_species_on_plant_belowground_biomass_of_different_dominant_species_in_the_feedback_experiment_/3460514
- http://www.rbc-scau.cn/sites/files/2012-3D%20Quantification%20of%20Plant%20Root%20Architecture%20In%20Situ.pdf
- https://digitalcommons.pepperdine.edu/faculty_pubs/119
- http://hdl.handle.net/10.1371/journal.pone.0255848.g001
- http://prodinra.inra.fr/record/485780
- https://zenodo.org/record/4977501
- https://zenodo.org/record/6388114
- http://tesi.cab.unipd.it/63166/1/mariateresa_benato_tesi.pdf
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/51/c7/pone.0062794.PMC3633840.pdf
- http://hdl.handle.net/21.11116/0000-0003-9329-9
- http://edepot.wur.nl/319295
- https://research.rug.nl/en/publications/effects-of-light-and-nutrient-availability-on-drymatter-and-nallocation-in-6-successional-grassland-species--testing-for-resource-ratio-effects(069a4ac3-190a-46c5-802c-31d5f281115c).html
- https://doaj.org/article/25d82a33c89e4c46893194ad50a67360
- https://dx.doi.org/10.3390/s141120078
- http://edepot.wur.nl/9183
- http://hdl.handle.net/2078.1/186198
- https://hdl.handle.net/2144/32714
- https://hal.science/hal-01329331
- https://juser.fz-juelich.de/record/20846
- https://hal.science/hal-02411711
- https://hal.science/hal-00594009
- https://research.wur.nl/en/publications/combining-crop-growth-modeling-and-statistical-genetic-modeling-t
- https://doaj.org/article/37f52fd485ce4b8d83f87675b91b9995
- http://ir.ihb.ac.cn/handle/342005/19287
- https://library.wur.nl/WebQuery/wurpubs/541649
- https://juser.fz-juelich.de/record/860087
- http://edepot.wur.nl/363569
- http://datacite.org/schema/kernel-4
- https://hal.inria.fr/hal-01948568/document
- https://openrepository.ru/article?id=44660
- https://figshare.com/articles/Trait_drivers_theory_A_basis_to_integrate_and_scale_from_plant_form_function_and_strategies_to_ecosystems_worldwide/5328004
- http://digitool.Library.McGill.CA:80/R/?func=dbin-jump-full&object_id=40833
- http://eprints.nottingham.ac.uk/52603/
- http://orcid.org/0000-0002-2303-4583
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:98213
- http://dx.doi.org/10.1016/j.jaridenv.2017.12.013
- http://library.wur.nl/WebQuery/wurpubs/431905
- http://www.escience.cn/system/file?fileId%3D66733
- http://hdl.handle.net/2072/440433
- http://hdl.handle.net/11336/51006
- https://research.vu.nl/en/publications/b2923f6c-1426-4f64-986f-77cac7143cb0
- https://digitalcommons.butler.edu/urc/2018/biology/24
- https://hal.inrae.fr/hal-02713822/file/1995_Kergoat_Tellus_1.pdf
- http://handle.westernsydney.edu.au:8081/1959.7/uws:39606
- https://escholarship.org/uc/item/26w2t6wz
- http://dx.doi.org/10.1016/j.pedsph.2022.06.018
- https://juser.fz-juelich.de/record/188889
- http://hdl.handle.net/10255/dryad.49804
- https://orcid.org/0000-0002-7297-0984
- https://repository.upenn.edu/dissertations/AAI3109193
- https://research.wur.nl/en/publications/on-the-importance-of-root-traits-in-seedlings-of-tropical-tree-sp
- http://www.loc.gov/mods/v3
- https://eprints.lancs.ac.uk/id/eprint/51265/
- https://research-repository.st-andrews.ac.uk/bitstream/10023/26161/1/Liang_2021_FGCS_Scalable_Adaptive_Optimizations_AAM.pdf
- https://library.wur.nl/WebQuery/wurpubs/501767
- http://www.agriculture.purdue.edu/fnr/htirc/pdf/publications/DavisandJacobs2005.pdf
- https://doaj.org/article/8c85a11b599e4127878e3fd1e45eaa43
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/70/26/1471-2180-14-171.PMC4096534.pdf
- https://orbi.uliege.be/handle/2268/201403
- http://hdl.handle.net/10150/621413
- http://hdl.handle.net/1773/43659
- https://hal.inrae.fr/hal-04021038/document
- https://hal.inrae.fr/hal-03826576
- https://researchbank.rmit.edu.au/view/rmit:49356
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:99514
- https://www.eventbrite.co.uk/e/bmva-technical-meeting-plants-in-computer-vision-registration-24677394752#
- https://zenodo.org/record/7222002
- https://researchonline.jcu.edu.au/56584/1/56584_togashi_et_al_2018.pdf
- https://hal.inrae.fr/hal-03745940/document
- https://doaj.org/toc/1679-0359
- http://prodinra.inra.fr/record/411642
- http://hdl.handle.net/20.500.11937/88505
- http://hdl.handle.net/11858/00-001M-0000-0014-4BC6-8
- http://nbn-resolving.de/urn:nbn:de:bsz:352-2-h7p2u6ms06l01
- https://doaj.org/article/940f8c2e443c483c843acbc1698a3bb3
- https://espace.library.uq.edu.au/view/UQ:75eefa1
- https://library.wur.nl/ojs/index.php/FAIRdata2018/article/view/16266
- https://doaj.org/article/eb054b9738674d8f94a2c9dde312c8f1
- https://doaj.org/toc/2336-1964
- http://hdl.handle.net/11380/1150396
- https://digitalcommons.morris.umn.edu/biology/6
- http://hdl.handle.net/10255/dryad.129878
- https://doaj.org/article/61a5fbcea03a4aad96960206245acc3b
- https://arbor.bfh.ch/17205/
- http://hdl.handle.net/11383/1486702
- http://hdl.handle.net/1885/52646
- https://zenodo.org/record/4011755
- https://openscholarship.wustl.edu/cse_research/120
- https://hdl.handle.net/10807/230879
- http://hdl.handle.net/11714/7420
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:102319
- http://hdl.handle.net/10.6084/m9.figshare.7513685.v1
- https://hal.inrae.fr/hal-03432028
- http://dare.ubvu.vu.nl/bitstream/handle/1871/21464/162086.pdf%3Bjsessionid%3D9BA25E1FC05C82EAA891EDD7C4DEDE10?sequence%3D2
- https://doaj.org/article/71d4619bcdb640d7a113adab3b99d1f3
- http://hdl.handle.net/1885/57667
- https://espace.library.uq.edu.au/view/UQ:a8ecf92
- https://espace.library.uq.edu.au/view/UQ:390707
- https://espace.library.uq.edu.au/view/UQ:8890f8d
- https://doi.org/10.1051/agro:2003019
- http://hdl.handle.net/10.3389/fpls.2019.00015.s001
- http://hdl.handle.net/1822/68102
- https://eprints.lancs.ac.uk/id/eprint/62631/
- https://doaj.org/article/6756e1195b88482bb092ef06f9e3dff0
- https://hal.inria.fr/hal-01057325/file/frontiers.pdf
- https://hal.archives-ouvertes.fr/hal-03142169