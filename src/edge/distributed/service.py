from __future__ import annotations

import hashlib
import json
from typing import Any

from .report import DistributedResearchReport, DistributedResearchUnitResult
from .workload import DistributedResearchWorkload, DistributedResearchUnit


class DistributedResearchError(ValueError):
    """Raised when a distributed research workload is invalid."""


class DistributedResearchService:
    """Application-facing coordination service for distributed research."""

    def __init__(self, executor: Any) -> None:
        self._executor = executor

    def execute(
        self,
        workload: DistributedResearchWorkload,
    ) -> DistributedResearchReport:
        self._validate_workload(workload)

        unit_results: list[DistributedResearchUnitResult] = []

        for unit in workload.units:
            try:
                pipeline_report = self._executor.execute(unit)
                if pipeline_report.session_id != unit.session.session_id:
                    raise DistributedResearchError(
                        "Distributed unit report session identity mismatch"
                    )

                unit_results.append(
                    DistributedResearchUnitResult(
                        unit_id=unit.unit_id,
                        session_id=unit.session.session_id,
                        status="completed",
                        execution_context=unit.execution_context,
                        pipeline_report=pipeline_report,
                    )
                )
            except Exception as exc:  # noqa: BLE001 - unit failures are contained.
                unit_results.append(
                    DistributedResearchUnitResult(
                        unit_id=unit.unit_id,
                        session_id=unit.session.session_id,
                        status="failed",
                        execution_context=unit.execution_context,
                        pipeline_report=None,
                        failure_message=str(exc),
                    )
                )

        result_tuple = tuple(unit_results)
        completed_session_ids = tuple(
            result.session_id for result in result_tuple if result.status == "completed"
        )
        failed_session_ids = tuple(
            result.session_id for result in result_tuple if result.status == "failed"
        )
        completed_units = len(completed_session_ids)
        failed_units = len(failed_session_ids)

        if completed_units == len(result_tuple):
            status = "completed"
        elif completed_units > 0:
            status = "partial"
        else:
            status = "failed"

        return DistributedResearchReport(
            workload_id=workload.workload_id,
            workload_fingerprint=workload.fingerprint,
            status=status,
            unit_results=result_tuple,
            completed_units=completed_units,
            failed_units=failed_units,
            completed_session_ids=completed_session_ids,
            failed_session_ids=failed_session_ids,
            assumption_count=len(workload.assumptions),
            run_fingerprint=self._build_run_fingerprint(workload, result_tuple),
        )

    @staticmethod
    def _validate_workload(workload: DistributedResearchWorkload) -> None:
        if not workload.units:
            raise DistributedResearchError(
                "Distributed research workload requires at least one unit"
            )

        unit_ids = tuple(unit.unit_id for unit in workload.units)
        if len(set(unit_ids)) != len(unit_ids):
            raise DistributedResearchError(
                "Distributed research workload requires unique unit identities"
            )

    @staticmethod
    def _build_run_fingerprint(
        workload: DistributedResearchWorkload,
        unit_results: tuple[DistributedResearchUnitResult, ...],
    ) -> str:
        payload = {
            "workload_fingerprint": workload.fingerprint,
            "unit_results": [
                {
                    "unit_id": result.unit_id,
                    "session_id": result.session_id,
                    "status": result.status,
                    "execution_context": result.execution_context,
                    "pipeline_report_id": (
                        result.pipeline_report.report_id
                        if result.pipeline_report is not None
                        else None
                    ),
                    "failure_message": result.failure_message,
                }
                for result in unit_results
            ],
        }
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()