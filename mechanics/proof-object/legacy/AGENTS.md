# AGENTS.md

## Applies to

`mechanics/proof-object/legacy/`.

## Role

This legacy bridge preserves old proof-object template and schema placement
behind the active proof-object mechanic.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former proof-object template, schema, and bundle-authoring placement. |
| input | Old proof-object path, template alias, eval schema alias, bundle-authoring residue, or historical lookup question. |
| output | Active proof-object parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/proof-object/` owns current proof-object support; bundle-local `EVAL.md` and `eval.yaml` own source proof meaning; this legacy district owns archive-local lookup and lineage accounting. |
| next route | `../AGENTS.md`, `../README.md`, `../DIRECTION.md`, `../PARTS.md`, `../PROVENANCE.md`, then `INDEX.md` and `DISTILLATION_LOG.md` for archive detail. |
| tools | Root validators and semantic-agent validator listed below. |
| validation | Run the Validation commands after route-card, provenance, index, log, or raw changes. |

## Read before editing

1. root `AGENTS.md`
2. `mechanics/AGENTS.md`
3. `mechanics/proof-object/AGENTS.md`
4. `mechanics/proof-object/README.md`
5. `mechanics/proof-object/DIRECTION.md`
6. `mechanics/proof-object/PARTS.md`
7. `mechanics/proof-object/PROVENANCE.md`
8. `docs/LEGACY_NAMING.md`
9. `mechanics/proof-object/legacy/INDEX.md`

## Route Rules

- Start from active proof-object parts before using legacy.
- Place current bundle-authoring support, templates, and schema aliases in the
  active parent, owning part, or bundle-local source surface.
- Treat legacy path vocabulary as historical input that maps back to active
  topology.
- Keep source bundle meaning in `evals/**/EVAL.md` and `eval.yaml`.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which proof-object legacy source was mapped, which active parent, part,
or bundle-local source owns the current route, which archive accounting
changed, and which checks ran.
