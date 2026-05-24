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

`aoa-evals` owns this part's bounded adoption and compatibility proof readings,
schema/example contracts, and bundle-local interpretation. Authority beyond
those proof readings routes through the stronger owner split above.

Reviewed runtime distillation candidate adoption routes through
`mechanics/distillation/parts/runtime-candidate-adoption/`; this part keeps
adoption-federation proof support.

## Stop-Lines

Boundary routes keep adoption-federation pressure with the owner that can act on it:

| Pressure | Owner route |
| --- | --- |
| owner-local adoption pressure | owner repository adoption route |
| owner consent pressure | owner repository consent route |
| KAG adoption pressure | `aoa-kag` substrate route plus owner consent |
| Tree-of-Sophia meaning or write pressure | Tree-of-Sophia authored-meaning route |
| memory canon or memo adoption pressure | `aoa-memo` memory route |
| routing authorship pressure | `aoa-routing` route-authority lane |
| automatic activation pressure | owner activation and runtime route |
| runtime distillation candidate adoption pressure | `mechanics/distillation/parts/runtime-candidate-adoption/` |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
