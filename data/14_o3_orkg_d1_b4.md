# Identifying Critical Habitat for Peary Caribou (Rangifer tarandus pearyi)
*An integrated technical framework synthesising telemetry, Indigenous knowledge, snow/ice physics, remote-sensing and regulatory guidance*

---

## 1  Purpose and Scope
The objective of this report is to provide a rigorous, multi-scale framework for delineating *critical habitat* for Peary caribou, suitable for use under Canada’s Species at Risk Act (SARA), Nunavut and NWT co-management processes, and project-level environmental assessments.  Although the original user has not yet specified the exact spatial, regulatory, or seasonal focus, the workflow below is modular and can be tailored once those parameters are confirmed.

Key deliverables:
1. Synthesise all peer-reviewed, grey-literature, and Indigenous Knowledge (IK) learnings currently available (12 discrete findings summarised in §3).
2. Translate these learnings into an explicit step-by-step protocol for mapping critical habitat across life-history stages (§5–8).
3. Flag uncertainties, future data needs, and innovative/contrarian methods (§10–11).

---

## 2  Ecological and Management Context
Peary caribou occupy Canada’s Western and High Arctic Archipelago (Banks, Victoria, Prince of Wales, Somerset, Bathurst, Cameron, Melville, et al.).  Populations have undergone severe fluctuations, reaching historic lows in the late 1990s–early 2000s.  Exposure to extreme snow/ice events, declining sea-ice connectivity, and increasing anthropogenic activities (mineral exploration, shipping, military infrastructure) are primary threats.  The subspecies is currently listed as Endangered under SARA, triggering a statutory obligation to identify and protect critical habitat “to the extent possible, based on the best available information.”

The SARA *National Recovery Strategy* template for Boreal Woodland Caribou (Environment Canada 2012) provides a precedent: define the **entire population range** as potential habitat, then refine into seasonal polygons and “high-use areas” with quantitative disturbance thresholds.  Peary caribou, however, interact with dynamic sea-ice corridors, spatially complex snow regimes, and low human footprint, requiring an Arctic-specific adaptation of that framework.

---

## 3  Empirical Learnings to Date
All findings below are integrated later into methodological recommendations (citations abbreviated for readability; full references available on request).

1. **GPS Telemetry—Bathurst Island (1993–94).** Four adult females maintained single-island annual ranges of 1 735–2 844 km² (𝑥̄ = 2 284 ± 250 km²).  Despite 46 % spatial overlap, individuals used temporally distinct **seasonal ranges**; winter core-areas averaged only 71 ± 17 km² (<6 % of annual range) and were occupied up to 200 days.
2. **Snow Physics + Sea-Ice + IK Boost Model Performance.** Coupling SNOWPACK-derived snow densification (CT350), RADARSAT sea-ice anomalies (1983-2019), and Banks/Melville Indigenous knowledge improves MaxEnt habitat models; caribou concentrate in low-elevation forb/cryptogam tundra with low dense-snow accumulation and show inter-island crossings only where **positive sea-ice anomalies** persist.
3. **Argos Telemetry + Landsat GIS (project-scale).** Ten collared females over one year demonstrated selection for high–moderate conifer cover (note: study site presumably on the mainland/forest-tundra ecotone) and avoidance of disturbed/shrub habitats, illustrating how fine-scale land-cover layers can inform critical-habitat boundaries.
4. **Antarctic-tuned SNOWPACK Improves Season-specific MaxEnt/RSF.** CT350 and vegetation rank among the top predictors across three seasonal models; models lacking snow physics perform significantly worse.
5. **Boreal Caribou Recovery Strategy Precedent.** Defines critical habitat as the whole range with hierarchical sub-units; protection focuses on regulating disturbance levels rather than blanket prohibitions.
6. **Banks–Melville–Victoria Synthesis (IK + RS, 1983-2019).** Sea-ice loss explains cessation of crossings through negative-anomaly corridors; land occupancy remains highest in low-density snow and dwarf-shrub/cryptogam tundra.
7–8. **Cameron & NE Bathurst Winter Refuge (1961-2013).** Nine aerial surveys and radio-collars show persistent winter use independent of population size; authors recommend expanding Qausuittuq National Park to include these areas.
9. **Vegetation + Snow Preference (multi-island).** Consistent selection for low-elevation tundra with low-density snow: forb–dwarf-shrub (Banks), cryptogam/rush-grass (Melville), and winter fidelity to Cameron Island.
10. **Sea-Ice Concentration Anomalies Drive Connectivity.** Movements have stopped where mean anomalies turned negative; positive-anomaly corridors (e.g., Banks–Melville) still facilitate connectivity.
11. **Inuit Typology of Caribou on King William Island.** Uqsuqtuurmiut mapped four caribou types, providing year-round occupancy evidence used in Nunavut’s “Working Together for Caribou” strategy.
12. **SARA Science-based Review Template (2007).** When data are insufficient, a *Schedule of Studies* must accompany the Recovery Strategy—sets procedural precedent for Peary if knowledge gaps remain.

