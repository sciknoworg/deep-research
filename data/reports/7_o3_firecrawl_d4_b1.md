# Designing Realistic yet Mechanistically-Informative Pesticide Exposure Ranges for Bee Toxicology Experiments

## 1  Scope and Rationale
Research on pesticide effects on bees often fails because the exposure regime is either (i) too narrow—focusing only on a single “field-realistic” point estimate—or (ii) unrealistically high, undermining ecological relevance.  The goal is to define *tier-1* (acute) and *tier-2* (chronic/sub-lethal) concentration ranges that 
1. span the **full gradient** from undetectable background residues up to clear mortality thresholds, and 
2. reflect **matrices** (nectar, pollen, wax, soil, spray droplets) and **taxa/stages** (honey-bee foragers, bumblebee queens, larvae) actually encountered in real landscapes.

This report synthesises published residue data, steep dose–response characteristics, and known synergisms to recommend exposure ranges and experimental design options for three pesticide classes—**neonicotinoids, pyrethroids, and organophosphates**—plus fungicide co-formulants that modulate detoxification.  All quantitative values below are drawn from the compiled learnings unless stated otherwise; speculative extrapolations are flagged as such.

---

## 2  Empirical Foundations
### 2.1  Field Residue Envelope (six-order magnitude span)
• Nectar: <0.3 – 17 µg kg⁻¹ (seed-treated crops ≤5.4 µg kg⁻¹; soil-drench pumpkin 17.6 µg kg⁻¹).

• Pollen: 0.3 – 51 µg kg⁻¹ typical, but spikes of 122 µg kg⁻¹ (pumpkin) and 912 µg kg⁻¹ (imidacloprid, Saskatchewan).

• Guttation / planter dust: µg–mg L⁻¹ pulses—e.g. imidacloprid 346 mg L⁻¹ in droplets, clothianidin 102 mg L⁻¹ airborne.

• Wax (long-term sink): up to 154 µg kg⁻¹ thiacloprid.

• Soil reservoir: clothianidin half-life 148–6 900 d → chronic root uptake for years.

### 2.2  Toxicodynamic Steepness
• Acute LD₅₀ (48 h) for honey bees and bumble bees: **1–5 ng bee⁻¹** for clothianidin/imidacloprid.

• Time-to-50 % mortality vs. dose shows **log-dose × log-time linearity**; chronic exposure can increase lethality **10⁵-fold** relative to 48 h LD₅₀.

• Sub-lethal diet levels: 0.7 µg kg⁻¹ nectar + 6 µg kg⁻¹ pollen imidacloprid → **–85 %** Bombus queen output; 3.7 µg kg⁻¹ syrup halves micro-colony foraging; 1 µg kg⁻¹ thiamethoxam shortens honey-bee lifespan 41 %.

### 2.3  Synergistic Interactions
• Azole fungicides (fenbuconazole, triflumizole) inhibit CYP P450s; co-exposure with thiacloprid ↑ toxicity **up to 1 141×**.

• Clothianidin + coumaphos oxon (or assorted fungicides) produce additive neural blockade.

• Average field sample: **5–14 active ingredients** per bee-relevant matrix (mean 12.9–14.2 in honey), making interaction experiments ecologically pertinent.

---

## 3  Recommended Concentration Framework
The table below gives *start-of-gradient* (minimum), *field-realistic*, *upper field spike*, and *lethal window* concentrations for three exposure matrices.  Convert units carefully; syrup or pollen-paste feeding is expressed µg kg⁻¹ (ppb), contact as ng bee⁻¹, and spray residue as ng cm⁻².

| Class (AI example) | Matrix | Min (control+) | Realistic Mode | High-Spike | Lethal Window |
|--------------------|--------|----------------|----------------|------------|---------------|
| Neonic (clothianidin) | Oral syrup (foragers) | 0.02 µg kg⁻¹ (detect limit) | 0.5 µg kg⁻¹ | 20 µg kg⁻¹ | 50–500 µg kg⁻¹ |
|                    | Contact (queen) | 0.01 ng bee⁻¹ | 0.3 ng bee⁻¹ | 2 ng bee⁻¹ | 5–10 ng bee⁻¹ |
| Pyrethroid (λ-cyhal.)| Spray residue | 0.1 ng cm⁻² | 2 ng cm⁻² | 10 ng cm⁻² | 30–100 ng cm⁻² |
| Organophos (chlorpyrifos)| Larval diet | 0.05 µg kg⁻¹ | 1 µg kg⁻¹ | 10 µg kg⁻¹ | 100 µg kg⁻¹ |

