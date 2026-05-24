# Distillation / Runtime Candidate Adoption Part

## Role

This part owns support surfaces for reviewed runtime distillation candidate
adoption proof.

It keeps runtime writeback target mapping, reviewed adoption, live receipt
visibility, candidate posture, and object-facing recall inspectable while source
proof bundles stay under `evals/`.

## Source Surfaces

- `evals/workflow/aoa-memo-reviewed-candidate-adoption-integrity/EVAL.md`
- `mechanics/distillation/parts/runtime-candidate-adoption/fixtures/memo-reviewed-candidate-adoption-guardrail-v1/README.md`

## Related Ingress

- `docs/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md`

That root note explains why reviewed-candidate adoption became the next
stricter memo gap after the base writeback-act pilot. It remains ingress and
quest pressure, not an active source surface for this part and not a reason to
pull confirmed writeback-act proof into Distillation.

## Inputs

- `distillation_claim_candidate`, `distillation_pattern_candidate`, or
  `distillation_bridge_candidate` runtime mappings;
- reviewed adoption refs, adopted memo object refs, live receipt visibility,
  and object-facing recall surfaces;
- bundle-local fixture, runner, and report contracts.

## Outputs

- bounded reviewed-candidate adoption proof reading;
- fixture family route for reviewed runtime distillation candidate cases;
- report expectation for target mapping, review-to-adoption alignment, receipt
  visibility, candidate-posture honesty, and recall-surface alignment;
- owner handoff route when candidate adoption requires memo, runtime, KAG,
  Experience, or owner-local authority.

## Stronger Owner Split

`Agents-of-Abyss` owns Distillation law and candidate handoff posture.
`aoa-memo` owns memo object truth, durable memory review, writeback acceptance,
and memo recall implementation. `aoa-agents` owns runtime `distillation_pack`
artifact contracts. `abyss-stack` owns runtime storage, execution, and export
plumbing. `publication-receipts` owns receipt publication posture inside
`aoa-evals`. `experience/adoption-federation` owns generic adoption support.
`aoa-kag` owns KAG promotion and graph lift. Owner repositories own final
owner acceptance and owner-local adoption.

`aoa-evals` owns this part's bounded reviewed-candidate adoption proof wording,
fixture support, report expectations, and bundle-local interpretation for
`aoa-memo-reviewed-candidate-adoption-integrity`. Authority beyond those proof
readings routes through the stronger owner split above.

## Stop-Lines

Boundary routes keep runtime-candidate adoption pressure with the owner that can act on it:

| Pressure | Owner route |
| --- | --- |
| final promotion pressure | owner approval and durable memory review route |
| memory canon or memo object truth pressure | `aoa-memo` memory-object route |
| live memory-ledger behavior pressure | `aoa-memo` and `abyss-stack` runtime route |
| memo recall implementation pressure | `mechanics/recurrence/parts/memory-recall/` and `aoa-memo` route |
| runtime pack contract authority pressure | `aoa-agents` runtime artifact route |
| live receipt append behavior pressure | `publication-receipts` and runtime receipt route |
| Experience adoption federation pressure | `mechanics/experience/parts/adoption-federation/` |
| KAG lift or bridge-ready truth pressure | `aoa-kag` graph-lift route |
| owner-local adoption or final owner acceptance pressure | owner repository route |

Confirmed memo-surviving writeback acts stay with
`aoa-memo-writeback-act-integrity`; memo recall now routes through
`mechanics/recurrence/parts/memory-recall/`; contradiction guardrails stay with
their own bundle until a later evidence pass proves an active parent route.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
