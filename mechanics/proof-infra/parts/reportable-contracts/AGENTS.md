# AGENTS.md

## Applies to

`mechanics/proof-infra/parts/reportable-contracts/`.

## Role

This part owns reportable proof contract support: the shared runner surface,
shared bounded scorer helper, and shared schemas that each bundle-local runner
contract cites.

It does not own bundle-local meaning, report verdict interpretation, comparison
semantics, candidate evidence acceptance, publication receipts, or sibling
truth.

## Read before editing

1. repository root `AGENTS.md`
2. `DESIGN.md`
3. `docs/PROOF_TOPOLOGY.md`
4. `mechanics/EVIDENCE_CLUSTERS.md`
5. `mechanics/proof-infra/README.md`
6. `mechanics/proof-infra/PARTS.md`
7. `mechanics/proof-infra/parts/reportable-contracts/README.md`
8. affected `bundles/*/EVAL.md`
9. affected `bundles/*/runners/contract.json`
10. affected `bundles/*/reports/summary.schema.json`

## Boundaries

- Keep the shared runner surface weaker than bundle-local interpretation.
- Keep `runner_surface_path` and `scorer_helper_paths` explicit and current.
- Keep schema weakening visible as a proof-contract risk.
- Do not add hidden harness logic or private evidence here.
- Do not recreate active root aliases under `runners/`, `scorers/`, or
  `schemas/`.

## Validation

Run:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
python -m pytest -q mechanics/proof-infra/parts/reportable-contracts/tests/test_bounded_rubric_breakdown.py
```

Run broader catalog and validation tests when bundle-local runner contracts or
generated `proof_artifacts` change.

## Closeout

Report which reportable contract surface changed, which bundle-local contracts
consume it, whether generated `proof_artifacts` were rebuilt, and which
bundle-local interpretation boundary stayed stronger.
