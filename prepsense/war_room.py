"""
Live Dispatch War Room Module

Creates a control room style dashboard showing real-time platform operations.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from event_stream import EventStream, EventType
from kitchen_simulator import KitchenSimulator
from telemetry_service import TelemetryService
from reconstruction_service import ReconstructionService
from survival_prediction import SurvivalPrediction
from dispatch_optimizer import DispatchOptimizer


class WarRoomSimulator:
    """Simulates live platform operations for war room dashboard."""
    
    def __init__(self):
        self.events = []
        self.current_orders = {}
        self.kitchen = KitchenSimulator()
        self.telemetry_service = TelemetryService()
        self.reconstructor = ReconstructionService()
        self.predictor = None
        
    def generate_live_events(self, duration_minutes=5, arrival_rate=0.5):
        """Generate live event stream."""
        event_stream = EventStream(arrival_rate=arrival_rate)
        start_time = datetime.now() - timedelta(minutes=duration_minutes)
        events = event_stream.simulate_time_window(start_time, duration_minutes)
        
        # Process events
        processed_events = []
        for event in events:
            if event['event_type'] == EventType.ORDER_CREATED.value:
                order_id = event['order_id']
                order_time = pd.to_datetime(event['timestamp'])
                
                # Simulate kitchen processing
                kitchen_result = self.kitchen.process_order(order_time)
                
                # Generate telemetry
                packed_time = order_time + timedelta(minutes=kitchen_result['kpt_true'])
                telemetry = self.telemetry_service.generate_telemetry(
                    order_id, order_time, packed_time
                )
                
                # Reconstruct and predict
                recon_result = self.reconstructor.reconstruct_from_telemetry(telemetry)
                
                processed_events.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                    'event_type': event['event_type'],
                    'order_id': order_id,
                    'store_id': event['store_id'],
                    'kitchen_queue': kitchen_result['queue_length'],
                    'predicted_prep': recon_result['kpt_reconstructed'],
                    'confidence': np.random.uniform(1.5, 3.0),
                    'idle_risk': 'LOW' if recon_result['kpt_reconstructed'] < 15 else 'MEDIUM' if recon_result['kpt_reconstructed'] < 25 else 'HIGH'
                })
            else:
                # Add other event types with current timestamp
                event['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                processed_events.append(event)
        
        return processed_events
    
    def get_live_metrics(self, events):
        """Extract live metrics from events."""
        if not events:
            return {}
        
        df = pd.DataFrame(events)
        order_events = df[df['event_type'] == EventType.ORDER_CREATED.value]
        
        if len(order_events) == 0:
            return {
                'total_orders': 0,
                'avg_queue': 0,
                'avg_prediction': 0,
                'high_risk_orders': 0
            }
        
        return {
            'total_orders': len(order_events),
            'avg_queue': order_events['kitchen_queue'].mean() if 'kitchen_queue' in order_events.columns else 0,
            'avg_prediction': order_events['predicted_prep'].mean() if 'predicted_prep' in order_events.columns else 0,
            'high_risk_orders': len(order_events[order_events.get('idle_risk', pd.Series()) == 'HIGH']) if 'idle_risk' in order_events.columns else 0
        }


def create_war_room_map(events, restaurants, riders):
    """Create map visualization for war room."""
    fig = go.Figure()
    
    # Add restaurants
    for i, restaurant in enumerate(restaurants):
        fig.add_trace(go.Scatter(
            x=[restaurant.get('lon', 0)],
            y=[restaurant.get('lat', 0)],
            mode='markers',
            marker=dict(size=15, color='#EF4F5F', symbol='square'),
            name='Restaurant',
            text=[f"Restaurant {i+1}"],
            hovertemplate='<b>%{text}</b><extra></extra>'
        ))
    
    # Add riders
    for i, rider in enumerate(riders):
        fig.add_trace(go.Scatter(
            x=[rider.get('lon', 0)],
            y=[rider.get('lat', 0)],
            mode='markers',
            marker=dict(size=12, color='#4CAF50', symbol='circle'),
            name='Rider',
            text=[f"Rider {i+1}"],
            hovertemplate='<b>%{text}</b><extra></extra>'
        ))
    
    # Add order connections
    if events:
        df = pd.DataFrame(events)
        order_events = df[df['event_type'] == EventType.ORDER_CREATED.value]
        
        for idx, order in order_events.head(10).iterrows():
            rest_idx = order.get('store_id', 0) % len(restaurants)
            rider_idx = idx % len(riders)
            
            fig.add_trace(go.Scatter(
                x=[restaurants[rest_idx].get('lon', 0), riders[rider_idx].get('lon', 0)],
                y=[restaurants[rest_idx].get('lat', 0), riders[rider_idx].get('lat', 0)],
                mode='lines',
                line=dict(color='#FF9800', width=2, dash='dash'),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    fig.update_layout(
        title=dict(text="Live Platform Operations Map", 
                  font=dict(family='Poppins', size=18, color='#1C1C1C')),
        xaxis=dict(title="Longitude", showgrid=True, gridcolor='#E0E0E0'),
        yaxis=dict(title="Latitude", showgrid=True, gridcolor='#E0E0E0'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        showlegend=True,
        legend=dict(font=dict(size=12, color='#1C1C1C'))
    )
    
    return fig
