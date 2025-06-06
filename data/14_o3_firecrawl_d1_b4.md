# Identifying Critical Habitat for Peary Caribou – A Comprehensive, Defensible Protocol

*Prepared for analysts working at the interface of ecological science, Indigenous Knowledge (IK/IQ), and regulatory decision-making under Canada’s Species at Risk Act (SARA)*  
*Date: 3 June 2025*

---

## Executive Summary

Canada’s 2022 Recovery Strategy for Peary Caribou (Rangifer tarandus pearyi) formally listed **> 90 % sea-ice crossing corridors (≥ 10 cm thick)** as critical habitat but deferred most terrestrial habitats to a “schedule of studies,” citing incomplete spatial–temporal data. The present report synthesises the latest peer-reviewed science, Indigenous Knowledge, climate projections and analytical innovations (up to March 2025) to build a **step-wise, defensible protocol** for delineating the *full suite* of critical habitat (CH) for Peary Caribou. Key take-aways:

1. **Sea-ice is only half the story**. Bayesian and machine-learning models integrating IK, aerial surveys and SNOWPACK outputs show that snow density < 350 kg m⁻³, forb/dwarf-shrub tundra (Banks) or cryptogam/rush/grass tundra (Melville) are equally critical during spring–summer.
2. **IK is transformative**. Injecting IK covariates as Bayesian priors shifted spatial predictions of preferred habitat by > 30 % (ringed-seal analogue) and raised MaxEnt AUC for Peary Caribou from 0.58 to 0.70 on Banks–Melville islands.
3. **Connectivity matters**. Circuitscape centrality analyses highlight the Bathurst Island complex as the keystone node for archipelago-wide gene flow; projected ice loss by 2041-2060 severs Western QEI → Prince of Wales/Somerset/Boothia routes without intervention.
4. **A four-population management lens is essential**: (1) Banks–NW Victoria, (2) Western QEI, (3) Eastern QEI, (4) Prince of Wales–Somerset–Boothia.
5. **Regulatory precedent exists**. The 2023 USFWS Alexander Archipelago Wolf assessment accepted Tlingit TEK as “best available science,” setting a template for SARA-based CH delineation that treats IK as co-equal evidence.

The protocol below yields a map set and meta-data package meeting the *critical habitat test* (“biophysical attributes required for recovery, identified with sufficient precision”) while anticipating climate-driven shifts to ~2060. It explicitly addresses calving, rut, winter/forage, post-rut aggregation, and sea-ice corridors.

---

## 1. Context and Legal Framework

### 1.1 Species at Risk Act (SARA)

• **Critical Habitat Definition**: Under SARA s.2, critical habitat (CH) is the habitat *necessary* for the survival or recovery of a listed species; it must be identified in a recovery strategy “to the extent possible.”  
• **Current Gap**: The 2022 Recovery Strategy listed only sea-ice crossing corridors, leaving terrestrial CH to future study – a notable deficiency given that Peary Caribou spend > 95 % of their annual cycle on land.

### 1.2 Policy/Guidance That Shapes CH Delineation

1. **ECCC 2015 Destruction of CH Policy** – requires explicit biophysical attributes and measurable thresholds (e.g., snow density, vegetation class, disturbance buffers).  
2. **Guidelines on Incorporating Indigenous Knowledge** (2019, Crown-Indigenous Relations) – IK is *best available information*, not anecdotal.
3. **Regulatory Precedent**: *Alexander Archipelago Wolf* SSA (USFWS 2023) – first ESA listing to embed TEK spatial layers as primary data; accepted semistructured interviews, trapper maps, IK covariates.

### 1.3 Why This Matters for Peary Caribou

• The species’ “threatened” status hinges on demographic isolation among islands, small meta-population size (~13,200 mature animals in 2015) and climate-driven habitat loss.  
• Failure to identify terrestrial CH exposes federal decisions (permits, SEAs, impact assessments) to legal challenge (cf. Sage-grouse 2013 court case).

---

## 2. Ecology and Population Structure of Peary Caribou

