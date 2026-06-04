# Root Context Validator Boundary

- Decision ID: AOA-EV-D-0154
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/root_context.py`, root validation context, sibling repo-ref, and route-token lookup boundary

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: boundary-bridge, audit, cross-parent
- Guard families: source/topology, runtime-policy route
- Posture: active rationale

## Context

After the focused validator split, `scripts/validate_repo.py` still carried
root mutable context: sibling checkout roots, `repo:` reference parsing,
strict sibling compatibility flags, markdown anchor lookup, Abyss Stack source
resolution, and route-token companion lookup for part and parent validation
routes.

That made the root CLI look like both a command entrypoint and the source of
cross-repo reference truth. Tests and the latest-sibling canary also patched
`validate_repo.py` globals directly, which kept historical coupling alive after
the focused modules already owned their validation behavior.

## Decision

Root validation context lives in `scripts/validators/root_context.py`.

The module owns:

- sibling root resolution from environment variables;
- Abyss Stack source checkout resolution for source-vs-runtime mirror hygiene;
- `repo:` and named-surface reference parsing;
- strict sibling compatibility mode;
- markdown anchor lookup for repo-qualified refs;
- root route-token companion lookup through decision indexes, route-residue
  guards, mechanic parent `AGENTS.md`, part `VALIDATION.md`, and parts
  `AGENTS.md` child sections;
- explicit `refresh_roots()` for latest-sibling canary overrides.

`scripts/validate_repo.py` remains the CLI entrypoint and domain orchestrator.
Focused validators receive context objects or helper callables from
`root_context.py`; tests and canary scripts patch `root_context.py` directly.

## Rationale

Repo-ref resolution and route-token lookup are boundary context, not source eval
meaning, generated parity, mechanic payload truth, runtime acceptance, or live
release evidence. Keeping them in `validate_repo.py` made every focused
validator look dependent on a historical mega-script.

Moving the context to a named owner makes the dependency explicit: runtime audit,
route residue, source eval dependency checks, phase-alpha matrix parity, and
latest-sibling canary execution can share resolution rules without turning the
root CLI into a utility bucket.

## Consequences

- Positive: `scripts/validate_repo.py` shrinks to domain orchestration and no
  longer stores sibling root globals, repo-ref parser functions, markdown anchor
  helpers, or route-token companion lookup.
- Positive: latest-sibling canary overrides now patch `root_context.py` and
  call `refresh_roots()` instead of mutating the CLI module.
- Positive: repo-ref parser tests, source dependency tests, runtime evidence
  tests, and phase-alpha matrix tests import the context owner directly.
- Tradeoff: older external imports of root context globals from
  `scripts/validate_repo.py` are intentionally not preserved.

## Current Applicability

As of 2026-06-04:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  command.
- Changed: sibling root globals, strict compatibility flags, repo-ref parsing,
  Abyss Stack source resolution, and route-token lookup moved to
  `scripts/validators/root_context.py`.
- Superseded by: none.

## Boundaries

This decision does not let `root_context.py` define source eval claims,
generated projection freshness, mechanic payload meaning, runtime policy
acceptance, trace/eval grading, live receipt publication, or release artifact
identity.

It does not create a second root validator. It provides context used by focused
validators.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/root_context.py mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py tests/test_runtime_evidence_surfaces.py tests/test_downstream_feed_contracts.py tests/test_generated_route_residue.py tests/validate_repo_fixtures.py tests/test_route_residue.py tests/test_mechanic_parent_topology.py tests/test_mechanic_evidence_ledger.py tests/test_mechanic_root_district_recon.py`
- `python -m pytest -q tests/test_runtime_evidence_surfaces.py tests/test_downstream_feed_contracts.py tests/test_generated_route_residue.py tests/test_route_residue.py tests/test_eval_source_topology.py tests/test_validate_repo.py tests/test_quest_and_reader_surfaces.py mechanics/boundary-bridge/parts/latest-sibling-canary/tests/test_sibling_canary.py`
