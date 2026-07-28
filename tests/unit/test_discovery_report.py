from datetime import UTC, datetime

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.domain.descriptor_metadata import DescriptorMetadata
from edge.domain.market_description import MarketDescription
from edge.domain.services.experiment_executor import ExperimentExecutor
from edge.domain.services.hypothesis_factory import HypothesisFactory
from edge.domain.services.discovery_report import DiscoveryReport, DiscoveryReportService


def test_discovery_report_contains_all_hypotheses_and_orders_by_average_return_10() -> None:
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
            Bar(
                timestamp=datetime(2024, 1, 2),
                open=1.2000,
                high=1.2050,
                low=1.1950,
                close=1.2012,
            ),
            Bar(
                timestamp=datetime(2024, 1, 3),
                open=1.2050,
                high=1.2060,
                low=1.2040,
                close=1.2055,
            ),
            Bar(
                timestamp=datetime(2024, 1, 4),
                open=1.3000,
                high=1.3050,
                low=1.2950,
                close=1.3010,
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

    hypotheses = HypothesisFactory().create_hypotheses(market_description)
    executor = ExperimentExecutor()
    evidences = [executor.execute(hypothesis_to_experiment(hypothesis)) for hypothesis in hypotheses]

    report = DiscoveryReportService().create_report(hypotheses, evidences)

    assert len(report.rows) == len(hypotheses)
    assert {row.hypothesis_name for row in report.rows} == {hypothesis.statement for hypothesis in hypotheses}
    assert list(report.rows) == sorted(report.rows, key=lambda row: row.average_return_10, reverse=True)


def hypothesis_to_experiment(hypothesis):
    from edge.domain.experiment import Experiment
    from edge.domain.experiment_status import ExperimentStatus
    from edge.domain.research_configuration import ResearchConfiguration

    return Experiment(
        hypothesis=hypothesis,
        configuration=ResearchConfiguration(name="baseline"),
        status=ExperimentStatus.CREATED,
    )