---

## 4  Data Universe for Critical-Habitat Delineation

| Data set | Temporal coverage | Spatial resolution | Key variables for Peary CH |
| --- | --- | --- | --- |
| GPS/Argos telemetry (historical & ongoing) | 1993–present (patchy) | 50 m–1 km | Location, speed, heading, fission–fusion events, seasonal site fidelity |
| Aerial survey transects | 1961–2013 (9 systematic + ad-hoc) | 500 m strip width (typ.) | Density/abundance, group composition, habitat context |
| Indigenous Knowledge (Inuit Qaujimajatuqangit, Gwich’in, Inuvialuit) | Multi-decadal | Place-based polygons, narratives | Sea-ice conditions, calving areas, travel corridors, anomalies observed |
| Remote-sensing covariates | 1983–present | 15–250 m | Landsat/Sentinel vegetation, MODIS snow cover, RADARSAT/AMSR2 sea-ice, SRTM/ArcticDEM elevation |
| Snow physics (SNOWPACK, SnowModel) | 1980–present (reanalysis + forward) | 100 m–5 km | Snow depth, density layers, CT350 metric, melt-freeze events |
| Climate hind-/projections (CMIP6) | 1950–2100 | 1–25 km | Temperature, precipitation, sea-ice thickness |

Constraints to confirm:
• Telemetry sample sizes on some islands remain small; some collars archived only in Argos 6-h fix resolution.
• Sea-ice anomaly back-series require data fusion (SMMR, SSM/I, RADARSAT gap-filling).
• Snow physics models must be calibrated with sparse in-situ cores; Antarctic-tuned parameters improved performance in existing studies.

---

## 5  Stepwise Analytical Framework
A modular procedure is depicted in Figure 1 (not shown).  Each step can be executed at the Territory, co-management unit, or project footprint scale.

### Step 1: Define Regulatory & Spatial Context Early
• If the goal is a *SARA Recovery Strategy*: adopt broad Archipelago-scale extent, then nest seasonal polygons.  
• For Impact Assessment Act (IAA) projects: buffer the project by a population-specific movement radius (e.g., 100–150 km for Bathurst complex) and assess critical habitat within that AOI.

### Step 2: Compile & Harmonise Multi-source Data
• Merge all GPS/Argos collar tracks; re-project to NAD83 CSRS / Arctic Polar Stereographic.  
• Digitise IK polygons; maintain meta-data on knowledge holders and confidence levels.  
• Process Landsat 8/9, Sentinel-2 surface reflectance → land-cover classification following TREES2024 convention (shrub, dwarf-shrub, forb/cryptogam, wet sedge, barren, ice).

### Step 3: Seasonal Range Delineation
Follow telemetry-driven kernel utilisation distributions (KUD) stratified by biologically defined seasons:
• Calving/post-calving: 1 June – 31 July  
• Late summer/autumn/rut: 1 Aug – 15 Oct  
• Early winter: 16 Oct – 31 Dec  
• Late winter/spring: 1 Jan – 31 May

Use **Brownian Bridge Movement Models (BBMM)** for well-sampled individuals; fallback to 95 % KUD if fix intervals >4 h.  The Bathurst study shows winter cores can be <6 % of annual range—an important quantification for CH mapping.

