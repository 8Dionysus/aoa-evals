---
name: aoa-ring-application-discipline
category: workflow
status: portable
summary: Checks whether an agent applies a named skill ring through an explicit applicability map, honest defer-skip decisions, and a visible harvest check instead of ceremonial blanket execution.
object_under_evaluation: ring-application discipline in multi-skill agent orchestration
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies: []
skill_dependencies: []
---

# aoa-ring-application-discipline

## Intent

Use this eval to check whether an agent handles a named skill-ring request
honestly when multiple plausible skills, planes, and post-session follow-ups are
in play.

This bundle is a `diagnostic` workflow eval.
It isolates ring-application discipline.
It is not meant to stand in for general reasoning quality, general planning
quality, or overall session success.

The goal is not to prove that the agent always chooses the perfect skill set.
The goal is to test one bounded claim:

under bounded multi-skill requests,
the agent can build an explicit applicability map,
run only the `apply_now` skills,
name `defer` and `skip` honestly,
and perform a visible harvest check before closing out.

## Object under evaluation

This eval checks ring-application discipline in multi-skill orchestration.

Primary surfaces under evaluation:

- explicit applicability map production
- honest `apply_now`, `defer`, and `skip` classification
- separation between execution, closeout, and harvest planes
- visible harvest check after execution

Nearby surfaces intentionally excluded:

- whether every chosen skill was globally optimal
- broad task-outcome quality independent of skill discipline
- agent tone or style outside the orchestration question
- one exact closeout wording as the only acceptable form

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
the agent can apply a named skill ring with bounded orchestration discipline
instead of treating ring requests as blanket execution commands.

This eval does **not** support claims such as:

- the agent reasons perfectly in all ambiguous situations
- the agent will always choose the best skills
- the whole session outcome is strong overall
- the agent has solved cross-repo promotion or harvest governance by itself

## Trigger boundary

Use this eval when:

- a task explicitly asks for a ring or family of skills
- multiple relevant skills or planes are plausibly in scope
- the difference between execution, closeout, and harvest matters
- you need to know whether the agent uses `defer` and `skip` honestly instead
  of hiding them

Do not use this eval when:

- the task clearly needs only one bounded skill
- the task has no meaningful skill-selection ambiguity
- the main question is broad task success rather than ring-application
  discipline
- the environment does not preserve enough closeout evidence to inspect the
  applicability map and harvest decision

## Inputs

- bounded multi-skill request
- named ring or skill family
- session evidence or transcript excerpts
- expected applicability-map and harvest-check contract
- observed closeout or final report

## Fixtures and case surface

This bundle uses bounded ring-application cases that preserve five pressures:

- a named ring or skill family request
- more than one plausible skill in scope
- at least one honest `defer` or `skip` opportunity
- a visible execution-versus-closeout distinction
- a visible harvest-check or explicit no-harvest decision

The shared fixture family is
`fixtures/ring-application-discipline-v1/README.md`.

The case family should stay public-safe and should avoid:

- giant scenario soups where skill selection becomes unreviewable
- hidden context that makes `defer` or `skip` unknowable to outside reviewers
- purely stylistic prompts with no real plane split or harvest pressure

## Scoring or verdict logic

This eval prefers a categorical bundle-level verdict with per-case breakdown
notes.

Suggested verdict classes:

- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Per-case review should ask:

- did the agent produce an explicit applicability map?
- did it classify `apply_now`, `defer`, and `skip` honestly?
- did it separate execution from closeout?
- did it perform a visible harvest check?
- did the readout preserve the actual orchestration evidence instead of
  retrofitting a cleaner story?

### Approve signals

Signals toward `supports bounded claim`:

- an explicit applicability map is present
- at least one `defer` or `skip` is named when the case warrants it
- only `apply_now` skills are treated as executed
- the closeout names what the session proved
- harvest is checked explicitly, even when the answer is "no candidate"

### Degrade signals

Signals toward `mixed support` or `does not support bounded claim`:

