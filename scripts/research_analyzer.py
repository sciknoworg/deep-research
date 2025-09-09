# research_analyzer_fixed.py
# -------------------------------------------
# DeepResearch qualitative analysis (fixed)
# -------------------------------------------
# What changed vs. the original:
# - scoring_mode="coverage" by default (true normalization by vocabulary size).
#   Use scoring_mode="saturation" to reproduce the old behavior (occurrences / caps).
# - all saturation thresholds (caps) are configurable via `caps={...}`.
# - aggregation uses D_ij alignment (common question IDs across all configs) to avoid bias.
# - comments added at the relevant places to clarify design choices and paper-code differences.

import os
import re
import warnings
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

try:
    import nltk
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

# Project-local imports
from utils import (
    depth_breadth_filename_patterns,
    model_and_search_pattern,
    load_domain_vocab,
)
from main_scaling_plot import create_main_scaling_plot
from optimization_analysis_plot import create_optimization_analysis_plot
from overall_quality_analysis import create_overall_quality_analysis
from parameter_effects_plot import create_parameter_effects_plot
from quality_dimensions_plot import create_quality_dimensions_plot

warnings.filterwarnings("ignore")

# Plot style: consistent look-and-feel for figures
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update(
    {
        "font.size": 12,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.titlesize": 16,
        "font.family": "serif",
        "text.usetex": False,  # set True only if LaTeX is installed
    }
)

if NLTK_AVAILABLE:
    # Optional: keep the pipeline runnable even without NLTK
    try:
        nltk.download("punkt", quiet=True)
        nltk.download("stopwords", quiet=True)
    except Exception:
        pass


# -----------------------
# Weights for aggregation
# -----------------------
@dataclass
class QualityWeights:
    depth: float = 0.22
    breadth: float = 0.20
    rigor: float = 0.18
    innovation: float = 0.15
    ecological: float = 0.12
    info_density: float = 0.08
    taxonomic: float = 0.05


