"""Questbook route-card and mechanic route boundary contracts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators.common import ValidationIssue, read_text_or_issue, relative_location
from validators.questbook_route_paths import (
    AGON_QUEST_NOTE_PROVENANCE_DECISION_NAME,
    QUESTBOOK_DISPATCH_READER_PART_README_NAME,
    QUESTBOOK_MECHANIC_AGENTS_NAME,
    QUESTBOOK_MECHANIC_PARTS_NAME,
    QUESTBOOK_MECHANIC_PROVENANCE_NAME,
    QUESTBOOK_MECHANIC_README_NAME,
    QUESTBOOK_PART_OWNER_SPLIT_DECISION_NAME,
    QUESTBOOK_SOURCE_RECORD_PART_README_NAME,
    QUESTS_AGENTS_NAME,
    QUESTS_README_NAME,
    QUEST_LIFECYCLE_NAME,
)
from validators.questbook_route_tokens import (
    AGON_QUEST_NOTE_PROVENANCE_DECISION_REQUIRED_TOKENS,
    QUESTBOOK_DISPATCH_READER_PART_REQUIRED_TOKENS,
    QUESTBOOK_MECHANIC_AGENTS_REQUIRED_TOKENS,
    QUESTBOOK_MECHANIC_DECISION_REQUIRED_TOKENS,
    QUESTBOOK_MECHANIC_PARTS_REQUIRED_TOKENS,
    QUESTBOOK_MECHANIC_REQUIRED_TOKENS,
    QUESTBOOK_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS,
    QUESTBOOK_SOURCE_RECORD_PART_REQUIRED_TOKENS,
    QUESTS_AGENTS_REQUIRED_TOKENS,
    QUESTS_README_REQUIRED_TOKENS,
    QUEST_LIFECYCLE_DECISION_REQUIRED_TOKENS,
    QUEST_LIFECYCLE_REQUIRED_TOKENS,
)


@dataclass(frozen=True)
class QuestbookRouteContext:
    require_tokens: Callable[..., str]
    provenance_tokens: Sequence[str]


def _require(
    context: QuestbookRouteContext,
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


def validate_quest_route_surfaces(
    repo_root: Path,
    *,
    context: QuestbookRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require(context, repo_root, QUESTS_README_NAME, QUESTS_README_REQUIRED_TOKENS, issues)
    _require(context, repo_root, QUESTS_AGENTS_NAME, QUESTS_AGENTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, QUEST_LIFECYCLE_NAME, QUEST_LIFECYCLE_REQUIRED_TOKENS, issues)
    for path_name, stale_token in (
        (QUESTS_README_NAME, "It is not `QUESTBOOK.md`"),
        (QUESTS_README_NAME, "Quests are not eval bundles."),
        (QUEST_LIFECYCLE_NAME, "It is not `QUESTBOOK.md`"),
        (QUEST_LIFECYCLE_NAME, "does not create an eval result receipt"),
    ):
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if stale_token in text:
            issues.append(
                ValidationIssue(
                    path_name,
                    "quest route surfaces should use positive role routing instead of stale negative scaffold "
                    f"'{stale_token}'",
                )
            )
    _require(
        context,
        repo_root,
        "docs/decisions/AOA-EV-D-0004-questbook-topology.md",
        ("QUESTBOOK.md", "generated quest", "lane/state", "eval bundles"),
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/AOA-EV-D-0018-quest-lane-state-source-layout.md",
        (
            "quests/<lane>/<state>/",
            "generated quest readers",
            "legacy path vocabulary",
            "stale top-level quest source files",
        ),
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/AOA-EV-D-0021-quest-lifecycle-contract.md",
        QUEST_LIFECYCLE_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        AGON_QUEST_NOTE_PROVENANCE_DECISION_NAME,
        AGON_QUEST_NOTE_PROVENANCE_DECISION_REQUIRED_TOKENS,
        issues,
    )
    for stale_path in sorted((repo_root / "quests").glob("AOA-EV-Q-*.yaml")):
        issues.append(
            ValidationIssue(
                relative_location(stale_path, repo_root),
                "top-level quest source files must stay moved to quests/<lane>/<state>/",
            )
        )
    for stale_path in sorted((repo_root / "quests").glob("AOE-Q-AGON-*.md")):
        issues.append(
            ValidationIssue(
                relative_location(stale_path, repo_root),
                "top-level Agon quest notes must stay behind mechanics/agon/PROVENANCE.md",
            )
        )
    for markdown_path in sorted((repo_root / "quests").rglob("*.md")):
        relative_parts = markdown_path.relative_to(repo_root).parts
        if relative_parts in {
            ("quests", "README.md"),
            ("quests", "AGENTS.md"),
            ("quests", "LIFECYCLE.md"),
        }:
            continue
        issues.append(
            ValidationIssue(
                relative_location(markdown_path, repo_root),
                "markdown quest notes must not live under active quest lifecycle paths; "
                "route lineage through the owning mechanic PROVENANCE.md",
            )
        )
    return issues


def validate_questbook_route_surfaces(
    repo_root: Path,
    *,
    context: QuestbookRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require(context, repo_root, QUESTBOOK_MECHANIC_README_NAME, QUESTBOOK_MECHANIC_REQUIRED_TOKENS, issues)
    _require(context, repo_root, QUESTBOOK_MECHANIC_AGENTS_NAME, QUESTBOOK_MECHANIC_AGENTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, QUESTBOOK_MECHANIC_PARTS_NAME, QUESTBOOK_MECHANIC_PARTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, QUESTBOOK_SOURCE_RECORD_PART_README_NAME, QUESTBOOK_SOURCE_RECORD_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, QUESTBOOK_DISPATCH_READER_PART_README_NAME, QUESTBOOK_DISPATCH_READER_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, QUESTBOOK_MECHANIC_PROVENANCE_NAME, context.provenance_tokens, issues)
    _require(
        context,
        repo_root,
        "docs/decisions/AOA-EV-D-0006-questbook-mechanic-package.md",
        QUESTBOOK_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/AOA-EV-D-0021-quest-lifecycle-contract.md",
        QUEST_LIFECYCLE_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        QUESTBOOK_PART_OWNER_SPLIT_DECISION_NAME,
        QUESTBOOK_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            QUESTBOOK_PART_OWNER_SPLIT_DECISION_NAME,
            "Questbook Part Owner-split Contract",
        ),
        issues,
    )
    return issues


__all__ = (
    "QuestbookRouteContext",
    "validate_quest_route_surfaces",
    "validate_questbook_route_surfaces",
)
