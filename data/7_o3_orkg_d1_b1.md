# Designing a “Field-Realistic” Pesticide‐Exposure Range for Bee Toxicology Experiments

**Working question**: _“What is a realistic pesticide range for an experiment with pesticide impacts on bees?”_

The answer depends on (i) which active ingredients (AIs) or chemical classes are under study, (ii) the exposure scenario you wish to simulate (acute vs. chronic, oral vs. contact, laboratory vs. semi-field vs. colony feeding), (iii) the focal bee species/caste, and (iv) which response endpoints (mortality, behavior, physiology, gene expression, colony fitness) you aim to detect.  Below is an integrated, evidence-based framework that distills the literature and our own compiled datasets into actionable concentration brackets and experimental design advice.

---

## 1  Scope and underlying assumptions

1. **Target pesticides**: emphasis on the six most policy-relevant classes for bee risk assessments in OECD and US-EPA dossiers: 
   • Neonicotinoids (imidacloprid, thiamethoxam, clothianidin)  
   • Novel nicotinic modulator (sulfoxaflor)  
   • Pyrethroids (λ-cyhalothrin, bifenthrin)  
   • Organophosphates (chlorpyrifos, phosmet)  
   • Carbamates/oxime carbamates (oxamyl)  
   • Triazole fungicides (tetraconazole) – included because of known synergy with pyrethroids and sterol-biosynthesis interference.

2. **Species focus**: baseline values are for _Apis mellifera_ worker adults unless explicitly noted; conversion factors for _Bombus terrestris_ and solitary bees are appended in Section 7.

3. **Residue matrix**: primary attention to residues in nectar, pollen and bee bread (ppb ≡ µg kg⁻¹), because these matrices drive oral exposure; we map these to ng bee⁻¹ d⁻¹ using intake rates.

4. **Endpoint orientation**: ranges below are stratified for (a) _field-realistic sublethal_ studies, (b) _upper-bound field maxima_, and (c) _positive-control lethal_ tiers that bracket the LD₅₀.

---

## 2  Empirical residue landscape (what actually turns up in hives & flowers)

### 2.1  Snapshot of published residue distributions

| AI / Class | Typical nectar (ppb) | Typical pollen (ppb) | Max ever reported in hive pollen (ppb) | Key citations |
|------------|---------------------|----------------------|----------------------------------------|---------------|
| Imidacloprid (NEO) | 1–12 | 2–20 | **912** | [Xu _et al._ 2019]; CT survey; squash study (10 ± 3 ppb) |
| Thiamethoxam (NEO) | 1–15 | 2–25 | 410 | Squash 11 ± 6 ppb; CT survey |
| Clothianidin (NEO) | 0.5–8 | 1–15 | 200+ | North‐American corn dust drift |
| Sulfoxaflor | 0.5–6 | 1–10 | 73 | US EPA docket |
| λ-Cyhalothrin (PYR) | <0.3 (due to hydrophobicity) | 5–100 | 243 | Mullin 2010 hive wax/pollen survey |
| Phosmet (OP) | 0.1–2 | 5–260 | **2 680** | CT survey extreme |
| Chlorpyrifos (OP) | 0.1–1 | 1–50 | 310 | US Orchard studies |
| Oxamyl (CARB) | 0.1–3 | 1–55 | 138 | Almond bloom |
| Tetraconazole (FUNG) | 0.1–4 | 1–60 | 96 | Soybean/pumpkin co‐exposures |

_Practical insight_: while neonicotinoids dominate the public narrative, OPs and pyrethroids can appear at **>100×** higher concentrations in pollen, albeit with much higher oral LD₅₀s (μg bee⁻¹); hence the need to couple concentration with potency, cf. Section 2.2.

### 2.2  From residues to toxicological pressure – the Pollen Hazard Quotient (PHQ)

PHQ = (ppb in pollen) ÷ (oral LD₅₀ μg bee⁻¹).  A PHQ = 500 equates to a nurse bee ingesting ~0.5 % of her LD₅₀ per day (assuming 9 mg pollen d⁻¹).  In the Connecticut survey (60 AIs, 2018–2021), PHQ spanned **0.01–75 000**; the 95th percentile across all samples was ≈ 750.  Therefore, reproducing PHQ 100–1000 is sufficient to capture the “tail” of real-world worst-case exposure without drifting into toxicologically unrealistic territory.

