from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from edge.domain.evidence import Evidence
from edge.domain.experiment import Experiment


@dataclass(frozen=True, slots=True)
class OptimizationCandidateResult:
    """Result of evaluating a single experiment for an optimization problem."""

    experiment: Experiment
    objective_value: float | None
    evidence: Evidence | None
    knowledge: object | None
    constraint_violations: tuple[str, ...] = ()
    message: str | None = None

    @property
    def succeeded(self) -> bool:
        return (
            self.message is None
            and self.objective_value is not None
            and not self.constraint_violations
        )


@dataclass(frozen=True, slots=True)
class OptimizationReport:
    """Deterministic, traceable output of an optimization run."""

    problem_id: str
    problem_fingerprint: str
    status: str
    objective_name: str
    maximize: bool
    constraints: tuple[object, ...]
    assumptions: tuple[str, ...]
    candidates: tuple[OptimizationCandidateResult, ...]
    evaluated_configurations: tuple[str, ...]
    ranking: tuple[str, ...]
    winner_configuration: str | None
    best_objective_value: float | None
    succeeded_candidates: int
    failed_candidates: int
    failure_messages: tuple[str, ...]
    run_fingerprint: str
    created_at: datetime = field(default_factory=datetime.utcnow)
