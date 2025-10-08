# Final Report on Stepwise Uncertainty Estimation in Chain-of-thought Reasoning

This report provides an in-depth analysis of the emerging topic of stepwise uncertainty estimation within chain-of-thought (CoT) reasoning frameworks. Drawing upon a diverse body of research that spans hybrid symbolic-numerical methods, neurosymbolic integration, probabilistic logics, and high-performance computing, we critically examine the nuances of estimating uncertainty at each reasoning step versus adopting integrated, holistic metrics. The report is organized into several sections, including background and definitions, methodological approaches, hybrid frameworks, real-world applications, computational trade-offs, challenges, and future directions.

---

## 1. Introduction and Background

Chain-of-thought reasoning involves decomposing complex problem solving into a sequence of intermediate reasoning steps. This approach is particularly prominent in modern large language models and decision support systems, where the ability to transparently document the reasoning process enables enhanced interpretability and trust. However, with increasing reliance on sequential reasoning in AI, addressing both propagation and accumulation of uncertainty has become critical, especially when such systems are deployed in safety-critical domains such as robotics, healthcare, and autonomous systems.

This report addresses two intertwined queries: First, what constitutes "stepwise uncertainty estimation"? Specifically, does it denote the quantification of uncertainty at each individual reasoning step in a chain-of-thought, or does it refer to an integrated metric computed over the full reasoning chain? Second, is the uncertainty estimation confined to the domain of language models and CoT reasoning, or is it equally applicable in other algorithmic frameworks and decision-making contexts? The subsequent analysis is guided by these questions and underpinned by comprehensive research findings.

---

## 2. Defining Stepwise versus Integrated Uncertainty Estimation

### 2.1 Stepwise Uncertainty Estimation

In the stepwise paradigm, uncertainty is quantified at each individual reasoning step. This approach is analogous to sequential methods where uncertainty—whether from data noise (aleatoric) or model imperfections (epistemic)—is assessed incrementally. This methodology has several attractive properties:

- **Granularity:** It allows for fine-grained analysis, pinpointing the exact moment when uncertainty spikes. This is particularly valuable in dynamic and high-stakes applications where real-time decision signals are crucial.

- **Interpretability:** For chain-of-thought models, explicit uncertainty values for each reasoning step can provide insights into the model’s intermediate inferences, which in turn supports debugging and refinement.

- **Adaptive Decision-Making:** By isolating uncertain steps, systems can deploy intervention strategies (e.g., invoking additional computational resources or expert oversight) precisely where needed.

However, sequential stepwise estimation can be computationally intensive, as it necessitates the evaluation of uncertainty propagation across multiple layers of inference. Advanced caching strategies (e.g., ff Γ caching) and efficient pruning mechanisms become crucial, as noted in several studies addressing the combinatorial explosion inherent in dynamic symbolic reasoning.

### 2.2 Integrated Uncertainty Estimation

Alternately, integrated uncertainty estimation seeks to capture the total, cumulative uncertainty associated with the full chain-of-thought. This approach is informed by the concept of Total Uncertainty, which aggregates both aleatoric and epistemic components into a single metric. The integrated method offers these advantages:

- **Holistic Evaluation:** An integrated metric may more directly inform decision confidence by reflecting interactions between individual uncertainties at different reasoning steps.

- **Computational Efficiency:** While granular control is compromised, integrated metrics can reduce the computational overhead by summarizing uncertainty in a single pass, thus benefiting scenarios where rapid inference is essential.

- **Robust Control Mechanisms:** In fields such as engineering decisions and risk assessment, total uncertainty metrics have been deployed to regulate decision processes through criteria that combine mathematical soundness with computational tractability.

Both approaches have their merits and demerits. The tension between granularity and computational efficiency underscores the need for hybrid strategies that amalgamate the strengths of stepwise sensitivity analysis with holistic, integrated risk metrics.

---

## 3. Methodological Approaches and Hybrid Frameworks

Recent research has offered an array of methodologies to address uncertainty - spanning probabilistic methods, fuzzy logic, neurosymbolic frameworks, and hybrid belief systems. Below, we highlight several salient methods:

### 3.1 Probabilistic Methods and Bayesian Inference

