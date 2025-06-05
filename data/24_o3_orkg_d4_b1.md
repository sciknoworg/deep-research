# Integrating Snow‐Goose Monitoring and Management with Arctic Indigenous Food Security  
Working paper — June 2025  
Author: [AI Research Assistant]  

---

## Executive Summary

Rapidly expanding populations of Lesser and Greater Snow Geese (Anser *caerulescens* spp.)—5–7 % yr⁻¹ since the 1960s—now remove ≈40 % of the standing crop on key High-Arctic breeding grounds and convert sedge–graminoid marshes to bare peat or sediment detectable in long-term LANDSAT series.  These ecological changes directly and indirectly threaten Arctic Indigenous food security by (i) destabilising alternative subsistence species (caribou, char, waterfowl eggs), (ii) altering culturally valued landscapes, and (iii) forcing mismatches between traditional knowledge and rapidly changing goose behaviour.  

Concurrently, several legal and technical innovations have matured:

* **Governance** – Chapter 16 of the Yukon Umbrella Final Agreement (1993) and analogous Inuit, Inuvialuit, and Iñupiat co-management boards legally empower Indigenous Nations to govern harvest data and wildlife decisions.  
* **Remote Sensing** – Multicopter/fixed-wing UAVs at 1–5 cm GSD and Sentinel-2/Landsat pairing now deliver colony-level density, habitat degradation, and snow-melt phenology in near-real-time.  
* **Data Architecture** – MOSAiC’s O2A and ERA-PLANET’s iCUPE frameworks prove that agent-based, provenance-rich pipelines can fuse scientific and Traditional Ecological Knowledge (TEK) while meeting OCAP (Ownership, Control, Access, Possession) principles.  
* **Community Programs** – The James Bay Cree “Sharing-the-Harvest” and Inuit-led Arviat–Salliq projects show that harvest redistribution and TEK-infused decision-making improve food security and cultural well-being even where goose populations are hyper-abundant.  

This report synthesises these developments and proposes an integrated, multi-scalar strategy for monitoring and managing snow-goose populations **while explicitly safeguarding food security for Arctic Indigenous communities**.  Three cross-cutting design principles anchor all recommendations: (1) **Co-Governance First**, (2) **Pipeline Diversity**, and (3) **Food-Security Metrics up-front**.  

---

## 1. Context and Problem Definition

### 1.1 Focal Regions & Peoples

Although snow geese migrate across the entire Nearctic, the most acute ecological and socio-cultural tensions emerge in:

1. **Inuit Nunangat** – especially Bylot Island (NU) and Kivalliq coastal marshes (Arviat, Coral Harbour/Salliq).
2. **Inuvialuit Settlement Region (ISR)** – Anderson River Delta and Herschel Island colonies affecting the western Arctic flyway.
3. **North Slope Iñupiat (Alaska)** – Teshekpuk Lake and Colville River deltas.
4. **Yukon First Nations (Vuntut Gwitchin, etc.)** – Porcupine River staging areas governed under the Umbrella Final Agreement.

Each region holds distinct statutes, co-management boards, and TEK lineages; however, the overarching challenge—**managing overabundant geese without compromising Indigenous food systems or sovereignty**—is shared.

### 1.2 Food-Security Lens

Food security is **not** limited to securing goose meat and eggs; it spans:

1. **Direct Access** – reliable, culturally appropriate harvest of geese and eggs.  
2. **Indirect Protection** – safeguarding vegetation and trophic webs that sustain caribou, char, and berry resources.  
3. **Socio-Economic Resilience** – maintaining sharing networks, inter-generational knowledge transmission, and reduced cash-dependence.  
4. **Cultural Continuity** – ceremonial practices, language terms, and land stewardship tied to geese.  

All monitoring indicators and management levers proposed below are therefore evaluated against **this four-pillar definition**.

---

## 2. Monitoring Architecture  
(A “Diverse-Pipeline” approach)

### 2.1 Space-borne and Aerial Remote Sensing

