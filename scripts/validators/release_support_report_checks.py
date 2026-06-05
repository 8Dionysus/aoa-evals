"""Shared release-support report structure checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping

from validators.common import ValidationIssue
from validators.release_support_refs import parse_repo_ref


def validate_repo_ref_list(
    refs: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
    repo_ref_roots: Mapping[str, Path],
    strict_sibling_compat: bool,
) -> None:
    if not isinstance(refs, list) or not refs:
        issues.append(ValidationIssue(location, "evidence_refs must be a non-empty list"))
        return
    for ref_index, evidence_ref in enumerate(refs):
        parse_repo_ref(
            evidence_ref,
            location=f"{location}[{ref_index}]",
            issues=issues,
            repo_ref_roots=repo_ref_roots,
            strict_sibling_compat=strict_sibling_compat,
        )


def validate_required_object_ids(
    entries: Any,
    *,
    location: str,
    id_key: str,
    required_ids: set[str],
    status_value: str | None,
    min_claim_limit_length: int,
    issues: list[ValidationIssue],
    repo_ref_roots: Mapping[str, Path],
    strict_sibling_compat: bool,
) -> None:
    if not isinstance(entries, list):
        issues.append(ValidationIssue(location, f"{location.rsplit('.', 1)[-1]} must be a list"))
        return
    seen_ids: set[str] = set()
    for index, entry in enumerate(entries):
        entry_location = f"{location}[{index}]"
        if not isinstance(entry, dict):
            issues.append(ValidationIssue(entry_location, f"{id_key.removesuffix('_id')} entry must be an object"))
            continue
        entry_id = entry.get(id_key)
        if isinstance(entry_id, str):
            seen_ids.add(entry_id)
        else:
            issues.append(ValidationIssue(entry_location, f"{id_key} must be a string"))
        if status_value is not None and entry.get("status") != status_value:
            issues.append(ValidationIssue(entry_location, f"status must stay '{status_value}'"))
        if "evidence_refs" in entry:
            validate_repo_ref_list(
                entry.get("evidence_refs"),
                location=f"{entry_location}.evidence_refs",
                issues=issues,
                repo_ref_roots=repo_ref_roots,
                strict_sibling_compat=strict_sibling_compat,
            )
        claim_limit = entry.get("claim_limit")
        if not isinstance(claim_limit, str) or len(claim_limit) < min_claim_limit_length:
            issues.append(ValidationIssue(entry_location, "claim_limit must be a meaningful string"))
    for missing_id in sorted(required_ids - seen_ids):
        issues.append(ValidationIssue(location, f"missing {id_key} {missing_id!r}"))


def validate_verification_snapshot(
    payload: dict[str, Any],
    *,
    location: str,
    required_commands: set[str],
    issues: list[ValidationIssue],
) -> None:
    verification_snapshot = payload.get("verification_snapshot")
    if not isinstance(verification_snapshot, list):
        issues.append(ValidationIssue(location, "verification_snapshot must be a list"))
        return
    seen_commands: set[str] = set()
    for index, entry in enumerate(verification_snapshot):
        entry_location = f"{location}.verification_snapshot[{index}]"
        if not isinstance(entry, dict):
            issues.append(ValidationIssue(entry_location, "verification entry must be an object"))
            continue
        command = entry.get("command")
        if isinstance(command, str):
            seen_commands.add(command)
        else:
            issues.append(ValidationIssue(entry_location, "command must be a string"))
        if entry.get("result") != "passed":
            issues.append(ValidationIssue(entry_location, "result must stay 'passed'"))
        claim_limit = entry.get("claim_limit")
        if not isinstance(claim_limit, str) or len(claim_limit) < 20:
            issues.append(ValidationIssue(entry_location, "claim_limit must be a meaningful string"))
    for command in sorted(required_commands - seen_commands):
        issues.append(
            ValidationIssue(
                f"{location}.verification_snapshot",
                f"missing verification command {command!r}",
            )
        )


def require_joined_list_tokens(
    payload: dict[str, Any],
    *,
    location: str,
    key: str,
    tokens: Iterable[str],
    message_name: str,
    issues: list[ValidationIssue],
) -> None:
    value = payload.get(key)
    if not isinstance(value, list):
        issues.append(ValidationIssue(location, f"{key} must be a list"))
        return
    joined = "\n".join(item for item in value if isinstance(item, str))
    for token in tokens:
        if token not in joined:
            issues.append(ValidationIssue(f"{location}.{key}", f"{message_name} must mention '{token}'"))


def require_claim_limit_tokens(
    payload: dict[str, Any],
    *,
    location: str,
    tokens: Iterable[str],
    issues: list[ValidationIssue],
) -> None:
    claim_limit = payload.get("claim_limit")
    if not isinstance(claim_limit, str):
        issues.append(ValidationIssue(location, "claim_limit must be a string"))
        return
    for token in tokens:
        if token not in claim_limit:
            issues.append(ValidationIssue(location, f"claim_limit must mention '{token}'"))


__all__ = (
    "require_claim_limit_tokens",
    "require_joined_list_tokens",
    "validate_repo_ref_list",
    "validate_required_object_ids",
    "validate_verification_snapshot",
)
