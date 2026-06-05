# Mechanic Part Validation Route Validator Boundary

- Decision ID: AOA-EV-D-0165
- Status: Accepted
- Date: 2026-06-04
- Owner surface: mechanic part validation route guard family, `mechanics/AGENTS.md`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, mechanic part, mechanics/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

`scripts/validators/mechanic_parts.py` carried both mechanic part README/payload
contracts and validation-route checks:

- parent `PARTS.md` synchronization;
- part `VALIDATION.md` and parent `parts/AGENTS.md` validation route checks;
- validation command parsing and reachable path checks;
- payload coverage anchors for parts with payload; and
- validation-command decision-token posture.

Those checks are part-local, but they are not the same owner surface as README
contract shape, payload inventory, source-surface refs, or index H1 role checks.

## Decision

Mechanic part index-sync and validation-command validation initially moved into
`scripts/validators/mechanic_part_validation.py`. AOA-EV-D-0195 later removes
that aggregate and splits it into `mechanic_parts_index_sync.py` and
`mechanic_part_validation_commands.py`.

The module owns:

- local part slug discovery from parent `PARTS.md`;
- stale/missing part route checks;
- part validation route source collection from README, `VALIDATION.md`, and
  parent `parts/AGENTS.md`;
- validation command parsing and repo-relative path reachability;
- payload coverage anchor checks; and
- validation-command and parts-index decision-token checks.

`scripts/validators/mechanic_parts.py` remains the public compatibility surface.
README/index, payload inventory, and source-surface checks route through focused
contract modules. It delegates validation route behavior to
the mechanic part validation route guard family.

## Rationale

Validation commands are executable route evidence. They should prove that a part
has reachable, local, payload-aware checks, but they should not define the part's
payload meaning or source-surface contract.

Splitting the module keeps two questions separate:

- `mechanic_part_contracts.py`: does the part describe and bound its contract?
- `mechanic_part_validation_commands.py`: does the part route executable
  validation to owned, reachable validation surfaces?

This prevents the part contract validator from growing back into a historical
catch-all for every mechanic part rule.

## Consequences

- Positive: mechanic part README/index contracts, payload inventory, source
  refs, and validation-command routes now have separate validator modules.
- Positive: validation-command and PARTS index-sync checks have their own
  validator, inventory entries, mechanics ledger row, and decision rationale.
- Historical note: at the time, tests and callers could still import public
  helpers from `mechanic_parts.py` through thin compatibility adapters. Later
  decisions remove that facade and the remaining validation aggregate.
- Tradeoff: the mechanics route-domain orchestrator still calls focused part
  validators because part contracts are incomplete without reachable validation
  evidence.

## Current Applicability

As of 2026-06-04:

- Still valid: mechanic parts must keep explicit validation route evidence.
- Changed: validation-command and PARTS index-sync logic moved out of
  `mechanic_parts.py`; AOA-EV-D-0195 later splits the remaining aggregate into
  `mechanic_part_validation_commands.py` and `mechanic_parts_index_sync.py`.
- Superseded by: AOA-EV-D-0195 for the no-aggregate current shape.

## Boundaries

This decision does not let validation commands define part payload meaning,
source eval meaning, generated parity, release artifact freeze, runtime policy,
or trace/eval grading.

It does not move README contract, payload inventory, source-ref, or index-role
checks into the validation-command or index-sync validators.

## Validation

- `python -m py_compile scripts/validators/mechanic_parts_index_sync.py scripts/validators/mechanic_part_validation_commands.py scripts/validators/mechanic_part_validation_common.py scripts/validators/mechanics_routes.py tests/test_mechanic_parts_index.py tests/test_mechanic_part_validation_commands.py`
- `python -m pytest -q tests/test_mechanic_parts_index.py tests/test_mechanic_part_validation_commands.py tests/test_mechanic_part_contracts.py tests/test_index_surface_roles.py`
