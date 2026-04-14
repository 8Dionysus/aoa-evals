---
name: aoa-a2a-summon-return-checkpoint
category: workflow
status: draft
summary: Checks whether a reviewed summon child route preserves the contract from aoa-summon request through sdk.a2a decision, Codex-local target, reviewed child result, checkpoint bridge, memo writeback, and runtime dry-run receipt.
object_under_evaluation: reviewed A2A summon child-return checkpoint route
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies: []
skill_dependencies:
  - aoa-checkpoint-closeout-bridge
  - aoa-contract-test
---

# aoa-a2a-summon-return-checkpoint

## Intent

Use this eval to check whether a reviewed `aoa-summon` child route preserved
the contract through `sdk.a2a`, Codex-local target selection, reviewed child
return, checkpoint bridge, memo writeback, and runtime dry-run assembly.

This draft bundle is a workflow proof surface.

It focuses on one nearby question:
did the child-return route keep every ownership boundary visible while moving
from summon request to reviewed return and dry-run closeout receipt?

It is not a general child-agent quality eval.
It is not a runtime execution eval.
It is not a skill-readiness eval for `aoa-summon`.
It does not prove that live automation is safe or enabled.

## Object under evaluation

This eval checks a reviewed A2A summon child-return checkpoint route.

Primary surfaces under evaluation:

- `summon_request` contract fidelity
- `summon_decision` honesty
- `codex_local_target` source grounding
- `child_task_result` review posture
- `return_plan` and `checkpoint_bridge_plan` continuity
- `a2a_return_eval_packet` contract completeness
- `memo_writeback_ref` boundedness
- `runtime_closeout_dry_run_receipt` dry-run honesty

Nearby surfaces intentionally excluded:

- final quality of the child task output
- general delegation strategy
- live runtime execution
- remote transport reliability
- broad self-agent autonomy
- memo object truth after later review

## Bounded claim

This eval is designed to support a claim like:

under these conditions, a reviewed summon child route preserved its parent
anchor, A2A control-plane decision, reviewed child result, checkpoint bridge,
proof packet, memo writeback reference, and dry-run runtime receipt without
moving authority into the wrong repository or implying live automation.

This eval does not support claims such as:

- the child task solved the whole parent route
- `aoa-summon` is federation-ready
- SDK planning can execute by itself
- memo writeback has become canonical memory
- a dry-run receipt proves runtime execution
- one clean A2A route proves stable child-agent competence

## Trigger boundary

Use this eval when:

- a route has a reviewed parent anchor and `summon_request`
- the child route has a `summon_decision`
- `aoa-sdk` carried an A2A decision, Codex-local target, return plan, or
  reviewed closeout request
- the child result was reviewed before checkpoint bridge use
- the route emits a memo writeback reference, eval packet, or runtime dry-run
  receipt candidate

Do not use this eval when:

- no child route was actually summoned or planned
- the route lacks a reviewed child result
- the question is final-answer quality rather than return contract fidelity
- the route is live runtime execution rather than dry-run adapter assembly
- the memo writeback or eval packet is being treated as owner truth

## Inputs

- one `summon_request`
- one `summon_decision`
- one `codex_local_target`
- one reviewed `child_task_result`
- one `return_plan`
- one `checkpoint_bridge_plan`
- one `a2a_return_eval_packet`
- one `memo_writeback_ref`
- one `runtime_closeout_dry_run_receipt`
- selected owner-source refs for `aoa-skills`, `aoa-sdk`, `aoa-playbooks`,
  `aoa-memo`, `aoa-evals`, and `abyss-stack`

## Fixtures and case surface

A strong starter case surface should include:

- one route where a Codex-local child target is allowed and returns cleanly
- one route where the summon decision requires split before child execution
- one route where a human gate blocks return until review evidence is present
- one route where runtime dry-run receipt assembly succeeds but live execution
  remains out of scope

Fixtures should avoid:

- routes with no explicit summon decision
- routes whose only evidence is smooth summary prose
- routes that require hidden raw transcript continuity
- runtime receipts that were produced by live automation
- memo writebacks that claim canon status before review

The current materialized proof surface is intentionally light: a support note,
an integrity check, and an artifact-to-verdict hook. A later fixture family may
add machine-readable cases only if it preserves the same owner-boundary and
dry-run limits.

## Scoring or verdict logic

This eval prefers a summary-with-breakdown verdict.

Suggested verdict classes:

- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Suggested breakdown axes:

- `summon_contract_fidelity`
- `sdk_decision_grounding`
- `codex_target_source_grounding`
- `child_result_review`
- `checkpoint_bridge_boundedness`
- `proof_and_memo_subordination`
- `runtime_dry_run_honesty`

Per-case review should ask:

- does the `summon_request` name parent anchor and expected child outputs?
- does the `summon_decision` honestly allow, block, narrow, or split the route?
- does the Codex-local target cite the projection source or a reviewed
  fallback?
- was the child result reviewed before return?
- did the checkpoint bridge avoid treating notes as final authority?
- did the proof packet and memo reference stay subordinate to owner truth?
- did the runtime receipt remain dry-run only?

