from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PrimitiveDefinition:
    id: str
    name: str
    description: str
    category: str
    type: str
    builder: str


class PrimitiveCatalog:
    """Central catalog of atomic market primitives."""

    def __init__(self) -> None:
        self._primitives = (
            PrimitiveDefinition(
                id="close_gt_open",
                name="Close > Open",
                description="The close is greater than the open.",
                category="Price Action",
                type="Boolean",
                builder="ComparisonPrimitive",
            ),
            PrimitiveDefinition(
                id="close_lt_open",
                name="Close < Open",
                description="The close is less than the open.",
                category="Price Action",
                type="Boolean",
                builder="ComparisonPrimitive",
            ),
            PrimitiveDefinition(
                id="close_gt_previous_close",
                name="Close > Previous Close",
                description="The close is greater than the previous close.",
                category="Price Action",
                type="Boolean",
                builder="ComparisonPrimitive",
            ),
            PrimitiveDefinition(
                id="close_lt_previous_close",
                name="Close < Previous Close",
                description="The close is less than the previous close.",
                category="Price Action",
                type="Boolean",
                builder="ComparisonPrimitive",
            ),
            PrimitiveDefinition(
                id="high_gt_previous_high",
                name="High > Previous High",
                description="The high is greater than the previous high.",
                category="Price Action",
                type="Boolean",
                builder="ComparisonPrimitive",
            ),
            PrimitiveDefinition(
                id="low_lt_previous_low",
                name="Low < Previous Low",
                description="The low is less than the previous low.",
                category="Price Action",
                type="Boolean",
                builder="ComparisonPrimitive",
            ),
            PrimitiveDefinition(
                id="open_gt_previous_open",
                name="Open > Previous Open",
                description="The open is greater than the previous open.",
                category="Price Action",
                type="Boolean",
                builder="ComparisonPrimitive",
            ),
            PrimitiveDefinition(
                id="open_lt_previous_open",
                name="Open < Previous Open",
                description="The open is less than the previous open.",
                category="Price Action",
                type="Boolean",
                builder="ComparisonPrimitive",
            ),
        )

    def list_primitives(self) -> tuple[PrimitiveDefinition, ...]:
        return self._primitives

    def get_by_id(self, primitive_id: str) -> PrimitiveDefinition | None:
        for primitive in self._primitives:
            if primitive.id == primitive_id:
                return primitive
        return None
