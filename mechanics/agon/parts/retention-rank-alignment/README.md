# Agon / Retention Rank Alignment Part

## Role

This part owns retention and rank pressure alignment while preserving
candidate-only posture and forbidding rank or trust mutation.

It lets `aoa-evals` inspect whether retention or rank pressure is bounded
without giving the eval layer mutation authority.

## Route

`retention pressure -> rank alignment seed -> generated alignment registry -> no-mutation validation`

## Source Surfaces

- `mechanics/agon/parts/retention-rank-alignment/docs/AGON_RETENTION_RANK_EVAL_ALIGNMENT.md`
- `mechanics/agon/parts/retention-rank-alignment/config/agon_retention_rank_eval_alignment.seed.json`
- `mechanics/agon/parts/retention-rank-alignment/schemas/agon-retention-rank-eval-alignment*.schema.json`
- `mechanics/agon/parts/retention-rank-alignment/examples/agon_retention_rank_eval_alignment.example.json`
- `mechanics/agon/parts/retention-rank-alignment/generated/agon_retention_rank_eval_alignment_registry.min.json`
- `mechanics/agon/parts/retention-rank-alignment/manifests/`

## Inputs

- retention, rank, trust, and promotion-pressure alignment records;
- stop-lines that forbid mutation, retention execution, and stats-as-authority;
- part-local schema, example, builder, validator, and tests.

## Outputs

- deterministic `agon_retention_rank_eval_alignment_registry.min.json` output;
- candidate-only alignment records for retention and rank pressure;
- validation failures when runtime effect, mutation, or authority boundaries
  drift.

## Stronger Owner Split

`aoa-evals` owns the candidate alignment registry and no-mutation checks.

Agents-of-Abyss, stats, memory, runtime, and any future retention owner keep
rank truth, trust truth, retention execution, and durable state authority.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| rank, trust, retention schedule, scar, memory, stats truth, or Tree of Sophia canon mutation pressure | route to the owner of the durable state or canon; this part keeps no-mutation alignment evidence |
| promotion, demotion, quarantine, or retention execution pressure | route to the retention/rank owner before any live effect is considered |
| generated rank-pressure records look stronger than owner review or bundle-local proof | route back to review evidence before using the record outside the part |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
