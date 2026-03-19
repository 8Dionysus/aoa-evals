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

## Object under evaluation

What is being evaluated:
- agent
- workflow
- artifact class
- policy surface
- change across versions
- other bounded object

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

## Fixtures and case surface

Describe:
- what kinds of cases are included
- what is intentionally excluded
- whether fixtures are static, generated, or mixed
- what makes this surface representative enough for the bounded claim

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
- what counts as success
- what counts as regression
- what counts as ambiguous result
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

## Execution contract

Describe how to run the eval reproducibly:
- runner assumptions
- execution order
- retries or no retries
- deterministic vs non-deterministic expectations
- required environment boundaries

## Outputs

- compact report artifact
- verdict or score summary
- per-case breakdown if needed
- regression signal if applicable
- interpretation note

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

## Verification

- confirm the bounded claim is explicit
- confirm fixtures match the stated scope
- confirm scoring logic is reviewable
- confirm blind spots are named
- confirm the output does not imply stronger conclusions than the eval supports

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
