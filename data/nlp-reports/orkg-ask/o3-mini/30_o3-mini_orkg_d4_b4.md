# Final Report: Hierarchical Multi-Perspective Prompting Improves Factuality in Large Language Models in Specialized Domains

This report synthesizes a broad range of research findings on hierarchical multi-perspective prompting strategies and their impact on enhancing factuality in large language models (LLMs) across specialized domains such as legal, medical, technical, and beyond. The document provides an in‐depth examination of the methodological advances, hybrid frameworks, benchmarking paradigms, and empirical evaluations that collectively contribute to a robust multi-layered approach to mitigating errors and biases in LLM outputs. In doing so, it integrates lessons from simulation-based frameworks, effect size estimation methods, neural‐symbolic integration, decision theory, and multi‐criteria evaluation strategies.

---

## 1. Executive Summary

Recent developments in hierarchical and multi-perspective prompting have demonstrated that integrating multiple epistemological levels within LLM applications significantly improves factual consistency and contextual nuance, especially in domains that demand high precision such as legal reasoning, medical diagnostics, and technical document analysis. By combining simulation-based frameworks, robust statistical estimation, and hybrid neural-symbolic techniques, cutting-edge research is addressing long-standing challenges from hallucinations to evaluation biases. The Multi-Elo Rating System, dynamic LINMAP, and advanced normalization procedures have emerged as key tools for ensuring that independent evaluation dimensions (e.g., factual accuracy vs. stylistic conciseness) are independently quantified and recalibrated in real time.

---

## 2. Introduction

### 2.1 Background and Rationale

Factual fidelity in LLM outputs has often been compromised by myopic decision fragments and single-perspective designs. Recent work has shifted focus towards hierarchical prompting—a structured method that partitions reasoning tasks into subtasks across multiple epistemological layers. This approach reflects a converging trend: from traditional single-layer models to those that encapsulate socio-political, cultural, legal, and technical perspectives.

### 2.2 Scope of Specialized Domains

The application of hierarchical multi-perspective prompting is particularly compelling in several specialized domains:

- **Legal:** Enhancing transparency in decision-making by incorporating judicial principles, evidentiary reasoning, and symbolic legal theories.
- **Medical:** Integrating layered medical ontologies and historical case data to improve diagnostic reasoning and reduce biases in clinical decision support.
- **Technical:** Analyzing complex technical documentation and regulatory requirements using semantic parsing, description logic, and hierarchical abstraction.

These domains require deeply nuanced approaches where both factual accuracy and contextual sensitivity are paramount.

---

## 3. Methodological Innovations

### 3.1 Hierarchical and Multi-Perspective Modeling

Research emphasizes the need to transition from traditional single-perspective models to multi-perspective frameworks that introduce an additional epistemological level. For instance, studies from TU Delft have demonstrated that augmenting hierarchical models with socio-political and socio-cultural inputs can lead to more nuanced simulations of reality. This is mirrored in computational simulations where multi-level strategies capture complex interactions that simple models might neglect.

### 3.2 Simulation-Based Frameworks and Causal Modeling

Several works have combined simulation-based frameworks with advanced causal modeling to quantify interactions between machine reasoning and human-like decision processes. In a simulated corporate forecasting process, causal models integrated with data science methods revealed that narrowly focused assessments miss global system behaviors. These insights provide support for extending such approaches to LLM prompt design, where causal inference can capture underlying dependencies and counterintuitive outputs.

### 3.3 Robust Effect Size Estimation and Statistical Techniques

Incorporating shrinkage estimators, bootstrap bias-corrected techniques, and noncentral t-distribution based confidence intervals into hierarchical models (such as HLGM) has been critical in reducing estimation bias. By adapting these robust statistical methods to LLM frameworks, researchers are able to partition variance effectively, as observed in hierarchical linear models applied to educational assessments and transportation mode selections.

### 3.4 Neural-Symbolic Hybrid Architectures

