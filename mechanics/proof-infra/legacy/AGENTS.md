# AGENTS.md

## Applies to

`mechanics/proof-infra/legacy/`.

## Role

Legacy preserves old path lineage for proof-infra surfaces.

It does not own active fixture-family contracts, bundle meaning, generated
truth, or new work.

## Rules

- Start from `mechanics/proof-infra/README.md` and `PARTS.md` before reading
  legacy.
- Keep old root paths mapped to current active routes.
- Do not create new active fixture families here.
- Do not use legacy as a trash folder.

## Validation

Run `python scripts/validate_repo.py` after changing legacy maps.
