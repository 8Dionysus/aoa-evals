# Sophian Threshold Alignment

## Role

This part owns Sophian threshold alignment surfaces while forbidding direct
Tree of Sophia writes, automatic canonization, and canon-authority transfer.

It lets `aoa-evals` test threshold posture without becoming the threshold owner.

## Route

`Sophian threshold pressure -> alignment seed -> generated registry -> no-canon-write validation`

## Source Surfaces

- `mechanics/agon/parts/sophian-threshold-alignment/docs/AGON_SOPHIAN_EVAL_ALIGNMENT.md`
- `mechanics/agon/parts/sophian-threshold-alignment/config/agon_sophian_eval_alignment.seed.json`
- `mechanics/agon/parts/sophian-threshold-alignment/schemas/agon-sophian-eval-alignment*.schema.json`
- `mechanics/agon/parts/sophian-threshold-alignment/examples/agon_sophian_eval_alignment_registry.example.json`
- `mechanics/agon/parts/sophian-threshold-alignment/generated/agon_sophian_eval_alignment_registry.min.json`
- `mechanics/agon/parts/sophian-threshold-alignment/manifests/`

## Inputs

- Sophian threshold alignment records and owner-boundary refs;
- forbidden effects, no-canon-write posture, and candidate-only status;
- part-local doc, schema, example, builder, validator, and tests.

## Outputs

- deterministic `agon_sophian_eval_alignment_registry.min.json` output;
- candidate-only Sophian threshold checks;
- validation failures when threshold pressure implies Tree of Sophia canon
  write, direct promotion, or canon-authority transfer.

## Stronger Owner Split

`aoa-evals` owns local threshold alignment and no-canon-write validation.

Tree of Sophia owns authored meaning and canon. Agents-of-Abyss owns Agon law
and federation posture. Any future threshold owner keeps promotion authority.

## Stop-Lines

- Do not write Tree of Sophia canon or directly promote a candidate.
- Do not transfer canon authority, decide authored meaning, or use eval output
  as threshold acceptance.
- Do not issue live verdicts, arena actions, scars, memory writes, rank
  mutations, or hidden scheduler actions.

## Validation

```bash
python mechanics/agon/parts/sophian-threshold-alignment/scripts/build_agon_sophian_eval_alignment_registry.py --check
python mechanics/agon/parts/sophian-threshold-alignment/scripts/validate_agon_sophian_eval_alignment_registry.py
python -m pytest -q mechanics/agon/parts/sophian-threshold-alignment/tests/test_agon_sophian_eval_alignment_registry.py
```
