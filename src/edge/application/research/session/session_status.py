from __future__ import annotations

from enum import Enum


class SessionStatus(str, Enum):
    """
    Lifecycle states of a Research Session.

    A Research Session represents the execution context of a single
    quantitative research process within the Application Layer.
    """

    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

    @property
    def is_terminal(self) -> bool:
        """
        Returns True if the session reached a terminal state.
        """
        return self in (SessionStatus.COMPLETED, SessionStatus.FAILED)