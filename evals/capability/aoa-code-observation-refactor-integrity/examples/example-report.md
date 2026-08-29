# Example Report

## Bundle

- bundle: `aoa-code-observation-refactor-integrity`
- bundle shape: `capability`
- status: `draft`
- verdict: `supports bounded contract`
- machine-readable raw input: `fixtures/observation-report.example.json`
- machine-readable summary: `reports/example-report.json`

## Bounded Readout

The synthetic `refactor-torture-v1` family covers twelve operation cases:
rename, move, signature change, add, delete, import change, multi-file impact,
split, merge, stale index, delta/full parity, and affected-test selection.
The example envelope passes all twelve contract checks.

The positive readout means only that the supplied envelope keeps declared
lineage, freshness, invalidation, provenance, metric, parity, reproducibility,
and affected-test fields internally coherent for these synthetic cases.

## Interpretation Boundary

This example does not prove provider correctness, parser or index quality,
LSP/KAG currentness, production latency, canonical owner truth, proof
acceptance, deployment, runtime, transport, or owner acceptance. The bundle
remains `draft`, `review_required`, and not export-ready.
