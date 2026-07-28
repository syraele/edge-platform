from datetime import UTC, datetime

import pytest

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.domain.descriptor_metadata import DescriptorMetadata
from edge.domain.evidence import Evidence
from edge.domain.experiment import Experiment
from edge.domain.experiment_status import ExperimentStatus
from edge.domain.hypothesis_metadata import HypothesisMetadata
from edge.domain.market_description import MarketDescription
from edge.domain.research_configuration import ResearchConfiguration
from edge.domain.research_hypothesis import ResearchHypothesis
from edge.domain.services import ExperimentExecutor


def test_executor_produces_evidence() -> None:
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

    hypothesis = ResearchHypothesis(
        market_description=market_description,
        metadata=HypothesisMetadata(
            created_at=datetime.now(UTC),
        ),
        statement="Test hypothesis",
    )

    configuration = ResearchConfiguration(
        name="baseline",
    )

    experiment = Experiment(
        hypothesis=hypothesis,
        configuration=configuration,
        status=ExperimentStatus.CREATED,
    )

    executor = ExperimentExecutor()

    evidence = executor.execute(experiment)

    assert isinstance(evidence, Evidence)
    assert evidence.measurements["bars_processed"] == 4.0

    expected_average_return = (
        ((1.1005 - 1.1000) / 1.1000)
        + ((1.2012 - 1.2000) / 1.2000)
        + ((1.2055 - 1.2050) / 1.2050)
        + ((1.3010 - 1.3000) / 1.3000)
    ) / 4

    assert evidence.measurements["average_return"] == pytest.approx(expected_average_return)

    assert evidence.measurements["average_return_1"] == pytest.approx(
        (
            (1.2012 - 1.1005) / 1.1005
            + (1.2055 - 1.2012) / 1.2012
            + (1.3010 - 1.2055) / 1.2055
        )
        / 3
    )
    assert evidence.measurements["average_return_5"] == pytest.approx(0.0)
    assert evidence.measurements["average_return_10"] == pytest.approx(0.0)
    assert evidence.measurements["average_return_20"] == pytest.approx(0.0)


def test_executor_evaluates_hypothesis_statement_against_dataset() -> None:
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
        statement="close < open",
    )

    experiment = Experiment(
        hypothesis=hypothesis,
        configuration=ResearchConfiguration(name="baseline"),
        status=ExperimentStatus.CREATED,
    )

    executor = ExperimentExecutor()
    evidence = executor.execute(experiment)

    assert evidence.measurements["hypothesis_occurrences"] == 0.0
    assert evidence.measurements["hypothesis_matches"] == 0.0

    hypothesis = ResearchHypothesis(
        market_description=market_description,
        metadata=HypothesisMetadata(
            created_at=datetime.now(UTC),
        ),
        statement="close > open",
    )

    experiment = Experiment(
        hypothesis=hypothesis,
        configuration=ResearchConfiguration(name="baseline"),
        status=ExperimentStatus.CREATED,
    )

    evidence = executor.execute(experiment)

    assert evidence.measurements["hypothesis_occurrences"] == 3.0
    assert evidence.measurements["hypothesis_matches"] == 3.0


def test_executor_generates_autonomous_hypothesis_evidence() -> None:
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

    hypothesis = ResearchHypothesis(
        market_description=market_description,
        metadata=HypothesisMetadata(
            created_at=datetime.now(UTC),
        ),
        statement="close > open",
    )

    configuration = ResearchConfiguration(
        name="baseline",
    )

    experiment = Experiment(
        hypothesis=hypothesis,
        configuration=configuration,
        status=ExperimentStatus.CREATED,
    )

    executor = ExperimentExecutor()

    evidence = executor.execute(experiment)

    assert evidence.measurements["hypothesis_matches"] == 4.0
    assert evidence.measurements["hypothesis_occurrences"] == 4.0
    assert evidence.measurements["hypothesis_average_return"] == pytest.approx(
        (
            ((1.1005 - 1.1000) / 1.1000)
            + ((1.2012 - 1.2000) / 1.2000)
            + ((1.2055 - 1.2050) / 1.2050)
            + ((1.3010 - 1.3000) / 1.3000)
        )
        / 4
    )
    assert evidence.measurements["hypothesis_average_return_1"] == pytest.approx(
        (
            (1.2012 - 1.1005) / 1.1005
            + (1.2055 - 1.2012) / 1.2012
            + (1.3010 - 1.2055) / 1.2055
        )
        / 3
    )
    assert evidence.measurements["hypothesis_average_return_5"] == pytest.approx(0.0)
    assert evidence.measurements["hypothesis_average_return_10"] == pytest.approx(0.0)
    assert evidence.measurements["hypothesis_average_return_20"] == pytest.approx(0.0)