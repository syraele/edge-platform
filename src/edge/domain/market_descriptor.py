"""
EDGE_ENGINE

Market Descriptor
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MarketDescriptor:
    """
    Immutable descriptor extracted from a historical dataset.

    A MarketDescriptor represents a quantified characteristic
    describing market behaviour.

    The descriptor is intentionally generic so that new
    descriptor types can be introduced without changing
    the domain model.
    """

    name: str

    value: float

    unit: str = ""

    description: str = ""