# Root Context Validator Boundary

- Decision ID: AOA-EV-D-0154
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/root_context.py` and `scripts/validators/root_route_tokens.py`

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
Root route-token companion lookup lives in `scripts/validators/root_route_tokens.py`.

The module owns:

- sibling root resolution from environment variables;
- Abyss Stack source checkout resolution for source-vs-runtime mirror hygiene;
- `repo:` and named-surface reference parsing;
- strict sibling compatibility mode;
- markdown anchor lookup for repo-qualified refs;
- explicit `refresh_roots()` for latest-sibling canary overrides.

`scripts/validators/root_route_tokens.py` owns root route-token companion lookup
through decision indexes, route-residue guards, mechanic parent `AGENTS.md`,
part `VALIDATION.md`, and parts `AGENTS.md` child sections.

`scripts/validate_repo.py` remains the CLI entrypoint and domain orchestrator.
Focused validators receive context objects or helper callables from
`root_context.py` or `root_route_tokens.py`; tests and canary scripts patch
`root_context.py` directly for sibling-root overrides.

## Rationale

Repo-ref resolution and route-token lookup are boundary context, not source
eval meaning, generated parity, mechanic payload truth, runtime acceptance, or
live release evidence. Keeping them in `validate_repo.py` made every focused
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

As of 2026-06-05:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  command.
- Changed: sibling root globals, strict compatibility flags, repo-ref parsing,
  and Abyss Stack source resolution stay in `scripts/validators/root_context.py`.
  Root route-token companion lookup moved onward to
  `scripts/validators/root_route_tokens.py`.
- Superseded by: none.

## Review Log

### 2026-06-05 - Route-token lookup split from root context

- Previous assumption: repo-ref resolution and route-token companion lookup
  could share one root context module.
- New reality: sibling-root and `repo:` parsing are a different boundary from
  route-token companion lookup through decision indexes, route-residue guards,
  parent `AGENTS.md`, part `VALIDATION.md`, and parts `AGENTS.md` sections.
- Reason: `root_context.py` had become the largest validator helper and still
  behaved like a historical utility bucket after source/readout validators were
  split.
- Source surfaces updated: `scripts/validators/root_context.py`,
  `scripts/validators/root_route_tokens.py`, `scripts/validators/root_topology.py`,
  `scripts/validators/mechanics_routes.py`, validation inventories, and
  `mechanics/EVIDENCE_CLUSTERS.md`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Boundaries

This decision does not let `root_context.py` or `root_route_tokens.py` define
source eval claims, generated projection freshness, mechanic payload meaning,
runtime policy acceptance, trace/eval grading, live receipt publication, or
release artifact identity.

It does not create a second root validator. It provides context used by focused
validators.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
