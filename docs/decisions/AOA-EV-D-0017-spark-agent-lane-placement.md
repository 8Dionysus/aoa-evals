# Spark Agent Lane Placement

- Decision ID: AOA-EV-D-0017
- Status: Accepted
- Date: 2026-05-19
- Owner surface: `.agents/spark/`

## Index Metadata

- Original date: 2026-05-19
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
  district, `Spark/` is absent, and Spark lane guidance has local route
  validation.
- Tradeoff: references to `Spark/` must now be treated as legacy path
  vocabulary.
- Follow-up: future maintained agent lanes should start under
  `.agents/<lane>/` and get local validation before use.

## Current Applicability

As of 2026-07-16:

- Still valid: Spark remains a maintained fast-loop lane under
  `.agents/spark/`, and `.agents/` remains the district for agent-facing lanes.
- Changed: `.agents/skills/` is no longer an active support surface; a future
  repo-specific skill must first be admitted under the top-level `skills/`
  owner boundary.
- Superseded by: AOA-EV-D-0246 supersedes only the copied-skill support-lane
  assumption; it does not supersede Spark placement.

## Review Log

### 2026-07-16 - Skill ownership and projection route corrected

- Previous assumption: checked-in exported skills could coexist with maintained
  agent lanes under `.agents/`.
- New reality: shared procedures are delivered from `aoa-skills`, while a
  repository projection requires a separately admitted top-level `skills/`
  owner home.
- Reason: manual fresh-context inspection showed that copied foreign skills
  entered the model-visible routing catalog without becoming `aoa-evals`
  owner truth.
- Source surfaces updated: root and `.agents/` route cards,
  `DESIGN.AGENTS.md`, proof topology, and the agent-lane projection guard.
- Validation: D-0246, fresh prompt inspection, decision-index parity, focused
  agent-lane tests, and repository validation.

## Boundaries

This decision does not move `.agents/skills/`, proof bundles, generated
readers, mechanics packages, reports, receipts, runtime candidates, or sibling
owner truth.

It does not let Spark perform broad architecture rewrites or strengthen eval
claims beyond bundle-local evidence.

It does not make `.agents/` a doctrine center.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
