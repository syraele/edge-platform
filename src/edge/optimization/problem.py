from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from edge.domain.experiment import Experiment


@dataclass(frozen=True, slots=True)
class OptimizationConstraint:
    """Declarative optimization constraint for evidence-based evaluation."""

    metric_name: str
    minimum: float | None = None
    maximum: float | None = None


@dataclass(frozen=True, slots=True)
class OptimizationProblem:
    """Declarative optimization problem for research-oriented evaluation."""

    problem_id: str
    objective_name: str
    experiments: tuple[Experiment, ...]
    constraints: tuple[OptimizationConstraint, ...] = ()
    assumptions: tuple[str, ...] = ()
    maximize: bool = True

    @property
    def fingerprint(self) -> str:
        payload = {
            "problem_id": self.problem_id,
            "objective_name": self.objective_name,
            "maximize": self.maximize,
            "constraints": [
                {
                    "metric_name": constraint.metric_name,
                    "minimum": constraint.minimum,
                    "maximum": constraint.maximum,
                }
                for constraint in self.constraints
            ],
            "assumptions": list(self.assumptions),
            "experiments": [
                experiment.configuration.name for experiment in self.experiments
            ],
        }
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()
