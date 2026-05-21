# Mechanic Part README Contract

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/`, `scripts/validate_repo.py`

## Context

The mechanics refactor moved real proof operations out of root districts into
active parent packages and concrete parts. Parent-level allowlists and
part-specific guards are not enough by themselves: a future part could appear
under `mechanics/<parent>/parts/<part>/README.md` without being routed by the
parent `PARTS.md`, or without the same input/output/boundary contract that keeps
parts from becoming accidental parent mechanics.

## Options Considered

- Keep only named part validators: this protects current known parts but lets a
  new part directory bypass the contract until someone remembers to add a
  bespoke guard.
- Require exact full README paths in every parent `PARTS.md`: this is strong but
  too noisy for parent maps that already route parts by exact slug.
- Add a generic concrete-part guard: every active part README must expose the
  common contract headings, and parent `PARTS.md` must route the part by README
  path or exact part slug.

## Decision

`scripts/validate_repo.py` validates every concrete active part README under
`mechanics/<parent>/parts/<part>/README.md`.

Each part README must contain:

- `## Source Surfaces`
- `## Inputs`
- `## Outputs`
- `## Stronger Owner Split`
- `## Stop-Lines`
- `## Validation`

The same guard also rejects an orphan part by requiring the parent `PARTS.md` to
route each concrete part by README path or exact backticked part slug.

## Rationale

This keeps the growth principle local and reusable: a parent mechanic can grow
new parts, but the new part must immediately state what it consumes, what it
names as source surfaces, what it consumes, what it emits, which stronger owner
keeps truth, where it stops, and how it is checked.
That is the minimal shape needed for future `agon`, `titan`, proof-loop, and
evals-native growth without recreating wrong parent forms.

## Consequences

- Positive: new parts cannot silently appear as unreviewed topology.
- Tradeoff: experimental part directories need a README contract before they can
  live under active mechanics.
- Follow-up: part-specific validators still add stronger local invariants where
  a part has schemas, generated artifacts, reports, or seed files.

## Boundaries

This decision does not say every part is equally mature, executable, or
proof-complete. It only defines the minimum active topology contract for a part.
It does not promote legacy raw files, generated readers, seeds, reports, or
fixtures into stronger authority than their mechanic README and owning source
surfaces.

## Validation

- `python -m pytest -q tests/test_validate_repo.py -k mechanic_part_readme_contract`
- `python scripts/validate_repo.py`
