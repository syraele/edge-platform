from __future__ import annotations

from abc import ABC, abstractmethod

from edge.data.dataset.historical_dataset import HistoricalDataset

from .query import DatasetQuery


class DatasetProvider(ABC):
    """Architectural contract for dataset providers."""

    provider_id: str
    provider_version: str = "0.0.0"

    @abstractmethod
    def supports(self, query: DatasetQuery) -> bool:
        """Return True when provider can satisfy the query."""

    @abstractmethod
    def load(self, query: DatasetQuery) -> HistoricalDataset:
        """Load a historical dataset for the requested query."""
