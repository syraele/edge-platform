from edge.domain.evidence import Evidence
from edge.ml import (
    MachineLearningCapability,
    MachineLearningService,
    MachineLearningValidationRule,
)


class StubMLExecutor:
    def __init__(self, output: float | Exception) -> None:
        self._output = output

    def execute(self, capability, evidence):
        if isinstance(self._output, Exception):
            raise self._output
        return self._output


def test_ml_service_returns_traceable_completed_report():
    capability = MachineLearningCapability(
        capability_id="ml-score",
        capability_name="Score Predictor",
        input_metric_names=("profit_factor", "sharpe"),
        output_name="prediction_score",
        assumptions=("Input evidence remains representative.",),
    )
    service = MachineLearningService(StubMLExecutor(0.87))

    report = service.analyze(
        capability,
        Evidence(measurements={"profit_factor": 1.5, "sharpe": 0.9}),
    )

    assert report.status == "completed"
    assert report.result.succeeded is True
    assert report.input_metric_names == ("profit_factor", "sharpe")
    assert report.assumption_count == 1
    assert report.output_name == "prediction_score"
    assert report.result.output_value == 0.87
    assert report.output_value == 0.87
    assert report.failure_message is None
    assert report.result.input_measurements == {"profit_factor": 1.5, "sharpe": 0.9}
    assert report.capability_fingerprint == capability.fingerprint
    assert report.run_fingerprint


def test_ml_service_fails_when_required_inputs_are_missing():
    capability = MachineLearningCapability(
        capability_id="ml-score",
        capability_name="Score Predictor",
        input_metric_names=("profit_factor", "sharpe"),
        output_name="prediction_score",
    )
    service = MachineLearningService(StubMLExecutor(0.87))

    report = service.analyze(
        capability,
        Evidence(measurements={"profit_factor": 1.5}),
    )

    assert report.status == "failed"
    assert report.result.succeeded is False
    assert report.output_value is None
    assert report.failure_message == "Missing input measurements: ['sharpe']"
    assert report.result.message == "Missing input measurements: ['sharpe']"


def test_ml_service_contains_executor_failure():
    capability = MachineLearningCapability(
        capability_id="ml-score",
        capability_name="Score Predictor",
        input_metric_names=("profit_factor",),
        output_name="prediction_score",
    )
    service = MachineLearningService(StubMLExecutor(RuntimeError("model unavailable")))

    report = service.analyze(
        capability,
        Evidence(measurements={"profit_factor": 1.5}),
    )

    assert report.status == "failed"
    assert report.failure_message == "model unavailable"
    assert report.result.message == "model unavailable"


def test_ml_capability_fingerprint_is_deterministic():
    left = MachineLearningCapability(
        capability_id="ml-score",
        capability_name="Score Predictor",
        input_metric_names=("profit_factor",),
        output_name="prediction_score",
        assumptions=("Stable feature semantics.",),
    )
    right = MachineLearningCapability(
        capability_id="ml-score",
        capability_name="Score Predictor",
        input_metric_names=("profit_factor",),
        output_name="prediction_score",
        assumptions=("Stable feature semantics.",),
    )

    assert left.fingerprint == right.fingerprint


def test_ml_service_fails_when_output_violates_validation_rule():
    capability = MachineLearningCapability(
        capability_id="ml-score",
        capability_name="Score Predictor",
        input_metric_names=("profit_factor",),
        output_name="prediction_score",
        validation_rule=MachineLearningValidationRule(maximum_output=1.0),
    )
    service = MachineLearningService(StubMLExecutor(1.5))

    report = service.analyze(
        capability,
        Evidence(measurements={"profit_factor": 1.5}),
    )

    assert report.status == "failed"
    assert report.output_value is None
    assert report.failure_message == "Output above maximum 1.0"