### Approve signals

Signals toward `supports bounded claim`:

- the summon request and decision are inspectable
- the SDK A2A decision and target stay in `aoa-sdk`
- the child result was reviewed before checkpoint bridge use
- return and checkpoint bridge plans name real anchors
- memo writeback is a bounded reference rather than memory canon
- eval packet is a proof candidate rather than runtime execution
- runtime receipt explicitly says `dry_run` and `live_automation=false`

### Degrade signals

Signals toward `mixed support` or `does not support bounded claim`:

- the child route has no reviewed parent anchor
- the summon decision is inferred after the fact
- Codex target selection is role lore without a source ref
- the bridge uses checkpoint notes as final harvest, progression, or quest
  authority
- memo writeback replaces reviewed child evidence
- the eval packet claims live runtime readiness
- the dry-run receipt is described as live execution

## Baseline or comparison mode

This bundle uses `none`.

It is a standalone bounded proof surface for the current A2A summon
child-return checkpoint route.

A later stronger form may compare:

- two versions of the SDK A2A return helper on the same reviewed route
- dry-run versus live-receipt language on matched route artifacts
- split-before-summon and summon-then-return variants of the same parent route

Without a baseline, this bundle supports only modest claims about the selected
route and artifacts.

## Execution contract

A careful run should:

1. inspect the parent anchor, `summon_request`, and `summon_decision`
2. inspect the SDK A2A decision and Codex-local target
3. inspect the reviewed child result
4. inspect the `return_plan` and `checkpoint_bridge_plan`
5. inspect the eval packet, memo writeback ref, and runtime dry-run receipt
6. judge whether every ownership boundary stayed intact
7. publish a summary-with-breakdown artifact with explicit interpretation
   limits

Execution expectations:

- do not grade child-output quality as if it were return contract fidelity
- do not treat SDK helpers as runtime authority
- do not treat memo writeback as canonical memory
- do not treat a dry-run receipt as live automation
- do not reward prose that hides missing child-result review
- keep the playbook route and owner-source refs visible when interpreting the
  verdict

## Outputs

The eval should produce:

- one bundle-level verdict
- one breakdown across the A2A return-contract axes
- one note on the strongest owner-boundary support signal
- one note on the strongest hidden-automation risk gap
- one explicit interpretation boundary

## Failure modes

This eval can fail as an instrument when:

- the reviewer mistakes a neat closeout summary for reviewed child evidence
- the SDK A2A payload is treated as proof by itself
- memo writeback is treated as a settled memory object
- checkpoint bridge hints are treated as final closeout authority
- runtime dry-run wording hides live-execution claims

## Blind spots

This eval does not prove:

- final parent-route correctness
- child-agent quality
- live runtime readiness
- remote transport correctness
- general summon skill readiness
- durable memo truth after later review

Likely false-pass path:

- the route has all artifact names but the child result was never actually
  reviewed before checkpoint bridge use.

Likely misleading-result path:

- the route safe-stops because the human gate is missing, and the report looks
  weaker even though the stop preserved the contract honestly.

Nearby claim classes that should use a different bundle instead:

- return-anchor behavior without the summon-specific A2A surface should use
  `aoa-return-anchor-integrity`
- bounded repair posture should use `aoa-repair-boundedness`
- child output quality should use a task-specific eval outside this bundle

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the reviewed summon child-return route kept the summon, SDK, Codex-local,
checkpoint, memo, eval, and runtime dry-run ownership boundaries visible on
this selected route.

Do not treat a positive result as:

- proof that `aoa-summon` is governance-ready
- proof that live runtime automation is enabled or safe
- proof that memo writeback has become canonical memory
- proof that the child task solved the whole parent route
- proof that the SDK A2A helper owns runtime execution

A mixed or negative result is useful because it can reveal:

- missing reviewed child evidence
- hidden split or human-gate pressure
- source refs that were summarized but not inspectable
- dry-run wording that drifts toward live execution claims
- memo or eval artifacts being promoted beyond their owner boundary

## Verification

- confirm the parent anchor, summon request, and summon decision are inspectable
- confirm the SDK A2A decision and Codex-local target cite owner-source refs
- confirm the child task result was reviewed before checkpoint bridge use
- confirm memo writeback remains a reference, not a canonized memory object
- confirm the eval packet is a proof candidate, not a verdict by itself
- confirm the runtime receipt says `dry_run` and `live_automation=false`
- confirm the final report names any split or human-gate pressure explicitly

## Technique traceability

Primary source techniques:

- none yet; this bundle is workflow-contract shaped and currently depends on
  skill and artifact contracts rather than a promoted technique bundle

## Skill traceability

Primary checked skill surfaces:

- aoa-checkpoint-closeout-bridge
- aoa-contract-test

## Adaptation points

Project overlays may add:

- local reviewed child-route fixtures
- repo-specific A2A return payload examples
- stricter schema-backed checks for `summon_request` and `return_plan`
- runtime dry-run receipt validation against `abyss-stack` local schemas
- memo writeback candidate checks against `aoa-memo` generated intake surfaces
- later comparison baselines for split-before-summon versus summon-then-return
