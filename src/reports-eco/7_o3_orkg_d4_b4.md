# Determining Realistic Pesticide Concentration Ranges for Bee‐Impact Experiments

*All concentration units below are expressed as mass of active ingredient (a.i.). 1 µg kg⁻¹ = 1 ppb, 1 mg L⁻¹ ≈ 1 ppm, 1 ng bee⁻¹ ≈ 10⁻³ µg bee⁻¹.  Field rates are given as g a.i. ha⁻¹ where relevant.*

---

## 1  Objective and Scope
Experimental work on pesticide effects in bees must span a **“realistic range”** that (i) brackets the highest *measured* environmental residues in the relevant exposure matrix, (ii) exceeds the principal *effect thresholds* (LD₅₀, NOAEC/NOAEL, or well‐characterised sub-lethal bands) by at least one order of magnitude on the high side for positive controls, and (iii) provides ≤1/10 of field residues as a low-end “no-effect” anchor.  The learnings collated above supply the empirical residue distributions and toxicity benchmarks needed for a rational selection of test doses.

Because you have not yet finalised (i) the pesticide(s), (ii) exposure scenario (acute vs. chronic) or (iii) life stage, I outline ranges for each major insecticide and fungicide class across syrup, pollen‐paste, topical and field application routes, then map them onto acute and chronic designs.  Where class‐specific data are sparse I note uncertainties explicitly.

---

## 2  Empirical Residue Benchmarks
### 2.1  Systemic Insecticides (Neonics, Sulfoximines, Butenolides)
| Crop / Application | Nectar (ppb) | Pollen (ppb) | Reference |
|-------------------|--------------|--------------|-----------|
| Seed‐dressed sunflower / maize | ~10 | 2–3 | Bonmatin 2003/2005 |
| Oilseed rape (Elado®) | 1.3 | 1.7 | Germany 2014 |
| Squash soil drench / drip (imidacloprid or thiamethoxam) | 10±3 | 14±8 | 3× independent trials |
| Cover-crop pollen 2 y after beet treatment (clothianidin) | 0.07–1.7 | 0.07–1.7 | Simon‐Delso 2021 |

`Field extreme (95th percentile) ≈ 15 ppb nectar / 40 ppb pollen.`  **These numbers set the upper “realistic” bound for chronic dietary exposure** unless deliberate over-dosing is required.

### 2.2  Contact Spray Deposition
A surface‐area normalisation gives ≈1.05 cm² apparent spray deposition per honey-bee.  High-end orchard airblast delivers ≈1.2 µg a.i. bee⁻¹ (acetamiprid formulation), while typical row-crop boom sprays yield ≤0.1 µg bee⁻¹.  Conversion to ng bee⁻¹ is direct.

### 2.3  In‐Hive Matrices (Larval Diet & Wax)
– Pollen hazard monitoring: 0.1 to >75 000 PHQ units, translating to **0.1 ppb up to 7 500 ppb** active ingredient depending on LD₅₀.
– Wax: French survey detects neonics at **1–10 ng g⁻¹**; boscalid and deltamethrin dominate at 10–100 ng g⁻¹.

### 2.4  Fungicides & Acaricides as Co‐Stressors
– Propiconazole on blueberry blossoms peaked at **2084 ± 851 ppb**.
– Chlorothalonil “hive residue” = **34 mg L⁻¹ syrup (34 000 ppb)**.
– Fluvalinate typical strip volatilisation residues: **3 mg L⁻¹ larvae diet**.

These high mg L⁻¹ values justify using **10–100 ppm** tiers when exploring synergism with insecticides.

---

## 3  Effect Thresholds

