# COBOL System Map

This document is a lightweight inventory for understanding programs, interfaces, schedules, data stores, downstream consumers, and ownership. Keep it current as the system changes.

## How to use this map

1. Start with known programs and scheduled jobs.
2. Trace each program's inputs, outputs, data stores, and consumers.
3. Record evidence, such as source files, JCL members, job logs, copybooks, or runbooks.
4. Mark unknown values as `TBD` rather than guessing.
5. Assign an owner for every item and review the map after material changes or incidents.

## System context

| Field | Details |
|---|---|
| System name | TBD |
| Business capability | TBD |
| Environment(s) | Development: TBD; Test: TBD; Production: TBD |
| Primary platform | IBM z/OS or other: TBD |
| Business criticality | TBD |
| Recovery objectives | RTO: TBD; RPO: TBD |
| Last reviewed | 2026-09-22 |
| Map owner | TBD |

## Program inventory

| Program / module | Type | Business purpose | Trigger | Inputs | Outputs | Data stores | Owner | Evidence / status |
|---|---|---|---|---|---|---|---|---|
| TBD | COBOL batch / CICS / utility | TBD | TBD | TBD | TBD | TBD | TBD | Needs discovery |

**Types may include:** COBOL batch program, CICS transaction, copybook, DB2 stored procedure, utility, sort step, scheduler wrapper, or API adapter.

## Input and output interfaces

| Interface | Direction | Format / layout | Source or destination | Frequency / volume | Validation / reconciliation | Owner |
|---|---|---|---|---|---|---|
| TBD | Input / output | Fixed-width / CSV / XML / JSON / DB2 / VSAM | TBD | TBD | TBD | TBD |

Document important copybooks and record layouts here or link to their source locations. Treat changes to field positions, lengths, signs, packed decimals, and code pages as interface changes.

## Schedule and job flow

| Job / transaction | Schedule or trigger | Dependency | Main steps | SLA / deadline | Failure handling | Operations owner |
|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD |

### Dependency notes

- Upstream jobs: TBD
- Related JCL members: TBD
- Required files or resources: TBD
- Restart and checkpoint behavior: TBD
- Holiday or calendar exceptions: TBD

## Data stores

| Store | Technology | Data / records held | Read by | Written by | Retention / sensitivity | Data owner |
|---|---|---|---|---|---|---|
| TBD | DB2 / IMS / VSAM / sequential file | TBD | TBD | TBD | TBD | TBD |

## Downstream consumers

| Consumer | Purpose | Consumes | Delivery mechanism | Contract / SLA | Failure impact | Consumer owner |
|---|---|---|---|---|---|---|
| TBD | TBD | TBD | File transfer / API / queue / report | TBD | TBD | TBD |

## Ownership and escalation

| Responsibility | Primary owner | Backup | Contact / team | Escalation path |
|---|---|---|---|---|
| Business rules | TBD | TBD | TBD | TBD |
| COBOL application | TBD | TBD | TBD | TBD |
| JCL and scheduling | TBD | TBD | TBD | TBD |
| Database and storage | TBD | TBD | TBD | TBD |
| Operations and incident response | TBD | TBD | TBD | TBD |
| Security and compliance | TBD | TBD | TBD | TBD |
| Downstream consumers | TBD | TBD | TBD | TBD |

## Discovery backlog

Use this list to turn unknowns into small, verifiable investigations.

- [ ] Identify all production COBOL programs and their source repositories or libraries.
- [ ] Locate JCL members and scheduler definitions for each recurring job.
- [ ] Link each program to its copybooks and record layouts.
- [ ] Inventory DB2 tables, IMS databases, VSAM files, and sequential files.
- [ ] Trace upstream inputs and downstream consumers using job logs and transfer records.
- [ ] Confirm business, application, operations, data, and security owners.
- [ ] Record SLAs, restart procedures, retention rules, and data classifications.
- [ ] Validate this map with an operations representative and a business subject-matter expert.

## Change history

| Date | Change | Author |
|---|---|---|
| 2026-09-22 | Added initial lightweight system-map template. | TBD |
