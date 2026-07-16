from __future__ import annotations

import importlib
from typing import Any

from .base import DatasetProvider


class DatasetProviderDiscoveryError(ValueError):
    """Raised when a dataset provider spec cannot be loaded."""


class DatasetProviderLoader:
    """Discover dataset providers from declarative entrypoint specs."""

    def discover(
        self,
        provider_specs: list[dict[str, Any]] | None,
    ) -> list[DatasetProvider]:
        if not provider_specs:
            return []

        return [self.load(spec) for spec in provider_specs]

    def load(self, provider_spec: dict[str, Any]) -> DatasetProvider:
        entrypoint = provider_spec.get("entrypoint")

        if not isinstance(entrypoint, str) or ":" not in entrypoint:
            raise DatasetProviderDiscoveryError(
                "Provider entrypoint must be in 'module.path:ClassName' format"
            )

        module_name, class_name = entrypoint.split(":", maxsplit=1)

        try:
            module = importlib.import_module(module_name)
            provider_cls = getattr(module, class_name)
        except (ImportError, AttributeError) as exc:
            raise DatasetProviderDiscoveryError(
                f"Unable to load provider entrypoint '{entrypoint}'"
            ) from exc

        if not isinstance(provider_cls, type) or not issubclass(
            provider_cls,
            DatasetProvider,
        ):
            raise DatasetProviderDiscoveryError(
                f"Entrypoint '{entrypoint}' must reference a DatasetProvider subclass"
            )

        try:
            provider = provider_cls()
        except Exception as exc:
            raise DatasetProviderDiscoveryError(
                f"Failed to instantiate provider from '{entrypoint}'"
            ) from exc

        requested_id = provider_spec.get("id")
        if requested_id and requested_id != provider.provider_id:
            raise DatasetProviderDiscoveryError(
                f"Provider id mismatch: expected '{requested_id}', got '{provider.provider_id}'"
            )

        return provider
