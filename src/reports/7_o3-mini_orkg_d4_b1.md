# Final Report on Realistic Pesticide Ranges for Bee Impact Experiments

## Introduction

The challenge of determining a realistic pesticide exposure range for bee experiments requires integration of multi-scale, multi-disciplinary approaches. This report synthesizes multiple research learnings, covering chemical exposures, exposure simulations, agent-based and mechanistic models, and experimental validations. It also addresses experimental design implications regarding chronic vs. acute exposures and the multifaceted impacts on bee physiology, behavior, and colony health. This discussion is framed for experiments targeting common pesticides and pesticide classes (e.g., neonicotinoids such as imidacloprid, glyphosate as a representative herbicide, and fungicides like difenoconazole) and considers recent methodological advances, including physical determinations using Potter-type towers and X-tomography, coupled with advanced simulation tools.

## Background and Motivation for Pesticide Range Selection

Recent integrated studies have underscored the role of chronic, low-level exposures in modulating pesticide impacts on bees. For example, environmental concentrations as low as 0.01 and 0.1 μg/L of imidacloprid have been shown to affect bee survival and physiological traits within a window of 7 to 30 days. Such sub-lethal doses, in conjunction with mixtures that include herbicides and fungicides, create complex interaction landscapes, reinforcing the need for realistic pesticide ranges that incorporate cumulative and synergistic stressor effects.

### Key Considerations

1. **Chemical Mixtures and Sequential Exposures**: Sequential pre-exposure studies highlight that chronic pre-exposure to compounds such as imidacloprid and glyphosate can modulate the toxicity of subsequent exposures, as seen with difenoconazole. This stresses the importance of considering both primary toxicants and interacting agents in experimental designs.

2. **Study Design Variability**: Deployment of field studies, controlled laboratory conditions, or a hybrid of both introduces different exposure dynamics. Laboratory experiments allow for controlled dosing and endpoint assessments, whereas field studies incorporate macroecological stressors such as landscape-level microclimatic conditions, foraging behavior, and colony-level effects.

3. **Endpoints of Interest**: Endpoint selection—acute toxicity, behavioral changes, colony-level impacts—greatly informs the realistic pesticide range selection. Acute toxicity assessments (e.g., LD50 values below 100 μg/bee as predicted by QSAR-based in silico models) must be integrated with chronic exposure endpoints (observed in studies running from one week to one month) to capture full biological responses.

## Experimental Design and Exposure Scenarios

### Laboratory-Scale Investigations

In controlled laboratory settings, a realistic pesticide exposure range can be refined through:

- **Precise Dose Delivery**: Utilizing Potter-type towers has been demonstrated to define the pesticide exposure surface (e.g., ~1.05 cm²/bee for Apis mellifera). This is contrasted with physical validation using X-tomography (e.g., 3.27 cm²/bee) to fine-tune the hazard quotient (HQ) calculations.

- **Multi-Endpoint Monitoring**: Incorporate physiological endpoints (e.g., enzymatic activity alterations, gene expression differences) and behavioral endpoints (e.g., alterations in foraging dynamics, flight behavior) captured via real-time video tracking and biomarker analysis.

### Field Studies and Landscape-Level Modeling

Field studies offer the opportunity to incorporate spatial and temporal variability. The realistic range here must consider:

- **Environmental Heterogeneity**: Integrate factors such as growing degree days and microclimatic conditions. Modeling tools like LandscapePhenoBee and Bee++ emphasize the critical role of temperature-dependent developmental stages and landscape heterogeneity to predict exposure outcomes.

- **Species-Specific Foraging Behavior**: Extensive foragers like Apis mellifera will encounter a broader and often higher cumulative exposure compared to limited foragers like Osmia bicornis, with intermediate patterns in species such as Bombus terrestris. Foraging range and intensity, which are sensitive to pesticide-laden landscapes, need to be incorporated into exposure models.

- **Urban vs. Rural Gradient Effects**: Urban and rural hives yield differential genetic and behavioral responses to pesticide exposure. Large-scale exposome profiles from diverse geographic setups provide an integrative picture of how landscape-scale exposures interact with local physiology and gene expression plasticity.

## Incorporating Simulation Models

### Mechanistic and Agent-Based Modeling

Contemporary simulation models such as BeePop+, BeeGUTS, and DEBtox offer the capacity to integrate multi-route exposures—including acute, chronic, and sub-lethal doses—into colony-level risk assessments. Among the key model features are:

- **Multi-Scale Integration**: These models combine chemical biomarker data with population-level metrics and colony dynamics. They enable sensitivity analyses where various simulation scenarios capture differences in exposure routes, genetic plasticity, and behavioral outcomes.

- **Cumulative Stressor Effects**: Advanced simulations support identification of resilience tipping points and stress interactions. For instance, models that integrate colony-level social buffering effects (as observed in Bombus impatiens studies) can help refine which concentrations of pesticides prove detrimental when bees experience multiple sequential stress events.

- **Decision-Support for Regulatory Protocols**: Regulatory bodies (e.g., USEPA and USDA) increasingly depend on simulations to evaluate risk mitigation strategies, which can vary pesticide concentration recommendations based on landscape-scale interventions or temporal exposure adjustments.

### Quantitative Structure-Activity Relationship (QSAR) Approaches

The integration of in silico QSAR models, utilizing Dragon molecular descriptors and counter-propagation artificial neural networks (CPANN), has produced high predictive performance metrics (balanced accuracy of 0.90 and MCC of 0.78) for acute contact toxicity in honey bees. These QSAR models can be expanded to include layers of genetic plasticity data, thereby enabling realistic predictions for LD50 endpoints even in the context of aggregated pesticide exposures.

