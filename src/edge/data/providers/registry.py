from __future__ import annotations

from datetime import UTC, datetime

from edge.data.validation import AsIsNormalizationPolicy, DatasetNormalizationPolicy

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


class DatasetProviderLoadError(DatasetProviderError):
    """Raised when dataset loading fails across provider attempts."""


class DatasetProviderRegistry:
    """Registry and resolver for advanced dataset providers."""

    def __init__(
        self,
        normalization_policy: DatasetNormalizationPolicy | None = None,
    ) -> None:
        self._providers: dict[str, DatasetProvider] = {}
        self._normalization_policy = normalization_policy or AsIsNormalizationPolicy()

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
        self._validate_query(query)
        provider = self.resolve(query)
        return self._load_from_provider(provider, query)

    def load_with_fallback(
        self,
        query: DatasetQuery,
        fallback_provider_ids: list[str] | None = None,
    ) -> ProvenancedDataset:
        self._validate_query(query)
        candidate_provider_ids: list[str] = []

        if query.provider_id:
            candidate_provider_ids.append(query.provider_id)
        else:
            for provider_id in self.list_providers():
                provider = self._providers[provider_id]
                if provider.supports(query):
                    candidate_provider_ids.append(provider_id)

        for provider_id in fallback_provider_ids or []:
            if provider_id not in candidate_provider_ids:
                candidate_provider_ids.append(provider_id)

        if not candidate_provider_ids:
            raise DatasetProviderNotFoundError(
                f"No dataset provider available for {query.symbol}/{query.timeframe}"
            )

        last_error: Exception | None = None
        attempted: list[str] = []

        for provider_id in candidate_provider_ids:
            provider = self.get(provider_id)

            if not provider.supports(query):
                continue

            attempted.append(provider_id)

            try:
                return self._load_from_provider(provider, query)
            except Exception as exc:  # noqa: BLE001 - fallback requires broad capture.
                last_error = exc

        if not attempted:
            raise DatasetProviderNotFoundError(
                f"No compatible dataset provider available for {query.symbol}/{query.timeframe}"
            )

        raise DatasetProviderLoadError(
            f"All provider attempts failed for {query.symbol}/{query.timeframe}: {attempted}"
        ) from last_error

    def _load_from_provider(
        self,
        provider: DatasetProvider,
        query: DatasetQuery,
    ) -> ProvenancedDataset:
        dataset = provider.load(query)
        dataset = self._normalization_policy.normalize(dataset)

        self._validate_dataset_compatibility(dataset, query)

        dataset_start = None
        dataset_end = None
        if not dataset.is_empty:
            dataset_start = dataset.first_bar.timestamp
            dataset_end = dataset.last_bar.timestamp

        provenance = DatasetProvenance(
            provider_id=provider.provider_id,
            provider_version=getattr(provider, "provider_version", "0.0.0"),
            dataset_source=query.source or dataset.metadata.source,
            retrieved_at=datetime.now(UTC),
            requested_start=query.start,
            requested_end=query.end,
            dataset_start=dataset_start,
            dataset_end=dataset_end,
            normalization=self._normalization_policy.normalization_name,
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

        if not dataset.is_empty:
            first_timestamp = dataset.first_bar.timestamp
            last_timestamp = dataset.last_bar.timestamp

            if query.start is not None and first_timestamp < query.start:
                raise DatasetProviderCompatibilityError(
                    "Dataset starts before requested start time"
                )

            if query.end is not None and last_timestamp > query.end:
                raise DatasetProviderCompatibilityError(
                    "Dataset ends after requested end time"
                )

    @staticmethod
    def _validate_query(query: DatasetQuery) -> None:
        if query.start is not None and query.end is not None and query.start > query.end:
            raise DatasetProviderCompatibilityError(
                "Dataset query start time must not be after end time"
            )

    @staticmethod
    def _validate_provider(provider: DatasetProvider) -> str:
        provider_id = getattr(provider, "provider_id", None)

        if not isinstance(provider_id, str) or not provider_id.strip():
            raise DatasetProviderValidationError(
                "Dataset provider must declare a non-empty provider_id"
            )

        return provider_id.strip()
