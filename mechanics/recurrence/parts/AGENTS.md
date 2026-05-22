# AGENTS.md

## Applies To

This card applies to `mechanics/recurrence/parts/` and every descendant active part.

## Role

`mechanics/recurrence/parts/` holds active part contracts for the Recurrence proof mechanic.

Parts are operation nodes. They route part contracts, payload homes, source surfaces, and validation commands while keeping stronger owner truth visible.

## Operating Card

| Field | Route |
| --- | --- |
| role | part-contract and payload route law for this mechanic parent |
| input | part boundary change, payload movement, source-surface pressure, validation route change, or legacy placement question |
| output | parent `PARTS.md` alignment, nearest part `README.md`, part `VALIDATION.md`, centralized child validation command, or stronger-owner handoff |
| owner | parent `PARTS.md` owns the part map; nearest part `README.md` owns the part contract; this card owns executable child validation commands |
| next route | parent `AGENTS.md`, parent `DIRECTION.md`, parent `PARTS.md`, nearest part `README.md`, nearest part `VALIDATION.md`, and affected payload home |
| tools | parent validation lane, centralized child validation commands, root validator, semantic AGENTS validator |
| validation | this card's `Validation` section |

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, the parent `AGENTS.md`, parent `DIRECTION.md`, parent `PARTS.md`, parent `PROVENANCE.md`, and the nearest part `README.md` plus `VALIDATION.md` before editing a part.

## Route Rules

- Keep each part tied to one row in the parent `PARTS.md`.
- Keep source proof meaning in bundles or source docs; validation text carries check route and evidence coverage.
- Keep executable child validation commands in this card so README files stay route maps and contracts.
- Route legacy placement through parent `PROVENANCE.md` and `legacy/` rather than recreating old root payload paths.

## Validation

Run the parent validation lane first when part topology or route shape changes:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

<!-- centralized-child-validation:start -->

### Centralized Child Validation

Executable validation commands from child part routes live here. Child README and VALIDATION files route to this section instead of carrying command blocks.

### `mechanics/recurrence/parts/anchor-return/VALIDATION.md`

```bash
python scripts/validate_repo.py --eval aoa-return-anchor-integrity
python scripts/build_catalog.py --check
```

### `mechanics/recurrence/parts/control-plane-integrity/VALIDATION.md`

```bash
python mechanics/recurrence/parts/control-plane-integrity/scripts/run_recurrence_control_plane_integrity_eval.py --case mechanics/recurrence/parts/control-plane-integrity/fixtures/recurrence-control-plane-integrity-v1/cases/RCPI-001.registry-mixed-manifests.json --check-expected --json
python -m pytest -q mechanics/recurrence/parts/control-plane-integrity/tests/test_recurrence_control_plane_integrity_eval_seed.py
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```

### `mechanics/recurrence/parts/memory-recall/VALIDATION.md`

```bash
python scripts/validate_repo.py --eval aoa-memo-recall-integrity
python -m pytest -q mechanics/recurrence/parts/memory-recall/tests/test_memo_recall_phase_alpha_report.py
python scripts/build_catalog.py --check
```

### `mechanics/recurrence/parts/portable-proof-beacons/VALIDATION.md`

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
```

### `mechanics/recurrence/parts/recursor-boundary/VALIDATION.md`

```bash
python mechanics/recurrence/parts/recursor-boundary/scripts/run_recursor_readiness_boundary_eval.py --case mechanics/recurrence/parts/recursor-boundary/fixtures/recursor-readiness-boundary-v1/cases/RRB-001.no-spawn-readiness.json --check-expected --json
python -m pytest -q mechanics/recurrence/parts/recursor-boundary/tests/test_recursor_readiness_boundary_eval_seed.py
```

### `mechanics/recurrence/parts/stats-regrounding-boundary/VALIDATION.md`

```bash
python scripts/validate_repo.py --eval aoa-stats-regrounding-boundary-integrity
python -m pytest -q mechanics/recurrence/parts/stats-regrounding-boundary/tests/test_stats_regrounding_boundary_eval.py
python scripts/build_catalog.py --check
```

<!-- centralized-child-validation:end -->

## Closeout

Report active parts changed, source surfaces or payload homes moved, validation commands run, checks skipped, and stronger-owner boundaries preserved.
