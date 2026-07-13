"""
EDGE_ENGINE

Context tests.
"""

from tests.helpers import create_test_context


def test_context_creation():
    """
    Ensure a complete EdgeContext can be created.
    """

    ctx = create_test_context()

    assert ctx is not None

    assert ctx.config is not None

    assert ctx.market is not None

    assert ctx.runtime is not None

    assert ctx.session is not None

    assert ctx.services is not None


def test_context_default_values():
    """
    Verify default testing context.
    """

    ctx = create_test_context()

    assert ctx.session.symbol == "XAUUSD"

    assert ctx.session.mode == "TEST"

    assert ctx.runtime.started is False

    assert ctx.runtime.running is False

    assert ctx.runtime.paused is False

    assert ctx.runtime.error is False