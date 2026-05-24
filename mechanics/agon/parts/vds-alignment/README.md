# Agon / VDS Alignment Part

## Role

This part owns verdict draft status alignment and verdict-draft check surfaces.

It keeps draft verdict pressure inspectable while forbidding live verdict
authority inside `aoa-evals`.

## Route

`verdict draft pressure -> VDS alignment seed -> generated alignment registry -> no-live-verdict validation`

## Source Surfaces

- `mechanics/agon/parts/vds-alignment/docs/AGON_VDS_EVAL_ALIGNMENT.md`
- `mechanics/agon/parts/vds-alignment/docs/AGON_VERDICT_DRAFT_CHECKS.md`
- `mechanics/agon/parts/vds-alignment/config/agon_vds_eval_alignment.seed.json`
- `mechanics/agon/parts/vds-alignment/schemas/agon-vds-eval-alignment*.schema.json`
- `mechanics/agon/parts/vds-alignment/examples/agon_vds_eval_alignment.example.json`
- `mechanics/agon/parts/vds-alignment/generated/agon_vds_eval_alignment_registry.min.json`
- `mechanics/agon/parts/vds-alignment/manifests/`

## Inputs

- verdict draft status refs and candidate check definitions;
- seeded alignment records with `must_not_emit`, `may_emit`, and stop-line
  constraints;
- part-local docs, schema, example, builder, validator, and tests.

## Outputs

- deterministic `agon_vds_eval_alignment_registry.min.json` output;
- candidate-only verdict draft status checks;
- validation failures when a draft check implies live verdict authority or
  weakens emission constraints.

## Stronger Owner Split

`aoa-evals` owns draft-status alignment shape and no-live-verdict validation.

Agents-of-Abyss owns Agon verdict meaning, court posture, closure semantics, and
any future live verdict bridge.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| live verdict emission or acceptance pressure | keep this part on the no-live-verdict path and route verdict authority to Agents-of-Abyss |
| verdict draft status pressure asks for closure, arena action, rank mutation, scar write, memory write, or Tree of Sophia promotion | route to the stronger live owner; local output remains verdict-draft alignment |
| generated draft-status records conflict with `must_not_emit`, `may_emit`, the seed, validator, or bundle-local review | route back to the source seed and validator before treating the record as usable |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
