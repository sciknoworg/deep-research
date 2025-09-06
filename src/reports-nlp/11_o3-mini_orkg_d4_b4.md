# Final Report on Retrieval-Augmented Deductive Reasoning (RADR) Via Structural Decomposition of Legal Analysis

This report provides an in-depth discussion of Retrieval-Augmented Deductive Reasoning (RADR) in the context of legal analysis. By leveraging a structural decomposition of legal texts—not just fragmenting documents by sections but parsing argumentative, statutory, and case-specific elements—this approach aims to bridge the divide between traditional legal reasoning and modern machine learning augmented by advanced information retrieval (IR) methods. In this report, we detail the theoretical framework, technical methodologies, and empirical insights acquired from prior research. The discussion is structured around several core topics:

1. **Conceptual Foundations**
2. **Structural Decomposition in Legal Analysis**
3. **Integration of Retrieval Systems and Deductive Reasoning**
4. **Hybrid Approaches and Domain-Specific Adaptation**
5. **Evaluation Metrics and Empirical Findings**
6. **Challenges, Trade-Offs, and Future Directions**

---

## 1. Conceptual Foundations

Retrieval-Augmented Deductive Reasoning (RADR) is an integrated framework that leverages both traditional rule-based deductive logic and modern statistical methods. The historic evolution of AI in law—from the rudimentary indexing in early legal databases to today's domain-specific transformer models—provides the backdrop against which RADR is positioned. The aim is to marry retrieval (finding relevant legal precedents, statutes, or cases) with systematic deductive reasoning to support judicial decision-making and legal argumentation.

Key components include:

- **Information Retrieval (IR):** Traditionally, legal IR systems, using synonym expansion and heuristic methods (e.g., as seen with early systems such as IKBALS or OUIXOTE), are gradually being enhanced by deep learning techniques that improve contextual understanding.
- **Deductive Reasoning Engines:** These engines integrate statutory frameworks or defeasible argumentation structures (e.g., Toulmin’s model) to simulate legal reasoning.
- **Neural-Symbolic Integration:** Emerging hybrid systems integrate symbolic reasoning (from formal ontologies such as LKIF, LegalRuleML, CEN Metalex) with deep learning modules, resulting in both improved predictive accuracy and enhanced interpretability.

This integrated model is essential given the demands for both high accuracy (as measured by precision, recall, and F-measures in diverse jurisdictions like the European Court of Human Rights cases) and explainability (mandated by legal imperatives such as GDPR and contractual obligations in high-stake domains such as healthcare and corporate law).

---

## 2. Structural Decomposition in Legal Analysis

### 2.1. Defining Structural Decomposition

In this context, **structural decomposition** does not simply mean a basic text segmentation. Rather, it involves deconstructing legal documents into fine-grained argumentative units: statutory language, matching case precedents, oral and written argumentation, and even latent discursive patterns. The process embraces both deductive and abductive logic schemes, organizing legal texts as multi-layered graphs with nodes representing legal concepts, arguments, or statutory clauses.

- **Argumentative Decomposition:** Parsing argumentation frameworks, such as Toulmin’s model or Walton’s argument schemes, provides clear mappings of claims, grounds, warrants, and backing. This decomposition is critical for offering interpretable explanations and supporting decision-making processes.
- **Statutory and Case Components:** Legal texts are also segmented into normative (statutory) and case-specific narratives. Such decomposition enables the identification of jurisdiction-specific terminologies and supports domain adaptation through targeted fine-tuning, as seen in models like ITALIAN-LEGAL-BERT.

### 2.2. Addressing the Follow-up Questions

- **Query on Structural Components:** When referencing structural decomposition, the emphasis is on a multi-dimensional analysis—segmenting legal texts into argumentative components, statutory narratives, and case-specific contexts. This enables models to better capture nuances and maintain legal cohesion.

- **Retrieval Focus:** The retrieval component is not limited to traditional keyword-based IR; rather, it integrates modern NLP and machine learning approaches, such as transformer-based embeddings, to enable similarity detection and pattern recognition at a semantic level. Hybrid systems merge RegEx extraction methods with neural architectures (CNNs, RNNs, graph neural networks) to ensure robust retrieval even within unstructured legal texts.

