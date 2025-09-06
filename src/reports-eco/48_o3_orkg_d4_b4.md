# Methodological Challenges in Measuring Seedling Functional Traits – A Comprehensive Technical Synthesis (2025)

*This report integrates >100 peer-reviewed and pre-print findings (2011–2024) to map the current methodological landscape, identify persistent bottlenecks, and propose forward-looking solutions for rigorous, transferable measurement of seedling functional traits across taxa, biomes and experimental contexts.*

---
## 1. Conceptual Scope

1. **Trait space covered**  
   • Morphological: specific leaf area (SLA), leaf dry-matter content (LDMC), seed mass/shape, root system architecture (RSA) metrics.  
   • Physiological: photosynthetic capacity (A_max, α, R_d), intrinsic water-use efficiency (iWUE, δ¹³C), transpiration breakpoints, sap-ion dynamics.  
   • Biochemical: tissue N, P, K, C fractions, ROS/NO signalling during germination.  
   • ‘Hard’ regenerative & architectural traits: emergence probability, age at maximal growth, asymptotic height.

2. **Measurement arenas**  
   • Growth chambers / glasshouse (HTP platforms, controlled VPD).  
   • Field common gardens & chronosequences.  
   • In-situ automated chambers, minirhizotrons, X-ray CT/MRI, hyperspectral + depth cameras.  
   • Molecular & in-plant micro-electronic sensors (bioristor, sap δ¹³C).

3. **Why seedlings?**  
   Early ontogeny sets demographic filters (germination → emergence → survival). Yet cross-stage extrapolation is trait-dependent: only **27–36 %** of adult SLA and **17–31 %** of adult leaf N is explained by seedling measurements, whereas structural size traits retain >50 % correspondence. Hence methodological rigour at seedling stage is critical but cannot assume universal transferability.

---
## 2. Core Methodological Challenges

### 2.1 Ontogenetic Signal vs Environmental Noise

| Challenge | Empirical evidence | Consequence |
|-----------|-------------------|-------------|
| Weaker within-species trait correlations at seedling stage | Common-garden datasets show LDMC–SLA slope shallower than global inter-specific slope | Sampling designs that mimic adult trait networks over-estimate predictive power |
| Emergence dominance | Boulder (2021) & Oregon (2014) – emergence explains >90 % of first-season survival, classic seed traits explain ≤18 % of emergence variance | Trait lists must extend beyond seed mass to **emergence mechanics, coleoptile force, mucilage wetting** |
| Trait–growth link non-transferability | Only 1/3 post-fire chronosequences retained low SLA → tall stature, high N → fast growth | Model calibration must be site-specific; cross-ecosystem extrapolation risky |
| Greenhouse vs field rank inversion | Rice A_max, maize WUE rankings flip between environments | Requires environment-standardised protocols (VPD ramps, PPFD spectra) & correction models |

### 2.2 Sampling Design & Statistical Power

* Intraspecific trait variance ≈40 % of total; apparent trait–trait correlations inflate when n is small – emphasise **power analyses a priori**.
* Hierarchical Bayesian models outperform pooled regressions in partitioning species vs environment random effects (LAI, biomass allocation).  
  → **Recommendation**: use species-explicit random intercepts/slopes; plan >30 individuals per genotype × treatment for reliable slope estimates.

### 2.3 Instrumentation & Protocol Biases

1. **Gas exchange**  
   • Residence-time (τ) artefacts: Low-cost open chambers need τ-correction to keep C-uptake error <8 %.  
   • Non-sequential light curves cut runtime 4× but raise A_max; greenhouse microclimate is confounding factor.  
   • VPD breakpoints: Without scripted VPD ramps (PHENODYN vs PHENOARCH), WUE datasets are incomparable.

2. **Root imaging**  
   • Acquisition > Segmentation bottleneck: RootForce, 4DRoot, CT+U-Net reduce manual burden 10–100× but still need human QC.  
   • Modality trade-offs: CT excels ≤56 mm pots, MRI superior in larger volumes; DIRT/3D-COLMAP slashes photogrammetry image count by 90 %.

3. **Surface–seedling interactions**  
   • Paper substrate chemistry alters root architecture (GrowScreen-PaGe).  
   • HMDS vapour silanisation offers hydrophobic yet transparent paper; FDTS deteriorates at high RH → prefer ODTS or HMDS.

