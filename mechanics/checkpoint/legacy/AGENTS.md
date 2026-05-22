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

1. repository root `AGENTS.md`
2. `mechanics/AGENTS.md`
3. `../AGENTS.md`
4. `../README.md`
5. `../DIRECTION.md`
6. `../PARTS.md`
7. `../PROVENANCE.md`
8. `docs/LEGACY_NAMING.md`
9. `INDEX.md`
10. `DISTILLATION_LOG.md`

## Route Rules

- Start from active checkpoint surfaces before using legacy.
- Keep route changes in `mechanics/checkpoint/README.md`,
  `mechanics/checkpoint/DIRECTION.md`, `mechanics/checkpoint/PARTS.md`, and
  the relevant part.
- Add raw or historical material only when it has an active route in
  `legacy/INDEX.md` and distillation accounting.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which checkpoint legacy source was mapped, which active parent or part
owns the current route, which archive accounting changed, and which checks ran.
