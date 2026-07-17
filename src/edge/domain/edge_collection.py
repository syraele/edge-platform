"""
EDGE_ENGINE

Edge Collection
"""

from dataclasses import dataclass

from .edge import Edge


@dataclass(frozen=True, slots=True)
class EdgeCollection:
    """Immutable collection of managed edges."""

    edges: tuple[Edge, ...] = ()