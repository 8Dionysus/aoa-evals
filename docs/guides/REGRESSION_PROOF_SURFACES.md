# Regression Proof Surfaces

## Role

This guide is the root-owned map for regression proof in `aoa-evals`.

Use it when a report, bundle, comparison read, or runtime-adjacent packet claims
that a candidate preserved a previously promised behavior.

It keeps regression proof bounded: a regression surface may show that selected
service promises survived the candidate. Broader quality, safety, completeness,
or upgrade pressure routes to the owner that can carry that claim.

## Operating Card

| Field | Route |
| --- | --- |
| role | root regression-proof route map for bounded preservation claims |
| input | service-promise preservation claim, fixed-baseline pressure, repeated-window pressure, release/closeout regression pressure, runtime-candidate regression pressure, or generated-reader regression pressure |
| output | regression proof chain, surface-family route, interpretation boundary, or anti-overread route |
| owner | this guide owns docs-level regression routing; bundle-local proof objects, comparison-spine parts, audit packets, and release-support parts own concrete evidence |
| next route | [Baseline Comparison Guide](BASELINE_COMPARISON_GUIDE.md), [Comparison Spine Guide](COMPARISON_SPINE_GUIDE.md), [Repeated Window Discipline Guide](REPEATED_WINDOW_DISCIPLINE_GUIDE.md), [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md), `mechanics/comparison-spine/`, `mechanics/audit/`, `mechanics/release-support/`, or the affected bundle |
| validation | [docs/AGENTS.md#validation](../AGENTS.md#validation) and the nearest owner route card |

## Owner Split

`aoa-evals` owns:

- bounded regression claim wording;
- comparison and interpretation boundaries;
- bundle-local verdict meaning;
- report and fixture contracts that make the regression read reviewable;
- root guidance for choosing the right regression surface.

Mechanic-owned payload stays below the operation that owns the evidence:

- fixed baseline fixtures and repeated-window reports stay under
  `mechanics/comparison-spine/parts/`;
- source eval claims and bundle-local reports stay under `evals/**/`;
- runtime candidate evidence stays under audit or receipt support until reviewed;
- release-readiness evidence stays under `mechanics/release-support/parts/`.

## Regression Proof Chain

Read a regression claim through this chain:

```text
service promise
-> bounded source bundle or selected evidence packet
-> comparison mode
-> fixture or report payload
-> interpretation boundary
-> validation guard
-> decision or provenance trail when the route changed
```

This chain is intentionally narrower than a roadmap. It answers what survived,
what evidence says so, and which stronger readings route elsewhere.

## Surface Families

### Fixed Baseline

Use fixed-baseline proof when one candidate is compared against one frozen
target on the same bounded task family.

Primary routes:

- [Baseline Comparison Guide](BASELINE_COMPARISON_GUIDE.md)
- [Comparison Spine Guide](COMPARISON_SPINE_GUIDE.md)
- `mechanics/comparison-spine/parts/fixed-baseline/`
- `evals/comparison/fixed-baseline/aoa-regression-same-task/`

The claim shape is candidate-versus-frozen-target preservation; broad growth
routes to growth/progression owner review.

### Repeated Window

Use repeated-window proof when named windows stay on one bounded surface and the
question is movement across time.

Primary routes:

- [Repeated Window Discipline Guide](REPEATED_WINDOW_DISCIPLINE_GUIDE.md)
- `mechanics/comparison-spine/parts/longitudinal-window/`
- `evals/comparison/longitudinal-window/aoa-longitudinal-growth-snapshot/`
- `evals/comparison/longitudinal-window/aoa-stress-recovery-window/`

The claim shape is cautious movement or recovery inside a named window family.
When the job, fixture, or interpretation boundary changes, the read routes
through repeated-window review before carrying clean regression comparison.

### Release And Closeout Regression

Use release-support proof when the question is whether release-readiness,
handoff, or closeout promises remain reviewable.

Primary routes:

- [Releasing `aoa-evals`](../operations/RELEASING.md)
- `mechanics/release-support/README.md`
- `mechanics/release-support/parts/readiness-audit/reports/`
- `mechanics/release-support/parts/strategic-closeout/reports/`
- `mechanics/release-support/parts/pr-handoff/reports/`

The claim shape is release process integrity. Eval bundle claim strength and
GitHub status route through their own checked evidence.

### Runtime Candidate Regression

Use runtime-candidate proof when runtime or trace evidence is being considered
as selected evidence for an eval.

Primary routes:

- `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md`
- `mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`
- [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md)

The claim shape is candidate evidence posture. Runtime evidence becomes portable
regression proof only after `aoa-evals` gives it bounded meaning.

## Anti-Overread Routes

Regression proof should name the promise, candidate, baseline or window, fixture
family, report path, and interpretation boundary.

| Pressure | Route |
| --- | --- |
| one global quality score | bundle-local verdict and score-semantics review |
| broad model ranking | comparison owner review with explicit baseline semantics |
| general agent improvement | growth/progression owner review with bounded regression evidence |
| hidden runtime health authority | runtime owner route and selected-evidence review |
| release approval | release-support evidence and GitHub landing route |
| generated reader outranks authored bundle meaning | source bundle, builder, and generated-reader parity check |

## Validation

For root regression guide or comparison-reader edits, use
[docs/AGENTS.md#validation](../AGENTS.md#validation),
[generated/AGENTS.md#validation](../../generated/AGENTS.md#validation), and the
nearest comparison-spine route card.

Use the full test suite when the edit touches bundle manifests, generated
readers, release-support reports, runtime evidence selection, or validator
contracts.
