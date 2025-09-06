# Final Report on Resolving Ambiguous Translations via Language Model Prompting

This report synthesizes extensive research findings related to the resolution of lexical and structural ambiguities in machine translation, especially through advanced language model prompting techniques. It covers theoretical foundations, computational methodologies, empirical evaluations, and domain-specific adaptations, with particular focus on how iterative and context-aware approaches can mitigate ambiguity. The following sections provide a detailed account of the state-of-the-art methods, historical perspectives, and emerging innovations.

---

## 1. Introduction

Ambiguous translations remain one of the most challenging aspects in machine translation (MT) and natural language processing (NLP). These ambiguities can be broadly categorized into lexical challenges (polysemy) and structural/contextual issues that necessitate resolving interactions between syntax, semantics, and real-world cues. In recent years, language model prompting has emerged as a promising technique to address these challenges by harnessing both pre-trained transformer architectures and interactive prompting frameworks.

While traditional rule-based systems (like the Verbmobil legacy system) used static, multi-level contextual cues such as structural, semantic, prosodic, and discourse information, modern neural techniques leverage a combination of context-aware fine-tuning, sense embeddings, and iterative prompting. The goal of this report is to collate and elaborate on the gamut of findings from research, offering insights into methods that resolve ambiguous translations through dynamic language model prompting.

---

## 2. Historical and Traditional Approaches

### 2.1. Rule-Based Systems and Lexicalist Transfer

Early efforts in ambiguity resolution relied heavily on rule-based approaches. The Verbmobil system, notable for its lexicalist transfer method, combined multi-level contextual cues (structural, semantic, prosodic, and speech act information) to constrain ambiguous lexical mappings. However, its rigid rule-based design was limited by inflexibility in handling novel and dynamic language usages.

### 2.2. Statistical and Finite-State Techniques

Subsequent approaches integrated statistical models and Weighted Finite-State Transducers (WFSTs). For example, WFST-based techniques pre-compose statistical submodels—transforming n-gram grammars into efficient finite-state transducers—to reduce decoding ambiguities and speed up the translation process. Empirical evidence, such as a 2.9% improvement in word error rate on a Japanese spontaneous speech recognition task and a 7.3% relative improvement in broadcast audio recognition, underscores the practical benefits of these methods.

### 2.3. Bayesian and Unsupervised Bootstrapping Methods

Further progress was achieved through diverse computational approaches—including Bayesian discriminators, decision lists, and unsupervised bootstrapping from machine-readable dictionaries. These methods have delivered accuracies exceeding 96% on tasks like text-to-speech accent restoration and translation disambiguation in languages such as Spanish and French. Moreover, unsupervised methods using adaptive clustering algorithms (e.g., k-means, Chinese restaurant processes) have shown efficacy for word-sense disambiguation (WSD) in low-resource settings.

---

## 3. Modern Approaches and Contextual Integration

### 3.1. Sentence-Level and Document-Level Contextual Fine-Tuning

Modern translation systems now routinely incorporate sentence-level and even document-level contextual fine-tuning at inference time. This approach leverages abundant sentence-level data and addresses lexical ambiguities and coherence challenges by integrating inter-sentential cues. The improvements in BLEU scores, coupled with error reduction noted in human assessments, confirm that dynamically incorporating context is critical. Furthermore, integration of UD-based syntactic equivalence metrics (e.g., SACr and ASTrED) has demonstrated improved system ranking for language pairs like English-Dutch.

### 3.2. Cross-Modal and Interactive Approaches

Recent studies emphasize cross-modal integration where visual scene context and prosodic inputs are used alongside textual cues to simulate human disambiguation. Empirical evidence from eye-tracking studies and reading span tasks shows that native speakers effectively integrate contrastive prosody with visual contrasts, whereas L2 speakers often struggle under similar multimodal conditions. Additionally, iterative approaches such as interactive-chain prompting decompose translation tasks into sub-problems resolved over multiple sequential interactions (up to eight-step processes). Although this may increase inference calls and latency, it has been shown to yield significant improvements in resolving both lexical and structural ambiguities.

