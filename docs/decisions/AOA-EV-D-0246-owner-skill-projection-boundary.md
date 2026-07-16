# Owner Skill Projection Boundary

- Decision ID: AOA-EV-D-0246
- Status: Accepted
- Date: 2026-07-16
- Owner surface: `AGENTS.md`, `DESIGN.AGENTS.md`, `.agents/AGENTS.md`, and `docs/architecture/PROOF_TOPOLOGY.md`

## Index Metadata

- Original date: 2026-07-16
- Surface classes: agent-route, root/topology, owner-boundary
- Mechanic parents: none
- Guard families: repository skill admission, projection ownership
- Posture: accepted owner-boundary rationale

## Context

`aoa-evals` carried a checked-in `.agents/skills/` catalog copied from
`aoa-skills`. The copied packages were neither canonical owner truth nor a
projection of a repo-owned top-level skill home. Manual prompt inspection in a
fresh repository context confirmed that a subset entered the model-visible
catalog and competed for routing even though their source metadata named
`aoa-skills` as owner.

The consolidated `aoa-skills` model now installs shared skills once at the user
or explicit workspace delivery layer. A separate review of `aoa-eval` found no
behavioral evidence sufficient to claim an independent repo-home skill or an
improvement over the no-skill baseline. Structural symmetry is not admission
evidence.

## Options Considered

- Retain the copied shared catalog as local convenience.
- Replace the catalog immediately with a top-level `aoa-eval` home.
- Remove the foreign projection and keep both the canonical repo skill home and
  its derived projection absent until a candidate passes owner admission.

## Decision

Remove `.agents/skills/` from `aoa-evals` and keep `.agents/` limited to
maintained agent lanes.

A future repo-specific callable procedure may be admitted only when manual
trials establish:

- an independent applicability trigger;
- an explicit input and output ABI;
- reusable composition value;
- positive and negative routing behavior;
- coexistence behavior beside the active skill library;
- added value against a no-skill baseline, including held-out transfer where
  the procedure claims generality.

After an accepted owner decision, canonical skill source belongs under
top-level `skills/`. Any `.agents/skills/` surface is then a derived delivery
projection of that home, never an alternate owner or a place for copied shared
skills. Shared procedures remain owned and delivered by `aoa-skills`.

## Rationale

Removing the copied catalog eliminates demonstrated prompt competition and
restores one owner for shared procedure truth. Refusing to create an empty or
unproven home keeps filesystem symmetry from becoming false capability
evidence. The admission threshold leaves room for a real eval-owned skill while
requiring its value to be observed before permanent packaging and guards are
added.

## Consequences

- Positive: fresh repo sessions no longer discover foreign local skill copies.
- Positive: shared skills have one canonical source and one intentional
  delivery route.
- Positive: a future eval-owned skill has a clear source home and evidence
  threshold.
- Tradeoff: repo-local skill convenience is absent until a candidate earns it.
- Follow-up: apply the same owner-first classification to sibling repositories;
  do not infer their disposition mechanically from this decision.

## Current Applicability

As of 2026-07-16:

- Still valid: `.agents/` owns maintained agent lanes and proof authority stays
  with source proof surfaces; copied shared catalogs remain forbidden.
- Changed: the no-home state ended after manual evidence admitted one
  repository-owned bundle. `.agents/skills/aoa-evals` is now an exact generated
  projection of `skills/aoa-evals`, not a support lane or alternate source.
- Superseded by: AOA-EV-D-0247 supersedes only the temporary absence state and
  records the admitted owner bundle; this decision's projection boundary stays
  active.

## Review Log

### 2026-07-16 - Owner bundle admitted after manual trials

- Previous assumption: no repository skill had sufficient evidence for an
  owner home.
- New reality: one `aoa-evals` bundle passed the admission threshold.
- Reason: isolated, negative, coexistence, no-skill, drift, and held-out work
  established a distinct central-proof trigger and bounded result ABI.
- Source surfaces updated: `skills/`, `.agents/skills/`, root agent guidance,
  proof topology, and AOA-EV-D-0247.
- Validation: manual semantic trials remain the admission evidence; the common
  home-port guard checks only deterministic source/projection parity.

## Boundaries

This decision does not retire any shared skill globally, declare `aoa-eval`
permanently useless, or authorize an automated benchmark to substitute for
manual behavioral review.

It does not make a future skill a proof authority, permit session-local traces
to become owner truth, or require sibling repositories to create a `skills/`
directory.

## Validation

The active route is checked by source metadata inspection, fresh prompt
inspection before and after projection removal, the agent-lane projection
boundary guard, decision-index parity, and the current repository validation
lanes owned by `docs/validation/COMMAND_AUTHORITY.md` and the nearest
`AGENTS.md`.
