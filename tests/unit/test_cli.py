from datetime import UTC, datetime

import edge.cli.main as cli_main
from edge.domain.knowledge import Knowledge
from edge.domain.services.candidate_edge_selection import CandidateEdgeSelectionResult
from edge.domain.services.discovery_report import DiscoveryReport, DiscoveryReportRow


class DummyRegistry:
    def __init__(self) -> None:
        self.registered = []

    def register(self, provider) -> None:
        self.registered.append(provider)


class DummyPipeline:
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs
        self.calls = []

    def execute_discovery(self, query, session):
        self.calls.append((query, session))
        return "report"


def test_research_command_builds_query_and_runs_pipeline(monkeypatch, capsys) -> None:
    recorded = {}

    def fake_pipeline(**kwargs):
        recorded["kwargs"] = kwargs
        return DummyPipeline(**kwargs)

    monkeypatch.setattr(cli_main, "ResearchPipeline", fake_pipeline)
    monkeypatch.setattr(cli_main, "DatasetProviderRegistry", DummyRegistry)
    monkeypatch.setattr(cli_main, "Mt5DatasetProvider", lambda: object())
    monkeypatch.setattr(cli_main, "ExperimentRunner", lambda executor: executor)
    monkeypatch.setattr(cli_main, "ExperimentExecutor", lambda: object())
    monkeypatch.setattr(cli_main, "ResearchEvaluator", lambda: object())
    monkeypatch.setattr(cli_main, "ResearchSession", lambda: object())

    exit_code = cli_main.main(
        [
            "research",
            "--provider",
            "mt5",
            "--symbol",
            "XAUUSD",
            "--timeframe",
            "M1",
            "--from",
            "2026-04-20",
            "--to",
            "2026-04-22",
        ]
    )

    assert exit_code == 0
    assert capsys.readouterr().out.strip() == "report"
    assert recorded["kwargs"]["registry"].registered[0] is not None

    pipeline = recorded["kwargs"]["runner"]
    assert pipeline is not None

    query = recorded["kwargs"]["registry"].registered[0]
    assert query is not None


def test_research_command_renders_human_readable_report(monkeypatch, capsys) -> None:
    class DummyReport:
        rows = (
            DiscoveryReportRow(
                hypothesis_name="close > open",
                occurrences=10.0,
                average_return=0.001,
                average_return_1=0.0,
                average_return_5=-0.000030892,
                average_return_10=0.0001985628647,
                average_return_20=0.000435917183,
            ),
            DiscoveryReportRow(
                hypothesis_name="close > previous_close",
                occurrences=12.0,
                average_return=0.002,
                average_return_1=0.0,
                average_return_5=0.0,
                average_return_10=0.0,
                average_return_20=0.0,
            ),
        )

    class DummyPipeline:
        def __init__(self, **kwargs) -> None:
            self.kwargs = kwargs

        def execute_discovery(self, query, session):
            return DiscoveryReport(rows=DummyReport.rows)

    monkeypatch.setattr(cli_main, "ResearchPipeline", lambda **kwargs: DummyPipeline(**kwargs))
    monkeypatch.setattr(cli_main, "DatasetProviderRegistry", DummyRegistry)
    monkeypatch.setattr(cli_main, "Mt5DatasetProvider", lambda: object())
    monkeypatch.setattr(cli_main, "ExperimentRunner", lambda executor: executor)
    monkeypatch.setattr(cli_main, "ExperimentExecutor", lambda: object())
    monkeypatch.setattr(cli_main, "ResearchEvaluator", lambda: object())
    monkeypatch.setattr(cli_main, "ResearchSession", lambda: object())

    cli_main.main(
        [
            "research",
            "--provider",
            "mt5",
            "--symbol",
            "XAUUSD",
            "--timeframe",
            "M1",
            "--from",
            "2026-04-20",
            "--to",
            "2026-04-22",
        ]
    )

    output = capsys.readouterr().out
    assert "EDGE_ENGINE Discovery Report" in output
    assert "Rank #1" in output
    assert "close > previous_close" in output
    assert "Rank #2" in output
    assert "close > open" in output
    assert "-0.000031" in output
    assert "0.000199" in output
    assert "0.000436" in output
    assert "Win Rate" in output
    assert "Expectancy" in output
    assert "Profit Factor" in output
    assert "Payoff" in output
    assert "Drawdown" in output
    assert "Edge Score" in output


def test_research_command_renders_candidate_edge_selection_summary(monkeypatch, capsys) -> None:
    class DummyReport:
        rows = (
            DiscoveryReportRow(
                hypothesis_name="close > open",
                occurrences=10.0,
                average_return=0.001,
                average_return_1=0.0,
                average_return_5=-0.000030892,
                average_return_10=0.0001985628647,
                average_return_20=0.000435917183,
            ),
        )

    class DummyPipeline:
        def __init__(self, **kwargs) -> None:
            self.kwargs = kwargs

        def execute_discovery(self, query, session):
            return DiscoveryReport(
                rows=DummyReport.rows,
                selection_summary=type(
                    "Summary",
                    (),
                    {
                        "generated_count": 3,
                        "rejected_count": 2,
                        "selected_count": 1,
                        "rejections": (
                            CandidateEdgeSelectionResult(
                                knowledge=Knowledge(statement="rejected-1"),
                                is_selected=False,
                                reason="min_occurrences",
                            ),
                            CandidateEdgeSelectionResult(
                                knowledge=Knowledge(statement="rejected-2"),
                                is_selected=False,
                                reason="min_average_return_abs",
                            ),
                        ),
                    },
                )(),
            )

    monkeypatch.setattr(cli_main, "ResearchPipeline", lambda **kwargs: DummyPipeline(**kwargs))
    monkeypatch.setattr(cli_main, "DatasetProviderRegistry", DummyRegistry)
    monkeypatch.setattr(cli_main, "Mt5DatasetProvider", lambda: object())
    monkeypatch.setattr(cli_main, "ExperimentRunner", lambda executor: executor)
    monkeypatch.setattr(cli_main, "ExperimentExecutor", lambda: object())
    monkeypatch.setattr(cli_main, "ResearchEvaluator", lambda: object())
    monkeypatch.setattr(cli_main, "ResearchSession", lambda: object())

    cli_main.main(
        [
            "research",
            "--provider",
            "mt5",
            "--symbol",
            "XAUUSD",
            "--timeframe",
            "M1",
            "--from",
            "2026-04-20",
            "--to",
            "2026-04-22",
        ]
    )

    output = capsys.readouterr().out
    assert "Candidate Edge Selection" in output
    assert "Knowledge generate: 3" in output
    assert "Knowledge scartate: 2" in output
    assert "Candidate Edge: 1" in output
    assert "Rejected:" in output
    assert "min_occurrences" in output
    assert "min_average_return_abs" in output
