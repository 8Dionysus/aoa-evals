# Mechanic Parent Allowlist

- Decision ID: AOA-EV-D-0052
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: validation guard
- Mechanic parents: cross-parent
- Guard families: parent and package
- Posture: active guard rationale

## Context

The mechanics refactor fixed several bad parent forms by routing them to the
living operation names:

- `agon-proof` became `agon`;
- `titan-canaries` became `titan`;
- `proof-release` became `release-support`;
- `runtime-evidence` became `audit`;
- `sibling-proof-refs` became `boundary-bridge`.

Those repairs are not enough by themselves. If a future slice can create
`mechanics/<new-name>/` without proving a cross-root evidence cluster, the same
failure mode returns under a different spelling.

## Decision

Top-level mechanic parent directories are validator allowlisted: no invented parent packages
become active topology without evidence.

Every allowed parent must also expose `AGENTS.md`, `README.md`, and `PARTS.md`.
Every `PARTS.md` must carry the shared part contract shape: inputs, outputs,
owner split, stop-lines, and validation.

The current allowlist is derived from `mechanics/EVIDENCE_CLUSTERS.md` and
contains only parents that are already classified as AoA-aligned or
evals-native.

A new parent mechanic may be added only when the same slice updates:

- `mechanics/EVIDENCE_CLUSTERS.md`;
- `mechanics/README.md`;
- the new package route cards and part contracts;
- `docs/architecture/PROOF_TOPOLOGY.md`;
- this validator allowlist;
- decision/changelog/roadmap surfaces that explain why the name is not a form,
  artifact, report, canary, schema, runner, generated reader, or old path
  family.

## Rationale

Mechanics are operation parents, not convenient buckets. A parent name should
survive future growth: parts can multiply under it without the package name
becoming false.

The allowlist protects convex topology. It makes the absence of invented
parent packages a checked invariant instead of a matter of taste.
Active parents are active, not merely plausible candidates; candidate wording
must not soften the allowlist into a brainstorming surface.

## Consequences

- Positive: `python scripts/validate_repo.py` rejects undeclared
  `mechanics/<parent>/` directories.
- Positive: the validator also rejects missing parent route cards and missing
  part-contract wording for any allowlisted parent.
- Positive: future mechanics must pass through evidence-cluster review before
  they become active topology.
- Tradeoff: exploratory material cannot be parked as a top-level mechanic.
  It must stay in the owning current mechanic, source bundle, quest, ingress
  note, or provenance bridge until an active operation is proven.

## Boundaries

This decision does not freeze the mechanics atlas forever. It freezes only the
current active parent set until a later evidence-backed decision updates it.

It does not forbid new parts inside an existing mechanic when that mechanic's
owned operation actually covers the part and the part has inputs, outputs,
owner split, stop-lines, and validation.

## Validation

- `mechanics/EVIDENCE_CLUSTERS.md`
- `mechanics/README.md`
- `scripts/validate_repo.py`
- `tests/test_validate_repo.py`
- `python scripts/validate_repo.py`
- `python -m pytest -q tests/test_validate_repo.py -k 'mechanic_parent_allowlist or part_contract_files'`
