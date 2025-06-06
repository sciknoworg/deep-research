# Identifying Critical Habitat for Peary Caribou (Rangifer tarandus pearyi)

## 1  Purpose and Scope
This report lays out a comprehensive, stepwise framework for identifying, delineating, and legally describing *critical habitat* for Peary caribou under Canada’s Species at Risk Act (SARA), while remaining compatible with other decision-support contexts (general ecological assessment, territorial land‐use planning, park establishment, environmental impact assessment, etc.).  It synthesises **all** pertinent findings from recent research on Peary caribou and, where directly transferable, on other Rangifer designatable units (DUs) and Arctic ungulates.

Although the user has not yet specified (i) the governing regulatory framework, (ii) existing datasets, or (iii) preferred analytical tools, the workflow below is written so it can be modularly linked to any of those choices.  Where speculative or forward-looking elements are introduced they are explicitly flagged ⚠️.

---
## 2  Regulatory and Conceptual Foundations

### 2.1  Legal definitions of “critical habitat”
• Under SARA a location is *critical habitat* if **both** (1) it is necessary for survival or recovery, and (2) its key biophysical attributes can be described with enough precision that destruction can be prohibited (§2(1), §58).

• The 2012 Draft National Recovery Strategy for Boreal Woodland Caribou introduced a **hierarchical range concept**—entire range ➔ seasonal ranges ➔ high-use areas & calving sites—managed by disturbance caps rather than blanket bans.  This hierarchy is now the de-facto template adopted across several DUs and will almost certainly be applied to Peary caribou.

• COSEWIC’s 2014 reassessment split Canadian caribou into 11 DUs; Peary caribou remains a distinct DU.  Listing status under SARA is *Endangered* (2004); no final federal Recovery Strategy exists yet, meaning a **Schedule of Studies** may be required to fill data gaps.

### 2.2  Ecological specificities of Peary Caribou
• Island dwelling with strong fidelity to certain wintering, rutting, and calving areas; historically used **sea-ice corridors** to move among Banks, Melville, Victoria and Bathurst complexes.

• Key limiting factors differ from continental woodland caribou: industrial disturbance is minor; **snow conditions and sea ice persistence dominate** habitat selection and connectivity.

• Low, cyclic abundances (e.g., 25 845 in 1961; ~7 000 in 1973) mean that **Allee effects** and survey-design sensitivity become crucial.

---
## 3  Data Requirements and Existing Assets

### 3.1  Animal-location data
1. Historic systematic aerial surveys (1961–2013) – nine surveys covering Bathurst & satellites.  
2. GPS telemetry: 1994–97, 2003–06, plus newer collars where available (⚠️ speculation: Nunavut 2019–2024 collars).  
3. Indigenous Knowledge (IK): >1 272 documented sea-ice crossings (1977–1980) and 1983–2019 land-occupancy interviews.

Sampling-interval biases must be corrected (Fortymile herd study: 1-h vs 167-h fixes changed speed estimates by 35 %)—see Section 5.2.

### 3.2  Environmental covariates
• Topography: CDEM (30 m), ArcticDEM (2 m), UAS-derived 3-D microtopography (RMSE 20–35 mm).  
• Snow metrics:  
  – Daily 30 m MODSAT-NDSI snow cover (2000–present, 90 % OA).  
  – SnowModel 90 m depth for Alaska transferable to Bathurst ⚠️.  
  – Fusion products: UAS photogrammetry + GPR + LiDAR (0.5 m grids; RMSE ≈ 6 cm) suitable for local high-value areas.  
• Sea-ice persistence: RADARSAT concentration anomalies (1983–2019); forecast RCP8.5 (+20–77 % resistance by 2086).  
• Vegetation: 30 m ARCTICBorealVNIR land-cover; high-resolution UAV orthomosaics for cryptogam–rush–grass tundra mapping.

### 3.3  Disturbance layers
Although industrial linear features are sparse, **airstrips, research camps, diesel caches, and emergent mining interests** must be digitised because avoidance can occur at scales <200 m (woodland caribou 3rd-order avoidance of seismic lines).

### 3.4  Protected-area, tenure, and Indigenous stewardship layers
• Current/proposed Qausuittuq National Park boundaries (Bathurst).  
• Inuit Owned Lands (IOL) parcels.  
• Existing Important Bird Areas (IBA) & Key Terrestrial Marine Habitat Sites (KTMH) for potential synergies.

---
## 4  Conceptual Framework for Critical-Habitat Delineation
1. **Range identification**: island complexes + adjacent sea-ice mobility zones.  
2. **Ecological functional areas**: winter range, rut/summer range, calving grounds, staging areas, and inter-island corridors.  
3. **Biophysical attributes**: snow depth ≤50 cm, snow density ≤0.30 g cm⁻³, Ram hardness ≤85 (unless shallow slab); vegetated low elevations; line-of-sight land across straits.  
4. **Quantitative thresholds**: following Woodland template, set % allowable *change* in snow and ice metrics, not absolute closures (e.g., ≤10 % of winter range may exceed density threshold in any given year).

