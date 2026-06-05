"""Root-visible legacy archive-detail leakage checks."""

from __future__ import annotations

import re
from pathlib import Path

from validators import mechanics as mechanics_validator
from validators import root_legacy_common as common
from validators import root_route_cards as root_route_cards_validator
from validators.common import ValidationIssue, read_text_or_issue


LEGACY_EXTERNAL_ARCHIVE_DETAIL_RE = re.compile(
    r"(?:mechanics/[a-z0-9-]+/)?legacy/(?:INDEX\.md|DISTILLATION_LOG\.md|raw(?:/|`|\)|\]|\s|$))"
    r"|raw/README\.md"
)
LEGACY_EXTERNAL_ARCHIVE_DETAIL_SURFACE_NAMES = (
    common.DESIGN_NAME,
    common.DESIGN_AGENTS_NAME,
    common.LEGACY_NAMING_NAME,
    common.PROOF_TOPOLOGY_NAME,
    common.MECHANICS_EVIDENCE_CLUSTERS_NAME,
    "mechanics/README.md",
    common.ROADMAP_NAME,
    "CHANGELOG.md",
)
LEGACY_EXTERNAL_ROUTE_MANAGEMENT_FORBIDDEN_WORDING = (
    "validator-backed retirement",
    "before physical movement, deletion, or retirement",
    "move any package-local legacy surface",
    "retirement or containment posture",
    "retired root",
    "aliases retired",
    "retire-after table",
)
LEGACY_EXTERNAL_ARCHIVE_ACCOUNTING_FORBIDDEN_WORDING = (
    "Inside the archive, every raw payload",
    "raw payload accounting now requires",
    "raw payload accounting now rejects",
    "raw-only archive route",
)
LEGACY_EXTERNAL_ARCHIVE_ACCOUNTING_SURFACE_NAMES = (
    common.DESIGN_NAME,
    common.DESIGN_AGENTS_NAME,
    common.LEGACY_NAMING_NAME,
    common.PROOF_TOPOLOGY_NAME,
    common.MECHANICS_EVIDENCE_CLUSTERS_NAME,
    "mechanics/README.md",
    common.ROADMAP_NAME,
    "CHANGELOG.md",
)
LEGACY_EXTERNAL_ROUTE_MANAGEMENT_SURFACE_NAMES = (
    common.LEGACY_NAMING_NAME,
    common.ROADMAP_NAME,
    common.DESIGN_AGENTS_NAME,
    "docs/decisions/AOA-EV-D-0009-legacy-naming-containment.md",
    common.LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
    common.LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
)


def validate_legacy_external_leakage_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    archive_detail_surface_paths: set[str] = set(LEGACY_EXTERNAL_ARCHIVE_DETAIL_SURFACE_NAMES)
    decisions_root = repo_root / "docs" / "decisions"
    if decisions_root.is_dir():
        archive_detail_surface_paths.update(
            path.relative_to(repo_root).as_posix()
            for path in sorted(decisions_root.glob("*.md"))
        )
    for path_name in sorted(archive_detail_surface_paths):
        surface_path = repo_root / path_name
        if not surface_path.exists():
            continue
        surface_text = read_text_or_issue(surface_path, issues, root=repo_root)
        if not surface_text:
            continue
        for match in LEGACY_EXTERNAL_ARCHIVE_DETAIL_RE.finditer(surface_text):
            issues.append(
                ValidationIssue(
                    path_name,
                    "legacy route wording must cross only through PROVENANCE.md; "
                    "external surfaces must not carry archive-internal detail "
                    f"`{match.group(0)}`",
                )
            )
    for path_name in LEGACY_EXTERNAL_ARCHIVE_ACCOUNTING_SURFACE_NAMES:
        surface_path = repo_root / path_name
        if not surface_path.exists():
            continue
        surface_text = read_text_or_issue(surface_path, issues, root=repo_root)
        if not surface_text:
            continue
        for stale_phrase in LEGACY_EXTERNAL_ARCHIVE_ACCOUNTING_FORBIDDEN_WORDING:
            if stale_phrase in surface_text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "external legacy boundary wording must not carry archive-local "
                        f"accounting detail: '{stale_phrase}'",
                    )
                )
    route_management_surface_paths: set[str] = set(
        LEGACY_EXTERNAL_ROUTE_MANAGEMENT_SURFACE_NAMES
    )
    for district_name, allowed_names in (
        root_route_cards_validator.ROOT_ROUTE_CARD_ONLY_DISTRICTS.items()
    ):
        for allowed_name in allowed_names:
            route_management_surface_paths.add(f"{district_name}/{allowed_name}")
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = repo_root / "mechanics" / parent_name
        if not parent_root.is_dir():
            continue
        for path in sorted(parent_root.rglob("*.md")):
            if "legacy" in path.relative_to(parent_root).parts:
                continue
            route_management_surface_paths.add(path.relative_to(repo_root).as_posix())

    for path_name in sorted(route_management_surface_paths):
        surface_path = repo_root / path_name
        if not surface_path.exists():
            continue
        surface_text = read_text_or_issue(surface_path, issues, root=repo_root)
        if not surface_text:
            continue
        for stale_phrase in LEGACY_EXTERNAL_ROUTE_MANAGEMENT_FORBIDDEN_WORDING:
            if stale_phrase in surface_text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "external legacy boundary wording must not present legacy as a "
                        f"movement, deletion, or retirement route: '{stale_phrase}'",
                    )
                )
    return issues
