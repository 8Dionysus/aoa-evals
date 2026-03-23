---
name: aoa-regression-same-task
category: regression
status: baseline
summary: Compares a candidate against a frozen baseline on the same bounded task family to detect material regression without claiming general growth.
object_under_evaluation: same-task bounded workflow regression against a frozen baseline
claim_type: regression
baseline_mode: fixed-baseline
report_format: comparative-summary
comparison_surface:
  shared_family_path: fixtures/frozen-same-task-v1/README.md
  paired_readout_path: reports/same-task-baseline-proof-flow-v1.md
  integrity_sidecar: aoa-eval-integrity-check
  selection_question: Do you need a frozen-baseline comparison on the same bounded task family?
  anchor_surface: aoa-bounded-change-quality
  baseline_target_label: RS-v1 frozen bounded workflow reference
technique_dependencies:
  - AOA-T-0001
skill_dependencies:
  - aoa-change-protocol
---

# aoa-regression-same-task

## Intent

Use this eval to check whether a candidate regresses against a frozen baseline on the same bounded task family.

This baseline bundle is a `comparative` regression eval.
It is not a one-run workflow starter.
It is not meant to prove general capability growth or decline beyond the fixed comparison surface.

The goal is not to prove that one agent is globally better.
The goal is to test one bounded claim:

on the same bounded task family and against a frozen baseline,
the candidate does not materially regress on the chosen workflow surface,
or the regression is made visible enough to review directly.

## Object under evaluation

This eval checks same-task bounded workflow regression against a frozen baseline.

Primary surfaces under evaluation:
- candidate performance relative to the fixed baseline on the same cases
- whether regressions are visible even when style or presentation changes
- whether comparison remains bounded to the frozen task family
- whether the final comparative reading stays modest about what the comparison proves

Nearby surfaces intentionally excluded:
- general capability growth across broader task families
- long-term movement across time windows
- artifact-only excellence outside the bounded workflow comparison
- total replacement of one-run starter bundles for root-cause diagnosis

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
the candidate does not materially regress against the frozen baseline
on this same-task bounded workflow surface.

This eval does **not** support claims such as:
- the candidate is generally better than the baseline everywhere
- the candidate improved overall intelligence or engineering quality
- the candidate will generalize the same way to different task families
- one comparative run replaces root-cause workflow diagnostics

## Trigger boundary

Use this eval when:
- you need a fixed baseline comparison on the same bounded task family
- the main question is regression rather than one-run workflow quality
- style-only changes could otherwise look like progress
- the comparison surface is stable enough to freeze for bounded review

Do not use this eval when:
- you only need one-run workflow quality and no baseline exists yet
- the task family is still changing underneath the comparison
- the comparison target is not actually frozen
- the main question is longitudinal trend rather than same-task regression; use `aoa-longitudinal-growth-snapshot`

## Inputs

- frozen baseline run or baseline artifact set
- candidate run on the same bounded cases
- bounded task family and case contract
- comparison rubric
- captured workflow evidence needed for the chosen comparison surface
- final comparative summary

## Fixtures and case surface

This baseline bundle should use only bounded change tasks with a frozen case family.

A strong starter fixture set should include:
- repeatable bounded change tasks shared by baseline and candidate
- cases where style-only differences are plausible
- cases where workflow regressions can appear even if outputs still look polished
- cases where the baseline itself is reviewable enough to serve as a frozen comparison target

Fixture families should avoid:
- moving or still-being-written case sets
- giant heterogeneous scenario soups
- comparisons that depend on hidden local reviewer context
- cases where baseline capture is too thin to support a bounded review

The fixture surface is public-safe when:
- a bounded outside reviewer can inspect how the baseline was frozen
- the candidate and baseline are compared on the same visible cases
- another repo could replace the case family with a comparable frozen bounded set and preserve the same regression question

The current materialized shared family is `fixtures/frozen-same-task-v1/README.md`.

## Scoring or verdict logic

This eval prefers a comparative bundle-level verdict with per-case comparison notes.

Suggested verdict classes:
- `no material regression`
- `mixed regression signal`
- `regression present`

Per-case review should ask:
- what did the baseline establish on this case?
- what did the candidate change on the same case?
- is the difference an actual regression, a plausible improvement, or only noisy variation?
- could style or formatting changes be masquerading as capability movement?
- does the comparative summary preserve the same bounded comparison visible in the evidence?

Per-case comparison notes may also record `bounded improvement present`
when the candidate is reviewably stronger on the same frozen surface.
That does not force a stronger bundle-level growth claim by itself.

Bundle-level reading should stay downstream of per-case comparison notes.
If case evidence materially diverges, prefer `mixed regression signal` over a cleaner-looking aggregate claim.

### Approve signals

Signals toward `no material regression`:
- the candidate stays at least as strong as the frozen baseline on the reviewed surface
- style-only shifts are not over-read as capability movement
- per-case comparison notes remain bounded to the visible evidence
- the final comparative summary stays modest about what changed

### Degrade signals

Signals toward `mixed regression signal` or `regression present`:
- the candidate loses reviewable strengths the baseline had on the same cases
- polished presentation masks weaker workflow behavior than the baseline
- style-only changes are mistaken for genuine improvement
- the comparison surface drifts away from the frozen baseline contract
- the final summary overstates what the bounded comparison actually proved

### Baseline review outcome language

