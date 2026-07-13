# Proof Object Contract Parts

- Decision ID: AOA-EV-D-0048
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/proof-object/`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: mechanic part
- Mechanic parents: proof-object
- Guard families: part and payload
- Posture: active rationale

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

`mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md`

Move the eval frontmatter and manifest schemas to:

`mechanics/proof-object/parts/eval-contracts/schemas/`

Add `mechanics/proof-object/PARTS.md`, `PROVENANCE.md`, and legacy index/log
surfaces so active parts come first and former root placement remains
traceable.

## Rationale

This keeps topology convex. Template and eval schemas are proof-object parts,
not parent mechanics and not generic root contracts.

The source bundles stay under `evals/`, and generated readers stay under
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

This decision does not move source proof bundles out of `evals/`.

It does not move generated catalog, capsule, section, or comparison readers out
of `generated/`.

It does not make the template proof evidence, maturity proof, or a source
bundle.

It does not make eval schemas stronger than bundle-local meaning.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.

## Current Applicability

As of 2026-05-24:

- Still valid: `eval-authoring` and `eval-contracts` remain support parts for
  source proof-object authoring and validation.
- Clarified: `mechanics/proof-object/parts/README.md` is the lower index and
  part-admission route for proof-object support operations.
- Source surfaces updated: `mechanics/proof-object/parts/README.md`,
  `scripts/validate_repo.py`, and `tests/test_validate_repo.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Review Log

### 2026-05-24 - Parts route lower index clarified

- Previous assumption: the lower parts README could state the source-bundle and
  generated-reader boundary in prose after listing active parts.
- New reality: the lower index is clearer as an operating card plus
  part-admission route: input, output, owner, next route, validation, source
  surface, operation, and owner boundary.
- Reason: source eval meaning stays with `evals/**/EVAL.md` and
  `evals/**/eval.yaml`; the parts index should route support work to the right
  part without becoming a second proof-object contract.
- Source surfaces updated: `mechanics/proof-object/parts/README.md`,
  `scripts/validate_repo.py`, and `tests/test_validate_repo.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.
