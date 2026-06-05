"""Proof-loop route-card, part-contract, provenance, and legacy checks."""

from __future__ import annotations

from pathlib import Path

from validators import mechanic_provenance_bridge, proof_loop_common as common
from validators.common import ValidationIssue


DECISION_RECORDS_README_NAME = common.DECISION_RECORDS_README_NAME
PROOF_LOOP_MECHANIC_README_NAME = common.PROOF_LOOP_MECHANIC_README_NAME
PROOF_LOOP_MECHANIC_AGENTS_NAME = common.PROOF_LOOP_MECHANIC_AGENTS_NAME
PROOF_LOOP_MECHANIC_PARTS_NAME = common.PROOF_LOOP_MECHANIC_PARTS_NAME
PROOF_LOOP_MECHANIC_PROVENANCE_NAME = common.PROOF_LOOP_MECHANIC_PROVENANCE_NAME
PROOF_LOOP_LEGACY_INDEX_NAME = common.PROOF_LOOP_LEGACY_INDEX_NAME
PROOF_LOOP_LEGACY_DISTILLATION_LOG_NAME = common.PROOF_LOOP_LEGACY_DISTILLATION_LOG_NAME
PROOF_LOOP_LEGACY_RAW_README_NAME = common.PROOF_LOOP_LEGACY_RAW_README_NAME
PROOF_LOOP_PARTS_README_NAME = common.PROOF_LOOP_PARTS_README_NAME
PROOF_LOOP_ROUTE_SMOKE_PART_README_NAME = common.PROOF_LOOP_ROUTE_SMOKE_PART_README_NAME
PROOF_LOOP_SMOKE_REPORT_NAME = common.PROOF_LOOP_SMOKE_REPORT_NAME
PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_NAME = common.PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_NAME
PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_NAME = common.PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_NAME
PROOF_LOOP_MECHANIC_DECISION_NAME = common.PROOF_LOOP_MECHANIC_DECISION_NAME

MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS = (
    mechanic_provenance_bridge.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
)
PROOF_LOOP_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "proof question -> selection route -> source proof object",
    "candidate evidence packet",
    "bundle-local review",
    "optional receipt",
    "Step Owners",
    "EVAL_SELECTION.md",
    "mechanics/proof-object/",
    "mechanics/proof-infra/",
    "mechanics/audit/",
    "mechanics/publication-receipts/",
    "mechanics/boundary-bridge/",
    "PARTS.md",
    "route-smoke",
    "generated readers remain derived readers below bundle-local proof authority",
    "python scripts/validate_repo.py",
)
PROOF_LOOP_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "active proof-loop route",
    "source proof object",
    "candidate evidence packet",
    "bundle-local review",
    "optional receipt",
    "Keep generated readers subordinate",
    "Keep receipts below reviewed reports",
    "mechanics/proof-loop/PARTS.md",
    "Keep route-smoke reports",
    "python scripts/validate_repo.py",
)
PROOF_LOOP_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-loop/",
    "pick proof question",
    "existing mechanics",
    "does not own bundle meaning",
    "does not create runtime dispatch",
    "does not allow receipts",
)
PROOF_LOOP_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
PROOF_LOOP_LEGACY_INDEX_REQUIRED_TOKENS = (
    "reports/proof-loop-local-route-smoke-v1.md",
    "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md",
    "docs/decisions/AOA-EV-D-0020-proof-loop-local-smoke-report.md",
    "docs/decisions/AOA-EV-D-0030-proof-loop-route-smoke-part.md",
    "Former root report paths are provenance only",
)
PROOF_LOOP_LEGACY_DISTILLATION_REQUIRED_TOKENS = (
    "proof-loop",
    "route-smoke",
    "reports/proof-loop-local-route-smoke-v1.md",
    "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md",
    "Current route:",
    "new proof-loop route-smoke work starts in the owning active part",
)
PROOF_LOOP_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "No raw payload copies",
    "git history",
    "active proof-loop",
)
PROOF_LOOP_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "Proof Loop / Part Index",
    "proof question -> selection route -> source proof object",
    "route-smoke",
    PROOF_LOOP_SMOKE_REPORT_NAME,
    "bounded part contracts inside the parent mechanic",
    "no eval result receipt",
)
PROOF_LOOP_PARTS_README_REQUIRED_TOKENS = (
    "Proof Loop / Parts Route",
    "## Operating Card",
    "| role | lower index for active proof-loop part artifacts |",
    "## Active Parts",
    "route-smoke/README.md",
    "## Owner Pressure Routes",
    "| source proof object meaning | `mechanics/proof-object/` plus affected `evals/**/EVAL.md` and `evals/**/eval.yaml` |",
    "| support contract pressure | `mechanics/proof-infra/` |",
    "| candidate evidence packet | `mechanics/audit/` |",
    "| receipt publication or receipt-intake pressure | `mechanics/publication-receipts/` |",
    "## Part Admission Route",
    "| one local loop path needs public-safe routeability proof | bounded route-smoke report with no receipt publication | `route-smoke/README.md` |",
    "mechanics/proof-loop/parts/AGENTS.md#validation",
)
PROOF_LOOP_ROUTE_SMOKE_PART_README_REQUIRED_TOKENS = (
    "Route Smoke Part",
    PROOF_LOOP_SMOKE_REPORT_NAME,
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "bounded route-smoke report artifact",
    "no eval result receipt",
    "route-smoke report read as eval-result run",
    "full proof-loop completeness",
    "python scripts/validate_repo.py",
)
PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_REQUIRED_TOKENS = (
    PROOF_LOOP_SMOKE_REPORT_NAME,
    "route-smoke",
    "root `reports/`",
    "mechanics/proof-loop/PARTS.md",
    "does not create an eval result receipt",
)
PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_REQUIRED_TOKENS = (
    "Proof Loop Route-Smoke Contract",
    "mechanics/proof-loop/parts/route-smoke/README.md",
    "part-level contract",
    "stronger owner split",
    "stop-lines",
    "no eval result receipt",
    "full proof-loop completeness",
    "python scripts/validate_repo.py",
)