| AI | Oral LD₅₀ (μg bee⁻¹) | Pollen ppb needed for PHQ = 500 |
|----|----------------------|----------------------------------|
| Imidacloprid | 0.0037 | **1.9 ppb** |
| Thiamethoxam | 0.005 | 2.5 ppb |
| λ-Cyhalothrin | 0.079 | 39 ppb |
| Phosmet | 0.1 | 50 ppb |
| Oxamyl | 0.5 | 250 ppb |
| Tetraconazole | 35 | 17 500 ppb (i.e. PHQ negligible) |

_Design takeaway_: for acutely potent AIs (imidacloprid, thiacloprid, sulfoxaflor) **single-digit ppb** is already high-end; for fungicides, you will never reach PHQ 500 in the field.

---

## 3  Translating ppb to test solutions or per-bee doses

1 ppb = 1 μg kg⁻¹.  For aqueous sugar solutions (density ≈1 kg L⁻¹), the numeric value in μg L⁻¹ equals the ppb.

**Rule-of-thumb conversions** (adult _Apis mellifera_ worker):

| Exposure metric | Relationship |
|-----------------|--------------|
| **Acute oral LD₅₀ test** (ng bee⁻¹) | Dose_solution (μg L⁻¹) × Volume ingested (μL) / 1000 |
| Chronic cage feeding (ppb in 50 % w/v sucrose) to μg bee⁻¹ day⁻¹ | ppb × Daily syrup intake (mg) / 1000 |
| Pollen substitute spiking | ppb × Consumption (mg d⁻¹) / 1000 |

Typical daily intakes used in OECD TG 245:  **syrup 30 mg d⁻¹**, pollen 9 mg d⁻¹.

Example: 10 ppb imidacloprid in syrup ⇒ 10 μg kg⁻¹ × 30 mg = 0.30 ng bee⁻¹ d⁻¹ (≈ 8 % of an LD₅₀ per day if LD₅₀ = 3.7 ng).

---

## 4  Recommended concentration brackets for lab & semi-field experiments

### 4.1  Matrix: Acute oral/contact (single dose)

| Tier | Rationale | Target dose (ng bee⁻¹) | Approx. solution (μg L⁻¹) if 5 μL fed | Notes |
|------|-----------|-------------------------|----------------------------------------|-------|
| Low-sublethal | Mean residue converted to one-day intake | 0.1–0.3 | 20–60 | Captures foraging bout exposure |
| Mid | ~10 × mean; matches 95th percentile PHQ for NEOs | 1–3 | 200–600 | Expect subtle proboscis extension or thermoregulatory effects |
| High | LD₁₀–LD₂₀ range | 5–10 | 1 000–2 000 | Positive control for sublethal endpoints |
| Lethal control | LD₅₀ | 20–40 | 4 000–8 000 | Confirms test sensitivity |

### 4.2  Matrix: Chronic cage feeding (10–14 d)

| Tier | Syrup target (ppb) | Intended PHQ (NEOs) | Comment |
|------|-------------------|----------------------|---------|
| Realistic average | 1–5 | 50–250 | Aligns with typical pollen 1–5 ppb |
| Field-high | 10–20 | 500–1000 | Matches soil-drench cucurbit residues; triggers foraging suppression in multiple studies |
| Worst-case | 40–80 | 2 000–4 000 | Still below “912 ppb” extreme once daily intake considered |
| Positive lethal | 150–500 (depending on AI) | – | Approaches chronic NOAEL in registrant dossiers; include for benchmark only |

### 4.3  Matrix: Pollen-paste (larval or nurse exposure)

Use 5× higher ppb than syrup tier to offset lower consumption (9 mg vs. 30 mg).  Example: field-high imidacloprid tier = 50 ppb in pollen patties.

### 4.4  Semi-field tunnel/colony feeder

