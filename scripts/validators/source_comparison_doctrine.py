"""Comparison doctrine and selector alignment checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from validators.source_doctrine_common import (
    COMPARISON_SPINE_GUIDE_NAME,
    EVAL_INDEX_NAME,
    EVAL_SELECTION_NAME,
    ValidationIssue,
)


def validate_comparison_doctrine_surfaces(
    repo_root: Path,
    records: Sequence[Any],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    comparison_records = [
        record for record in records if record.manifest.get("baseline_mode") != "none"
    ]
    if selected_evals is not None:
        comparison_records = [
            record for record in comparison_records if record.name in selected_evals
        ]
    if not comparison_records:
        return []

    issues: list[ValidationIssue] = []
    doctrine_path = repo_root / COMPARISON_SPINE_GUIDE_NAME
    readme_path = repo_root / "README.md"
    docs_readme_path = repo_root / "docs" / "README.md"
    selection_path = repo_root / EVAL_SELECTION_NAME
    index_path = repo_root / EVAL_INDEX_NAME

    try:
        doctrine_text = doctrine_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [ValidationIssue(COMPARISON_SPINE_GUIDE_NAME, "file is missing")]

    try:
        readme_text = readme_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        readme_text = ""
        issues.append(ValidationIssue("README.md", "file is missing"))

    try:
        docs_readme_text = docs_readme_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        docs_readme_text = ""
        issues.append(ValidationIssue("docs/README.md", "file is missing"))

    try:
        selection_text = selection_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        selection_text = ""
        issues.append(ValidationIssue(EVAL_SELECTION_NAME, "file is missing"))

    try:
        index_text = index_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        index_text = ""
        issues.append(ValidationIssue(EVAL_INDEX_NAME, "file is missing"))

    if "generated reader index" not in readme_text:
        issues.append(
            ValidationIssue(
                "README.md",
                "README.md must route generated comparison readers through the generated reader index",
            )
        )

    if "Comparison Spine Guide" not in docs_readme_text:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs/README.md must list Comparison Spine Guide",
            )
        )
    if "generated/comparison_spine.json" not in docs_readme_text:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs/README.md must reference generated/comparison_spine.json",
            )
        )

    if "## Pick Comparison Surface" not in selection_text:
        issues.append(
            ValidationIssue(
                EVAL_SELECTION_NAME,
                "EVAL_SELECTION.md must include a 'Pick Comparison Surface' chooser section",
            )
        )

    if "comparison spine" not in index_text.lower():
        issues.append(
            ValidationIssue(
                EVAL_INDEX_NAME,
                "EVAL_INDEX.md must describe the comparison spine as a public program layer",
            )
        )

    doctrine_names = {record.name for record in comparison_records}
    doctrine_names.add("aoa-eval-integrity-check")
    for name in sorted(doctrine_names):
        if name not in doctrine_text:
            issues.append(
                ValidationIssue(
                    COMPARISON_SPINE_GUIDE_NAME,
                    f"comparison doctrine must mention '{name}'",
                )
            )

    for record in comparison_records:
        comparison_surface = record.manifest.get("comparison_surface")
        if not isinstance(comparison_surface, dict):
            continue
        selection_question = comparison_surface.get("selection_question")
        if isinstance(selection_question, str) and selection_question not in selection_text:
            issues.append(
                ValidationIssue(
                    EVAL_SELECTION_NAME,
                    f"EVAL_SELECTION.md must include the comparison selector question for '{record.name}'",
                )
            )

    return issues


__all__ = ("validate_comparison_doctrine_surfaces",)
