"""Source eval dependency, relation, and tree-location validation."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Mapping

import eval_catalog_contract

from validators.common import ValidationIssue
from validators.source_eval_common import CONTRACT_ROOT, relative_location


SOURCE_EVALS_DIR_NAME = "evals"
COMPARISON_FAMILY_BY_BASELINE_MODE = {
    "fixed-baseline": ("comparison", "fixed-baseline"),
    "peer-compare": ("comparison", "peer-compare"),
    "longitudinal-window": ("comparison", "longitudinal-window"),
}


def repo_root_from_env(env_name: str, default: Path) -> Path:
    override = os.environ.get(env_name)
    if not override:
        return default
    return Path(override).expanduser().resolve()


DEPENDENCY_REPO_ROOTS: Mapping[str, Path] = {
    "aoa-techniques": repo_root_from_env(
        "AOA_TECHNIQUES_ROOT", CONTRACT_ROOT.parent / "aoa-techniques"
    ),
    "aoa-skills": repo_root_from_env("AOA_SKILLS_ROOT", CONTRACT_ROOT.parent / "aoa-skills"),
}


def normalize_technique_dependency_refs(
    manifest: dict[str, Any],
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> list[dict[str, str]]:
    normalized, contract_issues = eval_catalog_contract.normalize_technique_dependency_refs(
        manifest,
        eval_yaml_path,
        eval_yaml_path.parents[2],
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in contract_issues
    )
    return normalized


def normalize_skill_dependency_refs(
    manifest: dict[str, Any],
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> list[dict[str, str]]:
    normalized, contract_issues = eval_catalog_contract.normalize_skill_dependency_refs(
        manifest,
        eval_yaml_path,
        eval_yaml_path.parents[2],
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in contract_issues
    )
    return normalized


def dependency_repo_root(
    repo_name: str,
    dependency_roots: Mapping[str, Path] | None = None,
) -> Path | None:
    roots = dependency_roots or DEPENDENCY_REPO_ROOTS
    return roots.get(repo_name)


def validate_dependency_target_exists(
    repo_name: str,
    raw_path: str,
    *,
    location: str,
    issues: list[ValidationIssue],
    dependency_roots: Mapping[str, Path] | None = None,
) -> None:
    if not raw_path:
        return

    repo_root = dependency_repo_root(repo_name, dependency_roots)
    if repo_root is None or not repo_root.exists():
        return

    target_path = repo_root / raw_path
    if not target_path.is_file():
        issues.append(
            ValidationIssue(
                location,
                f"dependency target does not exist: {repo_name}/{raw_path}",
            )
        )


def validate_dependency_drift(
    metadata: dict[str, Any],
    manifest: dict[str, Any],
    eval_md_path: Path,
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
    *,
    dependency_roots: Mapping[str, Path] | None = None,
) -> None:
    frontmatter_techniques = metadata.get("technique_dependencies", [])
    manifest_technique_refs = normalize_technique_dependency_refs(manifest, eval_yaml_path, issues)
    manifest_techniques = [item["id"] for item in manifest_technique_refs]
    if frontmatter_techniques != manifest_techniques:
        issues.append(
            ValidationIssue(
                relative_location(eval_yaml_path),
                f"ordered technique refs do not match {relative_location(eval_md_path)}.technique_dependencies",
            )
        )
    for index, item in enumerate(manifest_technique_refs):
        validate_dependency_target_exists(
            item["repo"],
            item["path"],
            location=f"{relative_location(eval_yaml_path)}.technique_dependencies[{index}].path",
            issues=issues,
            dependency_roots=dependency_roots,
        )

    frontmatter_skills = metadata.get("skill_dependencies", [])
    manifest_skill_refs = normalize_skill_dependency_refs(manifest, eval_yaml_path, issues)
    manifest_skills = [item["name"] for item in manifest_skill_refs]
    if frontmatter_skills != manifest_skills:
        issues.append(
            ValidationIssue(
                relative_location(eval_yaml_path),
                f"ordered skill refs do not match {relative_location(eval_md_path)}.skill_dependencies",
            )
        )
    for index, item in enumerate(manifest_skill_refs):
        validate_dependency_target_exists(
            item["repo"],
            item["path"],
            location=f"{relative_location(eval_yaml_path)}.skill_dependencies[{index}].path",
            issues=issues,
            dependency_roots=dependency_roots,
        )


def validate_manifest_relations(
    eval_name: str,
    manifest: dict[str, Any],
    eval_yaml_path: Path,
    known_eval_names: set[str],
    issues: list[ValidationIssue],
) -> None:
    seen_pairs: set[tuple[str, str]] = set()
    relations = manifest.get("relations", [])

    for index, relation in enumerate(relations):
        if not isinstance(relation, dict):
            continue
        relation_type = relation.get("type")
        target = relation.get("target")
        if not isinstance(relation_type, str) or not isinstance(target, str):
            continue

        location = f"{relative_location(eval_yaml_path)}.relations[{index}]"
        pair = (relation_type, target)
        if target == eval_name:
            issues.append(
                ValidationIssue(location, "relation target cannot point to the same eval")
            )
        if target not in known_eval_names:
            issues.append(
                ValidationIssue(location, f"relation target '{target}' does not exist")
            )
        if pair in seen_pairs:
            issues.append(
                ValidationIssue(
                    location,
                    f"duplicate relation '{relation_type}' -> '{target}'",
                )
            )
        seen_pairs.add(pair)


def expected_source_eval_relative_dir(
    eval_name: str,
    manifest: dict[str, Any],
) -> Path | None:
    baseline_mode = manifest.get("baseline_mode")
    family_parts = COMPARISON_FAMILY_BY_BASELINE_MODE.get(str(baseline_mode))
    if family_parts is not None:
        return Path(*family_parts, eval_name)

    category = manifest.get("category")
    if not isinstance(category, str) or not category.strip():
        return None
    return Path(category, eval_name)


def validate_source_eval_tree_location(
    repo_root: Path,
    bundle_dir: Path,
    eval_name: str,
    manifest: dict[str, Any],
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> None:
    expected_relative = expected_source_eval_relative_dir(eval_name, manifest)
    if expected_relative is None:
        return
    try:
        actual_relative = bundle_dir.relative_to(repo_root / SOURCE_EVALS_DIR_NAME)
    except ValueError:
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                f"source eval directory must live under {SOURCE_EVALS_DIR_NAME}/",
            )
        )
        return

    if actual_relative != expected_relative:
        issues.append(
            ValidationIssue(
                relative_location(eval_yaml_path, repo_root),
                "source eval directory must match claim-family topology: "
                f"expected {SOURCE_EVALS_DIR_NAME}/{expected_relative.as_posix()}",
            )
        )
