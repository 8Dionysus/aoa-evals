# 0048 Proof Object Contract Parts

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/proof-object/`

## Context

The proof-object mechanic owns the operation that keeps source eval bundles
complete, bounded, and stronger than generated readers:

`origin proof pressure -> source proof bundle -> proof-object completeness review -> generated reader derivation -> bundle-local report or downstream route`

Before this decision, core proof-object support was split across former root
districts:

- former root `templates/EVAL.template.md`
- former root `schemas/eval-frontmatter.schema.json`
- former root `schemas/eval-manifest.schema.json`

Those files are not generic proof-infra. They define how source proof bundles
are authored and validated.

## Options Considered

- Leave template and eval schemas in root `templates/` and `schemas/`.
- Move them into a flat `mechanics/proof-object/` directory.
- Split them into active proof-object parts.

## Decision

Move the authoring template to:

`mechanics/proof-object/parts/bundle-authoring/templates/EVAL.template.md`

Move the eval frontmatter and manifest schemas to:

`mechanics/proof-object/parts/bundle-contracts/schemas/`

Add `mechanics/proof-object/PARTS.md`, `PROVENANCE.md`, and legacy index/log
surfaces so active parts come first and former root placement remains
traceable.

## Rationale

This keeps topology convex. Template and eval schemas are proof-object parts,
not parent mechanics and not generic root contracts.

The source bundles stay under `bundles/`, and generated readers stay under
`generated/`. The part-local contracts support those surfaces without stealing
their authority.

## Consequences

- Positive: root `templates/` and root eval schema placement no longer hide a
  proof-object-owned operation.
- Positive: schema validation now points at active proof-object parts.
- Positive: old paths stay findable through provenance instead of active
  topology.
- Tradeoff: docs and validators use longer part-local paths.

## Boundaries

This decision does not move source proof bundles out of `bundles/`.

It does not move generated catalog, capsule, section, or comparison readers out
of `generated/`.

It does not make the template proof evidence, maturity proof, or a source
bundle.

It does not make eval schemas stronger than bundle-local meaning.

## Validation

- `mechanics/proof-object/PARTS.md` names active parts, stop-lines, and
  validation.
- `mechanics/proof-object/PROVENANCE.md` bridges former root placement
  questions into the owning legacy archive.
- `scripts/validate_repo.py` uses the part-local schema paths.
- `python scripts/validate_repo.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_semantic_agents.py`
