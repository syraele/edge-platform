import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from edge.data import DatasetProviderRegistry, DatasetQuery
from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.data.providers.filesystem_csv_provider import FilesystemCsvDatasetProvider


def test_filesystem_csv_provider_registers_and_supports_queries(tmp_path: Path) -> None:
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(
        "timestamp,open,high,low,close,volume\n"
        "2024-01-01T00:00:00,1.1000,1.1010,1.0990,1.1005,100\n"
        "2024-01-01T01:00:00,1.2000,1.2050,1.1950,1.2012,110\n",
        encoding="utf-8",
    )

    provider = FilesystemCsvDatasetProvider(base_path=tmp_path)
    registry = DatasetProviderRegistry()
    registry.register(provider)

    query = DatasetQuery(symbol="EURUSD", timeframe="M1", source="filesystem-csv")

    assert provider.provider_id == "filesystem-csv"
    assert provider.supports(query) is True
    assert provider.supports(DatasetQuery(symbol="GBPUSD", timeframe="M1", source="filesystem-csv")) is False

    result = provider.load(query)

    assert isinstance(result, HistoricalDataset)
    assert result.metadata.symbol == "EURUSD"
    assert result.metadata.timeframe == "M1"
    assert result.metadata.source == "filesystem-csv"
    assert len(result.bars) == 2
    assert result.bars[0].close == pytest.approx(1.1005)
    assert result.bars[1].close == pytest.approx(1.2012)

    loaded = registry.load(query)
    assert loaded.dataset.metadata.symbol == "EURUSD"
    assert loaded.dataset.metadata.timeframe == "M1"
    assert loaded.provenance.provider_id == "filesystem-csv"


def test_filesystem_csv_provider_loads_manifest_backed_dataset(tmp_path: Path) -> None:
    dataset_dir = tmp_path / "eurusd" / "m1" / "v2026-08-03"
    dataset_dir.mkdir(parents=True)

    manifest = {
        "dataset_id": "eurusd-m1-v2026-08-03",
        "symbol": "EURUSD",
        "timeframe": "M1",
        "version": "v2026-08-03",
        "source": "mt5-import",
        "file": "bars.csv",
        "bars_count": 2,
        "range_start": "2024-01-01T00:00:00+00:00",
        "range_end": "2024-01-01T01:00:00+00:00",
    }
    (dataset_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    csv_path = dataset_dir / "bars.csv"
    csv_path.write_text(
        "timestamp,open,high,low,close,volume\n"
        "2024-01-01T00:00:00,1.1000,1.1010,1.0990,1.1005,100\n"
        "2024-01-01T01:00:00,1.2000,1.2050,1.1950,1.2012,110\n",
        encoding="utf-8",
    )

    provider = FilesystemCsvDatasetProvider(base_path=tmp_path)
    result = provider.load(DatasetQuery(symbol="EURUSD", timeframe="M1", source="filesystem-csv"))

    assert len(result.bars) == 2
    assert result.bars[0].close == pytest.approx(1.1005)
    assert result.bars[1].close == pytest.approx(1.2012)
