from edge.domain.services.discovery_report import DiscoveryReportRow
from edge.domain.services.edge_scoring import EdgeScoringService


def test_edge_scoring_ranks_rows_by_composite_score() -> None:
    service = EdgeScoringService()

    rows = (
        DiscoveryReportRow(
            hypothesis_name="positive_edge",
            occurrences=40.0,
            average_return=0.02,
            average_return_1=0.01,
            average_return_5=0.015,
            average_return_10=0.01,
            average_return_20=0.008,
        ),
        DiscoveryReportRow(
            hypothesis_name="frequency_edge",
            occurrences=200.0,
            average_return=0.001,
            average_return_1=0.0005,
            average_return_5=0.0007,
            average_return_10=0.0001,
            average_return_20=0.0002,
        ),
        DiscoveryReportRow(
            hypothesis_name="negative_edge",
            occurrences=20.0,
            average_return=-0.01,
            average_return_1=-0.005,
            average_return_5=-0.007,
            average_return_10=-0.01,
            average_return_20=-0.008,
        ),
    )

    ranked = service.rank_rows(rows)

    assert [item.hypothesis_name for item in ranked] == ["frequency_edge", "positive_edge", "negative_edge"]
    assert ranked[0].score > ranked[1].score > ranked[2].score
