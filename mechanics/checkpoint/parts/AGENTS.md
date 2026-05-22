# AGENTS.md

## Applies To

This card applies to `mechanics/checkpoint/parts/` and every descendant active part.

## Role

`mechanics/checkpoint/parts/` holds active part contracts for the Checkpoint proof mechanic.

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

### `mechanics/checkpoint/parts/a2a-summon-return/VALIDATION.md`

```bash
python -m pytest -q mechanics/checkpoint/parts/a2a-summon-return/tests/test_a2a_summon_return_checkpoint_fixture.py
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```

### `mechanics/checkpoint/parts/restartable-inquiry/VALIDATION.md`

```bash
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```

### `mechanics/checkpoint/parts/self-agent-posture/VALIDATION.md`

```bash
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python scripts/validate_repo.py
```

<!-- centralized-child-validation:end -->

## Closeout

Report active parts changed, source surfaces or payload homes moved, validation commands run, checks skipped, and stronger-owner boundaries preserved.
