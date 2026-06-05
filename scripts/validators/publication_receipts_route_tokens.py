"""Publication receipt route token constants."""

from __future__ import annotations

from validators.publication_receipts_route_paths import (
    RECEIPT_INTAKE_DRY_REVIEW_NAME,
)

RECEIPT_INTAKE_DRY_REVIEW_REQUIRED_TOKENS = (
    "receipt_intake_dry_review",
    "candidate_payload_preview",
    "eval-result-receipt.schema.json",
    "stats-event-envelope.schema.json",
    "publish_live_receipts.py",
    ".aoa/live_receipts/eval-result-receipts.jsonl",
    "dry_review_only",
    "not_published",
    "not_created",
    "not_attempted",
    "publication pressure routes to a receipt envelope",
    "runtime acceptance pressure",
)
RECEIPT_INTAKE_DRY_REVIEW_DECISION_REQUIRED_TOKENS = (
    RECEIPT_INTAKE_DRY_REVIEW_NAME,
    "eval_result_receipt",
    "stats-event-envelope",
    ".aoa/live_receipts/",
    "candidate_payload_preview",
    "event_id",
    "dry review is weaker than a receipt",
    "Do not infer that an eval result receipt was published",
)
MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS = (
    "`PROVENANCE.md` is the active-to-archive bridge for this mechanic.",
    "Use active surfaces first:",
    "DIRECTION.md",
    "PARTS.md",
    "parts/",
    "legacy archive",
    "legacy/README.md",
    "owns its own details",
    "archive details stay in the legacy archive",
)
PUBLICATION_RECEIPTS_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md",
    "mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json",
    "mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json",
    "mechanics/publication-receipts/parts/receipt-payload/examples/eval_result_receipt.example.json",
    "mechanics/publication-receipts/parts/live-publisher/scripts/publish_live_receipts.py",
    "mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py",
    "mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py",
    "mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py",
    ".aoa/live_receipts/eval-result-receipts.jsonl",
    "eval_result_receipt",
    "stats-event-envelope",
    "optional receipt",
    "bundle-local verdict meaning",
    "repo-global score",
    "python scripts/validate_repo.py",
    "python scripts/validate_semantic_agents.py",
)
PUBLICATION_RECEIPTS_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "eval-result receipt",
    "stats-event-envelope",
    ".aoa/live_receipts/",
    "bundle-local report",
    "aoa-stats",
    "append-only",
    "public-safe",
    "python scripts/validate_repo.py",
)
PUBLICATION_RECEIPTS_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/publication-receipts/",
    "eval-result receipt",
    "stats-envelope-mirror",
    "aoa-stats",
    "does not move `.aoa/live_receipts/`",
    "bundle-local report",
    "repo-global score",
)
PUBLICATION_RECEIPTS_MECHANIC_PROVENANCE_REQUIRED_TOKENS = (
    MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
)
PUBLICATION_RECEIPTS_LEGACY_INDEX_REQUIRED_TOKENS = (
    "docs/EVAL_RESULT_RECEIPT_GUIDE.md",
    "mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md",
    "schemas/eval-result-receipt.schema.json",
    "mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json",
    "scripts/publish_live_receipts.py",
    "mechanics/publication-receipts/parts/live-publisher/scripts/publish_live_receipts.py",
    "reports/eval-result-receipt-intake-dry-review-v1.json",
    "mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json",
    ".aoa/live_receipts/eval-result-receipts.jsonl",
)
PUBLICATION_RECEIPTS_LEGACY_DISTILLATION_REQUIRED_TOKENS = (
    "publication-receipts",
    "receipt-payload",
    "stats-envelope-mirror",
    "live-publisher",
    "intake-dry-review",
    "Current route:",
    "new publication-receipt work starts in the owning active part",
)
PUBLICATION_RECEIPTS_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "No raw payload copies",
    "git history",
    "active publication-receipts",
)
PUBLICATION_RECEIPTS_PART_README_COMMON_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "python scripts/validate_repo.py",
)
PUBLICATION_RECEIPTS_RECEIPT_PAYLOAD_PART_REQUIRED_TOKENS = (
    "Receipt Payload Part",
    "eval_result_receipt",
    "schemas/eval-result-receipt.schema.json",
    "examples/eval_result_receipt.example.json",
    "reviewed bounded report",
    "source bundle",
    "The payload is a publication sidecar",
    "schema-valid payload reads as a published receipt",
) + PUBLICATION_RECEIPTS_PART_README_COMMON_TOKENS
PUBLICATION_RECEIPTS_STATS_ENVELOPE_PART_REQUIRED_TOKENS = (
    "Stats Envelope Mirror Part",
    "schemas/stats-event-envelope.schema.json",
    "canonical `aoa-stats`",
    "event-kind vocabulary",
    "owner-local live receipt log",
    "dry-review artifacts",
    "mirror edit reads as canonical `aoa-stats` schema work",
) + PUBLICATION_RECEIPTS_PART_README_COMMON_TOKENS
PUBLICATION_RECEIPTS_LIVE_PUBLISHER_PART_REQUIRED_TOKENS = (
    "Live Publisher Part",
    "scripts/publish_live_receipts.py",
    "tests/test_publish_live_receipts.py",
    "tests/test_live_receipt_log.py",
    "append-only JSONL writes",
    "duplicate `event_id` skips",
    "dry-review payload preview looks publishable",
) + PUBLICATION_RECEIPTS_PART_README_COMMON_TOKENS
PUBLICATION_RECEIPTS_INTAKE_DRY_REVIEW_PART_REQUIRED_TOKENS = (
    "Intake Dry Review Part",
    "receipt_intake_dry_review",
    "candidate_payload_preview",
    "`receipt_status` stays",
    "`not_published`",
    "top-level `event_kind`, `event_id`, `observed_at`, `object_ref`,",
    "`.aoa/live_receipts/` append appears",
) + PUBLICATION_RECEIPTS_PART_README_COMMON_TOKENS
PUBLICATION_RECEIPTS_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Publication Receipts Part Contract Guard",
    "mechanics/publication-receipts/parts/receipt-payload/README.md",
    "mechanics/publication-receipts/parts/stats-envelope-mirror/README.md",
    "mechanics/publication-receipts/parts/live-publisher/README.md",
    "mechanics/publication-receipts/parts/intake-dry-review/README.md",
    "part-level contracts",
    "receipt-payload",
    "stats-envelope-mirror",
    "live-publisher",
    "intake-dry-review",
    "stronger owner split",
    "stop-lines",
    "not_published",
    "python scripts/validate_repo.py",
)


__all__ = tuple(name for name in globals() if name.endswith("_TOKENS"))
