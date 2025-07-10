# Research Evaluation Pipeline

## 🎯 Overview
The qualitative analysis pipeline evaluates research documents generated
by the deep research system using multiple quality dimensions, including:

- **Research Depth**: Mechanistic detail, causal explanations, temporal precision
- **Research Breadth**: Source diversity, coverage scope, interdisciplinary connections  
- **Ecological Relevance**: Ecosystem services, conservation focus, climate relevance
- **Scientific Rigor**: Statistical analysis, quantitative data, formal citations
- **Content Quality**: Structure, coherence, policy implications

## Pipeline Components

### Core Scripts
- **`qualitative_analysis_pipeline.py`** - Main pipeline orchestrator
- **`research_analyzer.py`** - Core analysis engine with quality metrics
- **`utils.py`** - Shared utilities and configuration

### Visualization Scripts
- **`main_scaling_plot.py`** - Primary scaling effects visualization
- **`parameter_effects_plot.py`** - Individual parameter impact analysis
- **`quality_dimensions_plot.py`** - Multi-dimensional quality assessment
- **`optimization_analysis_plot.py`** - Cost-benefit optimization analysis
- **`overall_quality_analysis.py`** - Comprehensive quality evaluation

### Configuration Files
- **`vocab/ecology_dictionaries.json`** - Domain-specific vocabulary and keywords

## Quick Start

### Prerequisites

Ensure you have the required dependencies installed:
```bash
pip install pandas matplotlib numpy seaborn wordcloud scikit-learn
```

### Basic Usage

1. **Navigate to the scripts directory:**
```bash
cd scripts
```

2. **Run the complete analysis pipeline:**
```bash
python qualitative_analysis_pipeline.py
```

3. **Run individual visualization scripts:**
```bash
python main_scaling_plot.py
python parameter_effects_plot.py
python quality_dimensions_plot.py
```

## Input Requirements

### Data Structure

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

### Configuration Patterns
The pipeline analyzes four depth-breadth configurations:
- **d1_b1**: Low depth, low breadth (efficient)
- **d1_b4**: Low depth, high breadth (broad survey)
- **d4_b1**: High depth, low breadth (deep dive)
- **d4_b4**: High depth, high breadth (comprehensive)

### File Naming Convention
Files must follow the pattern: `{question_num}_o3_orkg_{config}.md`
- `question_num`: Numeric identifier (1, 2, 3, ...)
- `config`: One of d1_b1, d1_b4, d4_b1, d4_b4


## Outputs

### Generated Files

The pipeline creates the following outputs in the `docs/` directory:

#### Analysis Reports
- **`enhanced_analysis_report.md`** - Comprehensive quality analysis
- **`paper_summary.md`** - Academic paper summary
- **`comprehensive_summary_statistics.csv`** - Raw metrics data

#### Visualizations (`docs/figures/`)
- **`main_scaling_effects.png`** - Primary scaling analysis
- **`parameter_effects.png`** - Individual parameter impacts
- **`quality_dimensions.png`** - Quality dimension analysis
- **`optimization_analysis.png`** - Cost-benefit optimization
- **`plot_per_question/`** - Individual question visualizations


## Configuration

### Customizing Analysis
Edit the configuration variables in `qualitative_analysis_pipeline.py`:

```python
# Input directory (relative to scripts/)
REPORT_DIR = '../data/ecology-reports/orkg-ask/o3'

# Output directory
OUTPUT_DIR = 'docs'

# Sample size (None for all questions)
sample_size = 50
```

### Domain Vocabulary
Customize ecology-specific analysis by editing `vocab/ecology_dictionaries.json`:

