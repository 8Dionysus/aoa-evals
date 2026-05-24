# Artifact/Process Paired Proof Flow v1

This dossier defines the first materialized paired proof flow across:
- `aoa-artifact-review-rubric`
- `aoa-bounded-change-quality`
- `aoa-output-vs-process-gap`

## Shared case family

Use `mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v1/README.md` as the shared public case-family contract.

The paired read should preserve:
- one visible request surface
- one artifact-side read
- one process-side read
- one honest paired read after both sides are visible

## Read order

1. Read artifact quality with `aoa-artifact-review-rubric`.
2. Read workflow quality with `aoa-bounded-change-quality`.
3. Read the divergence or alignment with `aoa-output-vs-process-gap`.
4. If the pairing is being used for a maturity wave, add `aoa-eval-integrity-check` as the sidecar that checks whether the paired public read is still bounded and non-theatrical.

## Required paired shapes

- artifact outruns process
- process outruns artifact
- broadly aligned
- mixed or noise-limited and no honest winner

## Distinctness boundary

This paired flow routes artifact/process comparison through
`aoa-output-vs-process-gap`.

`aoa-trace-outcome-separation` asks whether outcome and path should stay separate.
This dossier asks whether artifact quality and process quality diverge or align on the same bounded cases.

## Route Checks

| Pressure | Route |
| --- | --- |
| one scalar score | paired verdict plus side-by-side interpretation |
| baseline-default comparator | fixed-baseline part route and source `baseline_mode` |
| one side always matters more | bundle-local claim review |
| root-cause diagnosis for every divergence | diagnosis owner route with paired evidence as support |