**Why these bounds?**
• 0.5 µg kg⁻¹ is the lower quartile of documented nectar residues.
• 20 µg kg⁻¹ equals the 95th percentile in soil-drench cucurbits.
• Contact 0.3 ng bee⁻¹ approximates foliar spray deposits on a 150 mg bee landing on a 2 µg g⁻¹ leaf surface.
• ≥50 µg kg⁻¹ begins to overlap the *in vivo* LD₅₀ when translated to total daily syrup intake (~30 mg day⁻¹ per worker).

### 3.1  Tiered Experimental Series
1. **Core 4-point semi-log series**: 0, 0.3, 3, 30 µg kg⁻¹ (or ng bee⁻¹ / ng cm⁻² equivalent).
2. **Fine sub-lethal grid (behaviour focus)**: 0, 0.1, 0.3, 1, 3 µg kg⁻¹.
3. **Lethal confirmation**: 10, 30, 100 µg kg⁻¹.
4. **Synergy blocks**: Repeat series with fungicide (fenbuconazole 1 µg kg⁻¹) held constant; hypothesised shift of entire curve leftward by ×10–1 000.

*(Speculative)* For bumblebee queens overwintering intake is only ~10 mg day⁻¹; therefore translate syrup concentrations by ×3 to achieve equivalent dose.

---

## 4  Matrix-Specific Implementation
### 4.1  Oral Syrup (Apis mellifera foragers)
• Feed groups of ~30 caged workers ad libitum 50 % sucrose spiked at target concentrations for 10 d.

• Measure daily consumption to derive µg bee⁻¹ d⁻¹, linking to chronic LD₅₀ time-scaling.

• Endpoints: survival, proboscis extension reflex (PER) learning on day 6, hypopharyngeal gland volume on day 10.

### 4.2  Pollen Paste / Larval Diet
• Mix pesticide into fresh frozen pollen : syrup 70:30 at stated µg kg⁻¹; feed to 2nd-instar larvae *in vitro*.

• For chronic studies, mimic brood-cycle 6 d larval + 12 d pupation; static concentration acceptable because of low metabolism in jelly.

### 4.3  Contact Residue (Bombus terrestris queens)
• Apply 1 µL acetone droplet to thorax containing ng target dose.

• Alternatively use Potter spray tower to achieve uniform ng cm⁻² leaf surrogate, then allow queens to walk on surface.

### 4.4  Spray Drift / Whole-Colony Tunnel
• Fog commercial formulation at label rate in 30 m × 3 m polytunnel; sample airborne and floral residues; adjust to hit 2 ng cm⁻² mean.

*(Contrarian idea)* Deploy **cold plasma-charged droplets** to evaluate whether electrodynamic deposition (a proposed “bee-safe precision spray”) genuinely reduces on-floral residues by >80 %.

---

## 5  Integration of Synergistic Stressors
Given the omnipresence of multi-AI residues (mean 12.9–14.2 AIs in honey), *single-compound tests alone are insufficient.*  Two practical additions:

1. **Fungicide pairing**: fenbuconazole 1 µg kg⁻¹ (field-realistic) + thiacloprid grid.  Expect up to 1 141× toxicity shift; design lower half-log dilutions (0.01, 0.03, 0.1 µg kg⁻¹) to capture shift.

2. **In-hive acaricide carryover**: coumaphos oxon at 100 µg kg⁻¹ wax; run contact trials where bees must traverse treated wax before feeding.

*(Speculative)* Incorporate common **herbicide glyphosate 5 mg kg⁻¹** to test indirect microbiome impairment enhancing neonic absorption.

---

