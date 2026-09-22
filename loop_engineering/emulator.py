"""Small, deterministic COBOL-style batch emulator for learning loop engineering."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


StepName = Literal["READ", "VALIDATE", "ACCUMULATE", "WRITE", "CLOSE"]


@dataclass
class EmulatorState:
    records: list[str]
    cursor: int = 0
    count: int = 0
    total_cents: int = 0
    current: str = ""
    output: list[str] = field(default_factory=list)
    log: list[str] = field(default_factory=list)
    status: str = "READY"
    error: str | None = None
    last_step: str = ""

    @property
    def done(self) -> bool:
        return self.status in {"COMPLETE", "FAILED"}


def new_state(records: list[str]) -> EmulatorState:
    state = EmulatorState(records=[record.rstrip("\r\n") for record in records])
    state.log.append("JOB READY: TRANSACTION-SUMMARY")
    return state


def _fail(state: EmulatorState, message: str) -> None:
    state.error = message
    state.status = "FAILED"
    state.log.append(f"ERROR: {message}")


def step(state: EmulatorState, requested: StepName | None = None) -> EmulatorState:
    """Execute one teaching step; this intentionally exposes machine state."""
    if state.done:
        return state

    if requested == "READ" or not state.current:
        if state.cursor >= len(state.records):
            state.status = "COMPLETE"
            state.last_step = "END-OF-FILE"
            state.log.append("READ: end of file")
            return state
        state.current = state.records[state.cursor]
        state.cursor += 1
        state.last_step = "READ"
        state.status = "RUNNING"
        state.log.append(f"READ: record {state.cursor} loaded")
        return state

    if requested in (None, "VALIDATE"):
        if len(state.current) != 20:
            _fail(state, f"record {state.cursor} has length {len(state.current)}; expected 20")
            return state
        if not state.current[:10].strip():
            _fail(state, f"record {state.cursor} has no account")
            return state
        amount = state.current[10:]
        if not amount.isdigit():
            _fail(state, f"record {state.cursor} has a non-numeric amount: {amount!r}")
            return state
        state.last_step = "VALIDATE"
        state.log.append(f"VALIDATE: record {state.cursor} accepted")
        if requested == "VALIDATE":
            return state

    if requested in (None, "ACCUMULATE"):
        state.count += 1
        state.total_cents += int(state.current[10:])
        state.last_step = "ACCUMULATE"
        state.log.append(f"ACCUMULATE: count={state.count}, total={state.total_cents}")
        if requested == "ACCUMULATE":
            return state

    if requested in (None, "WRITE"):
        state.output = [
            f"TRANSACTION-COUNT {state.count:010d}",
            f"TOTAL-CENTS      {state.total_cents:010d}",
        ]
        state.last_step = "WRITE"
        state.log.append("WRITE: summary refreshed")
        if requested == "WRITE":
            return state

    if requested in (None, "CLOSE"):
        state.current = ""
        state.last_step = "CLOSE"
        state.log.append("CLOSE: transaction record released")
        if requested == "CLOSE":
            return state
        return step(state, "READ")

    return state


def run_all(state: EmulatorState) -> EmulatorState:
    while not state.done:
        step(state)
    return state
