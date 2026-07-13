# Publication Receipts Route And Payload Subvalidators

- Decision ID: AOA-EV-D-0180
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/publication_receipts_routes.py`, `scripts/validators/publication_receipts_payload.py`
- Refined by: AOA-EV-D-0222

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, publication/receipt, boundary/runtime
- Mechanic parents: publication-receipts, proof-loop, cross-parent
- Guard families: generated/report/receipt/runtime, report/release/receipt
- Posture: active rationale

## Context

After AOA-EV-D-0161 and AOA-EV-D-0169, live receipt log validation and intake
dry-review validation no longer lived in `publication_receipts.py`. The file
still held two different boundaries:

- publication-receipts route cards, part contracts, validation-route text,
  provenance bridge, legacy archive, and decision-route checks; and
- eval-result receipt guide/schema/example checks plus stats-envelope mirror
  alignment against `aoa-stats`.

Those checks share publication-receipts vocabulary, but they answer different
questions. Route/provenance asks whether the mechanic is correctly bounded.
Payload/schema asks whether the optional receipt sidecar is shaped and mirrored
correctly. Keeping both inside one module preserved a smaller version of the
old broad-validator pressure.

## Decision

Publication-receipts validation is split again:

- `scripts/validators/publication_receipts_routes.py` owns route cards, part
  README/VALIDATION token checks, publication-receipts provenance, legacy
  archive pointers, and publication-receipts decision-route posture.
- `scripts/validators/publication_receipts_payload.py` owns eval-result receipt
  guide tokens, receipt payload schema checks, stats-envelope mirror checks,
  canonical `aoa-stats` enum comparison when available, example envelope
  validation, and repo-qualified evidence refs in the example.

AOA-EV-D-0191 later removes `scripts/validators/publication_receipts.py` after
existing callers move to the focused owner modules. Lightweight source-eval
lookup helpers used by the intake dry-review validator move to
`publication_receipts_common.py`.

## Rationale

Publication receipts are optional publication sidecars. The route/provenance
validator should not define receipt schema semantics, and the payload/schema
validator should not define whether the mechanic route is properly bounded.

The split keeps dry-review, live publication, route topology, and payload shape
as separate organs. It also keeps the old import path stable while making the
future owner boundary explicit in validation topology and inventories.

## Consequences

- Positive: route/provenance and payload/schema checks no longer share a broad
  publication-receipts file.
- Positive: route/provenance and payload/schema failures have separate
  inventory rows, mechanics ledger rows, and failure routes.
- Positive: intake and live validators import focused helpers and no longer
  route through a compatibility facade.

## Current Applicability

As of 2026-06-04:

- Still valid: receipts remain weaker than reviewed bundle-local reports,
  source bundles, proof-loop reports, release evidence, runtime acceptance, and
  canonical `aoa-stats` schema ownership.
- Changed: route/provenance checks moved into
  `publication_receipts_routes.py`; payload/schema checks moved into
  `publication_receipts_payload.py`.
- Changed: AOA-EV-D-0191 removes the remaining compatibility facade.
- Changed on 2026-06-05: AOA-EV-D-0222 keeps
  `publication_receipts_routes.py` as the blocking route/provenance validator
  while moving path constants, token sets, and route-token lookup helpers into
  focused helper modules.
- Superseded in part by: AOA-EV-D-0191 for facade removal and AOA-EV-D-0222
  for route support-layer ownership.

## Boundaries

This decision does not publish receipts, append to `.aoa/live_receipts/`,
accept proof verdict meaning, define source bundle truth, or become release
evidence.

It does not let route/provenance checks own receipt schema meaning.

It does not let payload/schema checks own route cards, provenance, live append
memory, dry-review acceptance, or canonical `aoa-stats` ownership.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
