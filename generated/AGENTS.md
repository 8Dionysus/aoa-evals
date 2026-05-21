# AGENTS.md

Local guidance for `generated/`.

## Purpose

`generated/` stores repo-wide derived reader surfaces only. Package-owned
generated companions live under their mechanic part and follow the same
derived-surface posture. No generated file is source-owned doctrine.

## Current surfaces

- `generated/eval_catalog.json`
- `generated/eval_catalog.min.json`
- `generated/eval_capsules.json`
- `generated/comparison_spine.json`
- `generated/eval_sections.full.json`
- `generated/eval_report_index.min.json`
- `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json`
- `mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json`
- `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/phase_alpha_eval_matrix.min.json`
- `generated/quest_catalog.min.json`
- `generated/quest_catalog.min.example.json`
- `generated/quest_dispatch.min.json`
- `generated/quest_dispatch.min.example.json`
- Agon generated registries now live under `mechanics/agon/parts/*/generated/`
- RPG unlock proof generated/example cards now live under
  `mechanics/rpg/parts/progression-unlocks/generated/`
- Phase Alpha eval matrix generated output now lives under
  `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/`

## Rules

Do not hand-edit files in this directory.
Regenerate them with the owning builder:

- `python scripts/build_catalog.py`
- `python scripts/generate_eval_report_index.py`
- `python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py`
- `python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py`
- `python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py`

Use each builder's `--check` mode or `python scripts/validate_repo.py` to
confirm generated surfaces stay current.
Keep the min catalog an exact projection of the full catalog.
Keep catalogs, capsules, sections, comparison spine, report index, runtime
candidate readers, quest readers, part-local Agon registries, part-local RPG
unlock proof cards, and the part-local Phase Alpha eval matrix aligned with
their source surfaces.

## Do not store

- new claim wording
- hidden provenance
- repo-local scratch notes
- receipt authority
- runtime acceptance
