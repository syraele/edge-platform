"""
EDGE_ENGINE

Filesystem CSV Dataset Provider
"""

from __future__ import annotations

import csv
from datetime import UTC, datetime
from pathlib import Path

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata

from .base import DatasetProvider
from .local_dataset_registry import LocalDatasetRegistry
from .query import DatasetQuery


class FilesystemCsvDatasetProvider(DatasetProvider):
    """Minimal filesystem CSV provider for historical datasets."""

    provider_id = "filesystem-csv"
    provider_version = "1.0.0"
    provider_name = "Filesystem CSV Dataset Provider"
    dataset_source = "filesystem-csv"
    supported_symbols = ("EURUSD", "XAUUSD")

    def __init__(self, base_path: str | Path | None = None) -> None:
        self.base_path = Path(base_path or ".")
        self._registry = LocalDatasetRegistry(self.base_path)

    def supports(self, query: DatasetQuery) -> bool:
        return query.symbol in self.supported_symbols

    def load(self, query: DatasetQuery) -> HistoricalDataset:
        csv_path = self._resolve_path(query)
        bars = []

        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                timestamp = self._parse_timestamp(row["timestamp"])
                bars.append(
                    Bar(
                        timestamp=timestamp,
                        open=float(row["open"]),
                        high=float(row["high"]),
                        low=float(row["low"]),
                        close=float(row["close"]),
                        volume=float(row.get("volume", 0.0)),
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

    def _resolve_path(self, query: DatasetQuery) -> Path:
        is_validation = False
        if query.provider_id is not None and "validation" in query.provider_id.lower():
            is_validation = True
        if query.source is not None and "validation" in query.source.lower():
            is_validation = True

        try:
            dataset_dir, manifest = self._registry.resolve(query.symbol, query.timeframe)
            return dataset_dir / manifest.file
        except FileNotFoundError:
            pass

        suffix = "-validation" if is_validation else ""
        candidates = [
            self.base_path / f"{query.symbol.lower()}-{query.timeframe.lower()}{suffix}.csv",
            self.base_path / f"{query.symbol.upper()}-{query.timeframe.upper()}{suffix}.csv",
            self.base_path / f"{query.symbol.lower()}-{query.timeframe.lower()}.csv",
            self.base_path / f"{query.symbol.upper()}-{query.timeframe.upper()}.csv",
            self.base_path / "sample.csv",
        ]

        for candidate in candidates:
            if candidate.exists():
                return candidate

        return candidates[0]

    @staticmethod
    def _parse_timestamp(value: str) -> datetime:
        normalized = value.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)
