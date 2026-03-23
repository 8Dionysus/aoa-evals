---
name: aoa-eval-integrity-check
category: capability
status: bounded
summary: Checks whether current public starter bundles stay coherent across manifest contract, verdict wording, evidence coverage, and public selection surfaces, and serves as the bounded integrity sidecar for comparison-spine wording waves.
object_under_evaluation: public starter eval bundle integrity on the current aoa-evals corpus
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies: []
skill_dependencies: []
---

# aoa-eval-integrity-check

## Intent

Use this eval to check whether the current public starter bundles stay coherent enough to support only their bounded claims.

This bounded bundle is a `diagnostic` capability eval.
It is a bounded integrity sidecar and meta-eval for eval bundles themselves.
It is not meant to stand in for direct agent-behavior evaluation,
and it is not a promotion gate by itself.

If the main question is direct agent behavior, use a workflow or artifact bundle instead.
If the main question is public eval coherence, this sidecar is the right surface.

The goal is not to prove that a bundle is canonical or universally trustworthy.
The goal is to test one bounded claim:

on the current public starter corpus,
the repository can review whether manifest contract,
verdict and report wording,
blind spots,
support artifacts,
and public chooser or index wording
stay coherent enough that a bundle supports only its bounded claim and not more,
especially when polished wording, thin evidence, or nearby surfaces tempt readers into saying too much.

## Object under evaluation

This eval checks integrity of public starter eval bundles.

Primary surfaces under evaluation:
- alignment between `EVAL.md` and `eval.yaml`
- verdict-shape and report-shape coherence
- blind-spot and nearby-bundle distinctness clarity
- support-artifact and evidence coverage
- public index and selection wording coherence
- semantic anti-theater risks such as bundle blur, baseline by association, and style-heavy overread

Nearby surfaces intentionally excluded:
- direct runtime quality of the evaluated agent
- hidden fixture quality not exposed publicly
- canonical-readiness proof
- replacement of human review before status promotion

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
the repository can review whether a starter eval bundle remains internally coherent enough
to support only its stated bounded claim on the public corpus.

This eval does **not** support claims such as:
- the evaluated bundle is canonical
- the evaluated bundle is immune to gaming
- the underlying agent behavior is strong
- the entire repository is permanently trustworthy

## Trigger boundary

Use this eval when:
- a public starter bundle has grown enough that manifest, docs, and examples may drift
- the main question is whether an eval surface is overstating what it proves
- index and selection wording materially shape how outside readers will use a starter bundle
- comparative, regression, or bridge bundles need a bounded integrity read before stronger reuse
- fixed-baseline, peer-compare, or longitudinal-window surfaces are changing wording, routing, or maturity posture and need an explicit bounded integrity sidecar

Do not use this eval when:
- the main question is direct agent performance
- the main question is hidden fixture realism rather than public coherence
- the surface is still a purely local sketch with no public starter posture
- a status promotion decision needs broader review evidence than this bounded integrity read provides

## Inputs

- one current public starter bundle target at a time
- `EVAL.md`
- `eval.yaml`
- `examples/example-report.md`
- support notes and checks
- `EVAL_INDEX.md` starter row and distinctness wording
- `EVAL_SELECTION.md` current posture and chooser wording
- roadmap wording where it materially defines current or next public posture

## Fixtures and case surface

This starter bundle should review only the current public starter corpus.

A target dossier should include:
- one bundle-local spec surface
- one manifest surface
- one compact example report
- one or more support notes or checks
- one public index mapping
- one public selection mapping

Strong review classes for v1:
- manifest-to-EVAL mismatch
- verdict-shape or report-shape mismatch
- category or routing mismatch
- blind-spot or nearby-bundle distinctness weakness
- baseline or comparative semantics mismatch where applicable
- thin evidence or support coverage
- style-over-substance
- artifact/process collapse
- baseline by association
- growth by association
- peer-compare blur
- fixed-baseline drift
- longitudinal overclaim
- schema-clean but claim-overstated
- routing overreach

Target families should avoid:
- planned bundles that are not yet public starters
- hidden fixture or scorer internals not exposed in the public bundle
- generalized repo philosophy disputes with no concrete bundle surface

## Scoring or verdict logic

This eval prefers per-target integrity notes plus a categorical bundle-level verdict.

Suggested verdict classes:
- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Per-target review should ask:
- does the manifest match the public eval description?
- does verdict and report wording match the actual bundle posture?
- do blind spots keep nearby bundles distinct?
- does public selection wording route readers to the bundle honestly?
- does the support and evidence surface make the bundle reviewable enough for its current public status?

Bundle-level reading should stay downstream of the target notes.
If different targets show materially different integrity risk classes,
prefer `mixed support` over a cleaner-looking pass.

### Approve signals

Signals toward `supports bounded claim`:
- manifest fields match the public bundle posture
- report and verdict wording stay bounded and readable
- blind spots clearly point to nearby bundles where needed
- evidence and integrity artifacts make the current public surface reviewable at its stated status
- public index and chooser wording stay consistent with the bundle job

### Degrade signals

Signals toward `mixed support` or `does not support bounded claim`:
- a bundle reads as `diagnostic` in one place and `composite` in another
- summary or selection wording upgrades the bundle into a broader proof surface
- starter bundles ship weak or missing evidence support
- comparative or baseline wording drifts away from manifest semantics
- public routing collapses nearby bundles into one vague category
- schema-backed report artifacts look clean while the bounded claim is still being overstated
- a draft bridge or longitudinal surface inherits stronger status by association

