import os
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import warnings
from dataclasses import dataclass

try:
    import nltk
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False


from utils import depth_breadth_filename_patterns, model_and_search_pattern, load_domain_vocab
from main_scaling_plot import create_main_scaling_plot
from optimization_analysis_plot import create_optimization_analysis_plot
from overall_quality_analysis import create_overall_quality_analysis
from parameter_effects_plot import create_parameter_effects_plot
from quality_dimensions_plot import create_quality_dimensions_plot

warnings.filterwarnings('ignore')

if NLTK_AVAILABLE:
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
    except:
        pass

plt.style.use('seaborn-v0_8-whitegrid')

plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
    'font.family': 'serif',
    'text.usetex': False  # Set to True if you have LaTeX installed
})


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
    Class to analyze deep research documents generated by the deep research pipeline.
    """
    def __init__(self):
        self.documents = {}
        self.metrics = {}
        self.vocab = load_domain_vocab()
        self.weights = QualityWeights()

    def load_document(self, filename, content):
        """
        Load a document and extract metadata from the filename
        """
        match = re.search(r'd(\d+)_b(\d+)', filename)

        if match:
            depth = int(match.group(1))
            breadth = int(match.group(2))
            key = f"d{depth}_b{breadth}"
            self.documents[key] = {
                'filename': filename,
                'depth': depth,
                'breadth': breadth,
                'content': content
            }


    def extract_mechanistic_detail(self, content):
        """
        Extract mechanistic detail from the content
        """
        mechanistic_terms = self.vocab['mechanistic_terms']
        return sum(content.lower().count(term) for term in mechanistic_terms)

    @staticmethod
    def extract_temporal_precision(content):
        """
        Extract temporal precision from the content
        """
        specific_patterns = [
            r'\d+(?:\.\d+)?(?:\s*[-–]\s*\d+(?:\.\d+)?)?\s*(?:yr|year|month|week|day|hour|decade|century)',
            r'(?:within|after|before)\s+\d+\s+(?:yr|year|month|week|day)',
            r'(?:every|each)\s+\d+\s+(?:yr|year|month|week|day)',
            r'\d{4}(?:\s*[-–]\s*\d{4})?(?:\s+(?:AD|BC|CE|BCE))?',  # Years
            r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}',
        ]

        vague_terms = [
            'recently', 'historically', 'traditionally', 'formerly', 'previously',
            'short-term', 'long-term', 'medium-term', 'near-term',
            'early', 'late', 'mid-', 'recent', 'ancient', 'modern',
            'soon', 'eventually', 'ultimately', 'initially', 'finally',
            'temporary', 'permanent', 'occasional', 'frequent', 'rare'
        ]

        specific_count = 0
        for pattern in specific_patterns:
            matches = re.findall(pattern, content.lower())
            specific_count += len(matches)

        vague_count = sum(content.lower().count(term) for term in vague_terms)

        return specific_count / max(1, specific_count + vague_count)

    @staticmethod
    def extract_temporal_references(content):
        """
        Extract temporal references from the content
        """
        temporal_patterns = re.findall(r'\d+[\s-]+(?:yr|year|decade)', content)
        return len(temporal_patterns)


    def extract_diversity_dimensions(self, content):
        """
        Extract diversity dimensions from the content
        """
        diversity_terms = self.vocab['diversity_dimensions']
        return sum(1 for term in diversity_terms if term.lower() in content.lower())


    def extract_source_count(self, content):
        """
        Extract source count from the content
        """
        sources = re.findall(r'https?://[^\s\)]+', content)
        return len(set(sources))

    def extract_metrics(self):
        """
        Extract comprehensive metrics from each document including advanced quality indicators
        """
        for key, doc in self.documents.items():
            content = doc['content']
            metrics = {}

            # Basic metrics
            metrics['word_count'] = len(content.split())
            metrics['char_count'] = len(content)
            metrics['source_count'] = self.extract_source_count(content)

            # Coverage and scope
            metrics['geographic_regions'] = sum(1 for r in self.vocab['regions'] if r.lower() in content.lower())
            metrics['intervention_types'] = sum(1 for i in self.vocab['interventions'] if i.lower() in content.lower())
            metrics['temporal_references'] = self.extract_temporal_references(content)
            metrics['temporal_precision'] = self.extract_temporal_precision(content)
            metrics['mechanistic_detail'] = self.extract_mechanistic_detail(content)
            metrics['causal_explanations'] = sum(content.lower().count(term) for term in self.vocab['causal_terms'])
            metrics['diversity_dimensions'] = self.extract_diversity_dimensions(content)

            # Research quality indicators
            metrics['research_gaps'] = content.lower().count('research gap') + content.lower().count('knowledge gap') + content.lower().count('data gap')
            metrics['speculative_ideas'] = content.lower().count('speculative') + content.lower().count('flagged') + content.lower().count('hypothetical')
            metrics['uncertainty_acknowledgment'] = content.lower().count('uncertain') + content.lower().count('unclear') + content.lower().count('unknown')
            metrics['hypothesis_testing'] = content.lower().count('hypothesis') + content.lower().count('test') + content.lower().count('experiment')

            # Trade-offs and complexity
            metrics['tradeoff_mentions'] = content.lower().count('trade-off') + content.lower().count('tradeoff') + content.lower().count('balance')

            # Quantitative rigor
            quantitative_patterns = re.findall(r'\d+\.?\d*\s*%', content)
            metrics['percentage_values'] = len(quantitative_patterns)

            metrics['statistical_rigor'] = sum(content.lower().count(term) for term in self.vocab['stats_terms'])
            metrics['policy_mentions'] = content.lower().count('policy') + content.lower().count('subsidy') + content.lower().count('regulation')

            # Structural quality indicators
            sections = content.split('\n## ')
            metrics['section_count'] = len(sections)

            # Citation patterns (beyond just URLs)
            citation_patterns = re.findall(r'\([^)]*\d{4}[^)]*\)', content)  # (Author, 2024) style
            metrics['formal_citations'] = len(citation_patterns)

            # Species-level specificity
            species_patterns = re.findall(r'\*[A-Z][a-z]+ [a-z]+\*', content)  # *Genus species*
            metrics['taxonomic_specificity'] = len(species_patterns)

            metrics['innovation_indicators'] = sum(content.lower().count(term) for term in self.vocab['innovation_terms'])
            metrics['ecosystem_services'] = sum(1 for es in self.vocab['ecosystem_services'] if es.lower() in content.lower())
            metrics['conservation_focus'] = sum(content.lower().count(term) for term in self.vocab['conservation_terms'])
            metrics['climate_relevance'] = sum(content.lower().count(term) for term in self.vocab['climate_terms'])
            metrics['ecological_complexity'] = sum(content.lower().count(term) for term in self.vocab['complexity_terms'])
            metrics['spatial_scales'] = sum(1 for scale in self.vocab['scale_terms'] if scale.lower() in content.lower())

            # Save metrics
            self.metrics[key] = metrics

    def calculate_quality_scores(self):
        """
        Calculate composite quality scores based on multiple dimensions
        """
        for key, metrics in self.metrics.items():
            # Normalize metrics to 0-1 scale for comparison
            word_count = metrics['word_count']

            # Research depth score (mechanistic understanding + causal explanations + temporal precision)
            depth_score = (
                min(metrics['mechanistic_detail'] / 20, 1.0) * 0.4 +
                min(metrics['causal_explanations'] / 10, 1.0) * 0.3 +
                metrics['temporal_precision'] * 0.3
            )

            # Research breadth score (geographic + intervention + diversity + ecosystem services + spatial scales)
            breadth_score = (
                min(metrics['geographic_regions'] / 8, 1.0) * 0.25 +
                min(metrics['intervention_types'] / 12, 1.0) * 0.25 +
                min(metrics['diversity_dimensions'] / 8, 1.0) * 0.25 +
                min(metrics['ecosystem_services'] / 10, 1.0) * 0.15 +
                min(metrics['spatial_scales'] / 6, 1.0) * 0.10
            )

            # Scientific rigor score (statistical terms + formal citations + uncertainty acknowledgment)
            rigor_score = (
                min(metrics['statistical_rigor'] / 5, 1.0) * 0.4 +
                min(metrics['formal_citations'] / 20, 1.0) * 0.4 +
                min(metrics['uncertainty_acknowledgment'] / 5, 1.0) * 0.2
            )

            # Innovation score (speculative ideas + innovation indicators + research gaps)
            innovation_score = (
                min(metrics['speculative_ideas'] / 3, 1.0) * 0.4 +
                min(metrics['innovation_indicators'] / 3, 1.0) * 0.3 +
                min(metrics['research_gaps'] / 3, 1.0) * 0.3
            )

            # Information density (sources per 1000 words)
            info_density = min(metrics['source_count'] / (word_count / 1000) / 50, 1.0)

            # Taxonomic sophistication
            taxonomic_score = min(metrics['taxonomic_specificity'] / 10, 1.0)

            # Ecological relevance score (conservation + climate + complexity)
            ecological_relevance = (
                min(metrics['conservation_focus'] / 8, 1.0) * 0.4 +
                min(metrics['climate_relevance'] / 6, 1.0) * 0.3 +
                min(metrics['ecological_complexity'] / 5, 1.0) * 0.3
            )

            w = self.weights

            overall_quality = (
                    depth_score          * w.depth        +
                    breadth_score        * w.breadth      +
                    rigor_score          * w.rigor        +
                    innovation_score     * w.innovation   +
                    ecological_relevance * w.ecological   +
                    info_density         * w.info_density +
                    taxonomic_score      * w.taxonomic
            )

            self.metrics[key].update({
                'depth_score': depth_score,
                'breadth_score': breadth_score,
                'rigor_score': rigor_score,
                'innovation_score': innovation_score,
                'ecological_relevance': ecological_relevance,
                'info_density': info_density,
                'taxonomic_score': taxonomic_score,
                'overall_quality': overall_quality
            })


    def analyze_multiple_questions(self, report_dir, question_numbers, output_dir) -> dict:
        """
        Analyze multiple questions and create comparative visualizations
        """
        os.makedirs(output_dir, exist_ok=True)

        all_results = {}

        for question_num in question_numbers:
            self.documents = {}
            self.metrics = {}

            loaded_count = 0
            for config in depth_breadth_filename_patterns:
                filename = f'{question_num}_{model_and_search_pattern}_{config}.md'
                try:
                    with open(f'{report_dir}/{filename}', 'r') as f:
                        content = f.read()
                    self.load_document(filename, content)
                    loaded_count += 1
                except FileNotFoundError:
                    print(f'File not found: {filename}')

            if loaded_count > 0:
                # Extract metrics and create visualizations
                self.extract_metrics()
                self.calculate_quality_scores()

                # Create output directory for plots
                os.makedirs(f'{output_dir}/plot_per_question', exist_ok=True)

                # Create visualizations for this question
                fig, df = self.create_visualizations()

                # Save the figure for this question
                fig.savefig(f'{output_dir}/plot_per_question/question_{question_num}_analysis.png',
                           dpi=300, bbox_inches='tight')
                plt.close(fig)

                # Add additional columns for aggregate analysis
                df['config'] = [f"d{self.documents[k]['depth']}_b{self.documents[k]['breadth']}" for k in df.index]
                df['question'] = question_num

                # Store results for aggregate analysis
                all_results[question_num] = df

                print(f'Analyzed question {question_num} with {loaded_count} documents')

        # Save comprehensive summary statistics with all metrics
        if all_results:
            self._save_comprehensive_summary_statistics(all_results, output_dir)

        return all_results

    @staticmethod
    def _save_comprehensive_summary_statistics(all_results, output_dir):
        """
        Save comprehensive summary statistics with all calculated metrics
        """
        # Combine all dataframes
        combined_df = pd.concat(all_results.values(), ignore_index=True)

        # Group by configuration and calculate comprehensive statistics
        summary_stats = combined_df.groupby('config').agg({
            # Basic metrics
            'source_count': ['mean', 'std', 'min', 'max'],
            'word_count': ['mean', 'std', 'min', 'max'],
            'char_count': ['mean', 'std'],

            # Geographic and coverage metrics
            'geographic_regions': ['mean', 'std'],
            'intervention_types': ['mean', 'std'],
            'diversity_dimensions': ['mean', 'std'],

            # Temporal metrics
            'temporal_references': ['mean', 'std'],
            'temporal_precision': ['mean', 'std'],

            # Mechanistic and causal metrics
            'mechanistic_detail': ['mean', 'std'],
            'causal_explanations': ['mean', 'std'],

            # Quality indicators
            'research_gaps': ['mean', 'std'],
            'speculative_ideas': ['mean', 'std'],
            'uncertainty_acknowledgment': ['mean', 'std'],
            'tradeoff_mentions': ['mean', 'std'],

            # Quantitative rigor
            'percentage_values': ['mean', 'std'],
            'statistical_rigor': ['mean', 'std'],
            'formal_citations': ['mean', 'std'],

            # Ecology-specific metrics
            'ecosystem_services': ['mean', 'std'],
            'conservation_focus': ['mean', 'std'],
            'climate_relevance': ['mean', 'std'],
            'ecological_complexity': ['mean', 'std'],
            'spatial_scales': ['mean', 'std'],

            # Innovation and policy
            'innovation_indicators': ['mean', 'std'],
            'policy_mentions': ['mean', 'std'],
            'taxonomic_specificity': ['mean', 'std'],

            # Quality scores
            'overall_quality': ['mean', 'std'],
            'depth_score': ['mean', 'std'],
            'breadth_score': ['mean', 'std'],
            'rigor_score': ['mean', 'std'],
            'innovation_score': ['mean', 'std'],
            'ecological_relevance': ['mean', 'std'],
            'info_density': ['mean', 'std'],
            'taxonomic_score': ['mean', 'std']
        }).round(3)

        # Flatten column names
        summary_stats.columns = ['_'.join(col).strip() for col in summary_stats.columns.values]

        # Save comprehensive summary statistics
        summary_stats.to_csv(f'{output_dir}/comprehensive_summary_statistics.csv')

    @staticmethod
    def create_publication_plots(statistics_file, all_results, figures_dir):
        """
        Create publication-ready plots for the paper
        """
        # Create main scaling plot
        create_main_scaling_plot(statistics_file, figures_dir)

        # Create parameter effects plot
        create_parameter_effects_plot(statistics_file, figures_dir)

        # Create optimization analysis plot
        create_optimization_analysis_plot(all_results, figures_dir)

        # Create quality dimensions plot
        create_quality_dimensions_plot(all_results, figures_dir)

        # Create overall quality analysis plot
        create_overall_quality_analysis(all_results, figures_dir)


    def create_visualizations(self):
        """
        Create comprehensive visualizations of the analysis.
        """
        df = pd.DataFrame(self.metrics).T
        df['depth'] = [self.documents[k]['depth'] for k in df.index]
        df['breadth'] = [self.documents[k]['breadth'] for k in df.index]

        # Create figure with subplots
        fig = plt.figure(figsize=(20, 16))

        # 1. Heatmap of key metrics
        ax1 = plt.subplot(4, 3, 1)
        heatmap_data = df.pivot_table(index='depth', columns='breadth', values='word_count')
        sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax1)
        ax1.set_title('Word Count by Depth and Breadth')

        # 2. Source count analysis
        ax2 = plt.subplot(4, 3, 2)
        heatmap_data2 = df.pivot_table(index='depth', columns='breadth', values='source_count')
        sns.heatmap(heatmap_data2, annot=True, fmt='.0f', cmap='Blues', ax=ax2)
        ax2.set_title('Source Count by Depth and Breadth')

        # 3. Geographic coverage
        ax3 = plt.subplot(4, 3, 3)
        heatmap_data3 = df.pivot_table(index='depth', columns='breadth', values='geographic_regions')
        sns.heatmap(heatmap_data3, annot=True, fmt='.0f', cmap='Greens', ax=ax3)
        ax3.set_title('Geographic Regions Covered')

        # 4. Mechanistic detail
        ax4 = plt.subplot(4, 3, 4)
        heatmap_data4 = df.pivot_table(index='depth', columns='breadth', values='mechanistic_detail')
        sns.heatmap(heatmap_data4, annot=True, fmt='.0f', cmap='Oranges', ax=ax4)
        ax4.set_title('Mechanistic Detail Score')

        # 5. Complexity metrics scatter
        ax5 = plt.subplot(4, 3, 5)
        scatter_size = df['source_count'] / 10
        scatter = ax5.scatter(df['mechanistic_detail'], df['temporal_references'],
                              s=scatter_size, alpha=0.7, c=df['depth'] + df['breadth'], cmap='viridis')
        ax5.set_xlabel('Mechanistic Detail Score')
        ax5.set_ylabel('Temporal References')
        ax5.set_title('Document Complexity (size=sources)')
        for idx, row in df.iterrows():
            ax5.annotate(idx, (row['mechanistic_detail'], row['temporal_references']), fontsize=8)

        # 6. Research quality indicators
        ax6 = plt.subplot(4, 3, 6)
        quality_score = (df['research_gaps'] + df['speculative_ideas'] + df['tradeoff_mentions'])

        # Only create heatmap if we have exactly 4 configurations
        if len(quality_score) == 4:
            heatmap_data6 = quality_score.values.reshape(2, 2)
            sns.heatmap(heatmap_data6, annot=True, fmt='.0f', cmap='Purples', ax=ax6,
                        xticklabels=[1, 4], yticklabels=[1, 4])
            ax6.set_xlabel('Breadth')
            ax6.set_ylabel('Depth')
        else:
            # Fallback to bar chart if we don't have complete data
            ax6.bar(df.index, quality_score, color='purple', alpha=0.7)
            ax6.set_xlabel('Configuration')
            ax6.set_ylabel('Quality Score')
            ax6.tick_params(axis='x', rotation=45)
        ax6.set_title('Research Quality Score')

        # 7. Quantitative information density
        ax7 = plt.subplot(4, 3, 7)
        quantitative_density = df['percentage_values'] / (df['word_count'] / 1000)
        bars = ax7.bar(df.index, quantitative_density, color=['lightblue', 'lightgreen', 'orange', 'red'])
        ax7.set_ylabel('Percentage Values per 1000 Words')
        ax7.set_title('Quantitative Information Density')
        ax7.tick_params(axis='x', rotation=45)

        # 8. Policy relevance
        ax8 = plt.subplot(4, 3, 8)
        policy_score = df['policy_mentions'] + df['tradeoff_mentions']

        # Only create heatmap if we have exactly 4 configurations
        if len(policy_score) == 4:
            heatmap_data8 = policy_score.values.reshape(2, 2)
            sns.heatmap(heatmap_data8, annot=True, fmt='.0f', cmap='RdYlBu', ax=ax8,
                        xticklabels=[1, 4], yticklabels=[1, 4])
            ax8.set_xlabel('Breadth')
            ax8.set_ylabel('Depth')
        else:
            # Fallback to bar chart
            ax8.bar(df.index, policy_score, color='blue', alpha=0.7)
            ax8.set_xlabel('Configuration')
            ax8.set_ylabel('Policy Score')
            ax8.tick_params(axis='x', rotation=45)
        ax8.set_title('Policy Relevance Score')

        # 9. Diversity dimensions coverage
        ax9 = plt.subplot(4, 3, 9)
        df_sorted = df.sort_values('diversity_dimensions')
        bars = ax9.barh(df_sorted.index, df_sorted['diversity_dimensions'],
                       color=['lightblue', 'lightgreen', 'orange', 'red'])
        ax9.set_xlabel('Number of Diversity Dimensions')
        ax9.set_title('Diversity Dimension Coverage')

        # 10. Intervention types coverage
        ax10 = plt.subplot(4, 3, 10)
        heatmap_data10 = df.pivot_table(index='depth', columns='breadth', values='intervention_types')
        sns.heatmap(heatmap_data10, annot=True, fmt='.0f', cmap='Reds', ax=ax10)
        ax10.set_title('Intervention Types Covered')

        # 11. Temporal specificity
        ax11 = plt.subplot(4, 3, 11)
        heatmap_data11 = df.pivot_table(index='depth', columns='breadth', values='temporal_references')
        sns.heatmap(heatmap_data11, annot=True, fmt='.0f', cmap='Greys', ax=ax11)
        ax11.set_title('Temporal References')

        # 12. Comprehensive comparison
        ax12 = plt.subplot(4, 3, 12)
        metrics_to_compare = ['source_count', 'geographic_regions', 'mechanistic_detail', 'diversity_dimensions']
        x_pos = np.arange(len(df))
        width = 0.2

        for i, metric in enumerate(metrics_to_compare):
            normalized_values = df[metric] / df[metric].max()
            ax12.bar(x_pos + i*width, normalized_values, width, label=metric.replace('_', ' ').title())

        ax12.set_xlabel('Configuration')
        ax12.set_ylabel('Normalized Score')
        ax12.set_title('Normalized Metrics Comparison')
        ax12.set_xticks(x_pos + width * 1.5)
        ax12.set_xticklabels(df.index, rotation=45)
        ax12.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        return fig, df
