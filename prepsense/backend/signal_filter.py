"""
Weighted Event Filtering for noisy telemetry observations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np


DEFAULT_RELIABILITY_SCORES: Dict[str, float] = {
    "pickup_time": 0.92,
    "rider_arrival_time": 0.65,
    "merchant_ready_time": 0.38,
    "kitchen_queue_snapshot": 0.52,
}


def estimate_noise_variance(
    observation_type: str,
    reliability_score: Optional[float] = None,
    queue_length: float = 0.0,
) -> float:
    """
    Estimate measurement noise variance for a telemetry observation.

    Lower reliability implies larger noise variance.
    """
    reliability = (
        reliability_score
        if reliability_score is not None
        else DEFAULT_RELIABILITY_SCORES.get(observation_type, 0.5)
    )
    reliability = float(np.clip(reliability, 0.05, 0.99))

    base_variance = {
        "pickup_time": 0.75,
        "rider_arrival_time": 2.0,
        "merchant_ready_time": 3.6,
        "kitchen_queue_snapshot": 2.4,
    }.get(observation_type, 2.5)

    congestion_multiplier = 1.0 + max(queue_length, 0.0) * 0.08
    return float(base_variance * congestion_multiplier / reliability)


def calculate_event_weights(variances: List[float]) -> np.ndarray:
    """
    Calculate reliability weights wi = 1 / sigma_i^2.
    """
    safe_variances = np.clip(np.asarray(variances, dtype=float), 1e-6, None)
    return 1.0 / safe_variances


def compute_weighted_estimate(observations: List[float], weights: List[float]) -> float:
    """
    Compute T_p_filtered = sum(wi * Zi) / sum(wi).
    """
    obs = np.asarray(observations, dtype=float)
    w = np.asarray(weights, dtype=float)
    if obs.size == 0:
        return 0.0
    denominator = float(w.sum())
    if denominator <= 0:
        return float(obs.mean())
    return float(np.dot(obs, w) / denominator)


@dataclass
class FilterObservation:
    signal_type: str
    observed_signal: float
    reliability_score: float
    variance: float
    timestamp: str


@dataclass
class WeightedEventFilter:
    """
    Incremental per-order weighted event filter.
    """
    order_id: str
    observations: List[FilterObservation] = field(default_factory=list)
    weighted_sum: float = 0.0
    total_weight: float = 0.0

    def update(
        self,
        signal_type: str,
        observed_signal: float,
        reliability_score: Optional[float] = None,
        queue_length: float = 0.0,
        timestamp: str = "",
    ) -> Dict[str, float]:
        variance = estimate_noise_variance(signal_type, reliability_score, queue_length)
        weight = float(calculate_event_weights([variance])[0])
        reliability = (
            reliability_score
            if reliability_score is not None
            else DEFAULT_RELIABILITY_SCORES.get(signal_type, 0.5)
        )

        self.observations.append(
            FilterObservation(
                signal_type=signal_type,
                observed_signal=float(observed_signal),
                reliability_score=float(reliability),
                variance=variance,
                timestamp=timestamp,
            )
        )

        self.weighted_sum += weight * float(observed_signal)
        self.total_weight += weight

        filtered_signal = self.incremental_estimate
        variance_raw = self.raw_variance
        variance_filtered = self.filtered_variance
        noise_reduction_pct = 0.0
        if variance_raw > 0:
            noise_reduction_pct = max(
                0.0, (variance_raw - variance_filtered) / variance_raw * 100.0
            )

        return {
            "observed_signal": float(observed_signal),
            "filtered_signal": filtered_signal,
            "variance_raw": variance_raw,
            "variance_filtered": variance_filtered,
            "noise_reduction_pct": noise_reduction_pct,
            "weight": weight,
            "reliability_score": float(reliability),
            "observation_count": len(self.observations),
        }

    @property
    def incremental_estimate(self) -> float:
        if self.total_weight <= 0:
            if not self.observations:
                return 0.0
            return float(
                np.mean([ob.observed_signal for ob in self.observations])
            )
        return float(self.weighted_sum / self.total_weight)

    @property
    def raw_variance(self) -> float:
        if len(self.observations) < 2:
            return 0.0
        return float(np.var([ob.observed_signal for ob in self.observations]))

    @property
    def filtered_variance(self) -> float:
        if self.total_weight <= 0:
            return self.raw_variance
        return float(1.0 / self.total_weight)

    def snapshot(self) -> Dict[str, float]:
        return {
            "filtered_signal": self.incremental_estimate,
            "variance_raw": self.raw_variance,
            "variance_filtered": self.filtered_variance,
            "observation_count": len(self.observations),
        }
