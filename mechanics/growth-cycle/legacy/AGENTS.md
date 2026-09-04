# AGENTS.md

## Applies to

`mechanics/growth-cycle/legacy/`.

## Role

This district preserves Growth Cycle provenance behind the active
`mechanics/growth-cycle/` package.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former Growth Cycle closeout, harvest, repair, progression, and quest pressure. |
| input | Old Growth Cycle path, deferred closeout note, harvest or repair note, progression residue, quest pressure, or historical lookup question. |
| output | Active Growth Cycle parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/growth-cycle/` owns current Growth Cycle proof work; this legacy district owns archive-local lookup and lineage accounting. |
| next route | `../AGENTS.md`, `../README.md`, `../DIRECTION.md`, `../PARTS.md`, `../PROVENANCE.md`, then `INDEX.md` and `DISTILLATION_LOG.md` for archive detail. |
| tools | Root validators and semantic-agent validator listed below. |
| validation | Run the Validation commands after route-card, provenance, index, log, or raw changes. |

## Route Rules

- When historical placement or package context is material, consult
  `../README.md`, `../PARTS.md`, and `../PROVENANCE.md` before the legacy
  accounting files.
- Place current Growth Cycle work in the active parent or owning part.
- Treat deferred closeout, harvest, repair, progression, and quest pressure as
  historical input that maps back to active topology.
- Move raw files here with a matching `../PROVENANCE.md` bridge, index row,
  distillation accounting, and validation.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

After editing, follow the root validation route in [VALIDATION.md](VALIDATION.md).

## Closeout

Report which Growth Cycle legacy source was mapped, which active parent or part
owns the current route, which archive accounting changed, and which checks ran.
