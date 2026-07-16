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


class NotAProvider:
    pass