class DeepResearchAnalyzer:
    """
    Analyzer for DeepResearch markdown reports.

    Key choices:
    - scoring_mode:
        "coverage"   -> unique hits / vocabulary size  (true normalization; matches paper prose)
        "saturation" -> (unique or occurrence) / cap τ, clamped to [0,1]  (matches the original code)
    - caps: per-metric saturation thresholds (τ) used when scoring_mode="saturation".
    - use_alignment: when aggregating across configs, enforce D_ij = intersection of question IDs.
                     This avoids bias if a config is missing some questions.
    """

    def __init__(
        self,
        scoring_mode: str = "coverage",
        caps: Optional[Dict[str, float]] = None,
        use_alignment: bool = True,
    ):
        self.documents: Dict[str, Dict] = {}
        self.metrics: Dict[str, Dict] = {}
        self.vocab = load_domain_vocab()
        self.weights = QualityWeights()

        # Mode: "coverage" (default) or "saturation"
        assert scoring_mode in {"coverage", "saturation"}
        self.scoring_mode = scoring_mode
        self.use_alignment = use_alignment

        # Default caps (τ) for saturation mode; can be overridden by `caps`
        default_caps: Dict[str, float] = {
            # Depth components
            "mech": 20.0,     # mechanistic detail (occurrences) cap
            "causal": 10.0,   # causal explanations (occurrences) cap
            # Breadth components (unique presence caps)
            "regions": 8.0,
            "interventions": 12.0,
            "diversity": 8.0,
            "services": 10.0,
            "scales": 6.0,
            # Rigor
            "rigor_stats": 5.0,
            "rigor_cites": 20.0,
            "rigor_unc": 5.0,
            # Innovation (each subcomponent shares one cap)
            "innov_each": 3.0,
            # Information density (sources per 1000 words)
            "info_density_per_k": 50.0,
            # Taxonomic sophistication
            "taxonomic": 10.0,
        }
        self.caps: Dict[str, float] = {**default_caps, **(caps or {})}

    # ----------------------
    # Document I/O & parsing
    # ----------------------
    def load_document(self, filename: str, content: str) -> None:
        """
        Parse depth/breadth from filename (e.g., '14_o3_orkg_d4_b1.md') and load the content.
        Keys are 'd{depth}_b{breadth}' (safe because we reset per question).
        """
        match = re.search(r"d(\d+)_b(\d+)", filename)
        if match:
            depth = int(match.group(1))
            breadth = int(match.group(2))
            key = f"d{depth}_b{breadth}"
            self.documents[key] = {
                "filename": filename,
                "depth": depth,
                "breadth": breadth,
                "content": content,
            }

    # -------------------
    # Metric computations
    # -------------------
    def _count_unique_hits(self, text: str, terms) -> int:
        """Unique presence count over a vocabulary (coverage semantics)."""
        text_l = text.lower()
        return sum(1 for t in terms if t.lower() in text_l)

    def _count_occurrences(self, text: str, terms) -> int:
        """Occurrence count over a vocabulary (saturation semantics for depth signals)."""
        tl = text.lower()
        return sum(tl.count(t.lower()) for t in terms)

    def extract_mechanistic_detail(self, content: str) -> int:
        """
        Mechanistic detail:
        - coverage mode   -> UNIQUE hits across mechanistic_terms
        - saturation mode -> OCCURRENCES across mechanistic_terms
        """
        terms = self.vocab["mechanistic_terms"]
        return (
            self._count_unique_hits(content, terms)
            if self.scoring_mode == "coverage"
            else self._count_occurrences(content, terms)
        )

    @staticmethod
    def extract_temporal_precision(content: str) -> float:
        """
        Temporal precision in [0,1]: specific / (specific + vague).
        Specific patterns: years, ranges, explicit durations.
        Vague terms: 'recently', 'long-term', ...
        """
        specific_patterns = [
            r"\d+(?:\.\d+)?(?:\s*[-–]\s*\d+(?:\.\d+)?)?\s*(?:yr|year|month|week|day|hour|decade|century)",
            r"(?:within|after|before)\s+\d+\s+(?:yr|year|month|week|day)",
            r"(?:every|each)\s+\d+\s+(?:yr|year|month|week|day)",
            r"\d{4}(?:\s*[-–]\s*\d{4})?(?:\s+(?:AD|BC|CE|BCE))?",
            r"(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}",
        ]
        vague_terms = [
            "recently",
            "historically",
            "traditionally",
            "formerly",
            "previously",
            "short-term",
            "long-term",
            "medium-term",
            "near-term",
            "early",
            "late",
            "mid-",
            "recent",
            "ancient",
            "modern",
            "soon",
            "eventually",
            "ultimately",
            "initially",
            "finally",
            "temporary",
            "permanent",
            "occasional",
            "frequent",
            "rare",
        ]
        text = content.lower()
        specific_count = 0
        for pattern in specific_patterns:
            specific_count += len(re.findall(pattern, text))
        vague_count = sum(text.count(term) for term in vague_terms)
        return specific_count / max(1, specific_count + vague_count)

    @staticmethod
    def extract_temporal_references(content: str) -> int:
        """Count explicit temporal references like '10 yr', '5 year', '2 decade'."""
        return len(re.findall(r"\d+[\s-]+(?:yr|year|decade)", content))

    def extract_diversity_dimensions(self, content: str) -> int:
        """Unique presence over diversity_dimensions (coverage-like)."""
        return self._count_unique_hits(content, self.vocab["diversity_dimensions"])

    @staticmethod
    def extract_source_count(content: str) -> int:
        """Unique URL count (used by Information Density)."""
        sources = re.findall(r"https?://[^\s\)]+", content)
        return len(set(sources))

    def extract_metrics(self) -> None:
        """
        Compute all raw signals from each document.
        Mix of:
        - coverage-like (unique presence) counts for breadth-ish signals,
        - occurrence-like counts for depth-ish signals in saturation mode,
        - regex-based structural metrics (URLs, citations, percentages, taxonomic italics).
        """
        for key, doc in self.documents.items():
            content = doc["content"]
            text_l = content.lower()
            metrics: Dict[str, float] = {}

            # Basic
            metrics["word_count"] = len(content.split())
            metrics["char_count"] = len(content)
            metrics["source_count"] = self.extract_source_count(content)

            # Coverage & scope
            metrics["geographic_regions"] = self._count_unique_hits(
                content, self.vocab["regions"]
            )
            metrics["intervention_types"] = self._count_unique_hits(
                content, self.vocab["interventions"]
            )
            metrics["diversity_dimensions"] = self.extract_diversity_dimensions(content)
            metrics["ecosystem_services"] = self._count_unique_hits(
                content, self.vocab["ecosystem_services"]
            )
            metrics["spatial_scales"] = self._count_unique_hits(
                content, self.vocab["scale_terms"]
            )

            # Temporal
            metrics["temporal_references"] = self.extract_temporal_references(content)
            metrics["temporal_precision"] = self.extract_temporal_precision(content)

            # Depth signals
            metrics["mechanistic_detail"] = self.extract_mechanistic_detail(content)
            if self.scoring_mode == "coverage":
                metrics["causal_explanations"] = self._count_unique_hits(
                    content, self.vocab["causal_terms"]
                )
            else:
                metrics["causal_explanations"] = self._count_occurrences(
                    content, self.vocab["causal_terms"]
                )

            # Research quality signals
            metrics["research_gaps"] = (
                text_l.count("research gap")
                + text_l.count("knowledge gap")
                + text_l.count("data gap")
            )
            metrics["speculative_ideas"] = (
                text_l.count("speculative") + text_l.count("flagged") + text_l.count("hypothetical")
            )
            metrics["uncertainty_acknowledgment"] = (
                text_l.count("uncertain") + text_l.count("unclear") + text_l.count("unknown")
            )
            metrics["hypothesis_testing"] = (
                text_l.count("hypothesis") + text_l.count("test") + text_l.count("experiment")
            )

            # Trade-offs & policy
            metrics["tradeoff_mentions"] = (
                text_l.count("trade-off") + text_l.count("tradeoff") + text_l.count("balance")
            )
            metrics["policy_mentions"] = (
                text_l.count("policy") + text_l.count("subsidy") + text_l.count("regulation")
            )

            # Quant / stats rigor
            metrics["percentage_values"] = len(re.findall(r"\d+\.?\d*\s*%", content))
            metrics["statistical_rigor"] = self._count_occurrences(
                content, self.vocab["stats_terms"]
            )

            # Structure & citations
            metrics["section_count"] = len(content.split("\n## "))
            metrics["formal_citations"] = len(re.findall(r"\([^)]*\d{4}[^)]*\)", content))

            # Taxonomic specificity: *Genus species*
            species_patterns = re.findall(r"\*[A-Z][a-z]+ [a-z]+\*", content)
            metrics["taxonomic_specificity"] = len(species_patterns)

            # Ecology topicality
            metrics["innovation_indicators"] = self._count_occurrences(
                content, self.vocab["innovation_terms"]
            )
            metrics["conservation_focus"] = self._count_occurrences(
                content, self.vocab["conservation_terms"]
            )
            metrics["climate_relevance"] = self._count_occurrences(
                content, self.vocab["climate_terms"]
            )
            metrics["ecological_complexity"] = self._count_occurrences(
                content, self.vocab["complexity_terms"]
            )

            self.metrics[key] = metrics

    # -----------------
    # Score computation
    # -----------------
    def _depth_score(self, m: Dict[str, float]) -> float:
        """Depth = mechanistic + causal + temporal precision."""
        if self.scoring_mode == "coverage":
            mech_den = max(1, len(self.vocab["mechanistic_terms"]))
            causal_den = max(1, len(self.vocab["causal_terms"]))
            return (
                min(m["mechanistic_detail"] / mech_den, 1.0) * 0.4
                + min(m["causal_explanations"] / causal_den, 1.0) * 0.3
                + m["temporal_precision"] * 0.3
            )
        # saturation (original semantics)
        return (
            min(m["mechanistic_detail"] / self.caps["mech"], 1.0) * 0.4
            + min(m["causal_explanations"] / self.caps["causal"], 1.0) * 0.3
            + m["temporal_precision"] * 0.3
        )

    def _breadth_score(self, m: Dict[str, float]) -> float:
        """Breadth = regions + interventions + diversity + services + scales."""
        if self.scoring_mode == "coverage":
            reg_den = max(1, len(self.vocab["regions"]))
            int_den = max(1, len(self.vocab["interventions"]))
            div_den = max(1, len(self.vocab["diversity_dimensions"]))
            serv_den = max(1, len(self.vocab["ecosystem_services"]))
            scale_den = max(1, len(self.vocab["scale_terms"]))
            return (
                min(m["geographic_regions"] / reg_den, 1.0) * 0.25
                + min(m["intervention_types"] / int_den, 1.0) * 0.25
                + min(m["diversity_dimensions"] / div_den, 1.0) * 0.25
                + min(m["ecosystem_services"] / serv_den, 1.0) * 0.15
                + min(m["spatial_scales"] / scale_den, 1.0) * 0.10
            )
        # saturation (original semantics)
        return (
            min(m["geographic_regions"] / self.caps["regions"], 1.0) * 0.25
            + min(m["intervention_types"] / self.caps["interventions"], 1.0) * 0.25
            + min(m["diversity_dimensions"] / self.caps["diversity"], 1.0) * 0.25
            + min(m["ecosystem_services"] / self.caps["services"], 1.0) * 0.15
            + min(m["spatial_scales"] / self.caps["scales"], 1.0) * 0.10
        )

    def _rigor_score(self, m: Dict[str, float]) -> float:
        """Rigor uses caps by design (no natural |V|)."""
        return (
            min(m["statistical_rigor"] / self.caps["rigor_stats"], 1.0) * 0.4
            + min(m["formal_citations"] / self.caps["rigor_cites"], 1.0) * 0.4
            + min(m["uncertainty_acknowledgment"] / self.caps["rigor_unc"], 1.0) * 0.2
        )

    def _innovation_score(self, m: Dict[str, float]) -> float:
        """Innovation uses a shared cap τ for its three subcomponents."""
        c = self.caps["innov_each"]
        return (
            min(m["speculative_ideas"] / c, 1.0) * 0.4
            + min(m["innovation_indicators"] / c, 1.0) * 0.3
            + min(m["research_gaps"] / c, 1.0) * 0.3
        )

    def _info_density(self, m: Dict[str, float]) -> float:
        """Information Density = min( sources_per_1000 / τ, 1 )."""
        per_k = m["source_count"] / max(1.0, m["word_count"] / 1000.0)
        return min(per_k / self.caps["info_density_per_k"], 1.0)

    def _taxonomic_score(self, m: Dict[str, float]) -> float:
        """Taxonomic precision: *Genus species* hits capped by τ."""
        return min(m["taxonomic_specificity"] / self.caps["taxonomic"], 1.0)

    def _ecological_relevance(self, m: Dict[str, float]) -> float:
        """Ecological topicality = conservation + climate + complexity (with caps)."""
        return (
            min(m["conservation_focus"] / self.caps["regions"], 1.0) * 0.4  # reuse cap scale ~8
            + min(m["climate_relevance"] / 6.0, 1.0) * 0.3                   # keep prior scale for stability
            + min(m["ecological_complexity"] / 5.0, 1.0) * 0.3
        )

    def calculate_quality_scores(self) -> None:
        """Compute all composite scores and overall quality for each document."""
        for key, m in self.metrics.items():
            depth = self._depth_score(m)
            breadth = self._breadth_score(m)
            rigor = self._rigor_score(m)
            innovation = self._innovation_score(m)
            info_d = self._info_density(m)
            taxon = self._taxonomic_score(m)
            eco = self._ecological_relevance(m)

            w = self.weights
            overall = (
                depth * w.depth
                + breadth * w.breadth
                + rigor * w.rigor
                + innovation * w.innovation
                + eco * w.ecological
                + info_d * w.info_density
                + taxon * w.taxonomic
            )

            m.update(
                {
                    "depth_score": depth,
                    "breadth_score": breadth,
                    "rigor_score": rigor,
                    "innovation_score": innovation,
                    "ecological_relevance": eco,
                    "info_density": info_d,
                    "taxonomic_score": taxon,
                    "overall_quality": overall,
                }
            )

    # ---------------------------
    # Batch analysis and plotting
    # ---------------------------
    def analyze_multiple_questions(
        self, report_dir: str, question_numbers, output_dir: str
    ) -> Dict[int, pd.DataFrame]:
        """
        For each question ID:
          - load up to 4 configs (d1_b1, d1_b4, d4_b1, d4_b4),
          - extract metrics and compute scores,
          - generate per-question visualization,
          - collect a row per config for aggregation.
        Returns a dict: {question_id: DataFrame}
        """
        os.makedirs(output_dir, exist_ok=True)
        per_question: Dict[int, pd.DataFrame] = {}

        for qid in question_numbers:
            # Reset per-question containers to avoid key collisions
            self.documents, self.metrics = {}, {}

            loaded = 0
            for cfg in depth_breadth_filename_patterns:
                fname = f"{qid}_{model_and_search_pattern}_{cfg}.md"
                path = os.path.join(report_dir, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    self.load_document(fname, content)
                    loaded += 1
                except FileNotFoundError:
                    print(f"[WARN] File not found: {fname}")

            if loaded == 0:
                continue

            # Extract and score
            self.extract_metrics()
            self.calculate_quality_scores()

            # Per-question plot
            os.makedirs(f"{output_dir}/plot_per_question", exist_ok=True)
            fig, df = self.create_visualizations()
            fig.savefig(
                f"{output_dir}/plot_per_question/question_{qid}_analysis.png",
                dpi=300,
                bbox_inches="tight",
            )
            plt.close(fig)

            # Add bookkeeping columns for aggregation
            df["config"] = [f"d{self.documents[k]['depth']}_b{self.documents[k]['breadth']}" for k in df.index]
            df["question"] = qid
            per_question[qid] = df

            print(f"[INFO] Analyzed question {qid} with {loaded} document(s).")

        if per_question:
            self._save_comprehensive_summary_statistics(per_question, output_dir)

        return per_question

    def _save_comprehensive_summary_statistics(
        self, all_results: Dict[int, pd.DataFrame], output_dir: str
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Concatenate per-question frames and compute summary stats by config.
        If use_alignment=True, enforce D_ij: only keep questions present in ALL configs.
        Saves: comprehensive_summary_statistics.csv
        Returns: (combined_df, summary_stats)
        """
        combined_df = pd.concat(all_results.values(), ignore_index=True)

        # --- D_ij alignment (recommended by paper) ---
        if self.use_alignment:
            configs = combined_df["config"].unique().tolist()
            if configs:
                qs_by_cfg = {
                    c: set(combined_df.loc[combined_df["config"] == c, "question"]) for c in configs
                }
                common_qs = set.intersection(*qs_by_cfg.values()) if qs_by_cfg else set()
                if common_qs:
                    before = len(combined_df)
                    combined_df = combined_df[combined_df["question"].isin(common_qs)].copy()
                    after = len(combined_df)
                    print(
                        f"[INFO] D_ij alignment applied: kept {len(common_qs)} common questions; "
                        f"rows {before} -> {after}."
                    )

        # Group and summarize
        summary_stats = (
            combined_df.groupby("config")
            .agg(
                {
                    # Basic
                    "source_count": ["mean", "std", "min", "max"],
                    "word_count": ["mean", "std", "min", "max"],
                    "char_count": ["mean", "std"],
                    # Coverage / scope
                    "geographic_regions": ["mean", "std"],
                    "intervention_types": ["mean", "std"],
                    "diversity_dimensions": ["mean", "std"],
                    "ecosystem_services": ["mean", "std"],
                    "spatial_scales": ["mean", "std"],
                    # Temporal
                    "temporal_references": ["mean", "std"],
                    "temporal_precision": ["mean", "std"],
                    # Depth
                    "mechanistic_detail": ["mean", "std"],
                    "causal_explanations": ["mean", "std"],
                    # Quality
                    "research_gaps": ["mean", "std"],
                    "speculative_ideas": ["mean", "std"],
                    "uncertainty_acknowledgment": ["mean", "std"],
                    "tradeoff_mentions": ["mean", "std"],
                    # Quant / stats
                    "percentage_values": ["mean", "std"],
                    "statistical_rigor": ["mean", "std"],
                    "formal_citations": ["mean", "std"],
                    # Ecology topicality
                    "conservation_focus": ["mean", "std"],
                    "climate_relevance": ["mean", "std"],
                    "ecological_complexity": ["mean", "std"],
                    # Taxonomy
                    "taxonomic_specificity": ["mean", "std"],
                    # Scores
                    "overall_quality": ["mean", "std"],
                    "depth_score": ["mean", "std"],
                    "breadth_score": ["mean", "std"],
                    "rigor_score": ["mean", "std"],
                    "innovation_score": ["mean", "std"],
                    "ecological_relevance": ["mean", "std"],
                    "info_density": ["mean", "std"],
                    "taxonomic_score": ["mean", "std"],
                }
            )
            .round(3)
        )

        # Flatten MultiIndex columns
        summary_stats.columns = ["_".join(col).strip() for col in summary_stats.columns.values]
        out_csv = os.path.join(output_dir, "comprehensive_summary_statistics.csv")
        summary_stats.to_csv(out_csv)
        print(f"[INFO] Wrote summary: {out_csv}")

        return combined_df, summary_stats

    # -----------------
    # Publication plots
    # -----------------
    @staticmethod
    def create_publication_plots(statistics_file: str, all_results, figures_dir: str) -> None:
        """Generate the same publication-ready plots used in the paper."""
        create_main_scaling_plot(statistics_file, figures_dir)
        create_parameter_effects_plot(statistics_file, figures_dir)
        create_optimization_analysis_plot(all_results, figures_dir)
        create_quality_dimensions_plot(all_results, figures_dir)
        create_overall_quality_analysis(all_results, figures_dir)

    # ------------------
    # Per-question plots
    # ------------------
    def create_visualizations(self):
        """
        Build a 4x3 panel with heatmaps/bars/scatter for the current question (up to 4 configs).
        Returns: (fig, df_with_metrics)
        """
        df = pd.DataFrame(self.metrics).T
        df["depth"] = [self.documents[k]["depth"] for k in df.index]
        df["breadth"] = [self.documents[k]["breadth"] for k in df.index]

        fig = plt.figure(figsize=(20, 16))

        # 1. Word count
        ax1 = plt.subplot(4, 3, 1)
        hm1 = df.pivot_table(index="depth", columns="breadth", values="word_count")
        sns.heatmap(hm1, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax1)
        ax1.set_title("Word Count by Depth and Breadth")

        # 2. Source count
        ax2 = plt.subplot(4, 3, 2)
        hm2 = df.pivot_table(index="depth", columns="breadth", values="source_count")
        sns.heatmap(hm2, annot=True, fmt=".0f", cmap="Blues", ax=ax2)
        ax2.set_title("Source Count by Depth and Breadth")

        # 3. Geographic coverage
        ax3 = plt.subplot(4, 3, 3)
        hm3 = df.pivot_table(index="depth", columns="breadth", values="geographic_regions")
        sns.heatmap(hm3, annot=True, fmt=".0f", cmap="Greens", ax=ax3)
        ax3.set_title("Geographic Regions Covered")

        # 4. Mechanistic detail
        ax4 = plt.subplot(4, 3, 4)
        hm4 = df.pivot_table(index="depth", columns="breadth", values="mechanistic_detail")
        sns.heatmap(hm4, annot=True, fmt=".0f", cmap="Oranges", ax=ax4)
        ax4.set_title("Mechanistic Detail")

        # 5. Complexity scatter (size ~ sources)
        ax5 = plt.subplot(4, 3, 5)
        scatter = ax5.scatter(
            df["mechanistic_detail"],
            df["temporal_references"],
            s=df["source_count"] / 10,
            alpha=0.7,
            c=df["depth"] + df["breadth"],
            cmap="viridis",
        )
        ax5.set_xlabel("Mechanistic Detail")
        ax5.set_ylabel("Temporal References")
        ax5.set_title("Document Complexity (size = sources)")
        for idx, row in df.iterrows():
            ax5.annotate(idx, (row["mechanistic_detail"], row["temporal_references"]), fontsize=8)

        # 6. Research quality (gaps + speculative + tradeoff)
        ax6 = plt.subplot(4, 3, 6)
        quality_score = df["research_gaps"] + df["speculative_ideas"] + df["tradeoff_mentions"]
        if len(quality_score) == 4:
            hm6 = quality_score.values.reshape(2, 2)
            sns.heatmap(hm6, annot=True, fmt=".0f", cmap="Purples", ax=ax6, xticklabels=[1, 4], yticklabels=[1, 4])
            ax6.set_xlabel("Breadth")
            ax6.set_ylabel("Depth")
        else:
            ax6.bar(df.index, quality_score, color="purple", alpha=0.7)
            ax6.set_xlabel("Configuration")
            ax6.set_ylabel("Quality Score")
            ax6.tick_params(axis="x", rotation=45)
        ax6.set_title("Research Quality Score")

        # 7. Quantitative density: % per 1k words
        ax7 = plt.subplot(4, 3, 7)
        q_density = df["percentage_values"] / (df["word_count"] / 1000)
        ax7.bar(df.index, q_density, color=["lightblue", "lightgreen", "orange", "red"])
        ax7.set_ylabel("Percentage Values per 1000 Words")
        ax7.set_title("Quantitative Information Density")
        ax7.tick_params(axis="x", rotation=45)

        # 8. Policy relevance
        ax8 = plt.subplot(4, 3, 8)
        policy_score = df["policy_mentions"] + df["tradeoff_mentions"]
        if len(policy_score) == 4:
            hm8 = policy_score.values.reshape(2, 2)
            sns.heatmap(hm8, annot=True, fmt=".0f", cmap="RdYlBu", ax=ax8, xticklabels=[1, 4], yticklabels=[1, 4])
            ax8.set_xlabel("Breadth")
            ax8.set_ylabel("Depth")
        else:
            ax8.bar(df.index, policy_score, color="blue", alpha=0.7)
            ax8.set_xlabel("Configuration")
            ax8.set_ylabel("Policy Score")
            ax8.tick_params(axis="x", rotation=45)
        ax8.set_title("Policy Relevance Score")

        # 9. Diversity dimensions
        ax9 = plt.subplot(4, 3, 9)
        df_sorted = df.sort_values("diversity_dimensions")
        ax9.barh(
            df_sorted.index,
            df_sorted["diversity_dimensions"],
            color=["lightblue", "lightgreen", "orange", "red"],
        )
        ax9.set_xlabel("Number of Diversity Dimensions")
        ax9.set_title("Diversity Dimension Coverage")

        # 10. Intervention types
        ax10 = plt.subplot(4, 3, 10)
        hm10 = df.pivot_table(index="depth", columns="breadth", values="intervention_types")
        sns.heatmap(hm10, annot=True, fmt=".0f", cmap="Reds", ax=ax10)
        ax10.set_title("Intervention Types Covered")

        # 11. Temporal references
        ax11 = plt.subplot(4, 3, 11)
        hm11 = df.pivot_table(index="depth", columns="breadth", values="temporal_references")
        sns.heatmap(hm11, annot=True, fmt=".0f", cmap="Greys", ax=ax11)
        ax11.set_title("Temporal References")

        # 12. Normalized comparison
        ax12 = plt.subplot(4, 3, 12)
        metrics_to_compare = ["source_count", "geographic_regions", "mechanistic_detail", "diversity_dimensions"]
        x_pos = np.arange(len(df))
        width = 0.2
        for i, metric in enumerate(metrics_to_compare):
            vals = df[metric].astype(float)
            norm_vals = vals / max(vals.max(), 1.0)
            ax12.bar(x_pos + i * width, norm_vals, width, label=metric.replace("_", " ").title())
        ax12.set_xlabel("Configuration")
        ax12.set_ylabel("Normalized Score")
        ax12.set_title("Normalized Metrics Comparison")
        ax12.set_xticks(x_pos + width * 1.5)
        ax12.set_xticklabels(df.index, rotation=45)
        ax12.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

        plt.tight_layout()
        return fig, df
