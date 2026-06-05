"""Publication receipt payload and schema mirror contracts."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from jsonschema import Draft202012Validator, SchemaError

from validators.publication_receipts_common import (
    EVAL_RESULT_RECEIPT_SCHEMA_NAME,
    EVAL_RESULT_RECEIPT_SCHEMA_PATH,
    PUBLICATION_RECEIPTS_PARTS_ROOT,
    SCHEMAS_DIR_NAME,
    STATS_EVENT_ENVELOPE_SCHEMA_NAME,
    STATS_EVENT_ENVELOPE_SCHEMA_PATH,
    ValidationIssue,
    get_schema_validator_with_format,
    load_json_payload,
    parse_repo_ref,
    read_text_or_issue,
    relative_location,
    validate_against_schema,
)

EVAL_RESULT_RECEIPT_GUIDE_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md"
)
EVAL_RESULT_RECEIPT_EXAMPLE_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/receipt-payload/examples/eval_result_receipt.example.json"
)
EVAL_RESULT_RECEIPT_REQUIRED_TOKENS = (
    "## Core Rule",
    "`eval_result_receipt`",
    "`stats-event-envelope`",
    "`supersedes`",
    "meaning stays with bundle-local review",
    "repo-global score",
    "## Receipt Pressure Routes",
    "Proof-canon pressure routes",
)


def validate_eval_result_receipt_surfaces(
    repo_root: Path,
    *,
    aoa_stats_root: Path,
    repo_ref_roots: Mapping[str, Path],
    strict_sibling_compat: bool,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    guide_path = repo_root / EVAL_RESULT_RECEIPT_GUIDE_NAME
    envelope_schema_path = repo_root / STATS_EVENT_ENVELOPE_SCHEMA_PATH
    payload_schema_path = repo_root / EVAL_RESULT_RECEIPT_SCHEMA_PATH
    example_path = repo_root / EVAL_RESULT_RECEIPT_EXAMPLE_NAME

    guide_text = read_text_or_issue(guide_path, issues, root=repo_root)
    if guide_text:
        for token in EVAL_RESULT_RECEIPT_REQUIRED_TOKENS:
            if token not in guide_text:
                issues.append(
                    ValidationIssue(
                        relative_location(guide_path, repo_root),
                        f"eval result receipt guide must mention '{token}'",
                    )
                )

    envelope_schema = load_json_payload(envelope_schema_path, issues, root=repo_root)
    envelope_validator: Draft202012Validator | None = None
    if isinstance(envelope_schema, dict):
        envelope_schema_valid = True
        if envelope_schema.get("title") != "aoa-evals stats event envelope":
            issues.append(
                ValidationIssue(
                    relative_location(envelope_schema_path, repo_root),
                    "stats event envelope schema title must be 'aoa-evals stats event envelope'",
                )
            )
            envelope_schema_valid = False
        canonical_schema_ref = envelope_schema.get("x-canonical_schema_ref")
        if canonical_schema_ref != "repo:aoa-stats/schemas/stats-event-envelope.schema.json":
            issues.append(
                ValidationIssue(
                    relative_location(envelope_schema_path, repo_root),
                    "stats event envelope mirror must point to repo:aoa-stats/schemas/stats-event-envelope.schema.json",
                )
            )
            envelope_schema_valid = False
        canonical_envelope_path = aoa_stats_root / SCHEMAS_DIR_NAME / STATS_EVENT_ENVELOPE_SCHEMA_NAME
        if canonical_envelope_path.exists():
            canonical_envelope = load_json_payload(canonical_envelope_path, issues, root=aoa_stats_root)
            if isinstance(canonical_envelope, dict):
                local_enum = envelope_schema.get("properties", {}).get("event_kind", {}).get("enum")
                canonical_enum = canonical_envelope.get("properties", {}).get("event_kind", {}).get("enum")
                if local_enum != canonical_enum:
                    issues.append(
                        ValidationIssue(
                            relative_location(envelope_schema_path, repo_root),
                            "stats event envelope mirror enum must match ../aoa-stats/schemas/stats-event-envelope.schema.json",
                        )
                    )
        try:
            Draft202012Validator.check_schema(envelope_schema)
        except SchemaError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(envelope_schema_path, repo_root),
                    f"invalid JSON schema: {exc.message}",
                )
            )
            envelope_schema_valid = False
        if envelope_schema_valid:
            envelope_validator = get_schema_validator_with_format(envelope_schema)
    elif envelope_schema is not None:
        issues.append(
            ValidationIssue(
                relative_location(envelope_schema_path, repo_root),
                "stats event envelope schema must be a JSON object",
            )
        )

    payload_schema = load_json_payload(payload_schema_path, issues, root=repo_root)
    payload_validator: Draft202012Validator | None = None
    if isinstance(payload_schema, dict):
        payload_schema_valid = True
        if payload_schema.get("title") != "aoa-evals eval result receipt":
            issues.append(
                ValidationIssue(
                    relative_location(payload_schema_path, repo_root),
                    "eval result receipt schema title must be 'aoa-evals eval result receipt'",
                )
            )
            payload_schema_valid = False
        try:
            Draft202012Validator.check_schema(payload_schema)
        except SchemaError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(payload_schema_path, repo_root),
                    f"invalid JSON schema: {exc.message}",
                )
            )
            payload_schema_valid = False
        if payload_schema_valid:
            payload_validator = get_schema_validator_with_format(payload_schema)
    elif payload_schema is not None:
        issues.append(
            ValidationIssue(
                relative_location(payload_schema_path, repo_root),
                "eval result receipt schema must be a JSON object",
            )
        )

    example_payload = load_json_payload(example_path, issues, root=repo_root)
    if isinstance(example_payload, dict):
        if envelope_validator is not None:
            validate_against_schema(
                example_payload,
                STATS_EVENT_ENVELOPE_SCHEMA_NAME,
                relative_location(example_path, repo_root),
                issues,
                validator=envelope_validator,
                fallback_repo_root=repo_root,
            )
        if example_payload.get("event_kind") != "eval_result_receipt":
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "eval result receipt example must keep event_kind as 'eval_result_receipt'",
                )
            )

        object_ref = example_payload.get("object_ref")
        if isinstance(object_ref, dict):
            if object_ref.get("repo") != "aoa-evals":
                issues.append(
                    ValidationIssue(
                        relative_location(example_path, repo_root),
                        "eval result receipt example object_ref.repo must be 'aoa-evals'",
                    )
                )
            if object_ref.get("kind") != "eval_bundle":
                issues.append(
                    ValidationIssue(
                        relative_location(example_path, repo_root),
                        "eval result receipt example object_ref.kind must be 'eval_bundle'",
                    )
                )

        evidence_refs = example_payload.get("evidence_refs")
        seen_primary = False
        if isinstance(evidence_refs, list):
            for index, evidence_ref in enumerate(evidence_refs):
                if not isinstance(evidence_ref, dict):
                    continue
                ref = evidence_ref.get("ref")
                if isinstance(ref, str):
                    parse_repo_ref(
                        ref,
                        location=f"{relative_location(example_path, repo_root)}.evidence_refs[{index}].ref",
                        issues=issues,
                        repo_ref_roots=repo_ref_roots,
                        strict_sibling_compat=strict_sibling_compat,
                    )
                if evidence_ref.get("role") == "primary":
                    seen_primary = True
        if not seen_primary:
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "eval result receipt example must include one primary evidence ref",
                )
            )

        payload = example_payload.get("payload")
        if isinstance(payload, dict):
            if payload_validator is not None:
                validate_against_schema(
                    payload,
                    EVAL_RESULT_RECEIPT_SCHEMA_NAME,
                    f"{relative_location(example_path, repo_root)}.payload",
                    issues,
                    validator=payload_validator,
                    fallback_repo_root=repo_root,
                )
            bundle_ref = payload.get("bundle_ref")
            if isinstance(bundle_ref, str):
                parse_repo_ref(
                    bundle_ref,
                    location=f"{relative_location(example_path, repo_root)}.payload.bundle_ref",
                    issues=issues,
                    repo_ref_roots=repo_ref_roots,
                    strict_sibling_compat=strict_sibling_compat,
                )
            report_ref = payload.get("report_ref")
            if isinstance(report_ref, str):
                parse_repo_ref(
                    report_ref,
                    location=f"{relative_location(example_path, repo_root)}.payload.report_ref",
                    issues=issues,
                    repo_ref_roots=repo_ref_roots,
                    strict_sibling_compat=strict_sibling_compat,
                )
            if (
                isinstance(object_ref, dict)
                and isinstance(payload.get("eval_name"), str)
                and payload["eval_name"] != object_ref.get("id")
            ):
                issues.append(
                    ValidationIssue(
                        relative_location(example_path, repo_root),
                        "eval result receipt example payload.eval_name must match object_ref.id",
                    )
                )
            if (
                isinstance(report_ref, str)
                and isinstance(evidence_refs, list)
                and report_ref not in {entry.get("ref") for entry in evidence_refs if isinstance(entry, dict)}
            ):
                issues.append(
                    ValidationIssue(
                        relative_location(example_path, repo_root),
                        "eval result receipt example payload.report_ref must also appear in evidence_refs",
                    )
                )
            interpretation_bound = payload.get("interpretation_bound")
            if isinstance(interpretation_bound, str) and "Example only." not in interpretation_bound:
                issues.append(
                    ValidationIssue(
                        relative_location(example_path, repo_root),
                        "eval result receipt example interpretation_bound must keep example-only posture explicit",
                    )
                )
        else:
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "eval result receipt example payload must be an object",
                )
            )
    elif example_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(example_path, repo_root),
                "eval result receipt example must be a JSON object",
            )
        )

    return issues


__all__ = (
    "EVAL_RESULT_RECEIPT_EXAMPLE_NAME",
    "EVAL_RESULT_RECEIPT_GUIDE_NAME",
    "EVAL_RESULT_RECEIPT_REQUIRED_TOKENS",
    "validate_eval_result_receipt_surfaces",
)
