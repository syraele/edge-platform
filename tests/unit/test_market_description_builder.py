from datetime import datetime

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.domain.market_description import MarketDescription
from edge.domain.services.market_description_builder import (
    MarketDescriptionBuilder,
)


def test_market_description_builder_creates_description():
    metadata = DatasetMetadata(
        symbol="EURUSD",
        timeframe="M1",
    )

    bars = (
        Bar(
            timestamp=datetime(2024, 1, 1),
            open=1.1000,
            high=1.1010,
            low=1.0990,
            close=1.1005,
        ),
    )

    dataset = HistoricalDataset(
        metadata=metadata,
        bars=bars,
    )

    builder = MarketDescriptionBuilder()

    description = builder.build(dataset)

    assert isinstance(description, MarketDescription)
    assert description.dataset is dataset
    assert description.is_empty
    assert description.size == 0
    assert description.metadata.builder_version == "1.0"