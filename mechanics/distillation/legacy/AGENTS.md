# AGENTS.md

## Applies to

`mechanics/distillation/legacy/`.

## Role

This district preserves Distillation placement provenance after active routes
exist.

## Boundaries

- Do not add new proof work here.
- Do not treat legacy placement as the active route.
- Do not recreate moved root or adjacent fixture paths.
- Keep source proof bundles under `bundles/`.

## Validation

After changing legacy maps, run:

```bash
python scripts/validate_repo.py
```

## Closeout

Report which old placement was mapped, which active part now owns the route,
and whether any raw source bundle or public compatibility path remains.
