"""
EDGE_ENGINE

Descriptor Definition
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DescriptorDefinition:
    """
    Immutable definition of a market descriptor.

    A DescriptorDefinition describes a descriptor that the
    system knows how to produce.

    It does not contain any calculated market value.
    """

    name: str

    description: str = ""

    category: str = "general"

    unit: str = ""