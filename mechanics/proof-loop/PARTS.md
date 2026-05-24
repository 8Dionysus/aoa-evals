# Proof Loop / Part Index

`mechanics/proof-loop/parts/` contains the active parts of the local
proof-loop operation.

The mechanic owns the route:

`proof question -> selection route -> source proof object -> support contract -> candidate evidence packet -> bundle-local review -> bounded report -> optional receipt`

## Parts

| Part | Role | Active surfaces |
| --- | --- | --- |
| `route-smoke` | Maintains the first public-safe proof-loop route-smoke report. | `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md` |

## Boundary

Proof-loop parts are bounded part contracts inside the parent mechanic. The
`route-smoke` part proves that one local proof-loop route can be followed into
a bounded report artifact. Bundle promotion, receipt publication, runtime
evidence acceptance, sibling-owner approval, and proof-loop authority stay with
their owners. Its receipt result remains no eval result receipt.

## Part Contract

Inputs are one proof question, one source proof object, support contracts,
candidate-evidence posture, and the selected local route-smoke scope.

Outputs are bounded route-smoke reports and deferred/handoff notes. Proof
promotion routes to bundle-local review and the owning promotion surfaces.

Owner split stays explicit: proof-loop coordinates proof-object, proof-infra,
audit, boundary-bridge, and publication-receipts while their meaning stays with
those owners.

Stop-lines route bundle promotion, receipt publication, runtime acceptance,
sibling approval, and coordinator-strength pressure back to the step owners.

Validation routes through [AGENTS](AGENTS.md#validation).
