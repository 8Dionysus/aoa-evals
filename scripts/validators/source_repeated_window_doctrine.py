"""Repeated-window doctrine alignment checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from validators.source_doctrine_common import (
    EVAL_INDEX_NAME,
    EVAL_SELECTION_NAME,
    REPEATED_WINDOW_GUIDE_NAME,
    ValidationIssue,
    read_text_or_issue,
    relative_location,
)


def validate_repeated_window_doctrine_surfaces(
    repo_root: Path,
    records: Sequence[Any],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    if selected_evals is not None and "aoa-longitudinal-growth-snapshot" not in selected_evals:
        return []

    issues: list[ValidationIssue] = []
    guide_text = read_text_or_issue(
        repo_root / REPEATED_WINDOW_GUIDE_NAME,
        issues,
        root=repo_root,
    )
    docs_readme_text = read_text_or_issue(
        repo_root / "docs" / "README.md",
        issues,
        root=repo_root,
    )
    selection_text = read_text_or_issue(
        repo_root / EVAL_SELECTION_NAME,
        issues,
        root=repo_root,
    )
    index_text = read_text_or_issue(
        repo_root / EVAL_INDEX_NAME,
        issues,
        root=repo_root,
    )

    if "Repeated Window Discipline Guide" not in docs_readme_text:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs/README.md must list Repeated Window Discipline Guide",
            )
        )
    for phrase in (
        "aoa-longitudinal-growth-snapshot",
        "context_note",
        "transition_note",
        "after",
    ):
        if phrase not in guide_text:
            issues.append(
                ValidationIssue(
                    REPEATED_WINDOW_GUIDE_NAME,
                    f"repeated-window doctrine must mention '{phrase}'",
                )
            )

    if "context_note" not in selection_text or "transition_note" not in selection_text:
        issues.append(
            ValidationIssue(
                EVAL_SELECTION_NAME,
                "EVAL_SELECTION.md must explain context_note and transition_note for repeated-window reading",
            )
        )
    if "mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v2.md" not in index_text:
        issues.append(
            ValidationIssue(
                EVAL_INDEX_NAME,
                "EVAL_INDEX.md must reference mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v2.md for repeated-window discipline",
            )
        )

    record_map = {record.name: record for record in records}
    record = record_map.get("aoa-longitudinal-growth-snapshot")
    if record is not None:
        bundle_text = "\n".join(record.sections.values())
        for phrase in ("context_note", "transition_note"):
            if phrase not in bundle_text:
                issues.append(
                    ValidationIssue(
                        relative_location(record.eval_md_path, repo_root),
                        f"longitudinal bundle wording must mention '{phrase}'",
                    )
                )
    return issues


__all__ = ("validate_repeated_window_doctrine_surfaces",)