### 3.3. Neural Architectures and Sense Embeddings

The advent of neural machine translation (NMT) has prompted the adoption of advanced neural architectures that incorporate fine-grained sense embeddings. By concatenating word vectors with sense-specific embeddings or integrating lexical chain inputs, modern systems have reached disambiguation rates of around 70% for ambiguous words, with additional gains in BLEU scores and manual quality assessments. Comparative evaluations, such as those between ModernMT and DeepL in legal domain translations, have illustrated that neural approaches—with additional contextual fine-tuning—can substantially outperform legacy systems.

---

## 4. Domain-Specific Considerations and Evaluations

### 4.1. Legal and Technical Translation Domains

Legal translation poses unique challenges due to the interplay of lexical, structural, and socio-cultural factors. Research reviewed herein indicates that legal ambiguity arises not only from translator competence issues but also from inherent cultural discrepancies. Integrated frameworks that combine legal, contextual, macrotextual, and microtextual evaluations have been developed to enhance objectivity. For instance, modern NMT systems in legal settings have managed to balance reduced errors in terminology (around 8.43% vs. 9.22% in competing systems) with improved BLEU scores (e.g., 29.14 vs. 27.02), although challenges remain in managing rare senses and domain-specific terminology.

Technical translation, similarly, benefits from a dual focus on semantic clarity and structural transformation. Comparative studies have provided evidence that pre- and post-editing practices remain integral to handling technical texts where ambiguous phrase structures (such as relative clauses) must be adjusted to maintain precision and coherence. Moreover, methodologies such as Hallucinating phrase translations—where multiple unigram translations are aggressively pruned—have been leveraged in low-resource scenarios for Spanish–English and Hindi–English settings, balancing recall and precision.

### 4.2. Evaluation Frameworks and Benchmark Datasets

Robust evaluation frameworks are essential for the advancement of ambiguity resolution in MT. Benchmark datasets like MuCoW and XL‐WSD, covering multiple language pairs with sense-annotated data, have standardized fair evaluations between neural methodologies and knowledge-based approaches. Additionally, emerging legal translation evaluation frameworks employ holistic metrics that consider lexicometric analysis, mixed-method studies, and traceable decision-making processes. These frameworks ensure that quality assessments account for both sentence-level lexical cohesion and overarching discourse coherence.

Metrics beyond BLEU, such as MEANT for semantic SMT and deep linguistic evaluations like SemPOS and BLANC, have provided improved correlations with human judgments. New evaluation strategies—including forced-choice binary comparisons and ambiguity-preserving techniques using weighted finite-state transducers—have also emerged, underscoring the need for dynamic, multi-layered assessments in both research and production settings.

---

## 5. Comparative Analysis and Innovative Prompting Frameworks

### 5.1. Lexical vs. Structural Ambiguity Resolution

The research highlights a bifurcated approach to ambiguity. Lexical disambiguation, centered on polysemy resolution, often benefits from techniques such as adaptive clustering and synset embeddings, while structural ambiguity requires more dynamic handling of context, syntactic cues, and document-level structures. Experimental studies—including those involving bilingual lexical access with Spanish-English homographs—illustrate that interference control and nonselective activation of lexical items are highly sensitive to task demands and language pair specifics.

### 5.2. Interactive Chain Prompting and Iterative Decomposition

A particularly promising approach is the interactive-chain prompting framework. By decomposing the translation process into iterative sub-tasks, this method not only manages ambiguity more granularly but also ensures that intermediate decisions are contextually validated. Although this increases computational overhead, real-time translation systems—when optimized via constrained decoding and adaptive caching—can mitigate these costs. For low-resource language pairs, integrating Chain-of-Thought strategies can be a viable solution to providing intermediate reasoning, thereby refining the translation process.

### 5.3. Proactive Adaptations for Future Research

Looking forward, several innovative solutions could further enhance ambiguity resolution in language model prompting:

