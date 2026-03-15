"""
Kitchen Simulator - Queueing Theory Based Kitchen Operations

Models kitchen as service queue with dynamic service rates.
"""

import numpy as np
from datetime import datetime, timedelta
from collections import deque


class KitchenSimulator:
    """Simulate kitchen operations using queueing theory."""
    
    def __init__(self, mu0=0.1, alpha=0.5, beta=0.3, gamma=0.2):
        """
        Initialize kitchen simulator.
        
        Parameters:
        -----------
        mu0 : float
            Base service rate (orders per minute)
        alpha : float
            Queue weight factor
        beta : float
            Rider weight factor
        gamma : float
            Load impact factor
        """
        self.mu0 = mu0
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        
        # State variables
        self.queue = deque()
        self.riders_waiting = 0
        self.completed_orders = []
        self.current_time = None
    
    def update_queue(self, arrivals, completions):
        """
        Update kitchen queue.
        
        Q(t) = Q(t-1) + arrivals - completed
        
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
        for _ in range(arrivals):
            self.queue.append(self.current_time)
        
        for _ in range(min(completions, len(self.queue))):
            if self.queue:
                completed_time = self.queue.popleft()
                self.completed_orders.append({
                    'start_time': completed_time,
                    'completion_time': self.current_time
                })
        
        return len(self.queue)
    
    def compute_kitchen_load(self):
        """
        Compute kitchen load.
        
        L(t) = alpha*Q(t) + beta*R(t)
        
        Returns:
        --------
        float
            Kitchen load
        """
        queue_length = len(self.queue)
        load = self.alpha * queue_length + self.beta * self.riders_waiting
        return load
    
    def compute_service_rate(self, load=None):
        """
        Compute service rate based on load.
        
        mu(t) = mu0 / (1 + gamma * L(t))
        
        Parameters:
        -----------
        load : float, optional
            Kitchen load (computed if not provided)
        
        Returns:
        --------
        float
            Service rate
        """
        if load is None:
            load = self.compute_kitchen_load()
        
        service_rate = self.mu0 / (1 + self.gamma * load)
        return max(0.01, service_rate)  # Prevent division by zero
    
    def compute_true_prep_time(self, load=None):
        """
        Compute true preparation time.
        
        KPT_true = 1 / mu(t)
        
        Parameters:
        -----------
        load : float, optional
            Kitchen load
        
        Returns:
        --------
        float
            True preparation time in minutes
        """
        mu = self.compute_service_rate(load)
        kpt_true = 1 / mu
        return kpt_true
    
    def process_order(self, order_time, kitchen_load=None):
        """
        Process a single order.
        
        Parameters:
        -----------
        order_time : datetime
            Order placement time
        kitchen_load : float, optional
            Current kitchen load
        
        Returns:
        --------
        dict
            Order processing details
        """
        self.current_time = order_time
        
        # Add to queue
        self.queue.append(order_time)
        
        # Compute metrics
        if kitchen_load is None:
            kitchen_load = self.compute_kitchen_load()
        
        kpt_true = self.compute_true_prep_time(kitchen_load)
        packed_time = order_time + timedelta(minutes=kpt_true)
        
        return {
            'order_time': order_time,
            'queue_length': len(self.queue),
            'kitchen_load': kitchen_load,
            'service_rate': self.compute_service_rate(kitchen_load),
            'kpt_true': kpt_true,
            'packed_time': packed_time
        }
    
    def simulate_completions(self, current_time, time_delta_minutes):
        """
        Simulate order completions based on service rate.
        
        Parameters:
        -----------
        current_time : datetime
            Current time
        time_delta_minutes : float
            Time step in minutes
        
        Returns:
        --------
        int
            Number of completions
        """
        self.current_time = current_time
        
        if not self.queue:
            return 0
        
        load = self.compute_kitchen_load()
        mu = self.compute_service_rate(load)
        
        # Expected completions = mu * time_delta
        expected_completions = mu * time_delta_minutes
        
        # Use Poisson process for completions
        completions = np.random.poisson(expected_completions)
        completions = min(completions, len(self.queue))
        
        self.update_queue(0, completions)
        
        return completions
    
    def get_state(self):
        """
        Get current kitchen state.
        
        Returns:
        --------
        dict
            Current state
        """
        return {
            'queue_length': len(self.queue),
            'riders_waiting': self.riders_waiting,
            'kitchen_load': self.compute_kitchen_load(),
            'service_rate': self.compute_service_rate(),
            'completed_count': len(self.completed_orders)
        }
