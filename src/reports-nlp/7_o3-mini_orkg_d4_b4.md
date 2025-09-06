# Final Report: Translation with LLMs through Prompting with Long-Form Context

This report synthesizes extensive research and experimental learnings on leveraging large language models (LLMs) to improve machine translation (MT) quality by integrating long-form context through enhanced prompting strategies. The goal is to address challenges in accuracy, ambiguity resolution, domain-specific terminology management, and low-resource language scenarios by incorporating document-level and multi-sentence context in translation workflows.

---

## 1. Introduction

Recent advancements in LLM architectures and prompt engineering have opened novel avenues for neural machine translation (NMT) to move beyond isolated sentence-level translation. By integrating long-form context such as chained sentences, extended document contexts, and domain-specific terminologies into the translation process, researchers aim to significantly improve translation accuracy, contextual coherence, and domain alignment. This report compiles key insights from previous research, including evaluations of zero-shot methods, Chain-of-Thought (CoT) prompting, few-shot learning, and domain adaptations, describing how these techniques can be harnessed for translation in legal, technical, and low-resource scenarios.

---

## 2. Background and Contextual Review

### 2.1. Translation Quality Improvement via Long-Form Context

Research has demonstrated that incorporating long-form context can resolve lexical ambiguities and enhance overall document coherence. For example, improvements in BLEU scores, as well as human error metrics, have been observed in systems that use contextual fine-tuning at inference time. This approach leverages extra context from surrounding sentences or full documents without requiring retraining on extensive document-level data.

### 2.2. Domain-Specific Challenges and Terminology Management

Legal and technical domains demand high precision. Studies from projects such as TermWise and domain-specific adaptations (e.g., Italian-to-South Tyrolean German translations) have underscored that hand-tailored terminological databases and the use of placeholders with morphosyntactic annotations result in significant performance improvements. This is crucial in environments where standard neural outputs may misinterpret complexities inherent in legal lexicon and near-synonym variability.

### 2.3. Techniques in Low-Resource Settings

The LoResMT 2020 Shared Task revealed that zero-shot translation for low-resource languages can be enhanced by methods like back-translation and domain adaptation. By borrowing techniques from related languages and incorporating pseudo-translations, researchers have mitigated the lack of parallel corpora for nearly 7000 languages. The integration of non-traditional training data and multiview approaches continues to expand the toolset for low-resource settings.

---

## 3. Innovative Approaches and Methodologies

### 3.1. Prompting Techniques

**Zero-Shot and Few-Shot Prompting:**

Large language models have increasingly been tested using zero-shot and few-shot prompting. However, evaluations across multiple language pairs consistently show that while generic prompting methods offer strong baselines, adding Chain-of-Thought (CoT) components significantly enhances performance. The CoT methodology provides explicit intermediate reasoning steps that help in preserving intra-document consistency across long text spans.

**Chain-of-Thought (CoT) Prompting:**

CoT techniques, as evidenced by frameworks like ThoughtSource, have improved translation quality primarily for larger models. This approach decomposes a translation task into intermediate steps, effectively balancing localized sentence-level semantic detail with global document context. Although challenges remain (e.g., generating consistent numerical scores in evaluations), the CoT framework represents a promising route for complex translations in legal and technical documents.

### 3.2. Sparse and Selective Attention Mechanisms

Sparse attention strategies—such as lightweight selection layers that restrict attention to a small percentage of tokens—offer computational benefits without sacrificing performance. For instance, systems that limit attention to around 5% of tokens have demonstrated up to 93% reduction in computational cost. These architectures are essential in real-time translation systems where maintaining low latency is as critical as preserving translation quality.

### 3.3. Dynamic and Context-Aware Fine-Tuning

Dynamic fine-tuning methods integrate contextual adjustments at inference time. Notably, instance-based adaptation methods and on-the-fly fine-tuning have been shown to yield improvements comparable to corpus-based approaches while lowering the cost of retraining. Techniques such as warm-start encoder/decoder states, hierarchical attention mechanisms, and residual connections contribute to capturing both local and global context. Empirical studies—supported by EC-funded projects (QT21, ModernMT)—have demonstrated that on-the-fly adaptation improves domain-specific terminology accuracy and overall BLEU scores, sometimes by as much as +9 points.