| Compound / End-point | Acute LD₅₀ (µg bee⁻¹ unless noted) | Chronic NOAEC (ppb in diet) | Notable Sub-Lethal Band |
|---------------------|----------------------------------------|----------------------------|--------------------------|
| Imidacloprid (Apis) | 0.081 oral, 0.024 contact | 0.1 ppb onset mortality (Hal 2005) | Homing loss @ 1/10 LD₅₀ (~2 ng head⁻¹) |
| Clothianidin (Apis) | 0.004–0.017 oral | Colony NOAEC 25 µg kg⁻¹ syrup | Survival ↓ with low sugar @ 1/25 LD₅₀ |
| Sulfoxaflor | 0.146 (Apis) • 0.011 (Osmia) | <100 ppb kills 100 % Osmia in 2–6 d | Weak synergy with fluxapyroxad 7.5–60 mg L⁻¹ |
| Flupyradifurone | 1.2–2.3 (formulated) | ~4 µg bee⁻¹ induced oxidative stress | Strong synergy with propiconazole (field rate) |
| Etofenprox (pyrethroid) | 130 ng head⁻¹ (homing @ 32.5 ng) | — | Behavioural losses at ¼ LD₅₀ |
| Propiconazole (contact LD₅₀) | 24.7 µg bee⁻¹ | — | 17 % shorter worker life @ 2 ppm blossom residue |
| Flumethrin (larvae) | — | ≥0.1 mg L⁻¹ = enzyme spike | Immune & detox gene ↓ at ≥1 mg L⁻¹ |

Rule of thumb for designing a **chronic dietary series**: pick (i) 0.05×, 0.2×, 1×, 5× and 20× the *field 95th percentile* residue, and verify that 20× still remains ≤1/2 LD₅₀ accumulated over the exposure window.

---

## 4  Recommended Test Ranges by Scenario

### 4.1  Chronic Syrup or Pollen Diet (10–30 d)
Using 95th‐percentile residues and sub-lethal trigger bands, the table below gives **five-point geometric series** suitable for adult worker or larval assays.  Numbers in bold designate levels solidly “realistic”; italic levels are *exaggerated-but‐plausible* for margin-of-exposure work.

| Class | Starting Matrix Residue (ppb) | Suggested Series (ppb) |
|-------|------------------------------|------------------------|
| Neonic (imidacloprid) | 15 (Nectar) / 40 (Pollen) | **2**, **6**, **20**, *60*, *200* |
| Neonic (clothianidin) | 2 (N) / 40 (P) | **0.2**, **1**, **5**, *25*, *125* |
| Sulfoxaflor | 10 (N/P blended) | **1**, **3**, **10**, *30*, *100* |
| Flupyradifurone | 5 | **0.5**, **1.5**, **5**, *15*, *50* |
| Pyrethroid (etofenprox) | <1 (diet) | **0.1**, **1**, **10**, *50*, *100* |
| Fungicide (propiconazole) | 2000 (blossom) | **20**, **200**, **2000**, *6000*, *20 000* |
| Fungicide (chlorothalonil) | 34 000 (hive syrup) | **340**, **3400**, **34 000**, *100 000*, *340 000* |

Note: For larval‐toxic fungicide × insecticide synergy work use **34 mg L⁻¹ chlorothalonil + 3 mg L⁻¹ fluvalinate** as the “synergy positive control” and 10-fold diluted mixture (3.4 + 0.3 mg L⁻¹) as an “antagonism control.”

### 4.2  Acute Topical (LD₅₀ Confirmation or Behavioural)

| Compound | ng bee⁻¹ range |
|----------|---------------|
| Imidacloprid | 0.25, 0.5, 1, 2, 4 (brackets LD₅₀ 0.024 µg = 24 ng) |
| Clothianidin | 0.05, 0.1, 0.2, 0.4, 0.8 (LD₅₀ 4–17 ng) |
| Sulfoxaflor | 5, 10, 20, 40, 80 (LD₅₀ ≈146 ng) |
| Etofenprox | 8, 16, 32, 64, 128 (¼ LD₅₀ homing deficit at 32 ng) |

Behaviours (homing, EEG, PER) should use **≤¼ LD₅₀** as the top concentration to avoid confounding lethality.

### 4.3  Semi-Field Cage / Tunnel Sprays
Convert intended deposit‐per‐bee to field application rates.

Example: **0.5 µg bee⁻¹ target** × (80 000 bees ha⁻¹ flying density) / 1.05 cm² deposition = **≈38 g a.i. ha⁻¹**.  Compare with label: Actara (thiamethoxam) orchard max 100 g ha⁻¹, so 0.5 µg bee⁻¹ sits mid-range.

Use **0.05, 0.2, 1, 5, 20 g ha⁻¹** for boom‐spray simulation and **5, 20, 50, 100 g ha⁻¹** for airblast orchards.

