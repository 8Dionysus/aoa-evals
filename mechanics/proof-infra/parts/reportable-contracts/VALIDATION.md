# Proof Infra / Reportable Contracts Validation

Executable validation commands for this part live in [parent parts AGENTS](../AGENTS.md#validation).

Use the `reportable-contracts` child validation block there. It covers the
active-organ C21-C23 schema and semantic validator, its executable negative
corpus including canonical C22 self-digest tampering, the bounded scorer
helper, and broader repository checks. The consuming
`aoa-memo-active-organ-offline-replay` bundle adds 25 conformance cases and
bundle-local methodology tests through its own source route. This file is the
part-local validation route marker so the README can remain a contract map.
