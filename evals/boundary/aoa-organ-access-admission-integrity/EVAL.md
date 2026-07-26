---
name: aoa-organ-access-admission-integrity
category: boundary
status: bounded
summary: Checks that one OS Abyss organ-access proof packet preserves independent maturity axes, policy-plane ceilings, owner acceptance, freshness, and admission boundaries.
object_under_evaluation: OS Abyss organ-access proof packet and its admission inferences
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies: []
skill_dependencies: []
capability_dependencies: []
---

# aoa-organ-access-admission-integrity

## Intent

Use this eval to validate one public-safe proof packet for one exact OS Abyss
organ capability on one policy plane. The bundle protects the boundary between
observed evidence and admission inference.

The bounded claim is:

> Given a packet shaped by this source contract, independent maturity axes stay
> independently evidenced, a lower policy plane does not authorize a higher
> effect, and central proof does not impersonate owner acceptance or control
> plane admission.

This is a source-contract and negative-invariant eval. It does not observe a
live MCP process, registry, consumer, or organ result by itself.

## Object under evaluation

The object under evaluation is one `organ_access_proof_packet_v1` packet with:

- one organ and capability identity;
- one policy plane and protocol pair;
- named source, access, control, runtime, proof, and acceptance owners;
- exact source, package, deploy, and consumer-schema revisions;
- an observation window;
- sixteen independently stated maturity axes;
- a bounded result that cannot authorize admission, infer acceptance, or raise
  effect authority.

## Bounded claim

The bundle can support only this claim:

- the supplied packet matches the public source contract; and
- the bundled negative scenarios do not allow the forbidden inferences named
  in this eval.

It cannot support claims that:

- an organ is installed, deployed, reachable, grounded, accepted, or admitted;
- the private registry contains a current entry;
- a named consumer invoked the organ successfully;
- a live owner accepted evidence;
- rollback works in the deployed runtime;
- one passing protocol pair proves another pair.

## Trigger boundary

Use this eval when:

- a central proof packet is being prepared or reviewed for the organ access
  fabric;
- a status surface risks collapsing reachability into grounding;
- owner acceptance or admission is being inferred from central evaluation;
- a read or candidate plane risks being treated as effect authority;
- evidence freshness, revision binding, or rollback independence must remain
  explicit.

Do not use this eval when:

- the task is owner-local semantic review;
- the task is live runtime, registry, or consumer observation;
- the task is capability-specific effect testing;
- the task is acceptance-owner receipt review;
- the task is control-plane admission or rollback execution.

## Inputs

- one JSON packet conforming to
  `schemas/organ-access-proof-packet.schema.json`;
- the exact organ capability and policy plane under review;
- owner-qualified evidence references and revision bindings for every asserted
  axis;
- explicit limitations and an observation window.

## Fixtures and case surface

The checked-in scenarios cover:

1. a valid bounded read-plane packet;
2. rejection of `endpoint_ready` evidence used for `result_grounded`;
3. rejection of a central-eval result used for `owner_accepted`;
4. rejection of read-plane authorization for a higher effect;
5. rejection of an asserted axis without complete evidence and revision data;
6. acceptance of an honest `insufficient_evidence` packet;
7. rejection of a packet that tries to authorize an admission change;
8. rejection of evidence that expires before the packet observation window
   closes;
9. rejection of a positive verdict when no maturity axis is asserted;
10. rejection of an asserted axis bound to the wrong revision slot.

These fixtures are public-safe contract examples. They contain no production
tokens, private payloads, live service addresses, or private registry data.

## Scoring or verdict logic

The scenario runner produces:

- `supports bounded claim` when every checked-in accept/reject expectation
  matches;
- `does not support bounded claim` when any scenario expectation diverges.

For direct packet validation, schema and semantic issues are returned as
machine-readable codes. An `insufficient_evidence` result is a valid and useful
readout when the packet is honest about missing proof.

