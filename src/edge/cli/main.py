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
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
