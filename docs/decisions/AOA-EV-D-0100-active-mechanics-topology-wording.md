# Active Mechanics Topology Wording

- Decision ID: AOA-EV-D-0100
- Status: Accepted
- Date: 2026-05-21
- Owner surface: `DESIGN.md`, `DESIGN.AGENTS.md`, `docs/architecture/PROOF_TOPOLOGY.md`, `ROADMAP.md`, `docs/decisions/AOA-EV-D-0005-proof-topology-map.md`

## Index Metadata

- Original date: 2026-05-21
- Surface classes: root/topology
- Mechanic parents: cross-parent
- Guard families: none
- Posture: active rationale

## Context

The mechanics refactor made `mechanics/` an active operation atlas, but several
source-of-truth surfaces still used preparatory language such as future
packages, readiness-only operation labels, and pre-movement topology mapping.

That wording is dangerous after the movement has happened. It can make an
active mechanic look provisional, invite new work to start from old route
vocabulary, and let legacy feel like a second active map instead of a
package-local archive behind `PROVENANCE.md`.

## Options Considered

- Leave the old wording as historical texture:
  this preserves chronology but keeps the wrong route visible to future agents.
- Move the explanation into legacy:
  this would put active topology authority inside the archive and invert the
  intended route.
- Update active source-of-truth surfaces and validate against stale
  preparatory wording:
  this keeps the current topology active-first while leaving archive details
  inside legacy.

## Decision

Active design and topology surfaces describe active mechanics.

`DESIGN.AGENTS.md` says active mechanic packages carry route cards and that new
parents require evidence, decisions, and validators. `docs/architecture/PROOF_TOPOLOGY.md`
names mechanic operations as an active authority class and treats further file
movement as additional movement after the mechanics refactor, not as a future
Phase 4 precondition. `DESIGN.md` names active mechanic authority classes.
`ROADMAP.md` and the proof-topology decision use the same current route.

Validators reject stale preparatory wording in these source-of-truth surfaces.

## Rationale

The current route must be readable without mentally replaying the refactor.
Active topology should point to current mechanics, current parts, current
validators, and the single `PROVENANCE.md` bridge when old lineage is needed.

Legacy details belong inside the owning `legacy/` archive. The active side may
state the bridge and the stop-line, but it must not keep enough archive detail
to make legacy behave like an active route.

## Consequences

- Positive: future agents see mechanics as active operation packages, not as
  speculative package candidates.
- Tradeoff: historical preparatory phrasing is no longer available in root
  source-of-truth prose; decision history preserves why it changed.
- Follow-up: if another source-of-truth surface reintroduces future-package or
  readiness-only wording, extend the same validator guard there.

## Current Applicability

As of 2026-05-24:

- Still valid: active roadmap wording should describe current direction and
  owner routes rather than replaying preparatory mechanics posture.
- Changed: `ROADMAP.md` now routes agent-index, proof-loop, and direction-anchor
  details through their owner surfaces instead of carrying ledger-style guard
  phrasing.
- Source surfaces updated: `ROADMAP.md`, `scripts/validate_repo.py`, and
  `tests/test_validate_repo.py`.
- Validation: `python -m pytest -q tests/test_validate_repo.py -k roadmap`.
- Superseded by: none.

## Review Log

### 2026-05-24 - Roadmap direction route language clarified

- Previous assumption: roadmap direction could preserve boundaries with compact
  negative phrases when adjacent owner surfaces were linked nearby.
- New reality: the roadmap is easier for low-context agents when each boundary
  points to the active owner: `docs/architecture/AGENT_INDEX.md`, bundle-local review,
  changelog, or validator ledger.
- Reason: roadmap should set direction and horizon order, while indices,
  changelog, validators, and proof bundles carry their own detail.
- Source surfaces updated: `ROADMAP.md`, `scripts/validate_repo.py`, and
  `tests/test_validate_repo.py`.
- Validation: `python -m pytest -q tests/test_validate_repo.py -k roadmap`.

## Boundaries

This does not authorize adding new parent mechanics by naming them active.
New parents still require `mechanics/EVIDENCE_CLUSTERS.md`, route cards,
decisions, owner split, parts, and validation.

This does not move legacy archive details into active design surfaces. Active
surfaces may name the `PROVENANCE.md` bridge and the rule that archive details
stay inside legacy.

## Validation

- `python -m pytest -q tests/test_root_surface_roles.py -k 'root_design or design_agents or proof_topology'`
- `python scripts/validate_repo.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_semantic_agents.py`
- `python -m pytest -q tests/test_validate_repo.py`
- `python scripts/release_check.py`
