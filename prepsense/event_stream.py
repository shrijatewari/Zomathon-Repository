"""
Event Stream Module - Kafka-like Platform Event Simulation

Simulates Zomato platform events: ORDER_CREATED, RIDER_ASSIGNED, RIDER_ARRIVED, ORDER_PICKED_UP
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import deque
from enum import Enum


class EventType(Enum):
    """Platform event types."""
    ORDER_CREATED = "ORDER_CREATED"
    RIDER_ASSIGNED = "RIDER_ASSIGNED"
    RIDER_ARRIVED = "RIDER_ARRIVED"
    ORDER_PICKED_UP = "ORDER_PICKED_UP"


class EventStream:
    """Simulates Kafka-like event stream for food delivery platform."""
    
    def __init__(self, arrival_rate=0.5, random_seed=42):
        """
        Initialize event stream.
        
        Parameters:
        -----------
        arrival_rate : float
            Lambda parameter for Poisson process (orders per minute)
        random_seed : int
            Random seed for reproducibility
        """
        self.arrival_rate = arrival_rate
        self.events = deque()
        self.order_counter = 0
        self.rider_counter = 0
        np.random.seed(random_seed)
    
    def generate_order_event(self, current_time):
        """
        Generate ORDER_CREATED event using Poisson process.
        
        Parameters:
        -----------
        current_time : datetime
            Current simulation time
        
        Returns:
        --------
        dict or None
            Event dictionary if order created, None otherwise
        """
        # Poisson process: N(t) ~ Poisson(lambda)
        prob = np.random.random()
        lambda_t = self.arrival_rate / 60  # Convert to per second
        
        if prob < lambda_t:
            self.order_counter += 1
            store_id = np.random.randint(1, 101)
            
            event = {
                'event_id': f"EVT_{self.order_counter:06d}",
                'event_type': EventType.ORDER_CREATED.value,
                'timestamp': current_time,
                'order_id': f"ORD_{self.order_counter:06d}",
                'store_id': store_id,
                'metadata': {
                    'order_value': np.random.uniform(200, 2000),
                    'items_count': np.random.randint(1, 10)
                }
            }
            return event
        return None
    
    def generate_rider_assigned_event(self, order_id, current_time):
        """
        Generate RIDER_ASSIGNED event.
        
        Parameters:
        -----------
        order_id : str
            Order ID
        current_time : datetime
            Assignment time
        
        Returns:
        --------
        dict
            Event dictionary
        """
        self.rider_counter += 1
        return {
            'event_id': f"EVT_{self.order_counter:06d}_RIDER",
            'event_type': EventType.RIDER_ASSIGNED.value,
            'timestamp': current_time,
            'order_id': order_id,
            'rider_id': f"RIDER_{self.rider_counter:06d}",
            'metadata': {
                'distance_km': np.random.uniform(1, 10),
                'estimated_travel_time': np.random.uniform(5, 20)
            }
        }
    
    def generate_rider_arrived_event(self, order_id, rider_id, arrival_time):
        """
        Generate RIDER_ARRIVED event.
        
        Parameters:
        -----------
        order_id : str
            Order ID
        rider_id : str
            Rider ID
        arrival_time : datetime
            Arrival time
        
        Returns:
        --------
        dict
            Event dictionary
        """
        return {
            'event_id': f"EVT_{self.order_counter:06d}_ARRIVED",
            'event_type': EventType.RIDER_ARRIVED.value,
            'timestamp': arrival_time,
            'order_id': order_id,
            'rider_id': rider_id,
            'metadata': {
                'location_lat': np.random.uniform(17.0, 18.0),
                'location_lon': np.random.uniform(78.0, 79.0)
            }
        }
    
    def generate_pickup_event(self, order_id, rider_id, pickup_time):
        """
        Generate ORDER_PICKED_UP event.
        
        Parameters:
        -----------
        order_id : str
            Order ID
        rider_id : str
            Rider ID
        pickup_time : datetime
            Pickup time
        
        Returns:
        --------
        dict
            Event dictionary
        """
        return {
            'event_id': f"EVT_{self.order_counter:06d}_PICKUP",
            'event_type': EventType.ORDER_PICKED_UP.value,
            'timestamp': pickup_time,
            'order_id': order_id,
            'rider_id': rider_id,
            'metadata': {
                'handover_duration': np.random.normal(2, 0.5)
            }
        }
    
    def simulate_time_window(self, start_time, duration_minutes):
        """
        Simulate events over a time window.
        
        Parameters:
        -----------
        start_time : datetime
            Start time
        duration_minutes : float
            Duration in minutes
        
        Returns:
        --------
        list
            List of events
        """
        events = []
        current_time = start_time
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        while current_time < end_time:
            # Generate order events
            order_event = self.generate_order_event(current_time)
            if order_event:
                events.append(order_event)
            
            # Advance time (simulate second by second)
            current_time += timedelta(seconds=1)
        
        return events
    
    def get_events_by_type(self, events, event_type):
        """
        Filter events by type.
        
        Parameters:
        -----------
        events : list
            List of events
        event_type : EventType
            Event type to filter
        
        Returns:
        --------
        list
            Filtered events
        """
        return [e for e in events if e['event_type'] == event_type.value]
    
    def to_dataframe(self, events):
        """
        Convert events to DataFrame.
        
        Parameters:
        -----------
        events : list
            List of events
        
        Returns:
        --------
        pd.DataFrame
            Events DataFrame
        """
        if not events:
            return pd.DataFrame()
        
        df = pd.DataFrame(events)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
