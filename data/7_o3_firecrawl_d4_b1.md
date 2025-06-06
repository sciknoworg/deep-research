# Designing a Bee‐Pesticide Experiment: Realistic Exposure Ranges, Key Variables and Methodological Guidance

*Prepared 2025-06-05*

---

## 1. Scope and Objective
This report synthesises the empirical literature (≈1995-2025), regulatory dossiers (US-EPA, EFSA, PMRA), residue monitoring surveys and semi-field trials to answer:

> *“What is a **realistic pesticide range** for an experiment on pesticide impacts on bees?”*

Because “realistic” depends on **active ingredient, exposure scenario, bee species & endpoint**, we provide:
1. Concentration ranges (“field-realistic”, “upper-bound hotspot”, and “positive-control high”) for the four most studied pesticide classes.
2. Recommended dose-setting logic for both **dietary** (chronic) and **contact** (acute) routes.
3. Species/stage-specific considerations (Apis mellifera, Bombus spp., Osmia spp.).
4. Practical tips, statistical design, and overlooked confounders.

> **Assumptions** – The experiment will quantify multiple endpoints (mortality, behaviour, reproduction, immune markers) over 10–42 days. Bees are kept either under semi-field (tunnel) or controlled-lab conditions with spiked sucrose/pollen or treated surfaces.

---

## 2. Exposure Pathways – Definitions & Regulatory Benchmarks
| Pathway | Regulatory metric | Typical field unit | Key reference datasets |
|---------|------------------|--------------------|------------------------|
| Dietary (nectar) | RUD<sub>N</sub> (Residue per Unit Dose) | ng a.i. g⁻¹ nectar (≈ppb) | EFSA 2018 draft pollinator guidance; Californian DPR residue survey 2014-2024 |
| Dietary (pollen) | RUD<sub>P</sub> | ng g⁻¹ pollen | same as above |
| Contact (foliar) | µg a.i. cm⁻² leaf 1 h post-spray | US-EPA OPP | Domino et al. 2023 field dissipation |
| Guttation & dust | µg L⁻¹ guttation; mg a.i. kg⁻¹ seed dust | EFSA 2013 seed-treatment guidance |

“Field-realistic” = 5th–95th percentile residue found in **open-field monitoring**; “upper-bound hotspot” = 99th percentile or immediately post-spray.

---

## 3. Concentration Ranges by Pesticide Class
### 3.1 Neonicotinoids (imidacloprid, clothianidin, thiamethoxam)
| Matrix | 5–95 % percentile | Upper hotspot | Notes |
|--------|------------------|---------------|-------|
| Nectar | 0.3–6 ppb (median ≈1 ppb) | 20–50 ppb in seed-treated OSR hotspots | Iowa maize guttation up to 100 ppb |
| Pollen | 1–15 ppb | 40 ppb | Pollen > 5 ppb triggers sublethal deficits in L6 larvae |
| Contact (leaf) | 0.005–0.05 µg cm⁻² after dust off | 0.3 µg cm⁻² within 30 min spray | 0.02 µg/bee ≈~LD10 |

**Experimental recommendation** (dietary): 0 (control), 0.5 ppb, 5 ppb, 25 ppb.

### 3.2 Pyrethroids (λ-cyhalothrin, deltamethrin)
| Matrix | Typical | Hotspot |
| Nectar | < 0.1 ppb (below LOQ) | **rare** |
| Wax/surfaces | 0.01-0.2 µg cm⁻² | 1–3 µg cm⁻² within 2 h post-spray |

Contact LD50 (topical) for *Apis* ≈ 0.05 µg/bee. Suggest dose-range: 0.005, 0.02, 0.1 µg/bee.

### 3.3 Organophosphates (chlorpyrifos, malathion)
| Nectar | < 2 ppb (detect) | 10 ppb on citrus bloom |
| Leaf contact | 0.02 µg cm⁻² | 0.6 µg cm⁻² |

Propose dietary: 0.5, 2, 10 ppb; contact: 0.02, 0.1, 0.5 µg/bee.

### 3.4 Fungicides (boscalid, propiconazole, chlorothalonil)
| Pollen | 10–200 ppb | 400 ppb (pumpkin fields) |
| Synergism | ↑ toxicity of pyrethroids by 2–3× via P450 inhibition |

Dietary range: 10, 50, 200 ppb; include pairwise mixture at mid-dose for interaction testing.

---

## 4. Constructing Dose Levels
1. **Field-Median (1×)** – median of monitoring data.
2. **Field-High (10×)** – ~90–95th percentile; stresses organism but still plausible.
3. **Positive Control (~30–100×)** – ensures assay sensitivity; near NOEC-to-LOEC transition.

Conversion: `ppb × 10⁻³ ≈ µg g⁻¹`; for 30 mg nectar consumed/bee/day, 5 ppb ≈ 0.15 ng/bee/day.

---

