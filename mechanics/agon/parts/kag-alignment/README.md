# Agon / KAG Alignment Part

## Role

This part owns KAG promotion-path alignment surfaces while preventing KAG
candidate checks from becoming canon, source truth, or automatic promotion.

It keeps KAG promotion pressure visible as candidate-only eval alignment.

## Route

`KAG promotion pressure -> alignment seed -> generated registry -> no-canon validation`

## Source Surfaces

- `mechanics/agon/parts/kag-alignment/docs/AGON_KAG_EVAL_ALIGNMENT.md`
- `mechanics/agon/parts/kag-alignment/docs/AGON_KAG_EVAL_BOUNDARY.md`
- `mechanics/agon/parts/kag-alignment/config/agon_kag_eval_alignment.seed.json`
- `mechanics/agon/parts/kag-alignment/schemas/agon-kag-eval-alignment*.schema.json`
- `mechanics/agon/parts/kag-alignment/examples/agon_kag_eval_alignment.example.json`
- `mechanics/agon/parts/kag-alignment/generated/agon_kag_eval_alignment_registry.min.json`
- `mechanics/agon/parts/kag-alignment/manifests/recurrence/`

## Inputs

- KAG promotion, retention, owner-truth, pattern-legitimacy, demotion, and ToS
  boundary alignment records;
- candidate-only status, runtime-effect fields, forbidden effects, and required
  stop-lines;
- part-local docs, schema, example, builder, validator, tests, and observe-only
  recurrence bindings.

## Outputs

- deterministic `agon_kag_eval_alignment_registry.min.json` output;
- candidate-only KAG promotion-path checks;
- observe-only recurrence component and hook metadata when present;
- validation failures when a record implies KAG canon, source-truth transfer,
  retention execution, rank mutation, or Tree of Sophia promotion.

## Stronger Owner Split

`aoa-evals` owns local KAG promotion-path alignment and generated candidate
navigation.

`aoa-kag`, Agents-of-Abyss, Tree of Sophia, stats, memo, and runtime owners keep
KAG canon, source truth, retention execution, rank truth, and promotion
authority.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| KAG candidate promotion, KAG canon, rank or trust mutation, retention execution, or Tree of Sophia promotion pressure | route to `aoa-kag`, rank/retention, or ToS owners; this part stays candidate-only alignment |
| live verdict, scar, memory write, hidden scheduler action, or owner acceptance pressure | route to the stronger live owner before any durable effect exists |
| generated KAG alignment records are needed as proof | route through owner review or bundle-local review before proof use |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