---

## 5  Matrix & Life-Stage Adjustments
1. **Larvae** ingest ~5 mg diet across 5–6 d.  To match 40 ppb pollen, feed = 0.2 ng cumulative.  Upscale chosen treatment levels to this ingestion mass.
2. **Nurse bees** consume ≈10× more pollen than foragers; use pollen matrix at the upper edge of field distribution.
3. **Queens** contact wax diffusively; use ng g⁻¹ wax levels (1–10) in chronic dermal assays.
4. **Stingless bees / Osmia** show 5–10× lower LD₅₀; multiply selected ng bee⁻¹ doses by 0.1 when testing those taxa.

---

## 6  Combination & Contextual Stress Testing
• Nutritional stress: run parallel cages on 33 % vs 50 % sucrose; **1/25 LD₅₀ clothianidin** halved survival only under low sugar.

• Fungicide synergy: include **propiconazole 2 ppm** or **fluxapyroxad 7.5 mg L⁻¹** with systemic insecticides; watch for oxidative stress and caspase activation endpoints.

• Adjuvants: dose N-methyl-2-pyrrolidone at 0.01–1 % v/v (0.1–10 g L⁻¹) to bracket larval toxicity seen in formulation screens.

---

## 7  Analytical Verification
– UHPLC–MS/MS with QuEChERS cleanup routinely achieves **LOD 0.1 ppb, LOQ 1 ppb** in nectar/pollen; for royal jelly or wax apply ultrasound‐assisted salting-out LLE for **0.25 ppb LOQ**.
– Sample 3–5 replicates per treatment/timepoint; confirm that delivered dietary ppm/ppb stay within ±20 % of nominal.

---

## 8  Proposed Experimental Templates
### 8.1  Chronic Dietary (Apis mellifera Workers)
• 30 × 4-frame colonies, 6‐treatment + control; feed 1 L syrup/day @ 0, 2, 6, 20, 60, 200 ppb imidacloprid for 21 d.
• Endpoints: adult survival, syrup intake, hypopharyngeal gland size, gene expression (CYP6AS, CYP305D), hive weight.

### 8.2  Larval Synergism Assay
• In vitro rearing plates; treatments: (i) chlorothalonil 34 mg L⁻¹, (ii) fluvalinate 3 mg L⁻¹, (iii) binary mix, (iv) 10× diluted, (v) ternary + coumaphos 8 mg L⁻¹.
• 48‐h and 120-h mortality plus oxidative enzyme panel.

### 8.3  Tunnel Spray + Nutrition Interaction
• Cucurbita plots, drip imidacloprid (soil) to reach 15 ppb nectar; overlay foliar sulfoxaflor at 20 g ha⁻¹ (bee deposit ≈0.25 µg).
• Two diet stations per hive: 33 % vs 50 % sucrose.
• Track flight counts (RFID) and colony thermoregulation.

---

## 9  Uncertainties & Caveats (Flagged Speculation)
1. **Long-term soil reservoirs**: systemic uptake into late-season cover crops suggests chronic field residues could exceed current 95th percentile in regions with high historic neonics use.
2. **Adjuvant toxicity** is largely unquantified; real‐world co-formulants may push effective doses 2–3× higher toxicity.
3. **Non-Apis taxa** can be an order of magnitude more sensitive; extrapolations here may under‐protect solitary bees.

---

## 10  Summary Guidance
1. **Anchor chronic syrup/pollen testing at 2–60 ppb for neonics**, 1–30 ppb for sulfoxaflor, 0.5–15 ppb for flupyradifurone; extend two higher tiers (×3 each) for margin‐of‐exposure purposes.
2. **Acute topical or spray designs should centre on ¼ LD₅₀ and 1 LD₅₀** for behavioural and lethal endpoints respectively, with one sub-LD₅₀ and one supra-LD₅₀ tier on either side.
3. **Synergy screens** require mg L⁻¹ fungicide/flo‐mixture levels that match in‐hive residues: chlorothalonil 34 mg L⁻¹, fluvalinate 3 mg L⁻¹, propiconazole 2 ppm.
4. Always verify delivered doses analytically; field residue heterogeneity is high, and formulation surfactants can substantially change toxicity ranking.
5. Integrate **nutritional quality and season/caste** to capture real-world modulating factors highlighted in recent synergy studies.

