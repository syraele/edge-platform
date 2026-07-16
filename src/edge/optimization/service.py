from __future__ import annotations

import hashlib
import json
from typing import Any

from edge.domain.evidence import Evidence
from edge.domain.services.research_evaluator import ResearchEvaluator

from .problem import OptimizationConstraint, OptimizationProblem
from .report import OptimizationCandidateResult, OptimizationReport


class OptimizationError(ValueError):
    """Raised when an optimization problem cannot be evaluated."""


class OptimizationService:
    """Research-oriented optimization orchestration service."""

    def __init__(
        self,
        runner: Any,
        evaluator: ResearchEvaluator,
    ) -> None:
        self._runner = runner
        self._evaluator = evaluator

    def optimize(self, problem: OptimizationProblem) -> OptimizationReport:
        if not problem.experiments:
            raise OptimizationError(
                "Optimization problem requires at least one experiment"
            )

        candidates: list[OptimizationCandidateResult] = []

        for experiment in problem.experiments:
            try:
                evidence = self._runner.run(experiment)
                objective_value = evidence.measurements.get(problem.objective_name)

                if objective_value is None:
                    raise OptimizationError(
                        f"Objective '{problem.objective_name}' missing from evidence"
                    )

                constraint_violations = self._evaluate_constraints(
                    evidence,
                    problem.constraints,
                )

                knowledge = self._evaluator.evaluate(evidence)

                candidates.append(
                    OptimizationCandidateResult(
                        experiment=experiment,
                        objective_value=objective_value,
                        evidence=evidence,
                        knowledge=knowledge,
                        constraint_violations=constraint_violations,
                    )
                )
            except Exception as exc:  # noqa: BLE001 - candidate failures are contained.
                candidates.append(
                    OptimizationCandidateResult(
                        experiment=experiment,
                        objective_value=None,
                        evidence=None,
                        knowledge=None,
                        message=str(exc),
                    )
                )

        ranking = tuple(
            candidate.experiment.configuration.name
            for candidate in sorted(
                candidates,
                key=lambda candidate: self._ranking_key(candidate, problem.maximize),
            )
        )

        evaluated_configurations = tuple(
            candidate.experiment.configuration.name for candidate in candidates
        )

        succeeded_candidates = sum(1 for candidate in candidates if candidate.succeeded)
        failed_candidates = len(candidates) - succeeded_candidates
        failure_messages = tuple(
            candidate.message
            for candidate in candidates
            if candidate.message is not None
        )

        winner_configuration = None
        best_objective_value = None
        for candidate in sorted(
            candidates,
            key=lambda candidate: self._ranking_key(candidate, problem.maximize),
        ):
            if candidate.succeeded:
                winner_configuration = candidate.experiment.configuration.name
                best_objective_value = candidate.objective_value
                break

        status = "completed" if winner_configuration is not None else "failed"

        return OptimizationReport(
            problem_id=problem.problem_id,
            problem_fingerprint=problem.fingerprint,
            status=status,
            objective_name=problem.objective_name,
            maximize=problem.maximize,
            constraints=problem.constraints,
            assumptions=problem.assumptions,
            candidates=tuple(candidates),
            evaluated_configurations=evaluated_configurations,
            ranking=ranking,
            winner_configuration=winner_configuration,
            best_objective_value=best_objective_value,
            succeeded_candidates=succeeded_candidates,
            failed_candidates=failed_candidates,
            failure_messages=failure_messages,
            run_fingerprint=self._build_run_fingerprint(
                problem=problem,
                ranking=ranking,
                winner_configuration=winner_configuration,
                best_objective_value=best_objective_value,
                candidates=tuple(candidates),
            ),
        )

    @staticmethod
    def _ranking_key(
        candidate: OptimizationCandidateResult,
        maximize: bool,
    ) -> tuple[int, float, str]:
        if not candidate.succeeded:
            return (1, 0.0, candidate.experiment.configuration.name)

        objective_value = candidate.objective_value or 0.0
        ranked_value = -objective_value if maximize else objective_value

        return (0, ranked_value, candidate.experiment.configuration.name)

    @staticmethod
    def _evaluate_constraints(
        evidence: Evidence,
        constraints: tuple[OptimizationConstraint, ...],
    ) -> tuple[str, ...]:
        violations: list[str] = []

        for constraint in constraints:
            value = evidence.measurements.get(constraint.metric_name)

            if value is None:
                violations.append(
                    f"Constraint metric '{constraint.metric_name}' missing"
                )
                continue

            if constraint.minimum is not None and value < constraint.minimum:
                violations.append(
                    f"{constraint.metric_name} below minimum {constraint.minimum}"
                )

            if constraint.maximum is not None and value > constraint.maximum:
                violations.append(
                    f"{constraint.metric_name} above maximum {constraint.maximum}"
                )

        return tuple(violations)

    @staticmethod
    def _build_run_fingerprint(
        *,
        problem: OptimizationProblem,
        ranking: tuple[str, ...],
        winner_configuration: str | None,
        best_objective_value: float | None,
        candidates: tuple[OptimizationCandidateResult, ...],
    ) -> str:
        payload = {
            "problem_fingerprint": problem.fingerprint,
            "ranking": list(ranking),
            "winner_configuration": winner_configuration,
            "best_objective_value": best_objective_value,
            "candidates": [
                {
                    "configuration": candidate.experiment.configuration.name,
                    "objective_value": candidate.objective_value,
                    "constraint_violations": list(candidate.constraint_violations),
                    "message": candidate.message,
                }
                for candidate in candidates
            ],
        }
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()
