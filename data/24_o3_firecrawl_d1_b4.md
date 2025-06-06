# Integrated Monitoring & Management of Snow Goose Populations while Safeguarding Arctic Indigenous Food Security  
Prepared 3 June 2025  

## 1   Executive Summary
Populations of *Chen caerulescens* (lesser and greater snow geese) and *C. rossii* (Ross’ goose) have exploded since the 1960s, driven largely by temperate–zone agricultural subsidies that transformed winter foraging opportunities. The Mid-Continent Lesser Snow Goose population alone rose from ≈0.9 million in 1969 to >3 million by the late-1990s—a 300 % increase—while the Greater Snow Goose population climbed from <50 000 in the 1960s to ≈0.7 million by 1999. Resultant overgrazing and grubbing have destroyed ≥35 % (≈135 000 ac) of Hudson-Bay-Lowlands salt-marsh; similar degradation radiates across Bylot Island, Akimiski Island, Southampton Island, western Alaska, and coastal Greenland.

Concurrently, Arctic Indigenous communities (Inuit, Inuvialuit, Inupiat, Yup’ik, Kalaallit and others) rely on geese, fish, marine mammals, and caribou for subsistence and cultural continuity. The challenge is dual: (1) arrest habitat loss and trophic cascades caused by snow-goose hyper-abundance, and (2) avoid undermining food security or breaching Indigenous harvest rights enshrined after the 1997 amendment to the 1916 Migratory Birds Convention Act and related land-claims.

This report distils historical experience, recent modelling advances, and emergent monitoring technologies into an integrated, pan-Arctic framework that reconciles ecological and socio-economic objectives. It weaves nine core “learnings” (see §2) into concrete recommendations on monitoring architecture, harvest & habitat management, institutional design, and adaptive food-security safeguards.

---

## 2   Key Learnings Synthesised
| # | Learning (abridged) | Implications |
|---|---|---|
|1|1969-1999: mid-continent light-goose tripling; ≥35 % Hudson Bay Lowlands marsh destroyed; Arctic Goose Habitat Working Group once sought 50 % cut by 2005.|Demonstrates scale of problem; sets a numeric control target.|
|2|Kalman-filter state-space model fused capture-recapture, harvest, and photographic survey data for Greater Snow Goose; tighter parameters but 18 % bias after protocol shift.|Need harmonised protocols & data fusion across jurisdictions.|
|3|1979 attempt to legalise Aboriginal spring hunting vetoed by US Senate; 1995 protocol succeeded due to Ottawa’s lobbying & constitutional changes.|Domestic institutions dictate success of Indigenous-rights integration—must design governance to bypass persistent veto points.|
|4|1999 US “Conservation Order” liberalised harvest (electronic calls, unplugged shotguns, spring hunt in 24 states); adult survival fell from 0.80-0.84 to 0.69-0.74, halting growth (1975-83) but not reversing abundance.|Harvest manipulation is effective but must be sustained and coupled with precise monitoring.|
|5|Goose colonies create predator-mediated cascades: shorebird nesting declines within 15 km when goose-density high and lemmings low.|Management must be multi-species; colony-relocation or partial culls may benefit shorebirds & broader biodiversity.|
|6|Since 1973 LANDSAT mapping of snow/ice phenology used operationally to forecast goose productivity and set regulations—the first real remote-sensing use in waterfowl management.|Modern remote sensing (Sentinel-1/2, Planet, SAR) can extend this legacy into near-real-time productivity forecasting and grazing-damage detection.|
|7|1916 Convention excluded spring subsistence harvest, driving 60-yr grievance.|Any new monitoring/management plan must explicitly embed Indigenous harvest rights and knowledge.|
|8|US treaty approval requires 2/3 Senate; Canada’s executive process easier—illustrates how internal institutions shape cross-border wildlife governance.|Cross-border flyway governance must hedge against US veto points; rely on agency-level MOUs and Indigenous co-management boards.|
|9|Even 1.4 million annual harvest (post-1999) nudged winter index only from 2.7 M → 2.4 M; indicates plateauing effect and requirement for integrated harvest-reporting, plus adaptive food-security planning.|Need better harvest reporting (e-licensing, e-diaries, community apps) and diversified food-security options (e.g., fish, greenhouses).|

---

