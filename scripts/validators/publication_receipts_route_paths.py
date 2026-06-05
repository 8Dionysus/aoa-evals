"""Publication receipt route path constants."""

from __future__ import annotations

from pathlib import Path

from validators.publication_receipts_common import PUBLICATION_RECEIPTS_PARTS_ROOT

EVAL_RESULT_RECEIPT_PUBLISHER_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/live-publisher/scripts/publish_live_receipts.py"
)
PROOF_LOOP_LOCAL_REPORT_NAME = (
    "evals/workflow/aoa-verification-honesty/reports/"
    "aoa-evals-slice-19-lifecycle-contract.report.json"
)
RECEIPT_INTAKE_DRY_REVIEW_NAME = (
    "mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json"
)
RECEIPT_INTAKE_DRY_REVIEW_DECISION_NAME = "docs/decisions/AOA-EV-D-0024-receipt-intake-dry-review.md"
PROOF_LOOP_MECHANIC_README_NAME = "mechanics/proof-loop/README.md"
PUBLICATION_RECEIPTS_MECHANIC_README_NAME = "mechanics/publication-receipts/README.md"
PUBLICATION_RECEIPTS_MECHANIC_AGENTS_NAME = "mechanics/publication-receipts/AGENTS.md"
PUBLICATION_RECEIPTS_MECHANIC_PROVENANCE_NAME = "mechanics/publication-receipts/PROVENANCE.md"
PUBLICATION_RECEIPTS_RECEIPT_PAYLOAD_PART_README_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/receipt-payload/README.md"
)
PUBLICATION_RECEIPTS_STATS_ENVELOPE_PART_README_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/stats-envelope-mirror/README.md"
)
PUBLICATION_RECEIPTS_LIVE_PUBLISHER_PART_README_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/live-publisher/README.md"
)
PUBLICATION_RECEIPTS_INTAKE_DRY_REVIEW_PART_README_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/intake-dry-review/README.md"
)
PUBLICATION_RECEIPTS_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0057-publication-receipts-part-contract-guard.md"
)
PUBLICATION_RECEIPTS_MECHANIC_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0013-publication-receipts-mechanic-package.md"
)
PUBLICATION_RECEIPTS_LEGACY_INDEX_NAME = "mechanics/publication-receipts/legacy/INDEX.md"
PUBLICATION_RECEIPTS_LEGACY_DISTILLATION_LOG_NAME = (
    "mechanics/publication-receipts/legacy/DISTILLATION_LOG.md"
)
PUBLICATION_RECEIPTS_LEGACY_RAW_README_NAME = "mechanics/publication-receipts/legacy/raw/README.md"
DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
DECISION_INDEX_PATHS = (
    Path("docs/decisions/indexes/by-number.md"),
    Path("docs/decisions/indexes/by-date.md"),
    Path("docs/decisions/indexes/by-surface.md"),
    Path("docs/decisions/indexes/by-mechanic.md"),
    Path("docs/decisions/indexes/by-validation-guard.md"),
)


__all__ = tuple(
    name
    for name in globals()
    if name.endswith("_NAME") or name == "DECISION_INDEX_PATHS"
)