---
## 5  Analytical Toolbox

### 5.1  Resource- and Step-Selection Functions (RSF / SSF)
• Multi-scale RSFs: avoid scale-specific misspecification (woodland example: cut-blocks avoided at 1st–2nd order, linear features at 3rd).  
• Integrated SSF/HMMs: jointly infer behavioural state (“encamped” vs “exploratory”) and selection, capturing diel cycles (zebra proof-of-concept).  This is critical because Peary caribou show **punctuated migration** analogues.

### 5.2  Bias-corrected estimation
• Local Gibbs MCMC SSF removes steady-state bias; 
• Sampling-regime correction (Fortymile study) ensures movement metrics and derived resistance surfaces are valid.

### 5.3  Agent-Based & Individual-Based Models (ABM/IBM)
The Québec woodland SSF-driven IBM achieved full k-fold and emergent-pattern validation and reproduced functional responses to land-cover change.  **Transferability**: parameterise with Peary caribou SSF coefficients to simulate space use under projected sea-ice loss or snow-depth anomalies.

### 5.4  Connectivity and Corridor Modelling
• Landscape-resistance layers combine SSF-derived cost coefficients with **sea-ice persistence** and **snow hardness**.  
• Circuitscape or Omniscape can then locate pinch-points; results feed into **Marxan** or **prioritizr** reserve scenarios.

### 5.5  Decision-Support Optimisation
• Large-area, data-poor MARXAN success in the Russian Arctic (47 PCAs covering 25 % of EEZ) confirms scalability.  
• Cost surface weights: roads (highest), seismic lines, old burns (lowest) from Little Smoky ABM provide transferable starting values.

### 5.6  Survey-Design Optimisation
Bathurst Island simulation: **moderate/low** aerial coverage (≥50 % detection, CV ≈18 %) outperformed intensive coverage at low densities—field-test this before committing to expensive full-coverage surveys.

---
## 6  Applying the Framework to Peary Caribou: A Stepwise Protocol

### Step 1  Compile & Harmonise Datasets
1. Standardise telemetry to ≤2-h fix intervals; apply movement-rate correction factors.  
2. Derive annual rasters: snow depth, density, hardness (UAS + GPR for calibration; MODSAT & SnowModel for time-series).  
3. Generate sea-ice cost surfaces (RADARSAT anomalies scaled 0–1).  
4. Digitise **all** anthropogenic footprints (satellite, field validation, IK).  
5. Produce 30 m base layers on a common polar stereographic grid.

### Step 2  Model Habitat Selection
1. Fit multi-scale RSF (island-wide 1st order; seasonal 2nd; step-based 3rd) with snow & ice covariates.  
2. Fit Integrated HMM-SSF capturing behavioural states; validate with Viterbi concordance.  
3. Cross-validate k = 5 spatial folds.

### Step 3  Build Dynamic Resistance Surface
• Convert SSF β coefficients to pixel-wise costs = exp(–βx).  
• Add anisotropic cost for sea-ice drift direction using winter wind climatology (75 % of ice-wedge polygons elongate parallel to wind).  
• Apply **temporal stacking**: annual rasters 1980–current and 2050/2080 RCP8.5 projections.

### Step 4  Identify Corridors and Core Patches
• Run Circuitscape for each decade; derive current density maps.  
• Threshold top 20 % cumulative density = *corridor network*; overlay with high-RSF cores (>75th percentile).  
• Label each core as Winter, Rut/Summer, Calving, Staging via date‐filtered telemetry.

### Step 5  Optimise Reserve Design
• Objective: include ≥90 % of core-corridor pixels, maximise connectivity, minimise overlap with high-cost anthropogenic features.  
• Scenario A: No-growth industrial baseline; Scenario B: Mining‐expansion; Scenario C: Climate 2080.  
• Use Marxan with boundary-length modifier; run 10 000 iterations, 100 solutions; select **lowest‐cost 95th percentile solution**.

### Step 6  Ground-Truth & IK Validation
• Return maps to community hunters; verify corridor realism vs observed crossings.  
• Spot-survey snow metrics via stake lines & UAS to test model predictions.

### Step 7  Legal Description and SARA Compliance
• Translate Marxan output into metes-and-bounds polygons; attach tabular biophysical attributes (snow ≤0.3 g cm⁻³, etc.).  
• Where data gaps exist (e.g., calving sites on Prince of Wales Island), insert a **Schedule of Studies** (<5 yr) referencing UAV snow-depth campaigns and light-coverage aerial surveys.

