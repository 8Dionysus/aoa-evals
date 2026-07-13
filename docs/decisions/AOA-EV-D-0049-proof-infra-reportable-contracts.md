# Proof Infra Reportable Contracts

- Decision ID: AOA-EV-D-0049
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/proof-infra/parts/reportable-contracts/`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: report/release/receipt
- Mechanic parents: proof-infra
- Guard families: generated/report/receipt/runtime
- Posture: report/release/receipt rationale

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

## Current Applicability

As of 2026-05-24:

- Still valid: reportable contracts route through
  `mechanics/proof-infra/parts/reportable-contracts/` when bundle-local runner
  contracts consume `runner_surface_path`, `scorer_helper_paths`, or shared
  schemas.
- Still valid: source bundles, bundle-local schemas, examples, and reviewed
  reports own proof interpretation.
- Changed: active part route text now expresses scorer, runner, schema, root
  alias, and report pressure as boundary routes instead of prohibition-heavy
  prose.
- Changed: descendant `AGENTS.md` now exposes an Operating Card and boundary
  route table for low-context agents while routing executable checks to the
  parent `parts/AGENTS.md` lane.
- Source surfaces updated:
  `mechanics/proof-infra/PARTS.md`,
  `mechanics/proof-infra/parts/reportable-contracts/README.md`,
  `mechanics/proof-infra/parts/reportable-contracts/AGENTS.md`,
  `scripts/validate_repo.py`.

## Review Log

### 2026-05-24 - Boundary-route wording

- Previous assumption: reportable-contract stop-lines needed repeated
  negative wording around scorer helpers, shared runner surfaces, root aliases,
  and bundle-local reports.
- New reality: the invariant is clearer as a route map: scoring pressure routes
  to source-bundle bounded review, shared-runner pressure routes to
  bundle-local interpretation, weak-report pressure routes to evidence or
  schema fit, root alias pressure routes to route-card-only districts, and
  reviewed-report pressure routes back to the source bundle.
- Reason: the active part already names inputs, outputs, stronger owner split,
  payload homes, and validation; the boundary is easier for agents to follow
  when each pressure has an owner route.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-05-24 - Agent route-card applicability

- Previous assumption: the descendant reportable-contract `AGENTS.md` could
  repeat local role limits and command blocks.
- New reality: the parent `parts/AGENTS.md` already owns centralized child
  validation commands, so the descendant card is clearer as an Operating Card
  plus boundary routes.
- Reason: low-context agents need role, input, output, owner, next route,
  tools, and validation ownership at the file boundary without duplicating the
  parent command lane.
- Source surfaces updated:
  `mechanics/proof-infra/parts/reportable-contracts/AGENTS.md`,
  `scripts/validate_repo.py`,
  `tests/test_validate_repo.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
