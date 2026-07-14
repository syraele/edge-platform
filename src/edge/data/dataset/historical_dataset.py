"""
EDGE_ENGINE

Historical Dataset
"""

from dataclasses import dataclass
from typing import Tuple

from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata


@dataclass(frozen=True, slots=True)
class HistoricalDataset:
    """
    Immutable historical market dataset.
    """

    metadata: DatasetMetadata

    bars: Tuple[Bar, ...]

    @property
    def size(self) -> int:
        return len(self.bars)

    @property
    def is_empty(self) -> bool:
        return self.size == 0

    @property
    def first_bar(self) -> Bar:
        return self.bars[0]

    @property
    def last_bar(self) -> Bar:
        return self.bars[-1]