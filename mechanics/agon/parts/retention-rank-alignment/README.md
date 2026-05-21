# Retention Rank Alignment

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

- Do not mutate rank, trust, retention schedules, scars, memory, stats truth, or
  Tree of Sophia canon.
- Do not treat eval alignment as promotion, demotion, quarantine, or retention
  execution.
- Do not let generated rank-pressure records outrank owner review or
  bundle-local proof.

## Validation

```bash
python mechanics/agon/parts/retention-rank-alignment/scripts/build_agon_retention_rank_eval_alignment_registry.py --check
python mechanics/agon/parts/retention-rank-alignment/scripts/validate_agon_retention_rank_eval_alignment.py
python -m pytest -q mechanics/agon/parts/retention-rank-alignment/tests/test_agon_retention_rank_eval_alignment.py
```