4. **HTP Platforms**  
   • Microphenotron achieves 4 320 treatments per 10 d but still manual plate handling dominates throughput.  
   • Platforms differ in VPD logging frequency (3 min vs daily) – harmonisation protocol lacking.

### 2.4 Trait Definition Gaps

* SLA, wood density, seed mass explain little RGR variance in global sapling meta-analysis – need **new predictive metrics** (e.g., architectural trajectory parameters, radicle hydraulics, dynamic photosynthate allocation).
* Root economics often proxied by SRL/Tissue density, yet near-infrared hyperspectral & PET tracers reveal spatial gradients and decay kinetics untapped by classical traits.

---
## 3. Emerging Solutions & Technologies

### 3.1 Sensors & Real-Time Physiology

| Technology | Capability | Application |
|------------|-----------|-------------|
| Bioristor textile transistor | Continuous sap-ion & VPD breakpoint detection | Irrigation scheduling; genotype screening for WUE |
| δ¹³C isotopic profiling | >70 % clonal repeatability; QTL anchored | Selection for intrinsic WUE in breeding |
| OCTOflux multiplex | 4–7× higher leaf A_max throughput | Field phenotyping campaigns |

### 3.2 Imaging & Computational Pipelines

1. **3-D reflectance + depth fusion** removes geometry-induced spectral noise; boosts crown-level trait precision.
2. **RootForce + 4DRoot**: cylinder-fitting of CT time-series yields volumetric growth, θ distribution, soil density interaction – critical for carbon sequestration modelling.
3. **Deep learning minirhizotron workflow**: Root-Painter + RhizoVision reduces analyst time by >98 % (R = 0.81), enabling seasonal RSA surveys.

### 3.3 High-Throughput Germination & Emergence Assays

• ScreenSeed / GERMINATOR / SoyRET deliver automated radicle detection; image-based RGI quantifies speed, capacity & uniformity.  
• Cost-effective imaging in inactinic green light distinguishes radicle/hypocotyl under darkness for hormone studies.

### 3.4 Functional–Structural Modelling (FSM)

• GreenLab multilevel model calibrated for Cecropia & chrysanthemum captures organogenesis, branching, sink–source dynamics; adding delay equations enables reproductive output prediction.  
• Virtual-ecology simulations used to pre-plan sampling and forecast accuracy of trait-growth models under limited data.

---
## 4. Best-Practice Recommendations (2025 Edition)

1. **Standardise Environmental Drivers**  
   • Adopt *scripted VPD ramps* (0.8–4 kPa, 0.3 kPa h⁻¹) and *fluctuating light waveforms* in both glasshouse and field HTP to align WUE and photosynthesis datasets.  
   • Log RH/T/PPFD at ≤1 min resolution; store with trait metadata.

2. **Residence-Time Corrections**  
   • Ensure chamber volume / flow ratio refreshes headspace every ≤3 s; implement τ-deconvolution for dynamic fluxes.

3. **Sample Size & Hierarchical Statistics**  
   • Minimum 30 seedlings per taxon × treatment; fit hierarchical Bayesian models with group-specific biases & kernels; share raw posteriors for meta-analysis.

4. **Cross-Platform Calibration**  
   • CO₂/H₂O flux systems: validate against lysimeter or BREB; target ±5 % accuracy.  
   • Root imaging: benchmark against manual tracings on a 10 % subsample; document modality-dependent detection limits.

5. **Trait Ontology Expansion**  
   • Incorporate *architectural trajectory traits* (age at peak growth, branch emission rate) and *dynamic physiological thresholds* (VPD breakpoint, RGI) alongside classic static traits.  
   • Register traits in TRY/BIEN with explicit ontogenetic stage tags.

6. **Surface Engineering for 2-D Root Platforms**  
   • Adopt HMDS-treated or PVOH-coated transparent papers to minimise variable paper–root adhesion; avoid FDTS in >80 % RH setups.

7. **Automate Pre- and Post-Imaging Logistics**  
   • Robotic plate handling, microfluidic sample cleanup, and error-detection algorithms are now rate-limiting; allocate budget accordingly (>50 % of HTP CAPEX).

8. **Data Transparency**  
   • Publish full image stacks and raw sensor streams under FAIR principles; provide calibration files (spectral, geometric, gas-flux) for re-analysis.

---
## 5. Speculative but Promising Frontiers (Flagged as *High Speculation*)

