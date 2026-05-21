# Runtime Candidate Adoption Part

## Role

This part owns support surfaces for reviewed runtime distillation candidate
adoption proof.

It keeps runtime writeback target mapping, reviewed adoption, live receipt
visibility, candidate posture, and object-facing recall inspectable while source
proof bundles stay under `bundles/`.

## Source Surfaces

- `bundles/aoa-memo-reviewed-candidate-adoption-integrity/EVAL.md`
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

`aoa-evals` owns only bounded reviewed-candidate adoption proof wording,
fixture support, report expectations, and bundle-local interpretation for
`aoa-memo-reviewed-candidate-adoption-integrity`.

## Stop-Lines

This part must not claim:

- final promotion;
- memory canon or memo object truth;
- generic live memory-ledger behavior;
- memo recall implementation;
- runtime pack contract authority;
- live receipt append behavior;
- Experience adoption federation;
- KAG lift or bridge-ready truth;
- owner-local adoption or final owner acceptance.

Confirmed memo-surviving writeback acts stay with
`aoa-memo-writeback-act-integrity`; memo recall now routes through
`mechanics/recurrence/parts/memory-recall/`; contradiction guardrails stay with
their own bundle until a later evidence pass proves an active parent route.

## Validation

```bash
python scripts/validate_repo.py --eval aoa-memo-reviewed-candidate-adoption-integrity
python scripts/build_catalog.py --check
```
