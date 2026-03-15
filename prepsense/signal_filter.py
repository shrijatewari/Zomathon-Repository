"""
Signal Filter - Weighted Event Filtering

Filters noisy observations using weighted averaging.
"""

import numpy as np
from collections import deque


class SignalFilter:
    """Weighted event filter for noise reduction."""
    
    def __init__(self):
        """Initialize signal filter."""
        self.events = deque()
        self.max_events = 100  # Keep last N events
    
    def add_event(self, observation, variance):
        """
        Add an event observation.
        
        Zi = T_p + epsilon_i
        
        Parameters:
        -----------
        observation : float
            Noisy observation
        variance : float
            Variance of the observation
        """
        event = {
            'observation': observation,
            'variance': variance,
            'weight': 1.0 / variance if variance > 0 else 0
        }
        
        self.events.append(event)
        
        # Keep only recent events
        if len(self.events) > self.max_events:
            self.events.popleft()
    
    def compute_filtered_estimate(self):
        """
        Compute filtered estimate using weighted average.
        
        T_p_filtered = sum(wi * Zi) / sum(wi)
        
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
    
    def compare_variances(self):
        """
        Compare filtered vs unfiltered variance.
        
        Returns:
        --------
        dict
            Variance comparison
        """
        if not self.events:
            return None
        
        unfiltered_var = np.var([e['observation'] for e in self.events])
        filtered_var = self.compute_variance()
        
        reduction = ((unfiltered_var - filtered_var) / unfiltered_var) * 100 if unfiltered_var > 0 else 0
        
        return {
            'unfiltered_variance': unfiltered_var,
            'filtered_variance': filtered_var,
            'variance_reduction_percent': reduction
        }
    
    def reset(self):
        """Reset filter state."""
        self.events.clear()
    
    def get_statistics(self):
        """
        Get filter statistics.
        
        Returns:
        --------
        dict
            Filter statistics
        """
        if not self.events:
            return None
        
        observations = [e['observation'] for e in self.events]
        filtered = self.compute_filtered_estimate()
        filtered_var = self.compute_variance()
        
        return {
            'num_events': len(self.events),
            'mean_unfiltered': np.mean(observations),
            'variance_unfiltered': np.var(observations),
            'mean_filtered': filtered,
            'variance_filtered': filtered_var,
            'std_unfiltered': np.std(observations),
            'std_filtered': np.sqrt(filtered_var) if filtered_var else None
        }
