from __future__ import annotations

import argparse
from datetime import UTC, datetime
from typing import Sequence

from edge.application.research.pipeline import ResearchPipeline
from edge.application.research.runner import ExperimentRunner
from edge.application.research.session import ResearchSession
from edge.data import DatasetProviderRegistry, DatasetQuery
from edge.data.providers.mt5_provider import Mt5DatasetProvider
from edge.domain.services import ExperimentExecutor, ResearchEvaluator
from edge.domain.services.edge_scoring import EdgeScoringService


def _parse_date(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        parsed = datetime.strptime(value, "%Y-%m-%d")

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)

    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="edge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    research_parser = subparsers.add_parser("research")
    research_parser.add_argument("--provider", default="mt5")
    research_parser.add_argument("--symbol", required=True)
    research_parser.add_argument("--timeframe", required=True)
    research_parser.add_argument("--from", dest="start", required=True)
    research_parser.add_argument("--to", dest="end", required=True)

    return parser


def _format_metric(value: float) -> str:
    if value == 0:
        return "0"

    if abs(value) >= 1e-6:
        return f"{value:.6f}".rstrip("0").rstrip(".")

    if abs(value) >= 1e-9:
        return f"{value:.9f}".rstrip("0").rstrip(".")

    return format(value, ".6g")


def _format_discovery_report(report, query) -> str:
    if not hasattr(report, "rows"):
        return str(report)

    ranking_service = EdgeScoringService()
    ranked_rows = ranking_service.rank_rows(report.rows)
    items = ranked_rows[:10]
    source_rows_by_name = {row.hypothesis_name: row for row in report.rows}

    lines: list[str] = []
    lines.append("=" * 50)
    lines.append("EDGE_ENGINE Discovery Report")
    lines.append("=" * 50)
    lines.append("")
    lines.append("Dataset:")
    lines.append(f"Provider : {query.provider_id}")
    lines.append(f"Symbol   : {query.symbol}")
    lines.append(f"Timeframe: {query.timeframe}")
    lines.append("")
    lines.append("Periodo:")
    lines.append(query.start.date().isoformat())
    lines.append(query.end.date().isoformat())
    lines.append("")
    lines.append("-" * 50)
    lines.append("")

    for index, item in enumerate(items, start=1):
        lines.append(f"Rank #{index}")
        lines.append("")
        lines.append("Hypothesis")
        lines.append(item.hypothesis_name.replace(" AND ", "\nAND\n"))
        lines.append("")
        lines.append("Occurrences")
        lines.append(_format_metric(item.occurrences))
        lines.append("")
        lines.append("Average Return")
        lines.append(_format_metric(item.average_return))
        lines.append("")
        source_row = source_rows_by_name.get(item.hypothesis_name)

        lines.append("Average Return 5")
        lines.append(_format_metric(source_row.average_return_5 if source_row else 0.0))
        lines.append("")
        lines.append("Average Return 10")
        lines.append(_format_metric(source_row.average_return_10 if source_row else 0.0))
        lines.append("")
        lines.append("Average Return 20")
        lines.append(_format_metric(source_row.average_return_20 if source_row else 0.0))
        lines.append("")
        lines.append("Edge Score")
        lines.append(_format_metric(item.score))
        lines.append("")
        lines.append("-" * 50)
        lines.append("")

    return "\n".join(lines).rstrip()


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command != "research":
        parser.error("unsupported command")
        return 1

    if args.provider != "mt5":
        parser.error("only the mt5 provider is currently supported")
        return 1

    registry = DatasetProviderRegistry()
    registry.register(Mt5DatasetProvider())

    pipeline = ResearchPipeline(
        runner=ExperimentRunner(ExperimentExecutor()),
        evaluator=ResearchEvaluator(),
        registry=registry,
    )

    query = DatasetQuery(
        symbol=args.symbol,
        timeframe=args.timeframe,
        start=_parse_date(args.start),
        end=_parse_date(args.end),
        provider_id=args.provider,
    )

    report = pipeline.execute_discovery(query, ResearchSession())
    print(_format_discovery_report(report, query))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
