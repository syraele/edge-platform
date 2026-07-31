"""
EDGE_ENGINE

Research Pipeline Integration Test
"""

from datetime import UTC, datetime
from pathlib import Path

from edge.application.research.pipeline import ResearchPipeline
from edge.application.research.dataset_access_service import DatasetAccessService
from edge.application.research.report import PipelineReport
from edge.application.research.runner import ExperimentRunner
from edge.application.research.session import (
    ResearchSession,
    SessionStatus,
)
from edge.data import DatasetProviderRegistry, DatasetQuery
from edge.data.providers.filesystem_csv_provider import FilesystemCsvDatasetProvider
from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.domain.descriptor_metadata import DescriptorMetadata
from edge.domain.experiment import Experiment
from edge.domain.experiment_status import ExperimentStatus
from edge.domain.hypothesis_metadata import HypothesisMetadata
from edge.domain.market_description import MarketDescription
from edge.domain.research_configuration import ResearchConfiguration
from edge.domain.research_hypothesis import ResearchHypothesis
from edge.domain.services import (
    CandidateEdgeSelectionConfig,
    CandidateEdgeSelectionService,
    ExperimentExecutor,
    ResearchEvaluator,
)
from edge.domain.evidence import Evidence
from edge.ml import MachineLearningCapability, MachineLearningService
from edge.optimization import OptimizationProblem, OptimizationService
from edge.visualization import (
    VisualizationCapability,
    VisualizationDataReference,
    VisualizationProjectionBuilder,
    VisualizationService,
)
from tests.unit.providers.sample_dataset_providers import HistoricalArchiveProvider


def test_research_pipeline_executes_complete_session() -> None:
    """
    Validate that the ResearchPipeline orchestrates a complete
    research session from start to completion.
    """

    dataset = HistoricalDataset(
        metadata=DatasetMetadata(
            symbol="EURUSD",
            timeframe="M1",
        ),
        bars=(
            Bar(
                timestamp=datetime(2024, 1, 1),
                open=1.1000,
                high=1.1010,
                low=1.0990,
                close=1.1005,
            ),
        ),
    )

    market_description = MarketDescription(
        dataset=dataset,
        metadata=DescriptorMetadata(
            created_at=datetime.now(UTC),
            builder_version="1.0",
        ),
        descriptors=(),
    )

    hypothesis = ResearchHypothesis(
        market_description=market_description,
        metadata=HypothesisMetadata(
            created_at=datetime.now(UTC),
        ),
        statement="Pipeline integration test",
    )

    configuration = ResearchConfiguration(
        name="baseline",
    )

    experiment = Experiment(
        hypothesis=hypothesis,
        configuration=configuration,
        status=ExperimentStatus.CREATED,
    )

    session = ResearchSession()
    session.experiments.append(experiment)

    pipeline = ResearchPipeline(
        runner=ExperimentRunner(
            ExperimentExecutor(),
        ),
        evaluator=ResearchEvaluator(),
    )

    result = pipeline.execute(session)

    assert isinstance(result, PipelineReport)
    assert result.session_id == session.session_id
    assert result.status is SessionStatus.COMPLETED
    assert len(result.evidences) == 1
    assert result.knowledge is not None
    assert result.knowledge.statement == "Evidence successfully validated."
    assert result.started_at is not None
    assert result.completed_at is not None
    assert result.dataset_provenance is None
    assert result.hypotheses == tuple(session.hypotheses)
    assert result.experiments == tuple(session.experiments)
    assert result.edges == tuple(session.edges)
    assert result.message is None


def test_research_pipeline_loads_dataset_from_provider_service() -> None:
    session = ResearchSession()

    provider_registry = DatasetProviderRegistry()
    provider_registry.register(HistoricalArchiveProvider())

    pipeline = ResearchPipeline(
        runner=ExperimentRunner(
            ExperimentExecutor(),
        ),
        evaluator=ResearchEvaluator(),
        dataset_access_service=DatasetAccessService(provider_registry),
    )

    result = pipeline.execute(
        session,
        dataset_request={
            "symbol": "XAUUSD",
            "timeframe": "H1",
            "provider_id": "historical-archive",
        },
    )

    assert isinstance(result, PipelineReport)
    assert result.status is SessionStatus.COMPLETED
    assert session.dataset is not None
    assert session.dataset.metadata.symbol == "XAUUSD"
    assert session.dataset_provenance is not None
    assert session.dataset_provenance.provider_id == "historical-archive"
    assert result.dataset_provenance is not None
    assert result.dataset_provenance.provider_id == "historical-archive"


