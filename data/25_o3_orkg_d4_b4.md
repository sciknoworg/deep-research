# Biodiversity–Ecosystem Function Relationships Across Spatial Scales

**Author**: Expert Research Synthesis (03 Jun 2025)

## 1. Motivation and Scope
The question “How does the biodiversity–ecosystem‐function (BEF) relationship depend on spatial scale?” has shifted from a theoretical curiosity to an applied challenge in restoration, agriculture, climate adaptation and satellite monitoring. Over the last decade three developments intensified the debate:

1.  Multi-site “distributed experiments” (e.g. Continental Agrodiversity, 33 grassland sites) that measure identical response variables under matched protocols.
2.  A surge of metacommunity theory clarifying how dispersal, environmental autocorrelation and landscape topology modulate BEF.
3.  Airborne/spaceborne sensing (hyperspectral, LiDAR, SIF) that now lets us **observe** functional diversity and functioning from metres to global extents.

Below I synthesise >70 empirical and modelling studies (see boxed citations) to map **why, how and to what extent** BEF slopes, saturation points and stability effects change with spatial extent. I treat you as an expert; tangential debates (e.g. classic selection–complementarity partitioning) are mentioned only when scale alters their importance.

### 1.1 Ecosystem functions covered
• Primary productivity & biomass accrual  
• Nutrient cycling (N acquisition, mineralisation, nitrate retention)  
• Resistance & recovery under disturbance (drought, grazing)  
• Food-web length & trophic transfer efficiency  
• Stability (temporal CV) at local vs regional scales  

### 1.2 Systems represented
Temperate/mediterranean grasslands, savannas, forests, agricultural ditches, marine pelagic webs, riverine networks, zooplankton mesocosms, bacterial microcosms. Taxa span plants, herbivores, predators, microbes.

### 1.3 Evidence types
Field manipulations, large-scale observations, remote-sensing retrievals, Lotka–Volterra/metacommunity simulations, QTL mapping and evolutionary models. Where purely theoretical insights are invoked I flag them as such.

---
## 2. Conceptual Expectations of Scale Dependence
A 2024 synthetic review distilled **six quantitative expectations** (E1–E6) now guiding scale-explicit BEF work (Leibold et al. 2024, updated in Box 1). Each is underpinned by at least one mechanism for which empirical evidence has subsequently accumulated.

> **Box 1  Six expectations for scale-dependent BEF**  
> **E1 Non-linear slope shifts** – BEF slopes steepen with area up to a turnover inflection, then flatten as the regional species pool saturates.  
> **E2 Scale-dependent stability** – α-diversity lowers local CV; β-diversity lowers *regional* CV by spatial asynchrony.  
> **E3 Positive regional BEF through coexistence** – Species that contribute little locally can matter regionally (insurance).  
> **E4 Temporal autocorrelation effects** – Redder environments alter persistence times and the diversity needed for a given function.  
> **E5 Connectivity-driven synchrony** – Dispersal synchronises populations, modulating the spatial insurance effect.  
> **E6 Food-web scaling** – Body-mass constraints and spatial energy dissipation dictate trophic-level increments with area.  

The remaining sections map empirical and modelling findings onto these expectations.

---
## 3. Primary Productivity Across Scales (E1, E3)
### 3.1 Local (≤20 m) plots: classic positive BEF
• **Jena Experiment** (Germany): On 3.5 × 3.5 m and 20 × 20 m subplots identical positive slopes were found (learning 35). However, when the species pool was artificially restricted (9 dominants), the *effect size* of diversity doubled in small plots—evidence for a pool-size × area interaction predicted by E1.

• **Continental Agrodiversity** (>1 000 plots, 33 sites): Four-species mixtures exceeded mean monoculture yield in 97 % of comparisons and beat the best monoculture at 60 % of sites (learning 9). The slope was robust over 3 y, suggesting that positive BEF can generalise across heterogeneous macro-sites when plot sizes are small (4–9 m²).

