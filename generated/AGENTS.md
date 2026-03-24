# AGENTS.md

Local guidance for `generated/`.

## Purpose

`generated/` stores derived reader surfaces only. No file here is source-owned doctrine.

## Current surfaces

- `generated/eval_catalog.json`
- `generated/eval_catalog.min.json`
- `generated/eval_capsules.json`
- `generated/comparison_spine.json`
- `generated/eval_sections.full.json`

## Rules

Do not hand-edit files in this directory.
Regenerate them with `python scripts/build_catalog.py`.
Use `python scripts/build_catalog.py --check` or `python scripts/validate_repo.py` to confirm they stay current.
Keep the min catalog an exact projection of the full catalog.
Keep catalogs, capsules, sections, and comparison spine 1:1 aligned with the source bundle surface.

## Do not store

- new claim wording
- hidden provenance
- repo-local scratch notes
