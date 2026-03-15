"""
Rider Map Visualization - Shows restaurants, riders, and orders.
"""

import plotly.graph_objects as go
import numpy as np
from typing import Dict, List, Optional


def create_rider_map(
    restaurants: List[Dict],
    riders: List[Dict],
    orders: List[Dict],
    title: str = "Live Dispatch Map"
) -> go.Figure:
    """
    Create interactive map showing restaurants, riders, and active orders.
    
    Parameters:
    -----------
    restaurants : List[Dict]
        List of restaurant dicts with 'id', 'lat', 'lon'
    riders : List[Dict]
        List of rider dicts with 'id', 'lat', 'lon', 'available'
    orders : List[Dict]
        List of active orders with 'order_id', 'restaurant_id', 'rider_id'
    title : str
        Map title
    
    Returns:
    --------
    go.Figure
        Plotly figure with map visualization
    """
    fig = go.Figure()
    
    # Add restaurants (red markers)
    if restaurants:
        rest_lats = [r.get('lat', 0) for r in restaurants]
        rest_lons = [r.get('lon', 0) for r in restaurants]
        rest_ids = [r.get('id', '') for r in restaurants]
        
        fig.add_trace(go.Scatter(
            x=rest_lons,
            y=rest_lats,
            mode='markers+text',
            name='Restaurants',
            marker=dict(
                size=25,
                color='#EF4F5F',
                symbol='square',
                line=dict(width=2, color='white')
            ),
            text=rest_ids,
            textposition="top center",
            textfont=dict(size=10, color='#000000', family='Poppins', weight='bold'),
            hovertemplate='<b>%{text}</b><br>Restaurant<extra></extra>'
        ))
    
    # Add riders (green markers for available, orange for busy)
    if riders:
        available_riders = [r for r in riders if r.get('available', True)]
        busy_riders = [r for r in riders if not r.get('available', True)]
        
        if available_riders:
            avail_lats = [r.get('lat', 0) for r in available_riders]
            avail_lons = [r.get('lon', 0) for r in available_riders]
            avail_ids = [r.get('id', '') for r in available_riders]
            
            fig.add_trace(go.Scatter(
                x=avail_lons,
                y=avail_lats,
                mode='markers+text',
                name='Available Riders',
                marker=dict(
                    size=20,
                    color='#4CAF50',
                    symbol='circle',
                    line=dict(width=2, color='white')
                ),
                text=avail_ids,
                textposition="bottom center",
                textfont=dict(size=9, color='#000000', family='Poppins'),
                hovertemplate='<b>%{text}</b><br>Available Rider<extra></extra>'
            ))
        
        if busy_riders:
            busy_lats = [r.get('lat', 0) for r in busy_riders]
            busy_lons = [r.get('lon', 0) for r in busy_riders]
            busy_ids = [r.get('id', '') for r in busy_riders]
            
            fig.add_trace(go.Scatter(
                x=busy_lons,
                y=busy_lats,
                mode='markers+text',
                name='Busy Riders',
                marker=dict(
                    size=20,
                    color='#FF9800',
                    symbol='circle',
                    line=dict(width=2, color='white')
                ),
                text=busy_ids,
                textposition="bottom center",
                textfont=dict(size=9, color='#000000', family='Poppins'),
                hovertemplate='<b>%{text}</b><br>Busy Rider<extra></extra>'
            ))
    
    # Add connections (rider to restaurant for active orders)
    for order in orders:
        rider_id = order.get('rider_id')
        restaurant_id = order.get('restaurant_id')
        
        if rider_id and restaurant_id:
            rider = next((r for r in riders if r.get('id') == rider_id), None)
            restaurant = next((r for r in restaurants if r.get('id') == restaurant_id), None)
            
            if rider and restaurant:
                fig.add_trace(go.Scatter(
                    x=[rider.get('lon', 0), restaurant.get('lon', 0)],
                    y=[rider.get('lat', 0), restaurant.get('lat', 0)],
                    mode='lines',
                    name='Dispatch',
                    line=dict(width=2, color='#888', dash='dash'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family='Poppins', size=18, color='#000000', weight='bold')
        ),
        xaxis=dict(
            title="Longitude",
            title_font=dict(size=14, color='#000000'),
            tickfont=dict(size=12, color='#000000'),
            showgrid=True,
            gridcolor='#E0E0E0',
            zeroline=False
        ),
        yaxis=dict(
            title="Latitude",
            title_font=dict(size=14, color='#000000'),
            tickfont=dict(size=12, color='#000000'),
            showgrid=True,
            gridcolor='#E0E0E0',
            zeroline=False
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600,
        hovermode='closest',
        font=dict(family='Inter', size=12, color='#000000'),
        legend=dict(
            font=dict(size=12, color='#000000'),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig
