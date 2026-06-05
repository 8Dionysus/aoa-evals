"""Runtime-candidate template index projection parity."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from jsonschema import Draft202012Validator

from validators.runtime_candidate_common import (
    ARTIFACT_VERDICT_HOOK_EXAMPLE_DIRS,
    GENERATED_DIR_NAME,
    MIN_CATALOG_NAME,
    NORMALIZED_RUNTIME_ARTIFACT_RE,
    RUNTIME_CANDIDATE_TEMPLATE_INDEX_NAME,
    RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCHEMA_PATH,
    RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCRIPT_NAME,
    RUNTIME_EVIDENCE_SELECTION_EXAMPLES_DIR,
    ValidationIssue,
    load_builder_module,
    load_json_payload,
    load_mapping_entries,
    relative_location,
    validate_against_schema,
    validate_inline_schema,
)


def load_runtime_candidate_template_index_builder(repo_root: Path):
    return load_builder_module(
        repo_root,
        RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCRIPT_NAME,
        "generate_runtime_candidate_template_index",
    )


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
            runtime_policy_boundary = example_payload.get("runtime_policy_boundary")
            expected_runtime_policy_boundary = (
                runtime_policy_boundary if isinstance(runtime_policy_boundary, dict) else None
            )
            if entry.get("runtime_policy_boundary") != expected_runtime_policy_boundary:
                issues.append(ValidationIssue(location, "runtime_policy_boundary must match the source hook example"))
            report_expectation = example_payload.get("report_expectation")
            expected_review_required = bool(
                isinstance(report_expectation, dict) and report_expectation.get("review_required") is True
            )
            if entry.get("review_required") is not expected_review_required:
                issues.append(ValidationIssue(location, "review_required must match report_expectation.review_required"))

    return issues


__all__ = (
    "load_runtime_candidate_template_index_builder",
    "validate_runtime_candidate_template_index",
)
