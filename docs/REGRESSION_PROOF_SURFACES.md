# Regression Proof Surfaces

## Role

This guide is the root-owned map for regression proof in `aoa-evals`.

Use it when a report, bundle, comparison read, or runtime-adjacent packet claims
that a candidate preserved a previously promised behavior.

It keeps regression proof bounded: a regression surface may show that selected
service promises survived the candidate. It does not make the assistant globally
better, safer, more complete, or generally upgraded.

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
what evidence says so, and what the read still cannot claim.

## Surface Families

### Fixed Baseline

Use fixed-baseline proof when one candidate is compared against one frozen
target on the same bounded task family.

Primary routes:

- [Baseline Comparison Guide](BASELINE_COMPARISON_GUIDE.md)
- [Comparison Spine Guide](COMPARISON_SPINE_GUIDE.md)
- `mechanics/comparison-spine/parts/fixed-baseline/`
- `evals/comparison/fixed-baseline/aoa-regression-same-task/`

The claim shape is candidate-versus-frozen-target preservation, not broad
growth.

### Repeated Window

Use repeated-window proof when named windows stay on one bounded surface and the
question is movement across time.

Primary routes:

- [Repeated Window Discipline Guide](REPEATED_WINDOW_DISCIPLINE_GUIDE.md)
- `mechanics/comparison-spine/parts/longitudinal-window/`
- `evals/comparison/longitudinal-window/aoa-longitudinal-growth-snapshot/`
- `evals/comparison/longitudinal-window/aoa-stress-recovery-window/`

The claim shape is cautious movement or recovery inside a named window family.
If the job, fixture, or interpretation boundary changed, the read is no longer a
clean regression comparison.

### Release And Closeout Regression

Use release-support proof when the question is whether release-readiness,
handoff, or closeout promises remain reviewable.

Primary routes:

- [Releasing `aoa-evals`](RELEASING.md)
- `mechanics/release-support/README.md`
- `mechanics/release-support/parts/readiness-audit/reports/`
- `mechanics/release-support/parts/strategic-closeout/reports/`
- `mechanics/release-support/parts/pr-handoff/reports/`

The claim shape is release process integrity. It does not strengthen eval bundle
claims or GitHub status beyond the evidence that was checked.

### Runtime Candidate Regression

Use runtime-candidate proof when runtime or trace evidence is being considered
as selected evidence for an eval.

Primary routes:

- `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md`
- `mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`
- [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md)

The claim shape is candidate evidence posture. Runtime evidence becomes portable
regression proof only after `aoa-evals` gives it bounded meaning.

## Anti-Overread

Regression proof should name the promise, candidate, baseline or window, fixture
family, report path, and interpretation boundary.

Avoid claims that collapse into:

- one global quality score;
- broad model ranking;
- general agent improvement;
- hidden runtime health authority;
- release approval without release-owner evidence;
- proof that a generated reader outranks authored bundle meaning.

## Validation

For root regression guide or comparison-reader edits, use
[docs/AGENTS.md#validation](AGENTS.md#validation),
[generated/AGENTS.md#validation](../generated/AGENTS.md#validation), and the
nearest comparison-spine route card.

Use the full test suite when the edit touches bundle manifests, generated
readers, release-support reports, runtime evidence selection, or validator
contracts.
