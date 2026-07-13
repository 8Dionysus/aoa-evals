# Publication Receipts Route Validator Layer Split

- Decision ID: AOA-EV-D-0222
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused publication receipt route validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, publication/receipt, observability/audit
- Mechanic parents: publication-receipts, proof-loop, cross-parent
- Guard families: source/topology, generated/report/receipt/runtime
- Posture: active rationale

## Context

AOA-EV-D-0180 correctly split publication-receipts route/provenance checks from
receipt payload/schema checks. AOA-EV-D-0191 then removed the old
`publication_receipts.py` compatibility facade. The remaining route validator
still carried four different support layers in one file:

- route, part, report, publisher, legacy, and decision path constants;
- route, part, provenance, legacy, and intake dry-review token sets;
- route-token lookup helpers that read part `VALIDATION.md` companions and
  decision indexes; and
- the blocking route/provenance validator.

That file was no longer a facade, but it still mixed helper ownership with the
actual route gate.

## Decision

Keep `scripts/validators/publication_receipts_routes.py` as the blocking
publication-receipts route/provenance validator.

Split its support layers into focused modules:

- `scripts/validators/publication_receipts_route_paths.py` owns route path
  constants.
- `scripts/validators/publication_receipts_route_tokens.py` owns route token
  sets.
- `scripts/validators/publication_receipts_route_helpers.py` owns route-token
  lookup helpers and companion validation-route text loading.
- `scripts/validators/publication_receipts_routes.py` owns only route,
  part-contract, provenance, legacy, and decision-route validation.

Intake dry-review validators import path constants, token sets, and lookup
helpers directly. Tests import path constants from
`publication_receipts_route_paths.py`. Mechanics route orchestration still
imports `publication_receipts_routes.py` for the blocking route gate.

## Rationale

Path constants, token matrices, lookup helpers, and route validation change for
different reasons. Keeping them together made the route validator a tempting
landing zone for future receipt-adjacent rules.

The split keeps route validation below receipt payload/schema meaning,
dry-review artifact meaning, live append-memory inspection, and bundle-local
proof verdict meaning.

## Consequences

- Positive: the route validator now carries only route/provenance validation.
- Positive: intake dry-review validators no longer import the route validator
  just to reuse constants or token sets.
- Positive: path and token helpers are non-blocking support surfaces in the
  validation inventory.
- Tradeoff: tests and intake validators import more precise helper modules.

## Boundaries

This split does not publish receipts, append to `.aoa/live_receipts/`, accept
proof verdict meaning, define source bundle truth, or become release evidence.

It does not make route helpers own receipt payload schema, dry-review artifact
shape, live receipt JSONL inspection, or canonical `aoa-stats` ownership.

It does not create a replacement aggregate publication-receipts facade.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
