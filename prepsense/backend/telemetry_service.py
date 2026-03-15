"""
Telemetry observation generator for weighted signal filtering.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

import numpy as np

from signal_filter import DEFAULT_RELIABILITY_SCORES


class TelemetryService:
    """
    Creates noisy telemetry observations with reliability metadata.
    """

    def __init__(self, random_seed: int = 42):
        self.rng = np.random.default_rng(random_seed)

    def build_observation(
        self,
        order_id: str,
        signal_type: str,
        true_packed_time: float,
        queue_length: float,
        base_value: Optional[float] = None,
        timestamp: Optional[str] = None,
    ) -> Dict[str, float]:
        reliability = DEFAULT_RELIABILITY_SCORES.get(signal_type, 0.5)
        noise_std = {
            "pickup_time": 0.9,
            "rider_arrival_time": 1.8,
            "merchant_ready_time": 2.8,
            "kitchen_queue_snapshot": 2.2,
        }.get(signal_type, 2.0)
        noise_std *= 1.0 + max(queue_length, 0.0) * 0.06

        center_value = true_packed_time if base_value is None else base_value
        observed_signal = max(
            0.5,
            float(center_value + self.rng.normal(0.0, noise_std)),
        )

        return {
            "order_id": order_id,
            "signal_type": signal_type,
            "observed_signal": observed_signal,
            "reliability_score": reliability,
            "queue_length": float(queue_length),
            "timestamp": timestamp or datetime.now().isoformat(),
        }
