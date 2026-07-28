from edge.domain.services.discovery_report import DiscoveryReport, DiscoveryReportRow
from edge.domain.services.edge_improvement_analysis import EdgeImprovementAnalysisService


def test_service_reports_improvement_over_base_hypothesis() -> None:
    base = DiscoveryReportRow(
        hypothesis_name="close > open",
        occurrences=10.0,
        average_return=0.001,
        average_return_1=0.0,
        average_return_5=0.0,
        average_return_10=0.0,
        average_return_20=0.0,
    )
    compound = DiscoveryReportRow(
        hypothesis_name="close > open AND high > previous_high",
        occurrences=20.0,
        average_return=0.002,
        average_return_1=0.0,
        average_return_5=0.0,
        average_return_10=0.0,
        average_return_20=0.0,
    )

    report = DiscoveryReport(rows=(base, compound))
    service = EdgeImprovementAnalysisService()

    analysis = service.analyze(report)

    assert len(analysis) == 1
    assert analysis[0].base_hypothesis == "close > open"
    assert analysis[0].compound_hypothesis == "close > open AND high > previous_high"
    assert analysis[0].occurrence_delta > 0
    assert analysis[0].average_return_delta > 0
    assert analysis[0].edge_score_delta > 0
    assert analysis[0].improves is True
