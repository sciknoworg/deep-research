# Final Report: Effects of Soil Biota on Plant Diversity in Calcareous Soils in Central Europe

## 1. Introduction

Calcareous soils, characterized by high calcium carbonate (CaCO3) levels and elevated pH, are a defining feature of many Central European landscapes, particularly in subalpine and grassland ecosystems. The intricate interplay between soil biota and plant communities in these systems has drawn significant attention, given its implications for ecosystem stability, nutrient cycling, and biodiversity. This report synthesizes extensive research learnings that elucidate the mechanistic pathways through which soil chemical properties, microbial dynamics, and land management practices converge to regulate plant diversity in calcareous soils.

## 2. Soil Chemistry and Physical Context

### 2.1. Chemical Characteristics of Calcareous Soils

Several studies have demonstrated that calcareous soils in Central Europe exhibit unique chemical profiles relative to non-calcareous soils. Key characteristics include:

- **Elevated pH and Calcium Levels:** For instance, Swiss subalpine studies indicate an order-of-magnitude increase in extractable calcium alongside enhanced pH levels, which can profoundly influence the solubility of nutrients and the bioavailability of micronutrients.
- **Enhanced Soil Organic Carbon (SOC) Stabilization:** Doubling of SOC levels in these soils suggests that processes such as flocculation and mineral sorption are at work, potentially stabilizing carbon inputs and altering microbial metabolism and gene expression. 
- **Buffering Capacity:** The high CaCO3 content acts as a chemical buffer, mitigating fluctuations in pH and indirectly modulating nutrient availability (e.g., alterations in Al, Fe, Cu concentrations) which in turn affect soil biota composition.

### 2.2. Spatial and Textural Variability

Geostatistical techniques (e.g., semivariograms, kriging) have revealed rapid spatial variability in properties such as pH—even noting shifts of up to 1.3 units over sub-50 cm distances. This spatial heterogeneity reinforces the necessity for high-resolution mapping, including modern CNN-based Digital Soil Mapping (DSM) methods which utilize multi-scale environmental covariate windows to upscale predictions of soil organic carbon and other critical soil attributes.

## 3. Soil Biota Composition and Its Role in Plant Diversity

### 3.1. Microbial Community Structure

Soil biota in calcareous environments encompass a diverse array of microorganisms, including bacteria, fungi, archaea, and other invertebrates such as nematodes and arthropods. Research has established several key points:

- **Differential Responses to pH and Calcium Gradients:** Bacterial communities tend to exhibit higher resilience to dispersal limitations compared to fungi. Quantitative studies have shown that the modular co-occurrence scores (e.g., 0.78 for fungi versus 0.67 for bacteria) indicate the impact of environmental thresholds on these communities.
- **AM Fungal Networks and Inoculation Effects:** The introduction of arbuscular mycorrhizal (AM) fungi has been found to significantly alter microbial trajectories by promoting plant growth and modifying carbon input profiles. Such shifts typically include a reduction in Proteobacteria and an increase in Firmicutes and Gastrotricha, elucidating the central role of mycorrhizal networks in shaping overall soil biotic composition.
- **Soil Physical Disturbances and Legacy Impacts:** Studies have consistently shown that land-use intensification, such as high grazing and fertilization, reduces microbial biomass and network complexity. For example, agricultural conversion in Burgundy led to a dramatic reduction in both microbial biomass (by 71%) and fungal richness, highlighting the susceptibility of certain groups to anthropogenic pressures.

### 3.2. Nematode and Faunal Contributions

Beyond microbes, soil fauna such as nematodes serve as bio-indicators of ecosystem health. Key insights include:

- **Functional Guild Sensitivities:** Nematode assemblages altering in response to organic matter quality, root density, and pH changes have been documented. Functional indices often vary based on eco-trophic groups like bacterivores, fungivores, and plant parasites, which are sensitive to environmental disturbances.
- **Indirect Influences on Nutrient Cycling:** The interplay between nematodes and microbial communities can shift energy channels toward either bacterial or fungal decomposition pathways, depending on seasonal moisture dynamics and land use changes.

### 3.3. Plant–Soil Feedbacks

