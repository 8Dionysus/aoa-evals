# Mechanic PARTS Index Synchronization

- Decision ID: AOA-EV-D-0088
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/README.md`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: mechanic part, validation guard
- Mechanic parents: cross-parent
- Guard families: part and payload
- Posture: active guard rationale

## Context

Parent mechanics now own active `PARTS.md` maps and concrete
`mechanics/<parent>/parts/<part>/README.md` contracts. The existing guard
already checked that every actual part directory had some route from the parent
`PARTS.md`, but it did not fully protect the reverse direction.

A parent `PARTS.md` can become stale after a part move or deletion. That would
leave the active map claiming a local part route that no longer exists, while
the real proof operation has moved elsewhere or never existed.

## Options Considered

- Keep the existing one-way check from actual part directory to `PARTS.md`.
- Forbid every `parts/<name>` reference in `PARTS.md` unless it is local.
- Add a local index synchronization guard that distinguishes local part routes
  from cross-parent references.

## Decision

Every `mechanics/<parent>/PARTS.md` must synchronize its declared local parts
with the actual part directory set under `mechanics/<parent>/parts/`.

`scripts/validate_repo.py` rejects:

- an actual part directory that is not declared as a local declared part route;
- a stale local part route with no matching actual part directory.

Cross-parent reference paths, such as a stop-line that routes pressure to
`mechanics/distillation/parts/runtime-candidate-adoption/`, remain allowed.
They are owner-split or stop-line references, not local part declarations for
the current parent.

## Rationale

The mechanics atlas needs convex topology: the local map should expose exactly
the local parts it owns, while still being able to point outward to stronger or
adjacent owner routes.

This preserves the difference between "this parent owns this part" and "this
parent must not steal that other part." That distinction matters especially for
Experience versus Distillation, Growth Cycle versus Antifragility/RPG, and
Method-growth versus Repair/RPG pressure.

## Consequences

- Positive: parent `PARTS.md` files remain truthful after part moves.
- Positive: cross-parent stop-lines stay expressible without becoming local
  topology.
- Positive: stale local part routes are caught by standard repository
  validation.
- Tradeoff: moving or deleting a part now requires updating the parent
  `PARTS.md` in the same slice.

## Boundaries

This decision does not require every cross-parent reference to become a local
part.

It does not create new parent mechanics, promote deferred pressure, or treat a
stop-line reference as proof that the referenced part is complete.

It does not replace the concrete part README, payload inventory, validation
command reachability, or legacy/provenance guards.

## Validation

```bash
python -m pytest -q tests/test_validate_repo.py -k mechanic_parts_index_sync
python scripts/validate_repo.py
```