### Review outcome language

- `approve for bounded promotion` means the integrity sidecar is strong enough to review starter-bundle coherence without pretending to replace broader promotion review.
- `defer for now` means the integrity surface still looks too structural, too local, or too easy to overread as stronger proof than it carries.

### Failure vs readout

- failure is semantic overreach, bundle blur, thin evidence, or routing drift in the public eval surface itself
- readout is the bounded public wording that reports that integrity risk
- a polished readout cannot repair an integrity failure underneath
- a cautious readout can still be valuable even when the bundle-level verdict stays mixed

## Baseline or comparison mode

This starter bundle uses `none`.

It is a standalone meta-eval surface.
A later stronger integrity form may compare:
- bundle integrity before and after a docs or schema revision
- the same bundle across review cycles
- starter-bundle integrity across broader maturity bands

Without a baseline, this bundle supports only modest claims about current public coherence on the chosen starter corpus.
Its current public job is to serve as the integrity sidecar for comparison-spine waves without pretending to replace direct bundle-specific comparison evidence.
In the current wave set it also serves as the anti-gaming sidecar for artifact/process pairing and repeated-window movement.

## Execution contract

A careful run should:
1. choose one current public starter bundle target
2. gather the target dossier
3. review the target against the integrity risk classes
4. assign a per-target integrity note
5. derive a bundle-level verdict from the set of reviewed starter targets
6. publish a summary-with-breakdown artifact with explicit public-status limits

Execution expectations:
- do not treat missing hidden internals as automatic failure
- do not treat a clean integrity read as proof of agent quality
- do not let roadmap or chooser wording outrun the bundle-local contract
- keep enough evidence that a careful reviewer can see why each integrity risk class was assigned
- when fixed-baseline, peer-compare, longitudinal-window, pairing, shared infra, or canonical waves materially change a public surface, carry this integrity sidecar or an equivalent bounded integrity packet
- when shipping a machine-readable report, validate it against `reports/summary.schema.json`

## Outputs

The eval should produce:
- one bundle-level verdict
- per-target integrity notes
- named integrity risk classes for each target
- support-coverage summary
- public-routing coherence summary
- explicit limitations note
- an optional schema-backed companion report artifact at `reports/example-report.json`

A compact public summary-with-breakdown may include:
- target bundle
- integrity risk class
- coherence note
- evidence-coverage note
- public-routing note
- bundle-level verdict

## Failure modes

This eval can fail as an instrument when:
- reviewers substitute taste for bounded coherence checks
- public wording changes faster than integrity notes are refreshed
- hidden local assumptions are mistaken for public defects
- one missing support artifact is treated as total bundle invalidity
- reviewers over-read this meta-eval as a promotion gate

## Blind spots

This eval does not prove:
- direct agent-behavior quality
- hidden fixture realism
- scorer calibration beyond the public bundle contract
- long-term gaming resistance
- canonical readiness by itself

Likely false-pass path:
- public wording looks coherent while thin evidence, style-heavy summaries, or shared infra drift still make the public claim stronger than the proof surface.

Likely misleading-result path:
- a starter bundle can fail this integrity read because documentation is thin for its stated public status,
  even when the underlying agent-behavior question is still valuable.

Nearby claim classes that should use a different bundle instead:
- end-to-end workflow quality should use `aoa-bounded-change-quality`
- artifact-versus-process divergence should use `aoa-output-vs-process-gap`
- same-task regression should use `aoa-regression-same-task`
- repeated-window movement should use `aoa-longitudinal-growth-snapshot`

This is the bounded integrity sidecar, not the direct agent-behavior starter.

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the current public starter bundles remain coherent enough to support their stated bounded claims modestly and reviewably.

Do not treat a positive result as:
- proof that the starter corpus is canonical
- proof that every bundle is equally mature
- proof that the underlying evaluated agents are strong
- proof that human promotion review is unnecessary

A negative or mixed result is valuable because it can reveal:
- semantic drift between manifest and prose
- public chooser overreach
- thin evidence coverage
- nearby bundles collapsing into each other conceptually
- style-only polish being mistaken for stronger proof
- baseline or growth posture being inferred by association rather than by evidence

Read the first screen as a meta-eval gate for public bundle coherence,
not as a direct measure of agent execution quality.

## Verification

- confirm the bounded claim is explicit
- confirm only current public starter bundles are reviewed
- confirm the verdict does not outrun per-target integrity notes
- confirm support and evidence coverage are inspected directly
- confirm blind spots and promotion limits are named clearly
- confirm semantic anti-theater classes such as bundle blur, baseline by association, and growth overclaiming are inspected when relevant

## Technique traceability

Technique linkage is intentionally deferred for this starter bundle.
It is a repository integrity surface rather than a direct agent-workflow technique surface.

## Skill traceability

Skill linkage is intentionally deferred for this starter bundle.
It checks bundle coherence rather than direct task-execution skill behavior.

## Adaptation points

Project overlays may add:
- local integrity review checklists
- local promotion gates
- local status-transition evidence requirements
- local bundle-family review batches
- local runner wrappers that still validate against `reports/summary.schema.json`

