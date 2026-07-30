# Active-Organ Proof Does Not Collapse Into Admission

- Decision ID: AOA-EV-D-0251
- Status: Accepted
- Date: 2026-07-29
- Owner surface: `evals/comparison/fixed-baseline/aoa-memo-active-organ-offline-replay/`

## Index Metadata

- Original date: 2026-07-29
- Surface classes: source eval package, proof contract, comparison
- Mechanic parents: proof-infra
- Guard families: bounded claim, run status, no production authority
- Posture: accepted reduced-organ rationale, unlanded

## Context

The active-organ program has multiple independently meaningful evidence lanes:
source/data readiness, model execution, reviewed OS outcomes, transaction and
erasure faults, accelerated lifecycle, natural wall-clock durability, host
admission, and operator benefit. A single green lane cannot justify the whole
organ.

## Options Considered

- Aggregate every passed lab into one active-organ success verdict.
- Treat missing public benchmark inputs as zero scores.
- Keep each lane typed and select the weaker R1 architecture at the current
  evidence ceiling.
- Make the eval bundle the production admission owner.

## Decision

Keep the lanes separate and preserve `complete`, `partial`, `invalid`,
`aborted`, and `blocked` status.

The current bounded evidence supports R1 explicit pull and disabled C/D
research contours. It does not establish natural proactive benefit,
cross-model portability, reviewed OS outcome quality, real 30-day durability,
training, production, or landing authority.

Public benchmarks are never sole proof. Accelerated days are never wall-clock
days. Model attempts without schema-valid reports remain failed attempts.
Host denial is a valid blocked result and may not be overridden to complete a
matrix.

## Rationale

Separating evidence classes prevents benchmark, mechanism, or process health
from laundering authority into a deployment decision. It also preserves useful
negative and partial results.

## Consequences

- The bundle can report one completed model while cross-model status remains
  partial.
- Six prepared OS refs remain zero reviewed/scored cases.
- Real 7/30-day flags remain false until elapsed-time coverage passes.
- Final landing selection belongs to the operator and owners, not the eval.

## Current Applicability

As of 2026-07-29:

- Still valid: all evidence and authority ceilings above.
- Changed: one pinned Gemma 4 E2B Phase 13 report is complete.
- Superseded by: none.

## Review Log

### 2026-07-29 - Select R1 at the current evidence ceiling

- Previous assumption: full C remained the target hypothesis.
- New reality: A is the admitted core; C/D remain disabled research contours.
- Reason: natural OS, cross-model, operator, and real 30-day evidence remain
  incomplete while B/always/automatic-sharing falsifiers fired.
- Source surfaces updated:
  - `evals/comparison/fixed-baseline/aoa-memo-active-organ-offline-replay/`
- Validation: bundle-specific, catalog parity, repository, semantic-agent, and
  full test gates.

## Boundaries

This decision is not an eval verdict that activates memory. It does not make
synthetic canary outcomes natural, turn mechanism proof into production
reliability, or authorize landing.

## Validation

Regenerate decision indexes and eval catalogs; validate the active-organ
bundle, root repository, semantic-agent surfaces, and full test suite.
