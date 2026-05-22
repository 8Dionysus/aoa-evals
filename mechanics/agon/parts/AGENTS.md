# AGENTS.md

## Applies To

This card applies to `mechanics/agon/parts/` and every descendant active part.

## Role

`mechanics/agon/parts/` holds active part contracts for the Agon proof mechanic.

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

### `mechanics/agon/parts/ccs-alignment/VALIDATION.md`

```bash
python mechanics/agon/parts/ccs-alignment/scripts/build_agon_ccs_eval_alignment_registry.py --check
python mechanics/agon/parts/ccs-alignment/scripts/validate_agon_ccs_eval_alignment.py
python -m pytest -q mechanics/agon/parts/ccs-alignment/tests/test_agon_ccs_eval_alignment.py
```

### `mechanics/agon/parts/court-prebinding/VALIDATION.md`

```bash
python mechanics/agon/parts/court-prebinding/scripts/build_agon_eval_prebinding_registry.py --check
python mechanics/agon/parts/court-prebinding/scripts/validate_agon_eval_prebindings.py
python -m pytest -q mechanics/agon/parts/court-prebinding/tests/test_agon_eval_prebindings.py
```

### `mechanics/agon/parts/epistemic-alignment/VALIDATION.md`

```bash
python mechanics/agon/parts/epistemic-alignment/scripts/build_agon_epistemic_eval_alignment_registry.py --check
python mechanics/agon/parts/epistemic-alignment/scripts/validate_agon_epistemic_eval_alignment.py
python -m pytest -q mechanics/agon/parts/epistemic-alignment/tests/test_agon_epistemic_eval_alignment.py
```

### `mechanics/agon/parts/kag-alignment/VALIDATION.md`

```bash
python mechanics/agon/parts/kag-alignment/scripts/build_agon_kag_eval_alignment_registry.py --check
python mechanics/agon/parts/kag-alignment/scripts/validate_agon_kag_eval_alignment_registry.py
python -m pytest -q mechanics/agon/parts/kag-alignment/tests/test_agon_kag_eval_alignment_registry.py
```

### `mechanics/agon/parts/mechanical-trial-suites/VALIDATION.md`

```bash
python mechanics/agon/parts/mechanical-trial-suites/scripts/build_agon_mechanical_trial_eval_suites.py --check
python mechanics/agon/parts/mechanical-trial-suites/scripts/validate_agon_mechanical_trial_eval_suites.py
python -m pytest -q mechanics/agon/parts/mechanical-trial-suites/tests/test_agon_mechanical_trial_eval_suites.py
```

### `mechanics/agon/parts/retention-rank-alignment/VALIDATION.md`

```bash
python mechanics/agon/parts/retention-rank-alignment/scripts/build_agon_retention_rank_eval_alignment_registry.py --check
python mechanics/agon/parts/retention-rank-alignment/scripts/validate_agon_retention_rank_eval_alignment.py
python -m pytest -q mechanics/agon/parts/retention-rank-alignment/tests/test_agon_retention_rank_eval_alignment.py
```

### `mechanics/agon/parts/slc-alignment/VALIDATION.md`

```bash
python mechanics/agon/parts/slc-alignment/scripts/build_agon_slc_eval_alignment_registry.py --check
python mechanics/agon/parts/slc-alignment/scripts/validate_agon_slc_eval_alignment_registry.py
python -m pytest -q mechanics/agon/parts/slc-alignment/tests/test_agon_slc_eval_alignment_registry.py
```

### `mechanics/agon/parts/sophian-threshold-alignment/VALIDATION.md`

```bash
python mechanics/agon/parts/sophian-threshold-alignment/scripts/build_agon_sophian_eval_alignment_registry.py --check
python mechanics/agon/parts/sophian-threshold-alignment/scripts/validate_agon_sophian_eval_alignment_registry.py
python -m pytest -q mechanics/agon/parts/sophian-threshold-alignment/tests/test_agon_sophian_eval_alignment_registry.py
```

### `mechanics/agon/parts/vds-alignment/VALIDATION.md`

```bash
python mechanics/agon/parts/vds-alignment/scripts/build_agon_vds_eval_alignment_registry.py --check
python mechanics/agon/parts/vds-alignment/scripts/validate_agon_vds_eval_alignment.py
python -m pytest -q mechanics/agon/parts/vds-alignment/tests/test_agon_vds_eval_alignment.py
```

<!-- centralized-child-validation:end -->

## Closeout

Report active parts changed, source surfaces or payload homes moved, validation commands run, checks skipped, and stronger-owner boundaries preserved.