| Management Unit | Core Islands / Range | 2021 Estimated Mature Animals* | Key Connectivity Corridors |
|-----------------|----------------------|--------------------------------|----------------------------|
| Banks–NW Victoria (BNV) | Banks, NW Victoria | 5,000–6,000 | Banks ↔ mainland (historically), Banks ↔ Melville |
| Western QEI (WQEI) | Melville, Bathurst, Byam-Martin | 3,000 | Bathurst ↔ E QEI, sea-ice routes southward |
| Eastern QEI (EQEI) | Devon, Ellesmere, Axel Heiberg | 2,500 | Devon ↔ Ellesmere (Jones Sound) |
| Prince of Wales–Somerset–Boothia (PSB) | Pwales, Somerset, Boothia | 2,000 | E Bellot Strait ice, PSB ↔ mainland |

*Numbers from 2015 aerial surveys updated with 2021 IK-informed imputation (Johnson et al. 2017 methodology).

Key life-history events:  
• **Calving**: late May–early June; selection for low-snow, high-forb tundra, gentle topography.  
• **Rut/Post-rut Aggregations**: October; concentrated on productive foraging plateaus.  
• **Winter Forage**: November–April; dependent on wind-scoured ridges, low snow density (< 350 kg m⁻³).  
• **Sea-ice Crossings**: December–April (north–south), May–June (south–north) historically.

---

## 3. Data Streams Available for CH Delineation

1. **Telemetry**: < 200 GPS collars (2000-2024), biased to Banks & Melville.  
2. **Aerial Survey Points**: ~18,000 observations (1961-2022); 40 % missingness pre-1990.  
3. **Indigenous Knowledge (IK/IQ)**:  
   • 110 semi-structured interviews (Inuvialuit, Qikiqtani Inuit, Kitikmeot) 2005-2024.  
   • 350 mapped place-names / travel routes, 275 event records (die-offs, calving areas).  
4. **Remote Sensing**:  
   • **SNOWPACK-OSSA v2** (4-km grid, 1980-2023): snow density, crust hardness, CT350.  
   • **Canadian Ice Service (CIS) Charts**: 1983-2024 weekly SIC, ice age.  
   • Sentinel-1/RCM SAR: 10-m snowmelt & roughness (near-real-time).  
5. **Climate Projections**: CanRCM4 & CMIP6 SSP2-4.5/SSP5-8.5 downscaled to 4 km.
6. **Genetics**: > 3,200 tissue samples (microsatellites, ddRAD-seq) delineating four clusters.

---

## 4. Analytical Innovations and Best Practice

### 4.1 Habitat-Selection / Species Distribution Models (SDM)

• **MaxEnt + IK**: Mentored approach (IK covariate rasters + priors) increased spring AUC to 0.70 on Banks–Melville.  
• **Resource Selection Functions (RSFs)**: Mixed-effects logistic models with random intercepts for individual/year mitigate pseudo-replication in telemetry.  
• **Bayesian Bernoulli-logistic meta-modelling** (Banks & QEI 2000-2013): Identified precipitation, wind > 6 m s⁻¹, rockland fraction as key drivers.

### 4.2 Bayesian IK-Prior Framework (Gryba et al. 2025)

• Elicited priors (beta distributions) for “relative preference” of IK features (currents, exclusion zones).  
• Implemented as prior surface or offset in INLA-based RSF.  
• Demonstrated > 30 % shift in spatial predictions when western science data were sparse.

### 4.3 Connectivity & Centrality

• **Circuitscape** on sea-ice cost surfaces: Bathurst complex emerges as keystone for gene flow.  
• Climate-adjusted models predict loss of WQEI–PSB corridors by 2060 without multi-modal pathways (ice bridging, assisted migration).  
• **Graph-theoretic thresholds**: maintaining current-flow centrality ≥ 0.15 needed for genetic viability per PVA.

### 4.4 Snow Metrics Integration

Adding **snow density < 350 kg m⁻³** raster and CT350 variable boosts prediction accuracy; matches hunter reports of forage accessibility. 

---

## 5. Step-wise Protocol for Identifying Critical Habitat

### STEP 0 – Scoping & Regulatory Alignment

• Declare purpose: SARA CH identification for four management units, for all seasons.  
• Confirm that IK will be treated as co-equal evidence; secure data-sharing agreements.  
• Establish spatial resolution (4 km base grid; 30 m for site-level features).

### STEP 1 – Collate and Clean Datasets

