from __future__ import annotations

from datetime import UTC, datetime

import pytest

from edge.application.research.report import PipelineReport
from edge.application.research.session import ResearchSession, SessionStatus
from edge.distributed import (
    DistributedResearchError,
    DistributedResearchService,
    DistributedResearchUnit,
    DistributedResearchWorkload,
)


def _build_report(session_id: str, *, message: str | None = None) -> PipelineReport:
    session = ResearchSession(session_id=session_id)
    session.status = SessionStatus.COMPLETED if message is None else SessionStatus.FAILED
    session.started_at = datetime(2024, 1, 1, tzinfo=UTC)
    session.completed_at = datetime(2024, 1, 1, 1, tzinfo=UTC)
    session.message = message
    return PipelineReport.from_session(session)


class StubDistributedExecutor:
    def __init__(self, reports: dict[str, PipelineReport], failures: set[str] | None = None) -> None:
        self._reports = reports
        self._failures = failures or set()
        self.calls: list[str] = []

    def execute(self, unit: DistributedResearchUnit) -> PipelineReport:
        self.calls.append(unit.unit_id)
        if unit.unit_id in self._failures:
            raise RuntimeError(f"executor failed for {unit.unit_id}")
        return self._reports[unit.unit_id]


def test_distributed_service_aggregates_ordered_unit_reports() -> None:
    workload = DistributedResearchWorkload(
        workload_id="workload-alpha",
        units=(
            DistributedResearchUnit(
                unit_id="unit-a",
                session=ResearchSession(session_id="session-a"),
                dataset_request={"symbol": "EURUSD", "timeframe": "H1"},
                execution_context="node-a",
            ),
            DistributedResearchUnit(
                unit_id="unit-b",
                session=ResearchSession(session_id="session-b"),
                execution_context="node-b",
            ),
        ),
        assumptions=("Unit order remains stable.",),
    )
    reports = {
        "unit-a": _build_report("session-a"),
        "unit-b": _build_report("session-b"),
    }
    service = DistributedResearchService(StubDistributedExecutor(reports))

    report = service.execute(workload)

    assert report.status == "completed"
    assert tuple(result.unit_id for result in report.unit_results) == ("unit-a", "unit-b")
    assert tuple(result.session_id for result in report.unit_results) == (
        "session-a",
        "session-b",
    )
    assert report.completed_units == 2
    assert report.failed_units == 0
    assert report.completed_session_ids == ("session-a", "session-b")
    assert report.failed_session_ids == ()
    assert report.assumption_count == 1
    assert report.workload_fingerprint == DistributedResearchWorkload(
        workload_id="workload-alpha",
        units=(
            DistributedResearchUnit(
                unit_id="unit-a",
                session=ResearchSession(session_id="session-a"),
                dataset_request={"symbol": "EURUSD", "timeframe": "H1"},
                execution_context="node-a",
            ),
            DistributedResearchUnit(
                unit_id="unit-b",
                session=ResearchSession(session_id="session-b"),
                execution_context="node-b",
            ),
        ),
        assumptions=("Unit order remains stable.",),
    ).fingerprint
    assert report.run_fingerprint == DistributedResearchService(
        StubDistributedExecutor(reports)
    ).execute(workload).run_fingerprint


def test_distributed_service_rejects_duplicate_unit_identity() -> None:
    workload = DistributedResearchWorkload(
        workload_id="workload-duplicate",
        units=(
            DistributedResearchUnit(
                unit_id="unit-a",
                session=ResearchSession(session_id="session-a"),
            ),
            DistributedResearchUnit(
                unit_id="unit-a",
                session=ResearchSession(session_id="session-b"),
            ),
        ),
    )

    with pytest.raises(DistributedResearchError):
        DistributedResearchService(StubDistributedExecutor({})).execute(workload)


def test_distributed_service_contains_unit_failures_and_marks_partial() -> None:
    workload = DistributedResearchWorkload(
        workload_id="workload-partial",
        units=(
            DistributedResearchUnit(
                unit_id="unit-a",
                session=ResearchSession(session_id="session-a"),
            ),
            DistributedResearchUnit(
                unit_id="unit-b",
                session=ResearchSession(session_id="session-b"),
            ),
        ),
    )
    executor = StubDistributedExecutor(
        {"unit-b": _build_report("session-b")},
        failures={"unit-a"},
    )

    report = DistributedResearchService(executor).execute(workload)

    assert report.status == "partial"
    assert executor.calls == ["unit-a", "unit-b"]
    assert report.completed_units == 1
    assert report.failed_units == 1
    assert report.completed_session_ids == ("session-b",)
    assert report.failed_session_ids == ("session-a",)
    assert report.unit_results[0].failure_message == "executor failed for unit-a"
    assert report.unit_results[1].pipeline_report is not None


def test_distributed_service_marks_failed_when_no_unit_succeeds() -> None:
    workload = DistributedResearchWorkload(
        workload_id="workload-failed",
        units=(
            DistributedResearchUnit(
                unit_id="unit-a",
                session=ResearchSession(session_id="session-a"),
            ),
        ),
    )

    report = DistributedResearchService(
        StubDistributedExecutor({}, failures={"unit-a"})
    ).execute(workload)

    assert report.status == "failed"
    assert report.completed_units == 0
    assert report.failed_units == 1
    assert report.failed_session_ids == ("session-a",)