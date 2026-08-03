from datetime import UTC, datetime
from pathlib import Path

import pytest

from edge.data.connectors.mt5_connector import Mt5DatasetConnector
from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.providers.local_dataset_registry import LocalDatasetRegistry


class FakeMT5Module:
    def __init__(self) -> None:
        self.initialized = False
        self.selected_symbol = None
        self.calls = []

    def initialize(self) -> bool:
        self.initialized = True
        return True

    def symbol_select(self, symbol: str, enable: bool) -> bool:
        self.selected_symbol = (symbol, enable)
        return True

    def copy_rates_range(self, symbol: str, timeframe: int, start: datetime, end: datetime):
        self.calls.append((symbol, timeframe, start, end))
        return [
            {"time": datetime(2024, 1, 1, 0, 0, tzinfo=UTC), "open": 1.1000, "high": 1.1010, "low": 1.0990, "close": 1.1005, "tick_volume": 100},
            {"time": datetime(2024, 1, 1, 0, 1, tzinfo=UTC), "open": 1.1005, "high": 1.1015, "low": 1.1000, "close": 1.1010, "tick_volume": 110},
        ]

    def shutdown(self) -> None:
        self.initialized = False


class EmptyHistoryMT5Module(FakeMT5Module):
    def copy_rates_range(self, symbol: str, timeframe: int, start: datetime, end: datetime):
        self.calls.append((symbol, timeframe, start, end))
        return []


class MissingSymbolMT5Module(FakeMT5Module):
    def symbol_select(self, symbol: str, enable: bool) -> bool:
        self.selected_symbol = (symbol, enable)
        return False


class ConnectionErrorMT5Module(FakeMT5Module):
    def initialize(self) -> bool:
        self.initialized = False
        return False


def test_mt5_connector_imports_m1_dataset_and_registers_it(tmp_path: Path) -> None:
    mt5_module = FakeMT5Module()
    connector = Mt5DatasetConnector(output_root=tmp_path, mt5_module=mt5_module)

    dataset, dataset_dir, manifest = connector.import_from_source(
        symbol="EURUSD",
        timeframe="M1",
        version="v2024-01",
        start=datetime(2024, 1, 1, tzinfo=UTC),
        end=datetime(2024, 1, 2, tzinfo=UTC),
    )

    assert isinstance(dataset, HistoricalDataset)
    assert dataset.metadata.symbol == "EURUSD"
    assert dataset.metadata.timeframe == "M1"
    assert len(dataset.bars) == 2

    assert dataset_dir == tmp_path / "eurusd" / "m1" / "v2024-01"
    assert (dataset_dir / "bars.csv").exists()
    assert (dataset_dir / "manifest.json").exists()
    assert (dataset_dir / "checksum.sha256").exists()

    manifest_payload = (dataset_dir / "manifest.json").read_text(encoding="utf-8")
    assert '"dataset_id": "eurusd-m1-v2024-01"' in manifest_payload
    assert manifest.bars_count == 2

    registry = LocalDatasetRegistry(base_path=tmp_path)
    verified = registry.verify(dataset_dir)
    assert verified["dataset_id"] == "eurusd-m1-v2024-01"
    assert verified["bars_count"] == 2

    assert mt5_module.calls[0][0] == "EURUSD"
    assert mt5_module.calls[0][1] == 1


def test_mt5_connector_rejects_non_m1_timeframe(tmp_path: Path) -> None:
    connector = Mt5DatasetConnector(output_root=tmp_path, mt5_module=FakeMT5Module())

    with pytest.raises(ValueError, match="Only M1 is supported by MT5Connector"):
        connector.import_from_source(
            symbol="EURUSD",
            timeframe="M5",
            version="v2024-01",
            start=datetime(2024, 1, 1, tzinfo=UTC),
            end=datetime(2024, 1, 2, tzinfo=UTC),
        )


def test_mt5_connector_rejects_start_after_end(tmp_path: Path) -> None:
    connector = Mt5DatasetConnector(output_root=tmp_path, mt5_module=FakeMT5Module())

    with pytest.raises(ValueError, match="start.*end"):
        connector.import_from_source(
            symbol="EURUSD",
            timeframe="M1",
            version="v2024-01",
            start=datetime(2024, 1, 2, tzinfo=UTC),
            end=datetime(2024, 1, 1, tzinfo=UTC),
        )


@pytest.mark.parametrize(
    ("module", "expected_message"),
    [
        (EmptyHistoryMT5Module(), "No MT5 historical data available"),
        (MissingSymbolMT5Module(), "does not exist"),
        (ConnectionErrorMT5Module(), "connection"),
    ],
)
def test_mt5_connector_reports_specific_no_data_errors(tmp_path: Path, module: FakeMT5Module, expected_message: str) -> None:
    connector = Mt5DatasetConnector(output_root=tmp_path, mt5_module=module)

    with pytest.raises(RuntimeError, match=expected_message):
        connector.import_from_source(
            symbol="EURUSD",
            timeframe="M1",
            version="v2024-01",
            start=datetime(2024, 1, 1, tzinfo=UTC),
            end=datetime(2024, 1, 2, tzinfo=UTC),
        )
