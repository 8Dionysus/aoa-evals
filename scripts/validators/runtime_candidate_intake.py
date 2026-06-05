"""Runtime-candidate intake projection parity."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from validators.runtime_candidate_common import (
    RUNTIME_CANDIDATE_INTAKE_NAME,
    RUNTIME_CANDIDATE_INTAKE_SCRIPT_NAME,
    RUNTIME_CANDIDATE_TEMPLATE_INDEX_NAME,
    ValidationIssue,
    load_builder_module,
    load_json_payload,
    relative_location,
)


def load_runtime_candidate_intake_builder(repo_root: Path):
    return load_builder_module(
        repo_root,
        RUNTIME_CANDIDATE_INTAKE_SCRIPT_NAME,
        "generate_runtime_candidate_intake",
    )


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
            "runtime_policy_boundary",
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


__all__ = (
    "load_runtime_candidate_intake_builder",
    "validate_runtime_candidate_intake",
)
