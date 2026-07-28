from edge.domain.services.primitive_catalog import PrimitiveCatalog
from edge.domain.services.primitive_discovery_engine import PrimitiveDiscoveryEngine


def test_primitive_catalog_contains_unique_and_complete_primitives() -> None:
    catalog = PrimitiveCatalog()
    primitives = catalog.list_primitives()

    assert len(primitives) > 0
    assert len({primitive.id for primitive in primitives}) == len(primitives)

    for primitive in primitives:
        assert primitive.id
        assert primitive.name
        assert primitive.description
        assert primitive.category
        assert primitive.type
        assert primitive.builder


def test_primitive_discovery_engine_reads_from_catalog() -> None:
    catalog = PrimitiveCatalog()
    engine = PrimitiveDiscoveryEngine(catalog=catalog)

    primitives = engine.list_catalog_primitives()

    assert primitives == catalog.list_primitives()
