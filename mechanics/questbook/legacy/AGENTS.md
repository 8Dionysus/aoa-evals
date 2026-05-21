# AGENTS.md

## Applies to

`mechanics/questbook/legacy/`.

## Role

This legacy bridge preserves old questbook path and placement lineage behind
the active questbook mechanic.

## Read before editing

1. root `AGENTS.md`
2. `mechanics/questbook/README.md`
3. `mechanics/questbook/PARTS.md`
4. `mechanics/questbook/PROVENANCE.md`
5. `mechanics/questbook/legacy/INDEX.md`

## Boundaries

- Do not start new quest work here.
- Do not use legacy path vocabulary as active source placement.
- Do not add raw files unless they preserve lineage that cannot stay in the
  active part or git history.
- Keep active routes first, then legacy lookup.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