## 6  Temporal Scaling and Endurance Tests
Because lethality escalates up to 10⁵-fold with exposure duration, running only 48 h assays underestimates risk.

Recommended timeline per replicate:
• 0–48 h: Acute endpoints (KD, mortality).
• Day 3–7: Behavioural assays (PER, homing flight in RFID tunnel).
• Day 10–14: Physiological metrics (hemocyte count, oxidative stress markers).
• Day 21: Survival plateau—compare Kaplan–Meier curves; fit log-dose × log-time linear model.

---

## 7  Statistical Design Guidance
1. **Replication**: ≥4 cages (n≈30 bees) per concentration to detect 15 % survival change with 80 % power, α = 0.05 assuming binomial dispersion.
2. **Randomised block** for temporal batches; include cage as random effect in GLMM.
3. **Synergy quantification**: apply Bliss independence and Loewe additivity models; report interaction factor (IF) and its CI.
4. **Dose–response fitting**: 4-parameter log-logistic; check goodness with lack-of-fit test; derive benchmark dose BMD₁₀.

---

## 8  Risk Translation and Predictive Modelling
• Integrate residue distribution (log-normal) with fitted dose–response to calculate **probability of effect** across landscapes (Bayesian kernel integration).

• Feed outputs into colony dynamic model (e.g. BEEHAVE) to translate individual impairment to colony growth; parameterise with –85 % queen production at 0.7/6 µg kg⁻¹ diet.

---

## 9  Future-Proofing and Emerging Technologies
1. **RNAi co-formulations**: test whether dsRNA targeting detox genes synergises with neonic at 0.1 µg kg⁻¹ (speculative, flagged).
2. **Photocatalytic detox films** on petals (TiO₂-based) that degrade residues within hours—include control plots to verify residue drop from 3→0.05 µg kg⁻¹.
3. **Metabolomic fingerprinting**: untargeted LC-HRMS on hemolymph to pick early distress signals before mortality.
4. **Contrarian**: Evaluate *low-dose hormesis*; include 0.01 µg kg⁻¹ where certain detox pathways may up-regulate and improve survivorship.

---

## 10  Checklist Before Execution
✓ Confirm analytical limits of detection (LOD ≤0.01 µg kg⁻¹).
✓ Validate spike recoveries in each matrix (>80 % recovery, RSD <15 %).
✓ Ensure solvent carrier ≤0.1 % v/v to avoid confounding toxicity.
✓ Calibrate micro-balance for ng dosing accuracy.
✓ Ethics/permits for Bombus collection and release.

---

## 11  Conclusions
A scientifically robust “realistic pesticide range” for bee impact experiments is **not a single point but a structured logarithmic series** bridging (i) non-detectable to (ii) median field residue, to (iii) upper-tail spikes, through (iv) confirmed lethal bands.  For neonicotinoids this means ~0.1 µg kg⁻¹ up to ~100 µg kg⁻¹ in dietary matrices or 0.01–10 ng bee⁻¹ contact.  Incorporating fungicide co-exposures is mandatory given empirical ≥1 000× synergisms.  Temporal scaling past 48 h reveals lethalities up-by-10⁵, so chronic assays (≥21 d) are essential.

Implementing the tiered design above will generate full dose–response curves, synergy coefficients, and mechanistic insights necessary for realistic risk assessment and for innovating mitigation technologies such as precision sprays or photocatalytic films.


## Sources

- https://pmc.ncbi.nlm.nih.gov/articles/PMC4284392/
- https://xerces.org/sites/default/files/2018-05/16-022_01_XercesSoc_How-Neonicotinoids-Can-Kill-Bees_web.pdf
- https://www.sciencedirect.com/science/article/pii/S1877343513000493
- https://www.sciencedirect.com/science/article/abs/pii/S0304389424004710
- https://www.researchgate.net/publication/284360069_Concentrations_of_neonicotinoid_insecticides_in_honey_pollen_and_honey_bees_Apis_mellifera_L_in_central_Saskatchewan_Canada
- https://www.beyondpesticides.org/programs/bee-protective-pollinators-and-pesticides/what-the-science-shows