1. *In-silico trait estimation*: Transformer-based multi-modal models could infer root hydraulic conductance directly from hyperspectral shoots + soil moisture history, bypassing destructive digging.
2. *On-chip metabolomics*: Mars-origin microfluidic automatons adapted to seedlings could deliver picomolar metabolite profiling during germination screens.
3. *Paper micro-robotics*: Electroactive HMDS-paper layers might bend with root exudate gradients, serving as self-reporting root force sensors.

---
## 6. Concluding Synthesis

The last decade revealed that methodological artefacts—from chamber residence times to substrate chemistry and underspecified statistical hierarchies—explain a substantial share of the mismatches that frustrate trait-based predictions of seedling performance. Concurrently, breakthroughs in imaging, sensor technology and functional–structural modelling provide a path to close the predictive gap if (and only if) protocols become **environment-standardised, statistically powered, and ontogenetically explicit**.

By integrating dynamic physiological thresholds (e.g., VPD breakpoints), architectural trajectory metrics, and high-throughput emergence assays with rigorous hierarchical analytics, the community can move beyond the classical SLA/LDMC paradigm toward a genuinely predictive seedling functional ecology relevant to restoration, crop breeding and Earth-system modelling.

*Prepared 2025-06-03. All citations available upon request.*

## Sources