def test_research_pipeline_executes_end_to_end_discovery_from_query(tmp_path: Path) -> None:
    csv_path = tmp_path / "eurusd-m1.csv"
    csv_path.write_text(
        "timestamp,open,high,low,close,volume\n"
        "2024-01-01T00:00:00,1.1000,1.1010,1.0990,1.1005,100\n"
        "2024-01-01T01:00:00,1.2000,1.2050,1.1950,1.2012,110\n",
        encoding="utf-8",
    )

    provider_registry = DatasetProviderRegistry()
    provider_registry.register(FilesystemCsvDatasetProvider(base_path=tmp_path))

    pipeline = ResearchPipeline(
        runner=ExperimentRunner(ExperimentExecutor()),
        evaluator=ResearchEvaluator(),
        registry=provider_registry,
    )

    report = pipeline.execute_discovery(
        DatasetQuery(symbol="EURUSD", timeframe="M1", source="filesystem-csv")
    )

    assert len(report.rows) >= 8
    assert report.rows[0].hypothesis_name in {
        "close > open",
        "close < open",
        "close > previous_close",
        "close < previous_close",
        "high > previous_high",
        "low < previous_low",
    }
    assert all(row.occurrences >= 0.0 for row in report.rows)
    assert all(row.average_return_10 >= 0.0 for row in report.rows)
    assert report.knowledge is not None
    assert report.knowledge.statement == "Evidence successfully validated."


def test_research_pipeline_reports_candidate_edge_selection_counts(tmp_path: Path) -> None:
    csv_path = tmp_path / "eurusd-m1.csv"
    csv_path.write_text(
        "timestamp,open,high,low,close,volume\n"
        "2024-01-01T00:00:00,1.1000,1.1010,1.0990,1.1005,100\n"
        "2024-01-01T01:00:00,1.2000,1.2050,1.1950,1.2012,110\n",
        encoding="utf-8",
    )

    selection_service = CandidateEdgeSelectionService(
        CandidateEdgeSelectionConfig(min_occurrences=1, min_average_return_abs=0.0)
    )
    provider_registry = DatasetProviderRegistry()
    provider_registry.register(FilesystemCsvDatasetProvider(base_path=tmp_path))

    pipeline = ResearchPipeline(
        runner=ExperimentRunner(ExperimentExecutor()),
        evaluator=ResearchEvaluator(),
        selection_service=selection_service,
        registry=provider_registry,
    )

    report = pipeline.execute_discovery(
        DatasetQuery(symbol="EURUSD", timeframe="M1", source="filesystem-csv")
    )

    assert report.selection_summary is not None
    assert report.selection_summary.generated_count >= 1
    assert report.selection_summary.rejected_count >= 0
    assert report.selection_summary.selected_count >= 0


def test_research_pipeline_runs_validation_on_separate_dataset(tmp_path: Path) -> None:
    discovery_csv = tmp_path / "eurusd-m1.csv"
    discovery_csv.write_text(
        "timestamp,open,high,low,close,volume\n"
        "2024-01-01T00:00:00,1.1000,1.1010,1.0990,1.1005,100\n"
        "2024-01-01T01:00:00,1.2000,1.2050,1.1950,1.2012,110\n",
        encoding="utf-8",
    )
    validation_csv = tmp_path / "eurusd-m1-validation.csv"
    validation_csv.write_text(
        "timestamp,open,high,low,close,volume\n"
        "2024-01-01T02:00:00,1.3000,1.3050,1.2950,1.3010,120\n"
        "2024-01-01T03:00:00,1.4000,1.4050,1.3950,1.4015,130\n",
        encoding="utf-8",
    )

    provider_registry = DatasetProviderRegistry()
    provider_registry.register(FilesystemCsvDatasetProvider(base_path=tmp_path))

    pipeline = ResearchPipeline(
        runner=ExperimentRunner(ExperimentExecutor()),
        evaluator=ResearchEvaluator(),
        registry=provider_registry,
    )

    report = pipeline.execute_discovery(
        DatasetQuery(symbol="EURUSD", timeframe="M1", source="filesystem-csv"),
        validation_query=DatasetQuery(
            symbol="EURUSD",
            timeframe="M1",
            source="filesystem-csv",
            provider_id="filesystem-csv",
        ),
    )

    assert len(report.rows) >= 1
    first_row = report.rows[0]
    assert hasattr(first_row, "validation_occurrences")
    assert hasattr(first_row, "validation_average_return")
    assert first_row.validation_occurrences >= 0.0
    assert isinstance(first_row.confirmed, bool)


class StaticOptimizationRunner:
    def __init__(self, scores: dict[str, float]) -> None:
        self._scores = scores

    def run(self, experiment: Experiment) -> Evidence:
        return Evidence(
            measurements={
                "score": self._scores[experiment.configuration.name],
            }
        )


class StaticMLExecutor:
    def execute(self, capability, evidence):
        return evidence.measurements[capability.input_metric_names[0]] * 2


class StaticVisualizationRenderer:
    def render(self, capability, payload, traceability):
        return {
            "capability": capability.capability_id,
            "sections": list(capability.required_sections),
            "traceability": [
                {
                    "type": reference.reference_type,
                    "id": reference.reference_id,
                }
                for reference in traceability
            ],
            "payload": payload,
        }


