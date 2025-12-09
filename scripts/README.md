# Research Evaluation Pipeline

# Dict based eval:

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

# LLM Judge based eval:

1) Install:
```bash
pip install numpy matplotlib
```

2) In scripts/judge_batch.py, set ONLY these lines at the top:

```python
SETTINGS = {
  "FOLDER": "../data/ecology-reports/orkg-ask/o3",  # input with *.md reports (generator = o3 or o3-mini)
  "OUT_DIR": "LLMJ-5-eco-o3",                       # output folder name
  "TOPIC": "ecology",                               # "ecology" or "nlp" (or None to auto-detect)
  "MODEL": "gpt-5-2025-08-07",                      # judge: GPT-5 (use *-mini for the comparison runs)
  "FILE_GLOB": "*.md",                              # use "**/*.md" for recursive folders if needed
  "MAX_FILES": 0,                                   # 0 = all files
  "SAVE_PROMPTS": False,                            # True = store system+user prompts per metric
  "FIGSIZE": (16, 12),
}
# Fixed in the script:
# METRICS = ["depth", "breadth", "rigor", "innovation", "gap"]
# CONFIG_ORDER = ["d1_b1", "d1_b4", "d4_b1", "d4_b4"]
```

3) Data and filenames:

Use the same report folders as for the dict eval; filenames must contain a config tag:
../data/{topic}-reports/orkg-ask/{engine}/
├── 1_o3_orkg_d1_b1.md
├── 1_o3_orkg_d1_b4.md
├── 1_o3_orkg_d4_b1.md
├── 1_o3_orkg_d4_b4.md
└── ...

Here {engine} is the generator (o3 or o3-mini). The judge is chosen via MODEL (e.g., gpt-5-2025-08-07 for main results, gpt-5-mini-2025-08-07 for the comparison).
Each metric call returns a strict JSON integer in [0,100] (no sampling, no free text); the script rescales to [0,1] and computes a local overall as the mean of the five dimensions.

4) Run from scripts/ or adjust in File as reffered in 2):

# Examples:

# Ecology, generator=o3, judge=GPT-5 (main results)
python llmj_batch.py --folder "../data/ecology-reports/orkg-ask/o3" --topic ecology \
  --model "gpt-5-2025-08-07" --out_dir "LLMJ-5-eco-o3"

# Ecology, generator=o3-mini, judge=GPT-5
python llmj_batch.py --folder "../data/ecology-reports/orkg-ask/o3-mini" --topic ecology \
  --model "gpt-5-2025-08-07" --out_dir "LLMJ-5-eco-o3-mini"

# NLP, generator=o3, judge=GPT-5
python llmj_batch.py --folder "../data/nlp-reports/orkg-ask/o3" --topic nlp \
  --model "gpt-5-2025-08-07" --out_dir "LLMJ-5-nlp-o3"

# (Optional judge comparison) NLP, generator=o3, judge=GPT-5-mini
python llmj_batch.py --folder "../data/nlp-reports/orkg-ask/o3" --topic nlp \
  --model "gpt-5-mini-2025-08-07" --out_dir "LLMJ-5-mini-nlp-o3"

5) Outputs will appear in:

"OUT_DIR": "LLMJ-5-eco-o3/"
├─ quality_dimensions.png            # 6 panels (Depth, Breadth, Rigor, Innovation, Gap, Overall)
├─ batch_reports.csv                 # per-report scores (0..1) + config + path
├─ batch_config_summary.csv          # means/std per config in fixed order
└─ <one folder per report>/scores.csv  # +/prompts/*.json if SAVE_PROMPTS=True

