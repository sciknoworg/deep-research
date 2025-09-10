# InsideOut: Debiased Emotional Dialogue Generation with a Multi-Agent System  
_v.2025-09-04_  

---

## 1  Executive Overview
InsideOut is an architectural blueprint and empirical research programme aimed at producing **dialogue agents that (i) express and recognise emotion, (ii) actively debias their own outputs, and (iii) co-ordinate through a multi-agent system (MAS)**.  
The present report synthesises **82 primary findings (“learnings”)** collected during the scoping study (2012-2025) and translates them into a detailed design, evaluation and deployment plan.  

Key take-aways
* **Multi-modal perception** (speech, vision, physiology) remains indispensable; fusion boosts accuracy by 5–25 pp versus the best single channel.  
* **Bias manifests at all levels**—data, metrics, optimisation and interaction loops.  
* **Licensing and privacy** issues (e.g.	modular DOIs, CC BY 4.0 vs “permissible closed-use”) dictate strict data-governance pipelines.  
* **PAD space + EmotionML** have emerged as the lingua franca for inter-agent affect exchange.  
* **Federated + differentially-private learning** is technically viable for mental-health scenarios that ban raw-data pooling.  
* In mental-health and customer-care use-cases **gender-sensitive calibration** and **uncertainty/disengagement detection** deliver the largest real-world gains.  

---

## 2  Background and Motivation
### 2.1  The Problem Space
Most open-domain LLM chatbots **hallucinate affect, amplify demographic biases and ignore interaction-level uncertainty**.  

### 2.2  Lessons from Related Work
1. **Demographic bias**: A disengagement-adaptive SDS helped men but _not_ women (ACL W14-4324).  
2. **Modality bias**: Gender-specific models beat generic ones by up to 12 pp (phoneme, EEG).  
3. **Metric instability**: BLEU, MERT, AMBER, METEOR variants show seed/implementation variance; robust evaluation is non-trivial.  
4. **Reproducibility**: ReproGen 2022 highlighted serious fragility in dialogue-metric pipelines.  

---

## 3  InsideOut System Architecture
### 3.1  High-Level Blocks
```
                ┌──────────────────────┐
 Sensors        │  Perception Layer    │ ← speech, video, EEG/EDA/PPG, eye-gaze
                └─────────┬────────────┘
                          │ PAD vector + sparse uncertainty
                ┌─────────▼────────────┐
 Affect Fusion  │  Multimodal Core     │ – dual-level attention, DoCM, sADDi
                └─────────┬────────────┘
                          │ EmotionML packets (category + PAD)
                ┌─────────▼────────────┐
 MAS            │  Agent Society       │ – planner, critics, debias agents
                └─────────┬────────────┘
                          │ KQML/FIPA-ACL + affect tags
                ┌─────────▼────────────┐
 NLG            │  Dialogue Generator  │ – InsideOut LLM, Dirichlet-prior loss
                └─────────┬────────────┘
                          │ text + prosody codes
                ┌─────────▼────────────┐
 TTS/Animation  │  Embodied Output     │ – PAD→PEP→facial, speech synthesis
                └──────────────────────┘
```

### 3.2  Multi-Agent Roles
| Role | Core Responsibility | Key Techniques |
|------|---------------------|----------------|
| **Perceptor** | Sensor fusion; outputs PAD-space estimate & uncertainty. | Dual-attention AV (CCC 0.72), DoCM EEG, i-vector→SER. |
| **Bias Auditor** | Monitors demographic & affective bias in generated utterances. | Annotator-disagreement priors; KL+Bayesian loss. |
| **Emotion Coach** | Decides target emotion trajectory (e.g.	de-escalation). | OCC-based appraisal, Wizard-of-Oz strategy library. |
| **Debias Critic** | Injects counterfactuals, re-ranks NLG beams. | Perspective-taking pragmatic focus; parity constraints. |
| **Dialogue Manager** | Maintains state, negotiates with other agents. | Ontology-backed FIPA-ACL with EmotionML payloads. |
| **Policy Scheduler** | Applies reinforcement/federated updates. | sADDi, federated DP, Hyperledger Aries creds. |

