from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DatasetProviderDescriptor:
    """Runtime metadata describing a dataset provider."""

    provider_id: str
    provider_version: str
    provider_name: str
    dataset_source: str
    supported_symbols: tuple[str, ...]
