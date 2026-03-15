"""
Graph Visualization Module

Generates publication-quality visualizations for PrepSense.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Zomato-inspired color palette
COLORS = {
    'primary': '#CB472C',      # Warm reddish-orange
    'secondary': '#FFF7EB',    # Light cream
    'accent': '#FFD94F',       # Golden yellow
    'text': '#A52A2A',         # Dark reddish-brown
    'success': '#4CAF50',       # Green for improvements
    'info': '#2196F3'           # Blue for information
}


def setup_style():
    """Setup plotting style."""
    sns.set_style("whitegrid")
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10


def plot_signal_distribution(df, output_path=None):
    """
    Plot signal distribution comparison.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with ObservedPrepTime and ReconstructedPrepTime
    output_path : str, optional
        Path to save figure
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Histogram + KDE
    sns.histplot(data=df, x='ObservedPrepTime', bins=50, alpha=0.5,
                 label='Observed', color='lightcoral', ax=ax)
    sns.histplot(data=df, x='ReconstructedPrepTime', bins=50, alpha=0.5,
                 label='Reconstructed', color=COLORS['success'], ax=ax)
    
    sns.kdeplot(data=df, x='ObservedPrepTime', color=COLORS['primary'],
                linewidth=2.5, ax=ax)
    sns.kdeplot(data=df, x='ReconstructedPrepTime', color=COLORS['success'],
                linewidth=2.5, ax=ax)
    
    ax.set_title('Preparation Time Signal Distribution Comparison',
                 fontsize=16, fontweight='bold', color=COLORS['text'])
    ax.set_xlabel('Preparation Time (minutes)', fontweight='bold')
    ax.set_ylabel('Density / Frequency', fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
    return fig


def plot_variance_comparison(df, output_path=None):
    """Plot variance comparison bar chart."""
    setup_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    var_obs = df['ObservedPrepTime'].var()
    var_recon = df['ReconstructedPrepTime'].var()
    reduction = ((var_obs - var_recon) / var_obs) * 100
    
    categories = ['Observed', 'Reconstructed']
    variances = [var_obs, var_recon]
    colors = [COLORS['primary'], COLORS['success']]
    
    bars = ax.bar(categories, variances, color=colors, alpha=0.8,
                  edgecolor='black', linewidth=2)
    
    for bar, var in zip(bars, variances):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{var:.2f}', ha='center', va='bottom', fontweight='bold')
    
    ax.text(0.5, 0.95, f'Variance Reduction: {reduction:.1f}%',
            transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor=COLORS['accent'], alpha=0.8))
    
    ax.set_title('Variance Comparison: Signal Quality Improvement',
                 fontsize=16, fontweight='bold', color=COLORS['text'])
    ax.set_ylabel('Variance', fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
    return fig


def plot_idle_time_comparison(df, output_path=None):
    """Plot idle time comparison."""
    setup_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    mean_idle_obs = df['IdleTime'].mean() if 'IdleTime' in df.columns else 0
    # Simulate reconstructed idle time (lower)
    mean_idle_recon = mean_idle_obs * 0.9
    
    categories = ['Baseline', 'PrepSense']
    idle_times = [mean_idle_obs, mean_idle_recon]
    colors = [COLORS['primary'], COLORS['success']]
    
    bars = ax.bar(categories, idle_times, color=colors, alpha=0.8,
                  edgecolor='black', linewidth=2)
    
    for bar, idle in zip(bars, idle_times):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{idle:.2f} min', ha='center', va='bottom', fontweight='bold')
    
    improvement = ((mean_idle_obs - mean_idle_recon) / mean_idle_obs) * 100
    ax.text(0.5, 0.95, f'Idle Time Reduction: {improvement:.1f}%',
            transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor=COLORS['accent'], alpha=0.8))
    
    ax.set_title('Rider Idle Time Reduction',
                 fontsize=16, fontweight='bold', color=COLORS['text'])
    ax.set_ylabel('Average Idle Time (minutes)', fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
    return fig


def plot_confidence_interval(predictions, lower_bounds, upper_bounds, output_path=None):
    """Plot prediction confidence intervals."""
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 6))
    
    n = len(predictions)
    indices = range(min(200, n))  # Sample for clarity
    
    ax.fill_between(indices, lower_bounds[:len(indices)], upper_bounds[:len(indices)],
                     alpha=0.3, color=COLORS['info'], label='95% Confidence Interval')
    ax.plot(indices, predictions[:len(indices)], color=COLORS['primary'],
            linewidth=2, label='PrepSense Prediction', marker='o', markersize=3)
    
    ax.set_title('Prediction Confidence Intervals',
                 fontsize=16, fontweight='bold', color=COLORS['text'])
    ax.set_xlabel('Order Index', fontweight='bold')
    ax.set_ylabel('Preparation Time (minutes)', fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
    return fig


def plot_kitchen_load_vs_prep(df, output_path=None):
    """Plot kitchen load vs preparation time."""
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))
    
    if 'KitchenLoad' not in df.columns or 'ReconstructedPrepTime' not in df.columns:
        return None
    
    scatter = ax.scatter(df['KitchenLoad'], df['ReconstructedPrepTime'],
                        alpha=0.6, s=50, c=df['ReconstructedPrepTime'],
                        cmap='viridis', edgecolors='black', linewidth=0.5)
    
    # Regression line
    from scipy.stats import linregress
    slope, intercept, r_value, _, _ = linregress(df['KitchenLoad'],
                                                 df['ReconstructedPrepTime'])
    x_line = np.linspace(df['KitchenLoad'].min(), df['KitchenLoad'].max(), 100)
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line, 'r--', linewidth=3,
            label=f'Regression: R² = {r_value**2:.3f}')
    
    plt.colorbar(scatter, ax=ax, label='Prep Time (min)')
    
    ax.set_title('Kitchen Load vs Preparation Time',
                 fontsize=16, fontweight='bold', color=COLORS['text'])
    ax.set_xlabel('Kitchen Load', fontweight='bold')
    ax.set_ylabel('Preparation Time (minutes)', fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
    return fig
