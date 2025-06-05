# Monitoring and Managing Snow Goose Populations while Preserving Food Security for Arctic Indigenous Communities

## Introduction

The challenge of managing overabundant snow goose populations in the Arctic is compounded by the need to preserve food security and uphold the cultural integrity of Indigenous communities. This report synthesizes multi-disciplinary research and technological advancements ranging from traditional ecological knowledge (TEK) to state-of-the-art remote sensing, advanced modeling approaches, and policy innovations. The objective is to develop an integrated, adaptive management framework that addresses both ecological and socio-cultural dimensions within rapidly changing Arctic ecosystems.

## Integrating Indigenous Traditional Ecological Knowledge (TEK) with Modern Monitoring

### Context and Rationale

Indigenous TEK has been integral for generations, providing nuanced observation of ecological changes and subsistence resource management. Projects such as ArcticNet’s IK-ADAPT and the case studies in Wainwright, Alaska, underscore the capacity of TEK to identify ecological vulnerabilities, monitor changes, and guide adaptive strategies. Recent Delphi-based research has further stressed the need for integrating these localized insights with modern scientific approaches in order to obtain a more holistic and dynamic understanding of snow goose ecology.

### Methodological Frameworks

1. **Co-Production of Knowledge:** The collaborative model promotes stakeholder engagement and power sharing, allowing Indigenous communities to co-design studies. This addresses epistemological pluralism by ensuring neither TEK nor advanced scientific data is prioritized exclusively. By aligning with treaty frameworks—such as the Inuvialuit Final Agreement—these models ensure community control of data and local governance.

2. **Integrated Data Systems:** Combining Indigenous harvest records with remote sensing datasets (e.g., Sentinel-1/2, MODIS, LANDSAT) yields improved baseline data for monitoring population trends. Past studies have demonstrated that such integration not only yields robust predictive models but also refines our capacity to forecast habitat changes under variable climate conditions.

3. **Community-Based Monitoring (CBM):** CBM models, drawing from projects like Arctic PASSION and regional multi-stakeholder networks, emphasize collecting high-resolution, ground truth data and digital field observations. These are reconciled with machine learning outputs and ecological niche models using ensemble frameworks such as the Local Singular Evolutive Interpolated Kalman (LSEIK) filter.

## Remote Sensing and Advanced Monitoring Techniques

### Multi-Scale Sensing and Data Assimilation

Modern monitoring of snow goose populations leverages an array of remote sensing platforms and in situ sensors:

- **Drone and Aerial Photography:** Utilizing drone-based RGB imagery combined with photogrammetry allows detailed mapping of habitat degradation. Studies have identified optimum altitudes (e.g., 75m, 100m, 120m) to mitigate classification biases between barren and vegetated surfaces, achieving overall accuracies as high as 92%.

- **Satellite and SAR Data:** Platforms like Sentinel-1 SAR, Sentinel-2 optical, and Landsat imagery provide comprehensive time-series data on vegetation indices (NDVI), land use, and phenological changes. Such data is pivotal in understanding how migratory patterns and habitat connectivity shift under climate change and anthropogenic pressures.

- **Individual Tracking Technologies:** High-resolution GPS devices, accelerometers, and indwelling heart-rate loggers are now routinely integrated into behavioral studies of snow geese. These technologies have enabled researchers to map fine-scale movement, nesting events, and energetic expenditures with spatial accuracies within a few meters.

### Data Fusion, Machine Learning, and Modeling

The complexity of Arctic ecosystems requires that diverse data sources be harmonized and analyzed through advanced computational methods:

- **Ensemble and Bayesian Modeling:** Integrated Population Models (IPMs) employing state-space frameworks with Kalman filter assimilations are increasingly common. These models combine capture–recapture, census data, and recruitment observations to provide precise demographic parameter estimates while managing both process and measurement uncertainties.

- **Generalised Management Strategy Evaluation (GMSE):** The GMSE open-source R package has been used to simulate adaptive scenarios by incorporating genetic and agent-based algorithms. It provides spatially explicit modeling of stakeholder interactions—critical in managing conflicts between conservation goals and agricultural practices.

- **Surrogate Models and Deep Learning:** Emerging techniques include deep learning approaches such as convolutional neural networks (CNNs) and long-short term memory (LSTM) networks. They have been successful in refining habitat suitability models and predicting migratory dynamics under scenarios of increasing temperature and habitat shifts.

