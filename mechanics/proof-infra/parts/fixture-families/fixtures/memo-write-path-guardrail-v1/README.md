# memo-write-path-guardrail-v1

Shared fixture family for `aoa-memo-write-path-guardrails`.

Use this family when the bounded question is whether a local memo candidate can
move toward reviewed aoa-memo corpus memory without losing source trust,
ingestion risk, derivation lineage, action-safety separation, durable landing
gate behavior, or access-plane authority split.

Canonical case archetypes:

- reviewed-intake packet with visible candidate, receipt, export, source refs,
  evidence refs, reviewed intake copy, landing receipt, and object refs
- blocked packet where `candidate_only`, untrusted source trust, missing
  source refs, missing evidence refs, or missing receipt refs cannot land
- derivation-lineage packet where rewritten candidate text can still walk back
  to source refs
- action-safety packet where embedded instructions remain source data
- authority-split packet where MCP or a local memo port validates or forwards
  without becoming durable memory authority
- downstream read-model packet where generated visibility remains weaker than
  the reviewed object

Family invariants:

- source trust must be visible before reviewed landing
- ingestion risks must remain reviewable before summarization or promotion
- derivation lineage must survive candidate shaping
- action-bearing source text must remain data unless a separate owner route
  authorizes action
- durable memory must land only through aoa-memo source change, reviewed-write
  posture, and validators
- MCP, local memo ports, KAG, RAG, vector, graph, and generated read models do
  not become memory authority

Replacement boundary:

- local repos may replace the concrete cases only if they preserve the same
  write-path guardrail question and still exercise all six bounded pressures
  above
- replacements must stay public-safe and must not depend on hidden runtime
  stores, private receipts, unreviewed promotion shortcuts, or source truth
  claims stronger than the packet evidence supports
