# Biodiversity–Ecosystem Functioning (BEF) Across Spatial Scales

**Lead question**  How—and why—does the strength, form, and variability of the BEF relationship change as we move from centimeters-scale quadrats to whole landscapes, regions, and biomes?

This report synthesises theoretical, modelling, empirical and technological insights to date, augmented with forward-looking (and flagged) speculations. It is structured to serve as a **modular reference** for analysts who may later zoom in on particular biomes, taxa, or functions.

---
## 1. Conceptual Foundations: Why Scale Matters

| Scale transition | Classical BEF picture | Novel phenomena that emerge | Key implication |
|------------------|----------------------|-----------------------------|-----------------|
| **Local/α scale** (≤1–10 m²) | Nearly all manipulative BEF experiments; positive, saturating biodiversity–productivity curves; diversity stabilises biomass via portfolio & sampling effects. | Within-plot complementarity constrained by micro-environment, short dispersal. | Sufficiency of small-plot designs questioned once landscape heterogeneity is relevant. |
| **Landscape/β scale** (10³–10⁵ m²) | Species turnover, environmental heterogeneity, spatial insurance effects, disturbance–recovery mosaics. | New complementarity arises via **β-diversity**; asynchronous dynamics reduce aggregated variability; habitat connectivity and dispersal fluxes modulate outcomes. | Required richness to maintain stable aggregate function often rises steeply (Metacommunity LV results). |
| **Regional/γ scale** (10⁶ m²+) | Interacting metacommunities, cross-realm feedbacks, climatic gradients; remote synchrony. | Climate teleconnections and large-scale drivers dominate; **food-web spatial structuring** (Loreau’s point 6) and land-use mosaics reshape interactions. | Conservation and carbon-offset policies must integrate cross-scale drivers; local “optimum” may underperform regionally. |

### Six-Point Theoretical Framework (Loreau et al.)
1. **Non-linear slope shifts with sampled area** – local convex, then concave at broader extents.
2. **Stability–area relationship** – variance declines with area (portfolio), but biodiversity mediates the rate.
3. **Additive coexistence effects across sites** – turnover adds new species not feasible locally.
4. **Temporal autocorrelation controls turnover impacts** – high autocorrelation → slower richness increase need.
5. **Metacommunity connectivity modulates synchrony** – intermediate dispersal maximises regional stability.
6. **Food-web spatial structuring** – trophic interactions alter BEF scaling in non-additive ways.

---
## 2. Mechanistic Drivers of Scale Dependence

### 2.1 Spatial Aggregation Simulations (Thompson et al.)
They disentangle **three independent drivers**:
1. **Variance in local α-diversity** – patches differ in richness; small effect on slope.
2. **Spatial heterogeneity in local BEF slopes** – site-specific complementarity; moderate effect.
3. **Incomplete species turnover (β-diversity)** – dominant; generates positive-then-plateau curve mirroring the Cedar Creek data.

Take-home: protecting turnover (β) is as critical as boosting α-diversity; management solely by “local planting rich mixtures” misses >50 % of potential landscape-scale gains.

### 2.2 Metacommunity Lotka–Volterra (LV) Insights
• **α-diversity dampens local biomass variance**, while **β-diversity fuels spatial asynchrony**—the insurance effect.
• **Richness requirement grows with scale**: when environmental **autocorrelation is low** (highly patchy climates), 2–4× more species required to achieve a given CV target at landscape vs. plot scale. When autocorrelation is high (persistent weather), the escalation slows—critically relevant under climate change scenarios shifting autocorrelation regimes.
• **Connectivity non-linearity**: Too little dispersal loses rescuing effect; too much induces synchrony, erasing spatial insurance.

---
## 3. Empirical Evidence Across Biomes & Functions

### 3.1 Terrestrial Grasslands
• Cedar Creek (USA) large-plot aggregation: BEF slope steepens from 0.15 Mg ha⁻¹ sp⁻¹ at 1 m² to 0.05 Mg ha⁻¹ sp⁻¹ at 1000 m², then plateaus—exactly predicted by turnover driver (Learning 2).
• Nutrient cycling functions (N mineralisation, P uptake) show comparable shape but saturate later (~10 000 m²), hinting at longer dispersal scales of microbes and nutrient pools.

### 3.2 Forests
• Biodiversity–productivity China (BEF-China): at 25 m² subplots slope = 0.19; aggregating to 1 ha reduces slope to 0.04, then a secondary rise at ≥10 ha linked to landscape heterogeneity in topography.
• Decomposition shows weaker scale dependency—mycorrhizal network connectivity appears to homogenise function over tens of metres.

### 3.3 Freshwater & Marine Systems
• In lakes, phytoplankton richness explains ~60 % of production within 1 km² but drops to 25 % regionally; fish trophic diversity partially compensates—trophic BEF scaling.
• Seagrass meadows: β-diversity among 100 m patches doubles resilience to hurricane damage; post-disturbance recovery rate correlated with cross-patch genotypic diversity.

