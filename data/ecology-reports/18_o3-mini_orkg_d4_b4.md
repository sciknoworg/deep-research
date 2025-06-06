# The Utility of Herbarium Specimens in Assessing Climate Change Impacts: Integrative Methodologies, Advances, and Future Directions

This report synthesizes decades of research and the latest innovations, drawing on advanced digitization, machine learning (ML), remote sensing, and integrative Bayesian and process-based models to answer the central question: Can herbaria specimens be used to study the effects of climate change? The evidence presented herein is derived from a comprehensive review of studies that integrate morphological, phenological, and geographic data, alongside climate data (e.g., temperature extremes, precipitation patterns, and atmospheric CO₂ levels).

---

## 1. Introduction

Herbaria have long been repositories of plant specimens, curated over centuries. With the advent of modern digitization and analytical techniques, these collections are now being repurposed to document climate-induced changes in phenology, morphology, and geographic distributions. Their extensive temporal coverage and global geographic extent make them invaluable for understanding the long‐term responses of flora to environmental change. Recent research leverages integrative approaches—combining remote sensing, ML, and innovative statistical modeling—to overcome limitations imposed by spatial and temporal biases in collection data.

---

## 2. Methodological Advances in Integrating Herbarium Data

### 2.1 Digitization and Image Analysis

Modern digitization workflows at institutions such as the Naturalis Biodiversity Center and the Natural History Museum (NHM) London have transformed traditional herbaria into digital datasets consisting of millions of high-resolution images. Modular machine learning workflows have been developed to segment specimen images, extract morphological traits, and score phenological stages:

- **Automated Image Segmentation:** Deep learning models, such as CNNs and mask R-CNN, have been employed to automatically segment plant organs and count reproductive structures. For example, studies on *Streptanthus tortuosus* showed that while reproductive organs might be undercounted, the derived phenological index (PI) closely matches manual annotations.
- **Optical Character Recognition and Natural Language Processing:** Techniques such as OCR and NLP have enabled the automated transcription of specimen labels, thus enriching the associated metadata and linking them with climate records.
- **Quality Control and Audit Trails:** Digitization initiatives now incorporate strict quality control protocols (with error rates below 1%) to ensure data integrity and facilitate reproducibility across vast collections.

### 2.2 Integrative Statistical and Machine Learning Models

Advances in statistical techniques and ML have enhanced the utility of herbarium data:

- **Bayesian Inference and Ensemble Modeling:** Methods employing Bayesian hierarchical frameworks address uncertainties, mitigating issues associated with spatial displacement and phenological biases. These models, applied in studies from Norway spruce budburst projections to Silene acaulis climate niche reconstructions, calibrate historical data against modeled climate scenarios.
- **Decision Trees, Random Forests, and Gradient Forests:** Comparative studies indicate that extreme climatic events (rather than averaged data) provide superior inputs for predicting shifts in plant communities. These models have shown high sensitivity to temperature, precipitation, and CO₂ levels, effectively capturing nonlinear responses.
- **Adversarial Domain Adaptation and Causal Graphs:** To improve interpretability and accuracy, explainable AI (xAI) techniques such as LIME have been used to elucidate variable importances and causal effects in complex networks integrating both herbarium and climate data.

---

## 3. Integrating Diverse Data Streams: From Herbaria to Remote Sensing

### 3.1 Remote Sensing Synergies

The integration of herbarium data with remote sensing has created robust spatial-temporal phenology models:

- **Multi-Channel Digital Imagery:** Studies leveraging RGB channels from remote sensing platforms in ecosystems like the cerrado savanna have demonstrated automated detection of phenological patterns (e.g., changes in leaf color) with increased accuracy during extreme daytime hours.
- **High-Resolution Climate Datasets:** Matched with climate products (e.g., PRISM, ClimateNA, ERA5-Land), herbarium specimens serve as ground-truthing tools that enhance the calibration of satellite-derived climatic estimates. Such integrations enable the construction of high-resolution, unified phenology prediction models that are crucial for both climate impact assessments and adaptive management strategies.

