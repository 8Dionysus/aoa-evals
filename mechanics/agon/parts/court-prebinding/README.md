# Agon / Court Prebinding Part

## Role

This part owns Agon court prebinding surfaces in `aoa-evals`.

It prepares local precheck candidates for closure legality, evidence floor,
assistant boundary, contradiction status, delta legitimacy, summon intent, and
trace integrity without opening an arena or granting court authority.

## Route

`court pressure -> prebinding seed -> generated prebinding registry -> precheck validation -> bundle-local review`

## Source Surfaces

- `mechanics/agon/parts/court-prebinding/docs/AGON_COURT_PREBINDING.md`
- `mechanics/agon/parts/court-prebinding/docs/AGON_EVAL_PREBINDING_MODEL.md`
- `mechanics/agon/parts/court-prebinding/config/agon_eval_prebindings.seed.json`
- `mechanics/agon/parts/court-prebinding/schemas/agon-eval-prebinding*.schema.json`
- `mechanics/agon/parts/court-prebinding/examples/agon_eval_prebinding.example.json`
- `mechanics/agon/parts/court-prebinding/generated/agon_eval_prebinding_registry.min.json`
- `mechanics/agon/parts/court-prebinding/manifests/recurrence/`

## Inputs

- seeded prebinding records and gate triggers;
- trial playbook refs and recurrence review inputs;
- must-not constraints, lawful moves, and allowed candidate outputs;
- part-local docs, schema, example, builder, validator, tests, and observe-only
  recurrence bindings.

## Outputs

- deterministic `agon_eval_prebinding_registry.min.json` output;
- precheck candidate records for later bundle-local review or owner handoff;
- observe-only recurrence component and hook bindings;
- validation failures when stop-lines, required fields, or generated output
  drift.

## Stronger Owner Split

`aoa-evals` owns prebinding shape, deterministic registry derivation,
candidate-only validation, and local proof-review boundaries.

Agents-of-Abyss owns Agon law, court meaning, closure authority, arena protocol,
and any future live verdict route.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| live verdict, closure, summon, scar, memory write, rank mutation, Tree of Sophia promotion, hidden scheduler action, or arena authority | route to Agents-of-Abyss or the stronger live owner; this part emits precheck candidates only |
| registry drift around `no_live_verdict`, `no_closure_grant`, `no_live_summon`, `no_durable_memory_write`, `no_rank_mutation`, or `no_tree_of_sophia_promotion` | fix the seed, builder, or validator while preserving the explicit stop-line token |
| generated prebinding output reads stronger than court evidence | route through bundle-local review or owner handoff before any accepted-proof claim |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
