# Live Packet Materializer Contract

## Authority

`materialize_live_packet.py` composes one private candidate
`organ_access_proof_packet_v1`. It can consume an already-issued owner-result
review, but it has no authority to issue or alter that review and no
proof-verdict, acceptance, admission, effect, or rollback authority.

The materializer reads only operator-supplied paths and writes one private
packet. It does not read bearer credentials, call MCP, scan workspaces, update
the registry, or mutate runtime state.

## Required inputs

- `--organ`: the exact registry and runtime organ identifier;
- `--registry`: a mode-private, deny-by-default
  `aoa_organ_registry_source_v1` source;
- `--deployment`: an exact `abyss_stack_mcp_deployment_manifest_v1`
  `latest.json` with its byte-identical content-addressed record beside it;
- `--observation`: a mode-private, unexpired
  `abyss_stack_runtime_observation_v1`;
- `--canary`: the mode-private immutable stack canary v1 or current attested
  v2 record under `records/<organ>/<receipt-digest>.json`, not a copied or
  rewritten receipt;
- `--result`: for a successful call, the exact mode-private artifact named by
  the canary `result_artifact_ref`;
- optionally `--owner-review`: one mode-private
  `aoa_organ_owner_result_review_v1` receipt issued by the source or acceptance
  owner for that exact capture;
- `--output`: a path beneath a mode-private directory; and
- optionally `--materialized-at`: an aware RFC 3339 time for deterministic
  replay.

The runtime observation must already include the stack canary overlay. Its
endpoint evidence and blocked canary evidence must name the same immutable
canary path, receipt digest, observation time, expiry, endpoint, schema, and
canary route supplied to the materializer.

## Binding checks

The materializer fails closed on:

- symlinked, non-regular, oversized, malformed, duplicate-key, secret-bearing,
  or overly broad private inputs;
- an expired registry, observation, or canary;
- deployment content-address or immutable-record mismatch;
- registry/observation owner, source revision, or record mismatch;
- package, deployed tree, manifest, runtime, endpoint, schema, server version,
  canary route, or receipt-reference mismatch;
- missing, rewritten, relocated, secret-bearing, or digest-mismatched
  successful-call result artifacts;
- malformed v2 Ed25519 attestation metadata or receipt/result signer drift;
- owner-review SDK-contract, content-address, owner-role, registry
  capability/primitive/schema, source-revision, capture-ref, result-digest,
  schema-digest, watermark, evidence, freshness-window, or authority-ceiling
  mismatch;
- a canary that exceeds the stack-issued read-only claim, or an observation
  that treats the stack canary as owner grounding.

These are local structural, permission, content-address, and cross-input
checks. For v2 they validate the attestation encoding and signer continuity,
but they do not authenticate the Ed25519 signature or establish the signer as
an owner trust root. That remains an explicit blind spot unless an
independently pinned owner verifier supplies a separately bound review.

## Output and claim ceiling

The output is atomically written with mode `0600` and validates against the
bundle packet contract. Its verdict is always `insufficient_evidence`.

The materializer may assert only:

- `declared`;
- `packaged`;
- `exported`;
- `deployed`;
- `process_alive`, when exact evidence remains unexpired;
- `endpoint_ready`;
- `registry_indexed`;
- `schema_observed`; and
- `call_succeeded`, when the stack receipt says the authenticated call
  succeeded;
- `result_grounded`, only from a content-addressed, exactly bound review whose
  owner verdict is `grounded`; and
- `freshness_satisfied`, only when that same review says `exact`.

It never asserts:

- `owner_reviewed`;
- `consumer_registered`;
- `owner_accepted`;
- `cross_organ_proven`; or
- `rollback_proven`.

A stack `result_contract_matched` value is call/result-shape evidence only. The
`result_grounded` axis requires a separate `owner_grounding_review` issued
through the source/acceptance-owner route. A result review is distinct from the
organ-contract `owner_reviewed` axis and never implies acceptance, proof, or
admission.

## Operator invocation

The runnable repository command belongs to
[`docs/validation/COMMAND_AUTHORITY.md`](../../../../docs/validation/COMMAND_AUTHORITY.md).
Select the materializer there, then supply the required inputs above. The
script's argument parser remains the executable authority for exact flag
spelling; this contract owns only their meaning and binding requirements.

Successful materialization means only that the output is an honest,
source-contract-valid candidate assembled from mutually bound local inputs. It
is not a central eval proof result.
