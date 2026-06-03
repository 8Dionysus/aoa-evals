# Mechanic Legacy Archive Boundary

- Decision ID: AOA-EV-D-0071

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: legacy/provenance
- Mechanic parents: cross-parent
- Guard families: legacy and provenance, sibling and boundary
- Posture: legacy/provenance rationale

## Context

The mechanics refactor now uses active parent packages with part-local
contracts and provenance bridges. The goal requires legacy to follow the AoA
model: lineage behind an active mechanic, not an active contract, trash
directory, cleanup timebox table, or place to start new work.
Legacy is not a new-work entrypoint.

Most active parents already expose the intended surfaces, but the invariant
needs repo-wide validation. Otherwise future mechanics can keep a parent
allowlist and part contract while silently losing the archive boundary that
keeps old paths and raw lineage subordinate to the active route.

## Decision

Every active mechanic parent must expose `PROVENANCE.md` and a package-local
legacy archive opened through `legacy/README.md`.

`PROVENANCE.md` bridges active route to the archive entrypoint only. It must
not carry archive-local route details. The legacy archive owns its own route
card, index, accounting log, raw-lineage boundary, and lookup instructions.

Each legacy README must route readers through `../PROVENANCE.md` before local
legacy lookup, then describe the archive-local route. It must state that legacy
is not active topology or a new-work entrypoint.

When a mechanic keeps a raw payload inside the legacy archive, that payload
must be referenced by the archive-local index or accounting log. Unindexed raw
payloads are not provenance; unindexed raw payloads are forgotten residue.
The archive-local index must also map that raw payload to a current active route.
For ordinary raw payloads this means a current active part route; for
package-wide raw sources this means both package `DIRECTION.md` and `PARTS.md`.
A parent-only route or raw-only archive route lets the archive account for
itself without returning to the active mechanic contract.

## Consequences

- Future parent mechanics cannot become active without route cards, part
  contracts, an active-side provenance bridge, and a package-local legacy
  archive boundary.
- Legacy remains weaker than active README/PARTS/parts/validation surfaces.
- Old names and paths remain traceable without becoming active topology.
- Empty or no-payload raw districts remain archive-local boundaries, not
  garbage folders.
- Every legacy README carries the same active-first entry contract.
- Raw legacy payloads cannot sit behind an active mechanic without an index or
  accounting-log reference.
- A raw legacy payload cannot satisfy the archive contract by pointing only to
  a raw-only archive route or parent-only route; it needs a current active part
  route, or package `DIRECTION.md` plus `PARTS.md`, in the archive index.

## Current Applicability

As of 2026-05-24:

- Still valid: each active mechanic parent exposes `PROVENANCE.md` and an
  archive-local legacy entry with `INDEX.md`, `DISTILLATION_LOG.md`, and
  raw-lineage entry.
- Changed: active legacy README route cards now express the entry as an
  archive-local route that returns historical sources to the current active
  route.
- Changed: archive indexes, distillation logs, and raw README route files now
  carry current-route expectations and validation through the nearest legacy `AGENTS.md`.
- Superseded by: no new decision; this is a route-language amendment of the
  same archive boundary.

## Review Log

### 2026-05-24 - Archive README wording made route-positive

- Previous assumption: legacy README cards carried the boundary through
  negative active-topology and new-work-entrypoint tokens.
- New reality: legacy README cards name the archive-local route, current active
  route return path, and archive-local accounting surfaces.
- Reason: low-context agents should see where an old path enters, what the
  archive owns, and which active route receives current work.
- Source surfaces updated: `mechanics/*/legacy/README.md`,
  `scripts/validate_repo.py`, `tests/test_mechanic_parent_topology.py`, and
  `tests/test_mechanic_legacy_archive_routes.py`.
- Validation: `python -m pytest -q tests/test_mechanic_parent_topology.py -k
  mechanic_legacy_skeleton`; `python scripts/validate_repo.py`.

### 2026-05-24 - Archive route files hand validation to AGENTS

- Previous assumption: archive-local `INDEX.md` and `DISTILLATION_LOG.md`
  files could carry command blocks and negative stop-line phrasing.
- New reality: archive-local route files describe role, lineage, current active
  route expectations, and validation pointer; executable commands live in the
  nearest legacy `AGENTS.md`.
- Reason: a low-context agent should read the archive map as topology and then
  follow the route card for tools, instead of treating every archive note as a
  command surface.
- Source surfaces updated: archive-local indexes, distillation logs, raw README
  route files, `scripts/validate_repo.py`, and `tests/test_validate_repo.py`.
- Validation: `python -m pytest -q tests/test_validate_repo.py -k
  mechanic_legacy`; `python scripts/validate_repo.py`;
  `python scripts/validate_semantic_agents.py`.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_mechanic_parent_topology.py -k mechanic_legacy_skeleton
python -m pytest -q tests/test_mechanic_legacy_archive_routes.py -k mechanic_legacy_raw_payload
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python -m pytest -q
```
