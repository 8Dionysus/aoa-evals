# 0005 Proof Topology Map

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `docs/PROOF_TOPOLOGY.md`

## Context

The refactor plan reached the phase where `aoa-evals` needs to decide what kind
of surfaces it already has before moving files or creating mechanics.

The repository contains source proof bundles, flat docs, generated readers,
runtime candidates, receipts, quests, sibling refs, Agon and wave lineage,
Titan canaries, installed skills, and a still-root-local `Spark/` lane. Without
a topology map, a future mechanics pass could become taxonomy-first or move
files by analogy with sibling repositories rather than by proof ownership.

## Options Considered

- Create `mechanics/` immediately and sort surfaces into packages as they are
  discovered.
- Keep the current tree unchanged and rely on roadmap text to explain future
  movement.
- Add a proof topology map first, then create mechanics only when a recurring
  operation has source artifacts, inputs, outputs, legacy posture, and
  validation.

## Decision

Add `docs/PROOF_TOPOLOGY.md` as the Phase 4 map of authority classes and root
technical districts.

The map names source proof objects, source guidance, shared proof
infrastructure, reports and examples, derived readers, candidate evidence,
receipts, quest obligations, decisions, agent guidance, sibling references,
legacy lineage, and mechanic-ready operations.

Keep physical movement deferred until the map proves a real operation that a
mechanic package should own.

## Rationale

This makes the topology more convex without pretending the future layout is
already built. A future agent can tell whether it is touching source proof
meaning, a generated companion, candidate evidence, a receipt, a quest
obligation, a decision, sibling-owned truth, or legacy lineage before editing.

It also preserves the meta-example lesson from neighboring repositories:
mechanics are useful when they route live operations, not when they are empty
taxonomy.

## Consequences

- Positive: Phase 5 can choose the first mechanic from live pressure instead of
  repo-shape symmetry.
- Tradeoff: the repo gains one more docs surface before file movement begins.
- Follow-up: the first mechanics slice should pick one package only after this
  map identifies the operation, source artifacts, validation, and legacy
  posture it will own.

## Boundaries

This decision does not create `mechanics/`.

It does not move quests, Agon notes, generated readers, Titan canaries, `Spark/`,
or receipt logs.

It does not let the topology map outrank `DESIGN.md`, source proof bundles,
bundle-local reports, generated builders, or sibling-owner truth.

## Validation

- `docs/PROOF_TOPOLOGY.md` names the authority classes and root technical
  districts.
- `README.md`, `docs/README.md`, `DESIGN.md`, `DESIGN.AGENTS.md`, `AGENTS.md`,
  and `ROADMAP.md` route readers to the topology map.
- `python scripts/validate_repo.py` checks the topology map and this decision.
