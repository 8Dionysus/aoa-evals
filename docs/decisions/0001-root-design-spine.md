# 0001 Root Design Spine

- Status: Accepted
- Date: 2026-05-19
- Owner surface: root docs and agent route surfaces

## Context

`aoa-evals` already had strong proof philosophy and a technical architecture
model, but it lacked the root design pair used by mature AoA organs:
`DESIGN.md` for system form and `DESIGN.AGENTS.md` for agent-facing form.

Without those surfaces, the long refactor plan had to live in a working note and
future agents had no durable root place to ask what shape the proof organ should
preserve.

## Options Considered

- Keep using `docs/ARCHITECTURE.md` as the highest design surface.
- Expand root `AGENTS.md` with the missing design doctrine.
- Add a root design spine and keep existing depth docs in their current roles.

## Decision

Add `DESIGN.md` and `DESIGN.AGENTS.md`, then keep root `AGENTS.md` as a compact
route card that points to those surfaces.

`docs/ARCHITECTURE.md` remains the technical proof model.
`docs/EVAL_PHILOSOPHY.md` remains the epistemic posture for evaluation.

## Rationale

The root design spine lets `aoa-evals` name its own proof-organ form without
copying sibling repositories literally. It also keeps agent guidance routeable:
the active root card can stay short while deeper design and technical meaning
have durable homes.

## Consequences

- Positive: future topology, quest, mechanics, legacy, and runtime-candidate
  changes can be judged against a local proof-organ design.
- Tradeoff: there is one more root surface to keep aligned with architecture
  and philosophy.
- Follow-up: validators should keep the design spine discoverable, and later
  roadmap/quest/mechanics work should cite the spine instead of repeating it.

## Boundaries

This decision does not make `DESIGN.md` a charter, roadmap, architecture
reference, eval bundle, or source of sibling-owner truth.

It does not authorize moving quests, mechanics, Spark, runtime candidates, or
legacy files by analogy alone.

## Validation

- root `AGENTS.md` links to `DESIGN.md` and `DESIGN.AGENTS.md`
- `docs/decisions/README.md` lists this decision
- `python scripts/validate_repo.py` checks the root design surfaces
- `python scripts/validate_semantic_agents.py` checks the existing semantic
  AGENTS mesh
