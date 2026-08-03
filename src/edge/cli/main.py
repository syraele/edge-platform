from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Sequence

from edge.application.research.pipeline import ResearchPipeline
from edge.application.research.runner import ExperimentRunner
from edge.application.research.session import ResearchSession
from edge.data import DatasetProviderRegistry, DatasetQuery
from edge.data.providers.filesystem_csv_provider import FilesystemCsvDatasetProvider
from edge.data.providers.local_dataset_registry import LocalDatasetRegistry
from edge.domain.services import ExperimentExecutor, ResearchEvaluator
from edge.domain.services.edge_classifier import EdgeClassifier
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
    research_parser.add_argument("--provider", default="filesystem-csv")
    research_parser.add_argument("--symbol", required=True)
    research_parser.add_argument("--timeframe", required=True)
    research_parser.add_argument("--from", dest="start", required=True)
    research_parser.add_argument("--to", dest="end", required=True)
    research_parser.add_argument("--validation-provider")
    research_parser.add_argument("--validation-symbol")
    research_parser.add_argument("--validation-timeframe")
    research_parser.add_argument("--validation-from", dest="validation_start")
    research_parser.add_argument("--validation-to", dest="validation_end")
    research_parser.add_argument("--validation-only", action="store_true")

    dataset_parser = subparsers.add_parser("dataset")
    dataset_subparsers = dataset_parser.add_subparsers(dest="dataset_command", required=True)

    verify_parser = dataset_subparsers.add_parser("verify")
    verify_parser.add_argument("--path", required=True)

    dataset_subparsers.add_parser("list")

    return parser


def _format_metric(value: float) -> str:
    if value == 0:
        return "0"

    if abs(value) >= 1e-6:
        return f"{value:.6f}".rstrip("0").rstrip(".")

    if abs(value) >= 1e-9:
        return f"{value:.9f}".rstrip("0").rstrip(".")

    return format(value, ".6g")


def _format_reason(source_row, item) -> str:
    reasons: list[str] = []

    if source_row is not None:
        if source_row.occurrences >= 3.0:
            reasons.append("occurrences above threshold")
        if source_row.average_return_10 != 0.0:
            reasons.append("positive 10-bar return")
        if source_row.average_return_5 != 0.0:
            reasons.append("positive 5-bar return")
        if source_row.average_return_1 != 0.0:
            reasons.append("positive 1-bar return")
        if source_row.win_rate > 0.5:
            reasons.append("win rate above 50%")
        if source_row.expectancy > 0.0:
            reasons.append("positive expectancy")
        if source_row.profit_factor > 1.0:
            reasons.append("profit factor above 1")
        if item.score > 0.0:
            reasons.append("positive edge score")

    if not reasons:
        reasons.append("weak but non-zero signal")

    return "; ".join(reasons)


