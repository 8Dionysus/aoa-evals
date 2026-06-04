"""Runtime-candidate generated reader boundary contracts."""

from __future__ import annotations

import importlib.util
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable

from jsonschema import Draft202012Validator, SchemaError


GENERATED_DIR_NAME = "generated"
MIN_CATALOG_NAME = "eval_catalog.min.json"
RUNTIME_EVIDENCE_SELECTION_EXAMPLES_DIR = "mechanics/audit/parts/selected-evidence-packets/examples"
ARTIFACT_VERDICT_HOOK_EXAMPLES_DIR = "mechanics/audit/parts/artifact-verdict-hooks/examples"
ARTIFACT_VERDICT_HOOK_EXAMPLE_DIRS = (
    ARTIFACT_VERDICT_HOOK_EXAMPLES_DIR,
    "mechanics/checkpoint/parts/a2a-summon-return/examples",
    "mechanics/checkpoint/parts/restartable-inquiry/examples",
    "mechanics/checkpoint/parts/self-agent-posture/examples",
)
RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCHEMA_NAME = "runtime-candidate-template-index.schema.json"
RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCHEMA_PATH = (
    "mechanics/audit/parts/candidate-readers/schemas/runtime-candidate-template-index.schema.json"
)
RUNTIME_CANDIDATE_TEMPLATE_INDEX_NAME = "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json"
RUNTIME_CANDIDATE_INTAKE_NAME = "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json"
RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCRIPT_NAME = (
    "mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py"
)
RUNTIME_CANDIDATE_INTAKE_SCRIPT_NAME = (
    "mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py"
)
NORMALIZED_RUNTIME_ARTIFACT_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


