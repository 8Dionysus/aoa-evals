# Mechanic Provenance Bridge Posture

## Status

Accepted.

## Context

`PROVENANCE.md` is the only active-side bridge from a mechanic parent into its
legacy archive. It is not the current operating route for the mechanic, and it
is not the archive inventory.

Without an explicit bridge posture, a future edit can accidentally put archive
detail in the bridge itself. That would create a second working route beside
the active parent, direction, part map, and archive-local accounting.

## Decision

Every active mechanic `PROVENANCE.md` must state:

- `PROVENANCE.md` is a bridge, not an active route.
- Use active surfaces first:
- `DIRECTION.md` is part of the active route before legacy lookup.
- The bridge opens `legacy/README.md`.
- The legacy archive owns its own details.

Validator coverage:

```bash
python -m pytest -q tests/test_validate_repo.py -k mechanic_provenance_bridge_posture
```

## Consequences

Active mechanic work starts from `README.md`, `DIRECTION.md`, `PARTS.md`, and
`parts/`. `PROVENANCE.md` opens the archive only after those active surfaces are
insufficient.

This keeps legacy important but archival: one bridge from active mechanics, and
then detailed accounting inside legacy.
