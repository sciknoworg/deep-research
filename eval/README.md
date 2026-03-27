<div align="center">
     <img src="../eval/images/logo.png" alt="LLM Judge Logo" width="500"/>
</div>

<div align="center">
 <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</div>

<h2 align="center">LLM-as-a-Judge (LLMJ) Framework</h2>

The **LLM-as-a-Judge** is a robust, Python-based evaluation toolkit designed for objective and configurable analysis of Large Language Model (LLM)-generated research reports. It enables researchers to quantify report quality across key dimensions like `breadth`, `depth`, `rigor`, `gap` and `innovation`, with pointwise rubrics implemented via **[YESciEval](https://yescieval.readthedocs.io/)** — a framework for scientific evaluation of LLM outputs.

---

## Usage

LLM-as-a-Judge includes two operation modes: **Single Evaluation** and **Batch Evaluation**. Each domain (`nlp` and `ecology`) has a dedicated notebook for each mode.

## Notebooks

The directory contains 4 notebooks — 2 per domain:

| Domain | Mode | Notebook |
|--------|------|----------|
| NLP | Single Evaluation | `evaluation_single_report_nlp.ipynb` |
| NLP | Batch Evaluation | `evaluation_batch_reports_nlp.ipynb` |
| Ecology | Single Evaluation | `evaluation_single_report_ecology.ipynb` |
| Ecology | Batch Evaluation | `evaluation_batch_reports_ecology.ipynb` |

---

## Single Evaluation Mode

Use the single evaluation notebook when you want to evaluate one markdown (`.md`) report at a time.

### Steps

1. Open the relevant notebook for your domain:
   - **NLP:** `evaluation_single_report_nlp.ipynb`
   - **Ecology:** `evaluation_single_report_ecology.ipynb`

2. Set the following parameters in the configuration cell:

   | Parameter | Description |
   |-----------|-------------|
   | `REPORT_PATH` | Path to the markdown report to be evaluated |
   | `DOMAIN` | Topic/domain of the report (e.g. `nlp` / `ecology`) |
   | `MODEL_ID` | LLM to be used for scoring |
   | `OUTPUT_DIR` | Directory where output files (JSON, CSV, plots) will be saved |
   | `QUESTIONS_CSV` | Path to the CSV file containing evaluation questions |
   | `DEVICE` | Compute device to use for evaluation (e.g. `cpu` / `cuda`) |

3. Run all cells sequentially.

---

## Batch Evaluation Mode

Use the batch evaluation notebook to evaluate all markdown (`.md`) reports within a specified folder.

### Steps

1. Open the relevant notebook for your domain:
   - **NLP:** `evaluation_batch_reports_nlp.ipynb`
   - **Ecology:** `evaluation_batch_reports_ecology.ipynb`

2. Set the following parameters in the configuration cell:

   | Parameter | Description |
   |-----------|-------------|
   | `REPORTS_DIR` | Path to the folder containing multiple markdown report files |
   | `DOMAIN` | Topic/domain of the reports (e.g. `nlp` / `ecology`) |
   | `MODEL_ID` | LLM to be used for scoring |
   | `OUTPUT_DIR` | Directory where output files (CSV, plots) for all reports will be saved |
   | `QUESTIONS_CSV` | Path to the CSV file containing evaluation questions |
   | `DEVICE` | Compute device to use for evaluation (e.g. `cpu` / `cuda`) |

3. Run all cells sequentially.

---


This work is licensed under a [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT).
