"""Artifact/process doctrine alignment checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from validators.source_doctrine_common import (
    ARTIFACT_PROCESS_GUIDE_NAME,
    EVAL_INDEX_NAME,
    EVAL_SELECTION_NAME,
    ValidationIssue,
    read_text_or_issue,
    relative_location,
)


def validate_artifact_process_doctrine_surfaces(
    repo_root: Path,
    records: Sequence[Any],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    relevant_names = {
        "aoa-artifact-review-rubric",
        "aoa-bounded-change-quality",
        "aoa-output-vs-process-gap",
        "aoa-witness-trace-integrity",
        "aoa-compost-provenance-preservation",
    }
    if selected_evals is not None and not relevant_names.intersection(selected_evals):
        return []

    issues: list[ValidationIssue] = []
    guide_text = read_text_or_issue(
        repo_root / ARTIFACT_PROCESS_GUIDE_NAME,
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

    if "Artifact Process Separation Guide" not in docs_readme_text:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs/README.md must list Artifact Process Separation Guide",
            )
        )
    if "## Artifact Process Layer" not in index_text:
        issues.append(
            ValidationIssue(
                EVAL_INDEX_NAME,
                "EVAL_INDEX.md must describe the artifact/process layer as a bounded program layer",
            )
        )
    if "standalone artifact and workflow surfaces" not in selection_text:
        issues.append(
            ValidationIssue(
                EVAL_SELECTION_NAME,
                "EVAL_SELECTION.md must say that the artifact/process bridge is read only after the standalone artifact and workflow surfaces",
            )
        )

    for phrase in (
        "aoa-artifact-review-rubric",
        "aoa-bounded-change-quality",
        "aoa-output-vs-process-gap",
        "aoa-witness-trace-integrity",
        "aoa-compost-provenance-preservation",
        "matched conditions",
        "style-over-substance",
        "mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v2/README.md",
        "mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v2.md",
    ):
        if phrase not in guide_text:
            issues.append(
                ValidationIssue(
                    ARTIFACT_PROCESS_GUIDE_NAME,
                    f"artifact/process doctrine must mention '{phrase}'",
                )
            )

    record_map = {record.name: record for record in records}
    bundle_phrase_checks = {
        "aoa-artifact-review-rubric": ("artifact-side reading",),
        "aoa-bounded-change-quality": ("process-side reading",),
        "aoa-output-vs-process-gap": ("matched-condition", "side_by_side_note"),
        "aoa-witness-trace-integrity": ("adjacent witness context",),
        "aoa-compost-provenance-preservation": ("adjacent compost context",),
    }
    for name, phrases in bundle_phrase_checks.items():
        record = record_map.get(name)
        if record is None:
            continue
        bundle_text = "\n".join(record.sections.values())
        for phrase in phrases:
            if phrase not in bundle_text:
                issues.append(
                    ValidationIssue(
                        relative_location(record.eval_md_path, repo_root),
                        f"artifact/process distinctness wording must mention '{phrase}'",
                    )
                )
    return issues


__all__ = ("validate_artifact_process_doctrine_surfaces",)
