# 0012 Proof Infra Mechanic Package

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/proof-infra/`

## Context

After the proof-object and comparison-spine packages, the remaining shared
support layer is visible but broad: fixtures, runners, scorers, schemas,
reports, templates, and generated catalog proof-artifact projections.

This should not become a junk drawer. The narrow live operation is shared proof
contract routing: a bundle needs reusable proof support, the shared surface
provides a public-safe reusable contract, bundle-local contracts bind that
support to one proof object, and generated catalog `proof_artifacts` expose the
route without becoming proof authority.

## Options Considered

- Leave proof infrastructure as top-level directories plus local AGENTS cards.
- Create one broad `proof-infra` package that owns all supporting directories.
- Create `mechanics/proof-infra/` as a route package for shared proof contract
  operation while leaving all existing directories in place.

## Decision

Create `mechanics/proof-infra/` for the operation:

`bundle proof need -> shared proof contract -> bundle-local contract -> generated proof_artifacts -> bounded review`

The package routes shared fixture families, runner surfaces, scorer helpers,
schemas, report dossiers, templates, and generated proof-artifact entries.

It does not move `fixtures/`, `runners/`, `scorers/`, `schemas/`, `reports/`,
or `templates/`.

## Rationale

Shared infrastructure is useful only if it reduces repeated contract plumbing
without hiding bundle-local meaning. A package route makes that split explicit:
shared surfaces support review, but the proof object remains stronger.

This also gives future agents a place to reason about generated catalog
`proof_artifacts` without hand-editing generated readers or weakening schemas
to make a report pass.

## Consequences

- Positive: shared proof contract work now has a package route and
  validator-backed discovery surface.
- Tradeoff: the package is intentionally a route layer, not a directory move.
  Future maintainers must keep the existing local AGENTS cards authoritative
  for their exact directories.
- Follow-up: later validators can tighten shared fixture, runner, scorer,
  schema, report, and generated proof-artifact invariants where real drift
  appears.

## Boundaries

This decision does not move shared infrastructure directories.

It does not make shared fixtures, runners, scorers, schemas, reports,
templates, or generated proof_artifacts stronger than bundle-local `EVAL.md`
and `eval.yaml`.

It does not authorize schema weakening, repo-global scoring, promotion by
shared infrastructure, generated-reader authority, or report-shape
monoculture.

## Validation

- `mechanics/proof-infra/README.md` names the owned operation, source surfaces,
  inputs, outputs, stronger-owner split, boundaries, validation, and next
  route.
- `mechanics/proof-infra/AGENTS.md` names local editing law.
- `mechanics/README.md`, `docs/PROOF_TOPOLOGY.md`, `README.md`,
  `docs/README.md`, `ROADMAP.md`, `CHANGELOG.md`, and
  `docs/decisions/README.md` route to the package.
- `python scripts/validate_repo.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_semantic_agents.py`
