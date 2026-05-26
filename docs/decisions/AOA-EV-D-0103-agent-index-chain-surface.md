# Agent Index Chain Surface

- Decision ID: AOA-EV-D-0103

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-22
- Surface classes: root/topology
- Mechanic parents: none
- Guard families: none
- Posture: active rationale

## Context

The repository now has enough route cards, topology maps, mechanics parents,
part contracts, generated readers, decisions, and validators that a future
agent can still lose the chain between a path name and its authority class.

The root README must stay compact, `docs/architecture/PROOF_TOPOLOGY.md` must keep authority
classes rather than become a dispatcher, and `AGENTS.md` must own executable
route law. Putting the whole agent route chain into any one of those surfaces
would either bloat an entrypoint or hide route-law detail in the wrong place.

## Decision

Add `docs/architecture/AGENT_INDEX.md` as an agent-facing pass-through index for the chain:

`repo -> authority class -> operation -> mechanic parent -> part -> payload -> validation`

The index is weaker than source truth, route cards, decisions, generated
readers, validators, and bundle-local proof meaning. It names where to go next
from a path shape and keeps route-card-only root districts explicit as
compatibility districts.

`docs/README.md` remains the human and agent docs map. Its topology route map
must list every active mechanic parent so agents can enter the operation layer
from docs without silently seeing only a partial parent set.

Executable validation commands remain in the nearest `AGENTS.md`, with mechanic
part routes flowing through part `VALIDATION.md` into the parent
`parts/AGENTS.md` centralized child validation lane.

## Consequences

- Positive: an agent can enter from a path name and recover the proof-organ
  chain without reading chat history.
- Positive: root README can stay shorter while still pointing to a complete
  agent route map.
- Positive: route-card-only districts become visible as compatibility surfaces
  instead of looking like active payload homes.
- Tradeoff: `docs/architecture/AGENT_INDEX.md` must stay a read model. If it starts carrying
  commands, source truth, or decision rationale, it should be trimmed and routed
  back to the owning surface.

## Current Applicability

As of 2026-05-22:

- Still valid: `docs/architecture/AGENT_INDEX.md` remains the pass-through chain from repo to
  authority class, operation, mechanic parent, part, payload, and validation.
- Changed: the root README now follows the public front-door pattern used by
  the neighboring AoA repositories: it names what the proof canon does, routes
  questions to owner surfaces, and points validation to `AGENTS.md` with
  positive operational wording.
- Superseded by: none.

## Review Log

### 2026-05-22 - Root entry route clarified

- Previous assumption: the root README only needed to stay compact and point at
  the agent index.
- New reality: the README is also the public proof-organ entry, so it needs a
  clear question-to-route map while leaving the full pass-through chain in
  `docs/architecture/AGENT_INDEX.md`.
- Reason: low-context agents orient better from role, route, owner, output, and
  validation cues than from repeated negative self-description.
- Source surfaces updated: `README.md`, `scripts/validate_repo.py`, and
  `tests/test_validate_repo.py`.
- Validation: use root validation and the focused root README surface-role test.

### 2026-05-24 - Index owner-route language clarified

- Previous assumption: the agent index could describe its trigger as a path name
  being insufficient.
- New reality: the index should state the positive route: use it when a path
  needs an explicit owner route.
- Reason: the index is an operating map for low-context agents, so it should
  begin from owner-route recovery rather than absence or insufficiency.
- Source surfaces updated: `docs/architecture/AGENT_INDEX.md`, `scripts/validate_repo.py`,
  and `tests/test_validate_repo.py`.
- Validation: `python -m pytest -q tests/test_validate_repo.py -k agent_index`.

## Validation

Use the root and docs validation lanes in `AGENTS.md` and `docs/AGENTS.md`.