### 3.2 Coupling with Genetic and Phylogenetic Data

The convergence of historical phenotypic records, genomic analyses, and digital specimen imagery facilitates:

- **Genomic Adaptation Models:** Using methods like canonical analysis of principal coordinates, researchers have quantified the genomic responses of species such as *Eucalyptus tricarpa* to climate stressors like aridity. These studies underpin assisted migration and genetic augmentation strategies.
- **Integrated Phenomic Pipelines:** Next-generation AI frameworks are now capable of converting heterogeneous multi-scale datasets into ML-ready formats. For example, the NSF’s GenoPhenoEnvo projects illustrate how biological knowledge graphs and ontologies bridge phenological data with rapid genetic barcoding, refining predictions of future species distributions.

---

## 4. Addressing Biases and Enhancing Data Reliability

Despite their value, herbarium collections come with inherent biases. Several strategies are now employed to mitigate these issues:

### 4.1 Spatial and Temporal Discrepancies

- **Spatial Uncertainty and Bayesian Adjustments:** Research indicates that spatial uncertainties, such as simulated geographic displacements (e.g., in *Nemophila menziesii*), can weaken phenological sensitivity estimates. Consequently, advanced Bayesian frameworks have been developed to incorporate these uncertainties explicitly as random effects, thus preserving the integrity of derived climate signals.
- **Temporal Gaps and Calibration:** Space-for-time substitution methods, coupled with robust statistical models, bridge the gap between historical phenological records and contemporary remote sensing observations. This calibrated approach reveals trends such as the average advancement of flowering dates (commonly documented as approximately 2.4 days per °C increase) in diverse regions ranging from North America to South Africa.

### 4.2 Standardization of Data Collection and Annotation

- **Consensus Protocols and Darwin Core Extensions:** Standardized protocols (e.g., Extended MeasurementOrFact) for scoring phenological stages have minimized historical inconsistencies, enabling aggregation across diverse collections. Collaborative initiatives like iDigBio and GBIF continue to refine these standards.
- **Interoperable Digital Specimen Architectures:** Infrastructures such as DiSSCo and platforms like Cordra leverage FAIR data principles, ensuring persistent, flexible links between disparate data objects (images, 3D models, genetic data) and promoting global data interoperability.

---

## 5. Case Studies and Application Examples

### 5.1 Phenological Shifts in Flowering Time

Herbarium specimens have robustly documented phenological changes linked to climate change. For instance:

- **North American Studies:** Over 141 species observed across 116,000 km² exhibit an average shift of 2.4 days per °C increase. Comparative analyses with field observations report high congruence (r up to 0.91) in peak flowering dates.
- **South African Pelargonium:** An increase in mean annual temperature of approximately 2.9°C was linked with an 11.6-day advancement in flowering, highlighting regional variation and responsiveness to climatic drivers.
- **Estonian Ranunculaceae:** Documented advances in flowering times over more than a century underscore how herbarium records can track long-term ecological trends.

### 5.2 Morphological Adaptations

Morphological changes, such as those observed in *Plantago lanceolata* in Kyiv, reveal that climate factors have contributed to increased leaf blade, petiole, and spike dimensions. Co-inertia analyses attribute up to 34% of these changes to rising temperatures during key developmental phases, suggesting a strong evolutionary pressure induced by climatic warming.

### 5.3 Integrated Agro-Climatic and Weed Management

Beyond natural ecosystems, herbarium data combined with high-resolution agro-climatic datasets have illuminated the dynamic responses of weed species under climate change. Elevated CO₂ and temperature regimes have modified physiological traits—such as phenotypic plasticity, flowering behaviors, and herbicide efficacy—in weed species. Mechanistic models that incorporate local-scale climate projections are increasingly used to guide adaptive management strategies in agricultural systems.

