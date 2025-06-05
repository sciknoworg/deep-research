# Monitoring and Managing Snow Goose Populations While Preserving Food Security for Arctic Indigenous Communities — A Comprehensive Technical Synthesis (2025)

*Prepared for experienced analysts engaged in Arctic wildlife co-management and food-system resilience planning*

---

## Executive Summary

•  Snow‐goose (Chen caerulescens) numbers increased 5–7 % yr⁻¹ between the late-1960s and mid-1990s, fuelled chiefly by temperate-zone agricultural nitrogen subsidies. Several sub-populations have now plateaued or declined, but at colony sites the legacy of hyper-abundance persists as large areas of exposed sediment, suppressed graminoid biomass and weakened permafrost hydrology (Learning IDs 3, 8, 9, 21, 31, 36, 38, 56, 73).

•  Intensive herbivory reduces C-sink strength, accelerates soil-C erosion and amplifies climate-driven drying of pond complexes; exclosure experiments reveal that wet moss meadows can recover CO₂ uptake and double live‐biomass C within < 10 yr once grazing stops (IDs 4-5, 14-15, 22-24, 28-30, 48, 50, 59, 69-70).

•  Food security for Inuit, Iñupiat/Yupik and Inuvialuit communities depends simultaneously on reliable access to snow geese as a country-food resource **and** on maintaining other tundra foods (caribou, char, berries) and ecosystem services jeopardised by ongoing habitat degradation.

•  Monitoring capacity now spans spaceborne NDVI trend analyses, GPU-accelerated sUAS Structure-from-Motion (SfM) with centimetre-scale GSD, Random-Forest and deep-learning classifiers, GPS-GSM accelerometer bio-logging, and community-led harvest and disturbance surveys. Cross-site transferability of image classifiers remains poor (< 50 % macro-F1) without local training data (IDs 1-2, 11-13, 17-20, 25-27, 34-35, 41-44, 52, 55, 57, 61, 66, 72).

•  Harvest-mortality compensation documented historically in lesser snow geese (q ≈ 0.47) has now collapsed; hunting is largely additive, giving managers greater leverage—provided hunter effort can be sustained despite diminishing marginal returns (IDs 6-7, 32, 45, 58, 62, 71).

•  Governance is legally fragmented (Migratory Birds Convention Act, MBCA‐1916/1994; Migratory Bird Treaties Protocol 1995; Inuvialuit Final Agreement 1984; Nunavut Agreement 1993; Alaska National Interest Lands Conservation Act 1980; Greenland Home Rule Act 1979) but converging toward co-management boards and Indigenous self-determination; participatory research in Arviat & Salliq illustrates this trajectory (IDs 9, 37, 40).

•  An **Integrated Circumpolar Framework (ICF)** is proposed, combining multi-scale remote sensing, Bayesian state-space population models, stochastic harvest decision analysis, habitat manipulation, and co-designed food-security indicators. Novel, un- or under-utilised levers include: (i) carbon-credit financed exclosures, (ii) biologically targeted hunt timing using near-real-time satellite phenology, (iii) GPU-accelerated on-device AI for field-deployable habitat classification, and (iv) predator-acoustic luring or low-power UAV hazing to redistribute local grazing pressure.

---

## 1 Background and Scope

The client has not specified a single focal region; therefore a **circumpolar comparative** approach is adopted, covering:

1.  Canadian Inuit Nunangat (Kivalliq, Qikiqtaaluk, Kitikmeot).
2.  Alaskan North Slope and Yukon–Kuskokwim Delta (Iñupiat & Yupik).
3.  Greenland (Avanersuaq, Kitaa) and Svalbard (Governor of Svalbard + Sámi use areas).
4.  Western Canadian Arctic (Inuvialuit Settlement Region).

We integrate **both monitoring technology and policy/management interventions** and link them explicitly to Indigenous food security, recognising that detailed quantitative modelling is valuable yet often secondary to immediate management needs.

---

## 2 Population Status and Demography

### 2.1 Main Flyway Populations

