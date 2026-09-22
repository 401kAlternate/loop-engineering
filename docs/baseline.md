# Baseline for the loop engineering lab

A baseline is a known-good snapshot of system behavior. In legacy engineering, the baseline is built from representative production-like data, recorded outputs, and observed behavior so that future changes can be tested safely.

## Purpose

The baseline lets the team answer: "What should this system do before any change?"

It is useful for:

- comparing before/after behavior
- catching regressions early
- validating the job result after a code change
- proving that a fix preserved intended business behavior
- training engineers on a stable reference point

## Baseline artifacts

For this repository, the baseline includes:

- representative production-like transaction data
- a golden output file
- a sample JCL job log
- a transaction trace showing each processing step
- regression tests that compare the generated output to the golden output

## Files in this baseline

- `examples/baseline/transactions.dat` — input workload
- `examples/baseline/expected-summary.out` — expected result
- `examples/baseline/job-log.txt` — sample job log for review
- `examples/baseline/transaction-trace.txt` — step-by-step trace
- `tests/test_baseline.py` — automated regression check

## Build the baseline

1. Collect a realistic sample from production-like data.
2. Run the batch process and capture the output.
3. Save that output as the golden file.
4. Record the job log and transaction trace.
5. Write a regression test that asserts the current output matches the golden file.
6. Treat the baseline as immutable until the business behavior intentionally changes.

## Operator questions

When using the baseline, ask:

- Does the output match the golden file?
- Did the job log show all expected steps?
- Did the trace reveal any field mismatches or malformed records?
- What changed relative to the baseline?
- Is the observed difference intentional or a regression?

This is the disciplined core of loop engineering: observe the existing behavior, capture a stable baseline, then change in small loops with validation.