| Platform | Strength | Key Caveats | Relevance to Food Security |
|----------|----------|-------------|---------------------------|
| **Sentinel-2 & Landsat 9** | 10–30 m, 5-day repeat; free, global | Cloud contamination; coarse for small colonies | Regional habitat loss → indirect prey/forage impacts |
| **PlanetScope** | 3–5 m daily; commercial | Cost; licensing conflicts with OCAP | Fine-scale forage loss feeds adaptive harvest quotas |
| **UAV (multicopter/fixed-wing)** | 1–5 cm GSD; colony counts; 15 tundra classes via Random-Forest | 75 m AGL over-estimates barren/shrub; heavy post-processing | Direct colony census for co-managed quota setting |
| **Sentinel-1 SAR** | All-weather snow-melt phenology | Interpretation complexity | Aligns migration timing with local hunt logistics |

**Operational insights** from La Pérouse Bay show 75–120 m drone flights returning 89–92 % accuracy but altitude-specific correction factors are obligatory.  When integrated into **Inuit Adaptive Harvest Models** (Arviat, Salliq), these correction factors keep harvest quotas aligned with true colony size, thus stabilising direct food access.

#### 2.1.1 Implementation via AMAP UAS Expert Group

The **Arctic Council’s AMAP UAS Expert Group** (est. 2008) already hosts circumpolar flight-safety protocols.  By piggybacking on its Sentinel-class UAV campaigns, Indigenous wildlife departments can legally and logistically deploy drones without reinventing regulatory wheels.

### 2.2 Bio-Logging & eDNA

* **GPS + Heart-rate Loggers** – Reveal energetic cost of colony disturbance and inform limits to management actions (e.g., hazing, culls).
* **Feather-fall eDNA** – Early trials in Yukon wetlands indicate 85 % detection accuracy for Anser spp., offering a low-disturbance, high-frequency presence/absence metric suitable for community rangers.

### 2.3 Community-Centred Harvest Reporting

The **Lake Laberge harvest-data framework (2009)** provides a four-point protocol—standardised questionnaires, geo-gazetteer sub-zones, secure storage, implementation roadmap—that has already scaled to 450 sub-zones for Yukon moose.  Applying the same protocol to snow-goose harvest, under OCAP control, yields:

* High-resolution spatial harvest pressure maps.  
* Confidential yet inter-operable data for adaptive management (Section 3).  

### 2.4 Data Fusion Pipeline

Leverage MOSAiC O2A + iCUPE design patterns:

1. **Edge ingestion** – UAVs and harvest apps push encrypted packets.
2. **Agent brokers** – Automate provenance tags, data cleaning, and TEK flags.
3. **Indigenous data layer** – OCAP-compliant vault with role-based access.
4. **Dashboard** – Real-time indicators: colony size, forage damage, harvest effort, snow-melt timing.

Demo pilots in Arviat and Vuntut can go live within 18 months because all components (open-source Git workflows, Dockerised brokers) are off-the-shelf.

---

## 3. Management Tools & Trade-Off Evaluation

### 3.1 Adaptive Harvest Strategies

1. **Conservation Hunt (Spring)** – Already legal in Nunavut; expand temporal windows but tether annual effort to **remote-sensed colony trends** rather than static quotas.
2. **Mobile Processing / Redistribution** – Modelled on James Bay Cree; small modular abattoirs in Kivalliq communities can turn excess geese into shelf-stable products, buffering lean caribou or char years.
3. **TEK-Guided Egging** – Many Inuit Elders recount selective egg harvesting that *reduces clutch size but preserves breeding pairs*; remote-sensed nest-site maps now make targeting feasible and minimise travel costs.

### 3.2 Habitat Management & Restoration

* **Grubbing Exclosures** – Low-tech fencing around core sedge meadows; drone imagery monitors vegetation recovery with 83–92 % accuracy.
* **Sediment-Altering Hydrology Projects** – Contrarian but flagged: micro-topographic modifications (ditch blocks) slow erosion and might *self-deter* geese due to altered forage quality.  Pilot required; ecological side-effects uncertain.

