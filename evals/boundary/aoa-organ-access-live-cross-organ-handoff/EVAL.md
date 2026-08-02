---
name: aoa-organ-access-live-cross-organ-handoff
category: boundary
status: bounded
summary: Checks one exact live KAG to Memo to Evals handoff for direct owner calls, typed transition continuity, freshness, and authority separation before explicit owner acceptance.
object_under_evaluation: one exact host-visible KAG evidence to Memo candidate to Evals request and result chain
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies: []
skill_dependencies: []
capability_dependencies: []
---

# aoa-organ-access-live-cross-organ-handoff

## Intent

This separately named live bundle closes the exact gap preserved by
`AOA-EV-D-0249`: the admission-integrity bundle validates a public packet
contract but cannot issue a pair-specific verdict over direct owner calls.

The bounded question is whether one exact host-visible chain proves that KAG,
Memo, and Evals were invoked directly, passed content-bound typed artifacts in
the pinned order, stayed within their policy ceilings, and stopped at an
`aoa-evals` proof result without inferring `aoa-memo` durable acceptance.

## Object under evaluation

The proof unit is one `aoa_cross_organ_orchestration_run_v1` snapshot in
`awaiting_eval_result` state plus seven explicit private inputs:

- the KAG MCP call and its exact result artifact;
- the Memo candidate MCP call and exact candidate file;
- the Evals request MCP call and exact eval-need file; and
- the aoa-sdk snapshot that binds their receipts and transitions.

Every input must be a private regular non-symlink file. The runner reads only
the paths supplied by the operator and never discovers a workspace or endpoint.

## Bounded claim

A `supported_bounded` proof result supports only that the inspected chain:

- contains three ordered, deterministic SDK stages with valid content and
  receipt digests;
- binds every stage input to the preceding owner output;
- uses the exact direct MCP server, tool, and profile inventory expected for
  KAG read, Memo candidate, and Evals request preparation;
- preserves current owner-qualified evidence and the declared read/candidate
  ceilings;
- keeps SDK owner execution, SDK proof computation, durable-memory write,
  acceptance inference, and runtime execution fixed false; and
- requires a later explicit `aoa-memo` owner decision.

It does not support admission, durable acceptance, runtime effects, rollback,
modern-protocol cutover, or generalization beyond the exact run.

## Trigger boundary

Use this eval when:

- a direct-owner organ workflow is already at `awaiting_eval_result`;
- all seven exact private inputs are available; and
- an aware review timestamp remains inside the request window.

Do not use this eval when:

- only source-level packet checks or generic MCP health are available;
- owner-local semantic truth, admission, or durable acceptance is requested; or
- rollback or runtime-effect authorization is requested.

## Inputs

- one private aoa-sdk orchestration snapshot;
- three private direct MCP call records;
- three exact owner output artifacts;
- an aware review timestamp inside the request window;
- the current bundle source files and report schema.

## Fixtures and case surface

The offline scenario lane constructs a fictional, public-safe chain in a
temporary private directory. It covers:

1. the motivating valid three-stage chain;
2. stale KAG evidence;
3. malformed Memo candidate output;
4. Evals request denial;
5. wrong owner;
6. expired receipt;
7. replayed stage;
8. output-schema drift;
9. acceptance falsely present before proof; and
10. restore from a serialized intermediate snapshot.

The scenarios establish runner behavior only. They are not live proof.

## Scoring or verdict logic

`review` emits `supported_bounded` only when every live binding and authority
check passes. Any mismatch fails closed and emits no positive report.

`run-scenarios` reports `supports bounded claim` only when the motivating case
passes and every negative case is rejected with its expected issue code.

## Baseline or comparison mode

This bundle uses `none`. One exact run cannot prove improvement, reliability,
consumer diversity, or portability.

## Execution contract

Run the exact commands in `runners/contract.json`. A live review:

- reads explicit private files only;
- validates content addresses, SDK snapshot reconstruction, stage receipts,
  direct MCP profiles, owner outputs, freshness, and stop lines;
- writes one mode-`0600` private report atomically; and
- performs no MCP call, owner acceptance, source write, registry change,
  admission, service action, or external effect.

The report is an `aoa-evals` proof artifact. It becomes the typed input to the
next explicit owner stage; it cannot close the chain itself.

## Outputs

- one private `aoa_organ_access_live_cross_organ_proof_result_v1` report;
- content digests for every reviewed input;
- per-check booleans and the exact request expiry;
- fixed-false acceptance, memory-write, admission, and runtime-effect fields;
- explicit limitations and next owner `aoa-memo`.

## Failure modes

- an MCP call record does not match its owner artifact;
- a stage or receipt digest cannot be reconstructed;
- an output is not the next stage's byte-identical typed input;
- a profile exposes an unexpected tool;
- evidence or receipt is expired, future-dated, replayed, or wrong-owner;
- Memo candidate guardrails permit durable write;
- Evals request preparation claims verdict authority;
- SDK or proof output claims owner acceptance or runtime effect;
- private payloads are copied into source fixtures or generated readers.

## Blind spots

This eval does not prove:

- a network trace for every server process or Git-hosting authenticity;
- consumer-catalog completeness or model-selection benefit;
- rollback or runtime-effect safety; or
- that a later owner decision is correct.

Source-level profile tests and runtime process isolation remain independent
evidence.

## Interpretation guidance

Treat `supported_bounded` as one proof-owner verdict over one exact chain. It
is stronger than a successful MCP call and weaker than the following explicit
`aoa-memo` acceptance receipt. It never authorizes admission or effects.

Do not treat `supported_bounded` as:

- durable-memory acceptance;
- organ admission;
- runtime-effect authorization; or
- proof that another run, owner pair, or protocol profile is valid.

## Verification

- run `runners/run_live_handoff.py run-scenarios`;
- run the focused tests named by `runners/contract.json`;
- validate the bundle with `scripts/validate_repo.py --eval`;
- inspect the private report mode, digest, expiry, fixed-false authority fields,
  and exact next-owner route;
- re-run from fresh evidence after any source, schema, protocol, owner, or
  request-expiry change.

## Technique traceability

No technique dependency is required.

## Skill traceability

The `aoa-evals` owner procedure authorizes source evolution and review routing;
it does not supply proof evidence or strengthen this bundle's verdict.

## Adaptation points

- additional direct-owner stages require a new source revision;
- a modern wire pair requires an independently pinned protocol profile;
- admission and runtime-effect proof remain separate evals and owner decisions.
