"""
EDGE_ENGINE

Descriptor Validator
"""

from edge.domain.descriptor_definition import DescriptorDefinition
from edge.domain.services.validation_result import ValidationResult


class DescriptorValidator:
    """
    Validates DescriptorDefinition instances.

    Validation rules are intentionally centralized here so the
    DescriptorRegistry remains focused only on descriptor management.
    """

    def validate(
        self,
        definition: DescriptorDefinition,
    ) -> ValidationResult:
        """
        Validate a descriptor definition.
        """
        errors: list[str] = []

        if not definition.name.strip():
            errors.append("Descriptor name cannot be empty.")

        if not definition.category.strip():
            errors.append("Descriptor category cannot be empty.")

        if errors:
            return ValidationResult.failure(*errors)

        return ValidationResult.success()