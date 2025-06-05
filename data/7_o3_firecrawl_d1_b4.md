# Designing a “Field-Realistic” Pesticide-Exposure Range for Bee Toxicology Experiments

*Prepared for: Laboratory/Field Investigators planning a multifactorial study on pesticide impacts on bees*

---

## 1. Why the Term “Field-Realistic” Is Contentious – and How to Anchor It Quantitatively

1. The phrase is used inconsistently across the literature. Regulators (e.g., EFSA, US-EPA) typically derive “field-realistic” from *measured residue distributions* in exposure matrices (pollen, nectar, guttation, soil, water). Academic studies sometimes extrapolate from application rates (g AI ha⁻¹) or modelling outputs (PRZM, AgDRIFT) without ground-truthing.
2. **Best practice** is to define the range **empirically** from *recent monitoring datasets* covering: 
   - Treated crop matrices (pollen, nectar, honey-dew, guttation) 
   - Non-crop matrices (wildflower pollen/nectar, field margin flora, soil dust, surface water, puddles, irrigation reservoirs)
3. A *percentile-based* approach captures both central-tendency and worst-case exposures: e.g., 5th/50th/90th/99th ‑percentile residues. This avoids the common criticism that single-point “field-realistic” doses cherry-pick low values.
4. **Exposure duration** must be coupled with concentration. Chronic scenarios (≥10 d) can leverage time-weighted-average (TWA) residues; acute scenarios (<48 h) should bracket the realistic worst-case peak.

> **Key implication**: You will need *at least four dose levels* (control + low + mid + high) to capture realistic variability, plus one supra-field reference toxicant (positive control) to confirm bioassay sensitivity.

---

## 2. Core Residue Learnings from the Last Decade (2014-2024)

| Matrix | Active Ingredient (AI) | Typical Range (ng g⁻¹ or µg L⁻¹) | 90th/Max | Notes |
|--------|-----------------------|------------------------------------|----------|-------|
| Agricultural soil (4–6 years seed treatments) | Clothianidin | 3.5–13 ng g⁻¹ (plateau) | – | Chronic background; exposes ground-nesting bees & soil–root uptake |
| Agricultural soil | Thiamethoxam | 0.4–4 ng g⁻¹ | – | Rapid degradation but metabolises to clothianidin |
| Surface waters (ditches, puddles) | Mix of neonics | G-mean 0.63 µg L⁻¹ | 63 µg L⁻¹ (puddles) | Pulses after seed drilling & rain |
| Cotton pollen (seed-dressed) | Imidacloprid | 1.61–64.6 ng g⁻¹ | 64.6 ng g⁻¹ | 100 % detection |
| Cotton nectar (seed-dressed) | Imidacloprid | ≤1.77 ng g⁻¹ | 1.77 ng g⁻¹ | 88.9 % detection |
| Cotton pollen | Thiamethoxam | ≤14.5 ng g⁻¹ | 14.5 ng g⁻¹ | 90 % detection |
| Cotton nectar | Thiamethoxam | ≤4.29 ng g⁻¹ | 4.29 ng g⁻¹ | 60 % detection |
| Wild-margin flora pollen | Thiamethoxam | up to 86 ng g⁻¹ | – | Non-crop exposure pathway |

Couple these concentrations with dose metrics:

• Contact LD₅₀ (Apis mellifera) – imidacloprid: **0.081 µg bee⁻¹**; thiamethoxam: **0.024 µg bee⁻¹**.  EFSA HQ/RQ > 1 = “high risk” for many real-world residues.

• Chronic, sub-lethal imidacloprid **1–10 µg L⁻¹ syrup for 10 weeks** → strong colony-level effects: ↓ food intake, ↓ growth, −35–85 % workers/gynes, behavioral shifts (brood care, queen activity), larger worker morphology.

---

## 3. Translating Residues to Test Solutions / Doses

Below is a conversion cheat-sheet (Apis mellifera oral exposure) assuming 30 mg daily sugar intake per worker (typical cage study):

