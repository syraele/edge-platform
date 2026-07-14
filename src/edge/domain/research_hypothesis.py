"""
EDGE_ENGINE

Research Hypothesis
"""

from dataclasses import dataclass

from edge.domain.hypothesis_metadata import HypothesisMetadata
from edge.domain.market_description import MarketDescription


@dataclass(frozen=True, slots=True)
class ResearchHypothesis:
    """
    Immutable research hypothesis.

    A ResearchHypothesis represents a single falsifiable
    statement about market behaviour derived from exactly
    one MarketDescription.
    """

    market_description: MarketDescription

    metadata: HypothesisMetadata

    statement: str