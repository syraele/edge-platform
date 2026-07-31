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

    assert [item.hypothesis_name for item in ranked] == ["positive_edge", "frequency_edge", "negative_edge"]
    assert ranked[0].score > ranked[1].score > ranked[2].score


def test_edge_scoring_uses_multiple_quality_metrics() -> None:
    service = EdgeScoringService()

    rows = (
        DiscoveryReportRow(
            hypothesis_name="high_expectancy",
            occurrences=30.0,
            average_return=0.04,
            average_return_1=0.02,
            average_return_5=0.025,
            average_return_10=0.015,
            average_return_20=0.012,
            win_rate=0.72,
            expectancy=0.018,
            profit_factor=1.75,
            payoff=0.8,
            drawdown=0.03,
        ),
        DiscoveryReportRow(
            hypothesis_name="high_frequency_low_quality",
            occurrences=300.0,
            average_return=0.001,
            average_return_1=0.0005,
            average_return_5=0.0007,
            average_return_10=0.0001,
            average_return_20=0.0002,
            win_rate=0.51,
            expectancy=0.0004,
            profit_factor=1.02,
            payoff=0.02,
            drawdown=0.2,
        ),
    )

    ranked = service.rank_rows(rows)

    assert [item.hypothesis_name for item in ranked] == ["high_expectancy", "high_frequency_low_quality"]
    assert ranked[0].score > ranked[1].score
