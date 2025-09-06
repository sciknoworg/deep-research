# Final Report: Overcoming the Narrow Context Window of LLMs in Requirements Analysis of an Industrial SRS Document

## Abstract

In modern industrial settings, a Software Requirements Specification (SRS) document is a critical source of knowledge, typically following formats such as IEEE 830. These documents, while comprehensive, often span hundreds of pages and contain heterogeneous content ranging from functional and non-functional requirements to embedded diagrams, tables, and even images. The narrow context window of standard Large Language Models (LLMs) poses a significant challenge in mining, classifying, and reasoning over such vast and complex textual environments. This report explores both architectural modifications (e.g., long-context models, integrated external memory mechanisms, and retrieval-augmented methods) and advanced preprocessing techniques (such as hierarchical segmentation and adaptive binarization) to alleviate such constraints. The research integrated insights from domains as diverse as machine control systems, safety compliance, transformer-based segmentation, risk analysis, and graph databases to propose a multi-layered solution for industrial SRS requirements analysis.

## 1. Introduction

The challenge in processing industrial SRS documents lies in their structural and semantic complexity. Despite standards like IEEE 830 providing a common template, industrial SRS documents often lean heavily on functional requirements while underrepresenting non-functional aspects that are essential for safety, maintainability, and scalability. This report compiles recent learnings and research findings from multiple fields including document image processing, model-based engineering, and advanced machine learning techniques to outline innovative pathways for overcoming the narrow context window inherent in current LLMs.

### 1.1 Motivation and Industrial Relevance

In the era where 70% of lifecycle costs are committed in early-phase requirements engineering, the ability to extract actionable insights from a massive SRS is critical. Such extraction not only supports compliance with industry benchmarks (ISO 13849-1, IEC 62061, ISO 26262, etc.) but also addresses non-functional requirements, safety assurance metrics (MTTFd, DC), and traceability. Integration of advanced LLM architectures and preprocessing paradigms that leverage state-of-the-art computer vision and NLP techniques can significantly reduce the risk of missing latent issues and ensure more holistic safety and performance evaluations.

## 2. Technical Deep-Dive: Architectures and Preprocessing Approaches

### 2.1 Architectures to Extend Context Window

#### 2.1.1 External Memory Integration

Recent research indicates that extending the LLM's memory via mechanisms like the Recurrent Memory Transformer or Block-State Transformer is effective in maintaining global context over long sequences. By adding memory tokens or integrating state-space models, these architectures are designed to separate local and global dependencies. This enables the extraction of sophisticated interdependencies crucial for SRS analysis. Techniques such as snapshot learning and linear self-attention allow LLMs to mitigate the quadratic complexity issue inherent in standard transformer models and can potentially achieve over 10× speed improvements with minimal accuracy loss.

#### 2.1.2 Retrieval-Augmented Methods

Beyond architectural modifications, retrieval-augmented LLMs combine indexed external databases (e.g., Neo4j) with NLP to enable dynamic information retrieval. Such systems can incorporate real-time information regarding similar past projects, thus augmenting the inherent context of the SRS analysis. Integration with industrial benchmarks for graph processing (as seen with the LDBC Social Network Benchmark) opens up pathways for using graph theory to cluster and correlate modular requirements sections, facilitating enhanced community segmentation in socio-technical systems.

#### 2.1.3 Latency-Aware and Adapter-Based Solutions

Latency reduction is essential when deploying these models on resource-constrained industrial systems. Techniques such as the Attention Context Contribution (ACC) metric and architectures like EdgeBERT, which incorporate latency-insensitive Fluid Pipelines, can help reduce inference latency drastically (e.g., up to 4.8× speedups). Adaptation frameworks such as AdapterHub allow for fine-tuning models with minimal overhead and facilitate dynamic model reconfiguration for both long-context processing and domain-specific optimizations.

### 2.2 Document Preprocessing Techniques

#### 2.2.1 Hierarchical Segmentation and Image Processing

