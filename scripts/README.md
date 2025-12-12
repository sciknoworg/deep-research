<div align="center">
     <img src="../scripts/images/logo.png" alt="LLM Judge Logo" width="500"/>
</div>

<div align="center">
 <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</div>

<h2 align="center">LLM-as-a-Judge (LLMJ) Framework</h2>

The **LLM-as-a-Judge** is a robust, Python-based evaluation toolkit designed for objective and configurable analysis of Large Language Model (LLM)-generated research reports. It enables researchers to quantify report quality across key dimensions like `breadth`, `depth`, `rigor`, `gap` and `innovation`.

---

## Usage

LLM-as-a-Judge includes two operation modes:

## Single Report Mode

Use this when you want to evaluate a single markdown (.md) report:

```bash
python llm_judge.py --report "../scripts/test-reports/ecology/1_o3-mini_orkg_d1_b1.md" --topic "ecology" --model "gpt-5-2025-08-07" --out_dir "LLMJ-5-eco-o3-mini"
```

| Argument   | Description                                             |
|------------|---------------------------------------------------------|
| `--report` | Path to the markdown report to be evaluated             |
| `--topic`  | Topic/category of the report (e.g: nlp/ecology)         |
| `--model`  | LLM to be used for scoring                            |
| `--out_dir`| Directory where output files (JSON, CSV, plots) will be saved |


## Batch Mode

Run batch evaluation on all markdown (.md) reports within the specified folder:
```bash
python llm_judge.py --run-batch --folder "../scripts/test-reports/ecology" --topic "ecology" --model "gpt-5-2025-08-07" --out_dir "LLMJ-5-eco-o3-mini"
```

| Argument      | Description                                                                   |
| ------------- | ----------------------------------------------------------------------------- |
| `--run-batch` | Flag indicating batch processing mode (process all files in the folder)       |
| `--folder`    | Path to the folder containing multiple markdown report files                  |
| `--topic`     | Topic/category of the report (e.g: nlp/ecology)                               |
| `--model`     | LLM to be used for scoring                                                  |
| `--out_dir`   | Directory where output files (CSV, plots) for all reports will be saved       |


## Optional Arguments

| Flag          | Description                               |
|---------------|-------------------------------------------|
| `--no-plot`   | Disable plotting and figure generation     |
| `--file_glob` | Override `FILE_GLOB` pattern               |
| `--max_files` | Limit number of reports processed          |
| `--save_prompts` | Store prompts used during evaluation   |

## Example Outputs

Example results for both `single` and `batch` modes are available under: 
```bash
../scripts/LLMJ-5-eco-o3-mini
```
This includes:

- JSON score summaries

- CSV score breakdowns

- Quality dimensions plots

This work is licensed under a [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT).
