# AGENTS.md

## Applies to

`mechanics/titan/legacy/`.

## Role

Legacy preserves former Titan `evals/` and canary-parent placement evidence
behind the active `mechanics/titan/` package.

## Operating Card

| Field | Route |
| --- | --- |
| role | Provenance and lineage route for former Titan eval, seed-boundary, and canary-parent placement. |
| input | Old Titan eval path, canary-parent path, seed-boundary residue, raw provenance question, or accepted historical vocabulary. |
| output | Active Titan parent or part route plus any needed `PROVENANCE.md`, `legacy/INDEX.md`, `legacy/DISTILLATION_LOG.md`, or raw accounting update. |
| owner | `mechanics/titan/` owns bounded Titan seed-boundary proof in `aoa-evals`; stronger Titan incarnation meaning routes to its stronger owner outside this repository. |
| next route | `../AGENTS.md`, `../README.md`, `../DIRECTION.md`, `../PARTS.md`, `../PROVENANCE.md`, then `INDEX.md` and `DISTILLATION_LOG.md` for archive detail. |
| tools | Root validators, semantic-agent validator, and Titan canary regression listed below. |
| validation | Run the Validation commands after route-card, provenance, index, log, or raw changes. |

## Read before editing

1. repository root `AGENTS.md`
2. `mechanics/README.md`
3. `mechanics/EVIDENCE_CLUSTERS.md`
4. `mechanics/titan/README.md`
5. `mechanics/titan/PARTS.md`
6. `mechanics/titan/PROVENANCE.md`
7. `mechanics/titan/legacy/INDEX.md`
8. `mechanics/titan/legacy/DISTILLATION_LOG.md`

## Route Rules

- Start from active Titan seed-boundary surfaces before using legacy.
- Treat `mechanics/titan-canaries/` as historical vocabulary that maps back to
  active Titan topology.
- Place current canary YAML files and Titan seed-boundary proof in the active
  parent or owning part.
- Limit legacy path compatibility to historical and accepted-input evidence;
  full Titan incarnation meaning routes to its stronger owner outside
  `aoa-evals`.

## Validation

Run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
python -m pytest -q tests/test_mechanic_surface_contracts.py -k titan
```

## Closeout

Report which former path was mapped, which active Titan seed route owns it, and
which stronger Titan owner boundary stayed outside `aoa-evals`.
