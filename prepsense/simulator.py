"""
Order and Kitchen Simulation Module

Simulates order arrivals using Poisson process and maintains kitchen queue.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class KitchenSimulator:
    """Simulate kitchen operations with order arrivals and queue management."""
    
    def __init__(self, arrival_rate=0.5, mu0=0.1, alpha=0.5, beta=0.3, gamma=0.2):
        """
        Initialize kitchen simulator.
        
        Parameters:
        -----------
        arrival_rate : float
            Lambda parameter for Poisson process (orders per minute)
        mu0 : float
            Base service rate
        alpha : float
            Queue weight factor
        beta : float
            Rider weight factor
        gamma : float
            Load impact factor
        """
        self.arrival_rate = arrival_rate
        self.mu0 = mu0
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        
        # State variables
        self.queue_length = 0
        self.riders_waiting = 0
        self.current_time = datetime.now()
        self.order_history = []
    
    def simulate_arrival(self, time_delta_minutes=1):
        """
        Simulate order arrivals using Poisson process.
        
        Parameters:
        -----------
        time_delta_minutes : float
            Time step in minutes
        
        Returns:
        --------
        int
            Number of new orders
        """
        # Poisson process: N(t) ~ Poisson(lambda * t)
        lambda_t = self.arrival_rate * time_delta_minutes
        num_arrivals = np.random.poisson(lambda_t)
        
        return num_arrivals
    
    def update_queue(self, arrivals, completions):
        """
        Update kitchen queue state.
        
        Parameters:
        -----------
        arrivals : int
            Number of new orders
        completions : int
            Number of completed orders
        
        Returns:
        --------
        int
            Updated queue length
        """
        # Q(t) = Q(t-1) + arrivals - completed
        self.queue_length = max(0, self.queue_length + arrivals - completions)
        return self.queue_length
    
    def compute_kitchen_load(self):
        """
        Compute kitchen load based on queue and riders.
        
        Returns:
        --------
        float
            Kitchen load L(t) = alpha*Q(t) + beta*R(t)
        """
        load = self.alpha * self.queue_length + self.beta * self.riders_waiting
        return load
    
    def compute_service_rate(self, load=None):
        """
        Compute service rate based on kitchen load.
        
        Parameters:
        -----------
        load : float, optional
            Kitchen load (computed if not provided)
        
        Returns:
        --------
        float
            Service rate mu(t) = mu0 / (1 + gamma * L(t))
        """
        if load is None:
            load = self.compute_kitchen_load()
        
        service_rate = self.mu0 / (1 + self.gamma * load)
        return service_rate
    
    def compute_true_prep_time(self, load=None):
        """
        Compute true preparation time.
        
        Parameters:
        -----------
        load : float, optional
            Kitchen load
        
        Returns:
        --------
        float
            True KPT = 1 / mu(t)
        """
        mu = self.compute_service_rate(load)
        kpt_true = 1 / mu if mu > 0 else 100  # Avoid division by zero
        return kpt_true
    
    def process_order(self, order_time):
        """
        Process a single order through the system.
        
        Parameters:
        -----------
        order_time : datetime
            Order placement time
        
        Returns:
        --------
        dict
            Order processing details
        """
        # Update state
        arrivals = self.simulate_arrival()
        self.update_queue(arrivals, 0)
        
        # Compute metrics
        load = self.compute_kitchen_load()
        kpt_true = self.compute_true_prep_time(load)
        
        # Packed time
        packed_time = order_time + timedelta(minutes=kpt_true)
        
        # Store order
        order_data = {
            'order_time': order_time,
            'queue_length': self.queue_length,
            'kitchen_load': load,
            'kpt_true': kpt_true,
            'packed_time': packed_time
        }
        
        self.order_history.append(order_data)
        
        # Simulate completion after prep time
        self.update_queue(0, 1)
        
        return order_data
