"""
PrepSense Reconstruction Module

Reconstructs packed time and KPT from telemetry signals.
"""

import numpy as np
from datetime import datetime, timedelta


class PrepSenseReconstructor:
    """Reconstruct preparation time using telemetry signals."""
    
    def __init__(self, handover_mean=2.0):
        """
        Initialize reconstructor.
        
        Parameters:
        -----------
        handover_mean : float
            Mean handover delay for reconstruction
        """
        self.handover_mean = handover_mean
    
    def reconstruct_packed_time(self, pickup_time):
        """
        Estimate packed time from pickup time.
        
        T_hat = T_pickup - mean_handover
        
        Parameters:
        -----------
        pickup_time : datetime
            Pickup time
        
        Returns:
        --------
        datetime
            Reconstructed packed time
        """
        reconstructed = pickup_time - timedelta(minutes=self.handover_mean)
        return reconstructed
    
    def reconstruct_kpt(self, order_time, pickup_time):
        """
        Compute reconstructed KPT.
        
        KPT_reconstructed = T_hat - T_order
        
        Parameters:
        -----------
        order_time : datetime
            Order placement time
        pickup_time : datetime
            Pickup time
        
        Returns:
        --------
        float
            Reconstructed preparation time in minutes
        """
        packed_time_hat = self.reconstruct_packed_time(pickup_time)
        kpt_reconstructed = (packed_time_hat - order_time).total_seconds() / 60
        return max(0, kpt_reconstructed)
    
    def add_noise_to_observed(self, true_prep_time, noise_std=3.0):
        """
        Generate noisy observed signal.
        
        T_obs = T_p + noise, noise ~ Normal(0, sigma)
        
        Parameters:
        -----------
        true_prep_time : float
            True preparation time
        noise_std : float
            Standard deviation of noise
        
        Returns:
        --------
        float
            Observed preparation time
        """
        noise = np.random.normal(0, noise_std)
        observed = true_prep_time + noise
        return max(0.5, observed)