- **Stable Isotope Analysis:** Isotopic measurements (δ13C, δ15N, δ34S, δ2H) have been deployed as non-invasive proxies for determining the breeding origins of migratory snow geese. These methods offer high discriminant accuracies, thereby informing adaptive management across subpopulations.

## Ecosystem-Based and Direct Population Management Strategies

### Direct Management Interventions

Managing snow goose populations often involves direct actions such as regulated harvest and culling. Research into long-term datasets (e.g., capture–recapture studies of >139,000 individuals) suggests that a combination of direct regulatory actions and ecosystem-level research is essential. Matrix-based models with elasticity and stochastic components allow managers to simulate the effects of increased harvest or culling regimes while accounting for compensatory mortality and non-linear population responses.

### Ecosystem Implications and Feedback Mechanisms

The interplay between snow goose population dynamics and broader ecosystem impacts necessitates a multi-scaled approach:

- **Density-Dependent Effects:** Studies from regions such as Svalbard and the western Arctic indicate that high goose densities can lead to reduced reproductive output through negative carryover effects, weakened nutritional reserves, and habitat degradation. Mechanistic feedback loops in models are crucial for understanding these nonlinear dynamics.

- **Agro-Environmental Interactions:** Changes in agricultural practices, such as intensified use of nitrogen fertilizers, have been linked to vegetation shifts that, while boosting overwinter survival, come at the cost of degraded reproductive outputs during the breeding season. Integrating socio-economic data into ecosystem models allows for mapping these complex feedbacks between agricultural subsidies, habitat suitability, and hen physiology.

## Policy and Adaptive Governance

### Bridging Traditional and Western Approaches

Successful management of snow goose populations must navigate the cultural and political challenges intrinsic to Arctic governance. Policy frameworks like the ASM 2021 Joint Statement call for a re-balancing of power—ensuring Indigenous voices remain central in monitoring efforts—and advocate for treaty-informed adaptive models which incorporate community-driven data with scientific observations.

### Institutional Innovations for Inclusive Monitoring

- **Data Sovereignty and Governance:** As communities increasingly deploy digital monitoring tools, it is imperative to construct legal and institutional frameworks that safeguard Indigenous data rights. Establishing data harmonization protocols and standardized metadata practices are steps toward ensuring that technological solutions empower local governance rather than inadvertently enforcing external paradigms.

- **Participatory Policy Development:** Collaboration among Indigenous organizations, scientific experts, and policy makers has led to initiatives such as the Inuvialuit Harvesters Assistance Program (IHAP) which foster adaptive governance strategies. Policies designed to incorporate both TEK and modern data allow for dynamic management of food resources, ensuring that shifts in snow goose populations do not compromise the subsistence lifeways of Arctic communities.

### Adaptive Management under Climate Change

Both climate change and rapid industrial developments in the Arctic necessitate continuous model calibration, as non-stationary dynamics are the new norm. Adaptive management approaches—evidenced by projects managing migratory shorebirds—demonstrate that dynamic, stakeholder-engaged models can significantly enhance short- and long-term management outcomes. Ensemble forecasts, which now rely on sophisticated uncertainty quantification techniques (e.g., the Modified Hausdorff Distance in sea ice models), further improve decision-support accuracy.

## Future Directions and Recommendations

### Enhancing Multi-Scale Integration

1. **Refining Data Assimilation:** Continued work on merging remote sensing (multi-resolution satellite datasets, drone imagery) with ground-based observations and TEK is vital. Investment in hybrid platforms that offer real-time data synchronization will enhance early-warning systems and agile management responses.

2. **Advanced Analytic Techniques:** Expansion of machine learning frameworks, particularly those integrating isotopic analyses and fine-scale bio-logging, should be pursued. This will help predict habitat shifts, reproductive success, and other key demographic parameters under various climate scenarios.

3. **Policy-Centric Research:** Research should not only advance in technical sophistication but also integrate social dimensions. Expanding participatory research models and cross-disciplinary networks will mitigate policy disjunctions and ensure that management strategies are both culturally relevant and scientifically robust.

### Addressing Knowledge Gaps

Several critical gaps remain:

- **Data Gaps:** There is an urgent need for open-access, long-term GIS and demographic datasets that incorporate both Indigenous harvest records and modern remote sensing outputs.