The feedback loop between plants and soil biota is critical. Phytosociological analyses on extensive datasets (e.g., 11,041 vegetation plots in the Czech Republic) have established strong correlations between soil pH/calcium gradients and vascular plant species richness. Specific plant traits—such as root length density and resource-acquisitive strategies—strongly influence both nematode functional guilds and the overall microbial community via nutrient modulation and enzyme-mediated pathways.

## 4. Advanced Methodologies and Technological Innovations

### 4.1. Monitoring Techniques and Sensor Technologies

Recent advances in sensor technology have revolutionized in-situ monitoring of plant-soil interactions:

- **High-resolution Remote Sensing and Digital Imaging:** Techniques such as LIDAR, infrared spectroscopy, and high-resolution digital imagers have been employed for real-time monitoring of plant CO2 uptake, integrating minimal on-node computation to handle large data flows.
- **Three-dimensional Imaging Modalities:** X-ray CT (both μCT and synchrotron-based CT) and Biospeckle Selective Plane Illumination Microscopy allow non-destructive 3D visualization of root architectures and soil pore structures, providing a window into microscale interactions with profound ecosystem-level implications.

### 4.2. Modeling and Statistical Approaches

To translate these microscale phenomena into robust predictive frameworks, a range of integrative techniques have been employed:

- **Structural Equation Modeling (SEM) and Network Analysis:** These approaches have been crucial for disentangling bottom-up (plant-driven) from top-down (microbial/nematode-mediated) processes, enabling researchers to quantitatively link variables like root traits, enzymatic stoichiometry, and nutrient availability.
- **Bayesian and Machine Learning Techniques:** Recent models, including Quantile Regression Forests, Random Forests, and LGD-LSTM integrations, provide enhanced predictive accuracy by capturing complex non-linearities and interspecific interactions.
- **Spatial and Geostatistical Tools:** Incorporating geostatistical simulations (e.g., Bayesian area-to-point regression kriging) and advanced variable selection techniques has significantly improved the mapping of soil properties and species distributions in diverse calcareous contexts.

### 4.3. Molecular and Functional Gene Approaches

A growing body of research has focused on molecular methods to track soil microbial function:

- **Adaptations to High pH and Carbonate Levels:** The calibration of molecular techniques (e.g., enzyme assays, substrate-induced respiration, functional gene monitoring) is critical for calcareous soils, where high pH and carbonate interference can skew standard assays. Emerging protocols are now seeking to standardize these methods, as evidenced by initiatives such as EcoFINDERS.
- **Bio-indicator Frameworks:** A structured 'logical sieve' framework has been developed to rank biological indicators. From an initial pool of 183 candidates, a refined set of 21 indicators—including 7 top molecular markers—provides a reproducible tool to monitor soil quality across diverse edaphic conditions.

## 5. Land Management, Climate Change, and Ecosystem Services

### 5.1. Land Use Intensity and Traditional Practices

Empirical data from various Central European regions reveal that land management strategies have profound effects on plant and soil biota.

- **Impacts of Intensification:** Increased fertilization, grazing intensity, and industrial agriculture have been directly linked to reduced soil food web complexity, evident in declines in earthworm, Collembolan, and oribatid mite populations, as well as lower microbial biomass and network intricacy. 
- **Role of Traditional Practices:** Conversely, low-intensity practices such as mowing, hay-making, and controlled burning help maintain high multifunctionality, preserving critical ecosystem services such as water regulation, erosion control, and carbon sequestration. A parallel can be drawn with EU CAP reforms which advocate for the 'greening' of agricultural practices to counteract biodiversity loss.

### 5.2. Climate Change Interactions

Climate change introduces additional layers of complexity in calcareous soil ecosystems:

- **Environmental Stressors:** Warming, variability in precipitation (including pulsed rewetting events), and elevated atmospheric CO2 levels have been shown to alter soil enzyme stoichiometry and microbial activity, with cascading effects on nutrient availability and nematode functional group dynamics.
- **Regional Variability and Temporal Dynamics:** Long-term monitoring, such as in the Debrecen‐Látókép and Harvard Forest studies, reveals significant seasonal and interannual variability in microbial biomass and respiration rates. Models integrating remote sensing with deep learning (e.g., CLM5 optimizations) suggest that advanced techniques are essential for capturing these dynamics on both local and landscape scales.

### 5.3. Ecosystem Services and Policy Implications

