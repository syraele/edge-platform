"""
EDGE_ENGINE

Lifecycle tests.
"""

from edge.application.bootstrap.startup import EdgeApplication


def test_application_lifecycle():

    app = EdgeApplication()

    app.start()

    assert app.engine.running is True

    app.stop()

    assert app.engine.running is False