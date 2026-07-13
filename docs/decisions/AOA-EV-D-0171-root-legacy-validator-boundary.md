# Root Legacy Validator Boundary

- Decision ID: AOA-EV-D-0171
- Status: Superseded
- Superseded by: AOA-EV-D-0213-root-legacy-layer-split
- Date: 2026-06-04
- Owner surface: `scripts/validators/root_legacy.py`, `docs/architecture/LEGACY_NAMING.md`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: cross-parent
- Guard families: source/topology, observability/audit
- Posture: superseded rationale

## Context

`scripts/validators/root_authority.py` still carried legacy naming posture,
single provenance bridge checks, external archive-detail leakage checks, and
no-movement/no-retirement wording checks across root guidance, decisions,
route-card-only districts, and active mechanics.

Those checks protect a different boundary from root design/proof topology:
legacy names must route through active owner surfaces and a single
`PROVENANCE.md` bridge before archive-internal details appear.

## Decision

Root legacy naming validation lives in `scripts/validators/root_legacy.py`.

The module owns:

- `docs/architecture/LEGACY_NAMING.md` posture guide token checks;
- legacy naming containment and single-bridge decision checks;
- direct mechanic legacy index and second-active-bridge residue checks;
- archive-internal detail leakage checks across external root/decision surfaces;
- archive-local accounting wording containment; and
- stale movement, deletion, or retirement route wording checks.

`root_topology.py` calls `root_legacy.py` directly. The former
`root_authority.py` compatibility aggregate is removed by AOA-EV-D-0196.

## Rationale

Legacy naming is a route/posture guard, not a root design thesis and not a
mechanic archive payload owner. Keeping it inside `root_authority.py` made the
root authority validator carry root design, proof topology, agent lanes, audit,
index roles, decision status, memory posture, and legacy archive route policy at
once.

The split keeps legacy route law visible while preventing root authority from
becoming the place where every historical surface accumulates.

## Consequences

- Positive: legacy naming posture has its own validator, inventory entry,
  mechanics ledger row, and decision rationale.
- Positive: the legacy validator no longer routes through the root authority
  aggregate.
- Historical note: this split originally kept compatibility aliases in
  `root_authority.py`; AOA-EV-D-0196 removes that aggregate.
- Tradeoff: the legacy validator still scans broad external surfaces because
  archive-detail leakage is a cross-root wording failure.

## Current Applicability

As of 2026-06-04:

- Still valid: legacy naming must route through active owners and the single
  provenance bridge before archive-internal details appear.
- Changed: legacy naming posture, archive-detail leakage, and
  movement/deletion/retirement wording checks moved out of
  `root_authority.py` and into `root_legacy.py`; AOA-EV-D-0196 later removes the
  remaining root authority aggregate; active validation later split across
  `root_legacy_naming.py`, `root_legacy_bridge_residue.py`,
  `root_legacy_external_leakage.py`, and helper-only `root_legacy_common.py`.
- Superseded by: AOA-EV-D-0196 for no-aggregate routing.
- Superseded by: AOA-EV-D-0213 for the aggregate root-legacy validator shape.

## Boundaries

This decision does not make `root_legacy.py` the owner of mechanic archive
payload accounting, mechanic history, generated parity, runtime outcomes,
source-eval meaning, release state, or physical movement/deletion policy.

It only checks root-visible legacy naming posture and route wording.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
