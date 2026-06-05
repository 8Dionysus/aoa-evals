# Route Residue Domain Validator Boundaries

- Decision ID: AOA-EV-D-0167
- Status: Accepted
- Date: 2026-06-04
- Owner surface: route residue guard family and focused `scripts/validators/route_residue_*.py` domain modules

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology, generated/read-model, mechanics/topology
- Mechanic parents: cross-parent
- Guard families: source/topology, projection/generated
- Posture: active rationale

## Context

`scripts/validators/route_residue.py` originally moved route residue checks out
of `scripts/validate_repo.py` as one family. After the larger validator cleanup,
it still mixed several residue domains:

- generated/readout JSON walking;
- active mechanic route-card residue;
- root-authored, decision, repo-config, and source-bundle residue; and
- mechanic payload and structured manifest route-field residue.

Generated/readout JSON, active mechanic route cards, root-authored docs,
decision records, repo config, source bundles, and mechanic payload files are
different owner surfaces. They should not remain as historical blocks inside
the same route residue module.

## Decision

Generated/readout route residue validation lives in
`scripts/validators/route_residue_generated.py`.

The module owns generated JSON and part-local generated JSON string-reference
checks for:

- route-card-only root district references;
- legacy mechanic parent references; and
- same-part generated reference allowances.

Mechanic payload route residue validation lives in
`scripts/validators/route_residue_mechanic_payload.py`.

The module owns active mechanic payload and manifest route-field checks for:

- route-card-only root district references;
- legacy mechanic parent references;
- same mechanic or part root allowances;
- repo-qualified sibling allowances; and
- root-authored docs glob resolution in mechanic manifests.

The remaining source-fast residue domains live in focused modules:

- active mechanic route-card residue:
  `scripts/validators/route_residue_active_mechanics.py`;
- root-authored authored-surface residue:
  `scripts/validators/route_residue_root_authored.py`;
- decision-record residue:
  `scripts/validators/route_residue_decisions.py`;
- repo-config residue:
  `scripts/validators/route_residue_repo_config.py`; and
- source-bundle residue:
  `scripts/validators/route_residue_source_bundle.py`.

Shared route-residue context, route-token regexes, and active mechanic token
normalization live in `scripts/validators/route_residue_common.py`.

AOA-EV-D-0192 later removes `scripts/validators/route_residue.py` after
orchestrators and tests import the focused domain modules directly.

## Rationale

Route residue is one guard family, but not one implementation owner. Generated
read models and mechanic payload files fail for different reasons, route to
different owners, and need different allowances.

The split keeps the family visible while preventing one file from becoming a
new `validate_everything.py` for every stale route problem.

## Consequences

- Positive: generated/readout residue now has a generated/read-model validator
  boundary.
- Positive: mechanic-payload residue now has a mechanic payload validator
  boundary.
- Positive: active mechanic, root-authored, decision, repo-config, and
  source-bundle residue checks now have focused source-fast validator
  boundaries.
- Positive: existing callers now import the focused route-residue domain module
  that owns the checked surface.

## Current Applicability

As of 2026-06-04:

- Still valid: route-card-only districts and legacy mechanic parent paths must
  not become current authority.
- Changed: generated/readout, active mechanic, root-authored, decision,
  repo-config, source-bundle, and mechanic-payload route residue logic moved out
  of `route_residue.py`.
- Changed: AOA-EV-D-0192 removes the remaining aggregate facade.
- Superseded in part by: AOA-EV-D-0192 for facade removal.

## Boundaries

This decision does not let generated/readout validators define source meaning,
does not let mechanic-payload residue checks define mechanic payload meaning,
and does not let route-card residue checks define runtime policy or release
artifact truth.

It does not promote route residue checks to runtime policy enforcement,
capability authorization, release artifact freeze, or trace/eval outcome
grading.

## Validation

- `python -m py_compile scripts/validators/route_residue_active_mechanics.py scripts/validators/route_residue_root_authored.py scripts/validators/route_residue_decisions.py scripts/validators/route_residue_repo_config.py scripts/validators/route_residue_source_bundle.py scripts/validators/route_residue_generated.py scripts/validators/route_residue_mechanic_payload.py scripts/validators/route_residue_common.py scripts/validators/root_topology.py scripts/validators/mechanics_routes.py`
- `python -m pytest -q tests/test_route_residue.py tests/test_generated_route_residue.py tests/test_mechanic_manifest_routes.py`
