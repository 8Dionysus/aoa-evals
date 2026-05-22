# 0104 Source Eval Tree Topology

## Status

Accepted.

## Context

The old `bundles/` source district made every eval package look equivalent at
the filesystem level. That was serviceable while the repo was small, but it no
longer matched how agents need to enter the proof organ: by claim family,
comparison posture, owning mechanic support, payload, and validation route.

The repo already distinguishes workflow, boundary, artifact, stress,
capability, and comparison evals in `eval.yaml`, generated catalogs, mechanics
guidance, and validation. Keeping those distinctions hidden below a flat
`bundles/<name>/` directory forced agents to infer topology from file contents
instead of seeing it in the path.

## Decision

Use `evals/<claim-family>/<eval-name>/` as the source eval package tree.

Comparison evals use one extra family level:

- `evals/comparison/fixed-baseline/<eval-name>/`
- `evals/comparison/peer-compare/<eval-name>/`
- `evals/comparison/longitudinal-window/<eval-name>/`

The claim family is derived from `eval.yaml`: normal evals use `category`, while
comparison evals use `baseline_mode`.

`evals/AGENTS.md` owns the local source package route card. Generated readers,
catalogs, report indexes, and validators must discover eval packages
recursively from `evals/**/eval.yaml` rather than assuming a flat source
district.

The word `bundle` may remain in legacy decision titles, schema fields, receipt
payloads, and historical contract wording where it names an existing external
or compatibility concept. It should not describe the active root source district
shape.

## Consequences

- Positive: an agent can see the proof family from the path before opening the
  files.
- Positive: validator, catalog, report-index, and mechanics references now
  agree on one convex source tree.
- Positive: route-card-only root districts are less tempting as hidden active
  payload homes because source eval packages are visibly grouped.
- Tradeoff: path-sensitive consumers must use recursive discovery and
  `eval.yaml`-backed family checks instead of `evals/<name>`.

## Validation

Validation routes through
[evals/AGENTS.md#validation](../../evals/AGENTS.md#validation).
Use the source-tree topology path there when changing this decision, recursive
eval discovery, generated catalog/report readers, or eval-source package
placement validators.
