# Questbook Route Validator Layer Split

- Decision ID: AOA-EV-D-0223
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused Questbook route validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: questbook, agon, cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0176 correctly moved Questbook route validation out of the historical
`questbook.py` facade. AOA-EV-D-0193 later removed that facade entirely. The
remaining `questbook_routes.py` file still mixed separate route support layers:

- questbook, quests, integration, part, and decision path constants;
- route, part, lifecycle, obligation-index, integration-note, and decision
  token sets; and
- the blocking Questbook route validators and injected route context.

That file was a real route validator, but it still acted as a constants bucket
for source, lifecycle, obligation, and test helpers.

## Decision

Keep `scripts/validators/questbook_routes.py` as the blocking Questbook route
validator.

Split support layers into focused modules:

- `scripts/validators/questbook_route_paths.py` owns Questbook route path
  constants.
- `scripts/validators/questbook_route_tokens.py` owns Questbook route token
  sets.
- `scripts/validators/questbook_routes.py` owns only the injected
  `QuestbookRouteContext`, quest route validation, and Questbook mechanic route
  validation.

Source constants, obligation-index checks, lifecycle checks, tests, and
fixtures import path or token helpers directly. Root and mechanics route
orchestration still import `questbook_routes.py` for the blocking route gate.

## Rationale

Route path constants, token matrices, and route validation change for different
reasons. Keeping them in one file made `questbook_routes.py` a convenient
landing zone for every Questbook-adjacent source/topology rule.

The split keeps route validation below source quest record schema, generated
reader parity, RPG progression bridge support, public obligation listing, live
task assignment, owner acceptance, and runtime dispatch.

## Consequences

- Positive: `questbook_routes.py` now carries only route validation and the
  context contract needed by route orchestration.
- Positive: source, lifecycle, obligation, and test helpers no longer import a
  route validator just to reuse constants.
- Positive: path and token helpers are non-blocking support surfaces in the
  validation inventory.
- Tradeoff: Questbook callers import more precise helper modules.

## Boundaries

This split does not make route helpers own source quest record schema,
generated quest reader parity, RPG progression bridge support, public obligation
listing, proof-surface promotion, owner acceptance, live task assignment,
runtime dispatch, or final quest state movement.

It does not create a replacement aggregate Questbook facade.

## Validation

- `python -m py_compile scripts/validators/questbook_route_paths.py scripts/validators/questbook_route_tokens.py scripts/validators/questbook_routes.py scripts/validators/questbook_source_constants.py scripts/validators/questbook_obligation_index.py scripts/validators/questbook_schema_lifecycle.py tests/test_quest_and_reader_surfaces.py tests/validate_repo_fixtures.py tests/test_mechanic_surface_contracts.py`
- `python -m pytest -q tests/test_quest_and_reader_surfaces.py tests/test_mechanic_surface_contracts.py -k "questbook or quest_route"`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/ci_gate.py --mode source-fast`
- `python scripts/release_check.py`
