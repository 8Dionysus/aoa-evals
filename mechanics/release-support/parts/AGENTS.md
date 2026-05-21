# AGENTS.md

## Applies To

This card applies to `mechanics/release-support/parts/` and every descendant active part.

## Role

`mechanics/release-support/parts/` holds active part contracts for the Release Support proof mechanic.

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

### `mechanics/release-support/parts/pr-handoff/VALIDATION.md`

```bash
python -m pytest -q mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py tests/test_validate_repo.py -k release_prep_pr_handoff
python scripts/validate_repo.py
python scripts/release_check.py
```

### `mechanics/release-support/parts/readiness-audit/VALIDATION.md`

```bash
python -m pytest -q mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py tests/test_validate_repo.py -k release_support_readiness
python scripts/validate_repo.py
python scripts/release_check.py
```

### `mechanics/release-support/parts/strategic-closeout/VALIDATION.md`

```bash
python -m pytest -q mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py tests/test_validate_repo.py -k strategic_closeout
python scripts/validate_repo.py
python scripts/release_check.py
```

<!-- centralized-child-validation:end -->

## Closeout

Report active parts changed, source surfaces or payload homes moved, validation commands run, checks skipped, and stronger-owner boundaries preserved.
