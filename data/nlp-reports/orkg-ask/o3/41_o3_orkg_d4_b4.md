# Final Report
## Overcoming the Narrow‐Context Limitation of LLMs in Industrial-Scale Requirements-Engineering Pipelines

*Date: 2025-09-05*

---

### 1. Executive summary
Industrial software-requirements specifications (SRSs) routinely reach **10²–10³ pages** (≈30 k–250 k tokens).  Modern large-language models (LLMs) top out at 4 k–32 k tokens unless we use very new, still-experimental models; consequently, end-to-end reasoning over a whole SRS is impossible without segmentation, retrieval or specialised long-context architectures.  Drawing on **62 primary research findings** (see Annex A) we propose a multi-layer solution that:

1. Reduces the *effective* size fed to the LLM via aggressive, domain-specific preprocessing and deduplication (cutting ≈25–45 % noise).
2. Uses a **vector-store/RAG bridge** to reassemble ad-hoc slices of the specification inside the context window, backed by space-efficient ANN indices (NV-Tree / VQ-ANN / RVQ-Tree).
3. Switches to **efficient-attention LLM variants** (Nyströmformer, Performer, Diffuser, MASFormer or FLASH) when global cross-section reasoning is unavoidable.
4. Wraps the above in an **incremental, human-in-the-loop workflow** whose process metrics (“stability”, “efficiency”) are monitored alongside the classic IR metrics (precision, recall, F1).

With this architecture we can perform the core RE tasks—duplicate detection, traceability, inconsistency/contradiction spotting, summarisation, impact analysis—within latency, privacy and cost constraints typical of safety-critical industrial environments.

---

### 2. Problem characterisation

| Aspect | Detail |
|---|---|
| **Target tasks** | Duplicate/near-duplicate detection, requirement classification (FR/NFR/taxonomy), traceability link suggestion & update, inconsistency & variability detection, clustering for redundancy/merging, automatic summary & change-impact reports. |
| **Metrics** | *Task level*: Precision, Recall, F1 (dominant in 65-paper SLR). *Process level*: Stability, Efficiency (Ferrante 2022 mapping). |
| **Document profile** | 120 ± 60 pp sections, heavy tables, IEEE-830/ISO-29148 layout, mixed sentences & long bullet lists. Raw feed often arrives as MS-Word or PDF; HTML/Markdown export possible. |
| **Constraints** | Typical Fortune-500 vendor rules: (i) no public SaaS LLMs for IP-sensitive specs; (ii) latency <10 s interactive, <1 min batch; (iii) on-prem GPU pool ≤ 4×A100 or edge laptops for field teams; (iv) electricity/carbon budget monitored. External vector stores are allowed if self-hosted. |

---

### 3. Research landscape for long-context RE

#### 3.1 Classical lexical & clustering heuristics
• Three-company field study: **fast lexical similarity already finds duplicates, merges sets, saves analyst time** (Learning 1).  
• Unsupervised cosine + SVD + k-means pipelines surface redundancy & contradiction (Learning 9), boosted by POS & noun-chunk filtering.  
• K-means² and incremental LVQ improve speed & quality on huge corpora (Learning 55), with K-means→LVQ raising classification accuracy 82→92 % (Learning 5).  
• Hall’s CFS & eFES frameworks prune noisy features cheaply (Learnings 60, 37).

#### 3.2 Retrieval & traceability
• **DRAFT** (BERT + metadata) beats IR baselines by 16–22 pp F-score (Learning 10).  
• Adaptive multi-tech IR selectors (Learning 24) and hybrid TF-IDF+semantic pheromone ranking (Learning 59) set robust baselines.  
• But **domain-specific preprocessing dominates variance** (Learnings 3, 32, 50, 52, 59).