| Flyway / Sub-population | 2023 est. abundance | Recent λ | Key notes |
|---|---|---|---|
| Mid-Continent Population (MCP) Lesser Snow Goose | 12–14 M | ▲ 1.01–1.02 yr⁻¹ post-2010 | Growth has slowed; hunting additive (IDs 3, 7, 32). |
| Western Arctic/ Wrangel Island Snow Goose | 0.45 M | ▲ 1.03 yr⁻¹ | Colony largely intact; philopatry high. |
| Atlantic Population (AP) Greater Snow Goose | 0.9 M | ≈ stable | Kalman filter shows survey shift bias (ID 60). |
| Ross’s Goose (Queen Maud Gulf) | 1.3 M | ▼ post-2018 | Shared with MCP; same degradation footprint (ID 50). |
| Pink-footed & Barnacle (Europe) | 0.08 M & 1.1 M | ▲ | Include for extrapolated management lessons. |

### 2.2 Vital Rates and Harvest

•  Multi-state capture–recapture of 139 k lesser snow geese (2006-15) → adult survival 0.79–0.94; juvenile 0.16–0.47; direct exploitation ≤ 0.06 (IDs 6-7, 32).

•  Process-correlation q collapsed from 0.47 partial compensation to near-zero; hunting mortality now **additive** (ID 45). 

•  2019 Illinois Light Goose Conservation Order (CO) efficiency ≈ 2.9 birds · hunter-day⁻¹; only 7.2 % of hunters saw improved success despite 44 % higher effort (IDs 20, 25, 55, 62).

•  Subsistence spring harvest (Inuvialuit 1987-90) ≈ 10 k geese yr⁻¹ (≈ 19 % of continental spring take) — often omitted from continental models (IDs 46, 68).

---

## 3 Ecological Impacts of Hyper-abundance

### 3.1 Vegetation Regime Shifts

Hudson Bay Lowlands and Karrak Lake colonies exhibit graminoid cover reductions of 46–61 % and shrub cover losses of 29–84 % with persistent bare sediment patches (IDs 21, 31, 50, 69, 70).

### 3.2 Carbon Cycling

•  Barnacle goose exclosures in Svalbard flipped peak-season NEE from +0.47 to −0.77 µmol CO₂ m⁻² s⁻¹ (IDs 4, 14, 59).

•  ITEX × grazing factorials show grazing dominates warming effects in wet meadows; warming partly offsets losses in mesic heaths (IDs 5, 15, 48).

•  Pink-footed goose grubbing turns intact tundra from sink to source within < 2 wk (IDs 22, 24, 59).

### 3.3 Hydrology and Permafrost

Western Banks Island pond complexes have lost 7.9 % surface water; grazing hotspots coincide with greatest drying (ID 19). Coupled with deltaic C/N thaw release (ID 23) this raises export fluxes to Arctic Ocean food webs.

---

## 4 Monitoring Technologies and Data Pipelines

### 4.1 Spaceborne Remote Sensing

•  Landsat & Sentinel-2 NDVI map “exposed sediment” states but miss patchiness; super-resolved PlanetScope + Shannon Evenness correct pixel mixing (IDs 12, 38).

•  Snow-cover phenology from Sentinel-2 predicts breeding-area selection by pink-footed geese (ID 65).

### 4.2 UAV / sUAS Photogrammetry

Hardware & Accuracy:

•  Fixed-wing RGB at 75–120 m AGL → 2.4–3.8 cm GSD; 88.8–92 % OA for habitat mapping (IDs 12, 34). 10–15 cm absolute accuracy with GCPs; direct PPK GNSS alone degrades to 65–120 cm (ID 1).

•  PPK GNSS + ≥ 5 GCPs → 0.026 m vertical RMSE (ID 18).

Processing Innovations:

•  GPU stereo-matching cuts multi-day builds to < 1 h (IDs 42, 64).

•  Self-Organising Map denoising, C-means clustering and Sub-Paths ROI extraction yield real-time LAI (IDs 13, 52, 71).

Classifier Performance:

•  RF macro-F1 83-85 % site-specific; < 50 % when transferred (IDs 2, 41, 63).

•  U-Net > 90 % OA on 54-band hyperspectral (IDs 27, 66). Compact CNNs perform comparably with fewer epochs (ID 52).