Numerous studies have integrated Bayesian logic programs, Monte Carlo methods, and even BetaProbLog techniques to quantitatively handle uncertainty. Bayesian frameworks allow for moment-independent assessments which, as documented, are critical when variance alone is insufficient to capture the full output distribution. Extensions such as Multi-Level Monte Carlo have been tailored to high-dimensional scenarios, effectively reallocating computational resources to minimize numerical error.

### 3.2 Symbolic-Numerical Integration

Hybrid frameworks that combine elements of symbolic reasoning (e.g., ATMS and logic programming with Kleene semantics) with numerical methods (e.g., Dempster-Shafer Theory, triangular norm uncertainty calculi) have demonstrated marked success in managing dependent evidence and complex hypothesis spaces. For instance, Baldwin’s Support Logic Programming system leverages such integration to address both aleatoric and epistemic uncertainties in a dynamic, multi-step inference process.

### 3.3 Neurosymbolic and Deep Learning Integrations

Modern uncertainty frameworks increasingly integrate deep learning with symbolic methods. Neurosymbolic platforms, such as those employing Logic Tensor Networks or neural-symbolic approaches in Real-Time BDI (RT-BDI) frameworks, have showcased dramatic improvements in both interpretability and robust reasoning. Empirical evidence (e.g., F1 score enhancements from 0.64 to 0.97) illustrates that combining data-driven weight learning with structured symbolic rules yields superior performance, particularly in tasks requiring chain-of-thought reasoning.

### 3.4 Fuzzy and Linguistic Approaches

Fuzzy logic and graded linguistic models offer an alternative by capturing imprecise and qualitative uncertainties, which are especially useful in natural language processing contexts. Systems adopting many-valued symbolic logics and fuzzy interval analysis have been effective in enhancing the explainability of uncertainty in chain-of-thought processes, although they often face a trade-off between calibration precision and computational overhead.

### 3.5 Hybrid Strategies: Merging Discrete and Continuous Models

Numerous studies underscore the importance of combining the strengths of both stepwise and integrated models. For example, the MIMDU framework extends traditional multi-criteria decision-making by incorporating fuzzy linguistic ratings and confidence assessments across multiple reasoning stages. Similarly, advanced pruning techniques that merge ff Γ caching with symbolic propagation offer promising avenues to tackle the scalability challenges posed by stepwise uncertainty estimation.

---

## 4. Applications and Real-world Examples

The utility of stepwise uncertainty estimation in chain-of-thought reasoning has been validated in various domains:

- **Safety-Critical Systems:** Applications in autonomous vehicles and robotics have used granular uncertainty measurements at each decision node to enhance real-time, safety-aware decision-making. The enhanced engine prognostics in turbofan systems (with prediction horizon improvements near 127%) exemplify how successive uncertainty evaluations contribute to robust system health predictions.

- **Medical Diagnostics and Digital Pathology:** Integrative models that combine deep learning with uncertainty quantified at each diagnostic step have achieved empirical gains—illustrated by improvements in precision (15%), F1 scores (11%), and reductions in negative log likelihood (12%). These outcomes are directly linked to incorporating uncertainty at individual chain-of-thought steps versus relying solely on a final aggregated output.

- **Cognitive Decision Support:** In domains where model complexity and subjective uncertainty play critical roles (for instance, in discrete time/cost trade-off problems), integrated metrics that capture both the overall and stepwise uncertainty serve as pivotal tools. This dual assessment strategy allows analysts to reconcile discrepancies between perceived and actual complexity, thereby optimizing resource allocation.

- **Hybrid Multi-agent Systems:** Research on dynamic normative systems and multi-agent games (e.g., Monopoly and associated hybrid deep RL models) demonstrate how iterative neurosymbolic approaches, through stepwise confidence evaluations, can enhance both system adaptability and performance in unpredictable environments.

Each application highlights unique trade-offs, but a recurring theme across domains is the need for methods that are both computationally efficient and robust in uncertainty quantification. Hardware acceleration (e.g., using NVIDIA A100 GPUs or next-generation platforms like Cerebras CS-2) further enables the real-time deployment of these sophisticated models.

---

## 5. Computational Trade-offs and Challenges

Efficiently managing uncertainty in chain-of-thought models involves balancing multiple computational and methodological challenges:

- **Resource Management and Caching Strategies:** Stepwise evaluation inherently requires frequent re-computation and propagation of uncertainty values. Advanced caching methods (e.g., ff Γ caching) are necessary to mitigate computational overhead, though they may increase memory demands and introduce complexities in cache coherence.

