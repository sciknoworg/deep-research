# New-Technology Leverage Points for Knowledge-Weaving in Wildlife Management  
*A synthesis of >70 recent research results (2011-2024) and forward-looking guidance*  
Date : 2025-06-03  
Author : Expert Researcher  

---

## 1  Executive summary
• Wildlife “knowledge weaving” is the deliberate fusion of heterogeneous ways of knowing—Indigenous world-views, sensor-derived data, agency reports, stakeholder experience—into a jointly owned evidence fabric that supports adaptive decisions.  
• A rapidly maturing tool-chain—edge AI, compressed-sensing sensor networks, low-energy blockchain provenance, serious-gaming/AR decision rooms—now allows the **generation→curation→trust-verification→co-interpretation** loop to be automated at field scale.  
• Field validations already exist in wetlands (Kakadu, Old Woman Creek, Yucatan Lake), temperate forests (Snapshot Serengeti, SE-Queensland koala sites), and protected-area negotiations (SimParc, CHIA).  
• Indigenous-science co-management thrives where six quantified pre-conditions (sovereignty, NAM alignment, funding, cultural-resource protection, stakeholder support, leadership) are satisfied and where data governance grants tribes veto power.  
• Blockchain + zero-knowledge proof (ZKP) stacks (BSTProv, zkLedger, zk-SNARK variants) can immutably link raw sensor traces, Indigenous qualitative scores and agency edits **without exposing sensitive records**, unlocking cross-domain analytics while respecting data sovereignty.  
• Energy neutrality is feasible: solar-powered smart traps (<5.3 W), insect cameras (3.5 mJ per frame), Rakeness compressed bioacoustic arrays (≈2× energy cut) and event-camera robots demonstrate multi-year unattended operation.  
• Late-fusion multi-sensor AI (thermal+RGB, radar+acoustic) cuts false alarms and is now benchmarked on public datasets (650 IR/RGB drone-detection videos) supporting open-science replication.  
• Immersive, ontology-indexed AR/VR workspaces (VAQUERO, Aïoli, Contextual Graph VR engines) already meet Reed et al.’s participation criteria and sustain near face-to-face negotiation performance.

> Bottom line: **the technical pieces for end-to-end, trustable knowledge weaving exist today**; institutional adoption hinges on governance, capacity building, and rigorous energy & ethical design.

---

## 2  Knowledge-weaving dimensions
1. **Epistemic integration** : merging Indigenous Knowledge (IK), Traditional Ecological Knowledge (TEK), Western science, local observations.  
2. **Data traceability & trust** : immutable provenance, selective disclosure, auditability.  
3. **Decision-making workflows** : stakeholder deliberation, co-governance boards, ranger knowledge brokers, consensus simulators.  
4. **Monitoring & feedback** : real-time or near-real-time sensing, AI analytics, edge/hybrid deployment, active-learning loops.  
5. **Educational & outreach interfaces** : VR/AR tours, high-resolution web portals, citizen-science pipelines.

### Why technology matters
• Sensors extend spatial & temporal reach of human observers.  
• Edge AI reduces data latency and respects data-sovereignty constraints.  
• Provenance tech earns cross-agency trust without central brokers.  
• Immersive collaboration tools overcome cognitive overload in multi-disciplinary teams.  
• Energy-aware networking enables deployments in remote, infrastructure-poor landscapes.

---

