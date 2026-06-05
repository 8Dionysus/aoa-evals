# Proof-infra Route Token Layer Split

- Decision ID: AOA-EV-D-0230
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused Proof-infra route validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, mechanics/topology, fixture/support
- Mechanic parents: proof-infra, proof-object, cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0201 removed the old Proof-infra aggregate and split route checks from
shared-support checks. The route validator still kept all route token matrices
and stale phrase lists inside `scripts/validators/proof_infra_routes.py`.

That made the blocking route validator double as a constants bucket for tests.

## Decision

Keep `scripts/validators/proof_infra_routes.py` as the blocking Proof-infra
route gate, but move route token sets and stale phrase lists into
`scripts/validators/proof_infra_route_tokens.py`.

Tests import path constants from `proof_infra_common.py` and stale phrase
constants from `proof_infra_route_tokens.py`. Route orchestration still imports
only `proof_infra_routes.py`.

`proof_infra_common.py` now uses shared `decision_index_paths.GENERATED_INDEX_PATHS`
for decision-index companion reads instead of keeping a local generated-index
path list.

## Rationale

Proof-infra route validation protects reusable fixture families,
runner/scorer/schema contract routes, provenance, legacy routing, and decisions.
The token matrix is route data, not the gate itself.

Separating tokens from the blocking validator keeps tests from treating the gate
as a constants bucket and removes another local copy of generated decision-index
paths.

## Consequences

- Positive: `proof_infra_routes.py` is now a thin route gate.
- Positive: Proof-infra token data has a named helper boundary.
- Positive: common Proof-infra helper code uses the shared decision-index path
  source.
- Tradeoff: Proof-infra route validation imports one additional helper module.

## Boundaries

This split does not make Proof-infra own source bundle meaning, shared guide
exercise, generated catalog freshness, bundle-local reports, publication
receipts, release packaging, or runtime outcomes.

It does not create a replacement Proof-infra aggregate facade.

## Validation

- `python -m py_compile scripts/validators/proof_infra_common.py scripts/validators/proof_infra_route_tokens.py scripts/validators/proof_infra_routes.py scripts/validators/mechanics_routes.py tests/test_mechanic_surface_contracts.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k proof_infra`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/ci_gate.py --mode source-fast`
- `python scripts/release_check.py`
