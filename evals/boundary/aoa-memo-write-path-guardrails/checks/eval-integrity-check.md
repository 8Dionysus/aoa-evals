# Eval Integrity Check

- The bundle stays on candidate-to-reviewed-memory write-path guardrails and
  does not drift into recall precision or contradiction handling.
- The bundle does not convert source refs into source truth.
- The bundle does not convert MCP validation, local receipts, or dry-runs into
  durable memory review authority.
- The bundle does not convert absence of adversarial input into proof of
  poisoning resistance.
- The bundle keeps KAG, RAG, graph, vector, and generated read-model surfaces
  downstream of reviewed memory objects.
- The bundle keeps action-bearing source text as data unless a separate owner
  route authorizes action.
