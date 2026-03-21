---
name: aoa-tool-trajectory-discipline
category: workflow
status: bounded
summary: Checks whether an agent uses tools in a disciplined, reviewable way on bounded tasks where the tool path itself is part of the bounded claim.
object_under_evaluation: tool-use trajectory discipline in bounded agent change workflows
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies:
  - AOA-T-0001
skill_dependencies:
  - aoa-change-protocol
---

# aoa-tool-trajectory-discipline

## Intent

Use this eval to check whether an agent uses tools in a disciplined, reviewable way on bounded tasks where the tool path itself matters.

This bounded bundle is a `diagnostic` workflow eval.
It isolates tool-use trajectory discipline.
It is not meant to stand in for a broader end-to-end workflow eval or a general outcome-quality judgment.

The goal is not to prove one ideal tool sequence.
The goal is to test one bounded claim:

under bounded tasks where the tool path is part of the claim,
the agent can use tools in a disciplined, proportionate, and reviewable way
without unnecessary churn, avoidable omissions, or opaque path theater.

## Object under evaluation

This eval checks tool-use trajectory discipline inside a bounded agent change workflow.

Primary surfaces under evaluation:
- whether the chosen tools fit the visible task and path requirements
- whether obvious tool-supported checks are skipped when they materially matter
- whether tool use stays proportionate instead of becoming churn or theater
- whether the resulting tool path remains reviewable to a bounded outside reader

Nearby surfaces intentionally excluded:
- overall workflow quality end to end
- final outcome quality when path does not materially matter
- claimed-vs-actual verification evidence as its own root-cause surface
- one exact tool sequence as the only acceptable path

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
the agent can use tools with disciplined path quality
on bounded tasks where tool-use trajectory is part of the bounded claim.

This eval does **not** support claims such as:
- the overall workflow was strong in every respect
- the final artifact is excellent overall
- the agent always chooses the globally optimal tool sequence
- the same tool discipline will generalize to all tasks or environments

## Trigger boundary

Use this eval when:
- the task is bounded and the tool path materially affects reviewability or risk
- the main question is whether tools were used with disciplined sequencing and proportionality
- the same outcome could be reached through either disciplined or noisy trajectories
- path quality matters for the claim rather than being decorative process commentary

Do not use this eval when:
- the main question is overall workflow quality rather than tool path quality
- the main question is outcome-vs-path separation at a broader level
- the final outcome is enough and tool-path review would add theater instead of evidence
- the environment does not expose enough tool evidence for bounded path review

## Inputs

- bounded task
- starting repository or sandbox state
- allowed tools and permissions
- captured tool calls or equivalent path evidence
- visible task rationale for why tool path matters here
- final report or execution summary

## Fixtures and case surface

This bounded bundle should use only bounded tasks where tool path matters to the claim.

A strong starter fixture set should include:
- a case where tool sequencing materially affects reviewability
- a case where unnecessary tool churn creates path noise without adding evidence
- a case where an obvious tool-backed check is skipped and that omission matters
- a case where the same outcome can be reached by either a disciplined or noisy trajectory
- a case where tool misuse hides risk or collapses reviewability

Fixture families should avoid:
- outcome-only tasks where path review would be performative
- cases with no visible tool evidence
- giant operational scenarios with hidden infrastructure dependencies
- cases where one exact sequence is hard-coded as the only acceptable path

The fixture surface is public-safe when:
- a bounded outside reviewer can inspect the tool evidence
- the reason path matters is visible in the case contract
- another repo could replace the cases with comparable bounded tasks where tool trajectory materially affects the same claim

## Scoring or verdict logic

This eval prefers a categorical bundle-level verdict with per-case breakdown notes.

Suggested verdict classes:
- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Per-case review should ask:
- why does tool path matter on this case?
- were the chosen tools proportionate to the task?
- were obvious tool-supported checks skipped when they materially mattered?
- did the path stay reviewable without unnecessary churn?
- did the final summary preserve why the path was judged the way it was?

Bundle-level reading should stay downstream of per-case notes.
If case evidence materially diverges, prefer `mixed support` over a cleaner-looking pass.

### Approve signals

Signals toward `supports bounded claim`:
- tools are chosen in a way that fits the visible task
- sequencing remains disciplined without performative extra churn
- obvious tool-supported checks are used when they materially matter
- multiple acceptable paths remain possible without requiring one exact sequence
- the final report preserves why the path was judged as disciplined

### Degrade signals

Signals toward `mixed support` or `does not support bounded claim`:
- unnecessary tool churn creates noise rather than evidence
- obvious path-relevant checks are skipped without explanation
- tool use is decorative rather than claim-supporting
- the path becomes too opaque for bounded review
- the final summary launders weak tool use into a cleaner-looking workflow story

