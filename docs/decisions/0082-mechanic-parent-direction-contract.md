# Mechanic Parent Direction Contract

## Status

Accepted.

## Context

Mechanic parents need an active current-direction surface between the package
entry card and part-local contracts. Without that surface, future edits can
jump from a package README into parts or legacy without seeing the current
operating contour.

## Decision

Every active mechanic parent must expose `DIRECTION.md`.

`DIRECTION.md` owns the current operating direction, source-of-truth split,
current contour, growth rule, stop-lines, and validation posture for the
parent. It is not `PARTS.md`, not a part map, and not provenance.

Parent `README.md` must expose `## Role`, `## Owned Operation`, `## Validation`,
and `## Next Route` around the entry route. The README is the short package
entry card: it names the operation, points validation to `AGENTS.md#validation`,
and tells the next agent which proof pressure belongs here next.

Parent `README.md` and parent `AGENTS.md` must route `DIRECTION.md` from their
entry route before part growth or legacy lookup.

Legacy remains behind `PROVENANCE.md`. Archive details stay inside the owning
`legacy/` archive.

Validator coverage:

```bash
python -m pytest -q tests/test_validate_repo.py -k mechanic_parent_direction
```

## Consequences

Future edits encounter active direction before part growth or legacy lookup.
This makes the active route harder to bypass and keeps archive material from
setting current direction directly.
