# Audit / Parts Route

## Operating Card

| Field | Route |
| --- | --- |
| role | lower index for `audit` part-local candidate-evidence suboperations |
| input | selected runtime evidence, artifact-to-verdict hook pressure, candidate-reader drift, integrity-review packet, or new audit suboperation pressure |
| output | part route, source surface set, generated-reader route, validation lane, or stronger-owner handoff |
| owner | `mechanics/audit/parts/AGENTS.md` for part-lane law; part README for local contract; parent `audit` package for the candidate-evidence loop |
| next route | parent [README](../README.md), [PARTS](../PARTS.md), part README, part source surfaces, and [audit AGENTS validation](../AGENTS.md#validation) |
| tools | candidate-reader generators, drift checks, repo validator, and focused tests through `mechanics/audit/AGENTS.md#validation` |
| validation | `mechanics/audit/AGENTS.md#validation`, focused validator tests, and generated candidate-reader checks when source examples move |

## Active Parts

Each part owns a bounded suboperation in the same candidate-evidence loop:

| Part | Route |
| --- | --- |
| `selected-evidence-packets/` | curates runtime-owner artifacts into public-safe evidence packets |
| `artifact-verdict-hooks/` | maps playbook or trace artifacts to eval anchors and review expectations |
| `candidate-readers/` | generates compact readers from source packet and hook examples |
| `integrity-review/` | keeps W10-shaped runtime continuity evidence candidate-only and replay-bounded |

## Part Admission Route

A new audit part enters this index when all admission fields have a current
answer:

| Field | Required route |
| --- | --- |
| source surfaces | docs, schemas, examples, fixtures, generated readers, scripts, tests, or reports that the part owns together |
| operation | one bounded audit suboperation inside the candidate-evidence loop |
| validation | drift-catching validation named by the part and reachable from `mechanics/audit/AGENTS.md#validation` |
| owner boundary | stronger-owner boundary for runtime, trace, playbook, memory, stats, or bundle-local proof authority |
| next route | parent `PARTS.md`, parent `DIRECTION.md`, part README, and generated-reader checks when applicable |

Pressure without those fields routes through the existing part, parent
`DIRECTION.md`, or `mechanics/EVIDENCE_CLUSTERS.md` until the operation is
clear enough to carry a part-local contract.
