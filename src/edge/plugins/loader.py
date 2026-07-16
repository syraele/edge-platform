from __future__ import annotations

import importlib
from typing import Any

from .base import EdgePlugin


class PluginDiscoveryError(ValueError):
    """Raised when a plugin spec cannot be discovered or instantiated."""


class PluginLoader:
    """Discover plugin instances from declarative entrypoint specs."""

    def discover(self, plugin_specs: list[dict[str, Any]] | None) -> list[EdgePlugin]:
        if not plugin_specs:
            return []

        return [self.load(spec) for spec in plugin_specs]

    def load(self, plugin_spec: dict[str, Any]) -> EdgePlugin:
        entrypoint = plugin_spec.get("entrypoint")

        if not isinstance(entrypoint, str) or ":" not in entrypoint:
            raise PluginDiscoveryError(
                "Plugin entrypoint must be in 'module.path:ClassName' format"
            )

        module_name, class_name = entrypoint.split(":", maxsplit=1)

        try:
            module = importlib.import_module(module_name)
            plugin_cls = getattr(module, class_name)
        except (ImportError, AttributeError) as exc:
            raise PluginDiscoveryError(
                f"Unable to load plugin entrypoint '{entrypoint}'"
            ) from exc

        if not isinstance(plugin_cls, type) or not issubclass(plugin_cls, EdgePlugin):
            raise PluginDiscoveryError(
                f"Entrypoint '{entrypoint}' must reference an EdgePlugin subclass"
            )

        try:
            plugin = plugin_cls()
        except Exception as exc:
            raise PluginDiscoveryError(
                f"Failed to instantiate plugin from '{entrypoint}'"
            ) from exc

        requested_id = plugin_spec.get("id")
        if requested_id and requested_id != plugin.plugin_id:
            raise PluginDiscoveryError(
                f"Plugin id mismatch: expected '{requested_id}', got '{plugin.plugin_id}'"
            )

        return plugin
