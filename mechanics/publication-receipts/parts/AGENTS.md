# AGENTS.md

## Applies To

This card applies to `mechanics/publication-receipts/parts/` and every descendant active part.

## Role

`mechanics/publication-receipts/parts/` holds active part contracts for the Publication Receipts proof mechanic.

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

### `mechanics/publication-receipts/parts/intake-dry-review/VALIDATION.md`

```bash
python -m pytest -q mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py tests/test_validate_repo.py -k receipt_intake_dry_review
python scripts/validate_repo.py
```

### `mechanics/publication-receipts/parts/live-publisher/VALIDATION.md`

```bash
python -m pytest -q mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py
python scripts/validate_repo.py
```

### `mechanics/publication-receipts/parts/receipt-payload/VALIDATION.md`

```bash
python scripts/validate_repo.py
python -m pytest -q mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py tests/test_validate_repo.py -k publication_receipts
```

### `mechanics/publication-receipts/parts/stats-envelope-mirror/VALIDATION.md`

```bash
python scripts/validate_repo.py
python -m pytest -q mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py tests/test_validate_repo.py -k live_receipt
```

<!-- centralized-child-validation:end -->

## Closeout

Report active parts changed, source surfaces or payload homes moved, validation commands run, checks skipped, and stronger-owner boundaries preserved.
