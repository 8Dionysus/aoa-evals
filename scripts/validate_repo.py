#!/usr/bin/env python3
"""Local validator and catalog builder helpers for aoa-evals bundles."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Sequence

import yaml
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLES_DIR_NAME = "bundles"
EVAL_INDEX_NAME = "EVAL_INDEX.md"
EVAL_SELECTION_NAME = "EVAL_SELECTION.md"
SCHEMAS_DIR_NAME = "schemas"
GENERATED_DIR_NAME = "generated"
FULL_CATALOG_NAME = "eval_catalog.json"
MIN_CATALOG_NAME = "eval_catalog.min.json"
CATALOG_VERSION = 1
CATALOG_SOURCE_OF_TRUTH = {
    "eval_markdown": "bundles/*/EVAL.md",
    "eval_manifest": "bundles/*/eval.yaml",
}

MIRRORED_FIELDS = (
    "name",
    "category",
    "status",
    "object_under_evaluation",
    "claim_type",
    "baseline_mode",
    "report_format",
)
MIN_ENTRY_KEYS = (
    "name",
    "category",
    "status",
    "summary",
    "object_under_evaluation",
    "claim_type",
    "baseline_mode",
    "verdict_shape",
    "report_format",
    "maturity_score",
    "rigor_level",
    "repeatability",
    "portability_level",
    "review_required",
    "validation_strength",
    "export_ready",
    "technique_dependencies",
    "skill_dependencies",
    "eval_path",
)
KNOWN_REPOS = (
    "aoa-routing",
    "aoa-techniques",
    "aoa-skills",
    "aoa-evals",
    "aoa-memo",
)

REQUIRED_HEADINGS = {
    "Intent",
    "Object under evaluation",
    "Bounded claim",
    "Trigger boundary",
    "Inputs",
    "Fixtures and case surface",
    "Scoring or verdict logic",
    "Baseline or comparison mode",
    "Execution contract",
    "Outputs",
    "Failure modes",
    "Blind spots",
    "Interpretation guidance",
    "Verification",
    "Technique traceability",
    "Adaptation points",
}
OPTIONAL_HEADINGS = {"Skill traceability"}


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


@dataclass(frozen=True)
class EvalBundleRecord:
    name: str
    bundle_dir: Path
    eval_md_path: Path
    eval_yaml_path: Path
    metadata: dict[str, Any]
    manifest: dict[str, Any]


@lru_cache(maxsize=None)
def load_schema(schema_name: str) -> dict[str, Any]:
    schema_path = REPO_ROOT / SCHEMAS_DIR_NAME / schema_name
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=None)
def get_schema_validator(schema_name: str) -> Draft202012Validator:
    return Draft202012Validator(load_schema(schema_name))


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate local aoa-evals bundles.")
    parser.add_argument(
        "--eval",
        help="Validate a single eval bundle by directory name.",
    )
    return parser.parse_args(argv)


def relative_location(path: Path, root: Path | None = None) -> str:
    target_root = root or REPO_ROOT
    try:
        return path.relative_to(target_root).as_posix()
    except ValueError:
        return path.as_posix()


def format_schema_path(path_parts: Iterable[Any]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        else:
            if parts:
                parts.append(f".{part}")
            else:
                parts.append(str(part))
    return "".join(parts)


def validate_against_schema(
    data: Any,
    schema_name: str,
    location: str,
    issues: list[ValidationIssue],
) -> bool:
    validator = get_schema_validator(schema_name)
    schema_errors = sorted(
        validator.iter_errors(data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    for error in schema_errors:
        error_path = format_schema_path(error.absolute_path)
        if error_path:
            message = f"schema violation at '{error_path}': {error.message}"
        else:
            message = f"schema violation: {error.message}"
        issues.append(ValidationIssue(location, message))
    return not schema_errors


def load_yaml_file(path: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path), "file is missing"))
        return None
    except yaml.YAMLError as exc:
        issues.append(ValidationIssue(relative_location(path), f"invalid YAML: {exc}"))
        return None
    return data


def parse_eval_markdown(
    eval_md_path: Path,
    issues: list[ValidationIssue],
) -> tuple[dict[str, Any] | None, set[str]]:
    try:
        text = eval_md_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(eval_md_path), "file is missing"))
        return None, set()

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        issues.append(
            ValidationIssue(
                relative_location(eval_md_path),
                "missing YAML frontmatter opening delimiter",
            )
        )
        return None, set()

    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        issues.append(
            ValidationIssue(
                relative_location(eval_md_path),
                "missing YAML frontmatter closing delimiter",
            )
        )
        return None, set()

    frontmatter_text = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1 :])

    try:
        metadata = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError as exc:
        issues.append(
            ValidationIssue(
                relative_location(eval_md_path),
                f"invalid frontmatter YAML: {exc}",
            )
        )
        return None, set()

    if not isinstance(metadata, dict):
        issues.append(
            ValidationIssue(
                relative_location(eval_md_path),
                "frontmatter must parse to a mapping",
            )
        )
        return None, set()

    headings = set(
        match.group(1).strip()
        for match in re.finditer(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE)
    )
    return metadata, headings


def find_support_artifacts(bundle_dir: Path) -> list[Path]:
    artifacts: list[Path] = []
    for folder_name in ("examples", "checks", "notes"):
        folder = bundle_dir / folder_name
        if folder.is_dir():
            artifacts.extend(sorted(folder.glob("*.md")))
    return artifacts


def resolve_manifest_path(bundle_dir: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    return bundle_dir / candidate


def normalize_repo_name(raw: str) -> str:
    text = raw.strip()
    if not text:
        raise ValueError("repo value must not be empty")
    if text in KNOWN_REPOS:
        return text

    if text.startswith("git@"):
        text = text.split(":", 1)[-1]
    if "://" in text:
        text = text.split("://", 1)[-1]
        if "/" in text:
            text = text.split("/", 1)[-1]
    text = text.rstrip("/")
    if text.endswith(".git"):
        text = text[:-4]

    candidate = text.rsplit("/", 1)[-1]
    if candidate in KNOWN_REPOS:
        return candidate

    raise ValueError(f"unsupported repo reference '{raw}'")


def is_repo_relative_path(raw_path: str) -> bool:
    if not raw_path or raw_path == "TBD":
        return False
    if re.match(r"^[A-Za-z]:[/\\\\]", raw_path) or raw_path.startswith(("/", "\\\\")):
        return False
    normalized = raw_path.replace("\\", "/")
    if normalized.startswith("./"):
        return False
    parts = normalized.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        return False
    return True


def ensure_repo_relative_path(raw_path: str, location: str, issues: list[ValidationIssue]) -> str:
    if not isinstance(raw_path, str) or not raw_path.strip():
        issues.append(ValidationIssue(location, "path must be a non-empty string"))
        return ""

    value = raw_path.strip().replace("\\", "/")
    if not is_repo_relative_path(value):
        issues.append(
            ValidationIssue(location, "path must be a concrete repo-relative path")
        )
    return value


def extract_table_eval_names(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    try:
        start_index = next(
            index for index, line in enumerate(lines) if line.strip() == heading
        )
    except StopIteration:
        return []

    table_lines: list[str] = []
    for line in lines[start_index + 1 :]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if stripped.startswith("|"):
            table_lines.append(line)
            continue
        if table_lines and not stripped:
            break
        if table_lines:
            break

    pattern = re.compile(r"^\|\s*(aoa-[a-z0-9-]+)\s*\|")
    return [
        pattern.match(line).group(1)
        for line in table_lines
        if pattern.match(line)
    ]


def load_starter_eval_names(
    repo_root: Path,
    issues: list[ValidationIssue],
) -> list[str]:
    index_path = repo_root / EVAL_INDEX_NAME
    try:
        text = index_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(EVAL_INDEX_NAME, "file is missing"))
        return []

    starter_names = extract_table_eval_names(text, "## Starter eval bundles")
    if not starter_names:
        issues.append(
            ValidationIssue(
                relative_location(index_path, repo_root),
                "missing or empty 'Starter eval bundles' table",
            )
        )
    return starter_names


def validate_eval_frontmatter(
    eval_name: str,
    metadata: dict[str, Any],
    eval_md_path: Path,
    issues: list[ValidationIssue],
) -> bool:
    location = relative_location(eval_md_path)
    valid = validate_against_schema(
        metadata, "eval-frontmatter.schema.json", location, issues
    )
    if metadata.get("name") != eval_name:
        issues.append(
            ValidationIssue(location, "frontmatter 'name' must match the directory name")
        )
        valid = False
    return valid


def validate_eval_headings(
    headings: set[str],
    eval_md_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(eval_md_path)
    for heading in sorted(REQUIRED_HEADINGS - headings):
        issues.append(ValidationIssue(location, f"missing required section '{heading}'"))

    if not OPTIONAL_HEADINGS.intersection(headings):
        issues.append(
            ValidationIssue(
                location,
                "missing section 'Skill traceability'; include it even if it only states none or deferred",
            )
        )


def validate_eval_manifest(
    eval_name: str,
    manifest: Any,
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> bool:
    location = relative_location(eval_yaml_path)
    if not isinstance(manifest, dict):
        issues.append(ValidationIssue(location, "manifest must parse to a mapping"))
        return False

    valid = validate_against_schema(manifest, "eval-manifest.schema.json", location, issues)
    if manifest.get("name") != eval_name:
        issues.append(
            ValidationIssue(location, "'name' must match the directory name")
        )
        valid = False
    return valid


def validate_manifest_evidence(
    manifest: dict[str, Any],
    bundle_dir: Path,
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(eval_yaml_path)
    evidence = manifest.get("evidence", [])

    for item in evidence:
        raw_path = item.get("path")
        if not isinstance(raw_path, str):
            continue
        resolved_path = resolve_manifest_path(bundle_dir, raw_path)
        if not resolved_path.exists():
            issues.append(
                ValidationIssue(
                    location,
                    f"evidence path '{raw_path}' does not exist",
                )
            )

    if manifest.get("baseline_mode") != "none":
        has_baseline_readiness = any(
            item.get("kind") == "baseline_readiness" for item in evidence
        )
        if not has_baseline_readiness:
            issues.append(
                ValidationIssue(
                    location,
                    "baseline_mode is not 'none' but no evidence entry with kind 'baseline_readiness' is present",
                )
            )


def validate_mirrored_manifest_fields(
    metadata: dict[str, Any],
    manifest: dict[str, Any],
    eval_md_path: Path,
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(eval_yaml_path)
    source_location = relative_location(eval_md_path)
    for field_name in MIRRORED_FIELDS:
        if metadata.get(field_name) != manifest.get(field_name):
            issues.append(
                ValidationIssue(
                    location,
                    f"field '{field_name}' does not match {source_location}",
                )
            )


def normalize_technique_dependency_refs(
    manifest: dict[str, Any],
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    dependencies = manifest.get("technique_dependencies", [])
    for index, item in enumerate(dependencies):
        location = f"{relative_location(eval_yaml_path)}.technique_dependencies[{index}]"
        if not isinstance(item, dict):
            continue
        dependency_id = item.get("id")
        repo_raw = item.get("repo")
        raw_path = item.get("path")

        if not isinstance(dependency_id, str):
            continue
        if not isinstance(repo_raw, str):
            continue

        try:
            repo_name = normalize_repo_name(repo_raw)
        except ValueError as exc:
            issues.append(ValidationIssue(location, str(exc)))
            repo_name = repo_raw

        if repo_name != "aoa-techniques":
            issues.append(
                ValidationIssue(location, ".repo must resolve to 'aoa-techniques'")
            )

        normalized_path = ""
        if isinstance(raw_path, str):
            normalized_path = ensure_repo_relative_path(
                raw_path,
                f"{location}.path",
                issues,
            )

        normalized.append(
            {
                "id": dependency_id,
                "repo": repo_name,
                "path": normalized_path,
            }
        )
    return normalized


def normalize_skill_dependency_refs(
    manifest: dict[str, Any],
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    dependencies = manifest.get("skill_dependencies", [])
    for index, item in enumerate(dependencies):
        location = f"{relative_location(eval_yaml_path)}.skill_dependencies[{index}]"
        if not isinstance(item, dict):
            continue
        dependency_name = item.get("name")
        repo_raw = item.get("repo")
        raw_path = item.get("path")

        if not isinstance(dependency_name, str):
            continue
        if not isinstance(repo_raw, str):
            continue

        try:
            repo_name = normalize_repo_name(repo_raw)
        except ValueError as exc:
            issues.append(ValidationIssue(location, str(exc)))
            repo_name = repo_raw

        if repo_name != "aoa-skills":
            issues.append(
                ValidationIssue(location, ".repo must resolve to 'aoa-skills'")
            )

        normalized_path = ""
        if isinstance(raw_path, str):
            normalized_path = ensure_repo_relative_path(
                raw_path,
                f"{location}.path",
                issues,
            )

        normalized.append(
            {
                "name": dependency_name,
                "repo": repo_name,
                "path": normalized_path,
            }
        )
    return normalized


def validate_dependency_drift(
    metadata: dict[str, Any],
    manifest: dict[str, Any],
    eval_md_path: Path,
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
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


def validate_bundle(
    repo_root: Path,
    eval_name: str,
    known_eval_names: set[str],
) -> tuple[list[ValidationIssue], EvalBundleRecord | None]:
    issues: list[ValidationIssue] = []
    bundle_dir = repo_root / BUNDLES_DIR_NAME / eval_name
    eval_md_path = bundle_dir / "EVAL.md"
    eval_yaml_path = bundle_dir / "eval.yaml"

    if not bundle_dir.is_dir():
        issues.append(
            ValidationIssue(relative_location(bundle_dir, repo_root), "bundle directory is missing")
        )
        return issues, None

    if not eval_md_path.is_file():
        issues.append(ValidationIssue(relative_location(eval_md_path, repo_root), "file is missing"))
    if not eval_yaml_path.is_file():
        issues.append(ValidationIssue(relative_location(eval_yaml_path, repo_root), "file is missing"))

    if not find_support_artifacts(bundle_dir):
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                "missing support artifact under examples/*.md, checks/*.md, or notes/*.md",
            )
        )

    metadata: dict[str, Any] | None = None
    manifest: dict[str, Any] | None = None
    headings: set[str] = set()
    frontmatter_valid = False
    manifest_valid = False

    if eval_md_path.is_file():
        metadata, headings = parse_eval_markdown(eval_md_path, issues)
        if metadata is not None:
            frontmatter_valid = validate_eval_frontmatter(eval_name, metadata, eval_md_path, issues)
            validate_eval_headings(headings, eval_md_path, issues)

    if eval_yaml_path.is_file():
        loaded_manifest = load_yaml_file(eval_yaml_path, issues)
        if loaded_manifest is not None:
            manifest_valid = validate_eval_manifest(eval_name, loaded_manifest, eval_yaml_path, issues)
            if isinstance(loaded_manifest, dict):
                manifest = loaded_manifest
                validate_manifest_evidence(manifest, bundle_dir, eval_yaml_path, issues)

    if metadata is not None and manifest is not None and frontmatter_valid and manifest_valid:
        validate_mirrored_manifest_fields(
            metadata,
            manifest,
            eval_md_path,
            eval_yaml_path,
            issues,
        )
        validate_dependency_drift(
            metadata,
            manifest,
            eval_md_path,
            eval_yaml_path,
            issues,
        )
        validate_manifest_relations(
            eval_name,
            manifest,
            eval_yaml_path,
            known_eval_names,
            issues,
        )
        record = EvalBundleRecord(
            name=eval_name,
            bundle_dir=bundle_dir,
            eval_md_path=eval_md_path,
            eval_yaml_path=eval_yaml_path,
            metadata=metadata,
            manifest=manifest,
        )
        return issues, record

    return issues, None


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
        eval_dirs = {
            path.name
            for path in (repo_root / BUNDLES_DIR_NAME).iterdir()
            if path.is_dir()
        }

        for name, count in sorted(counts.items()):
            if count > 1:
                issues.append(
                    ValidationIssue(
                        location,
                        f"starter eval '{name}' appears {count} times in the starter table",
                    )
                )

        starter_set = set(counts.keys())

        for missing in sorted(eval_dirs - starter_set):
            issues.append(
                ValidationIssue(
                    location,
                    f"eval '{missing}' is missing from the starter table",
                )
            )

        for extra in sorted(starter_set - eval_dirs):
            issues.append(
                ValidationIssue(
                    location,
                    f"starter eval '{extra}' has no matching bundle directory",
                )
            )
    else:
        for name in sorted(selected_evals):
            count = counts.get(name, 0)
            if count == 0:
                issues.append(
                    ValidationIssue(
                        location,
                        f"eval '{name}' is missing from the starter table",
                    )
                )
            elif count > 1:
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

    for name in sorted(names_to_check):
        bundle_dir = repo_root / BUNDLES_DIR_NAME / name
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
        manifest = load_yaml_file(manifest_path, manifest_issues)
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

    return issues


def discover_eval_names(repo_root: Path) -> list[str]:
    bundles_dir = repo_root / BUNDLES_DIR_NAME
    if not bundles_dir.is_dir():
        raise FileNotFoundError(f"missing bundles directory at {bundles_dir}")
    return sorted(path.name for path in bundles_dir.iterdir() if path.is_dir())


def collect_catalog_records(
    repo_root: Path,
    eval_names: Sequence[str] | None = None,
) -> tuple[list[ValidationIssue], list[EvalBundleRecord]]:
    all_eval_names = discover_eval_names(repo_root)
    selected_names = list(eval_names) if eval_names is not None else all_eval_names
    known_eval_names = set(all_eval_names)

    issues: list[ValidationIssue] = []
    records: list[EvalBundleRecord] = []
    for name in selected_names:
        bundle_issues, record = validate_bundle(repo_root, name, known_eval_names)
        issues.extend(bundle_issues)
        if record is not None:
            records.append(record)
    return issues, records


def full_catalog_entry(repo_root: Path, record: EvalBundleRecord) -> dict[str, Any]:
    metadata = record.metadata
    manifest = record.manifest
    technique_refs = [
        {
            "id": item["id"],
            "repo": normalize_repo_name(item["repo"]),
            "path": item["path"].replace("\\", "/"),
        }
        for item in manifest["technique_dependencies"]
    ]
    skill_refs = [
        {
            "name": item["name"],
            "repo": normalize_repo_name(item["repo"]),
            "path": item["path"].replace("\\", "/"),
        }
        for item in manifest["skill_dependencies"]
    ]
    return {
        "name": metadata["name"],
        "category": metadata["category"],
        "status": metadata["status"],
        "summary": metadata["summary"],
        "object_under_evaluation": metadata["object_under_evaluation"],
        "claim_type": metadata["claim_type"],
        "baseline_mode": metadata["baseline_mode"],
        "verdict_shape": manifest["verdict_shape"],
        "report_format": metadata["report_format"],
        "maturity_score": manifest["maturity_score"],
        "rigor_level": manifest["rigor_level"],
        "repeatability": manifest["repeatability"],
        "portability_level": manifest["portability_level"],
        "review_required": manifest["review_required"],
        "validation_strength": manifest["validation_strength"],
        "export_ready": manifest["export_ready"],
        "blind_spot_disclosure": manifest["blind_spot_disclosure"],
        "score_interpretation_bound": manifest["score_interpretation_bound"],
        "eval_path": relative_location(record.eval_md_path, repo_root),
        "technique_dependencies": list(metadata["technique_dependencies"]),
        "technique_refs": technique_refs,
        "skill_dependencies": list(metadata["skill_dependencies"]),
        "skill_refs": skill_refs,
        "relations": list(manifest["relations"]),
        "evidence": list(manifest["evidence"]),
    }


def project_min_catalog(full_catalog: dict[str, Any]) -> dict[str, Any]:
    return {
        "catalog_version": full_catalog["catalog_version"],
        "source_of_truth": full_catalog["source_of_truth"],
        "evals": [
            {key: entry[key] for key in MIN_ENTRY_KEYS}
            for entry in full_catalog["evals"]
        ],
    }


def build_catalog_payloads(
    repo_root: Path,
    records: list[EvalBundleRecord],
) -> tuple[dict[str, Any], dict[str, Any]]:
    sorted_records = sorted(records, key=lambda record: record.name)
    full_catalog = {
        "catalog_version": CATALOG_VERSION,
        "source_of_truth": CATALOG_SOURCE_OF_TRUTH,
        "evals": [full_catalog_entry(repo_root, record) for record in sorted_records],
    }
    return full_catalog, project_min_catalog(full_catalog)


def read_json_file(path: Path, issues: list[ValidationIssue], repo_root: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, repo_root), "file is missing"))
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(relative_location(path, repo_root), f"invalid JSON: {exc}"))
    return None


def write_json_file(path: Path, payload: Any, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if compact:
        text = json.dumps(
            payload,
            ensure_ascii=True,
            indent=None,
            separators=(",", ":"),
            sort_keys=True,
        )
    else:
        text = json.dumps(
            payload,
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
    path.write_text(f"{text}\n", encoding="utf-8")


def validate_generated_catalogs(
    repo_root: Path,
    records: list[EvalBundleRecord],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    full_path = repo_root / GENERATED_DIR_NAME / FULL_CATALOG_NAME
    min_path = repo_root / GENERATED_DIR_NAME / MIN_CATALOG_NAME

    expected_full, expected_min = build_catalog_payloads(repo_root, records)
    actual_full = read_json_file(full_path, issues, repo_root)
    actual_min = read_json_file(min_path, issues, repo_root)

    if actual_full is None or actual_min is None:
        return issues

    if actual_full != expected_full:
        issues.append(
            ValidationIssue(
                relative_location(full_path, repo_root),
                "generated catalog is out of date; run 'python scripts/build_catalog.py'",
            )
        )
    if actual_min != expected_min:
        issues.append(
            ValidationIssue(
                relative_location(min_path, repo_root),
                "generated min catalog is out of date; run 'python scripts/build_catalog.py'",
            )
        )

    projected_min = project_min_catalog(actual_full)
    if actual_min != projected_min:
        issues.append(
            ValidationIssue(
                relative_location(min_path, repo_root),
                "min catalog must stay a projection of the full catalog",
            )
        )

    return issues


def format_issues(issues: Sequence[ValidationIssue]) -> str:
    lines = [f"- {issue.location}: {issue.message}" for issue in issues]
    return "\n".join(lines)


def run_validation(
    repo_root: Path,
    eval_name: str | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    all_eval_names = discover_eval_names(repo_root)
    starter_names = load_starter_eval_names(repo_root, issues)

    if eval_name is not None:
        if eval_name not in all_eval_names:
            raise ValueError(f"unknown eval '{eval_name}'")
        target_evals = [eval_name]
        selected_evals = {eval_name}
    else:
        target_evals = all_eval_names
        selected_evals = None

    source_issues, records = collect_catalog_records(repo_root, target_evals)
    issues.extend(source_issues)

    issues.extend(
        validate_eval_index(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_evals,
        )
    )
    issues.extend(
        validate_eval_selection(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_evals,
        )
    )
    issues.extend(
        validate_starter_bundle_contract(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_evals,
        )
    )

    if eval_name is None and not source_issues:
        all_source_issues, all_records = collect_catalog_records(repo_root)
        if not all_source_issues:
            issues.extend(validate_generated_catalogs(repo_root, all_records))

    return issues


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        issues = run_validation(repo_root, eval_name=args.eval)
    except ValueError as exc:
        print(f"Argument error: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2

    if issues:
        scope = args.eval if args.eval else "repository"
        print(f"Validation failed for {scope}.")
        print(format_issues(issues))
        return 1

    if args.eval:
        print(f"Validation passed for eval '{args.eval}'.")
    else:
        eval_count = len(discover_eval_names(repo_root))
        print(f"Validation passed for {eval_count} eval bundles.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