## Genetic and Behavioral Plasticity Considerations

A recurring theme in recent research is the incorporation of genetic and behavioral plasticity. Key findings include:

- **Differential Gene Expression**: Urban versus rural bees demonstrate variable gene expression responses, which translate into divergent tolerance thresholds. These differences necessitate considering localized adaptation in pesticide risk assessments.

- **Adaptive Foraging Models**: Reinforcement learning frameworks, as exemplified by the HARVEST system, provide insights into adaptive foraging shifts when bees encounter pesticide stressors. These models can predict dynamic shifts in foraging intensity and risk sensitivity, informing the selection of environmental concentration ranges that trigger behavioral thresholds in bees.

- **Colony-Level Behavioral Dynamics**: Life-history traits such as nesting location (above vs. below ground), flight behavior, and resource persistence shape the exposure landscape. Simulation tools that incorporate these variables (BeePop+, BeeGUTS) help quantify realistic exposure thresholds by integrating individual behavioral responses with group dynamics.

## Summary and Recommended Concentration Ranges

To summarize, the selection of a realistic pesticide range must be placed within a framework where:

1. **Low-Level, Chronic Exposures** in the realm of 0.01 to 0.1 μg/L are shown to have significant standing effects on bees over short exposure durations.

2. **Acute Toxicity Thresholds** derived from QSAR and empirical data (LD50 values < 100 μg/bee) provide an upper bound in laboratory assays.

3. **Field Study Adjustments**: When field studies are considered, the effective exposure range must be adjusted upward to incorporate cumulative exposures from landscape-level variations. Modeling tools suggest that, for extensive foragers like Apis mellifera, exposure scenarios might need to account for higher effective dosages due to larger foraging areas and diluted application concentrations.

4. **Integration of Multiple Stressors**: Experiments must address interactions of multiple pesticide classes and synergistic effects given previous laboratory validations and simulation outcomes. The integration of chemical, biological, and environmental data streams is critical for refining these ranges.

5. **Experimental Validation**: Prior to full-scale deployment, pilot studies using both Potter-type towers and high-resolution imaging (i.e., X-tomography) are recommended to validate dosing surfaces and refine hazard quotient calculations.

## Conclusion

A realistic pesticide range for bee exposure experiments is multifaceted, relying on a robust integration of laboratory data, field experiments, and advanced simulation models. The ongoing research reveals that immediate impacts on bee survival, physiology, and behavior can occur at low environmental concentrations, thereby emphasizing the need for combined multi-stressor risk assessments. Regulatory implications further underscore the importance of species-specific, landscape-integrated, and temporally dynamic approaches. Future directions should explore incorporating additional parameters such as microbiome alterations and epigenetic changes to further hone in on sustainable and realistic pesticide exposure guidelines.

This comprehensive synthesis not only provides a pathway for designing experiments with rigor but also establishes a platform for iterative validation using both empirical and simulation-based approaches. Such integrative methodologies ensure that the selected experimental pesticide ranges realistically mirror the complexities encountered in natural and agricultural ecosystems.

---

*Note: The recommendations and models discussed are based on the current synthesis of available research findings. Some aspects are subject to further refinement as new methodologies and longitudinal data become available.*

## Sources

- http://hdl.handle.net/10.3389/fevo.2019.00051.s002
- http://hdl.handle.net/10.3389/fevo.2019.00051.s001
- https://library.oapen.org/handle/20.500.12657/49991
- https://irl.umsl.edu/dissertation/1175
- https://doaj.org/article/f4b6ce3422004c5bac16caed01e400b3
- https://figshare.com/articles/_a_Bee_habitat_suitability_according_to_species_distribution_model_outputs_for_a1_current_conditions_and_for_a2_2030_a3_2050_and_a4_2080_scenarios_of_climate_change_/1454696
- https://doaj.org/toc/1932-6203
- https://hal.inrae.fr/hal-03291190
- https://repository.rothamsted.ac.uk/item/8qz46/beehave-a-systems-model-of-honeybee-colony-dynamics-and-foraging-to-explore-multifactorial-causes-of-colony-failure
- http://hdl.handle.net/10068/965540
- http://dx.doi.org/10.1002/ece3.9014
- http://hdl.handle.net/10.3389/fevo.2019.00051.s003
- https://doaj.org/article/a3b9015411944641807433adcf9a519d
- http://prodinra.inra.fr/record/384589
- http://dx.doi.org/10.1038/s41559-023-01990-5
- https://figshare.com/articles/_Pesticide_residues_detected_in_treatment_combs_n_8202_8202_13_used_to_rear_worker_bees_in_experiments_/466572
- https://zenodo.org/record/6783930
- https://zenodo.org/record/4104277
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/a7/6a/pone.0113728.PMC4239102.pdf
- http://hdl.handle.net/10255/dryad.146750
- https://figshare.com/articles/A_Pragmatic_Approach_to_Assess_the_Exposure_of_the_Honey_Bee_Apis_mellifera_When_Subjected_to_Pesticide_Spray/1247984
- http://hdl.handle.net/Classification
- https://research.sabanciuniv.edu/id/eprint/42946/
- https://research.wur.nl/en/publications/beegutsa-toxicokinetictoxicodynamic-model-for-the-interpretation-
- http://prodinra.inra.fr/record/279343
- https://escholarship.org/uc/item/61v205zf
- www.beeplusplus.ca)
- http://hdl.handle.net/11336/66489
- https://doi.org/10.1371/journal.pone.0176289
- https://digitalcommons.wpi.edu/mqp-all/4943
- http://resolver.sub.uni-goettingen.de/purl?gldocs-11858/10259
- https://doaj.org/article/064c33cefb214ef2a5ecb6f4d8bf14f7