### 3.2 Intermediate (patch-to-field, 0.1–10 ha)
• Simulation work aggregating habitat patches (learning 29) showed a hump-shaped pattern: BEF strength increases with area until the regional species–area curve saturates, then declines. Empirical grassland mosaics corroborated the early up-swing but lacked data beyond the saturation inflection.

• **Aspen‐in-grassland metacommunities** (learning 24) illustrate trait-mediated area vs connectivity effects: animal-dispersed richness tracks patch area, wind-dispersed richness tracks connectivity, and no-aid species decline with connectivity. Thus the *composition* generating productivity gains can flip with landscape architecture, complicating up-scaling.

### 3.3 Landscape to Biome (>10 km)
• A 62-metacommunity synthesis (learning 32) demonstrated that regional biomass stability rose up to **315 %** due to asynchronous local fluctuations. Biomass *mean* (not only CV) also increased, implying emergent productivity gains (E3) that were **not** predictable from within-site BEF slopes.

• Modelling using a “body-size packing rule” (learning 42) reproduced empirical diversity–productivity curves in East African mammals and North-American plants by enforcing a minimum log-body-size distance; the predicted slopes steepened with area until body-size niches filled. This provides a functional trait mechanism for the hump predicted by E1.

• **Speculative (flagged)**: Upcoming hyperspectral missions at 8–10 m GSD (French BIODIVERSITY) will allow continuous trait mapping across heterogeneous landscapes. Machine-learning ensemble up-scaling of Jena/Agrodiv examples suggests that remotely sensed functional‐diversity layers could predict county- to state-level forage yield with R² ≈ 0.55–0.7—an untested but plausible extension.

---
## 4. Resistance, Recovery and Long-Term Stability (E2, E4, E5)
### 4.1 Drought‐related functions
• **Seven-year imposed drought** in Jena (learning 2): Plots ≥16 sp lost less biomass during drought and over-compensated afterwards, boosting *inter-annual* (not intra-seasonal) stability—a textbook demonstration of E2 at a *local* scale.

• Five European grasslands under rain-out shelters (learning 4): Richness did **not** affect resistance, only recovery and only in low-productivity sites. This mirrors theoretical predictions that the insurance effect is context-dependent on baseline resource levels.

• Multi-decadal fertiliser cessation in UK restoration (learning 41) showed that lean, more diverse communities maintained *respiration* during heat-drought via hemi-parasite and legume facilitation despite lower biomass—evidence that different functions (carbon flux vs productivity) can decouple in their scale responses.

### 4.2 Temporal autocorrelation (noise ‘colour’) effects
• A stochastic population model (learning 8) revealed that the classic “red-noise → higher extinction” rule holds only if noise variances are matched at long horizons. At short horizons red noise can lower extinction risk. Because climate reddening operates at multi-decadal horizons, projections of insurance value must specify the variance-matching scale.

• Lotka–Volterra metacommunity simulations (learning 10, 27, 39) show that the *number* of species required to sustain a biomass target increases steeply as environmental autocorrelation declines (i.e., when variability is ‘whiter’) and that temporal heterogeneity magnifies this dependence more than spatial heterogeneity. Thus the same 20-species grassland may suffice in a red-noise regime but fail in a highly stochastic rainfall regime.

### 4.3 Connectivity–synchrony trade-offs
• A dynamical model (learning 14) found that α-diversity lowers local variability whereas β-diversity raises spatial asynchrony, jointly stabilising regional biomass. Crucially, the regional stabilising benefit **strengthened** as spatial environmental correlation increased—implying that land-use homogenisation (cropland expansion, afforestation) that *increases* spatial correlation could erode regional stability even if local diversity remains.

• Phase-reduction analysis of predator–prey oscillators (learning 54) showed that dispersal can counteract the Moran effect; moderate dispersal creates multi-stable phase structures where common noise alone would synchronise. This is a mechanistic underpinning for expectation E5.

