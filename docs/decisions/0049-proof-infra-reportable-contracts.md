# 0049 Proof Infra Reportable Contracts

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/proof-infra/parts/reportable-contracts/`

## Context

After generic fixture families moved behind `proof-infra`, former root
`runners/`, `scorers/`, and `schemas/` still held active shared proof-infra
payloads:

- former root `runners/reportable_proof_contract.md`
- former root `scorers/bounded_rubric_breakdown.py`
- former root `schemas/fixture-contract.schema.json`
- former root `schemas/runner-contract.schema.json`
- former root `schemas/report-summary.schema.json`

These surfaces are not independent parent mechanics. They are shared
reportable proof contract support. Bundle-local
`evals/<family>/<eval>/runners/contract.json` files
consume them through `runner_surface_path` and `scorer_helper_paths`, validators
load their schemas, and generated catalog `proof_artifacts` exposes their paths
without making them proof authority.

## Options Considered

- Leave the active payloads in root `runners/`, `scorers/`, and `schemas/`.
- Create new parent mechanics for runner contracts, scorer helpers, or schemas.
- Move whole root infrastructure districts into `proof-infra`.
- Move only the active shared reportable contract payloads into a
  `proof-infra` part.

## Decision

Move the shared reportable contract payloads to:

`mechanics/proof-infra/parts/reportable-contracts/`

Bundle-local runner contracts now cite:

- `mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md`
- `mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py`

Shared schemas live under:

`mechanics/proof-infra/parts/reportable-contracts/schemas/`

The root `runners/`, `scorers/`, and `schemas/` remain compatibility route cards.

## Rationale

This preserves the distinction between reusable proof infrastructure and proof
meaning. The reportable contract part owns reusable runner/scorer/schema
support. Source bundles own bounded claims, objects under evaluation, verdict
logic, bundle-local report schemas, examples, and reviewed reports.

The route also avoids repeating the earlier error of naming mechanics from
artifact forms. Runner surfaces, scorer helpers, and schemas are parts of the
evals-native `proof-infra` operation, not parent packages.

## Consequences

- Positive: no active shared runner, scorer, or shared contract schema payload
  remains stranded in root compatibility districts.
- Positive: bundle contracts and generated `proof_artifacts` now point at the
  active part-local owner route.
- Tradeoff: path strings are longer, so validators, tests, and generated
  readers must keep the paths aligned.
- Follow-up: if a later reportable contract proves a narrower active mechanic
  owner, move it with its own decision and provenance map.

## Boundaries

This decision does not move source proof bundles, bundle-local runner contracts,
bundle-local report schemas, example reports, reviewed reports, top-level
shared dossiers, generated readers, or domain-owned mechanic support surfaces.

It does not make reportable contracts stronger than bundle-local meaning,
report interpretation, comparison semantics, audit candidate evidence,
publication receipts, sibling owner truth, or AoA center mechanics.

It does not authorize active root payload aliases under `runners/`, `scorers/`,
or `schemas/`.

## Validation

- `mechanics/proof-infra/PARTS.md`
- `mechanics/proof-infra/parts/reportable-contracts/README.md`
- `mechanics/proof-infra/PROVENANCE.md`
- owning proof-infra legacy archive for former root contract placement
- affected bundle `evals/<family>/<eval>/runners/contract.json` paths
- generated catalog `proof_artifacts`
- `python scripts/validate_repo.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_semantic_agents.py`
- `python -m pytest -q mechanics/proof-infra/parts/reportable-contracts/tests/test_bounded_rubric_breakdown.py tests/test_build_catalog.py tests/test_validate_repo.py`
