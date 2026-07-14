"""
EDGE_ENGINE

Knowledge
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Knowledge:
    """
    Immutable validated research conclusion.

    Knowledge represents a validated, reproducible and
    reusable research conclusion.
    """

    statement: str