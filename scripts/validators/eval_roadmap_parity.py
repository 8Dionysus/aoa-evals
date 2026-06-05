"""Source eval roadmap direction and public-surface parity checks."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from validators.common import ValidationIssue, relative_location
from validators.eval_bundle_common import (
    EVAL_INDEX_NAME,
    NO_ADDITIONAL_STARTER_BUNDLES_TEXT,
    ROADMAP_NAME,
    discover_eval_dirs,
    extract_bulleted_eval_names,
)

ROADMAP_DIRECTION_SURFACE_REQUIRED_TOKENS = (
    "# Proof Direction Roadmap",
    "active direction surface for `aoa-evals`",
    "roadmap owns direction and sequencing",
    "release history: [CHANGELOG.md](CHANGELOG.md)",
    "## Update Rule",
    "## Current Direction",
    "`docs/architecture/AGENT_INDEX.md` remains",
    "bundle-local review keeps bounded claim",
    "## Direction Anchors",
    "changelog and validator ledgers carry",
    "## Horizons",
)
ROADMAP_FORBIDDEN_ROUTE_SCAFFOLD = (
    "without making the roadmap an index",
    "without strengthening the bounded claim",
    "without turning the roadmap into",
)


def validate_roadmap_parity(
    repo_root: Path,
    starter_names: Sequence[str],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    roadmap_path = repo_root / ROADMAP_NAME
    try:
        roadmap_text = roadmap_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [ValidationIssue(ROADMAP_NAME, "file is missing")]

    location = relative_location(roadmap_path, repo_root)
    issues: list[ValidationIssue] = []
    for token in ROADMAP_DIRECTION_SURFACE_REQUIRED_TOKENS:
        if token not in roadmap_text:
            issues.append(
                ValidationIssue(
                    location,
                    f"ROADMAP.md must include '{token}'",
                )
            )
    for stale_phrase in ROADMAP_FORBIDDEN_ROUTE_SCAFFOLD:
        if stale_phrase in roadmap_text:
            issues.append(
                ValidationIssue(
                    location,
                    "ROADMAP.md should name direction owner routes before old "
                    f"negative scaffold '{stale_phrase}'",
                )
            )

    starter_set = set(starter_names)
    bundle_names = set(discover_eval_dirs(repo_root))
    current_public_surface_names = set(
        extract_bulleted_eval_names(roadmap_text, "Current public surface:")
    )
    names_to_check = current_public_surface_names
    if selected_evals is not None:
        names_to_check = current_public_surface_names.intersection(selected_evals)

    for name in sorted(names_to_check):
        if name not in bundle_names:
            issues.append(
                ValidationIssue(
                    location,
                    "roadmap 'Current public surface' eval "
                    f"'{name}' has no matching source eval package directory",
                )
            )
            continue
        if name not in starter_set:
            issues.append(
                ValidationIssue(
                    location,
                    f"roadmap 'Current public surface' eval '{name}' must appear in EVAL_INDEX.md starter bundles",
                )
            )

    if selected_evals is not None:
        return issues

    index_path = repo_root / EVAL_INDEX_NAME
    try:
        index_text = index_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return issues

    roadmap_has_absence_note = NO_ADDITIONAL_STARTER_BUNDLES_TEXT in roadmap_text
    index_has_absence_note = NO_ADDITIONAL_STARTER_BUNDLES_TEXT in index_text
    if roadmap_has_absence_note != index_has_absence_note:
        issues.append(
            ValidationIssue(
                location,
                f"absence note '{NO_ADDITIONAL_STARTER_BUNDLES_TEXT}' must stay synchronized with {EVAL_INDEX_NAME}",
            )
        )

    return issues


__all__ = (
    "NO_ADDITIONAL_STARTER_BUNDLES_TEXT",
    "ROADMAP_DIRECTION_SURFACE_REQUIRED_TOKENS",
    "ROADMAP_FORBIDDEN_ROUTE_SCAFFOLD",
    "validate_roadmap_parity",
)