## 3  Technology landscape and empirical evidence
### 3.1  Sensing, inference & compression
| Category | Representative results & insights |
|---|---|
| **SAR & multispectral remote sensing** | • NISAR-analog L-band UAVSAR + object-based Random Forest reached 81.9 % accuracy mapping Yucatan Lake wetlands, Gini importance singled out H/A/ALPHA & Freeman-Durden decompositions.<br>• WorldView-3 (8 VNIR + 8 SWIR + 1 Pan) plus UAV imagery + pixel SVM hit 93.8 % class accuracy in Old Woman Creek wetlands, outperforming four object-based baselines while staying lightweight. |
| **UAV thermal/RGB wildlife spotting** | • Koala searches: thermal+LiDAR drones detected 14 koalas at three SE-Queensland sites, feeding an AI cloud hub.<br>• Kim 2023 Sobel-edge fusion processed synchronized thermal+RGB at 30 fps (<0.033 s per frame) with precision 0.80.<br>• Late-fusion RetinaNet marine trials improved vessel detection; proposal-level fusion beat middle fusion. |
| **Multi-sensor drone detection & control** | • arXiv 2207.01927 stack (thermal, visible, fish-eye, mic, ADS-B, GPS) published 650-video dataset; late fusion halved false alarms.<br>• Fraunhofer acoustic+FMCW+EO network achieved 1.5° azimuth error; DLR laser vibrometer read UAV payload resonance. |
| **Camera-trap & edge ML** | • Snapshot Serengeti CNN auto-labelled 99 % of 3.2 M images at 96.6 % accuracy, saving >17 000 h.<br>• Domain-Aware NAS produced Jetson-TX2-class nets with top accuracy & small footprint.<br>• Solar smart-trap prototype logged 85 870 videos at 0.99 lab accuracy on 5.208 W.<br>• Insect-pest trap: 93 % accuracy with 3.5 mJ per frame.<br>• Swedish Pi-class prototypes confirm >12 h battery but stress custom lightweight CNNs. |
| **Compressed & event sensing** | • Rakeness CS cut acoustic-array energy 48-44 %.<br>• Covariance CS Beamforming robustly reconstructs noisy acoustic scenes.<br>• Compressive Multiplexer folds multi-channel audio into one ADC stream.<br>• DAVIS event-camera predator robot traded latency for power; mean angular error 8.7 %. |

### 3.2  Edge networking & energy optimisation
• **PEGASIS**: 8× first-node life gain; multi-chain variant adds +20 % lifetime.  
• **BIOSARP**: Ant-colony routing balances pheromone by delay, residual battery, link QoS → lower overhead vs EEABR, SRTLD.  
• **IPv6 RPL**: energy-harvesting nodes lose 40-45 % throughput; adaptive parent selection required.  
• **RAFT under jamming**: closed-form success probabilities guide rugged blockchain overlays.  
• **Edge-offloaded PoW**: 21 % energy, 24 % memory cut while keeping 20–60 min blocks.  
• **PoS & stake-pool studies**: reward-to-stake ratio drives decentralisation; PoSCS/Microchain tailored to IoT.

### 3.3  Provenance, privacy & trust stacks
1. **BSTProv**: slices DAG into encrypted sub-graphs on Ethereum consortium chain, smart contracts keep skeleton; allows per-peer ACLs, on-demand reconstruction.  
2. **zk-Bench (2023)**: 5 ZKP tool-chains, predicts PlonK costs within 6-32 %, hardware-tuned speed-ups ≥50 %.  
3. **zkLedger**: masked analytics on $13 T securitisation data → template for wildlife funding/flora-fauna trade ledgers.  
4. **Lattice-based post-quantum SNARK**: constant-size, designated-verifier proofs (5 LWE ciphertexts).  
5. **E3S review 2023**: immutable audit trails boost stakeholder trust in ecological monitoring.  
6. **Cross-agency forensic chains**: BACARDI for orbital debris, Barcode of Wildlife DNA chain—proof of feasibility in biodiversity law-enforcement.  
7. **Prototype WSN on-chain logging**: Arduino+ESP8266 storing samples on chain; viable when paired with external miners.

### 3.4  Immersive & participatory decision support
| Tool / Study | Key learnings |
|---|---|
| **SimParc serious game** | Distributed role-play + AI agents; tested in Tijuca NP & three IUCN Congresses; gains in conflict understanding, upcoming coupling with viability simulation engine. |
| **Dynamic participatory models** | CHIA live-tunes parcel weights; 2021 tiger-farming SDM runs online; both enhance trust & real-time feedback. |
| **AR/VR negotiation workspaces** | AlARCo corpus shows negligible performance drop vs face-to-face; EU VR-Planning and ISMAR-09 rescue study report measurable gains. |
| **Ontology-driven annotation** | VAQUERO, Aïoli: role-based semantic filters accelerate retrieval; users rate interaction cues highly. |
| **Serious-gaming evaluation frameworks** | ManuVAR, structured VR benchmarking provide metrics for usability & collaboration scope. |
| **Park website audit** | Yellowstone–Kruger high-res maps & VR tours vs Itatiaia’s basic portal; digital service gap affects outreach and sustainable tourism. |

