import csv
from datetime import UTC, datetime
from pathlib import Path

import pytest

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.data.providers.local_dataset_registry import LocalDatasetRegistry
from edge.data.services.timeframe_aggregation_service import TimeframeAggregationService


REPO_ROOT = Path(__file__).resolve().parents[2]
REAL_DATASET_ROOT = REPO_ROOT / "tmp-cli-demo" / "xauusd" / "m1" / "xauusd-m1-jul2026"


def _load_real_registry_dataset() -> HistoricalDataset:
    assert REAL_DATASET_ROOT.exists(), f"Real MT5 dataset not found at {REAL_DATASET_ROOT}"

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


def _bucketed_bars(bars: list[Bar], target_timeframe: str) -> list[tuple[datetime, list[Bar]]]:
    buckets: list[tuple[datetime, list[Bar]]] = []
    current_bucket: list[Bar] | None = None
    current_key: datetime | None = None
    for bar in bars:
        key = _bucket_start(bar.timestamp, target_timeframe)
        if current_bucket is None or current_key != key:
            if current_bucket is not None:
                buckets.append((current_key, current_bucket))
            current_bucket = [bar]
            current_key = key
        else:
            current_bucket.append(bar)
    if current_bucket is not None:
        buckets.append((current_key, current_bucket))
    return buckets


def _bucket_start(timestamp: datetime, target_timeframe: str) -> datetime:
    dt = timestamp.astimezone(UTC)
    if target_timeframe == "M15":
        minute = (dt.minute // 15) * 15
        return dt.replace(minute=minute, second=0, microsecond=0)
    if target_timeframe == "H1":
        return dt.replace(minute=0, second=0, microsecond=0)
    raise ValueError(f"Unsupported timeframe {target_timeframe}")


def _expected_bar_from_bucket(bucket_bars: list[Bar], target_timeframe: str) -> Bar:
    first = bucket_bars[0]
    last = bucket_bars[-1]
    return Bar(
        timestamp=_bucket_start(first.timestamp, target_timeframe),
        open=first.open,
        high=max(item.high for item in bucket_bars),
        low=min(item.low for item in bucket_bars),
        close=last.close,
        volume=sum(item.volume for item in bucket_bars),
    )


def _assert_bar_matches(actual: Bar, expected: Bar) -> None:
    assert actual.timestamp == expected.timestamp
    assert actual.open == pytest.approx(expected.open)
    assert actual.high == pytest.approx(expected.high)
    assert actual.low == pytest.approx(expected.low)
    assert actual.close == pytest.approx(expected.close)
    assert actual.volume == pytest.approx(expected.volume)


def test_aggregates_real_mt5_dataset_to_m15_and_h1() -> None:
    dataset = _load_real_registry_dataset()
    service = TimeframeAggregationService()

    for target_timeframe in ("M15", "H1"):
        aggregated = service.aggregate(dataset, target_timeframe)

        buckets = _bucketed_bars(list(dataset.bars), target_timeframe)
        assert len(aggregated.bars) == len(buckets)

        first_bucket = buckets[0][1]
        first_expected = _expected_bar_from_bucket(first_bucket, target_timeframe)
        _assert_bar_matches(aggregated.bars[0], first_expected)

        midpoint_index = len(buckets) // 2
        midpoint_bucket = buckets[midpoint_index][1]
        midpoint_expected = _expected_bar_from_bucket(midpoint_bucket, target_timeframe)
        _assert_bar_matches(aggregated.bars[midpoint_index], midpoint_expected)

        last_bucket = buckets[-1][1]
        last_expected = _expected_bar_from_bucket(last_bucket, target_timeframe)
        _assert_bar_matches(aggregated.bars[-1], last_expected)


def test_aggregates_m1_to_m5() -> None:
    service = TimeframeAggregationService()
    dataset = HistoricalDataset(
        metadata=DatasetMetadata(symbol="EURUSD", timeframe="M1", source="sample"),
        bars=(
            Bar(timestamp=datetime(2024, 1, 1, 0, 0, tzinfo=UTC), open=1.0, high=1.1, low=0.9, close=1.05, volume=10.0),
            Bar(timestamp=datetime(2024, 1, 1, 0, 1, tzinfo=UTC), open=1.05, high=1.2, low=0.95, close=1.1, volume=20.0),
            Bar(timestamp=datetime(2024, 1, 1, 0, 2, tzinfo=UTC), open=1.1, high=1.3, low=1.0, close=1.2, volume=30.0),
            Bar(timestamp=datetime(2024, 1, 1, 0, 3, tzinfo=UTC), open=1.2, high=1.4, low=1.1, close=1.3, volume=40.0),
        ),
    )

    aggregated = service.aggregate(dataset, "M5")

    assert aggregated.metadata.timeframe == "M5"
    assert len(aggregated.bars) == 1
    assert aggregated.bars[0].timestamp == datetime(2024, 1, 1, 0, 0, tzinfo=UTC)
    assert aggregated.bars[0].open == 1.0
    assert aggregated.bars[0].high == 1.4
    assert aggregated.bars[0].low == 0.9
    assert aggregated.bars[0].close == 1.3
    assert aggregated.bars[0].volume == 100.0


def test_aggregates_m1_to_h1() -> None:
    service = TimeframeAggregationService()
    dataset = HistoricalDataset(
        metadata=DatasetMetadata(symbol="EURUSD", timeframe="M1", source="sample"),
        bars=(
            Bar(timestamp=datetime(2024, 1, 1, 0, 0, tzinfo=UTC), open=1.0, high=1.1, low=0.9, close=1.05, volume=10.0),
            Bar(timestamp=datetime(2024, 1, 1, 0, 30, tzinfo=UTC), open=1.05, high=1.2, low=0.95, close=1.1, volume=20.0),
            Bar(timestamp=datetime(2024, 1, 1, 1, 0, tzinfo=UTC), open=1.1, high=1.3, low=1.0, close=1.2, volume=30.0),
        ),
    )

    aggregated = service.aggregate(dataset, "H1")

    assert aggregated.metadata.timeframe == "H1"
    assert len(aggregated.bars) == 2
    assert aggregated.bars[0].timestamp == datetime(2024, 1, 1, 0, 0, tzinfo=UTC)
    assert aggregated.bars[1].timestamp == datetime(2024, 1, 1, 1, 0, tzinfo=UTC)