The interplay between soil properties, biota, and management practices not only affects biodiversity but has far-reaching implications for ecosystem services and agricultural sustainability:

- **Carbon Sequestration:** Integrated modeling frameworks (CAPRI and CENTURY) indicate that increasing grassland areas—even by 5%—can convert millions of hectares and yield significant greenhouse gas (GHG) reductions. Such strategies necessitate economic instruments aligned with agricultural policies to incentivize low-intensity, ecologically beneficial practices.
- **Biodiversity Conservation:** Standardizing molecular and morphological bio-indicators helps maintain a consistent monitoring framework that can inform EU soil protection strategies. The contrasting responses of fungal and bacterial communities to land use highlight the need for adaptive management practices that safeguard both market outputs and non-market ecosystem services.

## 6. Discussion: Mechanisms and Emerging Research Directions

This comprehensive synthesis highlights several emergent themes and research needs:

- **Multifactorial Interactions:** The interaction of soil pH, high CaCO3 content, and spatial heterogeneity creates a complex regulatory network influencing both microbial gene expression and plant community assembly. Studies demonstrating that plant root traits and community composition modulate nematode dynamics underscore the feedback mechanisms that reinforce these interactions.
- **Methodological Refinements:** The need for calibrated standard operating procedures to adapt molecular bio-indicators for high carbonate and high pH environments is pressing. Future work should focus on refining these protocols to reduce interference and improve assay reproducibility.
- **Advanced Modeling and Remote Sensing Integration:** Integrative frameworks that combine high-resolution imaging, advanced geostatistical methods, and deep learning promise to bridge the gap between microscale observations and regional-scale predictions. These models could drive new research initiatives aimed at optimizing land management practices in the face of climate change.
- **Contingency in Land Management:** Beyond traditional intensification and abandonment debates, there is a growing need for novel management approaches that integrate economic incentives with ecological restoration. For example, combining traditional grazing with modern digital monitoring could form the basis of precision conservation strategies that optimize both biodiversity and productivity.

## 7. Conclusions and Future Recommendations

The effects of soil biota on plant diversity in calcareous soils are governed by a delicate balance of abiotic and biotic interactions. Key conclusions include:

1. **Chemical and Spatial Heterogeneity:** The high calcium content and buffered pH create distinct niches that are critical in structuring both microbial and plant communities. Variations at even small spatial scales necessitate high-resolution mapping techniques to accurately capture these dynamics.

2. **Dynamic Biotic Feedbacks:** Soil organisms—from bacteria and fungi to nematodes—play pivotal roles in driving plant–soil feedbacks that govern nutrient cycling and community assembly. Understanding these feedbacks is essential for predicting how calcareous ecosystems will respond to management and climatic shifts.

3. **Technological Innovations:** Emerging sensor technologies, three-dimensional imaging, and advanced modeling frameworks are revolutionizing our capacity to monitor and predict ecosystem changes. These advances are critical for bridging microscale observations with broader ecological outcomes.

4. **Policy and Management Integration:** Empirical evidence strongly advocates for the preservation of traditional low-intensity land management practices alongside modern restoration techniques. Policy instruments must therefore be realigned to support ecosystem multifunctionality and sustainable practices, particularly in the face of accelerating climate change.

### Future Directions

Given the rapid evolution of both technological and ecological research, the following directions are recommended:

- **Development of Calibrated Molecular Assays:** Invest in standardized testing protocols to mitigate the confounding effects of high pH/carbonate in molecular assays for soil quality indicators.
- **Enhanced Multi-scale Modeling:** Further integrate remote sensing data with deep learning models to improve spatial predictions of soil chemical and biotic properties, thereby enhancing land use planning.
- **Cross-disciplinary Initiatives:** Foster collaborations between soil scientists, ecologists, remote sensing specialists, and policymakers to co-develop management practices that are both economically viable and ecologically robust.
- **Long-term Experimental Networks:** Expand long-term, multi-factor experiments to assess the cumulative impacts of climate change, land management, and biotic interactions on calcareous soils, ensuring that adaptive management strategies are evidence-based.

