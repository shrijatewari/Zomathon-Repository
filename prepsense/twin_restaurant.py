"""
Twin Restaurant Comparison Module

Simulates two identical restaurants side-by-side to show baseline vs PrepSense.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from dataset_generator import DatasetGenerator
from reconstruction_service import ReconstructionService
from telemetry_service import TelemetryService
from dispatch_optimizer import DispatchOptimizer


class TwinRestaurantSimulator:
    """Simulates twin restaurants for comparison."""
    
    def __init__(self, n_orders=50):
        self.n_orders = n_orders
        self.generator = DatasetGenerator(n_samples=n_orders)
        self.reconstructor = ReconstructionService()
        self.telemetry_service = TelemetryService()
        self.optimizer = DispatchOptimizer()
        
    def simulate_baseline(self):
        """Simulate baseline system (using observed prep times)."""
        df = self.generator.generate_orders()
        
        # Baseline uses observed prep times (noisy)
        prep_times = df['ObservedPrepTime'].values
        
        # Simulate rider dispatch (arrives too early)
        rider_arrival_gaps = np.random.uniform(5, 10, len(prep_times))  # Arrives early
        idle_times = np.maximum(0, prep_times - rider_arrival_gaps)
        delays = np.maximum(0, rider_arrival_gaps - prep_times)
        
        return {
            'prep_times': prep_times,
            'idle_times': idle_times,
            'delays': delays,
            'variance': np.var(prep_times),
            'mae': np.mean(np.abs(prep_times - np.mean(prep_times)))
        }
    
    def simulate_prepsense(self):
        """Simulate PrepSense system (using reconstructed prep times)."""
        df = self.generator.generate_orders()
        
        # PrepSense uses reconstructed prep times (less noisy)
        prep_times = df['ReconstructedPrepTime'].values
        
        # Optimized rider dispatch using batch optimization
        mean_prep = np.mean(prep_times)
        std_prep = np.std(prep_times)
        optimal_assign = self.optimizer.optimal_assignment(mean_prep, std_prep, k=1.0)
        
        # Compute idle times and delays for each order
        idle_times = np.maximum(0, prep_times - optimal_assign)
        delays = np.maximum(0, optimal_assign - prep_times)
        
        return {
            'prep_times': prep_times,
            'idle_times': idle_times,
            'delays': delays,
            'variance': np.var(prep_times),
            'mae': np.mean(np.abs(prep_times - np.mean(prep_times)))
        }
    
    def compare(self):
        """Run comparison simulation."""
        baseline = self.simulate_baseline()
        prepsense = self.simulate_prepsense()
        
        return {
            'baseline': baseline,
            'prepsense': prepsense,
            'idle_reduction': ((baseline['idle_times'].mean() - prepsense['idle_times'].mean()) / baseline['idle_times'].mean()) * 100 if baseline['idle_times'].mean() > 0 else 0,
            'variance_reduction': ((baseline['variance'] - prepsense['variance']) / baseline['variance']) * 100 if baseline['variance'] > 0 else 0
        }


def create_twin_comparison_chart(comparison):
    """Create side-by-side comparison chart."""
    baseline = comparison['baseline']
    prepsense = comparison['prepsense']
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Idle Time Comparison', 'Delay Comparison', 
                       'Prep Time Variance', 'Prediction Error'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Idle Time
    fig.add_trace(
        go.Bar(name='Baseline', x=['Baseline'], y=[baseline['idle_times'].mean()], 
               marker_color='#EF4F5F', showlegend=True),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(name='PrepSense', x=['PrepSense'], y=[prepsense['idle_times'].mean()],
               marker_color='#4CAF50', showlegend=True),
        row=1, col=1
    )
    
    # Delay
    fig.add_trace(
        go.Bar(name='Baseline', x=['Baseline'], y=[baseline['delays'].mean()],
               marker_color='#EF4F5F', showlegend=False),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(name='PrepSense', x=['PrepSense'], y=[prepsense['delays'].mean()],
               marker_color='#4CAF50', showlegend=False),
        row=1, col=2
    )
    
    # Variance
    fig.add_trace(
        go.Bar(name='Baseline', x=['Baseline'], y=[baseline['variance']],
               marker_color='#EF4F5F', showlegend=False),
        row=2, col=1
    )
    fig.add_trace(
        go.Bar(name='PrepSense', x=['PrepSense'], y=[prepsense['variance']],
               marker_color='#4CAF50', showlegend=False),
        row=2, col=2
    )
    
    # MAE
    fig.add_trace(
        go.Bar(name='Baseline', x=['Baseline'], y=[baseline['mae']],
               marker_color='#EF4F5F', showlegend=False),
        row=2, col=2
    )
    fig.add_trace(
        go.Bar(name='PrepSense', x=['PrepSense'], y=[prepsense['mae']],
               marker_color='#4CAF50', showlegend=False),
        row=2, col=2
    )
    
    fig.update_layout(
        title=dict(text="Twin Restaurant Comparison: Baseline vs PrepSense",
                  font=dict(family='Poppins', size=20, color='#000000')),
        height=600,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', size=12, color='#000000'),
        showlegend=True,
        legend=dict(font=dict(size=12, color='#000000')),
        xaxis=dict(title_font=dict(color='#000000'), tickfont=dict(color='#000000')),
        yaxis=dict(title_font=dict(color='#000000'), tickfont=dict(color='#000000')),
        xaxis2=dict(title_font=dict(color='#000000'), tickfont=dict(color='#000000')),
        yaxis2=dict(title_font=dict(color='#000000'), tickfont=dict(color='#000000')),
        xaxis3=dict(title_font=dict(color='#000000'), tickfont=dict(color='#000000')),
        yaxis3=dict(title_font=dict(color='#000000'), tickfont=dict(color='#000000')),
        xaxis4=dict(title_font=dict(color='#000000'), tickfont=dict(color='#000000')),
        yaxis4=dict(title_font=dict(color='#000000'), tickfont=dict(color='#000000'))
    )
    fig.update_annotations(font=dict(size=14, color='#000000'))
    
    return fig