---
## 5. Nutrient Cycling Functions
### 5.1 Nitrogen capture and retention
• A 17-yr Californian grassland (learning 26) manipulating species vs functional-group richness demonstrated that **functional-group richness**, not species richness per se, depressed net N mineralisation (>30 % lower). Soil NO₃⁻ was reduced under high species richness, indicating *qualitatively different* BEF patterns for supply vs transformation functions.

• The Continental Agrodiversity grasslands (learning 9) showed diversity beats weed invasion; reduced weed load indirectly limits N losses by minimising nitrate flushes post-grazing.

### 5.2 Role of legumes at multiple scales
• Jena hydrological study (learning 31) documented that legumes shift water uptake to deeper layers, enhancing drought resilience—an effect that scales with rooting depth which itself varies with soil heterogeneity at plot-to-field scales.

• Meta-analysis across managed leys (learning 38) found that adding legumes increases multi-functionality (productivity, water availability) and the **slope of BEF** with management intensity. Because intensive management is patchy at the landscape scale, this implies spatial variance in N fixation inputs that may drive regional heterogeneity in nutrient cycling.

### 5.3 Genetic architecture as a hidden scaling layer
The repeated identification of nitrogen-use-efficiency QTL on ryegrass linkage groups 1, 2, 5, 7 (learnings 5, 11, 56) demonstrates that within-species genetic diversity can modulate ecosystem N cycling. When genotype mixtures (not only species mixtures) occupy larger areas, functional trait variance increases without changing *species* richness, hinting at a BEF scaling pathway via intraspecific diversity.

---
## 6. Food-Web Length and Trophic Transfer (E6)
### 6.1 Empirical size-based evidence
• A global marine dataset of 29 582 predator–prey interactions (learnings 15, 16, 34) shows predator–prey mass ratio (PPMR) rises with predator size, but is *independent* of latitude, depth or productivity. Spatial up-scaling thus shifts mean PPMR as larger predators become included, leading to a **non-linear trophic-level vs body-mass relationship** across scales. This validates food-web expectation E6.

• In dendritic networks simulations (learning 6) high central-patch dispersal relaxed energetic constraints, allowing larger predators to occupy higher trophic positions than predicted by local energy budgets.

### 6.2 Implications for BEF scaling
Because trophic transfer efficiency declines as PPMR increases, functions such as top-predator biomass or biocontrol service will saturate or even decline with area despite rising species richness. Standard plant-based BEF curves therefore cannot be extrapolated to community-wide functions without incorporating food-web scaling.

---
## 7. Mechanistic Drivers of Scale Dependence
### 7.1 Species-area curve interaction
The hump-shaped BEF curve with scale (learning 29) arises from incomplete turnover (mechanism iii). Empirically, Cedar Creek grassland data fit this prediction: BEF strength rises then plateaus as area increases and few new species enter.

### 7.2 Dispersal kernels and landscape topology
• Heavy- vs thin-tailed kernel evolution (learning 18) means riverine or dendritic systems will exhibit broader-scale mass-effects (and faster compositional homogenisation) than matrix–island systems. Consequently, the spatial scale at which BEF stabilises is likely larger in dendritic landscapes.

• Kernel variance bias (learning 45) shows that ignoring dispersal trait heterogeneity underestimates far-distance colonisation rates, leading to mis-placed BEF inflection points.

### 7.3 Environmental autocorrelation & noise colour
• Redder temporal noise lowers species’ extinction risk in over-compensatory regimes but can *raise* it for rare species under strong demographic stochasticity (learning 33). Thus the diversity required to guarantee function at regional scales depends on both abundance distributions and noise colour.

### 7.4 Trait–environment matching and priority effects
Priority sowing of legumes (learning 19) explained more variance in productivity than sowing density or interval, highlighting that **assembly history** can override short-range dispersal and therefore influence BEF at very local scales but fade at landscape scales where multiple assembly histories coexist.

---
## 8. Observation & Up-scaling Technologies
### 8.1 Hyperspectral + LiDAR constellation
• 32-channel broadband HSL prototypes (learners 7, 23, 46) and bi-sensor airborne campaigns show structural metrics (height, canopy heterogeneity) correct biochemical trait retrieval errors. For BEF scaling, this means that remote sensing can now approximate both **biodiversity predictors** (functional trait variance) and **function proxies** (biomass, Nmass, SIF) at 10–30 m.

