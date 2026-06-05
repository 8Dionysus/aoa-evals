# Release Support Facade Removal

- Decision ID: AOA-EV-D-0190
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/release_support_routes.py`, focused release-support helper modules, focused release-support report validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, release/support, observability/audit
- Mechanic parents: release-support, cross-parent
- Guard families: report/release/receipt, source/topology, release/nightly
- Posture: active rationale

## Context

AOA-EV-D-0182 split route/provenance checks into
`release_support_routes.py` and shared report helpers into
`release_support_common.py`. After AOA-EV-D-0189 removed the separate report
facade, `scripts/validators/release_support.py` only re-exported constants,
helpers, and the route validator for historical imports. AOA-EV-D-0217 later
removes the helper aggregate too.

That compatibility surface no longer protected an owner boundary.

## Decision

`scripts/validators/release_support.py` is removed.

Mechanic route orchestration imports
`release_support_routes.validate_release_support_route_surfaces` directly.

Release-support report validators import shared report constants and helpers
from focused `release_support_*` helper modules, and route/part constants from
`release_support_routes.py`.

Tests import the focused module that owns the constants or validator under
test.

## Rationale

Compatibility exports are useful during a split, but they become topology noise
once all callers can name the owning module. Keeping the facade would preserve a
generic release-support bucket after the real boundaries were already split.

The durable shape is explicit:

- `release_support_routes.py` owns release-support route, part-contract,
  provenance, legacy, and decision-token checks.
- focused `release_support_*` helper modules own report constants, command
  constants, route-token lookup, repo-ref parsing, and report-structure helpers
  without owning route or report meaning.
- focused report validators own readiness, strategic closeout, and PR handoff
  report contracts.

## Consequences

- Positive: no release-support compatibility validator remains in source-fast
  topology.
- Positive: report validators no longer import through a facade for shared
  helpers.
- Positive: mechanics orchestration names the route validator it calls.
- Tradeoff: tests and orchestrators import a few focused modules directly.

## Current Applicability

As of 2026-06-04:

- Still valid: release-support validation remains blocking source-fast and
  release-check coverage.
- Changed: `release_support.py` no longer exists.
- Changed: AOA-EV-D-0217 removes `release_support_common.py` as the remaining
  helper aggregate.
- Supersedes: the compatibility-facade shape left by AOA-EV-D-0121,
  AOA-EV-D-0162, AOA-EV-D-0179, AOA-EV-D-0182, and AOA-EV-D-0189.

## Boundaries

This decision does not change release-support report semantics, create live
release evidence, publish a release, accept runtime evidence, mutate sibling
repos, or mark a goal complete.

It does not add a replacement aggregate release-support facade under another
name.

## Validation

- `python -m py_compile scripts/validators/mechanics_routes.py scripts/validators/evidence_readouts.py scripts/validators/release_support_refs.py scripts/validators/release_support_report_checks.py scripts/validators/release_support_report_commands.py scripts/validators/release_support_report_constants.py scripts/validators/release_support_route_tokens.py scripts/validators/release_support_routes.py scripts/validators/release_support_readiness_report.py scripts/validators/release_support_strategic_closeout_report.py scripts/validators/release_support_pr_handoff_report.py`
- `python -m pytest -q mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py tests/test_mechanic_surface_contracts.py tests/test_mechanic_legacy_archive_routes.py tests/test_runtime_evidence_surfaces.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