---

## 6. Future Directions and Emerging Technologies

The field is moving toward increasingly integrative and multidimensional models. Some promising avenues include:

### 6.1 Advanced Machine Learning and HPC Integration

- **Modular and Scalable ML Pipelines:** Next-generation workflows integrate high-throughput genomic and phenomic data within HPC and big data frameworks (e.g., Galaxy-based Specimen Data Refinery) to simultaneously process millions of specimen images and climate records.
- **Hybrid Bayesian-ML Models:** The blending of causal graphs, ensemble predictors, and mechanistic simulation models will enhance our ability to predict climate-induced changes by incorporating both ecological and evolutionary data.

### 6.2 Expanded Data Streams and Global Collaborations

- **Citizen Science and Time-Lapse Cameras:** Combining herbarium records with citizen science initiatives (e.g., Season Spotter) and near-surface time-lapse imagery will fortify models by providing additional, high-resolution phenological snapshots.
- **Standardization Across Global Repositories:** Global collaboration networks (IPDES, DiSSCo, EOSC) are standardizing data models to foster interoperable digital ecosystems, essential for precise, species-specific, and regionally nuanced climate impact assessments.

### 6.3 Enhanced Predictive and Adaptive Models

- **Process-Based and Phenomic Models:** Integrative frameworks that merge process-based models (capturing soil type, water holding capacity, and microclimate) with digitized specimen data will refine predictions on plant demographics and range shifts.
- **Adaptive Genomic Modeling:** Community-level genomic inquiries, employing gradient forests and generalized dissimilarity models, will further disentangle the complex genotype–environment interactions driving adaptive responses to climate change.

---

## 7. Conclusion

Herbarium specimens, combining centuries of biological records with modern digitization and analytical techniques, provide an unparalleled window into the historical and ongoing impacts of climate change on plant phenology, morphology, and distribution. Integrative approaches combining remote sensing, ML, Bayesian statistics, and genomic tools are pushing the boundaries of our understanding. Despite inherent biases—whether temporal, spatial, or taxonomic—the continued refinement and standardization of methodologies promise to enhance the accuracy and predictive capabilities of climate-ecology models.

Continued investment in digitization, global data integration, and innovative modeling will ensure that herbaria remain a cornerstone for climate change research, informing both conservation strategies and adaptive management practices in our rapidly changing world.

---

*This report draws on a range of studies and learnings, outlining methodological innovations and interdisciplinary approaches that exemplify the emerging frontier in herbarium-based climate change research.*

## Sources

