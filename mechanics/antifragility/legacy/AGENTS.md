# AGENTS.md

## Applies to

`mechanics/antifragility/legacy/`.

## Role

This district preserves Antifragility provenance behind the active
`mechanics/antifragility/` package.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former Antifragility proof-support placement. |
| input | Old Antifragility path, raw packet, migration residue, or historical lookup question. |
| output | Active Antifragility parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/antifragility/` owns current Antifragility proof work; this legacy district owns archive-local lookup and lineage accounting. |
| next route | `../AGENTS.md`, `../README.md`, `../DIRECTION.md`, `../PARTS.md`, `../PROVENANCE.md`, then `INDEX.md` and `DISTILLATION_LOG.md` for archive detail. |
| tools | Root validators and semantic-agent validator listed below. |
| validation | Run the Validation commands after route-card, provenance, index, log, or raw changes. |

## Read before editing

1. repository root `AGENTS.md`
2. `mechanics/AGENTS.md`
3. `mechanics/antifragility/AGENTS.md`
4. `mechanics/antifragility/README.md`
5. `mechanics/antifragility/DIRECTION.md`
6. `mechanics/antifragility/PARTS.md`
7. `mechanics/antifragility/PROVENANCE.md`
8. `docs/LEGACY_NAMING.md`

## Route Rules

- Start from active Antifragility surfaces before using legacy.
- Place current Antifragility proof work in the active parent or owning part.
- Treat old paths as historical input that maps back to active topology.
- Add raw or historical material with an active route, an index row, and
  distillation accounting.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which legacy source was mapped, which active parent or part owns the
current route, which archive accounting changed, and which checks ran.
