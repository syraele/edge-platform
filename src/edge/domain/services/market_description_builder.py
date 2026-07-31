"""
EDGE_ENGINE

Market Description Builder
"""

from __future__ import annotations

from datetime import UTC, datetime

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.domain.descriptor_metadata import DescriptorMetadata
from edge.domain.market_description import MarketDescription
from edge.domain.market_descriptor import MarketDescriptor


class MarketDescriptionBuilder:
    """
    Domain Service responsible for transforming a HistoricalDataset
    into a MarketDescription.

    The builder derives objective market descriptors from the
    available bars so downstream discovery can reason over
    market context rather than raw data alone.
    """

    VERSION = "1.0"

    def build(self, dataset: HistoricalDataset) -> MarketDescription:
        """
        Build a MarketDescription from a HistoricalDataset.
        """
        descriptors = self._build_descriptors(dataset)

        metadata = DescriptorMetadata(
            created_at=datetime.now(UTC),
            builder_version=self.VERSION,
            description_type="objective_market_context",
        )

        return MarketDescription(
            dataset=dataset,
            metadata=metadata,
            descriptors=tuple(descriptors),
        )

    def _build_descriptors(self, dataset: HistoricalDataset) -> list[MarketDescriptor]:
        bars = dataset.bars
        if not bars:
            return []

        ranges = [bar.high - bar.low for bar in bars]
        body_sizes = [abs(bar.close - bar.open) for bar in bars]
        close_changes = [
            (bars[index].close - bars[index - 1].close) / bars[index - 1].close
            if index > 0 and bars[index - 1].close != 0.0
            else 0.0
            for index in range(len(bars))
        ]

        descriptors: list[MarketDescriptor] = [
            MarketDescriptor(
                name="bar_count",
                value=float(len(bars)),
                unit="bars",
                description="Total number of bars in the dataset.",
            ),
            MarketDescriptor(
                name="average_range",
                value=sum(ranges) / len(ranges) if ranges else 0.0,
                unit="price",
                description="Average bar range across the dataset.",
            ),
            MarketDescriptor(
                name="average_body_size",
                value=sum(body_sizes) / len(body_sizes) if body_sizes else 0.0,
                unit="price",
                description="Average candle body size across the dataset.",
            ),
            MarketDescriptor(
                name="average_close_change",
                value=sum(close_changes) / len(close_changes) if close_changes else 0.0,
                unit="return",
                description="Average close-to-close return across the dataset.",
            ),
            MarketDescriptor(
                name="volatility_score",
                value=(sum(ranges) / len(ranges) if ranges else 0.0) / max(1.0, abs(bars[-1].close - bars[0].close)),
                unit="ratio",
                description="Relative volatility score based on average range and total price displacement.",
            ),
        ]

        return descriptors