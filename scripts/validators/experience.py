"""Experience mechanic route and part-contract validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators.common import ValidationIssue


EXPERIENCE_MECHANIC_README_NAME = "mechanics/experience/README.md"
EXPERIENCE_MECHANIC_AGENTS_NAME = "mechanics/experience/AGENTS.md"
EXPERIENCE_MECHANIC_PARTS_NAME = "mechanics/experience/PARTS.md"
EXPERIENCE_MECHANIC_PROVENANCE_NAME = "mechanics/experience/PROVENANCE.md"
EXPERIENCE_PROTOCOL_PART_README_NAME = (
    "mechanics/experience/parts/protocol-integrity/README.md"
)
EXPERIENCE_CERTIFICATION_PART_README_NAME = (
    "mechanics/experience/parts/certification-gate/README.md"
)
EXPERIENCE_ADOPTION_PART_README_NAME = (
    "mechanics/experience/parts/adoption-federation/README.md"
)
EXPERIENCE_GOVERNANCE_PART_README_NAME = (
    "mechanics/experience/parts/governance-runtime-boundary/README.md"
)
EXPERIENCE_OFFICE_PART_README_NAME = (
    "mechanics/experience/parts/office-release-train/README.md"
)
EXPERIENCE_MECHANIC_DECISION_NAME = "docs/decisions/AOA-EV-D-0033-experience-mechanic-package.md"
EXPERIENCE_VERDICT_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0043-experience-verdict-residue-parts.md"
)
EXPERIENCE_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0063-experience-part-contract-guard.md"
)
EXPERIENCE_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "AoA-aligned",
    "experience pressure",
    "protocol-integrity",
    "certification-gate",
    "adoption-federation",
    "governance-runtime-boundary",
    "office-release-train",
    "evals/boundary/aoa-experience-protocol-integrity/EVAL.md",
    "evals/boundary/aoa-experience-certification-gate-integrity/EVAL.md",
    "runtime distillation candidate adoption",
    "Stronger Owner Split",
    "Stop-Lines",
    "| live workspace runtime or service dispatch pressure | `abyss-stack` runtime route |",
    "| office installation or assistant operational authority pressure | `aoa-agents` and owner operator route |",
    "| operator certification, release approval, deployment approval, or rollout promotion pressure | Agents-of-Abyss, release-support, and owner approval route |",
    "| owner-local adoption, consent, or acceptance pressure | owner repository adoption route |",
    "| memory sovereignty, recall authority, or memo canon pressure | `aoa-memo` memory route |",
    "| live router behavior or routing-layer authorship pressure | `aoa-routing` route-authority lane |",
    "| KAG promotion into owner repositories pressure | `aoa-kag` graph route plus owner adoption route |",
    "| Tree-of-Sophia runtime write or authored-meaning pressure | Tree-of-Sophia authored-meaning route |",
    "| broad Experience success pressure | bundle-local proof object plus source-owner evidence review |",
    "python -m pytest -q mechanics/experience/parts/protocol-integrity/tests/test_experience_protocol_integrity.py",
)
EXPERIENCE_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "Experience proof work",
    "mechanics/experience/PARTS.md",
    "PROVENANCE.md",
    "Keep source proof bundles under `evals/`",
    "Create Experience parts from a recurring proof operation",
    "python scripts/validate_repo.py",
)
EXPERIENCE_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "protocol-integrity",
    "certification-gate",
    "adoption-federation",
    "governance-runtime-boundary",
    "office-release-train",
    "Inputs",
    "Outputs",
    "Owner split",
    "Stop-lines",
    "Validation",
    "Continuity-context",
    "| live runtime activation or service dispatch | `abyss-stack` runtime route |",
    "| office installation or assistant operational authority | `aoa-agents` and owner operator route |",
    "| operator certification, release approval, deployment approval, or rollout promotion | Agents-of-Abyss, release-support, and owner approval route |",
    "| owner-local adoption, consent, or acceptance | owner repository adoption route |",
    "| memory canon, recall authority, or memory sovereignty | `aoa-memo` memory route |",
    "| route activation or routing-layer authorship | `aoa-routing` route-authority lane |",
    "| KAG forced adoption into owner repositories | `aoa-kag` graph route plus owner adoption route |",
    "| direct ToS runtime write or ToS-authored meaning | Tree-of-Sophia authored-meaning route |",
    "| broad Experience success | bundle-local proof object plus source-owner evidence review |",
)
EXPERIENCE_PART_README_COMMON_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
)
EXPERIENCE_PROTOCOL_PART_REQUIRED_TOKENS = (
    "aoa-experience-protocol-integrity",
    "mechanics/experience/parts/protocol-integrity/fixtures/experience-verdict-protocol-integrity-v1/README.md",
    "mechanics/experience/parts/protocol-integrity/tests/test_experience_protocol_integrity.py",
    "| Experience doctrine pressure | Agents-of-Abyss center route |",
    "| underlying-experience success pressure | owner evidence and source-review route |",
    "python scripts/build_catalog.py --check",
) + EXPERIENCE_PART_README_COMMON_REQUIRED_TOKENS
EXPERIENCE_CERTIFICATION_PART_REQUIRED_TOKENS = (
    "experience certification gate proof",
    "mechanics/experience/parts/certification-gate/fixtures/experience-certification-gate-integrity-v1/README.md",
    "rollback_drill_verdict",
    "| certification authority pressure | Agents-of-Abyss and owner operator certification route |",
    "| release approval pressure | release-support and owner approval route |",
    "| runtime health pressure | `abyss-stack` runtime health route |",
    "python scripts/build_catalog.py --check",
) + EXPERIENCE_PART_README_COMMON_REQUIRED_TOKENS
EXPERIENCE_ADOPTION_PART_REQUIRED_TOKENS = (
    "Experience adoption proof",
    "federation-harvest",
    "KAG/ToS boundary",
    "| owner-local adoption pressure | owner repository adoption route |",
    "| routing authorship pressure | `aoa-routing` route-authority lane |",
    "| runtime distillation candidate adoption pressure | `mechanics/distillation/parts/runtime-candidate-adoption/` |",
    "python scripts/build_catalog.py --check",
) + EXPERIENCE_PART_README_COMMON_REQUIRED_TOKENS
EXPERIENCE_GOVERNANCE_PART_REQUIRED_TOKENS = (
    "Experience governance and runtime-boundary",
    "APPEAL_REVIEW_VERDICT.md",
    "STAY_ORDER_ENFORCEMENT_VERDICT.md",
    "VOTE_SEAL_INTEGRITY_VERDICT.md",
    "REPLAY_HISTORY_INTEGRITY_VERDICT.md",
    "authority-resolution",
    "constitution-runtime",
    "| governance authority pressure | Agents-of-Abyss center governance route |",
    "| runtime enforcement pressure | `abyss-stack` runtime route |",
    "python scripts/validate_repo.py",
) + EXPERIENCE_PART_README_COMMON_REQUIRED_TOKENS
EXPERIENCE_OFFICE_PART_REQUIRED_TOKENS = (
    "Experience office and release-train",
    "REPLAY_AUDIT_VERDICTS.md",
    "SERVICE_MESH_REGRESSION_VERDICTS.md",
    "mechanics/experience/parts/certification-gate/schemas/rollback_drill_verdict_v1.json",
    "| office installation pressure | Agents-of-Abyss, `aoa-agents`, and owner operator route |",
    "| release approval pressure | Agents-of-Abyss, release-support, and owner approval route |",
    "| release-support publication pressure | `release-support` publication posture route inside `aoa-evals` |",
    "python scripts/validate_repo.py",
) + EXPERIENCE_PART_README_COMMON_REQUIRED_TOKENS
EXPERIENCE_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/experience/",
    "AoA-aligned",
    "protocol-integrity",
    "certification-gate",
    "adoption-federation",
    "governance-runtime-boundary",
    "office-release-train",
    "Source proof bundles stay under `evals/`",
    "operator certification",
    "owner-local adoption",
    "python scripts/validate_repo.py",
)
EXPERIENCE_VERDICT_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "mechanics/experience/parts/governance-runtime-boundary/docs/",
    "mechanics/experience/parts/office-release-train/docs/",
    "APPEAL_REVIEW_VERDICT.md",
    "SERVICE_MESH_REGRESSION_VERDICTS.md",
    "existing active parts",
    "does not grant governance authority",
    "python scripts/validate_repo.py",
)
EXPERIENCE_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Experience Part Contract Guard",
    "mechanics/experience/parts/protocol-integrity/README.md",
    "mechanics/experience/parts/certification-gate/README.md",
    "mechanics/experience/parts/adoption-federation/README.md",
    "mechanics/experience/parts/governance-runtime-boundary/README.md",
    "mechanics/experience/parts/office-release-train/README.md",
    "live runtime activation",
    "operator certification",
    "owner-local adoption",
    "governance authority",
    "memory canon",
    "routing authorship",
    "broad Experience success",
    "python scripts/validate_repo.py",
)


@dataclass(frozen=True)
class ExperienceRouteContext:
    require_tokens: Callable[..., str]
    provenance_tokens: Sequence[str]


def _require(
    context: ExperienceRouteContext,
    repo_root: Path,
    path_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    return context.require_tokens(
        repo_root=repo_root,
        path_name=path_name,
        tokens=tokens,
        issues=issues,
    )


def validate_experience_route_surfaces(
    repo_root: Path,
    *,
    context: ExperienceRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require(context, repo_root, EXPERIENCE_MECHANIC_README_NAME, EXPERIENCE_MECHANIC_REQUIRED_TOKENS, issues)
    _require(context, repo_root, EXPERIENCE_MECHANIC_AGENTS_NAME, EXPERIENCE_MECHANIC_AGENTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, EXPERIENCE_MECHANIC_PARTS_NAME, EXPERIENCE_MECHANIC_PARTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, EXPERIENCE_PROTOCOL_PART_README_NAME, EXPERIENCE_PROTOCOL_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, EXPERIENCE_CERTIFICATION_PART_README_NAME, EXPERIENCE_CERTIFICATION_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, EXPERIENCE_ADOPTION_PART_README_NAME, EXPERIENCE_ADOPTION_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, EXPERIENCE_GOVERNANCE_PART_README_NAME, EXPERIENCE_GOVERNANCE_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, EXPERIENCE_OFFICE_PART_README_NAME, EXPERIENCE_OFFICE_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, EXPERIENCE_MECHANIC_PROVENANCE_NAME, context.provenance_tokens, issues)
    _require(context, repo_root, EXPERIENCE_MECHANIC_DECISION_NAME, EXPERIENCE_MECHANIC_DECISION_REQUIRED_TOKENS, issues)
    _require(context, repo_root, EXPERIENCE_VERDICT_RESIDUE_DECISION_NAME, EXPERIENCE_VERDICT_RESIDUE_DECISION_REQUIRED_TOKENS, issues)
    _require(
        context,
        repo_root,
        EXPERIENCE_PART_CONTRACT_GUARD_DECISION_NAME,
        EXPERIENCE_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            EXPERIENCE_PART_CONTRACT_GUARD_DECISION_NAME,
            "Experience Part Contract Guard",
        ),
        issues,
    )
    return issues
