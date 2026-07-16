from datetime import UTC, datetime

import pytest

from edge.data import (
    DatasetProvider,
    DatasetProviderCompatibilityError,
    DatasetProviderLoadError,
    DatasetProviderNotFoundError,
    DatasetProviderRegistry,
    DatasetProviderValidationError,
    DatasetQuery,
)
from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.data.validation import SortedDeduplicatedNormalizationPolicy


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


class IncompatibleDatasetProvider(StaticDatasetProvider):
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
                symbol="EURUSD",
                timeframe=query.timeframe,
                source=query.source or self.provider_id,
            ),
            bars=(bar,),
        )


class FailingDatasetProvider(StaticDatasetProvider):
    def load(self, query: DatasetQuery) -> HistoricalDataset:
        raise RuntimeError("provider failure")


class EarlyDatasetProvider(StaticDatasetProvider):
    def load(self, query: DatasetQuery) -> HistoricalDataset:
        bar = Bar(
            timestamp=datetime(2023, 12, 31, 23, 0, tzinfo=UTC),
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


class UnorderedDuplicateDatasetProvider(StaticDatasetProvider):
    def load(self, query: DatasetQuery) -> HistoricalDataset:
        first = Bar(
            timestamp=datetime(2024, 1, 1, 2, 0, tzinfo=UTC),
            open=100.0,
            high=101.0,
            low=99.0,
            close=100.5,
            volume=10.0,
        )
        duplicate = Bar(
            timestamp=datetime(2024, 1, 1, 1, 0, tzinfo=UTC),
            open=110.0,
            high=111.0,
            low=109.0,
            close=110.5,
            volume=11.0,
        )
        original = Bar(
            timestamp=datetime(2024, 1, 1, 1, 0, tzinfo=UTC),
            open=90.0,
            high=91.0,
            low=89.0,
            close=90.5,
            volume=9.0,
        )

        return HistoricalDataset(
            metadata=DatasetMetadata(
                symbol=query.symbol,
                timeframe=query.timeframe,
                source=query.source or self.provider_id,
            ),
            bars=(first, duplicate, original),
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
    assert result.provenance.dataset_start == datetime(2024, 1, 1, tzinfo=UTC)
    assert result.provenance.dataset_end == datetime(2024, 1, 1, tzinfo=UTC)


def test_registry_load_with_explicit_provider_id():
    registry = DatasetProviderRegistry()
    registry.register(StaticDatasetProvider("provider-a", supported_symbol="XAUUSD"))
    registry.register(StaticDatasetProvider("provider-b", supported_symbol="XAUUSD"))

    result = registry.load(
        DatasetQuery(
            symbol="XAUUSD",
            timeframe="H1",
            provider_id="provider-b",
        )
    )

    assert result.provenance.provider_id == "provider-b"


def test_registry_raises_when_dataset_incompatible_with_query():
    registry = DatasetProviderRegistry()
    registry.register(IncompatibleDatasetProvider("bad-provider"))

    with pytest.raises(DatasetProviderCompatibilityError):
        registry.load(DatasetQuery(symbol="XAUUSD", timeframe="H1"))


def test_registry_raises_when_query_time_window_is_invalid():
    registry = DatasetProviderRegistry()
    registry.register(StaticDatasetProvider("history-provider"))

    with pytest.raises(DatasetProviderCompatibilityError):
        registry.load(
            DatasetQuery(
                symbol="XAUUSD",
                timeframe="H1",
                start=datetime(2024, 1, 2, tzinfo=UTC),
                end=datetime(2024, 1, 1, tzinfo=UTC),
            )
        )


def test_registry_raises_when_dataset_precedes_requested_start():
    registry = DatasetProviderRegistry()
    registry.register(EarlyDatasetProvider("early-provider"))

    with pytest.raises(DatasetProviderCompatibilityError):
        registry.load(
            DatasetQuery(
                symbol="XAUUSD",
                timeframe="H1",
                start=datetime(2024, 1, 1, tzinfo=UTC),
            )
        )


def test_registry_load_with_fallback_uses_next_provider_after_failure():
    registry = DatasetProviderRegistry()
    registry.register(FailingDatasetProvider("primary-provider"))
    registry.register(StaticDatasetProvider("backup-provider"))

    result = registry.load_with_fallback(
        DatasetQuery(
            symbol="XAUUSD",
            timeframe="H1",
            provider_id="primary-provider",
        ),
        fallback_provider_ids=["backup-provider"],
    )

    assert result.provenance.provider_id == "backup-provider"


def test_registry_load_with_fallback_raises_when_all_attempts_fail():
    registry = DatasetProviderRegistry()
    registry.register(FailingDatasetProvider("primary-provider"))
    registry.register(IncompatibleDatasetProvider("backup-provider"))

    with pytest.raises(DatasetProviderLoadError):
        registry.load_with_fallback(
            DatasetQuery(
                symbol="XAUUSD",
                timeframe="H1",
                provider_id="primary-provider",
            ),
            fallback_provider_ids=["backup-provider"],
        )


def test_registry_applies_sorted_deduplicated_normalization_policy():
    registry = DatasetProviderRegistry(
        normalization_policy=SortedDeduplicatedNormalizationPolicy(),
    )
    registry.register(UnorderedDuplicateDatasetProvider("unordered-provider"))

    result = registry.load(DatasetQuery(symbol="XAUUSD", timeframe="H1"))

    assert result.dataset.size == 2
    assert result.dataset.first_bar.timestamp == datetime(2024, 1, 1, 1, 0, tzinfo=UTC)
    assert result.dataset.last_bar.timestamp == datetime(2024, 1, 1, 2, 0, tzinfo=UTC)
    assert result.dataset.first_bar.open == 90.0
    assert result.provenance.normalization == "sorted_deduplicated"
