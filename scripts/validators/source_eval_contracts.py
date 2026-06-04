"""Source eval proof-object contract validation."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml
from jsonschema import Draft202012Validator, SchemaError

import eval_catalog_contract
import eval_capsule_contract
import eval_comparison_spine_contract
import eval_proof_contract_helpers
import eval_section_contract
from validators import proof_infra as proof_infra_validator
from validators.common import ValidationIssue


CONTRACT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_EVALS_DIR_NAME = "evals"
SCHEMAS_DIR_NAME = "schemas"
EVAL_FRONTMATTER_SCHEMA_NAME = (
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json"
)
EVAL_MANIFEST_SCHEMA_NAME = (
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json"
)
COMPARISON_FAMILY_BY_BASELINE_MODE = {
    "fixed-baseline": ("comparison", "fixed-baseline"),
    "peer-compare": ("comparison", "peer-compare"),
    "longitudinal-window": ("comparison", "longitudinal-window"),
}
MIRRORED_FIELDS = (
    "name",
    "category",
    "status",
    "object_under_evaluation",
    "claim_type",
    "baseline_mode",
    "report_format",
    "comparison_surface",
)
COMPARISON_SURFACE_COMMON_KEYS = (
    "shared_family_path",
    "paired_readout_path",
    "integrity_sidecar",
    "selection_question",
)
COMPARISON_SURFACE_ALLOWED_KEYS = {
    "fixed-baseline": set(
        COMPARISON_SURFACE_COMMON_KEYS + ("anchor_surface", "baseline_target_label")
    ),
    "previous-version": set(
        COMPARISON_SURFACE_COMMON_KEYS + ("anchor_surface", "baseline_target_label")
    ),
    "peer-compare": set(
        COMPARISON_SURFACE_COMMON_KEYS + ("peer_surfaces", "matched_surface")
    ),
    "longitudinal-window": set(
        COMPARISON_SURFACE_COMMON_KEYS + ("anchor_surface", "window_family_label")
    ),
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
    schema_candidate = Path(schema_name)
    schema_relative_path = (
        schema_candidate
        if schema_candidate.parent != Path(".")
        else Path(SCHEMAS_DIR_NAME) / schema_candidate
    )
    with (CONTRACT_ROOT / schema_relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=None)
def get_schema_validator(schema_name: str) -> Draft202012Validator:
    return Draft202012Validator(load_schema(schema_name))


def relative_location(path: Path, root: Path | None = None) -> str:
    target_root = root or CONTRACT_ROOT
    try:
        return path.relative_to(target_root).as_posix()
    except ValueError:
        return path.as_posix()


def markdown_python_commands(section: str) -> list[str]:
    commands: list[str] = []
    commands.extend(re.findall(r"`(python3? [^`]+)`", section))
    in_fence = False
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("$ "):
            stripped = stripped[2:].strip()
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()
        if stripped.startswith("python ") or stripped.startswith("python3 "):
            commands.append(stripped)
    return list(dict.fromkeys(commands))


def validate_source_eval_command_ownership(
    repo_root: Path,
    records: Sequence[EvalBundleRecord],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for record in records:
        path_name = relative_location(record.eval_md_path, repo_root)
        try:
            text = record.eval_md_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            issues.append(ValidationIssue(path_name, "file is missing"))
            continue
        if markdown_python_commands(text):
            issues.append(
                ValidationIssue(
                    path_name,
                    "source EVAL.md must route executable validation commands to evals/AGENTS.md or the nearest AGENTS.md",
                )
            )

    return issues


def format_schema_path(path_parts: Sequence[Any]) -> str:
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


def format_issues(issues: Sequence[ValidationIssue]) -> str:
    return "\n".join(f"- {issue.location}: {issue.message}" for issue in issues)


def validate_against_schema(
    data: Any,
    schema_name: str,
    location: str,
    issues: list[ValidationIssue],
    *,
    validator: Draft202012Validator | None = None,
) -> bool:
    active_validator = validator or get_schema_validator(schema_name)
    schema_errors = sorted(
        active_validator.iter_errors(data),
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


def load_json_payload(path: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path), "file is missing"))
        return None
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(relative_location(path), f"invalid JSON: {exc}"))
        return None


def validate_inline_schema(
    schema: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> bool:
    if not isinstance(schema, dict):
        issues.append(ValidationIssue(location, "schema must parse to an object"))
        return False
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        issues.append(ValidationIssue(location, f"invalid JSON schema: {exc.message}"))
        return False
    return True

def validate_json_against_inline_schema(
    data: Any,
    schema: dict[str, Any],
    *,
    location: str,
    issues: list[ValidationIssue],
) -> bool:
    validator = Draft202012Validator(schema)
    schema_errors = sorted(
        validator.iter_errors(data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    for error in schema_errors:
        error_path = format_schema_path(error.absolute_path)
        if error_path:
            message = f"report violation at '{error_path}': {error.message}"
        else:
            message = f"report violation: {error.message}"
        issues.append(ValidationIssue(location, message))
    return not schema_errors


def requires_materialized_comparison_artifacts(manifest: dict[str, Any] | None) -> bool:
    if not isinstance(manifest, dict):
        return False
    return (
        manifest.get("report_format") == "comparative-summary"
        and manifest.get("baseline_mode") != "none"
    )


def validate_repo_relative_contract_path(
    repo_root: Path,
    raw_path: str,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> str | None:
    normalized_path = ensure_repo_relative_path(raw_path, location, issues)
    if not normalized_path:
        return None
    resolved_path = repo_root / normalized_path
    if not resolved_path.exists():
        issues.append(
            ValidationIssue(
                location,
                f"path '{normalized_path}' does not exist",
            )
        )
        return None
    return normalized_path


def validate_raw_repo_relative_path(
    raw_value: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> str | None:
    if not isinstance(raw_value, str):
        return None
    normalized_path = ensure_repo_relative_path(raw_value, location, issues)
    return normalized_path or None


def validate_raw_repo_relative_path_list(
    payload: dict[str, Any],
    key: str,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> list[str]:
    raw_values = payload.get(key, [])
    if not isinstance(raw_values, list):
        return []

    normalized_paths: list[str] = []
    for index, raw_value in enumerate(raw_values):
        normalized_path = validate_raw_repo_relative_path(
            raw_value,
            location=f"{location}.{key}[{index}]",
            issues=issues,
        )
        if normalized_path is not None:
            normalized_paths.append(normalized_path)
    return normalized_paths


def validate_comparison_eval_target(
    raw_name: Any,
    *,
    location: str,
    known_eval_names: set[str],
    issues: list[ValidationIssue],
) -> str | None:
    if not isinstance(raw_name, str) or not raw_name:
        issues.append(
            ValidationIssue(location, "comparison target must be a non-empty eval name")
        )
        return None
    if raw_name not in known_eval_names:
        issues.append(
            ValidationIssue(location, f"comparison target '{raw_name}' does not exist")
        )
        return None
    return raw_name


def validate_comparison_surface_contract(
    repo_root: Path,
    bundle_dir: Path,
    manifest: dict[str, Any],
    *,
    known_eval_names: set[str],
    issues: list[ValidationIssue],
) -> None:
    baseline_mode = manifest.get("baseline_mode")
    if baseline_mode == "none":
        return

    location = relative_location(bundle_dir / "eval.yaml", repo_root)
    comparison_surface = manifest.get("comparison_surface")
    if not isinstance(comparison_surface, dict):
        issues.append(
            ValidationIssue(
                location,
                "comparison bundle must define comparison_surface in eval.yaml",
            )
        )
        return

    allowed_keys = COMPARISON_SURFACE_ALLOWED_KEYS.get(baseline_mode, set())
    unexpected_keys = sorted(set(comparison_surface) - allowed_keys)
    if unexpected_keys:
        issues.append(
            ValidationIssue(
                location,
                f"comparison_surface has unexpected keys for baseline_mode '{baseline_mode}': {', '.join(unexpected_keys)}",
            )
        )

    shared_family_path = comparison_surface.get("shared_family_path")
    normalized_shared_family_path = None
    if isinstance(shared_family_path, str):
        normalized_shared_family_path = validate_repo_relative_contract_path(
            repo_root,
            shared_family_path,
            location=f"{location}.comparison_surface.shared_family_path",
            issues=issues,
        )

    paired_readout_path = comparison_surface.get("paired_readout_path")
    normalized_paired_readout_path = None
    if isinstance(paired_readout_path, str):
        normalized_paired_readout_path = validate_repo_relative_contract_path(
            repo_root,
            paired_readout_path,
            location=f"{location}.comparison_surface.paired_readout_path",
            issues=issues,
        )

    integrity_sidecar = comparison_surface.get("integrity_sidecar")
    validate_comparison_eval_target(
        integrity_sidecar,
        location=f"{location}.comparison_surface.integrity_sidecar",
        known_eval_names=known_eval_names,
        issues=issues,
    )

    if baseline_mode in {"fixed-baseline", "previous-version", "longitudinal-window"}:
        validate_comparison_eval_target(
            comparison_surface.get("anchor_surface"),
            location=f"{location}.comparison_surface.anchor_surface",
            known_eval_names=known_eval_names,
            issues=issues,
        )

    if baseline_mode == "peer-compare":
        raw_peer_surfaces = comparison_surface.get("peer_surfaces")
        if not isinstance(raw_peer_surfaces, list):
            issues.append(
                ValidationIssue(
                    f"{location}.comparison_surface.peer_surfaces",
                    "peer_surfaces must be a list",
                )
            )
        else:
            for index, raw_name in enumerate(raw_peer_surfaces):
                validate_comparison_eval_target(
                    raw_name,
                    location=f"{location}.comparison_surface.peer_surfaces[{index}]",
                    known_eval_names=known_eval_names,
                    issues=issues,
                )

    fixture_contract_path = bundle_dir / "fixtures" / "contract.json"
    fixture_contract = eval_catalog_contract.load_optional_json(fixture_contract_path)
    if isinstance(fixture_contract, dict):
        fixture_family_paths = eval_proof_contract_helpers.collect_fixture_family_paths(
            fixture_contract
        )
        fixture_family_path = fixture_family_paths[0] if fixture_family_paths else None
        if (
            isinstance(fixture_family_path, str)
            and normalized_shared_family_path is not None
            and fixture_family_path.replace("\\", "/") != normalized_shared_family_path
        ):
            issues.append(
                ValidationIssue(
                    location,
                    "comparison_surface.shared_family_path must match fixtures/contract.json shared_fixture_family_path",
                )
            )

    runner_contract_path = bundle_dir / "runners" / "contract.json"
    runner_contract = eval_catalog_contract.load_optional_json(runner_contract_path)
    if isinstance(runner_contract, dict):
        paired_readout_paths = eval_proof_contract_helpers.collect_paired_readout_paths(
            runner_contract
        )
        runner_paired_readout_path = paired_readout_paths[0] if paired_readout_paths else None
        if (
            isinstance(runner_paired_readout_path, str)
            and normalized_paired_readout_path is not None
            and runner_paired_readout_path.replace("\\", "/") != normalized_paired_readout_path
        ):
            issues.append(
                ValidationIssue(
                    location,
                    "comparison_surface.paired_readout_path must match runners/contract.json paired_readout_path",
                )
            )


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


def validate_status_portability_monotonicity(
    manifest: dict[str, Any],
    location: str,
    issues: list[ValidationIssue],
) -> None:
    required_portability_by_status = {
        "draft": "local-shaped",
        "bounded": "local-shaped",
        "portable": "portable",
        "baseline": "portable",
        "canonical": "broad",
    }
    status = manifest.get("status")
    portability_level = manifest.get("portability_level")
    required_portability = required_portability_by_status.get(status)
    if required_portability is None:
        return
    if portability_level != required_portability:
        issues.append(
            ValidationIssue(
                location,
                f"status '{status}' requires portability_level '{required_portability}' but found '{portability_level}'",
            )
        )


def validate_public_safety_reviewed_at(
    manifest: dict[str, Any],
    location: str,
    issues: list[ValidationIssue],
) -> None:
    status = manifest.get("status")
    raw_value = manifest.get("public_safety_reviewed_at")
    if raw_value is None:
        if status == "canonical":
            issues.append(
                ValidationIssue(
                    location,
                    "status 'canonical' requires public_safety_reviewed_at with a fresh YYYY-MM-DD review date",
                )
            )
        return

    if not isinstance(raw_value, str) or not raw_value:
        issues.append(
            ValidationIssue(
                location,
                "public_safety_reviewed_at must be a non-empty string",
            )
        )
        return

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw_value):
        issues.append(
            ValidationIssue(
                location,
                "public_safety_reviewed_at must use YYYY-MM-DD format",
            )
        )
        return

    try:
        reviewed_date = date.fromisoformat(raw_value)
    except ValueError:
        issues.append(
            ValidationIssue(
                location,
                "public_safety_reviewed_at must be a valid calendar date",
            )
        )
        return
    if reviewed_date > date.today():
        issues.append(
            ValidationIssue(
                location,
                "public_safety_reviewed_at must not be in the future",
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


def validate_eval_frontmatter(
    eval_name: str,
    metadata: dict[str, Any],
    eval_md_path: Path,
    issues: list[ValidationIssue],
) -> bool:
    location = relative_location(eval_md_path)
    valid = validate_against_schema(metadata, EVAL_FRONTMATTER_SCHEMA_NAME, location, issues)
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
    section_pairs, pair_issues = eval_section_contract.extract_section_pairs(
        eval_md_path,
        location=location,
    )
    contract_issues = eval_section_contract.collect_section_contract_issues(
        section_pairs or list(sections.items()),
        location=location,
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in [*pair_issues, *contract_issues]
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

    valid = validate_against_schema(manifest, EVAL_MANIFEST_SCHEMA_NAME, location, issues)
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

    validate_status_portability_monotonicity(manifest, location, issues)
    validate_status_specific_evidence(manifest, bundle_dir, location, evidence, issues)
    validate_public_safety_reviewed_at(manifest, location, issues)
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


def validate_bundle_report_artifacts(
    repo_root: Path,
    bundle_dir: Path,
    manifest: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    schema_path = bundle_dir / "reports" / "summary.schema.json"
    example_path = bundle_dir / "reports" / "example-report.json"
    has_schema = schema_path.is_file()
    has_example = example_path.is_file()
    required_mode = manifest.get("baseline_mode") if isinstance(manifest, dict) else None
    requires_materialized = requires_materialized_comparison_artifacts(manifest)

    if has_schema and not has_example:
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                "bundle-local report schema exists but reports/example-report.json is missing",
            )
        )
    elif requires_materialized and not has_example:
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                f"comparative-summary bundle with baseline_mode '{required_mode}' must ship reports/example-report.json",
            )
        )

    if has_example and not has_schema:
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                "bundle-local report example exists but reports/summary.schema.json is missing",
            )
        )
    elif requires_materialized and not has_schema:
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                f"comparative-summary bundle with baseline_mode '{required_mode}' must ship reports/summary.schema.json",
            )
        )

    if not has_schema or not has_example:
        return

    schema_location = relative_location(schema_path, repo_root)
    example_location = relative_location(example_path, repo_root)
    schema_issues: list[ValidationIssue] = []
    schema = load_json_payload(schema_path, schema_issues)
    issues.extend(schema_issues)
    if schema is None or not validate_inline_schema(
        schema,
        location=schema_location,
        issues=issues,
    ):
        return

    example_payload = load_json_payload(example_path, issues)
    if example_payload is None:
        return
    example_valid = validate_json_against_inline_schema(
        example_payload,
        schema,
        location=example_location,
        issues=issues,
    )
    if manifest is not None and manifest.get("report_format") == "comparative-summary":
        validate_comparative_report_mode_contract(
            schema,
            example_payload,
            required_mode=required_mode,
            schema_location=schema_location,
            example_location=example_location,
            issues=issues,
        )
    if example_valid and required_mode == "longitudinal-window":
        validate_longitudinal_report_example(
            example_payload,
            location=example_location,
            issues=issues,
        )

    for report_path in sorted(schema_path.parent.glob("*.report.json")):
        validate_actual_bundle_report_artifact(
            report_path,
            schema,
            repo_root=repo_root,
            manifest=manifest,
            issues=issues,
        )


def validate_actual_bundle_report_artifact(
    report_path: Path,
    schema: dict[str, Any],
    *,
    repo_root: Path,
    manifest: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    report_location = relative_location(report_path, repo_root)
    report_payload = load_json_payload(report_path, issues)
    if report_payload is None:
        return

    validate_json_against_inline_schema(
        report_payload,
        schema,
        location=report_location,
        issues=issues,
    )

    if not isinstance(report_payload, dict) or not isinstance(manifest, dict):
        return

    expected_name = manifest.get("name")
    if isinstance(expected_name, str) and report_payload.get("eval_name") != expected_name:
        issues.append(
            ValidationIssue(
                report_location,
                f"actual bundle report eval_name must match manifest name '{expected_name}'",
            )
        )

    expected_status = manifest.get("status")
    if isinstance(expected_status, str) and report_payload.get("bundle_status") != expected_status:
        issues.append(
            ValidationIssue(
                report_location,
                f"actual bundle report bundle_status must match manifest status '{expected_status}'",
            )
        )


LONGITUDINAL_GROWTH_CLAIM_PHRASES = (
    "broad capability growth",
    "general capability growth",
)
LONGITUDINAL_GROWTH_NEGATION_CUES = (
    "does not",
    "do not",
    "did not",
    "doesn't",
    "don't",
    "cannot",
    "can't",
    "is not",
    "isn't",
    "not prove",
    "not proven",
    "not support",
    "not supported",
    "not imply",
    "not implied",
    "without proving",
    "without implying",
)
LONGITUDINAL_GROWTH_POST_NEGATION_CUES = (
    "is not proven",
    "is not supported",
    "is not implied",
    "not proven",
    "not supported",
    "not implied",
)


def claim_boundary_overclaims_longitudinal_growth(claim_boundary: str) -> bool:
    clauses = [
        clause.strip()
        for clause in re.split(r"[.;:\n]+", claim_boundary.lower())
        if clause.strip()
    ]
    for clause in clauses:
        for phrase in LONGITUDINAL_GROWTH_CLAIM_PHRASES:
            if phrase not in clause:
                continue
            if clause_negates_longitudinal_growth_phrase(clause, phrase):
                continue
            return True
    return False


def clause_negates_longitudinal_growth_phrase(clause: str, phrase: str) -> bool:
    phrase_index = clause.find(phrase)
    if phrase_index == -1:
        return False

    for cue in LONGITUDINAL_GROWTH_NEGATION_CUES:
        cue_index = clause.find(cue)
        if cue_index == -1:
            continue
        if cue_index <= phrase_index <= cue_index + len(cue) + 80:
            return True

    trailing_window = clause[phrase_index : phrase_index + len(phrase) + 80]
    return any(cue in trailing_window for cue in LONGITUDINAL_GROWTH_POST_NEGATION_CUES)


def validate_longitudinal_report_example(
    example_payload: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(example_payload, dict):
        return

    claim_boundary = example_payload.get("claim_boundary")
    if isinstance(claim_boundary, str):
        if claim_boundary_overclaims_longitudinal_growth(claim_boundary):
            issues.append(
                ValidationIssue(
                    f"{location}.claim_boundary",
                    "longitudinal example report claim_boundary must stay weaker than broad or general capability growth",
                )
            )

    limitations = example_payload.get("limitations")
    if isinstance(limitations, list):
        lowered_limitations = [
            item.lower()
            for item in limitations
            if isinstance(item, str)
        ]
        if not any("general capability growth" in item for item in lowered_limitations):
            issues.append(
                ValidationIssue(
                    f"{location}.limitations",
                    "longitudinal example report limitations must name that the report does not prove general capability growth",
                )
            )

    windows = example_payload.get("windows")
    if not isinstance(windows, list):
        return

    seen_window_ids: set[str] = set()
    last_order: int | None = None
    for index, window in enumerate(windows):
        if not isinstance(window, dict):
            continue

        window_id = window.get("window_id")
        if isinstance(window_id, str):
            if window_id in seen_window_ids:
                issues.append(
                    ValidationIssue(
                        f"{location}.windows[{index}].window_id",
                        f"longitudinal example report window_id '{window_id}' must be unique",
                    )
                )
            seen_window_ids.add(window_id)

        window_order = window.get("window_order")
        if isinstance(window_order, int):
            if last_order is not None and window_order <= last_order:
                issues.append(
                    ValidationIssue(
                        f"{location}.windows[{index}].window_order",
                        "longitudinal example report window_order values must be strictly increasing",
                    )
                )
            last_order = window_order

        transition_note = window.get("transition_note")
        if index == 0 and transition_note is None:
            continue
        if not isinstance(transition_note, str) or not transition_note.strip():
            issues.append(
                ValidationIssue(
                    f"{location}.windows[{index}].transition_note",
                    "longitudinal example report non-initial windows must include a non-empty transition_note",
                )
            )


def validate_comparative_report_mode_contract(
    schema: dict[str, Any],
    example_payload: Any,
    *,
    required_mode: str | None,
    schema_location: str,
    example_location: str,
    issues: list[ValidationIssue],
) -> None:
    if required_mode is None:
        return

    required_fields = schema.get("required", [])
    if "comparison_mode" not in required_fields:
        issues.append(
            ValidationIssue(
                schema_location,
                "comparative-summary report schema must require 'comparison_mode'",
            )
        )
    properties = schema.get("properties", {})
    comparison_mode_schema = properties.get("comparison_mode")
    if not isinstance(comparison_mode_schema, dict) or comparison_mode_schema.get("const") != required_mode:
        issues.append(
            ValidationIssue(
                schema_location,
                f"comparative-summary report schema must pin comparison_mode to '{required_mode}'",
            )
        )

    if not isinstance(example_payload, dict):
        return
    if example_payload.get("comparison_mode") != required_mode:
        issues.append(
            ValidationIssue(
                example_location,
                f"comparative-summary report example must set comparison_mode to '{required_mode}'",
            )
        )


def validate_bundle_fixture_contract(
    repo_root: Path,
    bundle_dir: Path,
    manifest: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    contract_path = bundle_dir / "fixtures" / "contract.json"
    if not contract_path.is_file():
        if requires_materialized_comparison_artifacts(manifest):
            baseline_mode = manifest.get("baseline_mode") if isinstance(manifest, dict) else "unknown"
            issues.append(
                ValidationIssue(
                    relative_location(bundle_dir, repo_root),
                    f"comparative-summary bundle with baseline_mode '{baseline_mode}' must ship fixtures/contract.json",
                )
            )
        return

    location = relative_location(contract_path, repo_root)
    payload = load_json_payload(contract_path, issues)
    if payload is None:
        return
    if not validate_against_schema(payload, proof_infra_validator.FIXTURE_CONTRACT_SCHEMA_NAME, location, issues):
        return

    validate_raw_repo_relative_path(
        payload.get("shared_fixture_family_path"),
        location=f"{location}.shared_fixture_family_path",
        issues=issues,
    )
    validate_raw_repo_relative_path_list(
        payload,
        eval_proof_contract_helpers.ADDITIONAL_FIXTURE_FAMILY_PATHS_KEY,
        location=location,
        issues=issues,
    )
    fixture_family_paths = eval_proof_contract_helpers.collect_fixture_family_paths(payload)
    for index, shared_fixture_family_path in enumerate(fixture_family_paths):
        field_name = (
            "shared_fixture_family_path"
            if index == 0
            else f"{eval_proof_contract_helpers.ADDITIONAL_FIXTURE_FAMILY_PATHS_KEY}[{index - 1}]"
        )
        validate_repo_relative_contract_path(
            repo_root,
            shared_fixture_family_path,
            location=f"{location}.{field_name}",
            issues=issues,
        )


def validate_bundle_runner_contract(
    repo_root: Path,
    bundle_dir: Path,
    manifest: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    contract_path = bundle_dir / "runners" / "contract.json"
    if not contract_path.is_file():
        if requires_materialized_comparison_artifacts(manifest):
            baseline_mode = manifest.get("baseline_mode") if isinstance(manifest, dict) else "unknown"
            issues.append(
                ValidationIssue(
                    relative_location(bundle_dir, repo_root),
                    f"comparative-summary bundle with baseline_mode '{baseline_mode}' must ship runners/contract.json",
                )
            )
        return

    location = relative_location(contract_path, repo_root)
    payload = load_json_payload(contract_path, issues)
    if payload is None:
        return
    if not validate_against_schema(payload, proof_infra_validator.RUNNER_CONTRACT_SCHEMA_NAME, location, issues):
        return

    for field_name in ("runner_surface_path", "report_schema_path", "report_example_path", "paired_readout_path"):
        raw_value = payload.get(field_name)
        if isinstance(raw_value, str):
            validate_repo_relative_contract_path(
                repo_root,
                raw_value,
                location=f"{location}.{field_name}",
                issues=issues,
            )

    validate_raw_repo_relative_path_list(
        payload,
        eval_proof_contract_helpers.ADDITIONAL_PAIRED_READOUT_PATHS_KEY,
        location=location,
        issues=issues,
    )
    additional_paired_readout_paths = eval_proof_contract_helpers.normalize_repo_relative_path_list(
        payload,
        eval_proof_contract_helpers.ADDITIONAL_PAIRED_READOUT_PATHS_KEY,
    )
    for index, value in enumerate(additional_paired_readout_paths):
        validate_repo_relative_contract_path(
            repo_root,
            value,
            location=(
                f"{location}.{eval_proof_contract_helpers.ADDITIONAL_PAIRED_READOUT_PATHS_KEY}[{index}]"
            ),
            issues=issues,
        )

    for field_name in ("fixture_contract_paths", "scorer_helper_paths"):
        values = payload.get(field_name, [])
        if not isinstance(values, list):
            continue
        for index, value in enumerate(values):
            if not isinstance(value, str):
                continue
            validate_repo_relative_contract_path(
                repo_root,
                value,
                location=f"{location}.{field_name}[{index}]",
                issues=issues,
            )


def validate_bundle_proof_artifacts(
    repo_root: Path,
    bundle_dir: Path,
    manifest: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    validate_bundle_report_artifacts(repo_root, bundle_dir, manifest, issues)
    validate_bundle_fixture_contract(repo_root, bundle_dir, manifest, issues)
    validate_bundle_runner_contract(repo_root, bundle_dir, manifest, issues)


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


def validate_bundle(
    repo_root: Path,
    eval_name: str,
    known_eval_names: set[str],
    eval_dirs: Mapping[str, Path] | None = None,
    *,
    dependency_roots: Mapping[str, Path] | None = None,
) -> tuple[list[ValidationIssue], EvalBundleRecord | None]:
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
                validate_source_eval_tree_location(
                    repo_root,
                    bundle_dir,
                    eval_name,
                    manifest,
                    eval_yaml_path,
                    issues,
                )
                validate_manifest_evidence(manifest, bundle_dir, eval_yaml_path, issues)
                if manifest_valid:
                    validate_comparison_surface_contract(
                        repo_root,
                        bundle_dir,
                        manifest,
                        known_eval_names=known_eval_names,
                        issues=issues,
                    )

    validate_bundle_proof_artifacts(repo_root, bundle_dir, manifest, issues)

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
            dependency_roots=dependency_roots,
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
) -> tuple[list[ValidationIssue], list[EvalBundleRecord]]:
    eval_dirs = discover_eval_dirs(repo_root)
    all_eval_names = sorted(eval_dirs)
    selected_names = list(eval_names) if eval_names is not None else all_eval_names
    known_eval_names = set(all_eval_names)

    issues: list[ValidationIssue] = []
    records: list[EvalBundleRecord] = []
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


def full_catalog_entry(repo_root: Path, record: EvalBundleRecord) -> dict[str, Any]:
    return eval_catalog_contract.full_catalog_entry(repo_root, record)


def project_min_catalog(full_catalog: dict[str, Any]) -> dict[str, Any]:
    return eval_catalog_contract.project_min_catalog(full_catalog)


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


def build_comparison_spine_payload(
    repo_root: Path,
    records: list[EvalBundleRecord],
    full_catalog: dict[str, Any],
) -> dict[str, Any]:
    return eval_comparison_spine_contract.build_comparison_spine_payload(
        repo_root,
        records,
        full_catalog,
    )
