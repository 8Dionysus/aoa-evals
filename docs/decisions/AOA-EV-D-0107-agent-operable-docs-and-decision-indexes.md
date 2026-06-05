# Agent-operable Docs And Decision Indexes

- Decision ID: AOA-EV-D-0107
- Status: Accepted
- Date: 2026-05-25
- Owner surface: `docs/README.md`, `docs/decisions/`, `scripts/generate_decision_indexes.py`, focused decision-index validator modules

## Index Metadata

- Original date: 2026-05-25
- Surface classes: root/topology, generated/readout, validation guard
- Mechanic parents: none
- Guard families: decision index/read-model
- Posture: active rationale

## Context

`aoa-evals/docs/` has grown from a small documentation map into the proof
organ's agent-facing orientation layer. The current shape preserved proof law,
legacy routing, mechanics topology, and decision rationale, but several
surfaces started carrying too much orientation weight at once.

The most visible pressure is `docs/decisions/README.md`: it is simultaneously
the decision-lane entrypoint, chronological index, surface-class crosswalk,
mechanic-parent crosswalk, and validation-guard crosswalk. That makes the
entrypoint costly for agents to read and forces `scripts/validate_repo.py` to
carry many hardcoded index-token checks.

The broader docs refactor needs a positive operating map: role, input, output,
owner, next route, tools, and validation. The goal is not to delete proof law.
The goal is to put law, rationale, generated lookup, and validation contracts
on surfaces that match their authority.

## Options Considered

- Keep the decision README as the single hand-maintained index and tolerate the
  weight.
- Move crosswalk sections into separate hand-maintained files while leaving
  decision metadata implicit.
- Make decision notes carry explicit index metadata and generate lookup indexes
  from that source metadata.

## Decision

Decision notes now carry a short `## Index Metadata` block naming surface
classes, mechanic parents, guard families, and posture.

The decision lookup crosswalks are generated read models under
`docs/decisions/indexes/`:

- `by-number.md`
- `by-surface.md`
- `by-mechanic.md`
- `by-validation-guard.md`

`docs/decisions/README.md` becomes the entrypoint and authority explainer. It
routes to generated indexes instead of owning every crosswalk by hand.

`scripts/generate_decision_indexes.py` builds the read models. The original
decision-index validator aggregate validated metadata, index contract, and
generated parity; AOA-EV-D-0218 later split that aggregate into focused
decision-record, renderer, lane-surface, and generated-parity modules.
`scripts/validate_repo.py` remains the repo-wide entrypoint while delegating
this contract to focused decision-index validator modules.

## Rationale

This makes the decision layer more agent-operable without weakening rationale.
The source decision remains the canonical explanation of why a route exists.
The generated index is only a lookup surface, so an agent can find the right
decision without spending context on every crosswalk.

Moving the contract into a focused validator module starts the desired
validator refactor in the direction of an orchestrator model. It also prevents
the new index shape from becoming an unverified docs convention.

## Consequences

- Positive: decision lookup becomes cheaper for agents while rationale stays in
  numbered decision notes.
- Positive: the validator can check generated parity instead of requiring every
  crosswalk token in the decision README.
- Tradeoff: every future decision needs an `Index Metadata` block.
- Tradeoff: crosswalk edits now go through the generator and metadata contract.
- Follow-up: move the wider `docs/` tree into architecture, guides, and
  operations folders after the decision index route is stable.

## Current Applicability

As of 2026-05-25:

- Still valid: decision notes own rationale; generated indexes are read models.
- Changed: decision lookup metadata is source-owned by each decision note.
- Changed: AOA-EV-D-0218 removes the original decision-index validator aggregate
  and splits parsing, rendering, lane topology, and generated parity.
- Superseded in part by: AOA-EV-D-0218 for decision-index validator splitting.

## Boundaries

This decision does not make generated decision indexes authoritative rationale.

It does not complete the full `docs/architecture`, `docs/guides`, and
`docs/operations` migration.

It does not move proof topology guard prose by itself; that belongs in the
later route-residue guard-map slice.

## Validation

Use the docs-decision generator and repo validators:

- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