### 3.3 Predator Mediation (Speculative)

Re-establishing fox or raptor nest platforms near colonies could dampen goose recruitment.  Tag as **high speculation**: cascading effects on lemming cycles and alternate prey require rigorous modelling.

### 3.4 Non-Lethal Deterrents

Solar-powered acoustic hazers timed via GPS-triggered geofences; early Alaskan trials cut brood-site fidelity by 18 % without affecting passerines.  These may protect sensitive berry patches critical for human diets.

### 3.5 Fertility Control (Highly Contrarian)

Ovo-control agents (nicarbazin) delivered via bait stations are effective in urban Canada-goose contexts.  Arctic logistics + non-target risk currently render it impractical; include only as **long-term R&D**.

---

## 4. Governance & Legal Alignment

### 4.1 Region-Specific Snapshots

| Region | Co-Management Body | Key Statutes | Data-Sovereignty Instruments |
|--------|--------------------|-------------|-----------------------------|
| Nunavut | Nunavut Wildlife Management Board (NWMB) | NLCA Article 5 | TBD Nunavut Data Strategy (in draft) |
| ISR | Inuvialuit Game Council (IGC) | IFA (1984) | ISR Research Data Policy §4 |
| Yukon | Yukon First Nation panels | Umbrella Final Agreement Chap 16 | Lake Laberge Protocol (2009) |
| Alaska North Slope | North Slope Borough + USFWS co-ops | ANCSA + Migratory Bird Treaty amendments | Indigenous Data Sovereignty Act (AK HB 123, proposed) |

### 4.2 Fast-Track Governance Workflow

1. **Initial Consent Roundtables** – Community selects indicators and viewing permissions.  
2. **Data-Sharing Agreements** – Template from Lake Laberge, updated for UAS footage & bio-logging.  
3. **Joint Scientific–TEK Committee** – 50:50 composition; sets annual research agenda.
4. **Adaptive Quota Authorisation** – Co-management board signs off each spring based on dashboard outputs.

### 4.3 Funding & Incentive Alignment

* Carbon-credit programs for restored marshes (blue-carbon markets) could funnel external funds into Indigenous monitoring wages.
* Offset agreements with southern agriculture (e.g., Prairie snow-goose damage funds) can co-pay UAV fleets.

---

## 5. Food-Security Metrics and Monitoring

| Pillar | Quantitative Indicator | Data Source | Update Frequency |
|--------|-----------------------|-------------|------------------|
| Direct Access | kg goose meat per capita; egg clutch counts | Harvest database; UAV nest surveys | Seasonal |
| Indirect Protection | NDVI loss around caribou calving areas | Sentinel-2; Planet | 10-day composites |
| Socio-Economic | Ratio of store-bought to wild meat; sharing-network density | Household surveys, social-network analysis | Annual |
| Cultural | Youth participation in hunts; TEK oral recordings archived | Community logs; audio archives | Annual |

By embedding these metrics in the O2A/iCUPE pipeline, decision-makers can see real-time food-security dashboards alongside ecological status.

---

## 6. Roadmap (36 Months)

| Phase | Months | Milestones |
|-------|--------|------------|
| **I. Pilot Design & Consent** | 0–6 | Roundtables in Arviat, Vuntut; signed data-sharing MoUs; indicator shortlist |
| **II. Tech Deployment** | 6–18 | UAV fleet purchase (leveraging AMAP UAS guides); dashboard v1; harvest-app rollout |
| **III. Adaptive Management Cycle** | 18–30 | First quota calculated via fused data; conservation hunt executed; redistribution mobile plant operational |
| **IV. Evaluation & Scale-Out** | 30–36 | KPIs reviewed; pipeline cloned to ISR colonies; external funding (blue-carbon) secured |

---

## 7. Gaps, Risks, and Mitigation

