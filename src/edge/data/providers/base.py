from __future__ import annotations

from abc import ABC, abstractmethod

from edge.data.dataset.historical_dataset import HistoricalDataset

from .descriptor import DatasetProviderDescriptor
from .query import DatasetQuery


class DatasetProvider(ABC):
    """Architectural contract for dataset providers."""

    provider_id: str
    provider_version: str = "0.0.0"
    provider_name: str = "Dataset Provider"
    dataset_source: str = "unknown"
    supported_symbols: tuple[str, ...] = ()

    def describe(self) -> DatasetProviderDescriptor:
        return DatasetProviderDescriptor(
            provider_id=self.provider_id,
            provider_version=self.provider_version,
            provider_name=self.provider_name,
            dataset_source=self.dataset_source,
            supported_symbols=tuple(self.supported_symbols),
        )

    @abstractmethod
    def supports(self, query: DatasetQuery) -> bool:
        """Return True when provider can satisfy the query."""

    @abstractmethod
    def load(self, query: DatasetQuery) -> HistoricalDataset:
        """Load a historical dataset for the requested query."""
