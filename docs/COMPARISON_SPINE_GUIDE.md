# Comparison Spine Guide

This guide defines how the current public comparison and regression surfaces fit together as one bounded program layer inside `aoa-evals`.

Use it when the question is no longer "what is a baseline?" in the abstract,
but rather:
- which comparison surface should I read first?
- what kind of bounded claim does each comparison mode support?
- when does `aoa-eval-integrity-check` need to travel as the integrity sidecar?

See also:
- [Documentation Map](README.md)
- [Baseline Comparison Guide](BASELINE_COMPARISON_GUIDE.md)
- [Artifact Process Separation Guide](ARTIFACT_PROCESS_SEPARATION_GUIDE.md)
- [Eval Selection](../EVAL_SELECTION.md)

## Current public comparison ladder

The current public ladder is:

`one-run anchor surfaces -> fixed-baseline -> peer-compare -> longitudinal-window -> integrity sidecar`

Current public comparison bundles:
- `aoa-regression-same-task`
- `aoa-output-vs-process-gap`
- `aoa-longitudinal-growth-snapshot`
- `aoa-eval-integrity-check`

This ladder is intentionally asymmetric:
- `aoa-regression-same-task` is the first and only public `baseline` default
- `aoa-output-vs-process-gap` remains a draft peer-comparison bridge
- `aoa-longitudinal-growth-snapshot` remains a draft repeated-window movement surface
- `aoa-eval-integrity-check` remains the bounded integrity sidecar, not a promotion shortcut

## Comparison modes

### `fixed-baseline`

Current bundle:
- `aoa-regression-same-task`

Use when:
- one candidate is being compared against one frozen baseline target
- the same bounded task family remains visible and stable
- the question is regression detection, not broad growth

Current machine-readable contract should keep explicit:
- anchor surface
- shared family path
- baseline target label
- paired readout path
- integrity sidecar

### `peer-compare`

Current bundle:
- `aoa-output-vs-process-gap`

Use when:
- two peer readings are being compared side by side on the same bounded cases
- neither side is the automatic default truth source
- the question is divergence or alignment, not default baseline comparison

Current machine-readable contract should keep explicit:
- shared family path
- peer surfaces
- matched surface
- paired readout path
- integrity sidecar

### `longitudinal-window`

Current bundle:
- `aoa-longitudinal-growth-snapshot`

Use when:
- ordered named windows stay on one bounded workflow surface
- the question is modest movement across windows
- report polish must stay weaker than movement evidence

Current machine-readable contract should keep explicit:
- anchor surface
- shared family path
- window family label
- paired readout path
- integrity sidecar

## Read order

Read the comparison spine in this order:

1. Read the one-run anchor surface first.
2. Read `fixed-baseline` when the question is candidate-versus-frozen-target regression.
3. Read `peer-compare` when the question is side-by-side divergence on the same bounded cases.
4. Read `longitudinal-window` when the question is ordered movement across named windows on one bounded surface.
5. Add `aoa-eval-integrity-check` when public wording, routing, maturity posture, or generated contracts are moving enough that the comparison read could start implying more than the evidence carries.

Shared public read-order artifact:
- `../reports/comparison-spine-proof-flow-v1.md`

## Anti-overread rules

Do not collapse the current comparison spine into:
- one global score
- proof of broad capability growth
- proof that one clean same-task comparison explains every nearby diagnostic change
- proof that a draft bridge or longitudinal surface inherited baseline status by association

Default honesty rules:
- style-only movement is not capability movement by default
- peer-comparison is not baseline by association
- repeated-window movement is not general growth by association
- integrity sidecar success is not direct agent-quality proof

## Status discipline

Status remains intentionally conservative:
- `aoa-regression-same-task` stays the only default public `baseline` surface
- `aoa-output-vs-process-gap` stays `draft`
- `aoa-longitudinal-growth-snapshot` stays `draft`
- `aoa-eval-integrity-check` stays `bounded`

This means:
- hardening contracts may advance faster than public status
- richer machine-readable surfaces do not imply promotion by themselves
- promotion review remains separate from comparison-surface hardening

## Machine-readable surfaces

Use these generated surfaces when routing or local runtime selection needs explicit comparison metadata:
- `../generated/eval_catalog.json`
- `../generated/eval_capsules.json`
- `../generated/comparison_spine.json`

`generated/comparison_spine.json` is the minimal filtered projection for comparison bundles only.
It should stay aligned with bundle manifests, bundle-local proof artifacts, and public reader wording.
