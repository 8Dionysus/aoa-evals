# Mechanic Evidence Dimension Ledger

- Decision ID: AOA-EV-D-0083
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/EVIDENCE_CLUSTERS.md`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: root/topology
- Mechanic parents: cross-parent
- Guard families: parent and package
- Posture: active rationale

## Context

The mechanics atlas already has an allowlist and a class split between
AoA-aligned and evals-native parent mechanics. That protects against invented
parent names, but it is still possible for the evidence map to become too
coarse: a parent row could name a broad cluster without showing the dimensions
that made the cluster legitimate.

The long refactor goal requires mechanics to come from real cross-root
evidence: meaning or doctrine, proof pressure, contracts or payloads,
builders/readouts, quest or deferred pressure, owner split, stop-lines, and
legacy or provenance routing.

## Options Considered

- Keep the evidence standard as prose only.
- Expand every parent README instead of strengthening the evidence map.
- Add a dimension ledger inside `mechanics/EVIDENCE_CLUSTERS.md` and validate
  that every active parent appears in it.

## Decision

`mechanics/EVIDENCE_CLUSTERS.md` owns an Active Parent Evidence Dimension Ledger.

Every active parent must have one row in that ledger. The row must classify the
parent and name the evidence dimensions that justify the parent:
meaning/doctrine, proof pressure, contracts/payloads, builders/readouts,
quest/deferred pressure, owner split and stop-lines, and legacy/provenance.
For owner-named evals-native parents such as `titan`, the row must also make
clear that `aoa-evals` owns the local proof operation while the stronger owner
keeps role, bearer, runtime, memory, or activation truth.

## Rationale

The ledger makes the parent map more than a name allowlist. It gives future
agents a compact proof of why the parent exists and what kind of evidence keeps
it honest. This is especially important for names that could otherwise slide
back into artifact-form parents such as `agon-proof`, `titan-canaries`,
`proof-release`, `runtime-evidence`, `sibling-proof-refs`, or `repair`.

## Consequences

- Positive: each active parent has a visible cross-root evidence profile.
- Positive: validators can reject a parent that exists in the allowlist but is
  missing from the dimension ledger.
- Tradeoff: the evidence map becomes longer, but the extra length replaces
  future confusion about why a parent name is valid.

## Boundaries

The ledger is not source proof authority and does not move payloads. It is a
route and classification surface.

It does not create new parents. Future parents still need an evidence-backed
slice that updates the cluster map, route cards, topology docs, decisions, and
validator constants together.

## Validation

```bash
python -m pytest -q tests/test_validate_repo.py -k mechanic_evidence_dimension
python scripts/validate_repo.py
```
