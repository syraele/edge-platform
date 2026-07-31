from datetime import UTC, datetime

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.domain.descriptor_metadata import DescriptorMetadata
from edge.domain.hypothesis_metadata import HypothesisMetadata
from edge.domain.market_description import MarketDescription
from edge.domain.research_hypothesis import ResearchHypothesis
from edge.domain.services.hypothesis_factory import HypothesisFactory


def test_hypothesis_factory_creates_primitive_hypotheses() -> None:
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

    factory = HypothesisFactory()
    hypotheses = factory.create_hypotheses(market_description)

    assert len(hypotheses) >= 8
    assert all(isinstance(hypothesis, ResearchHypothesis) for hypothesis in hypotheses)
    assert any(hypothesis.statement == "close > open" for hypothesis in hypotheses)
    assert any(hypothesis.statement == "close < open" for hypothesis in hypotheses)
    assert any(hypothesis.statement == "close > previous_close" for hypothesis in hypotheses)
    assert any(hypothesis.statement == "close < previous_close" for hypothesis in hypotheses)
    assert any(hypothesis.statement == "high > previous_high" for hypothesis in hypotheses)
    assert any(hypothesis.statement == "low < previous_low" for hypothesis in hypotheses)


def test_hypothesis_factory_creates_contextual_hypotheses() -> None:
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

    factory = HypothesisFactory()
    hypotheses = factory.create_hypotheses(market_description)

    statements = {hypothesis.statement for hypothesis in hypotheses}
    assert any("body_to_range_ratio" in statement for statement in statements)
    assert any("recent_return_3" in statement for statement in statements)
