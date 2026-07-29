# Eval Integrity Check

- The unit is one organ capability on one policy plane and protocol pair.
- All sixteen maturity axes are present and independent.
- Every asserted axis has an observation time, evidence ref, evidence kind,
  revision, and expiry or freshness policy.
- Evidence kinds are axis-specific.
- Every axis binds to its designated source, package, deploy, or
  consumer-schema revision slot, not merely any revision present in the packet.
- `endpoint_ready` cannot ground `result_grounded`.
- `central_eval_result` cannot ground `owner_accepted`.
- Read and candidate planes cannot authorize internal or external effects.
- The result cannot authorize admission or infer owner acceptance.
- `insufficient_evidence` remains a valid bounded readout.
- A positive verdict requires at least one independently asserted axis.
- The fixture set is public-safe and contains no live credentials or payloads.
- The runner and report name the source-only limit.
- The optional live materializer reads explicit paths only and has no MCP,
  credential, registry-mutation, admission, or effect path.
- Registry, observation, and canary inputs are private regular non-symlink
  files; deployment latest and immutable record are byte-identical.
- Registry, deployment, observation, endpoint, schema, package/server, and
  immutable canary identities remain cross-bound.
- A successful canary's private result artifact is content-addressed, bound to
  the receipt, marked untrusted/no-instruction, and asserts no maturity axis.
- A stack result-contract match never asserts `result_grounded`; owner
  grounding remains a separate owner-issued review.
- An optional owner-result review binds exactly to registry
  capability/primitive/schema identity, source revision, stack capture,
  result artifact, schema digests, and an unexpired evidence window.
- Only owner `grounded` may assert `result_grounded`; only owner freshness
  `exact` may assert `freshness_satisfied`.
- Owner-result review never asserts organ-contract `owner_reviewed`,
  `owner_accepted`, central proof, admission, cross-organ proof, or rollback.
- Materialized output remains `insufficient_evidence` and mode `0600`.
- A private packet review binds the exact packet and source-contract digests,
  replays all checked-in negative scenarios, preserves the packet's own
  verdict, and never infers owner acceptance, admission, effects, cross-organ
  benefit, or rollback.
