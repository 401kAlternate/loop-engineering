# Practice emulator

The browser app is now a learning simulator rather than an upload-only validator. It models a small COBOL-style batch job with a virtual input file, working storage, execution trace, output spool, and job status.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Use **STEP** to execute one phase at a time, or **RUN ALL** to complete the job. Select scenarios from the sidebar and use the trace to practice the loop:

1. Observe the current behavior.
2. Understand the record layout and program state.
3. Identify the smallest safe change.
4. Run and inspect the result.
5. Verify the output and explain the operational impact.

This is an educational emulator, not a COBOL compiler or a z/OS replacement. Its purpose is to make legacy-system reasoning visible and repeatable in a browser.