Industrial SRS documents often exist in scanned or mixed-content formats that include images, diagrams, and textual data. Hierarchical segmentation methods, which decompose images into multi-level homogeneous regions (background, text, diagrams) have shown processing time reductions up to 80×. Advanced techniques that employ Lp norm based color quantization and scale space segmentation can enhance binarization quality while dynamically adjusting to archival degradation. The Rotated Gaussian Discrimination Metric (RGDM) and similar metrics are critical for ensuring high accuracy in segmentation evaluations.

#### 2.2.2 Text-based Preprocessing: Stemming, Lemmatization, and NLP Pipelines

For pure text, preprocessing pipelines that employ Doc2vec, Doc2vecC, and morphosyntactic normalization enhance document representation. In context of industrial SRS analysis, hybrid pipelines that combine image-based segmentation with text analysis (stemming, lemmatization, semantic embedding) have been effective. This dual approach ensures that both the structured (sections, enumerated requirements) and unstructured (free narrative) parts of the SRS are accurately processed. Studies have demonstrated that integrating retrieval augmentation with graph-based approaches yields precision scores as high as 0.86 with recall up to 0.95 in requirement extraction tasks.

## 3. Evaluation Metrics and Benchmarks

### 3.1 Quantitative and Qualitative Metrics

Assessment frameworks such as those adopted in European projects like OPENCOSS combine qualitative insights (readability, verifiability, completeness) with quantitative measures (precision, recall, MTTFd). Emerging meta-learning frameworks (e.g., ProMetaUS) now integrate uncertainty and risk-based metrics such as confidence levels and sensitivity analysis outputs. For example, comparing transformer models in SRS extraction, the use of ensemble disagreement scores has demonstrated a decrease in mean average error (MAE) and improvements in classification accuracy by 13.8% over conventional methods.

### 3.2 Industrial Benchmarking Case Studies

Empirical studies in domains such as railway signaling, air traffic management, and defense have utilized traditional and performance-driven benchmarks. Metrics such as diagnostic coverage (DC) and Mean Time To Dangerous Failure (MTTFd) serve as safety assurance benchmarks, while industrial case studies have shown that employing hybrid architectures and metric-based requirement process improvement frameworks (REPI) can dramatically improve traceability and reduce error rates. Techniques like quantitative risk evaluation using fuzzy logic models (Fuzzy Delphi, FAHP) provide an additional layer of robustness when traditional models are insufficient due to ambiguous or incomplete data.

## 4. Integration of Advanced Models into Industrial SRS Analysis

### 4.1 Use of Graph Databases and Metamodeling

Industrial applications often involve complex, interdependent requirements. Utilizing graph databases such as Neo4j facilitates the management of these interconnected data points. Metamodeling, involving domain-specific languages and UML integration with formal methods (e.g., QuantUM), supports automated translation from conceptual models to validated safety analysis artifacts. This approach not only supports cross-domain mappings but also allows for reuse of pre-certified components, thereby i ncreasing the reliability and compliance of the safety assurance process.

### 4.2 Hybrid and Modular Frameworks

Integrating modular frameworks like CURATOR and using adapter-based fine-tuning (e.g., AdapterHub) are increasingly necessary to address the complexity of industrial SRS documents. These frameworks support both the inter-phase communication required in RE and the real-time operational demands. Containerized benchmarking frameworks that integrate tools such as METrICS facilitate unified monitoring across system-level metrics (e.g., KLOC, defect density) and workload simulations in a dynamically scaled environment.

### 4.3 From Compliance to Performance-Based Monitoring

Transitioning from compliance-based safety measures to performance-based monitoring necessitates sophisticated tools capable of real-time risk evaluation. Integrating UML-based models with formal safety metrics, and leveraging computational techniques such as Fuzzy Decision Analysis, can bridge the gap between informal stakeholder language and formal safety specifications. Such methods are being validated across industries such as aerospace, defense, and healthcare, ensuring robust and agile risk management.

## 5. Challenges, Future Directions, and Concluding Remarks

### 5.1 Limitations and Challenges

While advanced architectures and preprocessing techniques show promise, several challenges remain:

