# Key Mechanisms in Invasion Ecology – A Stage-Structured, Taxonomically Broad, and Forward-Looking Synthesis

*Date compiled: 2025-06-03*

## Executive Summary

Invasion ecology has matured from a narrative discipline into a quantitatively rigorous, data-integrative science.  Across the four canonical stages—**introduction, establishment, spread, impact**—a small set of first-order mechanisms explains most empirical variance, while a rapidly expanding suite of emerging processes (eco-evolutionary feedbacks, microbiome shifts, coupled human–natural dynamics, and climate interactions) adds important second-order nuance.  The most universal predictor remains **propagule pressure (PP)**, but modern work clarifies its fat-tailed statistical structure, its nonlinear coupling with **colonization pressure (CP)**, and the way vector-specific filters transform raw PP into establishment-effective PP.  Hierarchical Bayesian models, machine-learning architectures fed by AIS and global trade streams, and network-based early-warning indicators now allow quasi-real-time risk forecasting.  Below we provide a three-page, stage-by-stage synthesis of mechanisms, embed quantitative touchstones from >100 recent studies, and flag speculative yet plausible future directions.

---

## 1 Conceptual Foundations

1. **Terminological Precision** –  *Propagule pressure* is the number of individuals of a given species released; *colonization pressure* is the number of species released at a site.  Simulations and empirical syntheses show PP and CP are non-linearly coupled but must be modelled separately (Lockwood, Cassey & Blackburn 2009).  CP acts as the statistical null for patterns of non-native richness, whereas PP is the default null for establishment probability.
2. **Stage Continuum** –  Modern frameworks map >25 classical hypotheses (enemy release, EICA, novel weapons, etc.) onto a stage-structured continuum.  The **PAB+H paradigm** (Propagule, Abiotic, Biotic + Human forcing) and **Coupled Human–Natural Systems (CHANS)** lenses reduce theoretical redundancy and connect ecological drivers to feedbacks from trade, policy, and behaviour.
3. **Fat-Tailed Risk** –  Across vectors, PP distributions are highly leptokurtic.  In global ballast traffic, single discharges have contained 131–2 966 × the median propagule load; ballast volume proxies explain only R² ≈ 0.058 (port) to 0.169 (ocean-basin) of true PP variance.  These rare “mega-load” events dominate risk because they routinely breach demographic or genetic Allee thresholds.

---

## 2 Introduction Stage: Arrival Mechanisms

### 2.1 Vector Architecture and Filters

• **Shipping & Ballast Water** –  Ballast-water exchange often fails to reduce propagules and can raise dinoflagellate counts.  IMO D-2 standards (≤10 live org m⁻³) only reduce risk when community PP <25 org m⁻³; CP remains a key driver across linear→logistic dose–response functions.  Hybrid treatments (chlorination + exchange) and taxon-specific thresholds are essential.

• **Trade in Living Commodities** –  USDA interception data (2005-2014) show a mean 3 % arrival probability for arthropod pests; fresh herbs carry 2–10 × higher risk.  Seven of ten highest-risk countries are in the Western Hemisphere, suggesting future SSP5-like trade growth will strain phytosanitary capacity.

• **Recreational & Aquaculture Vectors** –  Gravity models for spiny waterflea spread indicate the unconstrained form best reproduces boater traffic, while doubly constrained forms most accurately predict establishment, highlighting the importance of model-vector fit.

• **Arctic & High-Latitude Routes** –  Destinational shipping is outpacing trans-Arctic shortcuts; Valdez (AK) and Churchill (MB) receive the highest ballast PP.  Under RCP 8.5 conditions, six of eight screened invaders will meet reproductive tolerances in Svalbard, underscoring emerging high-latitude risk.

### 2.2 Propagule Pressure Mechanics

• **Size, Frequency, Timing** –  Microcosms (Crassostrea gigas, Tribolium, protists) show that many small pulses can outperform one large pulse in terms of settlement and persistence—particularly for slow growers and where predation pressure exists.  In contrast, single large pulses benefit fast growers.