- **Hybrid Neuroimaging-Informed Models:** Integrating ERP’s temporal resolution with fMRI’s spatial mapping could lead to models that dynamically adjust for bilingual interference based on real-time cognitive load assessments.
- **Dynamic Prompt Generation:** Leveraging Chain-of-Thought prompts within neural architectures might scaffold multi-step reasoning processes, particularly for structural ambiguities in legal texts or low-resource languages.
- **Multi-modal Enhancements:** Coupling visual and prosodic cues with textual inputs in real-time interactive systems can offer richer context for disambiguation, as supported by research on cross-modal lexical priming.
- **Adaptive Evaluation Metrics:** Continued development and integration of advanced metrics (e.g., SemPOS, BLANC) with real-time quality estimation frameworks will be essential for scaling translation systems and ensuring they meet both automated and human-assessment standards.
- **Enhanced CAT Tool Integration:** As modern translations increasingly rely on computer-assisted translation (CAT) systems, refining training modules to incorporate real-time QA feedback and adaptive caching can help reduce post-editing burdens and improve translator productivity.

---

## 6. Conclusion

The landscape of resolving ambiguous translations via language model prompting is evolving rapidly. With traditional methods such as rule-based lexical transfer and WFSTs laying the groundwork, modern systems are moving towards interactive, context-aware, and multimodal approaches that bridge the gap between purely statistical methods and dynamic cognitive modeling.

By integrating sentence-level and document-level contextual cues, leveraging advanced neural architectures with sense embeddings, and enabling iterative prompting strategies, contemporary systems can achieve significant enhancements in translation quality across diverse domains. The challenges – particularly in the legal and technical translation sectors – demand specialized frameworks that amalgamate explicit linguistic markers with computational innovations.

Future research will likely continue to explore the integration of cross-modal data, the incorporation of Chain-of-Thought approaches for structured reasoning, and the development of hybrid neuroimaging-informed models to pinpoint and remediate bilingual interference. This multipronged strategy promises to push the field closer to human-level performance in handling both lexical and structural ambiguities, thereby enhancing the overall efficacy and utility of machine translation systems.

---

## 7. References to Empirical Findings and Future Directions

- **Empirical Evidence:** The report synthesizes findings demonstrating that contextual fine-tuning improves BLEU scores and reduces disambiguation error rates by nearly 20% manual accuracy enhancements. These results were validated across various language pairs (e.g., English-Spanish, English-German, Chinese-English) and tasks including legal translations and spoken language processing.

- **Future Innovations:** Proposals for dynamic prompt generation, adaptive evaluation metrics, and cross-modal integration offer promising avenues for future exploration. These innovations will be critical for handling low-resource languages and specialized translation domains where ambiguity is most pronounced.

In summary, the integration of interactive and context-aware prompting frameworks, enriched by a detailed understanding of both lexical and structural ambiguity, sets the stage for the next generation of machine translation systems. These systems will be better equipped to incorporate multi-layered contextual information and dynamic user feedback, ultimately bringing us closer to fully resolving the challenges of ambiguous translation in an increasingly interconnected linguistic landscape.

---

This detailed synthesis aims to serve as a comprehensive resource for researchers and practitioners seeking to navigate the complexities of ambiguity in machine translation through modern prompting techniques. The convergence of theoretical insights, empirical validations, and innovative proposals marks a significant milestone in the pursuit of more accurate, contextually coherent, and adaptive translation systems.

## Sources