1. Telemetry: filter to ≥ 4 hr fix interval; thin to one location/day to minimise autocorrelation.  
2. Aerial surveys: geolocate sightings; assign seasonal class.  
3. IK data: translate place-names to polygons; code event records by life-stage.  
4. Remote-sensing layers: create seasonal composites (snow, NDVI, SAR roughness).  
5. Climate hindcast: derive anomalies relative to 1981-2010 baseline.

### STEP 2 – Define Biophysical Attributes & Candidate Covariates

| Life Stage | Biophysical Attribute | Data Layer(s) | Justification |
|-----------|----------------------|---------------|---------------|
| Calving | Snow density < 350 kg m⁻³; forb/dwarf-shrub tundra; slopes < 5° | SNOWPACK CT350; CAVM vegetation; DEM | Cow energy balance & predation risk |
| Rut/Post-rut | High biomass plateaus; proximity to mineral licks | NDVI peak; IK lick sites | Reproductive condition |
| Winter | Wind-scoured ridges; ice crust hardness < 100 kPa | SNOWPACK; SAR backscatter | Forage accessibility |
| Sea-ice Corridors | > 90 % probability of ice ≥ 10 cm | CIS charts; RIOPS forecasts | Safe crossing threshold |

### STEP 3 – Model Occurrence & Selection

1. **Hierarchical RSF** in INLA: Presence (telemetry + survey) vs. availability (random points).  
2. Include IK-derived rasters (e.g., hunter-identified “no-go” currents).  
3. Spatial random field (SPDE) to account for unmeasured spatial autocorrelation.

### STEP 4 – Validate & Calibrate Thresholds

• 10-fold spatial block cross-validation (Roberts et al. 2017).  
• Use **PPV ≥ 0.8** & **sensitivity ≥ 0.9** for threshold choice.  
• Bootstrapped AUC intervals target ≥ 0.7 for each season & subpopulation.

### STEP 5 – Integrate Connectivity

• Convert seasonal habitat suitability into conductance surfaces.  
• Run Circuitscape for each SSP scenario (2-4.5, 5-8.5) mid-century (2041-2060).  
• Identify nodes with current-flow centrality ≥ 0.15 → add to CH.

### STEP 6 – Map Critical Habitat Polygons

1. Union seasonal layers; dissolve holes < 1 km² (implementation practicality).  
2. Buffer by 1 km around high-use calving polygons (disturbance avoidance).  
3. Clip sea-ice corridors to 90 % isopleth of historic crossing probability.

### STEP 7 – Uncertainty & Adaptive Management

• Provide per-pixel posterior standard deviation map.  
• Flag high-uncertainty zones for “Schedule of Studies” (< 7 yrs completion).  
• Commit to 5-yr CH review aligned with COSEWIC status update.

---

## 6. Climate-Change Scenario Analysis

• **Sea-ice**: CMIP6 SSP5-8.5 yields 50 % reduction in late-winter SIC and adds 30–40 days of open water by 2050; Banks–mainland corridor already functionally lost (40 % drop in young-ice since 2000).  
• **Snow Regime**: +15–25 cm mean SWE, increased rain-on-snow events create crusts > 100 kPa – likely reduces winter forage in PSB by ~12 %.  
• **Vegetation Shift**: Greening (NDVI ↑ 3-7 % dec⁻¹) may expand shrub tundra in EQEI, improving summer forage but complicating predator dynamics.

Implication: CH polygons must be **forward-looking**; otherwise they will be obsolete within two SARA reporting cycles.

---

## 7. Dealing with Data Gaps – Schedule of Studies Blueprint

1. **UAV LiDAR transects** (100-m swath) for fine-scale snow hardness calibration.  
2. **eDNA from snow & meltwater** to validate calving areas devoid of telemetry.  
3. **Low-cost VHF ear-tags** deployed via dart rifle in PSB (reduces capture logistics).  
4. **Citizen Science App** co-developed with Inuit communities for opportunistic sightings (photo-timestamp-GPS).  
5. **IK Permanent Working Group** (twice-annual): ensures co-production & immediate data integration.

Timeline: complete by **2029** (7 years from 2022 Strategy) – aligns with regulatory requirement.

---

## 8. Additional, Non-Obvious Solutions & Considerations

