# AGENTS.md

Local route card for `generated/`.

## Purpose

`generated/` stores repo-wide derived reader surfaces only. Package-owned
generated companions live under their mechanic part and follow the same
derived-surface posture. Authored source surfaces keep doctrine; generated
files remain derived readers.

Use [README.md](README.md) for the generated reader index. This card owns edit
law and validation posture.

The root reader names guarded here are `generated/eval_catalog.json`,
`generated/eval_catalog.min.json`, `generated/eval_capsules.json`,
`generated/comparison_spine.json`, `generated/eval_sections.full.json`,
`generated/eval_report_index.min.json`,
`generated/eval_readiness_dashboard.json`,
`generated/eval_readiness_dashboard.md`, and
`generated/eval_support_registry.json`, plus the quest reader pair
`generated/quest_catalog.min.json`, `generated/quest_dispatch.min.json`,
`generated/quest_catalog.min.example.json`, and
`generated/quest_dispatch.min.example.json`.

## Operating Card

| Field | Route |
| --- | --- |
| role | repo-wide derived reader district |
| input | source eval packages, quest source records, reports, mechanic payloads, and builder inputs |
| output | compact reader surfaces for agents, validators, and tools |
| owner | source surfaces and builders named in `generated/README.md` |
| next route | source bundle, quest record, report, mechanic part, or builder check |
| tools | catalog builder, report-index builder, readiness-dashboard builder, candidate-reader builders, phase-alpha matrix builder |
| validation | this card's `Validation` section |

## Edit Route

Regenerate files with the owning builder:

- `python scripts/build_catalog.py`
- `python scripts/generate_eval_report_index.py`
- `python scripts/build_eval_readiness_dashboard.py --write-generated`
- `python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py`
- `python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py`
- `python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py`

Use each builder's `--check` mode or `python scripts/validate_repo.py` to
confirm generated surfaces stay current.
Keep the min catalog an exact projection of the full catalog.
Keep catalogs, capsules, sections, comparison spine, report index, readiness
dashboard, support registry, runtime candidate readers, quest readers,
part-local Agon registries, part-local RPG unlock proof cards, and the
part-local Phase Alpha eval matrix aligned with their source surfaces.

The readiness dashboard may project local suite execution state from the v2
inventory contract. It keeps the exact `absent`/`invalid`/`stale`/`ready`
vocabulary and `invalid > stale > ready > absent` aggregate priority, but it
never executes `runner.argv`. A `.suite.md` note alone projects as `absent`.
`ready` projects source-contract readiness only, never pinned-runtime
reproducibility; the dashboard keeps canonical-owner and downstream
JIT/environment/receipt requirements visible.
Generated dashboard paths name the canonical `/srv/AbyssOS/aoa-evals` owner
checkout, never an ephemeral `.worktrees/` implementation path. V1 or unknown
inventory input is normalized to suite state `absent` before projection.

## Validation

For generated-reader freshness, run the matching non-mutating checks:

```bash
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
python scripts/build_eval_readiness_dashboard.py --check
python scripts/check_eval_support_registry.py --json
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
python scripts/validate_repo.py
```

Use source-owner checks as well when generated drift comes from bundle, quest,
report, or mechanic payload changes.

## Storage Route

Store only derived reader payloads and public-safe examples here.

| Need | Owner route |
| --- | --- |
| new claim wording | bundle-local `EVAL.md` and `eval.yaml` |
| provenance | owning mechanic `PROVENANCE.md`, `legacy/`, or decision record |
| scratch notes | local task workspace, not checked-in generated readers |
| receipt authority | publication-receipts mechanic or bundle-local report surface |
| runtime acceptance | runtime owner or audit intake surface before proof adoption |