- https://hdl.handle.net/1721.1/145034
- https://lirias.kuleuven.be/handle/123456789/656784
- https://surrey.eprints-hosting.org/852486/1/ITI_ResearchNetwork2018.pdf
- http://id.erudit.org/iderudit/002907ar
- http://www.computing.dcu.ie/~ygraham/lfg07.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.91.3641
- https://rio.tamiu.edu/psych_comm_facpubs/1
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.77.4606
- https://research.tilburguniversity.edu/en/publications/cb93fbb0-c33c-4dd8-8e45-115edb7ee07f
- http://disi.unitn.it/~riccardi/papers/mt_journal_special-02.pdf
- http://www.mt-archive.info/NAACL-HLT-2007-Utiyama.pdf
- https://doaj.org/toc/2391-8179
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.77.1809
- https://scholarworks.utep.edu/open_etd/766
- https://ezproxy.uws.edu.au/login?url=https://doi.org/10.1177/0023830918808823
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.67.451
- http://csjarchive.cogsci.rpi.edu/Proceedings/2008/pdfs/p663.pdf
- http://hdl.handle.net/10446/70190
- http://dspace.mit.edu/bitstream/handle/1721.1/75653/818354322-MIT.pdf%3Bjsessionid%3DCC57D1E605D531A0E5048B5A94E414E8?sequence%3D2
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.46.7485
- https://archive-ouverte.unige.ch/unige:100814
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.87.1793
- http://www.dlsi.ua.es/%7Efsanchez/pub/pdf/espla-gomis15c.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.64.553
- http://dx.doi.org/10.7910/DVN/W6WJVN
- http://amslaurea.unibo.it/view/cds/CDS9174/
- http://hdl.handle.net/2066/85875
- http://www.statmt.org/wmt09/pdf/WMT-0940.pdf
- https://hal.archives-ouvertes.fr/hal-01838551
- https://lirias.kuleuven.be/bitstream/123456789/603269/1/ThesisR1_Khachatryan_accepted.pdf
- https://doaj.org/toc/2386-0316
- http://doras.dcu.ie/22664/
- http://www.nusl.cz/ntk/nusl-304321
- https://repository.upenn.edu/cis_papers/11
- https://eprints.lancs.ac.uk/id/eprint/225755/
- http://wing.comp.nus.edu.sg/~antho/P/P13/P13-2067.pdf
- http://hdl.handle.net/11346/BIBLIO@id=-1880346103131882362
- https://orcid.org/0000-0003-2923-8365
- http://hdl.handle.net/10356/48055
- http://hdl.handle.net/2060/20110023765
- http://hdl.handle.net/11701/37323
- https://eprints.whiterose.ac.uk/152594/1/coli_a_00356.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.54.7465
- http://www.aclweb.org/anthology/W/W14/W14-4016.pdf
- http://hdl.handle.net/2072/405531
- https://repository.rudn.ru/records/article/record/6950/
- https://www.aclweb.org/anthology/2020.lrec-1.452.pdf
- https://archive-ouverte.unige.ch/unige:5699
- http://www.nusl.cz/ntk/nusl-510345
- http://aune.lpl-aix.fr/~frenck/pdfs/frenckpynte.pdf
- https://www.zora.uzh.ch/id/eprint/135056/
- https://dare.uva.nl/personal/pure/en/publications/understanding-and-enhancing-the-use-of-context-for-machine-translation(422122ad-f9d6-4952-9012-fcde9a820773).html
- http://www.mt-archive.info/CL-2004-Casacuberta.pdf
- https://doi.org/10.1017/S0731126500001219
- http://www.mt-archive.info/IWSLT-2007-Shen-2.pdf
- http://real.mtak.hu/144429/
- http://www.mt-archive.info/LREC-2008-Mauser.pdf
- http://aclweb.org/anthology/C/C14/C14-1040.pdf
- http://www.nusl.cz/ntk/nusl-501419
- https://hal.archives-ouvertes.fr/hal-02316397/document
- http://hdl.handle.net/2066/90090
- https://www.usenix.org/legacy/events/vee06/full_papers/p175-sridhar.pdf
- https://www.openaccessrepository.it/record/115395
- https://escholarship.org/uc/item/9t48p3x5
- http://arodes.hes-so.ch/record/3361
- http://hdl.handle.net/11368/2948249
- http://scholarbank.nus.edu.sg/handle/10635/41613
- https://hdl.handle.net/10356/93913
- http://doras.dcu.ie/19107/
- http://mte2014.github.io/MTE2014-Workshop-Proceedings.pdf
- http://hdl.handle.net/20.500.11850/626756
- https://doaj.org/article/aec492fc1d214b57a90d737e84763695
- http://hdl.handle.net/10045/76022
- http://hdl.handle.net/1903/11217
- http://hdl.handle.net/2066/203149
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1877042815056906/MAIN/application/pdf/ccbd141db0b0e1748076e20caf976ea3/main.pdf
- https://archive-ouverte.unige.ch/unige:99298
- http://www.mt-archive.info/Coling-2010-Yang.pdf
- http://hdl.handle.net/10.1184/r1/7347104.v1
- http://hdl.handle.net/10379/14889
- https://www.tdcommons.org/cgi/viewcontent.cgi?article=6275&amp;context=dpubs_series
- http://hdl.handle.net/1854/LU-8700133
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.94.6245
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.81.6936
- http://hdl.handle.net/2117/13092
- http://hdl.handle.net/11582/250630
- http://www.repositoriodigital.ipn.mx
- http://hdl.handle.net/10393/27425
- http://hdl.handle.net/2445/105793
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.78.1005
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.5.7304
- https://doi.org/10.18653/v1/2020.acl-main.448.
- https://www.repository.cam.ac.uk/handle/1810/360866
- https://doaj.org/article/7fd0243982f04cd69d17d35b9811b22a
- https://repository.upenn.edu/dissertations/AAI9628034
- http://ediss.sub.uni-hamburg.de/volltexte/2010/4800/pdf/Patrick.McCrae_PhD.Thesis.pdf
- http://www.mt-archive.info/HLT-EMNLP-2005-Vickrey.pdf
- https://biblio.ugent.be/publication/6934900/file/6934929
- http://www.mt-archive.info/EMNLP-2008-Sanchis-Trilles.pdf
- https://hdl.handle.net/1721.1/125796
- http://web.eecs.umich.edu/~mihalcea/papers/banea.iwcs11.pdf
- http://clg.wlv.ac.uk/papers/Specia_EAMT2006.pdf
- https://figshare.com/articles/Challenges_in_Predicting_Machine_Translation_Utility_for_Human_Post-Editors/6473105
- https://norma.ncirl.ie/5081/
- http://hdl.handle.net/21.11116/0000-0004-7985-E
- http://etd.adm.unipi.it/theses/available/etd-04122023-101720/
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0885230814001016/MAIN/application/pdf/7c087210ed4577379a141a0c7c718a2f/main.pdf
- http://www.mt-archive.info/EACL-2006-Wang.pdf
- http://www.cis.upenn.edu/%7Eljunyi/papers/discourse_mt.pdf
- http://www-cogsci.ucsd.edu/~coulson/cogs179/rodriguez-fornells.pdf
- https://research.monash.edu/en/publications/e7af0388-d67e-4f54-826e-ce01c9c6b6dc
- https://ufal.mff.cuni.cz/%7Etamchyna/papers/2013-wds.pdf
- http://files.eric.ed.gov/fulltext/ED275717.pdf
- http://publications.idiap.ch/downloads/papers/2013/Hajlaoui_CICLING-2013_2013.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.4907
- https://www.zora.uzh.ch/id/eprint/139470/1/LexChains_WSD.pdf
- https://researchmgt.monash.edu/ws/files/354703124/354699773_oa.pdf
- https://eprints.whiterose.ac.uk/158907/1/_SLTU20__Investigating_Language_Impact_in_Bilingual_Approaches_for_Computational_Language_Documentation.pdf
- https://nrc-publications.canada.ca/fra/voir/objet/?id=9acb3f2a-4cd2-47f7-b3ca-a73aa0efa9df
- http://hdl.handle.net/11582/325888
- http://nlp.stanford.edu/pubs/conll15_nlm.pdf
- https://digitalcommons.usu.edu/comd_facpub/287
- https://archive-ouverte.unige.ch/unige:43275
- https://orcid.org/0000-0002-9979-2188
- https://zenodo.org/record/834305
- http://staffwww.dcs.shef.ac.uk/people/K.Shah/papers/eamt2014.pdf
- http://hdl.handle.net/10251/64401
- http://hdl.handle.net/11346/BIBLIO@id=-8748738730419561250
- http://arxiv.org/abs/2301.10309
- https://scholarworks.utep.edu/open_etd/2615
- https://biblio.ugent.be/publication/5806135/file/6993787
- http://hdl.handle.net/10.1371/journal.pone.0207741.t001
- https://shs.hal.science/halshs-00190852/document
- http://hdl.handle.net/2066/112947
- http://hdl.handle.net/11346/BIBLIO@id=3218316309289671378
- https://doaj.org/toc/2350-420X
- http://www.mt-archive.info/EMNLP-2004-Tsukada.pdf
- http://www.mt-archive.info/IWSLT-2006-Watanabe.pdf
- https://scholarworks.utep.edu/dissertations/AAI3457763
- http://hdl.handle.net/11858/00-001M-0000-0013-AB98-8
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.434.229
- http://www.mt-archive.info/ACL-1991-Dagan-1.pdf
- https://lirias.kuleuven.be/handle/123456789/585484
- http://www-i6.informatik.rwth-aachen.de/~bender/papers/eamt05.pdf
- http://d-scholarship.pitt.edu/7229/1/Eddington_Chelsea_BphilThesis.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.75.3797
- https://hal.archives-ouvertes.fr/hal-00959144
- https://repository.rudn.ru/records/article/record/66070/
- https://digitalcollection.zhaw.ch/handle/11475/23474
- http://www-i6.informatik.rwth-aachen.de/publications/download/897/WuebkerJoernPeitzStephanAlkhouliTamerPeterJan-ThorstenFengMinweiFreitagMarkusNeyHermann--TheRWTHAachenMachineTranslationSystemsforIWSLT2013--2013.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.90.8451
- https://zenodo.org/record/4011614
- http://aclweb.org/anthology/P/P14/P14-2037.pdf
- http://ukcatalogue.oup.com/product/9780195151770.do
- http://doc.rero.ch/record/331259/files/11196_2014_Article_9390.pdf
- http://hdl.handle.net/11582/306283
- https://zenodo.org/record/2275709
- https://hdl.handle.net/10356/165027
- https://surrey.eprints-hosting.org/854965/1/27558137.pdf
- https://orcid.org/0000-0001-5736-5930
- https://www.matecat.com/wp-content/uploads/2014/11/1643.pdf
- https://doaj.org/article/a229fa052b90496399193a7fb06ea695
- http://www.kecl.ntt.co.jp/icl/signal/hori/publications/thori_icassp03-1.pdf
- https://zenodo.org/record/5543386
- http://doras.dcu.ie/24493/
- https://dialnet.unirioja.es/servlet/oaiart?codigo=5828441
- https://research.rug.nl/en/publications/8ba98488-05c6-4fe4-9203-33c9d96134f8
- http://hdl.handle.net/10045/76031
- https://rio.tamiu.edu/psych_comm_facpubs/2
- https://archive-ouverte.unige.ch/unige:78664
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.476.6933
- https://pressto.amu.edu.pl/index.php/cl/article/view/18273
- http://hdl.handle.net/10344/8184
- https://www.zora.uzh.ch/id/eprint/208876/
- https://www.openaccessrepository.it/record/115307
- https://eprints.whiterose.ac.uk/171411/1/Ref%203%20Findings.pdf
- http://archive-ouverte.unige.ch/unige:31405
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.96.9582
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1877042815044213/MAIN/application/pdf/f1d21219884e72692ecc4985bf3abd4a/main.pdf
- https://escholarship.org/uc/item/90b4b72q
- http://hdl.handle.net/11588/894252
- https://hal.archives-ouvertes.fr/hal-02895907
- http://aclweb.org/anthology/E/E14/E14-4011.pdf
- http://www.nici.ru.nl/~ardiroel/Roelofs_BLC_2006.pdf
- https://doaj.org/article/38d2d368e9e94f638e3158b681ce43e7
- http://hdl.handle.net/2445/65266
- https://hal.archives-ouvertes.fr/hal-00380690
- https://orcid.org/0000-0001-6462-3248
- http://hdl.handle.net/10045/76047
- http://aclweb.org/anthology/D/D14/D14-1130.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.1658
- http://www.loc.gov/mods/v3
- http://hdl.handle.net/10068/151097