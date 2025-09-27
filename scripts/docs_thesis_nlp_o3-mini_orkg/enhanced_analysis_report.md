# Research Quality Analysis (Simplified, Arithmetic)
============================================================

**Domain:** nlp  •  **Model/Search tag:** o3-mini_orkg

## Overview
- Total documents analyzed: **196**
- Questions analyzed: **49**
- Configurations per question: **4** (d1_b1, d1_b4, d4_b1, d4_b4)

## Configuration Performance

### d1_b1
- 📚 Sources: 10.0 ± 0.9
- 📝 Words: 1676 ± 187
- 🔬 Mechanistic coverage: 0.04
- 🔗 Causal coverage: 0.17
- ⏱️ Temporal precision: 0.67
- 📐 Stats rigor coverage: 0.13
- ❓ Uncertainty coverage: 0.07
- 💭 Speculative signals: 0.19
- 💡 Innovation terms coverage: 0.32
- 🧩 Research gaps (signals): 0.00
- 🧭 Tasks coverage: 0.12
- 🗃️ Datasets coverage: 0.00
- 🗣️ Languages coverage: 0.10
- 📊 Eval metrics coverage: 0.15
- 🖥️ Compute terms coverage: 0.06
- 🔁 Reproducibility coverage: 0.03
- ⚠️ Safety coverage: 0.07
- 🖥️ Compute (domain) coverage: 0.06
- ⭐ Overall quality: 0.148
- 🎯 Depth: 0.268
- 🌐 Breadth: 0.084
- 🔬 Rigor: 0.108
- 💡 Innovation: 0.174
- 🧭 Domain alignment: 0.049
- 📊 Info density: 0.121

### d1_b4
- 📚 Sources: 36.0 ± 3.7
- 📝 Words: 1717 ± 184
- 🔬 Mechanistic coverage: 0.06
- 🔗 Causal coverage: 0.17
- ⏱️ Temporal precision: 0.85
- 📐 Stats rigor coverage: 0.12
- ❓ Uncertainty coverage: 0.10
- 💭 Speculative signals: 0.15
- 💡 Innovation terms coverage: 0.33
- 🧩 Research gaps (signals): 0.00
- 🧭 Tasks coverage: 0.14
- 🗃️ Datasets coverage: 0.01
- 🗣️ Languages coverage: 0.13
- 📊 Eval metrics coverage: 0.14
- 🖥️ Compute terms coverage: 0.05
- 🔁 Reproducibility coverage: 0.04
- ⚠️ Safety coverage: 0.09
- 🖥️ Compute (domain) coverage: 0.05
- ⭐ Overall quality: 0.184
- 🎯 Depth: 0.330
- 🌐 Breadth: 0.095
- 🔬 Rigor: 0.114
- 💡 Innovation: 0.158
- 🧭 Domain alignment: 0.055
- 📊 Info density: 0.423

### d4_b1
- 📚 Sources: 31.9 ± 4.5
- 📝 Words: 1680 ± 165
- 🔬 Mechanistic coverage: 0.05
- 🔗 Causal coverage: 0.16
- ⏱️ Temporal precision: 0.85
- 📐 Stats rigor coverage: 0.13
- ❓ Uncertainty coverage: 0.08
- 💭 Speculative signals: 0.10
- 💡 Innovation terms coverage: 0.35
- 🧩 Research gaps (signals): 0.00
- 🧭 Tasks coverage: 0.13
- 🗃️ Datasets coverage: 0.00
- 🗣️ Languages coverage: 0.10
- 📊 Eval metrics coverage: 0.16
- 🖥️ Compute terms coverage: 0.07
- 🔁 Reproducibility coverage: 0.04
- ⚠️ Safety coverage: 0.10
- 🖥️ Compute (domain) coverage: 0.07
- ⭐ Overall quality: 0.177
- 🎯 Depth: 0.322
- 🌐 Breadth: 0.089
- 🔬 Rigor: 0.117
- 💡 Innovation: 0.142
- 🧭 Domain alignment: 0.067
- 📊 Info density: 0.383

### d4_b4
- 📚 Sources: 197.9 ± 24.6
- 📝 Words: 2074 ± 184
- 🔬 Mechanistic coverage: 0.09
- 🔗 Causal coverage: 0.15
- ⏱️ Temporal precision: 0.97
- 📐 Stats rigor coverage: 0.16
- ❓ Uncertainty coverage: 0.12
- 💭 Speculative signals: 0.08
- 💡 Innovation terms coverage: 0.34
- 🧩 Research gaps (signals): 0.00
- 🧭 Tasks coverage: 0.17
- 🗃️ Datasets coverage: 0.01
- 🗣️ Languages coverage: 0.15
- 📊 Eval metrics coverage: 0.19
- 🖥️ Compute terms coverage: 0.10
- 🔁 Reproducibility coverage: 0.05
- ⚠️ Safety coverage: 0.14
- 🖥️ Compute (domain) coverage: 0.10
- ⭐ Overall quality: 0.241
- 🎯 Depth: 0.369
- 🌐 Breadth: 0.120
- 🔬 Rigor: 0.148
- 💡 Innovation: 0.136
- 🧭 Domain alignment: 0.094
- 📊 Info density: 0.998

## 🔍 Key Findings
1. 📈 **Source scaling**: d4_b4 uses 19.8× more sources than d1_b1.
2. 📝 **Content scaling**: d4_b4 has 1.2× more words than d1_b1.
3. 🔄 **Depth effect**: +399% sources.
4. 🌐 **Breadth effect**: +459% sources.

## 🤖 NLP Notes
- Identical aggregation, weights, and density cap as in Ecology for comparability.
- Depth uses architecture/training/ablation as mechanistic proxies; Breadth swaps to tasks/datasets/languages/metrics/compute.
- Domain alignment maps to reproducibility/safety/compute; stored under the same key used by the plotters.

## 🔬 Methodological Notes
- Arithmetic aggregation only; no harmonic means.
- Dimensions: Depth, Breadth, Rigor, Innovation, Domain alignment, Info density.
- Coverage = unique term hits / dictionary size (clipped to [0,1]).
- CSV also includes the raw `sources_per_1k` used by your density panels.