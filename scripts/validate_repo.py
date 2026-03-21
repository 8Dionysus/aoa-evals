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

import eval_catalog_contract
import eval_capsule_contract
import eval_section_contract

REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLES_DIR_NAME = "bundles"
EVAL_INDEX_NAME = "EVAL_INDEX.md"
EVAL_SELECTION_NAME = "EVAL_SELECTION.md"
ROADMAP_NAME = "docs/ROADMAP.md"
SCHEMAS_DIR_NAME = "schemas"
GENERATED_DIR_NAME = "generated"
FULL_CATALOG_NAME = eval_catalog_contract.FULL_CATALOG_NAME
MIN_CATALOG_NAME = eval_catalog_contract.MIN_CATALOG_NAME
CATALOG_VERSION = eval_catalog_contract.CATALOG_VERSION
CATALOG_SOURCE_OF_TRUTH = eval_catalog_contract.CATALOG_SOURCE_OF_TRUTH
CAPSULE_NAME = eval_capsule_contract.CAPSULE_NAME
CAPSULE_VERSION = eval_capsule_contract.CAPSULE_VERSION
CAPSULE_SOURCE_OF_TRUTH = eval_capsule_contract.CAPSULE_SOURCE_OF_TRUTH
SECTION_NAME = eval_section_contract.SECTIONS_NAME
SECTION_VERSION = eval_section_contract.SECTION_VERSION
SECTION_SOURCE_OF_TRUTH = eval_section_contract.SECTION_SOURCE_OF_TRUTH

MIRRORED_FIELDS = (
    "name",
    "category",
    "status",
    "object_under_evaluation",
    "claim_type",
    "baseline_mode",
    "report_format",
)
MIN_ENTRY_KEYS = eval_catalog_contract.MIN_ENTRY_KEYS
KNOWN_REPOS = eval_catalog_contract.KNOWN_REPOS
NO_ADDITIONAL_STARTER_BUNDLES_TEXT = (
    "No additional planned starter bundles are currently named publicly."
)

REQUIRED_HEADINGS = set(eval_section_contract.CANONICAL_HEADINGS)


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
    sections: dict[str, str]


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
) -> tuple[dict[str, Any] | None, dict[str, str]]:
    try:
        text = eval_md_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(eval_md_path), "file is missing"))
        return None, {}

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        issues.append(
            ValidationIssue(
                relative_location(eval_md_path),
                "missing YAML frontmatter opening delimiter",
            )
        )
        return None, {}

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
        return None, {}

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
        return None, {}

    if not isinstance(metadata, dict):
        issues.append(
            ValidationIssue(
                relative_location(eval_md_path),
                "frontmatter must parse to a mapping",
            )
        )
        return None, {}

    sections: dict[str, str] = {}
    current_heading: str | None = None
    current_lines: list[str] = []
    for line in body.splitlines():
        heading_match = re.match(r"^##\s+(.+?)\s*$", line)
        if heading_match:
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = heading_match.group(1).strip()
            current_lines = []
            continue
        if current_heading is not None:
            current_lines.append(line)
    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines).strip()

    return metadata, sections


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
    return eval_catalog_contract.normalize_repo_name(raw)


def is_repo_relative_path(raw_path: str) -> bool:
    return eval_catalog_contract.is_repo_relative_path(raw_path)


def ensure_repo_relative_path(raw_path: str, location: str, issues: list[ValidationIssue]) -> str:
    value, contract_issues = eval_catalog_contract.ensure_repo_relative_path(raw_path, location)
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in contract_issues
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


def has_evidence_kind(evidence: Sequence[dict[str, Any]], kind: str) -> bool:
    return any(item.get("kind") == kind for item in evidence)


def load_evidence_texts(
    bundle_dir: Path,
    evidence: Sequence[dict[str, Any]],
    *,
    kind: str,
) -> list[str]:
    texts: list[str] = []
    for item in evidence:
        if item.get("kind") != kind:
            continue
        raw_path = item.get("path")
        if not isinstance(raw_path, str):
            continue
        resolved_path = resolve_manifest_path(bundle_dir, raw_path)
        if not resolved_path.is_file():
            continue
        try:
            texts.append(resolved_path.read_text(encoding="utf-8").lower())
        except OSError:
            continue
    return texts


