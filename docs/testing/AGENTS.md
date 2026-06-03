# AGENTS.md

## Applies to

`docs/testing/` topology docs and test coverage inventory.

## Role

This lane names how tests protect `aoa-evals` boundaries. Tests should make the
owner surface visible: source proof object, generated projection, route card,
mechanic part, sibling compatibility, trace/eval scenario, audit report,
release lane, or topology authority.

## Boundaries

- Test files are not command authority.
- Blocking lane commands live in `docs/validation/validation_lanes.json`.
- Root tests protect repo-wide contracts.
- Mechanic part tests stay beside the owning part when the invariant is local.
- Scenario, fault, safety, trace, memory, and handoff tests should be added as
  focused suites with explicit owner routes, not as release-check duplicates.

## Validation

Use:

```bash
python -m pytest -q tests/test_test_topology.py
```

Run broader suites only after the focused topology inventory passes.

## Closeout

Report changed test families, home scopes, coverage authority, focused targets,
and any part-local or advisory surfaces not executed.
