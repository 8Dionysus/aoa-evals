"""Shared root legacy naming constants and token helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from validators import decision_index_paths
from validators.common import ValidationIssue, read_text_or_issue


DESIGN_NAME = "DESIGN.md"
DESIGN_AGENTS_NAME = "DESIGN.AGENTS.md"
ROADMAP_NAME = "ROADMAP.md"
PROOF_TOPOLOGY_NAME = "docs/architecture/PROOF_TOPOLOGY.md"
ROUTE_RESIDUE_GUARDS_NAME = "docs/architecture/ROUTE_RESIDUE_GUARDS.md"
DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
LEGACY_NAMING_NAME = "docs/architecture/LEGACY_NAMING.md"
MECHANICS_EVIDENCE_CLUSTERS_NAME = "mechanics/EVIDENCE_CLUSTERS.md"

LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0091-legacy-naming-single-bridge-language.md"
)
LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_COMMAND = (
    "python -m pytest -q tests/test_root_surface_roles.py -k legacy_naming_single_bridge_language"
)
LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0096-legacy-naming-posture-guide.md"
)
LEGACY_NAMING_POSTURE_GUIDE_COMMAND = (
    "python -m pytest -q tests/test_root_surface_roles.py -k legacy_naming_posture_guide"
)

LEGACY_NAMING_REQUIRED_TOKENS = (
    "Legacy Naming Posture",
    "posture guide",
    "archive details",
    "active",
    "historical",
    "accepted-input",
    "generated-projection",
    "candidate-only",
    "provenance-bridge",
    "active-first route",
    "PROVENANCE.md",
    "single controlled bridge",
    "active mechanic surfaces",
    "Active Owner Lookup",
    "Route Rules",
)
LEGACY_NAMING_FORBIDDEN_DETAIL_TOKENS = (
    "It is not an archive map",
    "Do not put legacy archive details in this file",
    "## Current Active Owners",
    "Wrong parent forms such as",
    "`agon-proof`",
    "`titan-canaries`",
    "`proof-release`",
    "`runtime-evidence`",
    "`sibling-proof-refs`",
    "`repair`",
    "The old `Spark/` root path",
)
LEGACY_NAMING_DECISION_REQUIRED_TOKENS = (
    "docs/architecture/LEGACY_NAMING.md",
    "posture guide",
    "accepted-input",
    "active topology",
    "generated projections",
    "archive details",
    "not authorize starting new work from legacy directories",
)
LEGACY_NAMING_POSTURE_GUIDE_DECISION_REQUIRED_TOKENS = (
    "Legacy Naming Posture Guide",
    "docs/architecture/LEGACY_NAMING.md",
    "posture guide",
    "not a global archive map",
    "archive details",
    "PROVENANCE.md",
    LEGACY_NAMING_POSTURE_GUIDE_COMMAND,
)
LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_REQUIRED_TOKENS = (
    "Legacy Naming Single-Bridge Language",
    "docs/architecture/LEGACY_NAMING.md",
    "`PROVENANCE.md`",
    "single controlled bridge",
    "archive details",
    LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_COMMAND,
)
ROADMAP_LEGACY_NAMING_DIRECTION_TOKENS = (
    LEGACY_NAMING_NAME,
    "Legacy naming",
    "active names",
    "legacy bridge posture",
)


def require_tokens(
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
        for relative_path in decision_index_paths.GENERATED_INDEX_PATHS:
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
            issues.append(ValidationIssue(path_name, f"file must mention '{token}'"))
    return text
