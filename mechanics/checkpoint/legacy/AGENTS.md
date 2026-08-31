# AGENTS.md

## Applies to

`mechanics/checkpoint/legacy/`

## Role

This legacy district preserves checkpoint provenance behind the active
checkpoint mechanic.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former checkpoint placement and checkpoint-proof vocabulary. |
| input | Old checkpoint path, raw checkpoint note, migration residue, or historical lookup question. |
| output | Active checkpoint parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/checkpoint/` owns current checkpoint proof work; this legacy district owns archive-local lookup and lineage accounting. |
| next route | `../AGENTS.md`, `../README.md`, `../DIRECTION.md`, `../PARTS.md`, `../PROVENANCE.md`, then `INDEX.md` and `DISTILLATION_LOG.md` for archive detail. |
| tools | Root validators and semantic-agent validator listed below. |
| validation | Run the Validation commands after route-card, provenance, index, log, or raw changes. |

## Read before editing
Read only the route needed for the touched source: consult the nearest README when its human or semantic contract is required, then follow the source-owner and validation routes conditionally.
## Route Rules

- Start from active checkpoint surfaces before using legacy.
- Keep route changes in `mechanics/checkpoint/README.md`,
  `mechanics/checkpoint/DIRECTION.md`, `mechanics/checkpoint/PARTS.md`, and
  the relevant part.
- Add raw or historical material only when it has an active route in
  `legacy/INDEX.md` and distillation accounting.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

## Closeout

Report which checkpoint legacy source was mapped, which active parent or part
owns the current route, which archive accounting changed, and which checks ran.
