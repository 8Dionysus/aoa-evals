# Proof Loop Parts

`mechanics/proof-loop/parts/` contains the active parts of the local
proof-loop operation.

The mechanic owns the route:

`proof question -> selection route -> source proof object -> support contract -> candidate evidence packet -> bundle-local review -> bounded report -> optional receipt`

## Parts

| Part | Role | Active surfaces |
| --- | --- | --- |
| `route-smoke` | Maintains the first public-safe proof-loop route-smoke report. | `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md` |

## Boundary

Parts are not standalone mechanics. The `route-smoke` part proves only that one
local proof-loop route can be followed into a bounded report artifact. It does
not promote a bundle, publish a receipt, accept runtime evidence, approve
sibling truth, or make `mechanics/proof-loop/` stronger than the packages it
coordinates. Its receipt result remains no eval result receipt.

## Part Contract

Inputs are one proof question, one source proof object, support contracts,
candidate-evidence posture, and the selected local route-smoke scope.

Outputs are bounded route-smoke reports and deferred/handoff notes, not proof
promotion.

Owner split stays explicit: proof-loop coordinates proof-object, proof-infra,
audit, boundary-bridge, and publication-receipts without owning their meaning.

Stop-lines forbid bundle promotion, receipt publication, runtime acceptance,
sibling approval, or making the coordinator stronger than step owners.

Validation is `python scripts/validate_repo.py`.
