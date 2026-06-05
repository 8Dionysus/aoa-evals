# Root Guidance Aggregate Removal

- Decision ID: AOA-EV-D-0202
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused root front-door, eval-guide, operations, and release guidance validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: none
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0152 moved root guidance checks out of `scripts/validate_repo.py` and
into `scripts/validators/root_guidance.py`. That module still mixed separate
front-door and guidance owner surfaces:

- root README and docs route-map posture;
- eval philosophy, portability, score semantics, eval review, and blind-spot
  proof-guide posture;
- closeout writeback ingress and public contribution route posture; and
- release guide route-map posture.

Those surfaces are all source/topology guidance guards, but they route to
different owners and should not share one aggregate module.

## Decision

`scripts/validators/root_guidance.py` is removed.

Root guidance validation now routes through focused modules:

- `root_frontdoor_guidance.py` owns root README compactness and docs route-map
  reader posture.
- `root_eval_guides.py` owns eval philosophy, portable eval boundary, score
  semantics, eval review, and blind-spot disclosure guide posture.
- `root_operations_guidance.py` owns closeout writeback ingress, its boundary
  decision token check, and `CONTRIBUTING.md` route posture.
- `root_release_guidance.py` owns the release guide route-map posture.
- `root_guidance_common.py` is helper-only token and markdown-command logic.

`root_topology.py` calls each focused validator directly.

## Rationale

Guidance validators should protect entry and route posture without turning
root prose into hidden proof authority. A single root guidance aggregate made
front-door docs, proof guides, operations notes, contribution policy, and release
route language look like one historical gate.

Splitting keeps repair routes specific: README drift does not route through the
release guide, score semantics drift does not route through docs front-door
maps, and closeout ingress does not become proof-guide meaning.

## Consequences

- Positive: no root guidance aggregate validator remains.
- Positive: root front-door, eval guide, operations, and release guide failures
  now name separate owner modules.
- Positive: shared token helpers are helper-only and have no guidance authority.
- Tradeoff: tests import the focused validator for the surface they mutate.

## Current Applicability

As of 2026-06-04:

- Still valid: root guidance surfaces route proof meaning to source bundles,
  generated readers, mechanic parts, operations guides, or owner decisions
  instead of carrying hidden payload authority.
- Changed: root guidance behavior no longer lives in `root_guidance.py`; it is
  split across focused root guidance validators.
- Supersedes: the aggregate module shape left by AOA-EV-D-0152.

## Boundaries

This decision does not let root guidance validators own generated parity,
source-eval contract meaning, runtime policy, trace grading, live release
publication evidence, or route-card-only root district topology.

It does not make guidance prose a proof source and does not create a replacement
root guidance aggregate under another name.

## Validation

- `python -m py_compile scripts/validators/root_guidance_common.py scripts/validators/root_frontdoor_guidance.py scripts/validators/root_eval_guides.py scripts/validators/root_operations_guidance.py scripts/validators/root_release_guidance.py scripts/validators/root_topology.py tests/test_docs_topology.py tests/test_root_surface_roles.py tests/test_route_residue.py tests/test_guidance_surface_routes.py`
- `python -m pytest -q tests/test_guidance_surface_routes.py tests/test_docs_topology.py tests/test_route_residue.py tests/test_root_surface_roles.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
