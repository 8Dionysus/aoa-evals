# 0010 Proof Object Mechanic Package

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/proof-object/`

## Index Metadata

- Surface classes: mechanic package
- Mechanic parents: proof-object
- Guard families: none
- Posture: active rationale

## Context

Decision `0002` established the source proof object as the authority for one
bounded eval claim. Since then, `aoa-evals` has added a proof topology map,
mechanics atlas, audit package, boundary-bridge package, and
legacy naming map.

The source proof object is now the recurring operation that all those surfaces
return to: runtime candidates need bundle-local review, sibling refs need a
local proof object, generated readers derive from bundles, receipts stay below
reports, and quest obligations often ask whether a new or changed proof object
is needed.

## Options Considered

- Keep `proof-object` as a candidate family until after more file movement.
- Create a package only when `evals/` is reorganized.
- Create `mechanics/proof-object/` now as a route package, while keeping
  `evals/` in place.

## Decision

Create `mechanics/proof-object/` as the package for the operation:

`origin proof pressure -> source proof bundle -> proof-object completeness review -> generated reader derivation -> bundle-local report or downstream route`

The package routes existing source surfaces:

- `evals/**/EVAL.md`
- `evals/**/eval.yaml`
- `mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md`
- architecture, philosophy, rubric, review, score, verdict, blind spot,
  portability, and comparison guides
- generated catalog, capsule, and section readers

It does not move `evals/`.

## Rationale

This makes the central proof atom convex before more package movement happens.
A future agent can now find the route for bundle lifecycle, source/manifest
alignment, status posture, blind spots, comparison posture, generated
derivation, and bundle-local review without treating generated readers or
runtime evidence as stronger truth.

## Consequences

- Positive: proof-object completeness now has a mechanics route and
  validator-backed discovery surface.
- Tradeoff: the package routes source bundles without owning their directory.
  That split must stay explicit so `mechanics/` does not become proof canon.
- Follow-up: later validators can constrain proof-object completeness more
  directly, especially status movement, evidence posture, comparison contracts,
  and generated-source derivation.

## Boundaries

This decision does not move, rename, promote, deprecate, or rewrite any eval
bundle.

It does not make `mechanics/proof-object/` stronger than `evals/**/EVAL.md`
and `evals/**/eval.yaml`.

It does not make generated readers, runtime candidates, receipts, reports, or
sibling references verdict authority.

It does not authorize one proof object as a universal agent ranking.

## Validation

- `mechanics/proof-object/README.md` names the owned operation, source
  surfaces, inputs, outputs, stronger-owner split, boundaries, lifecycle
  posture, validation, and next route.
- `mechanics/proof-object/AGENTS.md` names local editing law.
- `mechanics/README.md`, `docs/architecture/PROOF_TOPOLOGY.md`, `README.md`,
  `docs/README.md`, `ROADMAP.md`, `CHANGELOG.md`,
  `docs/architecture/LEGACY_NAMING.md`, and `docs/decisions/README.md` route to the
  package.
- `python scripts/validate_repo.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_semantic_agents.py`
