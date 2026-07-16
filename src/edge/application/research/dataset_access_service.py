from __future__ import annotations

from datetime import datetime

from edge.data import DatasetProviderRegistry, DatasetQuery


class DatasetAccessService:
    """Application-facing service for requesting provenanced datasets."""

    def __init__(self, registry: DatasetProviderRegistry) -> None:
        self._registry = registry

    def request_dataset(
        self,
        *,
        symbol: str,
        timeframe: str,
        start: datetime | None = None,
        end: datetime | None = None,
        source: str | None = None,
        provider_id: str | None = None,
        fallback_provider_ids: list[str] | None = None,
    ):
        query = DatasetQuery(
            symbol=symbol,
            timeframe=timeframe,
            start=start,
            end=end,
            source=source,
            provider_id=provider_id,
        )

        if fallback_provider_ids:
            return self._registry.load_with_fallback(
                query,
                fallback_provider_ids=fallback_provider_ids,
            )

        return self._registry.load(query)
