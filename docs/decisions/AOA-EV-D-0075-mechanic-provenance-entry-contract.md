# Mechanic Provenance Entry Contract

- Decision ID: AOA-EV-D-0075
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/*/PROVENANCE.md`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: legacy/provenance
- Mechanic parents: cross-parent
- Guard families: legacy and provenance
- Posture: legacy/provenance rationale

## Context

The mechanics refactor made every active parent expose a legacy/provenance
skeleton. File presence alone is not enough: if `PROVENANCE.md` starts carrying
archive details, it becomes a second archive map outside the archive.

## Decision

Every active `mechanics/<parent>/PROVENANCE.md` must name the active route first
and then bridge only to `legacy/README.md`.

The legacy archive owns its own details. `PROVENANCE.md` must not copy archive
details and is not active topology.

`scripts/validate_repo.py` enforces this across the active mechanic parent
allowlist.

## Rationale

This matches the AoA-style legacy posture for `aoa-evals`: active mechanics own
the living route, `PROVENANCE.md` is the single crossing point, and detailed
legacy accounting stays in the owning `legacy/` archive.

## Consequences

- Positive: every mechanic gives the same first-hop route from active work into
  legacy without duplicating archive detail.
- Positive: future agents cannot use `PROVENANCE.md` as a quiet replacement for
  archive-local maps.
- Tradeoff: archive detail requires one more click into the archive, which is
  intentional.

## Boundaries

This decision does not delete legacy, weaken archive accounting, or make raw
lineage less important. It only keeps archive details out of active-side bridge
surfaces.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
