from __future__ import annotations

from typing import Any

from .base import EdgePlugin


class PluginValidationError(ValueError):
    """Raised when a plugin does not satisfy contract requirements."""


class PluginNotFoundError(KeyError):
    """Raised when a plugin cannot be found in the registry."""


class PluginActivationError(RuntimeError):
    """Raised when plugin activation fails."""


class PluginManager:
    """Minimal plugin lifecycle manager for controlled platform extension."""

    def __init__(self) -> None:
        self._plugins: dict[str, EdgePlugin] = {}
        self._active: set[str] = set()

    def register(self, plugin: EdgePlugin) -> None:
        plugin_id = self._validate_plugin(plugin)

        if plugin_id in self._plugins:
            raise PluginValidationError(
                f"Plugin '{plugin_id}' is already registered"
            )

        self._plugins[plugin_id] = plugin

    def activate(self, plugin_id: str, context: Any | None = None) -> None:
        plugin = self._get_plugin(plugin_id)

        if plugin_id in self._active:
            return

        try:
            plugin.activate(context)
        except Exception as exc:
            raise PluginActivationError(
                f"Activation failed for plugin '{plugin_id}'"
            ) from exc

        self._active.add(plugin_id)

    def deactivate(self, plugin_id: str, context: Any | None = None) -> None:
        plugin = self._get_plugin(plugin_id)

        if plugin_id not in self._active:
            return

        plugin.deactivate(context)
        self._active.remove(plugin_id)

    def remove(self, plugin_id: str, context: Any | None = None) -> None:
        if plugin_id not in self._plugins:
            raise PluginNotFoundError(f"Plugin '{plugin_id}' is not registered")

        if plugin_id in self._active:
            self.deactivate(plugin_id, context)

        del self._plugins[plugin_id]

    def list_plugins(self) -> list[str]:
        return sorted(self._plugins.keys())

    def is_active(self, plugin_id: str) -> bool:
        return plugin_id in self._active

    def _get_plugin(self, plugin_id: str) -> EdgePlugin:
        plugin = self._plugins.get(plugin_id)

        if plugin is None:
            raise PluginNotFoundError(f"Plugin '{plugin_id}' is not registered")

        return plugin

    @staticmethod
    def _validate_plugin(plugin: EdgePlugin) -> str:
        plugin_id = getattr(plugin, "plugin_id", None)

        if not isinstance(plugin_id, str) or not plugin_id.strip():
            raise PluginValidationError("Plugin must declare a non-empty plugin_id")

        return plugin_id.strip()
