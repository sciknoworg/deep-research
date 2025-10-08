# Final Report: Hallucinations and Data Augmentation in Low-Resource Neural Machine Translation (NMT)

## Abstract

This report provides a comprehensive analysis of hallucination-based approaches and synthetic data augmentation techniques to improve Neural Machine Translation (NMT) in low-resource languages. The study synthesizes a broad range of research findings, including empirical evaluations in Spanish–English and Hindi–English translation tasks, the incorporation of multiple unigram translations into hallucinated phrase tables, and the integration of aggressive feature functions and pruning strategies. In addition to exploring synthetic rare-word augmentation and curriculum training, the report discusses alternative training strategies such as adequacy-oriented reinforcement learning and methods for mitigating exposure bias. Finally, implications for future research, including potential applications for emerging low-resource languages and novel intersections with adversarial training, are discussed.

## 1. Introduction

Neural Machine Translation faces significant challenges when applied to low-resource languages due to limited parallel corpora and coverage of linguistic phenomena. Recent research has identified counter-intuitive yet promising techniques, such as the deliberate introduction of hallucinated data, to address these issues. It is essential to clarify that the notion of hallucinations in this context extends beyond unintended model outputs to include deliberately induced “hallucinations” as a form of data augmentation.

This report reviews techniques that *deliberately produce hallucinations* (e.g., hallucinated phrase tables, synthetic rare-word augmentation) to boost translation quality, alongside examinations of reinforcement learning strategies that optimize adequacy metrics, such as BLEU and CHRF3. We aim to present a detailed synthesis of these techniques and their empirical impact, particularly in language pairs like Spanish–English, Hindi–English, German–English, and French–English.

## 2. Hallucinated Phrase Tables: Structure and Mechanism

### 2.1 Building Hallucinated Data

A core finding in the reviewed literature is the construction of hallucinated phrase tables for low-resource translation. The mechanism involves combining multiple unigram translations derived from:

- **Baseline Phrase Tables:** Traditional phrase extraction methods yield a starting point for translation probabilities.
- **Monolingually Induced Translations:** These are generated from monolingual data that has been processed through auxiliary translation models or language models (e.g., BERT).

This combination is enhanced by incorporating up to 30 novel feature functions, which embed diverse linguistic signals to offset the trade-off between precision and recall. Aggressive pruning strategies are employed to filter out noise, thereby maintaining an acceptable level of precision even as recall is increased. Empirical evaluations have demonstrated significant improvements in quality for Spanish–English and Hindi–English translations when using these hallucinated phrase tables.

### 2.2 Noise Management and Trade-Offs

The introduction of noise via hallucinated entries is an inherent risk. The approach prioritizes high recall, ultimately increasing coverage of rare or unseen translations at the expense of precision. The integration of 30 feature functions provides significant robustness. These feature functions can capture syntactic, semantic, and even contextual signals, making it easier for the translation model to assign higher confidence scores to contextually appropriate phrase pairs. Aggressive pruning is vital here to remove spurious translations that do not contribute to adequate translation quality.

## 3. Synthetic Data Augmentation Approaches

### 3.1 Rare-Word Augmentation

A recurring challenge in low-resource scenarios is the poor representation of rare or infrequent words. Synthetic data augmentation techniques have been developed specifically to target these words by generating enriched sentence pairs that provide contextually varied examples. Empirical studies point out that such methods have led to improvements of up to 2.9 BLEU points over baseline systems and 3.2 BLEU points relative to back-translation methods. The approach benefits from:

- **Incorporation of Bilingual Word Embeddings:** These embeddings capture cross-lingual semantic similarities and help anchor rare words in a shared vector space.
- **Application of Pre-trained BERT Models:** The context-aware representations from BERT further refine the translation output, offering improved generalization for rare words.

### 3.2 Complementary Strategies with Curriculum Training

Synthetic rare-word augmentation can also be enhanced by adopting curriculum training strategies. Such strategies involve a progressive training regime, where the model is first exposed to simpler or more frequent examples before tackling complex and rare entries. Additional techniques include:

- **Neighboring Sample Diversification:** By leveraging translations from nearby samples, the models can be trained on a diversified set of representations for the same or similar inputs.
- **Cross-Lingual Embedding Alignment:** It ensures that vector representations of words from different languages are brought into an aligned space, facilitating better translation of low-frequency words.

These approaches, when used in tandem with hallucination-based methods, can synergistically boost overall BLEU and CHRF3 scores in a unified training framework.

## 4. Alternative Training Strategies

### 4.1 Adequacy-Oriented Reinforcement Learning

Another dimension of the research explores framing NMT as a stochastic policy optimization problem with adequacy-oriented rewards. Unlike maximum likelihood estimation (MLE) or coverage-augmented approaches, these methods provide explicit sequence-level and word-level feedback during training. Metrics such as word-level BLEU and character-level CHRF3 form the basis for the reward function. This approach has several advantages:

- **Mitigation of Exposure Bias:** By training with sequence-level rewards, the model is less prone to errors that accumulate during inference.
- **Enhanced Robustness:** Adequacy-oriented reinforcement learning tends to produce models that are more robust to domain shifts and variations in the input data.

These methods have been extensively tested across diverse language pairs, demonstrating consistent improvements over both standard MLE and more advanced attention-based models.

### 4.2 Minimization of Exposure Bias via Minimum Risk Training

Exposure bias, where the model’s generation process deviates due to the discrepancy between training and inference distributions, has also been addressed using Minimum Risk Training (MRT). This approach modifies training objectives to focus on minimizing the risk associated with translation errors, further reducing the impact of hallucinations that arise from domain shifts. Studies suggest that fine-tuning beam search and adjusting model parameters under MRT conditions could complement hallucination reduction, especially in low-resource scenarios.

### 4.3 Synergies with Adversarial Training

Recent work indicates potential synergies when combining reinforcement learning and adversarial training to enhance adequacy. Adversarial training introduces perturbations or removes noise through competing objectives, thereby refining both the generated outputs and the underlying feature representations. Although still largely experimental, the integration of adversarial losses alongside adequacy-based rewards could serve as a potent means to curtail unintended model outputs and further harness hallucinated data effectively.

## 5. Empirical Impact and Evaluation

The studies highlighted in this report show considerable empirical gains from the aforementioned approaches:

- **Quantitative Improvements:** Statistical metrics reveal improvements ranging from 2.9 to 3.2 BLEU points in several translation tasks. Notably, the deliberate generation of hallucinated phrase tables has led to improved translation quality in Spanish–English and Hindi–English pairs by boosting coverage and recall.

- **Comprehensive Evaluation Metrics:** The use of both word-level BLEU and character-level CHRF3 allows a multidimensional assessment of translation adequacy, capturing both lexical accuracy and morphological reliability. This dual-metric approach ensures that increases in recall do not come at the cost of overall translation quality.

- **Noise and Domain Handling:** The combined effects of hallucinated data, synthetic data augmentation, and reinforcement learning indicate that properly managed noise can serve as an asset rather than a detriment, particularly in settings where parallel data is scarce.

## 6. Discussion and Future Directions

### 6.1 Deliberate Hallucinations vs. Unintended Model Outputs

It is important to differentiate between the deliberate induction of hallucinations as a data augmentation strategy and the unintended outputs that typically plague NMT under domain shift conditions. The deliberate approach aims to strategically increase recall by synthesizing plausible translations that are later pruned. This is distinct from the common narrative around hallucination in NMT, wherein unintended outputs are seen solely as negative artifacts that need correction.

### 6.2 Broader Applicability Across Language Families

While the improvements have been most clearly demonstrated in languages like Spanish, Hindi, German, and French paired with English, there is significant potential for extending these methods to other language families. A more systematic examination across unrelated language pairs could further validate the generality of hallucination-based augmentation and reinforcement learning strategies.

### 6.3 Integration of Latest Technological Advances

Emerging techniques in unsupervised learning, self-supervised methods, and large-scale pre-trained language models (exemplified by subsequent generations after BERT) are continuously altering the landscape of MT. Future research may benefit from integrating these advanced representations to further enhance hallucination-based translation augmentation. Additionally, leveraging adversarial and reinforcement techniques in a multi-task learning framework could provide a more holistic solution to both noise management and rare word propagation.

