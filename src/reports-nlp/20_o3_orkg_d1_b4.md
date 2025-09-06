# Enhancing Multilingual LLM Performance through Prompt-based Common-Sense Integration for Low-Resource Languages

_A comprehensive technical roadmap, 2025-09-04_

---

## 1  Motivation and Problem Statement
Current multilingual large language models (mLLMs) (e.g., XLM-R, mT0, GPT-4o) exhibit impressive zero-shot transfer. Yet their performance on **low-resource languages (LRLs)** degrades markedly, especially on reasoning-heavy downstream tasks (question answering, named-entity recognition, dialogue, code-switch translation). Prior evidence attributes part of the gap to missing **commonsense knowledge (CSK)** and to domain/language mismatch during pre-training. We therefore ask:

> _Can we systematically inject language-agnostic commonsense knowledge into mLLMs at **prompt time** (or with minimal parameter overhead) to close the low-resource gap under tight compute/data budgets?_

The rest of this report distils recent research, identifies knowledge gaps, and proposes an end-to-end experimental plan that combines **prompt engineering, parameter-efficient tuning, and cross-lingual knowledge projection**.


## 2  Target Languages and Tasks
### 2.1  Language Selection Rationale
We prioritise LRLs that are (i) genetically diverse, (ii) geographically disparate, (iii) have a nascent NLP ecosystem, and (iv) exhibit **available evaluation data or feasible construction pipelines**. Drawing on the learnings:

* **Amharic (am)** – Afro-Asiatic; ~32 M speakers; government documents available; no large CSK resources.
* **Yoruba (yo)** – Niger-Congo; ~45 M speakers; script largely Latin; existing Bible-aligned corpora help MT.
* **Sinhala (si)** – Indo-Aryan; ~19 M speakers; *Sinhala WordNet* shows active lexical crowdsourcing momentum.
* **Nepali (ne)** – Indo-Aryan; ~17 M speakers; decent bilingual data via Hindi; underexplored in CSK.

These four satisfy the _"Amharic–Yoruba–Sinhala–Nepali (AYSN) suite"_ we will use henceforth.

### 2.2  Downstream Tasks
1. **Commonsense QA** – primary measure; uses low-shot TG-CSR and CommonsenseQA-Trans.
2. **Named-Entity Recognition (NER)** – XLM-R+MAD-X results motivate cross-task generality.
3. **Machine Translation (MT)** – evaluate hallucination reduction in EN↔LRL by CSK prompts.

The trio spans reasoning, sequence labelling, and sequence-to-sequence paradigms.


## 3  Commonsense Knowledge Sources and Representations
| Source | Size | Pros | Cons | Action in this project |
|--------|------|------|------|------------------------|
| **ConceptNet 5** | 34 M edges | High-coverage English triples; multilingual labels | Anglocentric bias | Translate-project  → AYSN triples |
| **ATOMIC-2020** | 1.33 M if-then chains | Event-centric; cause/effect | English only; free-text nodes | Translate & BLEU rerank, limited to Si/Yoruba |
| **Wikidata-CS** | 2.5 M cleaned triples | Already multilingual; KG-friendly | Sparse for LRLs | Directly usable for KG probing |
| **Hand-crafted rules** (Gordon & Hobbs categories) | 970 curated | Language-independent core | Tiny scale | Use as universal prompt templates |