• **Transport-Phase Selection** –  Surviving individuals are often pre-adapted to vector stressors, enriching for adaptive genotypes (Bemisia tabaci, ballast zooplankton).  Ignoring such winnowing underestimates establishment probability by conflating raw and effective PP.

• **Demographic Critical Band** –  Bayesian meta-analyses across >500 studies converge on a steep rise in establishment once 10–100 individuals are introduced, with effect sizes ≈20–30 % larger in animals than plants.

### 2.3 Emerging Toolkits

• **Hierarchical Bayesian Fusion** converts coarse ballast-volume proxies into absolute PP PDFs, capturing fat tails and enabling voyage-specific risk.

• **AIS-Coupled Dashboards** generate 12 h–multi-day berth-level arrival forecasts (ETA MAE ≈5 days; spatial error ≈6 km, R² > 0.98), facilitating dynamic inspection prioritisation and simultaneous CO₂/NOₓ mitigation analytics.

---

## 3 Establishment Stage: Surviving the Filter

### 3.1 Abiotic & Biotic Filters

• **Climate** –  For terrestrial arthropods in Great Britain, climate warming is the only driver with strong empirical evidence for establishment surges.  Trait-based delay-differential models show tropical ectotherms gain a thermal-niche edge as +2–4 °C warming pushes temperate zones into their optimum.

• **Diurnal Variability** –  Across 32°–50° N forest soils, daily temperature variance—more than mean temperature—explains latitudinal increases in microbial turnover, creating over-dispersed communities that can resist or facilitate invaders depending on phylogenetic distance.

• **Resource & Community Structure** –  Soil-heating experiments demonstrated that reduced resident diversity and predator release, not carbon availability, drove bacterial invasion success.

### 3.2 Trait Syndromes

• **Plants** –  A 117-study meta-analysis shows consistent invader advantages across six performance trait groups; specific leaf area (SLA) emerges as the single most robust predictor of transition from naturalized → invasive.  In Australia, invasives have +25–30 g m⁻² SLA, longer flowering, greater height.

• **Aquatic Animals** –  Meta-analysis of marine + freshwater taxa pinpoints two universal traits: high consumption & growth rates, and enhanced predator avoidance.  The evidence base is temperate-biased; tropical and polar data are a priority.

• **Behavioural Risk Traits** –  Hemimysis anomala maintains feeding under predation, while native Mysis salemaai reduces feeding—demonstrating how boldness moderates establishment.

### 3.3 Genetic & Evolutionary Dynamics

• **Standing Genetic Variation** can compensate for low founder numbers; outbred Bemisia tabaci founders boosted R₀ irrespective of N.  Whole-genome reconstructions show multiple introductions offset severe bottlenecks, challenging the “genetic paradox of invasion.”

• **Rapid Adaptation** –  Round goby evolved heritable body-shape divergence within <15 generations during a stepping-stone spread; functional responses in Pseudorasbora parva shifted from Type II → Type III on Daphnia in Europe, amplifying prey-density-dependent impacts.

• **Genomic Shock & Epigenetics** –  Stress-induced transposable‐element activation can generate heritable novelty, offering a mechanism for rapid adaptation even in clonally propagating invaders.

### 3.4 Microbiome & Pathogen Interactions

• Bayesian non-parametric ordination (normalized GG process) partitions variance across P, A, B + H axes and reveals how resident microbiome turnover can inhibit or facilitate invader microbiota.  Temperature-fluctuation paradox studies show parasites acclimate faster than hosts, increasing infection risk under variability.

---

## 4 Spread Stage: From Local Footprint to Regional Presence

### 4.1 Dispersal Kernels and Gravity Processes

• **Gravity-Weibull Models** fitted to Aleurodicus dispersus and Bythotrephes reveal that jointly estimating local build-up, human-mediated transport, and natural spread yields superior risk maps; production-constrained formulations offer a data-effort compromise.