def test_research_pipeline_executes_optimization_problem() -> None:
    dataset = HistoricalDataset(
        metadata=DatasetMetadata(
            symbol="EURUSD",
            timeframe="M1",
        ),
        bars=(
            Bar(
                timestamp=datetime(2024, 1, 1),
                open=1.1000,
                high=1.1010,
                low=1.0990,
                close=1.1005,
            ),
        ),
    )

    market_description = MarketDescription(
        dataset=dataset,
        metadata=DescriptorMetadata(
            created_at=datetime.now(UTC),
            builder_version="1.0",
        ),
        descriptors=(),
    )

    hypothesis = ResearchHypothesis(
        market_description=market_description,
        metadata=HypothesisMetadata(
            created_at=datetime.now(UTC),
        ),
        statement="Optimization integration test",
    )

    baseline = Experiment(
        hypothesis=hypothesis,
        configuration=ResearchConfiguration(name="baseline"),
        status=ExperimentStatus.CREATED,
    )

    improved = Experiment(
        hypothesis=hypothesis,
        configuration=ResearchConfiguration(name="improved"),
        status=ExperimentStatus.CREATED,
    )

    pipeline = ResearchPipeline(
        runner=StaticOptimizationRunner({"baseline": 1.0, "improved": 2.0}),
        evaluator=ResearchEvaluator(),
        optimization_service=OptimizationService(
            runner=StaticOptimizationRunner({"baseline": 1.0, "improved": 2.0}),
            evaluator=ResearchEvaluator(),
        ),
    )

    result = pipeline.execute_optimization(
        OptimizationProblem(
            problem_id="opt-integration",
            objective_name="score",
            experiments=(baseline, improved),
        )
    )

    assert result.problem_id == "opt-integration"
    assert result.ranking == ("improved", "baseline")
    assert result.winner_configuration == "improved"


def test_research_pipeline_executes_ml_analysis() -> None:
    session = ResearchSession()
    evidence = Evidence(measurements={"profit_factor": 1.5})

    pipeline = ResearchPipeline(
        runner=ExperimentRunner(ExperimentExecutor()),
        evaluator=ResearchEvaluator(),
        ml_service=MachineLearningService(StaticMLExecutor()),
    )

    report = pipeline.execute_ml_analysis(
        session,
        MachineLearningCapability(
            capability_id="ml-profit",
            capability_name="Profit Factor Amplifier",
            input_metric_names=("profit_factor",),
            output_name="ml_score",
            assumptions=("Profit factor remains informative.",),
        ),
        evidence,
    )

    assert report.status == "completed"
    assert report.result.output_value == 3.0
    assert session.ml_report is report


def test_research_pipeline_executes_visualization() -> None:
    session = ResearchSession()

    pipeline = ResearchPipeline(
        runner=ExperimentRunner(ExperimentExecutor()),
        evaluator=ResearchEvaluator(),
        visualization_service=VisualizationService(StaticVisualizationRenderer()),
    )

    report = pipeline.execute_visualization(
        session,
        VisualizationCapability(
            capability_id="viz-pipeline-summary",
            capability_name="Pipeline Summary",
            required_sections=("summary", "metrics"),
            assumptions=("Evidence aggregation remains deterministic.",),
        ),
        payload={
            "summary": {"status": "completed"},
            "metrics": {"evidence_count": 3},
        },
        traceability=(
            VisualizationDataReference(
                reference_type="pipeline_report",
                reference_id="session-123",
                fingerprint="run-fingerprint-1",
            ),
        ),
    )

    assert report.status == "completed"
    assert report.rendered_sections == ("summary", "metrics")
    assert report.traceability_count == 1
    assert report.result.snapshot["capability"] == "viz-pipeline-summary"
    assert session.visualization_report is report


def test_research_pipeline_session_can_be_projected_for_visualization() -> None:
    session = ResearchSession(session_id="visualization-projection-session")
    pipeline = ResearchPipeline(
        runner=ExperimentRunner(ExperimentExecutor()),
        evaluator=ResearchEvaluator(),
    )

    report = pipeline.execute(session)
    projection = VisualizationProjectionBuilder().build(session, report)

    assert report.status is SessionStatus.COMPLETED
    assert projection.section("session").data["status"] == "completed"
    assert projection.section("session").data["pipeline_report_id"] == report.report_id
    assert projection.section("research").data["evidence_count"] == 0


def test_research_pipeline_executes_projection_visualization() -> None:
    session = ResearchSession(session_id="projection-visualization-session")
    pipeline = ResearchPipeline(
        runner=ExperimentRunner(ExperimentExecutor()),
        evaluator=ResearchEvaluator(),
        visualization_service=VisualizationService(StaticVisualizationRenderer()),
    )
    pipeline_report = pipeline.execute(session)
    projection = VisualizationProjectionBuilder().build(session, pipeline_report)

    visualization_report = pipeline.execute_visualization_projection(
        session,
        VisualizationCapability(
            capability_id="viz-session",
            capability_name="Session",
            required_sections=("session", "research"),
        ),
        projection,
    )

    assert visualization_report.status == "completed"
    assert visualization_report.rendered_sections == ("session", "research")
    assert visualization_report.result.snapshot["payload"] == {
        "session": projection.section("session").data,
        "research": projection.section("research").data,
    }
    assert session.visualization_report is visualization_report
    assert session.status is SessionStatus.COMPLETED