### 3.3  Communication Layer
* **KQML/FIPA-ACL Ext.** enriched with `:<emotionML>` slot.  
* Formal semantics verified in OWL 2 DL reasoner (Dynamic T-Box).  
* The PAD Negotiation Model maps utility deltas into PAD so that agents can bargain while exhibiting human-like affect.  

---

## 4  Debiasing and Emotion Control Techniques
### 4.1  Data-Level
* **Balanced sampling** across gender, language, modality (HUMOD, IEMOCAP, MSP-Podcast, HUMOD 3-D MoCap).  
* **Label ambiguity embrace**: Utterance-specific Dirichlet priors to keep multiple valid emotion labels alive.  
* **Synthetic oversampling** guided by OCC appraisal trajectories.  

### 4.2  Model-Level
1. **Dirichlet+KL Objective** – mirrors annotator disagreement, yields SOTA UAR & AUPRC.  
2. **sADDi self-supervision** – domain-invariant latent space, cross-corpus SOTA.  
3. **Emotion-conditioned LM** – conditioning GPT-style probabilities on prosody-derived continuous PAD (−1.35 % perplexity, Switchboard).  
4. **Explicit Uncertainty Head** – Bayesian weights + Monte-Carlo dropout.  

### 4.3  Decoding-Level
* **Perspective & Pragmatics** module highlights cause words; improves empathy (ACL 2021).  
* **Debias Re-ranking** uses parity constraints (gender, valence).  
* **Overgeneration vs Classification-and-Ranking**: For intention-labelled corpora (theatre dataset) C&R hits 91 % vs 68 % for NLG overgen.  

### 4.4  Interaction-Level
* **Dynamic Strategy Switching**: Wizard-of-Oz study shows that coupling disengagement & uncertainty detection increases task success across genders (Pitt 2014) ‑> implemented as a policy in the Emotion Coach.  
* **Negotiation Affects** via PAD Emotional Negotiation Model preserve concession frequencies while boosting perceived warmth.  

---

## 5  Perception: Multimodal Affect Fusion
| Modality | SOTA/Key Result | Notes |
|----------|-----------------|-------|
| **Audio** | WavLM+TCN detects gender 97.9 %, overlap SOTA. | Transfer to SER. |
| **Vision** | InceptionV3 92.78 % facial affect; compass-map optical flow flags negative valence. | Gender bias in cues. |
| **Physiology** | PPG artefact-corrected HRV ↑ accuracy 18 pp; EEG DoCM flex-index outperforms band-power; foot GSR viable (r≈0.8); glasses-type fusion +8.46 pp. | Useful for mental-health. |
| **Eye-Gaze** | Pupillary + saccade features beat speech for V-A and cut ASR WER. | Adds robustness. |

**Fusion gains**
* Audio–facial SVR RMSE ≈ 0.29 (SEMAINE); Bayesian tri-modal fusion ↑7–10 pp UAR compared to best solo channel.  
* Feature-level PAD-vector fusion yields cross-modality interoperability and correlates with temperament scores.  

---

## 6  Evaluation Protocols
### 6.1  Datasets & Licences
* **GORDAN 1.0** raw audio/video (separate DOI for transcripts) – highlights modular licence strategy.  
* **HUMOD** (dialogue) + HUMOD 3-D MoCap (movement) – open access.  
* **SEMAINE, AVEC 2013/14**, IEMOCAP, RECOLA – emotion corpora.  
* **Hudup/FilmTrust** – recommender bias tests (licence unclear!).  
* **Zacchiroli FOSS licence corpus** – used to audit legal-text bias.  
* All new InsideOut data will be released under **CC BY 4.0** in line with IPCC 2022 recommendations; code under OSI-approved licence.  

### 6.2  Metrics
1. **METEOR-NEXT / m-BLEU / m-TER** for textual quality.  
2. **CCC / RMSE / UAR** for affect regression/classification.  
3. **Fairness Gaps** by gender, language, emotion quadrant.  
4. **Uncertainty AUPRC** for high-entropy utterances.  
5. **Seed-Robust MERT** variants mitigate optimisation variance.  

### 6.3  Human-in-the-Loop Protocols
* Double-confidential federated learning + verifiable creds ensure judges never see private data.  
* Eye-tracking load-manipulation (McGurk dual-task) to test cognitive load effects on perception of InsideOut outputs.  

---

## 7  Reproducibility & Deployment Pipelines
| Layer | Reprod. Asset | Notes |
|-------|--------------|------|
| Data  | MAAS PAD-XML, EmotionML files, sensor raw streams. | Upload to CEDA-style closed-use if needed. |
| Training | Docker + Snakemake; seeds logged; Foster et al. MERT fixes. | ReproGen-compliant. |
| Privacy | Federated + DP; raw stays on device; only DP KPIs to managers. | Aligns with GDPR + RA 11036. |
| Evaluation | Open-sourced metric implementations; variance reported. | Avoids metric drift. |

Hardware: Real-time prototypes verified on **Emotiv Epoch**, **Shimmer3**, **Empatica E4**, Intel RealSense, Muse EEG; computation off-loaded to edge GPU or phone (OpenVINO).  

---

## 8  Application Domains
### 8.1  Mental-Health Conversational Care
* WHO 2022: 15 % of workforce has mental disorders.  
* Philippines case: 53 % employees affected → RA 11036 & DOLE 208 mandate corporate mental-health programmes.  
* Functional gap: 80 % B2B SaaS lack manager dashboards → InsideOut can surface anonymised KPIs.  
* Debias focus: gender-specific calibration, uncertainty mitigation.  

### 8.2  Customer Service / TELCO
* Disengagement detection reduces churn; decision-level Bayesian fusion flagged neutral states poorly (30–40 % accuracy) → refine neutrality detectors.  

### 8.3  Group Decision Support
* ABS4GD 2008 demonstrated that MAS with emotional profiles improves fidelity of committee simulations; InsideOut extends this to live human-agent hybrid meetings.  

### 8.4  Licensing Advisory Chatbots
* Combines dialogue NLG with the 6.5 M-licence corpus; Paraphrase-aware metrics (METEOR/PARMESAN) safeguard textual similarity while retaining legal meaning.  

---

## 9  Risk, Ethics & Compliance
* **Differential privacy**: smartphone FL + DP-SGLD proven viable (2023 preprint).  
* **Role-based dashboards & generalisation** per privacy-by-design patterns (MUSES, Fraunhofer).  
* **Emotion manipulation**: integrate explicit opt-in & explainable logs; Wizard-of-Oz framework benchmarks ethical strategies.  
* **Licensing**: Use CC BY 4.0; fall back to CUGL/CUNCGL when onward sharing restricted.  

---

## 10  Roadmap and Open Research Questions
| Phase | Milestone | Dependencies |
|-------|-----------|--------------|
| Q4 2025 | MVP: speech-only biased-aware GPT head fine-tuned with Dirichlet loss. | HUMOD, IEMOCAP; METEOR-NEXT metrics; gender calibration. |
| Q2 2026 | Multimodal Perceptor with dual-attention AV + DoCM EEG; PAD fusion. | RealSense D435, Muse EEG; MAAS. |
| Q4 2026 | Full MAS with Bias Auditor + Debias Critic; OWL reasoning online. | FIPA-ACL ext., Dynamic T-Box. |
| 2027 | Federated roll-out to enterprise mental-health SaaS; DP dashboards. | Hyperledger Aries, RA 11036 compliance. |