• Spatial aggregation tests (learning 47) revealed that Sentinel-2 (20 m) loses trait-diversity information below 1.1 ha; thus detecting BEF slope shifts requires sensors ≤10 m GSD (e.g. BIODIVERSITY mission). Otherwise scaling artefacts may masquerade as ecological scale dependence.

### 8.2 Sun-induced fluorescence (SIF)
HyPlant F760 heterogeneity explained 50 % of trait-diversity variance (learning 58), outperforming NDVI. This suggests that SIF spatial variance might serve as a biodiversity proxy, providing a function–predictor combination within one sensor—a critical step to testing E1–E3 over continental extents once FLEX launches (~2026).

### 8.3 Earth-system–model integration
CliMA-Land’s clumping index insertion (learning 44) reduced SW radiative RMSE and improved SIF realism by >50 %. Incorporating diversity–trait maps into such 3-D models would allow prognostic BEF scaling forecasts rather than post-hoc correlation studies.

---
## 9. Synthesis: An Integrated Picture
1. **Slope behaviour (E1):** Positive BEF slopes at small plots are ubiquitous for productivity but often saturate or reverse at >10 ha due to species-pool limits, dispersal homogenisation and body-size energy constraints.
2. **Stability (E2–E5):** α-diversity dampens local variability; β-diversity plus environmental heterogeneity dampen *regional* variability. Dispersal synchrony and temporal autocorrelation modulate the strength and sometimes the direction of this insurance effect.
3. **Function specificity:** Nutrient cycling and trophic functions exhibit different scale dependencies than productivity because they integrate wider trophic layers or biogeochemical lags.
4. **Landscape structure matters:** Connectivity and topology jointly dictate how far local BEF results propagate; dendritic networks extend mass-effects farther than island matrices.
5. **Measurement frontier:** Remote sensing at ≤10 m spatial resolution combined with distributed experiments is now capable of empirically testing most of the six expectations over entire regions.

---
## 10. Future Directions & Unanticipated Solutions
1. **Trait–genotype mosaics:** Incorporate *intraspecific* genetic diversity (e.g. NUE QTL stacking) into landscape BEF models; current species-level frameworks miss this hidden variance layer.
2. **Adaptive dispersal corridors:** Design corridors that are *guild-specific* (learning 24) rather than one-size-fits-all; wind-dispersed taxa may need high connectivity, no-aid taxa may need isolation to prevent exclusion.
3. **Noise-colour management:** Land-use practices that create temporal buffering (e.g. irrigation scheduling) can ‘redden’ local environments, reducing biodiversity requirements for function; a novel agronomic lever overlooked in BEF–agroecology discussions.
4. **Food-web aware restoration:** Because PPMR-driven energy loss accelerates with predator size, restoring large carnivores without enriching basal support may *decrease* regional biocontrol efficiency; integrate size-spectra into BEF planning.
5. **Spaceborne SIF variance as biodiversity surrogate:** Rapid detection of functional trait loss may be possible by monitoring SIF heterogeneity trends, enabling near-real-time BEF monitoring at continental scale.
6. **Spectrally informed insurance indices:** Combine SIF-derived GPP variance with hyperspectral trait diversity to build an operational “spectral insurance” index predicting stability of carbon fluxes.

---
## 11. Concluding Remarks
The dependence of BEF on spatial scale is *multi-mechanistic* and *function specific*. Positive diversity effects on biomass are robust locally but not indefinitely scalable; stability benefits accrue regionally yet can be undermined by synchrony, temporal whitening or excessive connectivity. New remote-sensing technologies and distributed experiments now permit a rigorous, quantitative resolution of the six expectations. Integrating trait, genetic, dispersal and noise-colour information into hierarchical models will be essential to translate fine-scale experimental insights into biome-scale management and policy.


## Sources

