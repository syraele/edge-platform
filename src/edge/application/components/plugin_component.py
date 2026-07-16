from __future__ import annotations

from edge.plugins import PluginLoader, PluginManager


class PluginComponent:
    """Application lifecycle component for plugin orchestration."""

    def __init__(self, manager: PluginManager, engine_config: dict | None = None) -> None:
        self._manager = manager
        self._engine_config = engine_config or {}
        self._loader = PluginLoader()

    def initialize(self) -> None:
        plugins_cfg = self._engine_config.get("plugins", {})
        enabled_plugins = plugins_cfg.get("enabled", [])

        for plugin in self._loader.discover(enabled_plugins):
            self._manager.register(plugin)

    def start(self) -> None:
        self._manager.activate_all()

    def stop(self) -> None:
        self._manager.deactivate_all()
