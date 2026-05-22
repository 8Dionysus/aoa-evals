# AGENTS.md

## Applies to

`mechanics/audit/legacy/` provenance and lineage files.

## Role

This directory preserves old audit/runtime-evidence placement and naming
history behind the active `audit` mechanic.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former audit, runtime-evidence, packet, and generated-reader placement. |
| input | Old audit path, runtime-evidence name, raw packet, generated-reader residue, or historical lookup question. |
| output | Active audit parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/audit/` owns current audit packet, candidate-reader, and runtime-evidence routes; this legacy district owns archive-local lookup and lineage accounting. |
| next route | `../AGENTS.md`, `../README.md`, `../DIRECTION.md`, `../PARTS.md`, `../PROVENANCE.md`, then `INDEX.md` and `DISTILLATION_LOG.md` for archive detail. |
| tools | Root validators and semantic-agent validator listed below. |
| validation | Run the Validation commands after route-card, provenance, index, log, or raw changes. |

## Read before editing

1. root `AGENTS.md`
2. `mechanics/audit/AGENTS.md`
3. `mechanics/audit/README.md`
4. `mechanics/audit/PARTS.md`
5. `mechanics/audit/PROVENANCE.md`
6. `docs/LEGACY_NAMING.md`

## Route Rules

- Start from active audit parts before reading legacy.
- Keep `runtime-evidence` as evidence-class vocabulary that routes through
  active audit parts.
- Place current schemas, examples, generated readers, and candidate packets in
  the active audit parent or owning part.
- Preserve old root paths as historical input that maps back to active
  topology.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which audit or runtime-evidence legacy source was mapped, which active
part owns the current route, which archive accounting changed, and which checks
ran.
