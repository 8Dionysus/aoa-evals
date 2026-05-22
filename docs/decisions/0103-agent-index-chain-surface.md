# 0103 Agent Index Chain Surface

## Status

Accepted.

## Context

The repository now has enough route cards, topology maps, mechanics parents,
part contracts, generated readers, decisions, and validators that a future
agent can still lose the chain between a path name and its authority class.

The root README must stay compact, `docs/PROOF_TOPOLOGY.md` must keep authority
classes rather than become a dispatcher, and `AGENTS.md` must own executable
route law. Putting the whole agent route chain into any one of those surfaces
would either bloat an entrypoint or hide route-law detail in the wrong place.

## Decision

Add `docs/AGENT_INDEX.md` as an agent-facing pass-through index for the chain:

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
- Tradeoff: `docs/AGENT_INDEX.md` must stay a read model. If it starts carrying
  commands, source truth, or decision rationale, it should be trimmed and routed
  back to the owning surface.

## Validation

Use the root and docs validation lanes in `AGENTS.md` and `docs/AGENTS.md`.
