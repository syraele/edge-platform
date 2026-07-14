"""
EDGE_ENGINE

Knowledge Collection
"""

from dataclasses import dataclass

from .knowledge import Knowledge


@dataclass(frozen=True, slots=True)
class KnowledgeCollection:
    """
    Immutable collection of validated Knowledge.

    Represents accumulated research knowledge.
    """

    knowledge: tuple[Knowledge, ...] = ()