def contains_phrase_group(text: str, phrases: Sequence[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def validate_status_specific_evidence(
    manifest: dict[str, Any],
    bundle_dir: Path,
    location: str,
    evidence: Sequence[dict[str, Any]],
    issues: list[ValidationIssue],
) -> None:
    required_evidence_by_status = {
        "portable": ("portable_review",),
        "baseline": ("portable_review",),
        "canonical": ("portable_review", "canonical_readiness"),
    }
    status = manifest.get("status")
    for kind in required_evidence_by_status.get(status, ()):
        if not has_evidence_kind(evidence, kind):
            issues.append(
                ValidationIssue(
                    location,
                    f"status '{status}' requires an evidence entry with kind '{kind}'",
                )
            )

    if status == "bounded":
        support_note_text = "\n".join(
            load_evidence_texts(bundle_dir, evidence, kind="support_note")
        )
        if not support_note_text:
            issues.append(
                ValidationIssue(
                    location,
                    "status 'bounded' requires an evidence entry with kind 'support_note'",
                )
            )
            return

        phrase_groups = (
            ("approve for bounded", "approve for bounded promotion"),
            ("readout",),
            ("failure",),
        )
        if not all(contains_phrase_group(support_note_text, group) for group in phrase_groups):
            issues.append(
                ValidationIssue(
                    location,
                    "status 'bounded' requires a support_note that records approve-for-bounded outcome plus failure and readout distinctions",
                )
            )


def validate_comparative_summary_contract(
    manifest: dict[str, Any],
    bundle_dir: Path,
    location: str,
    evidence: Sequence[dict[str, Any]],
    issues: list[ValidationIssue],
) -> None:
    if manifest.get("report_format") != "comparative-summary":
        return

    if not has_evidence_kind(evidence, "support_note"):
        issues.append(
            ValidationIssue(
                location,
                "report_format 'comparative-summary' requires an evidence entry with kind 'support_note'",
            )
        )
        return

    support_note_text = "\n".join(
        load_evidence_texts(bundle_dir, evidence, kind="support_note")
    )
    baseline_mode = manifest.get("baseline_mode")

    if baseline_mode in {"fixed-baseline", "previous-version"}:
        phrase_groups = (
            ("baseline",),
            ("noisy variation",),
            ("style-only", "style only"),
        )
        if not all(contains_phrase_group(support_note_text, group) for group in phrase_groups):
            issues.append(
                ValidationIssue(
                    location,
                    f"comparative-summary bundle with baseline_mode '{baseline_mode}' must state the baseline target, noisy variation, and style-only overread limits in a support note",
                )
            )
    elif baseline_mode == "peer-compare":
        phrase_groups = (
            ("matched",),
            ("side-by-side", "side by side"),
        )
        if not all(contains_phrase_group(support_note_text, group) for group in phrase_groups):
            issues.append(
                ValidationIssue(
                    location,
                    "comparative-summary bundle with baseline_mode 'peer-compare' must state matched conditions and side-by-side interpretation limits in a support note",
                )
            )
    elif baseline_mode == "longitudinal-window":
        phrase_groups = (
            ("ordered",),
            ("window",),
            ("same bounded workflow surface", "anchor workflow surface"),
            ("no clear directional movement", "mixed or unstable movement"),
        )
        if not all(contains_phrase_group(support_note_text, group) for group in phrase_groups):
            issues.append(
                ValidationIssue(
                    location,
                    "comparative-summary bundle with baseline_mode 'longitudinal-window' must state ordered windows, cross-window invariants, and cautious movement interpretation in a support note",
                )
            )


def extract_bulleted_eval_names(text: str, label: str) -> list[str]:
    lines = text.splitlines()
    names: list[str] = []
    for index, line in enumerate(lines):
        if line.strip() != label:
            continue
        for candidate in lines[index + 1 :]:
            stripped = candidate.strip()
            if not stripped:
                break
            if not stripped.startswith("- "):
                break
            names.extend(re.findall(r"aoa-[a-z0-9-]+", stripped))
    return names


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
    sections: dict[str, str],
    eval_md_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(eval_md_path)
    contract_issues = eval_section_contract.collect_section_contract_issues(
        sections,
        location=location,
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in contract_issues
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

    validate_status_specific_evidence(manifest, bundle_dir, location, evidence, issues)
    validate_comparative_summary_contract(
        manifest,
        bundle_dir,
        location,
        evidence,
        issues,
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
    sections: dict[str, str] = {}
    frontmatter_valid = False
    manifest_valid = False

    if eval_md_path.is_file():
        metadata, sections = parse_eval_markdown(eval_md_path, issues)
        if metadata is not None:
            frontmatter_valid = validate_eval_frontmatter(eval_name, metadata, eval_md_path, issues)
            validate_eval_headings(sections, eval_md_path, issues)
            capsule_source_issues = eval_capsule_contract.validate_capsule_source_sections(
                sections,
                eval_md_path,
                repo_root,
            )
            issues.extend(
                ValidationIssue(issue.location, issue.message)
                for issue in capsule_source_issues
            )

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
            sections=sections,
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

        has_origin_need = any(
            item.get("kind") == "origin_need" for item in evidence
        )
        if not has_origin_need:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    "starter bundle must include an evidence entry with kind 'origin_need'",
                )
            )

    return issues


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
    starter_set = set(starter_names)
    bundle_names = {
        path.name
        for path in (repo_root / BUNDLES_DIR_NAME).iterdir()
        if path.is_dir()
    }
    current_public_surface_names = set(
        extract_bulleted_eval_names(roadmap_text, "Current public surface:")
    )
    names_to_check = current_public_surface_names
    if selected_evals is not None:
        names_to_check = current_public_surface_names.intersection(selected_evals)

    issues: list[ValidationIssue] = []
    for name in sorted(names_to_check):
        if name not in bundle_names:
            issues.append(
                ValidationIssue(
                    location,
                    f"roadmap 'Current public surface' eval '{name}' has no matching bundle directory",
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
    return eval_catalog_contract.full_catalog_entry(repo_root, record)


def project_min_catalog(full_catalog: dict[str, Any]) -> dict[str, Any]:
    return eval_catalog_contract.project_min_catalog(full_catalog)


def project_min_catalog_safely(
    full_catalog: dict[str, Any],
    *,
    location: str,
    label: str,
    issues: list[ValidationIssue],
) -> dict[str, Any] | None:
    try:
        return project_min_catalog(full_catalog)
    except (KeyError, TypeError):
        issues.append(
            ValidationIssue(
                location,
                f"{label} is malformed; min projection could not be computed",
            )
        )
        return None


def validate_catalog_metadata(
    actual_catalog: dict[str, Any],
    expected_catalog: dict[str, Any],
    *,
    location: str,
    label: str,
    issues: list[ValidationIssue],
) -> None:
    if (
        actual_catalog.get("catalog_version") != expected_catalog["catalog_version"]
        or actual_catalog.get("source_of_truth") != expected_catalog["source_of_truth"]
    ):
        issues.append(
            ValidationIssue(
                location,
                f"{label} metadata is out of date; run 'python scripts/build_catalog.py'",
            )
        )


def build_catalog_payloads(
    repo_root: Path,
    records: list[EvalBundleRecord],
) -> tuple[dict[str, Any], dict[str, Any]]:
    return eval_catalog_contract.build_catalog_payloads(repo_root, records)


def build_capsule_payload(
    repo_root: Path,
    records: list[EvalBundleRecord],
    full_catalog: dict[str, Any],
) -> dict[str, Any]:
    return eval_capsule_contract.build_capsule_payload(repo_root, records, full_catalog)


def read_json_file(path: Path, issues: list[ValidationIssue], repo_root: Path) -> Any | None:
    payload, contract_issues = eval_catalog_contract.read_json_file(path, repo_root)
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in contract_issues
    )
    return payload


def write_json_file(path: Path, payload: Any, compact: bool = False) -> None:
    eval_catalog_contract.write_json_file(path, payload, compact=compact)


def validate_generated_catalogs(
    repo_root: Path,
    records: list[EvalBundleRecord],
    target_eval_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    full_path = repo_root / GENERATED_DIR_NAME / FULL_CATALOG_NAME
    min_path = repo_root / GENERATED_DIR_NAME / MIN_CATALOG_NAME

    expected_full, expected_min = build_catalog_payloads(repo_root, records)
    actual_full = read_json_file(full_path, issues, repo_root)
    actual_min = read_json_file(min_path, issues, repo_root)

    if actual_full is None or actual_min is None:
        return issues

    full_location = relative_location(full_path, repo_root)
    min_location = relative_location(min_path, repo_root)
    if target_eval_names is None:
        if actual_full != expected_full:
            issues.append(
                ValidationIssue(
                    full_location,
                    "generated catalog is out of date; run 'python scripts/build_catalog.py'",
                )
            )
        if actual_min != expected_min:
            issues.append(
                ValidationIssue(
                    min_location,
                    "generated min catalog is out of date; run 'python scripts/build_catalog.py'",
                )
            )

        projected_min = project_min_catalog_safely(
            actual_full,
            location=full_location,
            label="generated catalog",
            issues=issues,
        )
        if projected_min is None:
            return issues
        if actual_min != projected_min:
            issues.append(
                ValidationIssue(
                    min_location,
                    "min catalog must stay a projection of the full catalog",
                )
            )
        return issues

    validate_catalog_metadata(
        actual_full,
        expected_full,
        location=full_location,
        label="generated catalog",
        issues=issues,
    )
    validate_catalog_metadata(
        actual_min,
        expected_min,
        location=min_location,
        label="generated min catalog",
        issues=issues,
    )

    full_entries, full_entry_issues = eval_catalog_contract.catalog_entries_by_name(
        actual_full,
        array_key="evals",
        key_name="name",
        location=full_location,
    )
    min_entries, min_entry_issues = eval_catalog_contract.catalog_entries_by_name(
        actual_min,
        array_key="evals",
        key_name="name",
        location=min_location,
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in full_entry_issues + min_entry_issues
    )

    expected_full_entries = {
        record.name: full_catalog_entry(repo_root, record)
        for record in records
    }
    expected_min_entries = {
        name: project_min_catalog(
            {
                "catalog_version": CATALOG_VERSION,
                "source_of_truth": CATALOG_SOURCE_OF_TRUTH,
                "evals": [entry],
            }
        )["evals"][0]
        for name, entry in expected_full_entries.items()
    }

    for eval_name in target_eval_names:
        actual_full_entry = full_entries.get(eval_name)
        actual_min_entry = min_entries.get(eval_name)
        if actual_full_entry is None:
            issues.append(
                ValidationIssue(
                    full_location,
                    f"generated catalog is missing eval '{eval_name}'",
                )
            )
            continue
        if actual_min_entry is None:
            issues.append(
                ValidationIssue(
                    min_location,
                    f"generated min catalog is missing eval '{eval_name}'",
                )
            )
            continue

        expected_full_entry = expected_full_entries[eval_name]
        expected_min_entry = expected_min_entries[eval_name]
        if actual_full_entry != expected_full_entry:
            issues.append(
                ValidationIssue(
                    full_location,
                    f"generated catalog entry for '{eval_name}' is out of date; run 'python scripts/build_catalog.py'",
                )
            )
        if actual_min_entry != expected_min_entry:
            issues.append(
                ValidationIssue(
                    min_location,
                    f"generated min catalog entry for '{eval_name}' is out of date; run 'python scripts/build_catalog.py'",
                )
            )

        projected_min_catalog_payload = project_min_catalog_safely(
            {
                "catalog_version": actual_full.get("catalog_version"),
                "source_of_truth": actual_full.get("source_of_truth"),
                "evals": [actual_full_entry],
            },
            location=full_location,
            label=f"generated catalog entry for '{eval_name}'",
            issues=issues,
        )
        if projected_min_catalog_payload is None:
            continue
        projected_min_entry = projected_min_catalog_payload["evals"][0]
        if actual_min_entry != projected_min_entry:
            issues.append(
                ValidationIssue(
                    min_location,
                    f"generated min catalog entry for '{eval_name}' must stay a projection of the full catalog",
                )
            )

    return issues


def validate_generated_capsules(
    repo_root: Path,
    records: list[EvalBundleRecord],
    target_eval_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    full_path = repo_root / GENERATED_DIR_NAME / FULL_CATALOG_NAME
    capsule_path = repo_root / GENERATED_DIR_NAME / CAPSULE_NAME
    capsule_location = relative_location(capsule_path, repo_root)

    expected_full, _expected_min = build_catalog_payloads(repo_root, records)
    expected_capsules = build_capsule_payload(repo_root, records, expected_full)
    actual_capsules = read_json_file(capsule_path, issues, repo_root)
    if actual_capsules is None:
        return issues

    if not isinstance(actual_capsules, dict):
        issues.append(
            ValidationIssue(capsule_location, "generated capsules payload must be an object")
        )
        return issues

    if actual_capsules.get("capsule_version") != CAPSULE_VERSION:
        issues.append(
            ValidationIssue(capsule_location, f"capsule_version must be {CAPSULE_VERSION}")
        )
    if actual_capsules.get("source_of_truth") != CAPSULE_SOURCE_OF_TRUTH:
        issues.append(
            ValidationIssue(capsule_location, "source_of_truth does not match the capsule contract")
        )

    if target_eval_names is None:
        if actual_capsules != expected_capsules:
            issues.append(
                ValidationIssue(
                    capsule_location,
                    "generated capsules are out of date; run 'python scripts/build_catalog.py'",
                )
            )
    else:
        expected_entries, expected_entry_issues = eval_catalog_contract.catalog_entries_by_name(
            expected_capsules,
            array_key="evals",
            key_name="name",
            location=capsule_location,
        )
        actual_entries, actual_entry_issues = eval_catalog_contract.catalog_entries_by_name(
            actual_capsules,
            array_key="evals",
            key_name="name",
            location=capsule_location,
        )
        issues.extend(
            ValidationIssue(issue.location, issue.message)
            for issue in expected_entry_issues + actual_entry_issues
        )
        for eval_name in target_eval_names:
            actual_entry = actual_entries.get(eval_name)
            if actual_entry is None:
                issues.append(
                    ValidationIssue(
                        capsule_location,
                        f"generated capsules are missing eval '{eval_name}'",
                    )
                )
                continue
            if actual_entry != expected_entries[eval_name]:
                issues.append(
                    ValidationIssue(
                        capsule_location,
                        f"generated capsule entry for '{eval_name}' is out of date; run 'python scripts/build_catalog.py'",
                    )
                )

    alignment_issues: list[ValidationIssue] = []
    actual_full = read_json_file(full_path, alignment_issues, repo_root)
    issues.extend(alignment_issues)
    if isinstance(actual_full, dict):
        contract_issues = eval_capsule_contract.validate_capsule_alignment(
            actual_full,
            actual_capsules,
            location=capsule_location,
            target_eval_names=set(target_eval_names) if target_eval_names is not None else None,
        )
        issues.extend(
            ValidationIssue(issue.location, issue.message)
            for issue in contract_issues
        )

    return issues


def validate_generated_sections(
    repo_root: Path,
    records: list[EvalBundleRecord],
    target_eval_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    full_path = repo_root / GENERATED_DIR_NAME / FULL_CATALOG_NAME
    sections_path = repo_root / GENERATED_DIR_NAME / SECTION_NAME
    sections_location = relative_location(sections_path, repo_root)

    expected_sections, section_contract_issues = eval_section_contract.build_sections_payload(
        repo_root,
        records,
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in section_contract_issues
    )
    if section_contract_issues:
        return issues

    actual_sections = read_json_file(sections_path, issues, repo_root)
    if actual_sections is None:
        return issues
    if not isinstance(actual_sections, dict):
        issues.append(
            ValidationIssue(sections_location, "generated sections payload must be an object")
        )
        return issues

    if actual_sections.get("section_version") != SECTION_VERSION:
        issues.append(
            ValidationIssue(sections_location, f"section_version must be {SECTION_VERSION}")
        )
    if actual_sections.get("source_of_truth") != SECTION_SOURCE_OF_TRUTH:
        issues.append(
            ValidationIssue(sections_location, "source_of_truth does not match the section contract")
        )

    if target_eval_names is None:
        if actual_sections != expected_sections:
            issues.append(
                ValidationIssue(
                    sections_location,
                    "generated sections are out of date; run 'python scripts/build_catalog.py'",
                )
            )
    else:
        expected_entries, expected_entry_issues = eval_catalog_contract.catalog_entries_by_name(
            expected_sections,
            array_key="evals",
            key_name="name",
            location=sections_location,
        )
        actual_entries, actual_entry_issues = eval_catalog_contract.catalog_entries_by_name(
            actual_sections,
            array_key="evals",
            key_name="name",
            location=sections_location,
        )
        issues.extend(
            ValidationIssue(issue.location, issue.message)
            for issue in expected_entry_issues + actual_entry_issues
        )
        for eval_name in target_eval_names:
            actual_entry = actual_entries.get(eval_name)
            if actual_entry is None:
                issues.append(
                    ValidationIssue(
                        sections_location,
                        f"generated sections are missing eval '{eval_name}'",
                    )
                )
                continue
            if actual_entry != expected_entries[eval_name]:
                issues.append(
                    ValidationIssue(
                        sections_location,
                        f"generated section entry for '{eval_name}' is out of date; run 'python scripts/build_catalog.py'",
                    )
                )

    actual_full = read_json_file(full_path, issues, repo_root)
    if not isinstance(actual_full, dict):
        return issues

    catalog_entries, catalog_entry_issues = eval_catalog_contract.catalog_entries_by_name(
        actual_full,
        array_key="evals",
        key_name="name",
        location=relative_location(full_path, repo_root),
    )
    section_entries, section_entry_issues = eval_catalog_contract.catalog_entries_by_name(
        actual_sections,
        array_key="evals",
        key_name="name",
        location=sections_location,
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in catalog_entry_issues + section_entry_issues
    )
    if catalog_entry_issues or section_entry_issues:
        return issues

    catalog_names = set(catalog_entries)
    section_names = set(section_entries)
    if target_eval_names is not None:
        target_name_set = set(target_eval_names)
        catalog_names &= target_name_set
        section_names &= target_name_set

    for missing in sorted(catalog_names - section_names):
        issues.append(
            ValidationIssue(
                sections_location,
                f"generated sections are missing eval '{missing}' from generated/eval_catalog.json",
            )
        )
    for extra in sorted(section_names - catalog_names):
        issues.append(
            ValidationIssue(
                sections_location,
                f"generated sections include unknown eval '{extra}' from generated/eval_catalog.json",
            )
        )

    for eval_name in sorted(catalog_names & section_names):
        catalog_entry = catalog_entries[eval_name]
        section_entry = section_entries[eval_name]
        for field_name in ("category", "status", "verdict_shape", "eval_path"):
            if section_entry.get(field_name) != catalog_entry.get(field_name):
                issues.append(
                    ValidationIssue(
                        sections_location,
                        f"generated section entry for '{eval_name}' must align with full catalog field '{field_name}'",
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
    issues.extend(
        validate_roadmap_parity(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_evals,
        )
    )

    if eval_name is None and not source_issues:
        all_source_issues, all_records = collect_catalog_records(repo_root)
        if not all_source_issues:
            issues.extend(validate_generated_catalogs(repo_root, all_records))
            issues.extend(validate_generated_capsules(repo_root, all_records))
            issues.extend(validate_generated_sections(repo_root, all_records))
    elif eval_name is not None and not source_issues:
        issues.extend(
            validate_generated_catalogs(
                repo_root,
                records,
                target_eval_names=target_evals,
            )
        )
        issues.extend(
            validate_generated_capsules(
                repo_root,
                records,
                target_eval_names=target_evals,
            )
        )
        issues.extend(
            validate_generated_sections(
                repo_root,
                records,
                target_eval_names=target_evals,
            )
        )

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
