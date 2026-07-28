import sys
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import Mock

import numpy as np
import pytest

from edge.data import DatasetProviderRegistry, DatasetQuery
from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.providers.mt5_provider import Mt5DatasetProvider


class DummyTicks:
    def __init__(self, records):
        self.records = records

    def __iter__(self):
        return iter(self.records)


def test_mt5_provider_initializes_and_loads_historical_data(monkeypatch: pytest.MonkeyPatch) -> None:
    mt5_module = SimpleNamespace(
        initialize=Mock(return_value=True),
        shutdown=Mock(),
        symbol_select=Mock(return_value=True),
        copy_rates_from_pos=Mock(return_value=[
            {
                "time": 1704067200,
                "open": 1.1000,
                "high": 1.1010,
                "low": 1.0990,
                "close": 1.1005,
                "tick_volume": 100,
            }
        ]),
        copy_rates_range=Mock(return_value=[
            {
                "time": 1704067200,
                "open": 1.1000,
                "high": 1.1010,
                "low": 1.0990,
                "close": 1.1005,
                "tick_volume": 100,
            }
        ]),
        copy_rates_from=Mock(return_value=[
            {
                "time": 1704067200,
                "open": 1.1000,
                "high": 1.1010,
                "low": 1.0990,
                "close": 1.1005,
                "tick_volume": 100,
            }
        ]),
    )
    monkeypatch.setitem(__import__("sys").modules, "MetaTrader5", mt5_module)

    provider = Mt5DatasetProvider()
    registry = DatasetProviderRegistry()
    registry.register(provider)

    query = DatasetQuery(symbol="EURUSD", timeframe="M1", start=datetime(2024, 1, 1, tzinfo=UTC), end=datetime(2024, 1, 2, tzinfo=UTC))

    assert provider.provider_id == "mt5"
    assert provider.supports(query) is True
    assert provider.supports(DatasetQuery(symbol="GBPUSD", timeframe="M1")) is False

    result = provider.load(query)

    assert isinstance(result, HistoricalDataset)
    assert result.metadata.symbol == "EURUSD"
    assert result.metadata.timeframe == "M1"
    assert result.metadata.source == "mt5"
    assert len(result.bars) == 1
    assert result.bars[0].close == pytest.approx(1.1005)

    loaded = registry.load(query)
    assert loaded.dataset.metadata.symbol == "EURUSD"
    assert loaded.provenance.provider_id == "mt5"


def test_mt5_provider_reports_when_all_rates_are_filtered_out(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    mt5_module = SimpleNamespace(
        initialize=Mock(return_value=True),
        shutdown=Mock(),
        symbol_select=Mock(return_value=True),
        copy_rates_range=Mock(return_value=[
            {
                "time": 1704067200,
                "open": 1.1000,
                "high": 1.1010,
                "low": 1.0990,
                "close": 1.1005,
                "tick_volume": 100,
            }
        ]),
    )
    monkeypatch.setitem(__import__("sys").modules, "MetaTrader5", mt5_module)

    provider = Mt5DatasetProvider()
    query = DatasetQuery(symbol="EURUSD", timeframe="M1", start=datetime(2024, 1, 2, tzinfo=UTC), end=datetime(2024, 1, 3, tzinfo=UTC))

    result = provider.load(query)

    assert isinstance(result, HistoricalDataset)
    assert len(result.bars) == 0
    assert "copy_rates_range" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("rates", "expected_bars"),
    [
        (None, 0),
        (np.array([], dtype=[("time", "i8"), ("open", "f8"), ("high", "f8"), ("low", "f8"), ("close", "f8"), ("tick_volume", "i8")]), 0),
        (
            np.array(
                [(1704067200, 1.1000, 1.1010, 1.0990, 1.1005, 100)],
                dtype=[("time", "i8"), ("open", "f8"), ("high", "f8"), ("low", "f8"), ("close", "f8"), ("tick_volume", "i8")],
            ),
            1,
        ),
    ],
)
def test_mt5_provider_handles_rates_containers(monkeypatch: pytest.MonkeyPatch, rates: object | None, expected_bars: int) -> None:
    mt5_module = SimpleNamespace(
        initialize=Mock(return_value=True),
        shutdown=Mock(),
        symbol_select=Mock(return_value=True),
        copy_rates_range=Mock(return_value=rates),
    )
    monkeypatch.setitem(sys.modules, "MetaTrader5", mt5_module)

    provider = Mt5DatasetProvider()
    query = DatasetQuery(symbol="EURUSD", timeframe="M1", start=datetime(2024, 1, 1, tzinfo=UTC), end=datetime(2024, 1, 2, tzinfo=UTC))

    if rates is None or len(rates) == 0:
        with pytest.raises(RuntimeError, match="No MT5 data available"):
            provider.load(query)
    else:
        result = provider.load(query)
        assert len(result.bars) == expected_bars


def test_mt5_provider_handles_api_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    mt5_module = SimpleNamespace(
        initialize=Mock(return_value=False),
        last_error=Mock(return_value=SimpleNamespace(description="init failed")),
        shutdown=Mock(),
    )
    monkeypatch.setitem(sys.modules, "MetaTrader5", mt5_module)

    provider = Mt5DatasetProvider()

    with pytest.raises(RuntimeError, match="MT5 initialization failed"):
        provider.load(DatasetQuery(symbol="EURUSD", timeframe="M1"))
