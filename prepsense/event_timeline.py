"""
Event Timeline Replay Module

Allows users to replay an order lifecycle and see prediction updates.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from event_stream import EventStream, EventType
from kitchen_simulator import KitchenSimulator
from telemetry_service import TelemetryService
from reconstruction_service import ReconstructionService
from survival_prediction import SurvivalPrediction


class OrderLifecycleReplay:
    """Replay a single order's lifecycle."""
    
    def __init__(self):
        self.kitchen = KitchenSimulator()
        self.telemetry_service = TelemetryService()
        self.reconstructor = ReconstructionService()
        self.predictor = SurvivalPrediction(distribution='gamma')
        
    def generate_order_lifecycle(self, order_id="ORD_001"):
        """Generate complete order lifecycle with prediction updates."""
        order_time = datetime.now() - timedelta(hours=1)
        
        # Simulate kitchen processing
        kitchen_result = self.kitchen.process_order(order_time)
        true_prep_time = kitchen_result['kpt_true']
        packed_time = order_time + timedelta(minutes=true_prep_time)
        
        # Generate telemetry
        telemetry = self.telemetry_service.generate_telemetry(
            order_id, order_time, packed_time
        )
        
        # Timeline events
        timeline = [
            {
                'time': order_time,
                'event': 'ORDER_CREATED',
                'description': 'Order placed by customer',
                'prediction': None,
                'confidence': None
            },
            {
                'time': order_time + timedelta(minutes=2),
                'event': 'RIDER_ASSIGNED',
                'description': 'Rider assigned to order',
                'prediction': None,
                'confidence': None
            },
            {
                'time': telemetry['arrival_time'],
                'event': 'RIDER_ARRIVED',
                'description': 'Rider arrived at restaurant',
                'prediction': None,
                'confidence': None
            },
            {
                'time': packed_time,
                'event': 'ORDER_PACKED',
                'description': 'Food ready for pickup',
                'prediction': true_prep_time,
                'confidence': 0.5
            },
            {
                'time': telemetry['pickup_time'],
                'event': 'ORDER_PICKED_UP',
                'description': 'Rider picked up order',
                'prediction': None,
                'confidence': None
            }
        ]
        
        # Add prediction updates
        for i, event in enumerate(timeline):
            if event['time'] >= telemetry['arrival_time']:
                # After rider arrives, we can reconstruct
                recon_result = self.reconstructor.reconstruct_from_telemetry(telemetry)
                event['prediction'] = recon_result['kpt_reconstructed']
                event['confidence'] = np.random.uniform(1.0, 2.5)
        
        return {
            'order_id': order_id,
            'timeline': timeline,
            'true_prep_time': true_prep_time,
            'final_prediction': timeline[-2]['prediction'] if timeline[-2]['prediction'] else None
        }


def create_timeline_replay_chart(lifecycle):
    """Create timeline visualization."""
    timeline = lifecycle['timeline']
    
    fig = go.Figure()
    
    # Add timeline line
    times = [event['time'] for event in timeline]
    fig.add_trace(go.Scatter(
        x=times,
        y=[i for i in range(len(timeline))],
        mode='lines+markers',
        line=dict(color='#2196F3', width=3),
        marker=dict(size=12, color='#2196F3'),
        name='Timeline',
        showlegend=False
    ))
    
    # Add event annotations - larger, high-contrast text
    for i, event in enumerate(timeline):
        color = '#EF4F5F' if event['event'] == 'ORDER_CREATED' else \
                '#2196F3' if event['event'] == 'RIDER_ASSIGNED' else \
                '#4CAF50' if event['event'] == 'RIDER_ARRIVED' else \
                '#FF9800' if event['event'] == 'ORDER_PACKED' else '#9C27B0'
        
        fig.add_annotation(
            x=event['time'],
            y=i,
            text=f"<b>{event['event']}</b><br>{event['description']}",
            showarrow=True,
            arrowhead=2,
            arrowcolor=color,
            bgcolor='white',
            bordercolor=color,
            borderwidth=2,
            font=dict(size=14, color='#000000', family='Inter')
        )
        
        if event['prediction']:
            fig.add_annotation(
                x=event['time'],
                y=i + 0.3,
                text=f"Prediction: {event['prediction']:.1f} min<br>Confidence: ±{event['confidence']:.1f} min",
                showarrow=False,
                bgcolor='#E8F5E9',
                bordercolor='#4CAF50',
                borderwidth=1,
                font=dict(size=13, color='#000000', family='Inter')
            )
    
    fig.update_layout(
        title=dict(text=f"Order Lifecycle: {lifecycle['order_id']}",
                  font=dict(family='Poppins', size=20, color='#000000')),
        xaxis=dict(
            title="Time",
            title_font=dict(size=14, color='#000000'),
            tickfont=dict(size=13, color='#000000'),
            showgrid=True,
            gridcolor='#E0E0E0'
        ),
        yaxis=dict(
            title="Event",
            title_font=dict(size=14, color='#000000'),
            tickfont=dict(size=13, color='#000000'),
            showgrid=False,
            tickmode='array',
            tickvals=list(range(len(timeline))),
            ticktext=[e['event'] for e in timeline]
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        font=dict(family='Inter', size=14, color='#000000')
    )
    
    return fig
