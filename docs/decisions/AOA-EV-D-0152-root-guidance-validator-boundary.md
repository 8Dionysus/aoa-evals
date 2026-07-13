# Root Guidance Validator Boundary

- Decision ID: AOA-EV-D-0152
- Status: Accepted
- Date: 2026-06-04
- Historical owner surface: `scripts/validators/root_guidance.py`, root guidance and README route guard family
- Refined by: AOA-EV-D-0202

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: none
- Guard families: source/topology
- Posture: active rationale

## Context

Root guidance validation protects repo-front-door guidance surfaces: `README.md`,
`docs/README.md`, root proof guides under `docs/guides/`, operational route notes
under `docs/operations/`, and `CONTRIBUTING.md`.

Before this split, `scripts/validate_repo.py` held these route/posture checks
beside source eval contracts, generated parity, mechanics topology, runtime audit,
and release-support checks. That made root guidance look like generic root
validator glue instead of a bounded source/topology guard.

## Decision

Root guidance, README, and operations route validation lives in
`scripts/validators/root_guidance.py`.

The module owns:

- root README compact proof-canon posture;
- docs route-map posture and command-free reader paths;
- eval philosophy route wording;
- portable eval boundary guide wording;
- closeout writeback ingress route wording and its boundary decision tokens;
- contribution route posture;
- score semantics, eval review, and blind-spot disclosure guide wording;
- release guide route-map wording below live release evidence.

`scripts/validate_repo.py` remains the repo-wide entrypoint and delegates this
domain to the module. Tests import `validators/root_guidance.py` directly instead
of using root wrappers.

## Rationale

These checks are source/topology guidance boundaries. They protect how agents
and humans enter the repo, find the right owner route, and avoid mistaking
guidance prose for generated truth, runtime evidence, source eval meaning, or
live release state.

They do not validate generated reader freshness, source eval proof-object
contracts, runtime guardrails, trace/eval outcomes, release publication state, or
route-card-only root district topology.

## Consequences

- Positive: `validate_repo.py` no longer exports root guidance, docs route-map,
  release-guide, or proof-guide wrapper checks.
- Positive: guidance tests now import the focused module directly.
- Positive: root guidance has its own inventory, residual ledger row, and module
  topology entry.
- Follow-up: remaining root design, proof-topology, legacy, agent-index, and
  mechanics orchestration checks should split only by their own owner boundary.

## Current Applicability

As of 2026-06-04:

- Still valid: root guidance surfaces must route proof meaning to the correct
  source bundle, generated reader, mechanic part, operations guide, or owner
  decision instead of carrying hidden payload authority.
- Changed: root guidance/readme/operations checks moved from
  `scripts/validate_repo.py` to `scripts/validators/root_guidance.py`.
- Further changed on 2026-06-04: AOA-EV-D-0202 removes
  `scripts/validators/root_guidance.py`; active guidance validation is split
  across front-door, eval-guide, operations, release, and helper modules.
- Superseded by: AOA-EV-D-0202 for the aggregate module shape.

## Boundaries

This decision does not let root guidance validators own generated parity,
source-eval contract meaning, runtime policy, trace grading, live release
publication evidence, or route-card-only root district topology.

It does not make guidance prose a proof source.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
