# Proof Loop Aggregate Removal

- Decision ID: AOA-EV-D-0211
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused proof-loop route and report validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, trace/eval, report/readout
- Mechanic parents: proof-loop, publication-receipts, proof-object, proof-infra, audit, boundary-bridge
- Guard families: source/topology, generated/report/receipt/runtime
- Posture: active rationale

## Context

AOA-EV-D-0122 moved proof-loop validation out of the broad mechanics pass into
`scripts/validators/proof_loop.py`. That module then carried several different
failure routes in one file:

- proof-loop parent route cards, part index, route-smoke part contract,
  provenance, legacy bridge, and route-smoke decisions;
- the bounded route-smoke report and local-smoke decision; and
- the first bundle-local proof-loop report plus support-route references.

Those surfaces are related by the proof-loop operation, but they do not have the
same owner of truth.

## Options Considered

- Keep `proof_loop.py` as the broad route/report owner.
- Keep `proof_loop.py` as a delegating compatibility facade.
- Remove the aggregate and let `mechanics_routes.py` call focused proof-loop
  validators directly.

## Decision

`scripts/validators/proof_loop.py` is removed.

Active proof-loop validation now routes through:

- `proof_loop_routes.py` for proof-loop route cards, part contracts, provenance,
  legacy lineage, mechanic decision, route-smoke part decision, and
  route-smoke contract decision.
- `proof_loop_smoke_report.py` for the bounded route-smoke report, smoke
  decision, parent route references, and root reports compatibility route.
- `proof_loop_local_report.py` for the bundle-local report, local report
  decision, proof-loop/proof-infra support references, roadmap, and changelog
  posture.
- `proof_loop_common.py` for helper-only path constants, markdown command
  parsing, validation-route text lookup, and decision-index token search.

`mechanics_routes.py` calls the focused validators directly.

## Rationale

Proof-loop is a coordination route, not a single authority surface. The parent
mechanic can say how a proof question moves through proof-object, proof-infra,
audit, receipts, and boundary-bridge support; it should not own the meaning of a
route-smoke payload or a bundle-local report.

Splitting the validators keeps each failure routed to the source that can fix
it. Route-card drift belongs to proof-loop route validation. Route-smoke payload
drift belongs to the route-smoke report validator. Bundle-local report drift
belongs to the source bundle report boundary and support-route references.

## Consequences

- Positive: proof-loop route failures no longer share a module with report
  payload checks.
- Positive: bundle-local report checks stay visibly weaker than receipt
  publication, runtime evidence acceptance, sibling truth, and bundle
  promotion.
- Positive: `proof_loop_common.py` is helper-only and cannot become a hidden
  compatibility facade.
- Tradeoff: mechanics route orchestration imports three focused proof-loop
  validators plus the helper through those modules.

## Current Applicability

As of 2026-06-04:

- Still valid: proof-loop remains a source/topology and trace/eval route gate
  that checks routeability without claiming proof verdict authority.
- Changed: the broad `proof_loop.py` module no longer exists.
- Supersedes: AOA-EV-D-0122 for aggregate proof-loop validator shape.

## Boundaries

This decision does not publish eval result receipts, append live receipt memory,
accept runtime evidence, require sibling-owner approval, promote any bundle, or
claim full proof-loop completeness.

It also does not move bundle-local report authority out of `evals/**/reports/`
or make the route-smoke report stronger than a bounded routeability smoke.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
