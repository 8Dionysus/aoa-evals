# Root Authority Aggregate Removal

- Decision ID: AOA-EV-D-0196
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused root source/topology validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: none
- Guard families: source/topology, observability/audit
- Posture: active rationale

## Context

AOA-EV-D-0153 moved root authority checks out of `scripts/validate_repo.py`.
AOA-EV-D-0171 and AOA-EV-D-0172 later split legacy naming and root
design/proof topology into focused modules. The remaining
`scripts/validators/root_authority.py` file still carried unrelated root
boundaries: agent index, `.agents/` lanes, audit/GitHub route cards, memory
proof boundary, read-model command ownership, decision status, index roles, and
validator surface roles.

That file had become a root aggregate rather than an owner boundary.

## Decision

`scripts/validators/root_authority.py` is removed.

Root source/topology validation now routes through focused modules:

- `root_agent_index.py` owns the agent-index chain.
- `root_agent_lanes.py` owns `.agents/` and Spark route posture.
- `root_audit_routes.py` owns audit and GitHub route-card posture.
- `root_memory_boundary.py` owns memory-as-context proof boundary checks.
- `root_read_model_commands.py` owns executable command ownership on read-model
  surfaces.
- `root_index_surfaces.py` owns root index heading/role checks.
- `root_validator_surfaces.py` owns scripts/tests AGENTS surface role checks.
- `root_decision_status.py` owns atomic decision status-line checks.
- `root_common.py` is helper-only token lookup and markdown command parsing.

`root_topology.py` orchestrates these modules directly. Tests import the focused
module that owns the checked surface.

## Rationale

Root-authored surfaces protect different boundaries. A GitHub route card is not
a memory proof-boundary, an agent index is not a validator route-card, and a
decision status-line check is not root design.

Keeping those checks behind one `root_authority.py` aggregate invited every
future root-shaped rule to land in the same broad bucket. Direct focused modules
keep failures close to the owner surface and make the root topology
orchestrator explicit.

## Consequences

- Positive: no root authority aggregate/facade validator remains.
- Positive: root tests and inventories now name concrete root owner surfaces.
- Positive: root design and legacy validators no longer route through a
  compatibility file.
- Tradeoff: `root_topology.py` imports more focused root validators because it is
  the root source/topology orchestrator.

## Current Applicability

As of 2026-06-04:

- Still valid: root-authored surfaces must point agents toward source truth,
  generated parity, runtime evidence, mechanics payloads, audit evidence, and
  release evidence.
- Changed: those checks no longer share `root_authority.py`.
- Supersedes: the remaining aggregate shape left by AOA-EV-D-0153,
  AOA-EV-D-0171, and AOA-EV-D-0172.

## Boundaries

This decision does not let focused root validators own generated parity,
source-eval meaning, runtime outcomes, trace grading, live release state, proof
verdicts, or mechanic payload details.

It does not create a replacement root aggregate under another name.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
