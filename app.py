"""Practice console for learning loop engineering with a COBOL-style emulator."""
from __future__ import annotations

import streamlit as st

from loop_engineering.emulator import EmulatorState, new_state, run_all, step


SCENARIOS = {
    "Healthy nightly batch": {
        "brief": "Run the baseline, inspect each phase, and explain why the result is safe to release.",
        "records": ["ACCT0000010000000125", "ACCT0000020000000300", "ACCT0000030000000075"],
        "hint": "Start with STEP and watch READ → VALIDATE → ACCUMULATE → WRITE → CLOSE.",
    },
    "Malformed production record": {
        "brief": "A nightly job fails. Find the bad record and explain the operational response.",
        "records": ["ACCT0000010000000125", "ACCT000002      BAD", "ACCT0000030000000075"],
        "hint": "Use STEP until VALIDATE fails. Inspect the current record and the error log.",
    },
    "Copybook mismatch": {
        "brief": "A partner sends a record with the wrong layout. Identify the interface contract problem.",
        "records": ["ACCT0000010000000125", "ACCT000002000000030", "ACCT0000030000000075"],
        "hint": "The record layout is fixed-width: 10 characters for account plus 10 digits for cents.",
    },
}


st.set_page_config(page_title="Loop Engineering Lab", page_icon="🔁", layout="wide")
st.title("🔁 Loop Engineering Lab")
st.caption("Learn by observing, changing, testing, and operating a COBOL-style batch system.")

practice_tab, proposal_tab, acceptance_tab = st.tabs(
    ["Practice Lab", "Change Proposal", "Acceptance Criteria"]
)

with proposal_tab:
    st.subheader("Business outcome")
    st.write(
        "Enable engineers to learn loop engineering by practicing safe changes to a COBOL-style batch system in a browser. "
        "The emulator makes legacy-system behavior visible so learners can observe execution, understand record layouts and working storage, "
        "diagnose failures, run regression checks, and interpret operational impact."
    )

    st.subheader("Affected interfaces")
    interfaces = [
        ("Streamlit browser app", "Provides guided scenarios, execution controls, traces, and emulator state."),
        ("loop_engineering.emulator", "Exposes deterministic state and step execution for the teaching simulator."),
        ("Scenario definitions", "Provides healthy, malformed-record, and copybook-mismatch exercises."),
        ("User controls", "Provides STEP, RUN ALL, RESET, and scenario selection."),
        ("Output spool", "Displays transaction count and total-cents output."),
        ("Job logs and traces", "Displays simulated execution events and failures."),
        ("Existing batch processor", "Remains available for file-based regression testing and is not replaced."),
        ("COBOL and JCL artifacts", "Remain production-shaped reference artifacts and are not modified by the emulator."),
    ]
    for name, detail in interfaces:
        with st.container():
            st.markdown(f"**{name}:** {detail}")

    st.subheader("Rollback plan")
    st.markdown(
        "1. Revert the emulator application commit.\n"
        "2. Restore the previous upload-based `app.py`.\n"
        "3. Remove `loop_engineering/emulator.py` and `tests/test_emulator.py` if the emulator is no longer wanted.\n"
        "4. Restart or redeploy Streamlit.\n"
        "5. Run the existing batch and golden-file tests to confirm the original validator still works."
    )

with acceptance_tab:
    st.subheader("Acceptance criteria")
    criteria = [
        "`streamlit run app.py` starts successfully.",
        "The healthy scenario completes with `RUN ALL` and status `COMPLETE`.",
        "The healthy scenario reports the expected transaction count and total.",
        "`STEP` advances execution and exposes the current phase.",
        "The trace includes `READ`, `VALIDATE`, `ACCUMULATE`, `WRITE`, and `CLOSE`.",
        "The malformed-record scenario ends with status `FAILED` and identifies the invalid record and validation problem.",
        "`RESET` returns the selected scenario to its initial state.",
        "Switching scenarios loads the correct mission and records.",
        "The output spool displays the generated summary.",
        "Existing batch and baseline regression tests pass.",
        "Emulator tests pass with `pytest`.",
        "The baseline golden-file comparison remains unchanged.",
    ]
    for item in criteria:
        st.checkbox(item, value=False, key=item)

with practice_tab:
    scenario_name = st.sidebar.selectbox("Practice scenario", list(SCENARIOS))
    scenario = SCENARIOS[scenario_name]
    if st.session_state.get("scenario") != scenario_name:
        st.session_state.scenario = scenario_name
        st.session_state.emulator = new_state(scenario["records"])

    state: EmulatorState = st.session_state.emulator

    st.info(f"**Mission:** {scenario['brief']}  \n**Hint:** {scenario['hint']}")

    controls = st.columns(4)
    if controls[0].button("STEP", type="primary", use_container_width=True):
        step(state)
    if controls[1].button("RUN ALL", use_container_width=True):
        run_all(state)
    if controls[2].button("RESET", use_container_width=True):
        st.session_state.emulator = new_state(scenario["records"])
        state = st.session_state.emulator
    if controls[3].button("NEW SCENARIO", use_container_width=True):
        st.session_state.scenario = scenario_name
        st.session_state.emulator = new_state(scenario["records"])
        state = st.session_state.emulator

    left, right = st.columns(2)
    with left:
        st.subheader("Virtual mainframe")
        st.write(f"Job status: **{state.status}**")
        metrics = st.columns(3)
        metrics[0].metric("Last step", state.last_step or "—")
        metrics[1].metric("Record", f"{state.cursor}/{len(state.records)}")
        metrics[2].metric("Total cents", state.total_cents)

        st.markdown("**Input file: TRANSACTION-FILE**")
        for number, record in enumerate(state.records, start=1):
            marker = "▶" if number == state.cursor and state.current else " "
            st.code(f"{marker} {number:02d} | {record}", language="text")

        st.markdown("**Working storage**")
        st.code(
            f"CURRENT-RECORD: {state.current or '(none)'}\n"
            f"TRANSACTION-COUNT: {state.count:010d}\n"
            f"TOTAL-CENTS: {state.total_cents:010d}",
            language="text",
        )

    with right:
        st.subheader("Execution trace")
        st.code("\n".join(state.log), language="text")
        if state.error:
            st.error(f"Job failed: {state.error}")
        elif state.status == "COMPLETE":
            st.success("Job complete. Inspect the trace, then explain what you would monitor in production.")

        st.subheader("Output spool")
        st.code("\n".join(state.output) or "(nothing written yet)", language="text")

    st.divider()
    st.markdown(
        "**The loop:** observe the trace → understand the data layout → make one safe change → "
        "run again → verify the output → document what you learned."
    )
