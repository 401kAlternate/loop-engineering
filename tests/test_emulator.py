"""Tests for the teaching emulator."""
from loop_engineering.emulator import new_state, run_all, step


def test_healthy_job_completes_with_expected_totals():
    state = new_state(["ACCT0000010000000125", "ACCT0000020000000300"])
    run_all(state)
    assert state.status == "COMPLETE"
    assert state.count == 2
    assert state.total_cents == 425
    assert "TRANSACTION-COUNT 0000000002" in state.output


def test_bad_record_stops_in_validation():
    state = new_state(["ACCT0000010000000125", "ACCT000002      BAD"])
    for _ in range(10):
        step(state)
        if state.done:
            break
    assert state.status == "FAILED"
    assert state.error is not None
    assert "non-numeric amount" in state.error
