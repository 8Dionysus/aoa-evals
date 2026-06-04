"""Generated eval report index boundary contracts."""

from __future__ import annotations

import importlib.util
import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable


EVAL_REPORT_INDEX_NAME = "generated/eval_report_index.min.json"
EVAL_REPORT_INDEX_DECISION_NAME = "docs/decisions/AOA-EV-D-0023-eval-report-index-reader.md"
DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
DECISION_INDEX_PATHS = (
    Path("docs/decisions/indexes/by-number.md"),
    Path("docs/decisions/indexes/by-date.md"),
    Path("docs/decisions/indexes/by-surface.md"),
    Path("docs/decisions/indexes/by-mechanic.md"),
    Path("docs/decisions/indexes/by-validation-guard.md"),
)


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


def relative_location(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def load_json_payload(path: Path, issues: list[ValidationIssue], *, root: Path) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return None
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid JSON: {exc}"))
        return None


def read_text_or_issue(path: Path, issues: list[ValidationIssue], *, root: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return ""


def require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: tuple[str, ...],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return text
    search_text = text
    if path_name == DECISION_RECORDS_README_NAME:
        index_texts = []
        for relative_path in DECISION_INDEX_PATHS:
            index_path = repo_root / relative_path
            if index_path.is_file():
                index_texts.append(index_path.read_text(encoding="utf-8"))
        if index_texts:
            search_text = "\n\n".join((text, *index_texts))
    for token in tokens:
        if token not in search_text:
            issues.append(ValidationIssue(path_name, f"file must mention '{token}'"))
    return text


def load_eval_report_index_builder(repo_root: Path):
    module_path = repo_root / "scripts" / "generate_eval_report_index.py"
    spec = importlib.util.spec_from_file_location(
        "generate_eval_report_index",
        module_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load eval report index generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_eval_report_index(
    repo_root: Path,
    *,
    builder_loader: Callable[[Path], object] = load_eval_report_index_builder,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    generated_path = repo_root / EVAL_REPORT_INDEX_NAME
    generated_location = relative_location(generated_path, repo_root)

    try:
        builder = builder_loader(repo_root)
        expected = builder.build_eval_report_index_payload()
    except (Exception, SystemExit) as exc:
        issues.append(ValidationIssue(generated_location, str(exc)))
        return issues

    payload = load_json_payload(generated_path, issues, root=repo_root)
    if payload is None:
        return issues
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(generated_location, "generated eval report index must be an object"))
        return issues
    if payload != expected:
        issues.append(
            ValidationIssue(
                generated_location,
                "generated eval report index is out of date or mismatched",
            )
        )
    if payload.get("schema_version") != 1:
        issues.append(ValidationIssue(generated_location, "schema_version must equal 1"))
    if payload.get("layer") != "aoa-evals":
        issues.append(ValidationIssue(generated_location, "layer must equal 'aoa-evals'"))
    expected_source_of_truth = {
        "bundle_reports": "evals/**/reports/*.report.json",
        "bundle_report_schema": "evals/**/reports/summary.schema.json",
        "bundle_manifest": "evals/**/eval.yaml",
        "eval_review_guide": "docs/guides/EVAL_REVIEW_GUIDE.md",
    }
    if payload.get("source_of_truth") != expected_source_of_truth:
        issues.append(ValidationIssue(generated_location, "source_of_truth must stay stable"))
    boundary = payload.get("interpretation_boundary")
    if not isinstance(boundary, str) or not all(
        token in boundary
        for token in ("not a receipt", "promotion signal", "runtime acceptance", "verdict authority")
    ):
        issues.append(
            ValidationIssue(
                generated_location,
                "interpretation_boundary must keep receipt, promotion, runtime, and verdict authority limits explicit",
            )
        )

    reports = payload.get("reports")
    if not isinstance(reports, list):
        issues.append(ValidationIssue(generated_location, "reports must be a list"))
        return issues

    keys: list[tuple[str, str]] = []
    source_paths: list[str] = []
    for index, entry in enumerate(reports):
        location = f"{generated_location}.reports[{index}]"
        if not isinstance(entry, dict):
            issues.append(ValidationIssue(location, "report entry must be an object"))
            continue

        eval_name = entry.get("eval_name")
        report_id = entry.get("report_id")
        source_report_path = entry.get("source_report_path")
        if not isinstance(eval_name, str) or not eval_name:
            issues.append(ValidationIssue(location, "eval_name must be a non-empty string"))
            continue
        if not isinstance(report_id, str) or not report_id:
            issues.append(ValidationIssue(location, "report_id must be a non-empty string"))
            continue
        if not isinstance(source_report_path, str) or not source_report_path.endswith(".report.json"):
            issues.append(ValidationIssue(location, "source_report_path must point to a bundle-local .report.json"))
            continue

        keys.append((eval_name, report_id))
        source_paths.append(source_report_path)
        report_path = repo_root / source_report_path
        if not report_path.is_file():
            issues.append(ValidationIssue(location, f"source_report_path does not exist: {source_report_path}"))
            continue

        report_payload = load_json_payload(report_path, issues, root=repo_root)
        if not isinstance(report_payload, dict):
            continue
        for field_name in ("eval_name", "bundle_status", "verdict", "case_family", "claim_boundary"):
            if entry.get(field_name) != report_payload.get(field_name):
                issues.append(
                    ValidationIssue(location, f"{field_name} must match source_report_path")
                )
        limitations = report_payload.get("limitations")
        expected_limitations_count = len(limitations) if isinstance(limitations, list) else 0
        if entry.get("limitations_count") != expected_limitations_count:
            issues.append(ValidationIssue(location, "limitations_count must match source_report_path"))

        report_eval_dir = PurePosixPath(source_report_path).parents[1]
        if entry.get("source_bundle_ref") != f"{report_eval_dir.as_posix()}/EVAL.md":
            issues.append(ValidationIssue(location, "source_bundle_ref must point to the owning bundle EVAL.md"))
        if entry.get("manifest_ref") != f"{report_eval_dir.as_posix()}/eval.yaml":
            issues.append(ValidationIssue(location, "manifest_ref must point to the owning bundle eval.yaml"))
        if entry.get("report_schema_ref") != f"{report_eval_dir.as_posix()}/reports/summary.schema.json":
            issues.append(ValidationIssue(location, "report_schema_ref must point to the owning bundle report schema"))
        for ref_field in ("source_bundle_ref", "manifest_ref", "report_schema_ref"):
            ref_value = entry.get(ref_field)
            if isinstance(ref_value, str) and not (repo_root / ref_value).exists():
                issues.append(ValidationIssue(location, f"{ref_field} does not exist: {ref_value}"))

        if entry.get("report_posture") != "bounded_report_output":
            issues.append(ValidationIssue(location, "report_posture must stay 'bounded_report_output'"))
        authority_boundary = entry.get("authority_boundary")
        if not isinstance(authority_boundary, str) or "derived index only" not in authority_boundary:
            issues.append(ValidationIssue(location, "authority_boundary must keep derived-index posture explicit"))
        if entry.get("receipt_status") != "not_a_receipt":
            issues.append(ValidationIssue(location, "receipt_status must stay 'not_a_receipt'"))

    if keys != sorted(keys):
        issues.append(ValidationIssue(generated_location, "reports must stay ordered by eval_name and report_id"))
    if len(keys) != len(set(keys)):
        issues.append(ValidationIssue(generated_location, "reports must not duplicate eval_name/report_id entries"))
    if len(source_paths) != len(set(source_paths)):
        issues.append(ValidationIssue(generated_location, "reports must not duplicate source_report_path entries"))

    return issues


def validate_eval_report_index_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    require_tokens(
        repo_root=repo_root,
        path_name=EVAL_REPORT_INDEX_DECISION_NAME,
        tokens=(
            EVAL_REPORT_INDEX_NAME,
            "derived reader",
            "not_a_receipt",
            "no report verdict is promoted into generated authority",
            "scripts/generate_eval_report_index.py",
        ),
        issues=issues,
    )
    for path_name in (
        "docs/README.md",
        "CHANGELOG.md",
        "generated/AGENTS.md",
        "mechanics/proof-loop/README.md",
        "mechanics/proof-infra/README.md",
        "reports/README.md",
    ):
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=(EVAL_REPORT_INDEX_NAME,),
            issues=issues,
        )
    require_tokens(
        repo_root=repo_root,
        path_name="ROADMAP.md",
        tokens=("Generated report readers", "generated/README.md"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(EVAL_REPORT_INDEX_DECISION_NAME,),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name="scripts/release_check.py",
        tokens=("scripts/generate_eval_report_index.py", "--check"),
        issues=issues,
    )
    return issues
