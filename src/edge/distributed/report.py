from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from edge.application.research.report import PipelineReport


@dataclass(frozen=True, slots=True)
class DistributedResearchUnitResult:
    """Contained result for one executed distributed workload unit."""

    unit_id: str
    session_id: str
    status: str
    execution_context: str | None
    pipeline_report: PipelineReport | None
    failure_message: str | None = None


@dataclass(frozen=True, slots=True)
class DistributedResearchReport:
    """Aggregated report for a distributed research workload."""

    workload_id: str
    workload_fingerprint: str
    status: str
    unit_results: tuple[DistributedResearchUnitResult, ...]
    completed_units: int
    failed_units: int
    completed_session_ids: tuple[str, ...]
    failed_session_ids: tuple[str, ...]
    assumption_count: int
    run_fingerprint: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))