def _format_discovery_report(report, query) -> str:
    if not hasattr(report, "rows"):
        return str(report)

    ranking_service = EdgeScoringService()
    ranked_rows = ranking_service.rank_rows(report.rows)
    strongest_rows = [
        item
        for item in ranked_rows
        if item.score > 0.0 and (item.occurrences >= 3.0 or item.average_return != 0.0)
    ]
    items = strongest_rows[:10]
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

    summary = getattr(report, "selection_summary", None)
    if summary is not None:
        lines.append("=" * 50)
        lines.append("Candidate Edge Selection")
        lines.append("=" * 50)
        lines.append("")
        lines.append(f"Knowledge generate: {getattr(summary, 'generated_count', 0)}")
        lines.append("")
        lines.append(f"Knowledge scartate: {getattr(summary, 'rejected_count', 0)}")
        lines.append("")
        lines.append(f"Candidate Edge: {getattr(summary, 'selected_count', 0)}")
        lines.append("")
        rejections = getattr(summary, "rejections", ()) or ()
        if rejections:
            lines.append("Rejected:")
            for rejection in rejections:
                lines.append(f"- {getattr(rejection.knowledge, 'statement', 'unknown')}")
                lines.append(f"  Motivo: {getattr(rejection, 'reason', 'unknown')}")
                lines.append("")
            lines.append("-" * 50)
            lines.append("")

    knowledge = getattr(report, "knowledge", None)
    if knowledge is not None:
        classifier = EdgeClassifier()
        validation = classifier.classify(knowledge)
        lines.append("=" * 50)
        lines.append("Knowledge")
        lines.append("=" * 50)
        lines.append("")
        lines.append(f"Statement: {knowledge.statement}")
        lines.append("")
        lines.append(f"Quality: {validation.label}")
        lines.append("")
        lines.append(f"Score: {validation.score:.3f}")
        lines.append("")
        lines.append("-" * 50)
        lines.append("")

    summary = getattr(report, "summary", None)
    if summary is not None:
        lines.append("=" * 50)
        lines.append("Final Summary")
        lines.append("=" * 50)
        lines.append("")
        lines.append(f"Hypotheses generated: {getattr(summary, 'hypotheses_generated', 0)}")
        lines.append("")
        lines.append(f"Knowledge generated: {getattr(summary, 'knowledge_generated', 0)}")
        lines.append("")
        lines.append(f"Candidate Edge: {getattr(summary, 'candidate_edges', 0)}")
        lines.append("")
        lines.append(f"Confirmed: {getattr(summary, 'candidate_edges_confirmed', 0)}")
        lines.append("")
        lines.append(f"Rejected: {getattr(summary, 'candidate_edges_rejected', 0)}")
        lines.append("")
        lines.append(f"Confirmation rate: {getattr(summary, 'confirmation_rate', 0.0):.2f}%")
        lines.append("")
        lines.append("-" * 50)
        lines.append("")

    if items:
        top_edge = items[0]
        lines.append("=" * 50)
        lines.append("Candidate Edge")
        lines.append("=" * 50)
        lines.append("")
        lines.append("Hypothesis")
        lines.append(top_edge.hypothesis_name.replace(" AND ", "\nAND\n"))
        lines.append("")
        lines.append("Occurrences")
        lines.append(_format_metric(top_edge.occurrences))
        lines.append("")
        lines.append("Average Return")
        lines.append(_format_metric(top_edge.average_return))
        lines.append("")
        lines.append("Edge Score")
        lines.append(_format_metric(top_edge.score))
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

        lines.append("Discovery Metrics")
        lines.append("Average Return 5")
        lines.append(_format_metric(source_row.average_return_5 if source_row else 0.0))
        lines.append("")
        lines.append("Average Return 10")
        lines.append(_format_metric(source_row.average_return_10 if source_row else 0.0))
        lines.append("")
        lines.append("Average Return 20")
        lines.append(_format_metric(source_row.average_return_20 if source_row else 0.0))
        lines.append("")
        lines.append("Win Rate")
        lines.append(_format_metric(source_row.win_rate if source_row else 0.0))
        lines.append("")
        lines.append("Expectancy")
        lines.append(_format_metric(source_row.expectancy if source_row else 0.0))
        lines.append("")
        lines.append("Profit Factor")
        lines.append(_format_metric(source_row.profit_factor if source_row else 0.0))
        lines.append("")
        lines.append("Payoff")
        lines.append(_format_metric(source_row.payoff if source_row else 0.0))
        lines.append("")
        lines.append("Drawdown")
        lines.append(_format_metric(source_row.drawdown if source_row else 0.0))
        lines.append("")
        lines.append("Validation Metrics")
        lines.append("Occurrences")
        lines.append(_format_metric(source_row.validation_occurrences if source_row else 0.0))
        lines.append("")
        lines.append("Average Return")
        lines.append(_format_metric(source_row.validation_average_return if source_row else 0.0))
        lines.append("")
        lines.append("Average Return 5")
        lines.append(_format_metric(source_row.validation_average_return_5 if source_row else 0.0))
        lines.append("")
        lines.append("Average Return 10")
        lines.append(_format_metric(source_row.validation_average_return_10 if source_row else 0.0))
        lines.append("")
        lines.append("Average Return 20")
        lines.append(_format_metric(source_row.validation_average_return_20 if source_row else 0.0))
        lines.append("")
        lines.append("Win Rate")
        lines.append(_format_metric(source_row.validation_win_rate if source_row else 0.0))
        lines.append("")
        lines.append("Expectancy")
        lines.append(_format_metric(source_row.validation_expectancy if source_row else 0.0))
        lines.append("")
        lines.append("Profit Factor")
        lines.append(_format_metric(source_row.validation_profit_factor if source_row else 0.0))
        lines.append("")
        lines.append("Payoff")
        lines.append(_format_metric(source_row.validation_payoff if source_row else 0.0))
        lines.append("")
        lines.append("Drawdown")
        lines.append(_format_metric(source_row.validation_drawdown if source_row else 0.0))
        lines.append("")
        lines.append("Status")
        lines.append("confirmed" if (source_row.confirmed if source_row else False) else "rejected")
        lines.append("")
        lines.append("Edge Score")
        lines.append(_format_metric(item.score))
        lines.append("")
        lines.append("Why it was selected")
        lines.append(_format_reason(source_row, item))
        lines.append("")
        lines.append("-" * 50)
        lines.append("")

    return "\n".join(lines).rstrip()


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "dataset":
        if args.dataset_command == "verify":
            registry = LocalDatasetRegistry(base_path=Path(args.path))
            result = registry.verify(args.path)
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0

        if args.dataset_command == "list":
            registry = LocalDatasetRegistry(base_path=Path("data/datasets"))
            datasets = registry.list_datasets()
            for entry in datasets:
                print(entry)
            return 0

        parser.error("unsupported dataset command")
        return 1

    if args.command != "research":
        parser.error("unsupported command")
        return 1

    registry = DatasetProviderRegistry()
    registry.register(FilesystemCsvDatasetProvider(base_path=Path("data/datasets")))

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

    validation_query = None
    if args.validation_symbol and args.validation_timeframe:
        validation_query = DatasetQuery(
            symbol=args.validation_symbol,
            timeframe=args.validation_timeframe,
            start=_parse_date(args.validation_start) if args.validation_start else None,
            end=_parse_date(args.validation_end) if args.validation_end else None,
            provider_id=args.validation_provider or args.provider,
        )
    elif args.validation_start or args.validation_end:
        validation_query = DatasetQuery(
            symbol=args.symbol,
            timeframe=args.timeframe,
            start=_parse_date(args.validation_start) if args.validation_start else None,
            end=_parse_date(args.validation_end) if args.validation_end else None,
            provider_id=args.provider,
        )

    report = pipeline.execute_discovery(query, ResearchSession(), validation_query=validation_query)
    print(_format_discovery_report(report, query))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
