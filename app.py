"""Browser UI for the COBOL-style transaction regression loop."""
from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from loop_engineering.batch import parse_line, summarize


ROOT = Path(__file__).parent
SAMPLE_INPUT = ROOT / "examples/transactions/input.dat"
SAMPLE_GOLDEN = ROOT / "examples/transactions/expected.out"


st.set_page_config(page_title="Loop Engineering", page_icon="🔁", layout="centered")
st.title("🔁 Loop Engineering")
st.caption("A browser-based COBOL-style batch validation loop")

st.markdown(
    "Upload a fixed-width transaction file, validate its records, generate a summary, "
    "and optionally compare it with a golden output file."
)

uploaded_input = st.file_uploader("Transaction input file", type=["dat", "txt"])
use_sample = st.checkbox("Use the included sample transaction file", value=uploaded_input is None)

if uploaded_input is not None and not use_sample:
    input_name = uploaded_input.name
    input_bytes = uploaded_input.getvalue()
elif use_sample:
    input_name = "examples/transactions/input.dat"
    input_bytes = SAMPLE_INPUT.read_bytes()
else:
    input_name = ""
    input_bytes = b""

if input_bytes:
    try:
        input_text = input_bytes.decode("utf-8")
    except UnicodeDecodeError:
        st.error("The input file must be UTF-8 text.")
        st.stop()

    st.subheader("Input preview")
    st.code(input_text, language="text")

    errors: list[str] = []
    records = input_text.splitlines()
    for number, line in enumerate(records, start=1):
        try:
            parse_line(line, number)
        except ValueError as error:
            errors.append(str(error))

    if errors:
        st.error(f"Validation failed: {len(errors)} invalid record(s)")
        for error in errors:
            st.write(f"- {error}")
    else:
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / input_name.split("/")[-1]
            output_path = Path(directory) / "summary.out"
            input_path.write_text(input_text)
            result = summarize(input_path)

        count = len(records)
        total_cents = sum(int(line[10:]) for line in records)
        first, second = result.rstrip().splitlines()
        st.subheader("Batch result")
        metric_one, metric_two = st.columns(2)
        metric_one.metric("Transactions", count)
        metric_two.metric("Total", f"${total_cents / 100:,.2f}")
        st.code(result, language="text")
        st.download_button(
            "Download generated output",
            data=result,
            file_name="transaction-summary.out",
            mime="text/plain",
        )

        golden_file = st.file_uploader("Optional golden output file", type=["out", "txt"])
        if golden_file is None and use_sample:
            expected = SAMPLE_GOLDEN.read_text()
            golden_name = "examples/transactions/expected.out"
        elif golden_file is not None:
            expected = golden_file.getvalue().decode("utf-8")
            golden_name = golden_file.name
        else:
            expected = None
            golden_name = ""

        if expected is not None:
            if result == expected:
                st.success(f"PASS: output matches {golden_name}")
            else:
                st.error(f"FAIL: output differs from {golden_name}")
                with st.expander("Expected output"):
                    st.code(expected, language="text")
else:
    st.info("Choose the sample file or upload a transaction file to begin.")

st.divider()
st.caption("Record format: 10-character account followed by a 10-digit amount in cents.")