- **High-dimensionality and Sparse Data Issues:** Sequential estimation often grapples with the exponential growth of hypothesis spaces. Techniques such as graph decomposition and scalable Monte Carlo extensions (including multi-index and quasi-Monte Carlo variants) have been successfully employed to counteract these issues.

- **Trade-off between Granularity and Aggregation:** While granular, stepwise uncertainty metrics provide detailed insight into each reasoning step, they also incur significant computational costs. Integrated metrics offer efficiency but may obscure critical step-specific variations. Future frameworks will likely need to adopt hybrid models that integrate both approaches in a layered architecture.

- **Algorithmic Optimizations and Hardware-specific Constraints:** Empirical studies indicate strong performance dependencies on both algorithmic decisions (e.g., evolutionary algorithms like NEMOKD on specialized hardware) and platform characteristics. Balancing latency, memory footprint, and inference accuracy remains an ongoing challenge.

---

## 6. Future Directions and Recommendations

Given the current state of research, several promising avenues merit exploration in the realm of stepwise uncertainty estimation:

1. **Hybrid, Multi-Layered Frameworks:** Development of models that seamlessly integrate stepwise and integrated uncertainty metrics could enable adaptive precision, dynamically switching between detailed and holistic evaluations based on context.

2. **Neurosymbolic Enhancements:** Further research into neurosymbolic systems that couple deep learning with extended symbolic reasoning (e.g., using extended Dempster-Shafer frameworks) will likely yield improvements in both model transparency and dynamic hypothesis space management.

3. **Advanced Sensitivity Analysis:** Incorporating novel statistical measures such as Rényi divergence into Bayesian sensitivity analysis frameworks could provide deeper insights into non-linear interactions and distributional shifts at the intermediate steps of chain-of-thought reasoning.

4. **Optimal Hardware Utilization:** As AI systems increasingly deploy on specialized hardware platforms, tailored algorithmic optimizations and caching strategies that account for platform-specific idiosyncrasies are essential. Collaborative research between algorithm designers and hardware engineers is recommended to unlock further improvements in real-time chain-of-thought implementations.

5. **Cross-Domain Benchmarking:** Given that uncertainty estimation methods are applicable across diverse domains—from aerospace and biomedical applications to dynamic multi-agent systems—establishing standardized benchmarks that evaluate both stepwise and integrated approaches will enhance cross-domain transferability and reproducibility.

6. **Integration of Fuzzy and Probabilistic Methods:** Hybrid approaches that combine fuzzy linguistic models with probabilistic sampling (e.g., using methods like Random/Fuzzy [RaFu] and PUQpy) hold promise in reconciling the differing advantages of qualitative and quantitative uncertainty representation.

---

## 7. Conclusion

Stepwise uncertainty estimation in chain-of-thought reasoning represents an important evolution in the design of transparent, robust AI systems. By enabling fine-grained analysis of uncertainty at each inference step, this approach supports improved decision-making in complex, dynamic environments. However, challenges remain—most notably in balancing computational efficiency with detailed uncertainty representation. The synthesis of probabilistic, symbolic, fuzzy, and neurosymbolic methodologies presents a fertile ground for future research and application.

Overall, reconciling the dual paradigms of stepwise versus integrated uncertainty estimation will likely be central to the next generation of AI models, ensuring that systems are both explainable and highly reliable in real-world, safety-critical settings.

---

This detailed analysis provides a comprehensive overview of available models, the trade-offs involved, and potential strategies to further enhance chain-of-thought reasoning in AI through sophisticated uncertainty estimation methodologies.

## Sources

- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1877050916324772/MAIN/application/pdf/20e6cfffebc4a0758d79ff83f497a15e/main.pdf
- https://resolver.caltech.edu/CaltechAUTHORS:20190816-144341264
- http://gala.gre.ac.uk/id/eprint/6438/1/ISMVL_2009_1_Abstract.pdf
- https://arodes.hes-so.ch/record/6446/files/Author%20postprint.pdf
- https://hal.inrae.fr/hal-02664027
- http://hdl.handle.net/11565/40060
- https://digitalcommons.usf.edu/cgi/viewcontent.cgi?article=10870&amp;context=etd
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.7.3810
- https://repository.upenn.edu/cgi/viewcontent.cgi?article=7224&amp;context=edissertations
- http://hdl.handle.net/11577/2520429
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:0888613X88901181/MAIN/application/pdf/8fd76b93988a7fef8c50cb057e1184e1/main.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.85.3414
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/27701
- http://hdl.handle.net/11311/725973
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.7701
- https://bibliotekanauki.pl/articles/91806
- https://ojs.aaai.org/index.php/aimagazine/article/view/4812
- http://www.ict.csiro.au/staff/Mikhail.Prokopenko/AORC
- https://doi.org/10.1016/j.cirp.2021.04.049
- https://openaccess.city.ac.uk/id/eprint/12696/6/RASensitivity_accepted.pdf
- https://dare.uva.nl/personal/pure/en/publications/neural-networks-penalty-logic-and-optimality-theory(9c98854e-e5d8-4d56-9247-43a8dee785fc).html
- https://zenodo.org/record/4651517
- http://discovery.ucl.ac.uk/1506251/
- http://hdl.handle.net/1822/36777
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-489084
- https://lirias.kuleuven.be/bitstream/123456789/623098/1//slides.pdf
- http://hdl.handle.net/10261/220048
- http://edepot.wur.nl/108077
- http://eprints.iisc.ac.in/53033/1/Str_Saf_58-94_2016.pdf
- https://lup.lub.lu.se/record/4814a197-f7a7-4fb1-920c-e62f50e2d994
- https://escholarship.org/uc/item/5r19480f
- http://www.mdpi.com/books/pdfview/book/624
- https://ojs.aaai.org/index.php/AAAI/article/view/25070
- http://hdl.handle.net/20.500.12127/5493
- https://hal-utt.archives-ouvertes.fr/hal-02365901
- http://resolver.tudelft.nl/uuid:fdc0105c-e601-402a-8f16-ca97e9963592
- http://hdl.rutgers.edu/1782.2/rucore10001600001.ETD.000051885
- www.blackwellpublishers.co.uk/asp/journal.asp?ref=0272-4332
- https://www.fig.net/commission6/lisbon_2008/papers/pas03/pas03_04_neumann_mc083.pdf
- http://publications.jrc.ec.europa.eu/repository/handle/JRC54701
- https://scholarsmine.mst.edu/mec_aereng_facwork/3512
- https://scholarworks.utep.edu/dissertations/AAI1435337
- https://madoc.bib.uni-mannheim.de/46637/
- http://resolver.tudelft.nl/uuid:eb0257b7-6791-49e0-ac2d-3a4c8803b29a
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.43.3016
- https://orca.cardiff.ac.uk/id/eprint/116510/1/manhaeve-nips18.pdf
- http://le.uwpress.org/content/79/4/549.abstract
- https://github.com/topipa/rsens-paper
- http://www2.mta.ac.il/~oarieli/Papers/wollic08.pdf
- https://scholarworks.umass.edu/dissertations/AAI3427492
- http://hdl.handle.net/2117/366503
- http://hdl.handle.net/20.500.11850/506035
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:0888613X93900178/MAIN/application/pdf/4d44b651641ead8929bbd6e18e8bf095/main.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/21245
- https://tud.qucosa.de/id/qucosa%3A82450
- https://cris.maastrichtuniversity.nl/en/publications/282f6fe9-7caa-4660-af9e-1d2bc7021e78
- http://gala.gre.ac.uk/id/eprint/35411/7/35411_RAUSEO_A_systematic_review_of_decision_making.pdf
- http://hdl.handle.net/21.11116/0000-000A-B54F-2
- http://dx.doi.org/10.18419/opus-13229.
- https://ecommons.luc.edu/cs_facpubs/353
- https://zenodo.org/record/3515975
- https://drops.dagstuhl.de/opus/volltexte/2008/1423/
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:0004370295000097/MAIN/application/pdf/832f92bc900d122bddf754e4697c7646/main.pdf
- http://amslaurea.unibo.it/23856/1/%5B2021-07-14%5D%20Jason%20Dellaluce%20-%20Master%20Thesis.pdf
- http://centria.di.fct.unl.pt/~jja/updates/page1/page4/assets/epia01c.pdf
- http://www.sciencedirect.com/science/article/B6VCT-4K4WH30-1/1/17f085836a5c5e92684582c95a29eb4d
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.5682
- https://dare.uva.nl/personal/pure/en/publications/reasoning-in-nonprobabilistic-uncertainty-logic-programming-and-neuralsymbolic-computing-as-examples(297f803e-3318-4cce-8ddf-5c004bda4a33).html
- http://repository.tudelft.nl/assets/uuid%3Afdc0105c-e601-402a-8f16-ca97e9963592/Walker_2003.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.8.2380
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-163419
- https://hal.archives-ouvertes.fr/hal-03463124
- https://ojs.aaai.org/index.php/AAAI/article/view/10495
- http://resolver.tudelft.nl/uuid:d17a6921-b2c6-4da6-9508-d240bc05d0c3
- https://hal.archives-ouvertes.fr/hal-03394664
- https://scholar.smu.edu/cgi/viewcontent.cgi?article=1013&amp;context=engineering_managment_etds
- https://www.utupub.fi/handle/10024/155568
- http://www.cs.iit.edu/~calinesc/Yu-TakeIntelligentRisk.pdf
- https://hdl.handle.net/10657/16840
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.53.4593
- http://psasir.upm.edu.my/id/eprint/20897/1/ID%2020897.pdf
- https://doi.org/10.2514/6.2014-0298
- https://scholarworks.rit.edu/theses/100
- https://drops.dagstuhl.de/opus/volltexte/2017/6915/
- https://zenodo.org/record/8262850
- http://pan.oxfordjournals.org/content/early/2014/11/04/pan.mpu016.full.pdf
- https://discovery.ucl.ac.uk/id/eprint/10145639/
- http://arxiv.org/abs/2103.06727
- http://cds.cern.ch/record/2264304
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.91.8351
- http://arxiv.org/pdf/1404.7173.pdf
- https://repository.upenn.edu/dissertations/AAI29067593
- http://cds.cern.ch/record/2317533
- https://docs.lib.purdue.edu/dissertations/AAI30506206
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:0888613X87900053/MAIN/application/pdf/79fd59e83eb61b4dc731952521663f55/main.pdf
- https://hal.science/hal-03141719/document
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.54.2477
- http://hdl.handle.net/20.500.11850/129881
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:0270025587905781/MAIN/application/pdf/ebbca0836b41daae1739369dc9e7137c/main.pdf
- https://scholarsmine.mst.edu/mec_aereng_facwork/1458
- https://openaccess.city.ac.uk/id/eprint/28163/1/paper3.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/4127
- http://dx.doi.org/10.13039/501100007273
- http://hdl.handle.net/1773/23481
- http://cfmetrologie.edpsciences.org/articles/metrology/pdf/2015/01/metrology_metr2015_02005.pdf
- http://hal-irsn.archives-ouvertes.fr/docs/00/19/66/63/PDF/SAMO2007_BaccouChojDes.pdf
- http://hdl.handle.net/10.1184/r1/21830340.v1
- http://hdl.handle.net/11311/1149308
- https://cris.maastrichtuniversity.nl/en/publications/bd49eae7-0f44-4dd5-a4db-e11c4833db6c
- http://hdl.handle.net/11565/40432
- https://hal.science/hal-02860485/file/volume-1-chapitre-17-Springer.pdf
- https://escholarship.org/uc/item/9xx9c76h
- https://zenodo.org/record/7634488
- https://docs.lib.purdue.edu/dissertations/AAI9003886
- https://lirias.kuleuven.be/bitstream/123456789/570134/1/ibm.pdf
- http://aaaipress.org/Papers/FLAIRS/1998/FLAIRS98-080.pdf
- http://www.hull.ac.uk/php/479886/publications/smps08-uv.pdf
- https://hdl.handle.net/11511/47271
- https://stars.library.ucf.edu/scopus2015/6947
- http://cardinalscholar.bsu.edu/handle/handle/183695
- http://hdl.handle.net/1885/62318
- http://hdl.handle.net/11379/529007
- https://escholarship.org/uc/item/9j33z8zg
- https://orbilu.uni.lu/bitstream/10993/30739/1/reasoning_in_non-probabilistic_uncertainty.pdf
- http://hdl.handle.net/10261/162416
- http://hdl.handle.net/1822/31239
- http://digitool.Library.McGill.CA:80/R/?func=dbin-jump-full&object_id=69581
- http://www.armyconference.org/ACAS00-02/ACAS01/BookerJane/BookerJane.paper.pdf
- http://dspace.cc.tut.fi/dpub/handle/123456789/23577
- http://hdl.handle.net/2117/374885
- http://euclid.ucc.ie/pages/staff/seda/htdocs/cie-komendantskayaseda.pdf
- http://www.aaai.org/ocs/index.php/SSS/SSS15/paper/viewFile/10281/10029%26sa%3DU%26ved%3D0CAQQFjAAahUKEwjd3tPQqPvGAhWCVhQKHacjCJQ%26client%3Dinternal-uds-cse%26usg%3DAFQjCNF4wF1u_JS20P9rQfT25aSsc26HMg/
- https://lirias.kuleuven.be/handle/123456789/584680
- http://cds.cern.ch/record/1985671
- http://hdl.handle.net/10.1184/r1/21652148.v1
- http://journals.sfu.ca/int_assess/index.php/iaj/article/download/122/79/
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-178027
- https://doi.org/10.2514/6.2014-0300
- http://hdl.handle.net/10536/DRO/DU:30111072
- http://hdl.handle.net/10261/189116
- http://hdl.handle.net/2117/364239
- http://arxiv.org/abs/2308.12486
- https://osf.io/cz9ja
- https://www.sciencedirect.com/science/article/pii/S2212420919309070#!
- http://publica.fraunhofer.de/documents/N-518409.html
- http://dx.doi.org/10.3233/FAIA210354
- https://hal.science/hal-01270598
- http://hdl.handle.net/2013/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/260528
- http://hdl.handle.net/1822/31331
- https://doi.org/10.1145/3378678.3391882
- http://urn.fi/urn:nbn:fi-fe2021090645179
- https://dr.lib.iastate.edu/handle/20.500.12876/30148
- http://hdl.handle.net/11565/53243
- http://arxiv.org/abs/2111.08164
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:0888613X88900047/MAIN/application/pdf/49a952abfe58c6a10aa2bfca014584e0/main.pdf
- http://hdl.handle.net/11565/40061
- https://docs.lib.purdue.edu/dissertations/AAI3686872
- https://research.vu.nl/en/publications/12b0e305-02a5-426e-80eb-f69a5ea89763
- https://ojs.aaai.org/index.php/AAAI/article/view/26920
- http://hdl.handle.net/2077/40579
- https://digital.library.unt.edu/ark:/67531/metadc926591/
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:0888613X91900013/MAIN/application/pdf/454bf4e8bf04e6dd624b340bdd69cd2b/main.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0888613X09000553/MAIN/application/pdf/b14d5d4085451b213b16df189ae50bfe/main.pdf
- https://research.chalmers.se/en/publication/538365cf-05cf-4938-ba74-74324dd95e3b
- https://doi.org/10.1007/978-3-031-47958-8_11
- https://lirias.kuleuven.be/handle/123456789/624590
- https://scholarworks.utep.edu/cs_techrep/1108
- http://www.eis.mdx.ac.uk/staffpages/juanaugusto/LuALWA2012.pdf
- https://digital.library.unt.edu/ark:/67531/metadc929879/
- http://research.microsoft.com/en-us/um/people/horvitz/ftp/u87.pdf
- https://opus.bibliothek.uni-augsburg.de/opus4/frontdoor/index/index/docId/21437
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:0888613X9090001I/MAIN/application/pdf/ea92c23a2abcee30dff5f03bbac4e8f0/main.pdf
- https://lirias.kuleuven.be/handle/123456789/642636
- http://hdl.handle.net/11311/1021071
- https://hal.archives-ouvertes.fr/hal-01401195
- http://hdl.handle.net/11615/28276
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:0888613X91900057/MAIN/application/pdf/41a972e307f139e0d9abab64dd78a1b5/main.pdf
- http://wrap.warwick.ac.uk/86898/1/encyclopedia_cog_neuro_revision.pdf
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0888613X07000849/MAIN/application/pdf/b0d3407abb8ba9f33c0d405dda4e5619/main.pdf
- http://resolver.tudelft.nl/uuid:85b36b9b-2db3-451a-b7cb-70f6b9d24de9
- http://home.robotic.de/fileadmin/control/hecker/publications/hecker_ijc2006.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0019995878901651/MAIN/application/pdf/ac1b2dd96a08b545ad1b75983f07ccca/main.pdf
- http://hdl.handle.net/11365/1122216