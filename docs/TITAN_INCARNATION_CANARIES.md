# Titan Incarnation Canaries

## Role

This guide routes Titan boundary canaries in `aoa-evals`.

It is not full Titan doctrine, runtime activation guidance, summon authority,
memory authority, or proof that incarnation is complete.

## Active Route

Use `mechanics/titan-canaries/README.md` for Titan canary package work.

The current seed route is:

`Titan boundary pressure -> seed canary YAML -> shape validation -> future executable scorer route -> bounded proof or owner handoff`

## Current Seed Surfaces

Primary canary seeds live under `evals/titan_*_canary.yaml`.

They cover boundary pressures such as:

- named identity and no generic role shadow;
- Forge mutation gate payload completeness;
- Delta judgment gate payload completeness;
- memory source refs and no memory sovereignty;
- lineage non-erasure;
- runtime roster visibility;
- closeout receipt completeness;
- no hidden arena or background runtime.

`docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md` carries the summon-discipline guide
for the same seed family.

## Shape Rule

Every Titan seed canary should be public-safe and falsifiable. These seed canaries stay weaker than full incarnation proof.

The validator expects:

- `id` or `eval_id` matching the filename stem;
- optional integer `version` when a version is present;
- a non-empty `purpose`, `claim`, `kind`, `description`, or `objective`;
- `checks`, `expected_failure`, `expected_result`, `expected`, `forbidden`, or
  failure examples that make the seed reviewable.

## Boundaries

- Seed canaries are not full incarnation proof.
- Seed canaries do not activate a runtime cohort.
- Seed canaries do not grant summon authority.
- Seed canaries do not create memory sovereignty.
- Seed canaries do not bypass mutation gate or judgment gate requirements.
- Seed canaries should become executable scorer-backed proof only after scorer,
  fixture, and report contracts exist.

## Validation

Run:

```bash
python scripts/validate_repo.py
python -m pytest -q tests/test_validate_repo.py -k titan_canary
```
