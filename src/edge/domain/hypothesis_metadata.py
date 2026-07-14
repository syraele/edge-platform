"""
EDGE_ENGINE

Hypothesis Metadata
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class HypothesisMetadata:
    """
    Immutable metadata describing a ResearchHypothesis.
    """

    created_at: datetime

    version: str = "1.0"

    author: str = ""