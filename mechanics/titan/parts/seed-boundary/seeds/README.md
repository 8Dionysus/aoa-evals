# Titan Canary Seeds

## Role

`mechanics/titan/parts/seed-boundary/seeds/` owns the source YAML seed family
for the Titan mechanic.

These files are seed-defined boundary checks. They are not full eval bundles,
executable scorer suites, runtime activation receipts, summon authority,
memory authority, or proof of Titan incarnation.

## Source Shape

Current seed files match `titan*.yaml`.

Each seed must keep:

- an `id` or `eval_id` matching the filename stem;
- public-safe boundary pressure;
- a non-empty `purpose`, `claim`, `kind`, `description`, or `objective`;
- falsifiability through `checks`, `required_fields`, `expected_failure`,
  `expected_result`, `expected`, `forbidden`, `description`, or failure
  examples.

## Boundaries

- Keep seed files package-local under
  `mechanics/titan/parts/seed-boundary/seeds/`.
- Keep seed-defined status unless scorer contracts, fixtures, and reports are
  added.
- Do not claim full incarnation proof, runtime activation, hidden arena, live
  summon authority, memory sovereignty, mutation-gate bypass, or judgment-gate
  bypass.
- Keep stronger Titan owner law outside `aoa-evals`.

## Validation

Run:

```bash
python scripts/validate_repo.py
python -m pytest -q tests/test_validate_repo.py -k titan_canary
```
