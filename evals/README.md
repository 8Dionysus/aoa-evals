# Eval Source Index

`evals/` is the source proof object district for `aoa-evals`.
Its active shape is `evals/<claim-family>/<eval-name>/`, so an agent can read
the proof class from the path before opening the manifest.

Each bundle owns one bounded eval claim. The strongest local meaning for that
claim lives in the bundle's `EVAL.md` and `eval.yaml`, with support artifacts
kept beside the bundle when they help the claim remain reviewable.

## Operating Card

| Field | Route |
|---|---|
| role | source eval package tree for bundle-local proof objects |
| input | source proof question, bundle lookup, claim-family path, manifest question, or support-artifact question |
| output | source bundle route, generated reader route, mechanic support route, or validation route |
| owner | bundle-local `EVAL.md` and `eval.yaml` own claim meaning; `evals/AGENTS.md` owns source-tree edit law |
| next route | `EVAL_SELECTION.md`, `EVAL_INDEX.md`, `generated/README.md`, `mechanics/proof-object/README.md`, or the nearest bundle |
| tools | eval source validator, catalog builders, report-index builder, and semantic AGENTS validator |
| validation | [evals/AGENTS.md#validation](AGENTS.md#validation) and root [AGENTS.md#verify](../AGENTS.md#verify) |

## Source Chain

Read a bundle through this chain:

```text
evals/<claim-family>/<eval-name>/
-> EVAL.md
-> eval.yaml
-> notes, checks, examples, reports, fixtures, runners, or local contracts
-> generated catalog/readers
-> docs and mechanics maps only for wider route context
```

The root readers, generated catalogs, and mechanics maps route the bundle back
to its bundle-local claim wording.

## Required Core

Every active bundle should expose:

- `EVAL.md` for public claim wording, scope, verdict posture, blind spots, and
  interpretation boundaries;
- `eval.yaml` for machine-readable metadata, dependency refs, comparison
  posture, and evidence refs;
- at least one support artifact under bundle-local `notes`, `checks`, or
  `examples` when the bundle is part of the public starter surface.

## Claim Families

Top-level family directories should match the active claim posture:

- `workflow/`
- `boundary/`
- `artifact/`
- `stress/`
- `capability/`
- `comparison/fixed-baseline/`
- `comparison/peer-compare/`
- `comparison/longitudinal-window/`

For non-comparison evals, the first family segment mirrors `category` in
`eval.yaml`. For comparison evals, the `comparison/*` branch mirrors
`baseline_mode`.

## Support Artifacts

Small support files are evidence atoms with routes recoverable from owner
surfaces.

Common support atoms:

- `notes/origin-need.md`: why this eval exists and what overread it prevents;
- `checks/eval-integrity-check.md`: the smallest local integrity review for the
  bundle's claim;
- `evals/<family>/<eval>/examples/example-report.md`: a human-readable example of
  the bundle's report posture;
- local report schemas or runner contracts when the bundle has materialized
  proof artifacts.

These files may be short. Route recovery comes from `EVAL.md`, `eval.yaml`,
this index, and
[EVAL_INDEX](../EVAL_INDEX.md).

## Selection Surfaces

Use these root readers to choose a bundle:

- [Eval Bundle Selection Chooser](../EVAL_SELECTION.md) for a quick chooser by question;
- [Eval Bundle Index](../EVAL_INDEX.md) for the full public bundle map;
- [Documentation Map](../docs/README.md) for guide and mechanic context.

Use these generated readers when tooling needs compact projections:

- `generated/eval_catalog.json`
- `generated/eval_catalog.min.json`
- `generated/eval_capsules.json`
- `generated/eval_sections.full.json`

Generated readers are derived from source bundle content and rebuild through
their builders.

## Mechanic Links

Mechanics support source eval packages while bundle-local files keep eval
meaning.

- Proof-object owns eval authoring and eval contract support.
- Proof-infra owns reusable fixture, runner, scorer, and reportable-contract
  support.
- Comparison-spine owns fixed-baseline, peer-compare, and repeated-window
  readout support.
- Audit owns selected runtime evidence and artifact-to-verdict bridge support.
- Release-support owns release readiness, closeout, and handoff report support.

When an eval package needs narrower operation support, route to the owning
mechanic part from the eval-local evidence path or from
[Mechanics](../mechanics/README.md).

## Validation

Executable bundle validation routes live in
[evals/AGENTS.md#validation](AGENTS.md#validation) and the target bundle's
owning proof-object route. This source index names what bundle artifacts are
and how they relate. Executable command ownership stays in the route cards
named above.
