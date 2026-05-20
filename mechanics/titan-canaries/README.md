# Titan Canaries Mechanic

## Role

`mechanics/titan-canaries/` routes the operation that keeps Titan seed canary
surfaces shaped, bounded, and visibly weaker than full incarnation proof.

It is not the Titan doctrine owner, runtime roster owner, summon runtime,
executable scorer suite, memory authority, or proof that Titan incarnation is
complete.

## Owned Operation

`Titan boundary pressure -> seed canary YAML -> shape validation -> future executable scorer route -> bounded proof or owner handoff`

This package routes Titan canary work. Current source seeds stay under
`evals/titan_*_canary.yaml`.

## Source Surfaces

- `docs/TITAN_INCARNATION_CANARIES.md`
- `docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md`
- `evals/titan_*_canary.yaml`
- `evals/AGENTS.md`
- `docs/LEGACY_NAMING.md`
- `docs/PROOF_TOPOLOGY.md`
- `scripts/validate_repo.py` function `validate_titan_canary_surfaces`
- `tests/test_validate_repo.py`

## Inputs

- one Titan boundary pressure such as named identity, summon discipline, gate
  payload, memory provenance, lineage non-erasure, runtime roster, closeout
  receipt, or hidden-arena prevention
- one public-safe canary YAML file under `evals/`
- an `id` or `eval_id` that matches the filename stem
- a `purpose`, `claim`, `kind`, `description`, or `objective`
- `checks`, `expected_failure`, `expected_result`, `expected`, `forbidden`, or
  failure examples that make the seed falsifiable

## Outputs

- seed-defined Titan boundary canary
- validator-visible canary shape
- route to a future executable scorer only when scorer contracts exist
- bounded proof or owner handoff only after review accepts the canary result

## Stronger Owner Split

`aoa-evals` owns the canary seed shape and bounded proof posture.

Titan role law, summon rights, runtime activation, memory authority, and
incarnation doctrine remain stronger-owner concerns. A canary can point at a
boundary pressure; it cannot grant runtime authority, activate a Titan cohort,
or certify incarnation by itself.

When a canary depends on external Titan law, the source owner keeps the stronger
meaning and `aoa-evals` keeps only the bounded check surface.

## Boundaries

- Do not move `evals/titan_*_canary.yaml` into this package.
- Do not treat seed canaries as full incarnation proof.
- Do not claim runtime activation, hidden arena or hidden background arena, or live summon
  authority from a YAML seed.
- Do not let memory canaries create memory sovereignty.
- Do not bypass mutation gate or judgment gate boundaries.
- Do not convert seed canaries to executable scorer claims until scorer
  contracts and fixtures exist.
- Do not erase historical Titan canary vocabulary before replacement routes and
  validators can follow.

## Validation

After changing Titan canary route surfaces, run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

For a narrow canary-shape check, run:

```bash
python -m pytest -q tests/test_validate_repo.py -k titan_canary
```

When canary seeds are later converted into executable scorer surfaces, add the
new scorer, fixture, and report checks before calling them executable proof.

## Next Route

Use this package before:

- adding or changing `evals/titan_*_canary.yaml`;
- changing Titan canary guide wording;
- changing `validate_titan_canary_surfaces`;
- deciding whether a Titan seed canary can become an executable scorer-backed
  eval;
- routing Titan canary legacy vocabulary into active topology.
