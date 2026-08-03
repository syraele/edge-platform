"""
EDGE_ENGINE

Baseline Comparison
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class BaselineComparisonConfig:
    """Configuration for comparing hypothesis metrics to dataset baseline metrics."""

    min_effect_size: float = 0.1
    min_occurrences: int = 3


@dataclass(frozen=True, slots=True)
class BaselineComparisonResult:
    """Outcome of the baseline comparison for a single hypothesis."""

    is_significant: bool
    reason: str
    effect_size: float = 0.0


class BaselineComparisonService:
    """Reject hypotheses whose metrics are not meaningfully different from baseline."""

    def __init__(self, config: BaselineComparisonConfig | None = None) -> None:
        self._config = config or BaselineComparisonConfig()

    def compare(self, metadata: Mapping[str, object]) -> BaselineComparisonResult:
        occurrences = self._read_metric(metadata, "hypothesis_occurrences")
        if occurrences is None:
            return BaselineComparisonResult(is_significant=False, reason="missing_metrics")

        if occurrences < self._config.min_occurrences:
            return BaselineComparisonResult(is_significant=False, reason="min_occurrences")

        comparisons = (
            ("hypothesis_average_return", "average_return"),
            ("hypothesis_average_return_10", "average_return_10"),
            ("hypothesis_average_return_5", "average_return_5"),
            ("hypothesis_average_return_1", "average_return_1"),
        )

        max_effect_size = 0.0
        saw_baseline_metrics = False
        for hypothesis_metric_key, baseline_metric_key in comparisons:
            hypothesis_value = self._read_metric(metadata, hypothesis_metric_key)
            baseline_value = self._read_metric(metadata, baseline_metric_key)
            if hypothesis_value is None or baseline_value is None:
                continue

            saw_baseline_metrics = True
            if abs(baseline_value) <= 1e-9:
                if abs(hypothesis_value) <= 1e-9:
                    continue
                effect_size = float("inf")
            else:
                effect_size = abs(hypothesis_value - baseline_value) / abs(baseline_value)

            max_effect_size = max(max_effect_size, effect_size)
            if effect_size >= self._config.min_effect_size:
                return BaselineComparisonResult(
                    is_significant=True,
                    reason="baseline_significant",
                    effect_size=effect_size,
                )

        if not saw_baseline_metrics:
            return BaselineComparisonResult(
                is_significant=True,
                reason="baseline_not_applicable",
                effect_size=0.0,
            )

        return BaselineComparisonResult(
            is_significant=False,
            reason="baseline_not_significant",
            effect_size=max_effect_size,
        )

    @staticmethod
    def _read_metric(metadata: Mapping[str, object], key: str) -> float | None:
        value = metadata.get(key)
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