Sensor Fusion:

•  Field spectroscopy → 5-band UAV → Sentinel-2 up-scaling recovers water, N, P, C:N (r² 0.61-0.88) (IDs 16, 61).

•  Cross-modal GAN/variational encoders harmonise ground, UAV and satellite data in latent space; reduce labelled sample demand (ID 53).

### 4.3 Bio-logging

GPS-GSM + triaxial accelerometers classify nesting with 98.6 % accuracy; nests located within 0.8-3.6 m (ID 26). A low-cost alternative to ground nest checks, valuable for Indigenous Guardian programs.

### 4.4 Community-Based Monitoring

Participatory harvest surveys (Inuvialuit, Kivalliq) fill data gaps and embed Inuit Qaujimajatuqangit (IQ) (IDs 37, 40, 46). Drone imagery review by community members increases habitat-class labelling throughput (ID 34).

### 4.5 Data Integration and Modelling

•  Kalman filter state-space integration tightens survival–harvest regression precision (ID 60).

•  Stochastic dynamic-programming (SDP) for geese shows harvest ceilings shape optimal abundance targets; robust rules nearly match adaptive ones (IDs 18, 44, 58).

---

## 5 Indigenous Food Security Interface

Food security is multidimensional: (i) availability (harvest success, climate hazard), (ii) access (equipment, fuel, policy), (iii) utilisation (nutrition, cultural preference), (iv) stability. Hyper-abundant snow geese affect all four:

1.  **Positive** — more birds available for country food; high-protein spring harvest.
2.  **Negative** — tundra degradation reduces caribou forage and berry productivity, undermining diet diversity; pond drying threatens char overwinter habitat.
3.  Effort–yield divergence indicates growing hunter fatigue and expense (ID 6, 62).
4.  Co-management systems (e.g., Nunavut Wildlife Management Board, Inuvialuit Game Council) already legally empower Indigenous communities; integrating high-resolution monitoring data can strengthen their negotiating position.

We recommend co-developing a **Snow-Goose Food-Security Index (SG-FSI)** that blends quantitative (kg goose · capita⁻¹ yr⁻¹, NDVI of berry patches) and qualitative (community interviews on hunting constraints) metrics.

---

## 6 Management Interventions and Evidence Base

### 6.1 Harvest tools

•  **Spring Conservation Orders (COs):** liberal methods (electronic calls, unplugged shotguns) documented high adoption but falling efficiency. We advise dynamic licensing that bundles data submission with access to CO benefits, thereby replenishing monitoring datasets.

•  **Flyway-specific seasons:** September Atlantic Flyway harvest selectively removed 98 % resident AFRP geese, demonstrating fine-grained temporal targeting to avoid collateral take (ID 33).

•  **Quota optimisation via SDP:** incorporate additive mortality (post-compensation era) and hunter capacity ceilings (IDs 44, 58). Lower quotas may paradoxically yield higher realised harvest when hunter effort responds to perceived scarcity (cf. Norway ptarmigan implementation uncertainty, ID 41).

### 6.2 Habitat Manipulation

•  Temporary exclosures (< 10 yr) can rapidly restore wet meadow C-sink function; financing via carbon markets is now plausible (IDs 4, 14).

•  Predator attraction (fox dens, raptor perches) shown effective for colonial seabirds; speculative for geese but merits trial (**speculative**).

•  Hydrological engineering (small berms, beaver-analog dams) may buffer ponds against combined goose/trend drying (**contrarian**, ID 19).

### 6.3 Redistribution Rather Than Reduction

•  UAV hazing or predator‐acoustic playback can move grazing pressure away from sensitive berry/green forage areas. Low-power, long-endurance fixed-wing drones could patrol < 500 ha nightly.

•  Agricultural subsidy agreements along temperate flyways could condition bait-field support on verified goose take (instrumented via RFID shot-logging) to draw birds southward longer, easing Arctic pressure.

### 6.4 Governance Innovations

•  **Indigenous Guardian UAV Cohorts:** Training local operators to fly and process imagery using open-source GRAPHOS + cloud GPU nodes (IDs 36, 42) reduces external-consultant dependency.

