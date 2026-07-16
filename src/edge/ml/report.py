from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from edge.domain.evidence import Evidence


@dataclass(frozen=True, slots=True)
class MachineLearningResult:
    """Traceable result of an ML-assisted analysis."""

    capability_id: str
    capability_fingerprint: str
    output_name: str
    output_value: float | None
    input_measurements: dict[str, float]
    evidence: Evidence
    assumptions: tuple[str, ...]
    message: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.message is None and self.output_value is not None


@dataclass(frozen=True, slots=True)
class MachineLearningReport:
    """Deterministic report for an ML-assisted research analysis."""

    capability_id: str
    capability_fingerprint: str
    status: str
    result: MachineLearningResult
    input_metric_names: tuple[str, ...]
    assumption_count: int
    output_name: str
    output_value: float | None
    failure_message: str | None
    run_fingerprint: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
