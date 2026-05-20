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
- `generated/eval_report_index.min.json`
- `generated/runtime_candidate_template_index.min.json`
- `generated/runtime_candidate_intake.min.json`
- `generated/phase_alpha_eval_matrix.min.json`
- `generated/quest_catalog.min.json`
- `generated/quest_catalog.min.example.json`
- `generated/quest_dispatch.min.json`
- `generated/quest_dispatch.min.example.json`
- `generated/agon_*_registry.min.json`
- `generated/unlock_proof_cards.min.example.json`

## Rules

Do not hand-edit files in this directory.
Regenerate them with the owning builder:

- `python scripts/build_catalog.py`
- `python scripts/generate_eval_report_index.py`
- `python scripts/generate_runtime_candidate_template_index.py`
- `python scripts/generate_runtime_candidate_intake.py`
- `python scripts/generate_phase_alpha_eval_matrix.py`

Use each builder's `--check` mode or `python scripts/validate_repo.py` to
confirm generated surfaces stay current.
Keep the min catalog an exact projection of the full catalog.
Keep catalogs, capsules, sections, comparison spine, report index, runtime
candidate readers, quest readers, and Agon registries aligned with their source
surfaces.

## Do not store

- new claim wording
- hidden provenance
- repo-local scratch notes
- receipt authority
- runtime acceptance
