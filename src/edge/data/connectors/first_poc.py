from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.data.providers.local_dataset_registry import DatasetManifest


@dataclass(frozen=True, slots=True)
class ImportedDatasetArtifact:
    dataset: HistoricalDataset
    dataset_dir: Path
    manifest: DatasetManifest


class FirstDatasetConnectorProofOfConcept:
    """Isolated proof-of-concept connector that writes a registry-ready dataset artifact."""

    def __init__(self, output_root: str | Path | None = None) -> None:
        self.output_root = Path(output_root or "data/datasets")

    def import_from_source(
        self,
        *,
        symbol: str,
        timeframe: str,
        version: str,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> tuple[HistoricalDataset, Path, DatasetManifest]:
        url = self._build_yahoo_url(symbol, start=start, end=end)
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
        return self.import_dataset(
            symbol=symbol,
            timeframe=timeframe,
            version=version,
            source_name="yahoo-finance",
            raw_payload=body,
        )

    def import_dataset(
        self,
        *,
        symbol: str,
        timeframe: str,
        version: str,
        source_name: str,
        raw_payload: str,
    ) -> tuple[HistoricalDataset, Path, DatasetManifest]:
        normalized_payload = self._normalize_payload(raw_payload)
        bars = self._parse_bars(normalized_payload)
        dataset = HistoricalDataset(
            metadata=DatasetMetadata(
                symbol=symbol.upper(),
                timeframe=timeframe.upper(),
                source=source_name,
                timezone="UTC",
                asset_class="fx",
                exchange="",
                currency="",
            ),
            bars=tuple(bars),
        )

        dataset_dir = self.output_root / symbol.lower() / timeframe.lower() / version.lower()
        dataset_dir.mkdir(parents=True, exist_ok=True)

        data_file = dataset_dir / "bars.csv"
        data_file.write_text(normalized_payload, encoding="utf-8")

        checksum = hashlib.sha256(data_file.read_bytes()).hexdigest()
        checksum_path = dataset_dir / "checksum.sha256"
        checksum_path.write_text(checksum, encoding="utf-8")

        created_at = datetime.now(UTC).isoformat()
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
            created_at=created_at,
            checksum=checksum,
        )

        manifest_path = dataset_dir / "manifest.json"
        manifest_path.write_text(json.dumps(self._manifest_to_mapping(manifest), indent=2), encoding="utf-8")

        return dataset, dataset_dir, manifest

    @staticmethod
    def _build_yahoo_url(symbol: str, *, start: datetime | None = None, end: datetime | None = None) -> str:
        normalized = symbol.upper().strip()
        mapping = {
            "EURUSD": "EURUSD=X",
            "GBPUSD": "GBPUSD=X",
            "USDJPY": "USDJPY=X",
            "AUDUSD": "AUDUSD=X",
            "USDCAD": "USDCAD=X",
            "NZDUSD": "NZDUSD=X",
            "XAUUSD": "GC=F",
            "XAGUSD": "SI=F",
        }
        symbol_query = mapping.get(normalized, normalized)

        if start is not None and end is not None:
            start_ts = int(start.timestamp())
            end_ts = int(end.timestamp())
            return (
                f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol_query}"
                f"?interval=1d&period1={start_ts}&period2={end_ts}"
            )

        return f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol_query}?interval=1d&range=5d"

    @staticmethod
    def _normalize_payload(raw_payload: str) -> str:
        try:
            payload = json.loads(raw_payload)
        except json.JSONDecodeError:
            return raw_payload

        chart_result = payload.get("chart", {}).get("result", [])
        if not chart_result:
            raise ValueError("No chart result found in payload")

        result = chart_result[0]
        timestamps = result.get("timestamp", [])
        quote = result.get("indicators", {}).get("quote", [{}])[0]
        rows = []
        for idx, timestamp in enumerate(timestamps):
            rows.append(
                {
                    "timestamp": FirstDatasetConnectorProofOfConcept._format_timestamp(
                        datetime.fromtimestamp(int(timestamp), tz=UTC)
                    ),
                    "open": quote.get("open", [None])[idx],
                    "high": quote.get("high", [None])[idx],
                    "low": quote.get("low", [None])[idx],
                    "close": quote.get("close", [None])[idx],
                    "volume": quote.get("volume", [0.0])[idx],
                }
            )

        output = []
        output.append("timestamp,open,high,low,close,volume")
        for row in rows:
            output.append(
                ",".join(
                    [
                        row["timestamp"],
                        str(row["open"]),
                        str(row["high"]),
                        str(row["low"]),
                        str(row["close"]),
                        str(row["volume"]),
                    ]
                )
            )
        return "\n".join(output)

    @staticmethod
    def _parse_bars(raw_payload: str) -> list[Bar]:
        rows: list[Bar] = []
        reader = csv.DictReader(raw_payload.splitlines())
        for row in reader:
            timestamp = FirstDatasetConnectorProofOfConcept._parse_timestamp(row["timestamp"])
            rows.append(
                Bar(
                    timestamp=timestamp,
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row.get("volume", 0.0)),
                )
            )
        return rows

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
    parser = argparse.ArgumentParser(description="Import a historical dataset into the local registry")
    parser.add_argument("--symbol", required=True, help="Ticker symbol, e.g. XAUUSD or EURUSD")
    parser.add_argument("--timeframe", required=True, help="Timeframe, e.g. M1 or D1")
    parser.add_argument("--version", default="latest", help="Dataset version label")
    parser.add_argument("--from", dest="start", help="Inclusive start date (YYYY-MM-DD)")
    parser.add_argument("--to", dest="end", help="Inclusive end date (YYYY-MM-DD)")
    parser.add_argument("--output-root", default="data/datasets", help="Root directory for written datasets")
    args = parser.parse_args(argv)

    connector = FirstDatasetConnectorProofOfConcept(output_root=args.output_root)
    start_dt = _parse_datetime(args.start) if args.start else None
    end_dt = _parse_datetime(args.end) if args.end else None

    dataset, dataset_dir, manifest = connector.import_from_source(
        symbol=args.symbol,
        timeframe=args.timeframe,
        version=args.version,
        start=start_dt,
        end=end_dt,
    )

    print(f"dataset={manifest.dataset_id}")
    print(f"bars={len(dataset.bars)}")
    print(f"dataset_dir={dataset_dir}")
    print(f"manifest={dataset_dir / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
