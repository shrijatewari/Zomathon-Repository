"""
Dispatch Decision Engine - Converts KPT predictions into optimal rider assignments.

Implements cost-based optimization with uncertainty handling.
"""

import numpy as np
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class DispatchDecision:
    """Represents a dispatch decision."""
    order_id: str
    predicted_kpt: float  # mu_T
    confidence: float  # sigma_T
    travel_time: float  # T_travel
    dispatch_time: float  # T_assign*
    idle_risk: float  # Probability of idle time > 0
    delay_risk: float  # Probability of delay > 0
    timestamp: datetime


class DispatchEngine:
    """
    Dispatch Decision Engine that optimizes rider assignment based on KPT predictions.
    
    Uses predictive uncertainty to minimize expected cost:
    Cost = C1 * Idle + C2 * Delay
    """
    
    def __init__(self, cost_idle: float = 1.0, cost_delay: float = 2.0):
        """
        Initialize dispatch engine.
        
        Parameters:
        -----------
        cost_idle : float
            Cost per unit of rider idle time (C1)
        cost_delay : float
            Cost per unit of delivery delay (C2)
        """
        self.cost_idle = cost_idle
        self.cost_delay = cost_delay
        
        # Optimal k parameter based on cost ratio
        self.k = (cost_idle - cost_delay) / (cost_idle + cost_delay)
    
    def compute_optimal_dispatch_time(
        self,
        predicted_kpt: float,
        confidence: float,
        travel_time: float,
        z_score: float = 1.96
    ) -> float:
        """
        Compute optimal assignment time using predictive uncertainty.
        
        Formula: T_assign* = mu_T + k*sigma_T - T_travel
        
        Parameters:
        -----------
        predicted_kpt : float
            Predicted preparation time (mu_T)
        confidence : float
            Prediction uncertainty (sigma_T)
        travel_time : float
            Rider travel time to restaurant
        z_score : float
            Z-score for confidence interval (default 1.96 for 95%)
        
        Returns:
        --------
        float
            Optimal dispatch time
        """
        # Optimal assignment time accounting for uncertainty
        optimal_assignment = predicted_kpt + self.k * confidence
        
        # Dispatch time = assignment time - travel time
        dispatch_time = optimal_assignment - travel_time
        
        # Ensure non-negative
        return max(0.0, dispatch_time)
    
    def compute_idle_risk(
        self,
        predicted_kpt: float,
        confidence: float,
        dispatch_time: float,
        travel_time: float
    ) -> float:
        """
        Compute probability of rider idle time > 0.
        
        Idle occurs when: Tp_true > T_assign
        Where T_assign = dispatch_time + travel_time
        
        Parameters:
        -----------
        predicted_kpt : float
            Predicted preparation time
        confidence : float
            Prediction uncertainty
        dispatch_time : float
            Time to dispatch rider
        travel_time : float
            Rider travel time
        
        Returns:
        --------
        float
            Probability of idle time (0-1)
        """
        assignment_time = dispatch_time + travel_time
        
        # Probability that actual KPT > assignment time
        # Using normal distribution approximation
        z = (assignment_time - predicted_kpt) / (confidence + 1e-6)
        
        # P(T > assignment_time) = 1 - Phi(z)
        idle_prob = 1 - self._normal_cdf(z)
        
        return max(0.0, min(1.0, idle_prob))
    
    def compute_delay_risk(
        self,
        predicted_kpt: float,
        confidence: float,
        dispatch_time: float,
        travel_time: float
    ) -> float:
        """
        Compute probability of delivery delay > 0.
        
        Delay occurs when: T_assign > Tp_true
        Where T_assign = dispatch_time + travel_time
        
        Parameters:
        -----------
        predicted_kpt : float
            Predicted preparation time
        confidence : float
            Prediction uncertainty
        dispatch_time : float
            Time to dispatch rider
        travel_time : float
            Rider travel time
        
        Returns:
        --------
        float
            Probability of delay (0-1)
        """
        assignment_time = dispatch_time + travel_time
        
        # Probability that actual KPT < assignment time
        z = (assignment_time - predicted_kpt) / (confidence + 1e-6)
        
        # P(T < assignment_time) = Phi(z)
        delay_prob = self._normal_cdf(z)
        
        return max(0.0, min(1.0, delay_prob))
    
    def make_dispatch_decision(
        self,
        order_id: str,
        predicted_kpt: float,
        confidence: float,
        travel_time: float
    ) -> DispatchDecision:
        """
        Make optimal dispatch decision for an order.
        
        Parameters:
        -----------
        order_id : str
            Unique order identifier
        predicted_kpt : float
            Predicted kitchen preparation time
        confidence : float
            Prediction uncertainty (standard deviation)
        travel_time : float
            Estimated rider travel time to restaurant
        
        Returns:
        --------
        DispatchDecision
            Complete dispatch decision with risks
        """
        # Compute optimal dispatch time
        dispatch_time = self.compute_optimal_dispatch_time(
            predicted_kpt, confidence, travel_time
        )
        
        # Compute risk metrics
        idle_risk = self.compute_idle_risk(
            predicted_kpt, confidence, dispatch_time, travel_time
        )
        
        delay_risk = self.compute_delay_risk(
            predicted_kpt, confidence, dispatch_time, travel_time
        )
        
        return DispatchDecision(
            order_id=order_id,
            predicted_kpt=predicted_kpt,
            confidence=confidence,
            travel_time=travel_time,
            dispatch_time=dispatch_time,
            idle_risk=idle_risk,
            delay_risk=delay_risk,
            timestamp=datetime.now()
        )
    
    def _normal_cdf(self, z: float) -> float:
        """
        Cumulative distribution function for standard normal distribution.
        
        Uses approximation: Phi(z) ≈ 0.5 * (1 + erf(z/sqrt(2)))
        """
        return 0.5 * (1 + np.sign(z) * (1 - np.exp(-2 * z**2 / np.pi)))


if __name__ == "__main__":
    # Test dispatch engine
    engine = DispatchEngine(cost_idle=1.0, cost_delay=2.0)
    
    decision = engine.make_dispatch_decision(
        order_id="ORD_001",
        predicted_kpt=11.4,
        confidence=2.0,
        travel_time=4.2
    )
    
    print(f"Order: {decision.order_id}")
    print(f"Predicted KPT: {decision.predicted_kpt:.2f} min")
    print(f"Confidence: ±{decision.confidence:.2f} min")
    print(f"Travel Time: {decision.travel_time:.2f} min")
    print(f"Dispatch Time: {decision.dispatch_time:.2f} min")
    print(f"Idle Risk: {decision.idle_risk:.2%}")
    print(f"Delay Risk: {decision.delay_risk:.2%}")