---
## 7  Key Findings and Recommendations
1. Persistent critical habitat already evident: Cameron Island (winter), NE Bathurst (rut/summer), Banks & Melville low-density-snow tundra.  These areas should be immediately designated *core* in any Recovery Strategy.

2. Sea-ice persistence is now the dominant corridor predictor; protective zoning must include **sea-ice mobility buffers** that extend beyond island shorelines.

3. Sub-decimetre UAV snow mapping is operationally feasible (0.06–0.09 m RMSE) at <$2 k per system; deploy annually on high-value winter ranges.

4. Moderate/low transect aerial surveys are *more* accurate at low densities—re-allocate saved flight hours to expand spatial extent or increase revisit frequency.

5. Movement bias corrections (sampling interval, non-local destination kernels) are mandatory before deriving RSF/SSF coefficients; failure to do so could mis-place legal boundaries by >30 km.

6. Integrated SSF–IBMs provide the only tested way to forecast functional responses to *unobserved* snow-ice futures; incorporate them into climate-robust habitat planning.

7. A disturbance-cap approach (x % of winter range may exceed snow-density threshold) is legally defendable and adapts to inter-annual climatic volatility better than static polygons.

---
## 8  Outstanding Gaps and Future Work
• ⚠️ No public telemetry for 2010–2024 cohorts—initiate collaring focused on juveniles to capture potential Allee effects.

• Limited empirical snow-hardness data north of 78°N—deploy 5 GPR transects per key island.

• Sea-ice forecast uncertainty post-2050 warrants ensemble modelling (CMIP6 SSP2-4.5 & SSP5-8.5).

• Genetic connectivity monitoring: leverage historic mtDNA work to design eDNA sampling in inter-island leads.

• Socio-economic layer (emerging mining tenures) not yet integrated into cost surfaces; obtain Nunavut Planning Commission datasets.

---
## 9  Conclusion
A rigorous, data-rich, legally defensible critical-habitat delineation for Peary caribou is attainable **now** by combining modern movement-modelling advances (multi-scale RSF/SSF, HMM, IBM), high-resolution snow & sea-ice remote sensing, Marxan optimisation, and Indigenous Knowledge validation.  The proposed stepwise protocol meets SARA requirements, anticipates future climate and industrial scenarios, and is scalable from single islands to the full Canadian Arctic Archipelago.


## Sources