### 3.5  Indigenous knowledge integration & governance
• **Kakadu/Nardab program**: four mechanisms—holistic indicators, AI decision tools, continuous drones/traps, Indigenous-led data governance; Bininj veto over AI analysis.  
• **Boundary-work study**: success hinges on joint agenda, ranger brokers, shared boundary objects (datasets).  
• **Six-factor framework** (sovereignty, NAM alignment, funding, cultural-resource protection, stakeholder backing, leadership) repeatedly validated in U.S. tribal agencies.  
• **Indigenizing NAM (I-NAM)**: adds inter-generational stewardship, multi-nation collaboration, democracy lenses.  
• **Tribal data-sovereignty initiatives**: Ysleta del Sur, Cheyenne River Sioux build in-house data platforms to offset fragmented federal funds.  
• **Case-type taxonomy**: co-management & easement models enable full TEK uptake when tribes hold decision power.  
• **Djelk Rangers enterprises**: turtle & tarantula harvests illustrate negotiation of IK-science tensions and livelihood pathways.

---

## 4  Integration patterns for end-to-end knowledge weaving
1. **Sensor → Edge AI → Blockchain provenance → Immersive co-interpretation**  
   • E.g., solar smart-trap ↔ Jetson TX2 CNN ↔ BSTProv ↔ AR stakeholder room.  
2. **Indigenous qualitative scores + quantitative UAVSAR time-series**  
   • Shared boundary object: wetland-health dashboard coded as smart contract; traditional owners veto which layers are public.  
3. **Active-learning loops**  
   • Snapshot Serengeti model auto-labels; scientists curate mis-classifications onsite → model retrains; blockchain logs model version for audit.  
4. **Serious game-in-the-loop policy rehearsal**  
   • SimParc or CHIA pulls live sensor indicators and forecasts into negotiation rounds.  
5. **Role-based immersive visual filters**  
   • VAQUERO-style ontology indexes allow ranger, tourist, scientist to toggle layer visibility, respecting permission sets embedded in BSTProv ACLs.

---

## 5  Implementation roadmap (12- to 48-month)
### 5.1  Quick-start pilots (0-12 mo)
1. Deploy 5–10 solar smart-traps with Domain-Aware NAS models in a target protected area.  
2. Wrap raw video hashes + TEK site scores in BSTProv; test selective disclosure to external scientists.  
3. Conduct monthly AR-supported ranger meetings using Contextual Graph engine to overlay new sensor insights on 3D terrain.  
4. Run SimParc mini-scenario on imminent management decision (e.g., feral animal control) to familiarise stakeholders with serious-game process.

### 5.2  Scale-out (12-24 mo)
• Add UAVSAR/NISAR data streams; fine-tune Random Forest & CNN classifiers; link to koala/thermal UAV network.  
• Integrate Rakeness CS acoustic arrays for nocturnal species; multiplex via CMUX front-ends.  
• Begin blockchain evidence chain across agencies; port zkLedger masked analytics for funding transparency.  
• Formalise active-learning loop, logging model versions and curator interventions on chain.

### 5.3  Institutionalisation (24-48 mo)
• Codify Indigenous veto & benefit-sharing in governance charters; adopt I-NAM lens in policy language.  
• Migrate to post-quantum lattice SNARKs for long-term provenance resilience.  
• Replace PoW miner with stake-pool PoSCS node cluster running on ranger stations’ solar arrays.  
• Establish permanent VR/AR negotiation hub open to tourists for outreach; close digital-service gap highlighted by park website audit.

---

## 6  Risk map & mitigation
| Risk | Likely impact | Tech/Process guard-rail |
|---|---|---|
| Energy failure of edge nodes | Data gaps, network collapse | PEGASIS multi-chain, BIOSARP routing, energy-aware parent selection, solar oversizing factor ≥ 1.6 |
| Data-sovereignty breach | Loss of trust, legal action | BSTProv fine-grained ACLs, native-encryption sub-graphs, ZKP-only queries |
| Model drift / bias | Wrong management decisions | Active-learning human-in-loop, monthly calibration UAVSAR vs ground truth, transparent version control |
| Stakeholder fatigue | Governance breakdown | Serious-game refresh cycles, AR/VR engagement, digital portals with real-time dashboards |
| Litigation (ESA, treaty rights) | Project halt | Align with Secretarial Order 3206 templates, embed tribal co-governance legally |

---