### 6.4 Recommendations for Further Research

Based on the synthesis of research learnings, several promising avenues deserve exploration:

1. **Dynamic Pruning Algorithms:** Developing adaptive pruning mechanisms that can tune the precision-recall balance in real-time during training.

2. **Hybrid Augmentation Techniques:** Combining hallucinated data with traditional back-translation and augmented rare-word data to investigate potential additive gains.

3. **Fine-Grained Adequacy Metrics:** Exploring more granular metrics beyond BLEU and CHRF3, perhaps through semantic similarity measures or contextual embeddings, to better capture translation adequacy.

4. **Cross-Lingual Transfer Learning:** Employing cross-lingual embedding alignment in a multi-lingual setting could leverage shared linguistic features across low-resource languages, thus magnifying the benefits of hallucination-induced data augmentation.

5. **Adversarial Reinforcement Learning:** Further exploration into adversarial policies combined with reinforcement learning objectives might provide a streamlined solution to mitigate unforeseen model outputs while preserving high recall.

## 7. Conclusion

This report has comprehensively examined the use of hallucinations and synthetic data augmentation strategies to enhance low-resource NMT. By combining hallucinated phrase tables with aggressive pruning and enriched by multiple novel feature functions, researchers have demonstrated measurable improvements in translation quality. Moreover, augmented rare-word generation, curriculum training, and adequacy-oriented reinforcement learning offer complementary approaches that address the multifaceted challenges in this domain.

The convergence of these methods not only provides new insights into managing the delicate balance between precision and recall in low-resource settings, but also opens up exciting avenues for future research. As the NMT community continues to integrate novel data augmentation techniques with advanced training paradigms, the prospects for overcoming the limitations inherent in low-resource languages are increasingly promising.

Overall, the deliberate use of hallucinations—when properly managed—is emerging as a transformative tool in the quest to develop more robust, accurate translation systems for languages that have historically lacked sufficient parallel corpora. Future explorations should focus on integrating these methods with evolving technologies to unlock further improvements and wider applicability across diverse linguistic landscapes.

---
*Note: Some of these proposals remain speculative and require further empirical validation in operational settings.*

## Sources

- http://www.mt-archive.info/EMNLP-2007-Johnson.pdf
- http://hdl.handle.net/10138/563803
- https://ojs.aaai.org/index.php/AAAI/article/view/6514
- https://ojs.aaai.org/index.php/AAAI/article/view/26596
- https://doi.org/10.5445/IR/1000149804
- https://orcid.org/0000-0001-5736-5930
- http://hdl.handle.net/10251/201319
- https://doaj.org/article/e7de26d224fe42ec978c343c9eb19e5b
- http://hdl.handle.net/1721.1/103745
- http://www.loc.gov/mods/v3
- https://ojs.aaai.org/index.php/AAAI/article/view/4631
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll89/id/120458
- https://research.monash.edu/en/publications/e7af0388-d67e-4f54-826e-ce01c9c6b6dc
- http://www.nusl.cz/ntk/nusl-501419
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.434.229
- https://www.zora.uzh.ch/id/eprint/188223/1/2020.acl-main.326.pdf
- https://zenodo.org/record/1019697
- https://hdl.handle.net/2123/28809
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-421814
- http://hdl.handle.net/11346/BIBLIO@id=6912452893394780431
- http://arxiv.org/abs/2202.03629
- https://www.neliti.com/publications/398463/the-impact-of-translation-techniques-on-the-accuracy-of-the-translation-of-commi
- https://norma.ncirl.ie/5080/
- https://research.monash.edu/en/publications/a5f41e59-c85f-41dc-b766-781919eb020c
- http://hdl.handle.net/11250/2404116
- https://norma.ncirl.ie/4817/
- https://hdl.handle.net/10356/157475
- https://norma.ncirl.ie/3348/1/robertcallaghan.pdf
- https://etheses.whiterose.ac.uk/14284/1/thesis.pdf