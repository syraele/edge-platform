from __future__ import annotations

from itertools import combinations

from .primitive_catalog import PrimitiveCatalog


class CombinationEngine:
    """Generate valid two-primitive combinations from the primitive catalog."""

    def __init__(self, catalog: PrimitiveCatalog | None = None) -> None:
        self._catalog = catalog or PrimitiveCatalog()

    def generate_combinations(self) -> list[str]:
        primitives = self._catalog.list_primitives()
        seen: set[str] = set()
        combinations_list: list[str] = []

        for left, right in combinations(primitives, 2):
            left_name = left.name
            right_name = right.name
            candidate = f"{left_name} AND {right_name}"
            opposite = f"{right_name} AND {left_name}"

            if candidate in seen or opposite in seen:
                continue

            if left_name == right_name:
                continue

            if self._is_logically_impossible(left_name, right_name):
                continue

            seen.add(candidate)
            combinations_list.append(candidate)

        return combinations_list

    def _is_logically_impossible(self, left_name: str, right_name: str) -> bool:
        impossible_pairs = {
            ("Close > Open", "Close < Open"),
            ("Close < Open", "Close > Open"),
            ("Close > Previous Close", "Close < Previous Close"),
            ("Close < Previous Close", "Close > Previous Close"),
            ("Open > Previous Open", "Open < Previous Open"),
            ("Open < Previous Open", "Open > Previous Open"),
        }
        return (left_name, right_name) in impossible_pairs
