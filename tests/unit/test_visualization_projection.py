from copy import deepcopy
from datetime import UTC, datetime
from types import SimpleNamespace

from edge.application.research.report import PipelineReport
from edge.application.research.session import ResearchSession, SessionStatus
from edge.domain.evidence import Evidence
from edge.ml.report import MachineLearningReport, MachineLearningResult
from edge.optimization.report import OptimizationReport
from edge.portfolio.report import PortfolioResearchReport
from edge.visualization import (
    VisualizationCapability,
    VisualizationComposition,
    VisualizationProjectionBuilder,
)


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


def test_projection_builder_adapts_platform_evolution_reports() -> None:
    session = ResearchSession(session_id="session-platform-reports")
    pipeline_report = PipelineReport.from_session(session)
    portfolio_report = PortfolioResearchReport(
        portfolio_id="portfolio-1",
        units=(pipeline_report,),
        research_unit_ids=(session.session_id,),
        comparison_order=(session.session_id,),
        provider_ids=("archive",),
        dataset_sources=("EURUSD",),
        completed_units=1,
        failed_units=0,
        evidence_count=3,
        knowledge_count=1,
        edge_count=1,
    )
    optimization_report = OptimizationReport(
        problem_id="optimization-1",
        problem_fingerprint="problem-fingerprint",
        status="completed",
        objective_name="score",
        maximize=True,
        constraints=(),
        assumptions=("Stable data.",),
        candidates=(),
        evaluated_configurations=("baseline",),
        ranking=("baseline",),
        winner_configuration="baseline",
        best_objective_value=2.0,
        succeeded_candidates=1,
        failed_candidates=0,
        failure_messages=(),
        run_fingerprint="optimization-run",
    )
    machine_learning_report = MachineLearningReport(
        capability_id="ml-score",
        capability_fingerprint="capability-fingerprint",
        status="completed",
        result=MachineLearningResult(
            capability_id="ml-score",
            capability_fingerprint="capability-fingerprint",
            output_name="prediction",
            output_value=0.75,
            input_measurements={"score": 1.0},
            evidence=Evidence(measurements={"score": 1.0}),
            assumptions=("Score is meaningful.",),
        ),
        input_metric_names=("score",),
        assumption_count=1,
        output_name="prediction",
        output_value=0.75,
        failure_message=None,
        run_fingerprint="ml-run",
    )

    projection = VisualizationProjectionBuilder().build(
        session,
        pipeline_report,
        portfolio_report=portfolio_report,
        optimization_report=optimization_report,
        machine_learning_report=machine_learning_report,
    )

    assert projection.section_ids == (
        "session",
        "dataset",
        "research",
        "extensions",
        "portfolio",
        "optimization",
        "machine_learning",
    )
    assert projection.section("portfolio").data["portfolio_id"] == "portfolio-1"
    assert projection.section("optimization").data["run_fingerprint"] == "optimization-run"
    assert projection.section("machine_learning").data["output_value"] == 0.75
    assert {reference.reference_type for reference in projection.traceability} >= {
        "portfolio_report",
        "optimization_report",
        "machine_learning_report",
    }


def test_projection_builder_preserves_failed_report_context() -> None:
    session = ResearchSession(session_id="session-failed-reports")
    optimization_report = OptimizationReport(
        problem_id="optimization-failed",
        problem_fingerprint="problem-fingerprint",
        status="failed",
        objective_name="score",
        maximize=True,
        constraints=(),
        assumptions=("Stable data.",),
        candidates=(),
        evaluated_configurations=(),
        ranking=(),
        winner_configuration=None,
        best_objective_value=None,
        succeeded_candidates=0,
        failed_candidates=1,
        failure_messages=("No candidate succeeded.",),
        run_fingerprint="optimization-failed-run",
    )
    machine_learning_report = MachineLearningReport(
        capability_id="ml-failed",
        capability_fingerprint="capability-fingerprint",
        status="failed",
        result=MachineLearningResult(
            capability_id="ml-failed",
            capability_fingerprint="capability-fingerprint",
            output_name="prediction",
            output_value=None,
            input_measurements={"score": 1.0},
            evidence=Evidence(measurements={"score": 1.0}),
            assumptions=("Score is meaningful.",),
            message="executor unavailable",
        ),
        input_metric_names=("score",),
        assumption_count=1,
        output_name="prediction",
        output_value=None,
        failure_message="executor unavailable",
        run_fingerprint="ml-failed-run",
    )

    projection = VisualizationProjectionBuilder().build(
        session,
        optimization_report=optimization_report,
        machine_learning_report=machine_learning_report,
    )

    assert projection.section("optimization").data["failure_messages"] == [
        "No candidate succeeded."
    ]
    assert projection.section("machine_learning").data["failure_message"] == (
        "executor unavailable"
    )


def test_composition_selects_available_sections_in_capability_order() -> None:
    session = ResearchSession(session_id="session-composition")
    projection = VisualizationProjectionBuilder().build(session)
    capability = VisualizationCapability(
        capability_id="viz-research-session",
        capability_name="Research Session",
        required_sections=("research", "session"),
    )

    composition = VisualizationComposition.from_projection(capability, projection)

    assert composition.session_id == session.session_id
    assert tuple(composition.payload) == ("research", "session")
    assert composition.payload["research"] == projection.section("research").data
    assert composition.traceability == projection.traceability
    assert composition.fingerprint == VisualizationComposition.from_projection(
        capability, projection
    ).fingerprint
