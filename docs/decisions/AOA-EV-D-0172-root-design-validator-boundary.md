# Root Design Validator Boundary

- Decision ID: AOA-EV-D-0172
- Status: Superseded
- Superseded by: AOA-EV-D-0210-root-design-aggregate-removal
- Date: 2026-06-04
- Owner surface: `scripts/validators/root_design.py`, `DESIGN.md`, `docs/architecture/PROOF_TOPOLOGY.md`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: none
- Guard families: source/topology
- Posture: active rationale

## Context

`scripts/validators/root_authority.py` still carried root design, agent-facing
design, architecture proof model, proof topology, active-mechanics wording, and
roadmap topology posture checks alongside agent-lane, audit/GitHub, memory,
index-role, read-model command ownership, decision-status, and delegated legacy
checks.

Root design/proof topology is a coherent source/topology boundary. It explains
what the proof canon is, how generated/read-model surfaces relate to source
truth, and how mechanics fit into the proof organ. That boundary should not be
mixed with every root authority check.

## Decision

Root design and proof-topology validation lives in
`scripts/validators/root_design.py`.

The module owns:

- `DESIGN.md` proof-organ posture checks;
- `DESIGN.AGENTS.md` agent-facing design route checks;
- `docs/architecture/ARCHITECTURE.md` proof model posture checks;
- `docs/architecture/PROOF_TOPOLOGY.md` source/generated/mechanics topology
  checks;
- decision-template and decision-surface design-token checks;
- architecture proof model and active-mechanics topology wording decision
  checks; and
- roadmap stale topology wording checks.

`root_topology.py` calls `root_design.py` directly. The former
`root_authority.py` compatibility aggregate is removed by AOA-EV-D-0196.

## Rationale

Root design/proof topology protects the source-of-truth map. It is not the same
boundary as GitHub route posture, `.agents/` lanes, index roles, command
ownership, memory-as-context, or decision-status hygiene.

The split keeps the route from design to proof topology visible while preventing
`root_authority.py` from remaining the repository's catch-all root validator.

## Consequences

- Positive: root design and proof-topology checks have their own validator,
  inventory entry, mechanics ledger row, and decision rationale.
- Positive: root design/proof topology no longer routes through the root
  authority aggregate.
- Historical note: this split originally kept compatibility aliases in
  `root_authority.py`; AOA-EV-D-0196 removes that aggregate.
- Tradeoff: the design validator still reads decision indexes and route-residue
  companion text because those are part of the root design/proof topology
  surface.

## Current Applicability

As of 2026-06-04:

- Still valid: root design and proof topology must keep source truth, generated
  readers, mechanics, memory context, and proof interpretation boundaries
  explicit.
- Changed: root design, architecture proof model, proof topology,
  active-mechanics wording, decision-template, and roadmap topology posture
  checks moved out of `root_authority.py`; active validation later split into
  `root_design_docs.py`, `root_proof_topology.py`, and helper-only
  `root_design_common.py`.
- Superseded by: AOA-EV-D-0210 removes the `root_design.py` aggregate.
- Further changed by: AOA-EV-D-0196 removes the remaining root authority
  aggregate.

## Boundaries

This decision does not make root design validators the owner of source eval
meaning, generated parity, proof verdicts, runtime policy, trace grading,
release state, mechanic payload meaning, legacy archive payload accounting, or
GitHub/agent lane operation.

It checks root-authored design and proof topology posture only.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