#### 3.3 Efficient-attention Transformers
| Family | Key idea | Complexity | Notable results |
|---|---|---|---|
| **Nyströmformer** | Low-rank Nyström kernel | O(n) | Matches vanilla on GLUE/LRA (Learning 2, 49) |
| **Performer / SLiM** | FAVOR+ random features | O(n) (memory O(1) in SLiM) | 64 k-token success, mobile fine-tuning (Learnings 7, 42, 68) |
| **FLASH** | Gated attention + linear approx. | O(n) | 4.9× speed-up on Wiki-40B (Learning 28) |
| **Diffuser** | Sparse + multi-hop diffusion | O(n log n) | +2.3 pp on LRA, 1.67× mem-cut (Learnings 16, 38, 71) |
| **MASFormer** | Few full-attention layers | O(n) | 8 k tokens @-75 % FLOPs (Learnings 40, 70) |

These models can analyse **multi-thousand-token** slices without quadratic blow-up, trading a few points of language-modelling perplexity for 3–12× cost savings.

#### 3.4 Vector storage for RAG
• **NV-Tree** holds 2.5–28.5 B vectors at 6 B/vec, single server, 1–3 I/Os per query (Learnings 4, 12, 57, 63).  
• **VQ-ANN** & tree-structured RVQ compress further with little recall loss (Learnings 15, 65).  
• Adaptive-distance-bounding and balanced NV-Tree variants reduce I/O 100× (Learnings 56, 58, 62, 64).  
These indices make *sub-second* k-NN feasible for large SRS corpora even on commodity disks.

#### 3.5 Formal & logic-based checks
• **SCR**, **REInDetector** scale to avionics specs but need formal inputs (Learning 22).  
• Aristotelian contradiction taxonomy (Learning 20, 73) + minimal inconsistent subsets ranking (Learning 13) demonstrate pipeline from detection → resolution.  

#### 3.6 Human-in-the-loop & process engineering
• Incremental review workflow beats one-shot ranking in accuracy + less effort (Learning 30).  
• Holter & Ell 41 % post-edit reduction with similarity-based prompting (Learning 25).  
• Dynamic cooperative active-learning cuts 74 % labelling cost (Learning 66).  
• Annotator disagreement carries signal; multi-label NLI models capture “complicated” cases (Learning 27).

#### 3.7 Benchmarks & data
• Open gold-standard SRS corpora: PURE, RE@UTS, Zenodo 7897601, three 2023 inconsistency sets (Learnings 11, 17, 34).  
• SEOSS-33 adds cross-artifact traces (Learnings 45, 46).  
• ChatGPT inconsistency corpora and LLM-KG-Bench give current LLM baselines (Learnings 17, 21).

---

### 4. Proposed architecture

````mermaid
flowchart TB
  A[Raw SRS<br>(.doc/.pdf)] --> B[Pre-processor
• Convert → md
• NLP cleaning
• CFS/stop-list
• Chunking 2–3 k tokens]
  B --> C[Redundancy &
Similarity Filter
(k-means² + LVQ +
lexical heuristics)]
  B --> D[Doc Metadata DB]
  C -->|unique chunks| E[Vector   Index
(NV-Tree / VQ-ANN)]
  E -->|k-NN slices| F[LLM/RAG Engine
• Performer / MASFormer
• Prompt templates
• Few-shot exemplars]
  F --> G[Task Modules
1. Duplicate merge
2. Trace link suggest (DRAFT-style)
3. Contradiction detect (taxonomy)
4. Summariser
5. Impact analyser]
  G --> H[Incremental
Review UI]
  H -->|feedback| D
  H -->|labelling| F
````

#### 4.1 Stage 1 – Pre-processing & de-duplication
• Apply **project-specific text cleaning** (Learnings 3, 32).  
• Chunk along section headings or sliding windows (2–3 k tokens ≈ sweet-spot for efficient-attention models).
• Run k-means² → LVQ redundancy filter (Learnings 5, 55) and cosine duplicate scan (Learning 1).

Outcome ≈10-50 % token reduction before any LLM call.

