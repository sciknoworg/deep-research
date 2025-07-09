# Final Report: Will the AMOC Change Its Course?

This report synthesizes extensive research findings and modeling experiments on the Atlantic Meridional Overturning Circulation (AMOC), addressing the question of whether it will "change its course." For clarity, the term is unpacked into two distinct but interrelated aspects:

1. **Spatial Shifts vs. Dynamic/Intensity Changes:**
   - **Spatial Shifts:** Refers to changes in the physical path of the AMOC—from a reconfiguration of the current’s geographical trajectory (e.g., shifts in the mean centers, Gulf Stream/North Atlantic Current alignment, ITCZ repositioning) potentially driven by changes in submesoscale processes, basin-wide freshwater balances, and topographic effects.
   - **Dynamic/Intensity Changes:** Involves alterations in the strength, phase, or variability of the circulation. This includes variations in the magnitude of deep water formation, the rate of northward salinity transport, and the transient responses to anomalous forcing (freshwater input, temperature gradients, or atmospheric feedbacks).

In what follows, we provide a detailed discussion spanning near-term (decades) to long-term (centuries) perspectives, potential drivers, feedback processes, and the implications of advanced modeling and observational efforts.

---

## 1. Defining the Problem and Scope

### 1.1. Terminology and Distinctions

Studies across disciplines have distinguished between _spatial remapping_ (i.e., changes in the geographic locus or course, analogous to visuomotor remapping in cognitive neuroscience) and _dynamic or intensity variations_ (e.g., alterations in error-correction gains in adaptive systems). While a spatial shift might represent a reorganization in the AMOC’s mean pathway due to inherent oceanic and atmospheric interactions, changes in dynamics manifest as fluctuations in its strength, speed, or energy content over various timescales.

### 1.2. Timeframe Considerations

- **Near-term (Decadal) Adjustments:** Driven largely by rapid feedbacks such as those associated with the North Atlantic Oscillation (NAO), barotropic/baroclinic responses, and seasonal freshwater anomalies.
- **Long-term (Centennial to Millennial) Projections:** Governed by slower processes including coupled sea ice-ocean feedbacks, greenhouse gas-induced radiative changes, and land-ice meltwater contributions.

---

## 2. Drivers and Feedback Mechanisms

The AMOC is subject to complex and interwoven drivers. The following subsections outline key processes identified through both observational campaigns and high-resolution simulations:

### 2.1. Temperature and Salinity Feedbacks

A critical research finding is the role of compensatory temperature and salinity feedbacks. For example:

- **Temperature Effects:** Global warming reduces the air–sea temperature gradients, particularly in regions of deepwater formation, which can dampen convection.
- **Salinity Effects:** Freshwater input from melting ice alters the surface salinity, modifying the density structure essential for deep convection. Notably, freshwater anomalies can weaken the AMOC more effectively (a positive feedback mechanism), whereas negative anomalies require a larger magnitude to produce an equivalent intensification. The asymmetry in these responses underscores the observed nonlinearity in AMOC behavior.

### 2.2. Freshwater Forcing and Feedback Amplification

Several studies have demonstrated that regional freshwater anomalies, particularly in the North Atlantic and Greenland meltwater runoff, can yield dramatic reductions in AMOC strength. Sensitivity experiments (e.g., from the Bergen Climate Model) have indicated that enhanced freshwater runoff can depress the AMOC by up to 30% within 50 years. Importantly, once freshwater input declines, there can be a decadal-scale recovery, although lasting regional sea-level impacts may persist.

In addition, the role of South Atlantic dipole anomalies is crucial. Freshwater input in these regions can reconfigure the basin-scale salt-advection feedback, potentially triggering abrupt shifts or even a complete collapse of the AMOC if representatively strong gradients arise.

### 2.3. Aerosol-Cloud Interactions

CMIP6 simulations introduce refined aerosol-cloud interaction parameterizations that demonstrate anthropogenic aerosol forcing can lead to a strengthening (by up to ~10–20%) of the AMOC in the historical period (1850–1985). While these effects appear to modify the salinity budget and deep convection processes, there is debate over the magnitude and realism of this forcing. Aerosol-induced changes generally interact with thermal gradients and salinity anomalies, adding another layer of complexity to predicting whether the AMOC will shift spatially or change in strength.

