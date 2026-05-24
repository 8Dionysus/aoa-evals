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

## Current Applicability

As of 2026-05-24:

- Still valid: `route-smoke` remains the only active Proof Loop part and owns
  the first public-safe route-smoke report.
- Changed: the lower `mechanics/proof-loop/parts/README.md` now exposes an
  operating card, active part row, owner pressure routes, and part admission
  route before sending agents into `route-smoke/`.
- Superseded by: none.

## Review Log

### 2026-05-24 - Lower parts index operating route

- Previous assumption: the lower Proof Loop parts README could stay as a short
  pointer because the parent `PARTS.md` and route-smoke part README carried the
  contract.
- New reality: the lower index now names role, input, output, owner, next
  route, validation lane, owner pressure routes, and admission tests.
- Reason: a low-context agent entering `mechanics/proof-loop/parts/` should
  route source proof, support contracts, candidate evidence, sibling refs,
  receipts, route-smoke scope, and future proof-loop families without reading a
  thin placeholder first.
- Source surfaces updated: `mechanics/proof-loop/parts/README.md`,
  `scripts/validate_repo.py`, and `tests/test_validate_repo.py`.
- Validation: focused lower-index validator tests, root validation, semantic
  AGENTS validation, generated catalog check, diff whitespace check, and full
  pytest.

## Validation

- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
- `python -m pytest -q tests/test_validate_repo.py -k proof_loop`
