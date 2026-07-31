from datetime import UTC, datetime
from types import SimpleNamespace

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.domain.descriptor_metadata import DescriptorMetadata
from edge.domain.evidence import Evidence
from edge.domain.knowledge import Knowledge
from edge.domain.market_description import MarketDescription
from edge.domain.services.candidate_edge_selection import CandidateEdgeSelectionConfig, CandidateEdgeSelectionService
from edge.domain.services.experiment_executor import ExperimentExecutor
from edge.domain.services.hypothesis_factory import HypothesisFactory
from edge.domain.services.discovery_report import DiscoveryReport, DiscoveryReportService


def test_discovery_report_contains_all_hypotheses_and_orders_by_average_return_10() -> None:
    dataset = HistoricalDataset(
        metadata=DatasetMetadata(
            symbol="EURUSD",
            timeframe="M1",
        ),
        bars=(
            Bar(
                timestamp=datetime(2024, 1, 1),
                open=1.1000,
                high=1.1010,
                low=1.0990,
                close=1.1005,
            ),
            Bar(
                timestamp=datetime(2024, 1, 2),
                open=1.2000,
                high=1.2050,
                low=1.1950,
                close=1.2012,
            ),
            Bar(
                timestamp=datetime(2024, 1, 3),
                open=1.2050,
                high=1.2060,
                low=1.2040,
                close=1.2055,
            ),
            Bar(
                timestamp=datetime(2024, 1, 4),
                open=1.3000,
                high=1.3050,
                low=1.2950,
                close=1.3010,
            ),
        ),
    )

    market_description = MarketDescription(
        dataset=dataset,
        metadata=DescriptorMetadata(
            created_at=datetime.now(UTC),
            builder_version="1.0",
        ),
        descriptors=(),
    )

    hypotheses = HypothesisFactory().create_hypotheses(market_description)
    executor = ExperimentExecutor()
    evidences = [executor.execute(hypothesis_to_experiment(hypothesis)) for hypothesis in hypotheses]

    report = DiscoveryReportService().create_report(hypotheses, evidences)

    assert len(report.rows) == len(hypotheses)
    assert {row.hypothesis_name for row in report.rows} == {hypothesis.statement for hypothesis in hypotheses}
    assert list(report.rows) == sorted(report.rows, key=lambda row: row.average_return_10, reverse=True)


def test_discovery_report_uses_evaluator_knowledge_for_selection_counts() -> None:
    hypotheses = [SimpleNamespace(statement="first"), SimpleNamespace(statement="second")]
    evidences = [
        Evidence(measurements={"hypothesis_occurrences": 2.0, "hypothesis_average_return": 0.01}),
        Evidence(measurements={"hypothesis_occurrences": 1.0, "hypothesis_average_return": 0.0}),
    ]
    knowledge_items = [
        Knowledge(
            statement="selected-from-evaluator",
            evidence_reference="evaluator-1",
            metadata={"hypothesis_occurrences": "2.0", "hypothesis_average_return": "0.01"},
        ),
        Knowledge(
            statement="rejected-from-evaluator",
            evidence_reference="evaluator-2",
            metadata={"hypothesis_occurrences": "1.0", "hypothesis_average_return": "0.0"},
        ),
    ]

    selection_service = CandidateEdgeSelectionService(
        CandidateEdgeSelectionConfig(min_occurrences=2, min_average_return_abs=0.0)
    )
    report = DiscoveryReportService(selection_service=selection_service).create_report(
        hypotheses,
        evidences,
        knowledge_items=knowledge_items,
    )

    assert report.selection_summary is not None
    assert report.selection_summary.generated_count == 2
    assert report.selection_summary.selected_count == 1
    assert report.summary is not None
    assert report.summary.knowledge_generated == 2
    assert report.summary.candidate_edges == 1
    assert report.knowledge is not None
    assert report.knowledge.statement == "selected-from-evaluator"


def test_discovery_report_summary_counts_are_derived_from_row_confirmed_flags() -> None:
    hypotheses = [SimpleNamespace(statement="first"), SimpleNamespace(statement="second")]
    evidences = [
        Evidence(measurements={"hypothesis_occurrences": 2.0, "hypothesis_average_return": 0.01}),
        Evidence(measurements={"hypothesis_occurrences": 1.0, "hypothesis_average_return": 0.0}),
    ]
    validation_evidences = [
        Evidence(measurements={"hypothesis_occurrences": 0.0, "hypothesis_average_return": 0.0}),
        Evidence(measurements={"hypothesis_occurrences": 1.0, "hypothesis_average_return": 0.0}),
    ]
    knowledge_items = [
        Knowledge(
            statement="selected-from-evaluator-1",
            evidence_reference="evaluator-1",
            metadata={"hypothesis_occurrences": "1.0", "hypothesis_average_return": "0.0"},
        ),
        Knowledge(
            statement="selected-from-evaluator-2",
            evidence_reference="evaluator-2",
            metadata={"hypothesis_occurrences": "1.0", "hypothesis_average_return": "0.0"},
        ),
    ]

    selection_service = CandidateEdgeSelectionService(
        CandidateEdgeSelectionConfig(min_occurrences=1, min_average_return_abs=0.0)
    )
    report = DiscoveryReportService(selection_service=selection_service).create_report(
        hypotheses,
        evidences,
        validation_evidences=validation_evidences,
        knowledge_items=knowledge_items,
    )

    assert report.summary is not None
    assert report.summary.candidate_edges == 2
    assert report.summary.candidate_edges_confirmed == 0
    assert report.summary.candidate_edges_rejected == 0
    assert report.summary.confirmation_rate == 0.0


