# Summary Contract

This bundle is a `composite` workflow surface.
Its output is the `process-side reading` in the current artifact/process layer.

Use it when the main question is:
- did a bounded non-trivial change workflow hold together end to end?

Do not use it as the precise diagnostic surface for:
- claimed-vs-actual verification truthfulness
- requested-scope vs executed-scope alignment
- broader task-meaning ambiguity outside the bounded change workflow

Use `aoa-verification-honesty` when the main question is verification truthfulness.
Use `aoa-scope-drift-detection` when the main question is requested-scope vs executed-scope alignment.
Use `aoa-ambiguity-handling` when the main question is incomplete or conflicting task meaning.
Use `aoa-trace-outcome-separation` when the main question is whether outcome and path should stay separate in the readout.
Use `aoa-tool-trajectory-discipline` when the main question is tool-use path quality on cases where the path itself matters.
Use `aoa-output-vs-process-gap` when the main question is whether polished output is outrunning process discipline or vice versa.

Public summaries for this bundle should:
- keep the bounded workflow claim explicit
- distinguish bundle failure from case-level readout
- mention when case evidence materially diverges
- prefer `mixed support` over a cleaner-looking pass when nearby failure modes split
- stay compatible with the shared paired reads in `reports/artifact-process-paired-proof-flow-v1.md` and `reports/artifact-process-paired-proof-flow-v2.md` without collapsing workflow and artifact reads into one score
- keep matched conditions explicit whenever the same cases feed the downstream bridge verdict
- keep style-over-substance risk visible whenever cleaner artifact polish could look stronger than the workflow evidence
- keep any schema-backed companion report weaker than the bundle-local interpretation boundary

`aoa-witness-trace-integrity` may sit upstream as adjacent witness context,
but it does not replace the workflow discipline surface here.
