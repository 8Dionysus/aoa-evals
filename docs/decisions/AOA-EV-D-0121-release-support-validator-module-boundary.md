# Release Support Validator Module Boundary

- Decision ID: AOA-EV-D-0121
- Status: Accepted
- Date: 2026-06-03
- Owner surface: focused release-support validators, `mechanics/release-support/`

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

Release-support route validation routes through
`scripts/validators/release_support.py`.

Release-support report artifact validation later moves into focused report
validators.

`scripts/validators/release_support.py` initially owned release-support
route-card, part-contract, provenance, and legacy bridge token checks that
previously lived inside the broad mechanics surface validator. AOA-EV-D-0182
later narrowed this path to a compatibility facade and moved route/provenance
behavior into `scripts/validators/release_support_routes.py`.

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
- Positive: route/provenance checks and report artifact checks are now separate
  validator boundaries under the same release-support mechanic.
- Positive: shared report constants and helpers first moved into
  `release_support_common.py` instead of the route facade, then AOA-EV-D-0217
  split them across focused helper modules.
- Follow-up: future release publication validators must check frozen artifacts
  and live evidence separately from release-support reports.

## Current Applicability

As of 2026-06-04:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  entrypoint.
- Changed: readiness, strategic closeout, and PR handoff report checks moved
  to focused report validators.
- Changed: AOA-EV-D-0182 moved route/provenance checks into
  `scripts/validators/release_support_routes.py` and shared helpers first into
  `scripts/validators/release_support_common.py`; AOA-EV-D-0217 later split
  that helper layer across focused `scripts/validators/release_support_*`
  modules.
- Changed: AOA-EV-D-0189 removes the remaining report compatibility facade.
- Changed: AOA-EV-D-0190 removes the remaining release-support compatibility
  facade.
- Superseded in part by: AOA-EV-D-0162 for release-support report artifact
  validation; AOA-EV-D-0182 for the route/common split; AOA-EV-D-0189 for
  report facade removal; AOA-EV-D-0190 for release-support facade removal;
  AOA-EV-D-0217 for helper aggregate removal.

## Review Log

### 2026-06-04 - Report artifact validator split

- Previous assumption: one focused release-support validator could carry route,
  readiness, strategic closeout, and PR handoff checks.
- New reality: route/provenance validation and report artifact validation are
  distinct boundaries. The reports are part-local release-support artifacts
  below live git, GitHub, tag, release, and goal-completion evidence.
- Reason: the single file was growing back into a bulky historical validator
  after the broader validation refactor.
- Source surfaces updated:
  focused release-support validators,
  focused release-support report validators,
  `scripts/validators/evidence_readouts.py`,
  release-support part-local tests,
  `docs/validation/VALIDATOR_TOPOLOGY.md`,
  `docs/validation/script_inventory.json`,
  `docs/validation/validator_inventory.json`, and
  `mechanics/EVIDENCE_CLUSTERS.md`.
- Validation: `python -m pytest -q
  mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py
  mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py
  mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py`
  and `python -m pytest -q tests/test_validation_topology.py
  tests/test_script_topology.py tests/test_mechanics_topology.py
  tests/test_mechanic_root_district_recon.py`.

### 2026-06-04 - Route and helper validator split

- Previous assumption: `release_support.py` could stay as route/provenance
  owner after reports moved out.
- New reality: the file still carried shared report helpers/constants and route
  behavior, so it remained a broad compatibility container.
- Reason: route/provenance checks and report helper behavior are separate
  support surfaces; neither should silently own the other.
- Source surfaces updated:
  `scripts/validators/release_support.py`,
  focused `scripts/validators/release_support_*` helper modules,
  `scripts/validators/release_support_routes.py`,
  validation inventories, and `mechanics/EVIDENCE_CLUSTERS.md`.
- Validation: see AOA-EV-D-0182.

## Boundaries

This decision does not create a tag, branch, commit, PR, merge, GitHub Release,
or eval result receipt.

It does not treat readiness audit, strategic closeout, or PR handoff reports as
live GitHub Repo Validation evidence.

It does not mark any repo goal complete.

It does not let release-support helper modules own route/provenance meaning or
let `release_support_routes.py` own report artifact meaning.

## Validation

- `python -m pytest -q mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_test_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
