# Identifying Critical Habitat for Peary Caribou – Integrated Technical Framework (v2025-06)

## 1. Problem Statement & Context
Peary caribou (Rangifer tarandus pearyi) are listed as Endangered under the Canadian Species at Risk Act (SARA) and as a distinct **Designatable Unit (DU)** by COSEWIC. “Critical habitat” in the legal sense is the *habitat that is necessary for the survival or recovery of a listed wildlife species* (SARA §2). Beyond the statutory definition, managers require spatially explicit, seasonally resolved maps that capture both *terrestrial forage patches* and *sea‐ice movement corridors* so that land-use decisions, shipping regulation, mineral exploration, and emergency response can be aligned with species-at-risk obligations.

This report synthesises the latest empirical and remote-sensing research—including the eleven key findings listed in the *Learnings* block—and proposes an end-to-end workflow that (a) satisfies SARA’s regulatory tests for *identifiability, delineation, and scientific defensibility* and (b) provides a flexible, data-rich platform for adaptive conservation planning.

## 2. Regulatory vs. Scientific Products – Why Both Matter
| Product | Primary Audience | Spatial Grain | Typical Evidence | Statutory Weight |
|---------|-----------------|---------------|------------------|------------------|
| **SARA Critical Habitat Description** | Federal Court, IRB, project proponents | Polygon/parcel scale | *Best available* science & TK | Legally binding |
| **Conservation Planning Model (HSM/RSF/MaxEnt)** | Wildlife managers, EIA consultants | Raster ≤ 250 m | Telemetry, RSF, snow/ice remote sensing | Advisory but strongly influential |

The two products are mutually reinforcing. A defensible critical-habitat polygon must be underpinned by repeatable, peer-reviewed modelling; conversely, a habitat-suitability map has greater uptake when its high-probability cells are explicitly recognised in a SARA recovery strategy.

## 3. Spatial & Temporal Scope
1. **Designatable Unit** – High Arctic Archipelago populations centred on *Banks, Melville, Bathurst, and smaller satellite islands*.
2. **Temporal Resolution** – Three biologically defined seasons suffice for legal designation yet retain ecological nuance:
   • *Winter* (Nov–Apr) – Energetically limiting; snow physics paramount.
   • *Spring/Fall* (May–Jun; Sep–Oct) – Transition; ice crossings; parturition.
   • *Summer* (Jul–Aug) – Forage maximisation; insect avoidance.
3. **Movement Corridors** – Inter-island sea-ice routes (Sverdrup Channel, McClintock Channel, Byam Martin Channel) require their own layer given their functional difference from terrestrial foraging patches.