- `approve for baseline` means the frozen target, comparison rubric, and public readout are stable enough for bounded reuse.
- `defer for now` means the comparison surface is still too local-shaped, too unstable, or too easy to overread for baseline status.

### Regression vs noisy variation

- `regression present` means the candidate lost a reviewable strength the frozen baseline had on the same surface.
- `no material regression` means the candidate preserved the frozen baseline's reviewable strengths closely enough for the bounded claim.
- `noisy variation` means the visible difference is too weak, too style-shaped, or too ambiguous to justify a stronger comparison claim.

## Baseline or comparison mode

This baseline bundle uses `fixed-baseline`.
Its machine-readable comparison surface is anchored in `aoa-bounded-change-quality`,
uses the shared family `fixtures/frozen-same-task-v1/README.md`,
publishes through `reports/same-task-baseline-proof-flow-v1.md`,
and should carry `aoa-eval-integrity-check` whenever a public maturity, wording, or baseline-contract wave could otherwise turn the same-task read theatrical.

The baseline should be frozen before candidate comparison begins.
The same bounded case family should be used for both baseline and candidate.

The public v1 baseline target should stay named explicitly in the report.
A compact baseline label such as `RS-v1 frozen bounded workflow reference` is enough,
as long as the frozen target is inspectable and stable across comparison runs.

In this surface:
- improvement means the candidate is reviewably stronger on the bounded comparison surface
- regression means the candidate loses a reviewable strength the baseline had
- noisy variation means the difference is too weak or too style-driven to support a stronger claim

Style-only changes should not be treated as capability growth by default.

## Execution contract

A careful run should:
1. freeze the baseline run or baseline artifacts for the chosen bounded cases
2. run the candidate on the same bounded cases
3. capture the evidence needed for the comparison surface
4. review per-case baseline and candidate differences against the comparison rubric
5. derive a comparative summary only after the per-case notes exist
6. publish a comparative-summary artifact plus a bounded bundle-level regression verdict

Execution expectations:
- do not rewrite the case family after seeing the candidate
- do not move the baseline target after freezing it
- do not let style-only presentation shifts masquerade as capability movement
- keep the named frozen baseline target visible in the public report
- keep enough evidence that a careful reviewer can see why each comparative note was assigned
- when shipping a machine-readable report, validate it against `reports/summary.schema.json`
- keep the same-task baseline read compatible with `reports/same-task-baseline-proof-flow-v1.md`

## Outputs

The eval should produce:
- one bundle-level comparative verdict
- per-case comparison notes
- the named frozen baseline target
- baseline-strength summary
- candidate-change summary
- regression or no-regression reading
- noisy-variation notes where the comparison should stay weaker
- explicit interpretation note
- an optional schema-backed companion report artifact at `reports/example-report.json`

A compact public comparative-summary may include:
- baseline target
- case id
- baseline note
- candidate note
- comparative reading
- bundle-level verdict
- caution about what the result still does not prove

## Failure modes

This eval can fail as an instrument when:
- the baseline is not actually frozen
- the case family drifts between runs
- comparison notes reward style instead of bounded workflow evidence
- the baseline itself is too weak or opaque to anchor review
- the candidate and baseline are compared on mismatched evidence surfaces
- one clean comparison is treated as proof of general growth

## Blind spots

This eval does not prove:
- general capability growth
- long-term trend movement across windows
- improvement outside the frozen case family
- root-cause diagnosis for why a regression appeared
- total workflow quality outside the bounded comparison surface

Likely false-pass path:
- the candidate avoids obvious regressions on the frozen cases, but broader workflow quality still weakens elsewhere.

Likely misleading-result path:
- a baseline with weak evidence capture can make the candidate look cleaner or noisier than it really is.

Nearby claim classes that should use a different bundle instead:
- one-run bounded workflow quality should use `aoa-bounded-change-quality`
- broader outcome-vs-path split should use `aoa-trace-outcome-separation`
- movement across repeated windows should use `aoa-longitudinal-growth-snapshot`

## Interpretation guidance

Treat a positive result as support for one bounded claim:
on this frozen same-task surface,
the candidate did not materially regress against the baseline.

Do not treat a positive result as:
- proof of general capability growth
- proof that the candidate is universally better than the baseline
- proof that no nearby diagnostic regression exists
- proof that the same result will hold on different task families

Use this bundle together with one-run starter bundles
when you need both:
- a bounded regression read
- and a narrower root-cause diagnosis for why the comparison moved

Use `aoa-longitudinal-growth-snapshot`
when the main question is ordered movement across windows rather than one frozen same-task baseline.

A negative or mixed result is valuable because it can reveal:
- reviewable same-task regression
- style-vs-substance confusion
- baseline drift
- comparative overclaiming

## Verification

- confirm the bounded claim is explicit
- confirm the baseline is actually frozen
- confirm baseline and candidate use the same case family
- confirm per-case comparison notes remain grounded in inspectable evidence
- confirm the named baseline target remains visible in the public report
- confirm the bundle-level verdict does not outrun the comparison evidence

## Technique traceability

Primary source techniques:
- AOA-T-0001 plan-diff-apply-verify-report

## Skill traceability

Primary checked skill surface:
- aoa-change-protocol

## Adaptation points

Project overlays may add:
- local frozen baseline capture rules
- local bounded case families
- local comparative report formats that still preserve per-case evidence
- repo-specific comparison rubrics
- later stronger baseline-readiness evidence
