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

## Route Rules

- Start from active distillation parts before using legacy.
- Place current distillation proof work in the active parent or owning part.
- Treat moved root and adjacent fixture paths as historical input that maps
  back to active topology.
- Keep source proof bundles under `evals/`.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

After changing legacy maps, run:

## Closeout

Report which old placement was mapped, which active part now owns the route,
and whether any raw source bundle or public compatibility path remains.
