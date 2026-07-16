import pytest

from edge.plugins import PluginDiscoveryError, PluginLoader


def test_loader_discovers_plugin_from_entrypoint():
    loader = PluginLoader()

    plugin = loader.load(
        {
            "entrypoint": "tests.unit.plugins.sample_plugins:LifecycleProbePlugin",
            "id": "lifecycle-probe",
        }
    )

    assert plugin.plugin_id == "lifecycle-probe"


def test_loader_rejects_invalid_entrypoint_format():
    loader = PluginLoader()

    with pytest.raises(PluginDiscoveryError):
        loader.load({"entrypoint": "invalid"})


def test_loader_rejects_non_plugin_class():
    loader = PluginLoader()

    with pytest.raises(PluginDiscoveryError):
        loader.load(
            {"entrypoint": "tests.unit.plugins.sample_plugins:NotAPlugin"}
        )
