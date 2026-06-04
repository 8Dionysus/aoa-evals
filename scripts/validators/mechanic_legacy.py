"""Mechanic legacy archive and provenance bridge guards."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Sequence

from validators import docs_decisions
from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue


DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
MECHANICS_README_NAME = "mechanics/README.md"
MECHANICS_EVIDENCE_CLUSTERS_NAME = "mechanics/EVIDENCE_CLUSTERS.md"
PROOF_TOPOLOGY_NAME = "docs/architecture/PROOF_TOPOLOGY.md"
ROUTE_RESIDUE_GUARDS_NAME = "docs/architecture/ROUTE_RESIDUE_GUARDS.md"
LEGACY_NAMING_NAME = "docs/architecture/LEGACY_NAMING.md"
ROADMAP_NAME = "ROADMAP.md"
DESIGN_NAME = "DESIGN.md"
CHANGELOG_NAME = "CHANGELOG.md"

ACTIVE_LEGACY_PARENT_WORDING_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0092-active-legacy-parent-wording-boundary.md"
)
ACTIVE_LEGACY_PARENT_WORDING_COMMAND = (
    "python -m pytest -q tests/test_mechanic_legacy_archive_routes.py -k active_legacy_parent_wording"
)
ACTIVE_LEGACY_PARENT_WORDING_DECISION_REQUIRED_TOKENS = (
    "Active Legacy Parent Wording Boundary",
    "legacy parent form",
    "active route wording",
    "`runtime-evidence`",
    "evidence class",
    "not the parent mechanic",
    "schema filename",
    ACTIVE_LEGACY_PARENT_WORDING_COMMAND,
)

MECHANIC_PROVENANCE_FILES = tuple(
    f"mechanics/{parent_name}/PROVENANCE.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_LEGACY_README_FILES = tuple(
    f"mechanics/{parent_name}/legacy/README.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_LEGACY_INDEX_FILES = tuple(
    f"mechanics/{parent_name}/legacy/INDEX.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_LEGACY_DISTILLATION_LOG_FILES = tuple(
    f"mechanics/{parent_name}/legacy/DISTILLATION_LOG.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_LEGACY_RAW_README_FILES = tuple(
    f"mechanics/{parent_name}/legacy/raw/README.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_LEGACY_SKELETON_FILES = (
    MECHANIC_PROVENANCE_FILES
    + MECHANIC_LEGACY_README_FILES
    + MECHANIC_LEGACY_INDEX_FILES
    + MECHANIC_LEGACY_DISTILLATION_LOG_FILES
    + MECHANIC_LEGACY_RAW_README_FILES
)
MECHANIC_LEGACY_ARCHIVE_ROUTE_FILES = (
    MECHANIC_LEGACY_README_FILES
    + MECHANIC_LEGACY_INDEX_FILES
    + MECHANIC_LEGACY_DISTILLATION_LOG_FILES
    + MECHANIC_LEGACY_RAW_README_FILES
)

MECHANIC_LEGACY_SKELETON_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0071-mechanic-legacy-skeleton-contract.md"
)
MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0089-mechanic-legacy-single-bridge.md"
)
MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND = (
    "python -m pytest -q tests/test_mechanic_legacy_bridge.py -k mechanic_legacy_single_bridge"
)
MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0090-mechanic-provenance-bridge-posture.md"
)
MECHANIC_PROVENANCE_BRIDGE_POSTURE_COMMAND = (
    "python -m pytest -q tests/test_mechanic_legacy_bridge.py -k mechanic_provenance_bridge_posture"
)
MECHANIC_PROVENANCE_ENTRY_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0075-mechanic-provenance-entry-contract.md"
)

MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_REQUIRED_TOKENS = (
    "Mechanic Legacy Single Bridge",
    "`PROVENANCE.md`",
    "single controlled bridge",
    "active mechanic surfaces",
    "legacy archive",
    "active surface",
    "direct archive-internal references",
    "must not carry archive details",
    "JSON",
    "YAML",
    MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND,
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
MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_REQUIRED_TOKENS = (
    "Mechanic Provenance Bridge Posture",
    "Current Applicability",
    "active-to-archive bridge",
    "Review Log",
    "Use active surfaces first:",
    "`DIRECTION.md`",
    "legacy archive",
    "legacy/README.md",
    "owns its own details",
    MECHANIC_PROVENANCE_BRIDGE_POSTURE_COMMAND,
)
MECHANIC_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "git history",
    "INDEX.md",
)
MECHANIC_LEGACY_README_REQUIRED_TOKENS = (
    "../PROVENANCE.md",
    "INDEX.md",
    "DISTILLATION_LOG.md",
    "raw/README.md",
    "archive-local route",
    "current active route",
)
MECHANIC_LEGACY_RAW_PAYLOAD_DECISION_REQUIRED_TOKENS = (
    "raw payload",
    "archive-local index or accounting log",
    "forgotten residue",
    "current active route",
    "active part route",
    "raw-only archive route",
)
MECHANIC_LEGACY_SKELETON_DECISION_REQUIRED_TOKENS = (
    "Mechanic Legacy Archive Boundary",
    "`PROVENANCE.md`",
    "`legacy/README.md`",
    "archive-local route",
    "archive-local index",
    "accounting log",
    "`../PROVENANCE.md`",
    "Current Applicability",
    "Review Log",
    "current active route",
    "unindexed raw payloads",
    "current-route expectations",
    "validation through the nearest legacy `AGENTS.md`",
    "python -m pytest -q tests/test_mechanic_parent_topology.py -k mechanic_legacy_skeleton",
    "python -m pytest -q tests/test_mechanic_legacy_archive_routes.py -k mechanic_legacy_raw_payload",
)
MECHANIC_PROVENANCE_ENTRY_REQUIRED_TOKENS = (
    "active",
    "legacy/README.md",
    "legacy archive owns",
    "archive details",
)
MECHANIC_PROVENANCE_ENTRY_DECISION_REQUIRED_TOKENS = (
    "Mechanic Provenance Entry Contract",
    "`PROVENANCE.md`",
    "`legacy/README.md`",
    "active route first",
    "not active topology",
    "archive details",
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_provenance_entry",
)
ROADMAP_LEGACY_BRIDGE_DIRECTION_TOKENS = (
    "Legacy bridge",
    "single controlled bridge posture",
    "active mechanic surfaces",
    "runtime evidence limits",
)

MECHANIC_LEGACY_ARCHIVE_COMMAND_RE = re.compile(
    r"```(?:bash|sh)\b|`python (?:scripts/|-m pytest)|^python (?:scripts/|-m pytest)",
    re.MULTILINE,
)
MECHANIC_LEGACY_ARCHIVE_STALE_ROUTE_PHRASES = (
    "Do not create new",
    "Do not begin new",
    "Do not recreate",
    "Do not treat",
    "Do not use",
    "It is not",
    "does not own",
    "Legacy only explains",
    "legacy only explains",
    "not the active",
    "not an active",
    "not active",
    "not a changelog",
    " not ",
)
MECHANIC_LEGACY_ACTIVE_DIRECT_REF_RE = re.compile(
    r"(?:mechanics/[a-z0-9-]+/)?legacy/(?:README\.md|INDEX\.md|DISTILLATION_LOG\.md|raw(?:/|`|\)|\]|\s|$))"
    r"|raw/README\.md"
)
MECHANIC_LEGACY_ACTIVE_SURFACE_SUFFIXES = (".md", ".json", ".yaml", ".yml", ".py")
MECHANIC_PROVENANCE_ARCHIVE_DETAIL_RE = re.compile(
    r"legacy/(?:INDEX\.md|DISTILLATION_LOG\.md|raw(?:/|`|\)|\]|\s|$))"
    r"|raw/README\.md"
)
ACTIVE_LEGACY_PARENT_WORDING_FORBIDDEN: dict[str, tuple[str, ...]] = {
    "docs/operations/RELEASING.md": (
        "runtime-evidence example refs",
    ),
    "docs/architecture/PROOF_TOPOLOGY.md": (
        "audit runtime-evidence packets",
    ),
    "mechanics/boundary-bridge/README.md": (
        "runtime-evidence schema refs",
    ),
    "mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md": (
        "runtime-evidence schema",
    ),
    "mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json": (
        "runtime-evidence schema refs",
    ),
    "mechanics/recurrence/parts/portable-proof-beacons/manifests/recurrence/hooks/component.evals.portable-proof-beacons.hooks.json": (
        "runtime-evidence bridge",
    ),
    "mechanics/audit/parts/README.md": (
        "# Runtime Evidence Parts",
        "`runtime-evidence` mechanic",
    ),
    "mechanics/titan/README.md": (
        "This package routes Titan canary work",
    ),
    "mechanics/titan/parts/README.md": (
        "# Titan Canaries Parts",
        "Titan-canary-owned",
    ),
    "reports/README.md": (
        "Proof-release reports",
    ),
}


def _require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return text

    companion_texts: list[str] = []
    if path_name == DECISION_RECORDS_README_NAME:
        for relative_path in docs_decisions.GENERATED_INDEX_PATHS:
            index_path = repo_root / relative_path
            if index_path.is_file():
                companion_texts.append(index_path.read_text(encoding="utf-8"))
    if path_name == PROOF_TOPOLOGY_NAME:
        route_guard_path = repo_root / ROUTE_RESIDUE_GUARDS_NAME
        if route_guard_path.is_file():
            companion_texts.append(route_guard_path.read_text(encoding="utf-8"))

    search_text = "\n\n".join((text, *companion_texts)) if companion_texts else text
    for token in tokens:
        if token not in search_text:
            issues.append(ValidationIssue(path_name, f"missing required token: {token!r}"))
    return text


def validate_mechanic_legacy_single_bridge_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = repo_root / "mechanics" / parent_name
        if not parent_root.is_dir():
            continue

        for path in sorted(parent_root.rglob("*")):
            if not path.is_file() or path.suffix not in MECHANIC_LEGACY_ACTIVE_SURFACE_SUFFIXES:
                continue
            relative_parts = path.relative_to(parent_root).parts
            if "legacy" in relative_parts:
                continue
            text = read_text_or_issue(path, issues, root=repo_root)
            if text is None:
                continue
            if path.name == "PROVENANCE.md":
                for match in MECHANIC_PROVENANCE_ARCHIVE_DETAIL_RE.finditer(text):
                    issues.append(
                        ValidationIssue(
                            path.relative_to(repo_root).as_posix(),
                            f"PROVENANCE.md must bridge to legacy/README.md without carrying archive detail `{match.group(0)}`",
                        )
                    )
                continue
            for match in MECHANIC_LEGACY_ACTIVE_DIRECT_REF_RE.finditer(text):
                issues.append(
                    ValidationIssue(
                        path.relative_to(repo_root).as_posix(),
                        f"active mechanic surface must route legacy archive details through PROVENANCE.md, not direct `{match.group(0)}`",
                    )
                )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME,
        tokens=MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME,
            "Mechanic Legacy Single Bridge",
        ),
        issues=issues,
    )
    for path_name in (MECHANICS_README_NAME, PROOF_TOPOLOGY_NAME, LEGACY_NAMING_NAME):
        _require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=("single controlled bridge", "active mechanic surfaces", "legacy archive"),
            issues=issues,
        )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_LEGACY_BRIDGE_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


def validate_mechanic_legacy_archive_route_language(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name in MECHANIC_LEGACY_ARCHIVE_ROUTE_FILES:
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if text is None:
            continue
        command_match = MECHANIC_LEGACY_ARCHIVE_COMMAND_RE.search(text)
        if command_match is not None:
            issues.append(
                ValidationIssue(
                    path_name,
                    "legacy archive route files must point validation to AGENTS.md instead of carrying executable command blocks",
                )
            )
        for phrase in MECHANIC_LEGACY_ARCHIVE_STALE_ROUTE_PHRASES:
            if phrase in text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        f"legacy archive route files must name current active route expectations instead of stale negative scaffold `{phrase}`",
                    )
                )

    return issues


def validate_mechanic_legacy_raw_payload_accounting(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        legacy_root = repo_root / "mechanics" / parent_name / "legacy"
        raw_root = legacy_root / "raw"
        if not raw_root.is_dir():
            continue

        index_path = legacy_root / "INDEX.md"
        log_path = legacy_root / "DISTILLATION_LOG.md"
        if not index_path.is_file() or not log_path.is_file():
            continue

        accounting_text = (
            index_path.read_text(encoding="utf-8")
            + "\n"
            + log_path.read_text(encoding="utf-8")
        )
        index_text = index_path.read_text(encoding="utf-8")

        for path in sorted(raw_root.rglob("*")):
            if not path.is_file() or path.name == "README.md":
                continue
            legacy_relative = path.relative_to(legacy_root).as_posix()
            if legacy_relative not in accounting_text and path.name not in accounting_text:
                issues.append(
                    ValidationIssue(
                        path.relative_to(repo_root).as_posix(),
                        "legacy raw payload must be referenced by the archive-local index or accounting log",
                    )
                )
                continue

            raw_index_lines = [
                line
                for line in index_text.splitlines()
                if legacy_relative in line or path.name in line
            ]
            if not raw_index_lines:
                issues.append(
                    ValidationIssue(
                        path.relative_to(repo_root).as_posix(),
                        "legacy raw payload must have an archive-local INDEX.md row that maps it to a current active route",
                    )
                )
                continue

            active_part_route = f"mechanics/{parent_name}/parts/"
            package_wide_route = (
                f"mechanics/{parent_name}/DIRECTION.md",
                f"mechanics/{parent_name}/PARTS.md",
            )
            has_active_route = any(
                "/legacy/" not in line
                and (
                    active_part_route in line
                    or all(route in line for route in package_wide_route)
                )
                for line in raw_index_lines
            )
            if not has_active_route:
                issues.append(
                    ValidationIssue(
                        path.relative_to(repo_root).as_posix(),
                        "legacy raw payload INDEX.md row must map to a current active part route or package-wide DIRECTION/PARTS route, not only a raw-only archive route",
                    )
                )

    return issues


def validate_mechanic_provenance_entry_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name in MECHANIC_PROVENANCE_FILES:
        _require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_PROVENANCE_ENTRY_REQUIRED_TOKENS,
            issues=issues,
        )
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if text:
            for match in MECHANIC_PROVENANCE_ARCHIVE_DETAIL_RE.finditer(text):
                issues.append(
                    ValidationIssue(
                        path_name,
                        f"PROVENANCE.md must bridge to legacy/README.md without carrying archive detail `{match.group(0)}`",
                    )
                )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PROVENANCE_ENTRY_DECISION_NAME,
        tokens=MECHANIC_PROVENANCE_ENTRY_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_PROVENANCE_ENTRY_DECISION_NAME,
            "Mechanic Provenance Entry Contract",
        ),
        issues=issues,
    )

    return issues


def validate_mechanic_provenance_bridge_posture_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name in MECHANIC_PROVENANCE_FILES:
        _require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
            issues=issues,
        )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_NAME,
        tokens=MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_NAME,
            "Mechanic Provenance Bridge Posture",
        ),
        issues=issues,
    )
    for path_name in (MECHANICS_README_NAME, PROOF_TOPOLOGY_NAME, LEGACY_NAMING_NAME):
        _require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=(
                "`PROVENANCE.md` is the active-to-archive bridge",
                "Use active surfaces first:",
                "legacy archive",
            ),
            issues=issues,
        )
    _require_tokens(
        repo_root=repo_root,
        path_name=DESIGN_NAME,
        tokens=(
            "single controlled bridge",
            "active-to-archive bridge",
            "legacy archive",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_LEGACY_BRIDGE_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


def validate_mechanic_legacy_skeleton_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name in MECHANIC_LEGACY_SKELETON_FILES:
        if not (repo_root / path_name).is_file():
            issues.append(
                ValidationIssue(
                    path_name,
                    "active mechanic parent must expose PROVENANCE.md and archive-local legacy entry/accounting surfaces",
                )
            )
    for path_name in MECHANIC_LEGACY_README_FILES:
        _require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_LEGACY_README_REQUIRED_TOKENS,
            issues=issues,
        )
    for path_name in MECHANIC_LEGACY_RAW_README_FILES:
        _require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_LEGACY_RAW_README_REQUIRED_TOKENS,
            issues=issues,
        )
    issues.extend(validate_mechanic_legacy_archive_route_language(repo_root))
    issues.extend(validate_mechanic_legacy_raw_payload_accounting(repo_root))
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_LEGACY_SKELETON_DECISION_NAME,
        tokens=MECHANIC_LEGACY_SKELETON_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_LEGACY_SKELETON_DECISION_NAME,
        tokens=MECHANIC_LEGACY_RAW_PAYLOAD_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_LEGACY_SKELETON_DECISION_NAME,
            "Mechanic Legacy Archive Boundary",
        ),
        issues=issues,
    )

    return issues


def validate_active_legacy_parent_wording(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, forbidden_tokens in ACTIVE_LEGACY_PARENT_WORDING_FORBIDDEN.items():
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if not text:
            continue
        for token in forbidden_tokens:
            if token in text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        f"active route wording must not use legacy parent form {token!r}",
                    )
                )
    _require_tokens(
        repo_root=repo_root,
        path_name=ACTIVE_LEGACY_PARENT_WORDING_DECISION_NAME,
        tokens=ACTIVE_LEGACY_PARENT_WORDING_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            ACTIVE_LEGACY_PARENT_WORDING_DECISION_NAME,
            "Active Legacy Parent Wording Boundary",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_LEGACY_BRIDGE_DIRECTION_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=CHANGELOG_NAME,
        tokens=("Active Legacy Parent Wording Boundary", "runtime evidence"),
        issues=issues,
    )
    return issues


def validate_mechanic_legacy_bridge_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(validate_mechanic_legacy_single_bridge_surfaces(repo_root))
    issues.extend(validate_mechanic_provenance_entry_surfaces(repo_root))
    issues.extend(validate_mechanic_provenance_bridge_posture_surfaces(repo_root))
    return issues


def validate_mechanic_legacy_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(validate_mechanic_legacy_skeleton_surfaces(repo_root))
    issues.extend(validate_mechanic_legacy_bridge_surfaces(repo_root))
    return issues
