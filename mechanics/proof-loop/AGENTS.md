# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/proof-loop/DIRECTION.md` for current operating direction, `mechanics/proof-loop/PARTS.md` for active parts, and `mechanics/proof-loop/PROVENANCE.md` only when legacy or former placement matters.

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
8. `mechanics/proof-loop/PARTS.md`
9. `mechanics/proof-loop/parts/README.md`
10. `mechanics/proof-object/README.md`
11. `mechanics/proof-infra/README.md`
12. `mechanics/audit/README.md`
13. `mechanics/publication-receipts/README.md`
14. `mechanics/boundary-bridge/README.md`
15. `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json` when the loop
    reaches receipt-intake dry review
16. `docs/decisions/0019-proof-loop-mechanic-package.md`
17. `docs/decisions/0030-proof-loop-route-smoke-part.md`

## Boundaries

- Keep bundle-local `EVAL.md` and `eval.yaml` stronger than the loop route.
- Keep generated readers subordinate to source bundles.
- Keep candidate evidence below bundle-local review.
- Keep receipts below reviewed reports.
- Keep receipt-intake dry reviews below actual receipt publication.
- Keep sibling refs below sibling owner truth.
- Keep route-smoke reports in their proof-loop part, not root `reports/`.
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
