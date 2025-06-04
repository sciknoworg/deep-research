# Will the Atlantic Meridional Overturning Circulation (AMOC) Change Its Course?  
## A Comprehensive, Research-Level Synthesis (cut-off 2025-06)

---

### Executive Summary

1. **Consensus direction** – All lines of evidence (observations, process theory, CMIP-class GCMs, eddy-resolving models, and conceptual box models) agree that the AMOC is *already weakening* and will *continue to do so* for at least the next several decades under any plausible emissions pathway.  
2. **Magnitude & timing** – Best-estimate anthropogenic‐forcing projections range from a **15–40 % decline by 2100 under low–medium mitigation (SSP2-4.5) to 40–60 % under very high forcing (SSP5-8.5)**.  High-resolution (≤0.25° ocean) ensembles depict a *stronger present-day* AMOC but also a **steeper near-term (2015-2050) decline of 2–4 Sv**, dominated by a Florida Current slowdown.  
3. **Tipping risk** – Idealised hosing, multimodal stability diagnostics, and recently developed early-warning statistics converge on a **non-negligible probability (~15–35 %) of a sub-critical Hopf or saddle-node transition to a weak or collapsed state during 2035-2080**.  CMIP6 models reveal explicit hysteresis: ~½ recover after hosing, ~½ remain locked in a weak state, confirming model-dependent tipping thresholds.  
4. **Controls** – The **meridional density (mainly salinity) contrast between 48° N and ~34° S** explains >90 % of inter-model AMOC variance in ramp-up/ramp-down experiments; gyre exports, *not* salt–advection within the overturning, set the timing of both weakening and recovery.  
5. **Process resolution matters** – Mesoscale eddies *delay* tipping by raising the freshwater threshold for collapse, yet once the threshold is crossed they *amplify* coastal sea-level and storm-track impacts that low-resolution models miss.  
6. **Downstream impacts** – A 40–60 % AMOC weakening implies **+10–20 cm dynamic sea-level rise along European and eastern-North-American coasts**, a **1–3 °C cooling over western Europe**, altered storm tracks, and substantial freshwater/biogeochemical perturbations.  Rapid collapse shortens return periods of coastal sea-level extremes from decades to ≤1 yr.  
7. **Key uncertainties** – (i) Deep-water mixing parameterisations, (ii) realistic Antarctic Bottom Water (AABW) formation, (iii) Arctic freshwater export pathways, (iv) aerosol forcing history, and (v) eddy saturation/compensation physics still drive the widest spreads in projections.

---

## 1. Foundations: Mechanisms Governing AMOC Strength & Stability

| Mechanistic Class | Principal Scaling / Diagnostic | Key Research Learnings |
|-------------------|--------------------------------|-------------------------|
| **Diapycnal diffusivity (κᵥ)** | Ψ∝κᵥ^α (α≈0.4–0.7) while κᵥ≤10⁻⁵ m² s⁻¹ | Idealised two-basin GCMs show Atlantic & Pacific MOC magnitudes scale similarly with κᵥ up to O(10⁻⁵ m² s⁻¹); divergence emerges at higher κᵥ unless Gent-McWilliams mixing is included, but pycnocline depth retains identical κᵥ-sensitivity in both basins, decoupling depth-transport linkage. |
| **Southern-Ocean wind & eddies** | Unified scaling Ψ≈(τw/ρf)^{½}/κᵢ when isopycnal K dominates | Gnanadesikan’s cubic + Marshall–Radko energetics gives K_eddy∝√τw; eddy saturation leaves ACC volume transport nearly invariant to τw yet eddy kinetic energy (EKE) rises. Bottom drag controls residual overturning stratification and thus atmospheric CO₂. |
| **Freshwater transport indicators** | Mov (34° S) sign & transition probabilities | Corrected Mov places all CMIP5/6 models in a *multiple-equilibrium regime*; negative Mov and eddy-compensated salt budgets imply a latent collapsed state even without external hosing. |
| **Box-model bifurcation type** | Sub-critical Hopf vs saddle-node | FAMOUS-calibrated five-box model loses the ‘on’ state via a Hopf bifurcation, enabling *rate-induced* tipping even if forcing never crosses a static threshold. |
| **Eddy compensation** | Mesoscale fluxes neutralise low-res salt-advection | 0.1° POP run with 0.5 Sv meltwater retains basin-integrated freshwater import ~constant; low-res 1° counterpart does not—eddies raise the freshwater threshold for collapse. |