•  **Data Sovereignty Vaults:** All raw and processed data stored in in-region servers complying with OCAP® principles (Ownership, Control, Access, Possession).

•  **Performance-Based Carbon Credits:** Verified biomass recovery inside exclosures monetised via Article 6.2 bilateral agreements—revenue split to fund community harvest programs.

---

## 7 Integrated Circumpolar Framework (ICF)

1.  **Tier-1 Continental Surveillance** — Annual Landsat/Sentinel-2 NDVI change detection; Google Earth Engine script triggers UAV deployments when ΔNDVI < −0.05 for > 2 yr.
2.  **Tier-2 Regional sUAS Mapping** — Fixed-wing RGB/RE flights, RTK PPK, 10 cm accuracy; RF/U-Net classification; AI-guided GCP reduction (IDs 1, 18, 42). Output: 1:500 orthomosaics, disturbance masks.
3.  **Tier-3 Colony-Scale Bio-logging** — GPS-GSM tags on breeding females identify incubation success and local foraging hotspots (ID 26).
4.  **Tier-4 Community Telemetry & Harvest Logs** — Mobile app or offline-sync forms (FAIR data) capturing effort hours, ammo expenditure, success.
5.  **Bayesian State-Space & SDP Engine** — Feeds on Tiers 1-4. Computes forward 10-yr abundance envelope under quota scenarios; outputs management recommendations.
6.  **SG-FSI Dashboard** — Visualises goose availability vs. broader food-web indicators; colour-coded risk.

---

## 8 Additional / Contrarian Options

| Idea | Rationale | Caveats |
|---|---|---|
| Immunocontraceptive-loaded bait grains (**speculative**) | Rapid fertility reduction without relying on hunter capacity. | Regulatory, off-target risk, repeated dosing needed. |
| CRISPR-aided sex-ratio distortion (**highly speculative**) | Long-horizon population suppression. | Ethical, off-target gene flow, treaty compliance. |
| UAV borne thermal culling in molting aggregations | Precise, lower labour. | Logistics, public perception, treaty approval. |
| Predator reinforcement (arctic fox den enhancement) | Natural regulation, cultural alignment. | May affect other ground-nest birds. |
| Payment for Ecosystem Services to farmers along flyway | Incentivise prolonged stopovers south of Arctic. | Requires tight verification of goose numbers. |

---

## 9 Road-Map (2025–2035)

Year 1-2: Pilot SG-FSI in Arviat & Tuktoyaktuk; deploy Guardian UAV cohorts; begin carbon-credit negotiations for exclosure projects.

Year 3-5: Integrate Tier-1/2 data into Bayesian engine; implement adaptive quota adjustments; commence pond-buffer hydrological trials.

Year 6-10: Scale to circumpolar network; evaluate predator attraction efficacy; review immunocontraceptive feasibility.

---

## 10 Conclusions

All evidence converges on the need for **multi-scalar, Indigenous-centred adaptive management** that treats harvest, habitat and monitoring as an integrated system. Modern UAV-AI pipelines, bio-logging and cloud computation remove historical technical bottlenecks; the limiting factors are governance coordination, data sovereignty, and the economic sustainability of hunter participation. By aligning carbon-market finance, flyway agriculture policy and participatory monitoring, it is feasible to curb snow-goose impacts **without** compromising — and potentially enhancing — Arctic Indigenous food security.

---

## 11 Key Learning References (IDs correspond to supplied list)

1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 48, 49, 50, 52, 53, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 68, 69, 70, 71, 72, 73.

*(For brevity this list omits IDs with duplicate information; all provided learnings were integrated into the narrative above.)*


## Sources

