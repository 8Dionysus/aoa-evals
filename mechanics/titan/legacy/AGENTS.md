# AGENTS.md

## Applies to

`mechanics/titan/legacy/`.

## Role

Legacy preserves former Titan `evals/` and canary-parent placement evidence
behind the active `mechanics/titan/` package.

## Read before editing

1. repository root `AGENTS.md`
2. `mechanics/README.md`
3. `mechanics/EVIDENCE_CLUSTERS.md`
4. `mechanics/titan/README.md`
5. `mechanics/titan/PARTS.md`
6. `mechanics/titan/PROVENANCE.md`
7. `mechanics/titan/legacy/INDEX.md`
8. `mechanics/titan/legacy/DISTILLATION_LOG.md`

## Boundaries

- Start from active Titan seed-boundary surfaces before using legacy.
- Do not recreate `mechanics/titan-canaries/` as active topology.
- Do not put new canary YAML files in legacy.
- Do not treat legacy path compatibility as full incarnation proof.

## Validation

Run:

```bash
python scripts/validate_repo.py
python -m pytest -q tests/test_validate_repo.py -k titan_canary
```

## Closeout

Report which former path was mapped, which active Titan seed route owns it, and
which stronger Titan owner boundary stayed outside `aoa-evals`.
