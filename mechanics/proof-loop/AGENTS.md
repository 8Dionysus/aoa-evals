# AGENTS.md

## Entry Route

When package semantics or direction are relevant, consult the package README and then the `mechanics/proof-loop/DIRECTION.md`, `mechanics/proof-loop/PARTS.md`, and `mechanics/proof-loop/PROVENANCE.md` routes as needed for the touched source.

## Applies to

`mechanics/proof-loop/` and the active proof-loop route.

## Role

This package routes one local proof loop:

`proof question -> selection route -> source proof object -> support contract -> candidate evidence packet -> bundle-local review -> bounded report -> optional receipt`

It coordinates existing mechanics. Source truth stays with the step owner for
the current loop segment.

## Operating Card

| Field | Route |
| --- | --- |
| role | active proof-loop route across existing proof mechanics |
| input | proof question, selection route, source proof object, support contract, candidate evidence packet, bundle-local review, bounded report, or optional receipt |
| output | next loop step, stronger-owner handoff, bounded report, defer, quest, or receipt-intake route |
| owner | proof-loop owns loop order; each step owner owns its source truth |
| next route | `mechanics/proof-loop/README.md`, `DIRECTION.md`, `PARTS.md`, step-owner mechanics, and bundle-local source surfaces |
| tools | root validator, semantic AGENTS validator, generated-surface builders when loop inputs move |
| validation | this card's `Validation` section |

current operating direction `mechanics/proof-loop/DIRECTION.md`; active-to-archive bridge `mechanics/proof-loop/PROVENANCE.md`.

## Owner Routes

| Loop pressure | Owner route |
| --- | --- |
| source proof object | `mechanics/proof-object/` plus affected `evals/**/EVAL.md` and `evals/**/eval.yaml` |
| support contract | `mechanics/proof-infra/` |
| candidate evidence packet | `mechanics/audit/` |
| optional receipt | `mechanics/publication-receipts/` |
| sibling reference | `mechanics/boundary-bridge/` and the sibling owner route |
| legacy or former route | `mechanics/proof-loop/PROVENANCE.md` |

## Route Rules

- Keep bundle-local `EVAL.md` and `eval.yaml` stronger than the loop route.
- Keep generated readers subordinate to source bundles.
- Keep candidate evidence below bundle-local review.
- Keep receipts below reviewed reports.
- Keep receipt-intake dry reviews below actual receipt publication.
- Keep sibling refs below sibling owner truth.
- Keep route-smoke reports inside their proof-loop part rather than root
  `reports/`.
- Route runtime dispatch, hidden scheduling, global scoring, and proof
  acceptance to stronger owners before adoption.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

Use the proof-loop checks in [VALIDATION.md](VALIDATION.md).

Add owning generated-surface checks when generated readers or candidate intake
surfaces change.

## Closeout

Report which loop step changed, which stronger owner route still owns the
source meaning, what validation ran, and whether the loop ended in a bounded
report, defer, receipt, quest, or owner handoff.
