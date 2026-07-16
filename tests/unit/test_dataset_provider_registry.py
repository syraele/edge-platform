from datetime import UTC, datetime

import pytest

from edge.data import (
    DatasetProvider,
    DatasetProviderNotFoundError,
    DatasetProviderRegistry,
    DatasetProviderValidationError,
    DatasetQuery,
)
from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata


class StaticDatasetProvider(DatasetProvider):
    provider_version = "1.2.0"

    def __init__(self, provider_id: str, supported_symbol: str = "XAUUSD") -> None:
        self.provider_id = provider_id
        self._supported_symbol = supported_symbol

    def supports(self, query: DatasetQuery) -> bool:
        return query.symbol == self._supported_symbol

    def load(self, query: DatasetQuery) -> HistoricalDataset:
        bar = Bar(
            timestamp=datetime(2024, 1, 1, tzinfo=UTC),
            open=100.0,
            high=101.0,
            low=99.0,
            close=100.5,
            volume=10.0,
        )

        return HistoricalDataset(
            metadata=DatasetMetadata(
                symbol=query.symbol,
                timeframe=query.timeframe,
                source=query.source or self.provider_id,
            ),
            bars=(bar,),
        )


def test_registry_rejects_duplicate_provider_id():
    registry = DatasetProviderRegistry()

    registry.register(StaticDatasetProvider("demo"))

    with pytest.raises(DatasetProviderValidationError):
        registry.register(StaticDatasetProvider("demo"))


def test_registry_resolve_raises_when_no_provider_matches():
    registry = DatasetProviderRegistry()
    registry.register(StaticDatasetProvider("demo", supported_symbol="BTCUSD"))

    with pytest.raises(DatasetProviderNotFoundError):
        registry.resolve(DatasetQuery(symbol="XAUUSD", timeframe="H1"))


def test_registry_load_returns_provenanced_dataset():
    registry = DatasetProviderRegistry()
    registry.register(StaticDatasetProvider("history-provider"))

    result = registry.load(
        DatasetQuery(symbol="XAUUSD", timeframe="H1", source="archive-v1")
    )

    assert result.dataset.size == 1
    assert result.provenance.provider_id == "history-provider"
    assert result.provenance.provider_version == "1.2.0"
    assert result.provenance.dataset_source == "archive-v1"
