# Root Legacy Layer Split

- Decision ID: AOA-EV-D-0213
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused root legacy naming, bridge-residue, and external-leakage validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: cross-parent
- Guard families: source/topology, observability/audit
- Posture: active rationale

## Context

AOA-EV-D-0171 moved root legacy naming checks out of the root-authority
aggregate into `scripts/validators/root_legacy.py`. That file still mixed
several different repair routes:

- the `docs/architecture/LEGACY_NAMING.md` posture guide and legacy naming
  decisions;
- direct legacy-index and second-bridge residue across root route-card and
  decision surfaces;
- archive-detail and archive-accounting leakage in root-visible surfaces; and
- stale movement, deletion, or retirement route wording.

Those are all legacy-route protections, but they are not one owner surface.

## Options Considered

- Keep `root_legacy.py` as the broad legacy naming validator.
- Keep `root_legacy.py` as a delegating compatibility facade.
- Remove the aggregate and let `root_topology.py` call focused root legacy
  validators directly.

## Decision

`scripts/validators/root_legacy.py` is removed.

Active root legacy validation now routes through:

- `root_legacy_naming.py` for the legacy naming posture guide, naming
  decisions, decision-index references, README/proof-topology/roadmap/changelog
  route tokens, and concrete legacy-inventory wording.
- `root_legacy_bridge_residue.py` for direct mechanic legacy-index references,
  second active-bridge wording, and root route-card or decision residue where
  legacy routing crosses through an archive index instead of only
  `PROVENANCE.md`.
- `root_legacy_external_leakage.py` for archive-detail leakage, archive-local
  accounting leakage, and movement/deletion/retirement wording across
  root-visible, decision, route-card, and active mechanic surfaces.
- `root_legacy_common.py` for helper-only constants and token lookup.

`root_topology.py` calls the focused validators directly. Tests collect the
three hard validators explicitly instead of importing a facade.

## Rationale

Legacy naming posture is not the same failure as archive-detail leakage. A
missing posture token belongs in the legacy naming guide or decision record.
A direct archive-index route belongs to bridge-residue cleanup. A stale
retirement phrase belongs to the external surface that leaked movement policy.

Splitting these validators keeps root legacy checks as route guards rather than
a broad historical container.

## Consequences

- Positive: legacy guide, bridge residue, and external leakage failures now
  route to the exact owner surface.
- Positive: root topology orchestration remains the single source/topology
  entrypoint without owning root legacy semantics.
- Positive: `root_legacy_common.py` is helper-only and cannot become a hidden
  compatibility facade.
- Tradeoff: root surface tests and root topology orchestration import more
  focused modules.

## Current Applicability

As of 2026-06-04:

- Still valid: legacy naming must route through active owners and the single
  provenance bridge before archive-internal details appear.
- Changed: the broad `root_legacy.py` module no longer exists.
- Supersedes: AOA-EV-D-0171 for aggregate root-legacy validator shape.

## Boundaries

This decision does not make root legacy validators the owner of mechanic
archive payload accounting, mechanic history, generated parity, runtime
outcomes, source-eval meaning, release state, or physical movement/deletion
policy.

It checks root-visible legacy naming posture and route wording only.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
