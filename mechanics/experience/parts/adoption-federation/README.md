# Experience / Adoption Federation Part

## Role

This part owns the support route for Experience adoption proof.

It keeps adoption, consent, shadow, agonic adoption, compatibility,
federation-harvest, KAG/ToS boundary, and owner adoption support together
while source proof bundles stay under `evals/`.

## Source Surfaces

- `mechanics/experience/parts/adoption-federation/docs/`
- `mechanics/experience/parts/adoption-federation/examples/`
- `mechanics/experience/parts/adoption-federation/schemas/`
- `mechanics/experience/parts/adoption-federation/tests/test_experience_wave3_seed_contracts.py`

## Inputs

- adoption requests;
- owner consent refs;
- compatibility and shadow proof;
- KAG and ToS boundary refs;
- federation harvest, lineage, and regression verdict packets.

## Outputs

- bounded adoption proof readings;
- schema/example contracts for adoption and compatibility verdicts;
- one reviewed-candidate adoption fixture family contract;
- owner handoff route when adoption evidence requires consent, routing, KAG,
  ToS, memo, or runtime authority.

## Stronger Owner Split

`Agents-of-Abyss` owns Experience adoption route language and federation
boundaries. Owner repositories own owner consent, owner-local adoption, and
activation. `aoa-routing` owns routing behavior. `aoa-kag` owns KAG substrate
meaning and promotion mechanics. `Tree-of-Sophia` owns authored meaning and
canon. `aoa-memo` owns memory objects and memo adoption truth.

`aoa-evals` owns only bounded adoption and compatibility proof readings,
schema/example contracts, and bundle-local interpretation.

Reviewed runtime distillation candidate adoption is not this part's active
fixture family anymore; it routes through
`mechanics/distillation/parts/runtime-candidate-adoption/`.

## Stop-Lines

This part must not claim:

- owner-local adoption;
- owner consent;
- KAG forced adoption;
- direct ToS runtime write or Tree-of-Sophia meaning;
- memory canon or memo adoption truth;
- routing authorship;
- automatic activation;
- reviewed runtime distillation candidate adoption.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