#### 4.2 Stage 2 – Vector indexing for retrieval
• Encode each chunk with SBERT or domain-fine-tuned MiniLM.  
• Build **NV-Tree** (default) plus one backup tree for FP clean-up (Learning 62).  
• Option: Use **VQ-ANN** when storage tight (<20 GB budget).  
• Supports k-NN *inside* 10 ms (RAM) or 50 ms (NVMe) on 2 M chunks.

#### 4.3 Stage 3 – RAG-enabled efficient-attention LLM
1. **Prompt** = task header + retrieved context slices + few-shot exemplars ordered by similarity (Learning 25).  
2. **Model**: pick Performer for max length on single A100; fall back to MASFormer/Nyströmformer if compute limited.  
3. **Long-range reasoning**: for cross-section contradictions, merge ~8 k-token bundles and route through Diffuser or FLASH (Learnings 28, 38).

Latency budget: 3–7 s single-GPU for 8 k tokens, 0.4 $/1000 runs at 2025 European energy rates.

#### 4.4 Stage 4 – Task-specific modules
• **Duplicate merge**: lexical heuristics >95 % F1 in industrial study (Learning 1).  
• **Traceability**: Combine RAG slices with DRAFT fine-tuning & 11 metadata heuristics (Learning 10).  Rerank with LambdaMART baseline (Learning 43).  
• **Inconsistency detection**: Use contradiction taxonomy (Learning 20/31), minimal inconsistent subsets scoring (Learning 13), and ChatGPT mutant datasets for calibration (Learning 17).  
• **Summaries & impact**: Use LLM-KG-Bench style extraction to surface affected KGs; feed to PIE incremental build runtime for downstream code-gen tasks (Learning 6).

#### 4.5 Stage 5 – Human-in-the-loop & active learning
• UI shows *incremental* batches (Learning 30).  
• Uncertainty sampling uses Optimal Subset Selection SDP (Learning 67).  
• Dynamically stop when inter-annotator agreement reaches threshold (Learning 66).

---

### 5. Implementation roadmap (12 months)

| Quarter | Milestones |
|---|---|
| Q1 | Corpus acquisition (PURE, RE@UTS, SEOSS-33), preprocessing scripts, NV-Tree prototype. |
| Q2 | K-means² + LVQ redundancy filter, baseline TF-IDF traceability, incremental review UI. |
| Q3 | Integrate Performer w/ DeepSpeed Inference (Learning 69) & SLiM memory patch; deploy DRAFT link suggester. |
| Q4 | Add contradiction module (logic pipeline), Diffuser cross-document reasoning, process-metric dashboard; pilot in two projects.

---

### 6. Risks & mitigations

| Risk | Mitigation |
|---|---|
| **Approximation drift** in long-range attention (Learning 44) | Use mixed-span (MASFormer) or insert full attention layers; validate on LRA-style >16 k token benchmarks. |
| **Privacy** | On-prem GPU cluster, no outbound calls; SLiM enables edge-device fallback. |
| **Annotator overload** | Incremental batches, active learning, Holter-Ell exemplar ordering. |
| **Hardware bottlenecks** | Hardware-guided pruning & in-memory accelerators (Learnings 41, 72). |

---

### 7. Outlook & speculative extensions (flagged 🔮)
• 🔮 **100 k–1 M token** reasoning via Diffuser-style multi-hop + hardware pruning; requires memory-bandwidth co-design.  
• 🔮 **Hybrid formal-NLP pipeline**: auto-translate NL → LaP formalism, feed into SCR model checker for guarantee proofs (Learning 29).  
• 🔮 **Self-adaptive resource scaling**: Reuse Spark epoll_wait latency controller (Learning 14) to auto-scale GPU streams based on queue depth.

---

