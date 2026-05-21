# Agon / Mechanical Trial Suites Part

## Role

This part owns candidate eval suites that align Agon mechanical trial surfaces
without running an arena or issuing verdict authority.

The suites describe what `aoa-evals` may inspect about mechanical trials, not
how the trials are run.

## Route

`trial-suite pressure -> eval-suite seed -> generated suite registry -> candidate-only validation`

## Source Surfaces

- `mechanics/agon/parts/mechanical-trial-suites/docs/AGON_MECHANICAL_TRIAL_EVAL_SUITES.md`
- `mechanics/agon/parts/mechanical-trial-suites/config/agon_mechanical_trial_eval_suites.seed.json`
- `mechanics/agon/parts/mechanical-trial-suites/schemas/agon_mechanical_trial_eval_suites*.schema.json`
- `mechanics/agon/parts/mechanical-trial-suites/examples/agon_mechanical_trial_eval_suites.example.json`
- `mechanics/agon/parts/mechanical-trial-suites/generated/agon_mechanical_trial_eval_suite_registry.min.json`
- `mechanics/agon/parts/mechanical-trial-suites/manifests/`

## Inputs

- trial ids, playbook ids, expected terminal candidates, and required prechecks;
- source-surface refs into stronger trial-run or trial-suite owners;
- part-local schema, example, builder, validator, and test coverage.

## Outputs

- deterministic `agon_mechanical_trial_eval_suite_registry.min.json` output;
- candidate-only eval-suite records for later review;
- validation failures when a suite claims live protocol, arena execution,
  verdict authority, rank mutation, or durable state mutation.

## Stronger Owner Split

`aoa-evals` owns the candidate eval-suite registry and local proof-alignment
checks.

Agents-of-Abyss and runtime owners keep mechanical trial law, trial execution,
arena state, run truth, and verdict authority.

## Stop-Lines

- Do not run an arena, open a live protocol, or execute a trial from this part.
- Do not issue verdicts, write scars, mutate rank or trust, retain candidates,
  or promote anything into Tree of Sophia canon.
- Do not use candidate eval-suite output as proof without bundle-local review.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
