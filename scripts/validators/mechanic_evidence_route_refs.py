"""Active mechanic parent evidence route-ref ledger contracts."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanic_parent_registry import ACTIVE_MECHANIC_PARENT_NAMES
from validators.mechanics_common import (
    MECHANICS_EVIDENCE_CLUSTERS_NAME,
    MECHANICS_README_NAME,
    PROOF_TOPOLOGY_NAME,
    _markdown_heading_section,
    _markdown_table_rows,
    _require_tokens,
)


MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0101-mechanic-evidence-route-refs.md"
)
MECHANIC_EVIDENCE_ROUTE_REFS_COMMAND = (
    "python -m pytest -q tests/test_mechanic_evidence_ledger.py -k mechanic_evidence_route_refs"
)
MECHANIC_EVIDENCE_ROUTE_REFS_SECTION = "Active Parent Evidence Route Refs"
MECHANIC_EVIDENCE_ROUTE_REFS_REQUIRED_TOKENS = (
    MECHANIC_EVIDENCE_ROUTE_REFS_SECTION,
    "concrete local route refs",
    "repo-relative",
    "non-mechanics route ref",
    "living non-mechanics evidence",
    "rationale-only decision",
    "generic root validator",
)
MECHANIC_EVIDENCE_ROUTE_REFS_COLUMNS = (
    "Parent",
    "Route refs",
)
MECHANIC_EVIDENCE_ROUTE_REFS_MIN_COUNT = 3
MECHANIC_EVIDENCE_ROUTE_REFS_FORBIDDEN_GENERIC_REFS = frozenset(
    {
        "scripts/validate_repo.py",
        "tests/test_validate_repo.py",
    }
)
MECHANIC_EVIDENCE_ROUTE_REFS_RATIONALE_ONLY_PREFIXES = (
    "docs/decisions/",
)
MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_REQUIRED_TOKENS = (
    "Mechanic Evidence Route Refs",
    MECHANIC_EVIDENCE_ROUTE_REFS_SECTION,
    "concrete local route refs",
    "repo-relative",
    "non-mechanics route ref",
    "living non-mechanics evidence",
    "rationale-only decision",
    "generic root validator",
    "cross-root evidence",
    MECHANIC_EVIDENCE_ROUTE_REFS_COMMAND,
)

SOURCE_SURFACE_CODE_REF_RE = re.compile(r"`([^`\n]+)`")
SOURCE_SURFACE_FILE_REF_RE = re.compile(r"\.[A-Za-z0-9][A-Za-z0-9_.-]*$")


def _source_surface_ref_is_path_like(ref: str) -> bool:
    return (
        ref.startswith(("repo:", ".", "/"))
        or "/" in ref
        or "*" in ref
        or "?" in ref
        or "[" in ref
        or SOURCE_SURFACE_FILE_REF_RE.search(ref) is not None
    )


def _source_surface_ref_resolution_issue(repo_root: Path, ref: str) -> str | None:
    if ref.startswith("repo:"):
        return None
    if ref.startswith(("http://", "https://")):
        return None
    if ref.startswith("/"):
        return "source surface ref must be repo-relative or repo-qualified, not absolute"
    if ".." in PurePosixPath(ref).parts:
        return "source surface ref must not traverse outside the repository"
    if "<" in ref or ">" in ref:
        return None

    if any(char in ref for char in "*?["):
        if any(repo_root.glob(ref)):
            return None
        return "stale source surface ref must resolve as a repo-relative glob"

    if (repo_root / ref.rstrip("/")).exists():
        return None
    return "stale source surface ref must resolve as a repo-relative path"


def validate_mechanic_evidence_route_refs(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    text = read_text_or_issue(repo_root / MECHANICS_EVIDENCE_CLUSTERS_NAME, issues, root=repo_root)
    if not text:
        return issues
    route_refs_section = _markdown_heading_section(text, MECHANIC_EVIDENCE_ROUTE_REFS_SECTION)
    if not route_refs_section:
        issues.append(
            ValidationIssue(
                MECHANICS_EVIDENCE_CLUSTERS_NAME,
                f"mechanics evidence cluster map must contain section {MECHANIC_EVIDENCE_ROUTE_REFS_SECTION!r}",
            )
        )

    for token in MECHANIC_EVIDENCE_ROUTE_REFS_REQUIRED_TOKENS:
        if token not in route_refs_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"mechanics evidence route refs ledger must mention {token!r}",
                )
            )

    route_ref_rows: dict[str, list[str]] = {}
    for cells in _markdown_table_rows(route_refs_section):
        parent_cell = cells[0] if cells else ""
        parent_name = parent_cell.strip("`")
        if parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
            if parent_name in route_ref_rows:
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"active parent `{parent_name}` must appear only once in the evidence route refs ledger",
                    )
                )
            route_ref_rows[parent_name] = cells
            if len(cells) != len(MECHANIC_EVIDENCE_ROUTE_REFS_COLUMNS):
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"evidence route refs row for `{parent_name}` must have {len(MECHANIC_EVIDENCE_ROUTE_REFS_COLUMNS)} columns",
                    )
                )
                continue
            route_refs = [
                match.group(1).strip()
                for match in SOURCE_SURFACE_CODE_REF_RE.finditer(cells[1])
                if _source_surface_ref_is_path_like(match.group(1).strip())
            ]
            route_refs = list(dict.fromkeys(route_refs))
            if len(route_refs) < MECHANIC_EVIDENCE_ROUTE_REFS_MIN_COUNT:
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"evidence route refs row for `{parent_name}` must name at least {MECHANIC_EVIDENCE_ROUTE_REFS_MIN_COUNT} path-like route refs",
                    )
                )
            parent_prefix = f"mechanics/{parent_name}/"
            if not any(ref.startswith(parent_prefix) for ref in route_refs):
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"evidence route refs row for `{parent_name}` must include an active parent route under `{parent_prefix}`",
                    )
                )
            if not any(not ref.startswith("mechanics/") for ref in route_refs):
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"evidence route refs row for `{parent_name}` must include at least one non-mechanics route ref",
                    )
                )
            living_non_mechanics_refs = [
                ref
                for ref in route_refs
                if not ref.startswith("mechanics/")
                and ref not in MECHANIC_EVIDENCE_ROUTE_REFS_FORBIDDEN_GENERIC_REFS
                and not any(ref.startswith(prefix) for prefix in MECHANIC_EVIDENCE_ROUTE_REFS_RATIONALE_ONLY_PREFIXES)
            ]
            if not living_non_mechanics_refs:
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"evidence route refs row for `{parent_name}` must include living non-mechanics evidence; rationale-only decision refs are not enough",
                    )
                )
            for ref in route_refs:
                if ref in MECHANIC_EVIDENCE_ROUTE_REFS_FORBIDDEN_GENERIC_REFS:
                    issues.append(
                        ValidationIssue(
                            MECHANICS_EVIDENCE_CLUSTERS_NAME,
                            f"evidence route refs row for `{parent_name}` must not use generic root validator route `{ref}` as parent evidence",
                        )
                    )
                if ref.startswith("repo:") or "<" in ref or ">" in ref:
                    issues.append(
                        ValidationIssue(
                            MECHANICS_EVIDENCE_CLUSTERS_NAME,
                            f"evidence route refs row for `{parent_name}` must use concrete local repo-relative route refs, not `{ref}`",
                        )
                    )
                    continue
                ref_issue = _source_surface_ref_resolution_issue(repo_root, ref)
                if ref_issue is not None:
                    issues.append(
                        ValidationIssue(
                            MECHANICS_EVIDENCE_CLUSTERS_NAME,
                            f"evidence route refs row for `{parent_name}` has stale route ref: {ref_issue}: `{ref}`",
                        )
                    )

    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
        if parent_name not in route_ref_rows:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"active parent `{parent_name}` must appear in the evidence route refs ledger",
                )
            )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME,
        tokens=MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=(
            MECHANIC_EVIDENCE_ROUTE_REFS_SECTION,
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=(
            MECHANIC_EVIDENCE_ROUTE_REFS_SECTION,
        ),
        issues=issues,
    )
    return issues


__all__ = (
    "MECHANIC_EVIDENCE_ROUTE_REFS_COLUMNS",
    "MECHANIC_EVIDENCE_ROUTE_REFS_COMMAND",
    "MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME",
    "MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_REQUIRED_TOKENS",
    "MECHANIC_EVIDENCE_ROUTE_REFS_FORBIDDEN_GENERIC_REFS",
    "MECHANIC_EVIDENCE_ROUTE_REFS_MIN_COUNT",
    "MECHANIC_EVIDENCE_ROUTE_REFS_RATIONALE_ONLY_PREFIXES",
    "MECHANIC_EVIDENCE_ROUTE_REFS_REQUIRED_TOKENS",
    "MECHANIC_EVIDENCE_ROUTE_REFS_SECTION",
    "validate_mechanic_evidence_route_refs",
)
