import pandas as pd
from matplotlib import pyplot as plt

from scripts.utils import depth_breadth_filename_patterns


def create_optimization_analysis_plot(all_results, figures_dir):
        """
        Create an optimization analysis showing diminishing returns and optimal configurations
        """
        combined_df = pd.concat(all_results.values(), ignore_index=True)
        combined_df['config'] = combined_df.apply(lambda row: f"d{row['depth']}_b{row['breadth']}", axis=1)

        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Research Configuration Optimization Analysis', fontsize=16, fontweight='bold')

        colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']

        # 1. Quality vs Cost (sources as proxy for cost)
        ax1 = axes[0, 0]
        quality_means = []
        source_means = []

        for config in depth_breadth_filename_patterns:
            config_data = combined_df[combined_df['config'] == config]
            if len(config_data) > 0:
                if 'overall_quality' in config_data.columns:
                    quality_means.append(config_data['overall_quality'].mean())
                else:
                    quality_means.append(0)
                source_means.append(config_data['source_count'].mean())
            else:
                quality_means.append(0)
                source_means.append(0)

        scatter = ax1.scatter(source_means, quality_means, c=colors, s=200, alpha=0.8)
        for i, config in enumerate(depth_breadth_filename_patterns):
            ax1.annotate(config, (source_means[i], quality_means[i]),
                        xytext=(5, 5), textcoords='offset points', fontweight='bold')

        ax1.set_xlabel('Average Source Count (Cost Proxy)')
        ax1.set_ylabel('Overall Quality Score')
        ax1.set_title('Quality vs Cost Trade-off')
        ax1.grid(True, alpha=0.3)

        # 2. Efficiency analysis (Quality per source)
        ax2 = axes[0, 1]
        efficiency = [q/s if s > 0 else 0 for q, s in zip(quality_means, source_means)]
        bars = ax2.bar(depth_breadth_filename_patterns, efficiency, color=colors, alpha=0.8)
        ax2.set_title('Quality Efficiency (Quality/Source)')
        ax2.set_ylabel('Quality per Source')

        for bar, eff in zip(bars, efficiency):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.0001,
                   f'{eff:.4f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

        # 3. Diminishing returns analysis
        ax3 = axes[1, 0]
        # Calculate marginal improvements
        baseline_quality = quality_means[0]  # d1_b1
        marginal_improvements = [(q - baseline_quality) for q in quality_means]
        marginal_costs = [(s - source_means[0]) for s in source_means]

        bars = ax3.bar(depth_breadth_filename_patterns, marginal_improvements, color=colors, alpha=0.8)
        ax3.set_title('Marginal Quality Improvement')
        ax3.set_ylabel('Quality Improvement vs d1_b1')

        for bar, imp in zip(bars, marginal_improvements):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{imp:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

        # 4. Configuration ranking
        ax4 = axes[1, 1]
        # Create a composite ranking based on quality and efficiency
        ranking_scores = [q * 0.7 + e * 0.3 for q, e in zip(quality_means, efficiency)]
        sorted_configs = sorted(zip(depth_breadth_filename_patterns, ranking_scores), key=lambda x: x[1], reverse=True)

        ranked_configs, ranked_scores = zip(*sorted_configs)
        bars = ax4.barh(range(len(ranked_configs)), ranked_scores,
                       color=[colors[depth_breadth_filename_patterns.index(c)] for c in ranked_configs], alpha=0.8)
        ax4.set_yticks(range(len(ranked_configs)))
        ax4.set_yticklabels(ranked_configs)
        ax4.set_xlabel('Composite Ranking Score')
        ax4.set_title('Configuration Ranking (Quality + Efficiency)')

        for i, (bar, score) in enumerate(zip(bars, ranked_scores)):
            width = bar.get_width()
            ax4.text(width + 0.01, bar.get_y() + bar.get_height()/2.,
                   f'{score:.3f}', ha='left', va='center', fontweight='bold', fontsize=10)

        plt.tight_layout()
        output_path = f'{figures_dir}/optimization_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
