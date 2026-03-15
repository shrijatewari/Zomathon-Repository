"""
PrepSense Real-Time Dispatch Dashboard

Streamlit frontend that connects to FastAPI WebSocket backend
to display live dispatch decisions and visualizations.
"""

import streamlit as st
import json
import plotly.graph_objects as go
from datetime import datetime
from typing import Dict, List, Optional
import sys
import os
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.rider_map import create_rider_map
from frontend.metrics_panel import render_metrics_panel, render_dispatch_cards
from frontend.websocket_client import get_websocket_client


# WebSocket configuration
WEBSOCKET_URL = "ws://localhost:8000/ws/dispatch"


def initialize_session_state():
    """Initialize session state variables."""
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
            'delay_change': 0.0
        }
    
    if 'ws_connected' not in st.session_state:
        st.session_state.ws_connected = False
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()


def on_websocket_message(data: dict):
    """Callback function for WebSocket messages."""
    # Process event
    process_dispatch_event(data)
    st.session_state.last_update = datetime.now()


def process_dispatch_event(event: Dict):
    """Process incoming dispatch event and update session state."""
    event_type = event.get('event_type', '')
    order_id = event.get('order_id', '')
    
    # Add to event history
    st.session_state.dispatch_events.append({
        **event,
        'processed_at': datetime.now().isoformat()
    })
    
    # Keep only last 100 events
    if len(st.session_state.dispatch_events) > 100:
        st.session_state.dispatch_events = st.session_state.dispatch_events[-100:]
    
    # Handle different event types
    if event_type == 'ORDER_CREATED':
        # Add restaurant if new
        restaurant_id = event.get('restaurant_id')
        if restaurant_id:
            restaurant = {
                'id': restaurant_id,
                'lat': event.get('restaurant_lat', 0),
                'lon': event.get('restaurant_lon', 0)
            }
            if not any(r['id'] == restaurant_id for r in st.session_state.restaurants):
                st.session_state.restaurants.append(restaurant)
    
    elif event_type == 'KPT_PREDICTED':
        # Update metrics
        st.session_state.metrics['total_orders'] += 1
    
    elif event_type == 'RIDER_DISPATCHED':
        # Add to active dispatches
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
        
        # Update or add dispatch
        existing = next(
            (d for d in st.session_state.active_dispatches if d['order_id'] == order_id),
            None
        )
        if existing:
            existing.update(dispatch)
        else:
            st.session_state.active_dispatches.append(dispatch)
        
        # Update rider status
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
        # Update rider position
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
        # Remove from active dispatches
        st.session_state.active_dispatches = [
            d for d in st.session_state.active_dispatches if d['order_id'] != order_id
        ]
        
        # Mark rider as available
        rider_id = event.get('rider_id')
        if rider_id:
            rider = next(
                (r for r in st.session_state.riders if r.get('id') == rider_id),
                None
            )
            if rider:
                rider['available'] = True
    
    # Update metrics
    update_metrics()


def update_metrics():
    """Update aggregated metrics from active dispatches."""
    dispatches = st.session_state.active_dispatches
    
    if dispatches:
        avg_idle_risk = sum(d.get('idle_risk', 0) for d in dispatches) / len(dispatches)
        avg_delay_risk = sum(d.get('delay_risk', 0) for d in dispatches) / len(dispatches)
        
        # Estimate idle time from risk (simplified)
        avg_idle_time = avg_idle_risk * 5.0  # Assume avg 5 min if idle
        
        # Efficiency = 1 - (idle_risk + delay_risk) / 2
        efficiency = (1 - (avg_idle_risk + avg_delay_risk) / 2) * 100
        
        st.session_state.metrics.update({
            'avg_idle_time': avg_idle_time,
            'dispatch_efficiency': efficiency,
            'delay_probability': avg_delay_risk * 100,
            'active_dispatches': len(dispatches)
        })


