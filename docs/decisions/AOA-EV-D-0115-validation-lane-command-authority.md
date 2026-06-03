# Validation Lane Command Authority

- Decision ID: AOA-EV-D-0115
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `docs/validation/`, `scripts/validation_lanes.py`, `scripts/release_check.py`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, root/topology, generated/readout
- Mechanic parents: cross-parent
- Guard families: route residue, generated/report/receipt/runtime, decision index/read-model
- Posture: active rationale

## Context

The validator/test/script refactor needs one command authority before more
validator domains move out of `scripts/validate_repo.py`.

Sibling repositories already moved lane command storage into explicit manifests
and loaders, but `aoa-evals` has a local constraint: root `config/` is currently
a route-card-only compatibility district. Adding an active root-config command
payload would force a topology change before the validator refactor has its own
validation lane. Current root-config routes stay documented in
`config/README.md` and `config/AGENTS.md`.

The immediate pressure is to make release, source-fast, generated, part-local,
pinned-sibling, latest-sibling, trace/eval, audit, nightly, and advisory lane
boundaries visible without changing eval bundle meaning.

## Options Considered

- Keep command sequences in `AGENTS.md`, `scripts/release_check.py`, workflow
  YAML, and tests.
- Copy the sibling shape exactly and promote root `config/` into an active
  command-payload district.
- Put the lane manifest under `docs/validation/`, add a loader and inventories,
  and leave root `config/` route-card-only for this slice.

## Decision

`docs/validation/validation_lanes.json` is the active validation lane command
manifest for `aoa-evals`.

`scripts/validation_lanes.py` loads that manifest. `scripts/ci_gate.py` executes
named lanes. `scripts/release_check.py` remains the local release entrypoint,
but it now reads the release command sequence from the lane manifest.

`docs/validation/validator_inventory.json`,
`docs/validation/script_inventory.json`, and `docs/testing/test_inventory.json`
are descriptive topology inventories. They do not store blocking command
sequences.

## Rationale

This preserves the local proof topology while giving the refactor a real command
surface. The lane manifest makes it possible to split validators, tests, and
scripts by owner boundary without letting each slice invent a private command
sequence.

Keeping the manifest under `docs/validation/` avoids a premature root-config
payload promotion. If root `config/` later becomes an active command district,
that should be a separate topology decision with route-card guard updates.

## Consequences

- Positive: release command order now has one manifest-backed source.
- Positive: future validator and script splits have lane ids and inventories to
  update.
- Positive: latest-sibling canary and pinned-sibling compatibility are explicit
  and separate from local release identity.
- Tradeoff: the manifest path differs from `aoa-skills`, `aoa-memo`, and
  `aoa-techniques` because `aoa-evals` currently protects root `config/` as
  route-card-only.
- Follow-up: continue extracting validator domains from `scripts/validate_repo.py`
  into focused modules and split `tests/test_validate_repo.py` by owner surface.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validator
  entrypoint while domain modules continue to split out.
- Changed: release, source-fast, generated, part-local, sibling, trace/eval,
  audit, nightly, and advisory lane boundaries now have a manifest and focused
  topology tests.
- Superseded by: none.

## Boundaries

This decision does not make generated validators source-meaning owners.

It does not make advisory runtime policy, trace grading, memory/RAG authority,
inter-agent execution, observability policy, security enforcement, or sibling
path existence hard gates.

It does not promote root `config/` into an active command payload district.

## Validation

- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_test_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