def validate_proof_loop_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (PROOF_LOOP_MECHANIC_README_NAME, PROOF_LOOP_MECHANIC_REQUIRED_TOKENS),
        (PROOF_LOOP_MECHANIC_AGENTS_NAME, PROOF_LOOP_MECHANIC_AGENTS_REQUIRED_TOKENS),
        (PROOF_LOOP_MECHANIC_PARTS_NAME, PROOF_LOOP_MECHANIC_PARTS_REQUIRED_TOKENS),
        (PROOF_LOOP_PARTS_README_NAME, PROOF_LOOP_PARTS_README_REQUIRED_TOKENS),
        (PROOF_LOOP_ROUTE_SMOKE_PART_README_NAME, PROOF_LOOP_ROUTE_SMOKE_PART_README_REQUIRED_TOKENS),
        (
            PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_NAME,
            PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_REQUIRED_TOKENS,
        ),
        (
            PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_NAME,
            PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_REQUIRED_TOKENS,
        ),
        (
            DECISION_RECORDS_README_NAME,
            (
                PROOF_LOOP_ROUTE_SMOKE_PART_DECISION_NAME,
                PROOF_LOOP_ROUTE_SMOKE_CONTRACT_DECISION_NAME,
                "Proof Loop Route-Smoke Contract",
            ),
        ),
        (PROOF_LOOP_MECHANIC_PROVENANCE_NAME, PROOF_LOOP_MECHANIC_PROVENANCE_REQUIRED_TOKENS),
        (PROOF_LOOP_LEGACY_INDEX_NAME, PROOF_LOOP_LEGACY_INDEX_REQUIRED_TOKENS),
        (PROOF_LOOP_LEGACY_DISTILLATION_LOG_NAME, PROOF_LOOP_LEGACY_DISTILLATION_REQUIRED_TOKENS),
        (PROOF_LOOP_LEGACY_RAW_README_NAME, PROOF_LOOP_LEGACY_RAW_README_REQUIRED_TOKENS),
        (PROOF_LOOP_MECHANIC_DECISION_NAME, PROOF_LOOP_MECHANIC_DECISION_REQUIRED_TOKENS),
    ):
        common.require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)
    return issues