*Implication* – Any quantitative AMOC forecast must track (i) κᵥ, (ii) isopycnal/eddy diffusivity K, (iii) gyre-mediated meridional salinity contrasts, and (iv) Arctic freshwater export, all of which remain poorly constrained in CMIP-class models.

---

## 2. Observational Diagnostics & Historical Evolution

### 2.1 Direct arrays and hydrographic lines

* **RAPID-MOCHA (26.5 °N)** – 2004–2024 mean transport ≈17 Sv with a −0.1 to −0.18 Sv decade⁻¹ trend (CMIP5 historical spread); early-warning variance trends detect critical slowing.  
* **OSNAP & OVIDE (Subpolar N. Atlantic)** – 2014–21 data reveal a Nordic-Sea (50 °N-centred) deep-water mode controlling centennial trends, corroborating the Trend Mode versus AMO dichotomy. Anthropogenic CO₂ accumulation in the Iceland & Irminger basins accelerated by +61 % during high-NAO phases.  
* **79 °N and Denmark Strait** – Deep-strait temperature minima rose 0.24 °C since 1982; Greenland Sea Deep Water disappeared post-1997, intermediate Eurasian-Basin signatures growing. DSOW anomalies propagate 500 km in ~13 days—argues for denser mooring spacing.  
* **Fram Strait & Arctic budget** – Mandated export ≈2.3 Sv water, 0.1 Sv liquid freshwater, releasing ~10 TW to atmosphere; variability set by local SLP gradient and stratospheric vortex rather than NAO.

### 2.2 Sea-level fingerprints

* **Bay of Biscay altimetry (1993–2002)** – +3.09 ± 0.21 mm yr⁻¹, ~15 % linked to inverse barometer; dynamic component tied to AMOC weakening adds 10–20 cm when AMOC collapses in models.  
* **Eddy-permitting model experiments** – Rapid (sub-decadal) collapse cuts Gulf-Stream separation latitude, shortening return times of coastal storm-surge/SSH extremes from multi-decadal to ≤1 yr.

### 2.3 Early-warning statistics

• Rising variance & autocorrelation detected in multiple reconstructions imply a crossing of a critical threshold **~2050 ± 10 yr**, contradicting AR6’s “very unlikely” wording and suggesting policy-relevant lead times.

---

## 3. Coupled-Model Evidence: CMIP5, CMIP6 & High-ResMIP

### 3.1 Forced future scenarios (RCP/SSP)

| Forcing Pathway | Median 2100 AMOC Decline | Ensemble Spread | Notes |
|-----------------|--------------------------|-----------------|-------|
| SSP1-2.6 / RCP2.6 | 15–25 % | 10–35 % | ~22 % mean across 30 CMIP5 models |
| SSP2-4.5 / RCP4.5 | 25–40 % | 15–45 % | Stabilises mid-century, no full collapse |
| SSP5-8.5 / RCP8.5 | 40–60 % | 30–85 % | Two CMIP5 models yield slow shutdown |

*CMIP6 historical bias* – +10 % strengthening 1850–1985 due to aerosol forcing reproduction; undermines SSP5-8.5 projections because starting point differs.  

### 3.2 Resolution sensitivity

* **HighResMIP (0.25°)** – Present-day AMOC stronger by +2–4 Sv but 2015-2050 decline twice as steep (−2.5 Sv decade⁻¹); decline dominated by Florida Current weakening absent in 1° versions.  
* **1/12° eddy-resolving hindcast** – Exports freshwater southward across 34° S; basin resides in bistable regime consistent with negative Mov.  
* **Eddy saturation & κᵥ dependence** – At ≲1/10° grid spacing ∂Ψ/∂κᵥ ≫ ∂Ψ/∂τw, reversing coarse-model sensitivities and highlighting the importance of vertical mixing schemes.

### 3.3 Freshwater-hosing experiment synthesis (NAHosMIP)

| Hosing Protocol | Models | Outcome During Hosing | Post-Hose Fate |
|-----------------|--------|-----------------------|---------------|
| +0.1 Sv uniform NA, 100 yr | 9 CMIP6 | Collapse in all | 4 recover to ≥18 Sv; 5 remain ≤10 Sv (≥40 % weaker) |
| +0.2 Sv uniform NA, 50 yr | Same | Collapse in all | 5 recover, 4 stalled; dynamic SLR +10–20 cm Europe |
| +0.1 Sv Greenland-centred | Same | Collapse faster | Similar bifurcation |

*Feedback attribution* – Models that recover exhibit positive salt-advection feedback and gyre-mediated salinity export; stalled models retain high-latitude freshwater cap & suppressed convection.

---

## 4. Stability Theory, Multiple Equilibria & Tipping Thresholds

