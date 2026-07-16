from __future__ import annotations

from edge.data.providers import DatasetProviderLoader, DatasetProviderRegistry
from edge.data.validation import build_normalization_policy


class DatasetProviderComponent:
    """Application lifecycle component for dataset provider orchestration."""

    def __init__(
        self,
        registry: DatasetProviderRegistry,
        engine_config: dict | None = None,
    ) -> None:
        self._registry = registry
        self._engine_config = engine_config or {}
        self._loader = DatasetProviderLoader()

    def initialize(self) -> None:
        providers_cfg = self._engine_config.get("dataset_providers", {})
        enabled_providers = providers_cfg.get("enabled", [])
        normalization_policy_name = providers_cfg.get("normalization_policy")

        self._registry.set_normalization_policy(
            build_normalization_policy(normalization_policy_name)
        )

        for provider in self._loader.discover(enabled_providers):
            self._registry.register(provider)

    def start(self) -> None:
        # Provider lifecycle for PE-002 is registration-oriented.
        return None

    def stop(self) -> None:
        return None
