# Final Report: Realistic Pesticide Ranges for Experiments on Pesticide Impacts on Bees

**Date:** 2025-06-03

---

## Table of Contents

1. [Introduction](#introduction)
2. [Conceptual Framework and Definitions](#conceptual-framework-and-definitions)
3. [Quantification of Bee Exposure: Advanced Dosimetry and Imaging Methods](#quantification-of-bee-exposure)
4. [Field-Realistic vs. Experimental Exposure: Dose Metrics and Exposure Routes](#field-vs-experimental)
5. [Integration of Modeling, Simulation, and Computational Approaches](#modeling-simulation)
6. [Species-Specific Responses and Behavioral Endpoints](#species-specific-responses)
7. [Mixture Synergies and Interaction Effects](#mixture-synergies)
8. [Environmental and Seasonal Modulation](#environmental-seasonal-modulation)
9. [Regulatory and Risk Assessment Implications](#regulatory-risk-assessment)
10. [Conclusions and Recommendations](#conclusions)

---

## 1. Introduction <a name="introduction"></a>

The determination of a realistic pesticide range for experiments assessing pesticide impacts on bees is a multi-faceted challenge that involves integrating field-realistic exposure data with laboratory-controlled experimental dosages. Researchers must account for both lethal and sublethal endpoints, different pesticide classes (with neonicotinoids, pyrethroids, organophosphates, and systemic agents among the common candidates), and a range of exposure routes including oral, contact, and systemic exposure via pollen and nectar. This report synthesizes decades of research advancements—including advanced imaging, dosimetry, computational modeling, and behavioral assessments—to provide a comprehensive framework that is both theoretically robust and practically applicable for experimental design.

---

## 2. Conceptual Framework and Definitions <a name="conceptual-framework-and-definitions"></a>

**Realistic Pesticide Range:** 

- **Field-Realistic Concentration Range:** Concentration levels typically found in agricultural settings. These range from extremely low sub-ng/bee levels (on the order of 0.01 to 1.0 ng/bee for some compounds) to exposures in the tens of ng/bee as documented in field studies (e.g., 1.62 to 35.77 ng/bee in orchard and Phacelia field trials).
- **Experimental Dosage Regimens:** These include controlled dosing protocols that mimic sublethal and lethal effects. Laboratory studies frequently deploy Potter-type tower application techniques to ensure repeatability. Experimental dosages are typically reported in units (ng/bee) that can be directly related to LD50 values and sublethal endpoints using advanced dosimetric conversions.

**Exposure Metrics:** 

- **Apparent Exposure Surface Area:** Derived from Potter-type tower spraying, measured at 1.05 cm²/bee.
- **Physical Exposure Surface Area:** Confirmed by X-tomography, measuring 3.27 cm²/bee, which helps in adjusting hazard quotient (HQ) calculations.

---

## 3. Quantification of Bee Exposure: Advanced Dosimetry and Imaging Methods <a name="quantification-of-bee-exposure"></a>

Recent breakthroughs in imaging and dosimetry have refined our understanding of pesticide exposure on an individual bee basis:

- **Potter-Type Tower Spraying:** Provides precise pesticide deposition metrics. The use of this method, combined with chemical residue quantification, has resulted in an *apparent exposure surface area* of 1.05 cm² per bee. This metric allows researchers to convert field application rates (g/ha) to dosages (ng/bee) and subsequently align risk assessments with EFSA and US EPA protocols.
- **X-Tomography:** With a measured physical surface area of 3.27 cm² per bee, X-tomography provides an independent validation method to correct for over- or underestimations in dosimetry. The reconciliation between the apparent (1.05 cm²/bee) and physical surface areas enables more accurate hazard quotient calculations.
- **Fluorescent Tracers:** Utilization of sodium-fluorescein and similar compounds has enhanced the spatial resolution with which pesticide deposition and transfer between surfaces can be monitored.

The synergy between imaging techniques and chemical analyses constitutes a robust framework to ensure that both in vivo and in silico models are calibrated appropriately for real-world exposures.

---

## 4. Field-Realistic vs. Experimental Exposure: Dose Metrics and Exposure Routes <a name="field-vs-experimental"></a>

Given that bee exposure is highly variable and context dependent, it is necessary to distinguish between field-realistic exposures and controlled experimental doses:

### Field-Realistic Exposures:

- **Dose Ranges:** Field trials (e.g., apple orchards and Phacelia fields from the early 1990s studies) report doses ranging from approximately 1.62 to 35.77 ng/bee. These values represent a realistic spectrum of exposure as bees encounter pesticide residues in situ.
- **Routes of Exposure:** Bees can be exposed through:
  - **Contact:** Direct deposition on the bee’s integument, predominantly measured using Potter-type tower protocols.
  - **Oral:** Ingesting contaminated nectar or pollen, where even very low doses (as low as 11 ng/bee/day for systemic pesticides like flupyradifurone) can result in chronic and sublethal behavioral effects.

### Experimental Dosages:

- **Controlled Regimens:** Experimental studies often apply doses that replicate observed field ranges while also testing higher concentrations to delineate thresholds for acute lethality (LD50 values for pyrethroids typically being ≤2 µg/bee for highly toxic compounds, and 2–11 µg/bee for moderate toxicity).
- **Sublethal Endpoints:** These include alterations in locomotion (with video tracking indicating reductions between 30–71%), impaired proboscis extension reflexes (PER), altered gas exchange in respiratory assays, and changes in social and foraging behaviors. The dose ranges are selected carefully—from low doses capable of revealing subtle behavioral changes to higher doses that produce overt toxicity in controlled settings.

The conversion of field pesticide rates (g/ha) to individual doses (ng/bee) via refined surface area calculations is critical. The revised hazard quotient (HQ) approach aligns dosage metrics with biologically significant endpoints and makes comparative risk assessments more consistent across species.

---

## 5. Integration of Modeling, Simulation, and Computational Approaches <a name="modeling-simulation"></a>

A significant trend in recent years has been the integration of multiple modeling and computational approaches to predict pesticide impacts, which include:

### Mechanistic and Agent-Based Models:

- **ApisRAM & BeePop+:** Detailed colony-level simulation tools designed to integrate foraging behavior, environmental stressors (e.g., weather, Varroa infestations) and pesticide mixtures over temporal scales. These models have been pivotal in revealing how colony dynamics link individual exposure doses to colony health outcomes.
- **BEEHAVE and Bee++:** Although initially developed using procedural frameworks like NetLogo, there is a movement towards object-oriented platforms (e.g., in C++) to allow more realistic landscape representations, modular incorporation of pesticide modules, and improved scalability.

### Advanced Statistical Methods and Machine Learning:

- **Bayesian Neural Networks & Bootstrapping:** These methods are employed to quantify both aleatory and epistemic uncertainty in exposure predictions and toxicological assessments.
- **Counter-Propagation Artificial Neural Networks (CPANN):** Employing up to 56 Dragon molecular descriptors, CPANN has shown great potential for predicting acute contact toxicity (LD50 values) and can be recalibrated for non-Apis species. Integration of QSAR, PNN, and GRNN models provides robust prediction capabilities with high sensitivity (up to 0.93) and specificity.
- **Hybrid Approaches:** Combining mechanistic fate models (such as CASCADE-TOXSWA) and dynamic population models with machine learning (e.g., using exposure data from the CartoExpo project) enables the creation of multi-scale, spatially explicit risk assessments.

### In Silico and Data Fusion Techniques:

- **High-Throughput Screening:** In silico chemoinformatics platforms facilitate rapid risk prioritization, reducing reliance on exhaustive in vivo assays when assessing hundreds of pesticides simultaneously.
- **Transfer Learning:** To accommodate species-specific differences (e.g., Apis mellifera vs. Bombus terrestris vs. Osmia bicornis), machine learning models are being adjusted to include ecological and behavioral descriptors that capture unique exposure pathways.

Together, these computational approaches create a layered modeling framework that integrates physical exposure data with colony- and landscape-level outcomes, thereby providing more nuanced and context-dependent toxicological predictions.

---

## 6. Species-Specific Responses and Behavioral Endpoints <a name="species-specific-responses"></a>

Worker-specific and species-specific variations are a cornerstone of modern pesticide risk assessment:

- **Species Variability:** Apis mellifera, Bombus terrestris, and Osmia bicornis each exhibit distinct foraging, nesting, and social behaviors, which influence exposure. For instance, Osmia may experience up to a near threefold increase in toxicity with clothianidin when combined with a fungicide like propiconazole.
- **Worker Type Differences:** Within colonies, differences are noted between foragers and in-hive bees. Foragers may experience higher susceptibility, sometimes up to fourfold, due to differences in contact exposures and physiological uptake.
- **Behavioral Assessments:** Advanced video-tracking systems (such as EthoVision XT) have been used to quantitatively measure sublethal effects, including reduced locomotion, altered foraging patterns, and impaired learning capabilities using assays like the proboscis extension reflex (PER) test.
- **Physiological and Molecular Markers:** Alterations in respiratory physiology (e.g., gas exchange rates) and molecular markers associated with nicotinic acetylcholine receptors provide critical sublethal endpoints. Genomic and transcriptomic responses also highlight differential detoxification pathways among species, which should be factored into dose-response experiments.

These findings emphasize the need to design experiments that account for dynamic differences in behavior and physiology, ensuring that exposure levels being tested reflect the complexity of real-world conditions.

---

## 7. Mixture Synergies and Interaction Effects <a name="mixture-synergies"></a>

A key insight from recent studies is the importance of chemical mixtures in modulating toxicity:

- **Synergistic Toxicity:** Studies report that concurrent exposure to neonicotinoids (e.g., clothianidin) with fungicides (e.g., propiconazole) can lead to additive or even synergistic lethal and sublethal effects in several bee species. One study noted nearly a threefold increase in clothianidin toxicity in Osmia bicornis when combined with propiconazole.
- **Other Interactions:** The presence of pyrethroids such as tau-fluvalinate can exacerbate neonicotinoid impacts, while synergistic interactions have also been observed with mixtures involving organophosphates and herbicides. These effects underscore the need to simulate realistic mixture exposures rather than testing single compounds in isolation.
- **Mechanistic Frameworks:** DEBtox and BeeGUTS are among the frameworks that integrate multi-exposure scenarios within their predictions, highlighting the need for comprehensive dose-response experiments that incorporate both the individual and combined effects of multiple agrochemicals.

For experimental design, it is recommended that both single-chemical and mixture studies are conducted to capture the full breadth of possible interactions, and that these analyses incorporate the adjusted HQ methodology based on refined dosimetry metrics.

---

## 8. Environmental and Seasonal Modulation <a name="environmental-seasonal-modulation"></a>

Pesticide toxicity in bees does not occur in a vacuum, and both environmental conditions and seasonal variations significantly affect outcomes:

- **Temporal Factors:** Field-realistic studies indicate that exposure impacts can vary dramatically between seasons. For example, flupyradifurone exerts pronounced sublethal effects in summer compared to spring, and effective doses (ED) for pesticides like thiamethoxam can shift considerably based on additional stressors such as Varroa mite infestations.
- **Weather and Landscape:** Models incorporating spatially explicit ecological parameters (e.g., using ALMaSS) demonstrate that fine-scale variations in weather and landscape physiognomy directly modify pesticide fate, transport, and bee exposure profiles. The emerging Effective Dose (ED) framework is particularly adept at decoupling treatment-induced effects from environmental interactions.

Experimental protocols must therefore incorporate environmental variability by simulating different weather regimes or using spatially diverse field sites to better capture real-world complexity.

---

## 9. Regulatory and Risk Assessment Implications <a name="regulatory-risk-assessment"></a>

One of the primary goals of refining pesticide exposure experiments is to translate laboratory findings into effective regulatory risk assessments:

- **Revised Hazard Quotient (HQ) Calculations:** Traditional HQ calculations based on ratios of field rates (g/ha) to LD50 (µg/bee) are being updated by converting field application rates into dose-based metrics (ng/bee). Integration of the apparent exposure surface area (1.05 cm²/bee) aligns HQ values with established standards by EFSA and US EPA.
- **Tiered Testing Frameworks:** The integration of high-throughput in vitro assays, in vitro-to-in vivo extrapolation (IVIVE), and pharmacokinetic modeling within tiered frameworks supports animal-sparing, risk-based approaches. This is reinforced by the adoption of integrated models such as BeePop+ and APisRAM that merge individual toxicity predictions with colony-level dynamics.
- **Computational and QSAR Models:** Utilization of QSAR and QSTR frameworks not only supports rapid screening of pesticide toxicity but also facilitates cross-species extrapolations. With stringent performance metrics (e.g., high sensitivity, specificity, and balanced accuracy), these computational models enhance decision-making for regulatory bodies.
- **Data Gaps:** Meta-analyses covering vast numbers of pesticides underscore significant data gaps, particularly in sublethal (71%) and combined toxicity effects (≈99%). Addressing these gaps is essential for an integrated, precautionary approach in risk assessment.

---

## 10. Conclusions and Recommendations <a name="conclusions"></a>

### Conclusions:

This report provides a detailed integration of advanced methodologies and multi-scale modeling approaches to define a realistic pesticide range for experimental studies assessing impacts on bees. Key conclusions include:

- **Precision Dosimetry:** The integration of Potter-type tower spraying and X-tomography establishes an apparent exposure surface area of 1.05 cm²/bee, critically refining the conversion of field application rates to ng/bee metrics.
- **Multi-Route Exposure:** Realistic experimental design must account for both oral (nectar and pollen contamination) and contact exposures. Behavioral endpoints, including altered foraging, reduced locomotion, and learning impairments, are reliable sublethal indicators.
- **Species and Worker Variation:** Differential exposure routes among bee species (Apis mellifera, Bombus terrestris, Osmia bicornis) necessitate species-specific calibration using advanced modeling (CPANN, QSAR) and in silico methods.
- **Chemical Mixtures:** Synergistic and antagonistic interactions among pesticides are common. Experimental rigs should simulate realistic pesticide mixtures rather than isolated exposures.
- **Environmental Context:** Seasonal variation and spatial heterogeneity (weather, landscape physiognomy) critically modulate toxicity outcomes. The use of effective dose (ED) frameworks and spatially explicit ecological models further refines risk assessment.
- **Regulatory Alignment:** Revised hazard quotient calculations that convert field rates into individual doses improve consistency with EFSA and US EPA risk assessments. This integrated framework supports regulation by incorporating both acute and chronic endpoints.

### Recommendations for Experimental Design:

1. **Dose Range Selection:** Base experimental pesticide doses on field-realistic exposure levels ranging from approximately 1.5 to 35 ng/bee for typical field conditions. For sublethal endpoints, consider doses as low as 0.01–1.0 ng/bee, while ensuring lethal endpoints are characterized using a tiered approach (e.g., LD50, LD90 determinations).

2. **Exposure Pathways:** Incorporate both contact and oral exposure routes. Utilize Potter-type tower applications for contact exposures and simulate oral dosing via spiked nectar or pollen formulations to mimic chronic exposure.

3. **Species Specificity:** Design experiments that include multiple bee species and worker types to account for differential sensitivities. Use agent-based models (ApisRAM, BeePop+) to simulate colony-level impacts and isolate species-specific responses.

4. **Mixture Studies:** Given the documented synergistic effects (e.g., clothianidin with propiconazole), incorporate mixture exposures at realistic ratios. Both additive and potentiation effects should be measured, with attention to both lethal and sublethal endpoints across species.

5. **Environmental Simulation:** Where feasible, simulate seasonal variability and environmental stressors (temperature, Varroa mite loads) using controlled chambers or field sites with diverse landscape characteristics. This will clarify how extrinsic factors modulate pesticide impact.

6. **Utilize Advanced Analytics:** Embrace statistical methods such as Bayesian modeling, machine learning meta-models, and QSAR techniques to validate experimental findings and predict outcomes across untested scenarios. Consider hybrid models integrating in vivo, in silico, and ex vivo data.

7. **Data Integration and Continuous Calibration:** Use advanced dosimetry combined with spatially resolved exposure mapping (e.g., CartoExpo methodologies) to provide constant calibration and real-time assessment of pesticide deposition. This ensures that experimental dosages remain representative of field conditions over time.

---

## Final Remarks

This comprehensive report underlines that a realistic pesticide range for bee experiments is not a fixed number but a continuum that must integrate laboratory dosimetry, field observations, and complex ecosystem interactions. Incorporating advanced imaging techniques, robust uncertainty quantification, multi-method assessment, and integrated simulation models provides a pathway to designing experiments that can inform both scientific inquiry and regulatory risk assessments. Future research should address current data gaps—particularly in sublethal and mixture toxicity research—to further refine these experimental ranges and enhance pollinator protection strategies.

By implementing the detailed recommendations herein, researchers and regulators can develop a more accurate and context-sensitive framework for assessing the impacts of pesticides on bee health, ensuring that both individual-level toxic effects and colony-level dynamics are fully captured.

---

*This report synthesizes all the learnings from previous research, offering both a state-of-the-art review of methodologies and actionable recommendations for designing experiments that simulate realistic bee pesticide exposures.*


## Sources

- http://hdl.handle.net/11390/1105626
- https://escholarship.org/uc/item/5xb5n20c
- http://nbn-resolving.de/urn:nbn:de:bsz:352-2-1ivbsukfdkqc47
- http://hdl.handle.net/11299/183475
- http://hdl.handle.net/11379/509098
- https://zenodo.org/record/824923
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/06/8a/pone.0077550.PMC3797043.pdf
- https://digitalcommons.unl.edu/entomologyfacpub/462
- https://hal.archives-ouvertes.fr/hal-01326560
- https://journal.fsst.ca/index.php/jsst/article/view/26
- https://doaj.org/article/064c33cefb214ef2a5ecb6f4d8bf14f7
- http://ageconsearch.umn.edu/record/277258
- http://resolver.sub.uni-goettingen.de/purl?gldocs-11858/10259
- https://www.sciencedirect.com/science/article/pii/S0160412019334221?via%3Dihub
- https://doaj.org/article/28b59eead76e423a88fd2ba74e4bcaa9
- https://figshare.com/articles/_Pesticide_residues_detected_in_treatment_combs_n_8202_8202_13_used_to_rear_worker_bees_in_experiments_/466572
- http://hdl.handle.net/10.3389/ftox.2022.981928.s001
- https://ojs.openagrar.de/index.php/JKA/article/view/1935
- http://dx.doi.org/10.3897/oneeco.6.e63653
- http://library.wur.nl/WebQuery/wurpubs/456250
- http://prodinra.inra.fr/record/264904
- https://escholarship.org/uc/item/0670x0mx
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/5e/7d/ukmss-49946.PMC3495159.pdf
- https://ojs.openagrar.de/index.php/JKA/article/view/10026
- https://www.wellbeingintlstudiesrepository.org/invrmod/2
- http://hdl.handle.net/Genomic
- http://library.wur.nl/WebQuery/wurpubs/343708
- http://prodinra.inra.fr/record/384589
- http://hdl.handle.net/11585/594085
- http://hdl.handle.net/10453/18214
- https://escholarship.org/uc/item/6ms9n181
- http://prodinra.inra.fr/record/198573
- www.beeplusplus.ca)
- http://doi.org/10.1371/journal.pone.0103592
- https://ojs.openagrar.de/index.php/JKA/article/view/5320
- http://prodinra.inra.fr/ft/1B5CAF94-FF1D-4A0F-B18D-7EFDA0739741
- https://zenodo.org/record/5710735
- http://hdl.handle.net/10.1371/journal.pone.0213249.g003
- https://hal.science/hal-01826153
- https://hal.archives-ouvertes.fr/hal-02411819
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/3b/f5/pone.0094482.PMC3981812.pdf
- https://doaj.org/article/9b083028e4cb4a24b7173f8701073191
- http://nbn-resolving.de/urn:nbn:de:bsz:352-2--pe5kpp1b39us2
- http://hdl.handle.net/Classification
- http://dx.doi.org/10.1038/s41559-023-01990-5
- https://escholarship.org/uc/item/5r9312mk
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/a7/6a/pone.0113728.PMC4239102.pdf
- https://figshare.com/articles/_Comparison_of_the_exposure_and_physical_surface_area_of_a_bee_/1247978
- http://annhyg.oxfordjournals.org/content/48/6/519.full.pdf
- https://eprints.lancs.ac.uk/id/eprint/80241/
- https://hal.inrae.fr/hal-03291190
- https://doaj.org/article/07e5b39712364bcf82800fb5440f9e93
- https://doaj.org/article/bb28c7b4621a49fa8a2942d4e2d7625e
- http://publica.fraunhofer.de/documents/N-391848.html
- http://dx.doi.org/10.1016/j.chemosphere.2020.128518
- https://ojs.openagrar.de/index.php/JKA/article/view/5312
- https://repository.rothamsted.ac.uk/item/8qz46/beehave-a-systems-model-of-honeybee-colony-dynamics-and-foraging-to-explore-multifactorial-causes-of-colony-failure
- http://ir.nhri.org.tw/handle/3990099045/15288
- https://hal.archives-ouvertes.fr/hal-03362566
- https://www.repository.cam.ac.uk/handle/1810/358720
- https://doaj.org/toc/2075-4450
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/ae/7b/etc0033-0719.PMC4312970.pdf
- https://research.sabanciuniv.edu/id/eprint/43746/
- http://hdl.handle.net/2263/66275
- http://hdl.handle.net/10255/dryad.146750
- http://prodinra.inra.fr/record/279343
- https://eprints.lancs.ac.uk/id/eprint/83275/
- http://hdl.handle.net/10468/9147
- https://hal.archives-ouvertes.fr/hal-00318756
- https://escholarship.org/uc/item/4577m58c
- https://dspace.library.uu.nl/handle/1874/35840
- https://hal.archives-ouvertes.fr/hal-02994660
- http://hdl.handle.net/10150/555565
- https://figshare.com/articles/_Comparison_of_current_A_and_proposed_B_toxicity_testing_paradigms_/434379
- http://www.bulletinofinsectology.org/pdfarticles/vol66-2013-001-009matsumoto.pdf
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:97564
- https://www.apidologie.org/10.1051/apido:19970610/pdf
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0304380013002895/MAIN/application/pdf/182a5a9911850a167195db39975850e1/main.pdf
- https://www.zora.uzh.ch/id/eprint/212642/1/EFS2-19-e06607.pdf
- https://www.sciencedirect.com/science/article/pii/S0048969722039547
- https://discovery.ucl.ac.uk/id/eprint/10091077/
- http://www.cdpr.ca.gov/docs/risk/rcd/chlorpyr.pdf
- https://doaj.org/article/73cc393ede7840caa3d59760e33da510
- http://creativecommons.org/licenses/by-nc-nd/3.0/us/
- https://dx.doi.org/10.1111/1365-2664.12792
- https://digitalcommons.unl.edu/entomologyfacpub/608
- http://hdl.handle.net/2142/97773
- https://figshare.com/articles/Using_a_Hazard_Quotient_to_Evaluate_Pesticide_Residues_Detected_in_Pollen_Trapped_from_Honey_Bees_Apis_mellifera_in_Connecticut_/823812
- https://dspace.library.uu.nl/handle/1874/408980
- http://www.loc.gov/mods/v3
- https://doaj.org/article/a3b9015411944641807433adcf9a519d
- https://zenodo.org/record/4141779
- http://hdl.handle.net/20.500.11794/40169
- https://regsci-ojs-tamu.tdl.org/regsci/article/view/216
- https://research.sabanciuniv.edu/id/eprint/42946/
- http://hdl.handle.net/10255/dryad.182455
- https://digitalcommons.unl.edu/entomologyfacpub/377
- https://figshare.com/articles/Dataset_pesticide_risk_assessment_in_the_honey_bee/1222839
- https://lup.lub.lu.se/record/775d0a64-472f-4839-9376-fe4dcedcc1df
- https://figshare.com/articles/_Determination_of_the_exposure_surface_area_per_bee_for_each_active_substance_/1247982
- https://doi.org/10.1002/wcms.1516
- https://library.wur.nl/WebQuery/wurpubs/548375
- https://figshare.com/articles/Aquatic_Exposure_Predictions_of_Insecticide_Field_Concentrations_Using_a_Multimedia_Mass_Balance_Model/3101440
- https://hal.science/hal-03868878/document
- https://figshare.com/articles/Modeling_Effects_of_Honeybee_Behaviors_on_the_Distribution_of_Pesticide_in_Nectar_within_a_Hive_and_Resultant_in-Hive_Exposure/5045092
- www.elsevier.com/inca/publications/store/4/0/5/8/5/3
- http://hdl.handle.net/10197/12306
- http://hdl.handle.net/10255/dryad.146217
- https://espace.library.uq.edu.au/view/UQ:382988
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877343513000493/MAIN/application/pdf/db930e82d61db92ba561c622fa250ca3/main.pdf
- http://www.ent.uga.edu/bees/personnel/documents/PLOSONE_Field-LevelSublethalEffectsofApprovedBeeHiveChemicalsonHoneyBees.pdf
- https://dspace.library.uu.nl/handle/1874/408979
- https://hal.archives-ouvertes.fr/hal-01504455
- https://serval.unil.ch/notice/serval:BIB_1596B54D65A3
- http://publica.fraunhofer.de/documents/PX-8300.html
- https://hal-ineris.archives-ouvertes.fr/ineris-01853555
- https://doaj.org/article/f7235b9d96134085b65236cbdaba491d
- http://thescipub.com/PDF/ajessp.2006.33.40.pdf
- http://nbn-resolving.de/urn:nbn:de:bsz:352-2-149wcgv6cisgi6
- https://univ-rennes.hal.science/hal-01477203/file/Quantifying%20exposure%20of%20wild%20bumblebees_accepted.pdf
- https://hal.inrae.fr/hal-02627625
- https://zenodo.org/record/5217630
- https://doaj.org/article/1b498516a11a4c878b9aef10b6b4975b
- http://edepot.wur.nl/199846
- https://doi.org/10.2903/j.efsa.2021.6607
- https://doaj.org/toc/1932-6203
- https://zenodo.org/record/6037714
- http://hdl.handle.net/11585/571464
- https://espace.library.uq.edu.au/view/UQ:5be5b31
- https://figshare.com/articles/A_Pragmatic_Approach_to_Assess_the_Exposure_of_the_Honey_Bee_Apis_mellifera_When_Subjected_to_Pesticide_Spray/1247984
- https://figshare.com/articles/High_Throughput_Models_for_Exposure_Based_Chemical_Prioritization_in_the_ExpoCast_Project/2390248
- https://hal.archives-ouvertes.fr/hal-02994667/document
- http://hdl.handle.net/1959.14/282567
- http://annhyg.oxfordjournals.org/content/50/1/75.full.pdf
- https://escholarship.org/uc/item/6ds6j4h5
- http://hdl.handle.net/11588/556409
- https://doi.org/10.3897/fmj.4.107849
- http://hdl.handle.net/11380/1151494
- http://hdl.handle.net/10150/276577
- https://digitalcommons.unl.edu/cgi/viewcontent.cgi?article=1856&amp;context=entomologyfacpub
- https://research.wur.nl/en/publications/beegutsa-toxicokinetictoxicodynamic-model-for-the-interpretation-
- http://hdl.handle.net/1773/49289
- https://figshare.com/articles/_Determination_and_comparison_of_the_HQ_and_the_revisited_HQ_/1247983
- http://dx.doi.org/10.1371/journal.pone.0136928
- http://pub.jki.bund.de/index.php/JKA/article/download/1932/2308/
- https://ojs.openagrar.de/index.php/JKA/article/view/5317
- https://figshare.com/articles/QSTR_Modeling_for_Qualitative_and_Quantitative_Toxicity_Predictions_of_Diverse_Chemical_Pesticides_in_Honey_Bee_for_Regulatory_Purposes/2255158
- https://hal-ineris.archives-ouvertes.fr/ineris-03229712
- https://escholarship.org/uc/item/7v96b2dx