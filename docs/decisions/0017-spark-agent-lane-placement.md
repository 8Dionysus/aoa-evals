# 0017 Spark Agent Lane Placement

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `.agents/spark/`

## Index Metadata

- Surface classes: proof topology
- Mechanic parents: none
- Guard families: none
- Posture: active rationale

## Context

`Spark/` was the last maintained agent lane still sitting at the repository
root. Earlier design work intentionally kept it there until
`DESIGN.AGENTS.md`, validators, and a decision could authorize a local move.

That condition is now met. `DESIGN.AGENTS.md` defines the agent-facing mesh,
`.agents/skills/` already exists as an agent companion surface, and
`docs/architecture/LEGACY_NAMING.md` marks root `Spark/` as historical until validator-backed
placement is ready.

## Options Considered

- Keep `Spark/` at the repository root as a historical lane.
- Move the lane under `mechanics/` because it supports proof work.
- Move the lane to `.agents/spark/` and add `.agents/AGENTS.md` plus validator
  checks.

## Decision

Move the maintained Spark lane from `Spark/` to `.agents/spark/`.

Add `.agents/AGENTS.md` as the district card for agent lanes and support
surfaces. Keep `.agents/skills/` as exported/support skills, and keep
`.agents/spark/` as the fast-loop lane for bounded proof-surface work.

## Rationale

The lane is agent-facing guidance, not a proof bundle, mechanic package,
generated reader, receipt, runtime candidate, or sibling reference. `.agents/`
is the convex home for that class.

Moving the lane now reduces root clutter while preserving proof ownership:
Spark can route one bounded claim or seam at a time, but bundle-local
`EVAL.md` and `eval.yaml` still own proof meaning.

## Consequences

- Positive: root topology is cleaner, `.agents/` becomes the durable agent
  district, and Spark lane guidance has local route validation.
- Tradeoff: references to `Spark/` must now be treated as legacy path
  vocabulary.
- Follow-up: future maintained agent lanes should start under
  `.agents/<lane>/` and get local validation before use.

## Boundaries

This decision does not move `.agents/skills/`, proof bundles, generated
readers, mechanics packages, reports, receipts, runtime candidates, or sibling
owner truth.

It does not let Spark perform broad architecture rewrites or strengthen eval
claims beyond bundle-local evidence.

It does not make `.agents/` a doctrine center.

## Validation

- `.agents/AGENTS.md` names the agent district route.
- `.agents/spark/AGENTS.md` names the Spark fast-loop lane route.
- `.agents/spark/SWARM.md` uses the current path.
- `Spark/` is absent.
- `docs/architecture/PROOF_TOPOLOGY.md`, `docs/architecture/LEGACY_NAMING.md`, `README.md`,
  `ROADMAP.md`, and `docs/decisions/README.md` route the new placement.
- `scripts/validate_repo.py`
- `python scripts/validate_nested_agents.py`
- `python scripts/validate_semantic_agents.py`