## 7  Contrarian & speculative outlook *(flagged as informed speculation)*
1. **Event cameras + neuromorphic processors** could cut wildlife-detection power budget by 90 % within five years, enabling disposable seed-pod sensors sprinkled by drones.  
2. **Zero-knowledge federated learning** on BSTProv graphs may allow cross-nation model sharing where raw images never leave tribal land, solving privacy/power asymmetry.  
3. **Drone-resonance fingerprinting** could evolve into airborne anti-poaching nets that auto-deny flight paths to payload-capable intruders via RF geofencing smart contracts.  
4. **AR citizen-science overlays** on consumer smart-glasses may crowd-source qualitative habitat health scores, complementing professional TEK surveys.

---

## 8  Conclusion
The compiled evidence shows decisive progress along every link of the knowledge-weaving chain—from sub-Watt edge sensors and SAR classifiers to immutable, privacy-preserving provenance and immersive multi-stakeholder deliberation rooms. Where technical pilots were embedded in **co-governance structures with enforceable data sovereignty**, adaptive management gains are already measurable (Kakadu, Snapshot Serengeti, SE-Queensland koalas). Scaling these successes requires:  
• Upholding the six pre-conditions for sustained Indigenous Knowledge integration.  
• Mainstreaming energy-aware edge+blockchain design patterns.  
• Institutionalising serious games and AR/VR as standard participatory practice.  
• Committing to post-quantum, selective-disclosure provenance so that trust scales with data volume and stakeholder diversity.

With these elements in place, wildlife agencies can move from fragmented data silos to a **living, braided knowledge fabric** that accelerates conservation outcomes while honouring cultural values and ecological complexity.


## Sources

- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877050916315940/MAIN/application/pdf/1cf46246a6f9279c01f7f42fcf171d8b/main.pdf
- http://cds.cern.ch/record/1503772
- http://hdl.handle.net/20.500.11897/153867
- https://doaj.org/article/ee683b099f2645cbab2455b33355095b
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-52588
- https://researchonline.jcu.edu.au/24849/1/24849_Weiss_etal_2013.pdf
- https://digitalcommons.mtu.edu/techtalks/29
- https://ebpj.e-iph.co.uk/index.php/EBProceedings/article/view/5484
- https://zenodo.org/record/8124074
- http://publica.fraunhofer.de/documents/N-502802.html
- https://etd.ohiolink.edu/%21etd.send_file?accession%3Dosu1167587930%26disposition%3Dinline
- http://hdl.handle.net/11389/29357
- https://zenodo.org/record/7466455
- https://doaj.org/article/19e4186e21594dcf853a57868c464810
- http://dx.doi.org/10.1109/ACCESS.2019.2925010
- https://library.wur.nl/WebQuery/wurpubs/545332
- https://doi.org/10.3233/WOR-2012-0443-2208
- https://digitalcommons.usu.edu/aggieair_pres/59
- https://eprint.iacr.org/2023/1503
- https://research.gold.ac.uk/id/eprint/31943/1/1-s2.0-S1574954122001066-main.pdf
- https://ir.lib.uwo.ca/iipj/vol5/iss4/1
- http://hdl.handle.net/10138/347230
- https://figshare.com/articles/WiseEye_Next_Generation_Expandable_and_Programmable_Camera_Trap_Platform_for_Wildlife_Research/4543510
- http://hdl.handle.net/11349/6721
- http://digital.library.unt.edu/ark:/67531/metadc299861/
- http://infoscience.epfl.ch/record/225757
- https://research.utwente.nl/en/publications/innovative-remote-sensing-methodologies-for-kenyan-land-tenure-mapping(0899df37-fd49-4ce1-8257-eb4dd6f342a3).html
- https://doi.org/10.23919/ICCAS52745.2021.9649961
- http://apo.org.au/node/9011
- https://serval.unil.ch/notice/serval:BIB_497AD28159A3
- https://eprints.utas.edu.au/26300/
- https://hdl.handle.net/1721.1/131728
- https://zenodo.org/record/3560063
- http://pqdtopen.proquest.com/#viewpdf?dispub=3252817
- https://doaj.org/article/8f6bd616134e4b8b84867e53ee95f947
- https://publiscologne.th-koeln.de/frontdoor/index/index/docId/1127
- http://hdl.handle.net/11582/323008
- https://digitalcommons.law.uw.edu/faculty-books/90
- http://hdl.handle.net/10150/624737
- http://hdl.handle.net/2078.1/225830
- https://dx.doi.org/10.3390/proceedings2191230
- https://zenodo.org/record/4279862
- https://doaj.org/article/18204f42b04f4f04ac61da1735cc38fd
- http://eprints.utm.my/id/eprint/52665/
- http://library.wur.nl/WebQuery/wurpubs/545332
- http://urn.kb.se/resolve?urn=urn:nbn:se:lnu:diva-104952
- http://hdl.handle.net/10068/802005
- http://hdl.handle.net/11380/1068199
- http://hdl.handle.net/10070/265404
- https://digitalcommons.wcl.american.edu/facsch_bk_contributions/78
- https://doaj.org/article/1cd7029ebcfb4fffa8de61c25790f82d
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-177483
- https://zenodo.org/record/4423119
- https://researchonline.jcu.edu.au/62446/1/Ruaro%20et%20al.%202020-Brazilian-parks-Imperiled.pdf
- https://pure.qub.ac.uk/en/publications/aa7e0075-821b-457b-8a1f-dd07ff45ca74
- http://www.iucnworldconservationcongress.org
- https://doaj.org/article/91d7e3405a0a4bf7a6a621d889f4186d
- http://hdl.handle.net/2117/327883
- http://hdl.handle.net/2042/53988
- https://doi.org/10.1109/JIOT.2022.3171237
- https://zenodo.org/record/4637946
- https://hal.archives-ouvertes.fr/hal-01297912
- http://hdl.handle.net/10355/9303
- https://issuelab.org/permalink/resource/34732
- https://www.neliti.com/publications/554858/development-of-an-advanced-method-of-video-information-resource-compression-in-n
- https://norma.ncirl.ie/4283/
- http://ijcsit.com/docs/Volume+5/vol5issue06/ijcsit20140506251.pdf
- https://doaj.org/article/ed112b546db54a73a1e875512f41c36b
- https://hal.archives-ouvertes.fr/hal-01294557
- https://opensiuc.lib.siu.edu/theses/2438
- http://hdl.handle.net/10261/256186
- https://digitalcommons.unl.edu/lawfacpub/21
- https://doaj.org/article/67b915fea6b94ef2b6491518c34b6e4d
- http://www.jait.us/index.php?m=content&c=index&a=show&catid=191&id=1057
- https://digitalcommons.usf.edu/sustainable_futures/210
- http://www.seas.ucla.edu/~pottie/papers/3713-34NoFigs.pdf
- https://zenodo.org/record/4066615
- http://www.teses.usp.br/teses/disponiveis/91/91131/tde-30082019-163551/
- https://pdxscholar.library.pdx.edu/cgi/viewcontent.cgi?article=1293&amp;context=compsci_fac
- https://eprints.bournemouth.ac.uk/37900/1/Drone_One_Elsevier.pdf
- https://doaj.org/article/4531cdda7c9042fab93741da4b548fa9
- http://publica.fraunhofer.de/documents/N-216058.html
- https://doaj.org/article/b7ef9a7118a34343929f8cb7ebb5e476
- http://hdl.handle.net/20.500.11797/RP2089
- https://hdl.handle.net/10356/140306
- https://openlibrary.telkomuniversity.ac.id/pustaka/154792/integrasi-drone-dengan-floating-robot-untuk-monitoring-di-sungai-pendaratan-drone-secara-otomatis-di-atas-sungai-.html
- https://openprairie.sdstate.edu/etd/2485
- https://napier-repository.worktribe.com/file/2817546/1/A%20Blockchain%20Framework%20In%20Post-Quantum%20Decentralization%20%28accepted%20version%29
- http://home.elka.pw.edu.pl/~mpaszta/wstep/protokoly/PEGASIS_Power_Efficient_GAthering_in_Sensor_Information_Systems.pdf
- http://www.mirlab.org/conference_papers/International_Conference/ICASSP%202011/pdfs/0003980.pdf
- http://www.nusl.cz/ntk/nusl-398094
- https://doaj.org/article/6c142b13346e462b833fc6d90cb0e954
- https://zenodo.org/record/4902949
- https://hal.inrae.fr/hal-03548551
- https://tel.archives-ouvertes.fr/tel-01271795
- http://hdl.handle.net/11583/2969541
- https://dx.doi.org/10.3390/s16010097
- http://urn.kb.se/resolve?urn=urn:nbn:se:hh:diva-40459
- https://digitalcommons.law.uidaho.edu/facw_books/59
- http://hdl.handle.net/10070/86976
- http://hdl.handle.net/2142/99078
- https://doaj.org/article/a6ee5b00f9ed4be19f06a0427dc7f1ca
- http://www.sciencedirect.com.proxy1.dom1.nhtv.nl/science/article/pii/S096456911300104X
- http://hdl.handle.net/10161/12150
- http://www.suaire.sua.ac.tz/handle/123456789/2936
- https://dialnet.unirioja.es/servlet/oaiart?codigo=5975452
- http://hdl.handle.net/10945/65766
- https://halshs.archives-ouvertes.fr/halshs-01837886
- http://users.auth.gr/drazioti/lattice_1.pdf
- https://hal.inria.fr/hal-01180899
- http://www.ivt-rj.net/sapis/2006/pdf/JeanPierreBriot.pdf
- https://doaj.org/article/2329671c69ce4d25b3ab58ea71890b99
- https://online-journals.org/index.php/i-jim/article/view/35549
- http://hdl.handle.net/10356/68532
- https://lib.dr.iastate.edu/language_pubs/208
- https://zenodo.org/record/8037447
- http://hdl.handle.net/11585/800223
- http://hdl.handle.net/2148/1353
- https://elib.dlr.de/111772/1/thesis.pdf
- https://digitalcommons.usmalibrary.org/presentations/13
- https://digitalcommons.usf.edu/jea/vol14/iss1/2
- https://www.utupub.fi/handle/10024/157235
- https://doaj.org/article/5b9df8647fad4a7dbf69ab567c1d105f
- https://zenodo.org/record/8278460
- http://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15740-f03/public/suggested_papers/sensors/zebranet_asplos02.pdf
- https://doi.org/
- https://pub.uni-bielefeld.de/download/2964199/2964200
- https://zenodo.org/record/7996090
- https://doaj.org/article/59e2678eeb324e6dac1fd98da7256c28
- http://hdl.handle.net/10722/86108
- https://doaj.org/article/231e3f11fa86457fa7cb33220e42abd2
- https://hal.archives-ouvertes.fr/hal-01299549
- https://dialnet.unirioja.es/servlet/oaiart?codigo=5118214
- https://espace.library.uq.edu.au/view/UQ:176608
- https://digitalcommons.usf.edu/sustainable_futures/205
- http://arxiv.org/abs/2202.06877
- http://hdl.handle.net/11693/27993
- http://hdl.handle.net/10092/2337
- https://doaj.org/article/0acee152af434e978fd977e17d485abd
- http://hdl.handle.net/10453/150513
- https://elib.dlr.de/119980/
- https://doaj.org/article/58504d7270eb4176b9041c51854de8e6
- https://issuelab.org/permalink/resource/33365
- https://library.wur.nl/WebQuery/wurpubs/538940
- http://link.springer.com/content/pdf/10.1007/978-3-642-36642-0_19.pdf
- http://boufounos.com/Publications/B_ICASSP11_US.pdf
- http://irep.iium.edu.my/2313/
- http://hdl.handle.net/1928/27254
- http://hdl.handle.net/11025/35598
- https://monami.hs-mittweida.de/frontdoor/index/index/docId/11863
- https://doaj.org/article/aa6805bb87424820a52d812da35267f4
- https://espace.library.uq.edu.au/view/UQ:0d349a3
- http://hdl.handle.net/10.26181/23682672.v1
- https://drops.dagstuhl.de/opus/volltexte/2017/8016/
- http://eujournal.org/index.php/esj/article/download/2120/2033/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.1052.9622
- https://zenodo.org/record/8092269
- https://hal.archives-ouvertes.fr/hal-01305998
- https://espace.library.uq.edu.au/view/UQ:297011
- https://openprairie.sdstate.edu/datascience_symposium/2018/posters/14
- https://research.wur.nl/en/publications/use-cases-and-future-prospects-of-blockchain-applications-in-glob
- https://scholarbank.nus.edu.sg/handle/10635/217677
- https://hal.inria.fr/hal-03512784
- http://urn.kb.se/resolve?urn=urn:nbn:se:hh:diva-42141
- https://hal.archives-ouvertes.fr/hal-03621589
- https://eprints.ugd.edu.mk/20450/
- https://digitalcommons.lib.uconn.edu/context/dissertations/article/7748/viewcontent/thesis.pdf
- http://orbilu.uni.lu/handle/10993/28474
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll89/id/77414
- http://arxiv.org/abs/2207.01927
- https://hdl.handle.net/1887/138563
- http://apo.org.au/node/20699
- https://ojs.lib.uwo.ca/index.php/iipj/article/view/7440
- http://www.esto.nasa.gov/conferences/estc2003/papers/A7P4(Tanner).pdf
- http://op.niscair.res.in/index.php/IJTK/article/view/47670
- https://dare.uva.nl/personal/pure/en/publications/optimizing-observing-strategies-for-monitoring-animals-using-dronemounted-thermal-infrared-cameras(c7f63da6-517b-418b-b032-43f6b296a2a7).html
- http://utouch.cpsc.ucalgary.ca/docs/LandNavigation-CHI2014.pdf
- https://doi.org/10.1109/ICDSP.2013.6622711
- https://doi.org/10.1051/e3sconf/202341903008
- https://doaj.org/article/992cb261229449f49fc7adfc7d0b23c8
- https://tches.iacr.org/index.php/TCHES/article/view/8591
- https://doaj.org/article/3f8342b5074a433e8baa8fff66ed20ca
- https://digitalcommons.usf.edu/cgi/viewcontent.cgi?article=1200&amp;context=sustainable_futures
- http://hdl.handle.net/20.500.126780000002679
- https://hdl.handle.net/10356/148894
- https://ink.library.smu.edu.sg/sis_research/7545
- https://dx.doi.org/10.3390/s120912126
- https://hal.archives-ouvertes.fr/hal-01743360
- http://ir.sia.cn/handle/173321/8157
- https://zenodo.org/record/7808191
- https://zenodo.org/record/1043234
- https://hal.archives-ouvertes.fr/hal-01306205
- http://hdl.handle.net/11349/13991
- http://www.revistaiberoamericana.org/ojs/index.php/ibero/article/view/2528
- http://hdl.handle.net/10.26174/thesis.lboro.21379542.v1
- https://eujournal.org/index.php/esj/article/view/2120
- https://researchonline.gcu.ac.uk/en/publications/c8bfd70a-3b40-4806-8d38-b5c1e0ba22dd
- http://hdl.handle.net/11349/13072
- https://hal.archives-ouvertes.fr/hal-00830038/document
- https://doi.org/10.1109/ICUAS51884.2021.9476825
- https://e-space.mmu.ac.uk/view/creators/Jung=3ATH=3A=3A.html
- https://doaj.org/article/d63c7a69d2f94b18ae5c2cfb775a941f
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-98704
- https://escholarship.org/uc/item/4g84d17x
- https://scholarworks.umt.edu/etd/1140
- https://zenodo.org/record/6278379
- https://doi.org/10.1109/ICA-SYMP50206.2021.9358449
- https://escholarship.org/uc/item/7dk329xm
- http://ir.psych.ac.cn:8080/handle/311026/5976
- https://hdl.handle.net/11250/2783635
- http://ieeexplore.ieee.org/xpl/conferences.jsp
- http://dx.doi.org/10.1016/j.landurbplan.2013.02.010
- http://eprints.gla.ac.uk/view/journal_volume/IEEE_Wireless_Communications_Letters.html
- https://eprints.lincoln.ac.uk/id/eprint/42421/1/2018_EBCCSP_Moyes_et_al.pdf
- http://sbgames.org/papers/sbgames09/computing/full/cp7_09.pdf
- https://research.wur.nl/en/publications/perspectives-in-machine-learning-for-wildlife-conservation
- http://doi.org/10.5255/UKDA-SN-7185-1
- https://zenodo.org/record/1491568
- https://doaj.org/article/9bf96d5862584ed2ae897da1bc92557b
- http://nrs.harvard.edu/urn-3:HUL.InstRepos:37298550
- http://purl.umn.edu/61688
- https://computerresearch.org/index.php/computer/article/view/271
- http://hdl.handle.net/2134/24950
- https://zenodo.org/record/7332566
- http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp?punumber=6663375
- http://hdl.handle.net/10400.22/16585
- http://hdl.handle.net/2060/20080040976