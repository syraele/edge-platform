from datetime import UTC, datetime

from edge.data import DatasetProvider, DatasetQuery
from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata


class HistoricalArchiveProvider(DatasetProvider):
    provider_id = "historical-archive"
    provider_version = "2.0.0"

    def supports(self, query: DatasetQuery) -> bool:
        return query.symbol in {"XAUUSD", "EURUSD"}

    def load(self, query: DatasetQuery) -> HistoricalDataset:
        bar = Bar(
            timestamp=datetime(2024, 1, 1, tzinfo=UTC),
            open=2000.0,
            high=2010.0,
            low=1990.0,
            close=2005.0,
            volume=123.0,
        )

        return HistoricalDataset(
            metadata=DatasetMetadata(
                symbol=query.symbol,
                timeframe=query.timeframe,
                source="archive-store",
            ),
            bars=(bar,),
        )


class UnorderedArchiveProvider(DatasetProvider):
    provider_id = "unordered-archive"
    provider_version = "2.1.0"

    def supports(self, query: DatasetQuery) -> bool:
        return query.symbol == "XAUUSD"

    def load(self, query: DatasetQuery) -> HistoricalDataset:
        first = Bar(
            timestamp=datetime(2024, 1, 1, 2, 0, tzinfo=UTC),
            open=2000.0,
            high=2010.0,
            low=1990.0,
            close=2005.0,
            volume=123.0,
        )
        duplicate = Bar(
            timestamp=datetime(2024, 1, 1, 1, 0, tzinfo=UTC),
            open=2100.0,
            high=2110.0,
            low=2090.0,
            close=2105.0,
            volume=124.0,
        )
        original = Bar(
            timestamp=datetime(2024, 1, 1, 1, 0, tzinfo=UTC),
            open=1900.0,
            high=1910.0,
            low=1890.0,
            close=1905.0,
            volume=122.0,
        )

        return HistoricalDataset(
            metadata=DatasetMetadata(
                symbol=query.symbol,
                timeframe=query.timeframe,
                source="unordered-archive-store",
            ),
            bars=(first, duplicate, original),
        )


class NotAProvider:
    pass
