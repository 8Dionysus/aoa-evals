"""Runtime integrity review example payload and reference checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from validators import (
    runtime_integrity_review_common as common,
    runtime_integrity_review_schema as schema_validator_module,
)
from validators.common import (
    ValidationIssue,
    load_json_payload,
    relative_location,
    validate_against_schema,
)


RUNTIME_INTEGRITY_REVIEW_EXAMPLE_NAME = common.RUNTIME_INTEGRITY_REVIEW_EXAMPLE_NAME
RUNTIME_INTEGRITY_REVIEW_BUDGET_REF = common.RUNTIME_INTEGRITY_REVIEW_BUDGET_REF
RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS = common.RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS
RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS = common.RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS
RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS = common.RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS


def validate_runtime_integrity_review_example_surface(
    repo_root: Path,
    *,
    context: Any,
    schema_validator: Draft202012Validator | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if schema_validator is None:
        schema_validation = schema_validator_module.runtime_integrity_review_schema_validation(repo_root)
        issues.extend(schema_validation.issues)
        schema_validator = schema_validation.validator
    if schema_validator is None:
        return issues

    example_path = repo_root / RUNTIME_INTEGRITY_REVIEW_EXAMPLE_NAME
    payload = load_json_payload(example_path, issues, root=repo_root)
    if payload is None:
        return issues
    location = relative_location(example_path, repo_root)
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(location, "runtime integrity review example must be an object"))
        return issues

    validate_against_schema(
        payload,
        location=location,
        issues=issues,
        validator=schema_validator,
    )

    if payload.get("schema_version") != "runtime_integrity_review_v1":
        issues.append(
            ValidationIssue(
                location,
                "runtime integrity review example schema_version must be 'runtime_integrity_review_v1'",
            )
        )
    if payload.get("owner_repo") != "aoa-evals":
        issues.append(ValidationIssue(location, "owner_repo must remain aoa-evals"))
    if payload.get("surface_kind") != "runtime_integrity_review":
        issues.append(ValidationIssue(location, "surface_kind must remain runtime_integrity_review"))
    if payload.get("status") != "candidate_only":
        issues.append(ValidationIssue(location, "status must remain candidate_only"))

    if payload.get("budget_ref") != RUNTIME_INTEGRITY_REVIEW_BUDGET_REF:
        issues.append(
            ValidationIssue(
                location,
                "budget_ref must stay bound to the Experience continuity-context owner split surface",
            )
        )
    else:
        context.parse_named_surface_ref(
            payload.get("budget_ref"),
            prefix_name="Agents-of-Abyss",
            repo_root=context.agents_of_abyss_root,
            location=f"{location}.budget_ref",
            issues=issues,
        )

    evidence_refs = payload.get("evidence_refs")
    resolved_evidence_refs: set[str] = set()
    if not isinstance(evidence_refs, list):
        issues.append(ValidationIssue(f"{location}.evidence_refs", "evidence_refs must be a list"))
    else:
        for index, ref in enumerate(evidence_refs):
            resolution = context.parse_repo_ref(
                ref,
                location=f"{location}.evidence_refs[{index}]",
                issues=issues,
            )
            if resolution is None:
                continue
            repo_name, target_path, anchor = resolution
            normalized_ref = f"repo:{repo_name}/{target_path.relative_to(context.repo_ref_roots[repo_name]).as_posix()}"
            if anchor:
                normalized_ref = f"{normalized_ref}#{anchor}"
            resolved_evidence_refs.add(normalized_ref)
        if resolved_evidence_refs and resolved_evidence_refs != set(RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS):
            issues.append(
                ValidationIssue(
                    location,
                    "evidence_refs must resolve to the bounded W10 runtime integrity review surfaces",
                )
            )

    expected_replay_requirements = {field_name: True for field_name in RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS}
    if payload.get("replay_requirements") != expected_replay_requirements:
        issues.append(
            ValidationIssue(
                location,
                "replay_requirements must keep selected-evidence, owner-local replay, fail-closed, and review-required posture",
            )
        )

    if payload.get("human_review_needed") is not True:
        issues.append(ValidationIssue(location, "human_review_needed must remain true"))

    forbidden_claims = payload.get("forbidden_claims")
    if not isinstance(forbidden_claims, list):
        issues.append(
            ValidationIssue(
                f"{location}.forbidden_claims",
                "forbidden_claims must be a list",
            )
        )
    elif set(forbidden_claims) != set(RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS):
        issues.append(
            ValidationIssue(
                location,
                "forbidden_claims must exactly preserve the bounded no-authority guard",
            )
        )

    notes = payload.get("notes")
    if not isinstance(notes, str) or "Candidate only." not in notes:
        issues.append(
            ValidationIssue(
                location,
                "runtime integrity review example notes must keep candidate-only posture explicit",
            )
        )
    elif "activation pressure to Experience or runtime-owner gates" not in notes:
        issues.append(
            ValidationIssue(
                location,
                "runtime integrity review example notes must keep activation routing explicit",
            )
        )

    return issues