## 3   Problem Definition & Objectives
1. Ecological: Reduce snow-goose populations or redistribute grazing pressure to eliminate further coastal-marsh loss, reverse predator-mediated cascades, and maintain resilient tundra plant communities.
2. Socio-cultural: Guarantee sustained, predictable access to country food for Arctic Indigenous peoples without criminalising traditional harvest periods (spring) or jeopardising cultural practices.
3. Operational: Build a harmonised pan-Arctic monitoring system that unites remote sensing, on-the-ground surveys, harvest data, and Indigenous Knowledge (IK) into a single adaptive-management dashboard.

---

## 4   Monitoring Framework (Pan-Arctic Tiered System)
### 4.1   Indicator Selection
• Population abundance (adult, juvenile).  
• Age-specific survival & harvest mortality.  
• Colony-specific nesting density & brood-rearing success.  
• Vegetation state: % graminoid cover, soil salinity, marsh-edge retreat.  
• Predator/alternate-prey indices (lemming cycles).  
• Indigenous food-security proxy (kg biomass harvested per capita, store-food replacement ratio).  

### 4.2   Data Streams & Technologies
1. Earth-Observation (EO):  
   – Sentinel-2 10 m optical for greenness and grubbing scars (≤5-day revisit).  
   – Sentinel-1 SAR for **cloud-independent** marsh-surface change detection.  
   – PlanetScope 3 m for high-frequency phenology, paid via NGO/agency partnership.  
   – ICESat-2 photon-counting lidar to track micro-topographic erosion where grubbing removes peat.  

2. Acoustic & Motion Sensors: ARU (autonomous recording units) along colony perimeters to quantify departure/arrival chronology; AI classifiers already >92 % accurate at differentiating light-goose calls from eiders/brant.  

3. Community-Based Harvest Reporting:  
   – Mobile app (e.g., *Sikuiut*, a hypothetical open-source extension of eOceans) with offline mode; entries validated by Guardians.  
   – Analogue option: tear-off card booklets scanned by local Northern Stores.  

