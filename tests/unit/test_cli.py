from datetime import UTC, datetime

import edge.cli.main as cli_main


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
