# Research Quality Analysis (Simplified, Arithmetic)
============================================================

**Domain:** nlp  •  **Model/Search tag:** o3_orkg

## Overview
- Total documents analyzed: **196**
- Questions analyzed: **49**
- Configurations per question: **4** (d1_b1, d1_b4, d4_b1, d4_b4)

## Configuration Performance

### d1_b1
- 📚 Sources: 10.1 ± 0.9
- 📝 Words: 1478 ± 179
- 🔬 Mechanistic coverage: 0.16
- 🔗 Causal coverage: 0.15
- ⏱️ Temporal precision: 0.73
- 📐 Stats rigor coverage: 0.04
- ❓ Uncertainty coverage: 0.18
- 💭 Speculative signals: 0.54
- 💡 Innovation terms coverage: 0.16
- 🧩 Research gaps (signals): 0.05
- 🧭 Tasks coverage: 0.22
- 🗃️ Datasets coverage: 0.03
- 🗣️ Languages coverage: 0.13
- 📊 Eval metrics coverage: 0.24
- 🖥️ Compute terms coverage: 0.16
- 🔁 Reproducibility coverage: 0.12
- ⚠️ Safety coverage: 0.22
- 🖥️ Compute (domain) coverage: 0.16
- ⭐ Overall quality: 0.207
- 🎯 Depth: 0.330
- 🌐 Breadth: 0.146
- 🔬 Rigor: 0.084
- 💡 Innovation: 0.281
- 🧭 Domain alignment: 0.163
- 📊 Info density: 0.139

### d1_b4
- 📚 Sources: 38.3 ± 3.2
- 📝 Words: 1574 ± 159
- 🔬 Mechanistic coverage: 0.14
- 🔗 Causal coverage: 0.16
- ⏱️ Temporal precision: 0.88
- 📐 Stats rigor coverage: 0.06
- ❓ Uncertainty coverage: 0.12
- 💭 Speculative signals: 0.57
- 💡 Innovation terms coverage: 0.15
- 🧩 Research gaps (signals): 0.02
- 🧭 Tasks coverage: 0.19
- 🗃️ Datasets coverage: 0.02
- 🗣️ Languages coverage: 0.14
- 📊 Eval metrics coverage: 0.22
- 🖥️ Compute terms coverage: 0.16
- 🔁 Reproducibility coverage: 0.14
- ⚠️ Safety coverage: 0.20
- 🖥️ Compute (domain) coverage: 0.16
- ⭐ Overall quality: 0.235
- 🎯 Depth: 0.368
- 🌐 Breadth: 0.138
- 🔬 Rigor: 0.080
- 💡 Innovation: 0.279
- 🧭 Domain alignment: 0.164
- 📊 Info density: 0.492

### d4_b1
- 📚 Sources: 33.4 ± 4.4
- 📝 Words: 1541 ± 153
- 🔬 Mechanistic coverage: 0.16
- 🔗 Causal coverage: 0.16
- ⏱️ Temporal precision: 0.86
- 📐 Stats rigor coverage: 0.08
- ❓ Uncertainty coverage: 0.13
- 💭 Speculative signals: 0.57
- 💡 Innovation terms coverage: 0.15
- 🧩 Research gaps (signals): 0.03
- 🧭 Tasks coverage: 0.18
- 🗃️ Datasets coverage: 0.02
- 🗣️ Languages coverage: 0.15
- 📊 Eval metrics coverage: 0.28
- 🖥️ Compute terms coverage: 0.20
- 🔁 Reproducibility coverage: 0.13
- ⚠️ Safety coverage: 0.20
- 🖥️ Compute (domain) coverage: 0.20
- ⭐ Overall quality: 0.239
- 🎯 Depth: 0.372
- 🌐 Breadth: 0.149
- 🔬 Rigor: 0.096
- 💡 Innovation: 0.282
- 🧭 Domain alignment: 0.169
- 📊 Info density: 0.437

### d4_b4
- 📚 Sources: 224.4 ± 21.0
- 📝 Words: 2204 ± 280
- 🔬 Mechanistic coverage: 0.16
- 🔗 Causal coverage: 0.16
- ⏱️ Temporal precision: 0.96
- 📐 Stats rigor coverage: 0.10
- ❓ Uncertainty coverage: 0.19
- 💭 Speculative signals: 0.46
- 💡 Innovation terms coverage: 0.16
- 🧩 Research gaps (signals): 0.05
- 🧭 Tasks coverage: 0.24
- 🗃️ Datasets coverage: 0.03
- 🗣️ Languages coverage: 0.17
- 📊 Eval metrics coverage: 0.29
- 🖥️ Compute terms coverage: 0.20
- 🔁 Reproducibility coverage: 0.15
- ⚠️ Safety coverage: 0.20
- 🖥️ Compute (domain) coverage: 0.20
- ⭐ Overall quality: 0.287
- 🎯 Depth: 0.401
- 🌐 Breadth: 0.172
- 🔬 Rigor: 0.133
- 💡 Innovation: 0.245
- 🧭 Domain alignment: 0.178
- 📊 Info density: 1.000

## 🔍 Key Findings
1. 📈 **Source scaling**: d4_b4 uses 22.2× more sources than d1_b1.
2. 📝 **Content scaling**: d4_b4 has 1.5× more words than d1_b1.
3. 🔄 **Depth effect**: +432% sources.
4. 🌐 **Breadth effect**: +504% sources.

## 🤖 NLP Notes
- Identical aggregation, weights, and density cap as in Ecology for comparability.
- Depth uses architecture/training/ablation as mechanistic proxies; Breadth swaps to tasks/datasets/languages/metrics/compute.
- Domain alignment maps to reproducibility/safety/compute; stored under the same key used by the plotters.

## 🔬 Methodological Notes
- Arithmetic aggregation only; no harmonic means.
- Dimensions: Depth, Breadth, Rigor, Innovation, Domain alignment, Info density.
- Coverage = unique term hits / dictionary size (clipped to [0,1]).
- CSV also includes the raw `sources_per_1k` used by your density panels.