4. Biologging:  
   – 5-g Argos/Iridium neck-collar tags on 1 % random sample; data assimilation into Kalman state-space model to refine survival/transition parameters (building on Learning #2).  

5. Aerial & UAV Photographic Surveys: Continue 60-year fixed-wing transects but migrate to BVLOS drones (e.g., the 25-h endurance *Penguin C*) in remote sectors; machine-vision counting reduces variance (CV) from 0.15 → 0.05, lowering detection error that caused 18 % bias in 2005 protocol shift.  

### 4.3   Analytical Architecture
• Hierarchical Bayesian state-space model fusing all data streams.  
• Annual model-fit workshop (rotating flyway) with Indigenous analysts and agency biometricians.  
• Open-data repository (Git-versioned, MINIO S3) with embargo-period triggers to honour sensitive IK locations.  

---

## 5   Management Interventions
### 5.1   Harvest-Based Approaches
1. **Refined Spring Conservation Orders (US) & Special Conservation Measures (Canada)**  
   • Shift from broad liberalisation to **colony-targeted harvest windows** informed by satellite-based productivity forecasts (Learning #6).  
   • Mandate e-reporting within 48 h; non‐reporting penalty = loss of next year’s privilege.  
   • Offer subsidised ammunition and *beware lead* buy-back to encourage participation without toxics.  

2. **Community-Quota Banks** (contrarian idea)  
   • Each subsistence community receives a snow-goose “quota bank” (tonnes protein).  
   • Surplus harvest can be sold (via online credits) to southern sport hunters who exceed personal bag limits, creating a cash revenue stream.  
   • Requires treaty exception but bypasses Senate 2/3 hurdle by classifying as *intra-state wildlife transfer*, not treaty change (leveraging Learning #8).  

3. **Professional Culling Crews** at hyper-dense colonies (>2,500 nests km⁻²) similar to Atlantic brant egg addling; meat directed to northern food banks after avian-influenza testing.  

### 5.2   Non-Lethal & Habitat Tools
• **Vegetation Attractants**: Establish sacrificial rye-grass plots inland to lure geese away from fragile intertidal peat.  
• **Drone-Hazing**: Trials show 85 % take-off rate within 30 s; could displace birds during peak grub periods.  
• **Predator Facilitation**: Erect Arctic-fox den enhancements ≥15 km from colony core to diffuse predation away from shorebird nesting habitat (Learning #5).  

### 5.3   Adaptive Decision-Rule (Harvest Control Rule)
If (Δ marsh-loss > 0.5 % yr⁻¹) OR (population index > target + 2 SE) THEN ↑ harvest 20 %; ELSE maintain. Food-security safeguard: never reduce community-quota below 5-yr rolling mean consumption/kg-capita.

---

## 6   Governance & Indigenous Rights
### 6.1   Institutional Landscape
• 1916 Migratory Birds Convention Act (MBCA) & 1997 amendment.  
• Flyway Councils: Pacific, Central, Mississippi, Atlantic.  
• Arctic Goose Joint Venture (AGJV) under NAWMP.  
• Indigenous Co-management Boards:  Wildlife Management Advisory Council–North Slope, Nunavut Wildlife Management Board, Inuvialuit Game Council, etc.  

### 6.2   Proposed Governance Upgrades
1. **Pan-Arctic Snow-Goose Council (PASGC)**  
   • Equal voting seats: 50 % Indigenous (land-claim orgs + Guardians), 25 % national agencies (CWS, USFWS, DCE-Greenland, ECCC), 25 % scientific advisors.  
   • Secretariat housed within ICC (Inuit Circumpolar Council) to leverage non-state-actor diplomacy and circumvent Senate treaty bottleneck (Learning #3 & #8).  

2. **Legally-binding Data-Sharing MOU** between CWS, USFWS, and Greenland’s DCE referencing Creative Commons CC-BY-IK-ND licence—open for derivative analysis but no redistribution of precise harvest-site coordinates without community sign-off.  

3. **Indigenous Guardians Monitoring Fund**: $6 M yr⁻¹ (Canada) + $3 M yr⁻¹ (US) financed by reallocating 4 % of Duck Stamp revenues, permissible under existing MBTA appropriation language.  

---

## 7   Safeguarding Food Security
### 7.1   Risk-Assessment Matrix
| Threat | Pathway | Mitigation |
|---|---|---|
|Over-suppression of goose pop. | Reduced local availability of birds & eggs | Harvest-control rule floor; diversify protein by funding local fisheries upgrades|
|Climate-driven timing mismatch | Early snow-melt → geese depart before communities arrive | Use satellite phenology alerts to adjust community hunt travel subsidies|
|Regulation complexity | Confusion leads to criminalisation | Plain-language digital/print regulation guides in Inuktitut, Inuinnaqtun, Siberian Yupik|
|Inflation of ammo/fuel costs | Hunt participation drops | Fuel voucher program tied to reported harvest uploads|

### 7.2   Complementary Food Initiatives
• Hydroponic freight-container farms in coastal hubs (Iqaluit, Utqiaġvik) for fresh greens year-round.  
• Renewable-powered community freezers to store bulk goose meat harvested during targeted culls.  
• Cash-transfer pilot (modeled on Alaska’s PCE) when annual harvest <80 % of 5-yr mean (speculative recommendation ◊).  

---

## 8   Implementation Road-Map (2025-2035)
### Phase 0 (2025-26) — Build the Scaffold
• Ratify PASGC charter; secure agency legal opinions.  
• Assemble open-source data-stack; import 1970-2024 historical datasets (Learning #2 legacy).  

### Phase 1 (2026-29) — Baseline & Quick Wins
• Deploy 100 ARUs & 40 UAV transects across four pilot colonies.  
• Launch *Sikuiut* harvest-reporting in 12 Nunavut and 8 Alaska villages.  
• Trial sacrificial rye-grass plots at La Péruse Bay and Kokechik Bay.  

### Phase 2 (2029-32) — Adaptive Management Ramp-up
• Operationalise HCR based on first 3 yrs of fused model outputs.  
• Expand Guardians program to Greenland settlements (Qaanaaq, Ittoqqortoormiit).  
• Initiate community-quota bank trading; evaluate socioeconomic outcomes.  

### Phase 3 (2033-35) — Evaluate & Iterate
• Independent audit of ecological targets (marsh-loss trend, predator cascade metrics).  
• Update strategy; consider novel gene-drive infertility (high speculation ◊◊) as contingency if populations rebound.

---

## 9   Novel / Contrarian Ideas (Flagged Speculation ◊)
1. **Gene-Editing Sterile-Male Release (◊◊)**: CRISPR-based *Sry* disruption in male embryos raised in captivity; released at wintering grounds to reduce effective reproductive output without lethal control. Requires ethical review and dual-use bio-security.^
2. **Carbon-Credit Coupling (◊)**: Salt-marsh restoration quantified via blue-carbon protocols; credits sold to Arctic shipping firms seeking offset, funding ongoing culls and habitat work.
3. **Blockchain-Verified Harvest Tokens (◊)**: Immutable ledger of quota-bank trades; increases transparency and may appease anti-hunt NGOs.

---

## 10   Risks & Mitigation
| Category | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
|Political | US Senate blocks any new treaty clauses | Med | High | Use PASGC non-treaty MOUs, agency rule-making |
|Ecological | Rapid climate change outpaces management | High | High | Annual adaptive update; diversified interventions |
|Social | Anti-hunt activism leads to litigation | Med | Med | Transparency, emphasizing habitat degradation data |
|Tech | Data gaps due to satellite failure | Low | Med | Multi-constellation redundancy (SAR + optical) |

---

## 11   Conclusions & Next Steps
Arctic snow-goose hyper-abundance is a *wicked* problem intertwining continental agriculture, migratory connectivity, Indigenous rights, and fragile tundra ecosystems. Past liberalised harvests (1999–present) slowed but did not reverse population growth, in part because monitoring lagged, protocols shifted, and Indigenous food-security considerations remained siloed.

The integrated framework herein leverages half-a-century of lessons (state-space modelling, satellite remote sensing, governance failures and successes) and folds in emerging tools—from UAV transects to blockchain quotas—to forge a genuinely adaptive, pan-Arctic program. Critical to success is the empowerment of Indigenous Guardians and the institutional nimbleness offered by the proposed Pan-Arctic Snow-Goose Council, which can operate below the treaty-amendment threshold yet above piecemeal regional schemes.

Immediate action items:
1. Convene founding PASGC meeting (target September 2025, Yellowknife).  
2. Secure $12 M seed funding (Duck Stamp apportionment, philanthropic foundations).  
3. Begin open-data migration and historical survey re-calibration to eliminate 18 % bias anomalies.  

By systematically aligning ecological targets with Indigenous food-security imperatives—and doing so through robust, transparent, and innovative governance—the Arctic can avert further habitat collapse while honouring the subsistence cultures that have stewarded these landscapes for millennia.


---

**References (abbreviated)**:  
• Reeves, Cooch & Munro 1975; Lamarre et al. 2017; Arctic Goose Habitat Working Group 1998; USFWS 2023 harvest reports; ICC submissions 2022.  
(Supplementary detailed bibliography available on request.)


## Sources

- https://www.collectionscanada.gc.ca/obj/s4/f2/dsk3/ftp04/NQ58255.pdf
- https://www.pame.is/images/03_Projects/AMSA/AMSA_2009_report/AMSA_2009_Report_2nd_print.pdf
- https://publications.gc.ca/collections/collection_2015/ec/CW69-16-44-2014-eng.pdf
- https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2019.00309/full
- https://datadryad.org/dataset/doi:10.5061/dryad.796t8
- https://www.fws.gov/law/migratory-bird-treaty-act-1918
- https://cdnsciencepub.com/toc/as/11
- https://www.mdpi.com/2071-1050/13/13/7400
- https://www.researchgate.net/publication/227735181_The_dynamics_of_landscape_change_and_Snow_Geese_in_mid-continent_North_America
- https://www.researchgate.net/publication/228609013_Changes_in_survival_rates_and_population_dynamics_of_greater_snow_geese_over_a_30-year_period_Implications_for_hunting_regulations
- https://arctic.noaa.gov/wp-content/uploads/2023/04/ArcticReportCard_full_report2022.pdf
- https://publications.gc.ca/collections/collection_2018/eccc/En4-337-2018-eng.pdf
- https://www.researchgate.net/publication/346034399_Anthropogenic_impacts_on_the_demographics_of_Arctic-breeding_birds
- https://www.jstor.org/stable/26608864
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4980315/
- https://www.fws.gov/testimony/ecological-problems-associated-overabundant-white-goose-populations
- https://pubmed.ncbi.nlm.nih.gov/17601135/
- https://pubs.usgs.gov/publication/5220909