| Nectar concentration (ng g⁻¹ ≈ µg L⁻¹) | Daily AI intake/bee (ng) | % of acute LD₅₀ (0.185 µg, oral imidacloprid) |
|------------------------------------------|--------------------------|---------------------------------------------|
| 1 ng g⁻¹ | 0.03 ng | 0.016 % |
| 5 ng g⁻¹ | 0.15 ng | 0.081 % |
| 20 ng g⁻¹ | 0.60 ng | 0.32 % |
| 100 ng g⁻¹ | 3 ng | 1.6 % |

Thus, “field-realistic” chronic exposures often operate at <2 % of oral LD₅₀ per day, yet multi-week accumulation may still yield adverse colony outcomes.

---

## 4. Recommended Dose Blocks for Your Experiment (Neonicotinoid Focal Example)

Assuming you **will test thiamethoxam and imidacloprid** and plan both acute & chronic scenarios on *Bombus terrestris* workers (12–14 d old) via oral dosing (sugar syrup) and contact patches – adapt numbers for other species by LD₅₀ ratio.

### 4.1 Chronic Oral (10 wk)

| Level | Concentration in 50 % sucrose (µg L⁻¹) | Rationale |
|-------|----------------------------------------|-----------|
| Control | 0 | Baseline |
| Low | 1 | Geometric mean background in surface waters; below most nectar detections |
| Mid | 5 | Median cotton pollen residue; at upper quartile for wildflowers |
| High | 20 | 90th percentile wildflower pollen; still <10 % of imidacloprid study range |
| Positive | 100 | Supra-field (×5–10 realistic) – assures reference effect |

Each colony receives 10 wk continuous access. Confirm TWA by LC-MS/MS every 2 wk.

### 4.2 Acute Oral (24 h)

| Level | Dose per bee (ng) | Source |
|-------|-------------------|--------|
| Control | 0 | – |
| Low | 1 | Equivalent to 63 µg L⁻¹ puddle diluted 1:10 by foraging |
| Mid | 4 | 90th-percentile puddle; near EFSA RQ >1 for thiamethoxam |
| High | 10 | Worst-case puddle, still ≤0.05 LD₅₀ (B. terrestris more tolerant than Apis) |
| Positive | 75 | ~0.5 × contact LD₅₀ (B. terrestris), confirm mortality slope |

### 4.3 Contact Topical

Use 2 µL acetone carrier:

0 (control), 0.05, 0.2, 0.8, 4 µg bee⁻¹. Covers regulatory Tier I screen + sub-lethal bracket.

---

## 5. Adjustments for Other Pesticide Classes

1. **Pyrethroids (e.g., lambda-cyhalothrin, deltamethrin):** High contact toxicity (LD₅₀ 0.05–0.15 µg bee⁻¹) but low systemic residues in nectar. Field-realistic contact arises from foliar spray drift; measured pollen residues usually 10–40 ng g⁻¹. Therefore oral chronic 0.5–5 µg L⁻¹, contact patches 0.02–0.2 µg bee⁻¹ recommended.
2. **Organophosphates (e.g., chlorpyrifos):** Mostly withdrawn in EU/US but still relevant elsewhere. Drift residues in pollen up to 200 ng g⁻¹; acute contact LD₅₀ 0.07 µg bee⁻¹. Acute oral 2–20 ng bee⁻¹; chronic 5–25 µg L⁻¹.
3. **Fungicides (azoles) & Synergism:** Alone they have high LD₅₀ (>100 µg bee⁻¹) but potentiate neonics via P450 inhibition. You may integrate a factorial: 10 µg L⁻¹ imidacloprid ± 1 mg L⁻¹ propiconazole.

---

## 6. Species- and Life-Stage-Specific Sensitivity Multipliers