- **Scope and Universality:** The application framework is envisioned to be adaptable across jurisdictions. While domain-specific fine-tuning and adaptation (using legal pre-training and parameter-efficient techniques) are essential, efforts such as modular ontology construction and linked open data facilitate a universally applicable framework that can be tailored to local legal terminologies and practices.

---

## 3. Integration of Retrieval Systems and Deductive Reasoning

### 3.1. Retrieval-Augmented Architectures

Modern RADR systems integrate IR components directly into deductive reasoning processes:

- **Hybrid IR-ML Systems:** The integration frameworks use deep neural networks for pattern recognition and context interpretation while the retrieval components fetch legal data that is processed and verified via deductive logic. Recent studies have shown that combining transformer models with traditional heuristic systems may sometimes yield non-linear performance gains but might also impose additional computational overhead.

- **Empirical Assessments:** Experiments in domains such as personal injury (Italian RTA cases) and medical disputes have demonstrated that hybrid IR plus deductive reasoning systems achieve high performance metrics (with precision and recall in the high 80s to low 90s percentage range) while maintaining the necessary explainability required for legally sensitive applications.

### 3.2. Technical Integration Strategies

- **Neural-Symbolic Pipelines:** Neural networks are deployed to extract legal concepts and argument patterns from case datasets. These outputs are then translated into symbolic representations using frameworks like LegalRuleML or through defeasible argumentation frameworks, facilitating further deductive reasoning.

- **Linked Data and Ontological Layers:** Integration with Linked Open Data facilitates the modularization of historical and contemporary legal corpora, linking disparate systems through standards such as RDF, OWL, and XML Schema. The LKIF core ontology and modular strategies like middle-out construction are critical for ensuring interoperability and scalability.

- **Dynamic Performance Calibration:** Leveraging techniques from UAV dynamic data-driven systems, modern architectures incorporate error-based adaptivity. This means recalibration triggers when discrepancies arise between sensor-model outputs and legal standards, ensuring compliance with evolving regulatory frameworks.

---

## 4. Hybrid Approaches and Domain-Specific Adaptation

### 4.1. Combining Deep Learning with Rule-Based Methods

Hybrid approaches that fuse deep learning with explicit rule representations are emerging as particularly effective in legal domains:

- **Defeasible Logic and Argumentation Frameworks:** Systems based on frameworks like Abstract Dialectical Framework layers or Toulmin-based models support the handling of judicial discretion. Such frameworks have been successfully applied in domains ranging from Australian Family Courts to sentencing eligibility assessments.

- **Parameter-Efficient Adaptation:** Techniques that fine-tune only a small fraction of model parameters (e.g., 0.1% for legal transformations) have shown competitive performances relative to fully retrained large models. Domain-specific models such as LEGAL-BERT and variants of transformer models illustrate that incorporating local legal jargon and nuanced argumentative structures significantly enhances accuracy.

- **Cross-Jurisdictional Transfer:** Ensuring retrievability and legal reasoning accuracy across jurisdictions—leveraging multilingual and cross-lingual adaptations—is advanced using graph-based representations and ontology-driven retrieval systems. Empirical findings, such as those from French appellate court datasets, reveal that hybrid systems can seamlessly adjust for legal heterogeneity.

### 4.2. Benefits Across the Legal Spectrum

- **Enhanced Predictive Accuracy:** Studies consistently demonstrate that hybrid models capture context better than traditional IR systems alone, even though occasionally a standalone IR system may perform faster. This balance between speed and interpretability is a key consideration.

- **Explainability:** Integrating causal inference techniques with predictive models creates dual outputs that are both accurate and legally justified. For example, advanced legal frameworks now report not only F-measure scores but also provide defensible argumentation structures that align with legal doctrines.

- **Interoperability and Scalability:** Ontology-based systems and linked data architectures enable legal documents ranging from Roman Digest texts to modern legislations to be interfaced seamlessly. This ensures that retrieval and analysis systems remain current despite the inherent diversity of legal language and structure.

---

## 5. Evaluation Metrics and Empirical Findings

### 5.1. Quantitative Assessments

Numerous studies have benchmarked RADR and related hybrid systems against traditional IR and deductive reasoning platforms:

- **Precision, Recall, and F-measures:** Evaluations in high-stakes domains show precision in the high 80s and low 90s (e.g., 89.1% precision for European Court cases). Similarly, case-based systems, such as those dealing with road traffic accident claims, have demonstrated notable predictive capabilities in cost estimation and outcome prediction.

