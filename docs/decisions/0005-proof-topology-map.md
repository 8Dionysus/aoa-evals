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

Later mechanics decisions created an active `mechanics/` atlas. This decision
still owns the topology-map reason: classify authority before movement, then
keep using that map to constrain further movement.

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
legacy lineage, and mechanic operations.

Further physical movement or new parent creation stays blocked until the map,
the mechanics evidence ledger, route cards, decisions, and validators prove a
real operation that a mechanic package should own.

## Rationale

This makes the topology more convex without pretending package names are enough
proof. A future agent can tell whether it is touching source proof meaning, a
generated companion, candidate evidence, a receipt, a quest obligation, a
decision, sibling-owned truth, legacy lineage, or an active mechanic operation
before editing.

It also preserves the meta-example lesson from neighboring repositories:
mechanics are useful when they route live operations, not when they are empty
taxonomy.

## Consequences

- Positive: mechanic movement remains tied to authority class, source
  artifacts, validation, and legacy posture instead of repo-shape symmetry.
- Tradeoff: topology changes must update both the map and the validator-backed
  surfaces that depend on it.
- Follow-up: later mechanics slices must keep using the map and
  `mechanics/EVIDENCE_CLUSTERS.md` before moving additional payloads.

## Current Applicability

As of 2026-05-22:

- Still valid: `docs/PROOF_TOPOLOGY.md` owns authority-class routing and the
  convex topology frame.
- Changed: detailed mechanic activation, parent evidence, payload home, and
  validation lane detail now routes through `mechanics/README.md`, parent
  route cards, part maps, and `mechanics/EVIDENCE_CLUSTERS.md`.
- Superseded by: none.

## Review Log

### 2026-05-22 - Mechanics detail routed to mechanics surfaces

- Previous assumption: the proof topology map could carry active mechanic
  package detail alongside authority-class routing.
- New reality: the active mechanics atlas and evidence gate now provide the
  clearer owner surfaces for parent evidence, part contracts, payload homes,
  and validation lanes.
- Reason: low-context agents should use `docs/PROOF_TOPOLOGY.md` to classify a
  surface, then descend into mechanics through the operation atlas instead of
  reading duplicated package detail in the topology map.
- Source surfaces updated: `docs/PROOF_TOPOLOGY.md` and this decision.
- Validation: use root validation and the focused proof-topology validator
  tests.

## Boundaries

This decision did not by itself create `mechanics/`; later decisions created
the active `mechanics/` atlas.

It does not create new parent mechanics by itself, move quests, move generated
readers, promote Titan canaries, revive `Spark/`, or publish receipt logs.

It does not let the topology map outrank `DESIGN.md`, source proof bundles,
bundle-local reports, generated builders, or sibling-owner truth.

## Validation

- `docs/PROOF_TOPOLOGY.md` names the authority classes and root technical
  districts.
- `README.md`, `docs/README.md`, `DESIGN.md`, `DESIGN.AGENTS.md`, `AGENTS.md`,
  and `ROADMAP.md` route readers to the topology map.
- `python scripts/validate_repo.py` checks the topology map and this decision.
