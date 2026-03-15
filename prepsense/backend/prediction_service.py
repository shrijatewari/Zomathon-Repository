"""
Prediction Service - Generates KPT predictions with uncertainty estimates.
"""

import numpy as np
from typing import Dict, Tuple
from datetime import datetime
import random


class PredictionService:
    """
    Service that generates KPT predictions with confidence intervals.
    
    In production, this would use the trained ML model.
    For simulation, we generate realistic predictions.
    """
    
    def __init__(self, base_prep_time: float = 10.0, noise_level: float = 2.0):
        """
        Initialize prediction service.
        
        Parameters:
        -----------
        base_prep_time : float
            Base preparation time in minutes
        noise_level : float
            Prediction uncertainty level
        """
        self.base_prep_time = base_prep_time
        self.noise_level = noise_level
    
    def predict_kpt(
        self,
        queue_length: int = 0,
        orders_last_10min: int = 0,
        handover_delay: float = 2.0
    ) -> Tuple[float, float]:
        """
        Predict kitchen preparation time with uncertainty.
        
        Parameters:
        -----------
        queue_length : int
            Current kitchen queue length
        orders_last_10min : int
            Orders in last 10 minutes
        handover_delay : float
            Estimated handover delay
        
        Returns:
        --------
        Tuple[float, float]
            (predicted_kpt, confidence)
            predicted_kpt: Mean prediction (mu_T)
            confidence: Standard deviation (sigma_T)
        """
        # Simulate prediction based on kitchen load
        load_factor = 1 + 0.1 * queue_length + 0.05 * orders_last_10min
        predicted_kpt = self.base_prep_time * load_factor + handover_delay
        
        # Add some realistic noise
        predicted_kpt += np.random.normal(0, 0.5)
        predicted_kpt = max(5.0, predicted_kpt)  # Minimum 5 minutes
        
        # Confidence increases with queue length (more uncertainty)
        confidence = self.noise_level * (1 + 0.1 * queue_length)
        confidence = max(1.0, min(5.0, confidence))  # Clamp between 1-5 min
        
        return predicted_kpt, confidence
    
    def predict_with_confidence_interval(
        self,
        queue_length: int = 0,
        orders_last_10min: int = 0,
        handover_delay: float = 2.0,
        z_score: float = 1.96
    ) -> Dict[str, float]:
        """
        Predict KPT with full confidence interval.
        
        Returns:
        --------
        Dict[str, float]
            {
                'predicted_kpt': mu_T,
                'confidence': sigma_T,
                'lower_bound': mu_T - z*sigma_T,
                'upper_bound': mu_T + z*sigma_T
            }
        """
        mu_T, sigma_T = self.predict_kpt(queue_length, orders_last_10min, handover_delay)
        
        return {
            'predicted_kpt': mu_T,
            'confidence': sigma_T,
            'lower_bound': max(0, mu_T - z_score * sigma_T),
            'upper_bound': mu_T + z_score * sigma_T
        }


if __name__ == "__main__":
    # Test prediction service
    service = PredictionService()
    
    prediction = service.predict_with_confidence_interval(
        queue_length=3,
        orders_last_10min=5
    )
    
    print(f"Predicted KPT: {prediction['predicted_kpt']:.2f} min")
    print(f"Confidence: ±{prediction['confidence']:.2f} min")
    print(f"95% CI: [{prediction['lower_bound']:.2f}, {prediction['upper_bound']:.2f}] min")
