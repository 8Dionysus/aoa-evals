# Questbook Validator Route Boundary

- Decision ID: AOA-EV-D-0143
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validators/questbook.py`, `mechanics/questbook/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, source/topology, generated/read-model
- Mechanic parents: questbook, rpg, agon, cross-parent
- Guard families: source/topology, projection/generated, trace/eval
- Posture: active rationale

## Context

`scripts/validators/questbook.py` already owned quest source records,
generated quest dispatch readers, quest schemas, and, at the time, RPG unlock
bridge checks.
`scripts/validate_repo.py` still carried the adjacent Questbook route surfaces:
`quests/` route cards, lifecycle route residue, Agon quest-note provenance
decision checks, Questbook parent route cards, part owner-split contracts,
provenance bridge posture, and Questbook decision-token checks.

Those checks are one Questbook boundary. They do not own live task assignment,
proof-surface promotion, owner acceptance, runtime dispatch, or final quest
state movement.

## Decision

Quest route and Questbook mechanic route validation live in
`scripts/validators/questbook.py`.

`scripts/validate_repo.py` calls the Questbook validator module directly,
supplying a `QuestbookRouteContext` with the root token lookup helper and
shared provenance bridge tokens for route-token checks.

The module owns Questbook-specific source, projection, route, part-contract,
lifecycle residue, and decision expectations. Shared lookup and provenance
posture remain injected.

## Rationale

Keeping source/projection truth in `scripts/validators/questbook.py` while
leaving route and part-contract truth in the root validator split one owner
surface across two modules. That made the repo-wide entrypoint remember
Questbook history and Agon quest-note routing.

The module boundary keeps `aoa-evals` responsible for source quest records,
generated dispatch parity, route cards, and part owner-split posture while
routing live assignment, proof promotion, owner acceptance, and runtime dispatch
to stronger owners.

## Consequences

- Positive: Quest source/projection, route residue, parent route, part
  owner-split, provenance, and decision-token checks have one focused owner.
- Positive: `validate_mechanics_surfaces` no longer retains
  Questbook-specific token matrices, and root no longer re-exports Questbook
  source/projection helper APIs.
- Positive: tests import Questbook route constants from the owner module
  directly.
- Follow-up: remaining root constants should be reduced only when the owning
  module can carry the full boundary without compatibility aliases.

## Current Applicability

As of 2026-06-04:

- Still valid: `scripts/validate_repo.py` remains the repo-wide command
  entrypoint.
- Changed: Quest route and Questbook mechanic route validation moved from
  `scripts/validators/questbook.py` into
  `scripts/validators/questbook_routes.py`. The remaining `questbook.py`
  compatibility facade was removed under AOA-EV-D-0193. RPG
  progression/unlock bridge checks moved to
  `scripts/validators/questbook_progression.py`. Generated projection checks
  later split across `scripts/validators/questbook_projection_records.py`,
  `scripts/validators/questbook_projection_parity.py`, and
  `scripts/validators/questbook_orchestrator_refs.py`. Source record, schema,
  lifecycle, and active/closed Questbook listing checks moved to
  `scripts/validators/questbook_source.py`.
- Superseded by: AOA-EV-D-0160 for Questbook-linked RPG progression/unlock
  bridge checks; AOA-EV-D-0163 for Questbook generated projection checks;
  AOA-EV-D-0170 for Questbook source record, schema, and lifecycle checks;
  AOA-EV-D-0176 for Questbook route-card and mechanic route checks;
  AOA-EV-D-0193 for removal of the remaining compatibility facade; and
  AOA-EV-D-0197 for removal of the projection aggregate.

## Review Log

### 2026-06-04 - RPG progression bridge split

- Previous assumption: `questbook.py` owned RPG unlock bridge checks because a
  Questbook source record referenced the bridge.
- New reality: `questbook.py` delegates that bridge to
  `scripts/validators/questbook_progression.py` while preserving the public
  adapter used by tests.
- Reason: a quest reference does not transfer RPG progression/unlock ownership
  into Questbook.
- Source surfaces updated: `scripts/validators/questbook.py`,
  `scripts/validators/questbook_progression.py`, validation inventories, and
  mechanics residual classification.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-06-04 - Generated projection split

- Previous assumption: `questbook.py` owned source, route, and generated
  projection checks as one Questbook boundary.
