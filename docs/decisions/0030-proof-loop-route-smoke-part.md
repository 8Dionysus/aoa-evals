# 0030 Proof Loop Route-Smoke Part

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/proof-loop/`

## Context

The first proof-loop route-smoke report was created to test whether one local
proof question could move through the proof-loop route into a bounded report
without promoting generated readers, runtime candidates, sibling refs, or
receipts into authority.

After comparison-spine and release-support reports moved into mechanic-owned
parts, the former root `reports/` district still carried
`reports/proof-loop-local-route-smoke-v1.md`. That was no longer the cleanest
topology: the report is not a general cross-bundle dossier. It is the first
proof-loop route-smoke artifact and belongs to the proof-loop mechanic.

## Options Considered

- Leave the route-smoke report under `reports/` as a special-case exception.
- Move the report directly under `mechanics/proof-loop/`.
- Create a proof-loop parts map and move the report under a `route-smoke` part.

## Decision

Create the proof-loop parts map:

- `mechanics/proof-loop/PARTS.md`
- `mechanics/proof-loop/parts/README.md`
- `mechanics/proof-loop/parts/route-smoke/README.md`

Move the route-smoke report to:

`mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md`

## Rationale

The report is proof-loop-owned evidence about routeability. Putting it in a
part keeps the parent mechanic as the operation route while making the report's
narrow role visible.

Leaving it under root `reports/` would keep a future bug alive: a reader could
mistake root reports for the owner of proof-loop route-smoke artifacts. Moving
it directly into the package root would flatten the mechanic and leave no place
for later proof-loop report families if they become real.

## Consequences

- Positive: root `reports/` now keeps only repo-wide report-district guidance
  unless a future artifact truly lacks a narrower mechanic owner.
- Positive: `mechanics/proof-loop/` now has a `PARTS.md` contract like other
  artifact-owning mechanics.
- Positive: validators and tests now follow the part-local route-smoke path.
- Tradeoff: historical references to the old root report path must be updated
  or treated as legacy prose only.

## Boundaries

This decision does not create an eval result receipt, promote
`aoa-verification-honesty`, accept runtime evidence, approve sibling truth, or
make the proof-loop mechanic a proof authority.

It only moves the route-smoke artifact into its mechanic-owned part.

## Validation

- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
- `python -m pytest -q tests/test_validate_repo.py -k proof_loop`
