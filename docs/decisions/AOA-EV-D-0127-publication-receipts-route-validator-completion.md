# Publication Receipts Route Validator Completion

- Decision ID: AOA-EV-D-0127
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validators/publication_receipts_routes.py`, `mechanics/publication-receipts/`
- Refined by: AOA-EV-D-0222

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, publication/receipt, mechanics/topology
- Mechanic parents: publication-receipts, proof-loop, proof-object, cross-parent
- Guard families: source/topology, generated/report/receipt/runtime
- Posture: active rationale

## Context

Decision AOA-EV-D-0120 moved publication receipt payload, live-log, and
dry-review validation into `scripts/validators/publication_receipts.py`.

The publication-receipts route-card and part-contract checks still remained in
the broad `validate_mechanics_surfaces` body. That left one owner organ split
across two validator places: route meaning in root, receipt payload behavior in
the module.

## Options Considered

- Leave route-card checks in `scripts/validate_repo.py` as generic mechanics
  validation.
- Create a second publication-receipts route module.
- Move publication-receipts route, part, provenance, legacy, and decision token
  checks into the existing `scripts/validators/publication_receipts.py` module.

## Decision

Publication-receipts route validation also lives in
`scripts/validators/publication_receipts.py`.

`scripts/validate_repo.py` delegates publication-receipts route-card,
part-contract, provenance, legacy, and decision checks to
`validate_publication_receipts_route_surfaces`.

Tests import publication-receipts constants from
`scripts/validators/publication_receipts.py` directly. `scripts/validate_repo.py`
no longer re-exports publication-receipts compatibility aliases.

## Rationale

Publication receipts are one owner organ: route cards explain the same receipt
sidecar boundary that payload, stats-envelope mirror, live publisher, live log,
and dry-review checks enforce.

Keeping route checks in root made the root validator preserve historical
receipt knowledge after the focused module already existed. Moving the route
checks into the module makes the boundary complete while preserving the rule
that receipts stay weaker than reviewed bundle-local reports.

## Consequences

- Positive: another long route-card block leaves `validate_mechanics_surfaces`.
- Positive: publication-receipts route, payload, and dry-review checks now have
  one validator owner; live-log inspection remains reachable through the
  compatibility adapter and is owned by a narrower validator after D-0161.
- Positive: publication-receipts test fixtures now route to the focused module
  instead of preserving root compatibility aliases.
- Follow-up: audit and boundary-bridge route blocks can receive the same
  treatment when their focused module boundary is ready.

## Current Applicability

As of 2026-06-04:

- Still valid: route-card and part-contract checks remain blocking.
- Changed: route-card and part-contract checks now live in
  `scripts/validators/publication_receipts_routes.py`.
- Changed on 2026-06-05: AOA-EV-D-0222 split route path constants, token
  sets, and route-token lookup helpers out of
  `publication_receipts_routes.py`; the route validator remains the blocking
  route/provenance owner.
- Superseded in part by: AOA-EV-D-0161 for live receipt log validation,
  AOA-EV-D-0180 for route/payload split, and AOA-EV-D-0191 for
  publication-receipts facade removal; AOA-EV-D-0222 for route support-layer
  ownership.

## Review Log

### 2026-06-04 - Live-log validation narrowed

- Previous assumption: publication-receipts route completion meant route,
  payload, live-log, and dry-review checks should share one validator owner.
- New reality: route, payload, and dry-review checks stay together, while
  live-log inspection belongs to a live-publisher and `.aoa/live_receipts/`
  boundary.
- Reason: route-card validation and live append-memory inspection are different
  guard families even when they belong to the same mechanic.
- Source surfaces updated:
  `scripts/validators/publication_receipts.py`,
  `scripts/validators/publication_receipts_live.py`,
  `docs/validation/validator_inventory.json`, and
  `mechanics/EVIDENCE_CLUSTERS.md`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Boundaries

This decision does not make receipts stronger than reviewed reports.

It does not publish, append, rewrite, or accept live receipt entries.

It does not move release-support, runtime integrity review, generated report
index parity, or bundle-local verdict meaning into publication-receipts.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