### 3.4. Hardware Acceleration and Utility-Based Resource Management

Integration with hardware-level QoS mechanisms (for instance, on platforms like the Xilinx Zynq UltraScale+ MPSoC) has further optimized translation pipelines. These studies indicate that utility-driven resource management and dynamic scheduling can markedly reduce latency variability, a key requirement for resource-constrained real-time applications. Additionally, dynamic architectures such as Dynamic-HAT demonstrate sub-second adaptation for switching Transformer sub-models, maintaining BLEU score losses below 1.5% and recovering slight gains in translation accuracy.

### 3.5. Contextual and Document-Level Metrics

The evolution of evaluation metrics is as critical as the models themselves. Combining classical metrics like BLEU, TER, and NIST with learning-based approaches (e.g., SVM methods, regression-based metrics) and discourse-level assessments (using Rhetorical Structure Theory) has provided a multidimensional picture of translation quality. Tools like TermEval, MQM-based frameworks, and discourse metrics such as DiscoTK have enabled fine-grained system-level evaluations that capture both adequacy and fluency in translated documents.

---

## 4. Application Scenarios and Domain-Specific Insights

### 4.1. Legal Translation

Legal translation stands as one of the most demanding scenarios. Studies indicate that integrating advanced lexicography resources (e.g., IATE and UNOGTerm), coupled with contextual fine-tuning approaches, can significantly improve legal term precision and reduce post-editing time. Moreover, transforming legal texts into formal representations (first-order logic or semantic tags) can facilitate consistency checks and system explainability—an essential requirement in jurisdictions with rapidly evolving colloquial legal constructs.

Researchers have documented improvements such as:

- A boost in BLEU scores by up to +9 points in domain-adapted systems
- Increased term translation accuracy by over 3 percent
- Improved human-annotated semantic correlations, with some systems achieving normalized DCG scores as high as 0.9 for jurisprudence texts

### 4.2. Technical and Broadcast Translation

Technical texts, including broadcast captions and specialized industrial communications, benefit substantially from leveraging long-context models. In these cases, techniques like inference-time contextual fine-tuning (which does not require complete retraining on document-level data) prove useful. By addressing lexical ambiguities and resolving context mismatches, these methods have demonstrated improved BLEU scores and significantly reduced error rates, thereby enhancing real-time machine translation systems.

### 4.3. Low-Resource and Multi-Modal Environments

For low-resource languages, innovative methods that utilize related language transfers, pseudo-translations, and dynamic data selection have been employed to overcome parallel data scarcity. Approaches such as non-traditional training pipelines (e.g., borrowing from multilingual languages and using simplified layers for low-dimensional contextual representations) present a promising direction. Further, adaptations such as the coupling of a reflective LLM with a translation-specific LLM—as evidenced by improvements in metrics like BERTScore and METEOR—hint at a robust agentic translation framework for low-resource settings.

---

## 5. Evaluation Strategies

### 5.1. Metrics and Comprehensive Evaluations

A rigorous evaluation framework is essential for measuring the improvements from integrating long-form context. Key evaluations include:

- **Corpus-Level Metrics:** Traditional BLEU, NIST, TER, and newer metrics like BLANC, which combine local semantic coherence with global structural accuracy.
- **Segment-Level Analyses:** Tools such as MQM, SemPOS, and unsupervised methods (e.g., UMEANT) which offer fine-grained performance assessments, especially in handling nuance and lexical ambiguities.
- **Learning-Based Evaluations:** Regression and SVM-based evaluations have outperformed traditional metrics in several experiments, particularly when paired with chain-of-thought prompting.
- **Domain-Specific Tests:** Legal and technical translations are additionally evaluated via bespoke metrics (e.g., TermEval) and human error analyses.

### 5.2. Prompt Engineering and Comparative Outputs

Evaluation experiments consistently highlight that larger LLMs benefit disproportionately from Chain-of-Thought prompting relative to few-shot or zero-shot methods. Incorporating rigorous reference translations and detailed error annotation schemes is indispensable. Moreover, prompt chaining strategies—evident in systems developed for legal document classification—demonstrate that decomposing complex texts into summarization and exemplar retrieval tasks can help even smaller models outperform larger zero-shot models.

