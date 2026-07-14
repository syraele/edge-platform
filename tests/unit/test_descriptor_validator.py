from edge.domain.descriptor_definition import DescriptorDefinition
from edge.domain.services.descriptor_validator import DescriptorValidator


def test_valid_descriptor():
    validator = DescriptorValidator()

    definition = DescriptorDefinition(
        name="trend",
        category="trend",
    )

    result = validator.validate(definition)

    assert result.is_valid
    assert not result.has_errors
    assert result.error_count == 0
    assert result.errors == ()


def test_empty_name():
    validator = DescriptorValidator()

    definition = DescriptorDefinition(
        name="",
        category="trend",
    )

    result = validator.validate(definition)

    assert not result.is_valid
    assert result.has_errors
    assert result.error_count == 1
    assert "Descriptor name cannot be empty." in result.errors


def test_blank_name():
    validator = DescriptorValidator()

    definition = DescriptorDefinition(
        name="   ",
        category="trend",
    )

    result = validator.validate(definition)

    assert not result.is_valid
    assert result.has_errors
    assert result.error_count == 1


def test_empty_category():
    validator = DescriptorValidator()

    definition = DescriptorDefinition(
        name="trend",
        category="",
    )

    result = validator.validate(definition)

    assert not result.is_valid
    assert result.has_errors
    assert result.error_count == 1
    assert "Descriptor category cannot be empty." in result.errors


def test_multiple_validation_errors():
    validator = DescriptorValidator()

    definition = DescriptorDefinition(
        name="",
        category="",
    )

    result = validator.validate(definition)

    assert not result.is_valid
    assert result.has_errors
    assert result.error_count == 2