• **Mobile Sea-Ice Platforms**: Explore temporary artificial ice bridges (high-salt slush pumped & flash-frozen) to maintain WQEI ↔ Bathurst connectivity during key migration windows (experimental; flagged speculative).  
• **Assisted Gene Flow**: Cryogenic semen repositories and translocations between PSB & WQEI to offset corridor loss (already used in woodland caribou recovery).  
• **Radar-Based Automatic Alert System** on Arctic shipping routes to trigger slow-downs when caribou detected near ice edges (leverages dual-use defense radars).  
• **SAR-AI Snow Hardness Mapping**: Deploy machine-learning models on continuous Sentinel-1/RCM for near-real-time forage accessibility forecasting for managers and harvesters.

---

## 9. Deliverables & Documentation Package

1. **GIS Layers** (GeoPackage): CH polygons by season, 30-m raster of habitat suitability, connectivity centrality map.  
2. **Metadata & Methods Report**: Full INLA script, priors, IK covariate derivation protocol.  
3. **Uncertainty Appendix**: Posterior SD maps, model diagnostics.  
4. **Schedule of Studies Plan** (Gantt chart).  
5. **Plain-Language IK Summary** for community review before publication.

---

## 10. Conclusion

A rigorous, co-produced approach can close the terrestrial critical-habitat gap for Peary Caribou within the next SARA reporting cycle. Integrating Indigenous Knowledge as spatial priors, embracing emerging remote-sensing tools, and embedding forward-looking climate scenarios are essential to ensure that critical habitat retains its functional value through mid-century. The protocol above meets the dual test of *best available science* and *regulatory defensibility*, positioning managers to safeguard a culturally and ecologically irreplaceable Arctic ungulate.

---

*Prepared by: AI Research Analyst – Arctic Conservation Unit*


## Sources

- https://www.federalregister.gov/documents/2021/08/31/2021-18098/endangered-and-threatened-wildlife-and-plants-threatened-status-with-section-4d-rule-for-the-dolphin
- https://www.sciencedirect.com/science/article/pii/S1476945X19300935#!
- https://www.northerncaribou.ca/threats/climate-change/
- https://cdnsciencepub.com/doi/10.1139/er-2017-0032
- https://www.researchgate.net/publication/279956915_A_multi-attribute_approach_to_mapping_Boreal_Woodland_caribou_habitat_in_Labrador_Oral_presentation
- https://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.2976
- https://polarresearch.net/index.php/polar/article/download/7964/14835?inline=1
- https://publications.gc.ca/collections/collection_2017/eccc/CW66-560-2017-eng.pdf
- https://search.proquest.com/openview/086643eef01574209ac812749407d22f/1?pq-origsite=gscholar&cbl=2026366&diss=y
- https://www.canada.ca/en/environment-climate-change/services/species-risk-education-centre/caribou.html
- https://www.sciencedirect.com/science/article/pii/S1574954119303243
- https://www.researchgate.net/profile/Isabelle-Schmelzer/publication/279956915_A_multi-attribute_approach_to_mapping_Boreal_Woodland_caribou_habitat_in_Labrador_Oral_presentation/links/559fc44208ae0e0bf613d409/A-multi-attribute-approach-to-mapping-Boreal-Woodland-caribou-habitat-in-Labrador-Oral-presentation.pdf
- https://www.researchgate.net/publication/366238094_Indigenous-led_conservation_in_the_Arctic_supports_global_conservation_practices
- https://wildlife.onlinelibrary.wiley.com/doi/10.1002/jwmg.22563
- https://www.researchgate.net/figure/Predictions-of-habitat-suitability-for-Peary-caribou-and-muskoxen-across-the_fig5_343853067
- https://www.canada.ca/en/environment-climate-change/services/species-risk-public-registry/recovery-strategies/peary-caribou-2022.html
- https://publications.gc.ca/site/eng/9.838094/publication.html
- https://www.researchgate.net/publication/390416353_A_Bayesian_approach_to_include_Indigenous_Knowledge_in_habitat_selection_functions
- https://www.thearcticinstitute.org/leveraging-indigenous-knowledge-effective-nature-based-solutions-arctic/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6392347/
- https://esajournals.onlinelibrary.wiley.com/doi/pdf/10.1002/ecs2.2976