---

## 6. Implications, Limitations, and Future Directions

### 6.1. Implications

The integration of long-form context in MT systems provides tangible benefits in reducing ambiguity, capturing discourse-level coherence, and aligning translations with domain-specific terminology. This approach unlocks the ability to process full-length documents in a manner that is both context-aware and computationally viable, paving the way for advanced legal, technical, and broadcast translation systems.

### 6.2. Limitations

Several practical challenges remain:

- **Computational Overhead:** Extending context windows (e.g., up to 32,768 tokens with Llama 2 adaptations) increases computational complexity and may result in higher latency, necessitating advanced hardware optimization strategies.
- **Evaluation Consistency:** Inconsistencies in numerical output—particularly in chain-of-thought evaluations—highlight that further work is needed to standardize and validate benchmarks across different languages and domains.
- **Scalability:** While dynamic fine-tuning approaches offer adaptability, scaling these techniques to high-throughput, real-time translation systems in resource-constrained environments remains an open research question.

### 6.3. Future Directions

Several promising avenues have been identified:

1. **Hybrid Architectures:** Combining neural MT systems with symbolic logic frameworks and rule-based post-processing could further enhance interpretability and performance, especially in legal translation.
2. **Enhanced Sparse Attention Models:** Further refining sparse attention mechanisms to balance long-context processing while reducing latency could yield significant computational savings.
3. **Dynamic Scheduling and Inference-Time Adaptation:** Greater integration with hardware-accelerated QoS management and adaptive computation time models promises improved system responsiveness without compromising translation quality.
4. **Agentic Translation Frameworks:** Coupling specialized translation LLMs with reflective LLMs in a unified, agentic system may unlock further accuracy gains in low-resource environments.
5. **Advanced Evaluation Frameworks:** Future work should explore holistic evaluation strategies that integrate discourse metrics, human-in-the-loop assessments, and cost-efficient unsupervised (or minimally supervised) training-less approaches.

---

## 7. Conclusion

The convergence of advanced prompting techniques, longer document context integration, and dynamic fine-tuning represents a pivotal evolution in machine translation research. By bridging the gap between sentence-level performance and document-level coherence, modern LLM-driven systems are laying the groundwork for highly specialized, context-aware translations in legal, technical, and multilingual domains. While challenges such as computational complexity and evaluation consistency persist, continued interdisciplinary research integrating deep neural networks with explicit symbolic reasoning and dynamic resource management is poised to overcome these hurdles.

This report consolidates the comprehensive learnings from previous research, identifying both validated strategies and speculative avenues that promise to reshape how we use LLMs for translation—especially in settings where precision, context, and domain-specific accuracy are paramount.

---

*Prepared on 2025-09-05 by an expert researcher, this report aims to provide a detailed, multi-faceted overview of current methodologies and future directions in long-form context-enhanced translation using LLMs.*


## Sources

