# Root Authority Validator Boundary

- Decision ID: AOA-EV-D-0153
- Status: Accepted
- Date: 2026-06-04
- Owner surface: root source/topology guard family

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

Root authority facade, agent-lane, audit/GitHub route, index-role, read-model
command ownership, memory proof boundary, validator posture, and
decision-status validation initially moved into
`scripts/validators/root_authority.py`. AOA-EV-D-0196 later removes that
aggregate and splits these checks into focused root validators.

The module owns:

- agent index chain, root index-role, and validator-surface posture checks;
- `.agents/` and `.agents/spark/` lane route checks;
- `.github/AGENTS.md` and root audit route checks;
- read-model command ownership for non-executable reader surfaces;
- memory-as-context proof boundary checks;
- atomic decision status line checks.

`scripts/validate_repo.py` remains the repo-wide entrypoint and delegates this
domain through `root_topology.py`. Current tests import focused root modules
directly instead of using root wrappers.

Root design/proof topology now delegates to `scripts/validators/root_design.py`.
Legacy naming posture now delegates to `scripts/validators/root_legacy.py`
through compatibility aliases and thin wrappers.

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
  proof-topology, agent-index, audit/GitHub, read-model command ownership,
  decision-status, or agent-lane wrapper checks.
- Positive: root authority tests now import the focused module directly.
- Positive: root authority has its own inventory, residual ledger row, and
  module topology entry.
- Positive: legacy naming posture has a separate validator boundary under
  AOA-EV-D-0171.
- Positive: root design and proof-topology posture has a separate validator
  boundary under AOA-EV-D-0172.
- Follow-up: remaining root mechanics orchestration and command-ownership
  checks should split only by coherent owner boundary.

## Current Applicability

As of 2026-06-04:

- Still valid: root authority surfaces must point agents toward the real owner
  of source truth, generated parity, runtime evidence, mechanics payloads,
  audit evidence, and release evidence.
- Changed: root authority/design/proof/agent route checks moved from
  `scripts/validate_repo.py` to root validator modules; legacy naming posture
  later moved to `scripts/validators/root_legacy.py`; root design and
  proof-topology posture later moved to `scripts/validators/root_design.py`; the
  remaining `root_authority.py` aggregate is later removed.
- Superseded by: AOA-EV-D-0171 for legacy naming posture checks; AOA-EV-D-0172
  for root design and proof-topology posture checks; AOA-EV-D-0196 for root
  aggregate removal.

## Boundaries

This decision does not let root authority validators own generated parity,
source-eval contract meaning, runtime policy, trace grading, live release
publication evidence, or mechanic payload details.

It does not make root route prose a proof source.

Root design and proof-topology posture routes to
`scripts/validators/root_design.py`. Legacy naming posture routes to
`scripts/validators/root_legacy.py`. Remaining root authority checks route to
the focused modules named by AOA-EV-D-0196; no compatibility aggregate remains.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
