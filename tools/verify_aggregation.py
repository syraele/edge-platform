from __future__ import annotations

import csv
from datetime import UTC, datetime, timedelta
from pathlib import Path

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.data.providers.local_dataset_registry import LocalDatasetRegistry
from edge.data.services.timeframe_aggregation_service import TimeframeAggregationService


REPO_ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = REPO_ROOT / "tmp-cli-demo" / "xauusd" / "m1" / "xauusd-m1-jul2026"


def load_real_dataset() -> HistoricalDataset:
    registry = LocalDatasetRegistry(base_path=REPO_ROOT / "tmp-cli-demo")
    dataset_dir, manifest = registry.resolve("XAUUSD", "M1", "xauusd-m1-jul2026")

    bars: list[Bar] = []
    with (dataset_dir / manifest.file).open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            timestamp = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=UTC)
            bars.append(
                Bar(
                    timestamp=timestamp.astimezone(UTC),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row.get("volume", 0.0)),
                )
            )

    return HistoricalDataset(
        metadata=DatasetMetadata(
            symbol="XAUUSD",
            timeframe="M1",
            source="mt5",
            timezone="UTC",
            asset_class="fx",
            exchange="",
            currency="",
        ),
        bars=tuple(bars),
    )


def build_expected_m15_bar(bars: list[Bar]) -> Bar:
    first = bars[0]
    last = bars[-1]
    return Bar(
        timestamp=first.timestamp,
        open=first.open,
        high=max(item.high for item in bars),
        low=min(item.low for item in bars),
        close=last.close,
        volume=sum(item.volume for item in bars),
    )


def bucket_start(timestamp: datetime, target_timeframe: str) -> datetime:
    dt = timestamp.astimezone(UTC)
    if target_timeframe == "M15":
        minute = (dt.minute // 15) * 15
        return dt.replace(minute=minute, second=0, microsecond=0)
    raise ValueError(f"Unsupported timeframe {target_timeframe}")


def build_buckets(bars: list[Bar], target_timeframe: str) -> list[list[Bar]]:
    buckets: list[list[Bar]] = []
    current_bucket: list[Bar] = []
    current_key: datetime | None = None

    for bar in bars:
        key = bucket_start(bar.timestamp, target_timeframe)
        if current_key is None:
            current_key = key
            current_bucket = [bar]
            continue

        if key == current_key:
            current_bucket.append(bar)
        else:
            buckets.append(current_bucket)
            current_key = key
            current_bucket = [bar]

    if current_bucket:
        buckets.append(current_bucket)

    return buckets


def find_bucket_for_window(bars: list[Bar], start_time: datetime, end_time: datetime) -> list[Bar]:
    return [bar for bar in bars if start_time <= bar.timestamp <= end_time]


def main() -> None:
    dataset = load_real_dataset()
    service = TimeframeAggregationService()
    aggregated = service.aggregate(dataset, "M15")

    if len(aggregated.bars) < 2:
        print("Not enough aggregated bars to inspect the second M15 bar")
        return

    target_bar = aggregated.bars[1]
    bucket_start_ts = target_bar.timestamp
    bucket_end_ts = bucket_start_ts + timedelta(minutes=14)
    bucket_bars = find_bucket_for_window(list(dataset.bars), bucket_start_ts, bucket_end_ts)

    expected_bucket = build_expected_m15_bar(bucket_bars)
    actual = target_bar

    print("Seconda barra M15 prodotta")
    print(actual.timestamp)
    print("Indice della barra M15 nel dataset aggregato")
    print(1)
    print("Timestamp inizio intervallo")
    print(bucket_start_ts)
    print("Timestamp fine intervallo")
    print(bucket_end_ts)
    print("Numero barre M1 nell'intervallo")
    print(len(bucket_bars))
    print("Timestamp delle barre M1 nell'intervallo")
    for bar in bucket_bars:
        print(bar.timestamp)
    print("Elenco barre M1 nell'intervallo")
    for bar in bucket_bars:
        print(bar)

    print("\nOpen atteso")
    print(expected_bucket.open)
    print("Open ottenuto")
    print(actual.open)

    print("\nHigh atteso")
    print(expected_bucket.high)
    print("High ottenuto")
    print(actual.high)

    print("\nLow atteso")
    print(expected_bucket.low)
    print("Low ottenuto")
    print(actual.low)

    print("\nClose atteso")
    print(expected_bucket.close)
    print("Close ottenuto")
    print(actual.close)

    print("\nVolume atteso")
    print(expected_bucket.volume)
    print("Volume ottenuto")
    print(actual.volume)

    comparable = (
        expected_bucket.open == actual.open
        and expected_bucket.high == actual.high
        and expected_bucket.low == actual.low
        and expected_bucket.close == actual.close
        and expected_bucket.volume == actual.volume
    )
    print("\nRESULT: PASS" if comparable else "\nRESULT: FAIL")


if __name__ == "__main__":
    main()
