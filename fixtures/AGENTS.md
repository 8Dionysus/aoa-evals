# AGENTS.md

Local guidance for `fixtures/`.

## Purpose

`fixtures/` stores public-safe shared fixture families for portable proof reuse.

## Current shared families

- `bounded-change-paired-v1`
- `bounded-change-paired-v2`
- `frozen-same-task-v1`
- `repeated-window-bounded-v1`

## Rules

Keep each shared family weaker than the bundle-local EVAL.md meaning it supports.
Preserve replacement guidance so another repo can keep the bounded claim surface when cases are swapped.
When a bundle points here, keep `shared_fixture_family_path` explicit and use `additional_shared_fixture_family_paths` only for real secondary reusable families.
Do not add secret-bearing logs, hidden benchmark dumps, or private telemetry.

## Validation

Run `python scripts/validate_repo.py` after changing shared families or their replacement contract.
