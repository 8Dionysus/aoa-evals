# Mechanic Part Validation Aggregate Removal

- Decision ID: AOA-EV-D-0195
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused mechanic-part validation modules

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, mechanic part, mechanics/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0165 moved part validation checks into
`scripts/validators/mechanic_part_validation.py`, and AOA-EV-D-0188 removed the
older `mechanic_parts.py` facade. The remaining module still carried two
different boundaries:

- parent `PARTS.md` local route synchronization; and
- part `VALIDATION.md` plus `parts/AGENTS.md` command reachability.

That made the part validation module a new small aggregate after the larger
facade was gone.

## Decision

`scripts/validators/mechanic_part_validation.py` is removed.

The checks now route through focused modules:

- `mechanic_parts_index_sync.py` owns parent `PARTS.md` synchronization against
  actual part directories and the AOA-EV-D-0088 decision posture.
- `mechanic_part_validation_commands.py` owns part validation command
  reachability, command ownership, stale paths, absolute paths, payload anchors,
  and AOA-EV-D-0087/AOA-EV-D-0102 decision posture.
- `mechanic_part_validation_common.py` is helper-only parsing for markdown
  validation sections, python command extraction, and validation route text.

`mechanics_routes.py` calls the index-sync and command validators directly.
Tests import the focused module they exercise.

## Rationale

Parent index synchronization and executable command reachability are adjacent,
but they do not protect the same surface. The first compares a parent route map
to actual part directories. The second checks whether a part's validation route
leaves recoverable, repo-relative executable evidence.

Keeping both behind one module would preserve the historical gate pile at a
smaller scale. Splitting them keeps failure routes local and makes future rules
land in the surface that actually owns them.

## Consequences

- Positive: no mechanic-part validation aggregate remains after the
  `mechanic_parts.py` facade removal.
- Positive: inventories, residual classification, and mechanics evidence ledger
  name the focused boundaries directly.
- Positive: focused mechanic part contract validators use shared helper parsing
  instead of importing through a validation aggregate.
- Tradeoff: `mechanics_routes.py` imports one more focused validator because it
  is the mechanics route-domain orchestrator.

## Current Applicability

As of 2026-06-04:

- Still valid: mechanic parts must keep explicit PARTS index coverage and
  validation-command evidence.
- Changed: those checks no longer share `mechanic_part_validation.py`.
- Supersedes: the aggregate validation-route shape left by AOA-EV-D-0147,
  AOA-EV-D-0165, AOA-EV-D-0175, and AOA-EV-D-0188.
- Refined by: AOA-EV-D-0204 removes the remaining
  `mechanic_part_contracts.py` contract aggregate; AOA-EV-D-0225 splits
  validation-command tokens, parsing, and source collection out of the blocking
  command validator.

## Boundaries

This decision does not let index sync own validation commands, command
reachability own parent `PARTS.md`, helper parsing own any gate meaning, or part
validators define payload meaning.

It does not add a replacement aggregate mechanic-part validation module.

## Validation

- `python -m py_compile scripts/validators/mechanic_part_validation_common.py scripts/validators/mechanic_parts_index_sync.py scripts/validators/mechanic_part_validation_commands.py scripts/validators/mechanic_part_contract_common.py scripts/validators/mechanic_part_contract_index.py scripts/validators/mechanic_part_readme_contract.py scripts/validators/mechanic_part_role_headings.py scripts/validators/mechanics_routes.py tests/test_mechanic_parts_index.py tests/test_mechanic_part_validation_commands.py`
- `python -m pytest -q tests/test_mechanic_parts_index.py tests/test_mechanic_part_validation_commands.py tests/test_mechanic_part_contracts.py -k "mechanic_parts_index_sync or mechanic_part_validation_command or mechanic_part"`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
