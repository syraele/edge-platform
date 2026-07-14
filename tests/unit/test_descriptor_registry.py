from edge.domain.descriptor_definition import DescriptorDefinition
from edge.domain.services.descriptor_registry import DescriptorRegistry


def test_register_descriptor():
    registry = DescriptorRegistry()

    definition = DescriptorDefinition(
        name="trend",
        description="Trend strength",
        category="trend",
    )

    registry.register(definition)

    assert registry.exists("trend")
    assert registry.get("trend") == definition


def test_all_returns_registered_descriptors():
    registry = DescriptorRegistry()

    trend = DescriptorDefinition(name="trend")
    volatility = DescriptorDefinition(name="volatility")

    registry.register(trend)
    registry.register(volatility)

    descriptors = registry.all()

    assert len(descriptors) == 2
    assert trend in descriptors
    assert volatility in descriptors


def test_duplicate_registration_raises():
    registry = DescriptorRegistry()

    definition = DescriptorDefinition(name="trend")

    registry.register(definition)

    try:
        registry.register(definition)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_get_unknown_descriptor_raises():
    registry = DescriptorRegistry()

    try:
        registry.get("unknown")
        assert False, "Expected KeyError"
    except KeyError:
        pass


def test_register_invalid_descriptor_raises():
    registry = DescriptorRegistry()

    definition = DescriptorDefinition(
        name="",
        category="trend",
    )

    try:
        registry.register(definition)
        assert False, "Expected ValueError"
    except ValueError:
        pass