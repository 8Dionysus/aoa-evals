# Mechanic Provenance Bridge Posture

- Decision ID: AOA-EV-D-0090

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: legacy/provenance, boundary/runtime/sibling
- Mechanic parents: cross-parent
- Guard families: legacy and provenance, sibling and boundary
- Posture: legacy/provenance rationale

## Context

`PROVENANCE.md` is the only active-side bridge from a mechanic parent into its
legacy archive. It is not the current operating route for the mechanic, and it
is not the archive inventory.

Without an explicit bridge posture, a future edit can accidentally put archive
detail in the bridge itself. That would create a second working route beside
the active parent, direction, part map, and archive-local accounting.

## Decision

Every active mechanic `PROVENANCE.md` must state:

- `PROVENANCE.md` is a bridge, not an active route.
- Use active surfaces first:
- `DIRECTION.md` is part of the active route before legacy lookup.
- The bridge opens `legacy/README.md`.
- The legacy archive owns its own details.

Validator coverage:

```bash
python -m pytest -q tests/test_validate_repo.py -k mechanic_provenance_bridge_posture
```

## Consequences

Active mechanic work starts from `README.md`, `DIRECTION.md`, `PARTS.md`, and
`parts/`. `PROVENANCE.md` opens the archive only after those active surfaces are
insufficient.

This keeps legacy important but archival: one bridge from active mechanics, and
then detailed accounting inside legacy.

## Current Applicability

As of 2026-05-24:

- Still valid: `PROVENANCE.md` is the only first-hop route from active mechanic
  surfaces into the owning legacy archive.
- Changed: active route surfaces now express the contract as an
  active-to-archive bridge with route, owner, and next-step wording.
- Superseded by: no new decision; this is a route-language amendment of the
  same bridge posture.

## Review Log

### 2026-05-24 - Active bridge wording made positive

- Previous assumption: active surfaces and validators carried the sentence
  "`PROVENANCE.md` is a bridge, not an active route."
- New reality: active surfaces use active-to-archive bridge wording, keep
  "Use active surfaces first", and route archive details to the owning legacy
  archive.
- Reason: live route surfaces should give low-context agents a route, owner,
  and next step.
- Source surfaces updated: `mechanics/*/PROVENANCE.md`,
  `mechanics/README.md`, `docs/architecture/PROOF_TOPOLOGY.md`,
  `docs/architecture/LEGACY_NAMING.md`, `DESIGN.md`, `scripts/validate_repo.py`, and
  `tests/test_validate_repo.py`.
- Validation: `python -m pytest -q tests/test_validate_repo.py -k
  mechanic_provenance_bridge_posture`; `python scripts/validate_repo.py`.
