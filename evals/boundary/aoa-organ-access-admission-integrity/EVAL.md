---
name: aoa-organ-access-admission-integrity
category: boundary
status: bounded
summary: Checks that one OS Abyss organ-access proof packet preserves independent maturity axes, policy-plane ceilings, owner acceptance, freshness, and admission boundaries.
object_under_evaluation: OS Abyss organ-access proof packet, bounded rollback-readiness candidate, and matched progressive-tool-exposure disclosure candidates
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
live MCP process, registry, consumer, or organ result by itself. Its optional
live-packet materializer can compose already-issued local evidence into one
candidate packet, but it cannot issue a proof verdict or owner decision.

The bundle also exposes an optional rollback-readiness review for one exact
stack-issued last-known-good candidate. That review checks reproducibility and
authority stop-lines only. It neither executes rollback nor promotes readiness
to the `rollback_proven` maturity axis.

## Object under evaluation

The primary object under evaluation is one `organ_access_proof_packet_v1`
packet with:

- one organ and capability identity;
- one policy plane and protocol pair;
- named source, access, control, runtime, proof, and acceptance owners;
- exact source, package, deploy, and consumer-schema revisions;
- an observation window;
- sixteen independently stated maturity axes;
- a bounded result that cannot authorize admission, infer acceptance, or raise
  effect authority.

The optional secondary object is one
`abyss_stack_mcp_rollback_candidate_v1` candidate bound to the exact private
runtime observation, immutable deployment record, consumer registration,
stable restorable process target, and a distinct owner-grounded
last-known-good canary. It remains a candidate until an independent stack
projector revalidates those live inputs.

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

Materializing a packet does not change those claim limits. A materialized
packet remains an `insufficient_evidence` candidate until the missing axes are
independently supplied and reviewed through their named owners.

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

For optional live packet materialization:

- one private deny-by-default `aoa-sdk` registry source in the organ-record v1
  or contour-based v2 shape;
- one exact content-addressed `abyss-stack` deployment manifest and its
  byte-identical immutable record;
- one current private `abyss-stack` runtime observation whose endpoint and
  blocked-canary links reference the exact canary record;
- one immutable private `abyss-stack` authenticated read-canary receipt in
  the legacy v1, attested v2, or deployment-bound attested v3 shape;
- for a successful call, its exact private content-addressed result artifact;
- optionally, one exact private `aoa_organ_owner_result_review_v1` receipt from
  the named source or acceptance owner; and
- one private output path under a non-group/world-accessible directory.

For optional rollback-readiness review:

- one private mode-`0600`, non-symlink stack-issued candidate conforming to
  `schemas/rollback-readiness-candidate.schema.json`;
- an unexpired observation window that covers the candidate lifetime;
- byte-identical source, deployed package, and last-known-good package
  identities;
- one immutable deployment manifest reference and digest;
- one stable restorable unit/executable identity, credential class without
  credential bytes, and exact consumer registration;
- one distinct `/last-known-good` canary receipt in the private
  `rollback-canaries` lane; and
- one private output path for the bounded review.

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
10. rejection of an asserted axis bound to the wrong revision slot;
11. rejection of a reversed RFC 3339 observation window using lowercase
    `t`/`z`.

These fixtures are public-safe contract examples. They contain no production
tokens, private payloads, live service addresses, or private registry data.

### Live packet materializer

`runners/materialize_live_packet.py` is a fail-closed composition helper, not a
second verdict runner. Its exact input, binding, output, and claim ceiling are
recorded in `runners/live-materializer-contract.md`.

It performs bounded local checks over:

- secret-free input shape, regular-file and symlink posture, duplicate JSON
  keys, and private permissions for registry, observation, and canary inputs;
- deployment content addressing and byte parity with the immutable record;
- registry/observation owner, source-revision, and exact v1 record or v2 read
  contour identity; a v2 shadow contour without declared maturity must carry
  one exact owner-source observation for the selected source revision;
- package/deploy/runtime identity and digest continuity;
- canary content addressing, read-plane claim limit, server/package identity,
  loopback endpoint, schema, immutable evidence reference, blocked
  owner-grounding posture, for v2/v3 the Ed25519 attestation field shape plus
  receipt/result signer continuity, and for v3 exact deployment manifest,
  service, source revision, package, deployed tree, and deployment-time
  binding;
- result-artifact content addressing, captured-payload digest, receipt
  identity, and explicit untrusted/no-instruction posture;
- optional owner-review content addressing, source/acceptance-owner identity,
  registry capability/primitive/payload-schema identity, source revision,
  capture/result/schema digests, evidence lifetime, and fixed authority
  ceiling.

It may assert only the independently supported subset of `declared`,
`packaged`, `exported`, `deployed`, `process_alive`, `endpoint_ready`,
`registry_indexed`, `schema_observed`, and `call_succeeded`. An optional exact
owner review may additionally assert `result_grounded` when its owner verdict
is `grounded`, and `freshness_satisfied` only when its freshness verdict is
`exact`. It never asserts `owner_reviewed`, `consumer_registered`,
`owner_accepted`, `cross_organ_proven`, or `rollback_proven`.

The output verdict is always `insufficient_evidence`. In particular,
`result_contract_matched` in a stack canary is not
`owner_grounding_review`, and the materializer does not convert it into
`result_grounded`. The preserved result artifact exists so a later owner
reviewer can inspect the exact payload; its presence alone asserts no maturity
axis. A consumed result review is not the organ-contract `owner_reviewed` axis
and cannot create acceptance, central proof, admission, or effect authority.

