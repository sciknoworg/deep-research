# thesis-scripts/plots.py
# All thesis publication figures in one place.
# - No empty subplots: build layouts dynamically based on available panels.
# - "Average Research Quality" panel is explicitly scaled to 0–4 for comparability.

from __future__ import annotations
import os
from typing import Dict, List
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ----------------------------- Small utilities --------------------------------

def _ensure_depth_breadth(df: pd.DataFrame) -> pd.DataFrame:
    """Guarantee 'depth' and 'breadth' integer columns exist."""
    out = df.copy()
    if 'config' in out.columns:
        out['depth'] = out['config'].str.extract(r'd(\d+)').astype(int)
        out['breadth'] = out['config'].str.extract(r'b(\d+)').astype(int)
    else:
        # Fallback: try to parse from index like 'd1_b4'
        idx = out.index.to_series().astype(str)
        out['depth'] = idx.str.extract(r'd(\d+)').astype(int)
        out['breadth'] = idx.str.extract(r'b(\d+)').astype(int)
        out['config'] = 'd' + out['depth'].astype(str) + '_b' + out['breadth'].astype(str)
    return out


def _concat_results(all_results: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Concatenate question-level DataFrames with consistent columns."""
    df = pd.concat(all_results.values(), ignore_index=True)
    return _ensure_depth_breadth(df)


# --------------------------- Per-question dashboard ---------------------------

def create_question_dashboard(df: pd.DataFrame) -> plt.Figure:
    """
    Compact dashboard for a single question. No empty subplots.
    Panels:
      - Heatmap: word_count by (depth, breadth)
      - Heatmap: source_count by (depth, breadth)
      - Bar:     Average Research Quality (overall_quality * 4), y-axis [0, 4]
    """
    df = _ensure_depth_breadth(df)

    panels = []

    # Panel 1: word count heatmap
    if 'word_count' in df.columns:
        piv_w = df.pivot_table(index='depth', columns='breadth', values='word_count', aggfunc='mean')
        panels.append(('Word Count by Depth & Breadth', piv_w, 'heatmap_words'))

    # Panel 2: source count heatmap
    if 'source_count' in df.columns:
        piv_s = df.pivot_table(index='depth', columns='breadth', values='source_count', aggfunc='mean')
        panels.append(('Sources by Depth & Breadth', piv_s, 'heatmap_sources'))

    # Panel 3: Average Research Quality (scaled 0–4)
    if 'overall_quality' in df.columns:
        # Average across configs in this question
        qual = df.groupby('config')['overall_quality'].mean().reindex(sorted(df['config'].unique()))
        qual_scaled = qual * 4.0
        panels.append(('Average Research Quality (0–4 scale)', qual_scaled, 'bar_quality'))

    # Layout: 1 row if ≤3, otherwise 2 rows
    n = len(panels)
    cols = min(3, n)
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(6.0 * cols, 4.5 * rows), squeeze=False)

    for ax, (title, data, kind) in zip(axes.flatten(), panels):
        if kind.startswith('heatmap'):
            sns.heatmap(data, annot=True, fmt='.0f', cmap='YlOrRd' if 'words' in kind else 'Blues', ax=ax)
            ax.set_title(title)
        elif kind == 'bar_quality':
            ax.bar(range(len(data.index)), data.values)
            ax.set_xticks(range(len(data.index)))
            ax.set_xticklabels(data.index, rotation=45, ha='right')
            ax.set_ylim(0, 4)  # show up to 4 for comparability to max
            ax.set_ylabel('Score (0–4)')
            ax.set_title(title)

    # Hide any unused axes (in case n < rows*cols)
    for ax in axes.flatten()[n:]:
        ax.set_visible(False)

    fig.tight_layout()
    return fig


# ------------------------------ Scaling heatmaps ------------------------------

def save_scaling_heatmaps(all_results: Dict[str, pd.DataFrame], figures_dir: str) -> None:
    """
    Save a 1×3 panel figure showing means by (depth, breadth) for:
      - Word count
      - Sources
      - Sources per 1k words
    """
    df = _concat_results(all_results)

    p1 = df.pivot_table(index='depth', columns='breadth', values='word_count', aggfunc='mean')
    p2 = df.pivot_table(index='depth', columns='breadth', values='source_count', aggfunc='mean')
    p3 = df.pivot_table(index='depth', columns='breadth', values='sources_per_1k', aggfunc='mean')

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    sns.heatmap(p1, annot=True, fmt='.0f', cmap='YlOrRd', ax=axes[0]); axes[0].set_title('Word Count')
    sns.heatmap(p2, annot=True, fmt='.0f', cmap='Blues',   ax=axes[1]); axes[1].set_title('Sources')
    sns.heatmap(p3, annot=True, fmt='.1f', cmap='Greens',  ax=axes[2]); axes[2].set_title('Sources per 1k')

    fig.tight_layout()
    fig.savefig(os.path.join(figures_dir, 'main_scaling_effects.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)


# -------------------------- Parameter effects (lines) -------------------------

def create_parameter_effects_plot(all_results: Dict[str, pd.DataFrame], figures_dir: str) -> None:
    """
    Two simple line plots:
      - Mean sources vs depth (averaged over breadth)
      - Mean sources vs breadth (averaged over depth)
    Also saves the same figure as 'optimization_analysis.png' for compatibility
    with existing LaTeX paths that expect that filename.
    """
    df = _concat_results(all_results)

    depth_curve = df.groupby('depth')['source_count'].mean()
    breadth_curve = df.groupby('breadth')['source_count'].mean()

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].plot(depth_curve.index, depth_curve.values, marker='o')
    axes[0].set_title('Mean Sources vs Depth'); axes[0].set_xlabel('Depth'); axes[0].set_ylabel('Sources')

    axes[1].plot(breadth_curve.index, breadth_curve.values, marker='o')
    axes[1].set_title('Mean Sources vs Breadth'); axes[1].set_xlabel('Breadth'); axes[1].set_ylabel('Sources')

    fig.tight_layout()
    fig.savefig(os.path.join(figures_dir, 'parameter_effects.png'), dpi=300, bbox_inches='tight')
    fig.savefig(os.path.join(figures_dir, 'optimization_analysis.png'), dpi=300, bbox_inches='tight')  # compat
    plt.close(fig)


# ----------------------------- Dimension bars --------------------------------

def create_quality_dimensions_plot(all_results: Dict[str, pd.DataFrame], figures_dir: str) -> None:
    """
    Grouped bars for the six dimensions, averaged per config across questions:
      depth_score, breadth_score, rigor_score, innovation_score,
      ecological_relevance, info_density
    """
    df = _concat_results(all_results)
    dims = ['depth_score','breadth_score','rigor_score','innovation_score',
            'ecological_relevance','info_density']
    # ensure columns exist
    for d in dims:
        if d not in df.columns:
            df[d] = 0.0

    means = df.groupby('config')[dims].mean()
    ax = means.plot(kind='bar', figsize=(12, 5))
    ax.set_ylim(0, 1)
    ax.set_ylabel('Score (0–1)')
    ax.set_title('Quality Decomposition by Configuration')
    ax.legend(title='Dimension', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'quality_dimensions.png'), dpi=300, bbox_inches='tight')
    plt.close()


# ------------------------ Overall quality (3–6 panels) -----------------------

def create_overall_quality_analysis(all_results: Dict[str, pd.DataFrame], figures_dir: str) -> None:
    """
    Overview figure without empty subplots. Panels:
      (A) Average Research Quality per config (overall_quality * 4) — y in [0,4]
      (B) Distribution of Sources per 1k (boxplot) by config
      (C) Scatter: Sources per 1k vs Overall Quality (color by config)

    If later you want more panels, just append to `panels` below;
    layout will expand automatically.
    """
    df = _concat_results(all_results)
    panels = []

    # (A) Average Research Quality (scaled 0–4)
    if 'overall_quality' in df.columns:
        qual = df.groupby('config')['overall_quality'].mean()
        panels.append(('Average Research Quality (0–4)', qual * 4.0, 'bar_quality'))

    # (B) Boxplot: sources per 1k by config
    if 'sources_per_1k' in df.columns:
        panels.append(('Sources per 1k by Config', df[['config','sources_per_1k']], 'box_sources_per_1k'))

    # (C) Scatter: sources per 1k vs overall_quality
    if 'sources_per_1k' in df.columns and 'overall_quality' in df.columns:
        panels.append(('Sources per 1k vs Overall Quality', df[['config','sources_per_1k','overall_quality']], 'scatter'))

    n = len(panels)
    cols = 3 if n >= 3 else n
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(6.2 * cols, 4.8 * rows), squeeze=False)

    for ax, (title, data, kind) in zip(axes.flatten(), panels):
        if kind == 'bar_quality':
            data = data.reindex(sorted(data.index))
            ax.bar(range(len(data.index)), data.values)
            ax.set_xticks(range(len(data.index)))
            ax.set_xticklabels(data.index, rotation=45, ha='right')
            ax.set_ylim(0, 4)
            ax.set_ylabel('Score (0–4)')
            ax.set_title(title)

        elif kind == 'box_sources_per_1k':
            order = sorted(data['config'].unique())
            sns.boxplot(data=data, x='config', y='sources_per_1k', order=order, ax=ax)
            ax.set_title(title); ax.set_xlabel(''); ax.set_ylabel('Sources per 1k')
            ax.tick_params(axis='x', rotation=45)

        elif kind == 'scatter':
            # jitter the x per-config for readability
            cfgs = sorted(data['config'].unique())
            xmap = {c: i for i, c in enumerate(cfgs)}
            x = data['config'].map(xmap).astype(float)
            ax.scatter(x, data['sources_per_1k'], s=18, alpha=0.6, label='sources/1k')
            # color by overall quality (0–1) using colormap
            sc = ax.scatter(x + 0.05, data['overall_quality'] * 4.0, s=18, alpha=0.6, c=data['overall_quality'],
                            cmap='viridis', label='quality (×4)')
            ax.set_xticks(range(len(cfgs))); ax.set_xticklabels(cfgs, rotation=45, ha='right')
            ax.set_ylabel('Value (sources/1k or quality×4)')
            ax.set_title(title)
            cbar = plt.colorbar(sc, ax=ax); cbar.set_label('Overall Quality (0–1)')

    # Hide unused axes
    for ax in axes.flatten()[n:]:
        ax.set_visible(False)

    fig.tight_layout()
    fig.savefig(os.path.join(figures_dir, 'overall_quality_analysis.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
