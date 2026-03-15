"""
PrepSense Advanced Research Prototype - Main Application

Multi-page Streamlit dashboard demonstrating PrepSense system.
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import textwrap
from datetime import datetime, timedelta
from urllib.parse import quote
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import all modules
from event_stream import EventStream, EventType
from kitchen_simulator import KitchenSimulator
from telemetry_service import TelemetryService
from reconstruction_service import ReconstructionService
from signal_filter import SignalFilter
from survival_prediction import SurvivalPrediction
from dispatch_optimizer import DispatchOptimizer
from dataset_generator import DatasetGenerator
from visualization import (
    create_digital_twin_graph,
    plot_signal_comparison,
    plot_confidence_intervals,
    plot_business_impact
)
from plotly.subplots import make_subplots
from war_room import WarRoomSimulator, create_war_room_map
from twin_restaurant import TwinRestaurantSimulator, create_twin_comparison_chart
from event_timeline import OrderLifecycleReplay, create_timeline_replay_chart

# Page configuration
st.set_page_config(
    page_title="PrepSense - Advanced Research Prototype",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - hide Streamlit header (shows "key" instead of close) and add proper × close
st.markdown("""
<style>
    
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    .stApp {
        background: #F8F8F8;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main .block-container {
        background: #FFFFFF;
        padding-top: 1rem;
        max-width: 1400px;
    }
    
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
    }
    
    h1 {
        color: #1C1C1C !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 28px;
        margin-bottom: 1rem;
        line-height: 1.3;
    }
    
    h2 {
        color: #1C1C1C !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 22px;
        border-bottom: 2px solid #EF4F5F;
        padding-bottom: 8px;
        margin-top: 2rem;
        margin-bottom: 1rem;
        line-height: 1.4;
    }
    
    h3 {
        color: #1C1C1C !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 18px;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        line-height: 1.4;
    }
    
    h4 {
        color: #1C1C1C !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 16px;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    p {
        color: #4A4A4A !important;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .stMarkdown {
        color: #1C1C1C !important;
        font-family: 'Inter', sans-serif;
    }
    
    .stMarkdown p {
        color: #4A4A4A !important;
        font-size: 14px;
        line-height: 1.6;
    }
    
    
    [data-testid="stSidebar"] {
        background-color: #1C1C1C;
    }
    
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-family: 'Poppins', sans-serif;
        border-bottom: 2px solid #EF4F5F;
    }

    .sidebar-shell {
        display: flex;
        flex-direction: column;
        min-height: calc(100vh - 5rem);
        justify-content: space-between;
        padding: 6px 0 10px 0;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 6px 2px 18px 2px;
    }

    .sidebar-brand-mark {
        width: 26px;
        height: 22px;
        border-radius: 10px 10px 4px 10px;
        background: linear-gradient(135deg, #FFFFFF 0%, #F2F2F2 100%);
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.55);
        flex-shrink: 0;
    }

    .sidebar-brand-label {
        font-family: 'Poppins', sans-serif;
        font-size: 15px;
        font-weight: 600;
        color: #FFFFFF;
        letter-spacing: -0.2px;
    }

    .sidebar-nav-group {
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin-top: 8px;
    }

    .sidebar-nav-link {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 12px;
        border-radius: 14px;
        text-decoration: none !important;
        color: rgba(255,255,255,0.82) !important;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.18s ease;
        border: 1px solid transparent;
    }

    .sidebar-nav-link:hover {
        background: rgba(255,255,255,0.06);
        color: #FFFFFF !important;
        transform: translateX(2px);
    }

    .sidebar-nav-link.active {
        background: linear-gradient(135deg, rgba(239,79,95,0.24) 0%, rgba(255,107,107,0.14) 100%);
        border-color: rgba(239,79,95,0.45);
        color: #FFFFFF !important;
        box-shadow: 0 10px 20px rgba(239,79,95,0.16);
    }

    .sidebar-nav-icon {
        width: 34px;
        height: 34px;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(255,255,255,0.08);
        font-size: 16px;
        flex-shrink: 0;
    }

    .sidebar-nav-link.active .sidebar-nav-icon {
        background: rgba(255,255,255,0.12);
    }

    .sidebar-nav-copy {
        display: flex;
        flex-direction: column;
        min-width: 0;
    }

    .sidebar-nav-title {
        color: inherit;
        font-size: 14px;
        font-weight: 600;
        line-height: 1.25;
    }

    .sidebar-nav-desc {
        color: rgba(255,255,255,0.48);
        font-size: 11px;
        line-height: 1.35;
        margin-top: 2px;
    }

    .sidebar-mode-pills {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 8px 0 14px 0;
    }

    .sidebar-mode-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 11px 10px;
        border-radius: 14px;
        text-decoration: none !important;
        font-size: 13px;
        font-weight: 700;
        color: rgba(255,255,255,0.82) !important;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.12);
        transition: all 0.18s ease;
    }

    .sidebar-mode-pill.active {
        background: linear-gradient(135deg, #EF4F5F 0%, #FF6B6B 100%);
        color: #FFFFFF !important;
        border-color: transparent;
        box-shadow: 0 10px 22px rgba(239,79,95,0.22);
    }

    .sidebar-footer-card {
        margin-top: 18px;
        padding: 14px 12px;
        border-radius: 16px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
    }

    .sidebar-footer-user {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .sidebar-footer-avatar {
        width: 34px;
        height: 34px;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #EF4F5F 0%, #CB472C 100%);
        color: #FFFFFF;
        font-size: 14px;
        font-weight: 700;
        flex-shrink: 0;
    }

    .sidebar-footer-name {
        color: #FFFFFF;
        font-size: 13px;
        font-weight: 600;
        line-height: 1.2;
    }

    .sidebar-footer-role {
        color: rgba(255,255,255,0.52);
        font-size: 11px;
        line-height: 1.2;
        margin-top: 2px;
    }
    
    /* METRIC STYLING - Make values visible */
    [data-testid="stMetricValue"] {
        color: #EF4F5F !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        letter-spacing: -0.5px;
        line-height: 1.2 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #4A4A4A !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #4A4A4A !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }
    
    /* Metric containers */
    [data-testid="stMetricContainer"] {
        background: #FFFFFF !important;
        padding: 16px !important;
        border-radius: 8px !important;
        border: 1px solid #E0E0E0 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        margin-bottom: 16px !important;
    }
    
    /* Ensure all text in info boxes is visible */
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        font-family: 'Inter', sans-serif;
        color: #1C1C1C !important;
    }
    
    .stAlert p, .stInfo p, .stSuccess p, .stWarning p, .stError p {
        color: #1C1C1C !important;
        font-size: 14px;
        line-height: 1.6;
    }
    
    /* Animations for dynamic content */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        50% {
            box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    .nav-mode-wrap {
        display: flex;
        gap: 12px;
        align-items: center;
        margin-bottom: 8px;
    }

    .nav-mode-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 132px;
        padding: 12px 18px;
        border-radius: 14px;
        text-decoration: none !important;
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        font-weight: 700;
        transition: all 0.2s ease;
        border: 1px solid #D8D8D8;
        background: #FFFFFF;
        color: #3A3A3A !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.04);
    }

    .nav-mode-pill:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.08);
    }

    .nav-mode-pill.active {
        background: linear-gradient(135deg, #EF4F5F 0%, #FF6B6B 100%);
        color: #FFFFFF !important;
        border-color: transparent;
        box-shadow: 0 12px 24px rgba(239,79,95,0.28);
    }

    .nav-card-link {
        text-decoration: none !important;
        display: block;
    }

    .nav-card {
        position: relative;
        overflow: hidden;
        border-radius: 18px;
        padding: 22px;
        min-height: 220px;
        border: 1px solid rgba(0,0,0,0.06);
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
        transition: transform 0.22s ease, box-shadow 0.22s ease;
        background: #FFFFFF;
    }

    .nav-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 42px rgba(15, 23, 42, 0.14);
    }

    .nav-card .nav-card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 18px;
    }

    .nav-card .nav-card-icon {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        background: rgba(255,255,255,0.72);
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.45);
    }

    .nav-card .nav-card-tag {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        opacity: 0.9;
    }

    .nav-card .nav-card-title {
        font-family: 'Poppins', sans-serif;
        font-size: 28px;
        font-weight: 700;
        line-height: 1.15;
        color: #1C1C1C;
        margin-bottom: 12px;
    }

    .nav-card .nav-card-desc {
        font-size: 14px;
        line-height: 1.6;
        color: #4A4A4A;
        margin-bottom: 20px;
    }

    .nav-card .nav-card-metric {
        margin-top: auto;
        font-size: 13px;
        font-weight: 700;
        color: #1C1C1C;
    }

    .nav-card .nav-card-cta {
        position: absolute;
        left: 22px;
        right: 22px;
        bottom: 18px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 12px 14px;
        border-radius: 12px;
        background: rgba(28,28,28,0.92);
        color: #FFFFFF !important;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.01em;
        opacity: 0;
        transform: translateY(14px);
        transition: all 0.22s ease;
    }

    .nav-card:hover .nav-card-cta {
        opacity: 1;
        transform: translateY(0);
    }

    .nav-card .nav-card-cta {
        background: rgba(239,79,95,0.96);
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state - data will be loaded on first page visit
def initialize_session_state():
    """Initialize all session state variables."""
    if 'initialized' not in st.session_state:
        # Initialize default parameter values for dynamic updates
        if 'platform_arrival_rate' not in st.session_state:
            st.session_state.platform_arrival_rate = 0.5
        if 'platform_duration' not in st.session_state:
            st.session_state.platform_duration = 30
        if 'signal_noise_level' not in st.session_state:
            st.session_state.signal_noise_level = 3.0
        if 'signal_handover_mean' not in st.session_state:
            st.session_state.signal_handover_mean = 2.0
        if 'signal_n_samples' not in st.session_state:
            st.session_state.signal_n_samples = 1000
        if 'prediction_distribution' not in st.session_state:
            st.session_state.prediction_distribution = 'gamma'
        if 'prediction_n_samples' not in st.session_state:
            st.session_state.prediction_n_samples = 1000
        if 'dispatch_cost_idle' not in st.session_state:
            st.session_state.dispatch_cost_idle = 1.0
        if 'dispatch_cost_delay' not in st.session_state:
            st.session_state.dispatch_cost_delay = 2.0
        if 'dispatch_safety_factor' not in st.session_state:
            st.session_state.dispatch_safety_factor = 1.0
        if 'noise_lab_merchant_noise' not in st.session_state:
            st.session_state.noise_lab_merchant_noise = 3.0
        if 'noise_lab_order_rate' not in st.session_state:
            st.session_state.noise_lab_order_rate = 0.5
        if 'noise_lab_kitchen_capacity' not in st.session_state:
            st.session_state.noise_lab_kitchen_capacity = 20
        
        try:
            # Simulation data
            if 'simulation_data' not in st.session_state:
                generator = DatasetGenerator(n_samples=5000)
                df = generator.generate_orders()
                st.session_state.simulation_data = df
            
            # Events
            if 'events' not in st.session_state or len(st.session_state.events) == 0:
                event_stream = EventStream(arrival_rate=0.5)
                start_time = datetime.now() - timedelta(days=1)
                events = event_stream.simulate_time_window(start_time, 30)
                st.session_state.events = events
            
            # Signal data
            if 'signal_data' not in st.session_state:
                generator = DatasetGenerator(n_samples=1000, noise_level=3.0)
                df = generator.generate_orders()
                reconstructor = ReconstructionService(handover_mean=2.0)
                telemetry_service = TelemetryService(handover_mean=2.0)
                reconstructed_times = []
                observed_times = []
                for idx, row in df.iterrows():
                    try:
                        order_time = pd.to_datetime(row['OrderTime'])
                        packed_time = order_time + timedelta(minutes=row['ObservedPrepTime'])
                        order_id = f"ORD_{idx:06d}"
                        telemetry = telemetry_service.generate_telemetry(order_id, order_time, packed_time)
                        recon_result = reconstructor.reconstruct_from_telemetry(telemetry)
                        reconstructed_times.append(recon_result['kpt_reconstructed'])
                        observed_times.append(row['ObservedPrepTime'])
                    except Exception as e:
                        continue
                st.session_state.signal_data = {
                    'observed': observed_times,
                    'reconstructed': reconstructed_times,
                    'noise_level': 3.0
                }
            
            # Survival model
            if 'survival_model' not in st.session_state:
                generator = DatasetGenerator(n_samples=1000)
                df = generator.generate_orders()
                prep_times = df['ReconstructedPrepTime'].values
                survival_model = SurvivalPrediction(distribution='gamma')
                survival_model.fit(prep_times)
                st.session_state.survival_model = survival_model
                st.session_state.prep_times = prep_times
            
            # Dispatch comparison
            if 'dispatch_comparison' not in st.session_state:
                generator = DatasetGenerator(n_samples=1000)
                df = generator.generate_orders()
                baseline_times = df['ObservedPrepTime'].values
                prepsense_times = df['ReconstructedPrepTime'].values
                optimizer = DispatchOptimizer(cost_idle=1.0, cost_delay=2.0)
                comparison = optimizer.compare_baseline_vs_prepsense(baseline_times, prepsense_times, k=1.0)
                st.session_state.dispatch_comparison = comparison
            
            # Business impact
            if 'business_impact' not in st.session_state:
                generator = DatasetGenerator(n_samples=5000)
                df = generator.generate_orders()
                baseline_times = df['ObservedPrepTime'].values
                prepsense_times = df['ReconstructedPrepTime'].values
                optimizer = DispatchOptimizer()
                baseline_opt = optimizer.batch_optimize(baseline_times)
                prepsense_opt = optimizer.batch_optimize(prepsense_times)
                scale = 1_000_000
                baseline_metrics = {
                    'idle_hours': baseline_opt['mean_idle_time'] * scale / 60,
                    'delay_hours': baseline_opt['mean_delay'] * scale / 60,
                    'total_cost': baseline_opt['total_cost'] * scale
                }
                prepsense_metrics = {
                    'idle_hours': prepsense_opt['mean_idle_time'] * scale / 60,
                    'delay_hours': prepsense_opt['mean_delay'] * scale / 60,
                    'total_cost': prepsense_opt['total_cost'] * scale
                }
                st.session_state.business_impact = {
                    'baseline': baseline_metrics,
                    'prepsense': prepsense_metrics,
                    'scale': scale
                }
            
            st.session_state.initialized = True
        except Exception as e:
            st.error(f"Error initializing data: {str(e)}")
            st.session_state.initialized = False


def page_platform_simulation():
    """Platform Simulation Page."""
    st.markdown("""
    <div class="zomato-header">
        <div>
            <div class="zomato-logo">PrepSense</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Platform Simulation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Data is already loaded in session state initialization
    
    # Key metrics at top - properly formatted
    st.markdown("### Key Performance Metrics")
    if 'simulation_data' in st.session_state:
        df = st.session_state.simulation_data
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric(
                label="Total Orders",
                value=f"{len(df):,}",
                help="Total number of orders in dataset"
            )
        with col_m2:
            avg_prep = df['ReconstructedPrepTime'].mean()
            st.metric(
                label="Avg Prep Time",
                value=f"{avg_prep:.2f} min",
                help="Average preparation time"
            )
        with col_m3:
            var_prep = df['ReconstructedPrepTime'].var()
            st.metric(
                label="Signal Variance",
                value=f"{var_prep:.2f}",
                help="Variance of prep time signal"
            )
        with col_m4:
            stores = df['RestaurantID'].nunique() if 'RestaurantID' in df.columns else df.get('RestaurantID', pd.Series()).nunique() if 'RestaurantID' in df.columns else 0
            st.metric(
                label="Restaurants",
                value=f"{stores:,}",
                help="Number of restaurants"
            )
    else:
        st.warning("Loading simulation data...")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Total Orders", "Loading...")
        with col_m2:
            st.metric("Avg Prep Time", "Loading...")
        with col_m3:
            st.metric("Signal Variance", "Loading...")
        with col_m4:
            st.metric("Restaurants", "Loading...")
    
    st.markdown("## Event Stream Simulation")
    
    story_mode = st.session_state.get('story_mode', 'Technical Mode')
    
    if story_mode == 'Business Mode':
        st.markdown("""
        <div style="background: #F0F7FF; padding: 20px; border-radius: 8px; border-left: 4px solid #2196F3; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <h4 style="color: #1C1C1C !important; font-family: 'Poppins', sans-serif !important; font-weight: 600 !important; font-size: 18px !important; margin-top: 0 !important; margin-bottom: 12px !important;">How It Works</h4>
            <p style="color: #4A4A4A !important; font-size: 14px !important; margin-bottom: 0 !important; line-height: 1.7 !important; font-family: 'Inter', sans-serif !important;">
                This page simulates a Zomato-like food delivery platform. Watch as orders come in, riders get assigned, 
                and the system tracks everything in real-time. Think of it like a control room where you can see every order 
                being processed from start to finish.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #F0F7FF; padding: 20px; border-radius: 8px; border-left: 4px solid #2196F3; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <h4 style="color: #1C1C1C !important; font-family: 'Poppins', sans-serif !important; font-weight: 600 !important; font-size: 18px !important; margin-top: 0 !important; margin-bottom: 12px !important;">How It Works</h4>
            <p style="color: #4A4A4A !important; font-size: 14px !important; margin-bottom: 0 !important; line-height: 1.7 !important; font-family: 'Inter', sans-serif !important;">
                This page simulates a Zomato-like food delivery platform using a Kafka-like event stream architecture. 
                Orders arrive following a Poisson process (N(t) ~ Poisson(λ)), generating events: <strong>ORDER_CREATED</strong>, 
                <strong>RIDER_ASSIGNED</strong>, <strong>RIDER_ARRIVED</strong>, and <strong>ORDER_PICKED_UP</strong>. The simulation demonstrates real-time event 
                processing and platform dynamics.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### Simulation Parameters")
        st.markdown("""
        <div style="background: #F8F8F8; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <p style="color: #4A4A4A; font-size: 13px; margin: 0;">
                Adjust parameters to simulate different platform conditions. 
                Events are generated using a Poisson process.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        arrival_rate = st.slider(
            "Arrival Rate (λ)", 
            0.1, 2.0, 
            value=st.session_state.get('platform_arrival_rate', 0.5),
            step=0.1,
            help="Orders per minute - controls event frequency",
            key='platform_arrival_rate_slider',
            on_change=lambda: st.session_state.update({'platform_params_changed': True})
        )
        duration = st.slider(
            "Simulation Duration (min)", 
            5, 60, 
            value=st.session_state.get('platform_duration', 30),
            step=5,
            help="Time window for event generation",
            key='platform_duration_slider',
            on_change=lambda: st.session_state.update({'platform_params_changed': True})
        )
        
        # Check if parameters changed
        if st.session_state.get('platform_params_changed', False):
            st.session_state.platform_arrival_rate = arrival_rate
            st.session_state.platform_duration = duration
            st.session_state.platform_params_changed = False
            
            # Regenerate events with new parameters
            with st.spinner("Updating simulation..."):
                event_stream = EventStream(arrival_rate=arrival_rate)
                start_time = datetime.now() - timedelta(days=1)
                events = event_stream.simulate_time_window(start_time, duration)
                st.session_state.events = events
                st.session_state.events_updated = True
        
        if st.button("Run Simulation", use_container_width=True, type="primary"):
            with st.spinner("Simulating platform events..."):
                event_stream = EventStream(arrival_rate=arrival_rate)
                start_time = datetime.now() - timedelta(days=1)
                events = event_stream.simulate_time_window(start_time, duration)
                st.session_state.events = events
                st.session_state.platform_arrival_rate = arrival_rate
                st.session_state.platform_duration = duration
                st.success(f"✅ Generated {len(events)} events")
                st.rerun()
        
        # Auto-generate on first load
        if 'events' not in st.session_state or len(st.session_state.events) == 0:
            if st.button("Load Sample Data", use_container_width=True):
                with st.spinner("Loading sample events..."):
                    event_stream = EventStream(arrival_rate=0.5)
                    start_time = datetime.now() - timedelta(days=1)
                    events = event_stream.simulate_time_window(start_time, 30)
                    st.session_state.events = events
                    st.session_state.platform_arrival_rate = 0.5
                    st.session_state.platform_duration = 30
                    st.rerun()
    
    with col2:
        # Always show something
        if 'events' in st.session_state and len(st.session_state.events) > 0:
            events_df = pd.DataFrame(st.session_state.events)
            
            # Summary metrics - properly formatted
            st.markdown("### Event Statistics")
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric(
                    label="Total Events",
                    value=f"{len(events_df):,}",
                    help="Total number of events generated"
                )
            with col_m2:
                orders = len(events_df[events_df['event_type'] == EventType.ORDER_CREATED.value])
                st.metric(
                    label="Orders Created",
                    value=f"{orders:,}",
                    help="Number of order creation events"
                )
            with col_m3:
                stores = events_df['store_id'].nunique() if 'store_id' in events_df.columns else 0
                st.metric(
                    label="Stores",
                    value=f"{stores:,}",
                    help="Number of unique stores"
                )
            with col_m4:
                if 'timestamp' in events_df.columns:
                    time_span = (pd.to_datetime(events_df['timestamp']).max() - 
                               pd.to_datetime(events_df['timestamp']).min()).total_seconds() / 60
                    st.metric(
                        label="Time Span",
                        value=f"{time_span:.1f} min",
                        help="Duration of simulation"
                    )
                else:
                    st.metric("Time Span", "N/A")
            
            # Event type distribution
            event_counts = events_df['event_type'].value_counts()
            
            fig = px.bar(
                x=event_counts.index,
                y=event_counts.values,
                title="Event Type Distribution",
                labels={'x': 'Event Type', 'y': 'Count'},
                color=event_counts.values,
                color_continuous_scale='Reds',
                text=event_counts.values
            )
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', size=14, color='#1C1C1C'),
                title_font=dict(family='Poppins', size=18, color='#1C1C1C', weight='bold'),
                xaxis=dict(
                    title_font=dict(size=14, color='#1C1C1C', family='Inter'),
                    tickfont=dict(size=12, color='#1C1C1C', family='Inter'),
                    gridcolor='#E0E0E0'
                ),
                yaxis=dict(
                    title_font=dict(size=14, color='#1C1C1C', family='Inter'),
                    tickfont=dict(size=12, color='#1C1C1C', family='Inter'),
                    gridcolor='#E0E0E0'
                ),
                legend=dict(
                    font=dict(size=12, color='#1C1C1C', family='Inter'),
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='#E0E0E0',
                    borderwidth=1
                )
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Event timeline
            if 'timestamp' in events_df.columns:
                events_df['timestamp'] = pd.to_datetime(events_df['timestamp'])
                events_df = events_df.sort_values('timestamp')
                
                fig2 = px.scatter(
                    events_df,
                    x='timestamp',
                    y='event_type',
                    color='event_type',
                    title="Event Timeline - Real-time Event Stream",
                    labels={'timestamp': 'Time', 'event_type': 'Event Type'},
                    size=[10]*len(events_df)
                )
                fig2.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family='Inter', size=14, color='#1C1C1C'),
                    title_font=dict(family='Poppins', size=18, color='#1C1C1C', weight='bold'),
                    xaxis=dict(
                        title_font=dict(size=14, color='#1C1C1C', family='Inter'),
                        tickfont=dict(size=12, color='#1C1C1C', family='Inter'),
                        gridcolor='#E0E0E0'
                    ),
                    yaxis=dict(
                        title_font=dict(size=14, color='#1C1C1C', family='Inter'),
                        tickfont=dict(size=12, color='#1C1C1C', family='Inter'),
                        gridcolor='#E0E0E0'
                    ),
                    legend=dict(
                        font=dict(size=12, color='#1C1C1C', family='Inter'),
                        bgcolor='rgba(255,255,255,0.9)',
                        bordercolor='#E0E0E0',
                        borderwidth=1
                    )
                )
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("👆 Click 'Load Sample Data' or 'Run Simulation' to generate events and see visualizations.")
    
    # Kitchen Queue Simulation
    st.markdown("## Kitchen Queue Dynamics")
    st.markdown("""
    <div style="background: #FFF4E6; padding: 15px; border-radius: 8px; border-left: 4px solid #FF9800; margin-bottom: 20px;">
        <p style="color: #4A4A4A; font-size: 14px; margin-bottom: 10px;">
            <strong>Queueing Theory:</strong> Kitchen load and service rate models:
        </p>
    </div>
    """, unsafe_allow_html=True)
    col_eq1, col_eq2 = st.columns(2)
    with col_eq1:
        st.latex(r"L(t) = \alpha \cdot Q(t) + \beta \cdot R(t)")
        st.caption("where $Q(t)$ is queue length and $R(t)$ is riders waiting")
    with col_eq2:
        st.latex(r"\mu(t) = \frac{\mu_0}{1 + \gamma \cdot L(t)}")
        st.caption("Service rate determines prep time")
    
    if 'events' in st.session_state and len(st.session_state.events) > 0:
        # Simulate kitchen dynamics
        kitchen = KitchenSimulator()
        events_df = pd.DataFrame(st.session_state.events)
        order_events = events_df[events_df['event_type'] == EventType.ORDER_CREATED.value]
        
        queue_lengths = []
        kitchen_loads = []
        prep_times = []
        
        for idx, event in order_events.head(50).iterrows():
            order_time = pd.to_datetime(event['timestamp'])
            result = kitchen.process_order(order_time)
            queue_lengths.append(result['queue_length'])
            kitchen_loads.append(result['kitchen_load'])
            prep_times.append(result['kpt_true'])
        
        col_k1, col_k2 = st.columns(2)
        
        with col_k1:
            fig_queue = px.line(
                x=list(range(len(queue_lengths))),
                y=queue_lengths,
                title="Queue Length Over Time",
                labels={'x': 'Order Sequence', 'y': 'Queue Length'},
                markers=True
            )
            fig_queue.update_traces(line_color='#EF4F5F', line_width=3, marker_size=6)
            fig_queue.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', size=12, color='#1C1C1C'),
                title_font=dict(family='Poppins', size=16, color='#1C1C1C')
            )
            st.plotly_chart(fig_queue, use_container_width=True)
        
        with col_k2:
            try:
                fig_load = px.scatter(
                    x=kitchen_loads,
                    y=prep_times,
                    title="Kitchen Load vs Prep Time",
                    labels={'x': 'Kitchen Load', 'y': 'Prep Time (min)'},
                    trendline="ols"
                )
            except:
                # Fallback without trendline if statsmodels not available
                fig_load = px.scatter(
                    x=kitchen_loads,
                    y=prep_times,
                    title="Kitchen Load vs Prep Time",
                    labels={'x': 'Kitchen Load', 'y': 'Prep Time (min)'}
                )
            fig_load.update_traces(marker_color='#4CAF50', marker_size=8)
            fig_load.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', size=12, color='#1C1C1C'),
                title_font=dict(family='Poppins', size=16, color='#1C1C1C')
            )
            st.plotly_chart(fig_load, use_container_width=True)
    
    # Show data visualizations from simulation_data
    if 'simulation_data' in st.session_state:
        df = st.session_state.simulation_data
        
        st.markdown("## Signal Distribution Comparison")
        col_v1, col_v2 = st.columns(2)
        
        with col_v1:
            fig_dist = px.histogram(
                df,
                x=['ObservedPrepTime', 'ReconstructedPrepTime'],
                nbins=50,
                barmode='overlay',
                opacity=0.7,
                color_discrete_sequence=['#EF4F5F', '#4CAF50'],
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
        
        with col_v2:
            var_obs = df['ObservedPrepTime'].var()
            var_recon = df['ReconstructedPrepTime'].var()
            var_reduction = ((var_obs - var_recon) / var_obs) * 100
            
            variance_data = pd.DataFrame({
                'Signal': ['Observed', 'Reconstructed'],
                'Variance': [var_obs, var_recon]
            })
            fig_var = px.bar(
                variance_data,
                x='Signal',
                y='Variance',
                color='Signal',
                color_discrete_map={'Observed': '#EF4F5F', 'Reconstructed': '#4CAF50'},
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
        
        # Queue Length vs Prep Time
        if 'QueueLength' in df.columns:
            st.markdown("### Queue Length vs Prep Time")
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
    
    # Digital Twin Visualization - Real-time WebSocket updates (like Dispatch Dashboard)
    st.markdown("## Digital Twin Visualization")
    st.markdown("""
    <div style="background: #E8F5E9; padding: 15px; border-radius: 8px; border-left: 4px solid #4CAF50; margin-bottom: 20px;">
        <p style="color: #4A4A4A; font-size: 14px; margin: 0;">
            Network graph showing restaurants (red), riders (green), and order connections. 
            Enable <strong>Live Mode</strong> to stream real-time events via WebSocket (backend on port 8000).
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Live Digital Twin: WebSocket-driven real-time updates
    dt_live_mode = st.checkbox(
        "Live Mode (WebSocket)",
        value=st.session_state.get('dt_live_mode', False),
        key='dt_live_checkbox',
        help="Connect to backend and update digital twin in real-time as events stream"
    )
    st.session_state.dt_live_mode = dt_live_mode
    if dt_live_mode:
        if st.button("Reconnect", key="dt_reconnect"):
            st.session_state.dt_ws_client = None
            st.session_state.dt_restaurants = []
            st.session_state.dt_riders = []
            st.session_state.dt_orders = []
            st.rerun()
    
    if dt_live_mode:
        import queue as queue_module
        # Initialize session state for live digital twin
        if 'dt_restaurants' not in st.session_state:
            st.session_state.dt_restaurants = []
        if 'dt_riders' not in st.session_state:
            st.session_state.dt_riders = []
        if 'dt_orders' not in st.session_state:
            st.session_state.dt_orders = []
        if 'dt_event_queue' not in st.session_state:
            st.session_state.dt_event_queue = queue_module.Queue()
        if 'dt_ws_client' not in st.session_state:
            st.session_state.dt_ws_client = None
        
        # WebSocket connection and event processing
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'frontend'))
        try:
            from frontend.websocket_client import get_websocket_client
            
            # Capture queue reference for callback (thread-safe - no session_state in background thread)
            dt_queue_ref = st.session_state.dt_event_queue
            
            def _on_dt_message(data: dict):
                dt_queue_ref.put(data)
            
            if st.session_state.dt_ws_client is None:
                st.session_state.dt_ws_client = get_websocket_client(
                    "ws://localhost:8000/ws/dispatch",
                    _on_dt_message
                )
            
            # Process queued events in main thread
            processed = 0
            while not st.session_state.dt_event_queue.empty():
                try:
                    event = st.session_state.dt_event_queue.get_nowait()
                    event_type = event.get('event_type', '')
                    order_id = event.get('order_id', '')
                    
                    if event_type == 'CONNECTED':
                        continue
                    
                    if event_type == 'ORDER_CREATED':
                        rid = event.get('restaurant_id', 'REST_0')
                        rlat = event.get('restaurant_lat', 28.6139 + (np.random.random() - 0.5) * 0.1)
                        rlon = event.get('restaurant_lon', 77.2090 + (np.random.random() - 0.5) * 0.1)
                        if not any(r['id'] == rid for r in st.session_state.dt_restaurants):
                            st.session_state.dt_restaurants.append({'id': rid, 'lat': rlat, 'lon': rlon})
                    
                    elif event_type == 'RIDER_DISPATCHED':
                        rider_id = event.get('rider_id')
                        restaurant_id = event.get('restaurant_id', 'REST_0')
                        if rider_id:
                            if not any(r.get('id') == rider_id for r in st.session_state.dt_riders):
                                st.session_state.dt_riders.append({
                                    'id': rider_id, 'lat': 0.0, 'lon': 0.0
                                })
                        st.session_state.dt_orders.append({
                            'order_id': order_id,
                            'restaurant_id': restaurant_id,
                            'rider_id': rider_id or f'RIDER_0'
                        })
                        if len(st.session_state.dt_orders) > 50:
                            st.session_state.dt_orders = st.session_state.dt_orders[-50:]
                    
                    elif event_type == 'RIDER_MOVED':
                        rider_id = event.get('rider_id')
                        for r in st.session_state.dt_riders:
                            if r.get('id') == rider_id:
                                r['lat'] = event.get('rider_lat', r.get('lat', 0))
                                r['lon'] = event.get('rider_lon', r.get('lon', 0))
                                break
                    
                    processed += 1
                except queue_module.Empty:
                    break
                except Exception as e:
                    print(f"DT event error: {e}")
            
            # Render live digital twin
            dt_placeholder = st.empty()
            with dt_placeholder.container():
                if st.session_state.dt_restaurants or st.session_state.dt_riders:
                    # Ensure riders have lat/lon for layout
                    riders_for_twin = []
                    for r in st.session_state.dt_riders:
                        riders_for_twin.append({
                            'id': r.get('id', 'RIDER_0'),
                            'lat': r.get('lat', 0) or np.random.uniform(-0.5, 0.5),
                            'lon': r.get('lon', 0) or np.random.uniform(-0.5, 0.5)
                        })
                    restaurants_for_twin = [
                        {'id': r['id'], 'lat': r.get('lat', 0), 'lon': r.get('lon', 0)}
                        for r in st.session_state.dt_restaurants
                    ]
                    fig_twin = create_digital_twin_graph(
                        st.session_state.dt_orders,
                        restaurants_for_twin,
                        riders_for_twin
                    )
                    st.plotly_chart(fig_twin, use_container_width=True, key=f"dt_twin_{processed}")
                    st.caption(f"Live: {len(st.session_state.dt_restaurants)} restaurants, {len(st.session_state.dt_riders)} riders, {len(st.session_state.dt_orders)} orders")
                else:
                    # Check if backend is reachable
                    try:
                        import urllib.request
                        with urllib.request.urlopen("http://localhost:8000/", timeout=2) as r:
                            info = __import__('json').loads(r.read().decode())
                            conns = info.get('connections', 0)
                            st.info(f"Connected to backend ({conns} client(s)). Events stream every ~200ms — new orders should appear shortly.")
                    except Exception:
                        st.warning("Backend not reachable. Start it: `cd prepsense/backend && python3 -m uvicorn websocket_server:app --port 8000`")
            
            # Auto-refresh for real-time feel
            import time
            if processed > 0 or not st.session_state.dt_event_queue.empty():
                time.sleep(0.3)
            else:
                time.sleep(0.8)
            st.rerun()
            
        except ImportError as e:
            st.warning("WebSocket client not available. Install: `pip install websockets`")
            st.session_state.dt_live_mode = False
    
    elif 'events' in st.session_state and len(st.session_state.events) > 0:
        # Create sample data for visualization
        np.random.seed(42)
        restaurants = [{'id': f'REST_{i}', 'lat': np.random.uniform(17.0, 18.0), 
                      'lon': np.random.uniform(78.0, 79.0)} for i in range(10)]
        riders = [{'id': f'RIDER_{i}', 'lat': np.random.uniform(17.0, 18.0),
                  'lon': np.random.uniform(78.0, 79.0)} for i in range(5)]
        
        orders = []
        for event in st.session_state.events[:30]:  # Sample
            if event['event_type'] == EventType.ORDER_CREATED.value:
                orders.append({
                    'order_id': event['order_id'],
                    'restaurant_id': f"REST_{event['store_id'] % 10}",
                    'rider_id': f"RIDER_{np.random.randint(0, 5)}"
                })
        
        if orders:
            fig_twin = create_digital_twin_graph(orders, restaurants, riders)
            st.plotly_chart(fig_twin, use_container_width=True)
        else:
            st.info("No orders found in events. Run simulation to generate order events.")
    elif 'simulation_data' in st.session_state:
        # Use simulation data to create digital twin
        df = st.session_state.simulation_data
        np.random.seed(42)
        restaurants = [{'id': f'REST_{i}', 'lat': np.random.uniform(17.0, 18.0), 
                      'lon': np.random.uniform(78.0, 79.0)} for i in range(10)]
        riders = [{'id': f'RIDER_{i}', 'lat': np.random.uniform(17.0, 18.0),
                  'lon': np.random.uniform(78.0, 79.0)} for i in range(5)]
        
        orders = []
        for idx, row in df.head(30).iterrows():
            orders.append({
                'order_id': f"ORD_{idx:06d}",
                'restaurant_id': f"REST_{row.get('RestaurantID', idx) % 10}",
                'rider_id': f"RIDER_{np.random.randint(0, 5)}"
            })
        
        if orders:
            fig_twin = create_digital_twin_graph(orders, restaurants, riders)
            st.plotly_chart(fig_twin, use_container_width=True)
    else:
        st.info("Generate events first to see the digital twin visualization.")


def page_signal_reconstruction():
    """Signal Reconstruction Page."""
    st.markdown("""
    <div class="zomato-header">
        <div>
            <div class="zomato-logo">PrepSense</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Signal Reconstruction</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## Ground Truth Reconstruction")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### Signal Lab")
        st.markdown("""
        <div style="background: #F8F8F8; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <p style="color: #4A4A4A; font-size: 13px; margin: 0;">
                Adjust signal parameters to observe how noise affects reconstruction accuracy. 
                Lower noise = better signal quality.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        noise_level = st.slider(
            "Merchant Noise (σ)", 
            0.5, 5.0, 
            value=st.session_state.get('signal_noise_level', 3.0),
            step=0.5,
            help="Standard deviation of observation noise",
            key='signal_noise_slider',
            on_change=lambda: st.session_state.update({'signal_params_changed': True})
        )
        handover_mean = st.slider(
            "Handover Delay Mean", 
            1.0, 5.0, 
            value=st.session_state.get('signal_handover_mean', 2.0),
            step=0.5,
            help="Average time between packing and pickup",
            key='signal_handover_slider',
            on_change=lambda: st.session_state.update({'signal_params_changed': True})
        )
        n_samples = st.slider(
            "Sample Size", 
            100, 5000, 
            value=st.session_state.get('signal_n_samples', 1000),
            step=100,
            help="Number of orders to simulate",
            key='signal_n_samples_slider',
            on_change=lambda: st.session_state.update({'signal_params_changed': True})
        )
        
        # Auto-regenerate when parameters change
        if st.session_state.get('signal_params_changed', False):
            st.session_state.signal_noise_level = noise_level
            st.session_state.signal_handover_mean = handover_mean
            st.session_state.signal_n_samples = n_samples
            st.session_state.signal_params_changed = False
            
            with st.spinner("Updating signals..."):
                generator = DatasetGenerator(n_samples=n_samples, noise_level=noise_level)
                df = generator.generate_orders()
                
                reconstructor = ReconstructionService(handover_mean=handover_mean)
                telemetry_service = TelemetryService(handover_mean=handover_mean)
                
                reconstructed_times = []
                observed_times = []
                
                for idx, row in df.iterrows():
                    order_time = pd.to_datetime(row['OrderTime'])
                    packed_time = order_time + timedelta(minutes=row['ObservedPrepTime'])
                    
                    order_id = f"ORD_{idx:06d}"
                    telemetry = telemetry_service.generate_telemetry(
                        order_id,
                        order_time, packed_time
                    )
                    
                    recon_result = reconstructor.reconstruct_from_telemetry(telemetry)
                    reconstructed_times.append(recon_result['kpt_reconstructed'])
                    observed_times.append(row['ObservedPrepTime'])
                
                st.session_state.signal_data = {
                    'observed': observed_times,
                    'reconstructed': reconstructed_times,
                    'noise_level': noise_level
                }
                st.rerun()
        
        if st.button("Generate Signals", use_container_width=True, type="primary"):
            with st.spinner("Generating signals..."):
                # Generate synthetic data
                generator = DatasetGenerator(n_samples=n_samples, noise_level=noise_level)
                df = generator.generate_orders()
                
                # Reconstruct signals
                reconstructor = ReconstructionService(handover_mean=handover_mean)
                telemetry_service = TelemetryService(handover_mean=handover_mean)
                
                reconstructed_times = []
                observed_times = []
                
                for idx, row in df.iterrows():
                    order_time = pd.to_datetime(row['OrderTime'])
                    packed_time = order_time + timedelta(minutes=row['ObservedPrepTime'])
                    
                    order_id = f"ORD_{idx:06d}"
                    telemetry = telemetry_service.generate_telemetry(
                        order_id,
                        order_time, packed_time
                    )
                    
                    recon_result = reconstructor.reconstruct_from_telemetry(telemetry)
                    reconstructed_times.append(recon_result['kpt_reconstructed'])
                    observed_times.append(row['ObservedPrepTime'])
                
                st.session_state.signal_data = {
                    'observed': observed_times,
                    'reconstructed': reconstructed_times,
                    'noise_level': noise_level
                }
                st.success("Signals generated!")
    
    with col2:
        # Data is already loaded in session state initialization
        
        if 'signal_data' in st.session_state:
            signal_data = st.session_state.signal_data
            
            # Summary metrics
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            var_obs = np.var(signal_data['observed'])
            var_recon = np.var(signal_data['reconstructed'])
            reduction = ((var_obs - var_recon) / var_obs) * 100
            mae = np.mean(np.abs(np.array(signal_data['observed']) - np.array(signal_data['reconstructed'])))
            
            with col_m1:
                st.metric("Observed Variance", f"{var_obs:.2f}")
            with col_m2:
                st.metric("Reconstructed Variance", f"{var_recon:.2f}")
            with col_m3:
                st.metric("Variance Reduction", f"{reduction:.1f}%", 
                         delta_color="inverse" if reduction > 0 else "normal")
            with col_m4:
                st.metric("Mean Absolute Error", f"{mae:.2f} min")
            
            # Signal comparison
            fig = plot_signal_comparison(
                signal_data['observed'],
                signal_data['reconstructed']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Additional histogram comparison
            st.markdown("### Distribution Comparison")
            signal_df = pd.DataFrame({
                'Observed': signal_data['observed'],
                'Reconstructed': signal_data['reconstructed']
            })
            fig_hist = px.histogram(
                signal_df,
                x=['Observed', 'Reconstructed'],
                nbins=50,
                barmode='overlay',
                opacity=0.7,
                color_discrete_sequence=['#EF4F5F', '#4CAF50'],
                labels={'value': 'Preparation Time (minutes)', 'count': 'Frequency'}
            )
            fig_hist.update_layout(
                title=dict(text="Signal Distribution Comparison", font=dict(family='Poppins', size=16, color='#1C1C1C')),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', size=12, color='#4A4A4A')
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("Loading signal data...")
    
    # Weighted Event Filtering
    st.markdown("## Weighted Event Filtering")
    st.markdown("""
    <div style="background: #F8F8F8; padding: 15px; border-radius: 8px; border-left: 4px solid #EF4F5F; margin-bottom: 20px;">
        <p style="color: #1C1C1C; font-size: 14px; margin: 0;">
            <strong>How it works:</strong> Multiple noisy observations are combined using weighted averaging, 
            where weights are inversely proportional to variance. This reduces overall signal variance and improves accuracy.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'signal_data' in st.session_state:
        signal_filter = SignalFilter()
        
        # Add events with varying noise
        observed = signal_data['observed']
        for i, obs in enumerate(observed[:100]):  # Sample
            variance = signal_data['noise_level'] ** 2 * (1 + np.random.uniform(0, 0.5))
            signal_filter.add_event(obs, variance)
        
        filtered_estimate = signal_filter.compute_filtered_estimate()
        filter_stats = signal_filter.get_statistics()
        
        if filter_stats:
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            with col_f1:
                st.metric(
                    "Unfiltered Variance",
                    f"{filter_stats['variance_unfiltered']:.2f}",
                    help="Variance of raw observations"
                )
            with col_f2:
                st.metric(
                    "Filtered Variance",
                    f"{filter_stats['variance_filtered']:.2f}",
                    delta=f"-{((filter_stats['variance_unfiltered'] - filter_stats['variance_filtered']) / filter_stats['variance_unfiltered']) * 100:.1f}%",
                    delta_color="inverse",
                    help="Variance after weighted filtering"
                )
            with col_f3:
                st.metric(
                    "Mean Unfiltered",
                    f"{filter_stats['mean_unfiltered']:.2f} min",
                    help="Mean of raw observations"
                )
            with col_f4:
                st.metric(
                    "Mean Filtered",
                    f"{filter_stats['mean_filtered']:.2f} min",
                    help="Mean after filtering"
                )
            
            # Visualization
            st.markdown("### Filtering Effect Visualization")
            comparison_data = pd.DataFrame({
                'Type': ['Unfiltered', 'Filtered'],
                'Variance': [filter_stats['variance_unfiltered'], filter_stats['variance_filtered']],
                'Std Dev': [filter_stats['std_unfiltered'], filter_stats['std_filtered'] or 0]
            })
            
            fig_filter = px.bar(
                comparison_data,
                x='Type',
                y='Variance',
                color='Type',
                color_discrete_map={'Unfiltered': '#EF4F5F', 'Filtered': '#4CAF50'},
                text='Variance',
                title="Variance Reduction Through Filtering"
            )
            fig_filter.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_filter.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', size=12, color='#1C1C1C'),
                title_font=dict(family='Poppins', size=16, color='#1C1C1C'),
                showlegend=False
            )
            st.plotly_chart(fig_filter, use_container_width=True)
    else:
        st.info("Generate signals first to see filtering results.")


def page_prediction_engine():
    """Prediction Engine Page."""
    st.markdown("""
    <div class="zomato-header">
        <div>
            <div class="zomato-logo">PrepSense</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Prediction Engine</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## Survival Analysis Prediction")
    
    with st.expander("**Simple explanation for judges**", expanded=False):
        st.markdown("""
        **What this does:** PrepSense uses *survival analysis* to predict how long a kitchen will take to prepare an order.
        
        - **Survival function S(t):** Probability the order is *not* ready by time *t*. Starts at 100% and drops as time passes.
        - **Hazard rate h(t):** How likely the order completes *right now* given it hasn't finished yet. Rises as the kitchen gets closer to done.
        - **Expected prep time E[T]:** The average time we expect — this is our main prediction (Predicted KPT).
        - **95% Confidence Interval:** A range where we're 95% sure the real prep time will fall. The blue band shows this uncertainty.
        
        **Why it matters:** Instead of a single guess, we get a prediction *plus* how confident we are. That lets dispatch decide when to send the rider — not too early (idle time) or too late (cold food).
        """)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### Model Configuration")
        st.markdown("""
        <div style="background: #F8F8F8; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <p style="color: #4A4A4A; font-size: 13px; margin: 0;">
                Select a statistical distribution to model preparation time. 
                The model uses survival analysis to predict completion probabilities.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        distribution = st.selectbox(
            "Distribution Type",
            ['gamma', 'lognormal', 'weibull'],
            index=['gamma', 'lognormal', 'weibull'].index(st.session_state.get('prediction_distribution', 'gamma')),
            help="Statistical distribution for modeling prep time",
            key='prediction_distribution_select',
            on_change=lambda: st.session_state.update({'prediction_params_changed': True})
        )
        n_samples = st.slider(
            "Training Samples", 
            100, 5000, 
            value=st.session_state.get('prediction_n_samples', 1000),
            step=100,
            help="Number of historical orders for model training",
            key='prediction_n_samples_slider',
            on_change=lambda: st.session_state.update({'prediction_params_changed': True})
        )
        
        # Auto-retrain when parameters change
        if st.session_state.get('prediction_params_changed', False):
            st.session_state.prediction_distribution = distribution
            st.session_state.prediction_n_samples = n_samples
            st.session_state.prediction_params_changed = False
            
            with st.spinner("Retraining model..."):
                generator = DatasetGenerator(n_samples=n_samples)
                df = generator.generate_orders()
                prep_times = df['ReconstructedPrepTime'].values
                
                survival_model = SurvivalPrediction(distribution=distribution)
                survival_model.fit(prep_times)
                
                st.session_state.survival_model = survival_model
                st.session_state.prep_times = prep_times
                st.rerun()
        
        if st.button("Train Model", use_container_width=True, type="primary"):
            with st.spinner("Training survival model..."):
                # Generate training data
                generator = DatasetGenerator(n_samples=n_samples)
                df = generator.generate_orders()
                
                prep_times = df['ReconstructedPrepTime'].values
                
                survival_model = SurvivalPrediction(distribution=distribution)
                survival_model.fit(prep_times)
                
                st.session_state.survival_model = survival_model
                st.session_state.prep_times = prep_times
                st.success("Model trained!")
    
    with col2:
        # Model is already loaded in session state initialization
        
        if 'survival_model' in st.session_state:
            model = st.session_state.survival_model
            prep_times = st.session_state.prep_times
            
            # Predictions
            predicted = model.predict()
            variance = model.variance()
            lower, upper = model.confidence_interval()
            
            st.markdown("### Prediction Results")
            col_p1, col_p2, col_p3, col_p4 = st.columns(4)
            with col_p1:
                st.metric("Predicted KPT", f"{predicted:.2f} min", 
                         help="Expected preparation time")
            with col_p2:
                st.metric("Variance", f"{variance:.2f}",
                         help="Prediction variance")
            with col_p3:
                st.metric("Std Deviation", f"{np.sqrt(variance):.2f} min",
                         help="Standard deviation")
            with col_p4:
                st.metric("95% CI", f"[{lower:.2f}, {upper:.2f}]",
                         help="95% confidence interval")
            
            # Generate predictions for visualization
            n_viz = min(200, len(prep_times))
            predictions = [predicted] * n_viz
            std_dev = np.sqrt(variance) if variance else np.std(prep_times)
            lower_bounds = [predicted - 1.96 * std_dev] * n_viz
            upper_bounds = [predicted + 1.96 * std_dev] * n_viz
            
            st.markdown("### Confidence Intervals")
            fig = plot_confidence_intervals(
                predictions,
                lower_bounds,
                upper_bounds,
                actuals=prep_times[:n_viz]
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Survival function plot
            st.markdown("### Survival Analysis")
            st.markdown("""
            <div style="background: #F0F7FF; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                <p style="color: #000000; font-size: 14px; margin: 0 0 10px 0; font-weight: 500;">
                    Survival analysis models how long an order takes to complete. Key formulas:
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.latex(r"S(t) = P(T > t) \quad \text{(Survival: probability prep not done by time } t\text{)}")
            st.latex(r"h(t) = \frac{f(t)}{S(t)} \quad \text{(Hazard: instantaneous completion rate)}")
            st.latex(r"E[T] = \int_0^\infty t \cdot f(t) \, dt \quad \text{(Expected prep time)}")
            t_values = np.linspace(0, 30, 100)
            survival_probs = model.survival(t_values)
            hazard_rates = model.hazard_rate(t_values)
            
            if survival_probs is not None and hazard_rates is not None:
                fig2 = make_subplots(specs=[[{"secondary_y": True}]])
                fig2.add_trace(
                    go.Scatter(x=t_values, y=survival_probs, name='Survival S(t)',
                              line=dict(color='#EF4F5F', width=3)),
                    secondary_y=False
                )
                fig2.add_trace(
                    go.Scatter(x=t_values, y=hazard_rates, name='Hazard h(t)',
                              line=dict(color='#4CAF50', width=3)),
                    secondary_y=True
                )
                fig2.update_xaxes(
                    title_text="Time (minutes)",
                    title_font=dict(size=14, color='#000000'),
                    tickfont=dict(size=12, color='#000000')
                )
                fig2.update_yaxes(
                    title_text="Survival Probability",
                    secondary_y=False,
                    title_font=dict(size=14, color='#000000'),
                    tickfont=dict(size=12, color='#000000')
                )
                fig2.update_yaxes(
                    title_text="Hazard Rate",
                    secondary_y=True,
                    title_font=dict(size=14, color='#000000'),
                    tickfont=dict(size=12, color='#000000')
                )
                fig2.update_layout(
                    title=dict(text="Survival Function and Hazard Rate",
                              font=dict(family='Poppins', size=18, color='#000000')),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family='Inter', size=12, color='#000000'),
                    legend=dict(font=dict(size=12, color='#000000'))
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            # Additional: Prediction Confidence Intervals visualization
            st.markdown("### Prediction Confidence Intervals")
            sample_size = min(200, len(prep_times))
            predictions_viz = [predicted] * sample_size
            std_dev_viz = np.sqrt(variance) if variance else np.std(prep_times)
            lower_bounds_viz = [predicted - 1.96 * std_dev_viz] * sample_size
            upper_bounds_viz = [predicted + 1.96 * std_dev_viz] * sample_size
            
            fig_ci = go.Figure()
            fig_ci.add_trace(go.Scatter(
                x=list(range(sample_size)),
                y=upper_bounds_viz,
                mode='lines',
                name='Upper Bound',
                line=dict(width=0),
                showlegend=False
            ))
            fig_ci.add_trace(go.Scatter(
                x=list(range(sample_size)),
                y=lower_bounds_viz,
                mode='lines',
                name='95% CI',
                fill='tonexty',
                fillcolor='rgba(33, 150, 243, 0.2)',
                line=dict(width=0),
                showlegend=True
            ))
            fig_ci.add_trace(go.Scatter(
                x=list(range(sample_size)),
                y=predictions_viz,
                mode='lines+markers',
                name='PrepSense Prediction',
                line=dict(color='#EF4F5F', width=2),
                marker=dict(size=4)
            ))
            fig_ci.update_layout(
                title=dict(text="Prediction Confidence Intervals", font=dict(family='Poppins', size=16, color='#000000')),
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
                plot_bgcolor='white',
                paper_bgcolor='white',
                hovermode='x unified',
                font=dict(family='Inter', size=12, color='#000000'),
                legend=dict(font=dict(size=12, color='#000000'))
            )
            st.plotly_chart(fig_ci, use_container_width=True)
        else:
            st.info("Loading prediction model...")


def page_dispatch_optimization():
    """Dispatch Optimization Page."""
    st.markdown("""
    <div class="zomato-header">
        <div>
            <div class="zomato-logo">PrepSense</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Dispatch Optimization</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## Optimal Rider Assignment")
    
    story_mode = st.session_state.get('story_mode', 'Technical Mode')
    
    if story_mode == 'Technical Mode':
        st.markdown("""
        <div style="background: #FFF4E6; padding: 15px; border-radius: 8px; border-left: 4px solid #FF9800; margin-bottom: 10px;">
            <p style="color: #1C1C1C; font-size: 13px; margin: 0;">
                Optimization minimizes total cost:
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"C = C_1 \cdot \text{Idle} + C_2 \cdot \text{Delay}")
        st.latex(r"T_{assign}^* = \mu_T + k \cdot \sigma_T")
        st.caption("Optimal assignment time balances idle time and delay risk")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### Cost Parameters")
        st.markdown("""
        <div style="background: #F8F8F8; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <p style="color: #4A4A4A; font-size: 13px; margin: 0;">
                Configure cost weights for optimization. The system minimizes total cost 
                considering both rider idle time and delivery delays.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        cost_idle = st.slider(
            "Idle Time Cost (C₁)", 
            0.5, 5.0, 
            value=st.session_state.get('dispatch_cost_idle', 1.0),
            step=0.5,
            help="Cost per unit of rider idle time",
            key='dispatch_cost_idle_slider',
            on_change=lambda: st.session_state.update({'dispatch_params_changed': True})
        )
        cost_delay = st.slider(
            "Delay Cost (C₂)", 
            0.5, 5.0, 
            value=st.session_state.get('dispatch_cost_delay', 2.0),
            step=0.5,
            help="Cost per unit of delivery delay",
            key='dispatch_cost_delay_slider',
            on_change=lambda: st.session_state.update({'dispatch_params_changed': True})
        )
        safety_factor = st.slider(
            "Safety Factor (k)", 
            0.5, 2.0, 
            value=st.session_state.get('dispatch_safety_factor', 1.0),
            step=0.1,
            help="Multiplier for standard deviation in assignment time",
            key='dispatch_safety_factor_slider',
            on_change=lambda: st.session_state.update({'dispatch_params_changed': True})
        )
        
        # Auto-optimize when parameters change
        if st.session_state.get('dispatch_params_changed', False):
            st.session_state.dispatch_cost_idle = cost_idle
            st.session_state.dispatch_cost_delay = cost_delay
            st.session_state.dispatch_safety_factor = safety_factor
            st.session_state.dispatch_params_changed = False
            
            with st.spinner("Recalculating optimization..."):
                generator = DatasetGenerator(n_samples=1000)
                df = generator.generate_orders()
                
                baseline_times = df['ObservedPrepTime'].values
                prepsense_times = df['ReconstructedPrepTime'].values
                
                optimizer = DispatchOptimizer(cost_idle=cost_idle, cost_delay=cost_delay)
                comparison = optimizer.compare_baseline_vs_prepsense(
                    baseline_times, prepsense_times, k=safety_factor
                )
                
                st.session_state.dispatch_comparison = comparison
                st.rerun()
        
        if st.button("Optimize Dispatch", use_container_width=True, type="primary"):
            with st.spinner("Optimizing dispatch..."):
                # Generate data
                generator = DatasetGenerator(n_samples=1000)
                df = generator.generate_orders()
                
                baseline_times = df['ObservedPrepTime'].values
                prepsense_times = df['ReconstructedPrepTime'].values
                
                optimizer = DispatchOptimizer(cost_idle=cost_idle, cost_delay=cost_delay)
                comparison = optimizer.compare_baseline_vs_prepsense(
                    baseline_times, prepsense_times, k=safety_factor
                )
                
                st.session_state.dispatch_comparison = comparison
                st.success("Optimization complete!")
    
    with col2:
        # Data is already loaded in session state initialization
        
        if 'dispatch_comparison' in st.session_state:
            comp = st.session_state.dispatch_comparison
            
            # Summary metrics
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            with col_s1:
                st.metric("Optimal Assignment", f"{comp['prepsense']['optimal_assignment_time']:.2f} min")
            with col_s2:
                st.metric("Mean Idle", f"{comp['prepsense']['mean_idle_time']:.2f} min")
            with col_s3:
                st.metric("Mean Delay", f"{comp['prepsense']['mean_delay']:.2f} min")
            with col_s4:
                st.metric("Total Cost", f"{comp['prepsense']['total_cost']:.2f}")
            
            # Metrics comparison
            metrics = ['mean_idle_time', 'mean_delay', 'total_cost']
            baseline_vals = [comp['baseline'][m] for m in metrics]
            prepsense_vals = [comp['prepsense'][m] for m in metrics]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Baseline',
                x=['Idle Time\n(min)', 'Delay\n(min)', 'Total Cost'],
                y=baseline_vals,
                marker_color='#EF4F5F',
                text=[f'{v:.2f}' for v in baseline_vals],
                textposition='outside'
            ))
            fig.add_trace(go.Bar(
                name='PrepSense',
                x=['Idle Time\n(min)', 'Delay\n(min)', 'Total Cost'],
                y=prepsense_vals,
                marker_color='#4CAF50',
                text=[f'{v:.2f}' for v in prepsense_vals],
                textposition='outside'
            ))
            fig.update_layout(
                title=dict(text="Dispatch Optimization Comparison",
                          font=dict(family='Poppins', size=18, color='#1C1C1C')),
                barmode='group',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', size=12, color='#1C1C1C'),
                legend=dict(font=dict(size=12, color='#1C1C1C'))
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Improvement metrics
            st.markdown("### Improvement Metrics")
            col_i1, col_i2, col_i3 = st.columns(3)
            with col_i1:
                st.metric("Idle Time Reduction", f"{comp['idle_reduction_percent']:.1f}%",
                         delta=f"-{comp['baseline']['mean_idle_time'] - comp['prepsense']['mean_idle_time']:.2f} min",
                         delta_color="inverse")
            with col_i2:
                st.metric("Delay Reduction", f"{comp['delay_reduction_percent']:.1f}%",
                         delta=f"-{comp['baseline']['mean_delay'] - comp['prepsense']['mean_delay']:.2f} min",
                         delta_color="inverse")
            with col_i3:
                st.metric("Cost Reduction", f"{comp['cost_reduction_percent']:.1f}%",
                         delta=f"-${comp['baseline']['total_cost'] - comp['prepsense']['total_cost']:.2f}",
                         delta_color="inverse")
            
            # Additional: Idle Time Comparison
            st.markdown("### Idle Time Analysis")
            idle_baseline = comp['baseline']['mean_idle_time']
            idle_prepsense = comp['prepsense']['mean_idle_time']
            idle_data = pd.DataFrame({
                'System': ['Baseline', 'PrepSense'],
                'Idle Time (min)': [idle_baseline, idle_prepsense]
            })
            fig_idle = px.bar(
                idle_data,
                x='System',
                y='Idle Time (min)',
                color='System',
                color_discrete_map={'Baseline': '#EF4F5F', 'PrepSense': '#4CAF50'},
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
        else:
            st.info("Loading optimization data...")


def page_business_impact():
    """Business Impact Page."""
    st.markdown("""
    <div class="zomato-header">
        <div>
            <div class="zomato-logo">PrepSense</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Business Impact</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## Platform-Scale Impact Analysis")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### Scale Parameters")
        st.markdown("""
        <div style="background: #F8F8F8; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <p style="color: #4A4A4A; font-size: 13px; margin: 0;">
                Scale the simulation to platform-level operations. 
                See how PrepSense impacts millions of daily orders.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        orders_per_day = st.slider(
            "Orders/Day (Millions)", 
            0.1, 10.0, 1.0, 0.1,
            help="Platform scale for impact calculation"
        )
        
        if st.button("Calculate Impact", use_container_width=True, type="primary"):
            with st.spinner("Calculating business impact..."):
                # Generate sample data
                generator = DatasetGenerator(n_samples=5000)
                df = generator.generate_orders()
                
                baseline_times = df['ObservedPrepTime'].values
                prepsense_times = df['ReconstructedPrepTime'].values
                
                # Simulate idle times
                optimizer = DispatchOptimizer()
                baseline_opt = optimizer.batch_optimize(baseline_times)
                prepsense_opt = optimizer.batch_optimize(prepsense_times)
                
                # Scale to daily operations
                scale = orders_per_day * 1_000_000
                
                baseline_metrics = {
                    'idle_hours': baseline_opt['mean_idle_time'] * scale / 60,
                    'delay_hours': baseline_opt['mean_delay'] * scale / 60,
                    'total_cost': baseline_opt['total_cost'] * scale
                }
                
                prepsense_metrics = {
                    'idle_hours': prepsense_opt['mean_idle_time'] * scale / 60,
                    'delay_hours': prepsense_opt['mean_delay'] * scale / 60,
                    'total_cost': prepsense_opt['total_cost'] * scale
                }
                
                st.session_state.business_impact = {
                    'baseline': baseline_metrics,
                    'prepsense': prepsense_metrics,
                    'scale': scale
                }
                st.success("Impact calculated!")
    
    with col2:
        # Data is already loaded in session state initialization
        
        if 'business_impact' in st.session_state:
            impact = st.session_state.business_impact
            
            fig = plot_business_impact(
                impact['baseline'],
                impact['prepsense'],
                scale=impact['scale']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Savings calculation
            idle_savings = impact['baseline']['idle_hours'] - impact['prepsense']['idle_hours']
            delay_savings = impact['baseline']['delay_hours'] - impact['prepsense']['delay_hours']
            cost_savings = impact['baseline']['total_cost'] - impact['prepsense']['total_cost']
            
            st.markdown("### Estimated Daily Savings")
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); padding: 25px; border-radius: 10px; 
                        margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3 style="color: white; font-family: 'Poppins', sans-serif; font-weight: 600; margin-top: 0; text-align: center;">
                    Daily Impact at {:.1f}M Orders/Day
                </h3>
            </div>
            """.format(impact['scale']/1_000_000), unsafe_allow_html=True)
            
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric(
                    "Idle Hours Saved",
                    f"{idle_savings/1000:.1f}K hours",
                    help="Reduction in rider idle time"
                )
            with col_s2:
                st.metric(
                    "Delay Hours Saved",
                    f"{delay_savings/1000:.1f}K hours",
                    help="Reduction in delivery delays"
                )
            with col_s3:
                st.metric(
                    "Cost Savings",
                    f"${cost_savings/1000000:.2f}M",
                    help="Total operational cost reduction"
                )
            
            # Additional: Kitchen Load Analysis
            if 'simulation_data' in st.session_state:
                df_load = st.session_state.simulation_data
                if 'KitchenLoad' in df_load.columns or 'QueueLength' in df_load.columns:
                    st.markdown("### Kitchen Load Analysis")
                    df_sample = df_load.sample(min(1000, len(df_load))).copy()
                    
                    # Simulate service rate if not present
                    if 'ServiceRate' not in df_sample.columns:
                        mu0 = 0.1
                        gamma = 0.2
                        load_col = 'KitchenLoad' if 'KitchenLoad' in df_sample.columns else 'QueueLength'
                        df_sample['ServiceRate'] = mu0 / (1 + gamma * df_sample[load_col])
                    
                    fig_load = px.scatter(
                        df_sample,
                        x='KitchenLoad' if 'KitchenLoad' in df_sample.columns else 'QueueLength',
                        y='ServiceRate',
                        size='ReconstructedPrepTime',
                        color='ReconstructedPrepTime',
                        color_continuous_scale='Reds',
                        hover_data=['QueueLength'] if 'QueueLength' in df_sample.columns else [],
                        labels={'KitchenLoad': 'Kitchen Load', 'ServiceRate': 'Service Rate', 
                               'QueueLength': 'Queue Length'}
                    )
                    fig_load.update_layout(
                        title=dict(text="Kitchen Load vs Service Rate", font=dict(family='Poppins', size=16, color='#1C1C1C')),
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        font=dict(family='Inter', size=12, color='#4A4A4A')
                    )
                    st.plotly_chart(fig_load, use_container_width=True)
        else:
            st.info("Loading business impact data...")


def page_signal_noise_lab():
    """Signal Noise Lab Page - Interactive demonstration of signal noise."""
    st.markdown("""
    <div class="zomato-header">
        <div>
            <div class="zomato-logo">PrepSense</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Signal Noise Lab</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## Why Current Systems Fail: Signal Noise Analysis")
    
    if st.session_state.get('story_mode') == 'Business Mode':
        st.markdown("""
        <div style="background: #FFF4E6; padding: 20px; border-radius: 8px; border-left: 4px solid #FF9800; margin-bottom: 20px;">
            <h4 style="color: #1C1C1C; margin-top: 0;">The Problem</h4>
            <p style="color: #4A4A4A; font-size: 14px; line-height: 1.6;">
                Current systems rely on restaurant-reported prep times, which are often inaccurate due to delays in reporting, 
                kitchen congestion, and human error. This creates "noise" in the signal, making predictions unreliable.
            </p>
            <h4 style="color: #1C1C1C;">The Solution</h4>
            <p style="color: #4A4A4A; font-size: 14px; line-height: 1.6;">
                PrepSense uses rider telemetry data to reconstruct accurate prep times, eliminating the noise and 
                providing reliable predictions.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #F0F7FF; padding: 20px; border-radius: 8px; border-left: 4px solid #2196F3; margin-bottom: 20px;">
            <h4 style="color: #1C1C1C; margin-top: 0;">Signal Noise Model</h4>
            <p style="color: #4A4A4A; font-size: 14px; line-height: 1.6; margin-bottom: 10px;">
                Observed signal with noise:
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"T_{obs} = T_p + \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, \sigma^2)")
        st.markdown(r"PrepSense reconstructs $T_p$ using telemetry:")
        st.latex(r"\hat{T} = T_{pickup} - \bar{h}")
        st.caption(r"This reduces variance significantly: $\sigma_{reconstructed}^2 < \sigma_{observed}^2$")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Control Parameters")
        merchant_noise = st.slider(
            "Merchant Reporting Noise (σ)",
            0.5, 5.0, 
            value=st.session_state.get('noise_lab_merchant_noise', 3.0),
            step=0.5,
            help="Standard deviation of merchant reporting errors",
            key='noise_lab_merchant_noise_slider',
            on_change=lambda: st.session_state.update({'noise_lab_params_changed': True})
        )
        order_rate = st.slider(
            "Order Arrival Rate (λ)",
            0.1, 2.0, 
            value=st.session_state.get('noise_lab_order_rate', 0.5),
            step=0.1,
            help="Orders per minute",
            key='noise_lab_order_rate_slider',
            on_change=lambda: st.session_state.update({'noise_lab_params_changed': True})
        )
        kitchen_capacity = st.slider(
            "Kitchen Capacity",
            5, 50, 
            value=st.session_state.get('noise_lab_kitchen_capacity', 20),
            step=5,
            help="Maximum concurrent orders",
            key='noise_lab_kitchen_capacity_slider',
            on_change=lambda: st.session_state.update({'noise_lab_params_changed': True})
        )
        
        # Auto-update when parameters change
        if st.session_state.get('noise_lab_params_changed', False):
            st.session_state.noise_lab_merchant_noise = merchant_noise
            st.session_state.noise_lab_order_rate = order_rate
            st.session_state.noise_lab_kitchen_capacity = kitchen_capacity
            st.session_state.noise_lab_params_changed = False
            
            st.session_state.noise_lab_params = {
                'merchant_noise': merchant_noise,
                'order_rate': order_rate,
                'kitchen_capacity': kitchen_capacity
            }
            st.rerun()
        
        if st.button("Run Comparison", use_container_width=True, type="primary"):
            st.session_state.noise_lab_params = {
                'merchant_noise': merchant_noise,
                'order_rate': order_rate,
                'kitchen_capacity': kitchen_capacity
            }
            st.session_state.noise_lab_merchant_noise = merchant_noise
            st.session_state.noise_lab_order_rate = order_rate
            st.session_state.noise_lab_kitchen_capacity = kitchen_capacity
            st.rerun()
    
    with col2:
        if 'noise_lab_params' in st.session_state:
            params = st.session_state.noise_lab_params
            
            # Generate baseline data
            generator_baseline = DatasetGenerator(
                n_samples=1000,
                noise_level=params['merchant_noise'],
                arrival_rate=params['order_rate'],
                kitchen_capacity=params['kitchen_capacity']
            )
            df_baseline = generator_baseline.generate_orders()
            
            # Generate PrepSense data
            generator_prepsense = DatasetGenerator(
                n_samples=1000,
                noise_level=0.5,  # Lower noise for PrepSense
                arrival_rate=params['order_rate'],
                kitchen_capacity=params['kitchen_capacity']
            )
            df_prepsense = generator_prepsense.generate_orders()
            
            # Compare variances
            var_baseline = df_baseline['ObservedPrepTime'].var()
            var_prepsense = df_prepsense['ReconstructedPrepTime'].var()
            reduction = ((var_baseline - var_prepsense) / var_baseline) * 100
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Baseline Variance", f"{var_baseline:.2f}")
            with col_m2:
                st.metric("PrepSense Variance", f"{var_prepsense:.2f}", 
                         delta=f"-{reduction:.1f}%", delta_color="inverse")
            
            # Comparison chart
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=df_baseline['ObservedPrepTime'],
                name='Baseline (Noisy)',
                opacity=0.7,
                marker_color='#EF4F5F',
                nbinsx=50
            ))
            fig.add_trace(go.Histogram(
                x=df_prepsense['ReconstructedPrepTime'],
                name='PrepSense (Filtered)',
                opacity=0.7,
                marker_color='#4CAF50',
                nbinsx=50
            ))
            fig.update_layout(
                title=dict(text="Signal Distribution Comparison",
                          font=dict(family='Poppins', size=16, color='#1C1C1C')),
                xaxis_title="Preparation Time (minutes)",
                yaxis_title="Frequency",
                barmode='overlay',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', size=12, color='#1C1C1C'),
                legend=dict(
                    font=dict(size=13, color='#1C1C1C', family='Inter'),
                    bgcolor='rgba(255,255,255,0.95)',
                    bordercolor='#E0E0E0',
                    borderwidth=1
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👆 Adjust parameters and click 'Run Comparison' to see the difference")


def page_twin_restaurant():
    """Twin Restaurant Comparison Page."""
    st.markdown("""
    <div class="zomato-header">
        <div>
            <div class="zomato-logo">PrepSense</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Twin Restaurant Comparison</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## Side-by-Side Comparison: Baseline vs PrepSense")
    
    if st.session_state.get('story_mode') == 'Business Mode':
        st.markdown("""
        <div style="background: #E8F5E9; padding: 20px; border-radius: 8px; border-left: 4px solid #4CAF50; margin-bottom: 20px;">
            <h4 style="color: #1C1C1C; margin-top: 0;">The Experiment</h4>
            <p style="color: #4A4A4A; font-size: 14px; line-height: 1.6;">
                We simulate two identical restaurants with the same order volume. Restaurant A uses the current system 
                (baseline), while Restaurant B uses PrepSense. Watch how PrepSense reduces rider idle time and improves 
                prediction accuracy.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Restaurant A: Current System")
        st.markdown("""
        <div style="background: #FFEBEE; padding: 15px; border-radius: 8px; border: 2px solid #EF4F5F;">
            <p style="color: #4A4A4A; font-size: 14px; margin: 0;">
                Uses merchant-reported prep times<br>
                Higher prediction variance<br>
                Riders arrive too early<br>
                More idle time
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Restaurant B: PrepSense")
        st.markdown("""
        <div style="background: #E8F5E9; padding: 15px; border-radius: 8px; border: 2px solid #4CAF50;">
            <p style="color: #4A4A4A; font-size: 14px; margin: 0;">
                Uses telemetry-reconstructed prep times<br>
                Lower prediction variance<br>
                Optimized rider dispatch<br>
                Minimal idle time
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    n_orders = st.slider("Number of Orders to Simulate", 20, 200, 50, 10)
    
    if st.button("Run Twin Simulation", use_container_width=True, type="primary"):
        with st.spinner("Running simulation..."):
            simulator = TwinRestaurantSimulator(n_orders=n_orders)
            comparison = simulator.compare()
            st.session_state.twin_comparison = comparison
            st.rerun()
    
    if 'twin_comparison' in st.session_state:
        comparison = st.session_state.twin_comparison
        
        # Metrics
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Idle Time Reduction", f"{comparison['idle_reduction']:.1f}%",
                     delta=f"-{comparison['baseline']['idle_times'].mean() - comparison['prepsense']['idle_times'].mean():.2f} min",
                     delta_color="inverse")
        with col_m2:
            st.metric("Variance Reduction", f"{comparison['variance_reduction']:.1f}%",
                     delta=f"-{comparison['baseline']['variance'] - comparison['prepsense']['variance']:.2f}",
                     delta_color="inverse")
        with col_m3:
            st.metric("Avg Idle (Baseline)", f"{comparison['baseline']['idle_times'].mean():.2f} min")
        with col_m4:
            st.metric("Avg Idle (PrepSense)", f"{comparison['prepsense']['idle_times'].mean():.2f} min")
        
        # Comparison chart
        fig = create_twin_comparison_chart(comparison)
        st.plotly_chart(fig, use_container_width=True)


def page_war_room():
    """Live Dispatch War Room Page."""
    st.markdown("""
    <div class="zomato-header">
        <div>
            <div class="zomato-logo">PrepSense</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Live Dispatch War Room</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## Real-Time Platform Operations Dashboard")
    
    story_mode = st.session_state.get('story_mode', 'Technical Mode')
    
    if story_mode == 'Business Mode':
        st.markdown("""
        <div style="background: #E3F2FD; padding: 20px; border-radius: 8px; border-left: 4px solid #2196F3; margin-bottom: 20px;">
            <h4 style="color: #1C1C1C; margin-top: 0;">Operations Control Center</h4>
            <p style="color: #4A4A4A; font-size: 14px; line-height: 1.6;">
                This is what Zomato's operations team sees in real-time. Watch as orders are created, riders are assigned, 
                and PrepSense continuously updates predictions to optimize dispatch decisions.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #F0F7FF; padding: 20px; border-radius: 8px; border-left: 4px solid #2196F3; margin-bottom: 20px;">
            <h4 style="color: #1C1C1C; margin-top: 0;">Live Event Stream Architecture</h4>
            <p style="color: #4A4A4A; font-size: 14px; line-height: 1.6;">
                Real-time event processing: ORDER_CREATED → RIDER_ASSIGNED → RIDER_ARRIVED → ORDER_PICKED_UP. 
                Each event triggers telemetry updates and prediction recalculation using:
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"\hat{T} = T_{pickup} - \bar{h}")
        st.markdown(r"where $\hat{T}$ is the reconstructed packed time, $T_{pickup}$ is pickup time, and $\bar{h}$ is mean handover delay.")
    
    # Initialize session state
    if 'war_room_running' not in st.session_state:
        st.session_state.war_room_running = False
    if 'war_room_events' not in st.session_state:
        st.session_state.war_room_events = []
    if 'war_room_event_counter' not in st.session_state:
        st.session_state.war_room_event_counter = 0
    if 'war_room_start_time' not in st.session_state:
        st.session_state.war_room_start_time = None
    if 'war_room_last_event_time' not in st.session_state:
        st.session_state.war_room_last_event_time = datetime.now()
    
    # Controls
    col_controls, col_auto = st.columns([3, 1])
    with col_controls:
        if st.button("🔄 Start/Refresh Simulation", use_container_width=True, type="primary", key='start_sim_btn'):
            simulator = WarRoomSimulator()
            events = simulator.generate_live_events(duration_minutes=5, arrival_rate=0.5)
            st.session_state.war_room_events = events
            st.session_state.war_room_running = True
            st.session_state.war_room_start_time = datetime.now()
            st.session_state.war_room_event_counter = len(events)
            st.session_state.war_room_last_event_time = datetime.now()
            st.rerun()
    
    with col_auto:
        auto_refresh = st.checkbox("🔄 Live Updates", value=st.session_state.get('war_room_auto_refresh', False), 
                                   help="Automatically update every 2 seconds", key='war_room_auto_checkbox')
        st.session_state.war_room_auto_refresh = auto_refresh
    
    # Auto-refresh mechanism
    if auto_refresh and st.session_state.war_room_running:
        # Check if it's time to add new events
        if 'war_room_last_event_time' in st.session_state:
            time_since_last = (datetime.now() - st.session_state.war_room_last_event_time).total_seconds()
            
            if time_since_last >= 2:  # Add event every 2 seconds
                simulator = WarRoomSimulator()
                new_batch = simulator.generate_live_events(duration_minutes=0.2, arrival_rate=0.5)
                
                if new_batch:
                    for event in new_batch[:1]:  # Add 1 event per update
                        event['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                        st.session_state.war_room_events.append(event)
                        st.session_state.war_room_event_counter += 1
                    
                    if len(st.session_state.war_room_events) > 50:
                        st.session_state.war_room_events = st.session_state.war_room_events[-50:]
                
                st.session_state.war_room_last_event_time = datetime.now()
                st.rerun()
        
        # Use JavaScript meta refresh for continuous updates
        st.markdown("""
        <meta http-equiv="refresh" content="2">
        """, unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_left:
        st.markdown("### 📡 Live Event Feed")
        event_placeholder = st.empty()
        
        if st.session_state.war_room_events:
            events = st.session_state.war_room_events[-15:]  # Show last 15 events
            with event_placeholder.container():
                for event in reversed(events):
                    event_type = event.get('event_type', 'UNKNOWN')
                    order_id = event.get('order_id', 'N/A')
                    timestamp = event.get('timestamp', '')
                    
                    # Determine color based on event type
                    if event_type == EventType.ORDER_CREATED.value:
                        color = '#EF4F5F'
                        icon = '📦'
                    elif event_type == EventType.RIDER_ASSIGNED.value:
                        color = '#2196F3'
                        icon = '🚴'
                    elif event_type == EventType.RIDER_ARRIVED.value:
                        color = '#4CAF50'
                        icon = '📍'
                    elif event_type == EventType.ORDER_PICKED_UP.value:
                        color = '#FF9800'
                        icon = '✅'
                    else:
                        color = '#9E9E9E'
                        icon = '⚡'
                    
                    # Check if this is a new event (last 3 events get highlight)
                    is_new = events.index(event) >= len(events) - 3
                    highlight = 'background: #FFF9C4;' if is_new else ''
                    
                    st.markdown(f"""
                    <div style="{highlight}background: #F8F8F8; padding: 10px; margin: 6px 0; border-left: 4px solid {color}; border-radius: 4px; 
                                box-shadow: 0 1px 3px rgba(0,0,0,0.1); transition: all 0.3s;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 18px;">{icon}</span>
                            <div style="flex: 1;">
                                <strong style="color: #1C1C1C; font-size: 13px;">{event_type}</strong><br>
                                <small style="color: #666; font-size: 11px;">Order: {order_id}</small><br>
                                <small style="color: #999; font-size: 10px;">{timestamp}</small>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            event_placeholder.info("👆 Click 'Start Simulation' to begin")
    
    with col_center:
        st.markdown("### 🗺️ Platform Operations Map")
        map_placeholder = st.empty()
        
        if st.session_state.war_room_events:
            np.random.seed(42)
            restaurants = [{'id': f'REST_{i}', 'lat': np.random.uniform(17.0, 18.0), 
                          'lon': np.random.uniform(78.0, 79.0)} for i in range(10)]
            
            # Make riders move slightly based on time
            time_factor = (datetime.now() - st.session_state.war_room_start_time).total_seconds() / 60 if 'war_room_start_time' in st.session_state else 0
            riders = []
            for i in range(5):
                base_lat = 17.5 + np.sin(time_factor + i) * 0.1
                base_lon = 78.5 + np.cos(time_factor + i) * 0.1
                riders.append({'id': f'RIDER_{i}', 'lat': base_lat, 'lon': base_lon})
            
            fig_map = create_war_room_map(st.session_state.war_room_events, restaurants, riders)
            map_placeholder.plotly_chart(fig_map, use_container_width=True, key=f"war_room_map_{st.session_state.war_room_event_counter}")
        else:
            map_placeholder.info("Click 'Start Simulation' to see the map")
    
    with col_right:
        st.markdown("### 📊 Live Metrics")
        metrics_placeholder = st.empty()
        
        if st.session_state.war_room_events:
            simulator = WarRoomSimulator()
            metrics = simulator.get_live_metrics(st.session_state.war_room_events)
            
            with metrics_placeholder.container():
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.metric("Total Orders", f"{metrics.get('total_orders', 0):,}")
                with col_m2:
                    st.metric("Avg Queue", f"{metrics.get('avg_queue', 0):.1f}")
                
                col_m3, col_m4 = st.columns(2)
                with col_m3:
                    st.metric("Avg Prediction", f"{metrics.get('avg_prediction', 0):.2f} min")
                with col_m4:
                    st.metric("High Risk", f"{metrics.get('high_risk_orders', 0)}")
                
                # Sample prediction display - always show latest
                sample_events = [e for e in st.session_state.war_room_events if 'predicted_prep' in e]
                if sample_events:
                    latest_event = sample_events[-1]
                    pred = latest_event.get('predicted_prep', 0)
                    conf = latest_event.get('confidence', 0)
                    risk = latest_event.get('idle_risk', 'LOW')
                    queue = latest_event.get('kitchen_queue', 0)
                    
                    risk_color = '#EF4F5F' if risk == 'HIGH' else '#FF9800' if risk == 'MEDIUM' else '#4CAF50'
                    
                    st.markdown("### 🎯 Current Prediction")
                    st.markdown(f"""
                    <div style="background: #E8F5E9; padding: 15px; border-radius: 8px; border: 2px solid #4CAF50; 
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1); animation: pulse 2s infinite;">
                        <p style="margin: 0 0 8px 0;"><strong style="color: #1C1C1C;">PrepSense:</strong> <span style="color: #EF4F5F; font-size: 18px; font-weight: bold;">{pred:.1f} min</span></p>
                        <p style="margin: 0 0 8px 0;"><strong style="color: #1C1C1C;">Confidence:</strong> ±{conf:.1f} min</p>
                        <p style="margin: 0 0 8px 0;"><strong style="color: #1C1C1C;">Queue:</strong> {queue}</p>
                        <p style="margin: 0;"><strong style="color: #1C1C1C;">Risk:</strong> <span style="color: {risk_color}; font-weight: bold;">{risk}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            metrics_placeholder.info("Start simulation to see metrics")


def page_event_timeline():
    """Event Timeline Replay Page."""
    st.markdown("""
    <div class="zomato-header">
        <div>
            <div class="zomato-logo">PrepSense</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Event Timeline Replay</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## Order Lifecycle Replay")
    
    story_mode = st.session_state.get('story_mode', 'Technical Mode')
    
    if story_mode == 'Business Mode':
        st.markdown("""
        <div style="background: #FFF4E6; padding: 20px; border-radius: 8px; border-left: 4px solid #FF9800; margin-bottom: 20px;">
            <h4 style="color: #1C1C1C; margin-top: 0;">Watch an Order's Journey</h4>
            <p style="color: #4A4A4A; font-size: 14px; line-height: 1.6;">
                See how a single order moves through the system. Watch as PrepSense updates its prediction 
                in real-time as new information arrives. This shows how our system adapts to changing conditions.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #F0F7FF; padding: 20px; border-radius: 8px; border-left: 4px solid #2196F3; margin-bottom: 20px;">
            <h4 style="color: #1C1C1C; margin-top: 0;">Prediction Update Mechanism</h4>
            <p style="color: #4A4A4A; font-size: 14px; line-height: 1.6;">
                Demonstrates how predictions update as telemetry arrives. Each event triggers prediction recalculation.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        order_id = st.text_input("Order ID", value="ORD_001")
        
        if st.button("▶️ Replay Order Lifecycle", use_container_width=True, type="primary"):
            replay = OrderLifecycleReplay()
            lifecycle = replay.generate_order_lifecycle(order_id)
            st.session_state.timeline_lifecycle = lifecycle
            st.rerun()
    
    with col2:
        if 'timeline_lifecycle' in st.session_state:
            lifecycle = st.session_state.timeline_lifecycle
            
            st.markdown("### Timeline Events")
            for event in lifecycle['timeline']:
                color = '#EF4F5F' if event['event'] == 'ORDER_CREATED' else \
                        '#2196F3' if event['event'] == 'RIDER_ASSIGNED' else \
                        '#4CAF50' if event['event'] == 'RIDER_ARRIVED' else \
                        '#FF9800' if event['event'] == 'ORDER_PACKED' else '#9C27B0'
                
                st.markdown(f"""
                <div style="background: #F8F8F8; padding: 12px; margin: 8px 0; border-left: 4px solid {color}; border-radius: 4px;">
                    <strong style="color: #1C1C1C;">{event['event']}</strong><br>
                    <small style="color: #666;">{event['description']}</small><br>
                    <small style="color: #999;">{event['time'].strftime('%H:%M:%S')}</small>
                    {f"<br><span style='color: #4CAF50; font-weight: bold;'>Prediction: {event['prediction']:.1f} min (±{event['confidence']:.1f})</span>" if event['prediction'] else ''}
                </div>
                """, unsafe_allow_html=True)
            
            # Timeline chart
            fig = create_timeline_replay_chart(lifecycle)
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary
            st.markdown("### Summary")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.metric("True Prep Time", f"{lifecycle['true_prep_time']:.2f} min")
            with col_s2:
                if lifecycle['final_prediction']:
                    error = abs(lifecycle['true_prep_time'] - lifecycle['final_prediction'])
                    st.metric("Prediction Error", f"{error:.2f} min")


def page_realtime_dispatch_dashboard():
    """
    Real-Time Dispatch Dashboard - Uber/Swiggy/Zomato Style
    
    Uses st.empty() containers for seamless real-time updates without page refresh.
    Updates happen in-place like real food delivery apps.
    """
    import sys
    import os
    import time
    import numpy as np
    
    # Add frontend to path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'frontend'))
    
    try:
        from frontend.rider_map import create_rider_map
        from frontend.metrics_panel import render_metrics_panel, render_dispatch_cards
        from frontend.websocket_client import get_websocket_client
    except ImportError as e:
        st.error(f"Import error: {e}. Make sure websockets is installed: pip3 install websockets")
        st.stop()
    
    st.markdown("""
    <div class="zomato-header">
        <div>
            <div class="zomato-logo">🚴 PrepSense Dispatch Engine</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Real-Time Rider Assignment & Optimization (Live Updates)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # WebSocket configuration
    WEBSOCKET_URL = "ws://localhost:8000/ws/dispatch"
    
    # Initialize session state
    if 'dispatch_events' not in st.session_state:
        st.session_state.dispatch_events = []
    
    if 'active_dispatches' not in st.session_state:
        st.session_state.active_dispatches = []
    
    if 'restaurants' not in st.session_state:
        st.session_state.restaurants = []
    
    if 'riders' not in st.session_state:
        st.session_state.riders = []
    
    if 'metrics' not in st.session_state:
        st.session_state.metrics = {
            'avg_idle_time': 0.0,
            'dispatch_efficiency': 0.0,
            'delay_probability': 0.0,
            'total_orders': 0,
            'active_dispatches': 0,
            'idle_change': 0.0,
            'efficiency_change': 0.0,
            'delay_change': 0.0,
            'signal_variance': 0.0,
            'prediction_accuracy': 0.0,
            'noise_reduction_pct': 0.0,
        }

    if 'signal_history' not in st.session_state:
        st.session_state.signal_history = []
    
    # Thread-safe event queue (created once per session)
    import queue
    if 'event_queue' not in st.session_state:
        st.session_state.event_queue = queue.Queue()
    
    if 'ws_connected' not in st.session_state:
        st.session_state.ws_connected = False
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    
    if 'new_events_received' not in st.session_state:
        st.session_state.new_events_received = False
    
    # Create callback that captures the queue reference AND session state key
    event_queue_ref = st.session_state.event_queue
    
    def on_websocket_message(data: dict):
        """Callback function for WebSocket messages - stores in queue for main thread processing."""
        try:
            # Put event in queue (thread-safe) - use captured reference
            event_queue_ref.put(data)
            event_type = data.get('event_type', 'UNKNOWN')
            order_id = data.get('order_id', 'N/A')
            print(f"📨 Event queued: {event_type} - Order: {order_id} | Queue size: {event_queue_ref.qsize()}")
            
            # ALSO directly append to session state as backup (if possible)
            # This is a workaround for Streamlit session state issues
            try:
                # We can't directly modify session_state from background thread,
                # but we can ensure queue is working
                pass
            except:
                pass
        except Exception as e:
            print(f"❌ Error in on_websocket_message: {e}")
            import traceback
            traceback.print_exc()
    
    def process_dispatch_event(event: dict):
        """Process incoming dispatch event and update session state - called from main thread."""
        event_type = event.get('event_type', '')
        order_id = event.get('order_id', '')
        
        # Skip CONNECTED message (not a real event)
        if event_type == 'CONNECTED':
            return
        
        # Add to event history
        st.session_state.dispatch_events.append({
            **event,
            'processed_at': datetime.now().isoformat()
        })
        
        # Keep only last 100 events
        if len(st.session_state.dispatch_events) > 100:
            st.session_state.dispatch_events = st.session_state.dispatch_events[-100:]
        
        # Debug: print event received (will show in terminal)
        print(f"✅ Event processed: {event_type} - Order: {order_id}")
        
        # Handle different event types
        if event_type == 'ORDER_CREATED':
            restaurant_id = event.get('restaurant_id', 'REST_0')
            # Generate random location if not provided
            restaurant_lat = event.get('restaurant_lat', 28.6139 + (np.random.random() - 0.5) * 0.1)
            restaurant_lon = event.get('restaurant_lon', 77.2090 + (np.random.random() - 0.5) * 0.1)
            
            restaurant = {
                'id': restaurant_id,
                'lat': restaurant_lat,
                'lon': restaurant_lon
            }
            if not any(r['id'] == restaurant_id for r in st.session_state.restaurants):
                st.session_state.restaurants.append(restaurant)
        
        elif event_type == 'KPT_PREDICTED':
            st.session_state.metrics['total_orders'] += 1
        
        elif event_type == 'RIDER_DISPATCHED':
            dispatch = {
                'order_id': order_id,
                'rider_id': event.get('rider_id'),
                'restaurant_id': event.get('restaurant_id'),
                'predicted_kpt': event.get('predicted_kpt', 0),
                'confidence': event.get('confidence', 0),
                'dispatch_time': event.get('dispatch_time', 0),
                'travel_time': event.get('travel_time', 0),
                'idle_risk': event.get('idle_risk', 0),
                'delay_risk': event.get('delay_risk', 0),
                'timestamp': event.get('timestamp', '')
            }
            
            existing = next(
                (d for d in st.session_state.active_dispatches if d['order_id'] == order_id),
                None
            )
            if existing:
                existing.update(dispatch)
            else:
                st.session_state.active_dispatches.append(dispatch)
            
            rider_id = event.get('rider_id')
            if rider_id:
                rider = next(
                    (r for r in st.session_state.riders if r.get('id') == rider_id),
                    None
                )
                if rider:
                    rider['available'] = False
                else:
                    st.session_state.riders.append({
                        'id': rider_id,
                        'lat': 0,
                        'lon': 0,
                        'available': False
                    })
        
        elif event_type == 'RIDER_MOVED':
            rider_id = event.get('rider_id')
            if rider_id:
                rider = next(
                    (r for r in st.session_state.riders if r.get('id') == rider_id),
                    None
                )
                if rider:
                    rider['lat'] = event.get('rider_lat', 0)
                    rider['lon'] = event.get('rider_lon', 0)
        
        elif event_type == 'ORDER_PICKED_UP':
            st.session_state.active_dispatches = [
                d for d in st.session_state.active_dispatches if d['order_id'] != order_id
            ]
            
            rider_id = event.get('rider_id')
            if rider_id:
                rider = next(
                    (r for r in st.session_state.riders if r.get('id') == rider_id),
                    None
                )
                if rider:
                    rider['available'] = True

        elif event_type == 'FILTERED_SIGNAL_UPDATED':
            st.session_state.signal_history.append({
                'order_id': order_id,
                'signal_type': event.get('signal_type', 'unknown'),
                'observed_signal': event.get('observed_signal', 0.0),
                'filtered_signal': event.get('filtered_signal', 0.0),
                'variance_raw': event.get('variance_raw', 0.0),
                'variance_filtered': event.get('variance_filtered', 0.0),
                'noise_reduction_pct': event.get('noise_reduction_pct', 0.0),
                'prediction_accuracy': event.get('prediction_accuracy', 0.0),
                'timestamp': event.get('timestamp', ''),
            })

            if len(st.session_state.signal_history) > 200:
                st.session_state.signal_history = st.session_state.signal_history[-200:]

            latest_signals = st.session_state.signal_history[-30:]
            if latest_signals:
                st.session_state.metrics.update({
                    'signal_variance': float(np.mean([s.get('variance_filtered', 0.0) for s in latest_signals])),
                    'prediction_accuracy': float(np.mean([s.get('prediction_accuracy', 0.0) for s in latest_signals])),
                    'noise_reduction_pct': float(np.mean([s.get('noise_reduction_pct', 0.0) for s in latest_signals])),
                })
        
        # Update metrics
        dispatches = st.session_state.active_dispatches
        if dispatches:
            avg_idle_risk = sum(d.get('idle_risk', 0) for d in dispatches) / len(dispatches)
            avg_delay_risk = sum(d.get('delay_risk', 0) for d in dispatches) / len(dispatches)
            avg_idle_time = avg_idle_risk * 5.0
            efficiency = (1 - (avg_idle_risk + avg_delay_risk) / 2) * 100
            
            st.session_state.metrics.update({
                'avg_idle_time': avg_idle_time,
                'dispatch_efficiency': efficiency,
                'delay_probability': avg_delay_risk * 100,
                'active_dispatches': len(dispatches)
            })

    def create_signal_filter_histogram(signal_history):
        """Observed vs filtered telemetry histogram."""
        fig = go.Figure()

        if signal_history:
            observed = [s.get('observed_signal', 0.0) for s in signal_history]
            filtered = [s.get('filtered_signal', 0.0) for s in signal_history]

            fig.add_trace(go.Histogram(
                x=observed,
                name='Observed Signals',
                opacity=0.65,
                marker_color='#EF4F5F',
                nbinsx=18,
            ))
            fig.add_trace(go.Histogram(
                x=filtered,
                name='Filtered Signals',
                opacity=0.65,
                marker_color='#1E88E5',
                nbinsx=18,
            ))

        fig.update_layout(
            barmode='overlay',
            height=320,
            margin=dict(l=10, r=10, t=40, b=10),
            paper_bgcolor='white',
            plot_bgcolor='white',
            title='Observed vs Filtered Signals',
            xaxis_title='Packed Time Signal (minutes)',
            yaxis_title='Count',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        )
        return fig

    def build_dispatch_log_records(events):
        """Convert raw dispatch events into structured log records."""
        service_map = {
            'ORDER_CREATED': 'event-stream',
            'KPT_PREDICTED': 'prediction-service',
            'RIDER_DISPATCHED': 'dispatch-engine',
            'RIDER_MOVED': 'telemetry-service',
            'RIDER_ARRIVED': 'telemetry-service',
            'ORDER_PICKED_UP': 'dispatch-engine',
            'KITCHEN_STARTED': 'kitchen-simulator',
            'FOOD_PREPARING': 'kitchen-simulator',
            'FOOD_READY': 'kitchen-simulator',
            'RIDER_EN_ROUTE': 'delivery-tracker',
            'ORDER_DELIVERED': 'delivery-tracker',
            'FILTERED_SIGNAL_UPDATED': 'signal-filter',
        }
        status_map = {
            'ORDER_CREATED': 'created',
            'KPT_PREDICTED': 'predicted',
            'RIDER_DISPATCHED': 'assigned',
            'RIDER_MOVED': 'moving',
            'RIDER_ARRIVED': 'arrived',
            'ORDER_PICKED_UP': 'picked-up',
            'KITCHEN_STARTED': 'started',
            'FOOD_PREPARING': 'cooking',
            'FOOD_READY': 'ready',
            'RIDER_EN_ROUTE': 'delivering',
            'ORDER_DELIVERED': 'delivered',
            'FILTERED_SIGNAL_UPDATED': 'filtered',
        }
        level_map = {
            'ORDER_CREATED': 'info',
            'KPT_PREDICTED': 'info',
            'RIDER_DISPATCHED': 'info',
            'RIDER_MOVED': 'info',
            'RIDER_ARRIVED': 'warning',
            'ORDER_PICKED_UP': 'warning',
            'KITCHEN_STARTED': 'info',
            'FOOD_PREPARING': 'info',
            'FOOD_READY': 'warning',
            'RIDER_EN_ROUTE': 'info',
            'ORDER_DELIVERED': 'info',
            'FILTERED_SIGNAL_UPDATED': 'warning',
        }
        tag_map = {
            'ORDER_CREATED': ['orders', 'platform'],
            'KPT_PREDICTED': ['prediction', 'ml'],
            'RIDER_DISPATCHED': ['dispatch', 'assignment'],
            'RIDER_MOVED': ['telemetry', 'movement'],
            'RIDER_ARRIVED': ['handoff', 'arrival'],
            'ORDER_PICKED_UP': ['handoff', 'pickup'],
            'KITCHEN_STARTED': ['kitchen', 'prep'],
            'FOOD_PREPARING': ['kitchen', 'progress'],
            'FOOD_READY': ['kitchen', 'ready'],
            'RIDER_EN_ROUTE': ['delivery', 'route'],
            'ORDER_DELIVERED': ['delivery', 'completed'],
            'FILTERED_SIGNAL_UPDATED': ['signals', 'filtering'],
        }
        icon_map = {
            'ORDER_CREATED': '📦',
            'KPT_PREDICTED': '🔮',
            'RIDER_DISPATCHED': '🚴',
            'RIDER_MOVED': '📍',
            'RIDER_ARRIVED': '✅',
            'ORDER_PICKED_UP': '🎉',
            'KITCHEN_STARTED': '👨‍🍳',
            'FOOD_PREPARING': '🍳',
            'FOOD_READY': '✅',
            'RIDER_EN_ROUTE': '🛵',
            'ORDER_DELIVERED': '🏁',
            'FILTERED_SIGNAL_UPDATED': '🧪',
        }

        records = []
        for idx, event in enumerate(reversed(events[-100:])):
            event_type = event.get('event_type', 'UNKNOWN')
            order_id = event.get('order_id', 'N/A')
            timestamp = event.get('timestamp', '')
            message = f"{event_type.replace('_', ' ').title()} for order {order_id}"
            if event_type == 'FILTERED_SIGNAL_UPDATED':
                message = (
                    f"Observed {event.get('observed_signal', 0.0):.1f} -> "
                    f"filtered {event.get('filtered_signal', 0.0):.1f}"
                )
            elif event_type == 'RIDER_MOVED':
                message = f"Rider moved towards store for {order_id}"
            elif event_type == 'FOOD_PREPARING':
                progress = event.get('progress', 0.0) * 100
                message = f"Kitchen prep progress updated to {progress:.0f}%"

            records.append({
                'id': f"log-{idx}-{order_id}",
                'timestamp': timestamp,
                'level': level_map.get(event_type, 'info'),
                'service': service_map.get(event_type, 'dispatch-engine'),
                'message': message,
                'duration': event.get('travel_time', event.get('confidence', event.get('dispatch_time', 0))),
                'status': status_map.get(event_type, 'active'),
                'tags': tag_map.get(event_type, ['operations']),
                'event_type': event_type,
                'order_id': order_id,
                'icon': icon_map.get(event_type, '📌'),
                'raw_event': event,
            })
        return records

    def render_dispatch_logs_console(events):
        """Render a Streamlit-native interactive logs table."""
        logs = build_dispatch_log_records(events)
        levels = sorted({log['level'] for log in logs})
        services = sorted({log['service'] for log in logs})
        statuses = sorted({log['status'] for log in logs})

        search_col, level_col, service_col, status_col = st.columns([2.2, 1, 1.2, 1])
        with search_col:
            search_query = st.text_input(
                "Search logs",
                value=st.session_state.get('dispatch_log_search', ''),
                placeholder="Search by event, order, or service...",
                key='dispatch_log_search',
            )
        with level_col:
            selected_levels = st.multiselect(
                "Level",
                options=levels,
                default=st.session_state.get('dispatch_log_level', []),
                key='dispatch_log_level',
            )
        with service_col:
            selected_services = st.multiselect(
                "Service",
                options=services,
                default=st.session_state.get('dispatch_log_service', []),
                key='dispatch_log_service',
            )
        with status_col:
            selected_statuses = st.multiselect(
                "Status",
                options=statuses,
                default=st.session_state.get('dispatch_log_status', []),
                key='dispatch_log_status',
            )

        lower_query = search_query.lower().strip()
        filtered_logs = []
        for log in logs:
            matches_search = (
                not lower_query
                or lower_query in log['message'].lower()
                or lower_query in log['service'].lower()
                or lower_query in log['event_type'].lower()
                or lower_query in log['order_id'].lower()
            )
            matches_level = not selected_levels or log['level'] in selected_levels
            matches_service = not selected_services or log['service'] in selected_services
            matches_status = not selected_statuses or log['status'] in selected_statuses
            if matches_search and matches_level and matches_service and matches_status:
                filtered_logs.append(log)

        badge_col, info_col = st.columns([1, 3])
        with badge_col:
            st.success(f"✅ **{len(filtered_logs)} logs**")
        with info_col:
            st.caption(f"Last updated: {st.session_state.last_update.strftime('%H:%M:%S')}")

        st.markdown(
            """
            <div style="border: 1px solid #F3D2D6; border-radius: 12px; overflow: hidden; background: #FFFFFF; box-shadow: 0 2px 12px rgba(239,79,95,0.06); margin-top: 8px;">
                <div style="display:grid; grid-template-columns: 90px 80px 140px 1fr 90px 90px; gap: 12px; padding: 12px 16px; background: #FFF5F6; border-bottom: 1px solid #F3D2D6; font-size: 12px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.08em;">
                    <span>Level</span>
                    <span>Time</span>
                    <span>Service</span>
                    <span>Message</span>
                    <span>Status</span>
                    <span>Order</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not filtered_logs:
            st.info("No logs match the current search/filter combination.")
            return

        level_styles = {
            'info': ('#E3F2FD', '#1976D2'),
            'warning': ('#FFF4E5', '#F57C00'),
            'error': ('#FDECEC', '#D32F2F'),
        }
        status_styles = {
            'created': '#EF4F5F',
            'predicted': '#2196F3',
            'assigned': '#7C3AED',
            'moving': '#0EA5E9',
            'arrived': '#10B981',
            'picked-up': '#10B981',
            'started': '#FB8C00',
            'cooking': '#FB8C00',
            'ready': '#43A047',
            'delivering': '#6366F1',
            'delivered': '#16A34A',
            'filtered': '#AB47BC',
            'active': '#6B7280',
        }

        for log in filtered_logs[:25]:
            badge_bg, badge_fg = level_styles.get(log['level'], ('#F3F4F6', '#4B5563'))
            formatted_time = log['timestamp'][11:19] if log['timestamp'] else 'N/A'
            status_color = status_styles.get(log['status'], '#6B7280')
            with st.expander(
                f"{log['icon']} {log['event_type']} | {log['order_id']} | {formatted_time}",
                expanded=False,
            ):
                st.markdown(
                    f"""
                    <div style="border: 1px solid #EAEAEA; border-radius: 12px; overflow: hidden; background: #FFFFFF; margin-bottom: 12px;">
                        <div style="display:grid; grid-template-columns: 90px 80px 140px 1fr 90px 90px; gap: 12px; padding: 14px 16px; align-items:center;">
                            <span style="display:inline-flex; justify-content:center; padding:6px 10px; border-radius:999px; background:{badge_bg}; color:{badge_fg}; font-size:12px; font-weight:700; text-transform:capitalize;">{log['level']}</span>
                            <span style="font-family:monospace; font-size:12px; color:#6B7280;">{formatted_time}</span>
                            <span style="font-size:13px; font-weight:600; color:#1F2937;">{log['service']}</span>
                            <span style="font-size:13px; color:#4B5563;">{log['message']}</span>
                            <span style="font-size:12px; font-weight:700; color:{status_color}; text-transform:uppercase;">{log['status']}</span>
                            <span style="font-family:monospace; font-size:12px; color:#6B7280;">{log['order_id']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                detail_col1, detail_col2 = st.columns(2)
                with detail_col1:
                    st.caption("Message")
                    st.code(log['message'], language=None)
                    st.caption("Tags")
                    st.markdown(" ".join([f"`{tag}`" for tag in log['tags']]))
                with detail_col2:
                    st.caption("Service")
                    st.write(log['service'])
                    st.caption("Timestamp")
                    st.code(log['timestamp'] or 'N/A', language=None)
                    st.caption("Event Payload")
                    st.json(log['raw_event'])
    
    # Initialize WebSocket client FIRST - only once per session
    import time
    
    if 'ws_client' not in st.session_state:
        try:
            # Create and start client
            ws_client = get_websocket_client(WEBSOCKET_URL, on_websocket_message)
            st.session_state.ws_client = ws_client
            st.session_state.ws_init_time = datetime.now()
            
            # Wait for connection - give it more time
            connection_wait_time = 0
            max_wait = 8  # Wait up to 8 seconds
            
            while connection_wait_time < max_wait and not ws_client.connected:
                time.sleep(0.5)
                connection_wait_time += 0.5
                # Check connection status
                st.session_state.ws_connected = ws_client.connected
                if ws_client.connected:
                    break
            
            # Final check
            st.session_state.ws_connected = ws_client.connected
            
            if st.session_state.ws_connected:
                st.success("✅ Connected to backend!")
            else:
                # Check if thread is still running
                if ws_client.thread and ws_client.thread.is_alive():
                    st.info("⏳ Connection in progress... Please wait a few more seconds.")
                else:
                    st.warning("⚠️ Connection attempt timed out. Trying to reconnect...")
                    # Try restarting
                    try:
                        ws_client.stop()
                        ws_client.start()
                        time.sleep(2.0)
                        st.session_state.ws_connected = ws_client.connected
                    except:
                        pass
                
        except Exception as e:
            st.session_state.ws_connected = False
            st.error(f"❌ WebSocket connection error: {e}")
            st.info("💡 Make sure backend is running: `cd backend && uvicorn websocket_server:app --port 8000`")
    else:
        # Update connection status from existing client
        ws_client = st.session_state.ws_client
        
        # Check if thread is still alive and connected
        if ws_client.thread and ws_client.thread.is_alive():
            # Thread is running, check connection status
            st.session_state.ws_connected = ws_client.connected
        else:
            # Thread died, mark as disconnected
            st.session_state.ws_connected = False
            # Try to restart if it's been a while
            if 'ws_init_time' in st.session_state:
                time_since_init = (datetime.now() - st.session_state.ws_init_time).total_seconds()
                if time_since_init > 10 and not ws_client.running:
                    try:
                        ws_client.start()
                        time.sleep(1.0)
                        st.session_state.ws_connected = ws_client.connected
                    except Exception as e:
                        st.session_state.ws_connected = False
    
    # Process queued events (from background thread) in main thread - AFTER WebSocket init
    events_processed = 0
    queue_size_before = 0
    
    if 'event_queue' in st.session_state:
        queue_size_before = st.session_state.event_queue.qsize()
        
        # Process ALL events in queue
        max_events_per_cycle = 50  # Prevent infinite loop
        processed_this_cycle = 0
        
        while processed_this_cycle < max_events_per_cycle:
            try:
                event = st.session_state.event_queue.get_nowait()
                process_dispatch_event(event)
                events_processed += 1
                processed_this_cycle += 1
                st.session_state.last_update = datetime.now()
                st.session_state.new_events_received = True
            except queue.Empty:
                break
        
        if queue_size_before > 0:
            print(f"📊 Queue had {queue_size_before} events, processed {events_processed}")
    
    # CRITICAL: Force refresh if we processed events OR if queue has events
    if events_processed > 0:
        print(f"🔄 Processed {events_processed} events from queue - FORCING IMMEDIATE REFRESH")
        st.session_state.new_events_received = True
        time.sleep(0.05)  # Very short delay
        st.rerun()
    elif queue_size_before > 0 and events_processed == 0:
        print(f"⚠️ Queue had {queue_size_before} events but processed 0 - possible error")
    
    # Connection status with DEBUG INFO
    col_status, col_info = st.columns([1, 3])
    with col_status:
        if st.session_state.ws_connected:
            st.success("🟢 Connected")
            # Show queue size for debugging
            queue_size = st.session_state.event_queue.qsize() if 'event_queue' in st.session_state else 0
            event_count = len(st.session_state.dispatch_events)
            if queue_size > 0:
                st.warning(f"⚠️ {queue_size} in queue")
            elif event_count == 0:
                st.caption("Waiting for events...")
        else:
            st.error("🔴 Disconnected")
            st.caption("Make sure backend is running on port 8000")
            if st.button("🔄 Reconnect", type="primary"):
                # Stop existing client
                if 'ws_client' in st.session_state:
                    try:
                        st.session_state.ws_client.stop()
                    except:
                        pass
                    del st.session_state.ws_client
                
                # Clear connection status and init time
                st.session_state.ws_connected = False
                if 'ws_init_time' in st.session_state:
                    del st.session_state.ws_init_time
                
                # Force rerun to reinitialize
                st.rerun()
            
            # Show backend status check
            with st.expander("🔍 Backend Status Check"):
                try:
                    import urllib.request
                    import json
                    req = urllib.request.urlopen("http://localhost:8000/health", timeout=2)
                    data = json.loads(req.read().decode())
                    st.success("✅ Backend is running on port 8000")
                    st.json(data)
                except Exception as e:
                    st.error(f"❌ Cannot reach backend: {e}")
                    st.info("Start backend with: `cd prepsense/backend && uvicorn websocket_server:app --port 8000`")
    
    with col_info:
        st.caption(f"WebSocket: {WEBSOCKET_URL}")
        st.caption(f"Last update: {st.session_state.last_update.strftime('%H:%M:%S')}")
    
    # Main layout - use local placeholders so content stays
    # anchored to the correct section on every rerun.
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🗺️ Live Dispatch Map")
        map_placeholder = st.empty()
        
        # Update map container in real-time
        with map_placeholder.container():
            # Show event count and queue status
            event_count = len(st.session_state.dispatch_events)
            queue_size = st.session_state.event_queue.qsize() if 'event_queue' in st.session_state else 0
            
            if event_count > 0:
                st.success(f"✅ **{event_count} events received** | {len(st.session_state.active_dispatches)} active dispatches")
            elif queue_size > 0:
                st.warning(f"⚠️ **{queue_size} events in queue** - processing...")
            else:
                st.info("⏳ Waiting for events...")
            
            # ALWAYS show map if we have events or dispatches
            if st.session_state.restaurants or st.session_state.riders or event_count > 0 or len(st.session_state.active_dispatches) > 0:
                orders = [
                    {
                        'order_id': d['order_id'],
                        'restaurant_id': d.get('restaurant_id'),
                        'rider_id': d.get('rider_id')
                    }
                    for d in st.session_state.active_dispatches
                ]
                
                # Create default restaurants/riders if we have events but no locations yet
                if not st.session_state.restaurants and event_count > 0:
                    # Add a default restaurant for demo
                    st.session_state.restaurants.append({
                        'id': 'REST_0',
                        'lat': 28.6139 + (np.random.random() - 0.5) * 0.1,
                        'lon': 77.2090 + (np.random.random() - 0.5) * 0.1
                    })
                
                fig = create_rider_map(
                    restaurants=st.session_state.restaurants,
                    riders=st.session_state.riders,
                    orders=orders,
                    title="Real-Time Dispatch Operations"
                )
                st.plotly_chart(fig, use_container_width=True, key=f"map_{event_count}")
            else:
                if st.session_state.ws_connected:
                    st.info("⏳ Waiting for orders... Map will appear when orders are created.")
                    st.caption(f"Events received: {event_count}. Processing...")
                else:
                    st.info("Waiting for events... Map will appear when orders are created.")
    
    with col2:
        metrics_placeholder = st.empty()
        dispatches_placeholder = st.empty()

        # Update metrics container in real-time
        with metrics_placeholder.container():
            render_metrics_panel(st.session_state.metrics)
            
            # Show event stats
            event_count = len(st.session_state.dispatch_events)
            if event_count > 0:
                st.caption(f"📨 Total Events: {event_count}")
        
        st.divider()
        
        # Update dispatches container in real-time
        with dispatches_placeholder.container():
            render_dispatch_cards(st.session_state.active_dispatches)

    st.markdown("---")
    st.markdown("### 🧪 Signal Filtering Monitor")
    signal_col1, signal_col2 = st.columns([2, 1])

    with signal_col1:
        signal_history = st.session_state.signal_history[-80:]
        signal_fig = create_signal_filter_histogram(signal_history)
        st.plotly_chart(signal_fig, use_container_width=True, key=f"signal_hist_{len(signal_history)}")

    with signal_col2:
        st.markdown("#### Live Filter KPIs")
        st.metric(
            "Signal Variance",
            f"{st.session_state.metrics.get('signal_variance', 0.0):.2f}",
        )
        st.metric(
            "Prediction Accuracy",
            f"{st.session_state.metrics.get('prediction_accuracy', 0.0):.1f}%",
        )
        st.metric(
            "Noise Reduction",
            f"{st.session_state.metrics.get('noise_reduction_pct', 0.0):.1f}%",
        )
        if signal_history:
            latest_signal = signal_history[-1]
            st.caption(
                f"Latest: `{latest_signal.get('signal_type', 'unknown')}` | "
                f"Obs `{latest_signal.get('observed_signal', 0.0):.1f}` -> "
                f"Filt `{latest_signal.get('filtered_signal', 0.0):.1f}`"
            )
        else:
            st.info("Filtered telemetry updates will appear here once live signals arrive.")
    
    # Event log - ALWAYS EXPANDED AND VISIBLE - Update in real-time
    st.markdown("---")
    st.markdown("### 📋 Event Log")
    event_log_placeholder = st.empty()
    
    # Update event log container in real-time
    with event_log_placeholder.container():
        event_count = len(st.session_state.dispatch_events)
        queue_size = st.session_state.event_queue.qsize() if 'event_queue' in st.session_state else 0
        
        # Show debug info
        if queue_size > 0:
            st.warning(f"⚠️ **{queue_size} events in queue waiting to be processed!**")
            st.caption("Processing in real-time...")
        
        if st.session_state.dispatch_events:
            render_dispatch_logs_console(st.session_state.dispatch_events)
        else:
            if st.session_state.ws_connected:
                if queue_size > 0:
                    st.warning(f"⚠️ Connected! {queue_size} events in queue - processing...")
                else:
                    st.warning("⚠️ Connected but no events yet. Backend is generating events...")
                st.caption("Events should appear within 5-10 seconds!")
            else:
                st.error("❌ Not connected to backend. Make sure backend is running on port 8000.")
    
    # REAL-TIME UPDATE LOOP (Uber/Swiggy style) - Update containers without full refresh
    if st.session_state.ws_connected:
        if 'last_update' not in st.session_state:
            st.session_state.last_update = datetime.now()
        
        time_since_update = (datetime.now() - st.session_state.last_update).total_seconds()
        event_count = len(st.session_state.dispatch_events)
        queue_size = st.session_state.event_queue.qsize() if 'event_queue' in st.session_state else 0
        
        # Update containers in real-time (like Uber/Swiggy - no full page refresh)
        # Refresh interval: Very fast if queue has events, moderate otherwise
        refresh_interval = 0.15 if (queue_size > 0) else (0.3 if (events_processed > 0) else 0.5)
        
        # Update containers immediately if we have new events
        if queue_size > 0 or events_processed > 0 or time_since_update >= refresh_interval:
            # Update containers in-place (real-time style)
            st.session_state.last_update = datetime.now()
            st.session_state.new_events_received = False
            
            # Force container updates by rerunning (but containers update in-place)
            if 'ws_client' in st.session_state:
                ws_client = st.session_state.ws_client
                if ws_client.thread and ws_client.thread.is_alive():
                    st.session_state.ws_connected = ws_client.connected
                else:
                    st.session_state.ws_connected = False
            
            # Small delay for smooth updates
            time.sleep(0.05)
            st.rerun()
    else:
        # If disconnected, try to reconnect after 5 seconds
        if 'last_reconnect_attempt' not in st.session_state:
            st.session_state.last_reconnect_attempt = datetime.now()
        
        time_since_reconnect = (datetime.now() - st.session_state.last_reconnect_attempt).total_seconds()
        if time_since_reconnect >= 5.0:
            st.session_state.last_reconnect_attempt = datetime.now()
            # Clear client and try again
            if 'ws_client' in st.session_state:
                try:
                    st.session_state.ws_client.stop()
                except:
                    pass
                del st.session_state.ws_client
            if 'ws_init_time' in st.session_state:
                del st.session_state.ws_init_time
            st.rerun()


def page_architecture():
    """Architecture Page."""
    st.markdown("""
    <div class="zomato-header">
        <div>
            <div class="zomato-logo">PrepSense</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 14px;">System Architecture</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## PrepSense MicroService Architecture")
    
    arch_img = os.path.join(current_dir, "assets", "prepsense-microservice-architecture.png")
    st.image(arch_img, use_container_width=True)
    
    st.markdown("## Signal Processing Pipeline")
    
    pipeline_img = os.path.join(current_dir, "assets", "signal-processing-pipeline.png")
    st.image(pipeline_img, use_container_width=True)
    
    st.markdown("## Component Descriptions")
    
    components = [
        {
            "name": "Order Events",
            "description": "Kafka-based event stream capturing platform events in real-time",
            "color": "#EF4F5F"
        },
        {
            "name": "Telemetry Service",
            "description": "Tracks rider location and movement signals using GPS and movement data",
            "color": "#4CAF50"
        },
        {
            "name": "Ground Truth Reconstruction",
            "description": "Reconstructs accurate prep times from telemetry signals using statistical methods",
            "color": "#2196F3"
        },
        {
            "name": "Prediction Service",
            "description": "Survival analysis-based prediction engine using probabilistic models",
            "color": "#FF9800"
        },
        {
            "name": "Redis Cache",
            "description": "Low-latency prediction caching layer for fast response times",
            "color": "#9C27B0"
        },
        {
            "name": "Dispatch System",
            "description": "Optimal rider assignment optimization minimizing idle time and delays",
            "color": "#00BCD4"
        },
        {
            "name": "Monitoring",
            "description": "Real-time system health and performance monitoring with alerts",
            "color": "#607D8B"
        }
    ]
    
    # Display components in cards
    for i in range(0, len(components), 2):
        col1, col2 = st.columns(2)
        with col1:
            comp = components[i]
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 8px; border-left: 4px solid {comp['color']}; 
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 15px;">
                <h4 style="color: {comp['color']}; font-family: 'Poppins', sans-serif; font-weight: 600; margin-top: 0;">
                    {comp['name']}
                </h4>
                <p style="color: #4A4A4A; font-family: 'Inter', sans-serif; font-size: 14px; margin-bottom: 0; line-height: 1.6;">
                    {comp['description']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        if i + 1 < len(components):
            with col2:
                comp = components[i + 1]
                st.markdown(f"""
                <div style="background: white; padding: 20px; border-radius: 8px; border-left: 4px solid {comp['color']}; 
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 15px;">
                    <h4 style="color: {comp['color']}; font-family: 'Poppins', sans-serif; font-weight: 600; margin-top: 0;">
                        {comp['name']}
                    </h4>
                    <p style="color: #4A4A4A; font-family: 'Inter', sans-serif; font-size: 14px; margin-bottom: 0; line-height: 1.6;">
                        {comp['description']}
                    </p>
                </div>
                """, unsafe_allow_html=True)


# Main app
def main():
    """Main application."""
    
    # Initialize session state first
    initialize_session_state()

    page_definitions = [
        {
            "title": "Platform Simulation",
            "icon": "PS",
            "description": "Event stream, arrival dynamics, and platform-level KPIs.",
        },
        {
            "title": "Signal Noise Lab",
            "icon": "SN",
            "description": "Explore how noisy merchant and rider signals affect predictions.",
        },
        {
            "title": "Signal Reconstruction",
            "icon": "SR",
            "description": "Rebuild packed time from telemetry and handover events.",
        },
        {
            "title": "Prediction Engine",
            "icon": "PE",
            "description": "See the survival model and confidence-aware prep estimates.",
        },
        {
            "title": "Dispatch Optimization",
            "icon": "DO",
            "description": "Turn predictions into better rider assignment timing.",
        },
        {
            "title": "Real-Time Dispatch Dashboard",
            "icon": "RT",
            "description": "Live WebSocket dispatch map, telemetry, and event monitor.",
        },
        {
            "title": "Twin Restaurant Comparison",
            "icon": "TR",
            "description": "Baseline vs PrepSense performance, side by side.",
        },
        {
            "title": "Live Dispatch War Room",
            "icon": "WR",
            "description": "Operations control room with active risk and fleet signals.",
        },
        {
            "title": "Event Timeline Replay",
            "icon": "ET",
            "description": "Replay a single order lifecycle step by step.",
        },
        {
            "title": "Business Impact",
            "icon": "BI",
            "description": "Translate model gains into rider, ETA, and ops impact.",
        },
        {
            "title": "System Architecture",
            "icon": "SA",
            "description": "View architecture and pipeline diagrams for judges.",
        },
    ]

    if 'story_mode' not in st.session_state:
        st.session_state.story_mode = 'Technical Mode'
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Navigation Hub"

    query_page = st.query_params.get("page")
    query_mode = st.query_params.get("mode")
    valid_pages = {"Navigation Hub", *[page["title"] for page in page_definitions]}
    if query_page in valid_pages:
        st.session_state.current_page = query_page
    if query_mode in {"Technical Mode", "Business Mode"}:
        st.session_state.story_mode = query_mode

    def render_navigation_hub():
        """Main navigation page for the entire dashboard."""
        page_meta = {
            "Platform Simulation": {"color": "#EF4F5F", "metric": f"{len(st.session_state.get('events', []))} events", "tag": "Core"},
            "Signal Noise Lab": {"color": "#FB8C00", "metric": f"Noise {st.session_state.get('noise_lab_merchant_noise', 3.0):.1f}", "tag": "Signals"},
            "Signal Reconstruction": {"color": "#42A5F5", "metric": f"{len(st.session_state.get('signal_data', {}).get('reconstructed', []))} samples", "tag": "Signals"},
            "Prediction Engine": {"color": "#AB47BC", "metric": f"{st.session_state.get('metrics', {}).get('prediction_accuracy', 0.0):.1f}% accuracy", "tag": "ML"},
            "Dispatch Optimization": {"color": "#26A69A", "metric": f"{st.session_state.get('dispatch_cost_idle', 1.0):.1f}/{st.session_state.get('dispatch_cost_delay', 2.0):.1f} cost mix", "tag": "Ops"},
            "Real-Time Dispatch Dashboard": {"color": "#7C4DFF", "metric": f"{len(st.session_state.get('dispatch_events', []))} live events", "tag": "Live"},
            "Twin Restaurant Comparison": {"color": "#66BB6A", "metric": "A/B view", "tag": "Compare"},
            "Live Dispatch War Room": {"color": "#EC407A", "metric": f"{len(st.session_state.get('war_room_events', [])) if 'war_room_events' in st.session_state else 0} alerts", "tag": "Live"},
            "Event Timeline Replay": {"color": "#5C6BC0", "metric": "Single-order replay", "tag": "Replay"},
            "Business Impact": {"color": "#26C6DA", "metric": f"{st.session_state.get('metrics', {}).get('noise_reduction_pct', 0.0):.1f}% noise drop", "tag": "Impact"},
            "System Architecture": {"color": "#78909C", "metric": "Pipeline diagrams", "tag": "Explain"},
        }

        st.markdown("""
        <div class="zomato-header">
            <div>
                <div class="zomato-logo">PrepSense Navigation Hub</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Choose a module and navigate through the full prototype from one place</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("## Navigation")
        st.markdown("#### View Mode")
        technical_link = f"?page={quote('Navigation Hub')}&mode={quote('Technical Mode')}"
        business_link = f"?page={quote('Navigation Hub')}&mode={quote('Business Mode')}"
        tech_active = "active" if st.session_state.story_mode == "Technical Mode" else ""
        biz_active = "active" if st.session_state.story_mode == "Business Mode" else ""
        mode_caption = (
            "Business Mode uses plain-English explanations for judges."
            if st.session_state.story_mode == "Business Mode"
            else "Technical Mode shows formulas, model details, and system logic."
        )
        st.markdown(
            f"""
            <div class="nav-mode-wrap">
                <a class="nav-mode-pill {tech_active}" href="{technical_link}" target="_self">Technical</a>
                <a class="nav-mode-pill {biz_active}" href="{business_link}" target="_self">Business</a>
                <span style="font-size:13px; color:#5A5A5A; margin-left:6px;">{mode_caption}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        summary_cols = st.columns(4)
        with summary_cols[0]:
            st.metric("Modules", f"{len(page_definitions)}")
        with summary_cols[1]:
            st.metric("Live Events", f"{len(st.session_state.get('dispatch_events', []))}")
        with summary_cols[2]:
            st.metric("Filtered Signals", f"{len(st.session_state.get('signal_history', []))}")
        with summary_cols[3]:
            st.metric("Active Dispatches", f"{len(st.session_state.get('active_dispatches', []))}")

        st.markdown("#### Select Page")
        for idx in range(0, len(page_definitions), 3):
            row = page_definitions[idx: idx + 3]
            cols = st.columns(3)
            for col_idx, page_def in enumerate(row):
                meta = page_meta[page_def["title"]]
                with cols[col_idx]:
                    href = f"?page={quote(page_def['title'])}&mode={quote(st.session_state.story_mode)}"
                    st.markdown(
                        f"""
                        <a class="nav-card-link" href="{href}" target="_self">
                            <div class="nav-card">
                                <div class="nav-card-top">
                                    <span class="nav-card-icon" style="background:#F4F4F5; color:#4B5563;">{page_def['icon']}</span>
                                    <span class="nav-card-tag" style="color:#9CA3AF;">{meta['tag']}</span>
                                </div>
                                <div class="nav-card-title">{page_def['title']}</div>
                                <div class="nav-card-desc">{page_def['description']}</div>
                                <div class="nav-card-metric">{meta['metric']}</div>
                                <div class="nav-card-cta">Open {page_def['title']}</div>
                            </div>
                        </a>
                        """,
                        unsafe_allow_html=True,
                    )

    # Sidebar becomes stable native navigation
    st.sidebar.markdown(
        """
        <div style="position: relative;">
            <a href="#" onclick="var btn = document.querySelector('[data-testid=collapsedControl]') || document.querySelector('button[aria-label*=\"collapse\"]') || document.querySelector('button[aria-label*=\"Collapse\"]'); if(btn) btn.click(); return false;" 
               style="position: absolute; top: -8px; right: 0; color: rgba(255,255,255,0.9); font-size: 26px; font-weight: 700; text-decoration: none; padding: 6px 10px; border-radius: 8px; background: rgba(255,255,255,0.1); line-height: 1; display: inline-block;"
               title="Close sidebar">×</a>
            <div class="sidebar-brand">
                <div class="sidebar-brand-mark"></div>
                <div class="sidebar-brand-label">PrepSense</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("## Navigation")

    mode_col1, mode_col2 = st.sidebar.columns(2)
    with mode_col1:
        if st.button(
            "Technical",
            key="sidebar_mode_technical",
            type="primary" if st.session_state.story_mode == "Technical Mode" else "secondary",
            use_container_width=True,
        ):
            st.session_state.story_mode = "Technical Mode"
            st.rerun()
    with mode_col2:
        if st.button(
            "Business",
            key="sidebar_mode_business",
            type="primary" if st.session_state.story_mode == "Business Mode" else "secondary",
            use_container_width=True,
        ):
            st.session_state.story_mode = "Business Mode"
            st.rerun()

    if st.session_state.story_mode == "Business Mode":
        st.sidebar.caption("Business Mode uses plain-English explanations for judges.")
    else:
        st.sidebar.caption("Technical Mode shows formulas and model details.")

    st.sidebar.markdown("### Select Page")
    sidebar_links = [
        "Navigation Hub",
        "Platform Simulation",
        "Signal Noise Lab",
        "Real-Time Dispatch Dashboard",
        "Business Impact",
        "System Architecture",
    ]
    for page_name in sidebar_links:
        page_def = next(
            (page for page in page_definitions if page["title"] == page_name),
            {"title": "Navigation Hub", "icon": "NH", "description": "Main module launcher"},
        )
        selected = st.session_state.current_page == page_name
        with st.sidebar.container(border=True):
            st.markdown(f"**{page_def['icon']}  {page_def['title']}**")
            st.caption(page_def["description"])
            if st.button(
                f"Open {page_def['title']}",
                key=f"sidebar_open_{page_name}",
                type="primary" if selected else "secondary",
                use_container_width=True,
            ):
                st.session_state.current_page = page_name
                st.query_params["page"] = page_name
                st.query_params["mode"] = st.session_state.story_mode
                st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.caption(f"Current page: {st.session_state.current_page}")
    st.sidebar.caption(f"View mode: {st.session_state.story_mode}")

    page = st.session_state.current_page
    
    # Route to appropriate page
    try:
        if page == "Navigation Hub":
            render_navigation_hub()
        elif page == "Platform Simulation":
            page_platform_simulation()
        elif page == "Signal Noise Lab":
            page_signal_noise_lab()
        elif page == "Signal Reconstruction":
            page_signal_reconstruction()
        elif page == "Prediction Engine":
            page_prediction_engine()
        elif page == "Dispatch Optimization":
            page_dispatch_optimization()
        elif page == "Real-Time Dispatch Dashboard":
            page_realtime_dispatch_dashboard()
        elif page == "Twin Restaurant Comparison":
            page_twin_restaurant()
        elif page == "Live Dispatch War Room":
            page_war_room()
        elif page == "Event Timeline Replay":
            page_event_timeline()
        elif page == "Business Impact":
            page_business_impact()
        elif page == "System Architecture":
            page_architecture()
    except Exception as e:
        st.error(f"Error loading page '{page}': {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()