Open questions
1. **Neutrality detection** remains weak (30–40 % accuracy).  
2. **Cross-gender speech enhancement**: Bayesian fusion of emotion-specific LPC codebooks promising but untested at scale.  
3. **Cognitive-load adaptation**: integrate dual-task McGurk insights into real-time bandwidth allocation.  
4. **Planetary-scale N-body surrogate** (COMET, Oort-cloud findings) suggest transfer of Gaussian-process emulators to MAS negotiation cost prediction—needs exploration.  

---

## 11  Contrarian / Speculative Ideas (Flagged)
* **Bound Jovian-mass solar companion** hypothesis (Oort-cloud over-population) inspires _meta-dialogue_ scenario: treat extreme outlier user emotions as evidence of hidden ‘companion’ contexts; an unsupervised outlier detector could trigger policy escalation. _Speculative._  
* **Max-style 3-axis agents** (emotion, mood, boredom) might outperform PAD-only for long-running mental-health coaching. _Needs empirical proof._  
* **Eye-gaze-guided diarisation** hints at shifting some traditional NLP turn-taking tasks to computer-vision indices—contrary to speech-first orthodoxy.  

---

## 12  Conclusion
InsideOut fuses **state-of-the-art multimodal affect sensing, rigorous debiasing, and verifiable agent communication** into a coherent, privacy-respecting framework fit for sensitive domains such as corporate mental-health support.  
The compiled evidence base—from sensor fusion to licensing schemas—provides both a **blueprint and a realistic execution plan**.  
Key differentiators are:  
1. **End-to-end debias loop** spanning data→optimisation→interaction.  
2. **Interoperable affect semantics** via PAD & EmotionML in FIPA-ACL.  
3. **Federated, DP-protected deployment** aligned with emerging regulation.  
4. **Gap-filling dashboards and negotiation protocols** absent in 80 % of current SaaS.  

With disciplined adherence to the above architecture, InsideOut can become a reference platform for **emotionally intelligent, bias-aware conversational AI** by 2027.


## Sources

