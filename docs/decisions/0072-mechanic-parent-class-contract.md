# 0072 Mechanic Parent Class Contract

## Status

Accepted.

## Index Metadata

- Surface classes: proof topology
- Mechanic parents: cross-parent
- Guard families: parent and package
- Posture: active rationale

## Context

The mechanics atlas now has an allowlisted active parent set. The goal also
requires those parents to remain divided into two classes:

- AoA-aligned mechanics, where the proof-side parent keeps the named AoA
  mechanic form;
- evals-native mechanics, where the parent belongs to the local proof organ
  operation itself.

One evals-native parent may still be owner-named when the local operation is
real and the stronger-owner split is explicit. `titan` is that case: the
parent name follows the Titan role/bearer subject, while `aoa-evals` owns only
the seed-boundary proof operation and `aoa-agents` keeps Titan role, bearer, summon, and incarnation law.

The allowlist alone can reject unknown directories, but it cannot by itself
catch a future edit that moves a parent into the wrong class or lets an old
proof-suffix, canary-form, evidence-class, or stage-pressure name regain
topology authority.

## Decision

`mechanics/EVIDENCE_CLUSTERS.md` is the source class map. The validator must
check that:

- every AoA-aligned parent appears in the AoA-aligned table;
- every evals-native parent appears in the evals-native table;
- owner-named evals-native parents state the stronger owner split before they
  can be read as local proof-organ doctrine;
- the two class sets are disjoint and cover the active parent allowlist;
- former wrong parent forms stay documented as wrong forms, not active parents.

Current former wrong parent forms include `agon-proof`, `titan-canaries`,
`proof-release`, `runtime-evidence`, `sibling-proof-refs`, and `repair`.

## Consequences

- A future parent-class change must update the evidence map, validator
  constants, route cards, topology docs, and decisions in one slice.
- Proof-side specificity stays in operations, parts, and contracts instead of
  proof-suffix parent names.
- Owner-named evals-native specificity stays in the local operation and owner
  split instead of transferring stronger-owner authority into `aoa-evals`.
- Artifact forms such as canaries, receipts, generated readers, schemas,
  reports, and repair pressure remain parts or deferred pressure unless a real
  cross-root operation proves parent status.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_validate_repo.py -k mechanic_parent_class
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python -m pytest -q
```
