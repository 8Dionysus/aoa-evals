# Proof-object Validator Layer Split

- Decision ID: AOA-EV-D-0229
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused Proof-object validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, source/topology, mechanics/topology
- Mechanic parents: proof-object, cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0126 correctly moved Proof-object route validation out of the root
mechanics validator. The resulting `scripts/validators/proof_object.py` module
still mixed route path constants, route token matrices, token lookup helpers,
copied `ValidationIssue`/file-read helpers, decision-index companion reads, and
the blocking Proof-object route validator.

That shape kept Proof-object smaller than the root validator, but still made one
module a historical bucket for paths, tokens, helper behavior, and gate logic.

## Decision

Remove `scripts/validators/proof_object.py`.

Split Proof-object validation into focused modules:

- `scripts/validators/proof_object_route_paths.py` owns Proof-object route path
  constants.
- `scripts/validators/proof_object_route_tokens.py` owns Proof-object route
  token sets and forbidden route phrases.
- `scripts/validators/proof_object_route_helpers.py` owns token lookup,
  decision-index companion text, and validation-route companion text.
- `scripts/validators/proof_object_routes.py` owns the blocking Proof-object
  route validator.

The helper uses shared `validators.common.ValidationIssue` and
`read_text_or_issue` instead of local copies. Mechanics route orchestration
imports only `proof_object_routes.py`. Tests import path helpers directly.

## Rationale

Proof-object is the authored eval source-authority surface for source eval
packages, authoring templates, eval contract schemas, provenance, and part
decisions. Its validator must protect routeability without becoming the owner of
source eval meaning, generated readers, report verdicts, receipts, runtime
candidates, sibling refs, or quest dispatch.

Separating path constants, token matrices, lookup helpers, and route checks
keeps that boundary explicit while removing duplicated helper code.

## Consequences

- Positive: the former broad Proof-object module is gone rather than preserved
  as a compatibility entrypoint.
- Positive: Proof-object route validation now uses shared common
  issue/read helpers.
- Positive: tests no longer import constants from the blocking Proof-object
  validator.
- Tradeoff: Proof-object route validation imports three focused helper modules.

## Boundaries

This split does not make Proof-object validators own source eval proof meaning,
generated catalog/capsule/section freshness, bundle-local reports, publication
receipts, runtime candidates, sibling truth, or quest dispatch.

It does not create a replacement Proof-object aggregate facade.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
