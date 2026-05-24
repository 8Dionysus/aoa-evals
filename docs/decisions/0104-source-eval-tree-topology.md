# 0104 Source Eval Tree Topology

## Status

Accepted.

## Current Applicability

As of 2026-05-24:

- Still valid: `evals/<claim-family>/<eval-name>/` is the active source eval
  package tree, and recursive discovery remains required.
- Clarified: the entry surfaces for that tree are also agent operating cards:
  `EVAL_SELECTION.md`, `EVAL_INDEX.md`, and `evals/README.md` expose role,
  input, output, owner, next route, tools, and validation.
- Clarified: the root chooser and index now express first-bundle selection,
  comparison, diagnostic, artifact/process, and repeated-window choices as
  direct route criteria with neighboring surfaces named where the question
  belongs elsewhere.
- Source surfaces updated: `EVAL_SELECTION.md`, `EVAL_INDEX.md`,
  `evals/README.md`, `scripts/validate_repo.py`, and
  `tests/test_validate_repo.py`.
- Validation route: `evals/AGENTS.md#validation` and root `AGENTS.md#verify`.

## Review Log

### 2026-05-24 - Eval entry surfaces became operating cards

- Previous assumption: the source eval tree path and `evals/AGENTS.md` route
  card were enough for agents to recover the source eval chain.
- New reality: low-context agents benefit from the same operating-card fields
  on root chooser, root index, and source index surfaces.
- Reason: the source eval chain is now part of the repo-wide agent index path,
  so the entry route should state role, input, output, owner, next route, tools,
  and validation before a reader opens a bundle.
- Source surfaces updated: `EVAL_SELECTION.md`, `EVAL_INDEX.md`,
  `evals/README.md`, validator tokens, and validator tests.
- Validation: use the source-tree topology path in
  `evals/AGENTS.md#validation` plus root `AGENTS.md#verify`.

### 2026-05-24 - Root chooser and index route language clarified

- Previous assumption: the root chooser and public starter index could use
  contrast phrasing to separate neighboring eval surfaces.
- New reality: low-context agents select better when the chooser names the
  active route directly: task-meaning ambiguity, source-owned antifragility,
  owner-first stress recovery, outcome/path separation, tool-path discipline,
  narrow diagnostics, same-task regression, artifact review, and longitudinal
  movement.
- Reason: `EVAL_SELECTION.md` and `EVAL_INDEX.md` are source-eval entry
  surfaces; they should send the reader to the right bundle or neighboring
  route before bundle-local proof meaning is read.
- Source surfaces updated: root eval selection chooser and public eval index.
- Validation: source-tree topology and root validation routes.

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
