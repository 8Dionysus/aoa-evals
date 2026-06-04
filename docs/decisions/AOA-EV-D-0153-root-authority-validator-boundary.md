# Root Authority Validator Boundary

- Decision ID: AOA-EV-D-0153
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/root_authority.py`, root authority, proof topology, design, legacy, and agent-route guard family

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: none
- Guard families: source/topology
- Posture: active rationale

## Context

Root authority validation protects the authored surfaces that tell agents what
the repo is, where proof meaning lives, and which route owns a boundary:
`DESIGN.md`, `DESIGN.AGENTS.md`, root `AGENTS.md`, `.github/AGENTS.md`,
`.agents/`, `AUDIT.md`, `docs/architecture/PROOF_TOPOLOGY.md`,
`docs/architecture/AGENT_INDEX.md`, `docs/architecture/LEGACY_NAMING.md`, and
decision route surfaces.

Before this split, `scripts/validate_repo.py` still held these checks beside
source eval contracts, generated parity, guidance routes, mechanics topology,
runtime audit, release support, and route-residue checks. That made the root
entrypoint look like a second source of root authority instead of an
orchestrator.

## Decision

Root authority, design, proof-topology, legacy naming, agent-lane, audit/GitHub
route, index-role, read-model command ownership, memory proof boundary, and
decision-status validation lives in `scripts/validators/root_authority.py`.

The module owns:

- root design and architecture posture checks;
- proof topology token and stale-scaffold checks;
- legacy naming posture, single-bridge, and external archive-detail checks;
- agent index chain, root index-role, and validator-surface posture checks;
- `.agents/` and `.agents/spark/` lane route checks;
- `.github/AGENTS.md` and root audit route checks;
- read-model command ownership for non-executable reader surfaces;
- memory-as-context proof boundary checks;
- atomic decision status line checks.

`scripts/validate_repo.py` remains the repo-wide entrypoint and delegates this
domain to the module. Tests import `validators/root_authority.py` directly
instead of using root wrappers.

## Rationale

These checks are source/topology authority boundaries. They protect the route
from repo identity to source truth, generated readers, mechanics, runtime
evidence, release evidence, and agent-facing handoff surfaces.

They do not define source eval meaning, generated projection parity, runtime
policy, trace/eval outcomes, release artifact identity, or mechanic payload
meaning. They only verify that root-authored authority surfaces keep those
boundaries visible and command ownership routed.

## Consequences

- Positive: `validate_repo.py` no longer exports root authority, design,
  proof-topology, legacy naming, agent-index, audit/GitHub, read-model command
  ownership, decision-status, or agent-lane wrapper checks.
- Positive: root authority tests now import the focused module directly.
- Positive: root authority has its own inventory, residual ledger row, and
  module topology entry.
- Follow-up: remaining root mechanics orchestration and command-ownership
  checks should split only by coherent owner boundary.

## Current Applicability

As of 2026-06-04:

- Still valid: root authority surfaces must point agents toward the real owner
  of source truth, generated parity, runtime evidence, mechanics payloads,
  audit evidence, and release evidence.
- Changed: root authority/design/proof/legacy/agent route checks moved from
  `scripts/validate_repo.py` to `scripts/validators/root_authority.py`.
- Superseded by: none.

## Boundaries

This decision does not let root authority validators own generated parity,
source-eval contract meaning, runtime policy, trace grading, live release
publication evidence, or mechanic payload details.

It does not make root route prose a proof source.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/root_authority.py`
- `python -m pytest -q tests/test_root_surface_roles.py tests/test_read_model_command_ownership.py tests/test_index_surface_roles.py`
- `python scripts/validate_repo.py`
