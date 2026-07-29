from __future__ import annotations

from edge.domain.hypothesis_metadata import HypothesisMetadata
from edge.domain.market_description import MarketDescription
from edge.domain.research_hypothesis import ResearchHypothesis

from .primitive_catalog import PrimitiveCatalog


class PrimitiveDiscoveryEngine:
    """Generate primitive market hypotheses without introducing strategies or indicators."""

    def __init__(self, catalog: PrimitiveCatalog | None = None) -> None:
        self._catalog = catalog or PrimitiveCatalog()

    def list_catalog_primitives(self):
        return self._catalog.list_primitives()

    def generate_hypotheses(self, market_description: MarketDescription) -> list[ResearchHypothesis]:
        metadata = HypothesisMetadata(created_at=market_description.metadata.created_at)
        hypotheses: list[ResearchHypothesis] = []

        for primitive in self._catalog.list_primitives():
            hypotheses.append(
                ResearchHypothesis(
                    market_description=market_description,
                    metadata=metadata,
                    statement=self._statement_for(primitive),
                )
            )

        return hypotheses

    def _statement_for(self, primitive) -> str:
        mapping = {
            "close_gt_open": "close > open",
            "close_lt_open": "close < open",
            "close_gt_previous_close": "close > previous_close",
            "close_lt_previous_close": "close < previous_close",
            "high_gt_previous_high": "high > previous_high",
            "low_lt_previous_low": "low < previous_low",
            "open_gt_previous_open": "open > previous_open",
            "open_lt_previous_open": "open < previous_open",
            "range_gt_previous_range": "range > previous_range",
            "range_lt_previous_range": "range < previous_range",
            "body_gt_half_range": "body > half_range",
            "body_lt_half_range": "body < half_range",
            "close_gt_previous_open": "close > previous_open",
            "close_lt_previous_open": "close < previous_open",
            "close_gt_previous_close_by_pct": "close > previous_close by percentage",
            "close_lt_previous_close_by_pct": "close < previous_close by percentage",
            "volatility_gt_previous_volatility": "volatility > previous_volatility",
            "volatility_lt_previous_volatility": "volatility < previous_volatility",
        }
        return mapping[primitive.id]
