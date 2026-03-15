"""
Telemetry Signal Generation Module

Generates rider arrival and pickup telemetry signals.
"""

import numpy as np
from datetime import datetime, timedelta


class TelemetryGenerator:
    """Generate telemetry signals for order tracking."""
    
    def __init__(self, travel_time_mean=10, travel_time_std=3, 
                 handover_mean=2, handover_std=1):
        """
        Initialize telemetry generator.
        
        Parameters:
        -----------
        travel_time_mean : float
            Mean travel time for rider (minutes)
        travel_time_std : float
            Standard deviation of travel time
        handover_mean : float
            Mean handover delay (minutes)
        handover_std : float
            Standard deviation of handover delay
        """
        self.travel_time_mean = travel_time_mean
        self.travel_time_std = travel_time_std
        self.handover_mean = handover_mean
        self.handover_std = handover_std
    
    def generate_rider_arrival(self, order_time):
        """
        Generate rider arrival time.
        
        Parameters:
        -----------
        order_time : datetime
            Order placement time
        
        Returns:
        --------
        datetime
            Rider arrival time
        """
        travel_time = np.random.normal(self.travel_time_mean, self.travel_time_std)
        travel_time = max(2, travel_time)  # Minimum travel time
        
        arrival_time = order_time + timedelta(minutes=travel_time)
        return arrival_time
    
    def generate_pickup_time(self, packed_time):
        """
        Generate pickup time with handover delay.
        
        Parameters:
        -----------
        packed_time : datetime
            When order is packed
        
        Returns:
        --------
        tuple
            (pickup_time, handover_delay)
        """
        # handover_delay ~ Normal(2, 1)
        handover_delay = np.random.normal(self.handover_mean, self.handover_std)
        handover_delay = max(0.5, handover_delay)  # Minimum delay
        
        pickup_time = packed_time + timedelta(minutes=handover_delay)
        return pickup_time, handover_delay
    
    def compute_waiting_time(self, arrival_time, pickup_time):
        """
        Compute rider waiting time.
        
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
    
    def generate_telemetry(self, order_time, packed_time):
        """
        Generate complete telemetry signals.
        
        Parameters:
        -----------
        order_time : datetime
            Order placement time
        packed_time : datetime
            Packed time
        
        Returns:
        --------
        dict
            Complete telemetry data
        """
        arrival_time = self.generate_rider_arrival(order_time)
        pickup_time, handover_delay = self.generate_pickup_time(packed_time)
        waiting_time = self.compute_waiting_time(arrival_time, pickup_time)
        
        return {
            'arrival_time': arrival_time,
            'pickup_time': pickup_time,
            'handover_delay': handover_delay,
            'waiting_time': waiting_time
        }
