# Publication Receipts Facade Removal

- Decision ID: AOA-EV-D-0191
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused publication-receipts route, payload, intake, live, and helper validators
- Refined by: AOA-EV-D-0222

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, publication/receipt, boundary/runtime, observability/audit
- Mechanic parents: publication-receipts, proof-loop, cross-parent
- Guard families: generated/report/receipt/runtime, report/release/receipt, observability/audit
- Posture: active rationale

## Context

AOA-EV-D-0161, AOA-EV-D-0169, and AOA-EV-D-0180 split
publication-receipts validation into focused route, payload, intake, live, and
common helper modules. After callers could import those owner modules directly,
`scripts/validators/publication_receipts.py` only preserved historical import
compatibility.

The facade no longer protected a validator boundary.

## Decision

`scripts/validators/publication_receipts.py` is removed.

Mechanics route orchestration imports
`publication_receipts_routes.validate_publication_receipts_route_surfaces`
directly.

Evidence readout orchestration imports the focused payload, intake dry-review,
and live receipt validators directly.

Source-eval lookup helpers used by the intake dry-review validator move to
`publication_receipts_common.py`.

## Rationale

Publication receipts have several adjacent but distinct boundaries:

- route/provenance posture;
- payload/schema and stats-envelope mirror posture;
- dry-review non-publication posture; and
- owner-local live JSONL inspection.

Keeping an aggregate facade after the split would invite future checks to land
in a generic publication-receipts bucket instead of the owning boundary.

## Consequences

- Positive: no publication-receipts compatibility validator remains in
  source-fast topology.
- Positive: live, intake, payload, and route checks are direct hard gates.
- Positive: shared source-eval lookup helpers live in common helper code
  without owning receipt meaning.
- Tradeoff: orchestrators import several focused publication-receipts modules.

## Current Applicability

As of 2026-06-04:

- Still valid: receipt validation remains blocking below bundle-local reports,
  source bundles, runtime acceptance, and canonical `aoa-stats` ownership.
- Changed: `publication_receipts.py` no longer exists.
- Changed: AOA-EV-D-0214 later removes the broad intake validator and splits
  dry-review route, artifact, candidate-preview, and boundary checks.
- Changed: AOA-EV-D-0222 later narrows the route validator by moving route
  paths, route tokens, and route-token lookup helpers into focused helper
  modules without creating a replacement aggregate facade.
- Supersedes: the compatibility-facade shape left by AOA-EV-D-0120,
  AOA-EV-D-0161, AOA-EV-D-0169, and AOA-EV-D-0180.

## Boundaries

This decision does not publish receipts, append to `.aoa/live_receipts/`,
accept proof verdict meaning, define source bundle truth, or become release
evidence.

It does not add a replacement aggregate publication-receipts facade under
another name.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
