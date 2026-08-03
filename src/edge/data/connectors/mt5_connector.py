from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.data.providers.local_dataset_registry import DatasetManifest


@dataclass(frozen=True, slots=True)
class ImportedDatasetArtifact:
    dataset: HistoricalDataset
    dataset_dir: Path
    manifest: DatasetManifest


class Mt5DatasetConnector:
    """Connector that acquires M1 bars from MetaTrader5 and writes a canonical registry dataset."""

    def __init__(self, output_root: str | Path | None = None, mt5_module: Any | None = None) -> None:
        self.output_root = Path(output_root or "data/datasets")
        self._mt5_module = mt5_module

    def import_from_source(
        self,
        *,
        symbol: str,
        timeframe: str,
        version: str,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> tuple[HistoricalDataset, Path, DatasetManifest]:
        if timeframe.upper() != "M1":
            raise ValueError("Only M1 is supported by MT5Connector")

        if start is None or end is None:
            raise ValueError("MT5 connector requires both start and end timestamps")

        if start > end:
            raise ValueError("start date must be less than or equal to end date")

        mt5 = self._get_mt5_module()
        if not mt5.initialize():
            raise RuntimeError("MT5 connection failed: unable to initialize MetaTrader5")

        try:
            if not mt5.symbol_select(symbol, True):
                raise RuntimeError(f"MT5 symbol '{symbol}' does not exist or could not be selected")

            rates = mt5.copy_rates_range(symbol, 1, start, end)
            if rates is None:
                raise RuntimeError("MT5 connection failed: no response from MetaTrader5")
            if len(rates) == 0:
                raise RuntimeError("No MT5 historical data available for the requested range")

            bars = [
                Bar(
                    timestamp=self._coerce_timestamp(self._read_field_value(entry, "time")),
                    open=float(self._read_field_value(entry, "open") or 0.0),
                    high=float(self._read_field_value(entry, "high") or 0.0),
                    low=float(self._read_field_value(entry, "low") or 0.0),
                    close=float(self._read_field_value(entry, "close") or 0.0),
                    volume=float(
                        self._read_field_value(entry, "tick_volume")
                        if self._read_field_value(entry, "tick_volume") is not None
                        else self._read_field_value(entry, "volume")
                        or 0.0
                    ),
                )
                for entry in rates
            ]

            dataset = HistoricalDataset(
                metadata=DatasetMetadata(
                    symbol=symbol.upper(),
                    timeframe="M1",
                    source="mt5",
                    timezone="UTC",
                    asset_class="fx",
                    exchange="",
                    currency="",
                ),
                bars=tuple(bars),
            )

            return self.import_dataset(
                symbol=symbol,
                timeframe="M1",
                version=version,
                source_name="mt5",
                dataset=dataset,
            )
        finally:
            if hasattr(mt5, "shutdown"):
                mt5.shutdown()

    def import_dataset(
        self,
        *,
        symbol: str,
        timeframe: str,
        version: str,
        source_name: str,
        dataset: HistoricalDataset,
    ) -> tuple[HistoricalDataset, Path, DatasetManifest]:
        dataset_dir = self.output_root / symbol.lower() / timeframe.lower() / version.lower()
        dataset_dir.mkdir(parents=True, exist_ok=True)

        normalized_payload = self._serialize_bars(dataset.bars)
        data_file = dataset_dir / "bars.csv"
        data_file.write_text(normalized_payload, encoding="utf-8")

        checksum = hashlib.sha256(data_file.read_bytes()).hexdigest()
        (dataset_dir / "checksum.sha256").write_text(checksum, encoding="utf-8")

        manifest = DatasetManifest(
            dataset_id=f"{symbol.lower()}-{timeframe.lower()}-{version.lower()}",
            symbol=dataset.metadata.symbol,
            timeframe=dataset.metadata.timeframe,
            version=version.lower(),
            source=source_name,
            file="bars.csv",
            bars_count=len(dataset.bars),
            range_start=self._format_timestamp(dataset.first_bar.timestamp) if dataset.bars else None,
            range_end=self._format_timestamp(dataset.last_bar.timestamp) if dataset.bars else None,
            schema_version="1.0",
            created_at=datetime.now(UTC).isoformat(),
            checksum=checksum,
        )
        (dataset_dir / "manifest.json").write_text(json.dumps(self._manifest_to_mapping(manifest), indent=2), encoding="utf-8")
        return dataset, dataset_dir, manifest

    def _get_mt5_module(self) -> Any:
        if self._mt5_module is not None:
            return self._mt5_module
        try:
            import MetaTrader5 as mt5
        except ImportError as exc:
            raise RuntimeError("MetaTrader5 is not installed") from exc
        return mt5

    @staticmethod
    def _serialize_bars(bars: tuple[Bar, ...]) -> str:
        output = ["timestamp,open,high,low,close,volume"]
        for bar in bars:
            output.append(
                ",".join(
                    [
                        Mt5DatasetConnector._format_timestamp(bar.timestamp),
                        str(bar.open),
                        str(bar.high),
                        str(bar.low),
                        str(bar.close),
                        str(bar.volume),
                    ]
                )
            )
        return "\n".join(output)

    @staticmethod
    def _read_field_value(entry: Any, field: str) -> Any:
        if hasattr(entry, "get"):
            return entry.get(field)
        if hasattr(entry, field):
            return getattr(entry, field)
        if isinstance(entry, (list, tuple)):
            mapping = {
                "time": 0,
                "open": 1,
                "high": 2,
                "low": 3,
                "close": 4,
                "tick_volume": 5,
                "volume": 5,
            }
            index = mapping.get(field)
            if index is not None and index < len(entry):
                return entry[index]
        if hasattr(entry, "tolist"):
            values = entry.tolist()
            if isinstance(values, (list, tuple)):
                mapping = {
                    "time": 0,
                    "open": 1,
                    "high": 2,
                    "low": 3,
                    "close": 4,
                    "tick_volume": 5,
                    "volume": 5,
                }
                index = mapping.get(field)
                if index is not None and index < len(values):
                    return values[index]
        return None

    @staticmethod
    def _coerce_timestamp(value: Any) -> datetime:
        if isinstance(value, datetime):
            if value.tzinfo is None:
                return value.replace(tzinfo=UTC)
            return value
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(float(value), tz=UTC)
        return datetime.fromisoformat(str(value)).replace(tzinfo=UTC)

    @staticmethod
    def _format_timestamp(value: datetime) -> str:
        return value.astimezone(UTC).isoformat()

    @staticmethod
    def _manifest_to_mapping(manifest: DatasetManifest) -> dict[str, Any]:
        return {
            "dataset_id": manifest.dataset_id,
            "symbol": manifest.symbol,
            "timeframe": manifest.timeframe,
            "version": manifest.version,
            "source": manifest.source,
            "file": manifest.file,
            "bars_count": manifest.bars_count,
            "range_start": manifest.range_start,
            "range_end": manifest.range_end,
            "schema_version": manifest.schema_version,
            "created_at": manifest.created_at,
            "checksum": manifest.checksum,
        }


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=UTC)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Import a historical dataset from MT5 into the local registry")
    parser.add_argument("--symbol", required=True, help="Ticker symbol, e.g. EURUSD or XAUUSD")
    parser.add_argument("--from", dest="start", required=True, help="Inclusive start date (YYYY-MM-DD)")
    parser.add_argument("--to", dest="end", required=True, help="Inclusive end date (YYYY-MM-DD)")
    parser.add_argument("--version", default="latest", help="Dataset version label")
    parser.add_argument("--timeframe", default="M1", help="Timeframe to import (currently only M1 is supported)")
    parser.add_argument("--output-root", default="data/datasets", help="Root directory for written datasets")
    args = parser.parse_args(argv)

    connector = Mt5DatasetConnector(output_root=args.output_root)
    dataset, dataset_dir, manifest = connector.import_from_source(
        symbol=args.symbol,
        timeframe=args.timeframe,
        version=args.version,
        start=_parse_datetime(args.start),
        end=_parse_datetime(args.end),
    )
    print(f"dataset={manifest.dataset_id}")
    print(f"bars={len(dataset.bars)}")
    print(f"dataset_dir={dataset_dir}")
    print(f"manifest={dataset_dir / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    main()
