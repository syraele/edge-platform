import json
from datetime import UTC, datetime
from pathlib import Path

import edge.cli.main as cli_main
from edge.domain.knowledge import Knowledge
from edge.domain.services.candidate_edge_selection import CandidateEdgeSelectionResult
from edge.domain.services.discovery_report import DiscoveryReport, DiscoveryReportRow


class DummyRegistry:
    def __init__(self) -> None:
        self.registered = []

    def register(self, provider) -> None:
        self.registered.append(provider)


def test_research_command_uses_filesystem_provider_by_default(monkeypatch, capsys) -> None:
    recorded = {}

    class DummyPipeline:
        def __init__(self, **kwargs) -> None:
            self.kwargs = kwargs
            self.calls = []

        def execute_discovery(self, query, session, validation_query=None):
            self.calls.append((query, session, validation_query))
            return "report"

    def fake_pipeline(**kwargs):
        recorded["kwargs"] = kwargs
        return DummyPipeline(**kwargs)

    monkeypatch.setattr(cli_main, "ResearchPipeline", fake_pipeline)
    monkeypatch.setattr(cli_main, "DatasetProviderRegistry", DummyRegistry)
    monkeypatch.setattr(cli_main, "FilesystemCsvDatasetProvider", lambda base_path=None: object())
    monkeypatch.setattr(cli_main, "ExperimentRunner", lambda executor: executor)
    monkeypatch.setattr(cli_main, "ExperimentExecutor", lambda: object())
    monkeypatch.setattr(cli_main, "ResearchEvaluator", lambda: object())
    monkeypatch.setattr(cli_main, "ResearchSession", lambda: object())

    exit_code = cli_main.main(
        [
            "research",
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


def test_dataset_verify_command_reports_manifest_metadata(tmp_path: Path, monkeypatch, capsys) -> None:
    dataset_dir = tmp_path / "eurusd" / "m1" / "v2026-08-03"
    dataset_dir.mkdir(parents=True)
    manifest = {
        "dataset_id": "eurusd-m1-v2026-08-03",
        "symbol": "EURUSD",
        "timeframe": "M1",
        "version": "v2026-08-03",
        "source": "mt5-import",
        "file": "bars.csv",
        "bars_count": 2,
        "range_start": "2024-01-01T00:00:00+00:00",
        "range_end": "2024-01-01T01:00:00+00:00",
    }
    (dataset_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (dataset_dir / "bars.csv").write_text(
        "timestamp,open,high,low,close,volume\n"
        "2024-01-01T00:00:00,1.1000,1.1010,1.0990,1.1005,100\n"
        "2024-01-01T01:00:00,1.2000,1.2050,1.1950,1.2012,110\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(cli_main, "Path", lambda *args, **kwargs: tmp_path / Path(*args))

    cli_main.main(["dataset", "verify", "--path", str(dataset_dir)])

    output = capsys.readouterr().out
    assert "dataset_id" in output
    assert "eurusd-m1-v2026-08-03" in output
    assert "bars_count" in output
    assert "2" in output


def test_dataset_list_command_lists_available_datasets(tmp_path: Path, monkeypatch, capsys) -> None:
    dataset_dir = tmp_path / "data" / "datasets" / "eurusd" / "m1" / "v2026-08-03"
    dataset_dir.mkdir(parents=True)
    (dataset_dir / "manifest.json").write_text(
        json.dumps(
            {
                "dataset_id": "eurusd-m1-v2026-08-03",
                "symbol": "EURUSD",
                "timeframe": "M1",
                "version": "v2026-08-03",
                "source": "mt5-import",
                "file": "bars.csv",
                "bars_count": 1,
            }
        ),
        encoding="utf-8",
    )
    (dataset_dir / "bars.csv").write_text(
        "timestamp,open,high,low,close,volume\n2024-01-01T00:00:00,1.1,1.2,1.0,1.15,100\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    cli_main.main(["dataset", "list"])

    output = capsys.readouterr().out
    assert "EURUSD" in output
    assert "M1" in output
    assert "v2026-08-03" in output


def test_research_command_loads_manifest_backed_dataset_end_to_end(tmp_path: Path, monkeypatch, capsys) -> None:
    dataset_dir = tmp_path / "data" / "datasets" / "eurusd" / "m1" / "v2026-08-03"
    dataset_dir.mkdir(parents=True)
    (dataset_dir / "manifest.json").write_text(
        json.dumps(
            {
                "dataset_id": "eurusd-m1-v2026-08-03",
                "symbol": "EURUSD",
                "timeframe": "M1",
                "version": "v2026-08-03",
                "source": "mt5-import",
                "file": "bars.csv",
                "bars_count": 1,
            }
        ),
        encoding="utf-8",
    )
    (dataset_dir / "bars.csv").write_text(
        "timestamp,open,high,low,close,volume\n2024-01-01T00:00:00,1.1,1.2,1.0,1.15,100\n",
        encoding="utf-8",
    )

    recorded = {}

    class DummyPipeline:
        def __init__(self, **kwargs) -> None:
            self.kwargs = kwargs

        def execute_discovery(self, query, session, validation_query=None):
            loaded = self.kwargs["registry"].load(query)
            recorded["symbol"] = loaded.dataset.metadata.symbol
            return "report"

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli_main, "ResearchPipeline", lambda **kwargs: DummyPipeline(**kwargs))
    monkeypatch.setattr(cli_main, "ExperimentRunner", lambda executor: executor)
    monkeypatch.setattr(cli_main, "ExperimentExecutor", lambda: object())
    monkeypatch.setattr(cli_main, "ResearchEvaluator", lambda: object())
    monkeypatch.setattr(cli_main, "ResearchSession", lambda: object())

    exit_code = cli_main.main(
        [
            "research",
            "--symbol",
            "EURUSD",
            "--timeframe",
            "M1",
            "--from",
            "2024-01-01",
            "--to",
            "2024-01-02",
        ]
    )

    assert exit_code == 0
    assert recorded["symbol"] == "EURUSD"
    assert capsys.readouterr().out.strip() == "report"


def test_research_command_defaults_validation_query_to_primary_dataset(monkeypatch, capsys) -> None:
    recorded = {}

    class DummyPipeline:
        def __init__(self, **kwargs) -> None:
            self.kwargs = kwargs
            self.calls = []

        def execute_discovery(self, query, session, validation_query=None):
            recorded["query"] = query
            recorded["validation_query"] = validation_query
            return "report"

    monkeypatch.setattr(cli_main, "ResearchPipeline", lambda **kwargs: DummyPipeline(**kwargs))
    monkeypatch.setattr(cli_main, "DatasetProviderRegistry", DummyRegistry)
    monkeypatch.setattr(cli_main, "FilesystemCsvDatasetProvider", lambda base_path=None: object())
    monkeypatch.setattr(cli_main, "ExperimentRunner", lambda executor: executor)
    monkeypatch.setattr(cli_main, "ExperimentExecutor", lambda: object())
    monkeypatch.setattr(cli_main, "ResearchEvaluator", lambda: object())
    monkeypatch.setattr(cli_main, "ResearchSession", lambda: object())

    exit_code = cli_main.main(
        [
            "research",
            "--symbol",
            "EURUSD",
            "--timeframe",
            "M1",
            "--from",
            "2024-01-01",
            "--to",
            "2024-01-02",
            "--validation-from",
            "2024-01-03",
            "--validation-to",
            "2024-01-04",
        ]
    )

    assert exit_code == 0
    assert recorded["validation_query"].symbol == "EURUSD"
    assert recorded["validation_query"].timeframe == "M1"
    assert recorded["validation_query"].provider_id == "filesystem-csv"
    assert recorded["validation_query"].start == datetime(2024, 1, 3, tzinfo=UTC)
    assert recorded["validation_query"].end == datetime(2024, 1, 4, tzinfo=UTC)


def test_research_command_builds_query_and_runs_pipeline(monkeypatch, capsys) -> None:
    recorded = {}

    class DummyPipeline:
        def __init__(self, **kwargs) -> None:
            self.kwargs = kwargs
            self.calls = []

        def execute_discovery(self, query, session, validation_query=None):
            self.calls.append((query, session, validation_query))
            return "report"

    def fake_pipeline(**kwargs):
        recorded["kwargs"] = kwargs
        return DummyPipeline(**kwargs)

    monkeypatch.setattr(cli_main, "ResearchPipeline", fake_pipeline)
    monkeypatch.setattr(cli_main, "DatasetProviderRegistry", DummyRegistry)
    monkeypatch.setattr(cli_main, "FilesystemCsvDatasetProvider", lambda base_path=None: object())
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

        def execute_discovery(self, query, session, validation_query=None):
            return DiscoveryReport(rows=DummyReport.rows)

    monkeypatch.setattr(cli_main, "ResearchPipeline", lambda **kwargs: DummyPipeline(**kwargs))
    monkeypatch.setattr(cli_main, "DatasetProviderRegistry", DummyRegistry)
    monkeypatch.setattr(cli_main, "FilesystemCsvDatasetProvider", lambda base_path=None: object())
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


def test_research_command_renders_explicit_candidate_edge(monkeypatch, capsys) -> None:
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

        def execute_discovery(self, query, session, validation_query=None):
            return DiscoveryReport(rows=DummyReport.rows)

    monkeypatch.setattr(cli_main, "ResearchPipeline", lambda **kwargs: DummyPipeline(**kwargs))
    monkeypatch.setattr(cli_main, "DatasetProviderRegistry", DummyRegistry)
    monkeypatch.setattr(cli_main, "FilesystemCsvDatasetProvider", lambda base_path=None: object())
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
    assert "Candidate Edge" in output
    assert "close > previous_close" in output
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
                confirmed=True,
            ),
        )

    class DummyPipeline:
        def __init__(self, **kwargs) -> None:
            self.kwargs = kwargs

        def execute_discovery(self, query, session, validation_query=None):
            return DiscoveryReport(
                rows=DummyReport.rows,
                knowledge=Knowledge(statement="selected-knowledge"),
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
    monkeypatch.setattr(cli_main, "FilesystemCsvDatasetProvider", lambda base_path=None: object())
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


def test_research_command_renders_final_summary(monkeypatch, capsys) -> None:
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
                confirmed=True,
            ),
            DiscoveryReportRow(
                hypothesis_name="close > previous_close",
                occurrences=12.0,
                average_return=0.002,
                average_return_1=0.0,
                average_return_5=0.0,
                average_return_10=0.0,
                average_return_20=0.0,
                confirmed=False,
            ),
        )

    class DummyPipeline:
        def __init__(self, **kwargs) -> None:
            self.kwargs = kwargs

        def execute_discovery(self, query, session, validation_query=None):
            return DiscoveryReport(
                rows=DummyReport.rows,
                knowledge=Knowledge(statement="selected-knowledge"),
                selection_summary=type(
                    "Summary",
                    (),
                    {
                        "generated_count": 3,
                        "rejected_count": 1,
                        "selected_count": 2,
                        "rejections": (),
                    },
                )(),
                summary=type(
                    "SummaryData",
                    (),
                    {
                        "hypotheses_generated": 2,
                        "knowledge_generated": 1,
                        "candidate_edges": 2,
                        "candidate_edges_confirmed": 1,
                        "candidate_edges_rejected": 1,
                        "confirmation_rate": 50.0,
                    },
                )(),
            )

    monkeypatch.setattr(cli_main, "ResearchPipeline", lambda **kwargs: DummyPipeline(**kwargs))
    monkeypatch.setattr(cli_main, "DatasetProviderRegistry", DummyRegistry)
    monkeypatch.setattr(cli_main, "FilesystemCsvDatasetProvider", lambda base_path=None: object())
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
    assert "Final Summary" in output
    assert "Hypotheses generated: 2" in output
    assert "Knowledge generated: 1" in output
    assert "Candidate Edge: 2" in output
    assert "Confirmed: 1" in output
    assert "Rejected: 1" in output
    assert "Confirmation rate: 50.00%" in output