- http://hdl.handle.net/10255/dryad.38309
- http://dx.doi.org/10.1007/s10533-010-9545-z
- https://digitalcommons.library.umaine.edu/etd/2788
- http://hdl.handle.net/10451/35937
- https://zenodo.org/record/7957829
- https://doaj.org/article/c81ccaf459ab4d7cb2218e21c0567dce
- https://hdl.handle.net/1842/41201
- https://doaj.org/toc/1890-6729
- https://digitalcommons.unl.edu/biosysengfacpub/482
- http://pubs.aina.ucalgary.ca/arctic/arctic59-2-201.pdf
- https://hdl.handle.net/10037/25016
- https://doaj.org/article/28472ad73569415dbbf9b97b37d9a102
- https://doaj.org/article/63c132ce45cb4d07b04535ebb33d8fa1
- https://doi.org/10.1016/j.isprsjprs.2020.09.025
- https://doi.org/10.1890/07-1601.1
- https://doi.org/10.1111/1365-2664.12992
- https://doi.pangaea.de/10.1594/PANGAEA.897909
- http://hdl.handle.net/1807/24580
- http://hdl.handle.net/10255/dryad.95781
- https://hdl.handle.net/11250/2990905
- https://doi.org/10.1111/j.1365-2486.2006.01310.x
- http://raiith.iith.ac.in/10282/
- https://dx.doi.org/10.3390/rs4051392
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:219032
- http://resolver.tudelft.nl/uuid:40dddb4e-d0fa-42f5-9a54-f4fc32384cf4
- https://research.aber.ac.uk/en/publications/f6b61f3c-fd83-4a7e-874a-65e51481f756
- https://doaj.org/article/4ac1030a13124391b4e6b933895ba25e
- http://hdl.handle.net/10536/DRO/DU:30035111
- http://library.arcticportal.org/2811/1/aqhaliat-volume-4-english.pdf
- https://hal.archives-ouvertes.fr/hal-02074264/document
- https://doi.org/10.1016/j.rse.2019.01.030
- https://digitalcommons.lsu.edu/eecs_pubs/635
- http://hdl.handle.net/10.1371/journal.pone.0212773.g003
- https://dx.doi.org/10.3390/rs5031066
- http://hdl.handle.net/2142/10425
- https://www.rug.nl/research/portal/en/publications/arctic-geese(613145b9-1700-4fe9-aacb-80d774b3c3ad).html
- https://lib.dr.iastate.edu/etd/18348
- https://research.rug.nl/en/publications/hyperspectral-demosaicking-and-crosstalk-correction-using-deep-learning(cb241d38-f34a-475e-b0e3-c737faa4e540).html
- https://figshare.com/articles/_Spring_migration_route_for_three_barnacle_goose_populations_from_their_wintering_to_their_breeding_sites_/1178426
- http://hdl.handle.net/10.6084/m9.figshare.24290161.v1
- http://jornada.nmsu.edu/bibliography/09-010.pdf
- http://www.vims.edu/bridge/archive1001.html
- https://hal.science/hal-03279589/file/isprs-archives-XLIII-B3-2021-257-2021.pdf
- https://doaj.org/toc/2460-870X
- https://bearworks.missouristate.edu/articles-cnas/451
- https://doaj.org/article/929ffb6fb2654d85921add9cb5ddee25
- https://digitalcommons.usu.edu/hwi/vol9/iss1/3
- https://digitalcommons.unl.edu/birdstrike2002/49
- http://icb.oxfordjournals.org/content/44/2/119.full.pdf
- https://ir.library.oregonstate.edu/concern/graduate_thesis_or_dissertations/z603r247w
- http://hdl.handle.net/11585/545935
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0304380013005309/MAIN/application/pdf/0ec4b123a8cde8a57c0472aa1808bdd6/main.pdf
- http://www.maartenloonen.nl/literatuur/acia2004cooper.pdf
- https://research.brighton.ac.uk/en/publications/d67cf826-789e-458f-9a74-cd74c878a038
- https://digitalcommons.unl.edu/nebgamestaff/39
- https://elib.dlr.de/115501/
- https://www.neliti.com/publications/508786/geometric-accuracy-assessments-of-orthophoto-production-from-uav-aerial-images
- https://figshare.com/articles/Rusch_et_al_D_D_of_CAGO_harvest_in_MF/4257383
- https://polarresearch.net/index.php/polar/article/view/3232
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-92459
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.486.8070
- https://kent-islandora.s3.us-east-2.amazonaws.com/node/10087/10204-thumbnail.jpg
- http://www.loc.gov/mods/v3
- http://www.nusl.cz/ntk/nusl-451675
- http://hdl.handle.net/10.6084/m9.figshare.6960080.v1
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-175081
- http://www.inderscience.com/ijhpcn
- http://hdl.handle.net/11588/837190
- http://hdl.handle.net/2142/106520
- https://ir.library.carleton.ca/pub/13447
- http://hdl.handle.net/10255/dryad.170273
- http://hdl.handle.net/1807/26145
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-142019
- https://espace.library.uq.edu.au/view/UQ:134458
- https://digitalcommons.unl.edu/nacwgproc/155
- https://doi.org/10.1016/j.rse.2023.113935
- https://digitalcommons.lib.uconn.edu/dissertations/AAI3411470
- https://digitalcommons.usu.edu/wild_facpub/1499
- https://doaj.org/toc/1687-5974
- http://pure.iiasa.ac.at/view/iiasa/2135.html
- https://doaj.org/toc/2194-9050
- https://nipr.repo.nii.ac.jp/?action=repository_action_common_download&item_id=15312&item_no=1&attribute_id=16&file_no=1
- https://polarresearch.net/index.php/polar/article/view/2912
- https://583f7280-45d0-4861-b6bf-76c1451a664c.usrfiles.com/ugd/583f72_7168c272707e4a6aa86af7ffde060bdf.pdf
- http://hdl.handle.net/2117/176876
- https://doaj.org/article/64a0735f1c5c404090c34d47ef320789
- https://dx.doi.org/10.3390/rs3112529
- http://hdl.handle.net/10261/271756
- https://digitalcommons.usu.edu/hwi/vol4/iss2/9
- http://urn.fi/urn:nbn:fi-fe2020120499459
- http://ir.uitm.edu.my/id/eprint/30832/1/TD_SUAIBAH%20IBRAHIM%20AP%20R%2019_5.pdf
- https://doi.org/10.5194/egusphere-egu22-8301
- http://hdl.handle.net/10835/7572
- https://doaj.org/article/0d52b9c5b06e44fb92087db5fdbe03f4
- http://urn.kb.se/resolve?urn=urn:nbn:se:hb:diva-6782
- https://www.matec-conferences.org/10.1051/matecconf/202133606029/pdf
- https://zenodo.org/record/5016892
- https://doaj.org/article/28f4bbfdd852415aa83a13515c604fe0
- http://www.actazool.org/temp/%7Bc137f20f-7c5b-408c-b7f1-c991a1280f58%7D.pdf
- https://hal.archives-ouvertes.fr/hal-02425741
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/fc/9f/10533_2010_Article_9516.PMC4459552.pdf
- https://scholarworks.rit.edu/theses/5464
- https://commons.und.edu/bio-fac/11
- http://resolver.tudelft.nl/uuid:7e6c6398-6732-4212-b597-9561320795d1
- https://research.rug.nl/en/datasets/d5f5c7b4-1a69-43de-8bbc-f8d054961605
- http://www2.humboldt.edu/wildlife/faculty/black/pdf/Kanarek_NRM_2008.pdf
- http://munin.uit.no/bitstream/handle/10037/6651/article.pdf%3Bjsessionid%3DF5D9AEAC1EA3B0CD471D7F70341F11BF?sequence%3D1
- https://zenodo.org/record/6513051
- https://doaj.org/article/1cfd1f38b28a4abc8b9ce5184de2f77a
- http://hdl.handle.net/2429/31864
- https://digitalcommons.unl.edu/natrespapers/437
- https://rakuno.repo.nii.ac.jp/?action=repository_action_common_download&item_id=6393&item_no=1&attribute_id=21&file_no=1
- http://hdl.handle.net/2429/19697
- http://hdl.handle.net/2429/24375
- https://hal.science/hal-02393147/document
- https://mdpi.com/books/pdfview/book/1901
- https://doaj.org/toc/2194-9034
- https://doaj.org/article/c511b3ea126f4924b9f9ed6c091f5c39
- http://hdl.handle.net/10.6084/m9.figshare.7211795.v1
- https://hdl.handle.net/11250/2826221
- https://orcid.org/0000-0003-2890-8873
- https://digitalcommons.unl.edu/icwdm_usdanwrc/209
- http://ojs.francoangeli.it/_omp/index.php/oa/catalog/book/686
- https://figshare.com/articles/Pre-_and_post-survey_harvest_policies_for_the_mallard_model_with_additive_hunting_mortality_and_weak_density-dependent_reproduction_model_SaRw_/3445163
- https://doaj.org/article/574b5b3134eb49adbac37ae77c5a7133
- https://hdl.handle.net/11250/2999646
- http://repository.tue.nl/882127
- https://hdl.handle.net/10037/24588
- https://hdl.handle.net/11370/a319c60e-c2f5-4659-8867-0f7730d03523
- https://doaj.org/article/315c4a31ea7e45249a175a9eb27c846b
- https://hdl.handle.net/11250/2832519
- https://research.rug.nl/en/publications/25778291-b89a-48df-bd82-33584dab719f
- http://pubs.aina.ucalgary.ca/arctic/Arctic49-1-70.pdf
- http://www.nrcresearchpress.com/doi/abs/10.1139/AS-2016-0008
- https://lup.lub.lu.se/record/3401d381-fbbe-4a7e-a480-70cb474751d0
- http://hdl.handle.net/10045/36484
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877050911002250/MAIN/application/pdf/0953048bc27e2047b9a57745cd007719/main.pdf
- https://hdl.handle.net/2086/21502
- http://hdl.handle.net/11582/309281
- https://doaj.org/article/c47615369a0d45d0a9198faafd88ce61
- https://digitalcommons.usu.edu/context/wild_facpub/article/3525/type/native/viewcontent
- http://hdl.handle.net/2142/10213
- https://doaj.org/article/97d8f625391d4904bef6920c507e5315
- https://doaj.org/article/19103c2e54e34409837e58f63d09c573
- http://digitalcommons.usu.edu/cgi/viewcontent.cgi?article%3D2498%26context%3Dwild_facpub
- https://doaj.org/article/1554bd2141c54ffeb3b4ae04f00b1f1d
- https://journalhosting.ucalgary.ca/index.php/arctic/article/view/67172
- https://doaj.org/article/c8fb3d70d39b4bfb96308e02905904a7
- http://wildfowl.wwt.org.uk/index.php/wildfowl/article/download/1080/1080/
- http://pubs.aina.ucalgary.ca/arctic/arctic45-2-115.pdf
- https://zenodo.org/record/6792477
- https://doi.org/10.3390/rs12060959
- https://hdl.handle.net/10037/23541
- https://doi.org/10.1080/11956860.2016.1212684
- https://univ-rennes.hal.science/hal-01874635
- https://doaj.org/article/cf55329fad2a44428ea1459f71870ba7
- https://espace.library.uq.edu.au/view/UQ:2e7343f
- http://hdl.handle.net/10255/dryad.16350
- https://escholarship.org/uc/item/1426f4n2
- http://digital.library.unt.edu/ark:/67531/metadc843158/
- http://hdl.handle.net/2142/10088
- https://scholarworks.boisestate.edu/icur/2017/Poster_Session/27
- https://doi.pangaea.de/10.1594/PANGAEA.938077
- https://research-portal.st-andrews.ac.uk/files/298494669/as_6b.tif
- http://hdl.handle.net/10315/18743
- http://hdl.handle.net/11250/2392479
- http://fwf.ag.utk.edu/mgray/wfs560/SnowGeese.pdf
- https://hdl.handle.net/1969.6/89839
- https://espace.library.uq.edu.au/view/UQ:973d701
- https://doaj.org/article/c8e82bda65764685aafd7427db7749f8
- http://publications.jrc.ec.europa.eu/repository/handle/JRC53564
- http://hdl.handle.net/1807/103937
- https://doaj.org/article/3bd91dbeddcb4191ba08a20d4f4a8382
- http://dx.doi.org/10.1016/j.compag.2017.11.027
- https://dora.dmu.ac.uk/handle/2086/20948
- http://hdl.handle.net/10.1371/journal.pone.0208928.g004
- http://hdl.handle.net/11588/696225
- http://research.amnh.org/users/rfr/koonsetal13.pdf