| Bee group | Oral LD₅₀ ratio vs. *A. mellifera* | Chronic sensitivity trend | Notes |
|-----------|-------------------------------------|---------------------------|-------|
| *Bombus terrestris* workers | ≈1–3× less sensitive (higher LD₅₀) | Colony-level reproduction *more* sensitive than adults | Social buffering obscures individual LD₅₀ relevance |
| *Osmia bicornis* females | ~0.5× (more sensitive) | Nest provisioning long exposure | Soil contact important |
| Honey bee larvae | 2–5× more sensitive than adults | Gut detox pathways undeveloped | Consider larval diet fortification assays |

Thus, if you switch species, **scale realistic dose downward** by the LD₅₀ ratio—e.g., for *Osmia*, cut concentrations by half.

---

## 7. Endpoints Beyond Mortality

1. **Behavior:** Tri-axial accelerometer tags to log activity; queen/worker interaction time; nurse visitation rate.
2. **Growth & Reproduction:** Colony mass curve, worker number, gynes/males produced, brood–nest area by digital image.
3. **Morphometrics:** Tegula span, wing venation defects as chronic developmental markers (tie in with the finding of +0.2–0.3 mm in imidacloprid study).
4. **Physiology:** RNA-seq of detox genes (CYP9Q), vitellogenin, immune genes; energetic metabolism via respirometry.
5. **Residue Confirmation:** Analyze bees, wax, pollen bread at study end to relate internal dose to effect.

---

## 8. Experimental Design & Quality Assurance

• At least 8 colonies per treatment (power ≥0.8 to detect 25 % effect). 
• Randomize colony placement to avoid positional bias.
• Blind observers to treatment.
• Use LC-MS/MS validated down to 0.1 ng g⁻¹ (S/N >3) for residue QC.
• Include a solvent control if carriers used.
• Positive control substance (e.g., dimethoate 4 µg L⁻¹) verifies assay sensitivity.

---

## 9. Potential Pitfalls & Proactive Solutions

| Pitfall | Mitigation |
|---------|------------|
| Rapid hydrolysis of thiamethoxam in syrup (t ½ ≈ 4 d) | Replace feed twice weekly; measure TWA concentrations |
| Colony size heterogeneity | Equalize starting worker count/queen age; include initial weight as covariate |
| Sugar-water evaporation altering dose | Use gravity feeders with catch cups; weigh feeders at each refill |
| “Ageing” of contacts patches due to volatility (pyrethroids) | Apply dose to dorsal thorax; dry 1 h before cage return |

---

## 10. Knowledge Gaps & Contrarian Ideas (Flagged Speculative)

1. **Landscape metagenomics** could reveal whether chronic neonic exposure reshapes gut microbiota, cascading to immunity – not yet mainstream.
2. **Photo-activated toxicity**: Some neonics yield nitro radicals under UV; outdoor micro-colony studies could capture this hidden risk.
3. **Mixture–time toxicity models (GUTS)** might predict survival curves better than static LD₅₀; integrating with measured pulse data could refine “field realism”.
4. **Chronic low-level exposure may up-regulate detox enzymes** and confer *transgenerational tolerance* – untested speculation worth incorporation as F₁ assays.

---

## 11. Executive Dose-Range Recommendation (Concise)

• **Chronic oral (10 wk):** 1, 5, 20 µg L⁻¹ neonics (plus 0 & 100 µg L⁻¹ controls).  
• **Acute oral (24 h):** 1, 4, 10 ng bee⁻¹ (plus 0 & 75 ng bee⁻¹ controls).  
• **Contact topical:** 0.05, 0.2, 0.8, 4 µg bee⁻¹.

These ranges straddle the *5th–99th percentile residue landscape*, incorporate regulatory benchmarks, and are broad enough to generate dose-response functions without exceeding logistic constraints.

---

### Closing Note

“Field-realistic” should be a **distribution, not a single number**. By anchoring your doses to recent residue monitoring, spanning multiple matrices, and adjusting for species-specific sensitivity, you will produce results that regulators and ecologists alike can translate directly into risk-assessment models.


