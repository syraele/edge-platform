from edge.context import create_context
from edge.plugins import PluginManager


def test_plugin_manager_is_registered_in_context_registry():
    context = create_context(
        symbol="XAUUSD",
        timeframe="H1",
        mode="test",
        data_source="mock",
    )

    assert context.services.plugin_manager is not None
    assert isinstance(context.services.plugin_manager, PluginManager)

    plugin_manager = context.services.registry.get("plugin_manager")

    assert plugin_manager is context.services.plugin_manager
