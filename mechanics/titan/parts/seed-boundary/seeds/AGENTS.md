# AGENTS.md

## Applies to

`mechanics/titan/parts/seed-boundary/seeds/` seed canary surfaces.

## Role

This directory stores Titan seed canaries under
`mechanics/titan/parts/seed-boundary/seeds/titan*.yaml`.

These files are boundary-check seeds, not full eval bundles, executable scorer
suites, runtime activation receipts, or proof of Titan incarnation.

## Read before editing

1. repository root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `docs/LEGACY_NAMING.md`
6. `mechanics/titan/README.md`
7. `mechanics/titan/parts/seed-boundary/seeds/README.md`
8. `mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md`
9. `mechanics/titan/parts/seed-boundary/docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md`
10. `scripts/validate_repo.py` function `validate_titan_canary_surfaces`

## Boundaries

- Keep `id` or `eval_id` equal to the filename stem.
- Keep each canary public-safe and falsifiable through checks, required fields,
  expected output, forbidden output, or failure examples.
- Keep Titan canaries seed-defined unless executable scorer contracts,
  fixtures, and reports are added.
- Do not claim full incarnation proof, runtime activation, hidden arena,
  memory sovereignty, or summon authority from these YAML files.
- Do not bypass mutation gate or judgment gate boundaries.
- Do not move canary files out of this package without updating package route
  docs, decisions, and validators.

## Validation

Run:

```bash
python scripts/validate_repo.py
python -m pytest -q tests/test_validate_repo.py -k titan_canary
```

Run broader checks when canary edits affect generated, release, or public
selection surfaces.

## Closeout

Report which canaries changed, whether they remain seed-defined, which
boundary each protects, what validation ran, and what stronger Titan owner law
or runtime claim was not changed.
