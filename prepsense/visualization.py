"""
Visualization Module - Digital Twin and Interactive Charts

Creates animated simulations and high-quality visualizations.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx


def create_digital_twin_graph(orders, restaurants, riders):
    """
    Create digital twin visualization using NetworkX and Plotly.
    
    Parameters:
    -----------
    orders : list
        List of order dictionaries
    restaurants : list
        List of restaurant dictionaries
    riders : list
        List of rider dictionaries
    
    Returns:
    --------
    go.Figure
        Network graph figure
    """
    G = nx.Graph()
    
    # Add nodes
    for restaurant in restaurants:
        G.add_node(restaurant['id'], 
                  node_type='restaurant',
                  pos=(restaurant.get('lat', 0), restaurant.get('lon', 0)))
    
    for rider in riders:
        G.add_node(rider['id'],
                  node_type='rider',
                  pos=(rider.get('lat', 0), rider.get('lon', 0)))
    
    # Add edges (orders)
    for order in orders:
        if 'restaurant_id' in order and 'rider_id' in order:
            G.add_edge(order['restaurant_id'], order['rider_id'],
                      order_id=order.get('order_id', ''))
    
    # Create layout
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Extract node positions
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        node_data = G.nodes[node]
        if node_data.get('node_type') == 'restaurant':
            node_text.append(f"Restaurant {node}")
            node_color.append('#EF4F5F')
        else:
            node_text.append(f"Rider {node}")
            node_color.append('#4CAF50')
    
    # Extract edge positions
    edge_x = []
    edge_y = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    # Create figure
    fig = go.Figure()
    
    # Add edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines',
        name='Orders'
    ))
    
    # Add nodes with visible labels
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        name='Nodes',
        marker=dict(
            size=35,
            color=node_color,
            line=dict(width=3, color='white')
        ),
        text=node_text,
        textposition="middle center",
        textfont=dict(
            size=14,
            color='#1C1C1C',
            family='Poppins',
            weight='bold'
        ),
        hoverinfo='text',
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text="Digital Twin: Platform Operations", 
                  font=dict(family='Poppins', size=20, color='#1C1C1C', weight='bold')),
        showlegend=False,
        hovermode='closest',
        margin=dict(b=40, l=40, r=40, t=60),
        xaxis=dict(showgrid=True, gridcolor='#E0E0E0', zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor='#E0E0E0', zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600,
        font=dict(family='Inter', size=12, color='#1C1C1C')
    )
    
    return fig


def plot_signal_comparison(observed_times, reconstructed_times):
    """
    Plot signal comparison with distributions.
    
    Parameters:
    -----------
    observed_times : array-like
        Observed prep times
    reconstructed_times : array-like
        Reconstructed prep times
    
    Returns:
    --------
    go.Figure
        Comparison figure
    """
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Distribution Comparison', 'Variance Comparison',
                       'Time Series', 'Error Distribution'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Distribution comparison
    fig.add_trace(
        go.Histogram(x=observed_times, name='Observed', opacity=0.7,
                    marker_color='#EF4F5F', nbinsx=50),
        row=1, col=1
    )
    fig.add_trace(
        go.Histogram(x=reconstructed_times, name='Reconstructed', opacity=0.7,
                    marker_color='#4CAF50', nbinsx=50),
        row=1, col=1
    )
    
    # Variance comparison
    var_obs = np.var(observed_times)
    var_recon = np.var(reconstructed_times)
    
    fig.add_trace(
        go.Bar(x=['Observed', 'Reconstructed'],
              y=[var_obs, var_recon],
              marker_color=['#EF4F5F', '#4CAF50'],
              name='Variance'),
        row=1, col=2
    )
    
    # Time series
    n_samples = min(200, len(observed_times))
    indices = list(range(n_samples))
    
    fig.add_trace(
        go.Scatter(x=indices, y=observed_times[:n_samples],
                  name='Observed', line=dict(color='#EF4F5F')),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=indices, y=reconstructed_times[:n_samples],
                  name='Reconstructed', line=dict(color='#4CAF50')),
        row=2, col=1
    )
    
    # Error distribution
    errors = np.abs(np.array(observed_times) - np.array(reconstructed_times))
    fig.add_trace(
        go.Histogram(x=errors, name='Prediction Error',
                    marker_color='#FF9800', nbinsx=30),
        row=2, col=2
    )
    
    fig.update_layout(
        title_text="Signal Quality Comparison",
        showlegend=True,
        height=800,
        font=dict(family='Inter', size=12, color='#4A4A4A')
    )
    
    return fig


def plot_confidence_intervals(predictions, lower_bounds, upper_bounds, actuals=None):
    """
    Plot prediction confidence intervals.
    
    Parameters:
    -----------
    predictions : array-like
        Predicted values
    lower_bounds : array-like
        Lower confidence bounds
    upper_bounds : array-like
        Upper confidence bounds
    actuals : array-like, optional
        Actual values for comparison
    
    Returns:
    --------
    go.Figure
        Confidence interval figure
    """
    n = len(predictions)
    indices = list(range(min(200, n)))
    
    fig = go.Figure()
    
    # Confidence interval band
    fig.add_trace(go.Scatter(
        x=indices + indices[::-1],
        y=list(upper_bounds[:len(indices)]) + list(lower_bounds[:len(indices)])[::-1],
        fill='toself',
        fillcolor='rgba(33, 150, 243, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name='95% Confidence Interval'
    ))
    
    # Prediction line
    fig.add_trace(go.Scatter(
        x=indices,
        y=predictions[:len(indices)],
        mode='lines+markers',
        name='PrepSense Prediction',
        line=dict(color='#EF4F5F', width=2),
        marker=dict(size=4)
    ))
    
    # Actual values if provided
    if actuals is not None:
        fig.add_trace(go.Scatter(
            x=indices,
            y=actuals[:len(indices)],
            mode='markers',
            name='Actual',
            marker=dict(color='#4CAF50', size=6, symbol='circle')
        ))
    
    fig.update_layout(
        title=dict(text="Prediction Confidence Intervals",
                  font=dict(family='Poppins', size=18, color='#000000')),
        xaxis=dict(
            title="Order Index",
            title_font=dict(size=14, color='#000000'),
            tickfont=dict(size=12, color='#000000')
        ),
        yaxis=dict(
            title="Preparation Time (minutes)",
            title_font=dict(size=14, color='#000000'),
            tickfont=dict(size=12, color='#000000')
        ),
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', size=12, color='#000000'),
        legend=dict(font=dict(size=12, color='#000000')),
        height=500
    )
    
    return fig


def plot_business_impact(baseline_metrics, prepsense_metrics, scale=1_000_000):
    """
    Plot business impact comparison.
    
    Parameters:
    -----------
    baseline_metrics : dict
        Baseline system metrics
    prepsense_metrics : dict
        PrepSense metrics
    scale : int
        Scale factor (orders per day)
    
    Returns:
    --------
    go.Figure
        Business impact figure
    """
    categories = ['Idle Time\n(Hours)', 'Delay Time\n(Hours)', 'Total Cost\n(Units)']
    
    baseline_values = [
        baseline_metrics.get('idle_hours', 0) * scale / 1_000_000,
        baseline_metrics.get('delay_hours', 0) * scale / 1_000_000,
        baseline_metrics.get('total_cost', 0) * scale / 1_000_000
    ]
    
    prepsense_values = [
        prepsense_metrics.get('idle_hours', 0) * scale / 1_000_000,
        prepsense_metrics.get('delay_hours', 0) * scale / 1_000_000,
        prepsense_metrics.get('total_cost', 0) * scale / 1_000_000
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Baseline',
        x=categories,
        y=baseline_values,
        marker_color='#EF4F5F',
        text=[f'{v:.1f}M' for v in baseline_values],
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        name='PrepSense',
        x=categories,
        y=prepsense_values,
        marker_color='#4CAF50',
        text=[f'{v:.1f}M' for v in prepsense_values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=dict(text=f"Business Impact at {scale/1_000_000:.0f}M Orders/Day",
                  font=dict(family='Poppins', size=18, color='#1C1C1C')),
        xaxis_title="Metric",
        yaxis_title="Value (Millions)",
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', size=12, color='#4A4A4A'),
        height=500
    )
    
    return fig
