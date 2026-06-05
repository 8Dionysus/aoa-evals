"""Source eval starter index, selection, and evidence checks."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
from typing import Sequence

from validators.common import ValidationIssue, relative_location
from validators.eval_bundle_common import (
    EVAL_INDEX_NAME,
    EVAL_SELECTION_NAME,
    discover_eval_dirs,
    extract_table_eval_names,
    load_yaml_file,
)


def load_starter_eval_names(
    repo_root: Path,
    issues: list[ValidationIssue] | None = None,
) -> list[str]:
    active_issues = issues if issues is not None else []
    index_path = repo_root / EVAL_INDEX_NAME
    try:
        text = index_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        active_issues.append(ValidationIssue(EVAL_INDEX_NAME, "file is missing"))
        return []

    starter_names = extract_table_eval_names(text, "## Starter eval bundles")
    if not starter_names:
        active_issues.append(
            ValidationIssue(
                relative_location(index_path, repo_root),
                "missing or empty 'Starter eval bundles' table",
            )
        )
    return starter_names


def validate_eval_index(
    repo_root: Path,
    starter_names: Sequence[str],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    index_path = repo_root / EVAL_INDEX_NAME
    location = relative_location(index_path, repo_root)
    counts = Counter(starter_names)

    if selected_evals is None:
        eval_dirs = set(discover_eval_dirs(repo_root))

        for name, count in sorted(counts.items()):
            if count > 1:
                issues.append(
                    ValidationIssue(
                        location,
                        f"starter eval '{name}' appears {count} times in the starter table",
                    )
                )

        starter_set = set(counts.keys())

        for extra in sorted(starter_set - eval_dirs):
            issues.append(
                ValidationIssue(
                    location,
                    f"starter eval '{extra}' has no matching source eval package directory",
                )
            )
    else:
        for name in sorted(selected_evals):
            count = counts.get(name, 0)
            if count > 1:
                issues.append(
                    ValidationIssue(
                        location,
                        f"starter eval '{name}' appears {count} times in the starter table",
                    )
                )

    return issues


def validate_eval_selection(
    repo_root: Path,
    starter_names: Sequence[str],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    selection_path = repo_root / EVAL_SELECTION_NAME
    try:
        text = selection_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [ValidationIssue(EVAL_SELECTION_NAME, "file is missing")]

    location = relative_location(selection_path, repo_root)
    names_in_selection = set(re.findall(r"aoa-[a-z0-9-]+", text))
    names_to_check = selected_evals if selected_evals is not None else set(starter_names)
    issues: list[ValidationIssue] = []

    for token in (
        "# Eval Bundle Selection Chooser",
        "repository-wide chooser for public eval bundles",
    ):
        if token not in text:
            issues.append(
                ValidationIssue(
                    location,
                    f"EVAL_SELECTION.md must mention '{token}'",
                )
            )

    for name in sorted(names_to_check):
        if name not in names_in_selection:
            issues.append(
                ValidationIssue(
                    location,
                    f"starter eval '{name}' is missing from EVAL_SELECTION.md",
                )
            )

    return issues


def validate_starter_bundle_contract(
    repo_root: Path,
    starter_names: Sequence[str],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    names_to_check = selected_evals if selected_evals is not None else set(starter_names)
    eval_dirs = discover_eval_dirs(repo_root)

    for name in sorted(names_to_check):
        bundle_dir = eval_dirs.get(name, repo_root / "evals" / name)
        manifest_path = bundle_dir / "eval.yaml"
        location = relative_location(bundle_dir, repo_root)

        example_report = bundle_dir / "examples" / "example-report.md"
        if not example_report.is_file():
            issues.append(
                ValidationIssue(
                    location,
                    "starter bundle is missing examples/example-report.md",
                )
            )

        manifest_issues: list[ValidationIssue] = []
        manifest = load_yaml_file(manifest_path, manifest_issues, repo_root=repo_root)
        issues.extend(manifest_issues)
        if not isinstance(manifest, dict):
            continue

        evidence = manifest.get("evidence", [])
        if not evidence:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    "starter bundle must include at least one manifest evidence entry",
                )
            )
            continue

        has_integrity_check = any(
            item.get("kind") == "integrity_check" for item in evidence
        )
        if not has_integrity_check:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    "starter bundle must include an evidence entry with kind 'integrity_check'",
                )
            )

        has_origin_need = any(item.get("kind") == "origin_need" for item in evidence)
        if not has_origin_need:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    "starter bundle must include an evidence entry with kind 'origin_need'",
                )
            )

    return issues


__all__ = (
    "load_starter_eval_names",
    "validate_eval_index",
    "validate_eval_selection",
    "validate_starter_bundle_contract",
)