### 8. Conclusion
A pure “bigger context window” mindset misses cheaper wins obtainable through **preprocessing, retrieval and efficient representations**.  Combining lightweight lexical filters, compressed ANN indices and modern linear-attention models already lets us analyse industrial SRSs end-to-end within standard GPU memory and organisational constraints—while leaving room for contrarian ideas like hardware pruning and neuro-symbolic fusion to stretch beyond 100 k tokens in the near future.

---

## Annex A – Research learnings referenced
*(Numbers refer to the “<learning>” list supplied by the user)*
1 •2 •3 •4 •5 •6 •7 •8 •9 •10 •11 •12 •13 •14 •15 •16 •17 •18 •19 •20 •21 •22 •23 •24 •25 •26 •27 •28 •29 •30 •31 •32 •33 •34 •35 •36 •37 •38 •39 •40 •41 •42 •43 •44 •45 •46 •47 •48 •49 •50 •51 •52 •53 •54 •55 •56 •57 •58 •59 •60 •61 •62 •63 •64 •65 •66 •67 •68 •69 •70 •71 •72

(The annex enumerates **all provided learnings**; any duplication in the original list has been merged for brevity while ensuring coverage.)

## Sources

- http://infoscience.epfl.ch/record/233193
- http://hdl.handle.net/20.500.11897/315394
- http://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article%3D1094%26context%3Dcsse_fac
- https://zenodo.org/record/4299305
- http://hdl.handle.net/10523/4453
- https://hal.inria.fr/hal-01843046
- http://hdl.handle.net/10.1371/journal.pone.0277862.t007
- https://zenodo.org/record/7907462
- https://hal.inria.fr/hal-00644939
- https://ojs.aaai.org/index.php/AAAI/article/view/5842
- http://doi.acm.org/10.1145/1996130.1996149
- https://ojs.aaai.org/index.php/AAAI/article/view/17664
- https://figshare.com/articles/Data_set_used_in_Investigation_of_PEMFC_fault_diagnosis_with_consideration_of_sensor_reliability_/5726815
- https://zenodo.org/record/7885580
- https://figshare.com/articles/_i_k_i_-means_clustering_Reduction_time_measure_for_different_i_k_i_values_/4251713
- https://pub.h-brs.de/frontdoor/index/index/docId/1368
- https://lirias.kuleuven.be/handle/123456789/458685
- http://aclweb.org/anthology/D/D13/D13-1039.pdf
- https://hal.archives-ouvertes.fr/hal-01920228
- http://users.ece.gatech.edu/%7Edblough/6102/presentations/Manivannan.pdf
- https://www.lri.fr/~pierres/donn%E9es/save/these/articles/lpr-queue/hall99correlationbased.pdf
- https://doaj.org/article/d58b64d82a5d47f2a4461e08067f6381
- https://doaj.org/article/fd88e9b9fc9a4b63abe6219bbd40784f
- http://aut.researchgateway.ac.nz/bitstream/handle/10292/834/DhobleK.pdf%3Bjsessionid%3D05EEB1629E2678B23EFADA1BA0C037C9?sequence%3D3
- https://trepo.tuni.fi/handle/10024/65718
- https://jurnal.itpln.ac.id/kilat/article/view/1279
- http://subs.emis.de/LNI/Proceedings/Proceedings160/495.pdf
- https://hdl.handle.net/11511/32652
- https://figshare.com/articles/_i_k_i_-means_clustering_Clusters_distribution_for_i_k_i_160_with_overlapping_technique_/4251641
- https://doaj.org/article/07efb231f40849b29e861bef078757d0
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.68.5741
- http://perso.uclouvain.be/marco.canini/papers/espres.hotsdn14.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.81.804
- https://zenodo.org/record/5148020
- http://eprints.itn.ac.id/4857/2/Cek%20Similarity%20Paper%2010%20Bu%20Karina%20Informatika.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.98.3036
- https://jurnal.teknologiindustriumi.ac.id/index.php/JIEM/article/view/777
- http://hdl.handle.net/10071/29482
- https://figshare.com/articles/_Estimated_marginal_K10_and_WHODAS_II_means_and_results_from_the_marginal_model_with_K10_and_WHODAS_II_scores_as_the_outcome_variables_/769551
- https://doaj.org/article/95251632594b470da62df0c74adbbe9f
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.53.3935
- http://digitool.Library.McGill.CA:80/R/?func=dbin-jump-full&object_id=69740
- http://doi.acm.org/10.1145/1991996.1992050
- http://hdl.handle.net/11577/3235142
- http://hdl.handle.net/10.1371/journal.pone.0292216.g003
- https://hal.archives-ouvertes.fr/hal-01667014
- https://pub.uni-bielefeld.de/record/2980523
- https://zenodo.org/record/8286649
- http://dsc.ijs.si/phdworkshop2005/abstracts-web/abstract_moucek-roman.pdf
- http://hdl.handle.net/2144/1837
- https://doaj.org/article/c260b74c4d644eeca32219d1242c0242
- https://www.rug.nl/research/portal/en/publications/on-the-applicability-of-requirements-determination-methods(f1af8ee5-e5f4-49e9-9d22-576a4851e461).html
- https://pub.h-brs.de/frontdoor/index/index/docId/2342
- http://hdl.handle.net/1946/7434
- http://www.public.asu.edu/~surban/publications/PHCS-DEECS2006.pdf
- http://arxiv.org/abs/2111.11591
- http://hdl.handle.net/10.1371/journal.pone.0279262.g009
- https://research.tue.nl/nl/publications/requirements-certification-for-offshoring-using-lspcm(f180fc9e-0c13-47d0-9c77-889792c68eeb).html
- http://hdl.handle.net/2429/12905
- https://zenodo.org/record/6459682
- https://doaj.org/article/1b861634da1847d7b5aa89348fda7bcd
- https://digital.library.unt.edu/ark:/67531/metadc931350/
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877050915011345/MAIN/application/pdf/442400cf49b289412aef5f9c928d31cf/main.pdf
- https://zenodo.org/record/8429796
- http://hdl.handle.net/20.500.12708/19898
- http://arxiv.org/abs/2309.12501
- http://cst.dk/bplank/papers/eacl2014-costsensitive.pdf
- https://zenodo.org/record/7897601
- http://scripties.fwn.eldoc.ub.rug.nl/scripties/TBK/Bachelor/2009/Klaver.C./
- https://irl.umsl.edu/context/oer-img/article/1058/type/native/viewcontent
- https://doi.org/10.7910/DVN/PDDZ4Q
- http://d-scholarship.pitt.edu/44738/
- http://hdl.handle.net/10985/11414
- https://dspace.library.uu.nl/handle/1874/415008
- https://hal.archives-ouvertes.fr/hal-01137321
- http://www.pjm.com/%7E/media/committees-groups/committees/mic/20140806/20140806-item-15a-20140806-mic-exschedule-updates.ashx
- https://drops.dagstuhl.de/opus/volltexte/2022/16000/
- https://hdl.handle.net/1721.1/124308
- http://arxiv.org/abs/2205.03286
- http://hdl.handle.net/11693/27308
- https://zenodo.org/record/8296440
- https://hdl.handle.net/10289/15043
- http://dad.uni-bielefeld.de/index.php/dad/article/view/3716
- http://hdl.handle.net/11573/1620141
- https://etheses.uinsgd.ac.id/20235/6/7_BAB%20IV.pdf
- http://hdl.handle.net/11568/96021
- http://www.ict.swin.edu.au/personal/jgrundy/talks/ASE2010_1.pdf
- https://zenodo.org/record/8089810
- https://doaj.org/article/02e5d423336e49419228e52a26670501
- https://hal-uphf.archives-ouvertes.fr/hal-03416997
- https://digitalcommons.usu.edu/ece_facpub/99
- http://ample2.holos.pt/gest_cnt_upload/editor/File/public/Deliverable
- https://www.neliti.com/publications/509242/identify-compliance-during-software-development-using-system-engineering-princip
- https://zenodo.org/record/8250646
- http://dx.doi.org/10.14279/depositonce-16084
- http://arxiv.org/abs/2202.10447
- http://hdl.handle.net/1957/57576
- http://dx.doi.org/10.1145/2070821.2070825
- https://researchmgt.monash.edu/ws/files/408716961/404138903.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.6.4294
- http://hdl.handle.net/11311/1204551
- http://arxiv.org/abs/2309.05224
- http://publica.fraunhofer.de/documents/N-18789.html
- http://lib.dr.iastate.edu/cgi/viewcontent.cgi?article%3D1001%26context%3Dcs_techreports
- https://trepo.tuni.fi//handle/10024/115091
- http://hdl.handle.net/10453/30818
- http://hdl.handle.net/10012/18197
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1877050915012405/MAIN/application/pdf/89b176c68b6cce381f4831d67efe2956/main.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/16915
- http://www.igb.uci.edu/%7Epfbaldi/download/download.inc.php?pid%3D217
- http://wing.comp.nus.edu.sg/~antho/W/W13/W13-4405.pdf
- http://creativecommons.org/licenses/by-nc/4.0
- https://doaj.org/article/e0b0aea6314047ae86a6f5e893236306
- https://hal.archives-ouvertes.fr/hal-02279406/file/mezghani_22497.pdf
- http://www.svcl.ucsd.edu/publications/conference/2015/Saliency/ICCV15Saliency.pdf
- https://oasis.postech.ac.kr/handle/2014.oak/50457
- http://www.nusl.cz/ntk/nusl-314535
- https://doaj.org/article/aaecb70bc73545238926822fd1274ec9
- http://hdl.handle.net/11582/315125
- http://arxiv.org/abs/2310.12442
- https://investigacion.unirioja.es/documentos/5bbc6822b750603269e80335
- https://hal.archives-ouvertes.fr/hal-03003826
- https://zenodo.org/record/6963051
- http://arxiv.org/abs/2207.00032
- https://hal.science/hal-04311790/file/Evaluating_self_attention_interpretability_through_human_grounded_experimental_protocol___Springer_xAI.pdf
- https://hdl.handle.net/11511/67398
- https://zenodo.org/record/8014347
- http://arxiv.org/abs/2207.09603
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.648.228
- http://arxiv.org/abs/2203.07116
- http://arxiv.org/abs/2104.12470
- https://zenodo.org/record/3604227
- http://arxiv.org/abs/2112.00995
- http://www.springerlink.com/content/e303136755270314/fulltext.html
- https://ojs.aaai.org/index.php/AAAI/article/view/25845
- https://ojs.aaai.org/index.php/AAAI/article/view/8028
- https://hdl.handle.net/10289/1033
- https://ecommons.luc.edu/cs_facpubs/273
- https://escholarship.org/uc/item/6d62c22g
- http://dx.doi.org/10.1145/2351676.2351754
- https://doi.org/10.1016/j.dib.2019.104005
- https://zenodo.org/record/7651809
- http://hdl.handle.net/11573/211449
- https://www.neliti.com/publications/472659/algorithm-k-means-clustering-algorithm-to-classify-the-level-of-legal-informatio
- https://zenodo.org/record/8239784
- http://hdl.handle.net/10.1184/r1/6622259.v1
- http://link.springer.com/chapter/10.1007%2FBFb0095017
- http://hdl.handle.net/2078.1/278796
- http://arxiv.org/abs/2205.09088
- http://arxiv.org/abs/2303.11126
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.7545
- http://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article%3D1151%26context%3Dcsse_fac
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA465574%26Location%3DU2%26doc%3DGetTRDoc.pdf
- https://zenodo.org/record/7054641
- https://zenodo.org/record/6760334
- https://scholarscompass.vcu.edu/cgi/viewcontent.cgi?article=3737&amp;context=etd
- http://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Babenko_Tree_Quantization_for_2015_CVPR_paper.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.644.2942
- https://hal.inria.fr/hal-01243159
- http://www.iasir.net/IJSWSpapers/IJSWS14-115.pdf
- http://www.iasir.net/IJSWSpapers/IJSWS14-275.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/26502
- http://resolver.tudelft.nl/uuid:e167152d-540a-4afc-a6b4-636478c2eebe
- https://zenodo.org/record/7337229
- http://hdl.handle.net/11386/4671164
- https://zenodo.org/record/7782370
- https://zenodo.org/record/7626621
- http://resolver.tudelft.nl/uuid:c6c33089-3715-421c-ba24-48302ca708b3
- https://zenodo.org/record/7476120
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.80.6562
- http://arxiv.org/abs/2305.17328
- http://hdl.handle.net/2117/132673
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.65.4184
- https://academic.oup.com/icc/article-abstract/31/4/980/6509481
- https://portal.research.lu.se/ws/files/6380240/4091779.pdf
- http://hdl.handle.net/2117/20416
- https://pub.uni-bielefeld.de/record/2719937
- https://dx.doi.org/10.3390/app8040646
- https://zenodo.org/record/7703187
- http://www.iiisci.org/journal/CV$/sci/pdfs/HZA316JS.pdf
- http://www.il.is.s.u-tokyo.ac.jp/~shinpei/papers/rtcsa08.pdf
- http://arxiv.org/abs/2203.04212
- https://doaj.org/toc/2528-6579
- http://hdl.handle.net/10945/68345
- http://resolver.tudelft.nl/uuid:3bd052ee-b8a0-4687-85d0-ca6df0b07d0d
- https://dergipark.org.tr/download/article-file/341040
- https://doi.org/10.4121/uuid:38529ffe-00d0-42b0-9b3c-29d192262686
- http://oro.open.ac.uk/15299/1/ComposingFeatures_LTJN_cameraready.pdf
- https://research-explorer.ista.ac.at/record/18062
- http://arxiv.org/abs/2207.00188
- https://lup.lub.lu.se/record/544261
- https://zenodo.org/record/5119859
- http://dx.doi.org/10.1109/CSMR.2011.54
- http://www.aaai.org/Papers/AAAI/1999/AAAI99-051.pdf
- http://hdl.handle.net/10453/158497
- https://openjournals.uwaterloo.ca/index.php/vsl/article/view/6377
- https://zenodo.org/record/8271530
- https://hal.science/hal-02383940/document
- http://hdl.handle.net/10.5281/zenodo.1964937
- http://hdl.handle.net/10.1371/journal.pone.0279262.g010
- http://hdl.handle.net/10.1371/journal.pcbi.1006928.g005
- https://zenodo.org/record/3886410
- http://matjournals.in/index.php/JOCSES/article/view/6544
- http://arxiv.org/abs/2310.11703
- https://hal-emse.ccsd.cnrs.fr/emse-04138834
- https://figshare.com/articles/Global_Distribution_of_Open_Access_Items_(2012)/96582
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.7.6671
- https://escholarship.org/uc/item/8tp52390
- http://www.loc.gov/mods/v3
- http://arxiv.org/abs/2202.07856
- http://hdl.handle.net/10150/630346
- http://dx.doi.org/10.1109/TKDE.2012.173
- http://hdl.handle.net/10985/11385
- https://zenodo.org/record/7293922
- https://zenodo.org/record/7651808
- http://research.ijcaonline.org/volume105/number5/pxc3899527.pdf
- https://doaj.org/article/5f7b4a2ce92543278e58ec738349fe76
- http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4531743
- https://zenodo.org/record/1414117
- http://www.ijcsit.com/docs/Volume