We will rely on **machine-translated and adversarially validated ConceptNet** as the backbone, leveraging the _136 k Japanese pipeline_ that showed high precision **(research learning #2)**.


## 4  Integration Techniques
### 4.1  In-Context Prompting (ICP)
* Pros: no parameter update; instant iteration.
* Cons: context window cost; retrieval latency.

We design **two-stage prompts**:
1. _Retrieve_ n relevant CSK triples via embedding search (same-language if available, else pivot to English + MT).
2. _Transform_ triples into natural language statements and paste into the system/user fields.

### 4.2  Parameter-Efficient Tuning (PET)
1. **Prefix-Tuning** (0.1–3% params) – matches full fine-tune on CS benchmarks and _generalises better_ (**learning #1**). Implement 100-token virtual prefixes per task.–language pair.
2. **MAD-X Adapters** (≤3% params) – modular language & task adapters; proved cross-lingual gains (**learning #4**). We stack: _language-adapter → CSK-adapter → task-adapter_ (invertible order).
3. **KEAR External Attention** – optional light module to read CSK memory without scaling core model (**learning #10**).

**Why combine ICP and PET?** Under limited GPU hours we can _prototype_ with prompts, then _distil_ successful prompts into prefix vectors (Lester et al., 2021-style), saving tokens at inference.


## 5  Commonsense Knowledge Construction for AYSN Suite
The **cross-lingual knowledge projection pipeline** is adapted as follows:

1. **Extraction** – take English ConceptNet subsets covering relations used in CommonsenseQA (Causes, CapableOf, AtLocation, etc.).
2. **MT to target language** – use Marian-NMT base models; back-translate for quality estimation.
3. **Target-side completion** – follow Japanese work: run mT5 inference to propose missing tail entities in the target language.
4. **Label-free adversarial validation** – apply language-agnostic discriminator to filter triples (93.7 % precision@1 across 16 LRLs; **learning #5**).
5. **Human QC spot-checks** – 1 % sample reviewed via Prolific crowd workers.

Expected yield ≈ 120 k triples per language (Amharic slightly lower due to script MT quality).


## 6  Prompt Engineering Patterns
We catalogue reusable templates, grounded in **half-order-of-magnitude reasoning granularity** (learning #11):

```
You are answering in <LANG>. Assume the following commonsense facts:
1. <h> is typically 3–4× larger than <l>.
2. People carry umbrellas when it rains.
...
Question: <Q>
Answer in one short sentence.
```

Prompts explicitly mark the _language code_ to avoid English fallback. When triplets are lacking, we inject **pseudo-CSK** based on Gordon–Hobbs handcrafted categories (learning #7) to maintain structure.


## 7  Evaluation Suite
| Category | Benchmark | Metric | Languages |
|----------|-----------|--------|-----------|
| **Commonsense QA** | TG-CSR few-shot | Accuracy; Macro-F1 | AYSN (translated) + EN pivot |
| | CommonsenseQA-Trans | Accuracy | EN, AYSN |
| **NER** | WikiAnn | F1 | AYSN |
| | CrossNER (Odia→LRL subset) | F1 | si, ne |
| **MT** | Flores-200 | COMET-22; Hallucination rate | EN↔AYSN |
| **KG Probing** | Wikidata-CS subset | Hits@1 | AYSN |
| **Geo-culture** | GeoMLAMA (extended) | P@1 | hi proxy + AYSN |
| **Multimodal (long-term)** | Q-Bench | Visual QA accuracy | si (manual captions) |

GeoMLAMA findings (**learning #6**) caution we must probe _in both native and English text_; we thus generate bilingual prompts.


## 8  Experimental Design
### 8.1  Systems Compared
1. **mLLM-Base** – XLM-R-L or mT5-Large, no CSK.
2. **+ICP-CSK** – retrieval-augmented prompts.
3. **+Prefix-CSK** – prefix-tuned only.
4. **+MAD-X (Lang + Task) + ICP** – our modular stack.
5. **+KEAR** – extern attention reading CSK memory.
6. **Oracle Upper Bound** – full fine-tune with gold CSK (resource-unrealistic).

### 8.2  Compute Budget
* Training: single 8-GPU A100 node, 3 days.
* Inference: ≤3× base FLOPs due to retrieval/prefix.
* Storage: CSK index <4 GB/language.

### 8.3  Hypotheses
H1: Prefix-tuning w/ CSK yields ≥ +7 accuracy points on TG-CSR-AYSN over baseline.
H2: Commonsense-aware NER improves boundary decisions, +1.5 F1, mirroring MAD-X gains.
H3: MT hallucination rate drops 20 % when prompts add plausible world knowledge.


## 9  Advanced / Contrarian Ideas
1. **Graph-Completion-Aided Retrieval** – leverage GCN+PLM link-prediction model (**learning #9**) to _generate_ absent triples on-the-fly for very rare LRL entities.
2. **Cross-Lingual Chain-of-Thought** – ask the model to reason in English (higher CS coverage) but answer in the target language; GeoMLAMA suggests non-native language may surface deeper knowledge.
3. **Multimodal Bootstrapping** – Q-Bench trend implies aligning images with CSK. For example, annotate object affordances in local scripts; could improve physical commonsense.
4. **Prefix Distillation from Prompts** – iterative algorithm: (i) brute-force random CSK prompts, (ii) score downstream val set, (iii) use LoRA to regress context activations, producing **compressed prefixes** (speculation flag).


## 10  Risk Analysis and Mitigations
| Risk | Impact | Mitigation |
|------|--------|-----------|
| MT noise corrupts CSK | Wrong reasoning | Use adversarial validation; 1 % human check |
| Parameter-efficient methods still over-fit tiny LRL data | Poor generalisation | Prefix-tuning proven to mitigate over-fit (**learning #1**); keep validation adversarial |
| Cultural bias in ConceptNet | Offends users | Inject Geo-specific prompts; fine-tune with local corpora |
| License incompatibility | Legal | All resources (ConceptNet, Wikidata) are CC BY-SA-compatible |


## 11  Projected Timeline
1. **Month 0–1**  Build CSK translation pipeline (AYSN 120 k triples each).
2. **Month 2**  Implement ICP retrieval; run baseline → +ICP.
3. **Month 3**  Train prefix-tuned models; evaluate; ablation study.
4. **Month 4**  MAD-X adapter integration + KEAR optional.
5. **Month 5**  Write paper; release AYSN-CSK dataset.


## 12  Anticipated Outcomes and Contributions
* **AYSN Commonsense KB** – first public CSK graphs for Amharic, Yoruba, Sinhala, Nepali (>100 k triples each).
* **Empirical evidence** that **prompt-level CSK integration can rival full fine-tuning** for LRL reasoning, echoing prefix-tuning findings.
* A modular **open-source toolkit**: CSK retrieval, prompt templates, prefix distiller.
* Benchmarks (translated TG-CSR, GeoMLAMA-AYSN) to spur further work.


## 13  Conclusion
Combining **cross-lingual knowledge projection** with **parameter-efficient CSK injection (prefix-tuning, MAD-X, KEAR)** offers a cost-effective path to endow multilingual LLMs with richer commonsense in low-resource settings. The pipeline respects compute constraints, exploits existing high-precision validation techniques, and aligns with emerging multimodal trends. We expect meaningful gains across reasoning, NER, and MT tasks, forging a scalable template for future language coverage expansion.

---

_Contact: research@ay-commonsense.org | Code: github.com/ay-cs/prompt-csk_


## Sources

- https://ojs.aaai.org/index.php/AAAI/article/view/16793
- http://arxiv.org/abs/2112.03254
- http://arxiv.org/abs/2203.12184
- https://pub.uni-bielefeld.de/record/2951681
- https://biblio.ugent.be/publication/8756694
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.69.1452
- https://ojs.aaai.org/index.php/AAAI/article/view/5684
- https://hal.archives-ouvertes.fr/hal-01704457
- https://zenodo.org/record/3983030
- https://ojs.aaai.org/index.php/AAAI/article/view/11575
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.264
- http://hdl.handle.net/10.6084/m9.figshare.7258493.v2
- http://arxiv.org/abs/2203.09424
- https://www.repository.cam.ac.uk/handle/1810/315104
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.95.4216
- https://zenodo.org/record/3401897
- http://researchweb.iiit.ac.in/%7Eriyaz.bhat/Publications/hindiParsingWordnet.pdf
- http://anthology.aclweb.org/W/W14/W14-0114.pdf
- http://users.ics.forth.gr/%7Ekstef/docs/infsys11.pdf
- https://eprints.lancs.ac.uk/id/eprint/210068/
- https://doi.org/10.21979/N9/M41ERD
- http://hdl.handle.net/10379/16376
- http://students.depaul.edu/%7Eyzheng8/papers/Abstract_Talk_DePaul_2012_Differential_Context_Relaxation.pdf
- http://hdl.handle.net/2097/9951
- https://hdl.handle.net/1871.1/731fceb3-bf78-4492-b000-8187586525fb
- http://resolver.tudelft.nl/uuid:01a8584a-49e2-40f2-8591-75e15f9f96a7
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.81.7447
- http://hdl.handle.net/2115/63621
- http://www.mt-archive.info/MTS-2007-Singh.pdf
- https://zenodo.org/record/7140773
- http://hdl.handle.net/1802/11358
- http://arxiv.org/abs/2205.12247
- http://www.elsnet.org/mt2010/probst.pdf
- https://zenodo.org/record/7908824
- https://hdl.handle.net/11250/2830527
- https://journal.astanait.edu.kz/index.php/ojs/article/view/405
- https://zenodo.org/record/5089560
- http://hdl.handle.net/11311/553654
- http://www.planet-data.eu/sites/default/files/PD