- https://hdl.handle.net/1721.1/145034
- https://zenodo.org/record/3525546
- https://lirias.kuleuven.be/handle/123456789/656784
- https://zenodo.org/record/3524979
- https://orcid.org/0000-0002-0606-0050
- http://hdl.handle.net/2117/350177
- https://doaj.org/article/0fa14c3155b54d32b77706c11f88401a
- https://doaj.org/article/79c275b60a5e4b6b91242d1a8d1aa229
- https://nrc-publications.canada.ca/eng/view/object/?id=328f63b3-c8d0-4c4a-bd21-47ef78e5e696
- https://repository.vu.lt/VU:ELABAETD107115547&prefLang=en_US
- https://library.oapen.org/handle/20.500.12657/46391
- http://alt.qcri.org/semeval2014/cdrom/pdf/SemEval102.pdf
- http://www.mt-archive.info/Coling-1994-Nyberg.pdf
- https://arodes.hes-so.ch/record/12331/files/Popescu_2023_simplified_training.pdf
- http://doras.dcu.ie/19106/
- http://infoscience.epfl.ch/record/278200
- http://arxiv.org/abs/2205.11277
- https://ddd.uab.cat/record/189708
- http://hdl.handle.net/10230/42372
- http://computing.dcu.ie/%7Etokita/p/EC_3_dcuIWSLT.pdf
- https://eamt2022.com/
- http://hdl.handle.net/10045/76088
- http://dx.doi.org/10.1007/s10590-010-9077-2
- http://www.sciencedirect.com/science/article/pii/S0045790616301744
- http://hdl.handle.net/11582/302003
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.43.4663
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.67.451
- https://eprints.whiterose.ac.uk/149064/8/P19-1424.pdf
- http://www.nusl.cz/ntk/nusl-298425
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.44.8761
- http://www.mt-archive.info/MTS-1997-Nyberg.pdf
- http://arxiv.org/abs/2308.16797
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.87.1793
- http://aclweb.org/anthology/D/D12/D12-1037.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.96.1927
- https://hal.science/hal-00089626
- http://hdl.handle.net/10045/76016
- http://hdl.handle.net/10230/36827
- http://www.ics.uci.edu/%7Eyingyib/papers/QSIC2006.pdf
- http://amslaurea.unibo.it/view/cds/CDS9174/
- https://escholarship.org/uc/item/72x5j5vg
- http://www.statmt.org/wmt09/pdf/WMT-0940.pdf
- http://www.mt-archive.info/SpNL-1992-Brown.pdf
- http://hdl.handle.net/1885/103825
- https://zenodo.org/record/7828876
- http://www.ida.liu.se/~sarst/SLTC_2010_Bremin_et_al.pdf
- https://lirias.kuleuven.be/handle/123456789/329197
- http://www.nusl.cz/ntk/nusl-304321
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-3785
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.82.768
- https://lirias.kuleuven.be/handle/123456789/448814
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.432.1915
- https://eprints.lancs.ac.uk/id/eprint/225755/
- http://eprints-phd.biblio.unitn.it/2921/2/DOC260418-26042018182822.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.9.4214
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.80.8416
- http://alt.qcri.org/%7Eguzmanhe//papers/WMT2015-Guzman.pdf
- https://zenodo.org/record/6672725
- http://hdl.handle.net/2117/349294
- http://www.computing.dcu.ie/%7Eebicici/publications/2013/FDAforFDA.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.1042.946
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.54.7465
- http://www.lar.deis.unibo.it/people/crossi/files/SCD/Multiparadigm
- https://ojs.aaai.org/index.php/AAAI/article/view/26524
- http://www.cse.ust.hk/~dekai/library/WU_Dekai/LoWu_Wmt2013.pdf
- http://tubiblio.ulb.tu-darmstadt.de/76831/
- http://aclweb.org/anthology/D/D15/D15-1166.pdf
- http://mt-archive.info/AMTA-2010-Denkowski.pdf
- https://doaj.org/article/1635d185bebf4ceda1ed71b5beba511d
- https://doi.org/10.1109/ETFA.2010.5641322
- http://www.mt-archive.info/EMNLP-2009-Zaidan.pdf
- https://archive-ouverte.unige.ch/unige:154232
- https://publikationen.bibliothek.kit.edu/1000120793/81046799
- https://archive-ouverte.unige.ch/unige:146834
- https://dare.uva.nl/personal/pure/en/publications/understanding-and-enhancing-the-use-of-context-for-machine-translation(422122ad-f9d6-4952-9012-fcde9a820773).html
- http://www.mt-archive.info/MTS-2001-Miller-1.pdf
- https://doaj.org/article/cfd6089d4104413787e743dddb10d8e7
- http://web.mit.edu/smadnick/www/wp2/1995-03-SWP#3847.pdf/
- https://repository.vu.lt/VU:ELABAETD81705840&prefLang=en_US
- http://hdl.handle.net/11582/250641
- http://wwwling.arts.kuleuven.be/qlvl/prints/Heylen_Steurs_2014draft_Translating_Legal_Administrative_Language.pdf
- http://ssli.ee.washington.edu/people/amittai/mtrg/papers/MTS-2005-ECK.pdf
- https://www.open-access.bcu.ac.uk/16138/
- http://www.mt-archive.info/LREC-2008-Mauser.pdf
- http://aclweb.org/anthology/C/C14/C14-1040.pdf
- http://real.mtak.hu/144429/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.1658
- http://hdl.handle.net/10045/76101
- http://hdl.handle.net/11346/BIBLIO@id=8056635193312463081
- https://ojs.aaai.org/index.php/AAAI/article/view/11910
- https://zenodo.org/record/4537095
- https://hal.archives-ouvertes.fr/hal-02962195/file/Waitk_decoding__InterSpeech_2020_.pdf
- http://hdl.handle.net/2117/104733
- http://hdl.handle.net/20.500.11850/626756
- http://english.um.edu.my/anuvaada/main.html
- http://www.mt-archive.info/Coling-2010-Yang.pdf
- http://www.public.asu.edu/%7Ecbaral/papers/shruti2015.pdf
- http://hdl.handle.net/10.1184/r1/7347104.v1
- http://www.mt-archive.info/ACL-2005-Liu-2.pdf
- https://zenodo.org/record/6759978
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877050916300710/MAIN/application/pdf/3efe2d01d5fdc65be78c7995248d5089/main.pdf
- http://hdl.handle.net/2117/13092
- https://www.repository.cam.ac.uk/handle/1810/360866
- http://hdl.handle.net/11346/BIBLIO@id=-8469031730659020238
- https://doaj.org/article/7fd0243982f04cd69d17d35b9811b22a
- http://hdl.handle.net/10447/39626
- https://ojs.aaai.org/index.php/AAAI/article/view/11254
- http://hdl.handle.net/10393/26565
- http://arxiv.org/abs/2308.04138
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-440704
- https://hal.archives-ouvertes.fr/hal-01304184
- http://nthur.lib.nthu.edu.tw/dspace/handle/987654321/66622
- http://www.let.rug.nl/basile/papers/WynerEtAlCCBoxerJURIX2012.pdf
- http://www-public.int-evry.fr/~conan/Publications/2009_quacon.pdf
- http://mt-archive.info/LREC-2002-Dabbadie-2.pdf
- https://etheses.whiterose.ac.uk/14284/1/thesis.pdf
- http://etd.adm.unipi.it/theses/available/etd-04122023-101720/
- http://www.qcri.qa/app/media/4476/
- https://publications.rwth-aachen.de/record/679614
- http://hdl.handle.net/2117/26965
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.433.823
- https://zenodo.org/record/2276024
- http://hdl.handle.net/11346/BIBLIO@id=-3274296548556821754
- https://zenodo.org/record/7835211
- https://research.monash.edu/en/publications/e7af0388-d67e-4f54-826e-ce01c9c6b6dc
- https://www.publifarum.farum.it/index.php/publifarum/article/view/433
- http://hdl.handle.net/11585/881319
- https://digital.library.unt.edu/ark:/67531/metadc993374/
- https://content.sciendo.com/view/journals/cl/43/1/article-p17.xml
- http://hdl.handle.net/2117/86305
- http://www.informatik.uni-oldenburg.de/%7Eatzeko7/pub/RohrVanHoornGieseckeMatevskaHasselbringAlekseev08TraceContextSensitivePerformanceProfilingForEnterpriseSoftwareApplications.pdf
- http://wwwling.arts.kuleuven.be/qlvl/prints/Heylen_Bond_DeHertog_Vulic_Kockaert_2014abs_TermWise_CAT_tool_LREC.pdf
- https://archive-ouverte.unige.ch/unige:146556
- http://cemadoc.irstea.fr/cemoa/PUB00002083
- http://hdl.handle.net/11582/325888
- http://matjournals.in/index.php/JOCSES/article/view/5179
- http://arxiv.org/abs/2311.08306
- http://www.dodccrp.org/events/2004_CCRTS/CD/papers/223.pdf
- http://www.aclweb.org/anthology/W/W14/W14-4009.pdf
- http://hdl.handle.net/11582/250637
- https://hdl.handle.net/10356/168430
- http://www.mt-archive.info/MTS-2007-Stadler.pdf
- https://archive-ouverte.unige.ch/unige:43275
- http://www.mt-archive.info/IWSLT-2005-Gimenez.pdf
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll89/id/120458
- https://scholarship.law.pitt.edu/fac_articles/524
- http://doras.dcu.ie/24592/
- https://doaj.org/article/b006a58193cf4763989875cd9ee9087f
- http://hdl.handle.net/10138/327849
- http://hdl.handle.net/11346/BIBLIO@id=-8748738730419561250
- http://www.mt-archive.info/ACL-2007-Albrecht-2.pdf
- https://zenodo.org/record/8106807
- https://hdl.handle.net/1842/39298
- https://cris.maastrichtuniversity.nl/en/publications/e08ba8cd-72b3-4e20-99da-ff46d211ea7e
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.50.6036
- https://ojs.aaai.org/index.php/AAAI/article/view/6461
- http://alt.qcri.org/semeval2014/cdrom/pdf/SemEval123.pdf
- https://doaj.org/toc/2350-420X
- http://www.mt-archive.info/MTS-1999-Doyon.pdf
- https://lirias.kuleuven.be/handle/123456789/585484
- https://archive-ouverte.unige.ch/unige:3460
- http://arxiv.org/abs/2309.14174
- https://zenodo.org/record/6760020
- http://alt.qcri.org/%7Eguzmanhe//papers/WMT2014-Joty.pdf
- http://researchonline.federation.edu.au/vital/access/HandleResolver/1959.17/63428
- http://hdl.handle.net/10045/76037
- http://arxiv.org/abs/2309.16039
- http://www.nusl.cz/ntk/nusl-387899
- http://hdl.handle.net/10447/279560
- https://orcid.org/0000-0001-5736-5930
- https://ojs.aaai.org/index.php/AAAI/article/view/17522
- https://hal.science/hal-04300702
- http://hdl.handle.net/10174/7952
- http://amslaurea.unibo.it/24989/1/Contarino_dissertation.pdf
- https://doaj.org/article/79c1524018b64eafbc371a039e6054b6
- http://doras.dcu.ie/24493/
- https://library.oapen.org/handle/20.500.12657/46388
- https://dare.uva.nl/personal/pure/en/publications/latent-domain-models-for-statistical-machine-translation(7b929314-2537-4f7a-9562-cd401262c848).html
- https://research.rug.nl/en/publications/8ba98488-05c6-4fe4-9203-33c9d96134f8
- http://www.scopus.com/inward/record.url?scp=85160549410&partnerID=8YFLogxK
- http://hdl.handle.net/10379/16376
- http://dx.doi.org/10.1155/2012/484580
- https://www.zora.uzh.ch/id/eprint/208876/
- https://research.monash.edu/en/publications/16caa9dd-6d35-47a9-b846-2019150e6c7e
- http://doras.dcu.ie/22903/
- http://hdl.handle.net/2262/96110
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.71.3539
- http://www.tao2015.org/research/03_TaoCat_HeylenSteursKockaert_bis.pdf
- https://zenodo.org/record/3923505
- http://archive-ouverte.unige.ch/unige:31405
- http://hdl.handle.net/10061/14693
- http://www.iro.umontreal.ca/%7Efoster/papers/batchtune-naacl12.pdf
- http://www.mt-archive.info/MTS-2003-Roh.pdf
- https://dx.doi.org/10.3390/app8050739
- https://lirias.kuleuven.be/bitstream/123456789/448810/3/Heylen_Bond_DeHertog_Vulic_Kockaert_Steurs_2014pres_TermWise_TKE.pdf
- https://doaj.org/article/9176bf99a2354cdb807a011130ae84ac
- https://www.zora.uzh.ch/id/eprint/208882/1/2021.iwslt-1.19.pdf
- https://orcid.org/0000-0001-6462-3248
- http://hdl.handle.net/10.6084/m9.figshare.21228650.v1
- http://hdl.handle.net/10045/76047
- http://www.mt-archive.info/IWSLT-2009-Ma.pdf
- https://inria.hal.science/hal-04015863v2/document
- http://www.loc.gov/mods/v3