- **Performance Trade-Offs:** While enhanced retrieval quality via deep learning improves outcome accuracy, it sometimes introduces processing overhead. Comparative evaluations—such as those between a hybrid LLM+IR system and a standalone IR system—highlight that system design must balance computational efficiency with interpretability.

- **Defeasible and Hybrid Metrics:** Emerging metrics include nearest neighbors similarity assessments, contrastive studies (e.g., comparing Roman and common law statutory texts), and comprehensive performance measurement frameworks like DOVE used in RAD authorization prototypes.

### 5.2. Qualitative and Domain-Specific Evaluations

- **Case Study Applications:** Instruments such as the Split-Up initiative in Australian family law or the RTA insurance claim resolutions have shown that integrating structured rule-based methods with statistical models yields greater robustness, even in cases with incomplete data or ambiguous legal phrasing.

- **Empirical Validity:** Quantitative performance is complemented by qualitative benchmarks, such as explanatory adequacy and alignment with legal reasoning traditions (for example, consistency with Toulmin’s argumentation–which serves as a qualitative validity metric in such cases).

---

## 6. Challenges, Trade-Offs, and Future Directions

### 6.1. Current Challenges

- **Integration Complexity:** Reconciling probabilistic outputs from neural networks with the rigidity of formal statutory and case-based reasoning presents significant challenges, particularly concerning transparency and accountability.

- **Jurisdictional Nuances:** Fine-tuning across diverse legal systems (varying from codified Roman law to common law traditions) requires the development of modular legal ontologies and bespoke datasets that accurately capture jurisdiction-specific terminologies.

- **Scalability and Transparency:** While hybrid systems can achieve high accuracy, the computational overhead and potential opacity of combined models necessitate continuous human oversight and the development of standardized performance metrics.

### 6.2. Future Research Directions

- **Dynamic Calibration and Adaptive Learning:** Future RADR systems should incorporate real-time recalibration mechanisms that adjust model parameters in response to evolving legal standards and cross-jurisdictional shifts. Techniques from UAV error-based adaptivity might be further explored for such dynamic recalibration.

- **Enhanced Argument Mining:** Continued integration of deep learning with formal argumentation mining will further refine the extraction of latent legal structures. This research path, integrating neural outputs with Toulmin-based or defeasible frameworks, promises to boost both accuracy and explanation quality.

- **Interdisciplinary Integration:** Fostering collaboration between computer scientists, legal scholars, and domain experts will be crucial. Such interdisciplinary efforts will help in developing balanced, multifaceted systems that can negotiate the trade-offs between speed, accuracy, interpretability, and cost efficiency.

- **Regulatory and Ethical Considerations:** As regulatory requirements evolve (e.g., GDPR, ethical mandates in medicine, corporate mergers, etc.), the design of RADR systems must likewise incorporate new legal imperatives, making explainable AI and bias monitoring central to future deployments.

---

## Conclusion

Retrieval-Augmented Deductive Reasoning via structural decomposition offers a compelling path forward in legal analytics and decision support. By effectively breaking down legal texts into their constituent argumentative and statutory elements, and combining state-of-the-art IR methods with robust deductive reasoning engines, RADR systems promise both enhanced predictive accuracy and the interpretability required by high-stake legal applications. This report has reviewed empirical studies, hybrid architectures, and state-of-the-art methodologies that span a range of legal systems—from ancient Roman law to modern multi-jurisdictional frameworks.

Ongoing research must continue to refine integration techniques, balance domain-specific adaptations with general applicability, and address the inherent trade-offs between computational performance and legal explainability. Ultimately, the integration of deep neural models with symbolic reasoning frameworks represents a promising, evolving frontier in the intersection of law and artificial intelligence.

---

This report synthesizes all available research learnings and provides a comprehensive roadmap for further exploration of RADR via structural decomposition in legal analysis.

## Sources