- New reality: `questbook.py` delegates generated catalog/dispatch projection
  parity and strict orchestrator bridge checks to
  `scripts/validators/questbook_projection.py`.
- Reason: generated readers must prove rebuild parity from source records
  without becoming source quest meaning or runtime dispatch authority.
- Source surfaces updated: `scripts/validators/questbook.py`,
  `scripts/validators/questbook_projection.py`, validation inventories, and
  mechanics residual classification.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-06-04 - Source record and lifecycle split

- Previous assumption: `questbook.py` could own Questbook route cards, part
  contracts, source records, schema envelopes, lifecycle posture, generated
  handoff, and public helper compatibility as one boundary.
- New reality: `questbook.py` delegates source record, schema, lifecycle,
  active/closed listing, and source owner-constraint checks to
  `scripts/validators/questbook_source.py`.
- Reason: source quest records are authored truth and need a focused
  source/topology guard rather than another historical layer inside the route
  facade.
- Source surfaces updated: `scripts/validators/questbook.py`,
  `scripts/validators/questbook_source.py`, validation inventories, and
  mechanics residual classification.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-06-04 - Route-card split

- Previous assumption: `questbook.py` could remain the owner of route-card
  checks after source, projection, and RPG bridge checks moved out.
- New reality: `questbook.py` delegates Questbook route-card, stale residue,
  part owner-split, and route-decision checks to
  `scripts/validators/questbook_routes.py`.
- Reason: the compatibility facade should not retain the route-token body as
  another historical accumulation point.
- Source surfaces updated: `scripts/validators/questbook.py`,
  `scripts/validators/questbook_routes.py`, validation inventories, and
  mechanics residual classification.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-06-04 - Compatibility facade removal

- Previous assumption: `questbook.py` could remain as a historical public
  import facade after all behavior moved to focused modules.
- New reality: `questbook.py` no longer exists; shared constants and parsing
  helpers first lived in `scripts/validators/questbook_common.py`, then
  AOA-EV-D-0219 split that helper layer into focused context, IO,
  source-constant, and orchestrator-constant modules while callers import
  source, projection, route, or progression validators directly.
- Reason: a compatibility facade after the split is not an owner boundary and
  would keep inviting future Questbook-adjacent behavior back into one module.
- Source surfaces updated: focused Questbook helper modules,
  `scripts/validators/questbook_source.py`,
  `scripts/validators/questbook_projection_records.py`,
  `scripts/validators/questbook_projection_parity.py`,
  `scripts/validators/questbook_orchestrator_refs.py`,
  `scripts/validators/questbook_routes.py`,
  `scripts/validators/questbook_progression.py`, validation inventories, and
  mechanics residual classification.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-06-04 - Projection aggregate removal

- Previous assumption: the focused projection module could still own source
  projection builders, generated parity, and strict sibling orchestrator refs
  together.
- New reality: projection builders route to
  `scripts/validators/questbook_projection_records.py`, generated reader parity
  routes to `scripts/validators/questbook_projection_parity.py`, and strict
  sibling refs route to `scripts/validators/questbook_orchestrator_refs.py`.
- Reason: source-derived expected records, frozen generated parity, and sibling
  capability refs are different boundaries.
- Source surfaces updated: Questbook validator modules, validation inventories,
  and mechanics residual classification.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Boundaries

This decision does not make Questbook the owner of live task assignment,
proof-surface promotion, owner acceptance, runtime dispatch, or final quest
state movement.

It also no longer makes Questbook the owner of RPG progression evidence or
unlock proof bridge contracts; those route to
`scripts/validators/questbook_progression.py`.

Generated quest reader parity routes to
`scripts/validators/questbook_projection_parity.py`; expected projection
builders route to `scripts/validators/questbook_projection_records.py`; strict
sibling orchestrator refs route to
`scripts/validators/questbook_orchestrator_refs.py`. Generated readers remain
derived read models, not quest meaning authority.

Questbook source record, schema, lifecycle, and active/closed listing checks
route to `scripts/validators/questbook_source.py`; source quest records remain
authored truth, not generated reader output or live task assignment.

Questbook route-card, stale residue, part owner-split, and route-decision checks
route to `scripts/validators/questbook_routes.py`; there is no replacement
Questbook aggregate facade.

It does not move shared mechanic topology ledgers or route-token lookup helpers
into Questbook.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