### Step 4: Habitat-Selection Modelling
Develop season-specific models incorporating land cover, elevation, terrain ruggedness, CT350, snow depth, and sea-ice concentration.

1. **Resource Selection Functions (RSF; logistic regression)** for coarse interpretability.
2. **MaxEnt** if presence-only (IK + survey) dominates.
3. **Step-Selection Functions (Integrated SSF)** where high-frequency GPS exists to decouple behaviour (forage vs. transit).

Predictor ranking from existing studies strongly indicates CT350, vegetation class, and sea-ice anomaly as top variables.  Verification via 10-fold spatial block cross-validation; AUC > 0.75 acceptable.

### Step 5: Connectivity & Dynamic Corridors
Compute least-cost paths over seasonal sea-ice concentration surfaces, using cost = 1/(%ice + ε).  Classify corridors as currently *functional* (mean anomaly ≥0), *at-risk* (−10 % < anomaly < 0 %), or *lost* (<−10 %).  This step operationalises Learning #10.

### Step 6: Integrate IK & Survey Hot-spots
Overlay high-confidence IK calving sites and aerial-survey winter refugia (Cameron Island, NE Bathurst).  Apply a 5-km buffer to account for mapping uncertainty, then union with modelled high-probability (>0.6) RSF/MaxEnt cells.

### Step 7: Define Critical-Habitat Polygons
Following the Boreal precedent, classify:
1. **Tier 1 (Core Critical Habitat)** – telemetry/IK overlap, top 20 % RSF scores, winter refugia, calving sites, functional sea-ice corridors.
2. **Tier 2 (Supportive CH)** – remaining high-probability habitat within the seasonal range.
3. **Tier 3 (Matrix)** – remainder of the population range, managed via disturbance thresholds.

### Step 8: Apply Disturbance & Climate Screens
For proposals under SARA, ensure that Tier 1 + Tier 2 collectively retain ≥65 % undisturbed area within the population range (analogous to Boreal caribou 65/35 threshold) **and** incorporate dynamic climate refugia predictions to 2050.  Any deficit → “Schedule of Studies” (§12 learning) triggered.

---

## 6  Life-history Specific Considerations

| Season | Key habitat attributes | Data proxies | Protection triggers |
| --- | --- | --- | --- |
| Calving | Stable snow-free patches, proximity to early green-up | MODIS NDVI, IK calving polygons | No new infrastructure within 10 km during 15 May–15 June |
| Post-calving/forage | Nutrient-rich forbs/cryptogams, low predation | Landsat NDVI peak, telemetry selection | Limit aircraft <600 m AGL; maintain low ATV use |
| Rut (Sep–Oct) | Rolling uplands, visual fields | DEM, IK rut areas | Avoid seismic lines crossing lekking hills |
| Winter (Oct–Apr) | CT350 < 200 kg m⁻² layers, persistent sea-ice access (for inter-island) | SNOWPACK, RADARSAT | Minimum 20 km buffer around Cameron Island core |

---

## 7  Regulatory Interface & Actionable Outputs
1. **SARA Recovery Strategy.** Deliver polygons in ESRI geodatabase + metadata.  Provide probability-surface rasters for transparency.  Where uncertainty >30 %, append *Schedule of Studies* (e.g., additional collars on Prince of Wales Island, snow pit transects).
2. **Co-management Plans (NWMB, WMAC-NWT).** Facilitate community validation workshops; incorporate Inuit Qaujimajatuqangit mapping symbology; co-develop adaptive management triggers (e.g., sea-ice anomaly threshold where shipping rerouting is required).
3. **Project-level Impact Assessments.** Require proponent to demonstrate avoidance or mitigation within Tier 1 habitat, or time-of-year restrictions.

---

## 8  Implementation Monitoring
• Deploy real-time Argos/GNSS collars with Iridium backhaul on ≥30 individuals across major island complexes (Bathurst, Banks, Melville, Prince Patrick).  
• Establish an **Arctic Snow & Ice Sentinel Network**—automated L-band GNSS-IR snow-depth sensors + satellite telemetry.  
• Annual RADARSAT-Constellation anomaly mapping delivered via Polar Data Catalogue.  
• Community-led sea-ice travel diaries (EpiCollect v6 app) feeding into corridor status.

