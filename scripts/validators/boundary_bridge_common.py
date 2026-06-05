"""Shared boundary-bridge validation constants and helpers."""

from __future__ import annotations

REPO_VALIDATION_WORKFLOW_NAME = ".github/workflows/repo-validation.yml"
REPO_VALIDATION_AOA_MEMO_REF = "97f19698c94ebbebabe8b1b6f22e5ccff3bc5f1f"
REPO_VALIDATION_AOA_MEMO_PIN_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0028-repo-validation-aoa-memo-pin-refresh.md"
)
REPO_VALIDATION_AOA_MEMO_PIN_DECISION_REQUIRED_TOKENS = (
    REPO_VALIDATION_WORKFLOW_NAME,
    "Status: Superseded",
    "historical compatibility rationale",
    "AOA-EV-D-0115",
    "local release identity",
    "sibling checkout pins",
    "latest-sibling canary",
    "GitHub `Repo Validation`",
    "does not mutate `aoa-memo`",
)
BOUNDARY_BRIDGE_COMPATIBILITY_MAP_DOC_NAME = (
    "mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md"
)
BOUNDARY_BRIDGE_MECHANIC_README_NAME = "mechanics/boundary-bridge/README.md"
BOUNDARY_BRIDGE_MECHANIC_AGENTS_NAME = "mechanics/boundary-bridge/AGENTS.md"
BOUNDARY_BRIDGE_MECHANIC_PARTS_NAME = "mechanics/boundary-bridge/PARTS.md"
BOUNDARY_BRIDGE_MECHANIC_PROVENANCE_NAME = "mechanics/boundary-bridge/PROVENANCE.md"
BOUNDARY_BRIDGE_LEGACY_INDEX_NAME = "mechanics/boundary-bridge/legacy/INDEX.md"
BOUNDARY_BRIDGE_LEGACY_DISTILLATION_LOG_NAME = (
    "mechanics/boundary-bridge/legacy/DISTILLATION_LOG.md"
)
BOUNDARY_BRIDGE_LEGACY_RAW_README_NAME = "mechanics/boundary-bridge/legacy/raw/README.md"
BOUNDARY_BRIDGE_PARTS_README_NAME = "mechanics/boundary-bridge/parts/README.md"
BOUNDARY_BRIDGE_COMPATIBILITY_PART_README_NAME = (
    "mechanics/boundary-bridge/parts/compatibility-map/README.md"
)
BOUNDARY_BRIDGE_LATEST_SIBLING_CANARY_PART_README_NAME = (
    "mechanics/boundary-bridge/parts/latest-sibling-canary/README.md"
)
BOUNDARY_BRIDGE_ORCHESTRATOR_PROOF_ANCHORS_PART_README_NAME = (
    "mechanics/boundary-bridge/parts/orchestrator-proof-anchors/README.md"
)
BOUNDARY_BRIDGE_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0056-boundary-bridge-part-contract-guard.md"
)
BOUNDARY_BRIDGE_MECHANIC_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0008-boundary-bridge-mechanic-package.md"
)
SIBLING_CANARY_MATRIX_NAME = (
    "mechanics/boundary-bridge/parts/latest-sibling-canary/config/"
    "sibling_canary_matrix.json"
)
SIBLING_CANARY_RUNNER_NAME = (
    "mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/"
    "run_sibling_canary.py"
)
SIBLING_CANARY_COMMAND = f"python {SIBLING_CANARY_RUNNER_NAME} --repo-root . --format json"
SIBLING_CANARY_EXPLICIT_MATRIX_COMMAND = (
    f"python {SIBLING_CANARY_RUNNER_NAME} --repo-root . --matrix {SIBLING_CANARY_MATRIX_NAME}"
)
SIBLING_CANARY_EXPECTED_REPOS = (
    "aoa-techniques",
    "aoa-skills",
    "aoa-agents",
    "aoa-playbooks",
    "aoa-memo",
    "aoa-routing",
    "aoa-kag",
    "aoa-sdk",
    "aoa-stats",
    "abyss-stack",
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
BOUNDARY_BRIDGE_COMPATIBILITY_MAP_DOC_REQUIRED_TOKENS = (
    "compatibility map",
    "repo-qualified ref",
    "current/legacy/rejected/unresolved",
    "latest-sibling canary",
    "pinned `Repo Validation` ref",
    REPO_VALIDATION_AOA_MEMO_REF,
    SIBLING_CANARY_MATRIX_NAME,
    SIBLING_CANARY_RUNNER_NAME,
    "AGENTS.md#validation",
    "Authority-transfer pressure routes to the sibling owner",
)
BOUNDARY_BRIDGE_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md",
    "mechanics/boundary-bridge/PARTS.md",
    "mechanics/boundary-bridge/parts/README.md",
    SIBLING_CANARY_MATRIX_NAME,
    SIBLING_CANARY_RUNNER_NAME,
    REPO_VALIDATION_WORKFLOW_NAME,
    "latest-sibling canary",
    "pinned public-lane refresh",
    "current/legacy/rejected/unresolved",
    "route through the sibling owner before changing it",
    "bundle-local review",
)
BOUNDARY_BRIDGE_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "repo-qualified ref",
    "sibling owner route",
    "compatibility posture",
    "latest-sibling canary",
    SIBLING_CANARY_COMMAND,
)
BOUNDARY_BRIDGE_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "compatibility-map",
    "latest-sibling-canary",
    "Parts stay as limbs of `boundary-bridge`",
    "sibling owner route",
)
BOUNDARY_BRIDGE_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
BOUNDARY_BRIDGE_LEGACY_INDEX_REQUIRED_TOKENS = (
    "mechanics/sibling-proof-refs/",
    "mechanics/boundary-bridge/",
    "docs/SIBLING_PROOF_REFS.md",
    "mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md",
    "docs/ORCHESTRATOR_PROOF_ALIGNMENT.md",
    "mechanics/boundary-bridge/parts/orchestrator-proof-anchors/docs/ORCHESTRATOR_PROOF_ALIGNMENT.md",
    "generated/phase_alpha_eval_matrix.min.json",
    "mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/phase_alpha_eval_matrix.min.json",
)
BOUNDARY_BRIDGE_LEGACY_DISTILLATION_REQUIRED_TOKENS = (
    "boundary-bridge",
    "compatibility-map",
    "latest-sibling-canary",
    "orchestrator-proof-anchors",
    "phase-alpha-eval-matrix",
    "mechanics/sibling-proof-refs/",
    "Current route:",
    "new boundary-bridge work starts in the owning active part",
)
BOUNDARY_BRIDGE_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "No raw payload copies",
    "git history",
    "active boundary-bridge",
)
BOUNDARY_BRIDGE_PARTS_README_REQUIRED_TOKENS = (
    "compatibility-map/",
    "latest-sibling-canary/",
    "AGENTS.md#validation",
)
BOUNDARY_BRIDGE_COMPATIBILITY_PART_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "authored compatibility map",
    "current, legacy, rejected, or unresolved posture",
    "sibling owner acceptance",
    "sibling edit pressure appears",
)
BOUNDARY_BRIDGE_LATEST_SIBLING_CANARY_PART_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json",
    "mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py",
    "mechanics/boundary-bridge/parts/latest-sibling-canary/tests/test_sibling_canary.py",
    "GitHub `Repo Validation`",
    "sibling edit pressure appears",
    "GitHub `Repo Validation` replacement pressure appears",
)
BOUNDARY_BRIDGE_ORCHESTRATOR_PART_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "aoa-agents",
    "aoa-playbooks",
    "aoa-memo",
    "creating an `orchestrator` mechanic",
    "python scripts/build_catalog.py --check",
)
BOUNDARY_BRIDGE_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Boundary Bridge Part Contract Guard",
    "mechanics/boundary-bridge/parts/compatibility-map/README.md",
    "mechanics/boundary-bridge/parts/latest-sibling-canary/README.md",
    "mechanics/boundary-bridge/parts/orchestrator-proof-anchors/README.md",
    "part-level contracts",
    "sibling authority",
    "orchestrator",
    "latest-sibling-canary",
    "python scripts/validate_repo.py",
)
BOUNDARY_BRIDGE_DECISION_REQUIRED_TOKENS = (
    "mechanics/boundary-bridge/",
    "mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md",
    SIBLING_CANARY_MATRIX_NAME,
    SIBLING_CANARY_RUNNER_NAME,
    "latest-sibling canary",
    "current, legacy, rejected, or unresolved",
    "does not authorize editing sibling repositories",
)
