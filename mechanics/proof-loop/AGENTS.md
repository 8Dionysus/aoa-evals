# AGENTS.md

## Applies to

`mechanics/proof-loop/` and the active proof-loop route.

## Role

This package routes one local proof loop:

`proof question -> selection route -> source proof object -> support contract -> candidate evidence packet -> bundle-local review -> bounded report -> optional receipt`

It coordinates existing mechanics. It does not own their source truth.

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `ROADMAP.md`
5. `docs/PROOF_TOPOLOGY.md`
6. `mechanics/README.md`
7. `mechanics/proof-loop/README.md`
8. `mechanics/proof-object/README.md`
9. `mechanics/proof-infra/README.md`
10. `mechanics/runtime-evidence/README.md`
11. `mechanics/publication-receipts/README.md`
12. `mechanics/sibling-proof-refs/README.md`
13. `reports/eval-result-receipt-intake-dry-review-v1.json` when the loop
    reaches receipt-intake dry review
14. `docs/decisions/0019-proof-loop-mechanic-package.md`

## Boundaries

- Keep bundle-local `EVAL.md` and `eval.yaml` stronger than the loop route.
- Keep generated readers subordinate to source bundles.
- Keep candidate evidence below bundle-local review.
- Keep receipts below reviewed reports.
- Keep receipt-intake dry reviews below actual receipt publication.
- Keep sibling refs below sibling owner truth.
- Do not treat this package as runtime dispatch, hidden scheduling, global
  scoring, or proof acceptance.

## Validation

Run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

Add owning generated-surface checks when generated readers or candidate intake
surfaces change.

## Closeout

Report which loop step changed, which stronger owner route still owns the
source meaning, what validation ran, and whether the loop ended in a bounded
report, defer, receipt, quest, or owner handoff.
