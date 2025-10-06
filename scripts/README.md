# Research Evaluation Pipeline

1) Install:
```bash
pip install pandas numpy matplotlib tqdm
```

2) In `scripts/qual_analysis_thesis.py`, set ONLY these lines at the top:
```python
depth_breadth_filename_patterns = ['d1_b1', 'd1_b4', 'd4_b1', 'd4_b4']
model_and_search_pattern = "o3-mini_orkg"   # e.g., "o3_orkg" or "o3-mini_orkg"
topic = "ecology"                           # "ecology" or "nlp"
REPORT_DIR = f'../data/{topic}-reports/orkg-ask/{_model_root}'

# Optional run label
OUTPUT_SUFFIX = "_main"
```

3) Data and Dict
Dictionary check (must exist):
- `scripts/vocab/ecology_dictionaries.json` (for ecology), or
- `scripts/vocab/nlp_dictionaries.json` (for nlp)

If needed adjust Terms inside of groups or weights in there:

...
  "complexity_terms": [
    "nonlinear", "emergent", "synergistic", "interconnected", "complex", "multifaceted"
  ],

  "weights": {
    "alpha": {
      "depth": 0.31,
      "breadth": 0.27,
      "rigor": 0.17,
      "innov": 0.17,
      "gap": 0.08

...

The pipeline expects research documents in the following structure:
```
data/ecology-reports/orkg-ask/o3/
├── 1_o3_orkg_d1_b1.md
├── 1_o3_orkg_d1_b4.md
├── 1_o3_orkg_d4_b1.md
├── 1_o3_orkg_d4_b4.md
├── 2_o3_orkg_d1_b1.md
└── ...
```

4) Run from `scripts/`:
```bash
python qual_analysis_thesis.py
```

5) Outputs will appear in:
```
docs_thesis_{topic}_{model_and_search_pattern}{OUTPUT_SUFFIX}/
├─ figures/
└─ comprehensive_summary_statistics.csv
```

