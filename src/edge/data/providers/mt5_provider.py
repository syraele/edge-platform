"""
EDGE_ENGINE

MT5 Dataset Provider
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata

from .base import DatasetProvider
from .query import DatasetQuery


class Mt5DatasetProvider(DatasetProvider):
    """Minimal MetaTrader5-backed dataset provider."""

    provider_id = "mt5"
    provider_version = "1.0.0"
    provider_name = "MT5 Dataset Provider"
    dataset_source = "mt5"
    supported_symbols = ("EURUSD", "XAUUSD")

    def __init__(self, module: Any | None = None) -> None:
        self._module = module

    def supports(self, query: DatasetQuery) -> bool:
        return query.symbol in self.supported_symbols

    def load(self, query: DatasetQuery) -> HistoricalDataset:
        mt5 = self._get_mt5_module()

        if not mt5.initialize():
            error = mt5.last_error() if hasattr(mt5, "last_error") else None
            description = getattr(error, "description", None) or "unknown error"
            raise RuntimeError(f"MT5 initialization failed: {description}")

        try:
            if not mt5.symbol_select(query.symbol, True):
                raise RuntimeError(f"MT5 symbol '{query.symbol}' could not be selected")

            if query.start is None or query.end is None:
                raise RuntimeError("MT5 provider requires both start and end timestamps")

            rates = mt5.copy_rates_range(
                query.symbol,
                self._to_mt5_timeframe(query.timeframe),
                query.start,
                query.end,
            )

            if rates is None or len(rates) == 0:
                raise RuntimeError("No MT5 data available for the requested query")

            bars = []
            for entry in rates:
                timestamp = self._coerce_timestamp(self._read_field(entry, "time"))

                if query.start is not None and timestamp < query.start:
                    continue
                if query.end is not None and timestamp > query.end:
                    continue

                bars.append(
                    Bar(
                        timestamp=timestamp,
                        open=float(self._read_field(entry, "open", default=0.0)),
                        high=float(self._read_field(entry, "high", default=0.0)),
                        low=float(self._read_field(entry, "low", default=0.0)),
                        close=float(self._read_field(entry, "close", default=0.0)),
                        volume=float(self._read_field(entry, "tick_volume", default=self._read_field(entry, "volume", default=0.0))),
                    )
                )

            if not bars:
                first_rate_timestamp = None
                if rates:
                    first_rate_timestamp = self._coerce_timestamp(self._read_field(rates[0], "time"))

                print(
                    "MT5 diagnostic: symbol=%s timeframe=%s requested_range=%s..%s raw_rates=%s copy_rates_range=%s first_rate_timestamp=%s"
                    % (
                        query.symbol,
                        query.timeframe,
                        query.start,
                        query.end,
                        len(rates),
                        self._to_mt5_timeframe(query.timeframe),
                        first_rate_timestamp,
                    )
                )

            return HistoricalDataset(
                metadata=DatasetMetadata(
                    symbol=query.symbol,
                    timeframe=query.timeframe,
                    source=self.dataset_source,
                ),
                bars=tuple(bars),
            )
        finally:
            if hasattr(mt5, "shutdown"):
                mt5.shutdown()

    def _get_mt5_module(self) -> Any:
        if self._module is not None:
            return self._module

        try:
            import MetaTrader5 as mt5
        except ImportError as exc:
            raise RuntimeError("MetaTrader5 is not installed") from exc

        return mt5

    def _to_mt5_timeframe(self, timeframe: str) -> int:
        mapping = {
            "M1": 1,
            "M5": 5,
            "M15": 15,
            "M30": 30,
            "H1": 16384,
            "H4": 16384 * 4,
            "D1": 16384 * 24,
            "W1": 16384 * 24 * 7,
            "MN1": 16384 * 24 * 30,
        }

        normalized = timeframe.upper()
        if normalized not in mapping:
            raise RuntimeError(f"Unsupported MT5 timeframe: {timeframe}")

        return mapping[normalized]

    def _read_field(self, entry: Any, field_name: str, default: Any = None) -> Any:
        if hasattr(entry, "__getitem__"):
            try:
                return entry[field_name]
            except (KeyError, IndexError, TypeError, ValueError):
                return default

        if hasattr(entry, "get"):
            return entry.get(field_name, default)

        return default

    def _coerce_timestamp(self, value: Any) -> datetime:
        if isinstance(value, datetime):
            if value.tzinfo is None:
                return value.replace(tzinfo=UTC)
            return value

        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(float(value), tz=UTC)

        if hasattr(value, "tolist"):
            return self._coerce_timestamp(value.tolist())

        try:
            return datetime.fromisoformat(str(value))
        except ValueError:
            return datetime.fromtimestamp(float(str(value)), tz=UTC)
