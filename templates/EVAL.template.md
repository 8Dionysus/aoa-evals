---
name: eval-name
category: capability
status: draft
summary: One-sentence summary of the eval bundle.
object_under_evaluation: agent
claim_type: bounded
baseline_mode: none
report_format: summary
technique_dependencies: []
skill_dependencies: []
---

# eval-name

## Intent

What this eval is trying to learn or prove in a bounded way.

State bundle shape explicitly:
- `composite` if the bundle checks whether an end-to-end bounded workflow holds together
- `diagnostic` if the bundle isolates one nearby failure surface or review question

## Object under evaluation

What is being evaluated:
- agent
- workflow
- artifact class
- policy surface
- change across versions
- other bounded object

Also make explicit:
- whether this bundle is `composite` or `diagnostic`
- what nearby surfaces are intentionally included
- what nearby surfaces are intentionally excluded

## Bounded claim

State the claim this eval is designed to support.

Good form:
- under these conditions, the agent can do X with Y level of quality
- under these conditions, the workflow avoids Z failure mode
- across these fixtures, version B is not worse than version A on this bounded surface

Bad form:
- the agent is good
- the workflow is safe
- this proves overall intelligence

## Trigger boundary

Use this eval when:
- case 1
- case 2
- case 3

Do not use this eval when:
- case 1
- case 2
- case 3

## Inputs

- fixture set or case surface
- evaluated agent, mode, or version
- runner or execution assumptions
- scoring or rubric configuration
- baseline or comparison target if applicable

If `baseline_mode` is `longitudinal-window`, also make explicit:
- ordered named windows
- one public report or summary artifact per window
- context notes that affect comparability

## Fixtures and case surface

Describe:
- what kinds of cases are included
- what is intentionally excluded
- whether fixtures are static, generated, or mixed
- what makes this surface representative enough for the bounded claim
- whether the fixtures are public-safe
- what another repo would need to preserve when replacing the fixtures

## Scoring or verdict logic

Explain how results are interpreted.

Possible shapes:
- rubric-based review
- scalar score with interpretation contract
- categorical verdict
- pass / fail / signal
- comparison against baseline
- mixed method

Make explicit:
- whether the main result is per-case, bundle-level, or both
- the evidence hierarchy from direct observed evidence to final summary
- what counts as success
- what counts as regression
- what counts as ambiguous result
- what `mixed support` means for this bundle if used
- which scores or verdicts should not be over-interpreted

## Baseline or comparison mode

Describe the comparison surface:
- none
- fixed baseline
- previous version
- peer agent
- alternate policy or mode
- longitudinal window

If there is no baseline, say what kind of claim remains possible without one.

If comparison exists, also say:
- what counts as improvement
- what counts as regression
- what should only be treated as noisy variation
- how style-only changes are kept from looking like capability growth

If `report_format` is `comparative-summary`, also ship a tracked `support_note` evidence entry that names the comparison contract.

Make that note explicit:
- for `fixed-baseline` or `previous-version`, state the baseline target, what counts as noisy variation, and why style-only change is not enough
- for `peer-compare`, state the matched conditions and the limits of side-by-side interpretation
- for `longitudinal-window`, state the ordered windows, the cross-window invariants, and the cautious movement language

If the comparison is longitudinal:
- name why the windows are comparable
- state what would force a `mixed or unstable` or `no clear directional movement` read

## Execution contract

Describe how to run the eval reproducibly:
- runner assumptions
- execution order
- retries or no retries
- deterministic vs non-deterministic expectations
- required environment boundaries

## Outputs

- compact report artifact
- bundle-level verdict or comparison summary
- per-case breakdown if needed
- regression signal if applicable
- interpretation note

For public starter bundles, also ship:
- `notes/origin-need.md` or another tracked `origin_need` evidence note
- `examples/example-report.md`
- explicit manifest evidence entries for public support artifacts
- an integrity-review artifact such as `checks/eval-integrity-check.md`

## Failure modes

Name the main ways this eval can fail as an instrument:
- fixture overfitting
- scorer bias
- environment instability
- style substitution for quality
- false pass from shallow compliance
- hidden private context
- metric gaming
- other bounded failure modes

## Blind spots

Name what this eval does not prove.

Also name when relevant:
- likely false-pass paths
- likely false-fail or misleading-result paths
- nearby claim classes that should use a different bundle instead

Examples:
- long-term reliability
- performance outside the fixture family
- safety under adversarial tool use
- transfer to different domains
- artifact quality beyond this rubric surface

## Interpretation guidance

Tell the reader how to read the result.

Examples:
- treat this as a regression detector, not a total quality measure
- treat a pass as support for the bounded claim, not proof of general capability
- use this together with another eval family before making stronger claims
- say what this bundle should not be used to diagnose if it is `composite`
- say what this bundle intentionally does not cover if it is `diagnostic`

## Verification

- confirm the bounded claim is explicit
- confirm fixtures match the stated scope
- confirm scoring logic is reviewable
- confirm blind spots are named
- confirm the output does not imply stronger conclusions than the eval supports
- confirm manifest evidence is explicit and resolves publicly
- confirm status-shaped evidence is present when needed:
  `bounded` should carry a `support_note` with approve/defer bounded review outcome plus failure/readout distinctions;
  `portable`, `baseline`, and `canonical` should carry `portable_review`;
  `canonical` should also carry `canonical_readiness`
- confirm `EVAL_INDEX.md` and `EVAL_SELECTION.md` stay aligned if this bundle is a current public starter

## Technique traceability

List upstream techniques that shaped this eval design.

## Skill traceability

List skills this eval checks directly, uses as reference behavior, or compares.

## Adaptation points

Project overlays may add:
- local fixtures
- local runners
- local report sinks
- local baseline references
- local safety or approval rules
