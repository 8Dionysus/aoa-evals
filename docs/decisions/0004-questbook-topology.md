# 0004 Questbook Topology

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `QUESTBOOK.md`, `quests/`, and generated quest readers

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

## Boundaries

This decision does not turn quests into eval bundles, proof verdicts, roadmap
direction, or playbook routes.

It does not authorize moving Agon notes or `AOA-EV-Q-*` records yet.

## Validation

- `quests/README.md` and `quests/AGENTS.md` name the role split.
- `QUESTBOOK.md` lists active non-closed quest IDs and excludes closed
  foundation records.
- `generated/quest_catalog.min.json` and `generated/quest_dispatch.min.json`
  match source quest records.
- `python scripts/build_catalog.py --check`
- `python scripts/validate_repo.py`
