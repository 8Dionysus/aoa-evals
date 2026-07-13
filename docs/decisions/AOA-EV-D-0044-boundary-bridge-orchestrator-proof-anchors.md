# Boundary Bridge Orchestrator Proof Anchors

- Decision ID: AOA-EV-D-0044
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/boundary-bridge/parts/orchestrator-proof-anchors/`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: boundary/runtime/sibling
- Mechanic parents: boundary-bridge
- Guard families: sibling and boundary
- Posture: active rationale

## Context

`docs/ORCHESTRATOR_PROOF_ALIGNMENT.md` was still a root doc, but its evidence
cluster was not generic source guidance. It was tied to three orchestrator
quest records, generated quest readers, `scripts/validate_repo.py`,
`aoa-agents:*` orchestrator class refs, playbook family refs, and memo surface
refs.

That made the root placement too broad. At the same time, creating an
`orchestrator` parent mechanic would be wrong: orchestrator class identity lives
in `aoa-agents`, and this repo owns only bounded proof anchors and quest
obligation routing.

## Options Considered

- Keep the alignment note in root `docs/` as broad source guidance.
- Create a new `orchestrator` parent mechanic.
- Move the note into `boundary-bridge` as a part because the live operation is
  owner-boundary proof-anchor alignment.

## Decision

Move the authored alignment note to:

`mechanics/boundary-bridge/parts/orchestrator-proof-anchors/docs/ORCHESTRATOR_PROOF_ALIGNMENT.md`

Update orchestrator quest owner surfaces, validator constants, generated quest
readers, and route docs to point at the part-local owner.

The parent remains `boundary-bridge`. `orchestrator-proof-anchors` is a part,
not a parent mechanic.

## Rationale

This keeps topology convex: a future agent can see that the proof anchors cross
owner boundaries into `aoa-agents`, `aoa-playbooks`, and `aoa-memo`, but the
local proof obligation stays in `aoa-evals`.

It also prevents a repeat of the earlier naming mistake where artifact or role
forms became parent package names. Here, `orchestrator` is a stronger-owner
class family, while `proof anchors` are the local eval-side bridge part.

## Consequences

- Positive: root `docs/` loses one narrower mechanic-owned surface.
- Positive: the three orchestrator quests now point at a mechanic part with a
  part contract and owner split.
- Tradeoff: `boundary-bridge` now owns one proof-anchor part in addition to
  sibling-ref compatibility and latest-sibling canary checking.
- Follow-up: if future orchestrator proof work gains schemas, fixtures, or
  reports, add them under this part only after the local proof operation is
  explicit.

## Boundaries

This decision does not define orchestrator identity, role policy, playbook
authority, memo truth, or a new eval bundle.

It does not authorize editing sibling repositories.

It does not let quest records become proof verdicts.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
