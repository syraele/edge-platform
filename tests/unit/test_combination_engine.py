from edge.domain.services.primitive_catalog import PrimitiveCatalog
from edge.domain.services.combination_engine import CombinationEngine


def test_combination_engine_generates_unique_valid_two_primitive_combinations() -> None:
    catalog = PrimitiveCatalog()
    engine = CombinationEngine(catalog=catalog)

    combinations = engine.generate_combinations()

    assert len(combinations) > 0
    assert len(set(combinations)) == len(combinations)

    for combination in combinations:
        assert " AND " in combination
        assert combination.count(" AND ") == 1
        assert combination not in {
            "close > open AND close < open",
            "close < open AND close > open",
        }
