# Loop Engineering

A disciplined engineering approach for building reliable feedback loops around COBOL and other mission-critical systems.

## What “loop engineering” means here

Loop engineering combines the strengths of modern iterative development with the operational discipline required by COBOL systems:

1. **Observe** — capture business requirements, production behavior, job results, transaction metrics, and incidents.
2. **Understand** — map COBOL programs, copybooks, JCL, files, transactions, and database dependencies before changing them.
3. **Change safely** — make small, traceable changes with compatibility in mind.
4. **Verify** — use automated tests, compile checks, record-level comparisons, and controlled batch or CICS validation.
5. **Release and learn** — monitor outcomes, document discoveries, and feed lessons into the next iteration.

## Engineering principles

- Preserve business behavior before pursuing modernization.
- Treat copybooks, data layouts, job dependencies, and operational runbooks as first-class interfaces.
- Prefer small reversible changes over large rewrites.
- Test with representative files, edge cases, and high-volume workloads.
- Make legacy behavior observable before refactoring it.
- Pair domain experts with engineers so undocumented business rules become explicit.
- Modernize incrementally through APIs, automated tests, improved tooling, and clear seams—not a rewrite by default.

## Suggested workflow

### 1. Discover

Create a lightweight system map covering programs, inputs and outputs, schedules, data stores, downstream consumers, and ownership.

### 2. Characterize current behavior

Build a baseline using golden files, regression tests, job logs, transaction traces, and representative production-like data.

### 3. Define a small change

State the business outcome, affected interfaces, rollback plan, and measurable acceptance criteria.

### 4. Implement and validate

Compile early, run unit and integration tests, compare outputs with the baseline, and validate performance and operational behavior.

### 5. Operate and improve

Release with monitoring and runbooks. Record what was learned and use it to improve the next loop.

## Repository direction

This repository can grow into a practical toolkit for COBOL loop engineering, including:

- COBOL examples and reusable patterns
- Copybook and data-layout documentation
- Regression-test fixtures and golden-file comparison tools
- JCL and batch workflow examples
- CICS, DB2, VSAM, and API integration notes
- Modernization decision records and operational runbooks

## Status

The repository is an initial foundation. Add domain-specific examples, tests, and tooling as the project takes shape.
