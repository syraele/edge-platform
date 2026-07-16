"""
EDGE_ENGINE

Research Pipeline Integration Test
"""

from datetime import UTC, datetime

from edge.application.research.pipeline import ResearchPipeline
from edge.application.research.dataset_access_service import DatasetAccessService
from edge.application.research.report import PipelineReport
from edge.application.research.runner import ExperimentRunner
from edge.application.research.session import (
    ResearchSession,
    SessionStatus,
)
from edge.data import DatasetProviderRegistry
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
    ExperimentExecutor,
    ResearchEvaluator,
)
from edge.domain.evidence import Evidence
from edge.ml import MachineLearningCapability, MachineLearningService
from edge.optimization import OptimizationProblem, OptimizationService
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
    assert result.knowledge is None
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