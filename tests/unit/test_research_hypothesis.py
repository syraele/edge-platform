from datetime import datetime

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.domain.descriptor_metadata import DescriptorMetadata
from edge.domain.hypothesis_metadata import HypothesisMetadata
from edge.domain.market_description import MarketDescription
from edge.domain.research_hypothesis import ResearchHypothesis


def test_create_research_hypothesis():
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
        statement="The market trends after high volatility.",
    )

    assert hypothesis.market_description is market_description
    assert (
        hypothesis.statement
        == "The market trends after high volatility."
    )

    assert hypothesis.metadata.version == "1.0"