Hybrid frameworks that integrate neural networks with symbolic reasoning represent a promising avenue, particularly in legal AI. For example, systems like LEGAL-TransformerOverBERT and other neural-symbolic methods extract concepts from legal texts and then translate them into symbolic representations, enhancing both transparency and interpretability. These approaches address critical challenges in factuality by bridging intangible abstract concepts with explicit logic rules and causal priors.

### 3.5 Advanced Evaluation and Normalization Techniques

Recent research (e.g., the Multi-Elo Rating System) has highlighted the importance of separate evaluation dimensions to avoid biases where stylistic qualities may overshadow factual correctness. Employing advanced normalization procedures, including vector normalization and linear scale transformation, ensures ranking consistency in multi-attribute decision-making frameworks. Dynamic evaluation frameworks using methods such as dynamic LINMAP further offer real-time, stakeholder-specific recalibration.

---

## 4. Empirical Evidence and Benchmarking Paradigms

### 4.1 Multi-Attribute Decision-Making (MADM) and Hierarchical Approaches

Empirical studies using Analytic Hierarchy Process (AHP) and Best Worst Method (BWM) have shown that hierarchical structuring reduces cognitive biases (e.g., equalizing bias) considerably. For instance, research involving transportation mode selections among university students confirmed that hierarchical models outperform flat aggregation strategies in minimizing bias.

### 4.2 Ensemble Disagreement Scores and Cross-Validation

Modern evaluation frameworks have leveraged ensemble disagreement scores as a proxy for human labeling accuracy. With mean average errors as low as 0.4% in certain benchmarks, these metrics suggest that ensemble methods (and even the AlignLLM strategy that employs multiple LLMs as judges) are highly effective in validating outputs without ground truth. This multidimensional evaluation not only decomposes responses into factual accuracy, style, and brevity but also supports continuous feedback loops.

### 4.3 Simulation-Based and Directed Acyclic Graph (DAG)-Modeled Benchmarks

Simulation-based and DAG-modeled scenario benchmarks (as used in DOAJ and AIBench studies) provide robust frameworks for evaluating human-AI collaborations. By blending causal models with data science algorithms, these benchmarks capture nuanced delegation roles and systemic impacts that static evaluations may overlook.

### 4.4 Advanced Normalization and Dynamic Weighting Methods

The adoption of advanced normalization techniques—such as logarithmic scales with multiplicative aggregation—and dynamic weighting (using methods like Orness for time series weighting) has been shown to balance factual accuracy against stylistic quality. Empirical integrations of these methods into LLM evaluation frameworks have demonstrated reduced cognitive biases and heightened precision in multi-stakeholder environments.

---

## 5. Domain-Specific Applications and Adaptations

### 5.1 Legal Domain Adaptations

Legal AI presents unique challenges: multiple studies indicate that mainstream neural networks often fail to incorporate foundational legal theories. Hybrid neural-symbolic frameworks have been developed to bridge this gap, combining pretrained language models with symbolic reasoning to extract legal concepts and devise transparent, rule-based decisions. Approaches such as the Transformer-Hierarchical-Attention-Multi-Extra (THME) network have successfully integrated diverse inputs (fact descriptions, defendant data, court perspectives) to enhance legal judgment predictions. Moreover, contractual AI frameworks leverage a dual-process (fast rule-checking followed by detailed analysis) methodology to minimize biases and enhance stakeholder trust.

### 5.2 Medical Domain Integration

Within the medical field, multi-layered frameworks—such as the four-tiered knowledge taxonomy (covering ontology to individual case analysis)—demonstrate the benefits of hierarchical reasoning in improving diagnostic accuracy. Systems that integrate hierarchical linear temporal logic with deep reinforcement learning have proven effective in managing real-time patient data and iteratively updating decision criteria. This stratification of medical knowledge ensures that decisions incorporate both statistical prevalence and individual patient contingencies.

### 5.3 Technical and Regulatory Settings