1. **Mov indicator** – Negative Mov at 34° S in all analysed CMIP5/6 members → theoretically places system in bi-stable regime.  High-resolution CESM run flips from mono- to multi-stable under RCP8.5 once salt bias corrected.  
2. **Sub-critical Hopf** – Box-model analysis shows oscillatory precursors (decadal variability surge) prior to collapse; offers observational early-warning metric.  
3. **Rate-induced tipping** – Finite forcing rate, not just amplitude, can trigger collapse; relevant for rapid meltwater pulses from Greenland.  
4. **Eddy-compensated salt budget** – Mesoscale fluxes can mask freshwater-forced approach to tipping in standard volume-flux monitoring; alternative density-contrast metrics required.  
5. **Gyre control** – Meridional salinity gradient (48 °N−34 °S) explains >90 % variance across four CMIP5/6 models in CO₂ ramp-up/down; asynchronous gyre exports lead to overshoot, stagnation, or continued decline independent of overturning salt-advection.

---

## 5. Downstream & Socio-economic Impacts of AMOC Weakening / Collapse

### 5.1 Climate & hydrology

| Impact Zone | Moderate Weakening (40 %) | Collapse (>80 %) |
|-------------|---------------------------|------------------|
| Western Europe SAT | –1 °C winter cooling; slightly fewer heatwaves | –3 °C annual mean; winter cold spells akin to 1960s |
| Summer NAO pattern | Weak negative | Strong negative → −20 % June–Aug rainfall in Scandinavia, +15 % in Iberia |
| Peak river flow | Up to −30 % in Rhine, Elbe, Thames | >−40 % central/northern Europe |
| Crop productivity | −3–7 % cereals in NW Europe | −10–15 % plus frost damage |

### 5.2 Sea-level rise & extremes

* **Dynamic component** – +10–20 cm along European Atlantic coasts; 5–15 cm along U.S. east coast.  
* **Return times** – High-resolution hosing cuts extreme SSH return period from decades to sub-annual; coastal-protection design criteria must accommodate order-of-magnitude shift.  

### 5.3 Marine ecosystems & biogeochemistry

* Pacific-overturning rerouting (in a minority of parameter spaces) worsens deep-Pacific oxygen deficits and adds +20 ppm atmospheric CO₂ pulse via reduced Antarctic carbon sequestration.  
* North Atlantic productivity declines due to stratification & reduced nutrient import; mixed-layer deoxygenation coupled with cooling stresses cod & haddock nurseries.  

---

## 6. Critical Uncertainties & Research Frontiers (2025–2035)

1. **Vertical mixing parameterisations** – Richardson-number & TKE schemes improve overflow representation (Romanche FZ, DSOW), but interior κᵥ uncertainty (>×3 range) remains the dominant source of overturning spread.  
2. **Eddy parameterisations vs explicit eddies** – Hybrid-eddy energetics (Marshall–Radko) needed in CMIP7; constant K fails under variable τw.  
3. **Arctic gateways & freshwater sources** – Fram-Strait export variability drivers (SLP gradient, vortex) not NAO; improved observation networks & data-assimilating models required.  
4. **Aerosol forcing history** – CMIP6 aerosol–cloud interactions produced spurious 19th–20th-century AMOC strength; re-calibration essential to align hindcasts.  
5. **Coupled ice-sheet–climate feedbacks** – Rapid Greenland/Antarctic melt pulses can rate-induce tipping; interactive ice modules necessary.  
6. **Early-warning metrics operationalisation** – Combine variance, autocorrelation, meridional density contrast, and DSOW property tracking into decadal outlook products for policymakers.

---

## 7. Decision-Relevant Storylines

### 7.1 Mitigation-Success (SSP1-2.6)

AMOC weakens ~20 %, stabilises after 2060; no collapse. Coastal SLR driven mainly by steric & ice mass components. Adaptation focus remains on ~0.5 m global-mean rise.

### 7.2 Delayed-Action (SSP2-4.5)

Weakening 25–40 %; early-warning indicators approach critical threshold ~2080 but not crossed. Dynamic SLR +12 cm EU coast; moderate European cooling offsets some heatwave impacts, yet hydrological shifts affect agriculture.

### 7.3 Fossil-Fuel Continuation (SSP5-8.5)

Weakening 40–60 %; tipping probability 25–35 %. If collapse: +20 cm dynamic SLR, −3 °C western-Europe mean cooling, acute storm-track changes, and decadal oxygen loss. Requires robust adaptive pathways: edifices, agriculture, and energy demand all shift.

---

