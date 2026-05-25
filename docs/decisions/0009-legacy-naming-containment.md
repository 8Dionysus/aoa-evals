# 0009 Legacy Naming Containment

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `docs/architecture/LEGACY_NAMING.md`

## Index Metadata

- Surface classes: legacy/provenance
- Mechanic parents: none
- Guard families: legacy and provenance
- Posture: legacy/provenance rationale

## Context

The proof topology and the first live mechanic packages made old names more
dangerous if they remained only as habit. Some names are historical, some are
still accepted by schemas, examples, generated readers, tests, or source docs,
and some are current active route names.

Without a naming posture guide, future refactors could either erase provenance
too early or let legacy vocabulary steer active topology.

## Decision

Create `docs/architecture/LEGACY_NAMING.md` as the repo-level posture guide for old and
overloaded-name classes.

The guide names posture vocabulary:

- `active`
- `historical`
- `accepted-input`
- `generated-projection`
- `candidate-only`
- `provenance-bridge`

It does not own archive details. When old placement or source lineage matters,
the route is:

`active route -> PROVENANCE.md -> owning legacy archive`

Package-local legacy details stay inside the owning `legacy/` archive.
Concrete old-name inventories and wrong-parent mappings stay out of this guide;
active topology surfaces own those checks.

## Rationale

This preserves convex topology: old names remain visible, but their authority
class is named before they influence a refactor.

It also avoids a false cleanup move. Renaming source-compatible names before
validators and generated projections can follow would erase useful proof
lineage and create hidden compatibility drift.

## Consequences

- Positive: future agents can tell whether a name is active topology,
  historical lineage, accepted-input, generated-projection, candidate-only, or
  provenance-bridge vocabulary.
- Tradeoff: one more repo-level guide exists, but it must stay thin and cannot
  become an archive map.
- Follow-up: as packages mature, keep archive detail inside package-local
  `legacy/` surfaces.

## Boundaries

This decision does not rename, delete, or move old names by itself.

It does not make generated projections authoritative.

It does not authorize editing sibling repositories or treating runtime evidence
as proof canon.

It does not authorize starting new work from legacy directories.

It does not authorize copying archive details into root guidance.

## Validation

- `docs/architecture/LEGACY_NAMING.md` names posture vocabulary, current-route discipline,
  and boundary rules.
- package-local legacy route cards point back to `../PROVENANCE.md`.
- `README.md`, `docs/README.md`, `DESIGN.md`, `docs/architecture/PROOF_TOPOLOGY.md`,
  `ROADMAP.md`, `CHANGELOG.md`, and `docs/decisions/README.md` route to the
  guide.
- `python scripts/validate_repo.py`
