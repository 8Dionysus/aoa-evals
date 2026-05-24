# Proof Loop / Parts Route

`mechanics/proof-loop/parts/` is the lower index for proof-loop-owned
part artifacts. Use it after the parent Proof Loop route has selected a
part-level operation and the next agent needs the exact part, payload home,
owner route, and validation lane.

## Operating Card

| Field | Route |
| --- | --- |
| role | lower index for active proof-loop part artifacts |
| input | proof question, selected loop segment, support contract, candidate evidence packet, route-smoke scope, or bounded report pressure |
| output | part README route, bounded route-smoke report, defer note, owner handoff, or receipt-intake route |
| owner | proof-loop owns loop routeability; source proof, support contracts, candidate evidence, sibling refs, and receipts keep their step-owner authority |
| next route | `mechanics/proof-loop/PARTS.md`, selected part README, route-smoke report, step-owner mechanic, and parent validation lane |
| validation | `mechanics/proof-loop/parts/AGENTS.md#validation` and `mechanics/proof-loop/AGENTS.md#validation` |

## Active Parts

| Part | Operation | Start surface |
| --- | --- | --- |
| `route-smoke/` | public-safe route-smoke proof that one local loop path can reach a bounded report | `route-smoke/README.md` |

## Owner Pressure Routes

| Pressure | Route |
| --- | --- |
| source proof object meaning | `mechanics/proof-object/` plus affected `evals/**/EVAL.md` and `evals/**/eval.yaml` |
| support contract pressure | `mechanics/proof-infra/` |
| candidate evidence packet | `mechanics/audit/` |
| sibling reference or owner truth | `mechanics/boundary-bridge/` plus sibling owner route |
| receipt publication or receipt-intake pressure | `mechanics/publication-receipts/` |
| route-smoke reads as bundle promotion, runtime acceptance, sibling approval, or full proof-loop completeness | `route-smoke/README.md` stop-lines plus the relevant step-owner route |

## Part Admission Route

| Source signal | Operation test | Next route |
| --- | --- | --- |
| one local loop path needs public-safe routeability proof | bounded route-smoke report with no receipt publication | `route-smoke/README.md` |
| future shared proof-loop checklist or report family | distinct loop step, source surface, owner split, payload home, and validation lane | parent `PARTS.md` update plus decision review |
