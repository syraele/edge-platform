"""
EDGE_ENGINE

Research Hypothesis
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from edge.domain.hypothesis_metadata import HypothesisMetadata
from edge.domain.market_description import MarketDescription


class HypothesisPredicate(Enum):
    CLOSE_GT_OPEN = "close_gt_open"
    CLOSE_LT_OPEN = "close_lt_open"
    CLOSE_GT_PREVIOUS_CLOSE = "close_gt_previous_close"
    CLOSE_LT_PREVIOUS_CLOSE = "close_lt_previous_close"
    HIGH_GT_PREVIOUS_HIGH = "high_gt_previous_high"
    LOW_LT_PREVIOUS_LOW = "low_lt_previous_low"
    OPEN_GT_PREVIOUS_OPEN = "open_gt_previous_open"
    OPEN_LT_PREVIOUS_OPEN = "open_lt_previous_open"
    CLOSE_GT_PREVIOUS_OPEN = "close_gt_previous_open"
    CLOSE_LT_PREVIOUS_OPEN = "close_lt_previous_open"


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
    predicate: tuple[tuple[HypothesisPredicate, tuple[float, ...]], ...] | None = None

    def __post_init__(self) -> None:
        if self.predicate is None:
            predicate = self._build_predicate(self.statement)
            object.__setattr__(self, "predicate", predicate)

    @staticmethod
    def _build_predicate(statement: str) -> tuple[tuple[HypothesisPredicate, tuple[float, ...]], ...] | None:
        normalized = ResearchHypothesis._normalize_statement(statement)
        if not normalized:
            return None

        if " and " in normalized:
            parts = [part.strip() for part in normalized.split(" and ")]
            predicates = []
            for part in parts:
                predicate = ResearchHypothesis._build_predicate_for_part(part)
                if predicate is not None:
                    predicates.append(predicate)
            return tuple(predicates) if predicates else None

        predicate = ResearchHypothesis._build_predicate_for_part(normalized)
        return (predicate,) if predicate is not None else None

    @staticmethod
    def _normalize_statement(statement: str) -> str:
        return statement.strip().lower()

    @staticmethod
    def _build_predicate_for_part(statement: str) -> tuple[HypothesisPredicate, tuple[float, ...]] | None:
        mapping = {
            "close > open": (HypothesisPredicate.CLOSE_GT_OPEN, ()),
            "close < open": (HypothesisPredicate.CLOSE_LT_OPEN, ()),
            "close > previous_close": (HypothesisPredicate.CLOSE_GT_PREVIOUS_CLOSE, ()),
            "close < previous_close": (HypothesisPredicate.CLOSE_LT_PREVIOUS_CLOSE, ()),
            "close > previous close": (HypothesisPredicate.CLOSE_GT_PREVIOUS_CLOSE, ()),
            "close < previous close": (HypothesisPredicate.CLOSE_LT_PREVIOUS_CLOSE, ()),
            "high > previous_high": (HypothesisPredicate.HIGH_GT_PREVIOUS_HIGH, ()),
            "high > previous high": (HypothesisPredicate.HIGH_GT_PREVIOUS_HIGH, ()),
            "low < previous_low": (HypothesisPredicate.LOW_LT_PREVIOUS_LOW, ()),
            "low < previous low": (HypothesisPredicate.LOW_LT_PREVIOUS_LOW, ()),
            "open > previous_open": (HypothesisPredicate.OPEN_GT_PREVIOUS_OPEN, ()),
            "open < previous_open": (HypothesisPredicate.OPEN_LT_PREVIOUS_OPEN, ()),
            "close > previous_open": (HypothesisPredicate.CLOSE_GT_PREVIOUS_OPEN, ()),
            "close < previous_open": (HypothesisPredicate.CLOSE_LT_PREVIOUS_OPEN, ()),
            "range > previous_range": (HypothesisPredicate.CLOSE_GT_PREVIOUS_CLOSE, ()),
            "range < previous_range": (HypothesisPredicate.CLOSE_LT_PREVIOUS_CLOSE, ()),
            "body > half_range": (HypothesisPredicate.CLOSE_GT_PREVIOUS_CLOSE, ()),
            "body < half_range": (HypothesisPredicate.CLOSE_LT_PREVIOUS_CLOSE, ()),
            "volatility > previous_volatility": (HypothesisPredicate.CLOSE_GT_PREVIOUS_CLOSE, ()),
            "volatility < previous_volatility": (HypothesisPredicate.CLOSE_LT_PREVIOUS_CLOSE, ()),
        }
        return mapping.get(statement)