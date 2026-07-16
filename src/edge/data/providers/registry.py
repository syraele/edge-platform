from __future__ import annotations

from datetime import UTC, datetime

from .base import DatasetProvider
from .provenance import DatasetProvenance, ProvenancedDataset
from .query import DatasetQuery


class DatasetProviderError(RuntimeError):
    """Base error for dataset provider orchestration."""


class DatasetProviderValidationError(DatasetProviderError, ValueError):
    """Raised when provider registration fails validation."""


class DatasetProviderNotFoundError(DatasetProviderError, LookupError):
    """Raised when no compatible provider can satisfy a query."""


class DatasetProviderCompatibilityError(DatasetProviderError, ValueError):
    """Raised when returned dataset is incompatible with requested query."""


class DatasetProviderRegistry:
    """Registry and resolver for advanced dataset providers."""

    def __init__(self) -> None:
        self._providers: dict[str, DatasetProvider] = {}

    def register(self, provider: DatasetProvider) -> None:
        provider_id = self._validate_provider(provider)

        if provider_id in self._providers:
            raise DatasetProviderValidationError(
                f"Dataset provider '{provider_id}' is already registered"
            )

        self._providers[provider_id] = provider

    def list_providers(self) -> list[str]:
        return sorted(self._providers.keys())

    def get(self, provider_id: str) -> DatasetProvider:
        provider = self._providers.get(provider_id)

        if provider is None:
            raise DatasetProviderNotFoundError(
                f"Dataset provider '{provider_id}' is not registered"
            )

        return provider

    def resolve(self, query: DatasetQuery) -> DatasetProvider:
        if query.provider_id:
            provider = self.get(query.provider_id)

            if provider.supports(query):
                return provider

            raise DatasetProviderNotFoundError(
                f"Dataset provider '{query.provider_id}' does not support "
                f"{query.symbol}/{query.timeframe}"
            )

        for provider_id in self.list_providers():
            provider = self._providers[provider_id]

            if provider.supports(query):
                return provider

        raise DatasetProviderNotFoundError(
            f"No dataset provider available for {query.symbol}/{query.timeframe}"
        )

    def load(self, query: DatasetQuery) -> ProvenancedDataset:
        provider = self.resolve(query)
        dataset = provider.load(query)

        self._validate_dataset_compatibility(dataset, query)

        provenance = DatasetProvenance(
            provider_id=provider.provider_id,
            provider_version=getattr(provider, "provider_version", "0.0.0"),
            dataset_source=query.source or dataset.metadata.source,
            retrieved_at=datetime.now(UTC),
            normalization="as_is",
        )

        return ProvenancedDataset(dataset=dataset, provenance=provenance)

    @staticmethod
    def _validate_dataset_compatibility(dataset, query: DatasetQuery) -> None:
        if dataset.metadata.symbol != query.symbol:
            raise DatasetProviderCompatibilityError(
                "Dataset symbol does not match query symbol"
            )

        if dataset.metadata.timeframe != query.timeframe:
            raise DatasetProviderCompatibilityError(
                "Dataset timeframe does not match query timeframe"
            )

    @staticmethod
    def _validate_provider(provider: DatasetProvider) -> str:
        provider_id = getattr(provider, "provider_id", None)

        if not isinstance(provider_id, str) or not provider_id.strip():
            raise DatasetProviderValidationError(
                "Dataset provider must declare a non-empty provider_id"
            )

        return provider_id.strip()