- https://www.ssoar.info/ssoar/handle/document/80203
- https://surfsharekit.nl/public/9697206f-cde2-4dde-819f-58e38b8f1c1c
- http://hdl.handle.net/11588/863939
- http://hdl.handle.net/10446/160823
- http://publica.fraunhofer.de/documents/N-89783.html
- https://ddd.uab.cat/record/180648
- https://vuir.vu.edu.au/15929/1/15929.pdf
- https://hal.archives-ouvertes.fr/hal-01495835
- https://cris.maastrichtuniversity.nl/en/publications/2306424f-9502-4a38-bb02-559babbaaeb7
- http://livrepository.liverpool.ac.uk/3135748/1/CMNA_2021.pdf
- http://dx.doi.org/10.3233/faia241257
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-216004
- http://egov.ufsc.br/portal/sites/default/files/anexos/6670-6669-1-PB.pdf
- https://doi.org/10.1016/S0004-3702(03)00107-3
- https://zenodo.org/record/3973285
- http://scholar.uwindsor.ca/cgi/viewcontent.cgi?article%3D1477%26context%3Dossaarchive
- https://orbilu.uni.lu/handle/10993/57759
- https://uzjournals.edu.uz/rev_law/vol1/iss1/10
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.50.7751
- http://www.egov.ufsc.br/portal/sites/default/files/anexos/6638-6637-1-PB.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.74.9495
- http://hdl.handle.net/10945/64001
- http://hdl.handle.net/11585/781387
- http://hdl.handle.net/11585/87696
- http://hdl.handle.net/11585/101630
- https://zenodo.org/record/7105986
- https://sciformat.ca/journals/index.php/ciai/article/view/10
- https://eprints.qut.edu.au/71067/
- http://lawcat.berkeley.edu/record/1098846
- http://hdl.handle.net/11573/181569
- https://dare.uva.nl/personal/pure/en/publications/neural-networks-penalty-logic-and-optimality-theory(9c98854e-e5d8-4d56-9247-43a8dee785fc).html
- http://www.wseas.us/e-library/conferences/2005lisbon/papers/496-275.pdf
- http://hdl.handle.net/10119/7879
- https://scholar.law.colorado.edu/cgi/viewcontent.cgi?article=1812&amp;context=faculty-articles
- https://zenodo.org/record/8239725
- http://hdl.handle.net/2078.1/260555
- https://hdl.handle.net/11588/863939
- http://hdl.handle.net/1885/103825
- https://zenodo.org/record/7828876
- http://www.ling.helsinki.fi/sky/julkaisut/SKY2006/Yankova.pdf
- https://chicagounbound.uchicago.edu/law_and_economics/989
- https://dspace.library.uu.nl/handle/1874/420848
- https://lirias.kuleuven.be/bitstream/123456789/276004/1/Wyneretal2010.pdf
- http://hdl.handle.net/1814/30361
- https://www.utupub.fi/handle/10024/148857
- http://hdl.handle.net/11585/266133
- https://aisel.aisnet.org/iceb2018/95
- https://doaj.org/article/3ec57eae295549a49a77d759b3188056
- https://www.um.edu.mt/library/oar//handle/123456789/22368
- http://www.macrothink.org/journal/index.php/ijl/article/download/2578/pdf/
- https://zenodo.org/record/439627
- https://doaj.org/article/9d0edee3175c4ec6a2873f8174b63de5
- http://ftp.rta.nato.int/public/PubFullText/RTO/MP/RTO-MP-MSG-035/MP-MSG-035-04.pdf
- http://ebooks.iospress.nl/volumearticle/50847
- https://hal.inria.fr/hal-02331336/document
- https://dare.uva.nl/personal/pure/en/publications/lkif-core-principled-ontology-development-for-the-legal-domain(bd48bad5-d85f-4576-842c-2ff4c128a811).html
- https://larc.cardozo.yu.edu/faculty-books/39
- http://jurix.nl/proceedings/
- https://birmingham.elsevierpure.com/en/publications/3e2108ce-4ce1-4b74-bb41-5724fb7cbe88
- https://digitalcommons.law.uga.edu/books/22
- http://hdl.handle.net/1853/46194
- https://halshs.archives-ouvertes.fr/halshs-01306613
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-447240
- http://www.scopus.com/inward/record.url?scp=78650348033&partnerID=8YFLogxK
- http://eprints.rclis.org/43487/
- http://www2.warwick.ac.uk/fac/soc/law/elj/jilt/1996_2/hunter/
- https://doi.org/10.6084/m9.figshare.12333290.v1
- http://hdl.handle.net/2072/434984
- http://hdl.handle.net/11585/644630
- http://hdl.handle.net/10125/70894
- http://vuir.vu.edu.au/15929/
- https://zenodo.org/record/3760615
- http://hdl.handle.net/11585/113803
- https://hdl.handle.net/2152/109164
- https://hec.hal.science/hal-03885355
- http://wyner.info/research/Papers/WynerMochalesPalauMoensMilward2009.pdf
- http://hdl.handle.net/11573/1090586
- https://doi.org/10.25968/opus-2073
- https://zenodo.org/record/7561150
- https://escholarship.org/uc/item/2qw5s32p
- http://www.public.asu.edu/%7Ecbaral/papers/shruti2015.pdf
- http://www.aaai.org/Papers/Workshops/1998/WS-98-16/WS98-16-008.pdf
- http://www.di.uevora.pt/~pq/papers/book2008.pdf
- https://cs.anu.edu.au/people/Eric.McCreath/papers/JOAL2013Curtotti.pdf
- https://elib.psu.by/handle/123456789/30706
- http://download1.hermes.asb.dk/archive/download/H22_07.pdf
- https://scholar.law.colorado.edu/articles/81
- http://hdl.handle.net/11585/708232
- http://livrepository.liverpool.ac.uk/3153662/1/jurix21.pdf
- https://hal-mines-paristech.archives-ouvertes.fr/hal-00937740
- http://arxiv.org/abs/2206.05224
- http://hdl.handle.net/11382/549631
- http://hdl.handle.net/11585/555553
- http://hdl.handle.net/11585/78772
- https://zenodo.org/record/182497
- http://hdl.handle.net/11585/79342
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.81.2763
- http://hdl.handle.net/11585/523458
- http://publica.fraunhofer.de/documents/N-169353.html
- https://dopus.uni-speyer.de/frontdoor/index/index/docId/4786
- http://hdl.handle.net/2429/3460
- http://nlphist.hypotheses.org/1
- https://elibrary.law.psu.edu/pslr_symposia/2020/tech/3
- https://kar.kent.ac.uk/96048/11/jds1058.pdf
- https://arrow.tudublin.ie/scschcomart/216
- http://urn.kb.se/resolve?urn=urn:nbn:se:lnu:diva-121563
- http://hdl.handle.net/1822/52534
- https://zenodo.org/record/7686234
- https://orcid.org/0000-0003-2156-9338
- http://hdl.handle.net/11585/881319
- http://arxiv.org/abs/2310.11761
- http://hdl.handle.net/11585/789832
- http://www.unc.edu/~plmiller/writing/Evolution_of_Roman_Legal_long.pdf
- http://hdl.handle.net/11583/2971183
- https://birmingham.elsevierpure.com/en/publications/0dc9fd16-380b-40cd-9376-29f67e86bdeb
- https://online-journals.org/index.php/i-joe/article/view/28025
- http://hdl.handle.net/10536/DRO/DU:30085320
- https://irlaw.umkc.edu/faculty_works/24
- https://digitalcommons.montclair.edu/student-research-symposium/2024/poster04/42
- http://arxiv.org/abs/2211.02950
- https://www.repository.cam.ac.uk/handle/1810/311633
- https://doaj.org/article/a4a86f26fdab4580bd707c876525e985
- https://doaj.org/article/4bf711266c5e4c0e86fb5bac4a897885
- https://zenodo.org/record/7973785
- https://zenodo.org/record/7329023
- https://dialnet.unirioja.es/servlet/oaiart?codigo=6677875
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0004370203001073/MAIN/application/pdf/e56faa03882b0f21083387f93a3facf8/main.pdf
- https://digitalcommons.fiu.edu/etd/2126
- http://jhir.library.jhu.edu/handle/1774.2/67855
- http://scholar.uwindsor.ca/cgi/viewcontent.cgi?article%3D1436%26context%3Dossaarchive
- http://hdl.handle.net/11343/39621
- http://www.cs.rutgers.edu/%7Emccarty/research/rj90.pdf
- https://digitalcommons.law.uga.edu/books/1020/thumbnail.jpg
- https://scholar.uwindsor.ca/ossaarchive/OSSA6/papers/55
- https://scholarlycommons.law.emory.edu/cslr-books/5
- http://orbilu.uni.lu/handle/10993/45065
- http://livrepository.liverpool.ac.uk/3177223/1/JURIX_2023___Human_AI.pdf
- https://chicagounbound.uchicago.edu/cgi/viewcontent.cgi?article=2194&amp;context=public_law_and_legal_theory
- https://link.springer.com/chapter/10.1007/978-3-030-89811-3_1
- https://doaj.org/toc/2350-420X
- http://hdl.handle.net/11368/2871927
- http://calenda.org/587869
- https://doi.org/10.3233/FAIA200850
- http://www.ijcta.com/documents/volumes/vol3issue4/ijcta2012030456.pdf
- http://edoc.hu-berlin.de/18452/24345
- http://hdl.cqu.edu.au/10018/1019731
- http://arxiv.org/abs/2210.13712
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.79.769
- https://hal.archives-ouvertes.fr/hal-02397050/document
- https://www.openaccessrepository.it/record/131783
- http://researchonline.federation.edu.au/vital/access/HandleResolver/1959.17/63428
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.76.5683
- https://hdl.handle.net/11382/558232
- https://digitalcommons.law.uga.edu/fac_artchop/846
- http://vuir.vu.edu.au/2519/
- http://hdl.handle.net/11382/533342
- http://www.theses.fr/2018NORMIR16/document
- https://scholar.law.colorado.edu/cgi/viewcontent.cgi?article=2231&amp;context=faculty-articles
- http://hdl.handle.net/10174/7952
- https://commons.allard.ubc.ca/theses/86
- http://hdl.handle.net/10119/4651
- http://arxiv.org/abs/2311.08890
- http://hdl.handle.net/11386/4725167
- https://dialnet.unirioja.es/servlet/oaiart?codigo=5004480
- https://zenodo.org/record/6625852
- https://zenodo.org/record/6416648
- https://scholar.uwindsor.ca/ossaarchive/OSSA6/papers/22
- http://hdl.handle.net/11585/844314
- https://scholarcommons.sc.edu/aii_fac_pub/581
- https://zenodo.org/record/4729661
- https://openresearch.surrey.ac.uk/esploro/outputs/journalArticle/A-Corpus-Approach-to-Roman-Law/99519922202346
- http://sites.thomsonreuters.com.au/journals/2017/08/02/australian-law-journal-update-vol-91-pt-7/
- http://scholar.uwindsor.ca/cgi/viewcontent.cgi?article%3D1473%26context%3Dossaarchive
- https://scholarlycommons.law.hofstra.edu/faculty_scholarship/1151
- http://www.scopus.com/inward/citedby.url?scp=73049090174&partnerID=8YFLogxK
- http://arxiv.org/abs/2209.06049
- https://zenodo.org/record/5541413
- https://animorepository.dlsu.edu.ph/faculty_research/3208
- https://pubmed.ncbi.nlm.nih.gov/35395867
- https://doi.org/10.1017/err.2019.51
- https://doaj.org/toc/2306-6784
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.1035.4866
- http://hdl.handle.net/1854/LU-8630558
- http://www.governatori.net/papers/2009/ruleml2009norms.pdf
- http://vuir.vu.edu.au/10702/
- https://rgu-repository.worktribe.com/file/2754880/1/ABEYRATNE%202025%20Unsupervised%20similarity-aligned%20%28LINK%20ONLY%29
- https://brill.com/edcollbook/title/62134
- http://eprints.bournemouth.ac.uk/28269/1/IRLCT%20special%20issue%20%28final%20ms%29%20post%20proof.pdf
- https://scholarship.law.duke.edu/dltr/vol16/iss1/3
- https://dare.uva.nl/personal/pure/en/publications/specification-of-the-legal-knowledge-interchange-format-deliverable-11(c71fcec2-f2d4-49c6-b184-83e99215cabb).html
- https://hdl.handle.net/11250/3035536
- http://hdl.handle.net/10.6084/m9.figshare.21228650.v1
- https://hal.science/hal-03467669
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.76.1661
- https://hal.archives-ouvertes.fr/hal-01627322/document
- https://doaj.org/article/a393da7e0efd48fd9edb5f116e434b0a
- https://zenodo.org/record/4720371
- http://publica.fraunhofer.de/documents/N-74175.html