Technical domains require the detailed analysis of complex documentation and regulatory standards. Approaches like ModelWriter integrate semantic parsing, description logic theorem proving, and first-order relational logic to ensure traceability and consistency in technical documentation. Additionally, hierarchical graph rewriting and decoupled modular architectures (e.g., multi-core LTSmin) illustrate that separating language frontends, optimization layers, and execution backends can meet both performance and memory constraints in high-stakes technical applications.

### 5.4 Cross-Domain and Culturally Sensitive Approaches

The integration of multi-perspective frameworks is not limited to any one domain. In cross-cultural decision-making, frameworks that blend quantitative statistical models with culturally adaptive dialogue systems (using methods such as Extended Statecharts) ensure that agent behaviors remain realistic and context-sensitive. Empirical evidence from psycholinguistic and socio-cultural studies supports the use of multi-view learning to enhance system reliability across diverse cultural settings.

---

## 6. Future Directions and Research Opportunities

### 6.1 Enhanced Hybrid Neural-Symbolic Architectures

Given the scalability challenges observed in mapping neural embeddings to formal logic in large datasets (especially within legal and technical contexts), future work should explore more efficient causal inference techniques—such as counterfactual measures (e.g., Ctf-DE, Ctf-IE)—to bridge these gaps. Developing lightweight symbolic modules that complement neural networks could further improve real-time responsiveness.

### 6.2 Adaptive and Dynamic Evaluation Metrics

Emerging technologies such as AlignLLM and dynamic LINMAP suggest that real-time, adaptive weighting of evaluation criteria is both feasible and beneficial. Future frameworks could incorporate reinforcement learning methodologies that continuously adjust metrics based on feedback from ensemble models and human-in-the-loop systems, particularly in multi-stakeholder settings.

### 6.3 Expanded Cross-Domain Applications

While current research spans legal, medical, and technical domains, there is untapped potential in integrating hierarchical prompting strategies into other high-stakes environments such as financial risk assessment, public health policy, and cybersecurity. By further refining multi-perspective frameworks and embedding auxiliary inputs (e.g., domain-specific knowledge graphs), emergent systems can be both context-aware and resilient to unexpected data shifts.

### 6.4 Bridging Theoretical and Empirical Frameworks

There remains a significant opportunity to fuse rigorous theoretical models (e.g., policy-based causal decision theory) with empirical benchmarks (e.g., ensemble-based evaluation, Multi-Elo rating). A holistic benchmarking system that rigorously tests LLM outputs against multiple criteria will likely be the linchpin in advancing factual precision in LLM systems.

---

## 7. Conclusion

Hierarchical multi-perspective prompting represents a transformative leap in the quest to improve factuality and reduce bias in large language models. By integrating diverse epistemological perspectives and leveraging systems ranging from neural-symbolic hybrids to dynamic multi-attribute decision models, researchers and practitioners can now create more transparent, robust, and culturally sensitive AI systems. This report has synthesized extensive research findings—from simulation-based causal modeling and robust effect size estimation to advanced normalization techniques and cross-domain applications—to provide a comprehensive roadmap for future exploration and implementation in specialized domains.

Maintaining fidelity in fact-driven decision-making is a continually evolving challenge. However, the integration of hierarchical and multi-perspective strategies, when combined with advanced evaluative and delegation frameworks, provides a promising solution path that is as scalable as it is adaptable, ultimately paving the way for reliable, interpretable, and ethically sound AI systems.

---

*This report integrates insights from numerous advanced studies that span various domains and methodological frameworks, and it offers both detailed empirical evidence and strategic recommendations for advancing hierarchical prompting techniques in LLMs. Future research will likely expand on these foundations to capture even greater nuance and interdisciplinary depth in AI-driven decision-making.*


## Sources

