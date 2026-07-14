"""
EDGE_ENGINE

Descriptor Registry
"""

from edge.domain.descriptor_definition import DescriptorDefinition


class DescriptorRegistry:
    """
    Registry of available market descriptors.

    Stores the descriptor definitions known by the system.
    """

    def __init__(self) -> None:
        self._definitions: dict[str, DescriptorDefinition] = {}

    def register(self, definition: DescriptorDefinition) -> None:
        """
        Register a new descriptor definition.

        Raises:
            ValueError: if a descriptor with the same name
                        is already registered.
        """
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
            KeyError: if the descriptor does not exist.
        """
        return self._definitions[name]

    def all(self) -> tuple[DescriptorDefinition, ...]:
        """
        Return all registered descriptor definitions.
        """
        return tuple(self._definitions.values())