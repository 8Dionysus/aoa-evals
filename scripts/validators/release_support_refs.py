"""Release-support repo-qualified reference helpers."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

from validators.common import ValidationIssue

REPO_REF_PREFIX = "repo:"
MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def markdown_anchor(text: str) -> str:
    anchor = text.strip().lower()
    anchor = re.sub(r"[^\w\s-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor)
    anchor = re.sub(r"-+", "-", anchor)
    return anchor.strip("-")


@lru_cache(maxsize=None)
def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = MARKDOWN_HEADING.match(line)
        if not match:
            continue
        base = markdown_anchor(match.group(2))
        if not base:
            continue
        suffix = seen.get(base, 0)
        seen[base] = suffix + 1
        anchors.add(base if suffix == 0 else f"{base}-{suffix}")
    return anchors


def parse_repo_ref(
    raw_ref: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
    repo_ref_roots: Mapping[str, Path],
    strict_sibling_compat: bool,
) -> tuple[str, Path, str | None] | None:
    if not isinstance(raw_ref, str) or not raw_ref:
        issues.append(ValidationIssue(location, "reference must be a non-empty string"))
        return None
    if not raw_ref.startswith(REPO_REF_PREFIX):
        issues.append(ValidationIssue(location, "reference must start with 'repo:'"))
        return None

    payload = raw_ref[len(REPO_REF_PREFIX) :]
    if "/" not in payload:
        issues.append(ValidationIssue(location, "reference must include a repo name and repo-relative path"))
        return None

    repo_name, path_with_anchor = payload.split("/", 1)
    repo_root = repo_ref_roots.get(repo_name)
    if repo_root is None:
        issues.append(ValidationIssue(location, f"unknown repo in reference: '{repo_name}'"))
        return None

    path_text, _, anchor = path_with_anchor.partition("#")
    if not path_text:
        issues.append(ValidationIssue(location, "reference path must not be empty"))
        return None

    target = repo_root / path_text
    if repo_name != "aoa-evals" and not strict_sibling_compat:
        return repo_name, target, anchor or None
    if not repo_root.exists():
        issues.append(
            ValidationIssue(
                location,
                f"strict sibling compatibility requires available repo root for {repo_name}: {repo_root}",
            )
        )
        return None
    if not target.exists():
        issues.append(ValidationIssue(location, f"reference target does not exist: {repo_name}/{path_text}"))
        return None

    if anchor:
        if target.suffix.lower() != ".md":
            issues.append(ValidationIssue(location, f"markdown anchor refs must target a .md file: '{raw_ref}'"))
            return None
        if anchor not in markdown_anchors(target):
            issues.append(ValidationIssue(location, f"markdown anchor does not exist for ref '{raw_ref}'"))
            return None

    return repo_name, target, anchor or None


def repo_ref_roots_for_validation(
    repo_root: Path,
    repo_ref_roots: Mapping[str, Path] | None,
) -> Mapping[str, Path]:
    if repo_ref_roots is None:
        return {"aoa-evals": repo_root}
    return repo_ref_roots


__all__ = (
    "MARKDOWN_HEADING",
    "REPO_REF_PREFIX",
    "markdown_anchor",
    "markdown_anchors",
    "parse_repo_ref",
    "repo_ref_roots_for_validation",
)
