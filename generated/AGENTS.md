# AGENTS.md

Local guidance for `generated/`.

## Purpose

`generated/` stores repo-wide derived reader surfaces only. Package-owned
generated companions live under their mechanic part and follow the same
derived-surface posture. No generated file is source-owned doctrine.

Use [README.md](README.md) for the generated reader index. This card owns edit
law and validation posture.

The root reader names guarded here are `generated/eval_catalog.json`,
`generated/eval_catalog.min.json`, `generated/eval_capsules.json`,
`generated/comparison_spine.json`, `generated/eval_sections.full.json`, and
`generated/eval_report_index.min.json`, plus the quest reader pair
`generated/quest_catalog.min.json`, `generated/quest_dispatch.min.json`,
`generated/quest_catalog.min.example.json`, and
`generated/quest_dispatch.min.example.json`.

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

## Validation

For generated-reader freshness, run the matching non-mutating checks:

```bash
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
python scripts/validate_repo.py
```

Use source-owner checks as well when generated drift comes from bundle, quest,
report, or mechanic payload changes.

## Do not store

- new claim wording
- hidden provenance
- repo-local scratch notes
- receipt authority
- runtime acceptance