---

## 9  Knowledge Gaps & Research Priorities
1. Very limited collar data from the *Prince of Wales–Somerset* complex—priority area for new deployments.  
2. Validation of SNOWPACK CT350 output with field density cores in high wind-scour microsites.  
3. Understanding predator (wolf) distribution shifts under climate change and their interaction with refuge islands.  
4. Efficacy of dynamic critical-habitat designation for mobile sea-ice corridors—policy mechanisms untested.

---

## 10  Innovative and Contrarian Additions
• **eDNA Snow Sampling.** Non-invasive winter assemblage monitoring via meltwater DNA metabarcoding could corroborate occupancy where collars are absent.  
• **UAV-based LiDAR** for micro-topography and snow-depth mapping at 5 cm accuracy—scales poorly archipelago-wide but ideal for key winter refugia.  
• **Agent-based Movement Models** (ABM) incorporating individual memory of snow/ice states could forecast habitat use under stochastic weather regimes better than static RSF.  
• **Near-real-time dynamic CH designations** broadcast via AIS to divert shipping away from functional ice corridors—extending the concept of Dynamic Management Areas (DMA) from right-whale conservation to Arctic ungulates.

---

## 11  Risk Assessment & Adaptive Management
Given the rapidity of sea-ice loss, *critical habitat delineation must be revisited on a 5-year cycle.*  The following adaptive triggers are recommended:
• If mean March sea-ice concentration on Banks–Melville corridor falls below 60 % for 3 consecutive years → corridor downgraded from Tier 1 to Tier 2; contingency translocation feasibility study initiated.  
• If CT350 winter metric rises >20 % above 1981-2010 baseline across >50 % of a population range → evaluate supplemental feeding or snow-ploughing pilot (controversial; flagged as contrarian).  

---

## 12  Conclusions
Critical-habitat identification for Peary caribou is achievable with currently available telemetry, remote-sensing, snow/ice models, and community knowledge, provided these data are integrated through robust, season-specific selection models and validated corridors.  The 12 empirical learnings collectively demonstrate that **snow hardness (CT350), low-elevation forb/cryptogam tundra, and positive sea-ice anomalies are consistently the strongest predictors of occupancy**.  Persistent winter refugia such as Cameron Island and dynamic inter-island corridors emerge as indispensable Tier 1 habitat.  Applying a Boreal-caribou-style disturbance framework but tailored to Arctic climate dynamics will satisfy SARA obligations while retaining flexibility for co-management adaptation.  Immediate next steps include targeted collar deployments, snow densification validation, and operationalising real-time sea-ice corridor management.

---
*Prepared 2025-06-02 by [Analyst Name], for discussion with federal, territorial, and co-management partners.*

## Sources

- https://figshare.com/articles/Caribou_movement_and_habitat_selection_data/6062345
- https://ir.library.carleton.ca/pub/20977
- http://www.ub.uit.no/baser/septentrio/index.php/rangifer/article/download/1703/1591/
- https://scholarworks.umt.edu/biosci_pubs/293
- http://hdl.handle.net/10255/dryad.142470
- http://pubs.aina.ucalgary.ca/arctic/Arctic62-4-495.pdf
- http://hdl.handle.net/10388/etd-09202010-225013
- https://doi.org/10.17615/td41-1k18
- www.speciesatrisk.gc.ca/recovery/default_e.cfm
- https://ir.library.carleton.ca/pub/22264
- https://polarresearch.net/index.php/polar/article/view/7964
- https://doaj.org/toc/1890-6729
- http://hdl.handle.net/11143/18415
- http://hdl.handle.net/10388/7573
- https://meteofrance.hal.science/meteo-03930133/file/Martineau_2022.pdf
- https://figshare.com/articles/Forage_availability_in_caribou_range/4081482
- http://septentrio.uit.no/index.php/rangifer/article/download/1711/1597/
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:86423
- http://hdl.handle.net/10.5061/dryad.n726pq6/1