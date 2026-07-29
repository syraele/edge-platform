"""
EDGE_ENGINE

Knowledge
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class Knowledge:
    """
    Immutable validated research conclusion.

    Knowledge represents a validated, reproducible and
    reusable research conclusion.
    """

    statement: str
    knowledge_id: str = field(default_factory=lambda: str(uuid4()), compare=False)
    evidence_reference: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )