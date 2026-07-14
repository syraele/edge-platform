"""
EDGE_ENGINE

Descriptor Registry
"""

from edge.domain.descriptor_definition import DescriptorDefinition
from edge.domain.services.descriptor_validator import DescriptorValidator


class DescriptorRegistry:
    """
    Registry of available market descriptors.

    Stores validated descriptor definitions known by the system.
    """

    def __init__(self) -> None:
        self._definitions: dict[str, DescriptorDefinition] = {}
        self._validator = DescriptorValidator()

    def register(self, definition: DescriptorDefinition) -> None:
        """
        Register a validated descriptor definition.

        Raises:
            ValueError:
                If the descriptor is invalid or already registered.
        """
        result = self._validator.validate(definition)

        if result.has_errors:
            raise ValueError("; ".join(result.errors))

        if definition.name in self._definitions:
            raise ValueError(
                f"Descriptor '{definition.name}' is already registered."
            )

        self._definitions[definition.name] = definition

    def exists(self, name: str) -> bool:
        """
        Return True if the descriptor is registered.
        """
        return name in self._definitions

    def get(self, name: str) -> DescriptorDefinition:
        """
        Retrieve a registered descriptor.

        Raises:
            KeyError:
                If the descriptor does not exist.
        """
        return self._definitions[name]

    def all(self) -> tuple[DescriptorDefinition, ...]:
        """
        Return all registered descriptor definitions.
        """
        return tuple(self._definitions.values())