def main():
    """Main Streamlit dashboard."""
    st.set_page_config(
        page_title="PrepSense Dispatch Dashboard",
        page_icon="🚴",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .zomato-header {
        background: linear-gradient(135deg, #EF4F5F 0%, #D32F2F 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .zomato-logo {
        font-family: 'Poppins', sans-serif;
        font-size: 32px;
        font-weight: bold;
        color: white;
        margin-bottom: 5px;
    }
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="zomato-header">
        <div class="zomato-logo">🚴 PrepSense Dispatch Engine</div>
        <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Real-Time Rider Assignment & Optimization</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Initialize WebSocket client
    try:
        ws_client = get_websocket_client(WEBSOCKET_URL, on_websocket_message)
        st.session_state.ws_connected = ws_client.connected
    except Exception as e:
        st.session_state.ws_connected = False
        st.error(f"WebSocket error: {e}")
    
    # Connection status
    col_status, col_info = st.columns([1, 3])
    with col_status:
        if st.session_state.ws_connected:
            st.success("🟢 Connected")
        else:
            st.error("🔴 Disconnected")
            st.caption("Make sure backend is running on port 8000")
            if st.button("🔄 Reconnect"):
                st.session_state.ws_connected = False
                if 'ws_client' in locals():
                    ws_client.stop()
                st.rerun()
    
    with col_info:
        st.caption(f"WebSocket: {WEBSOCKET_URL}")
        st.caption(f"Last update: {st.session_state.last_update.strftime('%H:%M:%S')}")
    
    # Main layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🗺️ Live Dispatch Map")
        
        # Create map
        if st.session_state.restaurants or st.session_state.riders:
            orders = [
                {
                    'order_id': d['order_id'],
                    'restaurant_id': d.get('restaurant_id'),
                    'rider_id': d.get('rider_id')
                }
                for d in st.session_state.active_dispatches
            ]
            
            fig = create_rider_map(
                restaurants=st.session_state.restaurants,
                riders=st.session_state.riders,
                orders=orders,
                title="Real-Time Dispatch Operations"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Waiting for events... Map will appear when orders are created.")
    
    with col2:
        # Metrics panel
        render_metrics_panel(st.session_state.metrics)
        
        st.divider()
        
        # Dispatch cards
        render_dispatch_cards(st.session_state.active_dispatches)
    
    # Event log
    with st.expander("📋 Event Log", expanded=False):
        if st.session_state.dispatch_events:
            recent_events = st.session_state.dispatch_events[-20:]
            for event in reversed(recent_events):
                event_type = event.get('event_type', 'UNKNOWN')
                order_id = event.get('order_id', 'N/A')
                timestamp = event.get('timestamp', '')[:19]  # Remove microseconds
                
                icon_map = {
                    'ORDER_CREATED': '📦',
                    'KPT_PREDICTED': '🔮',
                    'RIDER_DISPATCHED': '🚴',
                    'RIDER_MOVED': '📍',
                    'RIDER_ARRIVED': '✅',
                    'ORDER_PICKED_UP': '🎉'
                }
                
                icon = icon_map.get(event_type, '📌')
                st.markdown(f"{icon} **{event_type}** - Order {order_id} - {timestamp}")
        else:
            st.info("No events yet. Waiting for WebSocket connection...")
    
    # Auto-refresh every 2 seconds to show new events
    if st.session_state.ws_connected:
        time.sleep(0.1)  # Small delay to allow WebSocket messages to process
        st.rerun()
    
    # Note about WebSocket
    st.sidebar.markdown("### ℹ️ Setup Instructions")
    st.sidebar.markdown("""
    1. **Start Backend:**
       ```bash
       cd prepsense/backend
       uvicorn websocket_server:app --reload
       ```
    
    2. **Start Frontend:**
       ```bash
       streamlit run frontend/dispatch_dashboard.py
       ```
    
    3. **View Dashboard:**
       Open http://localhost:8504
    """)


if __name__ == "__main__":
    # Note: Streamlit doesn't support async WebSocket clients directly
    # In production, you'd use a separate thread or process
    # For now, we'll use polling/refresh mechanism
    
    main()
