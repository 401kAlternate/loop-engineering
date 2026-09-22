# Build the first working loop

This repository now includes a runnable local regression loop for a COBOL-style fixed-width batch workload.

## Run it

Requires Python 3.10+ and `pytest` for the test suite.

```bash
python -m loop_engineering.batch \
  examples/transactions/input.dat \
  /tmp/transaction-summary.out \
  --golden examples/transactions/expected.out

python -m pytest
```

The local runner validates 20-character records consisting of a 10-character account followed by a 10-digit amount in cents. It produces a record count and total, then compares the result with the checked-in golden file.

## Repository layout

- `loop_engineering/batch.py` — executable local reference implementation and validator
- `src/cobol/transaction-summary.cbl` — corresponding COBOL batch program
- `copybooks/transaction.cpy` — shared record layout
- `examples/transactions/` — input and expected output fixtures
- `tests/` — regression tests
- `jcl/transaction-summary.jcl` — illustrative z/OS execution step
- `docs/system-map.md` — system inventory template

The Python implementation makes the feedback loop runnable without requiring a mainframe compiler. The COBOL and JCL artifacts preserve the target production shape and can be compiled and executed in a compatible environment.