## Sources

- https://pmc.ncbi.nlm.nih.gov/articles/PMC11636120/
- https://www.efsa.europa.eu/en/news/bees-and-pesticides-updated-guidance-assessing-risks
- https://www.researchgate.net/figure/Concentrations-of-clothianidin-imidacloprid-and-thiamethoxam-and-the-corresponding_fig5_317443084
- https://www.cabidigitallibrary.org/doi/pdf/10.5555/20210007897
- https://www.sciencedirect.com/science/article/am/pii/S0048969722039547
- https://pesticiderisk.org/materials/PRT_Bees_index_October_%202014_For%20release.pdf
- https://aaes.uada.edu/news/residual-pesticides-bees/
- https://xerces.org/sites/default/files/2018-05/16-022_01_XercesSoc_How-Neonicotinoids-Can-Kill-Bees_web.pdf
- https://www.sciencedirect.com/science/article/pii/S0160412022002380
- https://www.researchgate.net/publication/327144223_Plant_guttation_water_as_a_potential_route_for_pesticide_exposure_in_honey_bees_a_review_of_recent_literature
- https://setac.onlinelibrary.wiley.com/doi/10.1002/etc.5871
- https://efsa.onlinelibrary.wiley.com/doi/pdf/10.2903/sp.efsa.2012.EN-340
- https://royalsocietypublishing.org/doi/10.1098/rspb.2022.0253
- https://enveurope.springeropen.com/articles/10.1186/s12302-024-01039-9
- https://pubmed.ncbi.nlm.nih.gov/29524816/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC5533829/
- https://www.researchgate.net/publication/290475614_Determination_of_acute_lethal_doses_LD50_and_LC50_of_imidacloprid_for_the_native_bee_Melipona_scutellaris_Latreille_1811_Hymenoptera_Apidae
- https://www.sciencedirect.com/science/article/pii/S0048357520300572
- https://www.epa.gov/sites/default/files/2016-07/documents/guidance-exposure-effects-testing-assessing-risks-bees.pdf
- https://pmc.ncbi.nlm.nih.gov/articles/PMC11649340/
- https://www.epa.gov/sites/default/files/2014-06/documents/pollinator_risk_assessment_guidance_06_19_14.pdf
- https://www.mass.gov/doc/neonics-scientific-literature-review-framework/download
- https://www.beyondpesticides.org/programs/bee-protective-pollinators-and-pesticides/what-the-science-shows
- https://hal.science/hal-01284436/document
- https://www.researchgate.net/publication/323441816_Concentrations_of_imidacloprid_and_thiamethoxam_in_pollen_nectar_and_leaves_from_seed-dressed_cotton_crops_and_their_potential_risk_to_honeybees_Apis_mellifera_L
- https://www.beyondpesticides.org/assets/media/documents/pollinators/nolongeraBIGmystery.pdf
- https://www.efsa.europa.eu/sites/default/files/topic/files/BeeGD_1st_consultation_comments.xlsx
- https://www.sciencedirect.com/science/article/abs/pii/S0147651313004703
- https://www.unito.it/sites/default/files/1-s2.0-s0048969722039547-main.pdf
- https://www.epa.gov/sites/default/files/2015-06/documents/091112minutes.pdf
- https://www.researchgate.net/publication/358319226_Acute_oral_toxicity_and_risks_of_four_classes_of_systemic_insecticide_to_the_Common_Eastern_Bumblebee_Bombus_impatiens
- https://www.academia.edu/66527651/Assessment_of_risks_to_honey_bees_posed_by_guttation
- https://www.sciencedirect.com/science/article/abs/pii/S0045653518303801
- https://nora.nerc.ac.uk/id/eprint/516061/1/N516061PP.pdf
- https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7989
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8215506/
- https://www.eurofins.com/media/1069301/11-honey-bees-and-bumble-bees-data-sheet-a5-2pp-web.pdf
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4284396/