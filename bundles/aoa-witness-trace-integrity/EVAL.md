---
name: aoa-witness-trace-integrity
category: workflow
status: draft
summary: Checks whether a public witness trace for a bounded run keeps meaningful steps, tool visibility, state deltas, failures, redaction posture, and the markdown summary aligned enough for review.
object_under_evaluation: reviewable integrity of witness trace exports on bounded runs
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies: []
skill_dependencies: []
---

# aoa-witness-trace-integrity

## Intent

Use this eval to check whether a bounded run leaves behind a witness trace that a reviewer can actually inspect.

This draft bundle is a `diagnostic` workflow eval.
It checks whether the public witness artifact stays reviewable enough to support downstream memo writeback and compost distillation.
It is not meant to prove final outcome quality,
and it is not a substitute for full runtime instrumentation in `abyss-stack`.
It may sit upstream of artifact/process pairing as adjacent witness context,
but it does not replace `aoa-bounded-change-quality` as the process-side reading.

The goal is not to prove total transparency.
The goal is to test one bounded claim:

under these conditions,
a bounded run can leave a witness trace whose meaningful steps,
tool use,
external effects,
failure paths,
and summary readout remain visible enough for review.

## Object under evaluation

This eval checks reviewable integrity of witness trace exports on bounded runs.

Primary surfaces under evaluation:
- meaningful-step visibility
- tool-call visibility when tools materially shaped the run
- explicit `state_delta` notes for external effects
- failure-path preservation when the route degrades or stops early
- redaction-first handling
- alignment between the trace and the human-readable markdown summary

Nearby surfaces intentionally excluded:
- final artifact quality by itself
- exact one-true trace or one mandatory tool order
- hidden runtime logging quality in `abyss-stack`
- downstream compost promotion quality

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
the repository can preserve a witness trace that is reviewable enough
to understand what the run tried to do,
what materially happened,
where external effects occurred,
where failures or review flags appeared,
and what the summary still does not prove.

This eval does **not** support claims such as:
- the run outcome was correct
- the full internal reasoning process is available
- the runtime trace pipeline is production-ready
- every bounded run now requires the same trace depth

## Trigger boundary

Use this eval when:
- the run is non-trivial enough to need a reviewable witness
- a downstream memo writeback or compost route depends on the trace
- tool use or external effects materially shaped the route
- the main question is whether the trace contract stayed honest and legible

Do not use this eval when:
- the run is trivial and no meaningful witness surface is needed
- there was no material route to reconstruct beyond a simple answer
- the main question is outcome quality rather than trace honesty
- the surface depends on runtime instrumentation that this pilot wave does not yet implement

## Inputs

- `witness_trace_json`
- `witness_summary_md`
- the bounded task or run goal
- redaction notes when any step required them
- the governing route contract, such as `aoa-playbooks/witness-to-compost-pilot`

## Fixtures and case surface

A strong starter fixture set should include:
- a bounded run with visible tool use
- a bounded run with at least one explicit external effect
- a bounded run with a preserved partial failure path
- a bounded run where redaction is required but the trace still stays reviewable
- a bounded run where the markdown summary could easily over-polish what the trace shows

Fixture families should avoid:
- hidden private logs that outside reviewers cannot inspect
- runtime-only telemetry that this public pilot contract does not promise
- perfectly clean happy-path traces only
- cases where the trace can pass without saying anything meaningful

## Scoring or verdict logic

This eval prefers a bundle-level verdict with an explicit breakdown.

Suggested verdict classes:
- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Suggested breakdown axes:
- `step_visibility`
- `tool_visibility`
- `state_delta_visibility`
- `failure_path_preservation`
- `redaction_posture`
- `summary_alignment`

Per-run review should ask:
- are the meaningful steps visible enough to reconstruct the route?
- are tool calls named when tools materially shaped the result?
- are external effects marked as `state_delta` rather than hidden in prose?
- does failure still leave a partial witness?
- does redaction protect sensitive content without erasing the route?
- does the markdown summary stay weaker than the trace rather than stronger?

### Approve signals

