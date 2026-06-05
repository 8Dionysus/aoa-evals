# Questbook Progression Validator Boundary

- Decision ID: AOA-EV-D-0160
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/questbook_progression.py`, Questbook-linked RPG progression and unlock proof bridge guard family

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: questbook, rpg, cross-parent
- Guard families: source/topology, trace/eval
- Posture: active rationale

## Context

`scripts/validators/questbook.py` still carried RPG progression evidence and
unlock proof bridge checks because quest source record `AOA-EV-Q-0009` points
at the RPG `progression-unlocks` support surface.

That mixed two owner surfaces:

- Questbook source/projection and route contracts; and
- RPG progression/unlock support contracts referenced by a quest.

The link matters, but the RPG bridge is not Questbook source meaning.

## Decision

Questbook-linked RPG progression and unlock proof bridge validation lives in
`scripts/validators/questbook_progression.py`.

The module owns:

- RPG progression evidence model doc token checks;
- RPG progression evidence schema and example checks;
- RPG unlock proof bridge doc token checks;
- RPG unlock proof schema and example checks;
- legacy playbook quest id and missing progression evidence reference guards.

`scripts/validate_repo.py` calls the progression validator when focused
source-record validation reports quest `AOA-EV-Q-0009` is present. Historical
compatibility adapters were removed later by AOA-EV-D-0193.

## Rationale

Quest records can point at RPG progression surfaces, but they do not make
Questbook the owner of progression evidence, unlock semantics, runtime equip
state, or universal ranking. A separate validator keeps the cross-parent link
visible while preserving RPG ownership.

This also prevents the Questbook validator from becoming a mixed historical
container for every surface referenced by a quest.

## Consequences

- Positive: RPG bridge checks route to a focused module while source records,
  generated readers, route cards, and part contracts stay with their own
  focused validators.
- Positive: RPG progression/unlock bridge checks have their own validator,
  inventory entry, mechanics ledger row, and decision rationale.
- Tradeoff: Questbook still triggers this validator for `AOA-EV-Q-0009` because
  the quest-to-RPG bridge is part of the source-fast proof route.

## Current Applicability

As of 2026-06-04:

- Still valid: Questbook must validate the quest-to-RPG bridge when the unlock
  proof quest is present.
- Changed: bridge logic moved out of `questbook.py` and into
  `questbook_progression.py`; generated projection checks later split into
  `questbook_projection_records.py`, `questbook_projection_parity.py`, and
  `questbook_orchestrator_refs.py` under AOA-EV-D-0197, and
  source-record/lifecycle checks first moved to `questbook_source.py` under
  AOA-EV-D-0170, then split again into `questbook_schema_lifecycle.py`,
  `questbook_source_records.py`, and `questbook_obligation_index.py` under
  AOA-EV-D-0208. Questbook route-card and part-contract checks later moved to
  `questbook_routes.py` under AOA-EV-D-0176.
- Superseded by: AOA-EV-D-0193 removes the remaining `questbook.py`
  compatibility facade; AOA-EV-D-0197 removes the projection aggregate;
  AOA-EV-D-0208 removes the source aggregate.

## Boundaries

This decision does not let `questbook_progression.py` own quest acceptance,
universal score, runtime equip state, generated-card authority, growth-cycle
movement, final quest state movement, or owner acceptance.

It checks the RPG support surface that a Questbook source record references.

## Validation

- `python -m py_compile scripts/validators/questbook_context.py scripts/validators/questbook_io.py scripts/validators/questbook_source_constants.py scripts/validators/questbook_orchestrator_constants.py scripts/validators/questbook_source_records.py scripts/validators/questbook_progression.py scripts/validate_repo.py`
- `python -m pytest -q tests/test_quest_and_reader_surfaces.py tests/test_mechanic_surface_contracts.py -k 'questbook or unlock_proof or progression_unlocks'`
- `python scripts/ci_gate.py --mode source-fast`