• **Reaction–Diffusion Embedding** –  Eurasian Collared-Dove models that embed PDEs inside hierarchical detection frameworks propagate observation error and deliver absolute density maps, not merely presence–absence.

### 4.2 Climate-Assisted Expansion

• **Sleeper Populations** –  Models suggest >70 % of future UK alien range expansion will come from natural spread of existing casual populations.  Targeted surveillance near foci is the most cost-effective mitigation compared with broad border controls.

• **Thermal-Performance Edges** –  Trait-based metabolic theory predicts tropical ectotherms will prosper under warming; Daphnia–Ordospora experiments validated model forecasts of epidemic thresholds at +2 °C.

### 4.3 Behaviour & Physiology During Spread

• **Physiological Limits** –  Round goby maintains 61 % survival at 30 PSU despite a 30 % drop in aerobic scope, supporting a 30 km yr⁻¹ spread toward the North Sea.

• **Functional-Trait Plasticity** –  In Dutch rivers, invasive gobies span both specialist and generalist feeding profiles, predicting competition hotspots with native benthivores.

---

## 5 Impact Stage: Ecological & Socio-Economic Consequences

### 5.1 Per-Capita vs Population-Level Impact

• European green crab Carcinus maenas exhibits the highest functional response ratio among tested predators; because densities are >6 × those of native Cancer irroratus, scenario models project severe ecosystem impact.  Impact assessments must couple per-capita effects with expected abundance.

### 5.2 Trophic Cascades and Network Effects

• Meta-synthesis of 56 field studies shows invaders often depress diversity within their own trophic layer but enhance diversity in higher trophic levels (e.g., sessile invaders facilitate mobile consumers).  Trophic position thus modulates net biodiversity outcomes.

• Interaction-network topology metrics (degree, clustering) flag ecosystem-state shifts earlier than classical autocorrelation indicators, implying invader-driven regime shifts could be forecast using spatial correlation networks.

### 5.3 Coupled Human–Natural Feedbacks

• Non-native impacts alter trade, policy, and consumer behaviour, which in turn modulate PP and management.  These CHANS feedbacks are largely absent from current risk models but are essential for long-term forecasting and adaptive governance.

---

## 6 Cross-Cutting Emerging Mechanisms

1. **Eco-Evolutionary Feedbacks** –  Rapid adaptation changes trait distributions within years, feeding back into competitive and predator–prey dynamics.
2. **Microbiome Shifts** –  Invaders can re-shape resident microbial communities; conversely, resident microbiomes can pre-empt or facilitate invaders.
3. **Environmental Stochasticity** –  Enhanced temperature variance boosts invasion when residents are fluctuation-mal-adapted; future climates are expected to increase such variance.
4. **Genetic Introgression & Hybridisation** –  Trait-specific allele introgression in sunflowers illustrates how hybridisation can accelerate adaptation.
5. **Epigenetic & Transposon-Mediated Plasticity** –  “Genomic shock” offers a mechanism for rapid phenotypic innovation without standing genetic diversity.

---

## 7 Analytical & Technological Advances

• **Hierarchical Bayesian Toolchain** –  Unifies ecological samples, trade statistics, and detection error; provides full posterior predictive distributions of PP, spread, and impact.

• **Machine-Learning on AIS** –  Real-time ETA and anchor-time predictions (MAE ≈5 days) feed dynamic quarantine resource allocation.

• **Early Warning Systems (EWS)** –  Spectral-slope and network-topology indicators outperform AR(1) in periodically forced ecosystems; could be embedded in automated surveillance of ballast discharge or community time series.

---

## 8 Management Implications & Solutions Beyond Conventional Wisdom

