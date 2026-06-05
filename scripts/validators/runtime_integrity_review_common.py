"""Runtime integrity review shared constants."""

from __future__ import annotations


RUNTIME_INTEGRITY_REVIEW_DOC_NAME = (
    "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md"
)
RUNTIME_INTEGRITY_REVIEW_SCHEMA_NAME = "runtime-integrity-review.schema.json"
RUNTIME_INTEGRITY_REVIEW_SCHEMA_PATH = (
    "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json"
)
RUNTIME_INTEGRITY_REVIEW_EXAMPLE_NAME = (
    "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json"
)
RUNTIME_INTEGRITY_REVIEW_BUDGET_REF = (
    "Agents-of-Abyss:mechanics/experience/parts/continuity-context/CONTRACT.md#stronger-owner-split"
)
RUNTIME_INTEGRITY_REVIEW_REQUIRED_TOKENS = (
    "`candidate_only`",
    "`human_review_needed`",
    "`budget_ref`",
    "`evidence_refs`",
    "`replay_requirements`",
    "`forbidden_claims`",
    "`sealed_verdict`",
    "`activation_authority`",
    "`owner_override`",
    "`canon_write`",
    "Proof-canon pressure routes to bundle-local proof review.",
    "Runtime-continuity activation pressure routes to Experience and runtime-owner",
)
RUNTIME_INTEGRITY_REVIEW_LANDING_TOKENS = (
    "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
    "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json",
    "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json",
    "`candidate_only`",
    "`human_review_needed`",
)
RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS = (
    "repo:aoa-evals/mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md",
    "repo:aoa-evals/mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
    "repo:aoa-routing/docs/LIVE_SESSION_REENTRY_ROUTE_REVIEW.md",
    "repo:aoa-agents/mechanics/checkpoint/parts/continuity-lane/docs/self-agency-continuity-lane.md",
    "repo:aoa-memo/mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json",
    "repo:aoa-memo/mechanics/writeback/docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md",
)
RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS = (
    "selected_evidence_only",
    "owner_local_replay_required",
    "fail_closed",
    "publication_requires_review",
)
RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS = (
    "sealed_verdict",
    "activation_authority",
    "owner_override",
    "canon_write",
)
