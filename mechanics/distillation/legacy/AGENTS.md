# AGENTS.md

## Applies to

`mechanics/distillation/legacy/`.

## Role

This district preserves Distillation placement provenance after active routes
exist.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former distillation placement and source-bundle pressure. |
| input | Old distillation path, raw source-bundle placement, adjacent fixture path, or historical lookup question. |
| output | Active distillation parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/distillation/` owns current distillation proof work; this legacy district owns archive-local lookup and lineage accounting. |
| next route | `../AGENTS.md`, `../README.md`, `../DIRECTION.md`, `../PARTS.md`, `../PROVENANCE.md`, then `INDEX.md` and `DISTILLATION_LOG.md` for archive detail. |
| tools | Root validators and semantic-agent validator listed below. |
| validation | Run the Validation commands after route-card, provenance, index, log, or raw changes. |

## Read before editing

1. repository root `AGENTS.md`
2. `mechanics/AGENTS.md`
3. `../AGENTS.md`
4. `../README.md`
5. `../DIRECTION.md`
6. `../PARTS.md`
7. `../PROVENANCE.md`
8. `docs/architecture/LEGACY_NAMING.md`
9. `INDEX.md`
10. `DISTILLATION_LOG.md`

## Route Rules

- Start from active distillation parts before using legacy.
- Place current distillation proof work in the active parent or owning part.
- Treat moved root and adjacent fixture paths as historical input that maps
  back to active topology.
- Keep source proof bundles under `evals/`.

## Validation

After changing legacy maps, run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which old placement was mapped, which active part now owns the route,
and whether any raw source bundle or public compatibility path remains.