## 8. Recommendations for Modellers, Observers & Policymakers

1. **Accelerate high-resolution coupled modelling** – At <0.25° provide credible Gulf-Stream separation, Florida Current, and eddy compensation physics; essential for dynamic SLR and extreme-event risk estimation.  
2. **Deploy fine-spacing mooring arrays** – 180–320 km spacing plus sub-daily sampling along Denmark-Strait/Irminger route to track DSOW and variance growth precursors.  
3. **Integrate early-warning dashboard** – Combine RAPID transport anomalies, 48 N–34 S density gradient, NAO-adjusted hydrographic trends, and variance diagnostics.  
4. **Embed AMOC in coastal-flood standards** – Incorporate a +20 cm dynamic SLR contingency into European & U.S. east-coast planning horizons (2050–2100).  
5. **Treat North Atlantic Hosing as a realistic policy stress test** – Apply +0.1 Sv Greenland-melt pulses in CMIP7 ScenarioMIP to bracket abrupt-change damages.

---

### Concluding Perspective

The long-standing textbook view—“an AMOC collapse this century is very unlikely”—is no longer defensible. Improved observations, higher-resolution models, and refined stability theory now paint a *non-trivial* risk of an abrupt transition within the current century, particularly under high-emission pathways or rapid Greenland-ice loss. Given the disproportionate socio-economic consequences concentrated in regions with dense infrastructure and historical climate stability, prudence dictates incorporating AMOC tipping contingencies into both mitigation cost–benefit analyses and near-term adaptation planning.

> **Practical bottom line**: Even if global mean temperature targets are met, unmitigated freshwater forcing from the cryosphere can still push the AMOC across a tipping threshold. Vigilant monitoring, process-explicit modelling, and policy designs that are robust to a 20 cm dynamic sea-level surge and a 1–3 °C European cooling must be pursued starting now.


## Sources