No runner result changes admission. No positive result implies owner
acceptance. A source-contract pass is weaker than live pair-specific evidence.

## Baseline or comparison mode

This bundle uses `none`.

It is a standalone bounded source-contract and negative-invariant surface.
Without a baseline it can support only the current packet-shape claim. It
cannot support improvement, regression, comparative implementation quality, or
runtime reliability claims.

## Execution contract

Run the exact checked-in suite and packet-validation argv recorded in
`runners/contract.json`. The executable repository validation route is governed
by [`evals/AGENTS.md#validation`](../../AGENTS.md#validation); that owner card
defines the surrounding source checks and command ownership.

The runner is deterministic and offline. It validates packet shape and bounded
semantic invariants only. Live execution evidence must be gathered elsewhere,
then presented as owner-qualified candidate evidence.

## Outputs

- a deterministic summary-with-breakdown report;
- per-scenario expected and observed acceptance state;
- stable issue codes for violated inference boundaries;
- an explicit claim boundary and limitations list.

The report contract is
`reports/summary.schema.json`; `reports/example-report.json` is a checked-in
public-safe example, not a production receipt.

## Failure modes

The instrument fails its purpose if:

- one maturity axis is derived from another;
- an asserted axis lacks timestamp, evidence, revision, and freshness data;
- a central eval result is accepted as owner acceptance;
- read or candidate evidence authorizes an effect plane;
- a passing source scenario is reported as live organ admission;
- absent evidence is hidden instead of producing `insufficient_evidence`;
- private runtime material is copied into public fixtures.

## Blind spots

This eval does not prove:

- authenticity of an external evidence reference;
- correctness of a live owner implementation;
- runtime latency, cancellation, concurrency, or injection resistance;
- consumer diversity or protocol-pair interoperability;
- actual effect isolation between processes and credentials;
- durable rollback or recovery;
- owner acceptance or control-plane admission.

Those claims require pair-specific runtime evidence, named owner review, and
separate admission and rollback receipts.

## Interpretation guidance

A positive suite result means only that this checked-in source contract
preserves its bounded negative invariants. It is not an organ health score.

Do not treat a positive result as:

- evidence that a live organ is installed or reachable;
- evidence that a result is grounded or fresh;
- owner acceptance or control-plane admission;
- effect authorization;
- cross-organ or rollback proof.

Reviewers must keep these distinctions:

- declared is not packaged;
- packaged is not deployed;
- process alive is not endpoint ready;
- endpoint ready is not result grounded;
- call succeeded is not fresh or accepted;
- central proof is not owner acceptance;
- owner acceptance is not admission;
- read-plane proof is not effect authorization;
- successful operation is not rollback proof.

## Verification

- run the bundled scenario command;
- validate the example report against the report schema;
- run the bundle-specific repository check routed by
  `evals/AGENTS.md#validation`;
- confirm every asserted maturity axis retains its own evidence kind, revision,
  timestamp, and freshness field;
- confirm the report keeps admission, acceptance inference, and higher-effect
  authorization fixed to `false`;
- confirm the result names the live-evidence blind spot.

## Technique traceability

No registered technique dependency is required. The design follows the
owner-separated proof topology and packet law named in
`docs/architecture/AOA_EVALS_MCP_CONTRACT.md`.

## Skill traceability

No callable skill is under evaluation. `aoa-evals` selection and evolution
procedures may route to this bundle, but they do not supply proof evidence or
change its verdict.

## Adaptation points

Project overlays may replace the public-safe organ, capability, protocol pair,
owner labels, and evidence references. They must retain:

- all sixteen independent maturity axes;
- exact revision, timestamp, evidence-kind, and freshness data for every
  asserted axis;
- the endpoint, central-eval, effect-plane, insufficient-evidence, and
  admission-denial cases;
- false admission, acceptance-inference, and higher-effect authorization
  fields;
- the source-only claim limit.
