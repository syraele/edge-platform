import pytest

from edge.plugins import (
    EdgePlugin,
    PluginActivationError,
    PluginManager,
    PluginValidationError,
)


class DummyPlugin(EdgePlugin):
    plugin_id = "dummy"
    version = "1.0.0"

    def __init__(self) -> None:
        self.activated = 0
        self.deactivated = 0

    def activate(self, context=None) -> None:
        self.activated += 1

    def deactivate(self, context=None) -> None:
        self.deactivated += 1


class FailingPlugin(EdgePlugin):
    plugin_id = "failing"

    def activate(self, context=None) -> None:
        raise RuntimeError("boom")

    def deactivate(self, context=None) -> None:
        return None


class OrderedPlugin(EdgePlugin):
    version = "1.0.0"

    def __init__(self, plugin_id: str) -> None:
        self.plugin_id = plugin_id
        self.activated = 0
        self.deactivated = 0

    def activate(self, context=None) -> None:
        self.activated += 1

    def deactivate(self, context=None) -> None:
        self.deactivated += 1


def test_register_requires_non_empty_plugin_id():
    class InvalidPlugin(EdgePlugin):
        plugin_id = ""

        def activate(self, context=None) -> None:
            return None

        def deactivate(self, context=None) -> None:
            return None

    manager = PluginManager()

    with pytest.raises(PluginValidationError):
        manager.register(InvalidPlugin())


def test_register_rejects_duplicate_plugin_id():
    manager = PluginManager()

    manager.register(DummyPlugin())

    with pytest.raises(PluginValidationError):
        manager.register(DummyPlugin())


def test_activate_marks_plugin_as_active():
    manager = PluginManager()
    plugin = DummyPlugin()

    manager.register(plugin)
    manager.activate(plugin.plugin_id)

    assert manager.is_active(plugin.plugin_id) is True
    assert plugin.activated == 1


def test_activation_failure_is_contained():
    manager = PluginManager()
    plugin = FailingPlugin()

    manager.register(plugin)

    with pytest.raises(PluginActivationError):
        manager.activate(plugin.plugin_id)

    assert manager.is_active(plugin.plugin_id) is False


def test_remove_deactivates_active_plugin():
    manager = PluginManager()
    plugin = DummyPlugin()

    manager.register(plugin)
    manager.activate(plugin.plugin_id)
    manager.remove(plugin.plugin_id)

    assert manager.list_plugins() == []
    assert plugin.deactivated == 1


def test_activate_all_rolls_back_on_failure():
    manager = PluginManager()
    stable_plugin = OrderedPlugin("a-stable")
    failing_plugin = FailingPlugin()

    manager.register(stable_plugin)
    manager.register(failing_plugin)

    with pytest.raises(PluginActivationError):
        manager.activate_all()

    assert manager.is_active(stable_plugin.plugin_id) is False
    assert stable_plugin.activated == 1
    assert stable_plugin.deactivated == 1
