# Distillation Mechanic Package

- Decision ID: AOA-EV-D-0038
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/distillation/`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: mechanic package
- Mechanic parents: distillation
- Guard families: none
- Posture: active rationale

## Context

Distillation is a named AoA mechanic, and `aoa-evals` has a local proof-side
cluster that is specifically about provenance-preserving or
candidate-preserving distillation, not merely about memo, adoption, or artifact
polish.

The evidence cluster spans:

- `evals/artifact/aoa-compost-provenance-preservation/EVAL.md`
- `evals/workflow/aoa-memo-reviewed-candidate-adoption-integrity/EVAL.md`
- former root `fixtures/compost-provenance-v1/README.md`
- former Experience-adjacent
  `mechanics/experience/parts/adoption-federation/fixtures/memo-reviewed-candidate-adoption-guardrail-v1/README.md`
- bundle-local fixture and runner contracts, report schemas, example reports,
  generated catalog/capsule/section entries, tests, and
  `docs/operations/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md`

The same search found nearby memo recall, memo contradiction, confirmed
writeback-act, witness trace, audit hook, and generic Experience adoption
surfaces. Those are adjacent, but they do not all become Distillation parts.
Memo recall later proved an active recurrence support part through
`docs/decisions/AOA-EV-D-0039-recurrence-support-parts-expansion.md`.

## Options Considered

- Leave Distillation as a future candidate because the cluster is small.
- Keep reviewed-candidate adoption under `experience` because the old part used
  adoption vocabulary.
- Create proof-adjective parents such as `compost-proof` or
  `candidate-adoption-proof`.
- Create `mechanics/distillation/` as the AoA-aligned parent, move only the
  proven Distillation support fixtures into parts, and keep source bundles plus
  stronger-owner truth in their owning routes.

## Decision

Create `mechanics/distillation/` for the eval-side Distillation proof
operation:

`distillation pressure -> provenance-preserving or candidate-preserving proof question -> part-local support surface -> bundle-local review -> bounded abstraction/adoption read or owner handoff`

The active parts are:

- `compost-provenance` for `aoa-compost-provenance-preservation` support;
- `runtime-candidate-adoption` for
  `aoa-memo-reviewed-candidate-adoption-integrity` support.

Source proof bundles stay under `evals/`. Runtime-pack hook metadata stays
under `mechanics/audit/`. Generic adoption, consent, compatibility,
federation, KAG/ToS boundary, and shadow adoption support stay under
`mechanics/experience/`.

## Rationale

The parent name must be `distillation` because the proof-side work materializes
the center AoA Distillation mechanic: raw or candidate material becomes a
cleaner active or adopted form while provenance, review state, candidate
posture, receipt visibility, recall inspectability, and promotion boundaries
remain visible.

The package is deliberately narrow. Memo recall now routes through
`recurrence/memory-recall`; memo contradiction,
`aoa-memo-writeback-act-integrity` confirmed writeback-act proof, witness trace
integrity, artifact/process pairing, and generic Experience adoption are not
Distillation merely because they are nearby.

## Consequences

- Positive: future Distillation proof work starts from a clear active route,
  part contract, owner split, stop-lines, validation path, and provenance
  bridge.
- Positive: `experience/adoption-federation` no longer has to carry a
  runtime-to-memo distillation candidate fixture just because it says adoption.
- Tradeoff: source proof bundles remain outside the package, so package users
  must keep bundle-local proof authority visible.
- Follow-up: only create new Distillation parts when local support artifacts,
  inputs, outputs, owner split, stop-lines, and validation prove a recurring
  operation.

## Current Applicability

As of 2026-05-24:

- Still valid: `mechanics/distillation/` remains the eval-side parent for
  compost-provenance and runtime-candidate-adoption proof support.
- Changed: parent-level stop-line coverage now uses pressure-to-owner routes in
  `README.md`, `PARTS.md`, and `DIRECTION.md`, with validator tokens guarding
  the parent route rows.
- Superseded by: none.

## Review Log

### 2026-06-16 - Direction stop-line guard completed

- Previous assumption: `DIRECTION.md` carried the same parent-level
  pressure-to-owner-route stop-lines as the package README.
- New reality: the direction surface must mirror every parent README stop-line
  row, and the Distillation token matrix must guard each row explicitly.
- Reason: low-context readers can stop at `DIRECTION.md`; owner acceptance,
  Tree-of-Sophia canon, KAG lift, memo contradiction/writeback, and memo recall
  pressure must still route to the stronger owner.
- Source surfaces updated: `mechanics/distillation/DIRECTION.md`,
  `scripts/validators/distillation_route_tokens.py`, and
  `tests/test_mechanic_surface_contracts.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-05-24 - Parent boundary route wording

- Previous assumption: parent-level Distillation surfaces expressed boundaries
  through exclusion prose around summary-as-proof, memory canon, runtime
  activation, owner acceptance, ToS canon, KAG lift, memo recall, and adjacent
  memo proof.
- New reality: the parent route keeps the same authority boundary through
  pressure-to-owner-route rows.
- Reason: the package entry, part index, and direction surface now show the
  next owner route directly, matching the part-contract route shape introduced
  for `compost-provenance` and `runtime-candidate-adoption`.
- Source surfaces updated: `mechanics/distillation/README.md`,
  `mechanics/distillation/PARTS.md`, `mechanics/distillation/DIRECTION.md`, and
  `scripts/validate_repo.py`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Boundaries

This decision does not move source proof bundles into
`mechanics/distillation/`.

It does not authorize raw deletion authority, summary-as-proof, memory canon,
runtime activation, KAG lift, ToS canon, owner-local adoption, final promotion,
or generic live memory-ledger claims.

It does not transfer `Agents-of-Abyss`, `Tree-of-Sophia`, `aoa-memo`,
`aoa-agents`, `abyss-stack`, `aoa-kag`, `aoa-playbooks`, `aoa-skills`,
`aoa-techniques`, or owner-repository truth into `aoa-evals`.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
