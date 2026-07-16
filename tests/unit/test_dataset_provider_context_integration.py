from edge.context import create_context
from edge.data import DatasetProviderRegistry


def test_dataset_provider_registry_is_registered_in_context_registry():
    context = create_context(
        symbol="XAUUSD",
        timeframe="H1",
        mode="test",
        data_source="mock",
    )

    assert context.services.dataset_provider_registry is not None
    assert isinstance(context.services.dataset_provider_registry, DatasetProviderRegistry)

    registry = context.services.registry.get("dataset_provider_registry")

    assert registry is context.services.dataset_provider_registry