By adopting the graduated ranges above, your experiment will cover—without drifting into implausible extremes—the landscape of exposures bees actually face, while retaining toxicological resolution to detect both lethal and nuanced sub-lethal effects, including multi‐chemical and nutrition × pesticide interactions that current regulatory protocols overlook.

## Sources

- https://doaj.org/toc/1932-6203
- https://boris.unibe.ch/142075/
- https://doaj.org/article/8e86916f207842dab61f51a1442ff111
- https://doaj.org/article/3b7b6f5876b24e33abc8eba397a34a28
- https://figshare.com/articles/_Pesticide_residues_detected_in_treatment_combs_n_8202_8202_13_used_to_rear_worker_bees_in_experiments_/466572
- http://192.168.22.105/handle/311030/26868
- http://dx.doi.org/10.1038/s41467-019-08523-4
- https://hdl.handle.net/11386/4825696
- http://old.scielo.br/scielo.php?script=sci_arttext&pid=S1413-70542018000100051
- https://figshare.com/articles/_Four_Common_Pesticides_Their_Mixtures_and_a_Formulation_Solvent_in_the_Hive_Environment_Have_High_Oral_Toxicity_to_Honey_Bee_Larvae_/896626
- http://hdl.handle.net/11585/767477
- http://europepmc.org/backend/ptpmcrender.fcgi?accid%3DPMC2862711%26blobtype%3Dpdf
- https://doaj.org/article/e38a05e4e2a148a1a593938dbc47a19d
- https://hal.archives-ouvertes.fr/hal-01302262
- http://hdl.handle.net/11585/27617
- https://escholarship.org/uc/item/6ms9n181
- http://hdl.handle.net/10018/53945
- https://doi.org/10.1016/j.foodchem.2018.06.004
- https://doaj.org/article/dbb77e2d1788492e861a06d0fb6637b0
- http://nbn-resolving.de/urn/resolver.pl?urn:nbn:de:hebis:30:3-429197
- https://www.sciencedirect.com/science/article/pii/S0048969722039547
- https://zenodo.org/record/1124233
- https://figshare.com/articles/Using_a_Hazard_Quotient_to_Evaluate_Pesticide_Residues_Detected_in_Pollen_Trapped_from_Honey_Bees_Apis_mellifera_in_Connecticut_/823812
- https://digitalcommons.unl.edu/dissertations/AAI27838398
- https://figshare.com/articles/_Assessment_of_Chronic_Sublethal_Effects_of_Imidacloprid_on_Honey_Bee_Colony_Health_/1341195
- http://edepot.wur.nl/312196
- https://avesis.erciyes.edu.tr/publication/details/7dca8ede-2bd9-4891-b28e-216e991b1430/oai
- https://avesis.erciyes.edu.tr/publication/details/caad8e54-7221-478c-98bf-537554a4bf76/oai
- https://doi.org/10.3389/fpubh.2017.00361
- https://doaj.org/article/5632ae1714b44523954a1cda38149b10
- https://doaj.org/article/4308e7bbd99140edad567d4c82e8efb9
- http://www.ajol.info/index.php/ijbcs/article/download/118895/108373/
- https://setpublisher.com/index.php/jbas/article/view/2229
- http://hdl.handle.net/2263/76234
- http://ir.nhri.org.tw/handle/3990099045/12951
- http://hdl.handle.net/10261/286035
- http://nbn-resolving.de/urn/resolver.pl?urn:nbn:de:hebis:30:3-428387
- https://figshare.com/articles/_Synergistic_interactions_for_two_pairs_of_pesticide_mixtures_/896620
- http://hdl.handle.net/10068/372592
- www.elsevier.com/inca/publications/store/4/0/5/8/5/3
- https://doaj.org/toc/2167-8359
- https://bibliotekanauki.pl/articles/65746
- https://digitalcommons.unl.edu/entomologyfacpub/814
- http://hdl.handle.net/2078.1/250956
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/06/8a/pone.0077550.PMC3797043.pdf
- https://researchdata.reading.ac.uk/376/
- http://www.loc.gov/mods/v3
- https://ojs.openagrar.de/index.php/JKA/article/view/1934
- https://escholarship.org/uc/item/88d0p9j7
- https://figshare.com/articles/_MRM_chromatograms_/1017715
- https://doi.org/10.1007/s10646-015-1537-2
- http://hdl.handle.net/11588/337909
- https://doaj.org/article/a8c56c9e220245648018568a72564e86
- https://figshare.com/articles/_Toxicity_of_pesticides_to_Apis_mellifera_in_the_presence_and_absence_of_P450_inducers_/357031
- http://www.bulletinofinsectology.org/pdfarticles/vol66-2013-001-009matsumoto.pdf
- http://hdl.handle.net/Toxicodynamics
- https://figshare.com/articles/_Larval_survival_during_the_6_d_development_stage_reared_on_artificial_diet_contaminated_with_four_pesticides_at_the_selected_concentrations_and_a_1_solvent_control_/896619
- http://hdl.handle.net/10255/dryad.208089
- https://hal.archives-ouvertes.fr/hal-02082454
- http://hdl.handle.net/11585/616782
- https://escholarship.org/uc/item/88p3z7ht
- http://hdl.handle.net/10255/dryad.218560
- http://www.cdpr.ca.gov/docs/emon/pubs/fatememo/Imidclprdfate2.pdf
- https://hal.archives-ouvertes.fr/hal-02382527
- http://real.mtak.hu/60034/1/crc.40.2012.2.14.pdf
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/2a/07/pone.0068191.PMC3699529.pdf
- http://www.aphis.usda.gov/foia/foia_requests/2010/Plant
- https://www.teses.usp.br/teses/disponiveis/75/75135/tde-20112020-112848/
- http://periodicos.uefs.br/index.php/sociobiology/article/view/792
- http://hdl.handle.net/11577/2524913
- http://hdl.handle.net/2066/218320
- https://doaj.org/article/abf68c2ebcbc4541a60f9452e0463be7
- http://hdl.handle.net/2142/22907
- https://doaj.org/article/d0cd0420a38642e9b20169d5135bb1fb
- http://aspace.agrif.bg.ac.rs/handle/123456789/4419
- http://www.bulletinofinsectology.org/pdfarticles/vol56-2003-041-050schoning.pdf
- http://hdl.handle.net/2142/113204
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/5a/13/pone.0066375.PMC3680470.pdf
- https://figshare.com/articles/_Method_limits_of_detection_and_limits_of_quantification_for_the_80_compounds_analyzed_for_beehive_matrices_from_western_France_honey_bee_colonies_/722983
- http://yadda.icm.edu.pl/yadda/element/bwmeta1.element.agro-60f1a5bf-6999-490a-b510-ca36f671ecba/c/JPPR_53_4__11_El-Naggar.pdf
- http://hdl.handle.net/ESM
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/a7/6a/pone.0113728.PMC4239102.pdf
- https://figshare.com/articles/Movement_of_Soil_Applied_Imidacloprid_and_Thiamethoxam_into_Nectar_and_Pollen_of_Squash_Cucurbita_pepo_/123409
- https://push-zb.helmholtz-muenchen.de/frontdoor.php?source_opus=2746
- https://cigrjournal.org/index.php/Ejounral/article/view/6277
- https://doi.org/10.1051/apido:2004071
- https://hal.inrae.fr/hal-02608327
- https://www.apidologie.org/10.1051/apido:19970610/pdf
- https://doaj.org/article/1f9e85fe854748e5aa69097e4288e11f
- https://www.apidologie.org/10.1051/apido:2005032/pdf
- https://figshare.com/articles/_Comparison_of_estimated_times_to_LD50_T50_range_in_days_for_dietary_exposure_of_honey_bees_to_two_neonicotinoid_insecticides_using_standard_and_cumulative_risk_approaches_/993458
- https://research.wur.nl/en/publications/assessing-the-combined-toxicity-effects-of-three-neonicotinoid-pe
- https://hal.science/hal-00282377/document
- https://openprairie.sdstate.edu/plant_faculty_pubs/155
- https://doaj.org/article/f79f6a3fc0db448b976f6763feb80b83
- https://opus.hs-offenburg.de/frontdoor/index/index/docId/3553
- http://hdl.handle.net/10.3389/fphys.2022.1054769.s003
- https://repository.uwyo.edu/ugrd/2015_UGRD/Schedule/94
- https://doaj.org/article/24b977780ebd46e885663c1a780012e7
- http://hdl.handle.net/11585/571464
- https://doaj.org/article/953ea64c86f045a8a0a0b86642423299
- http://hdl.handle.net/10255/dryad.218562
- https://escholarship.org/uc/item/0670x0mx
- https://setpublisher.com/index.php/jbas/article/view/1603
- https://doaj.org/article/4a05a63e483544c2ba3def496b6c6954
- https://doaj.org/article/602c551bd82f4c3688be604c54c58d69
- https://figshare.com/articles/_Antagonistic_interactions_for_two_pairs_of_pesticide_mixtures_/896622
- https://figshare.com/articles/_Imidacloprid_and_clothianidin_residue_ppb_in_sugar_syrup_stock_solutions_50_from_one_sample_in_each_replicate_experiment_and_from_stored_syrup_in_wax_pots_3_colonies_mixed_from_replicate_1_1_sample_and_replicate_2_2_samples_experiment_residue_was_determi/965138
- http://hdl.handle.net/2142/84475
- http://digitalservices.scranton.edu/cdm/ref/collection/p15111coll1/id/1228
- https://doaj.org/article/03d2c2a44cc94ef8b44c516f8554bec7
- https://hal.science/hal-00087695/document
- https://figshare.com/articles/A_Pragmatic_Approach_to_Assess_the_Exposure_of_the_Honey_Bee_Apis_mellifera_When_Subjected_to_Pesticide_Spray/1247984
- https://doaj.org/article/d9478af14c8342b08c08a053859cf369
- http://prodinra.inra.fr/record/198573
- https://hal.inrae.fr/hal-03291190
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/8e/57/pone.0039114.PMC3384620.pdf
- http://prodinra.inra.fr/record/342022
- https://escholarship.org/uc/item/3r4852q5
- https://doi.org/10.1093/jee/toz231
- http://hdl.handle.net/10150/276577
- http://hdl.handle.net/11336/82571
- https://zenodo.org/record/3736549
- http://www.rcaap.pt/detail.jsp?id=oai:agregador.ibict.br.RI_UFLA:oai:localhost:1/9397
- https://doaj.org/article/b6aef479c7d940a996eaa8583b8ca9a2
- https://doaj.org/article/1b821087ad6a4b59a9bd8fbd90b0ad13
- https://ddd.uab.cat/record/255381
- https://figshare.com/articles/Quantitative_weight_of_evidence_assessment_of_higher_tier_studies_on_the_toxicity_and_risks_of_neonicotinoids_in_honeybees_3_Clothianidin/5607544
- https://doaj.org/article/96766123713e48fbba07cbf25266741a
- https://digitalcommons.unl.edu/wffdocs/93
- https://docs.lib.purdue.edu/dissertations/AAI1585379
- https://dx.doi.org/10.3390/agronomy3040794
- https://digitalcommons.unl.edu/dissertations/AAI10102754
- http://sro.sussex.ac.uk/id/eprint/57887/1/David2015_Article_SensitiveDeterminationOfMixtur.pdf
- https://doaj.org/article/f8c93011a42e4db19640fc160f9b7883
- https://academic.oup.com/jee/article/105/6/1890/790101?login=true
- https://doaj.org/toc/2299-4831
- https://opus.bibliothek.uni-wuerzburg.de/files/17585/Hesselbach_Scientific_Reports.pdf
- https://hal.inrae.fr/hal-02623692
- https://research.vu.nl/en/publications/36ca7f05-be7c-4ae0-8fbd-d4d9e4a6e943
- http://www.cdpr.ca.gov/docs/emon/pubs/ehapreps/report_gw09a.pdf
- https://figshare.com/articles/Trace_level_determination_of_pyrethroid_neonicotinoid_and_carboxamide_pesticides_in_beeswax_using_dispersive_solid_phase_extraction_followed_by_ultra_high_performance_liquid_chromatography_tandem_mass_spectrometry/1328452
- https://doi.org/10.3390/ijerph17072421.