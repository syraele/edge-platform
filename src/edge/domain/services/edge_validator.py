"""
EDGE_ENGINE

Edge Validator
"""

from edge.domain.knowledge import Knowledge
from edge.domain.services.validation_result import ValidationResult


class EdgeValidator:
    """
    Validates whether a Knowledge instance
    can generate an Edge.

    EF-002 intentionally introduces only the
    existence validation required by the
    Foundation Blueprint.
    """

    def validate(
        self,
        knowledge: Knowledge | None,
    ) -> ValidationResult:
        """
        Validate a Knowledge instance.
        """

        if knowledge is None:
            return ValidationResult.failure(
                "Knowledge is required to create an Edge."
            )

        return ValidationResult.success()
