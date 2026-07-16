from __future__ import annotations

import hashlib
import json
from typing import Any

from edge.domain.evidence import Evidence

from .capability import MachineLearningCapability
from .report import MachineLearningReport, MachineLearningResult


class MachineLearningError(ValueError):
    """Raised when an ML-assisted capability cannot be executed."""


class MachineLearningService:
    """Application-facing service for ML-assisted research analysis."""

    def __init__(self, executor: Any) -> None:
        self._executor = executor

    def analyze(
        self,
        capability: MachineLearningCapability,
        evidence: Evidence,
    ) -> MachineLearningReport:
        input_measurements = {
            metric_name: evidence.measurements[metric_name]
            for metric_name in capability.input_metric_names
            if metric_name in evidence.measurements
        }

        missing_inputs = [
            metric_name
            for metric_name in capability.input_metric_names
            if metric_name not in input_measurements
        ]

        if missing_inputs:
            result = MachineLearningResult(
                capability_id=capability.capability_id,
                capability_fingerprint=capability.fingerprint,
                output_name=capability.output_name,
                output_value=None,
                input_measurements=input_measurements,
                evidence=evidence,
                assumptions=capability.assumptions,
                message=f"Missing input measurements: {missing_inputs}",
            )
            return MachineLearningReport(
                capability_id=capability.capability_id,
                capability_fingerprint=capability.fingerprint,
                status="failed",
                result=result,
                input_metric_names=capability.input_metric_names,
                assumption_count=len(capability.assumptions),
                output_name=capability.output_name,
                output_value=None,
                failure_message=result.message,
                run_fingerprint=self._build_run_fingerprint(result),
            )

        try:
            output_value = self._executor.execute(capability, evidence)
            validation_message = self._validate_output(capability, output_value)
            result = MachineLearningResult(
                capability_id=capability.capability_id,
                capability_fingerprint=capability.fingerprint,
                output_name=capability.output_name,
                output_value=None if validation_message else output_value,
                input_measurements=input_measurements,
                evidence=evidence,
                assumptions=capability.assumptions,
                message=validation_message,
            )
            status = "completed" if validation_message is None else "failed"
        except Exception as exc:  # noqa: BLE001 - failures must be contained.
            result = MachineLearningResult(
                capability_id=capability.capability_id,
                capability_fingerprint=capability.fingerprint,
                output_name=capability.output_name,
                output_value=None,
                input_measurements=input_measurements,
                evidence=evidence,
                assumptions=capability.assumptions,
                message=str(exc),
            )
            status = "failed"

        return MachineLearningReport(
            capability_id=capability.capability_id,
            capability_fingerprint=capability.fingerprint,
            status=status,
            result=result,
            input_metric_names=capability.input_metric_names,
            assumption_count=len(capability.assumptions),
            output_name=capability.output_name,
            output_value=result.output_value,
            failure_message=result.message,
            run_fingerprint=self._build_run_fingerprint(result),
        )

    @staticmethod
    def _validate_output(
        capability: MachineLearningCapability,
        output_value: float,
    ) -> str | None:
        if capability.validation_rule is None:
            return None

        if (
            capability.validation_rule.minimum_output is not None
            and output_value < capability.validation_rule.minimum_output
        ):
            return (
                f"Output below minimum {capability.validation_rule.minimum_output}"
            )

        if (
            capability.validation_rule.maximum_output is not None
            and output_value > capability.validation_rule.maximum_output
        ):
            return (
                f"Output above maximum {capability.validation_rule.maximum_output}"
            )

        return None

    @staticmethod
    def _build_run_fingerprint(result: MachineLearningResult) -> str:
        payload = {
            "capability_id": result.capability_id,
            "capability_fingerprint": result.capability_fingerprint,
            "output_name": result.output_name,
            "output_value": result.output_value,
            "input_measurements": result.input_measurements,
            "assumptions": list(result.assumptions),
            "message": result.message,
        }
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()