def relative_location(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def format_schema_path(path_parts: Iterable[Any]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        elif parts:
            parts.append(f".{part}")
        else:
            parts.append(str(part))
    return "".join(parts)


def load_json_payload(path: Path, issues: list[ValidationIssue], *, root: Path) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return None
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid JSON: {exc}"))
        return None


def validate_inline_schema(
    schema: object,
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


def validate_against_schema(
    data: object,
    location: str,
    issues: list[ValidationIssue],
    *,
    validator: Draft202012Validator,
) -> bool:
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


def load_mapping_entries(
    payload: object,
    *,
    array_key: str,
    key_name: str,
    location: str,
    issues: list[ValidationIssue],
) -> dict[str, dict[str, Any]]:
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(location, "payload must be an object"))
        return {}
    items = payload.get(array_key)
    if not isinstance(items, list):
        issues.append(ValidationIssue(location, f"missing array '{array_key}'"))
        return {}

    entries: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        item_location = f"{location}.{array_key}[{index}]"
        if not isinstance(item, dict):
            issues.append(ValidationIssue(item_location, "entry must be an object"))
            continue
        key = item.get(key_name)
        if not isinstance(key, str) or not key:
            issues.append(
                ValidationIssue(item_location, f"entry must expose string key '{key_name}'")
            )
            continue
        if key in entries:
            issues.append(
                ValidationIssue(item_location, f"duplicate entry for '{key_name}' value '{key}'")
            )
            continue
        entries[key] = item
    return entries


def load_runtime_candidate_template_index_builder(repo_root: Path):
    module_path = repo_root / RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCRIPT_NAME
    spec = importlib.util.spec_from_file_location(
        "generate_runtime_candidate_template_index",
        module_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load runtime candidate template index generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_runtime_candidate_template_index(
    repo_root: Path,
    *,
    builder_loader: Callable[[Path], object] = load_runtime_candidate_template_index_builder,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    generated_path = repo_root / RUNTIME_CANDIDATE_TEMPLATE_INDEX_NAME
    generated_location = relative_location(generated_path, repo_root)
    schema_path = repo_root / RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCHEMA_PATH
    schema_location = relative_location(schema_path, repo_root)

    schema = load_json_payload(schema_path, issues, root=repo_root)
    if schema is None:
        return issues
    if not validate_inline_schema(schema, location=schema_location, issues=issues):
        return issues
    schema_validator = Draft202012Validator(schema)

    try:
        builder = builder_loader(repo_root)
        expected = builder.build_runtime_candidate_template_index_payload()
    except (Exception, SystemExit) as exc:
        issues.append(ValidationIssue(generated_location, str(exc)))
        return issues

    payload = load_json_payload(generated_path, issues, root=repo_root)
    if payload is None:
        return issues
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(generated_location, "generated template index must be an object"))
        return issues

    validate_against_schema(
        payload,
        generated_location,
        issues,
        validator=schema_validator,
    )

    if payload != expected:
        issues.append(
            ValidationIssue(
                generated_location,
                "generated runtime candidate template index is out of date or mismatched",
            )
        )

    templates = payload.get("templates")
    if not isinstance(templates, list):
        issues.append(ValidationIssue(generated_location, "templates must be a list"))
        return issues

    expected_refs = {
        relative_location(path, repo_root)
        for path in sorted((repo_root / RUNTIME_EVIDENCE_SELECTION_EXAMPLES_DIR).glob("runtime_evidence_selection.*.example.json"))
    }
    for examples_dir in ARTIFACT_VERDICT_HOOK_EXAMPLE_DIRS:
        expected_refs.update(
            relative_location(path, repo_root)
            for path in sorted((repo_root / examples_dir).glob("artifact_to_verdict_hook.*.example.json"))
        )
    indexed_refs = {
        entry.get("source_example_ref")
        for entry in templates
        if isinstance(entry, dict) and isinstance(entry.get("source_example_ref"), str)
    }
    if indexed_refs != expected_refs:
        missing = sorted(expected_refs - indexed_refs)
        extra = sorted(indexed_refs - expected_refs)
        if missing:
            issues.append(
                ValidationIssue(generated_location, "missing example refs in template index: " + ", ".join(missing))
            )
        if extra:
            issues.append(
                ValidationIssue(generated_location, "unexpected example refs in template index: " + ", ".join(extra))
            )

    eval_catalog_path = repo_root / GENERATED_DIR_NAME / MIN_CATALOG_NAME
    eval_catalog_location = relative_location(eval_catalog_path, repo_root)
    eval_catalog = load_json_payload(eval_catalog_path, issues, root=repo_root)
    if not isinstance(eval_catalog, dict):
        return issues
    evals_by_name = load_mapping_entries(
        eval_catalog,
        array_key="evals",
        key_name="name",
        location=eval_catalog_location,
        issues=issues,
    )

    for index, entry in enumerate(templates):
        location = f"{generated_location}.templates[{index}]"
        if not isinstance(entry, dict):
            issues.append(ValidationIssue(location, "template entry must be an object"))
            continue

        required_runtime_artifacts = entry.get("required_runtime_artifacts")
        if isinstance(required_runtime_artifacts, list):
            normalized_artifacts = [
                artifact
                for artifact in required_runtime_artifacts
                if isinstance(artifact, str) and bool(NORMALIZED_RUNTIME_ARTIFACT_RE.fullmatch(artifact))
            ]
            if len(normalized_artifacts) != len(required_runtime_artifacts):
                issues.append(
                    ValidationIssue(
                        location,
                        "required_runtime_artifacts must stay normalized to lowercase runtime artifact names",
                    )
                )
            if len(required_runtime_artifacts) != len(set(required_runtime_artifacts)):
                issues.append(
                    ValidationIssue(
                        location,
                        "required_runtime_artifacts must not duplicate runtime artifact names",
                    )
                )

        source_example_ref = entry.get("source_example_ref")
        if not isinstance(source_example_ref, str):
            continue
        example_path = repo_root / source_example_ref
        example_payload = load_json_payload(example_path, issues, root=repo_root)
        if example_payload is None or not isinstance(example_payload, dict):
            continue

        template_kind = entry.get("template_kind")
        if template_kind == "runtime_evidence_selection":
            if entry.get("template_name") != example_payload.get("selection_id"):
                issues.append(ValidationIssue(location, "template_name must match selection_id"))
            target_eval = example_payload.get("target_eval")
            if entry.get("eval_anchor") != target_eval:
                issues.append(ValidationIssue(location, "eval_anchor must match target_eval"))
            expected_bundle_ref = None
            if isinstance(target_eval, str):
                catalog_entry = evals_by_name.get(target_eval)
                if catalog_entry is None:
                    issues.append(
                        ValidationIssue(location, f"eval_anchor '{target_eval}' does not resolve in eval catalog")
                    )
                else:
                    expected_bundle_ref = f"repo:aoa-evals/{catalog_entry.get('eval_path')}"
            if entry.get("verdict_bundle_ref") != expected_bundle_ref:
                issues.append(ValidationIssue(location, "verdict_bundle_ref must match the resolved eval bundle or stay null"))
            selected_evidence = example_payload.get("selected_evidence")
            expected_artifacts = []
            if isinstance(selected_evidence, list):
                expected_artifacts = []
                for item in selected_evidence:
                    if not isinstance(item, dict):
                        continue
                    evidence_role = item.get("evidence_role")
                    if isinstance(evidence_role, str) and evidence_role not in expected_artifacts:
                        expected_artifacts.append(evidence_role)
            if entry.get("required_runtime_artifacts") != expected_artifacts:
                issues.append(ValidationIssue(location, "required_runtime_artifacts must match selected evidence roles"))
            review_posture = example_payload.get("review_posture")
            expected_review_required = bool(
                isinstance(review_posture, dict) and review_posture.get("human_review_required") is True
            )
            if entry.get("review_required") is not expected_review_required:
                issues.append(ValidationIssue(location, "review_required must match review_posture.human_review_required"))
        elif template_kind == "artifact_to_verdict_hook":
            if entry.get("template_name") != example_payload.get("hook_id"):
                issues.append(ValidationIssue(location, "template_name must match hook_id"))
            if entry.get("playbook_id") != example_payload.get("playbook_id"):
                issues.append(ValidationIssue(location, "playbook_id must match the source hook example"))
            if entry.get("eval_anchor") != example_payload.get("eval_anchor"):
                issues.append(ValidationIssue(location, "eval_anchor must match the source hook example"))
            if entry.get("verdict_bundle_ref") != example_payload.get("verdict_bundle_ref"):
                issues.append(ValidationIssue(location, "verdict_bundle_ref must match the source hook example"))
            expected_artifacts = example_payload.get("artifact_inputs")
            if entry.get("required_runtime_artifacts") != expected_artifacts:
                issues.append(ValidationIssue(location, "required_runtime_artifacts must match artifact_inputs"))
            report_expectation = example_payload.get("report_expectation")
            expected_review_required = bool(
                isinstance(report_expectation, dict) and report_expectation.get("review_required") is True
            )
            if entry.get("review_required") is not expected_review_required:
                issues.append(ValidationIssue(location, "review_required must match report_expectation.review_required"))

    return issues


def load_runtime_candidate_intake_builder(repo_root: Path):
    module_path = repo_root / RUNTIME_CANDIDATE_INTAKE_SCRIPT_NAME
    spec = importlib.util.spec_from_file_location(
        "generate_runtime_candidate_intake",
        module_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load runtime candidate intake generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_runtime_candidate_intake(
    repo_root: Path,
    *,
    builder_loader: Callable[[Path], object] = load_runtime_candidate_intake_builder,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    generated_path = repo_root / RUNTIME_CANDIDATE_INTAKE_NAME
    generated_location = relative_location(generated_path, repo_root)

    try:
        builder = builder_loader(repo_root)
        expected = builder.build_runtime_candidate_intake_payload()
    except (Exception, SystemExit) as exc:
        issues.append(ValidationIssue(generated_location, str(exc)))
        return issues

    payload = load_json_payload(generated_path, issues, root=repo_root)
    if payload is None:
        return issues
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(generated_location, "generated runtime candidate intake must be an object"))
        return issues
    if payload != expected:
        issues.append(
            ValidationIssue(
                generated_location,
                "generated runtime candidate intake is out of date or mismatched",
            )
        )
    if payload.get("schema_version") != 1:
        issues.append(ValidationIssue(generated_location, "schema_version must equal 1"))
    if payload.get("layer") != "aoa-evals":
        issues.append(ValidationIssue(generated_location, "layer must equal 'aoa-evals'"))
    expected_source_of_truth = {
        "runtime_candidate_template_index": "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json",
        "eval_review_guide": "docs/guides/EVAL_REVIEW_GUIDE.md",
        "trace_eval_bridge": "mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md",
        "runtime_bench_promotion_guide": "mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
    }
    if payload.get("source_of_truth") != expected_source_of_truth:
        issues.append(ValidationIssue(generated_location, "source_of_truth must stay stable"))

    templates = payload.get("templates")
    if not isinstance(templates, list):
        issues.append(ValidationIssue(generated_location, "templates must be a list"))
        return issues

    template_index_payload = load_json_payload(repo_root / RUNTIME_CANDIDATE_TEMPLATE_INDEX_NAME, issues, root=repo_root)
    if not isinstance(template_index_payload, dict):
        return issues
    templates_by_key = {
        (entry.get("template_kind"), entry.get("template_name")): entry
        for entry in template_index_payload.get("templates", [])
        if isinstance(entry, dict)
    }
    intake_keys = [
        (entry.get("template_kind"), entry.get("template_name"))
        for entry in templates
        if isinstance(entry, dict)
    ]
    if intake_keys != sorted(intake_keys):
        issues.append(ValidationIssue(generated_location, "templates must stay ordered by template_kind and template_name"))
    if len(intake_keys) != len(set(intake_keys)):
        issues.append(ValidationIssue(generated_location, "templates must not duplicate template entries"))
    if set(intake_keys) != set(templates_by_key):
        missing = sorted(set(templates_by_key) - set(intake_keys))
        extra = sorted(set(intake_keys) - set(templates_by_key))
        if missing:
            issues.append(
                ValidationIssue(
                    generated_location,
                    "missing template entries in runtime candidate intake: "
                    + ", ".join(f"{kind}:{name}" for kind, name in missing),
                )
            )
        if extra:
            issues.append(
                ValidationIssue(
                    generated_location,
                    "unexpected template entries in runtime candidate intake: "
                    + ", ".join(f"{kind}:{name}" for kind, name in extra),
                )
            )

    review_guide_by_kind = {
        "artifact_to_verdict_hook": "mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md",
        "runtime_evidence_selection": "mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
    }

    for index, entry in enumerate(templates):
        location = f"{generated_location}.templates[{index}]"
        if not isinstance(entry, dict):
            issues.append(ValidationIssue(location, "template entry must be an object"))
            continue
        key = (entry.get("template_kind"), entry.get("template_name"))
        source_entry = templates_by_key.get(key)
        if source_entry is None:
            continue

        for field_name in (
            "playbook_id",
            "eval_anchor",
            "verdict_bundle_ref",
            "required_runtime_artifacts",
            "review_required",
        ):
            if entry.get(field_name) != source_entry.get(field_name):
                issues.append(ValidationIssue(location, f"{field_name} must match mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json"))

        template_kind = entry.get("template_kind")
        expected_review_guide = review_guide_by_kind.get(template_kind, "docs/guides/EVAL_REVIEW_GUIDE.md")
        if entry.get("review_guide_ref") != expected_review_guide:
            issues.append(ValidationIssue(location, "review_guide_ref must stay aligned with the template kind"))

        owner_review_refs = entry.get("owner_review_refs")
        if not isinstance(owner_review_refs, list) or not owner_review_refs:
            issues.append(ValidationIssue(location, "owner_review_refs must stay a non-empty list"))
        else:
            expected_owner_review_refs = [
                expected_review_guide,
                "docs/guides/EVAL_REVIEW_GUIDE.md",
                source_entry.get("source_example_ref"),
            ]
            expected_owner_review_refs = [
                item for item in expected_owner_review_refs if isinstance(item, str) and item
            ]
            deduped: list[str] = []
            for item in expected_owner_review_refs:
                if item not in deduped:
                    deduped.append(item)
            if owner_review_refs != deduped:
                issues.append(ValidationIssue(location, "owner_review_refs must stay aligned with the source example and review guides"))
            for ref in owner_review_refs:
                if not isinstance(ref, str):
                    continue
                if not (repo_root / ref).exists():
                    issues.append(ValidationIssue(location, f"owner_review_ref '{ref}' must point to a live local file"))

        if entry.get("candidate_acceptance_posture") != "candidate_until_eval_review":
            issues.append(ValidationIssue(location, "candidate_acceptance_posture must stay 'candidate_until_eval_review'"))

    return issues
