"""
Metrics Panel - Displays real-time dispatch metrics.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List


def render_metrics_panel(metrics: Dict) -> None:
    """
    Render metrics panel with key dispatch metrics.
    
    Parameters:
    -----------
    metrics : Dict
        Dictionary containing:
        - avg_idle_time: Average rider idle time
        - dispatch_efficiency: Dispatch efficiency score
        - delay_probability: Probability of delivery delay
        - total_orders: Total orders processed
        - active_dispatches: Currently active dispatches
    """
    st.markdown("### 📊 Live Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Avg Idle Time",
            value=f"{metrics.get('avg_idle_time', 0.0):.2f} min",
            delta=f"{metrics.get('idle_change', 0.0):.2f} min"
        )
    
    with col2:
        efficiency = metrics.get('dispatch_efficiency', 0.0)
        st.metric(
            label="Dispatch Efficiency",
            value=f"{efficiency:.1f}%",
            delta=f"{metrics.get('efficiency_change', 0.0):.1f}%"
        )
    
    with col3:
        delay_prob = metrics.get('delay_probability', 0.0)
        st.metric(
            label="Delay Risk",
            value=f"{delay_prob:.1f}%",
            delta=f"{metrics.get('delay_change', 0.0):.1f}%"
        )
    
    col4, col5 = st.columns(2)
    
    with col4:
        st.metric(
            label="Total Orders",
            value=f"{metrics.get('total_orders', 0)}"
        )
    
    with col5:
        st.metric(
            label="Active Dispatches",
            value=f"{metrics.get('active_dispatches', 0)}"
        )


def render_dispatch_cards(dispatches: List[Dict]) -> None:
    """
    Render dispatch decision cards.
    
    Parameters:
    -----------
    dispatches : List[Dict]
        List of dispatch decisions with:
        - order_id
        - predicted_kpt
        - confidence
        - dispatch_time
        - idle_risk
        - delay_risk
    """
    st.markdown("### 🚴 Active Dispatches")
    
    if not dispatches:
        st.info("No active dispatches. Waiting for orders...")
        return
    
    for dispatch in dispatches[-10:]:  # Show last 10
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**Order {dispatch.get('order_id', 'N/A')}**")
                st.caption(f"Predicted KPT: {dispatch.get('predicted_kpt', 0):.1f} min (±{dispatch.get('confidence', 0):.1f})")
            
            with col2:
                idle_risk = dispatch.get('idle_risk', 0)
                risk_color = "🟢" if idle_risk < 0.3 else "🟡" if idle_risk < 0.6 else "🔴"
                st.markdown(f"{risk_color} Idle: {idle_risk:.1%}")
            
            with col3:
                delay_risk = dispatch.get('delay_risk', 0)
                risk_color = "🟢" if delay_risk < 0.3 else "🟡" if delay_risk < 0.6 else "🔴"
                st.markdown(f"{risk_color} Delay: {delay_risk:.1%}")
            
            st.divider()
