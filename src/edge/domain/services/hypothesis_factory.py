"""
EDGE_ENGINE

Hypothesis Factory
"""

from __future__ import annotations

from edge.domain.hypothesis_metadata import HypothesisMetadata
from edge.domain.market_description import MarketDescription
from edge.domain.research_hypothesis import ResearchHypothesis


class HypothesisFactory:
    """
    Minimal factory for generating a fixed set of primitive hypotheses.

    The implementation is intentionally small and easily extendable.
    """

    def create_hypotheses(self, market_description: MarketDescription) -> list[ResearchHypothesis]:
        """
        Create a stable collection of primitive hypotheses for the given market.
        """

        statements = (
            "close > open",
            "close < open",
            "close > previous_close",
            "close < previous_close",
            "high > previous_high",
            "low < previous_low",
        )

        metadata = HypothesisMetadata(
            created_at=market_description.metadata.created_at,
        )

        return [
            ResearchHypothesis(
                market_description=market_description,
                metadata=metadata,
                statement=statement,
            )
            for statement in statements
        ]
