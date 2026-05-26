# Comparison Spine Fixture Parts

- Decision ID: AOA-EV-D-0040
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/comparison-spine/parts/`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: mechanic part
- Mechanic parents: comparison-spine
- Guard families: part and payload
- Posture: active rationale

## Context

Decision `0011` created `mechanics/comparison-spine/` as the route for
fixed-baseline, peer-compare, and longitudinal-window proof claims. Decision
`0029` later moved comparison-spine-owned shared dossiers into package-local
parts, but the fixture families that feed those same comparison modes remained
in root `fixtures/`.

The remaining root placement was now misleading. The families were no longer
generic fixture inventory:

- former root `fixtures/frozen-same-task-v1/` feeds fixed-baseline regression.
- former root `fixtures/bounded-change-paired-v1/` and
  `fixtures/bounded-change-paired-v2/` feed peer-compare artifact/process
  reading.
- former root `fixtures/repeated-window-bounded-v1/` feeds longitudinal-window movement.

The paths are referenced by eval frontmatter, `eval.yaml`, bundle
`evals/<family>/<eval>/fixtures/contract.json`, generated comparison readers, tests, validators, and
comparison readout dossiers.

## Options Considered

- Keep the families in root `fixtures/` as shared proof infrastructure.
- Move them under `proof-infra` because they are fixtures.
- Move only comparison-spine-owned fixture families into the active
  comparison-spine parts that already own their readout dossiers.

## Decision

Move comparison-spine-owned fixture families into package-local parts:

- `fixed-baseline/fixtures/frozen-same-task-v1/`
- `peer-compare/fixtures/bounded-change-paired-v1/`
- `peer-compare/fixtures/bounded-change-paired-v2/`
- `longitudinal-window/fixtures/repeated-window-bounded-v1/`

Bundle source truth stays in `evals/**/EVAL.md` and `evals/**/eval.yaml`.
Bundle-local fixture contracts keep pointing at the part-local fixture family
paths. Generated readers remain derived from bundle source and contracts.

## Rationale

This keeps topology convex: a future agent can see that the fixed-baseline,
peer-compare, and longitudinal-window fixture contracts belong to the same
comparison operation as their paired readout dossiers.

It also prevents a false split where the report side of a comparison mode lives
under the mechanic while the fixture side still looks like anonymous root
infrastructure.

## Boundaries

This decision does not move comparison bundles, bundle-local contracts,
schemas, runner contracts, generated readers, or stress-recovery fixture
support owned by `mechanics/antifragility/parts/stress-recovery-window/`.

It does not make a fixture family stronger than the source proof object, and it
does not turn `generated/comparison_spine.json` into source truth.

It does not turn fixed-baseline, peer-compare, or longitudinal-window results
into broad capability growth, repo-global scoring, runtime health, or sibling
owner acceptance.

## Legacy

Former root fixture paths are historical path vocabulary. The current route is
bridged by `mechanics/comparison-spine/PROVENANCE.md`; the owning legacy
archive maps the historical placement internally.

## Validation

- Bundle `comparison_surface.shared_family_path` fields point to part-local
  fixture paths.
- Bundle `evals/<family>/<eval>/fixtures/contract.json` paths match the same part-local fixture
  paths.
- `mechanics/comparison-spine/PARTS.md` names the fixture and report surfaces
  for each active part.
- Generated catalog and comparison-spine readers are rebuilt from source.
- `python scripts/build_catalog.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
