# thesis-scripts/research_analyzer.py
# Thin batch runner used by qual_analysis_thesis.py (or your own driver scripts).

from __future__ import annotations
import os
from typing import List, Dict
import pandas as pd

from factory import get_analyzer  # robust factory


class ResearchBatchRunner:
    """
    Runs the batch analysis across multiple questions and emits publication figures.
    """
    def __init__(self, report_dir: str, output_dir: str, topic_override: str | None = None, config=None):
        self.report_dir = report_dir
        self.output_dir = output_dir
        self.topic_override = topic_override
        self.config = config

    def run(self, question_numbers: List[str]) -> Dict[str, pd.DataFrame]:
        analyzer = get_analyzer(custom_config=self.config, topic_override=self.topic_override)
        all_results = analyzer.analyze_multiple_questions(self.report_dir, question_numbers, self.output_dir)

        # Path is provided for completeness; current plots consume all_results directly.
        summary_csv = os.path.join(self.output_dir, "comprehensive_summary_statistics.csv")
        analyzer.domain_publication_plots(summary_csv, all_results, os.path.join(self.output_dir, "figures"))
        return all_results