### 2.4. Barotropic and Baroclinic Responses

Studies using coupled and atmosphere-only simulations reveal a two-timescale response in the AMOC:

- **Fast Barotropic Adjustment:** Occurring on sub-monthly timescales, primarily linked to immediate wind-driven and pressure adjustment processes.
- **Slower Baroclinic Response:** Occurring over around two years, reflecting deep water formation changes and linked to broader-scale phenomena like the NAO. This duality in response emphasizes that both rapid fluctuations and long term trends must be considered in any comprehensive evaluation of AMOC course changes.

---

## 3. Modeling Approaches and Advanced Techniques

Given the complexity of the system, recent advances in modeling and observational strategies have been essential in elucidating the AMOC’s behavior. We now describe several high-impact approaches:

### 3.1. High-Resolution and Multi-Resolution Modeling

- **Eddy-Resolving Models:** High-resolution studies (e.g., 1/24° resolution in the Labrador Sea) have shown more rapid and pronounced responses to Greenland freshwater runoff (e.g., a decline of ~2 Sv in 13 years) compared to coarser CMIP6 models. Such simulations capture mesoscale eddy interactions and spatial heterogeneity essential for realistic AMOC dynamics.

- **Coupled Model Intercomparison Projects (CMIP5/CMIP6):** Analyses across these ensembles reveal inter-model variability in the magnitude and even the sign of the AMOC trend. Differences in the treatment of aerosol-cloud interactions, zonal salinity contrasts, and spatial binning (depth vs. density frameworks) are systematically responsible for these differences. Novel techniques such as image warping and spatial binning corrections have been applied to align GCM outputs with observational reanalyses, thereby isolating the effects of spatial shifts versus intensity changes.

### 3.2. Data Assimilation and Multiscale Integration

Recent studies have integrated satellite remote sensing (using platforms such as MODIS, MISR, CALIPSO) with in situ measurements (e.g., AERONET and advanced lidar systems). The fusion of these datasets—facilitated by cloud-based frameworks like the Pangeo project—allows for improved quantification of aerosol optical properties and better constraints on the coupled interactions between the atmosphere and ocean.

- **Coupled Data Assimilation Techniques:** Approaches such as offline quadratic programming with non-negativity constraints have significantly reduced uncertainties in aerosol forcing, which directly impacts oceanic saline budgets. Adaptive observation methods, including UAV-based mobile platforms guided by information-theoretic algorithms, further enhance our observational capability to track AMOC transitions.

### 3.3. Statistical Downscaling and Machine Learning

- **Advanced Downscaling:** Methods involving multi-objective genetic programming, multiple-point geostatistics, and spectral nudging allow for the transformation of coarse-resolution climate fields into high-resolution datasets. These statistical downscaling approaches preserve the physical relationships between variables and improve the representation of air-sea interactions that modulate AMOC dynamics.

- **Machine Learning:** Random forests, gradient boosting, and XGBoost techniques have been effectively applied to forecast particulate matter and aerosol fields. Their integration into numerical models enhances the detection of rapid transitions in AMOC behavior, especially when combined with dynamic data assimilation techniques.

---

## 4. Synthesis of Model Findings and Observations

Drawing on dozens of simulation studies and observational campaigns, several patterns emerge:

### 4.1. Near-Term Variability and Threshold Behavior

- Studies using RAPID array data indicate that a sustained 20-year decline in the AMOC can be attributed to internal ocean dynamics—particularly a decline in subpolar salinity transport—rather than external atmospheric forcing alone. However, aerosol and radiative forcings are important in shaping broader trends.

- Sensitivity experiments consistently illustrate a threshold-like behavior with hysteresis. In many models, once the AMOC weakens due to freshwater anomalies or thermal differences, recovery may be slow or incomplete even if the original forcing is reversed.

### 4.2. Long-Term Projections and Stabilizing Feedbacks

- Multi-centennial simulations (e.g., the AWI climate model over 900 years) show that while interdecadal variability is robust, the long-term course of the AMOC is highly sensitive to both coupled feedbacks and external perturbations. The non-linear and asymmetric nature of the freshwater and temperature feedbacks implies that sustained changes—either spatial reorientations or intensity alterations—depend critically on the balance of these processes.

- Historical reconstructions indicate significant model-observation discrepancies. For instance, the unique "rogue" period observed between 1995 and 2015 has been linked to internal AMOC feedbacks, emphasizing that both internal variability and anthropogenic impacts must be adequately captured.

### 4.3. Spatial Reorientation Versus Intensity Modulation

- **Spatial Reorientation:** Evidence from mesoscale simulations and image warping techniques indicates that spatial shifts (e.g., a southward displacement of mid-latitude jets or a change in the Gulf Stream’s position) are possible. These reorientations are generally associated with changes in regional salinity contrasts and air–sea flux variations, though their magnitude varies considerably across models.

- **Intensity Modulation:** Several experiments—particularly those incorporating enhanced Greenland meltwater or targeted freshwater anomalies—demonstrate that changes in the overall strength of the AMOC can be abrupt (with reductions exceeding 20–30% over decades) and are subject to recovery dynamics that exhibit hysteresis. This sensitivity is further complicated by the interplay of aerosol effects, which under some assumptions have contributed to a historical strengthening that may now be transitioning into a decline under global warming.

---

## 5. Open Questions and Future Research Directions

Despite major advances, several key questions remain:

### 5.1. Uncertainty Reduction in Model Ensembles

- **Inter-model Variability:** Given the discrepancies between CMIP5 and CMIP6 simulations as well as the differences introduced by model resolution, future work should focus on reconciling these differences through improved proxy reconstructions, targeted observational campaigns, and enhanced physical parameterizations.

- **Hybrid Approaches:** Integrating high-resolution local observations with global datasets via advanced statistical and machine learning frameworks (e.g., Gaussian-process emulation) appears promising to provide tighter constraints on AMOC dynamics.

### 5.2. Role of Novel Feedback and Control Mechanisms

- **Air-Sea Interaction Nuances:** The latest findings on aerosol-induced effects suggest that further investigation into the coupling between aerosol forcing, cloud microphysics, and oceanic convection is warranted. Detailed process studies are needed to quantify how these interactions may tip the balance in favor of either spatial reorientation or intensity modulation.

- **Neuromodulatory and Adaptive Control Paradigms:** Recent interdisciplinary work, inspired by sensorimotor adaptation in biological systems, hints that dynamic adjustments and adaptation memory might be analogous to ocean response systems. These counterintuitive approaches might offer novel ways to conceptualize rapid versus gradual shifts in the AMOC system.

### 5.3. Observational Campaigns and Advanced Instrumentation

- **Enhanced Remote Sensing:** The integration of satellite observations (e.g., from new-generation instruments beyond the A-Train constellation) with in situ measurements will be critical for reducing uncertainties, particularly in aerosol optical properties and salinity fields.

- **Mobile Observers:** There is strong evidence supporting the deployment of high-resolution mobile measurement systems—including UAV-based platforms—for adaptive, real-time tracking of AMOC pathways and changes in the subpolar gyre.

---

## 6. Conclusions

The current state of research indicates that the AMOC is likely to "change its course" in both senses of the term: spatial reorientations and modulations in strength. 

- Under near-term scenarios, rapid barotropic adjustments driven by atmospheric fluctuations and internal oceanic variabilities are superimposed on slower baroclinic responses driven by alterations in deep water production.
- Long-term projections suggest that compounded effects from anthropogenic warming, freshwater forcing (especially from Greenland ice melt), and aerosol-cloud interactions may push the AMOC through non-linear thresholds resulting in significant reconfigurations and intensity declines with potential hysteresis.

While substantial uncertainties remain, particularly regarding model intercomparisons and parameter sensitivities (notably the magnitudes of aerosol forcing and freshwater perturbations), the use of advanced, high-resolution computational and observational tools is steadily narrowing these gaps. The path forward lies in coupling diverse observational strategies with robust, multi-scale models that incorporate both classic physical constraints and newer adaptive control paradigms inspired by neuromodulatory systems.

