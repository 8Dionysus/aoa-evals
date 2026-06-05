"""Source eval bundle discovery and catalog-record collection."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

from validators import (
    source_eval_comparison,
    source_eval_evidence,
    source_eval_fixture_contracts,
    source_eval_records,
    source_eval_references,
    source_eval_report_artifacts,
    source_eval_runner_contracts,
)
from validators.common import ValidationIssue
from validators.source_eval_common import format_issues, load_yaml_file, relative_location


SOURCE_EVALS_DIR_NAME = source_eval_records.SOURCE_EVALS_DIR_NAME


def validate_bundle(
    repo_root: Path,
    eval_name: str,
    known_eval_names: set[str],
    eval_dirs: Mapping[str, Path] | None = None,
    *,
    dependency_roots: Mapping[str, Path] | None = None,
) -> tuple[list[ValidationIssue], source_eval_records.EvalBundleRecord | None]:
    issues: list[ValidationIssue] = []
    eval_dirs = eval_dirs or discover_eval_dirs(repo_root)
    bundle_dir = eval_dirs.get(eval_name, repo_root / SOURCE_EVALS_DIR_NAME / eval_name)
    eval_md_path = bundle_dir / "EVAL.md"
    eval_yaml_path = bundle_dir / "eval.yaml"

    if not bundle_dir.is_dir():
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                "source eval package directory is missing",
            )
        )
        return issues, None

    if not eval_md_path.is_file():
        issues.append(ValidationIssue(relative_location(eval_md_path, repo_root), "file is missing"))
    if not eval_yaml_path.is_file():
        issues.append(ValidationIssue(relative_location(eval_yaml_path, repo_root), "file is missing"))

    if not source_eval_records.find_support_artifacts(bundle_dir):
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                "missing support artifact under examples/*.md, checks/*.md, or notes/*.md",
            )
        )

    metadata: dict[str, Any] | None = None
    manifest: dict[str, Any] | None = None
    sections: dict[str, str] = {}
    frontmatter_valid = False
    manifest_valid = False

    if eval_md_path.is_file():
        metadata, sections = source_eval_records.parse_eval_markdown(eval_md_path, issues)
        if metadata is not None:
            frontmatter_valid = source_eval_records.validate_eval_frontmatter(
                eval_name,
                metadata,
                eval_md_path,
                issues,
            )
            source_eval_records.validate_eval_headings(
                sections,
                eval_md_path,
                repo_root,
                issues,
            )

    if eval_yaml_path.is_file():
        loaded_manifest = load_yaml_file(eval_yaml_path, issues)
        if loaded_manifest is not None:
            manifest_valid = source_eval_records.validate_eval_manifest(
                eval_name,
                loaded_manifest,
                eval_yaml_path,
                issues,
            )
            if isinstance(loaded_manifest, dict):
                manifest = loaded_manifest
                source_eval_references.validate_source_eval_tree_location(
                    repo_root,
                    bundle_dir,
                    eval_name,
                    manifest,
                    eval_yaml_path,
                    issues,
                )
                source_eval_evidence.validate_manifest_evidence(
                    manifest,
                    bundle_dir,
                    eval_yaml_path,
                    issues,
                )
                if manifest_valid:
                    source_eval_comparison.validate_comparison_surface_contract(
                        repo_root,
                        bundle_dir,
                        manifest,
                        known_eval_names=known_eval_names,
                        issues=issues,
                    )

    source_eval_report_artifacts.validate_bundle_report_artifacts(repo_root, bundle_dir, manifest, issues)
    source_eval_fixture_contracts.validate_bundle_fixture_contract(repo_root, bundle_dir, manifest, issues)
    source_eval_runner_contracts.validate_bundle_runner_contract(repo_root, bundle_dir, manifest, issues)

    if metadata is not None and manifest is not None and frontmatter_valid and manifest_valid:
        source_eval_records.validate_mirrored_manifest_fields(
            metadata,
            manifest,
            eval_md_path,
            eval_yaml_path,
            issues,
        )
        source_eval_references.validate_dependency_drift(
            metadata,
            manifest,
            eval_md_path,
            eval_yaml_path,
            issues,
            dependency_roots=dependency_roots,
        )
        source_eval_references.validate_manifest_relations(
            eval_name,
            manifest,
            eval_yaml_path,
            known_eval_names,
            issues,
        )
        record = source_eval_records.EvalBundleRecord(
            name=eval_name,
            bundle_dir=bundle_dir,
            eval_md_path=eval_md_path,
            eval_yaml_path=eval_yaml_path,
            metadata=metadata,
            manifest=manifest,
            sections=sections,
        )
        return issues, record

    return issues, None


def discover_eval_dirs(repo_root: Path) -> dict[str, Path]:
    source_root = repo_root / SOURCE_EVALS_DIR_NAME
    if not source_root.is_dir():
        raise FileNotFoundError(f"missing source eval directory at {source_root}")

    eval_dirs: dict[str, Path] = {}
    for manifest_path in sorted(source_root.glob("**/eval.yaml")):
        eval_dir = manifest_path.parent
        eval_name = eval_dir.name
        if eval_name in eval_dirs:
            raise ValueError(
                "duplicate source eval directory name "
                f"'{eval_name}' at {relative_location(eval_dirs[eval_name], repo_root)} "
                f"and {relative_location(eval_dir, repo_root)}"
            )
        eval_dirs[eval_name] = eval_dir
    return eval_dirs


def discover_eval_names(repo_root: Path) -> list[str]:
    return sorted(discover_eval_dirs(repo_root))


def source_eval_dir(repo_root: Path, eval_name: str) -> Path:
    try:
        return discover_eval_dirs(repo_root).get(
            eval_name,
            repo_root / SOURCE_EVALS_DIR_NAME / eval_name,
        )
    except (FileNotFoundError, ValueError):
        return repo_root / SOURCE_EVALS_DIR_NAME / eval_name


def collect_catalog_records(
    repo_root: Path,
    eval_names: Sequence[str] | None = None,
    *,
    dependency_roots: Mapping[str, Path] | None = None,
) -> tuple[list[ValidationIssue], list[source_eval_records.EvalBundleRecord]]:
    eval_dirs = discover_eval_dirs(repo_root)
    all_eval_names = sorted(eval_dirs)
    selected_names = list(eval_names) if eval_names is not None else all_eval_names
    known_eval_names = set(all_eval_names)

    issues: list[ValidationIssue] = []
    records: list[source_eval_records.EvalBundleRecord] = []
    for name in selected_names:
        bundle_issues, record = validate_bundle(
            repo_root,
            name,
            known_eval_names,
            eval_dirs=eval_dirs,
            dependency_roots=dependency_roots,
        )
        issues.extend(bundle_issues)
        if record is not None:
            records.append(record)
    return issues, records


__all__ = (
    "SOURCE_EVALS_DIR_NAME",
    "collect_catalog_records",
    "discover_eval_dirs",
    "discover_eval_names",
    "format_issues",
    "source_eval_dir",
    "validate_bundle",
)
