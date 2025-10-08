# Cross-Culture Self-Debiasing through Cross-lingual Interactions among Large Language Models

## Abstract

This report provides an in-depth exploration of cross-culture self-debiasing in large language models (LLMs) through cross-lingual interactions. Our work synthesizes insights from recent advancements in debiasing methodologies—including Social Contact Debiasing (SCD), parameter-efficient fine-tuning techniques such as PoliTune, and advanced cross-lingual fusion strategies like the FILTER method. We discuss theoretical frameworks rooted in social psychology (notably the Contact Hypothesis) and provide detailed discussions of experimental protocols that employ cross-cultural and cross-lingual interventions. The report evaluates both internal self-corrective mechanisms and externally applied debiasing interventions, with extensive consideration of cultural nuances, diversified language pairs, and multi-dimensional bias domains.


## Table of Contents

1. [Introduction](#introduction)
2. [Theoretical Background](#theoretical-background)
   1. [Self-Debiasing Mechanisms](#self-debiasing-mechanisms)
   2. [Cross-Cultural Influences and the Contact Hypothesis](#cross-cultural-influences-and-the-contact-hypothesis)
3. [Methodological Approaches](#methodological-approaches)
   1. [Parameter-Efficient Fine-Tuning and Internal Self-Correction](#parameter-efficient-fine-tuning-and-internal-self-correction)
   2. [External Cross-Lingual Adjustments and Social Contact Debiasing (SCD)](#external-cross-lingual-adjustments-and-social-contact-debiasing-scd)
   3. [Multilingual Fusion Techniques and Advanced Tokenization Strategies](#multilingual-fusion-techniques-and-advanced-tokenization-strategies)
4. [Empirical Findings and Case Studies](#empirical-findings-and-case-studies)
   1. [Debiasing Across Multiple Models](#debiasing-across-multiple-models)
   2. [Cultural and Language Considerations](#cultural-and-language-considerations)
5. [Integrative Strategies and Future Directions](#integrative-strategies-and-future-directions)
6. [Conclusion](#conclusion)
7. [References and Further Readings](#references-and-further-readings)


## Introduction

In recent years, the transformative potential of LLMs has been tempered by concerns over their inherent biases. These biases often manifest along socio-cultural, political, and domain-specific dimensions. The paradigm of cross-culture self-debiasing leverages the interaction of language models across diverse linguistic and cultural datasets to effect internal corrections in model representations and outputs. 

This report explores the nuances of self-debiasing techniques – both internal, where LLMs attempt to self-correct via mechanisms implemented during training, inference, or post-hoc adjustments, and external, through interventions inspired by cross-lingual interactions. As LLMs such as LLaMA 2, Tulu, NousHermes, and others scale, addressing biases becomes critical not only from a technical perspective but also from a socio-political and ethical standpoint.


## Theoretical Background

### Self-Debiasing Mechanisms

Self-debiasing refers to the capacity of LLMs to internally adjust their representations and outputs to mitigate biases. This process can occur during different stages:

- **Training-Time Adjustments:** Here, models integrate tailored loss functions, such as reinforcement learning from human feedback (RLHF) or parameter-efficient techniques like Direct Preference Optimization (DPO), demonstrated by PoliTune's work with Llama3-8B and Mistral-7B.
- **Generation-Time Corrections:** Internal self-monitoring and prompt tuning strategies (e.g., ADEPT) enable dynamic adjustments during text generation, with manifold-learning inspired debiasing terms ensuring that fairness improvements do not compromise semantic coherence.
- **Post-Hoc Corrections:** Techniques that leverage activity dependency networks (ADNs) or self-report adjustments provide a corrective overlay post-generation, addressing issues like hallucination and unfaithful reasoning.

While these methods offer significant potential, the interplay between internal self-correction and external interventions is critical in a cross-cultural context.

### Cross-Cultural Influences and the Contact Hypothesis

Incorporating cross-cultural dynamics into LLM debiasing necessitates a theoretical underpinning that reflects real-world intergroup interactions. The Contact Hypothesis from social psychology, which posits that direct, structured interaction between diverse groups reduces prejudice, is particularly influential. This theoretical lens informs the design of Social Contact Debiasing (SCD) mechanisms:

- **Social Contact Debiasing (SCD):** By simulating intergroup contact using extensive prompt datasets (e.g., 108,000 prompts across 13 bias dimensions), SCD mimics real-world interactions. Studies have shown that such debiasing can lead to up to a 40% reduction in bias in models like LLaMA 2 after just a single epoch of instruction tuning.
- **Measurement and Validity:** Empirical approaches leveraging factor analysis, structural equation modeling, and differential item functioning ensure that the observed bias reductions are both statistically valid and culturally equivalent.

The integration of socio-psychological insights with computational techniques forms a core methodological bridge for bridging cross-cultural differences in LLM outputs.


## Methodological Approaches

### Parameter-Efficient Fine-Tuning and Internal Self-Correction

Research such as PoliTune demonstrates that parameter-efficient fine-tuning, including DPO, can adjust embedded economic and political biases. Such techniques have been validated in models such as Llama3-8B and Mistral-7B, confirming scalability. Benefits include:

- *Scalability:* Minimal parameter adjustments yield significant debiasing improvements.
- *Robustness:* The internal mechanisms rely less on external feedback, ensuring baseline improvements in bias mitigation.

However, these methods face challenges when confronted with cross-cultural datasets that introduce linguistic and socio-cultural variances absent in traditional training data.

### External Cross-Lingual Adjustments and Social Contact Debiasing (SCD)

The SCD approach leverages the simulation of intergroup interactions to externally debias LLM outputs. Key methodological innovations include:

- *Cross-Cultural Prompt Engineering:* A dataset comprising 108,000 social-contact simulation prompts, covering 13 distinct bias dimensions, has been applied to models like LLaMA 2, Tulu, and NousHermes. The outcomes indicate bias reduction up to 40% in very short tuning epochs.
- *Two-Stage Debiasing Processes:* Appropriate integration of continuous prompt augmentation with subsequent contrastive learning (as seen in the CCPA method) allows models to better differentiate and reconcile culturally divergent representations.
- *Comparison with Internal Mechanisms:* Unlike traditional internal self-correction that might be limited by inherent training data biases, the SCD approach applies external debiasing pressures that are dynamically informed by cross-cultural and cross-lingual interactions.

### Multilingual Fusion Techniques and Advanced Tokenization Strategies

Modern debiasing struggles not only with cultural disparity but also with technical challenges such as inefficient tokenization:

- **FILTER Methodology:** This approach fuses source and target language representations during cross-lingual finetuning, handling alignment issues inherent in monolingual training. Independent shallow encoding followed by KL-divergence self-teaching losses have achieved state-of-the-art outcomes on XTREME and XGLUE benchmarks.
- **Tokenization Challenges:** Utilizing English-only tokenizers leads to severe inefficiencies and performance degradation (up to 68% increased training cost). Multimedia tokenizers require larger vocabularies to capture cultural nuances, necessitating integrative strategies that balance complexity with representational fidelity.
- **Incorporation of Culturally Diverse Datasets:** By synthesizing linguistically and culturally rich datasets into the training process, debiasing extends beyond simple tokenization adjustments. This is critical for underrepresented languages and low-resource settings, as indicated by evaluations using adapted benchmarks (e.g., the French extension of CrowS-pairs and DisCo adaptations for Indian languages).


## Empirical Findings and Case Studies

### Debiasing Across Multiple Models

Empirical results provide mixed but promising outcomes:

- **Model Comparisons:** Social Contact Debiasing applied to LLaMA 2, Tulu, and NousHermes has demonstrated a consistent reduction in biases by up to 40% in only one epoch. This suggests that the external debiasing approaches are effective even when rapid intervention is required.
- **Reinforcement Learning and Adaptive Reward Design:** Models integrating adaptive reward functions with reinforcement learning (e.g., Okapi’s extended tuning in 26 languages) have shown both improved semantic consistency and enhanced cross-cultural performance, outperforming traditional supervised fine-tuning.

### Cultural and Language Considerations

Several studies emphasize that biases are not monolithic and require dynamic adaptation:

- **Cultural Nuance and Evaluation:** Benchmark development must account for multi-dimensional intersectional identities. Efforts to develop culturally inclusive benchmarks, such as GramAdapt and GeoMLAMA, underscore the diversity of constructs and challenges when comparing Western versus non-Western cultures.
- **Non-verbal and Multimodal Integration:** Recent breakthroughs in multimodal fusion (incorporating synthetic non-verbal cues like facial expressions and affective vocal signals) show additional promise in aligning AI outputs with realistic cultural behaviors.
- **Hybrid Fairness Approaches:** Incorporating adaptive strategies that reconcile binary definitions with intersectional identities provides a critical path forward. These approaches move beyond traditional fairness metrics to more nuanced, culturally-sensitive assessments.


## Integrative Strategies and Future Directions

Looking forward, the evolution of cross-culture self-debiasing in LLMs necessitates a multi-pronged approach combining internal and external debiasing mechanisms, reinforced by cross-cultural and cross-lingual insights:

1. **Iterative Multi-Epoch Instruction Tuning:** While one-epoch tuning can yield swift improvements, iterative methods augmented with RLHF may produce more sustainable debiasing across diverse cultural contexts.

2. **Enhanced Data Curation:** Continuous refinement of training data—particularly with culturally rich, non-Western datasets—will enable models to better capture intersectional nuances. This involves coordinated efforts in tokenization, translation/back-translation protocols, and culturally specific pretraining.

3. **Integration of Socio-Psychological Theories:** Future research should incorporate additional constructs from social psychology beyond the Contact Hypothesis. For example, strategies involving counterbiasing and mediation training may further refine how models process and output culturally relevant content.

4. **Custom and Adaptive Reward Models:** Tailoring reward functions with better alignment to human cultural preferences is another promising avenue. Adaptive prior-dependent correction (APDC) and coordinated RL approaches, when combined with techniques like activity dependency networks, can extract implicit decision criteria and enhance semantic fidelity.

5. **Interdisciplinary Research Synergy:** Combining insights from computational modeling, social psychology, and cross-cultural studies will be essential. This interdisciplinary approach could lead to the establishment of community standards for hybrid debiasing strategies, which are sensitive to both quantitative metrics and cultural context.

6. **Multimodal and Non-Verbal Data Integration:** Incorporating multimodal data sources (visual, auditory, and even physiological metrics) may offer a more holistic approach to debiasing. Integrative frameworks that simulate realistic social contexts will enhance model training and evaluation.


## Conclusion

Cross-culture self-debiasing through cross-lingual interactions represents a frontier in LLM research. By combining internal self-corrective mechanisms with externally applied debiasing interventions—grounded in robust socio-psychological theories such as the Contact Hypothesis—this interdisciplinary approach offers a scalable and replicable framework for mitigating biases. 

Empirical evidence—from methods like SCD and advanced fusion approaches (FILTER) to iterative reinforcement learning strategies—demonstrates significant potential, with reported bias reductions of up to 40% in remarkably short tuning periods. However, challenges remain, particularly around the integration of culturally rich datasets, efficient multilingual tokenization, and preserving semantic integrity. 

Future work will have to harmonize technical efficiency with cultural sensitivity, ensuring that global LLMs can operate effectively and equitably in multi-cultural contexts. The synthesis of computational and social science techniques promises to yield progress not only in debiasing performance but in the broader quest for culturally competent artificial intelligence.


## References and Further Readings

- PoliTune and Direct Preference Optimization results on Llama3-8B and Mistral-7B.
- Social Contact Debiasing (SCD) experiments on LLaMA 2, Tulu, and NousHermes.
- FILTER method for cross-lingual fusion and its performance on XTREME and XGLUE benchmarks.
- Studies on adaptive reward design, contrastive learning approaches (e.g., CCPA), and manifold learning-based prompt tuning (ADEPT).
- Cross-cultural evaluation frameworks including GramAdapt, GeoMLAMA, and adaptations of CrowS-pairs in non-English languages.
- Interdisciplinary research integrating social psychological theories with large-scale instruction tuning and reinforcement learning frameworks.

This report collects and synthesizes the state-of-the-art learnings from multiple research threads, providing an integrated overview that guides both current practice and future development in the field of LLM debiasing.

---

*Note: The research and methodologies described herein are based on recent developments and should be interpreted with an understanding of ongoing experiments and evolving interdisciplinary approaches in LLM debiasing.*

## Sources

- https://lirias.kuleuven.be/bitstream/123456789/538373/5/manevska__achterberg__houtman__american_journal_of_cultural_sociology_2017.pdf
- http://dx.doi.org/10.1177/0033294117729807
- http://hdl.handle.net/2117/348437
- https://pure.eur.nl/en/publications/ba69818e-a937-4524-899e-2c3d208a6a23
- https://eprints.whiterose.ac.uk/189117/7/farooq22b_interspeech.pdf
- https://dc.etsu.edu/etsu-works/18579
- http://casos.cs.cmu.edu/publications/papers/2008NetworkSimulationModels.pdf
- http://hdl.handle.net/1773/47999
- http://arxiv.org/abs/2310.12560
- https://ojs.aaai.org/index.php/AAAI/article/view/6249
- http://dro.dur.ac.uk/36483/1/36483.pdf
- http://www.scopus.com/inward/record.url?scp=85111243627&partnerID=8YFLogxK
- http://hdl.handle.net/10722/127182
- https://research.tilburguniversity.edu/en/publications/a6b3899b-ad8a-4bb5-bc4f-643640fd0216
- http://arxiv.org/abs/2311.08605
- http://hdl.handle.net/10210/8503
- https://eprints.whiterose.ac.uk/122612/1/dlferrisCogStylesCondAcceptv2.docx
- https://ojs.aaai.org/index.php/AAAI/article/view/17744
- https://aisel.aisnet.org/jais/vol20/iss4/5
- https://doaj.org/toc/1664-1078
- https://zenodo.org/record/5168433
- http://arxiv.org/abs/2308.12539
- https://doaj.org/article/b823d4b4e93b43b2b2f0d7b28d07975f
- http://arxiv.org/abs/2311.09071
- http://hdl.handle.net/1773/40551
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-338548
- http://arxiv.org/abs/2310.18458
- http://journals.rudn.ru/linguistics/article/view/20613/16692
- https://epublications.marquette.edu/cgi/viewcontent.cgi?article=1558&amp;context=edu_fac
- http://arxiv.org/abs/2108.00356
- https://ojs.aaai.org/index.php/AAAI/article/view/17512
- https://dspace.library.uu.nl/handle/1874/350522
- https://research.rug.nl/en/publications/c2101556-c819-4c66-b685-5817cc38bc6f
- http://arxiv.org/pdf/1305.6339.pdf
- http://edoc.mpg.de/226876
- https://espace.library.uq.edu.au/view/UQ:724324
- https://drops.dagstuhl.de/opus/volltexte/2021/14542/
- https://dc.etsu.edu/secfr-conf/2020/schedule/27
- http://urn.fi/URN:NBN:fi:jyu-202001221412
- http://aclweb.org/anthology/P/P14/P14-2072.pdf
- https://opencommons.uconn.edu/dissertations/AAI9707837
- https://research-portal.st-andrews.ac.uk/en/researchoutput/restricted-access-to-working-memory-does-not-prevent-cumulative-score-improvement-in-a-cultural-evolution-task(a606fbe2-8482-4ec3-8f3f-c72bcae2051b).html
- https://hdl.handle.net/2027.42/191727
- http://sse.stevens.edu/fileadmin/cser/2007/proceedings/46.pdf
- https://digitalcommons.law.umaryland.edu/salt/2012/oct6/17
- https://ir.stthomas.edu/cas_soccrim_pub/29
- https://shs.hal.science/halshs-02435197/file/chapter_en.pdf
- http://hdl.handle.net/2027.42/68329
- https://research.rug.nl/en/publications/9e3641c9-1fb6-40e6-9843-d68d2594c267
- https://ojs.aaai.org/index.php/AAAI/article/view/17504
- https://ojs.aaai.org/index.php/AAAI/article/view/4631
- https://hdl.handle.net/2027.42/175267
- https://ojs.aaai.org/index.php/AIES/article/view/31630
- http://hdl.handle.net/11858/00-001M-0000-0019-145F-2
- https://www.zora.uzh.ch/162863
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.80.29
- https://espace.library.uq.edu.au/view/UQ:6f7215f
- https://ojs.aaai.org/index.php/AAAI/article/view/26524
- http://arxiv.org/abs/2307.04280
- http://hdl.handle.net/10.36227/techrxiv.24708198.v1
- http://arxiv.org/abs/2205.12247
- http://ict.usc.edu/pubs/Socio-Cultural%20Modeling%20through%20Decision-Theoretic%20Agents%20with%20Theory%20of%20Mind.pdf
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S235197891500921X/MAIN/application/pdf/be7c98a05ebfc70435f0095aef50592c/main.pdf
- http://arxiv.org/abs/2210.12360
- https://zenodo.org/record/6322643
- https://hdl.handle.net/2152/122644
- https://serval.unil.ch/notice/serval:BIB_55AF78585489
- https://aisel.aisnet.org/cgi/viewcontent.cgi?article=1135&amp;context=icis2022
- http://cds.cern.ch/record/2720464
- https://hal.science/hal-04421595/document
- https://ojs.aaai.org/index.php/AAAI/article/view/21341
- http://arxiv.org/abs/2207.03391
- https://lup.lub.lu.se/record/4b7acb67-7463-43e7-91a5-6ff4d0cdee3e
- http://arxiv.org/abs/2311.01049
- http://arxiv.org/abs/2205.11152
- http://arxiv.org/abs/2308.03188
- https://calhoun.nps.edu/bitstream/handle/10945/30783/10S-SIW-053.pdf?sequence%3D1
- http://www.lscp.net/persons/dupoux/papers/Fourtassi_DD_2014_SelfConsistency.inCogSci.pdf
- http://arxiv.org/abs/2307.02971
- https://openrepository.ru/article?id=15703
- http://arxiv.org/abs/2310.11716
- http://arxiv.org/abs/2307.01595
- https://hrcak.srce.hr/78779
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-197948
- http://arxiv.org/abs/2307.16039
- https://dspace.library.uu.nl/handle/1874/420361
- https://ecommons.luc.edu/cs_facpubs/289
- https://escholarship.org/uc/item/0441n1tt
- https://research.vu.nl/en/publications/4b79b1d7-299b-4881-a1df-089f21211dce
- https://zenodo.org/record/6635194
- http://arxiv.org/abs/2309.00267
- https://zenodo.org/record/6823398
- https://ojs.aaai.org/index.php/AAAI/article/view/26279
- http://arxiv.org/abs/2308.14306
- http://bibliotecadigital.uca.edu.ar/repositorio/revistas/desarrollo-escalas-para-evaluacion.pdf
- https://cris.maastrichtuniversity.nl/en/publications/77f05b96-fb9a-4838-b21c-b9aba8ca66f2
- http://hdl.handle.net/20.500.11897/438390
- http://hdl.handle.net/2152/68903
- https://dspace.library.uu.nl/handle/1874/414830
- http://files.eric.ed.gov/fulltext/ED267303.pdf
- https://hal.inria.fr/hal-03629677
- https://ojs.aaai.org/index.php/AIES/article/view/31715
- http://arxiv.org/abs/2212.12017
- http://hdl.handle.net/10453/134999
- http://www.deomi.org/EOEEOResources/documents/Cross-level_Measurement_of_CC_Competence-vanDriel.pdf
- http://hdl.handle.net/1885/27481
- https://research.vu.nl/en/publications/c19efcd4-c636-40ba-9545-500610e03f20
- http://hdl.handle.net/10197/12456
- https://zenodo.org/record/8296440
- https://zenodo.org/record/7508054
- https://www.open-access.bcu.ac.uk/16136/
- http://www.chariscorp.com/wp-content/uploads/Introducing_Change_Across_Cultures_GLOBE.pdf
- http://arxiv.org/abs/2311.09205
- https://ojs.aaai.org/index.php/AIIDE/article/view/21967
- http://hdl.handle.net/20.500.11897/260330
- https://escholarship.org/uc/item/27v6k0d4
- https://ojs.aaai.org/index.php/AAAI/article/view/26879
- https://espace.library.uq.edu.au/view/UQ:296979
- http://arxiv.org/abs/2210.04492
- http://arxiv.org/abs/2310.12481
- https://ojs.aaai.org/index.php/AIES/article/view/31612
- https://scholarworks.bgsu.edu/psychology_diss/129
- http://arxiv.org/abs/2311.08711
- https://hal.science/hal-03984522/file/10.1515_lingty-2022-0005-1.pdf
- http://hdl.handle.net/1773/47617
- https://eprints.lancs.ac.uk/id/eprint/134400/
- http://nsuworks.nova.edu/cgi/viewcontent.cgi?article%3D1628%26context%3Dtqr
- https://dx.doi.org/10.1515/applirev-2024-0188
- https://drops.dagstuhl.de/opus/volltexte/2014/4594/
- http://hdl.handle.net/11346/BIBLIO@id=6875735052243671761
- http://hdl.handle.net/11582/331001
- https://hal.science/hal-03812319/document
- https://dx.doi.org/10.1186/s12889-023-15309-3
- https://research.rug.nl/en/publications/d9aca9fc-8185-4805-a553-5cda25a5a694
- http://arxiv.org/abs/2307.01503
- http://www-speech.sri.com/people/nfa/Publications/ayan-amta04-multialign.pdf
- https://scholarship.law.upenn.edu/faculty_scholarship/1680
- http://pubman.mpdl.mpg.de/pubman/item/escidoc%3A2044827/component/escidoc%3A2044941/Roberts_2014.pdf
- https://espace.library.uq.edu.au/view/UQ:83c0fce
- http://arxiv.org/abs/2311.05553
- https://doi.org/10.3389/fpsyg.2018.00005
- https://www.idref.fr/229784178
- https://digitalcommons.lmu.edu/cgi/viewcontent.cgi?article=1324&amp;context=honors-research-and-exhibition
- https://pub.uni-bielefeld.de/record/2966247
- https://hdl.handle.net/10657/15750
- https://madoc.bib.uni-mannheim.de/52168/
- http://hdl.handle.net/1721.1/58926
- https://lirias.kuleuven.be/handle/123456789/278241
- https://biblio.ugent.be/publication/8683965/file/8750332
- http://qualitysafety.bmj.com/content/early/2013/08/30/bmjqs-2012-001713.full.pdf
- http://eprints.gla.ac.uk/view/author/3606.html
- http://hdl.handle.net/2429/58658
- https://research.rug.nl/en/publications/00e97d59-48f4-42ce-8091-16ddfe1fc0e5
- https://scholarworks.utep.edu/cgi/viewcontent.cgi?article=2752&amp;context=cs_techrep
- http://libres.uncg.edu/ir/uncg/f/Lowery_uncg_0154D_10834.pdf
- https://pub.uni-bielefeld.de/record/2478013
- http://hdl.handle.net/11582/5252
- https://digitalcommons.wayne.edu/humbiol/vol83/iss2/7
- http://arxiv.org/abs/2308.09662
- https://scholarworks.gvsu.edu/iaccp_papers/50
- https://revistas.ucp.pt/index.php/jsta/article/view/7328
- http://hdl.handle.net/10356/72909
- http://www.mt-archive.info/LREC-2008-Babych-2.pdf
- http://arxiv.org/abs/2310.08754
- https://eprints.whiterose.ac.uk/202071/8/farooq23_interspeech.pdf
- https://doi.org/10.1186/s12874-020-01056-1
- https://hsrc.himmelfarb.gwu.edu/smhs_psych_facpubs/1553
- https://ojs.unito.it/index.php/deeuropa/issue/view/586/405
- http://creativecommons.org/licenses/by-nc-nd/3.0/es/
- https://openaccess.city.ac.uk/id/eprint/22233/1/DebiasingTrainingTransfers_InPress.pdf
- http://dx.doi.org/10.1002/per.1960
- https://ojs.aaai.org/index.php/AIES/article/view/31616
- https://pure.eur.nl/en/publications/954c1a75-2e6d-4534-8bf7-b2e07dee2521
- https://cris.maastrichtuniversity.nl/en/publications/d4b58aa3-2966-4958-bf19-903b7bfe136b
- http://www.umiacs.umd.edu/%7Ejbg/docs/jbg-mlslda-2010.pdf
- http://www.lingref.com/isb/4/001ISB4.PDF
- https://dc.etsu.edu/etsu-works/2061
- https://works.bepress.com/nasser_kashou/52
- https://eprints.lancs.ac.uk/id/eprint/3578/
- https://ojs.aaai.org/index.php/AAAI/article/view/25911
- https://hdl.handle.net/1721.1/127502
- https://ojs.unito.it/index.php/deeuropa/article/view/7139
- https://doi.org/10.1007/s10942-019-00319-1
- http://arxiv.org/abs/2205.12676
- http://arxiv.org/abs/2308.13089
- http://www.loc.gov/mods/v3
- http://files.eric.ed.gov/fulltext/ED478486.pdf