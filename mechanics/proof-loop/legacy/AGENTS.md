# AGENTS.md

## Applies to

`mechanics/proof-loop/legacy/` provenance and lineage files.

## Role

This directory preserves old proof-loop root report placement behind the active
`proof-loop` mechanic.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former proof-loop report, route-smoke, generated-reader, and receipt placement. |
| input | Old proof-loop report path, route-smoke residue, generated-reader residue, receipt path, or historical lookup question. |
| output | Active proof-loop parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/proof-loop/` owns current proof-loop reports and loops; this legacy district owns archive-local lookup and lineage accounting. |
| next route | `../AGENTS.md`, `../README.md`, `../DIRECTION.md`, `../PARTS.md`, `../PROVENANCE.md`, then `INDEX.md` and `DISTILLATION_LOG.md` for archive detail. |
| tools | Root validators and semantic-agent validator listed below. |
| validation | Run the Validation commands after route-card, provenance, index, log, or raw changes. |

## Read before editing

1. root `AGENTS.md`
2. `mechanics/proof-loop/AGENTS.md`
3. `mechanics/proof-loop/README.md`
4. `mechanics/proof-loop/PARTS.md`
5. `mechanics/proof-loop/PROVENANCE.md`
6. `docs/architecture/LEGACY_NAMING.md`

## Route Rules

- Start from active proof-loop parts before reading legacy.
- Keep old `reports/` paths as lookup lineage that maps back to active report
  placement.
- Place current proof-loop reports, route-smoke artifacts, generated readers,
  and receipts in the active parent or owning part.
- Preserve former root report paths as historical input.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which proof-loop legacy source was mapped, which active part owns the
current route, which archive accounting changed, and which checks ran.
