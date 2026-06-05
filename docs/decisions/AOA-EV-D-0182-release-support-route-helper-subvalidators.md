# Release Support Route And Helper Subvalidators

- Decision ID: AOA-EV-D-0182
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/release_support_routes.py`, focused `scripts/validators/release_support_*` helper modules

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, release/support, observability/audit
- Mechanic parents: release-support, cross-parent
- Guard families: report/release/receipt, source/topology
- Posture: active rationale, superseded in part by AOA-EV-D-0217

## Context

After release-support reports moved into focused modules, the original
`scripts/validators/release_support.py` file still carried two different
surfaces:

- route-card, part-contract, provenance, legacy, and release-support decision
  token checks; and
- shared report constants, repo-ref parsing, JSON loading, route-token lookup,
  verification snapshot checks, and claim-limit helpers used by the report
  validators.

Those are support surfaces, not one owner boundary. Route validation asks
whether the release-support mechanic is correctly bounded. Shared helpers
support report validators without defining report meaning.

## Decision

Release-support validation is split again:

- `scripts/validators/release_support_routes.py` owns release-support route
  cards, part contracts, provenance bridge, legacy archive pointers, and
  release-support decision-route checks.
- Shared release-support report constants and helper behavior first moved to
  `scripts/validators/release_support_common.py`; AOA-EV-D-0217 later split
  that layer into focused helper modules for report constants, command
  constants, route-token lookup, repo-ref parsing, and report structure checks.

AOA-EV-D-0190 later removes `scripts/validators/release_support.py` after
route, helper, report, and test imports move to the focused owner modules.

## Rationale

The route/provenance validator must not become the owner of readiness,
strategic closeout, or PR handoff report semantics. The shared helper module
must not become the owner of route semantics either.

Keeping a stable facade while splitting route and helper surfaces preserves the
current import contract and prevents the historical broad-gate shape from
reappearing under the release-support mechanic.

## Consequences

- Positive: route/provenance and helper behavior no longer share a broad
  release-support file.
- Positive: route/provenance checks have a focused validator and failure route.
- Positive: report validators share helpers without importing route ownership.
- Tradeoff: compatibility aliases remain until dependent validators can import
  the focused modules directly.

## Current Applicability

As of 2026-06-04:

- Still valid: release-support reports remain bounded below live git, GitHub,
  tag, release, and goal-completion evidence.
- Changed: route/provenance checks moved into
  `release_support_routes.py`; shared helpers first moved into
  `release_support_common.py`, then AOA-EV-D-0217 split that helper layer
  across focused `release_support_*` modules.
- Changed: report callers no longer route through the separate
  `release_support_reports.py` facade.
- Changed: AOA-EV-D-0190 removes `release_support.py` after callers import
  focused owner modules directly.
- Superseded in part by: AOA-EV-D-0189 for report facade removal,
  AOA-EV-D-0190 for release-support facade removal, and AOA-EV-D-0217 for
  release-support helper splitting.

## Boundaries

This decision does not create a branch, commit, PR, merge, tag, GitHub Release,
eval result receipt, live runtime acceptance, sibling mutation, or goal
completion.

It does not let route/provenance checks own report artifact meaning.

It does not let shared helper behavior own route/provenance meaning, live
publication truth, release evidence, or goal completion.

## Validation

- `python -m py_compile scripts/validators/release_support_refs.py scripts/validators/release_support_report_checks.py scripts/validators/release_support_report_commands.py scripts/validators/release_support_report_constants.py scripts/validators/release_support_route_tokens.py scripts/validators/release_support_routes.py scripts/validators/release_support_readiness_report.py scripts/validators/release_support_strategic_closeout_report.py scripts/validators/release_support_pr_handoff_report.py scripts/validators/evidence_readouts.py scripts/validators/mechanics_routes.py`
- `python -m pytest -q mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py tests/test_mechanic_surface_contracts.py -k release_support`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
