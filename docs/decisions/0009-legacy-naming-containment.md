# 0009 Legacy Naming Containment

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `docs/LEGACY_NAMING.md`

## Context

The proof topology and the first live mechanic packages are now present.
That makes old names more dangerous if they remain only as habit: `Agon`,
`wave`, `phase-alpha`, `runtime-candidate`, `artifact-to-verdict`,
`bundle-family`, `Titan canary`, `Spark`, and top-level quest paths all carry
real lineage or compatibility pressure.

Some of those names are still accepted by schemas, examples, generated readers,
tests, or source docs. Others are historical route markers. Without a naming
map, future refactors could either erase provenance too early or let legacy
vocabulary steer active topology.

## Options Considered

- Rename old surfaces immediately into current package names.
- Leave naming posture implicit inside each future mechanic package.
- Create a repo-level legacy naming map now, before physical movement or
  retirement.

## Decision

Create `docs/LEGACY_NAMING.md` as the repo-level active topology and
accepted-input map for legacy names.

The map uses explicit postures:

- `active`
- `historical`
- `accepted-input`
- `generated-projection`
- `candidate-only`
- `retire-after`

It routes old names to current active surfaces such as
`mechanics/runtime-evidence/`, `mechanics/sibling-proof-refs/`,
`mechanics/questbook/`, `docs/TRACE_EVAL_BRIDGE.md`, and
`docs/TITAN_INCARNATION_CANARIES.md`.

## Rationale

This preserves convex topology: old names remain visible, but their authority
class is named before they influence a refactor.

It also avoids a false cleanup move. Renaming Agon, wave, phase-alpha,
runtime-candidate, Spark, or source quest paths before validators and generated
projections can follow would erase useful proof lineage and create hidden
compatibility drift.

## Consequences

- Positive: future agents can tell whether a name is active topology,
  historical lineage, accepted-input, generated-projection, candidate-only, or
  marked for later retirement.
- Tradeoff: one more repo-level map exists before package-local `legacy/`
  ledgers. This is intentional until each package owns a real operation.
- Follow-up: future package moves should either reference this map or move the
  relevant portion into package-local legacy surfaces with validator coverage.

## Boundaries

This decision does not rename, delete, or move Agon, wave, phase-alpha,
runtime-candidate, artifact-to-verdict, bundle-family, Titan canary, Spark, or
quest source paths.

It does not make generated projections authoritative.

It does not authorize editing sibling repositories or treating runtime evidence
as proof canon.

It does not create an `agon-proof`, `titan-canaries`, or `proof-object` package
before those packages have live operation pressure and validation.

## Validation

- `docs/LEGACY_NAMING.md` names posture vocabulary, current routes, movement
  rules, and package relationships.
- `README.md`, `docs/README.md`, `DESIGN.md`, `docs/PROOF_TOPOLOGY.md`,
  `ROADMAP.md`, `CHANGELOG.md`, and `docs/decisions/README.md` route to the
  map.
- `python scripts/validate_repo.py`