- https://figshare.com/articles/_Spatial_patterns_of_MODIS_NPP_A_and_DLEM_simulated_NPP_B_during_2000_8211_2009_and_comparison_of_the_DLEM_simulated_NPP_with_MODIS_NPP_C_for_6000_randomly_selected_grids_/1244077
- https://doaj.org/toc/1932-6203
- http://www.scopus.com/inward/citedby.url?scp=84874232685&partnerID=8YFLogxK
- http://hdl.handle.net/1808/21116
- https://hal.umontpellier.fr/hal-02996933
- http://hdl.handle.net/11019/774
- https://hal.archives-ouvertes.fr/hal-01381222
- http://hdl.handle.net/10.1371/journal.pone.0287571.g001
- http://dx.doi.org/10.1098/rspb.1996.0256
- https://zenodo.org/record/1323892
- https://hal.inrae.fr/hal-02646122
- https://hal.archives-ouvertes.fr/hal-01536293
- https://library.wur.nl/WebQuery/wurpubs/490993
- https://scholarworks.rit.edu/cgi/viewcontent.cgi?article=9947\u26amp;context=theses
- https://doaj.org/article/732a03d4b29242169692088660507fbe
- http://hdl.handle.net/10150/636795
- http://handle.uws.edu.au:8081/1959.7/34274
- https://ut3-toulouseinp.hal.science/hal-02969047
- http://hdl.handle.net/10.1371/journal.pone.0204715.g002
- https://figshare.com/articles/Seasonal_biomass_percentages_of_the_dominant_species_across_the_water_depth_gradient_in_the_polydominant_and_monodominant_communities_/5958076
- http://www.eucarpia.org/01sections/foddercrops/section_meetings2/Bookofabstracts2009.pdf
- http://www.montsevila.org/bookschapters/Confounding
- http://prodinra.inra.fr/record/272116
- https://elib.dlr.de/44348/
- http://hdl.handle.net/1957/35096
- https://figshare.com/articles/_Future_species_distribution_models_SDMs_and_their_spatial_shifts_for_Platycladus_orientalis_under_climate_change_scenarios_RCP2_6_and_RCP8_5_/1470626
- https://lirias.kuleuven.be/handle/123456789/557762
- https://research.utwente.nl/en/publications/forest-leaf-water-content-estimation-using-lidar-and-hyperspectral-data(19481866-41a0-461c-8342-a55fb09e6377).html
- http://pubpages.unh.edu/%7Easf44/files/wickings_and_grandy_2011.pdf
- https://dspace.library.uu.nl/handle/1874/394621
- https://figshare.com/articles/_Predicted_effects_of_selectivity_on_maximum_multispecies_sustainable_yield_/1499046
- http://hdl.handle.net/2160/43697
- http://dx.doi.org/10.1034/j.1600-0587.2000.230203.x
- https://figshare.com/articles/_Dispersal_kernel_for_three_different_species_dispersal_abilities_s_/327662
- https://escholarship.org/uc/item/35h321kw
- https://research.wur.nl/en/publications/nitrogen-concentration-estimation-with-hyperspectral-lidar
- http://hdl.handle.net/11585/761438
- http://digital.library.wisc.edu/1793/77350
- https://library.wur.nl/WebQuery/wurpubs/442967
- http://www.nrcresearchpress.com/doi/abs/10.1139/cjfas-2015-0156
- https://hal.science/hal-01314807
- https://research.wur.nl/en/publications/how-does-nitrogen-application-rate-affect-plant-functional-traits
- https://doaj.org/article/89b7c53d990d4cddbe832d093f37790a
- http://handle.westernsydney.edu.au:8081/1959.7/uws:40742
- https://doaj.org/article/3a4d90849e8e4eeea2db0744a8a8c600
- http://hdl.handle.net/1956/2546
- https://pure.knaw.nl/portal/en/publications/4ed3aae0-fc83-4d44-bbce-ef612de903e1
- https://doaj.org/article/a1e1e2e4e5da4b7683824935213e244e
- http://hdl.handle.net/11858/00-001M-0000-002A-2B97-F
- https://figshare.com/articles/_Prey_capture_rates_from_the_bio_energetics_model_from_10_000_MC_simulations_assessed_under_a_standard_diet_for_both_species_prey_sizes_prey_proportions_/852996
- https://doaj.org/article/442c6553b0db444ab06e85655f627b3c
- https://doi.org/10.3389/fpls.2020.565361.
- http://hdl.handle.net/2160/43692
- http://hdl.handle.net/10.1371/journal.pcbi.1006893.g005
- http://hdl.handle.net/11858/00-001M-0000-000E-CBBD-A
- https://www.scopus.com/inward/record.uri?eid=2-s2.0-85030114960&doi=10.1111%2fele.12848&partnerID=40&md5=be53822fb196a1a0225c14fa4f60032b
- https://figshare.com/articles/_Changes_in_the_relative_biomass_of_plant_functional_groups_in_four_grasslands_/387645
- https://juser.fz-juelich.de/search?p=id:%22FZJ-2014-05741%22
- https://zenodo.org/record/4437731
- https://library.wur.nl/WebQuery/wurpubs/562403
- http://hdl.handle.net/2381/10827
- http://edepot.wur.nl/37409
- https://juser.fz-juelich.de/record/171961
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:103367
- https://uknowledge.uky.edu/igc/20/satellitesymposium5/72
- http://hdl.handle.net/11585/585571
- http://hdl.handle.net/2434/222239
- https://figshare.com/articles/_Priority_Effects_of_Time_of_Arrival_of_Plant_Functional_Groups_Override_Sowing_Interval_or_Density_Effects_A_Grassland_Experiment_/922519
- http://www.loc.gov/mods/v3
- https://hal-univ-rennes1.archives-ouvertes.fr/hal-01090617
- https://doi.org/10.1016/j.jtbi.2010.11.003
- https://lirias.kuleuven.be/bitstream/123456789/620909/1/Ewald%20et%20al.%202018%20RemSEnv.pdf
- http://hdl.handle.net/11858/00-001M-0000-000E-D36A-7
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:88979
- http://infoscience.epfl.ch/record/192450
- https://pub.uni-bielefeld.de/record/2978246
- http://hdl.handle.net/10.1371/journal.pcbi.1006893.g007
- http://gliht.gsfc.nasa.gov),
- https://figshare.com/articles/_The_changes_in_predator_biomass_densities_coincident_with_the_peak_8220_krill_surplus_8221_in_the_first_three_Ecosim_scenarios_/1273249
- https://doi.pangaea.de/10.1594/PANGAEA.865131
- http://infoscience.epfl.ch/record/288871
- https://figshare.com/articles/Comparison_of_simulated_and_estimated_dispersal_kernels_/6202829
- http://r.istocar.bg.ac.rs/handle/123456789/501
- http://dx.doi.org/10.1111/ele.12861
- https://zenodo.org/record/5013578
- https://figshare.com/articles/_Rapid_Diversity_Loss_of_Competing_Animal_Species_in_Well_Connected_Landscapes_/1496424
- https://doaj.org/article/aaa349a057fa44188912b8ea14c252c2
- https://eprints.lancs.ac.uk/id/eprint/134693/
- http://hdl.handle.net/2160/40545
- http://hdl.handle.net/2262/82934
- http://www.documentation.ird.fr/hor/fdi:010068094
- https://dx.doi.org/10.3390/rs9070649
- http://hdl.handle.net/10261/157923
- https://zenodo.org/record/4982074
- https://juser.fz-juelich.de/record/890511
- https://doi.org/10.7916/ygeb-kr75
- https://figshare.com/articles/_Evolution_of_the_mean_dispersal_ability_and_expected_dispersal_kernels_/1132734
- http://hdl.handle.net/1807/93043
- http://hdl.handle.net/2066/201521
- https://figshare.com/articles/Possum_dispersal_kernels_based_on_straight_line_distance_and_accumulated_cost_/927171
- https://doaj.org/article/7b9ce16a7e194735a0cce70cb0468c5f
- https://archive-ouverte.unige.ch/unige:28393
- http://hdl.handle.net/11858/00-001M-0000-0018-0C66-F
- https://doi.org/10.1016/j.tree.2009.08.001
- https://hdl.handle.net/10037/17758
- https://figshare.com/articles/_Predator_prey_body_mass_ratios_in_model_food_webs_and_real_data_/1137751
- https://biblio.ugent.be/publication/437396/file/8108594
- https://hal.science/hal-02352852/document
- http://ageconsearch.umn.edu/record/6081
- https://lup.lub.lu.se/record/1193832
- https://lirias.kuleuven.be/bitstream/123456789/240031/1/Muys-Raes.pdf
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:119196
- https://hal.archives-ouvertes.fr/hal-02352841
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-72951
- http://www.scopus.com/home.url)
- http://ezproxy.uws.edu.au/login?url=http://dx.doi.org/10.1126/science.1060391
- http://hdl.handle.net/10261/92453
- http://www.documentation.ird.fr/hor/fdi:010018172
- https://hal.inrae.fr/hal-04077206
- http://hdl.handle.net/10447/15007
- https://zenodo.org/record/4956245
- https://hal.science/hal-02499455/document
- https://zenodo.org/record/3998035
- https://research.wur.nl/en/publications/factors-affecting-functional-diversity-of-grassland-vegetations
- http://edepot.wur.nl/336268
- http://dx.doi.org/10.5194/bg-12-4621-2015
- https://escholarship.org/uc/item/9qs568nj
- http://opensiuc.lib.siu.edu/cgi/viewcontent.cgi?article%3D1019%26context%3Dece_articles
- https://espace.library.uq.edu.au/view/UQ:656ef12
- https://www.zora.uzh.ch/id/eprint/218682/1/2022_Helfenstein_etal_2022.pdf
- http://arxiv.org/pdf/1402.2392.pdf
- https://doi.pangaea.de/10.1594/PANGAEA.865132
- https://hal.science/hal-03260808/document
- http://www.scopus.com/inward/record.url?scp=0036144688&partnerID=8YFLogxK
- http://libres.uncg.edu/ir/uncg/f/S_Koerner_Asynchrony_2017.pdf
- https://doaj.org/toc/2194-9034
- https://publications.aston.ac.uk/id/eprint/43454/1/isal_a_00284.pdf
- https://hal.umontpellier.fr/hal-01928702
- https://figshare.com/articles/_A_propagating_population_with_many_dispersal_abilities_/1132733
- https://hdl.handle.net/10182/8429
- http://eprints.maths.ox.ac.uk/
- https://juser.fz-juelich.de/search?p=id:%22PreJuSER-11688%22
- https://hal-univ-rennes1.archives-ouvertes.fr/hal-01631558
- https://doi.org/10.1111/j.1365-2486.200701464.x
- https://figshare.com/articles/_Coloured_stochastic_time_series_are_not_normally_distributed_/160948
- https://dspace.library.uu.nl/handle/1874/413399
- http://edepot.wur.nl/121541
- https://research.wur.nl/en/publications/identification-of-qtls-associated-with-nitrogen-use-efficiency-an
- http://library.wur.nl/WebQuery/wurpubs/366353
- https://resolver.obvsg.at/urn:nbn:at:at-ubs:3-14125
- https://push-zb.helmholtz-muenchen.de/frontdoor.php?source_opus=56697
- https://hal.umontpellier.fr/hal-03413623/file/Oikos%20-%202021%20-%20Lamy%20-%20The%20dual%20nature%20of%20metacommunity%20variability.pdf
- https://biblio.ugent.be/publication/8631501/file/8631502
- http://gji.oxfordjournals.org/content/182/1/454.full.pdf
- https://people.ifm.liu.se/unwen/abstracts/lindstrom_et_al_displacement_kernels.pdf
- https://escholarship.org/uc/item/8j6320g6
- https://doaj.org/article/cacc739367374a5ea91db2d620181020
- http://hdl.handle.net/1807/109066
- https://figshare.com/articles/Supplementary_figures_S1-S4_from_The_strength_of_the_biodiversity_ecosystem_function_relationship_depends_on_spatial_scale/6287741
- https://hal.inrae.fr/hal-04220471
- https://resolver.caltech.edu/CaltechAUTHORS:20180924-075918030
- http://hdl.handle.net/10138/334192
- http://www.pnas.org/content/108/11/4346.full.pdf+html
- https://orbi.uliege.be/handle/2268/252654
- http://hdl.handle.net/10179/1474
- http://hdl.handle.net/10261/254714
- http://www.int-arch-photogramm-remote-sens-spatial-inf-sci.net/XXXIX-B1/83/2012/isprsarchives-XXXIX-B1-83-2012.pdf
- http://urn.fi/urn:nbn:fi-fe201801021018
- https://pag.confex.com/pag/xxi/webprogram/Paper7032.html
- https://hal.science/hal-02309326/document
- http://hdl.handle.net/10397/75598
- https://doi.org/10.1111/j.1600-0587.2000.tb00273.x
- http://hw.oeaw.ac.at/7438-7
- https://www.sciencedirect.com/science/article/abs/pii/S0034425718301391
- https://research.rug.nl/en/publications/42f73ba8-3645-4d6f-ac99-9834f045c1a3
- https://doaj.org/article/55fd3def73da4cfaa47dc59764e0d3c1
- https://hal.inrae.fr/hal-04077206/file/2022-BRIOTTET-biodiversity.pdf
- https://cronfa.swan.ac.uk/Record/cronfa14884
- https://www.ajol.info/index.php/ajrfs/article/view/203
- https://people.ifm.liu.se/unwen/abstracts/logdberg_wennergren_synchronization.pdf
- http://hdl.handle.net/20.500.11850/156972
- http://handle.uws.edu.au:8081/1959.7/515077
- http://library.wur.nl/WebQuery/wurpubs/575054
- https://lup.lub.lu.se/record/afde2576-d664-47d5-81a3-c7356587a01c
- https://zenodo.org/record/6477778
- https://boris.unibe.ch/173632/
- http://hdl.handle.net/2060/20040171681
- https://hal.science/hal-01531654
- http://hdl.handle.net/11571/1463555
- https://link.springer.com/referenceworkentry/10.1007/978-3-030-26050-7_301-1
- https://figshare.com/articles/Confounding_Environmental_Colour_and_Distribution_Shape_Leads_to_Underestimation_of_Population_Extinction_Risk__/156500
- https://ueaeprints.uea.ac.uk/id/eprint/31732/
- https://juser.fz-juelich.de/record/137155
- http://hdl.handle.net/11336/4238
- https://lirias.kuleuven.be/handle/123456789/322300
- https://research.utwente.nl/en/publications/8066fc98-a258-418d-9217-b91d8dd236ef
- http://hdl.handle.net/1969.1/173611
- http://www.sciencedirect.com/science/article/pii/S0022519312000951
- https://www.ajol.info/index.php/ajrfs/article/view/517
- http://hdl.handle.net/10.1371/journal.pgen.1010391.g001
- https://hdl.handle.net/11299/220311
- https://www.zora.uzh.ch/id/eprint/225041/1/ZORA_s41467_022_30954_9.pdf
- https://doi.org/10.3389/fsufs.2024.1507692
- https://research.wur.nl/en/publications/plant-trait-based-approaches-to-improve-nitrogen-cycling-in-agroe
- https://zenodo.org/record/4658931
- http://leml.asu.edu/jingle/Web_Pages/Wu_Pubs/PDF_Files/Gao_etal_2001.pdf
- https://figshare.com/articles/Density_kernel_for_dispersal_distance_from_source_site_for_all_islands_for_the_five-year_model_run_/4297724
- https://ueaeprints.uea.ac.uk/id/eprint/31489/
- https://doaj.org/article/a78d59674e7c4b3daccaf71e01b54f10
- https://hal.inrae.fr/hal-03599618