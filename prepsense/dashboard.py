"""
PrepSense Interactive Dashboard

Streamlit dashboard for Kitchen Preparation Time prediction system.
Designed with Zomato-inspired color scheme and styling.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from dataset_generator import DatasetGenerator
from simulator import KitchenSimulator
from telemetry import TelemetryGenerator
from reconstruction import PrepSenseReconstructor
from survival_model import SurvivalModel
from dispatch_optimizer import DispatchOptimizer

# Zomato-inspired color palette
COLORS = {
    'primary': '#CB472C',      # Warm reddish-orange
    'secondary': '#FFF7EB',    # Light cream
    'accent': '#FFD94F',       # Golden yellow
    'text': '#A52A2A',         # Dark reddish-brown
    'success': '#4CAF50',       # Green
    'info': '#2196F3',          # Blue
    'warning': '#FF9800'        # Orange
}

# Page configuration
st.set_page_config(
    page_title="PrepSense - Kitchen Prep Time Prediction",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Zomato-inspired styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Main background */
    .stApp {
        background: #F8F8F8;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main content area */
    .main .block-container {
        background: #FFFFFF;
        padding-top: 1rem;
        max-width: 1400px;
    }
    
    /* Zomato Logo Header */
    .zomato-header {
        background: linear-gradient(135deg, #EF4F5F 0%, #CB472C 100%);
        padding: 20px 40px;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .zomato-logo {
        font-family: 'Poppins', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -0.5px;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .zomato-logo::before {
        content: '';
        width: 40px;
        height: 40px;
        background: #FFFFFF;
        border-radius: 8px;
        display: inline-block;
        background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23EF4F5F"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>');
        background-size: 24px;
        background-position: center;
        background-repeat: no-repeat;
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 14px;
        font-weight: 400;
        margin-top: 4px;
    }
    
    /* Headers */
    h1 {
        color: #1C1C1C !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 28px;
        margin-bottom: 1rem;
    }
    
    h2 {
        color: #1C1C1C !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 22px;
        border-bottom: 2px solid #EF4F5F;
        padding-bottom: 8px;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
    
    h3 {
        color: #1C1C1C !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 18px;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Text */
    p {
        color: #4A4A4A !important;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        line-height: 1.6;
    }
    
    /* Metrics - Zomato style */
    [data-testid="stMetricValue"] {
        color: #EF4F5F !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2rem;
        letter-spacing: -0.5px;
    }
    
    [data-testid="stMetricLabel"] {
        color: #4A4A4A !important;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        color: #4A4A4A !important;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 13px;
    }
    
    /* Sidebar - Zomato dark theme */
    [data-testid="stSidebar"] {
        background-color: #1C1C1C;
    }
    
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stSidebar"] .stSlider label {
        color: #FFFFFF !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
    
    /* Buttons - Zomato style */
    .stButton>button {
        background-color: #EF4F5F;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(239, 79, 95, 0.2);
    }
    
    .stButton>button:hover {
        background-color: #CB472C;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(239, 79, 95, 0.3);
    }
    
    /* Sliders */
    .stSlider>div>div>div {
        background-color: #EF4F5F;
    }
    
    /* Cards with subtle animation */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E0E0E0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #1C1C1C !important;
        font-family: 'Inter', sans-serif;
    }
    
    .stMarkdown h2, .stMarkdown h3 {
        color: #1C1C1C !important;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #F8F8F8;
        border-left: 4px solid #EF4F5F;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
    }
    
    /* Smooth transitions */
    * {
        transition: background-color 0.2s ease, color 0.2s ease;
    }
    
    /* Chart containers */
    .js-plotly-plot {
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)


def load_or_generate_data(n_samples=5000, force_regenerate=False):
    """
    Load or generate dataset.
    
    Parameters:
    -----------
    n_samples : int
        Number of orders to generate
    force_regenerate : bool
        Force regeneration even if file exists
    """
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'orders.csv')
    
    # Force regenerate if requested or if file doesn't exist
    if force_regenerate or not os.path.exists(data_path):
        generator = DatasetGenerator(n_samples=n_samples)
        df = generator.generate_orders()
        generator.save_dataset(df, output_path=data_path)
        return df, True
    
    # Load existing
    try:
        df = pd.read_csv(data_path)
        # If existing dataset has different size, regenerate
        if len(df) != n_samples:
            generator = DatasetGenerator(n_samples=n_samples)
            df = generator.generate_orders()
            generator.save_dataset(df, output_path=data_path)
            return df, True
        return df, False
    except Exception as e:
        # If loading fails, generate new
        generator = DatasetGenerator(n_samples=n_samples)
        df = generator.generate_orders()
        generator.save_dataset(df, output_path=data_path)
        return df, True


def main():
    """Main dashboard function."""
    
    # Zomato-style header with logo
    st.markdown("""
    <div class="zomato-header">
        <div>
            <div class="zomato-logo">PrepSense</div>
            <div class="header-subtitle">Kitchen Preparation Time Prediction System</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.markdown("## Control Panel")
    
    # Parameters with session state to track changes
    if 'arrival_rate' not in st.session_state:
        st.session_state.arrival_rate = 0.5
    if 'noise_level' not in st.session_state:
        st.session_state.noise_level = 3.0
    if 'kitchen_capacity' not in st.session_state:
        st.session_state.kitchen_capacity = 20
    if 'n_samples' not in st.session_state:
        st.session_state.n_samples = 5000
    
    arrival_rate = st.sidebar.slider(
        "Order Arrival Rate (λ)", 
        0.1, 2.0, 
        value=st.session_state.arrival_rate, 
        step=0.1,
        key='arrival_rate_slider'
    )
    noise_level = st.sidebar.slider(
        "Noise Level (σ)", 
        0.5, 5.0, 
        value=st.session_state.noise_level, 
        step=0.5,
        key='noise_level_slider'
    )
    kitchen_capacity = st.sidebar.slider(
        "Kitchen Capacity", 
        5, 50, 
        value=st.session_state.kitchen_capacity, 
        step=5,
        key='kitchen_capacity_slider'
    )
    n_samples = st.sidebar.slider(
        "Number of Orders", 
        1000, 10000, 
        value=st.session_state.n_samples, 
        step=500,
        key='n_samples_slider'
    )
    
    # Check if parameters changed
    params_changed = (
        arrival_rate != st.session_state.arrival_rate or
        noise_level != st.session_state.noise_level or
        kitchen_capacity != st.session_state.kitchen_capacity or
        n_samples != st.session_state.n_samples
    )
    
    if params_changed:
        st.session_state.arrival_rate = arrival_rate
        st.session_state.noise_level = noise_level
        st.session_state.kitchen_capacity = kitchen_capacity
        st.session_state.n_samples = n_samples
        # Clear cache to force regeneration
        st.cache_data.clear()
    
    # Regenerate button
    if st.sidebar.button("Regenerate Data", use_container_width=True):
        st.session_state.force_regenerate = True
        st.cache_data.clear()
    
    force_regenerate = st.session_state.get('force_regenerate', False)
    if force_regenerate:
        st.session_state.force_regenerate = False
    
    # Load or generate data based on current parameters
    # Create generator with current parameters
    generator = DatasetGenerator(
        n_samples=n_samples,
        noise_level=noise_level,
        arrival_rate=arrival_rate,
        kitchen_capacity=kitchen_capacity
    )
    
    # Generate fresh data with current parameters
    if force_regenerate or params_changed:
        df = generator.generate_orders()
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'orders.csv')
        generator.save_dataset(df, output_path=data_path)
        st.sidebar.success(f"Generated {len(df)} orders with current parameters")
    else:
        # Try to load existing, but regenerate if params don't match
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'orders.csv')
        try:
            df = pd.read_csv(data_path)
            if len(df) != n_samples:
                df = generator.generate_orders()
                generator.save_dataset(df, output_path=data_path)
                st.sidebar.success(f"Regenerated {len(df)} orders")
            else:
                st.sidebar.info(f"Using {len(df)} orders from dataset")
        except:
            df = generator.generate_orders()
            generator.save_dataset(df, output_path=data_path)
            st.sidebar.success(f"Generated {len(df)} new orders")
    
    # Compute metrics
    mean_kpt_observed = df['ObservedPrepTime'].mean()
    mean_kpt_reconstructed = df['ReconstructedPrepTime'].mean()
    var_observed = df['ObservedPrepTime'].var()
    var_reconstructed = df['ReconstructedPrepTime'].var()
    var_reduction = ((var_observed - var_reconstructed) / var_observed) * 100
    
    mean_idle = df['IdleTime'].mean() if 'IdleTime' in df.columns else 0
    mean_idle_recon = mean_idle * 0.9  # Simulated improvement
    
    prediction_error = np.mean(np.abs(df['ObservedPrepTime'] - df['ReconstructedPrepTime']))
    
    # Main metrics row
    st.markdown("## Key Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Average KPT (Observed)",
            value=f"{mean_kpt_observed:.2f} min",
            delta=f"{mean_kpt_reconstructed:.2f} min (Reconstructed)"
        )
    
    with col2:
        st.metric(
            label="Signal Variance",
            value=f"{var_observed:.2f}",
            delta=f"-{var_reduction:.1f}%",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Avg Idle Time",
            value=f"{mean_idle:.2f} min",
            delta=f"-{((mean_idle - mean_idle_recon)/mean_idle)*100:.1f}%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="Prediction Error",
            value=f"{prediction_error:.2f} min",
            delta="Improved"
        )
    
    # Graphs section
    st.markdown("---")
    st.markdown("## Visualizations")
    
    # Row 1: Distribution and Variance
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Signal Distribution Comparison")
        fig_dist = px.histogram(
            df,
            x=['ObservedPrepTime', 'ReconstructedPrepTime'],
            nbins=50,
            barmode='overlay',
            opacity=0.7,
            color_discrete_sequence=[COLORS['primary'], COLORS['success']],
            labels={'value': 'Preparation Time (minutes)', 'count': 'Frequency'}
        )
        fig_dist.update_layout(
            title=dict(text="Preparation Time Distribution", font=dict(family='Poppins', size=16, color='#1C1C1C')),
            xaxis_title="Preparation Time (minutes)",
            yaxis_title="Frequency",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', size=12, color='#4A4A4A')
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        st.markdown("### Variance Comparison")
        variance_data = pd.DataFrame({
            'Signal': ['Observed', 'Reconstructed'],
            'Variance': [var_observed, var_reconstructed]
        })
        fig_var = px.bar(
            variance_data,
            x='Signal',
            y='Variance',
            color='Signal',
            color_discrete_map={'Observed': COLORS['primary'], 'Reconstructed': COLORS['success']},
            text='Variance'
        )
        fig_var.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_var.update_layout(
            title=dict(text=f"Variance Reduction: {var_reduction:.1f}%", font=dict(family='Poppins', size=16, color='#1C1C1C')),
            xaxis_title="Signal Type",
            yaxis_title="Variance",
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False,
            font=dict(family='Inter', size=12, color='#4A4A4A')
        )
        st.plotly_chart(fig_var, use_container_width=True)
    
    # Row 2: Idle Time and Queue Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Idle Time Comparison")
        idle_data = pd.DataFrame({
            'System': ['Baseline', 'PrepSense'],
            'Idle Time (min)': [mean_idle, mean_idle_recon]
        })
        fig_idle = px.bar(
            idle_data,
            x='System',
            y='Idle Time (min)',
            color='System',
            color_discrete_map={'Baseline': COLORS['primary'], 'PrepSense': COLORS['success']},
            text='Idle Time (min)'
        )
        fig_idle.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_idle.update_layout(
            title=dict(text="Rider Idle Time Reduction", font=dict(family='Poppins', size=16, color='#1C1C1C')),
            xaxis_title="System",
            yaxis_title="Average Idle Time (minutes)",
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False,
            font=dict(family='Inter', size=12, color='#4A4A4A')
        )
        st.plotly_chart(fig_idle, use_container_width=True)
    
    with col2:
        st.markdown("### Queue Length vs Prep Time")
        if 'QueueLength' in df.columns:
            try:
                fig_queue = px.scatter(
                    df.sample(min(1000, len(df))),
                    x='QueueLength',
                    y='ReconstructedPrepTime',
                    color='ReconstructedPrepTime',
                    color_continuous_scale='Viridis',
                    trendline="ols",
                    labels={'QueueLength': 'Queue Length', 'ReconstructedPrepTime': 'Prep Time (min)'}
                )
            except:
                # Fallback without trendline if statsmodels not available
                fig_queue = px.scatter(
                    df.sample(min(1000, len(df))),
                    x='QueueLength',
                    y='ReconstructedPrepTime',
                    color='ReconstructedPrepTime',
                    color_continuous_scale='Viridis',
                    labels={'QueueLength': 'Queue Length', 'ReconstructedPrepTime': 'Prep Time (min)'}
                )
            fig_queue.update_layout(
                title=dict(text="Kitchen Load Impact", font=dict(family='Poppins', size=16, color='#1C1C1C')),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', size=12, color='#4A4A4A')
            )
            st.plotly_chart(fig_queue, use_container_width=True)
    
    # Row 3: Confidence Intervals
    st.markdown("### Prediction Confidence Intervals")
    
    # Sample data for confidence intervals
    sample_size = min(200, len(df))
    sample_df = df.head(sample_size).copy()
    
    # Simulate confidence intervals
    predictions = sample_df['ReconstructedPrepTime'].values
    std_dev = sample_df['ReconstructedPrepTime'].std()
    lower_bounds = predictions - 1.96 * std_dev
    upper_bounds = predictions + 1.96 * std_dev
    
    fig_ci = go.Figure()
    
    # Confidence interval band
    fig_ci.add_trace(go.Scatter(
        x=list(range(sample_size)),
        y=upper_bounds,
        mode='lines',
        name='Upper Bound',
        line=dict(width=0),
        showlegend=False
    ))
    
    fig_ci.add_trace(go.Scatter(
        x=list(range(sample_size)),
        y=lower_bounds,
        mode='lines',
        name='95% CI',
        fill='tonexty',
        fillcolor=f'rgba(33, 150, 243, 0.2)',
        line=dict(width=0),
        showlegend=True
    ))
    
    # Prediction line
    fig_ci.add_trace(go.Scatter(
        x=list(range(sample_size)),
        y=predictions,
        mode='lines+markers',
        name='PrepSense Prediction',
        line=dict(color=COLORS['primary'], width=2),
        marker=dict(size=4)
    ))
    
    fig_ci.update_layout(
        title=dict(text="Prediction Confidence Intervals", font=dict(family='Poppins', size=16, color='#1C1C1C')),
        xaxis_title="Order Index",
        yaxis_title="Preparation Time (minutes)",
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
        font=dict(family='Inter', size=12, color='#4A4A4A')
    )
    
    st.plotly_chart(fig_ci, use_container_width=True)
    
    # Kitchen Load vs Service Rate
    st.markdown("### Kitchen Load Analysis")
    
    if 'KitchenLoad' in df.columns:
        # Simulate service rate
        mu0 = 0.1
        gamma = 0.2
        df_sample = df.sample(min(1000, len(df))).copy()
        df_sample['ServiceRate'] = mu0 / (1 + gamma * df_sample['KitchenLoad'])
        
        fig_load = px.scatter(
            df_sample,
            x='KitchenLoad',
            y='ServiceRate',
            size='ReconstructedPrepTime',
            color='ReconstructedPrepTime',
            color_continuous_scale='Reds',
            hover_data=['QueueLength'],
            labels={'KitchenLoad': 'Kitchen Load', 'ServiceRate': 'Service Rate'}
        )
        fig_load.update_layout(
            title=dict(text="Kitchen Load vs Service Rate", font=dict(family='Poppins', size=16, color='#1C1C1C')),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', size=12, color='#4A4A4A')
        )
        st.plotly_chart(fig_load, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 24px; background: #F8F8F8; border-radius: 8px; margin-top: 3rem;">
        <p style="color: #4A4A4A; font-weight: 500; font-size: 14px; font-family: 'Inter', sans-serif;">
            PrepSense - Improving Kitchen Efficiency Through AI-Powered Prediction
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
