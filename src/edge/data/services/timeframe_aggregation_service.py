from __future__ import annotations

from datetime import UTC, datetime
from typing import Iterable

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata


class TimeframeAggregationService:
    """Aggregate a lower-granularity dataset into coarser timeframes deterministically."""

    supported_timeframes = {"M5", "M15", "M30", "H1", "H4", "D1"}

    def aggregate(self, dataset: HistoricalDataset, target_timeframe: str) -> HistoricalDataset:
        normalized = target_timeframe.upper()
        if normalized not in self.supported_timeframes:
            raise ValueError(f"Unsupported target timeframe '{target_timeframe}'")

        if dataset.is_empty:
            return HistoricalDataset(
                metadata=DatasetMetadata(
                    symbol=dataset.metadata.symbol,
                    timeframe=normalized,
                    source=dataset.metadata.source,
                ),
                bars=tuple(),
            )

        bars = self._aggregate_bars(dataset.bars, normalized)
        return HistoricalDataset(
            metadata=DatasetMetadata(
                symbol=dataset.metadata.symbol,
                timeframe=normalized,
                source=dataset.metadata.source,
                timezone=dataset.metadata.timezone,
                asset_class=dataset.metadata.asset_class,
                exchange=dataset.metadata.exchange,
                currency=dataset.metadata.currency,
            ),
            bars=tuple(bars),
        )

    def _aggregate_bars(self, bars: Iterable[Bar], target_timeframe: str) -> list[Bar]:
        bucketed: list[list[Bar]] = []
        current_bucket: list[Bar] | None = None
        for bar in bars:
            if current_bucket is None:
                current_bucket = [bar]
                continue

            if self._same_bucket(current_bucket[-1].timestamp, bar.timestamp, target_timeframe):
                current_bucket.append(bar)
            else:
                bucketed.append(current_bucket)
                current_bucket = [bar]

        if current_bucket is not None:
            bucketed.append(current_bucket)

        aggregated: list[Bar] = []
        for bucket in bucketed:
            if not bucket:
                continue
            first = bucket[0]
            last = bucket[-1]
            aggregated.append(
                Bar(
                    timestamp=self._bucket_start(first.timestamp, target_timeframe),
                    open=first.open,
                    high=max(item.high for item in bucket),
                    low=min(item.low for item in bucket),
                    close=last.close,
                    volume=sum(item.volume for item in bucket),
                )
            )
        return aggregated

    @staticmethod
    def _same_bucket(left: datetime, right: datetime, target_timeframe: str) -> bool:
        left_bucket = TimeframeAggregationService._bucket_start(left, target_timeframe)
        right_bucket = TimeframeAggregationService._bucket_start(right, target_timeframe)
        return left_bucket == right_bucket

    @staticmethod
    def _bucket_start(timestamp: datetime, target_timeframe: str) -> datetime:
        normalized = target_timeframe.upper()
        dt = timestamp.astimezone(UTC)
        if normalized == "M5":
            minute = (dt.minute // 5) * 5
            return dt.replace(minute=minute, second=0, microsecond=0)
        if normalized == "M15":
            minute = (dt.minute // 15) * 15
            return dt.replace(minute=minute, second=0, microsecond=0)
        if normalized == "M30":
            minute = (dt.minute // 30) * 30
            return dt.replace(minute=minute, second=0, microsecond=0)
        if normalized == "H1":
            return dt.replace(minute=0, second=0, microsecond=0)
        if normalized == "H4":
            hour = (dt.hour // 4) * 4
            return dt.replace(hour=hour, minute=0, second=0, microsecond=0)
        if normalized == "D1":
            return dt.replace(hour=0, minute=0, second=0, microsecond=0)
        raise ValueError(f"Unsupported target timeframe '{target_timeframe}'")
