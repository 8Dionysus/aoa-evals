# Mechanic Part Validation-command Layer Split

- Decision ID: AOA-EV-D-0225
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused mechanic-part validation-command modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, mechanic part, mechanics/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0195 removed the mechanic-part validation aggregate and left
`scripts/validators/mechanic_part_validation_commands.py` as the focused owner
for validation-command reachability. That module still mixed four support
layers:

- decision names, required decision tokens, and the focused test command;
- command string parsing into referenced repo-relative paths;
- route source collection from README, `VALIDATION.md`, and parent
  `parts/AGENTS.md`; and
- the blocking validator that checks command ownership, stale paths, absolute
  paths, payload anchors, and decision posture.

That was not a historical facade, but it was still too broad for a durable
boundary.

## Decision

Keep `scripts/validators/mechanic_part_validation_commands.py` as the blocking
mechanic part validation-command validator.

Split support layers into focused helper modules:

- `scripts/validators/mechanic_part_validation_command_tokens.py` owns decision
  path constants, required token sets, and the focused test command.
- `scripts/validators/mechanic_part_validation_command_parsing.py` owns command
  string parsing.
- `scripts/validators/mechanic_part_validation_command_sources.py` owns source
  collection and payload-anchor support.
- `scripts/validators/mechanic_part_validation_commands.py` owns only the
  blocking validator and its issue assembly.

Tests import token constants directly. The blocking validator imports helpers
directly. No replacement aggregate facade is added.

## Rationale

Executable validation routes protect a different surface than command parsing
or source collection. The blocking validator should decide whether a part's
validation evidence is reachable and payload-aware, but helper modules should
not become additional owners of command policy.

The split keeps command parsing reusable only as parsing, source collection
reusable only as source collection, and decision tokens visible without making
the validator module a constants bucket for tests or reports.

## Consequences

- Positive: the remaining command validator is smaller and owns only the hard
  gate.
- Positive: tests no longer import decision constants from the blocking
  validator.
- Positive: validator and script inventories classify parser, source, and token
  helpers explicitly as non-blocking support surfaces.
- Tradeoff: the command validator imports three helper modules.

## Boundaries

This split does not let helper modules own validation-command policy,
repo-relative reachability, stale path detection, payload-anchor requirements,
PARTS index synchronization, README contracts, source-surface refs, generated
parity, runtime policy, or part payload meaning.

It does not create a replacement mechanic-part validation-command aggregate.

## Validation

- `python -m py_compile scripts/validators/mechanic_part_validation_command_tokens.py scripts/validators/mechanic_part_validation_command_parsing.py scripts/validators/mechanic_part_validation_command_sources.py scripts/validators/mechanic_part_validation_commands.py tests/test_mechanic_part_validation_commands.py`
- `python -m pytest -q tests/test_mechanic_part_validation_commands.py -k mechanic_part_validation_command`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/ci_gate.py --mode source-fast`
- `python scripts/release_check.py`