In summary, whether changes in the AMOC manifest predominantly as spatial shifts, intensity modulations, or a combination thereof depends critically on the interplay between rapid atmospheric forcing, slower oceanic feedbacks, and the evolving background state under a warming climate. Continued investment in high-resolution simulations, comprehensive data assimilation efforts, and innovative observational campaigns will be key to resolving these issues and informing projections of future climate impacts.

---

*This report integrates multidisciplinary insights from climate modeling, oceanography, remote sensing, and innovative computational techniques to provide a comprehensive overview addressing the multifaceted nature of potential AMOC changes.*

## Sources

- http://hdl.handle.net/20.500.11897/419756
- http://hdl.handle.net/11585/821587
- http://public.lanl.gov/wilbert/Publications/pdf/Weijer2012a.pdf
- https://figshare.com/articles/_The_CoP_progression_velocity_in_anterior_posterior_direction_and_stance_time_/1383507
- https://centaur.reading.ac.uk/115656/1/Cefalu_thesis_redacted.pdf
- https://epic.awi.de/id/eprint/57985/1/Sun_et_al_2022.pdf
- http://hdl.handle.net/21.11116/0000-0001-4852-2
- https://dspace.library.uu.nl/handle/1874/257329
- https://mural.maynoothuniversity.ie/12060/1/GM_Atlantic.pdf
- https://repository.uwyo.edu/cgi/viewcontent.cgi?article=1040\u26amp;context=atmospheric_facpub
- https://dx.doi.org/10.1175/BAMS-86-12-1795
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/27650
- http://resolver.tudelft.nl/uuid:46e1ed64-8aa7-4508-917b-8fe26b1956eb
- https://doaj.org/article/35ce16c6215c446488bcca5b7caf036c
- https://repository.uwyo.edu/cgi/viewcontent.cgi?article=1107\u26amp;context=geology_facpub
- https://hal.science/hal-00138640/file/%255B15200485%2520-%2520Journal%2520of%2520Physical%2520Oceanography%255D%2520Gulf%2520Stream%2520Variability%2520in%2520Five%2520Oceanic%2520General%2520Circulation%2520Models.pdf
- http://hdl.handle.net/2060/20070004780
- http://hdl.handle.net/11583/2959546
- https://doaj.org/article/3a840b292a25436d94cfc021fa87c44d
- http://hdl.handle.net/11858/00-001M-0000-0010-764F-0
- http://localhost:8080/xmlui/handle/123456789/18947
- http://digital.library.unt.edu/ark:/67531/metadc834490/
- https://hdl.handle.net/1956/804
- http://hdl.handle.net/2066/99722
- https://dspace.library.uu.nl/handle/1874/424095
- http://www.scopus.com/home.url)
- http://www.mssanz.org.au/modsim09/I13/katzfey_I13.pdf
- https://research.monash.edu/en/publications/b4405581-6335-43e1-8487-494d9f44a913
- http://hdl.handle.net/20.500.11937/45900
- https://hal.sorbonne-universite.fr/hal-01331257/document
- https://orcid.org/0000-0001-5993-9088
- https://openscholarship.wustl.edu/etd/1178
- https://doaj.org/article/defdf3782fe847fcb1699d79a37dad54
- http://sedici.unlp.edu.ar/bitstream/handle/10915/22665/Documento_completo.pdf?sequence%3D3
- https://doaj.org/toc/2072-4292
- https://hal.archives-ouvertes.fr/hal-00770689
- https://hal.science/hal-00985545
- https://hal.archives-ouvertes.fr/hal-02338493
- https://doi.org/10.1029/2021GL097114
- https://scholarworks.uvm.edu/graddis/1556
- http://www.documentation.ird.fr/hor/fdi:010048440
- http://hdl.handle.net/11858/00-001M-0000-0012-3050-7
- https://oceanrep.geomar.de/id/eprint/44233/1/jcli-d-17-0859.1.pdf
- https://hdl.handle.net/1912/6378
- https://doaj.org/toc/1932-6203
- https://archimer.ifremer.fr/doc/00746/85806/90953.jpg
- http://hdl.handle.net/2027.42/95340
- http://resolver.tudelft.nl/uuid:5550c9bc-5eca-4945-a084-2eeebcfbb4fe
- http://bjps.oxfordjournals.org/content/40/3/289.full.pdf
- http://digitool.Library.McGill.CA:80/R/?func=dbin-jump-full&object_id=34503
- http://conference2011.wcrp-climate.org/posters/C9/C9_Wen_M98B.pdf
- https://hal.science/hal-00753326
- http://unist.dcollection.net/common/orgView/200000643055
- https://figshare.com/articles/Consequences_of_Global_Warming_of_1_5_C_and_2_C_for_Regional_Temperature_and_Precipitation_Changes_in_the_Contiguous_United_States/4541557
- http://hdl.handle.net/2060/20000112948
- https://espace.library.uq.edu.au/view/UQ:81cb075
- https://escholarship.org/uc/item/3ww7v7s2
- http://hdl.handle.net/21.11116/0000-0004-87EE-8
- https://www.zora.uzh.ch/id/eprint/115456/1/3130.full.pdf
- https://osf.io/ewh4t
- https://escholarship.org/uc/item/8z8729ks
- https://mural.maynoothuniversity.ie/17729/1/mccarthy-caesar-2023-can-we-trust-projections-of-amoc-weakening-based-on-climate-models-that-cannot-reproduce-the-past.pdf
- https://centaur.reading.ac.uk/103346/8/fmars-09-830821.pdf
- https://escholarship.org/uc/item/4x24m9qr
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.468.3540
- https://doi.org/10.1175/BAMS-D-11-00151.1
- https://zenodo.org/record/3467549
- http://hdl.handle.net/2078.1/35529
- http://pqdtopen.proquest.com/#viewpdf?dispub=1505254
- http://resolver.sub.uni-goettingen.de/purl?gldocs-11858/8380
- https://doi.org/10.1002/2017JC013390
- http://hdl.handle.net/1885/69337
- https://figshare.com/articles/_Spatial_transfer_of_adaptation_/834628
- https://dspace.library.uu.nl/handle/1874/409300
- http://publications.jrc.ec.europa.eu/repository/handle/JRC108763
- http://hdl.handle.net/10397/27546
- https://hal.science/hal-03841884/file/Swingedouw_FC_2022.pdf
- http://www.perceptionandaction.com/pdf/publications/refJournals/2012-01-LawrenceBaughMarotta.pdf
- https://hal.sorbonne-universite.fr/hal-03838473
- https://figshare.com/articles/Behavioural_Distinction_between_Strategic_Control_and_Spatial_Realignment_during_Visuomotor_Adaptation_in_a_Viewing_Window_Task__/117264
- http://web.mit.edu/hanlimc/www/hl.docs/Choietal_ICCS07.pdf
- https://lirias.kuleuven.be/bitstream/123456789/553690/1/Hossein%20convection-permittmodels%20%28HESS%202016%29.pdf
- http://conference2011.wcrp-climate.org/posters/C37/C37_Dixon_TH85B.pdf
- https://escholarship.org/uc/item/13g840ps
- http://resolver.sub.uni-goettingen.de/purl?gldocs-11858/9990
- http://hdl.handle.net/10.6084/m9.figshare.7491629.v1
- https://zenodo.org/record/8163482
- https://hdl.handle.net/2104/11116
- http://hdl.handle.net/10.6084/m9.figshare.24100547.v1
- http://hdl.handle.net/20.500.11850/550679
- https://hal.science/hal-00770689
- http://hdl.handle.net/2144/2058
- http://hdl.handle.net/11858/00-001M-0000-000E-F4C1-E
- http://hdl.handle.net/10.1371/journal.pone.0280389.g002
- http://web.science.unsw.edu.au/%7Ejasone/publications/jhaetal2013.pdf
- https://doaj.org/article/1c7596edb9ab4dca9bb0f92ae02bc8f5
- https://escholarship.org/uc/item/69c684rd
- http://www.sfn.org/absarchive/
- http://www.atmos-chem-phys.net/12/3601/2012/acp-12-3601-2012.pdf
- https://archimer.ifremer.fr/doc/00358/46879/46760.pdf
- https://research.vu.nl/en/publications/23819acf-602d-4819-8a62-f3e866c28812
- https://hal.science/hal-03093315
- https://elib.dlr.de/195688/
- http://www.documentation.ird.fr/hor/fdi:010037648
- http://urn.kb.se/resolve?urn=urn:nbn:se:su:diva-155716
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0896627309007958/MAIN/application/pdf/d3ea55e74aabe0d84ddc6cf7d66767af/main.pdf
- http://hdl.handle.net/10454/2874
- https://mural.maynoothuniversity.ie/16046/
- http://edoc.mpg.de/223452
- https://doaj.org/article/e2010d89f7ec4aefb63cdb6ae520fcaa
- https://hal.science/hal-03869321
- http://www.loc.gov/mods/v3
- https://doaj.org/article/b8ce710803964d8cb279e3a537aa5a39
- https://authors.library.caltech.edu/39251/7/10.1175_bams-d-12-00015.2.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0960982201004158/MAIN/application/pdf/ac2837ec641ce8c45622660133f54fa2/main.pdf
- https://hdl.handle.net/
- https://hdl.handle.net/11591/485830
- http://hdl.handle.net/2078.1/72000
- https://escholarship.org/uc/item/6d30886d
- https://oskar-bordeaux.fr/handle/20.500.12278/170370
- http://hdl.handle.net/2060/20000050478
- https://centaur.reading.ac.uk/91305/10/2020GL088166.pdf
- https://escholarship.org/uc/item/9zh399j3
- http://digital.library.unt.edu/ark:/67531/metadc867492/
- https://hdl.handle.net/20.500.11766/11304
- https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2021GL096066
- https://figshare.com/articles/Contributions_of_Uncertainty_in_Droplet_Nucleation_to_the_Indirect_Effect_in_Global_Models/4503047
- http://hdl.handle.net/11858/00-001M-0000-0011-FB5D-D
- https://hal.science/hal-00763172/document
- http://hdl.handle.net/11858/00-001M-0000-0013-7900-4
- http://earth.huji.ac.il/data/pics/Space_Science_Reviews_Rosenfeld06.pdf
- https://dspace.library.uu.nl/handle/1874/361186
- http://hdl.handle.net/20.500.11850/441066
- https://orbi.uliege.be/handle/2268/230984
- https://doi.pangaea.de/10.1594/PANGAEA.897395
- https://oceanrep.geomar.de/id/eprint/39147/
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1364815216302122/MAIN/application/pdf/91aa06a61dd197b732ce091786d4fb9f/main.pdf
- http://hdl.handle.net/11858/00-001M-0000-002A-C590-5
- https://figshare.com/articles/_The_shift_in_intervention_strategy_and_intensity_for_the_range_of_the_alternative_future_intervention_strategies_considered_/1374654
- https://hal.science/hal-03023504
- https://orcid.org/0000-0002-5468-575X
- https://doaj.org/article/c6a3c51e9d194392b3ac55e16351c747
- https://figshare.com/articles/Shifts_in_distance_and_direction_of_the_mean_centers_of_highly_suitable_areas_in_different_periods_/5847501
- https://escholarship.org/uc/item/0z14d6c0
- https://hal-insu.archives-ouvertes.fr/insu-03779396
- https://www.repository.cam.ac.uk/handle/1810/261624
- https://escholarship.org/uc/item/75165150
- https://hal.science/hal-03662329
- http://hdl.handle.net/10.3389/feart.2023.1245815.s001
- https://journals.ametsoc.org/view/journals/clim/35/18/JCLI-D-21-0530.1.xml
- http://www.perceptionweb.com/abstract.cgi?id=v080387
- http://journal.frontiersin.org/researchtopic/2888/neural-and-computational-modeling-of-movement-control
- http://handle.unsw.edu.au/1959.4/56988
- https://dspace.library.uu.nl/handle/1874/275523
- https://orcid.org/0000-0001-8579-6068
- https://pearl.plymouth.ac.uk/secam-research/1466
- http://ivrylab.berkeley.edu/uploads/4/1/1/5/41152143/taylor_ivry_-_2012_-_annals_of_the_new_york_academy_of_sciences.pdf