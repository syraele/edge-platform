"""
EDGE_ENGINE

Hypothesis Factory
"""

from __future__ import annotations

from edge.domain.hypothesis_metadata import HypothesisMetadata
from edge.domain.market_description import MarketDescription
from edge.domain.research_hypothesis import ResearchHypothesis

from .combination_engine import CombinationEngine
from .primitive_discovery_engine import PrimitiveDiscoveryEngine


class HypothesisFactory:
    """Generate primitive and combination hypotheses through dedicated engines."""

    def __init__(
        self,
        primitive_engine: PrimitiveDiscoveryEngine | None = None,
        combination_engine: CombinationEngine | None = None,
    ) -> None:
        self._primitive_engine = primitive_engine or PrimitiveDiscoveryEngine()
        self._combination_engine = combination_engine or CombinationEngine()

    def create_hypotheses(self, market_description: MarketDescription) -> list[ResearchHypothesis]:
        """Create a stable collection of primitive and combination hypotheses for the given market."""

        metadata = HypothesisMetadata(created_at=market_description.metadata.created_at)
        hypotheses = self._primitive_engine.generate_hypotheses(market_description)

        for statement in self._combination_engine.generate_combinations():
            hypotheses.append(
                ResearchHypothesis(
                    market_description=market_description,
                    metadata=metadata,
                    statement=statement,
                )
            )

        return hypotheses
