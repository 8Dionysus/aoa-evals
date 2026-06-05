"""Live eval-result receipt JSONL log contracts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

from validators.publication_receipts_common import (
    EVAL_RESULT_RECEIPT_SCHEMA_NAME,
    LIVE_EVAL_RECEIPT_LOG_NAME,
    STATS_EVENT_ENVELOPE_SCHEMA_NAME,
    STATS_EVENT_ENVELOPE_SCHEMA_PATH,
    ValidationIssue,
    get_schema_validator_with_format,
    load_json_payload,
    parse_repo_ref,
    relative_location,
    validate_against_schema,
    validate_inline_schema,
)


def validate_live_receipt_log(
    repo_root: Path,
    *,
    fallback_repo_root: Path,
    repo_ref_roots: Mapping[str, Path],
    strict_sibling_compat: bool,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    log_path = repo_root / LIVE_EVAL_RECEIPT_LOG_NAME
    log_location = relative_location(log_path, repo_root)
    envelope_schema_path = repo_root / STATS_EVENT_ENVELOPE_SCHEMA_PATH
    envelope_schema_location = relative_location(envelope_schema_path, repo_root)
    if envelope_schema_path.exists():
        envelope_schema = load_json_payload(envelope_schema_path, issues, root=repo_root)
    elif repo_root != fallback_repo_root:
        envelope_schema = load_json_payload(
            fallback_repo_root / STATS_EVENT_ENVELOPE_SCHEMA_PATH,
            issues,
            root=fallback_repo_root,
        )
    else:
        envelope_schema = load_json_payload(envelope_schema_path, issues, root=repo_root)
    if not isinstance(envelope_schema, dict):
        if envelope_schema is not None:
            issues.append(
                ValidationIssue(envelope_schema_location, "stats event envelope schema must be a JSON object")
            )
        return issues
    if not validate_inline_schema(envelope_schema, location=envelope_schema_location, issues=issues):
        return issues
    envelope_validator = get_schema_validator_with_format(envelope_schema)
    try:
        raw_lines = log_path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return [ValidationIssue(log_location, "file is missing")]

    receipt_count = 0
    seen_event_ids: set[str] = set()
    for line_number, raw_line in enumerate(raw_lines, start=1):
        line = raw_line.strip()
        if not line:
            continue

        receipt_count += 1
        entry_location = f"{log_location}:{line_number}"
        try:
            receipt = json.loads(line)
        except json.JSONDecodeError as exc:
            issues.append(ValidationIssue(entry_location, f"invalid JSON: {exc.msg}"))
            continue
        if not isinstance(receipt, dict):
            issues.append(
                ValidationIssue(entry_location, "live eval receipt log entry must be a JSON object")
            )
            continue

        validate_against_schema(
            receipt,
            STATS_EVENT_ENVELOPE_SCHEMA_NAME,
            entry_location,
            issues,
            validator=envelope_validator,
            fallback_repo_root=fallback_repo_root,
        )
        if receipt.get("event_kind") != "eval_result_receipt":
            issues.append(
                ValidationIssue(
                    entry_location,
                    "live eval receipt log entry must keep event_kind as 'eval_result_receipt'",
                )
            )

        event_id = receipt.get("event_id")
        if isinstance(event_id, str) and event_id:
            if event_id in seen_event_ids:
                issues.append(
                    ValidationIssue(
                        entry_location,
                        f"duplicate event_id '{event_id}' is not allowed in the live eval receipt log",
                    )
                )
            seen_event_ids.add(event_id)

        object_ref = receipt.get("object_ref")
        if isinstance(object_ref, dict):
            if object_ref.get("repo") != "aoa-evals":
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "live eval receipt log object_ref.repo must be 'aoa-evals'",
                    )
                )
            if object_ref.get("kind") != "eval_bundle":
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "live eval receipt log object_ref.kind must be 'eval_bundle'",
                    )
                )

        evidence_refs = receipt.get("evidence_refs")
        seen_primary = False
        evidence_ref_values: set[str] = set()
        if isinstance(evidence_refs, list):
            for index, evidence_ref in enumerate(evidence_refs):
                if not isinstance(evidence_ref, dict):
                    continue
                raw_ref = evidence_ref.get("ref")
                if isinstance(raw_ref, str):
                    evidence_ref_values.add(raw_ref)
                    parse_repo_ref(
                        raw_ref,
                        location=f"{entry_location}.evidence_refs[{index}].ref",
                        issues=issues,
                        repo_ref_roots=repo_ref_roots,
                        strict_sibling_compat=strict_sibling_compat,
                    )
                if evidence_ref.get("role") == "primary":
                    seen_primary = True
            if not seen_primary:
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "live eval receipt log entry must include one primary evidence ref",
                    )
                )

        payload = receipt.get("payload")
        if isinstance(payload, dict):
            validate_against_schema(
                payload,
                EVAL_RESULT_RECEIPT_SCHEMA_NAME,
                f"{entry_location}.payload",
                issues,
                fallback_repo_root=fallback_repo_root,
            )

            bundle_ref = payload.get("bundle_ref")
            if isinstance(bundle_ref, str):
                parse_repo_ref(
                    bundle_ref,
                    location=f"{entry_location}.payload.bundle_ref",
                    issues=issues,
                    repo_ref_roots=repo_ref_roots,
                    strict_sibling_compat=strict_sibling_compat,
                )
                if bundle_ref not in evidence_ref_values:
                    issues.append(
                        ValidationIssue(
                            entry_location,
                            "live eval receipt log payload.bundle_ref must also appear in evidence_refs",
                        )
                    )

            report_ref = payload.get("report_ref")
            if isinstance(report_ref, str):
                parse_repo_ref(
                    report_ref,
                    location=f"{entry_location}.payload.report_ref",
                    issues=issues,
                    repo_ref_roots=repo_ref_roots,
                    strict_sibling_compat=strict_sibling_compat,
                )
                if report_ref not in evidence_ref_values:
                    issues.append(
                        ValidationIssue(
                            entry_location,
                            "live eval receipt log payload.report_ref must also appear in evidence_refs",
                        )
                    )

            if (
                isinstance(object_ref, dict)
                and isinstance(payload.get("eval_name"), str)
                and payload["eval_name"] != object_ref.get("id")
            ):
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "live eval receipt log payload.eval_name must match object_ref.id",
                    )
                )

            if (
                isinstance(object_ref, dict)
                and isinstance(object_ref.get("version"), str)
                and isinstance(payload.get("bundle_status"), str)
                and payload["bundle_status"] != object_ref["version"]
            ):
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "live eval receipt log payload.bundle_status must match object_ref.version when version is present",
                    )
                )

    if receipt_count == 0:
        issues.append(
            ValidationIssue(
                log_location,
                "live eval receipt log must contain at least one receipt entry",
            )
        )
    return issues
