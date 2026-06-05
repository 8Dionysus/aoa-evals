"""Boundary-bridge repo-validation workflow-pin hygiene."""

from __future__ import annotations

from pathlib import Path

from validators.boundary_bridge_common import (
    REPO_VALIDATION_AOA_MEMO_PIN_DECISION_NAME,
    REPO_VALIDATION_AOA_MEMO_PIN_DECISION_REQUIRED_TOKENS,
    REPO_VALIDATION_WORKFLOW_NAME,
    ValidationIssue,
    require_tokens,
)


def validate_repo_validation_workflow_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    require_tokens(
        repo_root=repo_root,
        path_name=REPO_VALIDATION_AOA_MEMO_PIN_DECISION_NAME,
        tokens=REPO_VALIDATION_AOA_MEMO_PIN_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    workflow_path = repo_root / REPO_VALIDATION_WORKFLOW_NAME
    try:
        workflow_text = workflow_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(REPO_VALIDATION_WORKFLOW_NAME, "file is missing"))
        return issues

    if "Run release audit" not in workflow_text or "python scripts/release_check.py" not in workflow_text:
        issues.append(
            ValidationIssue(
                REPO_VALIDATION_WORKFLOW_NAME,
                "repo validation workflow must run scripts/release_check.py",
            )
        )

    forbidden_tokens = (
        ".deps/",
        "AOA_TECHNIQUES_ROOT:",
        "AOA_SKILLS_ROOT:",
        "AOA_AGENTS_ROOT:",
        "AOA_PLAYBOOKS_ROOT:",
        "AOA_MEMO_ROOT:",
        "AOA_ROUTING_ROOT:",
        "AOA_KAG_ROOT:",
        "AOA_SDK_ROOT:",
        "AOA_STATS_ROOT:",
        "ABYSS_STACK_ROOT:",
        "repository: 8Dionysus/aoa-techniques",
        "repository: 8Dionysus/aoa-skills",
        "repository: 8Dionysus/aoa-agents",
        "repository: 8Dionysus/aoa-playbooks",
        "repository: 8Dionysus/aoa-memo",
        "repository: 8Dionysus/aoa-routing",
        "repository: 8Dionysus/aoa-kag",
        "repository: 8Dionysus/aoa-sdk",
        "repository: 8Dionysus/aoa-stats",
        "repository: 8Dionysus/abyss-stack",
    )
    for token in forbidden_tokens:
        if token in workflow_text:
            issues.append(
                ValidationIssue(
                    REPO_VALIDATION_WORKFLOW_NAME,
                    "repo validation workflow must not checkout or pin sibling repositories",
                )
            )
            break
    return issues


__all__ = ("validate_repo_validation_workflow_surface",)
