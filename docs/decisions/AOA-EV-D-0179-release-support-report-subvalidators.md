# Release Support Report Subvalidators

- Decision ID: AOA-EV-D-0179
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/release_support_readiness_report.py`, `scripts/validators/release_support_strategic_closeout_report.py`, `scripts/validators/release_support_pr_handoff_report.py`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, release/support, observability/audit
- Mechanic parents: release-support, cross-parent
- Guard families: report/release/receipt, release/nightly
- Posture: active rationale

## Context

AOA-EV-D-0162 moved release-support report checks out of
`scripts/validators/release_support.py`, but the new
`scripts/validators/release_support_reports.py` module still carried three
different report contracts in one file:

- readiness audit;
- strategic closeout audit; and
- release-prep PR handoff snapshot.

Those artifacts share release-support helpers, but they are not one owner
surface. Readiness checks local release-prep reviewability. Strategic closeout
checks goal-completion posture and trap/open-item coverage. PR handoff checks a
pre-PR snapshot and landing steps. Keeping all three in one report module would
recreate the historical broad-gate pressure at a smaller scale.

## Decision

Release-support report validation is split into focused modules:

- `scripts/validators/release_support_readiness_report.py` owns readiness audit
  report identity, requirement coverage, verification snapshot, publication
  boundary, open-publication requirements, and claim limits.
- `scripts/validators/release_support_strategic_closeout_report.py` owns
  strategic closeout report identity, goal-completion posture, requirements
  review, trap review, verification snapshot, open items, and claim limits.
- `scripts/validators/release_support_pr_handoff_report.py` owns PR handoff
  report identity, pre-handoff live-status boundary, changed surface groups,
  draft PR body, verification snapshot, landing steps, and claim limits.

AOA-EV-D-0189 later removes the compatibility facade after
`evidence_readouts.py`, tests, and release gates can import the focused report
validators directly.

## Rationale

Release-support reports are audit artifacts below live evidence. They must
preserve boundaries around branch/commit/push/PR state, GitHub Repo Validation,
merge, tag, GitHub Release publication, runtime evidence acceptance, sibling
mutation, and goal completion.

The checks need to stay close to their part-local artifacts, but the import
surface should remain stable. A facade plus three focused modules keeps current
callers working while preventing one report validator from becoming a growing
history bucket.

## Consequences

- Positive: each report artifact now has its own validator, inventory row,
  mechanics ledger row, and failure route.
- Positive: the focused report validators are now direct gates and cannot hide
  behind an aggregate compatibility path.
- Positive: route cards, part contracts, provenance, and legacy posture stay in
  `release_support_routes.py`.
- Positive: shared constants and helper functions now live in
  focused release-support helper modules.

## Current Applicability

As of 2026-06-04:

- Still valid: release-support reports remain bounded local artifacts below
  live git/GitHub/tag/release/runtime/goal evidence.
- Changed: report-specific behavior moved from `release_support_reports.py`
  into three focused report modules.
- Changed: AOA-EV-D-0189 removes the remaining compatibility facade and direct
  callers now import focused report validators.
- Changed: AOA-EV-D-0190 removes the remaining `release_support.py`
  compatibility facade.
- Changed: AOA-EV-D-0217 removes the remaining release-support helper aggregate
  and keeps shared report support in focused helper modules.
- Superseded in part by: AOA-EV-D-0189 for report facade removal and
  AOA-EV-D-0190 for release-support facade removal; AOA-EV-D-0217 for helper
  splitting.

## Boundaries

This decision does not make any report validator live release evidence.

It does not create a branch, commit, PR, merge, tag, GitHub Release, eval
receipt, runtime acceptance, sibling mutation, or goal completion.

It does not move release-support route-card, provenance, part-contract, or
legacy validation out of `release_support_routes.py`.

It does not let generated inventory, release packaging, or runtime policy
define the source meaning of part-local report artifacts.

## Validation

- `python -m py_compile scripts/validators/release_support_refs.py scripts/validators/release_support_report_checks.py scripts/validators/release_support_report_commands.py scripts/validators/release_support_report_constants.py scripts/validators/release_support_route_tokens.py scripts/validators/release_support_readiness_report.py scripts/validators/release_support_strategic_closeout_report.py scripts/validators/release_support_pr_handoff_report.py scripts/validators/evidence_readouts.py scripts/validators/mechanics_root_districts.py scripts/validators/root_authored_surface_common.py scripts/validators/root_authored_surface_inventory.py scripts/validators/root_authored_surface_ledger.py scripts/validators/root_authored_surface_decision.py`
- `python -m pytest -q mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py tests/test_runtime_evidence_surfaces.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
