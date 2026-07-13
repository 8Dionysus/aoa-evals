# Questbook Facade Removal

- Decision ID: AOA-EV-D-0193
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused Questbook validator and helper modules
- Refined by: AOA-EV-D-0223

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology, generated/read-model, mechanics/topology
- Mechanic parents: questbook, rpg, agon, cross-parent
- Guard families: source/topology, projection/generated, trace/eval
- Posture: active rationale

## Context

AOA-EV-D-0160, AOA-EV-D-0163, AOA-EV-D-0170, and AOA-EV-D-0176 split
Questbook progression, projection, source, and route behavior into focused
validator modules, but `scripts/validators/questbook.py` still remained as the
public compatibility facade and helper container.

That was useful while callers moved, but it preserved the old pressure: future
Questbook-adjacent checks could still treat `questbook.py` as the natural place
to add behavior.

## Decision

`scripts/validators/questbook.py` is removed.

Shared constants, schema loading, YAML/JSON parsing, repo-root overrides, and
token helper behavior first lived in `scripts/validators/questbook_common.py`.
AOA-EV-D-0219 later split that helper layer into focused context, IO,
source-constant, and orchestrator-constant modules.

Callers import the focused owner directly:

- `scripts/validate_repo.py` imports Questbook schema/lifecycle,
  source-record, obligation-index, generated parity, and progression validators
  directly;
- `scripts/build_catalog.py` imports `questbook_projection_records.py`;
- root and mechanics route orchestration import `questbook_routes.py`;
- Questbook source-record validation imports `questbook_projection_records.py`
  and `questbook_orchestrator_refs.py` for source-bound handoffs; and
- tests import the specific Questbook validator family they exercise.

## Rationale

Questbook has several real boundaries: authored quest source records, generated
reader projection parity, route-card and part-contract topology, and the
Questbook-linked RPG progression bridge. A compatibility facade after the split
is no longer a boundary; it is a historical import convenience.

Removing it makes the focused validators the only active paths and keeps the
shared helper from owning behavior.

## Consequences

- Positive: no Questbook aggregate or compatibility facade remains in
  source-fast topology.
- Positive: build, validation, route orchestration, and tests now name the
  focused Questbook owner they depend on.
- Positive: shared helper code is separated from validator behavior.
- Tradeoff: callers must import more specific Questbook modules.

## Current Applicability

As of 2026-06-04:

- Still valid: Questbook source, projection, route, and progression checks
  remain blocking source-fast guard families.
- Changed: `questbook.py` no longer exists.
- Changed: AOA-EV-D-0219 removes the `questbook_common.py` helper aggregate.
- Further changed by: AOA-EV-D-0197 removes the remaining
  `questbook_projection.py` aggregate; AOA-EV-D-0208 removes the
  `questbook_source.py` aggregate; AOA-EV-D-0223 moves Questbook route path
  constants and route token sets out of `questbook_routes.py` without creating
  a replacement aggregate facade.
- Supersedes: the compatibility-facade shape left by AOA-EV-D-0143,
  AOA-EV-D-0160, AOA-EV-D-0163, AOA-EV-D-0170, and AOA-EV-D-0176.

## Boundaries

This decision does not create a replacement aggregate Questbook validator under
another name.

Questbook helper modules must not own route-token checks, source-record schema
meaning, generated reader parity, RPG progression bridge validation, live task
assignment, proof-surface promotion, owner acceptance, runtime dispatch, or
final quest movement.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
