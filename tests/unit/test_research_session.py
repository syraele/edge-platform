from edge.application.research.session.research_session import ResearchSession
from edge.application.research.session.session_status import SessionStatus


def test_session_is_created():
    session = ResearchSession()

    assert session.status == SessionStatus.CREATED
    assert session.session_id is not None
    assert session.created_at is not None


def test_session_start():
    session = ResearchSession()

    session.start()

    assert session.status == SessionStatus.RUNNING
    assert session.started_at is not None


def test_session_complete():
    session = ResearchSession()

    session.start()
    session.complete()

    assert session.status == SessionStatus.COMPLETED
    assert session.completed_at is not None


def test_session_fail():
    session = ResearchSession()

    session.start()
    session.fail("failure")

    assert session.status == SessionStatus.FAILED
    assert session.completed_at is not None
    assert session.message == "failure"


def test_terminal_state():
    assert SessionStatus.COMPLETED.is_terminal
    assert SessionStatus.FAILED.is_terminal
    assert not SessionStatus.CREATED.is_terminal
    assert not SessionStatus.RUNNING.is_terminal