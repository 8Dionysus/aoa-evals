from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import eval_proof_contract_helpers


GENERATED_DIR_NAME = "generated"
FULL_CATALOG_NAME = "eval_catalog.json"
MIN_CATALOG_NAME = "eval_catalog.min.json"
CATALOG_VERSION = 1
CATALOG_SOURCE_OF_TRUTH = {
    "eval_markdown": "bundles/*/EVAL.md",
    "eval_manifest": "bundles/*/eval.yaml",
}
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
    "technique_refs",
    "skill_dependencies",
    "skill_refs",
    "evidence_kinds",
    "proof_surface_kinds",
    "eval_path",
)
KNOWN_REPOS = (
    "aoa-routing",
    "aoa-techniques",
    "aoa-skills",
    "aoa-evals",
    "aoa-memo",
)


@dataclass(frozen=True)
class ContractIssue:
    location: str
    message: str


def relative_location(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def format_issues(issues: list[ContractIssue]) -> str:
    return "\n".join(f"- {issue.location}: {issue.message}" for issue in issues)


def normalize_markdown_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n")
    normalized = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", normalized)
    normalized = re.sub(r"`([^`]+)`", r"\1", normalized)
    normalized = normalized.replace("**", "")
    normalized = normalized.replace("__", "")
    normalized = normalized.replace("*", "")
    normalized = normalized.replace("_", "")
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def trim_summary(
    text: str,
    *,
    max_words: int,
    max_chars: int,
) -> str:
    words = text.split()
    trimmed = " ".join(words[:max_words])
    if len(trimmed) > max_chars:
        trimmed = trimmed[: max_chars + 1].rsplit(" ", 1)[0].rstrip(" ,;:")
    if len(words) > max_words or len(text) > len(trimmed):
        return f"{trimmed}..."
    return trimmed


def collect_bullets_after_label(
    text: str,
    *,
    label_matcher: Any,
) -> list[str]:
    lines = text.splitlines()
    collecting = False
    bullets: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not collecting:
            if label_matcher(stripped):
                collecting = True
            continue

        if stripped.startswith("- "):
            bullets.append(normalize_markdown_text(stripped[2:]))
            continue
        if not stripped:
            if bullets:
                break
            continue
        if bullets:
            break
    return bullets


def extract_interpretation_limit_bullets(section_text: str) -> list[str]:
    return collect_bullets_after_label(
        section_text,
        label_matcher=lambda line: line.startswith("Do not treat ") and line.endswith(":"),
    )


def summarize_interpretation_limits(section_text: str) -> str:
    limits = extract_interpretation_limit_bullets(section_text)
    return trim_summary("; ".join(limits[:3]), max_words=28, max_chars=190)


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


def ensure_repo_relative_path(raw_path: str, location: str) -> tuple[str, list[ContractIssue]]:
    issues: list[ContractIssue] = []
    if not isinstance(raw_path, str) or not raw_path.strip():
        issues.append(ContractIssue(location, "path must be a non-empty string"))
        return "", issues

    value = raw_path.strip().replace("\\", "/")
    if not is_repo_relative_path(value):
        issues.append(
            ContractIssue(location, "path must be a concrete repo-relative path")
        )
    return value, issues


def normalize_technique_dependency_refs(
    manifest: dict[str, Any],
    eval_yaml_path: Path,
    repo_root: Path,
) -> tuple[list[dict[str, str]], list[ContractIssue]]:
    normalized: list[dict[str, str]] = []
    issues: list[ContractIssue] = []
    dependencies = manifest.get("technique_dependencies", [])
    for index, item in enumerate(dependencies):
        location = f"{relative_location(eval_yaml_path, repo_root)}.technique_dependencies[{index}]"
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
            issues.append(ContractIssue(location, str(exc)))
            repo_name = repo_raw

        if repo_name != "aoa-techniques":
            issues.append(
                ContractIssue(location, ".repo must resolve to 'aoa-techniques'")
            )

        normalized_path = ""
        if isinstance(raw_path, str):
            normalized_path, path_issues = ensure_repo_relative_path(
                raw_path,
                f"{location}.path",
            )
            issues.extend(path_issues)

        normalized.append(
            {
                "id": dependency_id,
                "repo": repo_name,
                "path": normalized_path,
            }
        )
    return normalized, issues


def normalize_skill_dependency_refs(
    manifest: dict[str, Any],
    eval_yaml_path: Path,
    repo_root: Path,
) -> tuple[list[dict[str, str]], list[ContractIssue]]:
    normalized: list[dict[str, str]] = []
    issues: list[ContractIssue] = []
    dependencies = manifest.get("skill_dependencies", [])
    for index, item in enumerate(dependencies):
        location = f"{relative_location(eval_yaml_path, repo_root)}.skill_dependencies[{index}]"
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
            issues.append(ContractIssue(location, str(exc)))
            repo_name = repo_raw

        if repo_name != "aoa-skills":
            issues.append(
                ContractIssue(location, ".repo must resolve to 'aoa-skills'")
            )

        normalized_path = ""
        if isinstance(raw_path, str):
            normalized_path, path_issues = ensure_repo_relative_path(
                raw_path,
                f"{location}.path",
            )
            issues.extend(path_issues)

        normalized.append(
            {
                "name": dependency_name,
                "repo": repo_name,
                "path": normalized_path,
            }
        )
    return normalized, issues


def load_optional_json(path: Path) -> Any | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def normalize_comparison_surface(manifest: dict[str, Any]) -> dict[str, Any] | None:
    comparison_surface = manifest.get("comparison_surface")
    if not isinstance(comparison_surface, dict):
        return None

    normalized: dict[str, Any] = {}
    for key, value in comparison_surface.items():
        if isinstance(value, str):
            normalized[key] = value.replace("\\", "/")
        elif isinstance(value, list):
            normalized[key] = [
                item.replace("\\", "/") if isinstance(item, str) else item
                for item in value
            ]
        else:
            normalized[key] = value
    return normalized


def build_proof_artifacts_entry(repo_root: Path, record: Any) -> dict[str, Any]:
    bundle_dir = record.bundle_dir
    fixture_contract_path = bundle_dir / "fixtures" / "contract.json"
    runner_contract_path = bundle_dir / "runners" / "contract.json"
    report_schema_path = bundle_dir / "reports" / "summary.schema.json"
    report_example_path = bundle_dir / "reports" / "example-report.json"

    fixture_contract = load_optional_json(fixture_contract_path)
    runner_contract = load_optional_json(runner_contract_path)

    shared_fixture_family_path = None
    fixture_family_paths = eval_proof_contract_helpers.collect_fixture_family_paths(
        fixture_contract if isinstance(fixture_contract, dict) else None
    )
    if fixture_family_paths:
        shared_fixture_family_path = fixture_family_paths[0]

    runner_surface_path = None
    scorer_helper_paths: list[str] = []
    paired_readout_path = None
    if isinstance(runner_contract, dict):
        raw_runner_surface_path = runner_contract.get("runner_surface_path")
        if isinstance(raw_runner_surface_path, str) and raw_runner_surface_path.strip():
            runner_surface_path = raw_runner_surface_path.replace("\\", "/")

        raw_scorer_paths = runner_contract.get("scorer_helper_paths", [])
        if isinstance(raw_scorer_paths, list):
            scorer_helper_paths = [
                path.replace("\\", "/")
                for path in raw_scorer_paths
                if isinstance(path, str) and path.strip()
            ]

        paired_readout_paths = eval_proof_contract_helpers.collect_paired_readout_paths(
            runner_contract
        )
        if paired_readout_paths:
            paired_readout_path = paired_readout_paths[0]

    return {
        "fixture_contract_path": relative_location(fixture_contract_path, repo_root)
        if fixture_contract_path.is_file()
        else None,
        "shared_fixture_family_path": shared_fixture_family_path,
        "runner_contract_path": relative_location(runner_contract_path, repo_root)
        if runner_contract_path.is_file()
        else None,
        "runner_surface_path": runner_surface_path,
        "scorer_helper_paths": scorer_helper_paths,
        "paired_readout_path": paired_readout_path,
        "report_schema_path": relative_location(report_schema_path, repo_root)
        if report_schema_path.is_file()
        else None,
        "report_example_path": relative_location(report_example_path, repo_root)
        if report_example_path.is_file()
        else None,
    }


def compact_evidence_kinds(evidence_entries: list[dict[str, Any]]) -> list[str]:
    kinds: list[str] = []
    for entry in evidence_entries:
        kind = entry.get("kind")
        if isinstance(kind, str) and kind not in kinds:
            kinds.append(kind)
    return kinds


def compact_proof_surface_kinds(proof_artifacts: dict[str, Any]) -> list[str]:
    kinds: list[str] = []
    if proof_artifacts.get("fixture_contract_path"):
        kinds.append("fixture_contract")
    if proof_artifacts.get("shared_fixture_family_path"):
        kinds.append("shared_fixture_family")
    if proof_artifacts.get("runner_contract_path"):
        kinds.append("runner_contract")
    if proof_artifacts.get("scorer_helper_paths"):
        kinds.append("scorer_helper")
    if proof_artifacts.get("report_schema_path"):
        kinds.append("report_schema")
    if proof_artifacts.get("paired_readout_path"):
        kinds.append("paired_readout")
    return kinds


def full_catalog_entry(repo_root: Path, record: Any) -> dict[str, Any]:
    metadata = record.metadata
    manifest = record.manifest
    technique_refs, technique_issues = normalize_technique_dependency_refs(
        manifest,
        record.eval_yaml_path,
        repo_root,
    )
    skill_refs, skill_issues = normalize_skill_dependency_refs(
        manifest,
        record.eval_yaml_path,
        repo_root,
    )
    if technique_issues or skill_issues:
        raise ValueError(format_issues(technique_issues + skill_issues))

    evidence_entries = list(manifest["evidence"])
    proof_artifacts = build_proof_artifacts_entry(repo_root, record)
    comparison_surface = normalize_comparison_surface(manifest)
    selection_summary = ""
    if isinstance(comparison_surface, dict):
        raw_question = comparison_surface.get("selection_question")
        if isinstance(raw_question, str):
            selection_summary = raw_question
    interpretation_boundary = summarize_interpretation_limits(
        record.sections["Interpretation guidance"]
    )

    entry = {
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
        "comparison_surface": comparison_surface,
        "selection_summary": selection_summary,
        "interpretation_boundary": interpretation_boundary,
        "technique_dependencies": list(metadata["technique_dependencies"]),
        "technique_refs": technique_refs,
        "skill_dependencies": list(metadata["skill_dependencies"]),
        "skill_refs": skill_refs,
        "relations": list(manifest["relations"]),
        "evidence": evidence_entries,
        "evidence_kinds": compact_evidence_kinds(evidence_entries),
        "proof_artifacts": proof_artifacts,
        "proof_surface_kinds": compact_proof_surface_kinds(proof_artifacts),
    }
    if "public_safety_reviewed_at" in manifest:
        entry["public_safety_reviewed_at"] = manifest["public_safety_reviewed_at"]
    return entry


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
    records: list[Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    sorted_records = sorted(records, key=lambda record: record.name)
    full_catalog = {
        "catalog_version": CATALOG_VERSION,
        "source_of_truth": CATALOG_SOURCE_OF_TRUTH,
        "evals": [full_catalog_entry(repo_root, record) for record in sorted_records],
    }
    return full_catalog, project_min_catalog(full_catalog)


def read_json_file(path: Path, repo_root: Path) -> tuple[Any | None, list[ContractIssue]]:
    issues: list[ContractIssue] = []
    try:
        return json.loads(path.read_text(encoding="utf-8")), issues
    except FileNotFoundError:
        issues.append(ContractIssue(relative_location(path, repo_root), "file is missing"))
    except json.JSONDecodeError as exc:
        issues.append(ContractIssue(relative_location(path, repo_root), f"invalid JSON: {exc}"))
    return None, issues


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


def catalog_entries_by_name(
    catalog: dict[str, Any],
    *,
    array_key: str,
    key_name: str,
    location: str,
) -> tuple[dict[str, dict[str, Any]], list[ContractIssue]]:
    entries = catalog.get(array_key)
    if not isinstance(entries, list):
        return {}, [ContractIssue(location, f"catalog field '{array_key}' must be a list")]

    issues: list[ContractIssue] = []
    entry_map: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            issues.append(
                ContractIssue(
                    location,
                    f"catalog field '{array_key}[{index}]' must be an object",
                )
            )
            continue
        name = entry.get(key_name)
        if not isinstance(name, str):
            issues.append(
                ContractIssue(
                    location,
                    f"catalog field '{array_key}[{index}].{key_name}' must be a string",
                )
            )
            continue
        if name in entry_map:
            issues.append(
                ContractIssue(
                    location,
                    f"catalog field '{array_key}' must not contain duplicate '{name}' entries",
                )
            )
            continue
        entry_map[name] = entry
    return entry_map, issues
