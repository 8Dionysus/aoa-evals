# Mechanic Legacy Validator Boundary

- Decision ID: AOA-EV-D-0148
- Status: Accepted
- Date: 2026-06-04
- Owner surface: mechanic legacy/provenance boundary guard family

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

Mechanic legacy/provenance checks protect the active-to-archive bridge between
current mechanic route surfaces and preserved legacy archive records.

Before this split, `scripts/validate_repo.py` owned legacy skeleton files,
legacy archive route language, raw payload accounting, `PROVENANCE.md` bridge
posture, provenance entry contracts, single-bridge restrictions, and active
legacy parent wording. That made the root validator define archive posture
directly while also orchestrating unrelated source topology, generated parity,
mechanic parts, route residue, and release-adjacent guards.

## Decision

Mechanic legacy/provenance validation lives in
`scripts/validators/mechanic_legacy.py`.

The module owns:

- mechanic `PROVENANCE.md` active-to-archive bridge checks;
- legacy skeleton file coverage;
- legacy archive route language checks;
- legacy raw payload accounting checks;
- provenance entry and bridge-posture decision checks;
- mechanic legacy single-bridge checks;
- active legacy parent wording checks.

`scripts/validate_repo.py` delegates to the module through focused aggregate
calls. Tests for moved behavior import `validators/mechanic_legacy.py`
directly instead of using root compatibility wrappers.

## Rationale

Legacy/provenance validation is a boundary organ, not a pile of historical
script residue. It decides whether preserved archive detail remains routed
through `PROVENANCE.md` and `legacy/README.md` without becoming current
authority.

It does not define mechanic payload meaning, generated read-model parity,
release artifact freeze, runtime policy, trace/eval grading, or sibling truth.
Keeping this boundary focused prevents `scripts/validate_repo.py` from
accumulating another wave-specific gate family.

## Consequences

- Positive: `validate_repo.py` no longer exports mechanic legacy/provenance
  constants or wrappers.
- Positive: legacy bridge and archive tests now call the owning module
  directly.
- Positive: script, validator, and evidence-cluster inventories name
  legacy/provenance as a distinct source-fast boundary.
- Follow-up: remaining parent direction and parent guidance checks should split
  only when their owner boundary is equally coherent.

## Current Applicability

As of 2026-06-04:

- Still valid: active mechanic surfaces route archive detail through
  `PROVENANCE.md` and archive-local legacy entry surfaces.
- Changed: mechanic legacy/provenance checks moved from
  `scripts/validate_repo.py` to `scripts/validators/mechanic_legacy.py`.
- Superseded by: AOA-EV-D-0186 for the split into focused archive,
  provenance-bridge, active-wording, and helper modules.

## Review Log

### 2026-06-04 - Focused legacy/provenance split

- Previous assumption: one `mechanic_legacy.py` module could own skeleton,
  archive route language, raw payload accounting, PROVENANCE bridge posture,
  provenance entry checks, single-bridge restrictions, and active legacy parent
  wording.
- New reality: those are adjacent but distinct boundaries. Archive skeleton and
  raw accounting belong to `mechanic_legacy_archive.py`; active-to-archive
  bridge posture belongs to `mechanic_provenance_bridge.py`; former legacy
  parent wording belongs to `active_legacy_parent_wording.py`; shared constants
  and token lookup belong to `mechanic_legacy_common.py`.
- Reason: preserving a single broad validator would turn the legacy boundary
  into another historical bucket.
- Superseded by: AOA-EV-D-0186.

## Boundaries

This decision does not let generated validators define source meaning.

It does not turn legacy archive records into active mechanic payload authority.

It does not make `PROVENANCE.md` carry archive-internal detail; archive detail
stays in `legacy/`.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/mechanic_legacy_archive.py scripts/validators/mechanic_provenance_bridge.py scripts/validators/active_legacy_parent_wording.py scripts/validators/mechanic_legacy_common.py`
- `python -m pytest -q tests/test_mechanic_legacy_bridge.py tests/test_mechanic_legacy_archive_routes.py tests/test_mechanic_parent_topology.py tests/test_mechanic_parent_direction.py`
