# Change Proposal: Interactive Loop Engineering Emulator

## Business outcome

Enable engineers to learn loop engineering by practicing safe changes to a COBOL-style batch system in a browser. The emulator makes legacy-system behavior visible so learners can observe execution, understand record layouts and working storage, diagnose failures, run regression checks, and interpret operational impact.

## Affected interfaces

| Interface | Impact |
|---|---|
| Streamlit browser app | Provides guided scenarios, execution controls, traces, and emulator state. |
| `loop_engineering.emulator` | Exposes deterministic state and step execution for the teaching simulator. |
| Scenario definitions | Provides healthy, malformed-record, and copybook-mismatch exercises. |
| User controls | Provides `STEP`, `RUN ALL`, `RESET`, and scenario selection. |
| Output spool | Displays transaction count and total-cents output. |
| Job logs and traces | Displays simulated execution events and failures. |
| Existing batch processor | Remains available for file-based regression testing and is not replaced. |
| COBOL and JCL artifacts | Remain production-shaped reference artifacts and are not modified by the emulator. |

## Rollback plan

1. Revert the emulator application commit.
2. Restore the previous upload-based `app.py`.
3. Remove `loop_engineering/emulator.py` and `tests/test_emulator.py` if the emulator is no longer wanted.
4. Restart or redeploy Streamlit.
5. Run the existing batch and golden-file tests to confirm the original validator still works.

The rollback is low risk because the emulator is isolated from the existing batch-processing function and does not alter the COBOL, JCL, baseline, or golden-file artifacts.

## Measurable acceptance criteria

### Functional

- [ ] `streamlit run app.py` starts successfully.
- [ ] The healthy scenario completes with `RUN ALL` and status `COMPLETE`.
- [ ] The healthy scenario reports the expected transaction count and total.
- [ ] `STEP` advances execution and exposes the current phase.
- [ ] The trace includes `READ`, `VALIDATE`, `ACCUMULATE`, `WRITE`, and `CLOSE`.
- [ ] The malformed-record scenario ends with status `FAILED` and identifies the invalid record and validation problem.
- [ ] `RESET` returns the selected scenario to its initial state.
- [ ] Switching scenarios loads the correct mission and records.
- [ ] The output spool displays the generated summary.

### Regression and quality

- [ ] Existing batch and baseline regression tests pass.
- [ ] Emulator tests pass with `pytest`.
- [ ] The baseline golden-file comparison remains unchanged.
- [ ] No production data is required to run the emulator.
- [ ] Every scenario is deterministic and resettable.
- [ ] The application remains compatible with the documented Python and Streamlit setup.

### Learning outcome

A learner can select the malformed-record scenario, step through the job, identify the failed validation phase and affected record, explain why processing stopped, reset the job, rerun the healthy baseline, and confirm that its output is correct.
