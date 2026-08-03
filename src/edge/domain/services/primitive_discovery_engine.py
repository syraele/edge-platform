from __future__ import annotations

from edge.domain.hypothesis_metadata import HypothesisMetadata
from edge.domain.market_description import MarketDescription
from edge.domain.research_hypothesis import HypothesisPredicate, ResearchHypothesis

from .primitive_catalog import PrimitiveCatalog


class PrimitiveDiscoveryEngine:
    """Generate primitive and contextual market hypotheses without introducing strategies or indicators."""

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
                    predicate=(self._predicate_for(primitive),),
                )
            )

        for statement in self._contextual_hypotheses(market_description):
            hypotheses.append(
                ResearchHypothesis(
                    market_description=market_description,
                    metadata=metadata,
                    statement=statement,
                )
            )

        return hypotheses

    def _contextual_hypotheses(self, market_description: MarketDescription) -> list[str]:
        dataset = getattr(market_description, "dataset", None)
        bars = getattr(dataset, "bars", None)
        if not bars or len(bars) < 2:
            return []

        last_bar = bars[-1]
        body_to_range_ratio = self._body_to_range_ratio(last_bar)
        recent_return_3 = self._recent_return_3(bars)
        relative_range = self._relative_range(bars)
        relative_volume = self._relative_volume(bars)

        statements: list[str] = []

        if body_to_range_ratio is not None:
            statements.append(
                f"close > previous_close when body_to_range_ratio > {self._format_threshold(body_to_range_ratio, 0.5)}"
            )
            statements.append(
                f"close < previous_close when body_to_range_ratio < {self._format_threshold(body_to_range_ratio, 0.5)}"
            )

        if recent_return_3 is not None:
            statements.append(
                f"close > previous_close when recent_return_3 > {self._format_threshold(recent_return_3, 0.0)}"
            )
            statements.append(
                f"close < previous_close when recent_return_3 < {self._format_threshold(recent_return_3, 0.0)}"
            )

        if relative_range is not None:
            statements.append(
                f"range > previous_range when relative_range > {self._format_threshold(relative_range, 1.0)}"
            )

        if relative_volume is not None:
            statements.append(
                f"close > previous_close when relative_volume > {self._format_threshold(relative_volume, 1.0)}"
            )

        return statements

    def _body_to_range_ratio(self, bar) -> float | None:
        body = abs(bar.close - bar.open)
        range_size = abs(bar.high - bar.low)
        if range_size == 0:
            return None
        return body / range_size

    def _recent_return_3(self, bars) -> float | None:
        if len(bars) < 4:
            return None

        start_close = bars[-4].close
        end_close = bars[-1].close
        if start_close == 0:
            return None
        return (end_close - start_close) / abs(start_close)

    def _relative_range(self, bars) -> float | None:
        if len(bars) < 2:
            return None

        current_range = abs(bars[-1].high - bars[-1].low)
        previous_ranges = [abs(bar.high - bar.low) for bar in bars[:-1]]
        if not previous_ranges:
            return None

        average_previous_range = sum(previous_ranges) / len(previous_ranges)
        if average_previous_range == 0:
            return None
        return current_range / average_previous_range

    def _relative_volume(self, bars) -> float | None:
        if len(bars) < 2:
            return None

        current_volume = bars[-1].volume
        previous_volumes = [bar.volume for bar in bars[:-1]]
        if not previous_volumes:
            return None

        average_previous_volume = sum(previous_volumes) / len(previous_volumes)
        if average_previous_volume == 0:
            return None
        return current_volume / average_previous_volume

    def _format_threshold(self, value: float, baseline: float) -> str:
        return str(round(value, 4) if value != baseline else baseline)

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

    def _predicate_for(self, primitive) -> tuple[HypothesisPredicate, tuple[float, ...]]:
        mapping = {
            "close_gt_open": (HypothesisPredicate.CLOSE_GT_OPEN, ()),
            "close_lt_open": (HypothesisPredicate.CLOSE_LT_OPEN, ()),
            "close_gt_previous_close": (HypothesisPredicate.CLOSE_GT_PREVIOUS_CLOSE, ()),
            "close_lt_previous_close": (HypothesisPredicate.CLOSE_LT_PREVIOUS_CLOSE, ()),
            "high_gt_previous_high": (HypothesisPredicate.HIGH_GT_PREVIOUS_HIGH, ()),
            "low_lt_previous_low": (HypothesisPredicate.LOW_LT_PREVIOUS_LOW, ()),
            "open_gt_previous_open": (HypothesisPredicate.OPEN_GT_PREVIOUS_OPEN, ()),
            "open_lt_previous_open": (HypothesisPredicate.OPEN_LT_PREVIOUS_OPEN, ()),
            "range_gt_previous_range": (HypothesisPredicate.CLOSE_GT_PREVIOUS_CLOSE, ()),
            "range_lt_previous_range": (HypothesisPredicate.CLOSE_LT_PREVIOUS_CLOSE, ()),
            "body_gt_half_range": (HypothesisPredicate.CLOSE_GT_PREVIOUS_CLOSE, ()),
            "body_lt_half_range": (HypothesisPredicate.CLOSE_LT_PREVIOUS_CLOSE, ()),
            "close_gt_previous_open": (HypothesisPredicate.CLOSE_GT_PREVIOUS_OPEN, ()),
            "close_lt_previous_open": (HypothesisPredicate.CLOSE_LT_PREVIOUS_OPEN, ()),
            "close_gt_previous_close_by_pct": (HypothesisPredicate.CLOSE_GT_PREVIOUS_CLOSE, ()),
            "close_lt_previous_close_by_pct": (HypothesisPredicate.CLOSE_LT_PREVIOUS_CLOSE, ()),
            "volatility_gt_previous_volatility": (HypothesisPredicate.CLOSE_GT_PREVIOUS_CLOSE, ()),
            "volatility_lt_previous_volatility": (HypothesisPredicate.CLOSE_LT_PREVIOUS_CLOSE, ()),
        }
        return mapping[primitive.id]