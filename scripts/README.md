# ⚖️ LLM-as-a-Judge

LLM as a Judge is a Python-based evaluation framework for analyzing LLM-generated reports. It supports **single-report** and **batchwise** processing, configurable metrics, environment-based settings, and visualizations for comparing evaluation results across configurations.

---

## 📦 Prerequisites

Before running the code, ensure you have:

- **Python 3.9+**
- **Pip**
- **Git**
- **An OpenAI API key** (`OPENAI_API_KEY`)  
- **A Firecrawl API key** (`FIRECRAWL_API_KEY`) — required if your workflow includes Firecrawl scraping or retrieval
- **A synthesized research report**

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sciknoworg/deep-research.git
cd deep-research
```
### 2. Create a virtual environment

```bash
python -m venv venv
```
Activate it:

### macOS/Linux
```bash
source venv/bin/activate
```

### Windows
```bash
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 📁 Project Structure
```bash
deep-research/
├── src/              # Main source code
├── scripts/          # Research evaluation pipeline
├── data/             # Research data and reports
├── requirements.txt  # Python dependencies
└── README.md         # Setup instructions
```


### ⚙️ Configuration
This project supports configuration through a .env file that overrides default settings in the script.

Create a .env file in the project root:

```bash
OPENAI_API_KEY=your-openai-api-key
FIRECRAWL_API_KEY=your-firecrawl-api-key
FIRECRAWL_BASE_URL=https://api.firecrawl.dev/v1
METRICS=depth,breadth,rigor,innovation,gap
CONFIG_ORDER=d1_b1,d1_b4,d4_b1,d4_b4
RESEARCH_PROVIDER=orkg_OR_firecrawl
BAR_FIGSIZE=9,4.5
BATCH_FIGSIZE=16,12
FILE_GLOB=*.md
MAX_FILES=0
SAVE_PROMPTS=false
```
> ⚠️ Do not commit .env to version control.

### 🚀 Usage

### 🔍 Running DeepResearch (Required Before Using LLM-as-a-Judge)

To use `llm_judge.py`, you must first generate a synthesized research report using the DeepResearch framework.

### . Navigate to the DeepResearch folder:

```bash
cd deepresearch
```

### . Run the research generation script:
```bash
python src/main.py
```

### . You will be prompted for inputs, for example:
```bash
Search provider in use: ORKGAskApp
Enter an OpenAI model to use (press Enter to use default 'o3-mini'):
Using model: o3-mini
What would you like to research? What is the best way to restore a degraded peat land?
Enter research breadth (recommended 2–10, default 4):
Enter research depth (recommended 1–5, default 2): 2
Do you want to generate a long report or a specific answer? (report/answer, default report):
```

> 📘 Optional: Get a Research Question from `../data/ecology/49-questions-ecology.csv`

After completion, DeepResearch will generate a `report.md` file.

This file is the input you provide to `llm_judge.py` for scoring and analysis.

The `llm_judge.py` pipeline expects research documents in the following structure:
```
../data/{topic}-reports/orkg-ask/{engine}/
├── 1_o3_orkg_d1_b1.md
├── 1_o3_orkg_d1_b4.md
├── 1_o3_orkg_d4_b1.md
├── 1_o3_orkg_d4_b4.md
└── ...
```
> Here `{engine}` is the generator (o3 or o3-mini). The judge is chosen via MODEL (e.g., gpt-5-2025-08-07 for main results, gpt-5-mini-2025-08-07 for the comparison).

LLM Judge includes two operation modes:

### 1.Single Report Mode

Use this when you want to evaluate a single markdown (.md) report:

```bash
python llm_judge.py --report "../data/ecology/reports/orkg-ask/o3-mini-test/1_o3-mini_orkg_d1_b1.md" --topic "ecology" --model "gpt-5-2025-08-07" --out_dir "./results_single"
```

| Argument   | Description                                             |
|------------|---------------------------------------------------------|
| `--report` | Path to the markdown report to be evaluated             |
| `--topic`  | Topic/category of the report (e.g: nlp/ecology)         |
| `--model`  | LLM model to use for scoring                            |
| `--out_dir`| Directory where output files (JSON, CSV, plots) will be saved |


### . Outputs will appear in:
```bash
"OUT_DIR": "{OUTPUT_DIR}"
├─ scores_only.json            # contains the JSON-formatted metric scores for the report
├─ repo_compatible_row.csv                 # report scores (0..1) 
├─ figures/quality_dimensions.png        # a plot showing metric distributions or quality dimensions
```

### 2. Batch Mode

Runs evaluation on all matching files in a folder:
```bash
python llm_judge.py --run-batch --folder "../data/ecology/reports/orkg-ask/o3-mini-test" --topic "ecology" --model "gpt-5" --out_dir "./results_batch""
```

| Argument      | Description                                                                   |
| ------------- | ----------------------------------------------------------------------------- |
| `--run-batch` | Flag indicating batch processing mode (process all files in the folder)       |
| `--folder`    | Path to the folder containing multiple report markdown files                  |
| `--topic`     | Topic/category of the report (e.g: nlp/ecology)                               |
| `--model`     | LLM model to use for scoring                                                  |
| `--out_dir`   | Directory where output files (CSV, plots) for all reports will be saved       |


### . Outputs will appear in:
```bash
"OUT_DIR": "{OUTPUT_DIR}"
├─ quality_dimensions.png            # 6 panels (Depth, Breadth, Rigor, Innovation, Gap, Overall)
├─ batch_reports.csv                 # per-report scores (0..1) + config + path
├─ batch_config_summary.csv          # means/std per config in fixed order
```
### Additional (Optional) Flags

| Flag          | Description                               |
|---------------|-------------------------------------------|
| `--no-plot`   | Disable plotting and figure generation     |
| `--file_glob` | Override `FILE_GLOB` pattern               |
| `--max_files` | Limit number of reports processed          |
| `--save_prompts` | Store prompts used during evaluation   |

## 📝 Example Runs

The outputs from the folder `data/ecology/reports/orkg-ask/o3-mini-test` are already generated for both **single** and **batchwise** pipeline and available in `scripts/LLMJ-5-eco-o3-mini`.

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/new-feature
```
3. Commit your changes with clear messages:
```bash
git commit -m "Add new feature"
```
4. Push to GitHub:
```bash
git push origin feature/new-feature
```
5. Open a Pull Request

### License
This project is licensed under the [MIT License](../LICENSE).