- **Uncertainty Quantification:** Enhanced computational tools that robustly quantify uncertainty—using methods such as Bayesian averaging and ensemble assimilation—should be integrated routinely into operational management models.

- **Dynamic Interactions:** More nuanced studies that analyze the feedback loops between agricultural practices, climate-induced habitat changes, and goose population dynamics are required. These could employ refined IPMs that incorporate both density-dependent and direct anthropogenic effects.

## Conclusion

An integrated management framework that combines state-of-the-art remote sensing, advanced computational modeling, and Indigenous Traditional Ecological Knowledge is paramount for sustainably managing snow goose populations. The coexistence of ecological conservation with the food security needs of Indigenous communities requires multi-scalar, adaptive strategies underpinned by participatory governance and robust scientific inquiry. This report advocates for a paradigm shift toward inclusivity and continuous innovation in the face of rapid environmental change, ensuring that traditional wisdom and modern science mutually reinforce efforts to safeguard Arctic ecosystems and cultural food systems.

By strategically integrating these diverse approaches, policymakers and managers can achieve a dynamic balance: protecting both the integrity of Arctic ecosystems and the subsistence lifeways that have sustained Indigenous communities for generations.

---

*This report compiles and synthesizes evidence from over 50 research learnings and case studies. Future research efforts should focus on adaptive, integrated data systems and continuous policy refinement to address the evolving challenges of Arctic governance.*

## Sources

