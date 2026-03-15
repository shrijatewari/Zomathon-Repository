"""
Telemetry Service - Rider Location and Movement Tracking

Simulates rider telemetry signals for order tracking.
"""

import numpy as np
from datetime import datetime, timedelta


class TelemetryService:
    """Service for generating and managing rider telemetry."""
    
    def __init__(self, travel_time_mean=10, travel_time_std=3,
                 handover_mean=2, handover_std=1, random_seed=42):
        """
        Initialize telemetry service.
        
        Parameters:
        -----------
        travel_time_mean : float
            Mean travel time (minutes)
        travel_time_std : float
            Standard deviation of travel time
        handover_mean : float
            Mean handover delay (minutes)
        handover_std : float
            Standard deviation of handover delay
        random_seed : int
            Random seed
        """
        self.travel_time_mean = travel_time_mean
        self.travel_time_std = travel_time_std
        self.handover_mean = handover_mean
        self.handover_std = handover_std
        np.random.seed(random_seed)
        self.telemetry_log = []
    
    def generate_travel_time(self):
        """
        Generate travel time for rider.
        
        Returns:
        --------
        float
            Travel time in minutes
        """
        travel_time = np.random.normal(self.travel_time_mean, self.travel_time_std)
        return max(2, travel_time)  # Minimum travel time
    
    def generate_rider_arrival(self, order_time):
        """
        Generate rider arrival time.
        
        T_arrival = T_order + travel_time
        
        Parameters:
        -----------
        order_time : datetime
            Order placement time
        
        Returns:
        --------
        datetime
            Rider arrival time
        """
        travel_time = self.generate_travel_time()
        arrival_time = order_time + timedelta(minutes=travel_time)
        
        return arrival_time, travel_time
    
    def generate_pickup_time(self, packed_time):
        """
        Generate pickup time with handover delay.
        
        T_pickup = T_p + handover_delay
        handover_delay ~ Normal(2, 1)
        
        Parameters:
        -----------
        packed_time : datetime
            Packed time
        
        Returns:
        --------
        tuple
            (pickup_time, handover_delay)
        """
        handover_delay = np.random.normal(self.handover_mean, self.handover_std)
        handover_delay = max(0.5, handover_delay)
        
        pickup_time = packed_time + timedelta(minutes=handover_delay)
        
        return pickup_time, handover_delay
    
    def compute_waiting_time(self, arrival_time, pickup_time):
        """
        Compute rider waiting time.
        
        W = T_pickup - T_arrival
        
        Parameters:
        -----------
        arrival_time : datetime
            Rider arrival time
        pickup_time : datetime
            Pickup time
        
        Returns:
        --------
        float
            Waiting time in minutes
        """
        waiting_time = (pickup_time - arrival_time).total_seconds() / 60
        return max(0, waiting_time)
    
    def generate_telemetry(self, order_id, order_time, packed_time):
        """
        Generate complete telemetry for an order.
        
        Z = {T_order, T_arrival, T_pickup}
        
        Parameters:
        -----------
        order_id : str
            Order ID
        order_time : datetime
            Order placement time
        packed_time : datetime
            Packed time
        
        Returns:
        --------
        dict
            Complete telemetry data
        """
        arrival_time, travel_time = self.generate_rider_arrival(order_time)
        pickup_time, handover_delay = self.generate_pickup_time(packed_time)
        waiting_time = self.compute_waiting_time(arrival_time, pickup_time)
        
        telemetry = {
            'order_id': order_id,
            'order_time': order_time,
            'arrival_time': arrival_time,
            'pickup_time': pickup_time,
            'travel_time': travel_time,
            'handover_delay': handover_delay,
            'waiting_time': waiting_time
        }
        
        self.telemetry_log.append(telemetry)
        return telemetry
    
    def get_telemetry_history(self):
        """
        Get telemetry history.
        
        Returns:
        --------
        list
            List of telemetry records
        """
        return self.telemetry_log.copy()