- https://doaj.org/toc/1683-1470
- https://zenodo.org/record/3524263
- http://nrs.harvard.edu/urn-3:HUL.InstRepos:22812360
- https://zenodo.org/record/5773353
- http://dx.doi.org/10.1111/mec.12751
- https://scholarworks.umt.edu/ntsg_pubs/148
- http://www.assessment.ucar.edu/uncertainty_models/BayesREA.pdf
- https://hal.umontpellier.fr/hal-02573627
- http://handle.unsw.edu.au/1959.4/44260
- http://hdl.handle.net/10.6084/m9.figshare.7163417.v1
- https://zenodo.org/record/3256841
- http://hdl.handle.net/10255/dryad.188432
- http://hdl.handle.net/10150/625772
- http://hdl.handle.net/21.11116/0000-000A-6B87-6
- https://escholarship.org/uc/item/03n7n0nh
- https://crossworks.holycross.edu/cgi/viewcontent.cgi?article=1005&amp;context=bio_fac_scholarship
- https://www.aaai.org/Papers/Symposia/Spring/2008/SS-08-05/SS08-05-005.pdf
- https://www.webofscience.com/api/gateway?GWVersion=2&SrcApp=PARTNER_APP&SrcAuth=LinksAMR&KeyUT=WOS:000396241600001&DestLinkType=FullRecord&DestApp=ALL_WOS&UsrCustomerID=42fe17854fe8be72a22db98beb5d2208
- http://discovery.ucl.ac.uk/1507980/
- https://zenodo.org/record/2566688
- https://zenodo.org/record/1254702
- https://zenodo.org/record/5542857
- https://cedar.wwu.edu/wwuet/202
- https://link.springer.com/article/10.1007/s00477-017-1383-2
- https://zenodo.org/record/7714545
- http://nbn-resolving.de/urn:nbn:de:bsz:352-2-ljyn1nhcdg7o2
- https://figshare.com/articles/_The_effect_of_climatic_covariates_PCA_axes_1_and_2_representing_temperature_and_precipitation_effects_respectively_competition_herbivory_and_plant_range_type_on_the_different_variables_of_plant_performance_measured_in_the_Botanical_Gardens_/1223871
- https://espace.library.uq.edu.au/view/UQ:b5b1e74
- http://hdl.handle.net/20.500.11897/458955
- https://doaj.org/article/1ea9b6e8319d45f3ae6f6c27b2210cec
- https://zenodo.org/record/3289110
- https://zenodo.org/record/4097657
- https://hal.inrae.fr/hal-03338823/file/Goeau_etal_BISS_2021_5_73751.pdf
- https://uknowledge.uky.edu/pss_etds/152
- https://zenodo.org/record/901379
- https://doaj.org/article/64a8c3caa4424bda8c46415086845e7a
- http://prodinra.inra.fr/record/436174
- https://library.wur.nl/WebQuery/wurpubs/552868
- https://doaj.org/article/754d5ae487a54761a5b5d348a6098a54
- https://doaj.org/article/513fa75441e44b12ab57075d6d3886ee
- https://escholarship.org/uc/item/8h53k6rz
- http://nrs.harvard.edu/urn-3:HUL.InstRepos:37160407
- http://hdl.handle.net/10255/dryad.62554
- https://zenodo.org/record/8323153
- https://doi.org/10.3897/BDJ.11.e109439
- http://hdl.handle.net/10871/127574
- https://doaj.org/article/6db0a310e35c4a24907b1229bec70a0c
- https://stars.library.ucf.edu/etd2020/1802
- https://doaj.org/article/128b0900c31f41c98b197deed3328738
- https://zenodo.org/record/1294438
- https://oist.repo.nii.ac.jp/?action=repository_uri&item_id=1876
- https://zenodo.org/record/4439518
- http://www.trend.org.au/sites/default/files/McGillivray_Ch_19.pdf
- http://biology.mcgill.ca/faculty/davies/pdfs/Cook%20et%20al.%202012.pdf
- http://hdl.handle.net/10150/644802
- http://hdl.handle.net/2142/110680
- https://repository.rothamsted.ac.uk/item/8qv48/a-process-based-approach-to-modelling-impacts-of-climate-change-on-the-damage-niche-of-an-agricultural-weed
- http://dx.doi.org/10.1016/j.scitotenv.2019.03.353
- https://zenodo.org/record/8264651
- https://doi.org/10.1111/gcb.12023.
- https://escholarship.org/uc/item/56b0f8xc
- http://hdl.handle.net/10852/93638
- http://hdl.handle.net/10.3389/fpls.2019.00529.s001
- https://dx.doi.org/10.3390/rs8090726
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.64.9165
- https://escholarship.org/uc/item/3j22c19z
- https://www.zora.uzh.ch/104103
- https://escholarship.org/uc/item/1tv2q8jm
- https://oasis.postech.ac.kr/handle/2014.oak/15555
- https://ojs.aaai.org/index.php/AAAI/article/view/17750
- http://ceur-ws.org/Vol-1598/paper14.pdf
- https://hal.inria.fr/hal-03454183/document
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/f4/6f/ele0016-1037.PMC3806244.pdf
- https://doaj.org/toc/2194-9034
- http://acervodigital.unesp.br/handle/11449/73807
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S221466281630024X/MAIN/application/pdf/e9d65fbca4ac177460c0d1e16d90bc0e/main.pdf
- https://zenodo.org/record/7576852
- https://zenodo.org/record/3261922
- http://dx.doi.org/10.1002/ece3.3476
- https://zenodo.org/record/5520329
- http://doc.rero.ch/record/328164/files/fla_egi.pdf
- https://www.intechopen.com/books
- https://pure.knaw.nl/portal/en/publications/c2d3501c-ade8-4f66-95aa-c1266ce68990
- https://researchrepository.murdoch.edu.au/view/author/Hu,
- https://doi.org/10.3897/bdj.11.e109439
- https://zenodo.org/record/3738810
- https://doaj.org/article/c39f163f230c44e1a87844ba1e65b5bf
- https://zenodo.org/record/8331989
- https://www.researchgate.net/profile/Alexander_Buyantuyev/publication/233909773_A_Space-For-Time_%28SFT%29_Substitution_Approach_to_Studying_Historical_Phenological_Changes_in_Urban_Environment/links/0fcfd50d1a580f1008000000.pdf
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:104077
- https://dx.doi.org/10.3390/cli4020024
- https://digitalcommons.du.edu/duurj/vol2/iss1/4
- http://resolver.tudelft.nl/uuid:ab8f569c-3d3b-40ee-a3a7-97e8c34ac1c1
- https://hdl.handle.net/10449/82375
- http://hdl.handle.net/10.1371/journal.pclm.0000320.g005
- https://zenodo.org/record/7233688
- https://zenodo.org/record/5809606
- https://figshare.com/articles/Data_from_Estimating_Uncertainty_in_Daily_Weather_Interpolations_a_Bayesian_Framework_for_Developing_Climate_Surfaces/3997116
- https://zenodo.org/record/1141
- http://hdl.handle.net/10068/939937
- https://zenodo.org/record/8091525
- https://zenodo.org/record/6955218
- https://hal.science/hal-03097366/document
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1369526613000022/MAIN/application/pdf/c98d67768dc5c52e085654ce73d9e87d/main.pdf
- http://ir.ibcas.ac.cn/handle/2S10CLM1/19559
- http://hdl.handle.net/10.3389/fpls.2019.00529.s002
- http://dx.doi.org/10.1111/j.1365-2486.2011.02515.x
- https://hdl.handle.net/20.500.11766/12383
- https://api.elsevier.com/content/abstract/scopus_id/85067510759
- https://doaj.org/toc/2224-4263
- http://eprints.whiterose.ac.uk/124176/8/1-s2.0-S2452074817301398-main.pdf
- https://escholarship.org/uc/item/3s12x2p1
- https://digitalcommons.lsu.edu/biosci_pubs/4035
- https://doi.org/10.1111/bij.12515
- https://journal.fi/afs/article/view/6321
- http://hdl.handle.net/11025/42982
- http://link.springer.com/article/10.1007/s00477-017-1383-2
- https://zenodo.org/record/6463977
- https://doaj.org/article/b823664ef3a24b55aff829976d1496c8
- https://zenodo.org/record/3975829
- http://hdl.handle.net/1893/28786
- https://zenodo.org/record/6416650
- https://repository.publisso.de/resource/frl:6430220
- https://escholarship.org/uc/item/3nw8s4d0
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.76.1308
- https://zenodo.org/record/4961727
- https://zenodo.org/record/1140551
- http://hdl.handle.net/10261/199334
- http://agritrop.cirad.fr/597012/
- https://zenodo.org/record/7434336
- https://hal.archives-ouvertes.fr/hal-03800621
- http://hdl.handle.net/10492/7412
- https://epublications.marquette.edu/liana_articles/696
- https://doaj.org/article/d028e549ccab416bb81e2f185bd0601e