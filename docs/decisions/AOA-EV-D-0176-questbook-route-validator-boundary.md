# Questbook Route Validator Boundary

- Decision ID: AOA-EV-D-0176
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/questbook_routes.py`, `mechanics/questbook/README.md`
- Refined by: AOA-EV-D-0223

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: questbook, agon, cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

After generated projection, RPG progression bridge, and source-record lifecycle
checks moved into focused modules, `scripts/validators/questbook.py` still
carried Questbook route cards, quests route cards, lifecycle route residue,
Agon quest-note provenance routing, part owner-split contracts, and public
compatibility aliases in one module.

That left the facade as another historical accumulation point. It was smaller
than before, but still mixed the public import surface with the actual
route-token owner.

## Decision

Questbook route-card and mechanic route validation lives in
`scripts/validators/questbook_routes.py`.

The module owns:

- `quests/README.md`, `quests/AGENTS.md`, and `quests/LIFECYCLE.md` route
  token checks;
- stale top-level quest source and markdown note residue checks;
- Agon quest-note provenance route decision checks;
- Questbook parent route cards and provenance posture;
- Questbook source-record and dispatch-reader part README route checks;
- Questbook mechanic and part owner-split decision token checks; and
- the injected `QuestbookRouteContext` contract used by root and mechanics
  aggregators.

Historical compatibility imports were removed later by AOA-EV-D-0193; route
callers import `questbook_routes.py` directly.

## Rationale

Route cards answer where a quest obligation may move next. Source records answer
what the authored quest is. Generated readers answer whether the projection is
fresh. RPG progression support answers whether a referenced proof bridge is
well-shaped.

Keeping route-token checks in the compatibility facade blurred those boundaries
and made `questbook.py` look like the natural place to add every future
Questbook-adjacent guard. A focused route validator keeps the boundary visible
without making generated, source, runtime, or progression checks subordinate to
route prose.

## Consequences

- Positive: `questbook_routes.py` owns route-card token matrices directly.
- Positive: Questbook route checks have their own validator inventory row,
  mechanics ledger row, and decision rationale.
- Tradeoff: callers must import `questbook_routes.py` rather than a broad
  Questbook facade.

## Current Applicability

As of 2026-06-04:

- Still valid: Questbook route cards, quests route cards, part route contracts,
  and route decisions must remain source/topology validation gates.
- Changed: route-card, stale residue, part owner-split, and route-decision
  checks moved out of `questbook.py` and into `questbook_routes.py`.
- Changed on 2026-06-05: AOA-EV-D-0223 keeps
  `questbook_routes.py` as the blocking route validator while moving route path
  constants and token sets into focused helper modules.
- Superseded by: AOA-EV-D-0193 removes the remaining `questbook.py`
  compatibility facade; AOA-EV-D-0223 for route support-layer ownership.

## Review Log

### 2026-06-14 - Stale quest route scaffold coverage expanded

- Previous assumption: stale negative quest route scaffold checks only needed to
  cover `quests/README.md` and `quests/LIFECYCLE.md`.
- New reality: stale negative quest route scaffold checks also cover
  `quests/AGENTS.md`.
- Reason: route-card drift can reappear through the quest agent guidance
  surface, not only through the public README or lifecycle card.
- Source surfaces updated: `scripts/validators/questbook_routes.py` and its
  focused quest-route scaffold regression.
- Validation: PR #388 Repo Validation covered the route scaffold guard.

## Boundaries

This decision does not let `questbook_routes.py` own source quest record schema,
active/closed listing semantics, generated quest reader parity, RPG progression
bridge support, live task assignment, proof-surface promotion, owner acceptance,
runtime dispatch, or final quest state movement.

Those route respectively to `questbook_schema_lifecycle.py`,
`questbook_source_records.py`, `questbook_obligation_index.py`,
`questbook_projection_records.py`, `questbook_projection_parity.py`,
`questbook_orchestrator_refs.py`, `questbook_progression.py`, and stronger
runtime or owner surfaces.

## Validation

- `python -m py_compile scripts/validators/questbook_context.py scripts/validators/questbook_io.py scripts/validators/questbook_route_paths.py scripts/validators/questbook_route_tokens.py scripts/validators/questbook_source_constants.py scripts/validators/questbook_orchestrator_constants.py scripts/validators/questbook_routes.py scripts/validators/questbook_schema_lifecycle.py scripts/validators/questbook_source_records.py scripts/validators/questbook_obligation_index.py scripts/validators/questbook_projection_records.py scripts/validators/questbook_projection_parity.py scripts/validators/questbook_orchestrator_refs.py scripts/validators/questbook_progression.py`
- `python -m pytest -q tests/test_quest_and_reader_surfaces.py tests/test_mechanic_surface_contracts.py -k 'questbook or quest_route'`
- `python -m json.tool docs/validation/script_inventory.json`
- `python -m json.tool docs/validation/validator_inventory.json`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