1. **Dynamic Inspection Prioritisation** –  Fuse AIS-driven propagule forecasts with Bayesian risk models to triage high-PP arrivals **before** docking.
2. **Hybrid Treatment Regimes** –  Couple chlorination/UV with exchange, adapting exposure time to taxa-specific mortality curves, particularly for dinoflagellates.
3. **Trait-Informed Weed Risk Assessment** –  Integrate SLA, native-range size, and seed weight into WRA algorithms; machine-learning prototypes already achieve AUROC 0.87.
4. **Surveillance of Sleeper Populations** –  Redirect funds from borders to local foci where >70 % of future spread is predicted to originate; leverage eDNA and UAV line-transect imaging.
5. **CHANS-Aware Policy Loops** –  Embed economic and behavioural feedbacks into predictive models to avoid perverse outcomes (e.g., trade diversion due to stringent unilateral regulations).
6. **Speculative (Flagged)**
   • *Gene-Drive Bio-Control* –  Next-gen CRISPR-based drives targeting invasive rodent populations on islands; ethical and ecological risks high.
   • *Synthetic Microbiome Shields* –  Designer microbial consortia that out-compete or pre-date invader-associated microbiota.
   • *Real-Time Satellite and Lidar Detection* –  High-resolution hyperspectral platforms could spot invasive plant nutrient signatures before canopy closure.

---

## 9 Research Gaps & Priorities

1. **Tropical & Polar Data Deficits** –  Most trait and impact syntheses are temperate-biased; high-latitude microbial dynamics and tropical aquatic invader traits remain under-sampled.
2. **Vector-Specific Selection Filters** –  Need controlled experiments quantifying genotype × transport stress interactions across taxa.
3. **Microbiome Mechanisms** –  Few field studies link microbiome turnover to invasion outcome; integrating non-parametric Bayesian ordination into field surveys can fill this gap.
4. **Coupled Feedback Quantification** –  Formal CHANS models require multi-disciplinary datasets linking ecological impact to trade and consumer behaviour.
5. **Standardised Propagule Metrics** –  Adoption of absolute PP estimation protocols (e.g., hierarchical ballast models) is necessary for cross-system comparability.

---

## 10 Conclusion

While invasion ecology hosts a rich tapestry of hypotheses, a small number of mechanisms—fat-tailed propagule pressure, abiotic filtering, key trait syndromes, rapid adaptation, and human-mediated dispersal—recurrently dominate explanatory power.  Emerging layers—microbiomes, epigenetic flexibility, stochastic climate variance, and CHANS feedbacks—modify but rarely overturn these fundamentals.  Methodological revolutions in Bayesian data fusion, machine learning, and network EWS enable proactive rather than reactive management.  The field’s next leap will couple these tools with socio-economic feedbacks and biotechnological interventions, pushing toward real-time, adaptive governance of biological invasions.

> *Prepared for experienced analysts; all quantitative figures trace back to peer-reviewed sources or large-scale meta-analyses cited in the accompanying learning set.*

## Sources