- http://www.ocean-sci.net/10/881/2014/
- https://hal.science/hal-00872044/document
- http://hdl.handle.net/2078.1/119081
- https://hal.science/hal-00267648
- http://web.science.unsw.edu.au/%7Ematthew/AMOC_Sijp_et_al_2014.pdf
- https://dspace.library.uu.nl/handle/1874/409138
- https://orcid.org/0000-0002-2326-619X
- https://hal.science/hal-03008090/document
- https://doaj.org/toc/1991-9603
- https://zenodo.org/record/28293
- https://mural.maynoothuniversity.ie/17729/1/mccarthy-caesar-2023-can-we-trust-projections-of-amoc-weakening-based-on-climate-models-that-cannot-reproduce-the-past.pdf
- https://doaj.org/article/8b74ce5a5c8441f78474dc0b3e65bb46
- http://hdl.handle.net/10068/942094
- https://zenodo.org/record/27932
- https://doi.pangaea.de/10.1594/PANGAEA.864251
- https://hal.archives-ouvertes.fr/hal-02892492
- http://hdl.handle.net/1721.1/71728
- http://hdl.handle.net/11858/00-001M-0000-0011-FB5D-D
- http://dx.doi.org/10.1029/2012GL053763
- https://dspace.library.uu.nl/handle/1874/349359
- https://research.vu.nl/en/publications/170c6063-8dac-464c-a5fa-ed7d220dc022
- https://dspace.library.uu.nl/handle/1874/409300
- http://www.vliz.be/imisdocs/publications/262922.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1463500313000437/MAIN/application/pdf/f846324d98ac97e3700673a0ae9c3e03/main.pdf
- https://hal.science/hal-01248244
- https://dspace.library.uu.nl/handle/1874/411234
- http://hdl.handle.net/10.1371/journal.pone.0214535.g003
- http://hdl.handle.net/11585/131792
- https://doaj.org/article/e297211b6ef249679bdea0e6e5fa2a2a
- https://escholarship.org/uc/item/14v523qn
- https://doaj.org/article/ff6b5e54206241db8be8af214144dc7e
- https://hal.science/hal-00836152
- www.duo.uio.no:10852/79797
- http://www.dhigroup.com/upload/publications/mikeshe/Butts_Improving_streamflow_simulations.pdf
- https://hal.archives-ouvertes.fr/hal-00853304
- http://www.loc.gov/mods/v3
- https://zenodo.org/record/8163448
- https://orcid.org/0000-0001-9230-3591
- https://escholarship.org/uc/item/7598h6tn
- https://doi.pangaea.de/10.1594/PANGAEA.942176
- https://hal.science/hal-02869856/document
- https://hal.sorbonne-universite.fr/hal-01449390/document
- http://web.maths.unsw.edu.au/~matthew/treguier_et_al.pdf
- https://hal.archives-ouvertes.fr/hal-03279860
- https://mural.maynoothuniversity.ie/15845/1/GerardMccarthyEff2022.pdf
- https://orcid.org/0000-0002-9111-7700
- https://hdl.handle.net/
- http://hdl.handle.net/1721.1/52347
- http://hdl.handle.net/2078.1/35529
- https://insu.hal.science/insu-03683236/document
- https://hal.science/hal-02892492/file/gmd-9-3993-2016.pdf
- https://zenodo.org/record/7225014
- http://www.vliz.be/nl/open-marien-archief?module=ref&refid=238450
- https://hal.archives-ouvertes.fr/hal-00770689
- http://hdl.handle.net/10871/36797
- http://www.scopus.com/home.url)
- http://web.science.unsw.edu.au/%7Ematthew/os-3-491-2007.pdf
- http://hdl.handle.net/10261/264557
- http://hdl.handle.net/1957/27668
- https://doaj.org/article/c27ec664258747bea1ba08d9c7aef227
- https://doi.org/10.17615/azt7-gs05
- http://hdl.handle.net/2078.1/39374
- https://hal.science/hal-03093315
- http://hdl.handle.net/20.500.11897/419756
- https://escholarship.org/uc/item/3ww7v7s2
- http://hdl.handle.net/11858/00-001M-0000-002D-CF17-0
- https://hal.archives-ouvertes.fr/hal-03008090
- http://hdl.handle.net/10068/256386
- https://orcid.org/0000-0001-5298-5233
- http://hdl.handle.net/20.500.11897/390640
- https://hal.archives-ouvertes.fr/hal-00690812
- http://hdl.handle.net/11858/00-001M-0000-0011-F546-4
- http://hdl.handle.net/20.500.11897/408842
- https://centaur.reading.ac.uk/103346/8/fmars-09-830821.pdf
- https://zenodo.org/record/8320904
- http://handle.unsw.edu.au/1959.4/unsworks_35002
- https://archimer.ifremer.fr/doc/00746/85806/90953.jpg
- http://www.vliz.be/nl/open-marien-archief?module=ref&refid=217394
- https://hal.science/hal-00783515
- http://rams.atmos.colostate.edu/cotton/vita/106.pdf
- https://zenodo.org/record/8163529
- http://hdl.handle.net/10379/11548
- http://www.biogeosciences.net/5/1373/2008/bg-5-1373-2008.pdf
- https://hal.archives-ouvertes.fr/hal-00297986
- https://orcid.org/0000-0001-8579-6068
- http://hdl.handle.net/10138/167236
- https://doi.pangaea.de/10.1594/PANGAEA.942034
- https://dspace.library.uu.nl/handle/1874/275523
- http://www.elic.ucl.ac.be/modx/users/thierry/articles/2005_Renssen_et_al_GRL.pdf
- http://hdl.handle.net/11858/00-001M-0000-000E-ACEF-E
- https://zenodo.org/record/7509968
- https://hal.science/hal-03869321
- http://eprints.soton.ac.uk/255/1/KLINGER_.MARTOZKE_JPO__S_2001.pdf
- http://hycom.org/attachments/067_diapycnal.pdf
- https://doi.pangaea.de/10.1594/PANGAEA.942047
- http://edoc.mpg.de/249275
- http://www.vliz.be/imisdocs/publications/90/309590.pdf
- https://mural.maynoothuniversity.ie/12060/1/GM_Atlantic.pdf
- https://centaur.reading.ac.uk/91960/2/2019MS002014.pdf
- https://hal.science/hal-00331133/file/osd-4-653-2007.pdf
- https://research.vu.nl/en/publications/955346d2-0a91-4390-b2d3-84eb45512132
- https://dspace.library.uu.nl/handle/1874/394430
- http://hdl.handle.net/20.500.11897/214825
- https://doi.org/10.1016/j.pocean.2011.10.002
- https://media.suub.uni-bremen.de/handle/elib/1267
- https://doaj.org/article/3a840b292a25436d94cfc021fa87c44d
- https://hdl.handle.net/1956/17028
- https://research.vu.nl/en/publications/23819acf-602d-4819-8a62-f3e866c28812
- https://doi.pangaea.de/10.1594/PANGAEA.942057
- https://zenodo.org/record/8005600
- https://doi.pangaea.de/10.1594/PANGAEA.942046
- https://doaj.org/toc/2190-4987
- http://hdl.handle.net/1721.1/70089
- https://digitalcommons.uri.edu/oce_facpubs/515