"""
EDGE_ENGINE

Market Description
"""

from dataclasses import dataclass
from typing import Tuple

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.domain.descriptor_metadata import DescriptorMetadata
from edge.domain.market_descriptor import MarketDescriptor


@dataclass(frozen=True, slots=True)
class MarketDescription:
    """
    Immutable description of market behaviour extracted
    from a HistoricalDataset.

    A MarketDescription always refers to exactly one
    HistoricalDataset and contains a collection of
    immutable MarketDescriptors.
    """

    dataset: HistoricalDataset

    metadata: DescriptorMetadata

    descriptors: Tuple[MarketDescriptor, ...]

    @property
    def size(self) -> int:
        """Return the number of descriptors."""
        return len(self.descriptors)

    @property
    def is_empty(self) -> bool:
        """Return True when no descriptors are present."""
        return self.size == 0