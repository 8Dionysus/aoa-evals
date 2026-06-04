# Release Support Validator Module Boundary

- Decision ID: AOA-EV-D-0121
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validators/release_support.py`, `mechanics/release-support/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, release/support, observability/audit
- Mechanic parents: release-support, cross-parent
- Guard families: report/release/receipt, source/topology
- Posture: active rationale

## Context

Release-support validation was split across two shapes inside
`scripts/validate_repo.py`: route-card checks embedded in the wider mechanics
pass, and three report validators for readiness audit, strategic closeout, and
PR handoff artifacts.

Those checks form one coherent owner surface. They protect bounded release
support posture below live git, GitHub Repo Validation, tag, GitHub Release,
and goal-completion evidence.

## Options Considered

- Keep release-support route and report checks inside the root validator
  because they touch release posture.
- Split readiness audit, strategic closeout, and PR handoff into separate
  validator modules.
- Move release-support route and report validation into
  `scripts/validators/release_support.py` while keeping `validate_repo.py` as
  the compatibility entrypoint.

## Decision

Release-support validation lives in
`scripts/validators/release_support.py`.

`scripts/validate_repo.py` keeps compatibility wrappers for
`validate_release_support_readiness_audit_surface`,
`validate_strategic_closeout_audit_surface`, and
`validate_release_prep_pr_handoff_surface`.

The module also owns release-support route-card, part-contract, provenance, and
legacy bridge token checks that previously lived inside the broad mechanics
surface validator.

## Rationale

Release-support reports are not release evidence by themselves. They are
bounded support artifacts that preserve what remains open before branch, PR,
Repo Validation, merge, tag, release, or goal-completion claims can be made.

Putting the checks behind a focused module keeps release/nightly/post-merge
support visible without creating another historical wave gate. It also keeps
generated/readout and receipt validators from absorbing release-support
meaning.

## Consequences

- Positive: release-support route and report checks leave the root validator.
- Positive: readiness, closeout, and PR-handoff posture stays grouped by owner
  instead of scattered through mechanics and report validation.
- Tradeoff: compatibility wrappers remain because tests still import through
  `scripts/validate_repo.py`.
- Follow-up: future release publication validators must check frozen artifacts
  and live evidence separately from release-support reports.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  entrypoint.
- Changed: release-support route and report checks now have a focused validator
  module.
- Superseded by: none.

## Boundaries

This decision does not create a tag, branch, commit, PR, merge, GitHub Release,
or eval result receipt.

It does not treat readiness audit, strategic closeout, or PR handoff reports as
live GitHub Repo Validation evidence.

It does not mark any repo goal complete.

## Validation

- `python -m pytest -q mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_test_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
