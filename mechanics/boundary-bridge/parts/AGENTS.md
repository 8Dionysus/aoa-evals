# AGENTS.md

## Applies To

This card applies to `mechanics/boundary-bridge/parts/` and every descendant active part.

## Role

`mechanics/boundary-bridge/parts/` holds active part contracts for the Boundary Bridge proof mechanic.

Parts are operation nodes. They are not root docs, generated authority, release ledgers, runtime facts, sibling-owner truth, or bundle-local proof meaning unless the owning source surface says so.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, the parent `AGENTS.md`, parent `DIRECTION.md`, parent `PARTS.md`, parent `PROVENANCE.md`, and the nearest part `README.md` plus `VALIDATION.md` before editing a part.

## Boundaries

- Keep each part tied to one row in the parent `PARTS.md`.
- Keep source proof meaning in bundles or source docs, not in validation text.
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

### `mechanics/boundary-bridge/parts/compatibility-map/VALIDATION.md`

```bash
python scripts/validate_repo.py
```

### `mechanics/boundary-bridge/parts/latest-sibling-canary/VALIDATION.md`

```bash
python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json
python -m pytest -q mechanics/boundary-bridge/parts/latest-sibling-canary/tests/test_sibling_canary.py
python scripts/validate_repo.py
```

### `mechanics/boundary-bridge/parts/orchestrator-proof-anchors/VALIDATION.md`

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```

### `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/VALIDATION.md`

```bash
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

<!-- centralized-child-validation:end -->

## Closeout

Report active parts changed, source surfaces or payload homes moved, validation commands run, checks skipped, and stronger-owner boundaries preserved.
