from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from edge.data.dataset.historical_dataset import HistoricalDataset


@dataclass(frozen=True, slots=True)
class DatasetProvenance:
    """Traceability metadata for loaded datasets."""

    provider_id: str
    provider_version: str
    dataset_source: str
    retrieved_at: datetime
    requested_start: datetime | None = None
    requested_end: datetime | None = None
    dataset_start: datetime | None = None
    dataset_end: datetime | None = None
    normalization: str = "as_is"


@dataclass(frozen=True, slots=True)
class ProvenancedDataset:
    """Dataset plus provenance metadata used by research workflows."""

    dataset: HistoricalDataset
    provenance: DatasetProvenance