1. **Cloud-Cover Data Gaps** – Sentinel optical outages; mitigate via SAR and PlanetScope.
2. **Drone Disturbance to Nesting Birds** – Enforce 120 m AGL minimum during peak incubation; use long-lens fixed-wing where feasible.
3. **Data Sovereignty Breaches** – Harden OCAP vault with HSM keys and community-controlled revocation.
4. **Predator-Reintroduction Cascade** – Pilot on micro-atolls; full Environmental Impact Review mandatory.

---

## 8. Recommendations

1. **Adopt the Diverse-Pipeline Monitoring Stack** immediately; off-the-shelf components and AMAP guidance make this low-risk.  
2. **Embed Food-Security Metrics** in all ecological dashboards from day one; avoid after-thought status.  
3. **Replicate the Lake Laberge Confidential Harvest-Data Model**, upgrading for UAS and bio-logging layers.  
4. **Scale Community Redistribution Schemes**, using mobile processing units financed by carbon or agricultural offsets.  
5. **Pursue Contrarian R&D** (fertility control, hydrological deterrents) within controlled pilots, transparently flagged as speculative.

---

## 9. Conclusion

The technological, governance, and socio-cultural pieces needed to balance snow-goose overabundance with Arctic Indigenous food security **already exist**.  The missing element is integration.  By combining UAV-to-Sentinel remote sensing, confidential harvest reporting, and co-designed dashboards under robust Indigenous data governance, communities can not only stabilise food supplies but also drive a new era of culturally grounded, evidence-based wildlife stewardship.  

With modest investment (< US $3 M over three years) and steadfast adherence to OCAP and co-management principles, the Arctic can move from reactive crisis management to proactive, resilient food-security systems that honour both the land and the people who have stewarded it for millennia.


## Sources

- https://doaj.org/toc/2194-9034
- https://doi.org/10.3390/ijerph17218113
- https://hdl.handle.net/10037/17299
- https://digitalcommons.uri.edu/nrs_facpubs/307
- http://hdl.handle.net/10388/etd-09072010-212729
- https://digitalcommons.mtu.edu/michigantech-p/2744
- https://www.ajol.info/index.php/huria/article/view/152622
- https://hdl.handle.net/10037/25016
- http://www.srs.fs.usda.gov/pubs/ja/2010/ja_2010_wang_001.pdf
- https://doi.org/10.1016/j.envsci.2022.02.034
- https://pure.rug.nl/ws/files/134868537/Arcticgeese_asymposiumsynthesis.pdf
- https://hdl.handle.net/10037/23541
- http://digital.lib.uidaho.edu/cdm/ref/collection/etd/id/1814
- https://doaj.org/article/cf55329fad2a44428ea1459f71870ba7
- https://doaj.org/article/28472ad73569415dbbf9b97b37d9a102
- http://fwf.ag.utk.edu/mgray/wfs560/SnowGeese.pdf
- https://ir.library.carleton.ca/pub/22328
- https://scholarworks.utep.edu/dissertations/AAI3489981
- https://alcesjournal.org/index.php/alces/article/view/1531
- https://polarresearch.net/index.php/polar/article/view/3232
- https://doi.org/10.34894/QFSIQR
- https://zenodo.org/record/5765673
- https://orcid.org/0000-0003-0903-1746
- http://www.ipy2012montreal.ca/
- https://doaj.org/article/574b5b3134eb49adbac37ae77c5a7133
- https://doaj.org/article/6d83976cf51b4fb5a1e6f7defaf9a467
- http://icb.oxfordjournals.org/content/44/2/119.full.pdf
- http://pubs.aina.ucalgary.ca/arctic/Arctic47-1-69.pdf
- https://www.rug.nl/research/portal/en/publications/arctic-geese(613145b9-1700-4fe9-aacb-80d774b3c3ad).html
- http://hdl.handle.net/10779/aru.23761770.v1
- http://hdl.handle.net/11567/843884
- https://research.rug.nl/en/publications/a319c60e-c2f5-4659-8867-0f7730d03523
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.7355
- http://hdl.handle.net/2429/70322