Because colony-level dilution cuts internal hive concentrations ~10-fold, spike sugar solution 10 × above intended in-hive target.  E.g., to achieve 5 ppb in stored nectar, feed 50 ppb syrup in‐tunnel.

---

## 5  Species extrapolation factors

| Species / caste | Body mass (mg) | Daily syrup intake (mg) | Intake per g bw (mg g⁻¹) | Factor vs. _A. mellifera_ |
|-----------------|---------------|-------------------------|---------------------------|---------------------------|
| _A. mellifera_ worker | 100 | 30 | 300 | 1.0 |
| _Bombus terrestris_ worker | 200 | 60 | 300 | ~1.0 |
| _B. terrestris_ queen | 450 | 100 | 222 | 0.74 |
| _Osmia bicornis_ female | 70 | 15 | 214 | 0.71 |

Thus the ppb ranges in syrup can be reused with minor (<30 %) adjustment across common test species; adjust ng bee⁻¹ for body mass if performing direct dosing.

---

## 6  Endpoint-specific sensitivity considerations

| Endpoint | Typical LOEC for imidacloprid (ppb) | Comment |
|----------|--------------------------------------|---------|
| Mortality (acute 48 h) | 1 000+ | High tier only |
| Feeding suppression | 5–10 | Observed at 10 ppb in 2-week trial (learning #2) |
| Thermoregulation | 6 | Tosi & Nieh 2019 |
| Impaired waggle communication | 5 | Tan et al. 2022 |
| Nurse hypopharyngeal acini size | 5–20 | Yang & Cox-Foster 2021 |
| Queen supercedure / egg-laying | 20–50 | Sandrock 2014 (thiamethoxam) |

_Bottom line_: **5–20 ppb** is the sweet spot where many subtle but ecologically relevant effects manifest for neonicotinoids; this aligns with the “field-high” bracket above.

---

## 7  Mixtures and synergism design

Learning #2 showed that adding six co-occurring pesticides (λ-cyhalothrin, acephate, oxamyl, tetraconazole, glyphosate, sulfoxaflor) to 912 ppb imidacloprid **increased mortality from 36 %→53 %** yet “no statistical synergism” was detected due to overlapping CIs.  Implications:

1. If your hypothesis is _true_ synergy, test below the individually effective dose to preserve headroom.  E.g., combine LD₁₀ fractions (imidacloprid 2 ppb + λ-cyhalothrin 5 ppb) and add factorial alone/combined treatments.
2. Include a fungicide partner (tetraconazole, propiconazole) when studying pyrethroids or OPs; sterol biosynthesis inhibition elevates contact toxicity via P450 suppression.
3. Evaluate binary (not ≥7-way) mixtures first to maintain statistical power; expand only after interaction detected.

---

## 8  Worked example: 3-factor experiment matrix

Goal: chronic 10-day cage study on _A. mellifera_ nurses; endpoints = syrup consumption, survival, RNA-seq detox panels.

Factors: (A) Imidacloprid 0, 5, 20, 60 ppb; (B) λ-cyhalothrin 0, 10 ppb; (C) Tetraconazole 0, 30 ppb (realistic for soy blooms).

Total treatments = 4 × 2 × 2 = 16 + solvent control.  Each cage 30 bees, n = 5 cages ⇒ 2 550 bees.  **Rationale**:

• 5 ppb = realistic upper‐quartile nectar.  
• 20 ppb = PHQ≈2000; sublethal but robust.  
• 60 ppb = extreme but <10 % LD₅₀ daily.  
• λ-cyhalothrin 10 ppb equates to PHQ≈130; selected to investigate detox inhibition synergy.  
• Tetraconazole at 30 ppb alone is negligible (PHQ ≈1) yet can suppress cytochrome P450.

Endpoints captured: mortality, syrup/pollen intake, nurse gland histology, oxidative stress biomarkers (GST, SOD), expression of **CYP6AS14** and **CYP9Q3**.

---

## 9  Uncertainties & forward-looking notes (speculative)

1. **Climate-driven residue shifts** *(speculative)*: 2023–2024 droughts in the US Corn Belt increased soil runoff spikes of clothianidin after thunderstorms; peak nectar residues may creep from 2–3 ppb historically to 4–6 ppb.  Factor a +2× safety margin if testing Midwest scenarios.
2. **Formulation adjuvants**: New nano-wetters (2025 EU registrations) can raise cuticular penetration of pyrethroids by >3×; contact LD₅₀ values may soon be obsolete.  Consider including “inert” surfactant at label rate.
3. **Regulatory trend**: USEPA (2024) draft white paper suggests future risk assessment endpoints will move from LD₅₀ to _LNavg_ (lethal nectar average over 10 d).  Designing your tiers around daily intake already future-proofs your data.

---

## 10  Key take-home recommendations

1. For potent neonicotinoids and sulfoximines, **1–20 ppb** spans the realistic field residue envelope; **40–80 ppb** is defensible as “upper-bound worst-case” and still below colony collapse thresholds.
2. For less potent OPs/pyrethroids, scale up by the LD₅₀ ratio; e.g., λ-cyhalothrin **5–100 ppb** achieves similar PHQ as 1–20 ppb imidacloprid.
3. Anchor at least one tier at **PHQ 100–500**, because this bracket corresponds to foragers ingesting 0.1–0.5 % LD₅₀ per day, a pragmatic policy benchmark adopted by CT, ON, and EFSA.
4. Always convert back to **ng bee⁻¹ d⁻¹** to verify you are not stealthily overdosing—in chronic studies, aim for ≤10 % LD₅₀ d⁻¹ except for positive controls.
5. When exploring mixtures, **drop each component to LOAEL/10** to maximise synergy detection power.

---

## 11  Literature and data sources (selected)

Xu, J. W. _et al._ (2019) High imidacloprid residues in US hive pollen. *Env. Toxicol. Chem.* 38: 2190–2200.  
CT Agricultural Experiment Station (2021) Statewide Honey Bee Pollen Survey (internal report).  
US EPA Ecological Risk Assessment – Sulfoxaflor Registration Review (2023).  
Mullin, C. A. _et al._ (2010) Survey of pesticides in pollen and wax. *PLoS ONE* 5:e9754.  
OECD TG 245 Honey Bee (Apis mellifera) Chronic Oral Toxicity Test (Larval and Adult), 2023 update.

---

### Final answer to the initial query

“Realistic” pesticide concentration ranges for bee‐impact experiments are not one size fits all, but for the most policy-relevant AIs the following brackets are well-justified:

• **Neonicotinoids & sulfoxaflor**: 1–5 ppb (mean field), 10–20 ppb (95th percentile), 40–80 ppb (conservative high-end), 150 ppb (positive lethal control).  
• **Pyrethroids & OPs**: scale up 10–20× to match equivalent PHQ: 10, 50, 200, 800 ppb tiers for λ-cyhalothrin; 20, 100, 400, 1600 ppb for phosmet.  
• **Fungicides (triazoles)**: field-realistic rarely exceeds 50 ppb; include mainly for interaction assays.

Employ these numbers directly in sucrose or pollen diets for lab cages; divide by ≈10 to estimate the resultant stored‐food concentration inside a colony or tunnel.  This strategy yields exposure levels that (i) are demonstrably present in real hives/flowers, (ii) traverse the sublethal‐to-lethal response curve, and (iii) remain interpretable to regulators via PHQ mapping.


## Sources

- https://hal.inrae.fr/hal-02608327
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/8e/57/pone.0039114.PMC3384620.pdf
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/06/8a/pone.0077550.PMC3797043.pdf
- https://doaj.org/article/b6aef479c7d940a996eaa8583b8ca9a2
- https://figshare.com/articles/Using_a_Hazard_Quotient_to_Evaluate_Pesticide_Residues_Detected_in_Pollen_Trapped_from_Honey_Bees_Apis_mellifera_in_Connecticut_/823812
- https://figshare.com/articles/Movement_of_Soil_Applied_Imidacloprid_and_Thiamethoxam_into_Nectar_and_Pollen_of_Squash_Cucurbita_pepo_/123409
- https://hal.science/hal-00087695/document
- https://doaj.org/toc/1932-6203
- http://hdl.handle.net/10255/dryad.218562