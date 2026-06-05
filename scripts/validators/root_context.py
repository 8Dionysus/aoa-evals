"""Root validation context for sibling refs and route-token lookup."""

from __future__ import annotations

import os
import re
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any, Sequence

from validators.common import ValidationIssue
from validators.root_route_tokens import (
    DECISION_RECORDS_README_NAME,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_NAME,
    ROUTE_RESIDUE_GUARDS_NAME,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def repo_root_from_env(env_name: str, default: Path) -> Path:
    override = os.environ.get(env_name)
    if not override:
        return default
    return Path(override).expanduser().resolve()


def is_abyss_stack_source_root(path: Path) -> bool:
    return (
        path.exists()
        and (path / "README.md").is_file()
        and (
            path
            / "mechanics"
            / "governed-execution"
            / "parts"
            / "return-policy"
            / "schemas"
            / "runtime-return-event.schema.json"
        ).is_file()
        and (path / "scripts" / "validate_stack.py").is_file()
    )

def resolve_abyss_stack_root(default: Path) -> Path:
    override = os.environ.get("ABYSS_STACK_ROOT")
    if override:
        return Path(override).expanduser().resolve()

    default_root = default.expanduser().resolve()
    home_src_root = (Path.home() / "src" / "abyss-stack").resolve()

    for candidate in (default_root, home_src_root):
        if is_abyss_stack_source_root(candidate):
            return candidate
    return default_root


AOA_TECHNIQUES_ROOT = repo_root_from_env(
    "AOA_TECHNIQUES_ROOT", REPO_ROOT.parent / "aoa-techniques"
)
AOA_SKILLS_ROOT = repo_root_from_env("AOA_SKILLS_ROOT", REPO_ROOT.parent / "aoa-skills")
AOA_AGENTS_ROOT = repo_root_from_env("AOA_AGENTS_ROOT", REPO_ROOT.parent / "aoa-agents")
AOA_PLAYBOOKS_ROOT = repo_root_from_env(
    "AOA_PLAYBOOKS_ROOT", REPO_ROOT.parent / "aoa-playbooks"
)
AOA_MEMO_ROOT = repo_root_from_env("AOA_MEMO_ROOT", REPO_ROOT.parent / "aoa-memo")
AOA_ROUTING_ROOT = repo_root_from_env("AOA_ROUTING_ROOT", REPO_ROOT.parent / "aoa-routing")
AOA_KAG_ROOT = repo_root_from_env("AOA_KAG_ROOT", REPO_ROOT.parent / "aoa-kag")
AOA_SDK_ROOT = repo_root_from_env("AOA_SDK_ROOT", REPO_ROOT.parent / "aoa-sdk")
AOA_STATS_ROOT = repo_root_from_env("AOA_STATS_ROOT", REPO_ROOT.parent / "aoa-stats")
AGENTS_OF_ABYSS_ROOT = repo_root_from_env(
    "AGENTS_OF_ABYSS_ROOT", REPO_ROOT.parent / "Agents-of-Abyss"
)
ABYSS_STACK_ROOT = resolve_abyss_stack_root(REPO_ROOT.parent / "abyss-stack")

LEGACY_NAMING_NAME = "docs/architecture/LEGACY_NAMING.md"

REPO_REF_PREFIX = "repo:"
STRICT_SIBLING_COMPAT_ENV = "AOA_EVALS_STRICT_SIBLING_COMPAT"


def visible_roots(repo_root: Path = REPO_ROOT) -> tuple[Path, ...]:
    return (
        repo_root,
        AOA_TECHNIQUES_ROOT,
        AOA_SKILLS_ROOT,
        AOA_AGENTS_ROOT,
        AOA_PLAYBOOKS_ROOT,
        AOA_MEMO_ROOT,
        AOA_ROUTING_ROOT,
        AOA_KAG_ROOT,
        AOA_SDK_ROOT,
        AOA_STATS_ROOT,
        ABYSS_STACK_ROOT,
    )


def repo_ref_roots(repo_root: Path = REPO_ROOT) -> dict[str, Path]:
    return {
        "aoa-evals": repo_root,
        "aoa-techniques": AOA_TECHNIQUES_ROOT,
        "aoa-skills": AOA_SKILLS_ROOT,
        "aoa-agents": AOA_AGENTS_ROOT,
        "aoa-playbooks": AOA_PLAYBOOKS_ROOT,
        "aoa-memo": AOA_MEMO_ROOT,
        "aoa-routing": AOA_ROUTING_ROOT,
        "aoa-kag": AOA_KAG_ROOT,
        "aoa-sdk": AOA_SDK_ROOT,
        "aoa-stats": AOA_STATS_ROOT,
        "abyss-stack": ABYSS_STACK_ROOT,
    }


VISIBLE_ROOTS = visible_roots()
REPO_REF_ROOTS = repo_ref_roots()


def refresh_roots(repo_root: Path = REPO_ROOT) -> None:
    global VISIBLE_ROOTS, REPO_REF_ROOTS
    VISIBLE_ROOTS = visible_roots(repo_root)
    REPO_REF_ROOTS = repo_ref_roots(repo_root)


def strict_sibling_compat_checks_enabled() -> bool:
    return os.environ.get(STRICT_SIBLING_COMPAT_ENV, "").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")


def display_location(path: Path) -> str:
    for root in VISIBLE_ROOTS:
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            continue
    return path.as_posix()


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
) -> tuple[str, Path, str | None] | None:
    if not isinstance(raw_ref, str) or not raw_ref:
        issues.append(ValidationIssue(location, "reference must be a non-empty string"))
        return None
    if not raw_ref.startswith(REPO_REF_PREFIX):
        issues.append(ValidationIssue(location, "reference must start with 'repo:'"))
        return None

    payload = raw_ref[len(REPO_REF_PREFIX) :]
    if "/" not in payload:
        issues.append(
            ValidationIssue(location, "reference must include a repo name and repo-relative path")
        )
        return None

    repo_name, path_with_anchor = payload.split("/", 1)
    repo_root = REPO_REF_ROOTS.get(repo_name)
    if repo_root is None:
        issues.append(ValidationIssue(location, f"unknown repo in reference: '{repo_name}'"))
        return None

    path_text, _, anchor = path_with_anchor.partition("#")
    if not path_text:
        issues.append(ValidationIssue(location, "reference path must not be empty"))
        return None

    target = repo_root / path_text
    if repo_name != "aoa-evals" and not strict_sibling_compat_checks_enabled():
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
        issues.append(
            ValidationIssue(
                location,
                f"reference target does not exist: {repo_name}/{path_text}",
            )
        )
        return None

    if anchor:
        if target.suffix.lower() != ".md":
            issues.append(
                ValidationIssue(location, f"markdown anchor refs must target a .md file: '{raw_ref}'")
            )
            return None
        if anchor not in markdown_anchors(target):
            issues.append(
                ValidationIssue(location, f"markdown anchor does not exist for ref '{raw_ref}'")
            )
            return None

    return repo_name, target, anchor or None