- https://hdl.handle.net/1721.1/137062
- http://eprints.usq.edu.au/27912/
- http://arxiv.org/abs/2305.10235
- https://digitalcommons.unf.edu/unf_faculty_publications/1705
- https://doaj.org/article/66b3def9f6b9467f9e1b2493745e16b9
- http://www.tqmp.org/Content/vol09-1/p025/p025.pdf
- https://zenodo.org/record/2634957
- http://hdl.handle.net/10.1184/r1/6570965.v1
- https://mural.maynoothuniversity.ie/15157/
- http://urn.kb.se/resolve?urn=urn:nbn:se:hb:diva-6707
- https://digitalcommons.georgiasouthern.edu/teach-secondary-facpubs/56
- http://ojs.excelingtech.co.uk/index.php/IJSCM/article/viewFile/1000/pdf/
- https://escholarship.org/uc/item/1vt8j05s
- https://doaj.org/article/ca9781654bb04f75b913c8886ee687be
- http://hdl.handle.net/2429/78301
- https://philpapers.org/rec/BARWDT-3
- https://ojs.aaai.org/index.php/AAAI/article/view/25748
- http://gala.gre.ac.uk/id/eprint/38384/3/38384_MOGAJI_Artificial_Intelligence_for_seamless_experience_across_channels.pdf
- https://zenodo.org/record/1034381
- https://doi.org/10.1016/j.eswa.2023.119902
- https://doaj.org/article/77cde2b43f4849f88ec4b6d596dd89ca
- https://cronfa.swan.ac.uk/Record/cronfa69051
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0004370203001097/MAIN/application/pdf/1ad4b68baa53a475d160488683941393/main.pdf
- https://researchmgt.monash.edu/ws/files/559640618/559638927_oa.pdf
- https://figshare.com/articles/Hierarchical_multiple_regression_model_with_exploration_time_as_a_DV_and_individual_differences_and_framing_condition_as_predictors_Indiv_x_Framing_interaction_terms_entered_at_Step_2_/6005855
- http://hdl.handle.net/10722/156422
- https://zenodo.org/record/848050
- http://hdl.handle.net/2066/112666
- https://research.vu.nl/en/publications/06a62d2d-23cf-4abc-89a0-19f9c423b8b0
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0747717110001379/MAIN/application/pdf/e840d0abe1d4780f0a65f6b2ce355283/main.pdf
- http://www.egov.ufsc.br/portal/sites/default/files/anexos/6638-6637-1-PB.pdf
- https://phaidra.univie.ac.at/o:721077
- http://arxiv.org/abs/2204.02889
- https://bibliotekanauki.pl/articles/122601
- https://doi.org/10.1145/3594536.3595154
- http://www.florisbex.com/papers/AILaw12.pdf
- https://doaj.org/article/a393da7e0efd48fd9edb5f116e434b0a
- https://zenodo.org/record/5158716
- http://arxiv.org/abs/2204.13775
- https://hal.science/hal-01071169
- http://bada.hb.se:80/bitstream/2320/10063/2/JanIVA07%5B1%5D.pdf
- http://hdl.handle.net/11588/884647
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-163592
- http://personales.upv.es/jbenitez/articulos/new_dynamic.pdf
- https://eprints.sztaki.hu/3210/
- http://hdl.handle.net/2066/34584
- https://rgu-repository.worktribe.com/file/2754840/1/ABEYRATNE%202025%20AlignLLM%20%28AAM%29
- http://hdl.handle.net/11585/600292
- https://hdl.handle.net/2027.42/191727
- https://ojs.aaai.org/index.php/AAAI/article/view/11564
- http://hdl.handle.net/2078.1/151995
- https://doaj.org/article/93f2bb471dd64cbfb0f8a2707a84fc76
- http://hdl.handle.net/10.1371/journal.pone.0213034.t004
- http://espace.library.uq.edu.au/view/UQ%3A318656/Kromodimoeljo_2013_04.pdf
- https://scholarcommons.scu.edu/poli_laws_regs/6
- https://uwe-repository.worktribe.com/file/9294561/1/A%20critical%20analysis%20of%20the%20model%20statement%20literature%3A%20Should%20this%20tool%20be%20used%20in%20practice%3F
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.75.4862
- https://dl.acm.org/doi/abs/10.1145/3514197.3549674
- https://ojs.aaai.org/index.php/AIES/article/view/31623
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/27676
- https://escholarship.org/uc/item/6k53x83p
- https://hal.inria.fr/hal-02075617/document
- http://hdl.handle.net/10356/14110
- http://purl.utwente.nl/publications/87041
- http://resolver.tudelft.nl/uuid:32b84c0e-b4d4-45f2-9783-986c6e13a499
- http://www.casact.org/library/astin/vol27no1/71.pdf
- https://scholarship.law.marquette.edu/mulr/vol105/iss3/4/
- https://scholarworks.utep.edu/cs_papers/9
- https://doaj.org/article/67c1e0d7ff63495e92bab5712f5254c9
- https://doi.org/10.1007/s12351-023-00811-8
- http://www.collegepublications.co.uk/ifcolog/?00056
- https://figshare.com/articles/_Unbiased_effect_size_estimation_for_the_efficacy_of_phonics_instruction_on_reading_performance_/945199
- https://csuepress.columbusstate.edu/cgi/viewcontent.cgi?article=1369&amp;context=theses_dissertations
- https://dx.doi.org/10.15240/tul/001/2019-4-013
- https://scholarlycommons.law.hofstra.edu/faculty_scholarship/1237
- https://researchrepository.wvu.edu/cgi/viewcontent.cgi?article=6335&amp;context=wvlr
- https://hal.archives-ouvertes.fr/hal-02012383
- http://hdl.handle.net/10234/22713
- http://dx.doi.org/10.15488/11260
- http://researchspace.csir.co.za/dspace/bitstream/10204/3029/1/Baumbach_2008.pdf
- http://www2.warwick.ac.uk/fac/soc/law/elj/jilt/1996_2/hunter/
- https://www.zora.uzh.ch/id/eprint/135887/1/HerzogHelversenJBDM2018.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.74.2332
- http://hdl.handle.net/10454/18135
- http://resolver.tudelft.nl/uuid:32bad14b-506b-4eec-8bd4-937b133a181a
- https://hal.archives-ouvertes.fr/hal-01538499
- https://journals.uic.edu/ojs/index.php/dad/article/view/10689
- https://lida.hse.ru/article/view/18256
- https://figshare.com/articles/_Hierarchical_structure_of_the_model_space_Perceptual_models_response_models_specific_models_/1161629
- http://hdl.handle.net/11586/232048
- https://pdxscholar.library.pdx.edu/etm_fac/101
- https://resolver.obvsg.at/urn:nbn:at:at-ubl:3-2681
- https://repository.vu.lt/VU:ELABAETD23322233&prefLang=en_US
- http://subs.emis.de/LNI/Proceedings/Proceedings82/GI-Proceedings-82-9.pdf
- http://www.aaai.org/Papers/Workshops/1998/WS-98-16/WS98-16-008.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.62.9531
- https://aisel.aisnet.org/amcis2020/cognitive_in_is/cognitive_in_is/8
- https://lirias.kuleuven.be/handle/123456789/500815
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.433.4270
- https://stars.library.ucf.edu/scopus2015/3746
- http://www.wseas.us/e-library/transactions/economics/2009/29-690.pdf
- http://arxiv.org/pdf/1408.6908.pdf
- https://cronfa.swan.ac.uk/Record/cronfa60445
- http://www.sfu.ca/%7Emtaboada/docs/Iruskieta_daCunha_Taboada_LRE.pdf
- https://eprints.whiterose.ac.uk/190286/1/shi2021neuralnetworks.pdf
- https://opus.hs-furtwangen.de/files/9052/applsci-12-11642-v2-2.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.68.4756
- http://publica.fraunhofer.de/documents/B-73055.html
- https://doaj.org/article/d9f6f632ed924f60a88ba7b1122220f1
- http://resolver.tudelft.nl/uuid:a01c32a1-acd4-405d-bb6f-bcc5bfd3a398
- https://zenodo.org/record/5169899
- http://www.stat.columbia.edu/%7Egelman/research/published/HierarchicalCausal.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/25741
- https://orcid.org/0000-0001-9008-142X
- https://research.rug.nl/en/publications/7b76261c-4fde-4382-8bd2-240c6182c0f9
- https://www.e3s-conferences.org/10.1051/e3sconf/202340203034/pdf
- https://doaj.org/article/906055af0f4a468886aee51d5fc8e093
- https://elibrary.law.psu.edu/pslr_symposia/2020/tech/3
- http://hdl.handle.net/11582/5084
- https://mpra.ub.uni-muenchen.de/19563/1/MPRA_paper_19563.pdf
- http://hdl.handle.net/11585/781553
- http://dad.uni-bielefeld.de/index.php/dad/article/view/3740
- https://ojs.aaai.org/index.php/aimagazine/article/view/2748
- https://dspace.library.uu.nl/handle/1874/392296
- http://arxiv.org/abs/2309.05619
- http://irep.iium.edu.my/66500/1/66500_The%20cooperative%20intercultural%20pragmatics%20of%20request%20strategies%20model%20%28CIPRS%29.pdf
- https://research.vu.nl/en/publications/b05a5e70-c006-45fc-976f-0e596bb2c68e
- https://research.rug.nl/en/publications/thresholds-and-intransitivities-in-pairwise-judgments(7b76261c-4fde-4382-8bd2-240c6182c0f9).html
- http://www.languageinindia.com/july2010/marranipoliteness.pdf
- https://repository.upenn.edu/dissertations/AAI22615466
- https://escholarship.org/uc/item/3dn5p2h9
- http://ssc.sagepub.com/content/8/2/196.full.pdf
- https://ojs.aaai.org/index.php/aimagazine/article/view/5322
- https://www.academyhealth.org/files/2009/monday/legalmethods.pdf
- https://hal.archives-ouvertes.fr/hal-01071169
- https://scholarworks.gsu.edu/eps_diss/71
- https://stars.library.ucf.edu/scopus2010/1553
- https://ojs.aaai.org/index.php/aimagazine/article/view/4813
- https://opus.hs-furtwangen.de/frontdoor/index/index/docId/9053
- https://www.cai.sk/ojs/index.php/cai/article/view/535
- http://arxiv.org/pdf/1009.3770.pdf
- http://gateway.proquest.com/openurl?url_ver=Z39.88-2004&rft_val_fmt=info:ofi/fmt:kev:mtx:dissertation&res_dat=xri:pqm&rft_dat=xri:pqdiss:9910029
- http://users.dsic.upv.es/~flip/papers/arxiv2014-ai-evaluation.pdf
- https://zenodo.org/record/7829250
- https://doi.org/10.1080/1068316X.2022.2114476
- https://library.oapen.org/handle/20.500.12657/56374
- http://strathprints.strath.ac.uk/13353/
- https://etd.uum.edu.my/8641/3/s96243_02.pdf
- http://jeb.sagepub.com/content/18/3/237.full.pdf
- https://hal.archives-ouvertes.fr/hal-01125802
- http://cds.cern.ch/record/2145365
- https://hdl.handle.net/11250/2774393
- http://arxiv.org/abs/2307.03025
- http://hdl.handle.net/10547/244268
- https://research.rug.nl/en/publications/9d0364a3-aa43-47db-88be-80617612f797
- http://opim.wharton.upenn.edu/risk/ackoff/Ackoff2012/Gurcay.pdf
- http://doc.utwente.nl/76211/1/Wieringa94lcm.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S000437020300105X/MAIN/application/pdf/1fb695e153a7246e8c781ecb52cab8be/main.pdf
- http://arxiv.org/abs/2307.03109
- https://lirias.kuleuven.be/handle/123456789/645440
- http://hdl.handle.net/2160/74
- https://resolver.caltech.edu/CaltechAUTHORS:20160812-142726711
- https://aisel.aisnet.org/icis2024/adv_theory/adv_theory/4
- https://doaj.org/toc/1875-6883
- http://www.tqmp.org/Content/vol08-1/p052/p052.pdf
- http://www.hss.cmu.edu/departments/sds/ddmlab/papers/LebiereGonzalezWarwick2009.pdf
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/27698
- https://dr.lib.iastate.edu/handle/20.500.12876/105717
- http://d-scholarship.pitt.edu/42315/1/kovashka_Poster%202.0_for_PMF%20Showcase_STEM.pdf
- http://resolver.tudelft.nl/uuid:c4db06fd-30f6-419f-a05f-bf6fbb76a421
- http://researchonline.federation.edu.au/vital/access/HandleResolver/1959.17/63428
- http://arxiv.org/abs/2305.17926
- https://hdl.handle.net/11382/558232
- https://orcid.org/0000-0002-0665-1889
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877050915029713/MAIN/application/pdf/ca3c288f7bb5ea8ec5c04595d5ec75c9/main.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/17522
- https://hdl.handle.net/1871.1/c5f80d08-ac5a-4aea-a766-9653759be960
- https://ejournal.unmus.ac.id/index.php/lite/article/view/2926
- https://digitalcommons.library.tmc.edu/dissertations/AAI3592570
- https://research.utwente.nl/en/publications/4d3e25c3-1f37-457e-b929-79b4e20fafd1
- http://predictiveanalytics.pnnl.gov/aaai_symposium/abstract/presentation/03_Rodriguez.pdf
- http://www.aaai.org/Papers/Symposia/Fall/2006/FS-06-05/FS06-05-014.pdf
- http://arxiv.org/pdf/1407.4607.pdf
- https://doaj.org/article/3285b53d68ca481ea0503a34d03308b8
- http://www.ssc.wisc.edu/soc/faculty/pages/DWM_page/PDF%20files/1989PDS_conversation.pdf
- http://discovery.ucl.ac.uk/1353697/
- https://hdl.handle.net/1814/44966
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1877042813036604/MAIN/application/pdf/280ef6ea0f1fd3509a8edcb04566ea6f/main.pdf
- http://clok.uclan.ac.uk/23334/1/Combining%20logical%2008109895.pdf
- https://aisel.aisnet.org/cgi/viewcontent.cgi?article=1077&amp;context=pacis2021
- http://people.hofstra.edu/vern_r_walker/WalkerICAIL2009ResAbs.pdf
- https://doi.org/10.18653/v1/2024.findings-acl.753
- http://dx.doi.org/10.1609/aimag.v38i3.2748
- http://research.microsoft.com/en-us/um/people/horvitz/ftp/u87.pdf
- http://vuir.vu.edu.au/10702/
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S2212567114003323/MAIN/application/pdf/19d8b9559d5d70095628dc380ecc10fe/main.pdf
- http://arxiv.org/abs/2309.07462
- https://journals.vilniustech.lt/index.php/TEDE/article/view/12726
- https://hal.inria.fr/hal-01438251
- http://arxiv.org/pdf/1202.1056.pdf
- http://hdl.handle.net/10.6084/m9.figshare.21228650.v1
- https://aisel.aisnet.org/icis2021/user_behaivors/user_behaivors/11
- http://edepot.wur.nl/283495
- http://arxiv.org/abs/2311.08547
- http://pcn.psychology.msstate.edu/Publications/Rouder_Morey_Pratte_Chapter_2015.pdf
- https://aisel.aisnet.org/hicss-54/da/data_text_web_mining/7
- http://www.loc.gov/mods/v3
- http://arxiv.org/abs/2309.14525
- https://dr.lib.iastate.edu/handle/20.500.12876/30276