- https://doaj.org/toc/1932-6203
- https://researchonline.ljmu.ac.uk/id/eprint/16349/1/Conservation%20Biology%20-%202022%20-%20Cavedon%20-%20Selection%20of%20both%20habitat%20and%20genes%20in%20specialized%20and%20endangered%20caribou.pdf
- https://zenodo.org/record/5010132
- http://hdl.handle.net/10255/dryad.124412
- https://journalhosting.ucalgary.ca/index.php/arctic/article/view/66473
- https://elib.dlr.de/142914/
- https://lup.lub.lu.se/record/058bc057-5918-419c-82ee-5cbc3a83485c
- http://septentrio.uit.no/index.php/rangifer/article/download/327/321/
- https://digitalcommons.usu.edu/wild_facpub/2769
- https://zenodo.org/record/4066637
- http://eprints.gla.ac.uk/view/author/48979.html
- http://arctic.journalhosting.ucalgary.ca/arctic/index.php/arctic/article/download/4186/4163/
- www.speciesatrisk.gc.ca/recovery/default_e.cfm
- https://doaj.org/toc/1890-6729
- http://hdl.handle.net/1807/71114
- http://pubs.aina.ucalgary.ca/arctic/arctic19-2-145.pdf
- http://www.ub.uit.no/baser/septentrio/index.php/rangifer/article/download/3647/3611/
- http://hdl.handle.net/20.500.11794/13682
- https://figshare.com/articles/Model_selection_amongst_the_candidate_models_of_step_selection_by_woodland_caribou_in_the_C_te_Nord_region_Qu_bec_Canada_in_winter_/1088843
- https://doaj.org/article/c08f48688a954696958e105a08d90706
- http://hdl.handle.net/11250/2471096
- http://pubs.aina.ucalgary.ca/arctic/arctic30-2-101.pdf
- http://hdl.handle.net/10388/etd-09202010-225013
- http://www.ub.uit.no/baser/septentrio/index.php/rangifer/article/download/1703/1591/
- https://figshare.com/articles/_Simulation_domain_and_winter_ranges_of_the_Central_Arctic_and_Porcupine_caribou_herds_Alaska_and_Yukon_/1092920
- http://arctic.synergiesprairies.ca/arctic/index.php/arctic/article/viewFile/1573/1552/
- http://septentrio.uit.no/index.php/rangifer/article/download/1197/1137/
- https://doaj.org/article/d0afc4ec0abe41b2a4b813e292029200
- http://hdl.handle.net/20.500.11794/66381
- https://scholarworks.umt.edu/wildbio_pubs/39
- http://hdl.handle.net/10255/dryad.193480
- http://www.ub.uit.no/baser/septentrio/index.php/rangifer/article/download/1276/1215/
- http://septentrio.uit.no/index.php/rangifer/article/download/1643/1541/
- https://doaj.org/article/17a87238603b42a58d97788a3ae74674
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/49/04/pone.0048697.PMC3489831.pdf
- https://research-repository.st-andrews.ac.uk/bitstream/10023/21123/1/Michelot_2019_Biometrics_MCMC_AAM.pdf
- https://mdpi.com/books/pdfview/book/4020
- http://hdl.handle.net/10388/7573
- https://research-portal.st-andrews.ac.uk/en/researchoutput/flexible-hidden-markov-models-for-behaviourdependent-habitat-selection(4dd76e34-031f-48f4-a498-c0276389766e).html
- http://hdl.handle.net/10255/dryad.142470
- http://pubs.aina.ucalgary.ca/arctic/Arctic39-1-24.pdf
- http://hdl.handle.net/10255/dryad.78835
- http://hdl.handle.net/11143/18415
- http://hdl.handle.net/10.5061/dryad.n726pq6/1
- https://zenodo.org/record/4962140
- http://eprints.usq.edu.au/29175/
- https://polarresearch.net/index.php/polar/article/view/7964
- http://hdl.handle.net/2429/62178
- https://doaj.org/article/442e53b4db324a42a8ebf77c128d0c10
- https://openrepository.ru/article?id=167665
- https://figshare.com/articles/Caribou_movement_and_habitat_selection_data/6062345
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1878029612000643/MAIN/application/pdf/36c9ebadf09a39c6680a80eba5278549/main.pdf
- https://hal.science/hal-03234752
- http://hdl.handle.net/20.500.11794/13707
- http://septentrio.uit.no/index.php/rangifer/article/download/1010/965/
- https://figshare.com/articles/Home_Range/4151790
- http://hdl.handle.net/2429/17789
- http://hdl.handle.net/20.500.11794/66475
- http://hdl.handle.net/10255/dryad.56738
- https://figshare.com/articles/Spatial_scales_of_habitat_selection_decisions_implication_for_telemetry-based_movement_modelling/5002343
- https://septentrio.uit.no/index.php/rangifer/article/view/318
- https://doi.org/10.1016/j.ecolmodel.2012.06.004
- http://septentrio.uit.no/index.php/rangifer/article/viewFile/254/241/
- https://septentrio.uit.no/index.php/rangifer/article/view/1710
- http://repository.lapan.go.id//index.php?p=show_detail&id=3828
- https://researchrepository.murdoch.edu.au/view/author/Renton,
- http://hdl.handle.net/11250/222194
- https://zenodo.org/record/5539766
- https://doaj.org/toc/2194-9034
- http://collections.lib.uwm.edu/cdm/ref/collection/polar/id/528
- https://arcabc.ca/islandora/object/sc:3335/datastream/PDF/download
- https://figshare.com/articles/_Opportunity_cost_of_the_reserve_system_relative_to_the_caribou_protection_target_/349934
- https://hdl.handle.net/11250/2755646
- http://hdl.handle.net/1807/100329
- http://www.nusl.cz/ntk/nusl-477016
- https://doaj.org/article/5b47097f65f8459ca8f2e8936da1ae23
- http://digital.lib.uidaho.edu/cdm/ref/collection/etd/id/1814
- https://doaj.org/article/b5445b2b34a345baa55d3256c23a291d
- http://www.ub.uit.no/baser/septentrio/index.php/rangifer/article/viewFile/1250/1189/
- https://escholarship.org/uc/item/7mj9q82f
- https://arc.lib.montana.edu/ojs/index.php/IJS/article/view/934
- http://www.fs.fed.us/pnw/pubs/journals/pnw_2006_mcnay001.pdf
- http://digital.lib.uidaho.edu/cdm/ref/collection/etd/id/821
- http://pubs.aina.ucalgary.ca/arctic/Arctic37-1-7.pdf
- https://figshare.com/articles/Uniting_Statistical_and_Individual_Based_Approaches_for_Animal_Movement_Modelling/1088849
- http://hdl.handle.net/10255/dryad.66929
- https://eprints.whiterose.ac.uk/121030/7/ecy.2452.pdf
- https://zenodo.org/record/2706019
- https://journalhosting.ucalgary.ca/index.php/arctic/article/view/64573
- https://zenodo.org/record/7525951
- https://septentrio.uit.no/index.php/rangifer/article/view/1712
- http://hdl.handle.net/2429/68633
- https://scholarworks.umt.edu/biosci_pubs/293
- https://doaj.org/article/e1e26ec509dd4805805219c16f8b9686
- http://hdl.handle.net/10255/dryad.46482