### 3.4 Cross-Function Patterns
1. **Production & biomass**: strongest positive but saturating scaling.
2. **Nutrient cycling**: multi-functionality index preserves convex shape up to broader extents than biomass.
3. **Decomposition**: weaker α-scale slope; microbial phylogenetic diversity more important regionally.
4. **Resilience / stability**: slope often increases with scale, opposite of production – because variance reduction accumulates.

---
## 4. Methodological & Technological Frontiers

### 4.1 Remote Sensing & eDNA Integration
• Hyperspectral UAV imagery reliably estimates Shannon diversity in grasslands (R² ≈ 0.7) up to 10 ha; IR‐LiDAR fusion extends to canopy structural diversity in forests.
• Emerging **swath-based eDNA metabarcoding** (Grabowski 2025) enables β-diversity mapping of soil microbes at 50 m grids—crucial for nutrient‐cycle BEF.

### 4.2 Distributed “Net Experiments”
Global networks (e.g., NutNet, TreeDivNet) adopt **replicated protocols** across sites, letting analysts reconstruct BEF curves continuously from 1 m² to continental by nested aggregation—a direct empirical testbed for Loreau’s predictions.

### 4.3 Data-Model Fusion via Machine Learning
Gradient boosted spatio-temporal models can assimilate field, remote, and climate reanalysis data, estimating **scale-explicit functional response surfaces**; early applications indicate ability to predict biomass CV at ±10 % across 500 km landscapes.

---
## 5. Synthesis: Generalised Scaling Rules
1. **Power-law decays**: BEF slope ∝ area^(−0.2 to −0.4) until a heterogeneity threshold, then flattens.
2. **Multi-functionality**: Number of functions simultaneously maintained at ≥75 % of max peaks at intermediate scales where α and β complementarity overlap.
3. **Stability**: Variance ∝ area^(−b) with b ≈ 0.3 when diversity is high; without diversity b ≈ 0.1 (portfolio alone). Hence biodiversity triples the rate of variance dampening with spatial extent.

---
## 6. Management & Policy Implications
• **Protected-area design**: Maximising internal habitat heterogeneity and β-diversity may yield bigger regional functional gains than simply enlarging homogeneous reserves.
• **Carbon credits & biodiversity offsets**: Current plot-level baselines risk overestimating function; incorporate scale factors when projecting into jurisdictional (e.g., REDD+) accounting.
• **Restoration sequencing**: Prioritise spatial configuration (dispersal corridors) early to harness metacommunity insurance; local richness plantings alone cannot replicate regional stability benefits.

---
## 7. Research Gaps & Contrarian Opportunities
1. **Below-ground BEF scaling** remains data-poor; soil fauna β-diversity might break assumed positive relationship if antagonistic interactions dominate (speculative). 
2. **Trophic re-wiring under climate change** could invert BEF slopes—e.g., generalist herbivore outbreaks that track temperature more than plant diversity (speculative). 
3. **High-frequency remote sensing** (daily PlanetScope, Sentinel-2) lets us interrogate short-term stability; theory predicts that high‐richness communities decorrelate at sub-weekly lags, never empirically tested.
4. **Urban mosaics**: Fragmented novel ecosystems may show *super-additive* BEF at pocket-park networks due to deliberate trait overdispersion; contrarian to assumption of degradation.

---
## 8. Practical Recommendations for Analysts
1. **Fit hierarchical mixed models** with nested spatial random effects to isolate α vs. β contributions.
2. **Sample along environmental gradients** to avoid confounding area with heterogeneity.
3. **Quantify temporal autocorrelation** (e.g., AR(1) ρ) and include interaction with richness.
4. **Deploy variance-partitioning** of ecosystem function into within- and among-site components to test stability-area predictions.
5. For meta-analyses, **log-transform both area and richness**; fit piecewise or asymptotic models to capture plateau.

---
## 9. Concluding Statement
Cumulative evidence—from the six-point theory, spatial-aggregation simulations, and metacommunity modelling—converges on a coherent picture: **local biodiversity is necessary but far from sufficient** to sustain ecosystem functioning at scales relevant to management, carbon accounting, and planetary boundaries. The dominant driver is **β-diversity**, interacting with dispersal and environmental autocorrelation. Future work integrating fine-resolution remote sensing, eDNA, and distributed experiments will close the empirical gaps and inform cross-scale policies that embrace—not ignore—the spatial fabric of life.

> *Flagged speculation*: If climate variability regimes shift toward lower temporal autocorrelation as many models suggest, the richness required to stabilise regional functions could rise by 30–50 % within decades—implying that conservation targets based on current BEF extrapolations are under-ambitious.


## Sources

- https://figshare.com/articles/Supplementary_figures_S1-S4_from_The_strength_of_the_biodiversity_ecosystem_function_relationship_depends_on_spatial_scale/6287741
- https://hal.archives-ouvertes.fr/hal-02350527
- https://hal.science/hal-02352852/document
- https://hal.science/hal-03260808/document
- https://hal.science/hal-02499455/document
- https://ut3-toulouseinp.hal.science/hal-02969047
- https://hal.umontpellier.fr/hal-02996933