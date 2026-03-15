"""
Weighted Event Filtering Module

Filters noisy observations using weighted averaging.
"""

import numpy as np


class EventFilter:
    """Filter events using weighted averaging based on variance."""
    
    def __init__(self):
        """Initialize event filter."""
        self.events = []
    
    def add_event(self, observation, variance):
        """
        Add an event observation.
        
        Parameters:
        -----------
        observation : float
            Noisy observation Zi = Tp + epsilon_i
        variance : float
            Variance of the observation
        """
        self.events.append({
            'observation': observation,
            'variance': variance,
            'weight': 1.0 / variance if variance > 0 else 0
        })
    
    def compute_filtered_estimate(self):
        """
        Compute filtered estimate using weighted average.
        
        Tp_est = sum(wi*Zi) / sum(wi)
        
        Returns:
        --------
        float
            Filtered estimate
        """
        if not self.events:
            return None
        
        weighted_sum = sum(e['weight'] * e['observation'] for e in self.events)
        weight_sum = sum(e['weight'] for e in self.events)
        
        if weight_sum == 0:
            return np.mean([e['observation'] for e in self.events])
        
        filtered = weighted_sum / weight_sum
        return filtered
    
    def compute_variance(self):
        """
        Compute variance of filtered estimate.
        
        Returns:
        --------
        float
            Variance estimate
        """
        if not self.events:
            return None
        
        weight_sum = sum(e['weight'] for e in self.events)
        if weight_sum == 0:
            return np.var([e['observation'] for e in self.events])
        
        variance = 1.0 / weight_sum
        return variance
    
    def reset(self):
        """Reset filter state."""
        self.events = []
