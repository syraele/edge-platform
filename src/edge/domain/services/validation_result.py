"""
EDGE_ENGINE

Validation Result
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """
    Immutable result of a domain validation.

    A successful validation contains no errors.
    A failed validation contains one or more validation
    error messages describing the validation failures.
    """

    is_valid: bool

    errors: Tuple[str, ...] = ()

    @classmethod
    def success(cls) -> "ValidationResult":
        """
        Create a successful validation result.
        """
        return cls(
            is_valid=True,
            errors=(),
        )

    @classmethod
    def failure(cls, *errors: str) -> "ValidationResult":
        """
        Create a failed validation result.
        """
        return cls(
            is_valid=False,
            errors=tuple(errors),
        )

    @property
    def has_errors(self) -> bool:
        """
        Return True when validation contains one or more errors.
        """
        return not self.is_valid

    @property
    def error_count(self) -> int:
        """
        Return the number of validation errors.
        """
        return len(self.errors)