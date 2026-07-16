from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class VisualizationDataReference:
    """Traceability reference used by visualization outputs."""

    reference_type: str
    reference_id: str
    fingerprint: str | None = None


@dataclass(frozen=True, slots=True)
class VisualizationResult:
    """Deterministic result produced by a visualization capability."""

    capability_id: str
    capability_fingerprint: str
    rendered_sections: tuple[str, ...]
    snapshot: dict[str, Any]
    traceability: tuple[VisualizationDataReference, ...]
    assumptions: tuple[str, ...]
    message: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.message is None


@dataclass(frozen=True, slots=True)
class VisualizationReport:
    """Application-level report for research visualization generation."""

    capability_id: str
    capability_fingerprint: str
    status: str
    result: VisualizationResult
    rendered_sections: tuple[str, ...]
    traceability_count: int
    assumption_count: int
    failure_message: str | None
    run_fingerprint: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
