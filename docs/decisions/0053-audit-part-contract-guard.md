# 0053 Audit Part Contract Guard

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/audit/parts/`

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
- `python -m pytest -q tests/test_validate_repo.py -k 'audit_part_readmes or provenance'`
