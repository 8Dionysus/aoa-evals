# AGENTS.md

## Applies to

`docs/validation/` validation topology, command authority, lane manifests, and
validator or script inventories.

## Role

This lane names how `aoa-evals` validation is organized as a bounded proof
organ. It explains which checks are source/topology guards, which are generated
projection parity, which are mechanic-local, which are release-facing, and
which are advisory routes to runtime, trace/eval, memory, handoff, observability,
or security owners.

## Boundaries

- `docs/validation/validation_lanes.json` is the command manifest for named
  lanes in this repository.
- `scripts/validation_lanes.py` is only a loader/API for callers.
- Inventories describe coverage and owner routes. They are not second command
  stores.
- Generated validators check parity and drift; authored source surfaces keep
  proof meaning.
- Advisory runtime, trace/eval, memory, handoff, observability, and security
  notes do not become hard gates without a current owner decision.

## Validation

Use focused topology tests first:

```bash
python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py
```

When command authority or generated parity lanes change, add the touched lane
or release command from `docs/validation/COMMAND_AUTHORITY.md`.

## Closeout

Report changed lane ids, inventory entries, command-authority changes, tests
run, and any lane still marked transitional.