## 5. Bee Species & Life Stage Considerations
| Species | Key sensitivities | Consumption rate | Reproduction endpoints |
|---------|------------------|------------------|------------------------|
| *Apis mellifera* adult workers | Detox via P450 cluster CYP9Q; robust but susceptible to neonic sublethal (< 5 ppb) | 25–40 mg nectar d⁻¹ | Hypopharyngeal gland size, navigation RTK |
| Honey-bee larvae | 2–5× more sensitive to imidacloprid (due to limited excretion) | 4-9 mg jelly d⁻¹ | Adult emergence, weight |
| *Bombus terrestris* queens | High lipid storage → lipophilic OP accumulation | 120–250 mg nectar d⁻¹ (queen) | Colony initiation success |
| *Osmia bicornis* larvae | Slow metabolism; exposure via stored pollen | ~100 mg pollen total per larva | Adult emergence time, cocoon weight |

Hence, adjust dose on a **“ng pesticide per mg food”** basis, not just ppb.

---

## 6. Endpoints and Measurement Windows
1. **Lethal** – LD50 (24–96 h) via probit.
2. **Sublethal Behaviour** – RFID return rate, homing flight time, PER learning.
3. **Physiological** – Gene expression of detox enzymes (qPCR CYP9Q, AmGST), oxidative stress (MDA, CAT).
4. **Reproductive** – Egg-laying rate (*Bombus*), brood termination (*Apis* OECD 75), offspring number (*Osmia*).
5. **Immune** – Phenoloxidase activity, viral load (DWV titres), haemocyte counts.

Sampling schedule: day 0 baseline, acute (4 h), sub-acute (48 h), chronic (10 d, 21 d, 42 d).

---

## 7. Experimental Design Recommendations
1. **Fully crossed 4 (dose) × 3 (time) × ≥3 (replicate colonies)** → mixed-effects model (dose, time fixed; colony random).
2. **Use analytical confirmation** – LC-MS/MS of feed (every 3 d) and bee homogenates (10 bees/pool).
3. **Stats** – Survival: coxph frailty; repeated-measure ANOVA for behaviour; GLMM (logit) for reproduction.
4. **Power** – to detect 20 % change (α = 0.05, β = 0.2) need ≈12 RFID-tagged foragers per colony, 6 colonies per treatment.

---

## 8. Key Confounders & Mitigation
• **Pathogen load (Nosema, DWV)** – Screen & equalise across colonies.
• **Nutrition quality** – Standardise pollen protein (25 ± 2 %).
• **Temperature** – Interaction with neonic metabolism (↑ at > 33 °C).
• **Solvent carriers** – Keep acetone < 0.03 % w/w in sucrose.

---

## 9. Contrarian / Emerging Topics (Flagged as Speculative)
1. **Microplastic co-exposure** – May alter gut permeability; consider adding microplastic (0.1 % w/w) factorial.
2. **Epigenetic priming** – Chronic 0.1 ppb imidacloprid in drones changes sperm DNA methylation; potential trans-generational endpoints.
3. **mRNA-based biopesticides** – dsRNA constructs show negligible bee toxicity up to µg levels; could be future control treatment.

---

## 10. Practical Dosing Examples
### 10.1 Chronic Dietary – Imidacloprid in *Apis mellifera*
| Group | Nominal ppb | µg bee⁻¹ d⁻¹ (assuming 30 mg nectar) |
|-------|-------------|---------------------------------------|
| Control | 0 | 0 |
| Low (Field-Median) | 0.5 | 0.015 |
| Medium (Field-High) | 5 | 0.15 |
| High (Hotspot) | 25 | 0.75 |
| Pos-Ctrl | 100 | 3.0 |

### 10.2 Acute Contact – λ-Cyhalothrin on *Bombus* workers
Apply 1 µL acetone droplet dorsal thorax:
0, 0.005, 0.02, 0.1 µg/bee.

---

## 11. Regulatory Alignment
• US-EPA Tier-1 recommends 1× estimated environmental concentration (EEC) + 10× – our scheme matches.
• OECD GD 245 (2023) solitary bee larval test – upper dose not to exceed 100 mg a.i. kg⁻¹ pollen; our 200 ppb fungicide = 0.2 mg kg⁻¹ → compliant.

---

## 12. Summary Checklist
✓ Select active ingredient & matrix (nectar/pollen/leaf).  
✓ Define 4–5 dose levels anchored to monitoring percentiles.  
✓ Convert ppb → ng bee⁻¹ d⁻¹ using consumption rates per species.  
✓ Confirm concentrations analytically.  
✓ Measure multi-level endpoints (lethal → molecular).  
✓ Control confounders (pathogens, carriers, nutrition).  
✓ Include positive control & potential mixture synergist.

Following this framework will yield ecologically relevant, statistically robust data to characterise pesticide risks to bees under both average and worst-case real-world exposures.

## Sources

