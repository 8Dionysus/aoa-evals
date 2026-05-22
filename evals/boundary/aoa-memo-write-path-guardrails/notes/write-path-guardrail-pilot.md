# Write Path Guardrail Pilot

This bundle is the first narrow downstream pilot for memory write-path safety.

It treats a guarded write as supportable only when the proof flow preserves, at
minimum:

- source trust and source refs before review
- ingestion risk markers before summarization or promotion
- derivation lineage for rewritten candidate material
- action-safety separation for embedded instructions or action pressure
- reviewed-write landing gates before durable corpus object creation
- MCP and local memo port posture as access or forwarding planes only

The pilot intentionally does not absorb recall precision, contradiction
handling, reviewed-candidate adoption, KAG lift, vector search, role
authorization, or broad platform security.

The current materialized proof flow runs through `aoa-memo` write-path
guardrail docs, reviewed-intake landing tests, reviewed intake packets, landing
receipts, durable `memo/objects/` bundles, this bundle's fixture and runner
contracts, and the schema-backed companion reports under `reports/`.

The current draft is allowed to report `mixed support`.
The point of the pilot is to expose what is already gated and what still needs
packet-backed hardening before memory growth accelerates.
