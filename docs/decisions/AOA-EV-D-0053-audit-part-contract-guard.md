# Audit Part Contract Guard

- Decision ID: AOA-EV-D-0053
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/audit/parts/`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: mechanic part, validation guard, boundary/runtime/sibling
- Mechanic parents: audit
- Guard families: part and payload
- Posture: active guard rationale

## Context

The audit mechanic is the highest-risk candidate-evidence intake route in
`aoa-evals`: selected runtime packets, artifact-to-verdict hooks, generated
candidate readers, and integrity reviews can easily be mistaken for accepted
proof if their part contracts are only implied by the parent `PARTS.md`.

The parent package already had the right operation shape, but the individual
part README files did not all expose inputs, outputs, stronger-owner split,
stop-lines, and validation directly.

## Decision

Make the four active audit part README files carry explicit part contracts:

- `mechanics/audit/parts/selected-evidence-packets/README.md`;
- `mechanics/audit/parts/artifact-verdict-hooks/README.md`;
- `mechanics/audit/parts/candidate-readers/README.md`;
- `mechanics/audit/parts/integrity-review/README.md`.

Add validator coverage so these README files must keep inputs, outputs,
stronger-owner split, stop-lines, and validation visible.

## Rationale

Audit is where runtime, trace, machine, and sibling-owned artifacts enter the
proof organ as candidates. A weak local part card can quietly turn candidate
navigation into proof acceptance, especially after files have moved out of root
districts.

Part-level contracts make the active route clear without creating new parent
mechanics or importing runtime authority.

## Consequences

- Positive: candidate-only posture is visible at the exact part a future agent
  edits.
- Positive: `python scripts/validate_repo.py` now catches drift in audit part
  contract wording.
- Tradeoff: audit README changes now have slightly tighter wording
  requirements.
- Follow-up: other mechanics can receive part-level contract guards as their
  risk justifies it; this decision does not require a blanket rewrite in one
  slice.

## Boundaries

This decision does not create new audit parts, accept runtime evidence as
proof, move bundle-local review into audit, or make generated candidate readers
authoritative.

It does not transfer `abyss-stack`, `aoa-playbooks`, `aoa-agents`, `aoa-memo`,
or `aoa-stats` owner truth into `aoa-evals`.

## Validation

- `mechanics/audit/parts/selected-evidence-packets/README.md`
- `mechanics/audit/parts/artifact-verdict-hooks/README.md`
- `mechanics/audit/parts/candidate-readers/README.md`
- `mechanics/audit/parts/integrity-review/README.md`
- `scripts/validate_repo.py`
- `tests/test_validate_repo.py`
- `python scripts/validate_repo.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k audit_part_readmes`
- `python -m pytest -q tests/test_validate_repo.py -k provenance`

## Current Applicability

As of 2026-05-24:

- Still valid: the four audit part README files remain explicit part contracts
  with inputs, outputs, stronger-owner split, stop-lines, and validation route.
- Clarified: the stop-line sections now use pressure-to-route tables so an
  agent sees the next owner action instead of only a blocked action.
- Source surfaces updated:
  - `mechanics/audit/parts/README.md`
  - `mechanics/audit/parts/selected-evidence-packets/README.md`
  - `mechanics/audit/parts/artifact-verdict-hooks/README.md`
  - `mechanics/audit/parts/candidate-readers/README.md`
  - `mechanics/audit/parts/integrity-review/README.md`
  - `scripts/validate_repo.py`
- Validation: the audit part README validator tokens now require the route-map
  wording that replaced prohibition-only phrasing.
- Clarified: `mechanics/audit/parts/README.md` is the lower index and
  part-admission route for audit suboperations.

## Review Log

### 2026-05-24 - Part stop-lines converted to route pressure maps

- Previous assumption: part contracts should prove safety by repeating direct
  prohibitions such as generated reader authority, verdict execution, runtime
  activation, and raw evidence ingestion.
- New reality: the contract is stronger when each pressure routes to an owner,
  source surface, or bundle-local review step.
- Reason: this matches the repo-wide target where a low-context agent can infer
  role, input, output, owner, next route, tool, and validation from the active
  part card.
- Source surfaces updated: the four audit part README contracts and their
  validator tokens.
- Validation: see the landing PR for the exact command battery.

### 2026-05-24 - Part index admission route clarified

- Previous assumption: the parts index could end with a direct warning about
  creating another part after listing the current audit suboperations.
- New reality: the index is clearer as an operating card plus part-admission
  route: source surfaces, operation, validation, owner boundary, and next route.
- Reason: a low-context agent should know how a new audit suboperation earns a
  part-local contract without reading the warning as the main instruction.
- Source surfaces updated: `mechanics/audit/parts/README.md`,
  `scripts/validate_repo.py`, and `tests/test_validate_repo.py`.
- Validation: focused audit parts validator tests plus full repo validation.
