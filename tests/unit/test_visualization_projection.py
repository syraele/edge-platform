from copy import deepcopy
from datetime import UTC, datetime
from types import SimpleNamespace

from edge.application.research.report import PipelineReport
from edge.application.research.session import ResearchSession, SessionStatus
from edge.visualization import VisualizationProjectionBuilder


def test_projection_builder_creates_traceable_core_sections() -> None:
    session = ResearchSession(session_id="session-001")
    session.status = SessionStatus.COMPLETED
    session.started_at = datetime(2025, 1, 1, tzinfo=UTC)
    session.completed_at = datetime(2025, 1, 1, 1, tzinfo=UTC)
    session.dataset = SimpleNamespace(
        metadata=SimpleNamespace(symbol="EURUSD", timeframe="H1")
    )
    session.dataset_provenance = SimpleNamespace(provider_id="archive")
    session.market_description = object()
    session.hypotheses.append(object())
    session.experiments.append(object())
    session.evidences.append(object())
    session.knowledge = object()
    session.edges.append(object())
    report = PipelineReport.from_session(session)

    projection = VisualizationProjectionBuilder().build(session, report)

    assert projection.session_id == "session-001"
    assert projection.section_ids == ("session", "dataset", "research", "extensions")
    assert projection.section("session").availability == "available"
    assert projection.section("session").data["status"] == "completed"
    assert projection.section("dataset").data == {
        "symbol": "EURUSD",
        "timeframe": "H1",
        "provider_id": "archive",
    }
    assert projection.section("research").data == {
        "market_description_available": True,
        "hypothesis_count": 1,
        "experiment_count": 1,
        "evidence_count": 1,
        "knowledge_available": True,
        "edge_count": 1,
    }
    assert projection.section("extensions").availability == "unavailable"
    assert {reference.reference_type for reference in projection.traceability} == {
        "research_session",
        "pipeline_report",
    }
    assert projection.fingerprint == VisualizationProjectionBuilder().build(
        session, report
    ).fingerprint


def test_projection_builder_makes_absent_artifacts_explicit() -> None:
    session = ResearchSession(session_id="session-empty")

    projection = VisualizationProjectionBuilder().build(session)

    assert projection.section("dataset").availability == "unavailable"
    assert projection.section("dataset").data == {}
    assert projection.section("research").availability == "available"
    assert projection.section("research").data["knowledge_available"] is False
    assert projection.section("extensions").data == {
        "portfolio_available": False,
        "optimization_available": False,
        "machine_learning_available": False,
    }


def test_projection_builder_does_not_mutate_source_session_or_report() -> None:
    session = ResearchSession(session_id="session-immutable")
    session.evidences.append("evidence")
    report = PipelineReport.from_session(session)
    original_session = deepcopy(session)
    original_report = deepcopy(report)

    VisualizationProjectionBuilder().build(session, report)

    assert session == original_session
    assert report == original_report