def test_discovery_report_uses_explicit_hypothesis_to_knowledge_mapping() -> None:
    hypotheses = [SimpleNamespace(statement="first"), SimpleNamespace(statement="second")]
    evidences = [
        Evidence(measurements={"hypothesis_occurrences": 2.0, "hypothesis_average_return": 0.01}),
        Evidence(measurements={"hypothesis_occurrences": 1.0, "hypothesis_average_return": 0.0}),
    ]
    validation_evidences = [
        Evidence(measurements={"hypothesis_occurrences": 1.0, "hypothesis_average_return": 0.0}),
        Evidence(measurements={"hypothesis_occurrences": 1.0, "hypothesis_average_return": 0.0}),
    ]
    knowledge_items = [
        Knowledge(
            statement="selected-from-evaluator",
            evidence_reference="evaluator-1",
            metadata={"hypothesis_occurrences": "1.0", "hypothesis_average_return": "0.0"},
        )
    ]

    selection_service = CandidateEdgeSelectionService(
        CandidateEdgeSelectionConfig(min_occurrences=1, min_average_return_abs=0.0)
    )
    report = DiscoveryReportService(selection_service=selection_service).create_report(
        hypotheses,
        evidences,
        validation_evidences=validation_evidences,
        knowledge_items=knowledge_items,
        knowledge_by_hypothesis={"second": knowledge_items[0]},
    )

    assert report.summary is not None
    assert report.summary.candidate_edges == 1
    assert report.summary.candidate_edges_confirmed == 1
    assert report.summary.candidate_edges_rejected == 0
    assert report.summary.confirmation_rate == 100.0


def test_discovery_report_summary_counts_only_rows_selected_via_mapping() -> None:
    hypotheses = [SimpleNamespace(statement="first"), SimpleNamespace(statement="second")]
    evidences = [
        Evidence(measurements={"hypothesis_occurrences": 2.0, "hypothesis_average_return": 0.01}),
        Evidence(measurements={"hypothesis_occurrences": 1.0, "hypothesis_average_return": 0.0}),
    ]
    validation_evidences = [
        Evidence(measurements={"hypothesis_occurrences": 0.0, "hypothesis_average_return": 0.0}),
        Evidence(measurements={"hypothesis_occurrences": 0.0, "hypothesis_average_return": 0.0}),
    ]
    knowledge_items = [
        Knowledge(
            statement="selected-from-evaluator-1",
            evidence_reference="evaluator-1",
            metadata={"hypothesis_occurrences": "1.0", "hypothesis_average_return": "0.0"},
        ),
        Knowledge(
            statement="selected-from-evaluator-2",
            evidence_reference="evaluator-2",
            metadata={"hypothesis_occurrences": "1.0", "hypothesis_average_return": "0.0"},
        ),
    ]

    selection_service = CandidateEdgeSelectionService(
        CandidateEdgeSelectionConfig(min_occurrences=1, min_average_return_abs=0.0)
    )
    report = DiscoveryReportService(selection_service=selection_service).create_report(
        hypotheses,
        evidences,
        validation_evidences=validation_evidences,
        knowledge_items=knowledge_items,
        knowledge_by_hypothesis={"second": knowledge_items[1]},
    )

    assert report.summary is not None
    assert report.summary.candidate_edges == 1
    assert report.summary.candidate_edges_confirmed == 0
    assert report.summary.candidate_edges_rejected == 1
    assert report.summary.confirmation_rate == 0.0


def test_discovery_report_summary_keeps_candidate_edge_balance() -> None:
    hypotheses = [SimpleNamespace(statement="first"), SimpleNamespace(statement="second")]
    evidences = [
        Evidence(measurements={"hypothesis_occurrences": 2.0, "hypothesis_average_return": 0.01}),
        Evidence(measurements={"hypothesis_occurrences": 1.0, "hypothesis_average_return": 0.0}),
    ]
    validation_evidences = [
        Evidence(measurements={"hypothesis_occurrences": 1.0, "hypothesis_average_return": 0.0}),
        Evidence(measurements={"hypothesis_occurrences": 0.0, "hypothesis_average_return": 0.0}),
    ]
    knowledge_items = [
        Knowledge(
            statement="selected-from-evaluator",
            evidence_reference="evaluator-1",
            metadata={"hypothesis_occurrences": "1.0", "hypothesis_average_return": "0.0"},
        )
    ]

    selection_service = CandidateEdgeSelectionService(
        CandidateEdgeSelectionConfig(min_occurrences=1, min_average_return_abs=0.0)
    )
    report = DiscoveryReportService(selection_service=selection_service).create_report(
        hypotheses,
        evidences,
        validation_evidences=validation_evidences,
        knowledge_items=knowledge_items,
        knowledge_by_hypothesis={"second": knowledge_items[0]},
    )

    assert report.summary is not None
    assert report.summary.candidate_edges == 1
    assert report.summary.candidate_edges_confirmed + report.summary.candidate_edges_rejected == report.summary.candidate_edges


def hypothesis_to_experiment(hypothesis):
    from edge.domain.experiment import Experiment
    from edge.domain.experiment_status import ExperimentStatus
    from edge.domain.research_configuration import ResearchConfiguration

    return Experiment(
        hypothesis=hypothesis,
        configuration=ResearchConfiguration(name="baseline"),
        status=ExperimentStatus.CREATED,
    )