- http://sail.usc.edu/%7Emetallin/papers/metallinou_multimodal_icassp10.pdf
- http://dspace.kpfu.ru/xmlui/handle/net/96191
- http://arxiv.org/abs/2203.04443
- http://hdl.handle.net/11566/294230
- https://zenodo.org/record/7439586
- https://archive-ouverte.unige.ch/unige:78565
- https://doi.org/10.1109/icip40778.2020.9191019
- http://www.ucs.louisiana.edu/%7Ejjm9638/acm2002/acm2002_05_06.pdf
- http://www.statmt.org/wmt09/pdf/WMT-0939.pdf
- http://www.aaai.org/Papers/Symposia/Spring/2004/SS-04-02/SS04-02-002.pdf
- http://publica.fraunhofer.de/documents/N-229308.html
- https://hal.archives-ouvertes.fr/hal-00371958
- http://i-rep.emu.edu.tr:8080/jspui/bitstream/11129/205/1/Mayboudi.pdf
- https://pub.uni-bielefeld.de/record/1607115
- http://hdl.handle.net/10810/25696
- http://hdl.handle.net/10292/8131
- http://hdl.handle.net/10261/336573
- https://research.rug.nl/en/publications/c6bb978d-29b3-4684-9c9d-0dbcef034545
- http://hcsi.cs.tsinghua.edu.cn/Paper/Paper10/JiaJia_ICAI2010.pdf
- http://hcsi.cs.tsinghua.edu.cn/Paper/paper08/4.pdf
- https://doaj.org/article/13b5827826334af4a5954926f833707e
- http://dspace.library.iitb.ac.in/xmlui/handle/10054/16404
- http://hdl.handle.net/10292/17204
- https://stars.library.ucf.edu/scopus2000/4803
- http://hdl.handle.net/11562/337911
- https://zenodo.org/record/7431834
- http://www.people.usi.ch/fornaran/papers/ACL_OWL_EUMAS2011.pdf
- http://researchdata.gla.ac.uk/view/author/3453.html
- https://doaj.org/article/12b34c85f3f747388796d738669ef1ed
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/7b/02/12913_2016_Article_1267.PMC4717621.pdf
- https://doaj.org/article/77cde2b43f4849f88ec4b6d596dd89ca
- http://hdl.handle.net/1721.1/16621
- https://cris.maastrichtuniversity.nl/en/publications/4bd5bd16-ad2c-481a-a303-ab150f3cd459
- http://sail.usc.edu/%7Emalandra/files/papers/icassp2014.pdf
- http://hdl.handle.net/11311/1079991
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.87.2373
- https://zenodo.org/record/3554229
- http://www.kyb.tuebingen.mpg.de/fileadmin/user_upload/files/publications/mpik-tr-158_%5B0%5D.pdf
- https://research.tilburguniversity.edu/en/publications/0a74ace0-f2e7-4d07-b6d4-ac8bafbaa9df
- https://animorepository.dlsu.edu.ph/etdm_market/67
- http://paper.ijcsns.org/07_book/200812/20081236.pdf
- http://www.mt-archive.info/WMT-2009-Foster.pdf
- https://zenodo.org/record/7419789
- https://doi.org/10.1109/ICASSP49357.2023.10094673
- https://www.drugsandalcohol.ie/30291/
- https://hal.archives-ouvertes.fr/hal-00519715
- http://hdl.handle.net/10.1371/journal.pone.0279997.t005
- http://www.metz.supelec.fr//metz/personnel/geist_mat/pdfs/Supelec764.pdf
- https://zenodo.org/record/5919444
- http://hdl.handle.net/1885/272904
- https://animorepository.dlsu.edu.ph/faculty_research/1280
- https://dspace.library.uu.nl/handle/1874/415009
- https://doaj.org/toc/2414-4088
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA512059%26Location%3DU2%26doc%3DGetTRDoc.pdf
- https://research.rug.nl/en/publications/a6fd5af8-a5a0-4302-bf40-9f60d8ad79a0
- https://ojs.aaai.org/index.php/AAAI/article/view/16743
- https://hal.archives-ouvertes.fr/hal-03770634/file/Interspeech2022_v5.pdf
- http://www.cs.cmu.edu/%7Emdenkows/pdf/meteor-1.5.pdf
- http://hdl.handle.net/10536/DRO/DU:30096306
- https://www.aaai.org/Papers/Symposia/Spring/2008/SS-08-04/SS08-04-015.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.92.5461
- http://hdl.handle.net/10400.22/1674
- https://www.tu-ilmenau.de/fileadmin/media/neurob/publications/conferences_int/2003/Schauer-DAGM-03.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:hh:diva-36499
- http://www.centreformentalhealth.org.uk/pdfs/Mental_health_workforce_for_the_future.pdf
- http://hdl.handle.net/10356/66620
- https://hal.science/hal-01530763
- http://hdl.handle.net/2142/21085
- http://publica.fraunhofer.de/documents/N-552618.html
- http://hdl.handle.net/10220/12706
- https://orcid.org/0000-0002-0506-2409
- http://publica.fraunhofer.de/documents/N-188980.html
- http://repository.cmu.edu/cgi/viewcontent.cgi?article%3D1131%26context%3Dlti
- https://research.vu.nl/en/publications/bb0b0818-1992-40e1-bc78-f6fc8f405a62
- https://figshare.com/articles/_Mean_and_variance_of_the_Canberra_stability_indicator_over_10_replicates_for_sets_with_random_lists_with_features_/309293
- https://research.utwente.nl/en/publications/do-you-want-to-talk-about-it(605e6d44-f16d-4758-93e6-95f9361e6a11).html
- https://napier-repository.worktribe.com/file/2756513/1/Privacy%20And%20Trust%20Redefined%20In%20Federated%20Machine%20Learning
- https://doaj.org/article/db061a8f3bee4ca49c81099555bd1490
- http://www.di.unito.it/~argo/papers/2012_IA_IOS.pdf
- http://publications.jrc.ec.europa.eu/repository/handle/JRC93830
- http://d-scholarship.pitt.edu/22882/
- https://hdl.handle.net/10356/148092
- http://etheses.bham.ac.uk//id/eprint/9405/1/Alhargan2019PhD.pdf
- http://hdl.handle.net/2013/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/132737
- http://users.utcluj.ro/%7Ebenta/EATIS07_Benta.pdf
- http://www.cs.usask.ca/%7Ecroy/papers/2013/MondalACR2012Stability.pdf
- https://doi.org/10.1016/j.neucom.2017.09.049
- http://hdl.handle.net/10.1184/r1/6473054.v1
- https://zenodo.org/record/7322305
- http://d-scholarship.pitt.edu/22677/
- https://surrey.eprints-hosting.org/837608/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.53.7958
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:201043
- http://hdl.handle.net/10356/45380
- http://etd.uwc.ac.za/xmlui/bitstream/handle/11394/2353/Mabeka_LLM_2008.pdf%3Bjsessionid%3D19B9A98192B4F36CEC2E0116BD24491B?sequence%3D1
- https://doaj.org/article/5982bf0a41e2423cbd778b53039254f0
- https://zenodo.org/record/1885
- http://dx.doi.org/10.1109/JIOT.2020.3037207
- https://scholarlycommons.pacific.edu/esob-facarticles/153
- https://doaj.org/toc/1932-6203
- https://pub.uni-bielefeld.de/record/1857757
- https://dx.doi.org/10.3390/s120506075
- https://doi.org/10.1007/11573548_65
- http://hdl.handle.net/20.500.11937/80264
- https://hal.archives-ouvertes.fr/hal-02128846/document
- https://digitalcommons.lsu.edu/gradschool_dissertations/4243
- http://www.aaai.org/Papers/Symposia/Spring/1995/SS-95-06/SS95-06-026.pdf
- https://research.tue.nl/nl/publications/35552766-4e86-45e5-b88e-126fd0160abe
- http://wwwdh.cs.fau.de/IMMD8/Publications/DynTBoxOWLDL.pdf
- https://serval.unil.ch/notice/serval:BIB_62A464849206
- https://doaj.org/article/0fedea5f94f04f35b7c494ae5a7f8236
- https://scholarworks.utep.edu/dissertations/AAI3566544
- https://lirias.kuleuven.be/handle/123456789/396201
- http://publica.fraunhofer.de/documents/N-63647.html
- http://handle.westernsydney.edu.au:8081/1959.7/uws:49177
- https://zenodo.org/record/4746602
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.77.3264
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.610
- https://hal.science/hal-03081727
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.6115
- https://nrc-publications.canada.ca/fra/voir/objet/?id=493f767b-84cf-4ecb-b6f9-2f779e258000
- https://zenodo.org/record/4010763
- https://hal.archives-ouvertes.fr/hal-03215168/document
- https://zenodo.org/record/6998104
- https://animorepository.dlsu.edu.ph/cgi/viewcontent.cgi?article=13106&amp;context=etd_masteral
- https://doaj.org/article/73314969919240a0b38d2a9d5d84d5ad
- https://zenodo.org/record/5075094
- http://web.eecs.utk.edu/%7Esli22/resources/2013-emotion-sensing-pub.pdf
- http://www.mt-archive.info/ACL-SMT-2008-Agarwal.pdf
- http://hdl.handle.net/11858/00-001M-0000-0013-B706-4
- https://zenodo.org/record/6379164
- https://hdl.handle.net/11323/8410
- https://zenodo.org/record/7347647
- http://dx.doi.org/10.1145/2927006.2927008
- https://zenodo.org/record/8327452
- http://www.nusl.cz/ntk/nusl-218117
- https://www.tdcommons.org/dpubs_series/5066
- http://arxiv.org/abs/2011.10916
- http://arxiv.org/abs/2309.04849
- http://bnaic.liacs.leidenuniv.nl/bnaic2020proceedings.pdf
- http://research.microsoft.com/en-us/people/gokhant/is10-3.pdf
- http://www.lrec-conf.org/proceedings/lrec2010/pdf/506_Paper.pdf
- https://repository.vu.lt/VU:ELABAPDB72651172&prefLang=en_US
- http://hdl.handle.net/10.25905/21638054.v1
- https://hal.archives-ouvertes.fr/hal-00980495
- http://publications.jrc.ec.europa.eu/repository/handle/JRC61486
- https://escholarship.org/uc/item/32b4v122
- http://hdl.handle.net/10779/DRO/DU:21130969.v1
- https://scholarworks.utep.edu/open_etd/1851
- https://zenodo.org/record/1463156
- https://doaj.org/article/ec15448d5279452086ba3516d04d344e
- http://orcid.org/0000-0001-9228-1759
- https://hdl.handle.net/20.500.12412/4166
- https://interspeech2023.org/
- http://ir.psych.ac.cn/handle/311026/14067
- https://zenodo.org/record/7197274
- https://researchrepository.murdoch.edu.au/view/author/Koutsakis,
- https://ojs.aaai.org/index.php/AAAI/article/view/26514
- http://www.statmt.org/wmt10/pdf/WMT51.pdf
- http://hdl.handle.net/20.500.11850/393230
- https://doaj.org/article/b106a430bd6d4d60b74d6281c7ceda72
- http://hdl.handle.net/10092/6071
- https://www.drugsandalcohol.ie/34669/1/MHR21_AR20_WEB.pdf
- https://zenodo.org/record/846272
- http://hdl.handle.net/10.1371/journal.pone.0214587.t008
- http://www.ijcaonline.org/volume17/number3/pxc3872794.pdf
- http://archive-ouverte.unige.ch/files/downloads/47741/unige_47741_attachment01.pdf
- https://animorepository.dlsu.edu.ph/faculty_research/902
- https://jefsr.uwindsor.ca/index.php/jefsr/article/view/4869
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.70.5429
- http://journal.frontiersin.org/researchtopic/1120/audiovisual-speech-recognition-correspondence-between-brain-and-behavior
- https://zenodo.org/record/1071510
- http://mtg.upf.edu/system/files/publications/PhD_MHaro.pdf
- http://ir.unimas.my/id/eprint/40128/2/Ramos%20Ukar%20Anak%20Yakobus%20ft.pdf
- http://delicias.dia.fi.upm.es/%7Evrodriguez/pdf/2007.10.axmedis.pdf
- http://www.iikt.ovgu.de/iesk_media/Downloads/ks/publications/papers/2009/IS2009_bv-p-4292.pdf
- https://doaj.org/article/b991b24c57b4477fa87d1c64c32eb252
- https://doaj.org/article/b13610b427404bf4b1f8aa85867b61c6
- http://www.ijpg.org/index.php/IJACSci/article/view/488/202
- https://cris.vtt.fi/en/publications/73de173c-360b-4bd8-b19a-783a4fbeefee
- http://www.site.uottawa.ca/~diana/naacl2010_EmotionWorkshop.html
- http://hdl.handle.net/10.3389/fnhum.2022.1051463.s001
- https://www.tdcommons.org/cgi/viewcontent.cgi?article=6164&amp;context=dpubs_series
- https://www.researchgate.net/profile/Marc_Cavazza/publication/224088172_PAD-based_multimodal_affective_fusion/links/0fcfd50c992af8bfef000000.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:ltu:diva-85747
- http://people.cs.pitt.edu/~forbesk/papers/spcomm11.pdf
- http://eprints.gla.ac.uk/view/journal_volume/Data_Intelligence.html
- https://openresearch.surrey.ac.uk/esploro/outputs/journalArticle/Multimodal-Information-Fusion/99512832802346
- http://hdl.handle.net/11356/1292
- http://hdl.handle.net/10068/569963
- http://cran.wustl.edu/web/packages/HistData/HistData.pdf
- https://zenodo.org/record/5505959
- http://research.ijcaonline.org/volume115/number16/pxc3902200.pdf
- https://pub.uni-bielefeld.de/record/2610101
- http://tubiblio.ulb.tu-darmstadt.de/98969/
- http://www.hathitrust.org/access_use#pd-google.
- http://paginas.fe.up.pt/~las/conteudo/pub/agentes/oliveira_sarmento_aamas03.pdf
- https://research.vu.nl/en/publications/b6574890-1714-4134-9ccc-1e78ba1bc8ef
- http://pqdtopen.proquest.com/#viewpdf?dispub=3502353
- https://qmro.qmul.ac.uk/xmlui/handle/123456789/83437
- https://ieeexplore.ieee.org/document/9478673
- http://eprints.iums.ac.ir/33346/
- https://figshare.com/articles/_Average_accuracy_comparisons_on_the_synthesized_data_/1282663
- http://hdl.handle.net/10119/16095
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.76.3865
- https://zenodo.org/record/4893369
- https://zenodo.org/record/8093448
- http://www.csit.carleton.ca/~arya/pubs/ivp.pdf
- http://eprints.utm.my/id/eprint/101092/
- https://figshare.com/articles/Dataset_for_Drivers_Manoeuvre_Classification_for_Safe_HRI/6491512
- http://publica.fraunhofer.de/documents/N-332704.html
- https://www.zora.uzh.ch/id/eprint/142379/
- http://hdl.handle.net/2123/9359
- https://www.aaai.org/Papers/Symposia/Fall/2000/FS-00-04/FS00-04-001.pdf
- https://archive-ouverte.unige.ch/unige:21731
- https://ojs.aaai.org/index.php/AAAI/article/view/5361
- http://www.aclweb.org/anthology/W/W14/W14-3345.pdf
- http://www.barnrich.ch/wiki/lib/exe/fetch.php?media%3Dpub%3A2013_towards_a_mobile_galvanic_skin_response_measurement_system_for_mentally_disordered_patients.pdf
- https://doaj.org/article/f1d1495afbd147e6b3182ed1a3df8859
- http://www.mt-archive.info/ACL-SMT-2007-Lavie.pdf
- https://www.researchgate.net/profile/Tobias_Brosch/publication/23233470_Cross-modal_emotional_attention_Emotional_voices_modulate_early_stages_of_visual_processing._Journal_of_Cognitive_Neuroscience_21_1670-1679/links/02e7e5166d82a90cbc000000.pdf
- http://www.ar.media.kyoto-u.ac.jp/EN/bib/intl/INO-INTERSP14.pdf
- https://hdl.handle.net/11566/311027
- http://hdl.handle.net/2065/40124
- http://www.loc.gov/mods/v3
- https://zenodo.org/record/5841868
- https://doaj.org/article/90ef3b24fd144c32a16700b2343cc723
- https://embs.papercept.net/conferences/conferences/EMBC17/program/EMBC17_ContentListWeb_3.html
- https://www.repository.cam.ac.uk/handle/1810/266923
- https://hdl.handle.net/10371/183773
- http://hdl.handle.net/2013/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/239393
- https://doi.org/10.1051/0004-6361/200912871
- https://figshare.com/articles/Data_on_the_licensing_of_images_made_publicly_available_at_MorphoBank/994169
- https://doaj.org/article/f3d367baf794474f8590834b5f96edd7
- http://arxiv.org/abs/2208.01070
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0960982205003404/MAIN/application/pdf/115f5b7f08ceb6adbf0b05dae224a3cc/main.pdf
- http://www.aclweb.org/anthology/W/W14/W14-4324.pdf