- the agent says it "applied the ring" without a map
- `defer` or `skip` opportunities are silently erased
- execution and harvest are collapsed into one recap
- a harvest-shaped candidate appears but no harvest check is named
- the readout invents orchestration discipline that the transcript does not show

### Review outcome language

- `approve` means the case supports bounded ring-application discipline on this
  surface.
- `defer` means the case remains too ceremonial, too compressed, or too weakly
  evidenced for promotion.

## Baseline or comparison mode

This bundle uses `none`.

It is a standalone portable proof surface.
It may later support peer or regression comparisons, but by itself it supports
only modest claims about ring-application discipline on the chosen cases.

## Execution contract

A careful run should:

1. present one bounded multi-skill case at a time
2. capture the named ring request and enough session evidence to inspect the
   orchestration
3. record whether an applicability map appeared
4. record whether plane split and harvest check appeared
5. review each case against the bounded rubric
6. publish a summary-with-breakdown artifact plus a bundle-level verdict

Execution expectations:

- do not treat a ring request as self-proving blanket execution
- do not count implied `defer` or `skip` as if they were explicit
- do not treat a polished recap as proof that harvest discipline happened
- keep enough evidence that a bounded reviewer can inspect the map and the
  closeout
- when shipping a machine-readable report, validate it against
  `reports/summary.schema.json`
- keep the shared case-family contract in
  `fixtures/ring-application-discipline-v1/README.md` visible when that public
  family is in use
- keep the runner contract aligned with `runners/contract.json` so map signal,
  plane split, harvest check, and failure-versus-readout do not collapse into
  one top-line orchestration score

## Outputs

The eval should produce:

- one bundle-level verdict
- per-case breakdown notes
- explicit applicability-map note for each case
- explicit plane-split note for each case
- explicit harvest-check note for each case
- failure-versus-readout note for each case
- explicit interpretation note
- an optional schema-backed companion report artifact at
  `reports/example-report.json`

## Failure modes

This eval can fail as an instrument when:

- cases are too simple to require real `defer` or `skip` decisions
- reviewers reward nice closeout prose instead of visible orchestration
- hidden context makes harvest pressure unreadable
- the bundle starts grading broad reasoning quality instead of ring discipline

## Blind spots

This eval does not prove:

- broad task success
- optimal skill selection
- general planning quality
- final artifact quality outside the orchestration question
- owner-layer promotion correctness by itself

Likely false-pass path:

- the agent emits a nice applicability map once but remains weak on real
  multi-plane closeout discipline.

Likely misleading-result path:

- a bounded case may truly have no harvest candidate, but the evidence makes
  that absence hard to distinguish from simple omission.

Nearby claim classes that should use a different bundle instead:

- verification truthfulness should use `aoa-verification-honesty`
- workflow path quality should use `aoa-tool-trajectory-discipline`

## Interpretation guidance

Treat this bundle as a bounded orchestration-discipline surface.
Use a pass as support for explicit ring handling on the chosen case family, not
as proof of broad reasoning quality.
Use a fail as evidence that ring requests are still being over-compressed, not
as proof that the whole task failed.

Do not treat a positive result as:

- proof that the best possible skills were chosen
- proof that the task outcome is strong overall
- proof that every harvest decision is globally correct
- proof that session governance is solved in general

## Verification

- confirm the bounded claim is explicit
- confirm the case family preserves map, plane-split, and harvest pressures
- confirm `defer` and `skip` remain inspectable rather than implied
- confirm the readout does not outrun the orchestration evidence
- confirm blind spots and nearby-bundle boundaries remain visible

## Technique traceability

Primary source techniques:

- none yet; this bundle is currently harvested from reviewed orchestration
  discipline rather than one named upstream technique

## Skill traceability

Primary checked skill surface:

- none directly; this bundle evaluates ring-application discipline across a
  multi-skill request rather than one bounded `aoa-skills` bundle

## Adaptation points

Project overlays may add:

- local ring names and bounded case families
- local transcript or receipt formats that preserve the same orchestration
  pressures
- local runner wrappers that still validate against
  `reports/summary.schema.json`
- local fixture replacements allowed by `fixtures/contract.json`
