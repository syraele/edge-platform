from __future__ import annotations

from abc import ABC, abstractmethod

from edge.data.dataset.historical_dataset import HistoricalDataset


class DatasetNormalizationPolicy(ABC):
    """Controlled normalization contract for provider datasets."""

    normalization_name: str = "custom"

    @abstractmethod
    def normalize(self, dataset: HistoricalDataset) -> HistoricalDataset:
        """Return a normalized dataset compatible with research execution."""


class AsIsNormalizationPolicy(DatasetNormalizationPolicy):
    """Leave provider output unchanged."""

    normalization_name = "as_is"

    def normalize(self, dataset: HistoricalDataset) -> HistoricalDataset:
        return dataset


class SortedDeduplicatedNormalizationPolicy(DatasetNormalizationPolicy):
    """Sort bars by timestamp and drop duplicate timestamps."""

    normalization_name = "sorted_deduplicated"

    def normalize(self, dataset: HistoricalDataset) -> HistoricalDataset:
        if dataset.is_empty:
            return dataset

        ordered = sorted(dataset.bars, key=lambda bar: bar.timestamp)
        deduplicated: dict[object, object] = {}

        for bar in ordered:
            deduplicated[bar.timestamp] = bar

        return HistoricalDataset(
            metadata=dataset.metadata,
            bars=tuple(deduplicated[timestamp] for timestamp in sorted(deduplicated)),
        )


def build_normalization_policy(name: str | None) -> DatasetNormalizationPolicy:
    if name in (None, "", "as_is"):
        return AsIsNormalizationPolicy()

    if name == "sorted_deduplicated":
        return SortedDeduplicatedNormalizationPolicy()

    raise ValueError(f"Unknown dataset normalization policy '{name}'")
