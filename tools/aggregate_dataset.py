from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.data.providers.local_dataset_registry import DatasetManifest, LocalDatasetRegistry
from edge.data.services.timeframe_aggregation_service import TimeframeAggregationService


class AggregateDatasetTool:
    def __init__(self, registry_root: str | Path | None = None, output_root: str | Path | None = None) -> None:
        self.registry = LocalDatasetRegistry(base_path=registry_root or "data/datasets")
        self.output_root = Path(output_root or "data/datasets")

    def aggregate_dataset(self, *, symbol: str, version: str, target_timeframe: str) -> tuple[HistoricalDataset, Path, DatasetManifest]:
        dataset_dir, manifest = self.registry.resolve(symbol=symbol, timeframe="M1", version=version)
        dataset = self._load_dataset(dataset_dir)
        aggregated = TimeframeAggregationService().aggregate(dataset, target_timeframe)
        return self._write_output_dataset(symbol=symbol, target_timeframe=target_timeframe, version=version, dataset=aggregated)

    def _load_dataset(self, dataset_dir: Path) -> HistoricalDataset:
        bars_path = dataset_dir / "bars.csv"
        if not bars_path.exists():
            raise FileNotFoundError(f"Dataset bars file not found at {bars_path}")

        bars = []
        with bars_path.open("r", encoding="utf-8", newline="") as handle:
            for row in handle.read().splitlines()[1:]:
                if not row:
                    continue
                timestamp, open_str, high_str, low_str, close_str, volume_str = row.split(",")
                bars.append(
                    Bar(
                        timestamp=self._parse_timestamp(timestamp),
                        open=float(open_str),
                        high=float(high_str),
                        low=float(low_str),
                        close=float(close_str),
                        volume=float(volume_str),
                    )
                )

        return HistoricalDataset(
            metadata=DatasetMetadata(
                symbol=(dataset_dir.parent.parent.name or "").upper(),
                timeframe="M1",
                source="local-registry",
                timezone="UTC",
                asset_class="fx",
                exchange="",
                currency="",
            ),
            bars=tuple(bars),
        )

    def _write_output_dataset(
        self, *, symbol: str, target_timeframe: str, version: str, dataset: HistoricalDataset
    ) -> tuple[HistoricalDataset, Path, DatasetManifest]:
        dataset_dir = self.output_root / symbol.lower() / target_timeframe.lower() / version.lower()
        dataset_dir.mkdir(parents=True, exist_ok=True)

        payload = self._serialize_bars(dataset.bars)
        data_file = dataset_dir / "bars.csv"
        data_file.write_text(payload, encoding="utf-8")

        checksum = hashlib.sha256(data_file.read_bytes()).hexdigest()
        (dataset_dir / "checksum.sha256").write_text(checksum, encoding="utf-8")

        manifest = DatasetManifest(
            dataset_id=f"{symbol.lower()}-{target_timeframe.lower()}-{version.lower()}",
            symbol=dataset.metadata.symbol,
            timeframe=dataset.metadata.timeframe,
            version=version.lower(),
            source=dataset.metadata.source,
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

    @staticmethod
    def _serialize_bars(bars: tuple[Bar, ...]) -> str:
        output = ["timestamp,open,high,low,close,volume"]
        for bar in bars:
            output.append(
                ",".join(
                    [
                        AggregateDatasetTool._format_timestamp(bar.timestamp),
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
    def _parse_timestamp(value: str) -> datetime:
        normalized = value.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)

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
    parser = argparse.ArgumentParser(description="Aggregate an M1 local dataset into a higher timeframe and write a canonical output dataset")
    parser.add_argument("--symbol", required=True, help="Ticker symbol, e.g. XAUUSD or EURUSD")
    parser.add_argument("--version", required=True, help="Dataset version label to load from the registry")
    parser.add_argument("--target-timeframe", required=True, help="Target timeframe to generate, e.g. M15")
    parser.add_argument("--registry-root", default="data/datasets", help="Root directory containing the local dataset registry")
    parser.add_argument("--output-root", default="data/datasets", help="Root directory for the aggregated output dataset")
    args = parser.parse_args(argv)

    tool = AggregateDatasetTool(registry_root=args.registry_root, output_root=args.output_root)
    dataset, dataset_dir, manifest = tool.aggregate_dataset(
        symbol=args.symbol,
        version=args.version,
        target_timeframe=args.target_timeframe,
    )

    print(f"dataset={manifest.dataset_id}")
    print(f"bars={len(dataset.bars)}")
    print(f"dataset_dir={dataset_dir}")
    print(f"manifest={dataset_dir / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    main()