In conclusion, understanding and managing the effects of soil biota on plant diversity in calcareous soils require an integrative approach that combines advanced technological methodologies with a deep ecological understanding of plant-soil-microbe interactions. Drawing on comprehensive research from Central Europe, future efforts should aim to refine predictive models, improve monitoring techniques, and support sustainable land management that maintains both biodiversity and ecosystem functionality.

---

*This report comprehensively integrates multiple lines of evidence and cutting-edge research methodologies, reflecting the state-of-the-art in soil ecological studies and providing actionable insights for both researchers and land managers in Central Europe and beyond.*

## Sources

- http://hdl.handle.net/10447/534723
- https://push-zb.helmholtz-muenchen.de/frontdoor.php?source_opus=22219
- https://hal.science/hal-02476717
- http://hdl.handle.net/1885/86607
- http://hdl.handle.net/2440/114070
- http://www.scielo.br/pdf/sa/v70n4/a09v70n4.pdf
- http://prodinra.inra.fr/record/283951
- https://dr.lib.iastate.edu/handle/20.500.12876/EzR2BX8z
- https://library.wur.nl/WebQuery/wurpubs/548975
- https://escholarship.org/uc/item/561320gf
- https://refubium.fu-berlin.de/handle/fub188/32503
- https://escholarship.org/uc/item/3hm928sv
- http://hdl.handle.net/10255/dryad.85183
- https://boris.unibe.ch/111826/
- https://research.wur.nl/en/publications/permanent-grasslands-in-europe-land-use-change-and-intensificatio
- http://hdl.handle.net/11573/1628364
- https://hal.inrae.fr/hal-02738507
- https://trace.tennessee.edu/utk_graddiss/3730
- https://doaj.org/article/d673052c36a94099a200f6faa81d32a3
- http://home.comcast.net/~pgoovaerts/geoderma.pdf
- https://doaj.org/article/ed7f906ff8ea49a689f0e70edf804704
- https://escholarship.org/uc/item/9v85v3js
- https://research.wur.nl/en/publications/using-deep-learning-for-multivariate-mapping-of-soil-with-quantif
- https://zenodo.org/record/6540803
- http://library.wur.nl/WebQuery/wurpubs/440964
- https://hal.inrae.fr/hal-02746352
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/d4/f8/pone.0016055.PMC3017561.pdf
- https://hal.science/hal-04088229/file/pub%20Ninon%20land%20degradation.pdf
- https://hal.inrae.fr/hal-02668688
- http://prodinra.inra.fr/record/282563
- http://krishi.icar.gov.in/jspui/handle/123456789/72336
- https://library.wur.nl/WebQuery/wurpubs/563049
- http://www.rcaap.pt/detail.jsp?id=oai:agregador.ibict.br.RI_USP:oai:www.producao.usp.br:BDPI/33351
- https://doaj.org/article/cd8feaa5e33e4e41ba0aa16ad7a34f26
- http://hdl.handle.net/2078.1/153233
- https://hal.science/hal-01834227/document
- http://ezproxy.uws.edu.au/login?url=http://doi.org/10.1111/1365-2656.12574
- http://handle.uws.edu.au:8081/1959.7/uws:32464
- http://handle.uws.edu.au:8081/1959.7/uws:30699
- https://hal.inrae.fr/hal-03434006
- https://doaj.org/toc/1994-3849
- http://hdl.handle.net/2072/416734
- https://escholarship.org/uc/item/47f4100g
- https://zenodo.org/record/3631702
- http://www.sci.muni.cz/botany/chytry/FG2003.pdf
- https://digitalcommons.usu.edu/grcanyon/145
- https://research.vu.nl/en/publications/2ae10a2f-c13f-4def-b869-fd5d38561280
- http://library.wur.nl/WebQuery/wurpubs/429176
- https://zenodo.org/record/6922621
- https://doaj.org/article/1c449ba2fa4b4ea49ccdd0904add3ca7
- http://www.whoi.edu/cms/files/austin_2002_53551.pdf
- https://pure.knaw.nl/portal/en/publications/ae5a85e4-0fe5-4117-bb23-d863844fd9ae
- http://ir.ibcas.ac.cn/handle/2S10CLM1/21783
- http://dx.doi.org/10.1016/j.agee.2010.10.018
- http://handle.westernsydney.edu.au:8081/1959.7/uws:40123
- https://media.suub.uni-bremen.de/handle/elib/2268
- https://pure.knaw.nl/portal/en/publications/247d672a-148d-4860-9c08-1fa3f81eced6
- https://orbi.uliege.be/handle/2268/175006
- http://hdl.handle.net/11858/00-001M-0000-000E-D99E-7
- http://doi.org/10.7298/h89k-hy10
- http://edepot.wur.nl/272370
- https://hdl.handle.net/11244/335254
- http://handle.uws.edu.au:8081/1959.7/uws:36832
- https://ageconsearch.umn.edu/record/25383/files/pp060279.pdf
- http://ageconsearch.umn.edu/record/212651
- https://digitalcommons.unl.edu/usdaarsfacpub/1610
- https://epub.uni-regensburg.de/39288/
- https://www.scopus.com/inward/record.uri?eid=2-s2.0-48349147101&doi=10.1016%2fj.geoderma.2008.05.008&partnerID=40&md5=f0970b2114e834c7700af77d438435ac
- http://hdl.handle.net/2440/65713
- https://digitalcollection.zhaw.ch/handle/11475/19168
- http://hdl.handle.net/20.500.11850/507655
- http://dx.doi.org/10.1016/j.baae.2004.09.002
- https://dspace.library.uu.nl/handle/1874/411828
- http://onlinelibrary.wiley.com/doi/10.1111/tpj.13047/abstract
- https://api.elsevier.com/content/abstract/scopus_id/85128474353
- https://zenodo.org/record/5524941
- https://push-zb.helmholtz-muenchen.de/frontdoor.php?source_opus=52232
- https://doaj.org/article/fa0bf507cf1b4aa68a730bb6059ea221
- http://edepot.wur.nl/319663
- https://doaj.org/toc/1932-6203
- https://hal.science/hal-01269419
- http://dx.doi.org/10.1111/gcb.12752
- http://hdl.handle.net/10198/19135
- https://orbi.uliege.be/handle/2268/174852
- http://hdl.handle.net/10.57935/agr.23625303.v1
- https://pub.epsilon.slu.se/23728/1/ranheim_sveen_t_et_al_210521.pdf
- https://escholarship.org/uc/item/5vx6b93s
- https://doi.org/10.1016/j.soilbio.2015.04.013
- http://www.plosone.org/article/fetchObject.action?uri=info%3Adoi%2F10.1371%2Fjournal.pone.0111667&representation=PDF
- https://escholarship.org/uc/item/6sv6m2md
- https://escholarship.org/uc/item/6jm8v35q
- http://hdl.handle.net/11588/871666
- https://zenodo.org/record/1059175
- https://doaj.org/toc/2476-3217
- http://dx.doi.org/10.1007/s11104-016-2872-7
- https://www.sciencedirect.com/science/article/pii/S0048969723060813
- https://juser.fz-juelich.de/search?p=id:%22PreJuSER-14652%22
- http://hdl.handle.net/10068/985458
- http://dspace.lib.cranfield.ac.uk/handle/1826/5332
- https://doaj.org/article/dee06844c99744059a975dd6312f8c1d
- https://eprints.qut.edu.au/79517/
- http://eusoils.jrc.ec.europa.eu/events/soilclassification_2001/pdf/402nestroy.pdf
- http://depot.knaw.nl/11902/
- http://hdl.handle.net/2067/48118
- http://hdl.handle.net/20.500.11850/532357
- https://push-zb.helmholtz-muenchen.de/frontdoor.php?source_opus=46321
- https://www.oaepublish.com/cf/article/view/4791
- https://researchrepository.murdoch.edu.au/view/author/Standish,
- https://eprints.lancs.ac.uk/id/eprint/66660/
- https://hal.inrae.fr/hal-03167637/file/ICPR_2020_MAES___ML_Advances_Environmental_Science-2.pdf
- http://www.documentation.ird.fr/hor/fdi:010012848
- https://doi.org/10.1016/j.soilbio.2020.108038
- http://ageconsearch.umn.edu/record/97192
- https://ro.ecu.edu.au/ecuworkspost2013/6195
- http://dx.doi.org/10.1016/j.gexplo.2010.10.003
- https://hal.inrae.fr/hal-03040299
- https://library.wur.nl/WebQuery/wurpubs/540904
- http://dspace.stir.ac.uk/bitstream/1893/25934/1/2017_Dawud_et_al_Functional_Ecology.pdf
- http://hdl.handle.net/2123/18115
- https://www.webofscience.com/api/gateway?GWVersion=2&SrcApp=PARTNER_APP&SrcAuth=LinksAMR&KeyUT=WOS:000349386300001&DestLinkType=FullRecord&DestApp=ALL_WOS&UsrCustomerID=42fe17854fe8be72a22db98beb5d2208
- https://archives-publications.inrae.fr/214049_3
- https://hal.inrae.fr/hal-03434006/file/Hernandez%20et%20al.%202022%20-%20postprint.pdf
- http://hdl.handle.net/10278/30112
- https://doi.org/10.1016/j.soilbio.2015.06.012
- http://hdl.handle.net/20.500.11850/556653
- https://works.bepress.com/rebecca_mcculley/35
- https://research.rug.nl/en/publications/microbial-indicators-for-soil-quality(e0d3d177-564b-4fb9-b199-19f1e7234676).html
- https://digitalcommons.usu.edu/crc_research/526
- http://annalidibotanica.uniroma1.it/index.php/Annalidibotanica/article/view/13804
- http://hdl.handle.net/1885/201658
- http://hdl.handle.net/2437/271672
- https://pure.sruc.ac.uk/ws/files/14866654/14129.pdf
- https://figshare.com/articles/_Relative_interaction_index_RII_mean_SE_n_84_of_Artemisia_ordosica_Artemisia_sphaerocephala_Chloris_virgata_and_Setaria_viridis_in_different_treatments_of_biological_soil_crusts_BSCs_coverage_/921799
- http://edepot.wur.nl/16699
- https://research.vu.nl/en/publications/52637ff8-86ce-4402-acd8-ee768a3ccc0f
- http://om.ciheam.org/article.php?IDPDF=00007534
- https://juser.fz-juelich.de/record/857058
- https://doaj.org/article/e8f48eaa190f45baa3fc5afbd581f445
- https://doaj.org/article/0166ab892deb4d40a25dceb93e3bbe2e
- http://hdl.handle.net/10.3389/fmicb.2018.02803.s001
- http://dx.doi.org/10.1371/journal.pone.0090998
- http://hdl.handle.net/10447/77068
- http://www.jstor.org/stable/pdf/2261666.pdf
- https://doi.org/10.1038/s41598-018-36867-2
- https://doaj.org/article/6391826061ce4ba5879b0852aa714978
- https://www.zora.uzh.ch/id/eprint/211888/
- https://scholarworks.boisestate.edu/td/713
- https://orgprints.org/id/eprint/20693/
- http://prodinra.inra.fr/ft/D235AE70-55E0-4CE9-B627-31FC4BB2E302
- https://opus.hs-osnabrueck.de/frontdoor/index/index/docId/7220
- https://zenodo.org/record/7576882
- http://hdl.handle.net/1893/25934
- https://doaj.org/article/d59d61ce70a846dd80154d82354791b0
- http://doi.org/10.1371/journal.pone.0168497
- https://hal.archives-ouvertes.fr/hal-03279571/file/fdata-03-00017.pdf
- https://www.sciencedirect.com/science/article/pii/S0048969718301372
- http://publications.jrc.ec.europa.eu/repository/handle/JRC71703
- http://publications.jrc.ec.europa.eu/repository/handle/JRC101128
- https://doaj.org/article/25b0460812364dd0a97c4d537e01fe2e
- http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0103-90162005000500017
- https://orbi.uliege.be/handle/2268/21172
- http://hdl.handle.net/10.6084/m9.figshare.7000769.v1
- https://escholarship.org/uc/item/99d5599j
- https://www.zora.uzh.ch/id/eprint/168389/1/Wagg_et_al-2018-Functional_Ecology.pdf
- https://doaj.org/toc/1750-0680
- https://hal-amu.archives-ouvertes.fr/hal-02649554
- http://www.loc.gov/mods/v3
- http://hdl.handle.net/2027.42/42185
- https://research.wur.nl/en/publications/diversity-relations-of-plants-and-soil-microbes
- http://dx.doi.org/10.1128/aem.02090-22
- https://doi.org/10.1051/agro:2004041
- https://doaj.org/article/9e95f12026b248e3abea30e58d83657d
- http://doc.rero.ch/record/312516/files/12224_2007_Article_BF02803251.pdf
- https://pure.knaw.nl/portal/en/publications/b3654223-14db-4e28-8591-88a7ad5e0062
- http://dx.doi.org/10.1016/j.soilbio.2010.05.007
- https://push-zb.helmholtz-muenchen.de/frontdoor.php?source_opus=51536
- https://hal.inrae.fr/hal-03137074
- https://hal-u-picardie.archives-ouvertes.fr/hal-03616523
- https://research.vu.nl/en/publications/a4de96a0-f196-4588-9921-d4db740c80cd
- https://eprints.qut.edu.au/112365/
- https://lup.lub.lu.se/record/1726121
- http://publications.jrc.ec.europa.eu/repository/handle/JRC95921
- http://hdl.handle.net/11585/91930
- https://escholarship.org/uc/item/0cn3s5k9
- https://escholarship.org/uc/item/94m4m2s4
- https://mpra.ub.uni-muenchen.de/102945/
- https://hal.archives-ouvertes.fr/hal-01268038
- https://doi.org/10.1051/e3sconf/202338221001
- http://doi.org/10.1371/journal.pone.0114290
- https://serval.unil.ch/notice/serval:BIB_8209512C7651
- https://zenodo.org/record/5519669
- https://figshare.com/articles/Specialized_core_bacteria_associate_with_plants_adapted_to_adverse_environment_with_high_calcium_contents/5964649
- https://hal.archives-ouvertes.fr/hal-01600208
- http://essuir.sumdu.edu.ua/handle/123456789/11773
- http://hdl.handle.net/11585/720380
- https://discovery.dundee.ac.uk/en/publications/ba4b7109-f97d-4156-8c0e-a576bab05986
- https://pure.knaw.nl/portal/en/publications/e576fdeb-4a94-4224-9033-8e3d69a81206
- http://dx.doi.org/10.1016/j.soilbio.2021.108450
- https://escholarship.org/uc/item/82t445sg
- https://escholarship.org/uc/item/165913s6
- http://prodinra.inra.fr/record/344820
- https://doaj.org/toc/1854-9829
- https://digitalcollection.zhaw.ch/handle/11475/1511
- https://doaj.org/article/32a4ec296b4d4a549e22eb3d9205c3f9
- https://figshare.com/articles/Impacts_of_fertilization_practices_on_pH_and_the_pH_buffering_capacity_of_calcareous_soil/3971931
- http://prodinra.inra.fr/record/408188
- https://doaj.org/toc/2147-4249
- https://serval.unil.ch/notice/serval:BIB_24A756B364D3
- https://www.sciencedirect.com/science/article/abs/pii/S0031405623079623
- https://oskar-bordeaux.fr/handle/20.500.12278/107727
- https://doi.org/10.1016/j.ecolind.2009.02.009
- https://www.revistas.usp.br/sa/article/view/64055
- http://dzumenvis.nic.in/Microbes
- http://krishi.icar.gov.in/jspui/handle/123456789/69091
- https://escholarship.org/uc/item/8b31607d
- http://publications.jrc.ec.europa.eu/repository/handle/JRC45487
- https://doi.org/10.1016/j.apsoil.2005.11.004
- http://library.wur.nl/WebQuery/wurpubs/497316
- https://hal.archives-ouvertes.fr/hal-01208787
- https://pure.knaw.nl/portal/en/publications/soil-microbial-nematode-and-enzymatic-responses-to-elevated-co2-n-fertilization-warming-and-reduced-precipitation(b3654223-14db-4e28-8591-88a7ad5e0062).html
- http://hdl.handle.net/10388/10547
- https://pure.knaw.nl/portal/en/publications/63622a95-399a-4ed8-aa0d-eb1efe388f94
- https://push-zb.helmholtz-muenchen.de/frontdoor.php?source_opus=3145
- http://hdl.handle.net/10068/980425
- https://figshare.com/articles/General_Relationships_between_Abiotic_Soil_Properties_and_Soil_Biota_across_Spatial_Scales_and_Different_Land_Use_Types/120854
- http://ir.ibcas.ac.cn/handle/2S10CLM1/20698