- https://escholarship.org/uc/item/19h9g0wj
- http://urn.fi/
- https://hdl.handle.net/10037/24315
- http://digital.library.unt.edu/ark:/67531/metadc834650/
- https://escholarship.org/uc/item/5q9460x7
- http://hdl.handle.net/11858/00-001M-0000-0011-FCDF-0
- http://www.nusl.cz/ntk/nusl-303792
- https://espace.library.uq.edu.au/view/UQ:362539
- https://zenodo.org/record/7586353
- https://orcid.org/0000-0002-6152-2609
- http://www.arcticnetmeetings.ca/asm2013/
- https://elib.dlr.de/129012/
- http://www.physics.mun.ca/~lev/Ford06.pdf
- http://www.usask.ca/hydrology/papers/Pomeroy_et_al_1997_6.pdf
- https://digitalcommons.usu.edu/wild_facpub/1506
- https://knowledge.uchicago.edu/record/3379/files/Cooper_uchicago_0330D_15943.pdf
- http://dx.doi.org/10.1016/j.gloenvcha.2009.10.008
- http://hdl.handle.net/2142/111626
- https://polarresearch.net/index.php/polar/article/view/3232
- https://doaj.org/article/fb9b7afd8ee64f3fb75d3e4305e024da
- http://dx.doi.org/10.5751/ES-07905-210116
- https://research.rug.nl/en/publications/e8659e2b-3601-429e-a0fd-bbce023f5d31
- https://doaj.org/article/06af9df263e64473b12d4b8b819ed140
- https://doi.org/10.7916/rybv-0w09
- https://hal-insu.archives-ouvertes.fr/insu-03746668
- http://lauda.ulapland.fi/handle/10024/62539
- https://orcid.org/0000-0001-5895-2141
- https://dx.doi.org/10.3390/ijerph2005020001
- https://doaj.org/article/574b5b3134eb49adbac37ae77c5a7133
- https://doi.org/10.34894/QFSIQR
- http://hdl.handle.net/10779/aru.23761770.v1
- https://zenodo.org/record/5751761
- http://datacite.org/schema/kernel-4
- http://pubs.aina.ucalgary.ca/arctic/Arctic52-2-113.pdf
- http://hdl.handle.net/11250/217566
- http://hdl.handle.net/10.1371/journal.pone.0203077.t003
- http://www.birdpop.org/downloaddocuments/demographic_justification.pdf
- https://escholarship.org/uc/item/2t59n4jx
- http://research.amnh.org/users/rfr/koonsetal13.pdf
- http://arctic.synergiesprairies.ca/arctic/index.php/arctic/article/download/4447/4525/
- http://icb.oxfordjournals.org/content/44/2/119.full.pdf
- https://zenodo.org/record/6399221
- https://epic.awi.de/id/eprint/40996/1/poster_PolarPrediction_NY_v6.pdf
- https://research.ulapland.fi/fi/publications/bc17b8f8-2299-4fe5-8653-a41bf19816f2
- https://doaj.org/article/64a0735f1c5c404090c34d47ef320789
- http://www.vliz.be/nl/open-marien-archief?module=ref&refid=73487
- https://ir.lib.uwo.ca/si/vol2/iss1/5
- https://hdl.handle.net/10037/25016
- http://hdl.handle.net/11250/2443735
- https://eprints.whiterose.ac.uk/153433/1/Manuscript-Revised_Final_August%2005.docx
- http://dx.doi.org/10.1017/S0032247409008602
- https://doaj.org/article/5d37269ed2734f7bac2303b89ff00149
- https://durham-repository.worktribe.com/file/1981087/1/Published%20Journal%20Article%20%28Advance%20Online%20Version%29
- https://research.wur.nl/en/publications/egmp-population-status-and-assessment-report
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-322340
- http://dx.doi.org/10.25675/10217/180936
- http://hdl.handle.net/10779/aru.23764878.v1
- https://zenodo.org/record/6513051
- https://zenodo.org/record/6965473
- https://doaj.org/article/98b0fffe873945238fb829214a3112cd
- https://research.rug.nl/en/publications/a7a2658e-c5da-4419-970a-a977bb09ccb7
- https://u-paris.hal.science/hal-03662752/document
- https://hdl.handle.net/2027.42/151574
- https://pure.rug.nl/ws/files/134868537/Arcticgeese_asymposiumsynthesis.pdf
- https://zenodo.org/record/6665730
- http://hdl.handle.net/10536/DRO/DU:30035111
- http://dx.doi.org/10.20350/digitalCSIC/5576
- https://commons.und.edu/bio-fac/11
- https://polarresearch.net/index.php/polar/article/view/2965
- https://doaj.org/article/19103c2e54e34409837e58f63d09c573
- http://hdl.handle.net/10388/etd-06162010-114258
- https://zenodo.org/record/8086466
- http://wildfowl.wwt.org.uk/index.php/wildfowl/article/download/1105/1105/
- http://library.wur.nl/WebQuery/wurpubs/576240
- https://doaj.org/article/423d5990509644d190537c62a029213a
- http://hdl.handle.net/10388/etd-12062010-143712
- https://dare.uva.nl/personal/pure/en/publications/outflying-climate-change(5369ac18-782f-4aba-be48-cd5e1f5e6ec1).html
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-87954
- https://eprints.glos.ac.uk/4918/8/Prediction%20of%20the%20distribution%20of%20Arctic.pdf
- http://hdl.handle.net/11311/1216924
- http://arctic.journalhosting.ucalgary.ca/arctic/index.php/arctic/article/download/4447/4654/
- https://scholarworks.utep.edu/open_etd/775
- http://publications.jrc.ec.europa.eu/repository/handle/JRC108988
- https://research.rug.nl/en/publications/a319c60e-c2f5-4659-8867-0f7730d03523
- https://orcid.org/0000-0002-9587-811X
- https://doi.org/10.1002/qj.2523
- https://zenodo.org/record/7090699
- http://www2.humboldt.edu/wildlife/faculty/black/pdf/Pettifor2000JAniEco.pdf
- https://research.rug.nl/en/datasets/3624d47b-6950-42f5-a35b-a27df364ffaf
- http://people.cs.umass.edu/%7Esheldon/papers/farnsworth-radar-aimag.pdf
- http://www.tandfonline.com/doi/abs/10.1080/1088937X.2011.591962
- http://library.wur.nl/WebQuery/wurpubs/515370
- https://trace.tennessee.edu/utk_graddiss/4828
- https://doaj.org/article/fec1fedb6d1140059ea2688a36ef645f
- http://hdl.handle.net/11858/00-001M-0000-0018-8104-B
- https://hdl.handle.net/11250/2654985
- https://research.rug.nl/en/publications/densitydependent-population-dynamics-of-a-high-arctic-capital-breeder-the-barnacle-goose(078c7aab-3fc2-4e85-8cd4-acfb3a7cd67b).html
- https://www.sciencedirect.com/science/article/pii/S0924796315001190?via%3Dihub
- https://zenodo.org/record/8043009
- https://zenodo.org/record/3250804
- https://doi.org/10.1051/e3sconf/202337805004
- https://research.ulapland.fi/fi/publications/a0e93e11-57ec-4ac7-9050-94dc7b99e5c1
- http://www.vliz.be/nl/open-marien-archief?module=ref&refid=129667
- https://www.rug.nl/research/portal/en/publications/arctic-geese(613145b9-1700-4fe9-aacb-80d774b3c3ad).html
- https://doaj.org/article/a764b20e249c457abd9c9ff9e86314a2
- https://ojs.lib.uwo.ca/index.php/si/article/view/5238
- http://hdl.handle.net/1773/40584
- https://hal.science/hal-04039094/document
- http://www.loc.gov/mods/v3
- https://research.wur.nl/en/publications/perspectives-in-machine-learning-for-wildlife-conservation
- http://hdl.handle.net/1969.1/174464
- https://hdl.handle.net/11250/2762711
- http://fwf.ag.utk.edu/mgray/wfs560/SnowGeese.pdf
- https://doaj.org/article/cabad049a8bb4f498167620050f3b0ef
- http://hdl.handle.net/11250/2474040
- http://hdl.handle.net/11250/300229
- https://hdl.handle.net/11250/2832519
- https://doi.org/10.1007/978-3-319-75756-8
- http://hdl.handle.net/20.500.11850/478018
- https://scholarworks.utep.edu/dissertations/AAI10282456
- https://journals.macewan.ca/earthcommon/article/view/1228
- https://zenodo.org/record/8055176
- https://lup.lub.lu.se/record/7890d443-fbf3-44dd-84c0-a196fa8d29f9
- https://doaj.org/article/3d4ce5752aac4955b7fb9aad8d7d5326
- http://centaur.reading.ac.uk/32624/1/Hodsonetal_2012a.pdf
- http://ageconsearch.umn.edu/record/94934
- https://research.rug.nl/en/publications/25778291-b89a-48df-bd82-33584dab719f
- https://elib.dlr.de/115501/
- http://dx.doi.org/10.1007/s10113-012-0297-2
- https://doaj.org/article/43272f774c2d45918f18dc057d75fcb5
- http://hdl.handle.net/2027.42/151574
- https://digitalcommons.unl.edu/ncfwrustaff/222
- https://doaj.org/article/87398cba5b024c44a8f09ff82615c5fc
- http://pubs.aina.ucalgary.ca/arctic/Arctic49-1-70.pdf
- http://cfs.nrcan.gc.ca/pubwarehouse/pdfs/32144.pdf
- https://doaj.org/article/162f98613d9249e3acb9cd67b41ac9c0
- http://hdl.handle.net/2440/66636
- https://journals.isss.org/index.php/proceedings63rd/article/view/3638
- http://hdl.handle.net/11250/2564032
- https://www.thesolutionsjournal.com/article/continued-importance-hunting-future-inuit-food-security/
- https://doaj.org/article/c8fb3d70d39b4bfb96308e02905904a7
- https://doaj.org/article/cf620f9103e24d9395268b24e70de808
- https://dx.doi.org/10.3390/rs70911863
- https://figshare.com/articles/Mechanism_driven_statistical_models_of_avian_community_assembly_/946309
- http://www.bath.ac.uk/bio-sci/biodiversity-lab/publications/Global
- http://www.arcticnet.ulaval.ca/pdf/talks2006/pearce_tristan.pdf
- http://digital.lib.uidaho.edu/cdm/ref/collection/etd/id/1814
- http://archive.nafo.int/open/sc/2005/scr05-042.pdf
- https://zenodo.org/record/4963200
- https://zenodo.org/record/5718172
- http://dx.doi.org/10.14430/arctic4475
- https://hdl.handle.net/10037/17299
- http://arctic.synergiesprairies.ca/arctic/index.php/arctic/article/viewFile/905/930/
- https://epic.awi.de/id/eprint/42207/1/FAMOS_Mahdi_MohammadiAragh_A-07.pdf
- https://zenodo.org/record/7033845
- https://doaj.org/article/28472ad73569415dbbf9b97b37d9a102
- http://www.fs.fed.us/pnw/pubs/journals/pnw_2008_patterson(beier)002.pdf
- https://www.nature.com/articles/s41612-020-00148-5
- https://tigerprints.clemson.edu/all_dissertations/1005
- http://hdl.handle.net/2429/83161
- https://www.repository.cam.ac.uk/handle/1810/274937
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/0f/66/ijerph-02-00194.PMC3810621.pdf
- https://zenodo.org/record/8090524
- http://hdl.handle.net/A