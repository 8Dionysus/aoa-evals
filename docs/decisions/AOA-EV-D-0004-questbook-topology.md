# Questbook Topology

- Decision ID: AOA-EV-D-0004
- Status: Accepted
- Date: 2026-05-19
- Owner surface: `QUESTBOOK.md`, `quests/`, and generated quest readers

## Index Metadata

- Original date: 2026-05-19
- Surface classes: root/topology, quest/lane
- Mechanic parents: questbook
- Guard families: none
- Posture: active rationale

## Context

`aoa-evals` already has source quest records, generated quest catalog and
dispatch projections, and a public `QUESTBOOK.md`. The surfaces were useful but
too easy to blur: roadmap direction, open obligations, source quest records,
generated readers, and eval bundle meaning could all be mistaken for one
another.

The long refactor plan also names a future lane/state quest topology, but moving
files before validators and generated readers are ready would create path churn
instead of proof honesty.

## Options Considered

- Move all quest files into lane/state directories immediately.
- Leave the flat quest layout as-is and rely on convention.
- Clarify the role split now, add `quests/README.md` and `quests/AGENTS.md`,
  keep current paths stable, and defer physical movement until validators and
  generated projections can follow.

## Decision

Keep current top-level quest paths stable for now.

Add explicit route surfaces for `quests/`, rewrite `QUESTBOOK.md` as the human
open-obligation index, and keep `ROADMAP.md` as the direction surface.

Treat generated quest catalog and dispatch files as derived readers. They must
stay subordinate to source quest records and never become eval verdict
authority.

## Rationale

This preserves compatibility while making the topology more convex. Future
agents can now tell which surface owns direction, obligation, source record,
dispatch read model, and proof meaning before any file move happens.

## Consequences

- Positive: quest work can proceed without treating the flat layout as mature
  topology.
- Tradeoff: old top-level paths remain for another phase.
- Follow-up: a future `mechanics/questbook` package or lane/state migration
  should update validators, generated projections, and legacy path mappings in
  one slice.

## Current Applicability

As of 2026-05-24:

- Still valid: `QUESTBOOK.md` is the human open-obligation index, while
  `quests/` owns source records and generated quest files remain projections.
- Changed: the active `QUESTBOOK.md` harvest, closed-record, and generated-pair
  posture now names owner routes, reviewed promotion, and source-bundle
  authority directly.
- Historical text: the original topology decision remains the record of why
  quest surfaces were separated before lane/state movement.
- Superseded by: none.

## Review Log

### 2026-05-24 - Human quest index harvest route made positive

- Previous assumption: `QUESTBOOK.md` could explain closed records, harvest
  candidates, and generated quest pairs through negative boundary wording.
- New reality: the active human index now routes closed records to provenance,
  harvest output to reviewed owner acceptance, and eval meaning to source
  bundles.
- Reason: a low-context agent should see the quest obligation route and target
  owner without turning the human index into command law or verdict authority.
- Source surfaces updated: `QUESTBOOK.md`, `scripts/validate_repo.py`,
  `tests/test_validate_repo.py`, and this decision.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Boundaries

This decision does not turn quests into eval bundles, proof verdicts, roadmap
direction, or playbook routes.

It does not authorize moving Agon notes or `AOA-EV-Q-*` records yet.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
