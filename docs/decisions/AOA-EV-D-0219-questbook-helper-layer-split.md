# Questbook Helper Layer Split

- Decision ID: AOA-EV-D-0219
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused Questbook helper modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, quest/lane, generated/readout
- Mechanic parents: questbook, boundary-bridge, cross-parent
- Guard families: source/topology, projection/generated, sibling and boundary
- Posture: active rationale

## Context

After the Questbook facade and source/projection aggregates were removed, the
helper module `scripts/validators/questbook_common.py` still carried several
different surfaces:

- repo-root and `AOA_AGENTS_ROOT` context;
- JSON/YAML/text loading and schema validation helpers;
- quest source/projection paths, states, schema versions, and dispatch artifact
  constants; and
- orchestrator proof constants and alignment tokens.

Those surfaces support different validators and change for different reasons.
Keeping them in one helper kept a small generic Questbook bucket after the
facade removal.

## Decision

Remove `scripts/validators/questbook_common.py`.

Questbook helper behavior is split into focused modules:

- `scripts/validators/questbook_context.py` owns repo-root and sibling-root
  context.
- `scripts/validators/questbook_io.py` owns JSON/YAML/text loading and schema
  validation utilities.
- `scripts/validators/questbook_source_constants.py` owns quest source and
  generated projection constants.
- `scripts/validators/questbook_orchestrator_constants.py` owns orchestrator
  proof constants and alignment tokens.

Focused Questbook validators import these helper surfaces directly.

## Rationale

Questbook source records, generated readers, orchestrator refs, route cards, and
RPG progression bridge checks are separate behavior layers. A shared helper is
acceptable only when it names a narrow support surface. Context, IO,
source/projection constants, and orchestrator constants are not one owner
boundary.

The split keeps helpers below the validators they support and prevents a new
compatibility bucket from replacing the removed Questbook facade.

## Consequences

- Positive: sibling-root override tests now patch `questbook_context.py`
  directly.
- Positive: schema loading no longer sits beside route/projection constants.
- Positive: orchestrator proof constants no longer sit beside source schema
  version constants.
- Tradeoff: Questbook validators import more small helper modules.

## Boundaries

This split does not change Questbook source record meaning, generated reader
freshness rules, route-card validation, RPG progression bridge semantics,
sibling orchestrator truth, live task assignment, owner acceptance, or runtime
dispatch.

It does not create release evidence, runtime acceptance, or goal completion.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
