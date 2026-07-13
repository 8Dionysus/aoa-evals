# Mechanic Legacy Subvalidators

- Decision ID: AOA-EV-D-0186
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/mechanic_legacy_archive.py`, `scripts/validators/mechanic_provenance_bridge.py`, `scripts/validators/active_legacy_parent_wording.py`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology, mechanics/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0148 moved mechanic legacy/provenance checks out of
`scripts/validate_repo.py`, but `scripts/validators/mechanic_legacy.py` still
mixed four boundaries:

- archive skeleton, route language, and raw payload accounting;
- active-to-archive PROVENANCE bridge posture and single-bridge restrictions;
- active route wording for former legacy parent names; and
- shared constants, parent-derived file lists, and token lookup.

Those checks touch the same legacy pressure, but they do not share the same
source of truth or failure route.

## Decision

Mechanic legacy/provenance validation is split into focused modules:

- `scripts/validators/mechanic_legacy_archive.py` owns legacy archive skeleton
  coverage, archive route language, raw payload accounting, and the aggregate
  legacy surface check.
- `scripts/validators/mechanic_provenance_bridge.py` owns mechanic
  `PROVENANCE.md` bridge posture, provenance entry contracts, and the single
  controlled bridge restriction for active mechanic surfaces.
- `scripts/validators/active_legacy_parent_wording.py` owns active wording
  cleanup for former legacy parent names.
- `scripts/validators/mechanic_legacy_common.py` owns only shared constants,
  active-parent file lists, and token lookup helpers.

`scripts/validators/mechanic_legacy.py` is removed after callers and tests move
to the focused modules.

## Rationale

Legacy archive checks answer whether preserved records remain accountable and
routed to current active surfaces.

PROVENANCE bridge checks answer whether active surfaces reach archive detail
through a single controlled bridge instead of direct archive-internal links.

Active wording checks answer whether old parent names leak back into current
route language.

Keeping those checks in one module would preserve a broad historical bucket and
make future validator growth ambiguous.

## Consequences

- Positive: archive, bridge, and active-wording failures now point to their
  owning source surfaces.
- Positive: the shared helper has no validation authority.
- Positive: `mechanic_legacy.py` is removed instead of becoming another
  compatibility facade.
- Tradeoff: the aggregate legacy archive validator still delegates to the
  provenance bridge validator so existing repo-wide legacy checks keep one
  source-fast route.

## Current Applicability

As of 2026-06-04:

- Still valid: active mechanic surfaces must route legacy archive detail
  through `PROVENANCE.md`, and archive-local legacy records must map raw
  payloads back to current active routes.
- Changed: legacy archive checks moved into `mechanic_legacy_archive.py`;
  provenance bridge checks moved into `mechanic_provenance_bridge.py`; active
  wording checks moved into `active_legacy_parent_wording.py`; shared helpers
  moved into `mechanic_legacy_common.py`.
- Supersedes: the single-module owner shape described by AOA-EV-D-0148.

## Review Log

### 2026-06-16 - Targeted negative archive route wording

- Previous assumption: exact stale-route phrases were enough to keep archive
  records from becoming negative active-route scaffold.
- New reality: archive route files must also reject targeted lowercase and
  modal negative wording such as `do not use`, `should not use`, `should not be
  used`, and `not the current route`, while preserving neutral forms such as
  `not exhaustive`.
- Reason: these phrases still tell the reader what not to do instead of naming
  the current active route expectation.
- Source surfaces updated: `scripts/validators/mechanic_legacy_archive.py` and
  `tests/test_mechanic_legacy_archive_routes.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Boundaries

This decision does not let legacy validators define mechanic payload meaning.

It does not make generated projection parity, release packaging, runtime
policy, trace/eval grading, sibling truth, or security/adversarial checks part
of source-fast legacy validation.

It does not let `mechanic_legacy_common.py` own validation semantics.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
