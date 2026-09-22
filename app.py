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