- https://doaj.org/toc/1932-6203
- https://digitalcommons.unl.edu/dissertations/AAI10102328
- http://dspace.stir.ac.uk/bitstream/1893/3293/1/harris2011.pdf
- http://hdl.handle.net/2429/13696
- https://doaj.org/toc/2224-4263
- https://hal.archives-ouvertes.fr/hal-03781186/file/annurev-ecolsys-032522-015551.pdf
- http://era.daf.qld.gov.au/id/eprint/3044/
- http://biology.unm.edu/Whitney/Whitney%20Reprints/Whitney%20et%20al%202015%20Mol%20Ecol.pdf
- https://doi.org/10.1146/annurev-ecolsys-012021-095454
- http://hdl.handle.net/10.1371/journal.pntd.0007213.g001
- http://hdl.handle.net/10.1371/journal.pbio.3002260.s018
- https://zenodo.org/record/4014876
- https://hal.sorbonne-universite.fr/hal-03531081/file/e2116211118.full.pdf
- https://zenodo.org/record/4404477
- https://doi.org/10.1007/s10530-012-0284-z
- https://www.researchgate.net/profile/Emma_Johnston/publication/224816992_Propagule_pressure_and_disturbance_interact_to_overcome_biotic_resistance_of_marine_invertebrate_communities/links/0fcfd50546192e2062000000.pdf?origin%3Dpublication_detail
- https://doi.org/10.1111/j.1365-294X.2011.05322.x
- https://dspace.library.uu.nl/handle/1874/334678
- http://ir.ibcas.ac.cn/handle/2S10CLM1/25701
- https://figshare.com/articles/_Estimates_of_selection_pressures_acting_on_the_HSP70h_and_coat_protein_CP_genes_of_global_PBNSPaV_isolates_/1148453
- https://figshare.com/articles/_Analysis_of_molecular_variance_AMOVA_of_H_hippophaecolus_populations_/360040
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/7a/e5/pone.0106336.PMC4152270.pdf
- http://www.magpiedesign.com/miller/documents/Miller
- http://www.ufz.de/export/data/global/55141_Pysek%2C%20Jarosik%2C%20Pergl%2C%20Moravcova%2C%20Chytry%2C%20Kuhn-Temperate%20trees%20as%20global%20invaders_BiolInvas2014.pdf
- http://hdl.handle.net/10057/7120
- https://research.utwente.nl/en/publications/bf3c4491-24dc-42b4-9b62-5b823ae2a372
- https://figshare.com/articles/Parsing_propagule_pressure_Simulated_and_experimental_disentanglement_of_introduction_size_and_number_of_introductions_for_colonizing_individuals/4648865
- http://hdl.handle.net/11392/2399632
- http://dx.doi.org/10.13039/501100000780
- https://figshare.com/articles/AIS_spatial_data_files/6051950
- https://hal.inria.fr/hal-02139554/file/article_bajeux_grognard_mailleret2019_JTB.pdf
- https://hal.science/hal-00662157
- http://prodinra.inra.fr/record/478105
- http://hdl.handle.net/1959.14/1142050
- https://figshare.com/articles/_Effect_of_species_traits_on_invasiveness_invasive_or_naturalized_but_non_invasive_Models_I_and_dominance_percent_cover_in_invaded_communities_Models_II_of_alien_herbaceous_plants_/1392226
- https://escholarship.org/uc/item/576611s3
- http://hdl.handle.net/1807/101664
- http://urn.kb.se/resolve?urn=urn:nbn:se:lnu:diva-132248
- https://hal.science/hal-00908377
- https://doaj.org/article/d1d487f51ae94e60811dbab32e2f30d3
- https://pure.knaw.nl/portal/en/publications/fd5fbf8a-2289-4fd1-8898-029ca68192e7
- https://doaj.org/article/b8c2ab15a9f54e5fbb124052fd955684
- http://hdl.handle.net/1959.14/356418
- https://zenodo.org/record/5968360
- http://hdl.handle.net/2440/64506
- http://hdl.handle.net/2066/289158
- http://www.documentation.ird.fr/hor/fdi:010070995
- https://biblio.ugent.be/publication/880039/file/880040
- http://hdl.handle.net/10.1371/journal.pone.0282140.t001
- http://hdl.handle.net/10.3389/fmicb.2019.00674.s001
- http://eprints.bournemouth.ac.uk/23778/1/Functional%20response%20cyprinid%20invaders_accepted.pdf
- https://digitalcommons.usf.edu/bin_facpub/93
- https://zenodo.org/record/8266131
- https://figshare.com/articles/The_fruit_and_vegetable_import_pathway_for_potential_invasive_pest_arrivals/5898043
- https://hal.inrae.fr/hal-04007040/document
- https://zenodo.org/record/4486289
- http://urn.fi/URN:NBN:fi:jyu-201902061445
- https://zenodo.org/record/3754481
- http://hdl.handle.net/20.500.11794/69616
- http://www.loc.gov/mods/v3
- https://hal-mines-paristech.archives-ouvertes.fr/hal-03726782/file/ISAP2022Renaud.pdf
- http://hdl.handle.net/10355/9117
- https://nsuworks.nova.edu/cnso_osj/january-2018/day2/18
- https://hdl.handle.net/10182/8808
- http://hdl.handle.net/10356/70796
- http://resolver.tudelft.nl/uuid:f3026c06-e666-40b3-9e07-2242998a2e99
- https://orcid.org/0000-0003-1896-3860
- https://digitalcommons.stmarys-ca.edu/school-science-faculty-works/73
- http://resolver.tudelft.nl/uuid:cba0ef59-dd23-49aa-91d5-bed239e27395
- http://ir.ibcas.ac.cn/handle/2S10CLM1/20620
- https://www.springer.com/us/book/9789400721135
- https://figshare.com/articles/_Transmission_dynamics_of_genotypes_in_isolates_resistant_A_and_sensitive_B_to_first_line_drugs_/1446434
- http://hdl.handle.net/1807/100857
- http://edepot.wur.nl/234126
- http://handle.unsw.edu.au/1959.4/52666
- http://dx.doi.org/10.1890/ES11-000375.1
- https://epljournal.edpsciences.org/10.1209/0295-5075/121/10002/pdf
- http://doi.org/10.1371/journal.pone.0045306
- https://library.wur.nl/WebQuery/wurpubs/503987
- https://doi.org/10.1079/9781789242171.0009
- http://planet.botany.uwc.ac.za/nisl/invasives/refs/vermeij.pdf
- https://figshare.com/articles/_Hierarchical_analysis_of_molecular_variance_AMOVA_across_topographically_defined_populations_of_Pityophthorus_juglandis_in_the_USA_/1313413
- https://doi.org/10.1002/ece3.8348
- https://research.rug.nl/en/publications/1699ea3e-8e24-4058-a205-8c9db288db5a
- https://doaj.org/toc/1755-4365
- https://zenodo.org/record/4962782
- https://scholar.uwindsor.ca/etd/3210
- https://figshare.com/articles/Selection_pressure_analysis_of_the_RSV_ON1_genotype_of_the_second_hypervariable_region_of_G_protein_gene_using_SLAC_and_FEL_method_/4231079
- https://hal.inrae.fr/hal-02667769
- http://redpath-staff.mcgill.ca/ricciardi/Ricciardi_Elton_C17.pdf
- https://www.webofscience.com/api/gateway?GWVersion=2&SrcApp=PARTNER_APP&SrcAuth=LinksAMR&KeyUT=WOS:000388154100004&DestLinkType=FullRecord&DestApp=ALL_WOS&UsrCustomerID=42fe17854fe8be72a22db98beb5d2208
- https://dx.doi.org/10.1002/ecy.1852
- http://www.europe-aliens.org/pdf/Pseudorasbora_parva.pdf
- https://hdl.handle.net/1813/41099
- http://hdl.handle.net/20.500.11794/127023
- https://zenodo.org/record/4119425
- http://hdl.handle.net/1969.1/174464
- http://hdl.handle.net/10.1038/s41598-020-76602-4
- http://hdl.handle.net/10036/3858
- https://www.repository.cam.ac.uk/handle/1810/263577
- https://doi.org/10.1111/j.1472-4642.2011.00796.x
- https://cdr.lib.unc.edu/downloads/sn00b6291
- https://orbilu.uni.lu/handle/10993/58609
- https://figshare.com/articles/_Model_results_for_hierarchical_models_of_statistical_moments_/830887
- http://hdl.handle.net/1885/64576
- http://datacite.org/schema/kernel-4
- http://hdl.handle.net/20.500.11794/432
- http://hdl.handle.net/10044/1/79521
- http://hdl.handle.net/2440/64495
- http://hdl.rutgers.edu/1782.2/rucore10002600001.ETD.000052190
- https://zenodo.org/record/7030116
- http://hdl.handle.net/1807/107
- https://centaur.reading.ac.uk/98364/1/23022044_Prettyman_Thesis_Joshua%20Prettyman.pdf
- https://dspace.library.uu.nl/handle/1874/416158
- https://orbilu.uni.lu/handle/10993/50892
- https://hal.science/hal-03222798
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/0e/09/pone.0069775.PMC3732293.pdf
- https://zenodo.org/record/8297601
- https://figshare.com/articles/_Modelling_the_Dynamics_of_an_Experimental_Host_Pathogen_Microcosm_within_a_Hierarchical_Bayesian_Framework_/763028
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-23275
- http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3187879/pdf/cib0403_0247.pdf
- https://dx.doi.org/10.1086/379204
- https://figshare.com/articles/Dissecting_the_null_model_for_biological_invasions_A_meta-analysis_of_the_propagule_pressure_effect/6173318
- https://researchrepository.murdoch.edu.au/id/eprint/18175/
- https://hal.archives-ouvertes.fr/hal-01608618
- http://ifasstat.ifas.ufl.edu/DorazioWebSite/Publications/hooten_wikle2007.pdf
- https://doi.org/10.1111/1365-2656.12155
- https://figshare.com/articles/How_to_incorporate_information_on_propagule_pressure_in_the_analysis_of_alien_establishment_success_-_simulation_data/5537884
- http://hdl.handle.net/10.1371/journal.pone.0207359.g002
- https://zenodo.org/record/8178933
- https://dspace.library.uu.nl/handle/1874/283849
- https://figshare.com/articles/_Population_dynamics_of_genetic_diversity_in_human_metapneumovirus_/694127
- http://hdl.handle.net/10261/241194
- https://digital.library.unt.edu/ark:/67531/metadc949512/
- http://hdl.handle.net/10.1371/journal.pone.0208505.g002
- http://ir.gig.ac.cn/handle/344008/51686
- https://doi.org/10.1007/s10530-011-0070-3
- https://figshare.com/articles/_Negative_selection_pressure_analyses_at_specific_codons_of_the_VP1_region_of_Kenyan_EV68_isolates_/1115674
- https://doi.org/10.1007/s10750-014-2150-8
- http://hdl.handle.net/11383/2103172
- https://oceanrep.geomar.de/id/eprint/50098/1/Paolucci.pdf
- https://doaj.org/toc/1545-7885
- https://eprints.whiterose.ac.uk/180393/1/2019%20-%20Mofu%20freshwater%20Biol_mult_pred.pdf
- https://doaj.org/article/10cb945aa9054e77b08af1a582f0251f
- http://nbn-resolving.de/urn:nbn:de:bsz:352-164384
- https://zenodo.org/record/4931661
- https://digitalcommons.murraystate.edu/postersatthecapitol/2011/Murray/8
- http://pqdtopen.proquest.com/#viewpdf?dispub=1555186
- http://hdl.handle.net/1928/32960
- http://www.nusl.cz/ntk/nusl-53260
- https://pub.uni-bielefeld.de/record/2915203
- http://hdl.handle.net/11420/3760
- http://hdl.handle.net/10019.1/111626
- https://zenodo.org/record/7958223
- https://hal.inrae.fr/hal-02591043
- https://hal.archives-ouvertes.fr/hal-00682501
- https://nsuworks.nova.edu/occ_stuetd/491
- https://hal-agrocampus-ouest.archives-ouvertes.fr/hal-02063295
- http://nora.nerc.ac.uk/id/eprint/5949/
- https://biblio.ugent.be/publication/8651220
- https://dspace.library.uu.nl/handle/1874/281753
- http://dx.doi.org/10.1111/j.1365-2486.2009.01882.x
- https://hal.science/hal-01612032
- https://hal.inrae.fr/hal-02647522
- https://doaj.org/article/76fc7666c8ef41f6a1322798bf458fe2
- http://digitool.Library.McGill.CA:80/R/?func=dbin-jump-full&object_id=117064
- http://apo.ansto.gov.au/dspace/handle/10238/7261
- http://urn.fi/URN:NBN:fi:jyu-201704242049
- https://zenodo.org/record/4072168
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.6300
- http://nbn-resolving.de/urn:nbn:de:bsz:352-133266
- http://labs.eeb.utoronto.ca/barrett/pdf/ColauttiEtAl2006Propagule_Pressure.pdf