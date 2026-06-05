"""Mechanic parent guidance-doc boundary guards."""

from __future__ import annotations

from pathlib import Path

from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanic_parent_common import (
    DECISION_RECORDS_README_NAME,
    MECHANICS_README_NAME,
    require_tokens,
)


MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0097-mechanic-parent-guidance-boundary.md"
)
MECHANIC_PARENT_GUIDANCE_BOUNDARY_COMMAND = (
    "python -m pytest -q tests/test_mechanic_parent_topology.py -k mechanic_parent_guidance_boundary"
)
MECHANIC_PARENT_ROOT_ALLOWED_FILES = frozenset(
    {
        "AGENTS.md",
        "DIRECTION.md",
        "PARTS.md",
        "PROVENANCE.md",
        "README.md",
    }
)
MECHANIC_PARENT_ROOT_ALLOWED_DIRS = frozenset({"legacy", "parts"})
MECHANIC_PARENT_GUIDANCE_DOCS = {
    "agon": frozenset(
        {
            "AGON_EVAL_OWNER_HANDOFFS.md",
            "AGON_EVAL_RECURRENCE_REVIEW_BOUNDARY.md",
        }
    ),
    "recurrence": frozenset({"RECURRENCE_PROOF_PROGRAM.md"}),
}
MECHANIC_PARENT_GUIDANCE_DOC_REQUIRED_TOKENS = (
    "## Role",
    "## Mechanic-wide Scope",
    "## Source Surfaces",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
)
MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_REQUIRED_TOKENS = (
    "Mechanic Parent Guidance Boundary",
    "`mechanics/<parent>/docs/`",
    "mechanic-wide guidance",
    "parent guidance content contract",
    "part-owned payload",
    "`## Source Surfaces`",
    "`## Stronger Owner Split`",
    "`## Stop-Lines`",
    "allowlisted",
    "unallowlisted parent-level docs",
    "Titan canary guides",
    MECHANIC_PARENT_GUIDANCE_BOUNDARY_COMMAND,
)


def validate_mechanic_parent_guidance_boundary(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = repo_root / "mechanics" / parent_name
        if not parent_root.is_dir():
            continue

        allowed_guidance_docs = MECHANIC_PARENT_GUIDANCE_DOCS.get(
            parent_name,
            frozenset(),
        )
        for child in sorted(parent_root.iterdir(), key=lambda item: item.name):
            child_relative = child.relative_to(repo_root).as_posix()
            if child.is_file():
                if child.name not in MECHANIC_PARENT_ROOT_ALLOWED_FILES:
                    issues.append(
                        ValidationIssue(
                            child_relative,
                            "unexpected mechanic parent-root file must move under an owning part payload directory",
                        )
                    )
                continue
            if not child.is_dir():
                issues.append(
                    ValidationIssue(
                        child_relative,
                        "unexpected mechanic parent-root entry must be a route file, parts/, legacy/, or explicit guidance docs/",
                    )
                )
                continue
            if child.name in MECHANIC_PARENT_ROOT_ALLOWED_DIRS:
                continue
            if child.name != "docs":
                issues.append(
                    ValidationIssue(
                        child_relative,
                        "unexpected mechanic parent-root directory must move under parts/<part>/ or be declared as parent guidance",
                    )
                )
                continue
            if not allowed_guidance_docs:
                issues.append(
                    ValidationIssue(
                        child_relative,
                        "parent-level docs/ is only for explicit mechanic-wide guidance; part-owned payload docs must live under parts/<part>/docs/",
                    )
                )
            entries = sorted(child.iterdir(), key=lambda item: item.name)
            if not entries:
                issues.append(
                    ValidationIssue(
                        child_relative,
                        "empty parent-level docs/ directory must not be kept as future payload space",
                    )
                )
                continue
            for entry in entries:
                entry_relative = entry.relative_to(repo_root).as_posix()
                if not entry.is_file():
                    issues.append(
                        ValidationIssue(
                            entry_relative,
                            "parent-level docs/ may contain only explicitly allowlisted mechanic-wide guidance files",
                        )
                    )
                    continue
                if entry.name not in allowed_guidance_docs:
                    issues.append(
                        ValidationIssue(
                            entry_relative,
                            "unallowlisted parent-level docs must move under the owning part payload route",
                        )
                    )
                    continue
                guidance_text = read_text_or_issue(entry, issues, root=repo_root)
                if guidance_text is None:
                    continue
                for token in MECHANIC_PARENT_GUIDANCE_DOC_REQUIRED_TOKENS:
                    if token not in guidance_text:
                        issues.append(
                            ValidationIssue(
                                entry_relative,
                                f"mechanic-wide guidance doc must expose parent guidance content contract token {token!r}",
                            )
                        )
            for doc_name in allowed_guidance_docs:
                if not (child / doc_name).is_file():
                    issues.append(
                        ValidationIssue(
                            f"mechanics/{parent_name}/docs/{doc_name}",
                            "allowlisted mechanic-wide guidance doc is missing",
                        )
                    )

    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME,
        tokens=MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME,
            "Mechanic Parent Guidance Boundary",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("parent-level `docs/`", "part-owned payload"),
        issues=issues,
    )
    return issues


__all__ = (
    "MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_NAME",
    "MECHANIC_PARENT_GUIDANCE_BOUNDARY_COMMAND",
    "MECHANIC_PARENT_ROOT_ALLOWED_FILES",
    "MECHANIC_PARENT_ROOT_ALLOWED_DIRS",
    "MECHANIC_PARENT_GUIDANCE_DOCS",
    "MECHANIC_PARENT_GUIDANCE_DOC_REQUIRED_TOKENS",
    "MECHANIC_PARENT_GUIDANCE_BOUNDARY_DECISION_REQUIRED_TOKENS",
    "validate_mechanic_parent_guidance_boundary",
)
