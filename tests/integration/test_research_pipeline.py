"""
EDGE_ENGINE

Research Pipeline Integration Test
"""

from datetime import datetime

from edge.application.research.pipeline import ResearchPipeline
from edge.application.research.report import PipelineReport
from edge.application.research.runner import ExperimentRunner
from edge.application.research.session import (
    ResearchSession,
    SessionStatus,
)
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
            created_at=datetime.utcnow(),
            builder_version="1.0",
        ),
        descriptors=(),
    )

    hypothesis = ResearchHypothesis(
        market_description=market_description,
        metadata=HypothesisMetadata(
            created_at=datetime.utcnow(),
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
    assert result.hypotheses == tuple(session.hypotheses)
    assert result.experiments == tuple(session.experiments)
    assert result.edges == tuple(session.edges)
    assert result.message is None