# Eval Integrity Check

- The unit is one exact orchestration run, not an organ class.
- The snapshot is reconstructed from its request and ordered stages.
- Every stage, snapshot, receipt, and owner output is content-bound.
- KAG, Memo, and Evals use separate direct MCP call records.
- Tool inventories match the pinned read/candidate profiles exactly.
- Stage input equals the preceding output artifact.
- Owner, source revision, schema identity, authority ceiling, and expiry remain explicit.
- Stale, malformed, denied, wrong-owner, expired, replayed, or schema-drifted input fails closed.
- Memo remains candidate-only and cannot write durable memory.
- Evals request preparation cannot execute an eval or issue a verdict.
- The proof result names `aoa-memo` as next owner and cannot accept itself.
- SDK owner execution, proof computation, durable write, acceptance inference,
  admission, and runtime execution remain false.
- Private evidence stays outside the repository; only fictional scenario data is public.