- **Model Complexity vs. Interpretability:** Integration of complex hierarchical models and external memory tokens can reduce transparency in LLM decision processes, complicating audit trails needed for safety-critical systems.
- **Resource Constraints:** Despite improvements in latency and inference speeds, deploying these hybrid models on edge devices or within constrained industrial environments still requires careful trade-offs.
- **Heterogeneous Data Integration:** The need to seamlessly combine image-based and text-based preprocessing pipelines introduces system integration challenges and potential performance bottlenecks, especially when large-scale parallel processing is involved.

### 5.2 Future Research Directions

Several promising avenues remain to be explored:

- **Enhanced Memory Mechanisms:** Further research into memory-augmented transformers (e.g., novel gated attention units, linear approximation methods) promises to further offset the large context requirements while maintaining inference speed and reducing computational footprint.
- **Adaptive Hybrid Frameworks:** Developing adaptive systems that dynamically select between preprocessing strategies based on input characteristics can optimize resource usage and ensure higher segmentation accuracies. Incorporation of reinforcement learning for dynamic method selection is a potential research track.
- **Benchmark Development:** As industrial applications diversify, new benchmark initiatives designed specifically for SRS requirements extraction that combine both quantitative and qualitative metrics are needed. Developing unified hierarchical segmentation evaluation frameworks which integrate multi-scale metrics (IoU/Jaccard index) will be essential.
- **Risk and Safety Integration:** There is an emerging need to integrate fuzzy decision models and quantitative risk assessments with LLM outputs, further bridging the gap between automated extraction and industrial safety assurance standards.

### 5.3 Concluding Remarks

The integration of advanced transformer architectures with strategic preprocessing methodologies presents a transformative opportunity to overcome the narrow context window inherent in conventional LLMs. By leveraging external memory tokens, retrieval-augmented methods, hierarchical segmentation, and hybrid approaches, industrial SRS analysis can be significantly enhanced. Such integrated systems not only promise higher precision and recall in requirement extraction but also contribute to robust, performance-based safety monitoring in safety-critical domains. As these technologies mature, their fusion with formal risk analysis frameworks and real-time benchmarking systems will redefine best practices in requirements engineering and safety assurance.

In summary, overcoming the narrow context window challenge is not merely a technical hurdle but a multidimensional problem that necessitates integrated solutions spanning architecture, preprocessing, benchmarking, and risk management. The convergence of these diverse methodologies promises to elevate industrial safety and reliability to new heights.

---

*This report synthesizes extensive learnings from contemporary research studies, industry case reports, and pioneering benchmarks. While several proposed solutions remain at the cutting edge of research, proactive integration of these approaches will be critical to anticipating and meeting future industrial requirements analysis challenges.*

## Sources

- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.91.9334
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA450000%26Location%3DU2%26doc%3DGetTRDoc.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.91.2410
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-111149
- http://repository.tue.nl/780811
- http://hdl.handle.net/11556/152
- http://www.ijcsit.com/docs/Volume
- https://masi.vuse.vanderbilt.edu/images/7/7a/SPIE_hierarchy.pdf
- http://dx.doi.org/10.1109/IROS40897.2019.8968066
- http://hdl.handle.net/11380/1068369
- http://arxiv.org/abs/2201.06774
- https://hal.archives-ouvertes.fr/hal-02138688
- https://hal.science/hal-00089471
- https://lup.lub.lu.se/record/1653489
- https://ecommons.luc.edu/cs_facpubs/273
- http://hdl.handle.net/1822/50594
- https://hal.inria.fr/hal-02419195
- http://hdl.handle.net/2108/273369
- https://hdl.handle.net/10356/150258
- https://hdl.handle.net/11250/3022599
- http://nbn-resolving.de/urn:nbn:de:bsz:352-139839
- https://mailserver.di.unipi.it/ricerca/proceedings/ICSE2008/ulssis/p3.pdf
- http://hdl.handle.net/2108/273351
- http://hdl.handle.net/11588/411893
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-150356
- http://dx.doi.org/10.1007/s10462-024-10824-0
- http://www.ijesrt.com/issues+pdf+file/Archives-2014/April-2014/107.pdf
- https://hdl.handle.net/2027.42/4215
- https://scholar.utc.edu/rcio/2021/posters/18
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.7.25
- https://zenodo.org/record/3588551
- https://digitalcollection.zhaw.ch/handle/11475/19637
- http://hdl.handle.net/10985/12534
- http://www.sciencedirect.com/science/article/B6VBG-4WW16XM-1/2/fd3cb147ee1bec76d1bfa8c5120e17dc
- http://hdl.handle.net/American
- http://digital.library.unt.edu/ark:/67531/metadc688034/
- https://hal.science/hal-03837798
- http://publica.fraunhofer.de/documents/N-18789.html
- http://umpir.ump.edu.my/id/eprint/7390/1/Safety_Instrumented_Systems_between_Reliability_and_Fuzzy.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/17864
- http://dl.lib.mrt.ac.lk/handle/123/10091
- https://zenodo.org/record/3387418
- https://hal.inrae.fr/hal-03574696
- http://purl.utwente.nl/publications/79011
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1877050916301466/MAIN/application/pdf/d424585482792fedf0cbb7059f2519f3/main.pdf
- https://hal.archives-ouvertes.fr/hal-03002550
- https://hal.inria.fr/hal-01674731
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877050914010369/MAIN/application/pdf/79d222c607e2de6a35474bd93f7eda2b/main.pdf
- https://hal.archives-ouvertes.fr/hal-02442819/file/ERTS2020_paper_11.pdf
- https://zenodo.org/record/1337715
- https://research.tue.nl/en/publications/4d645cc6-931c-430b-91df-05aa46859115
- https://cris.vtt.fi/en/publications/c79508ed-520a-4383-99d8-1be64c35e43e
- https://journalkeberlanjutan.com/index.php/ijesss/article/view/228
- https://doi.org/10.17615/8qpj-7z52
- https://doi.org/10.1051/metrology/201312001
- http://hdl.handle.net/10261/337011
- http://arodes.hes-so.ch/record/6812
- https://zenodo.org/record/6400996
- http://publica.fraunhofer.de/documents/N-188277.html
- https://zenodo.org/record/1118299
- http://laser.cs.umass.edu/courses/cs521-621/papers/Lutz.pdf
- http://web.uvic.ca/%7Emroth/PREPRINTS/IJIER.pdf
- https://zenodo.org/record/5138731
- http://hdl.handle.net/11582/306173
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.50.2736
- https://ieeexplore.ieee.org/document/8192044/
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S187705091502517X/MAIN/application/pdf/fd43d30cf22171c1de9d1aa105a11229/main.pdf
- https://docs.lib.purdue.edu/dissertations/AAI10685608
- https://escholarship.org/uc/item/9md197hq
- https://edit.elte.hu/xmlui/bitstream/10831/71471/2/1206803273.pdf
- https://zenodo.org/record/1413307
- http://hdl.handle.net/10356/19765
- https://hdl.handle.net/11511/42716
- https://doaj.org/article/3825242bab73412d81f1143b3a4c9e99
- http://deploy-eprints.ecs.soton.ac.uk/104/1/2009-05_Requirements_Traceability.pdf
- http://arxiv.org/abs/2207.02126
- https://ijece.iaescore.com/index.php/IJECE/article/view/34005
- http://hdl.handle.net/11582/99803
- http://www.protsyk.com/mytexts/ewdts07.pdf
- https://commons.wmu.se/lib_chapters/5
- https://hal.archives-ouvertes.fr/hal-03633805/document
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.43.1726
- http://ir.lib.au.edu.tw/dspace/handle/987654321/3550
- http://publica.fraunhofer.de/documents/N-294132.html
- https://research.tue.nl/nl/publications/rttool--a-tool-for-extracting-relative-thresholds-for-source-code-metrics(7e160360-0b44-423d-b44d-a9c2cc2c821b).html
- https://research.tue.nl/en/publications/eff92a0c-8c5b-47ff-bb71-20ef31c7f294
- http://hdl.handle.net/10831/56269
- http://creativecommons.org/licenses/by-nc-nd/
- http://hdl.handle.net/2117/12979
- https://hdl.handle.net/1969.1/193822
- https://eprints.whiterose.ac.uk/94449/1/INFSOF_D_15_00295R1.pdf
- http://hdl.handle.net/10985/10269
- https://portal.research.lu.se/ws/files/6003012/2295432.pdf
- http://arxiv.org/abs/2207.06881
- http://eprints.utm.my/id/eprint/96479/
- http://www.lrec-conf.org/proceedings/lrec2012/pdf/664_Paper.pdf
- https://hal.inria.fr/hal-01526146
- http://dx.doi.org/10.1007/978-3-319-77243-1_10
- https://hal-paris1.archives-ouvertes.fr/hal-02299905
- https://hdl.handle.net/11311/1228552
- https://norma.ncirl.ie/3684/
- http://arxiv.org/abs/2204.06683
- http://link.springer.com/chapter/10.1007%2F978-3-642-19858-8_19
- https://zenodo.org/record/5879446
- https://zenodo.org/record/7897601
- http://hdl.handle.net/2108/273355
- https://push-zb.helmholtz-muenchen.de/frontdoor.php?source_opus=57113
- http://hdl.handle.net/10985/11393
- https://doi.org/10.1109/TPWRD.2006.882999
- http://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article%3D1115%26context%3Dcsse_fac
- http://arxiv.org/abs/2208.01753
- http://publica.fraunhofer.de/documents/B-73055.html
- http://hal.archives-ouvertes.fr/docs/00/08/94/71/PDF/RTDT_Elsevier_submit.pdf
- http://ceur-ws.org/Vol-1226/paper31.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-210987
- http://publica.fraunhofer.de/documents/N-169250.html
- http://ccsenet.org/journal/index.php/cis/article/download/4684/4279/
- https://doi.org/10.1109/PES.2007.385623
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA320931%26Location%3DU2%26doc%3DGetTRDoc.pdf
- http://ijret.org/Volumes/V03/I06/IJRET_110306025.pdf
- https://zenodo.org/record/5499096
- http://hdl.handle.net/123456789/40
- https://doaj.org/toc/1805-2363
- http://arxiv.org/abs/2309.05619
- http://research.ijcaonline.org/ncrtc/number9/mpginmc1076.pdf
- http://etd.adm.unipi.it/theses/available/etd-09052014-092100/
- http://hdl.handle.net/11585/847028
- http://www.cg.cs.tu-bs.de/media/publications/Albuquerque2014HBH.pdf
- http://hdl.handle.net/1959.14/155699
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-7539
- https://dx.doi.org/10.3390/pr4040044
- http://hdl.handle.net/20.500.11897/153600
- http://hdl.handle.net/2078.1/131468
- http://hdl.handle.net/11696/63970
- https://escholarship.org/uc/item/1446z4wg
- http://hdl.handle.net/10068/652127
- http://repository.tue.nl/913121
- https://epublications.marquette.edu/theses/4864
- http://hdl.handle.net/10.26434/chemrxiv.8058464.v1
- https://www.neliti.com/publications/313006/elaboration-of-the-hierarchical-approach-to-segmentation-of-scanned-documents-im
- http://dx.doi.org/10.1177/0148558X14535780
- http://hdl.handle.net/20.500.11897/293194
- https://doaj.org/article/1cbf566051df47fd832999c85453bf2c
- https://hal.archives-ouvertes.fr/hal-01276635/file/ESMCv3-sansEntete.pdf
- http://hdl.handle.net/2108/81916
- http://www6.in.tum.de/Main/Publications/Sojer2011a.pdf
- http://hdl.handle.net/10985/11385
- http://hdl.handle.net/11311/549584
- https://hal.archives-ouvertes.fr/hal-01276661
- https://www.um.edu.mt/library/oar/handle/123456789/86001
- http://hdl.handle.net/2060/19930022788
- http://eprints.utm.my/id/eprint/42244/
- https://zenodo.org/record/5759541
- http://publica.fraunhofer.de/documents/N-300587.html
- https://figshare.com/articles/_Values_of_quality_metrics_for_ITRN_RBF_and_classical_dimensionality_reduction_methods_/1479431
- https://www.duo.uio.no/bitstream/handle/10852/34821/1/dravhandling-panesar-walawege.pdf
- https://doi.org/10.1016/j.infsof.2015.12.012
- http://arxiv.org/abs/2202.07856
- http://umpir.ump.edu.my/id/eprint/19574/
- https://doaj.org/article/335d9c83341f4684a2e017540e5283d9
- https://scholar.uwindsor.ca/etd/1771
- https://hal-uphf.archives-ouvertes.fr/hal-03416997
- https://ecommons.luc.edu/ures/2021/2021/91
- http://hdl.handle.net/2429/58658
- http://www.springer.com/series/7899
- http://arxiv.org/abs/2201.03327
- https://www.repository.cam.ac.uk/handle/1810/315098
- https://cris.vtt.fi/en/publications/38a60ddc-9416-4a6a-a6da-15bdb9301400
- http://dx.doi.org/10.1109/MS.2017.94
- http://atlantis-press.com/php/download_paper.php?id%3D8700
- http://hdl.handle.net/10400.22/13915
- http://www.ijme.us/cd_08/PDF/29ent203.pdf
- https://research.vu.nl/en/publications/3d0fe75c-8f74-4dfa-901d-715dbb8ad283
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-16797
- http://dx.doi.org/10.1007/978-3-642-37422-7_18
- https://zenodo.org/record/1477518
- http://hdl.handle.net/10.1371/journal.pone.0288060.t001
- http://www.wseas.us/e-library/conferences/tenerife2001/papers/513.pdf
- https://hal.archives-ouvertes.fr/hal-02278292/file/ERTS_2018_paper_16.pdf
- https://zenodo.org/record/6043287
- http://hdl.handle.net/1822/37438
- http://plg.uwaterloo.ca/~migod/papers/2014/msr14-Oleksii-ElasticSearch.pdf
- http://hdl.handle.net/2108/124156
- https://hal.archives-ouvertes.fr/hal-02066561/file/lm21_com_4C_1_014_Ricque.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.93.1800
- https://hdl.handle.net/11250/3017317
- http://hdl.handle.net/10016/26902
- http://utpedia.utp.edu.my/id/eprint/19004/
- http://hdl.handle.net/10985/11414
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.83.4008
- https://zenodo.org/record/1314057
- https://escholarship.org/uc/item/30x346n8
- https://zenodo.org/record/3515044
- http://publica.fraunhofer.de/documents/N-169348.html
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.648.3630
- http://arxiv.org/abs/2202.10447
- https://aaltodoc.aalto.fi/handle/123456789/119368
- https://dspace.library.uu.nl/handle/1874/371396
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-20301
- http://hdl.handle.net/11556/607
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.50.3913
- https://journals.vilniustech.lt/index.php/JCEM/article/view/3831
- http://hal.inria.fr/docs/00/75/26/33/PDF/HAL_MUNOZ_et_al_ECCE2011.pdf
- http://publica.fraunhofer.de/documents/N-336498.html
- http://web.cefriel.it/~brandole/pc/17-dsd08.pdf
- http://doi.org/10.1109/ASWEC.2013.26
- https://doi.org/10.1109/IGCC.2016.7892611
- http://utpedia.utp.edu.my/id/eprint/20238/1/MUHAMMAD%20YASIR%20SHAMIM.pdf
- https://www.ajol.info/index.php/jcsia/article/view/205466
- http://www.mdpi.com/books/pdfview/book/720
- https://doaj.org/toc/1424-8220
- http://www.dsmforum.org/events/DSM04/Parssinen.pdf
- http://arxiv.org/abs/2306.09539
- http://www.win.tue.nl/%7Easerebre/ICSME2014TOOL.pdf
- http://www.loc.gov/mods/v3