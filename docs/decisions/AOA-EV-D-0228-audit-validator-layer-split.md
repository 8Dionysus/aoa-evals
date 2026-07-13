# Audit Validator Layer Split

- Decision ID: AOA-EV-D-0228
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused Audit validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, mechanics/topology, audit/observability
- Mechanic parents: audit, cross-parent
- Guard families: source/topology, runtime-policy
- Posture: active rationale

## Context

AOA-EV-D-0128 correctly moved Audit route validation out of the root mechanics
validator. The resulting `scripts/validators/audit.py` module still mixed route
paths, route tokens, token lookup helpers, copied `ValidationIssue`/file-read
helpers, and the blocking audit route validator.

That shape made Audit a smaller but still historical script: it had its own
common helper copies and tests imported constants from the blocking validator.

## Decision

Remove `scripts/validators/audit.py`.

Split Audit validation into focused modules:

- `scripts/validators/audit_route_paths.py` owns Audit route path constants.
- `scripts/validators/audit_route_tokens.py` owns Audit route token sets and
  forbidden route phrases.
- `scripts/validators/audit_route_helpers.py` owns token lookup, decision-index
  companion text, and validation-route companion text.
- `scripts/validators/audit_routes.py` owns the blocking Audit route validator.

The helper uses shared `validators.common.ValidationIssue` and
`read_text_or_issue` instead of local copies. Mechanics route orchestration
imports only `audit_routes.py`. Tests import path helpers directly.

## Rationale

Audit is a boundary organ for candidate evidence, selected evidence packets,
artifact verdict hooks, candidate readers, integrity review, provenance, and
legacy routing. It must not quietly become the runtime evidence owner or source
bundle proof owner.

Separating path constants, token matrices, lookup helpers, and route checks
keeps Audit validation focused while removing duplicated helper code.

## Consequences

- Positive: the former broad Audit module is gone rather than preserved as a
  compatibility entrypoint.
- Positive: Audit route validation now uses shared common issue/read helpers.
- Positive: tests no longer import constants from the blocking Audit validator.
- Tradeoff: Audit route validation imports three focused helper modules.

## Boundaries

This split does not make Audit validators own runtime evidence acceptance,
runtime facts, selected evidence proof canon, source bundle proof
interpretation, receipt publication, generated reader freshness, or runtime
outcomes.

It does not create a replacement Audit aggregate facade.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
