# AGENTS.md

Local guidance for `fixtures/`.

## Purpose

`fixtures/` is the public-safe compatibility route card for former root shared
fixture families.

No active fixture-family directory should live here after the proof-infra
fixture-family slice.

## Current shared families

Generic shared fixture families now live under:

- `mechanics/proof-infra/parts/fixture-families/fixtures/`

Comparison-spine fixture families now live under their active parts:

- `mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/`
- `mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v1/`
- `mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v2/`
- `mechanics/comparison-spine/parts/longitudinal-window/fixtures/repeated-window-bounded-v1/`

## Rules

Keep each shared family weaker than the bundle-local EVAL.md meaning it supports.
Preserve replacement guidance so another repo can keep the bounded claim surface when cases are swapped.
When a bundle points here, keep `shared_fixture_family_path` explicit and use `additional_shared_fixture_family_paths` only for real secondary reusable families.
When a bundle points to a mechanic-local fixture family, keep the part-local
path explicit and do not recreate a root fixture alias.
Route new generic shared fixture families through `mechanics/proof-infra/`
first; route domain-specific families through the active owning mechanic.
Do not add secret-bearing logs, hidden benchmark dumps, or private telemetry.

## Validation

Run `python scripts/validate_repo.py` after changing shared families or their replacement contract.