### Review outcome language

- `approve` means the trajectory reading stayed reviewable on this surface.
- `defer` means the evidence is too thin, too mixed, or too overstated for bounded promotion.

### Failure vs readout

- failure is the mismatch between the visible tool-path evidence and the trajectory claim
- readout is the public wording that summarizes that mismatch
- a clean readout cannot repair omitted or noisy tool evidence
- a clumsy readout does not by itself invalidate a supported path judgment

## Baseline or comparison mode

This bounded bundle uses `none`.

It is a standalone diagnostic proof surface.
A later baseline form may compare:
- the same agent before and after tool-use policy changes
- different tool-use strategies on the same bounded cases
- different repos using comparable path-sensitive tasks

Without a baseline, this bundle supports only modest claims about observed tool-trajectory discipline on the chosen cases.

## Execution contract

A careful run should:
1. present one bounded path-sensitive case at a time
2. capture why tool path matters on that case
3. capture the visible tool evidence
4. review the tool path against the trajectory rubric
5. record a per-case trajectory note plus why-path-matters note
6. publish a summary-with-breakdown artifact plus a bounded bundle-level verdict

Execution expectations:
- do not invent tool-path importance after the fact
- do not require one ideal sequence when multiple disciplined paths are plausible
- do not treat decorative tool usage as positive evidence
- keep enough evidence that a careful reviewer can see why the trajectory note was assigned
- keep approve/defer language separate from the failure/readout split

## Outputs

The eval should produce:
- one bundle-level verdict
- per-case breakdown notes
- trajectory note for each case
- why-path-matters note for each case
- visible omission or churn summary
- an explicit approval-or-defer readout for the bounded promotion review
- explicit interpretation note

A compact public summary-with-breakdown may include:
- case id
- why path matters here
- trajectory note
- major path-strength or path-failure signal
- bundle-level verdict
- caution about what the result still does not prove

## Failure modes

This eval can fail as an instrument when:
- the reason path matters is not visible in the case contract
- reviewers overfit to one preferred tool sequence
- tool evidence is incomplete or hidden
- decorative tool usage is mistaken for disciplined workflow
- outcome-only success is allowed to wash away tool-path weakness
- one clean trajectory is treated as proof of general workflow maturity

## Blind spots

This eval does not prove:
- overall workflow quality
- final outcome quality when path does not matter
- verification truthfulness as a standalone diagnostic question
- scope alignment as a standalone diagnostic question
- stable behavior across time unless used later in comparative form

Likely false-pass path:
- the visible tool path looks disciplined, but the final outcome is still weak on a different surface.

Likely misleading-result path:
- a case where path does not truly matter may make a noisy trajectory look more important than it really is.

Nearby claim classes that should use a different bundle instead:
- end-to-end workflow quality should use `aoa-bounded-change-quality`
- broader outcome-vs-path separation should use `aoa-trace-outcome-separation`
- claimed-vs-actual verification evidence should use `aoa-verification-honesty`

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the agent can use tools with disciplined, reviewable path quality
on this bounded surface where tool trajectory itself matters.

Do not treat a positive result as:
- proof that the overall workflow was strong
- proof that the final artifact is excellent
- proof that one exact tool sequence is required
- proof that the same tool discipline will hold on all tasks or environments

Use this bundle together with `aoa-trace-outcome-separation`
when you need both:
- a broader outcome-vs-path split
- and a narrower judgment about tool-use path quality

Use this bundle together with `aoa-bounded-change-quality`
when you need both:
- a composite workflow signal
- and a narrower read on whether tool-use trajectory helped or hurt that workflow

A negative or mixed result is valuable because it can reveal:
- tool churn
- avoidable path omissions
- opaque tool sequencing
- decorative tool-use theater

## Verification

- confirm the bounded claim is explicit
- confirm fixtures explain why tool path matters on each case
- confirm per-case notes remain grounded in visible tool evidence
- confirm the bundle-level verdict does not outrun the case evidence
- confirm the promotion note keeps approve/defer language separate from failure/readout language
- confirm blind spots and nearby-bundle boundaries are named clearly

## Technique traceability

Primary source techniques:
- AOA-T-0001 plan-diff-apply-verify-report

## Skill traceability

Primary checked skill surface:
- aoa-change-protocol

## Adaptation points

Project overlays may add:
- local path-sensitive bounded tasks
- local tool classes or tool policies
- repo-specific tool-review expectations
- local summary formats that still preserve why-path-matters evidence
- later comparison baselines for repeated runs