### Rollback-readiness review

`runners/review_rollback.py` reviews one exact candidate without probing or
mutating the runtime. It verifies the candidate schema and content address,
source/deployed/LKG package continuity, immutable manifest identity, stable
process-target shape, distinct LKG canary lane, observation lifetime, absence
of secret-like material, and fixed-false execution/admission/effect fields.

Its eleven deterministic scenarios include drift in source identity, manifest
identity, canary route, lifetime, registry posture, process identity, content
address, and authority ceilings. A `supported_bounded` verdict means the
candidate passed this source contract. It does not authenticate the referenced
live files; `abyss-stack` must revalidate them unchanged before projecting a
rollback-readiness observation.

### Progressive tool-exposure track

The bundle also carries a matched, public-safe source-contract track for the
provider-neutral `aoa_organ_exposure_plan_v1` candidate. The two fixtures use
the same owner-qualified capability and ordered primitive selection:

- `fixtures/exposure/01-default-off.json` keeps the feature and baseline gate
  closed and therefore exposes zero tools, two serialized bytes for the empty
  set, and no token count;
- `fixtures/exposure/02-explicit-candidate.json` exercises the future explicit
  disclosure path and records the ordered visible tool-set, schema digest,
  bytes, and an explicitly estimated token count.

`runners/review_exposure.py` checks content addressing, effect ceilings,
selection parity, refusal/expansion reasons, and the fixed-false activation and
execution fields. Its report keeps the matched visibility delta separate from
economy evidence. Because the current d0 baseline admission is not present,
the economy read is deliberately `not_run_baseline_admission_missing`: no
utility, latency, promotion, or economy claim is made by these fixtures.

The stack-side materialization and invocation receipt contract is reviewed by
the stack owner. This eval does not authenticate a live receipt, invoke a
tool, or turn a source candidate into runtime admission.

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

The live materializer is operator-invoked and reads only explicit paths. It
does not discover workspaces, read credentials, probe MCP endpoints, mutate the
registry, or execute admission. Its tests are part of the validation commands
in `runners/contract.json`.

## Outputs

- a deterministic summary-with-breakdown report;
- per-scenario expected and observed acceptance state;
- stable issue codes for violated inference boundaries;
- an explicit claim boundary and limitations list.
- optionally, one mode-`0600` materialized candidate packet plus a compact
  stdout summary naming its asserted axes and claim limit.
- optionally, one mode-`0600` `aoa_organ_access_packet_review_v1` report that
  binds an exact packet digest to the current source bundle and negative-suite
  replay without inferring owner acceptance, admission, cross-organ benefit,
  effects, or rollback.
- optionally, one mode-`0600` `aoa_organ_access_rollback_review_v1` report
  binding one exact rollback candidate to this bundle and its negative-suite
  replay while keeping rollback execution, admission change, higher effects,
  and actual effects fixed false.

The report contract is
`reports/summary.schema.json`; `reports/example-report.json` is a checked-in
public-safe example, not a production receipt.
`reports/live-review.schema.json` constrains the optional private packet-review
artifact. Its `supported_bounded` verdict means only that the exact packet
satisfies this source contract and the checked-in negative scenarios pass.
`reports/rollback-review.schema.json` constrains the optional private rollback
review and preserves the same source-versus-live boundary.

## Failure modes

The instrument fails its purpose if:

- one maturity axis is derived from another;
- an asserted axis lacks timestamp, evidence, revision, and freshness data;
- a central eval result is accepted as owner acceptance;
- read or candidate evidence authorizes an effect plane;
- a passing source scenario is reported as live organ admission;
- absent evidence is hidden instead of producing `insufficient_evidence`;
- private runtime material is copied into public fixtures.
- mismatched registry, deploy, observation, or canary identities are composed
  into one packet;
- an owner review is accepted without exact registry, capture, result,
  source-schema, lifetime, and authority-ceiling binding;
- materializer success is reported as a central proof verdict.
- rollback readiness is reported as rollback execution or post-restore health;
- a PID or current canary is accepted as a stable, distinct last-known-good
  restoration target;
- a rollback candidate contains credentials or authorizes process effects.

## Blind spots

This eval does not prove:

- cryptographic authenticity or owner signature of an input receipt;
- conformance of an external stack input to its full owner schema beyond the
  bounded fields checked by the materializer;
- correctness of a live owner implementation;
- runtime latency, cancellation, concurrency, or injection resistance;
- consumer diversity or protocol-pair interoperability;
- actual effect isolation between processes and credentials;
- durable rollback or recovery;
- owner acceptance or control-plane admission.

Those claims require pair-specific runtime evidence, named owner review, and
separate admission and rollback receipts.

The rollback-readiness review reduces uncertainty about whether an exact
last-known-good contour is reconstructable. It still does not prove that a
future restoration succeeds, that post-rollback health is good, or that the
target remains available after its evidence window expires.

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
- reproducible rollback target is not executed or verified rollback.

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
- run the live-materializer tests and confirm output mode, negative cross-input
  cases, secret rejection, and permanently unasserted owner/proof axes.
- run `review_rollback.py run-scenarios` and the rollback-readiness tests;
- confirm rollback review output is private, content-bound, source-contract
  bound, and fixed false for execution, admission, and effects;
- confirm only the stack-owned projector can turn unchanged live evidence into
  a temporary rollback-readiness observation.

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
- the source-contract claim limit and the rule that materialization is not a
  proof verdict.
