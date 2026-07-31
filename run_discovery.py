from datetime import UTC, datetime

from edge.application.research.pipeline import ResearchPipeline
from edge.application.research.runner import ExperimentRunner
from edge.application.research.session import ResearchSession
from edge.data import DatasetProviderRegistry, DatasetQuery
from edge.data.providers.mt5_provider import Mt5DatasetProvider
from edge.domain.services import ExperimentExecutor, ResearchEvaluator

registry = DatasetProviderRegistry()
registry.register(Mt5DatasetProvider())

query = DatasetQuery(
    symbol="XAUUSD",
    timeframe="M1",
    start=datetime(2026, 4, 1, tzinfo=UTC),
    end=datetime(2026, 4, 30, tzinfo=UTC),
)

pipeline = ResearchPipeline(
    runner=ExperimentRunner(ExperimentExecutor()),
    evaluator=ResearchEvaluator(),
    registry=registry,
)

report = pipeline.execute_discovery(query, ResearchSession())
print(report)