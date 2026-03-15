"""
Incremental packed-time reconstruction using weighted event filtering.
"""

from __future__ import annotations

from typing import Dict

from signal_filter import WeightedEventFilter


class ReconstructionService:
    """
    Maintains per-order weighted filtered packed-time estimates.
    """

    def __init__(self):
        self.filters: Dict[str, WeightedEventFilter] = {}

    def update_estimate(
        self,
        order_id: str,
        signal_type: str,
        observed_signal: float,
        reliability_score: float,
        queue_length: float,
        timestamp: str,
        true_packed_time: float | None = None,
    ) -> Dict[str, float]:
        if order_id not in self.filters:
            self.filters[order_id] = WeightedEventFilter(order_id=order_id)

        stats = self.filters[order_id].update(
            signal_type=signal_type,
            observed_signal=observed_signal,
            reliability_score=reliability_score,
            queue_length=queue_length,
            timestamp=timestamp,
        )

        prediction_accuracy = 0.0
        if true_packed_time is not None and true_packed_time > 0:
            error = abs(stats["filtered_signal"] - true_packed_time)
            prediction_accuracy = max(0.0, 100.0 - (error / true_packed_time) * 100.0)

        return {
            "order_id": order_id,
            "signal_type": signal_type,
            "observed_signal": stats["observed_signal"],
            "filtered_signal": stats["filtered_signal"],
            "variance_raw": stats["variance_raw"],
            "variance_filtered": stats["variance_filtered"],
            "noise_reduction_pct": stats["noise_reduction_pct"],
            "prediction_accuracy": prediction_accuracy,
            "reliability_score": stats["reliability_score"],
            "observation_count": stats["observation_count"],
            "timestamp": timestamp,
        }

    def clear_order(self, order_id: str) -> None:
        self.filters.pop(order_id, None)