- https://doaj.org/toc/1932-6203
- https://eprints.lancs.ac.uk/id/eprint/154661/
- https://figshare.com/articles/_Correlation_between_quantitative_traits_and_geographical_locations_of_origin_/1629620
- https://escholarship.org/uc/item/2f66029h
- https://juser.fz-juelich.de/search?p=id:%22FZJ-2015-02120%22
- http://web.utk.edu/~nsanders/Pubs/2010-MolecularEcology.pdf
- https://digitalcommons.mtu.edu/michigantech-p/1673
- https://figshare.com/articles/Sizes_of_random_effects_top_four_values_within_each_graph_including_residual_and_fixed_effects_bottom_three_values_expressed_in_standard_deviations_square_roots_of_variance_components_from_Bayesian_multilevel_analyses_of_variance_for_each_trait_/4886036
- https://library.wur.nl/WebQuery/wurpubs/438841
- http://www.documentation.ird.fr/hor/fdi:010079890
- https://escholarship.org/uc/item/6ff3d3rf
- http://hdl.handle.net/1957/42881
- http://fiver.ifvcns.rs/handle/123456789/3742
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/ad/8f/pone.0115732.PMC4275237.pdf
- https://doaj.org/article/0568dcc17cbb4508968dd0695f611a33
- http://www.doria.fi/handle/10024/128271
- https://juser.fz-juelich.de/search?p=id:%22FZJ-2016-03626%22
- https://hal.inria.fr/hal-00827469
- https://doi.org/10.1371/journal.pone.0176959.
- http://hdl.handle.net/10.3389/fpls.2023.1106672.s001
- https://cris.vtt.fi/en/publications/d69f0733-6f70-4209-a54b-6311d2312813
- https://hdl.handle.net/20.500.12636/1577
- https://figshare.com/articles/Multi-trait_multi-environment_Bayesian_model_reveals_G_x_E_interaction_for_nitrogen_use_efficiency_components_in_tropical_maize_-_Fig_1/6711923
- http://www.sciencedirect.com/science/article/pii/S0032386104012753
- https://www.revistas.usp.br/sa/article/view/183015
- http://agritrop.cirad.fr/520493/
- https://www.chimia.ch/chimia/article/view/2005_243
- https://www.mdpi.com/2223-7747/12/15/2866
- http://hdl.handle.net/10355/9121
- https://hal.science/hal-01190209
- http://library.wur.nl/WebQuery/wurpubs/426103
- https://juser.fz-juelich.de/record/873314
- http://eprints.nottingham.ac.uk/37691/
- https://zenodo.org/record/4426180
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-204518
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:104122
- http://hdl.handle.net/2440/127351
- http://hdl.handle.net/10.1371/journal.pone.0206861.t001
- https://figshare.com/articles/Influence_of_the_size_of_the_training_population_TP_of_whole_population_size_on_the_genomic_prediction_accuracy_r_sub_GPA_sub_for_the_seven_traits_seedling_emergence_lodging_resistance_seed_yield_days_to_flowering_DTF_seed_glucosinolate_content_GSL_oil_yi/3045262
- https://research.vu.nl/en/publications/d61d671a-374d-4623-b826-c692ce04bbe0
- http://orcid.org/0000-0002-4562-9131
- https://trepo.tuni.fi/handle/10024/143269
- http://hdl.handle.net/20.500.11850/103905
- http://hdl.handle.net/2117/16451
- https://juser.fz-juelich.de/record/828097
- https://hal.inria.fr/inria-00380520/file/ISCMDS08_Kang.pdf
- https://dx.doi.org/10.3390/s18082711
- http://repozitorij.ung.si/Dokument.php?id=23587&dn=
- http://hdl.handle.net/11568/202361
- https://scholarworks.rit.edu/ritamec/vol18/iss1/15
- https://hal.archives-ouvertes.fr/hal-01173152
- http://dx.doi.org/10.1088/0957-0233/17/12/S05
- https://escholarship.org/uc/item/7d49t9gk
- http://hdl.handle.net/2078.1/174415
- https://figshare.com/articles/Differences_in_plasticity_of_the_parameters_measured_in_i_Q_i_i_acutissima_i_seedlings_at_different_light_levels_and_nitrogen_deposition_rates_/5979190
- https://mel.cgiar.org/reporting/downloadmelspace/hash/9QuzRDmN/v/a4384564ab20f9e2b9644b012357b51c
- https://hal.inrae.fr/hal-03334503
- https://biblio.ugent.be/publication/8663377
- https://repository.publisso.de/resource/frl:6414703
- https://doaj.org/article/0b0deaa95d2f4cce992dac4fa690524a
- https://library.wur.nl/WebQuery/wurpubs/510290
- https://espace.library.uq.edu.au/view/UQ:4206777
- https://research.wur.nl/en/publications/the-acquisitive-conservative-axis-of-leaf-trait-variation-emerges
- http://prodinra.inra.fr/record/281601
- http://hdl.handle.net/11383/1486702
- https://zenodo.org/record/5549334
- http://www.scielo.br/pdf/aabc/v86n4/0001-3765-aabc-0001-3765201420130249.pdf
- http://hdl.handle.net/10179/14853
- http://mems.sandia.gov/tech-info/doc/SPIE.0699.pdf
- https://figshare.com/articles/_Variability_of_the_photosynthetic_efficiency_during_the_24h_laboratory_incubations_/1496088
- https://doaj.org/article/67e1458617e34fbbb54e3ea6210502a2
- https://escholarship.org/uc/item/3mg2x7gh
- http://edepot.wur.nl/257379
- https://biblio.ugent.be/publication/8673407
- https://research.chalmers.se/en/publication/9878
- http://www.publish.csiro.au/?act=view_file&file_id=FP09167.pdf
- https://hal.science/hal-01210019
- https://hdl.handle.net/2164/13307
- http://hdl.handle.net/11368/2998031
- https://zenodo.org/record/3830406
- https://dx.doi.org/10.1016/S0168-1923(02)00023-0
- http://old.scielo.br/scielo.php?script=sci_arttext&pid=S0100-84042007000300002
- https://escholarship.org/uc/item/0cm6p2r3
- http://www.loc.gov/mods/v3
- http://prodinra.inra.fr/record/457240
- https://zenodo.org/record/5703783
- http://digital.library.unt.edu/ark:/67531/metadc620309/
- http://www.publish.csiro.au/nid/103.htm
- http://sio2associates.com/docs/aip_452.pdf
- https://dx.doi.org/10.3390/ma9121019
- http://hdl.handle.net/2097/17543
- https://eprints.lancs.ac.uk/id/eprint/84838/
- http://hdl.handle.net/1959.14/103128
- https://zenodo.org/record/6818410
- http://terraweb.forestry.oregonstate.edu/pubs/Burba_2012.pdf
- http://edepot.wur.nl/39304
- http://hdl.handle.net/10388/13257
- https://oskar-bordeaux.fr/handle/20.500.12278/158421
- https://doaj.org/article/25d82a33c89e4c46893194ad50a67360
- https://digitalcommons.usf.edu/tropical_ecology/682
- https://zenodo.org/record/5009280
- http://repositorium.sdum.uminho.pt/bitstream/1822/24860/1/17601-o37p1_MSousa_SHpaper_ACSApplMatInterf_2013.pdf
- http://hdl.handle.net/10197/8093
- https://hal.inrae.fr/hal-02884893/document
- https://hal.inria.fr/inria-00121501
- http://edepot.wur.nl/306160
- http://www.journals.elsevier.com/agriculture-ecosystems-and-environment/
- http://hdl.handle.net/11585/678439
- https://hdl.handle.net/11250/2739374
- https://digitalcommons.unl.edu/biosysengfacpub/760
- https://juser.fz-juelich.de/search?p=id:%22FZJ-2023-02611%22
- https://doaj.org/article/3cd58aa173054fbda3ef611ddbe96499
- http://hdl.handle.net/11588/694776
- https://juser.fz-juelich.de/record/188889
- https://dx.doi.org/10.3390/polym10040448
- http://agritrop.cirad.fr/556068/
- http://eprints.nottingham.ac.uk/41078/
- https://ezproxy.uws.edu.au/login?url=https://doi.org/10.1071/BT12225
- https://revista.ufrr.br/agroambiente/article/view/5166
- http://hdl.handle.net/10.6084/m9.figshare.7163417.v1
- http://www.scopus.com/home.url)
- https://dx.doi.org/10.3390/agronomy8050071
- https://eprints.qut.edu.au/31240/
- http://publica.fraunhofer.de/documents/N-336546.html
- https://hal.archives-ouvertes.fr/hal-01512173
- https://doaj.org/article/97b3aec8a4e04688a17c69732ae1eadc
- https://doaj.org/article/af0203044b334087b744d5dd5e7309c2
- http://www.alice.cnptia.embrapa.br/alice/handle/doc/1118821
- https://nrc-publications.canada.ca/fra/voir/objet/?id=b1af95b7-f83e-4c7b-baa7-979c78dc17b9
- https://dr.lib.iastate.edu/handle/20.500.12876/105917
- https://doaj.org/article/6756e1195b88482bb092ef06f9e3dff0
- http://hdl.handle.net/11588/768703
- http://hdl.handle.net/10255/dryad.49806
- http://hdl.handle.net/11343/194879
- https://hal-centralesupelec.archives-ouvertes.fr/hal-00872390
- http://hdl.handle.net/2286/R.I.8870
- https://juser.fz-juelich.de/search?p=id:%22FZJ-2022-00412%22
- https://zenodo.org/record/7054485
- http://publikace.k.utb.cz/handle/10563/1009028
- http://digital.library.unt.edu/ark:/67531/metadc702298/
- http://hdl.handle.net/1853/58249
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S187770581300091X/MAIN/application/pdf/16c00c21c02e9e6595eb9964eac30d5b/main.pdf
- http://library.wur.nl/WebQuery/wurpubs/387436
- http://hdl.handle.net/1957/10909
- https://hdl.handle.net/2027.42/155513
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S2214574515000334/MAIN/application/pdf/fd1269725ba22c12c5ccd1ebec953587/main.pdf
- https://doi.org/10.48693/206
- https://juser.fz-juelich.de/record/202330
- https://digitalcommons.unl.edu/dissertations/AAI29167763
- http://library.soton.ac.uk/datarequest
- https://doaj.org/article/0739233af18f4e2a86f6391e8ea8a13b
- http://prodinra.inra.fr/record/344282
- https://cris.vtt.fi/en/publications/67d68f25-e0be-4f96-b106-4e378394e49d
- https://figshare.com/articles/Universal_Microfluidic_Automaton_for_Autonomous_Sample_Processing_Application_to_the_Mars_Organic_Analyzer/2384803
- https://doi.org/10.1051/epjap:2005071
- https://orbi.uliege.be/handle/2268/152116
- http://hdl.handle.net/2078.1/227038
- https://escholarship.org/uc/item/57966765
- https://eprints.lancs.ac.uk/id/eprint/79809/
- http://hdl.handle.net/10.3389/fevo.2022.983192.s001
- http://hdl.handle.net/1885/186100
- https://figshare.com/articles/Mean_rates_of_gas_exchange_during_Experiment_2_in_2017_/6345962
- https://doaj.org/article/990cb1ce17844c3685265fc738c49aaa
- https://dspace.unitus.it/handle/2067/30951
- http://edepot.wur.nl/178287
- http://hdl.handle.net/10.1371/journal.pone.0212200.g002
- https://dx.doi.org/10.3390/agronomy8050063
- https://doaj.org/article/920588c9f51e4914a677f6df0613bc8d
- http://hdl.handle.net/1885/66720
- https://hal.archives-ouvertes.fr/hal-02274473
- http://digitalcommons.library.umaine.edu/cgi/viewcontent.cgi?article%3D1250%26context%3Detd
- https://imisrise.tappi.org/TAPPI/Products/11/PAP/11PAP32.aspx
- https://institut-agro-dijon.hal.science/hal-03279153
- http://hdl.handle.net/11858/00-001M-0000-0014-79B5-8
- http://hdl.handle.net/10.1371/journal.pone.0210183.t002
- http://hdl.handle.net/1885/74050
- http://hdl.handle.net/10255/dryad.129878
- http://dx.doi.org/10.5194/bg-13-903-2016
- http://eprints.nottingham.ac.uk/44225/
- https://figshare.com/articles/_Shifting_correlations_between_plant_traits_and_species_abundance_at_the_plot_scale_over_a_range_of_soil_organic_matter_a_and_soil_total_nitrogen_content_b_/669891
- https://figshare.com/articles/_Shifting_correlations_between_plant_traits_and_species_abundance_at_the_plot_scale_over_a_range_of_air_humidity_a_and_soil_moisture_contents_b_and_c_/669889
- https://zenodo.org/record/7109006
- https://doaj.org/toc/1424-8220
- https://dspace.library.uu.nl/handle/1874/383047
- http://www.nrcresearchpress.com/doi/abs/10.1139/cjb-2016-0148
- http://hdl.handle.net/10255/dryad.51561
- https://figshare.com/articles/_Shifting_correlations_between_plant_traits_and_species_abundance_at_the_plot_scale_over_a_range_of_soil_pH_/669892
- https://doi.org/10.3390/app12189005
- https://hal.inrae.fr/hal-04169477/document
- http://hdl.handle.net/10150/644446
- http://agritrop.cirad.fr/556048/
- http://hdl.handle.net/11858/00-001M-0000-0027-5F93-7
- http://library.wur.nl/WebQuery/wurpubs/431562
- http://hdl.handle.net/10150/670193
- http://hdl.handle.net/20.500.11897/237697
- http://digital.library.unt.edu/ark:/67531/metadc710700/
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:102319
- https://zenodo.org/record/211797
- https://juser.fz-juelich.de/record/281945
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1369526615000266/MAIN/application/pdf/6a2e21a8b8a2cc332456ef8877b9f5d6/main.pdf
- https://juser.fz-juelich.de/record/860087
- http://hdl.handle.net/2078.1/262750
- http://hdl.handle.net/10.1371/journal.pone.0206210.g001
- https://hal.archives-ouvertes.fr/hal-03324566/file/giab052.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-68234
- https://juser.fz-juelich.de/record/280592
- https://figshare.com/articles/_Phenotype_of_high_and_low_vigor_bulks_in_seeds_collected_at_4_5_and_6_weeks_after_heading_in_2013_/1278112
- https://doaj.org/article/012ed85d53604cb1b7d34299d3cdcd96
- https://hal.univ-angers.fr/hal-03114726
- http://prodinra.inra.fr/record/267832
- https://figshare.com/articles/_Relationships_between_crop_growth_rate_CGR_and_leaf_functional_trait_values_a_leaf_dry_matter_content_LDMC_b_leaf_area_LA_and_relationships_between_crop_N_acquisition_rate_CNR_and_leaf_functional_trait_values_c_leaf_dry_matter_content_LDMC_c_leaf_area_LA/1342846
- http://hdl.handle.net/10255/dryad.100016
- http://umpir.ump.edu.my/id/eprint/6962/1/Assessment%20Of%20Organic%20Acid-Rich%20Bio-Sap%20To%20Generate%20Electricity.pdf
- http://hdl.handle.net/1957/59338
- http://catalog.lib.kyushu-u.ac.jp/handle/2324/8173/KJ00004506792.pdf
- http://acta.bibl.u-szeged.hu/64907/1/proceedings_of_isaep_2019_461-464.pdf
- http://library.wur.nl/WebQuery/wurpubs/431467
- https://doaj.org/article/76b824497dfc4b1fb28781f3f96c019c
- http://dare.ubvu.vu.nl/bitstream/handle/1871/21464/162086.pdf%3Bjsessionid%3D9BA25E1FC05C82EAA891EDD7C4DEDE10?sequence%3D2
- http://hdl.handle.net/2440/90086
- http://agritrop.cirad.fr/507958/
- http://library.wur.nl/WebQuery/wurpubs/425029
- https://research.aalto.fi/files/61232635/1_s2.0_S0141813021005651_main.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.88.2732
- https://hal.archives-ouvertes.fr/hal-01595406
- http://hdl.handle.net/11858/00-001M-0000-0029-2883-8
- http://hdl.handle.net/2072/440433
- http://lup.lub.lu.se/student-papers/record/8917201