def parse_named_surface_ref(
    raw_ref: Any,
    *,
    prefix_name: str,
    repo_root: Path,
    location: str,
    issues: list[ValidationIssue],
) -> tuple[Path, str | None] | None:
    if not isinstance(raw_ref, str) or not raw_ref:
        issues.append(ValidationIssue(location, "reference must be a non-empty string"))
        return None

    prefix = f"{prefix_name}:"
    if not raw_ref.startswith(prefix):
        issues.append(ValidationIssue(location, f"reference must start with '{prefix}'"))
        return None

    path_text, _, anchor = raw_ref[len(prefix) :].partition("#")
    if not path_text:
        issues.append(ValidationIssue(location, "reference path must not be empty"))
        return None

    target = repo_root / path_text
    if not repo_root.exists():
        return target, anchor or None
    if not target.exists():
        issues.append(
            ValidationIssue(
                location,
                f"reference target does not exist: {prefix_name}/{path_text}",
            )
        )
        return None
    if anchor:
        if target.suffix.lower() != ".md":
            issues.append(
                ValidationIssue(location, f"markdown anchor refs must target a .md file: '{raw_ref}'")
            )
            return None
        if anchor not in markdown_anchors(target):
            issues.append(
                ValidationIssue(
                    location,
                    f"anchor '{anchor}' was not found in {prefix_name}/{path_text}",
                )
            )
            return None

    return target, anchor or None


def _abyss_stack_ref_boundary_message(allowed_roots: Sequence[str]) -> str:
    if tuple(allowed_roots) == ("Logs",):
        return "reference must stay inside 'repo:abyss-stack/Logs/'"
    if len(allowed_roots) == 1:
        return f"reference must stay inside 'repo:abyss-stack/{allowed_roots[0]}/'"
    allowed_text = " or ".join(f"'repo:abyss-stack/{root}/'" for root in allowed_roots)
    return f"reference must stay inside {allowed_text}"


def validate_abyss_stack_ref(
    raw_ref: Any,
    *,
    allowed_roots: Sequence[str] = ("Logs",),
    location: str,
    issues: list[ValidationIssue],
) -> PurePosixPath | None:
    boundary_message = _abyss_stack_ref_boundary_message(allowed_roots)
    if not isinstance(raw_ref, str) or not raw_ref:
        issues.append(ValidationIssue(location, "reference must be a non-empty string"))
        return None
    if "#" in raw_ref:
        issues.append(ValidationIssue(location, "operational evidence refs must not include markdown anchors"))
        return None
    if "\\" in raw_ref:
        issues.append(ValidationIssue(location, "reference must use forward slashes"))
        return None
    if not raw_ref.startswith("repo:abyss-stack/"):
        issues.append(ValidationIssue(location, boundary_message))
        return None

    path_text = raw_ref[len("repo:abyss-stack/") :]
    if not path_text:
        issues.append(ValidationIssue(location, "reference path must not be empty"))
        return None

    ref_path = PurePosixPath(path_text)
    if ref_path.is_absolute():
        issues.append(ValidationIssue(location, "reference path must be repo-relative"))
        return None
    if any(part in {"", ".", ".."} for part in ref_path.parts):
        issues.append(ValidationIssue(location, "reference path must not contain empty, '.' or '..' segments"))
        return None
    if len(ref_path.parts) < 2 or ref_path.parts[0] not in set(allowed_roots):
        issues.append(ValidationIssue(location, boundary_message))
        return None

    return ref_path


def validate_abyss_stack_logs_ref(
    raw_ref: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> PurePosixPath | None:
    return validate_abyss_stack_ref(
        raw_ref,
        allowed_roots=("Logs",),
        location=location,
        issues=issues,
    )