Signals toward `supports bounded claim`:
- meaningful route steps are visible in order
- tool use is named where it mattered materially
- external effects are marked explicitly
- a failure path still leaves a partial witness
- summary wording matches the visible trace and keeps limits explicit

### Degrade signals

Signals toward `mixed support` or `does not support bounded claim`:
- a meaningful step is omitted from the witness
- tool use materially shaped the run but is hidden
- external effects appear only in prose and not as `state_delta`
- failure paths disappear behind a polished summary
- redaction strips away the route itself rather than only sensitive payloads
- the markdown summary claims more coherence or success than the trace supports

## Baseline or comparison mode

This bundle uses `none`.

It is a standalone bounded proof surface for witness integrity.
A later stronger form may compare:
- the same route before and after witness-contract revisions
- trace quality across repeated runs on the same playbook
- public witness exports against stronger runtime capture later in `abyss-stack`

Without that later comparison form,
this bundle supports only modest claims about current trace integrity on the chosen cases.

## Execution contract

A careful run should:
1. choose one bounded run that requires a witness trace
2. inspect the JSON trace and markdown summary together
3. confirm whether meaningful steps remain visible in order
4. confirm whether tool use and external effects are named honestly
5. confirm whether failures and redactions remain reviewable
6. publish a summary-with-breakdown artifact with an explicit interpretation boundary

Execution expectations:
- do not require a single perfect tool path
- do not treat hidden private runtime telemetry as part of the public contract
- do not let the markdown summary stand in for the trace itself
- do not upgrade partial visibility into total transparency

## Outputs

The eval should produce:
- one bundle-level verdict
- one breakdown across the witness-integrity axes
- one note on the most material trace gap or success
- one explicit interpretation boundary

A compact public summary-with-breakdown may include:
- run id
- verdict
- breakdown by witness-integrity axis
- major review flags
- one note on what a human should inspect next

## Failure modes

This eval can fail as an instrument when:
- reviewers mistake polished summaries for trace integrity
- the chosen cases are so small that witness quality is never really tested
- hidden local telemetry is treated as part of the public contract
- redaction is used as a reason to erase route visibility entirely
- reviewers quietly demand one exact tool sequence instead of bounded reviewability

## Blind spots

This eval does not prove:
- final outcome quality
- internal reasoning completeness
- runtime instrumentation coverage
- downstream compost quality
- long-term repeatability across broader task families

Likely false-pass path:
- the trace looks orderly and complete at a glance,
  but one material external effect or failure branch was never made explicit.

Likely misleading-result path:
- a bounded public trace can look mixed only because strong redaction was necessary,
  even when the underlying route stayed honest within its contract.

Nearby claim classes that should use a different bundle instead:
- outcome-versus-path split should use `aoa-trace-outcome-separation`
- tool-path quality where the path itself is the main claim should use `aoa-tool-trajectory-discipline`
- downstream provenance-preserving digestion should use `aoa-compost-provenance-preservation`

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the public witness trace stayed reviewable enough to support bounded downstream use.

Do not treat a positive result as:
- proof that the run outcome was correct
- proof that all internal reasoning is transparent
- proof that `abyss-stack` runtime instrumentation is already solved
- proof that every future run needs the same trace depth

A mixed or negative result is valuable because it can reveal:
- hidden tool use
- missing external-effect notes
- failure-path erasure
- over-polished summaries
- redaction posture that became too destructive to review

## Verification

- confirm the bounded claim is explicit
- confirm the trace and markdown summary are both inspected
- confirm tool use is visible where it mattered materially
- confirm external effects are marked as `state_delta`
- confirm failure-path and redaction posture remain reviewable
- confirm the summary stays weaker than the trace rather than stronger

## Technique traceability

Technique linkage is intentionally deferred for this starter bundle.
The current pilot is contract-first and does not yet assume a reusable witness-capture technique canon.

## Skill traceability

Skill linkage is intentionally deferred for this starter bundle.
The current pilot route lives first in `aoa-playbooks/witness-to-compost-pilot`
rather than in a standalone skill bundle.

## Adaptation points

Project overlays may add:
- local witness trace depths
- local redaction classes
- local state-delta review rules
- local summary templates
- later comparison or regression forms once the public witness contract stabilizes
