---
name: aoa-continuity-capsule-compaction
category: comparative
status: draft
summary: Checks field-level continuity preservation across a paired portable and private capsule materialization without turning a synthetic contract run into runtime or economy proof.
object_under_evaluation: evidence-backed continuity capsule preservation across paired compaction materializations
claim_type: comparative
baseline_mode: fixed-baseline
report_format: comparative-summary
technique_dependencies: []
skill_dependencies: []
comparison_surface:
  shared_family_path: mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/README.md
  paired_readout_path: mechanics/comparison-spine/parts/fixed-baseline/reports/same-task-baseline-proof-flow-v1.md
  integrity_sidecar: aoa-eval-integrity-check
  anchor_surface: aoa-regression-same-task
  baseline_target_label: canonical continuity capsule before materialization
  selection_question: Do you need a fixed-baseline field-preservation route for portable and private continuity capsule materializations?
---

# aoa-continuity-capsule-compaction

## Intent

Use this draft eval to check whether one canonical `continuity_capsule_v1`
retains its decision, constraint, obligation, evidence-navigation, source
watermark, compaction-event, and protected-tail posture across the paired
portable and private materializations.

The bundle is an eval-owner contract and a deterministic field-level runner.
It does not activate compaction, read raw session storage, invoke a provider,
or claim that a real session survived compaction. The fixed baseline is the
canonical capsule supplied to the materializer; the candidate side is the
resulting paired view packet.

## Object under evaluation

This eval covers:

- exact capsule identity and digest binding
- preservation of goal, constraints, completed work, current work, blockers,
  exact decisions, open obligations, evidence references, and omissions or
  uncertainty
- preservation of source watermark and compaction-event metadata
- omission of protected-tail bytes from the portable view
- verbatim protected-tail digest and byte-count preservation in the private
  view
- agreement between portable and private views on all non-tail content

It excludes provider quality, model choice, runtime health, transport
success, installed-artifact trust, lifecycle closure, owner acceptance, and
economy or latency claims.

## Bounded claim

For a schema-valid paired packet, the runner can report whether the named
capsule fields and protected-tail posture are preserved from one canonical
capsule into its portable and private materializations.

This eval does not support claims that:

- a real compaction event occurred
- a model or provider rehydrated the capsule correctly
- a session, thread, runtime, or transport remained live
- the capsule is sufficient evidence of semantic task success
- the direction improved validation cost, wall-clock economy, or quality
- a draft report is a proof verdict, activation admission, or acceptance

## Trigger boundary

Use this eval when:

- a compaction contract needs a paired, field-level preservation readout
- portable and private views must be compared without exposing protected-tail
  bytes
- a source change needs a deterministic report shape before baseline admission
- omissions, uncertainty, and evidence references must remain visible

Do not use this eval when:

- the question is runtime activation or live session recovery
- the input is raw private transcript or host telemetry
- a provider, model, route, or host is being ranked
- a real paired baseline and treatment run are being claimed
- a central proof verdict, promotion, or human acceptance is required

## Inputs

The runner accepts a versioned packet containing a case family and one or
more cases. Each case supplies:

- one canonical `continuity_capsule_v1` baseline object
- one portable materialization
- one private materialization
- exact capsule reference and digest fields on every side

The input packet is public-safe and synthetic until a separately reviewed
real-session evidence packet is admitted. No path, credential, raw transcript,
private host fingerprint, or generated reader is an observation authority.

## Fixtures and case surface

The shared fixed-baseline fixture family remains the frozen same-task family
named in `fixtures/contract.json`. The local case surface is a small schema
and runner contract for field-preservation cases, including a positive pair,
tail-exposure rejection, identity drift, and content drift.

Replacement cases must keep the canonical capsule as the baseline, preserve
the portable/private distinction, retain exact refs and digests, and keep
unknown or omitted information explicit rather than replacing it with empty
success values.

## Scoring or verdict logic

Each case receives one field-level check for every required content field,
source watermark, compaction event, and protected-tail invariant.

The comparative reading is:

- `no material regression` when every required check passes
- `mixed regression signal` when some checks pass and some fail
- `regression present` when identity or all required preservation checks fail

The bundle-level verdict is the conservative aggregate of case readings. A
passing synthetic case is only a contract-shape result. It never upgrades the
bundle from draft, creates a baseline-ready receipt, or supplies a runtime or
economy measurement.

## Baseline or comparison mode

This bundle uses `fixed-baseline`.

The baseline target is the canonical continuity capsule before materialization.
The candidate side is the paired portable/private packet produced from that
same capsule. The comparison remains field-level: it does not compare model
answers, elapsed time, or task quality.

## Execution contract

The runner validates the versioned input packet, recomputes the capsule and
view digests, checks exact reference binding, compares every required field,
and emits the bundle-local comparative report shape. It never executes an
arbitrary command, reads live state, starts a process, contacts a provider,
or repairs malformed input.

The source bundle remains draft until an independent reviewer admits a real
paired evidence packet and confirms the baseline gate. The report’s claim
boundary and limitations are part of the output contract.

## Outputs

- one draft comparative report
- one conservative bundle-level verdict
- one per-case preservation reading
- field-level preservation checks
- explicit protected-tail exposure and identity-drift failures
- claim-boundary and limitation text separating contract checks from runtime
  proof

## Failure modes

- capsule or materialization digest drift
- portable view contains protected-tail bytes
- private view loses or changes protected-tail bytes
- portable and private views disagree on non-tail content
- a view names a different owner, schema, object, or capsule digest
- missing fields are treated as empty success values
- synthetic contract output is read as a real compaction result
- draft output is treated as activation, promotion, economy, or acceptance

## Blind spots

This eval does not prove:

- raw session-memory capture or source watermark freshness
- actual hook or trigger behavior
- SDK continuation or runtime reinjection execution
- provider-neutral transport admission
- semantic task continuity after a live context boundary
- installed-release parity, trust admission, or owner acceptance
- validation speed, cost reduction, or economy improvement

## Interpretation guidance

Read a positive case as “the supplied packet is internally field-preserving.”
Read a negative case as a packet or implementation contract failure, not as a
model-quality diagnosis. Preserve the exact failed field and evidence class.

Only a separately admitted paired real-session eval may support a stronger
continuity statement, and even then runtime, transport, semantic, lifecycle,
closure, and acceptance claims remain separate.

Do not treat a positive field-preservation reading as:

- proof that the baseline or candidate ran in a live runtime
- evidence of a provider, model, or host quality difference
- evidence of economy improvement or a promotion recommendation
- owner or human acceptance

## Verification

Verify that the frontmatter, manifest, fixture contract, runner contract,
report schema, example report, and support notes agree on the fixed-baseline
route. Verify that the runner is deterministic, digest-bound, provider-neutral,
and unable to expose protected-tail bytes through its report. Verify that no
draft report is used as a baseline-ready, activation, promotion, economy, or
owner-acceptance claim.

## Technique traceability

- none yet; this bundle defines a continuity-contract comparison surface

## Skill traceability

- none yet; runtime and session-memory owner skills remain separate from eval
  verdict meaning

## Adaptation points

- add reviewed real-session case packets only after the direction’s baseline
  gate is admitted
- extend the required field set only with an explicit schema and report review
- keep provider-specific transport details outside this provider-neutral bundle
- preserve the portable/private tail boundary when adapting to other capsule
  materialization formats
