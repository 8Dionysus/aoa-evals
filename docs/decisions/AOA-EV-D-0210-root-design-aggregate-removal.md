# Root Design Aggregate Removal

- Decision ID: AOA-EV-D-0210
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused root design and proof-topology validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, root/topology, source/topology
- Mechanic parents: none
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0172 moved root design and proof-topology checks out of
`root_authority.py`, but the replacement `scripts/validators/root_design.py`
kept two different root boundaries in one module:

- DESIGN, DESIGN.AGENTS, AGENTS, architecture proof model, and decision-lane
  route checks; and
- PROOF_TOPOLOGY, proof-topology decision, route-residue companion, and ROADMAP
  topology posture checks.

Those surfaces are adjacent, but they fail through different owner routes.

## Options Considered

- Keep `root_design.py` as the broad root design/proof-topology owner.
- Keep `root_design.py` as a delegating compatibility facade.
- Remove the aggregate and let `root_topology.py` call focused root validators.

## Decision

`scripts/validators/root_design.py` is removed.

Active root design validation now routes through:

- `root_design_docs.py` for root design, agent design, architecture proof model,
  decision-lane route, and active-mechanics wording checks.
- `root_proof_topology.py` for proof-topology, proof-topology decision, route
  residue companion, and roadmap topology posture checks.
- `root_design_common.py` for helper-only path constants and token-loading
  companion lookup.

`root_topology.py` calls the focused validators directly.

## Rationale

Root design explains the proof organ and agent-facing source route. Proof
topology explains the topology of source proof objects, derived readers,
candidate evidence, mechanics, legacy lineage, and route-residue guards. They
must agree, but one validator should not become the catch-all for every root
topology or roadmap phrase.

## Consequences

- Positive: root design and proof-topology failures now route to the correct
  owner surface.
- Positive: root agent validators depend only on shared path constants instead
  of importing a broad design validator.
- Tradeoff: root topology orchestration imports two focused validators.

## Current Applicability

As of 2026-06-04:

- Still valid: root design, architecture proof model, proof topology, and
  roadmap topology posture remain blocking source/topology gates.
- Changed: the broad `root_design.py` module no longer exists.
- Supersedes: AOA-EV-D-0172 for aggregate root-design validator shape.

## Boundaries

This decision does not move proof verdicts, generated parity, runtime outcomes,
mechanic payload meaning, release evidence, or source eval meaning into root
design or proof-topology validators.

It also does not make `root_design_common.py` a compatibility facade; it is
helper-only.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