## 4. Data Sources & Analytical Methods
| Layer | Resolution/Period | Source | Learnings Hook |
|-------|------------------|--------|----------------|
| Elevation, slope, hill-shade | 30 m static | CDEM, ArcticDEM | RSF simulation (#1) |
| Vegetation (NDVI, shrub class) | 10 m / 5-day | Sentinel-2, Planet NICFI | Snow-cost interaction (#12) |
| Snow depth, CT₃₅₀ | 50 m / daily | SNOWPACK Arctic build | Snow physics (#2) |
| Sea-ice concentration, roughness | 50 m (RCM CP), 3 km (AMSR2) | RCM ScanSAR, NOAA AMSR2 | Corridors on/off (#8–#10) |
| Telemetry (GPS-ACC) | 1–30 min fix | COLLAR-LTE/FlexTracker | Energetics (#11–#12) |
| Aerial transect observations | 0.5–1 km | Twin-Otter w/ gyro-stabilised camera | Sampling design (#1) |
| Inuit Qaujimajatuqangit (IQ) | Feature polygons | Nunavut Planning Commission | Corridor persistence (#10) |

## 5. Key Empirical Findings and Their Implications
1. **Transect Optimisation (Bathurst Island)** – Moderate or low-intensity systematic aerial grids deliver *75–96 %* classification accuracy with ~18 % CV at low densities, *doubling* efficiency compared with intensive coverage. **Implication**: Recovery‐funded surveys can legitimately halve flight hours without statistical penalty, freeing budget for telemetry collars.

2. **Snow Physics as Habitat Filter** – CT₃₅₀ (cumulative thickness of >350 kg m⁻³ layers) is the single best predictor of winter occurrence; low-elevation areas with CT₃₅₀ ≈ 0 are systematically selected. **Implication**: Snow models must be run operationally (daily) to flag emergent crust episodes that may render critical forage unusable.

3. **RCM Compact Polarimetry (CP) Superiority** – RCM’s CP ScanSAR discriminates thin vs. deformed ice better than RADARSAT-2 HH–HV, ensuring continuity for ice-class maps crucial to sea-ice corridor monitoring. **Implication**: The Recovery Strategy’s remote-sensing annex should be updated to mandate RCM CP as the default corridor layer.

4. **Long-Term Sea-Ice Anomalies as Corridor Switches** – 37 years of RADARSAT anomaly analysis shows *post-2000 cessation* of crossings where anomalies are negative. **Implication**: Critical habitat boundaries can be dynamic; SARA allows adaptive description if the spatial entity is *ecologically functional* at listing time.

5. **Telemetry‐Observed Range Fidelity** – Four adult females exhibited 1 735–2 844 km² annual ranges with wintering areas averaging 71 ± 17 km² (<6 % of annual range). **Implication**: Critical habitat polygons do not need to blanket entire islands; compact winter patches are legally sufficient.

6. **Energetic Cost Landscapes** – GPS-ACC collars link snow depth & sub-freezing extremes to higher ODBA (Overall Dynamic Body Acceleration), enabling *dynamic RSF layers* that reflect true energetic penalties. **Implication**: CH maps can be tiered (Tier 1 = low energetic cost / highest legal protection).

## 6. Integrated Workflow for Critical Habitat Delineation
```mermaid
graph LR
A[Collar Deployment & IQ Workshops] --> B(Snow & Ice Model Setup)
B --> C[RSF / MaxEnt Modelling]
C --> D[Threshold Selection & Tiering]
D --> E[Legal Polygon Drafting (SARA Annex)]
E --> F[Adaptive Monitoring: RCM + AMSR2 + Aerial]
F --> C
```

### 6.1 Data Acquisition & Pre-processing
• Deploy 20–30 GPS-ACC collars per designatable unit (DU) for ≥24 months to span seasonal variability. 4-h fix; 40 Hz ACC bursts every 15 min.
• Ingest RCM CP scenes bi-weekly (Arctic Daily Mosaics to 50 m)
• Run SNOWPACK v1.24 in “advection-enhanced” mode, forced by ERA5-Land + AMPS, 5 km grid, downscaled to 50 m with CDEM lapse‐rate.
• Harmonise all rasters to common 50 m Albers Equal Area grid.

### 6.2 Modelling Suite
1. **RSF for high-frequency telemetry** – Use GLMM with individual random intercepts; predictors: (snow depth, CT₃₅₀, NDVI, slope, hill-shade, distance-to-water, sea-ice roughness, corridor class). Weight proportional to fix frequency.
2. **MaxEnt for occurrence (aerial + IQ)** – Presence‐only; background sampling stratified by CT₃₅₀ quintile to avoid snow-layer bias.
3. **Model Fusion** – Ensemble logistic average weighted by AUC; require *concordant top-quantile* for Tier 1 CH.

### 6.3 Thresholding & Legal Translation
• Adopt *Youden J* ≥ 0.65 as statistical cut-point.
• Dilate resulting Tier 1 cells by mean winter‐range radius (4.75 km) to ensure functional connectivity.
• For corridors, impose 90 % probability of ice ≥15 cm thickness for ≥45 consecutive days (Telegraph‐Strait standard) based on RCM-derived roughness class.
• Output: Multi-polygon shapefile with attribute table: {Season, Tier, Evidence, Date, SnowModelVer, RSF_AUC}

## 7. Sampling Design Recommendations
• **Transect Intensity** – Low-intensity (2 × transect spacing = island width / 20) is statistically optimal (#1) when paired with resource-selection simulation weights.
• **Timing** – Late March (peak snow hardness) for winter habitat; Late July for summer NDVI calibration.
• **Sensor Synergy** – Recommend *dual-use* flights: optical RGB for vegetation and thermal (FLIR) for calf heat signatures.

## 8. Remote-Sensing Technology Roadmap (2025–2030)
1. **WideScanSAR (TerraSAR-X/TanDEM-X wSC)** – 200 km swath sets a benchmark; lobbying for similar mode in *RADARSAT-Next* would drastically improve archipelago coverage.
2. **CubeSAR Constellations (Iceye, Capella)** – 15 min revisit; possible to trigger *contingency corridor alerts* during anomalous freeze-up.
3. **Hyperspectral UAV LiDAR** – Pilot on Somerset Island to resolve micro-lichen patches (<20 cm) that ground‐truth MaxEnt predictions.
4. **eDNA Snow Cores** (flagged speculative) – Metabarcoding residual DNA in snow layers to pinpoint usage; early trials suggest correlation with collar density (r = 0.61, n = 12 transects).

## 9. Decision-Support Products for Managers
1. **Tiered Critical Habitat Atlas** – Interactive WebMap (GeoServer) with *time slider* for dynamic corridors.
2. **Energetic Risk Surface** – Monthly maps of predicted ODBA surplus (kJ day⁻¹) overlaid on CT₃₅₀; red flags areas where warming events produce crust spikes.
3. **Corridor Status Dashboard** – Auto-ingests RCM CP scenes; traffic-light indicator (Green = open, Yellow = narrowing window, Red = closed) for each island pair.
4. **SARA Compliance Audit Layer** – Integrates mining claims and shipping routes; auto-flags spatial conflicts.

## 10. Gaps, Risks & Mitigation
| Gap/Risk | Consequence | Mitigation |
|----------|-------------|------------|
| Telemetry sample bias (collar drop-off, single-sex) | Skewed RSF | Balanced age/sex ratio; rapid collar retrieval via VHF beacon |
| RCM data latency (4–6 h) | Corridor closure notifications delayed | Exploit CubeSAR surge capacity as stop-gap |
| SNOWPACK parameter uncertainty | CT₃₅₀ mis-estimation | Deploy 5 automatic snow pits (Nautilus design) for assimilation |
| Legal challenges to dynamic CH | Injunctions on industrial permits | Maintain versioned shapefiles; peer-reviewed methods appendix |

## 11. Policy & Regulatory Recommendations
1. **Adopt “Dynamic Critical Habitat Annex”** – Allow seasonal updating within a fixed legal envelope via Ministerial Order; precedent exists in SARA (North Atlantic Right Whale closure zones).
2. **Mandate RCM CP archiving under Open Data** – Same tier as RADARSAT-1 legacy to remove procurement bottlenecks for researchers.
3. **Establish Indigenous Guardian Programme** – Community operators equipped with handheld SAR viewers (Teledyne-carried) to validate corridor status; qualifies under *Guardians Initiative* funding stream.
4. **Provisional Threshold for CT₃₅₀** – Declare CT₃₅₀ > 12 cm as “functionally unsuitable” for Peary winter forage in Recovery Strategy; provides clear trigger for emergency planning.

## 12. Conclusions
All lines of evidence converge on a *patchy yet predictable* distribution of high-value Peary caribou habitat. Modern snow physics, high-frequency telemetry, and next-generation SAR now permit near-real-time mapping of forage patches and sea-ice corridors at 50 m grain. Implementing the workflow outlined here, managers can produce a legally defensible critical-habitat description while retaining flexibility for adaptive management—squarely in line with SARA’s precautionary but evidence-based mandate.

The remaining frontier lies in shortening the sensor-to-decision latency below 3 h and in integrating novel biological proxies (eDNA, microbiome aerosols) to complement classic telemetry. With the High Arctic now on the leading edge of climate disruption, time-sensitive, data-rich habitat delineation is no longer optional—it is the linchpin of Peary caribou recovery.


## Sources

- https://elib.dlr.de/85258/
- https://doaj.org/toc/1890-6729
- http://www.ub.uit.no/baser/septentrio/index.php/rangifer/article/viewFile/1685/1574/
- https://dx.doi.org/10.3390/rs8040285
- https://archimer.ifremer.fr/doc/00660/77187/
- https://zenodo.org/record/7712503
- https://elib.dlr.de/91122/
- http://hdl.handle.net/11250/222194
- http://www.for.gov.bc.ca/hfd/library/documents/bib106870.pdf
- https://zenodo.org/record/8186170
- https://doi.org/10.5194/tc-17-889-2023
- https://doaj.org/article/a2823572f31741b486e925d9f8cfd1b1
- http://hdl.handle.net/10.6084/m9.figshare.7284677.v1
- https://meteofrance.hal.science/meteo-03930133/file/Martineau_2022.pdf
- https://elib.dlr.de/82892/
- http://hdl.handle.net/20.500.11850/361026
- http://septentrio.uit.no/index.php/rangifer/article/download/585/555/
- http://hdl.handle.net/10255/dryad.57475
- https://doaj.org/article/cd3133b6530041ec9f9c6a65cf2d0351
- https://figshare.com/articles/Data_for_RSF_analysis_of_moose/4177422
- https://doaj.org/toc/1994-0424
- http://hdl.handle.net/10.6084/m9.figshare.6969422.v1
- https://septentrio.uit.no/index.php/rangifer/article/view/1710
- http://hdl.handle.net/11143/18415
- https://doaj.org/article/97f0fdc0776f4d8484ae0bfb6faa1b0b
- https://digitalcommons.usu.edu/wild_facpub/2772
- https://doaj.org/article/b3560dfd75fb48bf95a53adbc3f9bb68
- https://dx.doi.org/10.3390/ecrs-2-05136
- https://research.chalmers.se/en/publication/695
- https://polarresearch.net/index.php/polar/article/view/7964
- www.osi-saf.org,