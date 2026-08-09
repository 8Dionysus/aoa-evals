#!/usr/bin/env python3
"""Materialize one honest live-evidence packet without issuing a proof verdict."""

from __future__ import annotations

import argparse
import base64
import binascii
import errno
import hashlib
import json
import os
import re
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from run_scenarios import validate_packet


MAX_INPUT_BYTES = 2 * 1024 * 1024
IDENTIFIER = re.compile(r"^[a-z0-9][a-z0-9._-]{1,127}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
FORBIDDEN_KEYS = frozenset(
    {
        "access_token",
        "api_key",
        "authorization",
        "bearer",
        "client_secret",
        "credential",
        "credentials",
        "passphrase",
        "password",
        "private_key",
        "refresh_token",
        "secret",
        "token",
    }
)
SECRET_KEY_MARKERS = frozenset(
    {
        "api_key",
        "bearer",
        "client_secret",
        "credential",
        "credentials",
        "passphrase",
        "password",
        "private_key",
        "secret",
        "secrets",
        "token",
    }
)
SAFE_SECURITY_METADATA_KEYS = frozenset(
    {
        "contains_secrets",
        "credential_class",
        "credential_contours",
        "last_known_good_credential_class",
    }
)
CANARY_CLAIM_LIMIT = (
    "This stack-issued receipt proves one authenticated loopback MCP "
    "schema observation and bounded read canary only. It does not prove "
    "owner grounding, owner freshness, owner acceptance, central proof, "
    "admission, or rollback."
)
CANARY_V3_CLAIM_LIMIT = (
    "This stack-issued receipt proves one authenticated loopback MCP "
    "schema observation, bounded read canary, and exact named-systemd "
    "process identity unchanged across the probe only. It does not prove "
    "owner grounding, owner freshness, owner acceptance, central proof, "
    "admission, or rollback."
)
RESULT_ARTIFACT_CLAIM_LIMIT = (
    "This private artifact preserves one bounded MCP canary result for "
    "independent owner review. Stack capture and content addressing do "
    "not prove owner grounding, freshness, acceptance, central proof, "
    "admission, or rollback."
)
OWNER_REVIEW_CLAIM_LIMIT = (
    "This owner-issued review proves only the named owner's schema "
    "grounding and freshness assessment for one content-addressed "
    "captured result. It does not prove owner acceptance, central proof, "
    "admission, cross-organ benefit, execution authorization, or rollback."
)
OWNER_REVIEW_KEYS = frozenset(
    {
        "schema_version",
        "review_owner",
        "organ_id",
        "capability_id",
        "primitive_id",
        "owners",
        "capture",
        "source_revision",
        "owner_payload_schema_ref",
        "owner_payload_schema_digest",
        "reviewed_at",
        "expires_at",
        "grounding_state",
        "freshness_state",
        "freshness_policy",
        "provider_watermark",
        "grounding_evidence",
        "reason_codes",
        "owner_accepted",
        "central_proof_asserted",
        "admission_asserted",
        "cross_organ_proven",
        "rollback_proven",
        "contains_secrets",
        "self_report_is_security_authority",
        "claim_limit",
        "review_id",
    }
)
OWNER_KEYS = frozenset(
    {
        "source_owner",
        "access_owner",
        "control_owner",
        "runtime_owner",
        "proof_owner",
        "acceptance_owner",
    }
)
CAPTURE_KEYS = frozenset(
    {
        "capture_owner",
        "capture_receipt_ref",
        "capture_receipt_id",
        "result_artifact_ref",
        "result_artifact_id",
        "organ_id",
        "capability_id",
        "primitive_id",
        "result_digest",
        "result_schema_identity",
        "server_schema_digest",
        "primitive_schema_digest",
        "observed_at",
        "expires_at",
    }
)
FRESHNESS_POLICY_KEYS = frozenset(
    {
        "policy_id",
        "max_age_seconds",
        "stale_readable_seconds",
        "cache_scope",
        "provider_watermark_required",
    }
)
MATURITY_AXES = (
    "declared",
    "owner_reviewed",
    "packaged",
    "exported",
    "deployed",
    "process_alive",
    "endpoint_ready",
    "registry_indexed",
    "consumer_registered",
    "schema_observed",
    "call_succeeded",
    "result_grounded",
    "freshness_satisfied",
    "owner_accepted",
    "cross_organ_proven",
    "rollback_proven",
)


class LivePacketError(ValueError):
    """Bounded materialization failure without private payload content."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def sdk_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def parse_time(value: Any, label: str) -> datetime:
    if not isinstance(value, str):
        raise LivePacketError(f"{label} must be an RFC 3339 timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise LivePacketError(f"{label} must be an RFC 3339 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise LivePacketError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def require_no_symlink_components(path: Path, label: str) -> Path:
    absolute = path.expanduser().absolute()
    for component in tuple(reversed(absolute.parents)) + (absolute,):
        if (component.exists() or component.is_symlink()) and component.is_symlink():
            raise LivePacketError(f"{label} cannot traverse a symlink")
    return absolute


def is_secret_key(value: Any) -> bool:
    canonical = re.sub(r"[^a-z0-9]", "_", str(value).casefold()).strip("_")
    if canonical in SAFE_SECURITY_METADATA_KEYS:
        return False
    if canonical in FORBIDDEN_KEYS:
        return True
    return any(
        canonical == marker
        or canonical.startswith(marker + "_")
        or canonical.endswith("_" + marker)
        or ("_" + marker + "_") in canonical
        for marker in SECRET_KEY_MARKERS
    )


def reject_secret_material(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if is_secret_key(key):
                raise LivePacketError(f"secret-bearing key is forbidden at {path}")
            reject_secret_material(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_secret_material(child, f"{path}[{index}]")
    elif isinstance(value, str) and value.lstrip().casefold().startswith(
        ("bearer ", "basic ")
    ):
        raise LivePacketError(f"secret-like value is forbidden at {path}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise LivePacketError("JSON input contains a duplicate object key")
        result[key] = value
    return result


def read_json(
    path: Path,
    label: str,
    *,
    require_private: bool = False,
) -> tuple[dict[str, Any], bytes]:
    path = require_no_symlink_components(path, label)
    try:
        descriptor = os.open(
            path,
            os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | getattr(os, "O_NONBLOCK", 0),
        )
        try:
            metadata = os.fstat(descriptor)
            if not stat.S_ISREG(metadata.st_mode):
                raise LivePacketError(f"{label} must be a regular non-symlink file")
            if require_private and stat.S_IMODE(metadata.st_mode) & 0o077:
                raise LivePacketError(f"{label} must not be group/world accessible")
            if metadata.st_size > MAX_INPUT_BYTES:
                raise LivePacketError(f"{label} exceeds the 2 MiB limit")
            chunks: list[bytes] = []
            remaining = MAX_INPUT_BYTES + 1
            while remaining:
                chunk = os.read(descriptor, min(65_536, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            raw = b"".join(chunks)
        finally:
            os.close(descriptor)
    except OSError as exc:
        if exc.errno == errno.ELOOP:
            raise LivePacketError(
                f"{label} must be a regular non-symlink file"
            ) from exc
        raise LivePacketError(f"{label} is unavailable") from exc
    if len(raw) > MAX_INPUT_BYTES:
        raise LivePacketError(f"{label} exceeds the 2 MiB limit")
    try:
        payload = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=unique_object,
        )
    except (UnicodeError, json.JSONDecodeError, LivePacketError) as exc:
        raise LivePacketError(f"{label} contains malformed JSON") from exc
    if not isinstance(payload, dict):
        raise LivePacketError(f"{label} must contain one JSON object")
    reject_secret_material(payload)
    return payload, raw


def required_string(
    value: Any,
    label: str,
    *,
    identifier: bool = False,
) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise LivePacketError(f"{label} must be a non-empty string")
    if identifier and IDENTIFIER.fullmatch(value) is None:
        raise LivePacketError(f"{label} must be a bounded identifier")
    return value


def required_digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or DIGEST.fullmatch(value) is None:
        raise LivePacketError(f"{label} must be a sha256 digest")
    return value


def write_private_json(path: Path, payload: dict[str, Any]) -> None:
    path = require_no_symlink_components(path, "live proof packet output")
    parent = require_no_symlink_components(
        path.parent,
        "live proof packet output root",
    )
    parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    parent = require_no_symlink_components(
        parent,
        "live proof packet output root",
    )
    if not parent.is_dir():
        raise LivePacketError("live proof packet output root must be a directory")
    if stat.S_IMODE(parent.stat().st_mode) & 0o077:
        raise LivePacketError(
            "live proof packet output root must not be group/world accessible"
        )
    if path.exists() and (path.is_symlink() or not path.is_file()):
        raise LivePacketError(
            "live proof packet output must be a regular non-symlink file"
        )
    content = (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
        directory_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        temporary.unlink(missing_ok=True)


def deployment_receipt(
    path: Path,
) -> tuple[dict[str, Any], Path]:
    payload, raw = read_json(path, "deployment manifest")
    if (
        payload.get("schema_version") != "abyss_stack_mcp_deployment_manifest_v1"
        or payload.get("digest_scope") != "abyss_stack_mcp_deployment_body_v1"
        or payload.get("provider") != "abyss-stack"
        or payload.get("contains_secrets") is not False
        or payload.get("parity_state") != "exact"
    ):
        raise LivePacketError(
            "deployment manifest is not an exact secret-free stack receipt"
        )
    unsigned = {
        key: value
        for key, value in payload.items()
        if key not in {"manifest_id", "record_ref", "latest_ref"}
    }
    expected = digest(unsigned)
    expected_ref = (
        "Logs/mcp/deployments/records/" + expected.removeprefix("sha256:") + ".json"
    )
    if (
        payload.get("manifest_id") != expected
        or payload.get("record_ref") != expected_ref
        or payload.get("latest_ref") != "Logs/mcp/deployments/latest.json"
    ):
        raise LivePacketError("deployment manifest content address is invalid")
    record_path = path.parent / "records" / Path(expected_ref).name
    _, record_raw = read_json(record_path, "immutable deployment record")
    if raw != record_raw:
        raise LivePacketError(
            "latest deployment manifest differs from its immutable record"
        )
    return payload, record_path


def canary_receipt(path: Path) -> dict[str, Any]:
    payload, _ = read_json(
        path,
        "canary receipt",
        require_private=True,
    )
    schema_version = payload.get("schema_version")
    if (
        schema_version
        not in {
            "abyss_stack_mcp_canary_receipt_v1",
            "abyss_stack_mcp_canary_receipt_v2",
            "abyss_stack_mcp_canary_receipt_v3",
        }
        or payload.get("issuer") != "abyss-stack"
        or payload.get("consumer_id") != "abyss-stack-mcp-canary"
        or payload.get("policy_family") != "read"
        or payload.get("contains_secrets") is not False
        or payload.get("content_trust") != "untrusted_data"
        or payload.get("instruction_authority") != "none"
        or payload.get("claim_limit")
        != (
            CANARY_V3_CLAIM_LIMIT
            if schema_version == "abyss_stack_mcp_canary_receipt_v3"
            else CANARY_CLAIM_LIMIT
        )
    ):
        raise LivePacketError(
            "canary input is not a stack-issued secret-free read receipt"
        )
    for field in (
        "organ_id",
        "service_id",
        "tool_name",
    ):
        required_string(
            payload.get(field),
            f"canary {field}",
            identifier=True,
        )
    for field in (
        "endpoint_ref",
        "canary_route",
        "protocol_version",
        "server_name",
        "server_version",
    ):
        required_string(payload.get(field), f"canary {field}")
    for field in (
        "receipt_id",
        "tool_arguments_digest",
        "server_schema_digest",
        "selected_tool_schema_digest",
    ):
        required_digest(payload.get(field), f"canary {field}")
    parsed_endpoint = urlsplit(payload["endpoint_ref"])
    if (
        parsed_endpoint.scheme not in {"http", "https"}
        or parsed_endpoint.hostname not in {"127.0.0.1", "localhost", "::1"}
        or parsed_endpoint.username is not None
        or parsed_endpoint.password is not None
        or parsed_endpoint.query
        or parsed_endpoint.fragment
    ):
        raise LivePacketError("canary endpoint must be a loopback HTTP URL")
    try:
        port = parsed_endpoint.port
    except ValueError as exc:
        raise LivePacketError("canary endpoint has an invalid port") from exc
    if port is not None and not 1 <= port <= 65_535:
        raise LivePacketError("canary endpoint has an invalid port")
    observed_at = parse_time(payload.get("observed_at"), "canary observed_at")
    expires_at = parse_time(payload.get("expires_at"), "canary expires_at")
    if expires_at <= observed_at:
        raise LivePacketError("canary expiry must follow observation")
    inventory = payload.get("inventory_counts")
    if (
        not isinstance(inventory, dict)
        or set(inventory) != {"tools", "resources", "resource_templates", "prompts"}
        or any(
            not isinstance(value, int)
            or isinstance(value, bool)
            or not 0 <= value <= 10_000
            for value in inventory.values()
        )
    ):
        raise LivePacketError("canary inventory counts are invalid")
    for field in ("call_latency_ms", "total_latency_ms"):
        value = payload.get(field)
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
            or not 0 <= value <= 3_600_000
        ):
            raise LivePacketError(f"canary {field} is invalid")
    call_succeeded = payload.get("call_succeeded")
    contract_matched = payload.get("result_contract_matched")
    if not isinstance(call_succeeded, bool) or not isinstance(
        contract_matched,
        bool,
    ):
        raise LivePacketError("canary result states must be booleans")
    reasons = payload.get("reason_codes")
    if (
        not isinstance(reasons, list)
        or any(
            not isinstance(reason, str) or IDENTIFIER.fullmatch(reason) is None
            for reason in reasons
        )
        or len(reasons) != len(set(reasons))
    ):
        raise LivePacketError("canary reason codes are invalid")
    if contract_matched and (not call_succeeded or reasons):
        raise LivePacketError("matching canary contract has contradictory result state")
    if not contract_matched and not reasons:
        raise LivePacketError("non-matching canary contract requires reason codes")
    if call_succeeded:
        required_string(
            payload.get("result_schema_identity"),
            "canary result_schema_identity",
        )
        required_digest(
            payload.get("result_digest"),
            "canary result_digest",
        )
        result_artifact_ref = required_string(
            payload.get("result_artifact_ref"),
            "canary result_artifact_ref",
        )
        expected_artifact_ref = (
            f"results/{payload['organ_id']}/"
            f"{payload['result_digest'].removeprefix('sha256:')}.json"
        )
        if result_artifact_ref != expected_artifact_ref:
            raise LivePacketError(
                "canary result artifact ref does not match result digest"
            )
    elif payload.get("result_artifact_ref") is not None:
        raise LivePacketError("failed canary cannot reference a result artifact")
    if schema_version in {
        "abyss_stack_mcp_canary_receipt_v2",
        "abyss_stack_mcp_canary_receipt_v3",
    }:
        validate_attestation_fields(payload, "canary receipt")
    if schema_version == "abyss_stack_mcp_canary_receipt_v3":
        for field in (
            "deployment_manifest_id",
            "deployment_package_digest",
            "deployment_tree_digest",
        ):
            required_digest(payload.get(field), f"canary {field}")
        for field in (
            "deployment_service_id",
            "deployment_source_revision",
            "deployment_deployed_at",
        ):
            required_string(payload.get(field), f"canary {field}")
        parse_time(
            payload.get("deployment_deployed_at"),
            "canary deployment_deployed_at",
        )
        process_identity = required_string(
            payload.get("process_identity"),
            "canary process_identity",
        )
        process_identity_before = required_string(
            payload.get("process_identity_before"),
            "canary process_identity_before",
        )
        process_identity_after = required_string(
            payload.get("process_identity_after"),
            "canary process_identity_after",
        )
        if not (
            process_identity_before
            == process_identity_after
            == process_identity
        ):
            raise LivePacketError(
                "v3 canary process identity changed across the probe"
            )
    unsigned = {
        key: value
        for key, value in payload.items()
        if key != "receipt_id"
        and not (
            schema_version
            in {
                "abyss_stack_mcp_canary_receipt_v2",
                "abyss_stack_mcp_canary_receipt_v3",
            }
            and key == "attestation"
        )
    }
    if payload.get("receipt_id") != digest(unsigned):
        raise LivePacketError("canary receipt content address is invalid")
    return payload


def validate_attestation_fields(payload: dict[str, Any], label: str) -> None:
    signer_id = payload.get("signer_id")
    required_digest(signer_id, f"{label} signer_id")
    if payload.get("attestation_algorithm") != "ed25519":
        raise LivePacketError(f"{label} attestation algorithm is unsupported")
    encoded = payload.get("attestation")
    if not isinstance(encoded, str):
        raise LivePacketError(f"{label} attestation is unavailable")
    try:
        attestation = base64.b64decode(
            encoded + ("=" * (-len(encoded) % 4)),
            altchars=b"-_",
            validate=True,
        )
    except (ValueError, binascii.Error) as exc:
        raise LivePacketError(f"{label} attestation is malformed") from exc
    if len(attestation) != 64:
        raise LivePacketError(f"{label} attestation is malformed")


def canary_result_artifact(
    path: Path | None,
    *,
    canary: dict[str, Any],
    canary_path: Path,
) -> dict[str, Any] | None:
    if canary.get("call_succeeded") is not True:
        if path is not None:
            raise LivePacketError("failed canary cannot supply a result artifact")
        return None
    if path is None:
        raise LivePacketError("successful canary requires its private result artifact")
    expected_path = canary_path.absolute().parents[2] / str(
        canary["result_artifact_ref"]
    )
    if path.absolute() != expected_path:
        raise LivePacketError("result artifact path does not match canary receipt")
    payload, _ = read_json(
        path,
        "canary result artifact",
        require_private=True,
    )
    canary_version = canary.get("schema_version")
    expected_artifact_version = (
        "abyss_stack_mcp_canary_result_artifact_v2"
        if canary_version
        in {
            "abyss_stack_mcp_canary_receipt_v2",
            "abyss_stack_mcp_canary_receipt_v3",
        }
        else "abyss_stack_mcp_canary_result_artifact_v1"
    )
    if (
        payload.get("schema_version") != expected_artifact_version
        or payload.get("issuer") != "abyss-stack"
        or payload.get("organ_id") != canary.get("organ_id")
        or payload.get("policy_family") != "read"
        or payload.get("service_id") != canary.get("service_id")
        or payload.get("canary_route") != canary.get("canary_route")
        or payload.get("tool_name") != canary.get("tool_name")
        or payload.get("tool_arguments_digest") != canary.get("tool_arguments_digest")
        or payload.get("result_schema_identity") != canary.get("result_schema_identity")
        or payload.get("result_digest") != canary.get("result_digest")
        or payload.get("contains_secrets") is not False
        or payload.get("content_trust") != "untrusted_data"
        or payload.get("instruction_authority") != "none"
        or payload.get("claim_limit") != RESULT_ARTIFACT_CLAIM_LIMIT
    ):
        raise LivePacketError("result artifact does not bind the canary receipt")
    if parse_time(
        payload.get("observed_at"),
        "result artifact observed_at",
    ) != parse_time(canary.get("observed_at"), "canary observed_at"):
        raise LivePacketError("result artifact time does not bind the canary receipt")
    owner_payload = payload.get("owner_payload")
    if not isinstance(owner_payload, dict):
        raise LivePacketError("result artifact owner payload must be an object")
    if digest(owner_payload) != canary.get("result_digest"):
        raise LivePacketError("result artifact owner payload digest is invalid")
    if canary_version in {
        "abyss_stack_mcp_canary_receipt_v2",
        "abyss_stack_mcp_canary_receipt_v3",
    }:
        validate_attestation_fields(payload, "result artifact")
        if payload.get("signer_id") != canary.get("signer_id"):
            raise LivePacketError("result artifact signer does not match canary receipt")
    unsigned = {
        key: value
        for key, value in payload.items()
        if key != "artifact_id"
        and not (
            canary_version
            in {
                "abyss_stack_mcp_canary_receipt_v2",
                "abyss_stack_mcp_canary_receipt_v3",
            }
            and key == "attestation"
        )
    }
    if payload.get("artifact_id") != digest(unsigned):
        raise LivePacketError("result artifact content address is invalid")
    return payload


def owner_result_review(
    path: Path | None,
    *,
    record: dict[str, Any],
    canary: dict[str, Any],
    canary_path: Path,
    result_artifact: dict[str, Any] | None,
    result_path: Path | None,
    materialized_at: datetime,
) -> tuple[
    dict[str, Any] | None,
    dict[str, Any] | None,
    dict[str, Any] | None,
]:
    if path is None:
        return None, None, None
    if result_artifact is None or result_path is None:
        raise LivePacketError(
            "owner review requires a successful captured result artifact"
        )
    review, _ = read_json(path, "owner result review", require_private=True)
    if set(review) != OWNER_REVIEW_KEYS:
        raise LivePacketError(
            "owner review fields differ from the SDK v1 receipt contract"
        )
    if (
        review.get("schema_version") != "aoa_organ_owner_result_review_v1"
        or review.get("contains_secrets") is not False
        or review.get("self_report_is_security_authority") is not False
        or review.get("claim_limit") != OWNER_REVIEW_CLAIM_LIMIT
    ):
        raise LivePacketError(
            "owner review is not a bounded secret-free SDK v1 receipt"
        )
    for field in (
        "owner_accepted",
        "central_proof_asserted",
        "admission_asserted",
        "cross_organ_proven",
        "rollback_proven",
    ):
        if review.get(field) is not False:
            raise LivePacketError(
                f"owner review cannot assert {field.replace('_', ' ')}"
            )
    unsigned = {key: value for key, value in review.items() if key != "review_id"}
    if review.get("review_id") != sdk_digest(unsigned):
        raise LivePacketError("owner review content address is invalid")

    owners = record.get("owners")
    review_owners = review.get("owners")
    if (
        not isinstance(owners, dict)
        or set(owners) != OWNER_KEYS
        or not isinstance(review_owners, dict)
        or set(review_owners) != OWNER_KEYS
        or review_owners != owners
    ):
        raise LivePacketError(
            "owner review roles differ from the private registry source"
        )
    review_owner = required_string(
        review.get("review_owner"),
        "owner review review_owner",
        identifier=True,
    )
    if review_owner not in {
        owners.get("source_owner"),
        owners.get("acceptance_owner"),
    }:
        raise LivePacketError(
            "result review owner is not the source or acceptance owner"
        )

    organ_id = required_string(
        review.get("organ_id"),
        "owner review organ_id",
        identifier=True,
    )
    capability_id = required_string(
        review.get("capability_id"),
        "owner review capability_id",
        identifier=True,
    )
    primitive_id = required_string(
        review.get("primitive_id"),
        "owner review primitive_id",
        identifier=True,
    )
    if organ_id != canary.get("organ_id"):
        raise LivePacketError("owner review organ does not bind the canary")

    capabilities = record.get("capabilities")
    if not isinstance(capabilities, list):
        raise LivePacketError(
            "registry lacks capability contracts for owner review binding"
        )
    selected_capabilities = [
        capability
        for capability in capabilities
        if isinstance(capability, dict)
        and capability.get("capability_id") == capability_id
        and capability.get("policy_family") == "read"
    ]
    if len(selected_capabilities) != 1:
        raise LivePacketError(
            "owner review capability does not bind one registry read contract"
        )
    capability = selected_capabilities[0]
    primitives = capability.get("primitives")
    if not isinstance(primitives, list):
        raise LivePacketError(
            "owner review capability has no registry primitive contracts"
        )
    selected_primitives = [
        primitive
        for primitive in primitives
        if isinstance(primitive, dict)
        and primitive.get("primitive_id") == primitive_id
        and primitive.get("policy_family") == "read"
        and primitive.get("effect_class") in {"observe", "derive", "validate"}
    ]
    if len(selected_primitives) != 1:
        raise LivePacketError(
            "owner review primitive does not bind one registry read primitive"
        )
    primitive = selected_primitives[0]
    owner_schema_ref = required_string(
        review.get("owner_payload_schema_ref"),
        "owner review owner_payload_schema_ref",
    )
    if owner_schema_ref != capability.get("owner_payload_schema_ref"):
        raise LivePacketError(
            "owner review payload schema identity differs from registry"
        )
    owner_schema_digest = required_digest(
        review.get("owner_payload_schema_digest"),
        "owner review owner_payload_schema_digest",
    )

    capture = review.get("capture")
    if not isinstance(capture, dict) or set(capture) != CAPTURE_KEYS:
        raise LivePacketError("owner review capture differs from the SDK v1 contract")
    if (
        capture.get("capture_owner") != owners.get("runtime_owner")
        or capture.get("capture_owner") != "abyss-stack"
        or (
            capture.get("organ_id"),
            capture.get("capability_id"),
            capture.get("primitive_id"),
        )
        != (organ_id, capability_id, primitive_id)
    ):
        raise LivePacketError(
            "owner review target does not bind the runtime-owner capture"
        )
    capture_root = canary_path.absolute().parents[2]
    try:
        canary_ref = canary_path.absolute().relative_to(capture_root).as_posix()
        artifact_ref = result_path.absolute().relative_to(capture_root).as_posix()
    except ValueError as exc:
        raise LivePacketError(
            "canary inputs are outside their private capture root"
        ) from exc
    expected_capture = {
        "capture_receipt_ref": canary_ref,
        "capture_receipt_id": canary.get("receipt_id"),
        "result_artifact_ref": artifact_ref,
        "result_artifact_id": result_artifact.get("artifact_id"),
        "result_digest": canary.get("result_digest"),
        "result_schema_identity": canary.get("result_schema_identity"),
        "server_schema_digest": canary.get("server_schema_digest"),
        "primitive_schema_digest": canary.get("selected_tool_schema_digest"),
    }
    for field, expected in expected_capture.items():
        if capture.get(field) != expected:
            raise LivePacketError(
                f"owner review capture {field} does not bind stack evidence"
            )
    capture_observed_at = parse_time(
        capture.get("observed_at"),
        "owner review capture observed_at",
    )
    capture_expires_at = parse_time(
        capture.get("expires_at"),
        "owner review capture expires_at",
    )
    canary_observed_at = parse_time(
        canary.get("observed_at"),
        "canary observed_at",
    )
    canary_expires_at = parse_time(
        canary.get("expires_at"),
        "canary expires_at",
    )
    if (
        capture_observed_at != canary_observed_at
        or capture_expires_at != canary_expires_at
    ):
        raise LivePacketError("owner review capture window does not bind the canary")

    source_revision_block = review.get("source_revision")
    registry_revisions = record.get("revisions")
    registry_source = (
        registry_revisions.get("source")
        if isinstance(registry_revisions, dict)
        else None
    )
    if (
        not isinstance(source_revision_block, dict)
        or set(source_revision_block)
        not in (
            {"revision", "schema_digest"},
            {"revision", "digest", "schema_digest"},
        )
        or not isinstance(registry_source, dict)
        or source_revision_block.get("revision") != registry_source.get("revision")
        or source_revision_block.get("schema_digest") != owner_schema_digest
    ):
        raise LivePacketError(
            "owner review source/schema revision differs from registry binding"
        )
    if (
        "digest" in source_revision_block
        and source_revision_block["digest"] is not None
    ):
        required_digest(
            source_revision_block["digest"],
            "owner review source digest",
        )

    reviewed_at = parse_time(review.get("reviewed_at"), "owner review reviewed_at")
    expires_at = parse_time(review.get("expires_at"), "owner review expires_at")
    if (
        reviewed_at < capture_observed_at
        or reviewed_at > materialized_at
        or expires_at <= materialized_at
        or expires_at > capture_expires_at
    ):
        raise LivePacketError(
            "owner review is outside the captured live evidence window"
        )
    freshness_policy = review.get("freshness_policy")
    if (
        not isinstance(freshness_policy, dict)
        or set(freshness_policy) != FRESHNESS_POLICY_KEYS
    ):
        raise LivePacketError("owner review freshness policy is invalid")
    required_string(
        freshness_policy.get("policy_id"),
        "owner review freshness policy_id",
        identifier=True,
    )
    max_age_seconds = freshness_policy.get("max_age_seconds")
    stale_readable_seconds = freshness_policy.get("stale_readable_seconds")
    if (
        not isinstance(max_age_seconds, int)
        or isinstance(max_age_seconds, bool)
        or max_age_seconds <= 0
        or not isinstance(stale_readable_seconds, int)
        or isinstance(stale_readable_seconds, bool)
        or stale_readable_seconds < 0
        or freshness_policy.get("cache_scope")
        not in {"none", "request", "task", "agent", "workspace"}
        or not isinstance(
            freshness_policy.get("provider_watermark_required"),
            bool,
        )
        or (expires_at - reviewed_at).total_seconds() > max_age_seconds
    ):
        raise LivePacketError("owner review freshness policy is invalid")

    grounding_state = review.get("grounding_state")
    freshness_state = review.get("freshness_state")
    if grounding_state not in {"grounded", "rejected", "blocked"}:
        raise LivePacketError("owner review grounding state is invalid")
    if freshness_state not in {
        "exact",
        "compatible_drift",
        "stale_readable",
        "blocked",
        "unknown",
    }:
        raise LivePacketError("owner review freshness state is invalid")
    reason_codes = review.get("reason_codes")
    if (
        not isinstance(reason_codes, list)
        or any(
            not isinstance(reason, str) or IDENTIFIER.fullmatch(reason) is None
            for reason in reason_codes
        )
        or len(reason_codes) != len(set(reason_codes))
        or (
            (grounding_state != "grounded" or freshness_state != "exact")
            and not reason_codes
        )
    ):
        raise LivePacketError("owner review reason codes are invalid")
    provider_watermark = review.get("provider_watermark")
    if provider_watermark is not None:
        required_string(
            provider_watermark,
            "owner review provider_watermark",
        )
    if (
        freshness_state in {"exact", "compatible_drift", "stale_readable"}
        and freshness_policy["provider_watermark_required"]
        and provider_watermark is None
    ):
        raise LivePacketError("owner review freshness requires a provider watermark")

    grounding_evidence = review.get("grounding_evidence")
    if not isinstance(grounding_evidence, list):
        raise LivePacketError("owner review grounding evidence is invalid")
    if grounding_state == "grounded" and not grounding_evidence:
        raise LivePacketError("grounded owner review lacks owner-qualified evidence")
    allowed_evidence_owners = {
        review_owner,
        owners.get("source_owner"),
        owners.get("acceptance_owner"),
    }
    seen_evidence: set[tuple[str, str, str]] = set()
    for index, evidence in enumerate(grounding_evidence):
        if (
            not isinstance(evidence, dict)
            or not {"owner", "evidence_ref", "revision", "observed_at"} <= set(evidence)
            or not set(evidence)
            <= {
                "owner",
                "evidence_ref",
                "revision",
                "observed_at",
                "expires_at",
            }
            or evidence.get("owner") not in allowed_evidence_owners
            or evidence.get("revision") != source_revision_block["revision"]
        ):
            raise LivePacketError(
                f"owner review grounding evidence {index} is not owner-qualified"
            )
        evidence_ref = required_string(
            evidence.get("evidence_ref"),
            f"owner review grounding evidence {index} ref",
        )
        evidence_observed_at = parse_time(
            evidence.get("observed_at"),
            f"owner review grounding evidence {index} observed_at",
        )
        if evidence_observed_at > reviewed_at:
            raise LivePacketError(
                "owner review grounding evidence cannot postdate review"
            )
        if evidence.get("expires_at") is not None:
            evidence_expiry = parse_time(
                evidence["expires_at"],
                f"owner review grounding evidence {index} expires_at",
            )
            if evidence_expiry <= materialized_at:
                raise LivePacketError("owner review grounding evidence is expired")
        identity = (
            str(evidence["owner"]),
            evidence_ref,
            str(evidence["revision"]),
        )
        if identity in seen_evidence:
            raise LivePacketError("owner review grounding evidence contains duplicates")
        seen_evidence.add(identity)
    if (
        grounding_state == "grounded"
        and canary.get("result_contract_matched") is not True
    ):
        raise LivePacketError(
            "grounded owner review cannot override a mismatched canary contract"
        )
    return review, capability, primitive


def registry_record(
    registry: dict[str, Any],
    organ_id: str,
    materialized_at: datetime,
) -> tuple[dict[str, Any], str, str, datetime]:
    schema_version = registry.get("schema_version")
    if (
        schema_version
        not in {"aoa_organ_registry_source_v1", "aoa_organ_registry_source_v2"}
        or registry.get("contains_secrets") is not False
        or registry.get("default_admission") != "deny"
    ):
        raise LivePacketError(
            "registry input is not a deny-by-default secret-free source"
        )
    expires_at = parse_time(registry.get("expires_at"), "registry expires_at")
    if expires_at <= materialized_at:
        raise LivePacketError("registry source is expired")
    parse_time(registry.get("authored_at"), "registry authored_at")
    required_string(
        registry.get("registry_id"),
        "registry registry_id",
        identifier=True,
    )
    required_string(
        registry.get("workspace_owner"),
        "registry workspace_owner",
        identifier=True,
    )
    records = registry.get("records")
    if not isinstance(records, list):
        raise LivePacketError("registry records are invalid")
    organ_ids = [
        record.get("organ_id") for record in records if isinstance(record, dict)
    ]
    if (
        len(organ_ids) != len(records)
        or any(
            not isinstance(value, str) or IDENTIFIER.fullmatch(value) is None
            for value in organ_ids
        )
        or len(organ_ids) != len(set(organ_ids))
    ):
        raise LivePacketError("registry organ identities are invalid")
    selected = [
        record
        for record in records
        if isinstance(record, dict) and record.get("organ_id") == organ_id
    ]
    if len(selected) != 1:
        raise LivePacketError("registry must contain one exact organ record")
    selected_record = selected[0]
    if schema_version == "aoa_organ_registry_source_v2":
        contours = selected_record.get("contours")
        selected_contours = [
            contour
            for contour in contours
            if isinstance(contour, dict)
            and contour.get("contour_id") == "read"
            and contour.get("policy_family") == "read"
        ] if isinstance(contours, list) else []
        if len(selected_contours) != 1:
            raise LivePacketError(
                "v2 registry must contain one exact organ/read contour"
            )
        contour = selected_contours[0]
        selected_record = {
            **selected_record,
            "registry_state": contour.get("registry_state"),
            "revisions": contour.get("revisions"),
            "maturity": contour.get("maturity"),
            "capabilities": contour.get("capabilities"),
            "credential_class": contour.get("credential_class"),
        }
        record_digest = digest(contour)
    else:
        record_digest = digest(selected_record)
    return (
        selected_record,
        record_digest,
        digest(registry),
        expires_at,
    )


def require_v3_deployment_binding(
    canary: dict[str, Any],
    deployment: dict[str, Any],
    service: dict[str, Any],
) -> None:
    if canary.get("schema_version") != "abyss_stack_mcp_canary_receipt_v3":
        return
    deployed_tree = service.get("deployed_tree")
    if not isinstance(deployed_tree, dict):
        raise LivePacketError("v3 canary deployment tree binding is unavailable")
    expected = {
        "deployment_manifest_id": deployment.get("manifest_id"),
        "deployment_service_id": service.get("service_id"),
        "deployment_source_revision": service.get("package_source_revision"),
        "deployment_package_digest": service.get("package_digest"),
        "deployment_tree_digest": deployed_tree.get("tree_digest"),
    }
    if any(canary.get(field) != value for field, value in expected.items()):
        raise LivePacketError("v3 canary does not bind the selected deployment")
    if parse_time(
        canary.get("deployment_deployed_at"),
        "canary deployment_deployed_at",
    ) != parse_time(deployment.get("deployed_at"), "deployment deployed_at"):
        raise LivePacketError("v3 canary deployment timestamp does not match")


def select_service(
    deployment: dict[str, Any],
    service_id: str,
) -> dict[str, Any]:
    services = deployment.get("services")
    if not isinstance(services, list):
        raise LivePacketError("deployment services are invalid")
    selected = [
        service
        for service in services
        if isinstance(service, dict) and service.get("service_id") == service_id
    ]
    if len(selected) != 1:
        raise LivePacketError("deployment must contain one exact canary service")
    service = selected[0]
    source_tree = service.get("source_tree")
    deployed_tree = service.get("deployed_tree")
    if (
        service.get("parity_state") != "exact"
        or service.get("package_artifact_kind") != "source_projection"
        or not isinstance(source_tree, dict)
        or not isinstance(deployed_tree, dict)
    ):
        raise LivePacketError("deployed service lacks exact package/export parity")
    for field in (
        "package_name",
        "package_version",
        "package_source_revision",
    ):
        required_string(service.get(field), f"deployment service {field}")
    package_digest = required_digest(
        service.get("package_digest"),
        "deployment service package_digest",
    )
    source_tree_digest = required_digest(
        source_tree.get("tree_digest"),
        "deployment service source tree digest",
    )
    deployed_tree_digest = required_digest(
        deployed_tree.get("tree_digest"),
        "deployment service deployed tree digest",
    )
    if source_tree_digest != package_digest or deployed_tree_digest != package_digest:
        raise LivePacketError("deployed service package/source/deploy digests differ")
    return service


def require_canary_link(
    value: Any,
    *,
    label: str,
    expected_state: str,
    canary: dict[str, Any],
    canary_path: Path,
) -> None:
    if not isinstance(value, dict) or value.get("state") != expected_state:
        raise LivePacketError(f"{label} is not {expected_state}")
    observed_at = parse_time(value.get("observed_at"), f"{label} observed_at")
    expires_at = parse_time(value.get("expires_at"), f"{label} expires_at")
    canary_observed_at = parse_time(
        canary.get("observed_at"),
        "canary observed_at",
    )
    canary_expires_at = parse_time(
        canary.get("expires_at"),
        "canary expires_at",
    )
    if observed_at != canary_observed_at or expires_at != canary_expires_at:
        raise LivePacketError(f"{label} does not bind canary time")
    evidence_refs = value.get("evidence_refs")
    if not isinstance(evidence_refs, list):
        raise LivePacketError(f"{label} evidence references are invalid")
    expected_ref = canary_path.absolute().as_posix()
    matching = [
        evidence
        for evidence in evidence_refs
        if isinstance(evidence, dict)
        and evidence.get("owner") == "abyss-stack"
        and evidence.get("evidence_ref") == expected_ref
        and evidence.get("revision") == canary.get("receipt_id")
        and parse_time(
            evidence.get("observed_at"),
            f"{label} evidence observed_at",
        )
        == canary_observed_at
        and parse_time(
            evidence.get("expires_at"),
            f"{label} evidence expires_at",
        )
        == canary_expires_at
    ]
    if len(matching) != 1:
        raise LivePacketError(
            f"{label} does not contain the exact immutable canary reference"
        )


def select_subject(
    observation: dict[str, Any],
    *,
    organ_id: str,
    registry: dict[str, Any],
    registry_record_source: dict[str, Any],
    registry_record_digest: str,
    deployment: dict[str, Any],
    service: dict[str, Any],
    canary: dict[str, Any],
    canary_path: Path,
    materialized_at: datetime,
) -> tuple[dict[str, Any], datetime]:
    if (
        observation.get("schema_version") != "abyss_stack_runtime_observation_v1"
        or observation.get("provider") != "abyss-stack"
        or observation.get("contains_secrets") is not False
    ):
        raise LivePacketError(
            "runtime observation is not a secret-free stack observation"
        )
    expires_at = parse_time(
        observation.get("expires_at"),
        "runtime observation expires_at",
    )
    generated_at = parse_time(
        observation.get("generated_at"),
        "runtime observation generated_at",
    )
    required_string(
        observation.get("provider_watermark"),
        "runtime observation provider_watermark",
    )
    if expires_at <= generated_at:
        raise LivePacketError("runtime observation expiry must follow generation")
    if generated_at > materialized_at:
        raise LivePacketError("runtime observation cannot postdate materialization")
    if expires_at <= materialized_at:
        raise LivePacketError("runtime observation is expired")
    subjects = observation.get("subjects")
    if not isinstance(subjects, list):
        raise LivePacketError("runtime observation subjects are invalid")
    selected = [
        subject
        for subject in subjects
        if isinstance(subject, dict)
        and subject.get("organ_id") == organ_id
        and subject.get("policy_family") == "read"
    ]
    if len(selected) != 1:
        raise LivePacketError(
            "runtime observation must contain one exact organ/read subject"
        )
    subject = selected[0]
    record_owners = registry_record_source.get("owners")
    subject_owners = subject.get("owners")
    if not isinstance(record_owners, dict) or not isinstance(
        subject_owners,
        dict,
    ):
        raise LivePacketError("runtime and registry owner roles are invalid")
    expected_subject_owners = {
        "source_owner": required_string(
            record_owners.get("source_owner"),
            "registry source_owner",
            identifier=True,
        ),
        "access_owner": required_string(
            record_owners.get("access_owner"),
            "registry access_owner",
            identifier=True,
        ),
        "runtime_owner": required_string(
            record_owners.get("runtime_owner"),
            "registry runtime_owner",
            identifier=True,
        ),
        "proof_owner": required_string(
            record_owners.get("proof_owner"),
            "registry proof_owner",
            identifier=True,
        ),
        "acceptance_owner": required_string(
            record_owners.get("acceptance_owner"),
            "registry acceptance_owner",
            identifier=True,
        ),
    }
    if subject_owners != expected_subject_owners:
        raise LivePacketError(
            "runtime observation owner roles differ from registry source"
        )
    if expected_subject_owners["runtime_owner"] != "abyss-stack":
        raise LivePacketError("runtime owner is not abyss-stack")

    revisions = registry_record_source.get("revisions")
    source_revision_block = (
        revisions.get("source") if isinstance(revisions, dict) else None
    )
    source_revision = (
        source_revision_block.get("revision")
        if isinstance(source_revision_block, dict)
        else None
    )
    source = subject.get("source")
    if (
        not isinstance(source, dict)
        or not isinstance(source_revision, str)
        or source.get("revision") != source_revision
    ):
        raise LivePacketError(
            "runtime observation source revision differs from registry source"
        )

    package = subject.get("package")
    deploy = subject.get("deploy")
    if (
        not isinstance(package, dict)
        or not isinstance(deploy, dict)
        or package.get("name") != service.get("package_name")
        or package.get("version") != service.get("package_version")
        or package.get("source_revision") != service.get("package_source_revision")
        or package.get("artifact_digest") != service.get("package_digest")
        or package.get("expected_deploy_tree_digest")
        != service.get("deployed_tree", {}).get("tree_digest")
        or deploy.get("revision") != service.get("package_source_revision")
        or deploy.get("manifest_digest") != deployment.get("manifest_id")
        or deploy.get("manifest_ref") != deployment.get("record_ref")
        or deploy.get("tree_digest")
        != service.get("deployed_tree", {}).get("tree_digest")
    ):
        raise LivePacketError(
            "runtime observation does not bind the selected deployment"
        )

    registry_observation = subject.get("registry")
    if (
        not isinstance(registry_observation, dict)
        or registry_observation.get("registry_id") != registry.get("registry_id")
        or registry_observation.get("registry_digest") != registry_record_digest
        or registry_observation.get("registry_state")
        != registry_record_source.get("registry_state")
    ):
        raise LivePacketError(
            "runtime observation does not bind the selected registry record"
        )

    endpoint = subject.get("endpoint")
    if (
        not isinstance(endpoint, dict)
        or endpoint.get("transport") != "streamable-http"
        or endpoint.get("endpoint_ref") != canary.get("endpoint_ref")
        or endpoint.get("ready") is not True
        or endpoint.get("server_schema_digest") != canary.get("server_schema_digest")
        or not isinstance(endpoint.get("protocol_versions"), list)
        or canary.get("protocol_version") not in endpoint["protocol_versions"]
    ):
        raise LivePacketError(
            "runtime endpoint observation does not bind the canary receipt"
        )
    require_canary_link(
        endpoint.get("evidence"),
        label="runtime endpoint evidence",
        expected_state="exact",
        canary=canary,
        canary_path=canary_path,
    )

    canary_observation = subject.get("canary")
    if (
        not isinstance(canary_observation, dict)
        or canary_observation.get("succeeded") is not False
        or canary_observation.get("result_grounded") is not False
        or canary_observation.get("canary_route") != canary.get("canary_route")
        or canary_observation.get("canary_ref") is not None
    ):
        raise LivePacketError(
            "runtime canary observation exceeds the stack receipt claim"
        )
    require_canary_link(
        canary_observation.get("evidence"),
        label="runtime canary evidence",
        expected_state="blocked",
        canary=canary,
        canary_path=canary_path,
    )
    reason_codes = canary_observation["evidence"].get("reason_codes")
    expected_reasons = (
        ["owner-grounding-review-required"]
        if canary.get("result_contract_matched") is True
        else canary.get("reason_codes")
    )
    if reason_codes != expected_reasons:
        raise LivePacketError(
            "runtime canary block reasons differ from the canary receipt"
        )

    package_name = required_string(
        service.get("package_name"),
        "deployment service package_name",
    )
    if canary.get("server_version") != service.get("package_version") or not str(
        canary.get("server_name")
    ).startswith(package_name):
        raise LivePacketError(
            "canary server identity differs from deployed package identity"
        )
    return subject, expires_at


def asserted_axis(
    *,
    observed_at: datetime,
    evidence_ref: str,
    evidence_kind: str,
    revision: str,
    expires_at: datetime | None = None,
    freshness_policy: str | None = None,
) -> dict[str, Any]:
    axis = {
        "state": "asserted",
        "observed_at": timestamp(observed_at),
        "evidence_ref": evidence_ref,
        "evidence_kind": evidence_kind,
        "revision": revision,
    }
    if expires_at is not None:
        axis["expires_at"] = timestamp(expires_at)
    elif freshness_policy is not None:
        axis["freshness_policy"] = freshness_policy
    else:
        raise LivePacketError(
            "asserted maturity axis requires expiry or freshness policy"
        )
    return axis


def materialize_packet(
    *,
    organ_id: str,
    registry_path: Path,
    deployment_path: Path,
    observation_path: Path,
    canary_path: Path,
    result_path: Path | None,
    owner_review_path: Path | None,
    materialized_at: datetime,
) -> dict[str, Any]:
    if IDENTIFIER.fullmatch(organ_id) is None:
        raise LivePacketError("organ id is invalid")
    materialized_at = materialized_at.astimezone(timezone.utc)
    registry, _ = read_json(
        registry_path,
        "private organ registry",
        require_private=True,
    )
    (
        record,
        registry_record_digest,
        registry_digest,
        registry_expiry,
    ) = registry_record(
        registry,
        organ_id,
        materialized_at,
    )
    canary = canary_receipt(canary_path)
    result_artifact = canary_result_artifact(
        result_path,
        canary=canary,
        canary_path=canary_path,
    )
    if canary.get("organ_id") != organ_id:
        raise LivePacketError("canary organ does not match requested organ")
    service_id = canary.get("service_id")
    if not isinstance(service_id, str):
        raise LivePacketError("canary service identity is unavailable")
    deployment, deployment_record_path = deployment_receipt(deployment_path)
    service = select_service(deployment, service_id)
    require_v3_deployment_binding(canary, deployment, service)
    review, review_capability, _ = owner_result_review(
        owner_review_path,
        record=record,
        canary=canary,
        canary_path=canary_path,
        result_artifact=result_artifact,
        result_path=result_path,
        materialized_at=materialized_at,
    )
    observation, _ = read_json(
        observation_path,
        "runtime observation",
        require_private=True,
    )
    subject, observation_expiry = select_subject(
        observation,
        organ_id=organ_id,
        registry=registry,
        registry_record_source=record,
        registry_record_digest=registry_record_digest,
        deployment=deployment,
        service=service,
        canary=canary,
        canary_path=canary_path,
        materialized_at=materialized_at,
    )
    if canary.get("schema_version") == "abyss_stack_mcp_canary_receipt_v3":
        process = subject.get("process")
        if (
            not isinstance(process, dict)
            or process.get("process_identity") != canary.get("process_identity")
        ):
            raise LivePacketError(
                "v3 canary process identity does not bind runtime observation"
            )

    canary_observed_at = parse_time(
        canary.get("observed_at"),
        "canary observed_at",
    )
    canary_expiry = parse_time(
        canary.get("expires_at"),
        "canary expires_at",
    )
    if canary_expiry <= materialized_at:
        raise LivePacketError("canary receipt is expired")
    deployment_at = parse_time(
        deployment.get("deployed_at"),
        "deployment deployed_at",
    )
    if canary_observed_at < deployment_at:
        raise LivePacketError("canary observation cannot predate deployment")
    owners = record.get("owners")
    revisions = record.get("revisions")
    maturity_source = record.get("maturity")
    if (
        not isinstance(owners, dict)
        or not isinstance(revisions, dict)
        or not isinstance(maturity_source, dict)
    ):
        raise LivePacketError(
            "registry owner, revision, or maturity contract is unavailable"
        )
    source_revision_block = revisions.get("source")
    declared = maturity_source.get("declared")
    control_owner = owners.get("control_owner") if isinstance(owners, dict) else None
    source_owner = required_string(
        owners.get("source_owner"),
        "registry source_owner",
        identifier=True,
    )
    if (
        not isinstance(source_revision_block, dict)
        or not isinstance(source_revision_block.get("revision"), str)
        or not isinstance(control_owner, str)
        or IDENTIFIER.fullmatch(control_owner) is None
    ):
        raise LivePacketError("registry lacks owner, source, or control identity")
    declaration = (
        declared.get("evidence")
        if isinstance(declared, dict) and declared.get("state") == "asserted"
        else None
    )
    if not isinstance(declaration, dict):
        observed_source = subject.get("source")
        source_evidence = (
            observed_source.get("evidence")
            if isinstance(observed_source, dict)
            else None
        )
        evidence_refs = (
            source_evidence.get("evidence_refs")
            if isinstance(source_evidence, dict)
            and source_evidence.get("state") == "exact"
            else None
        )
        matching_declarations = [
            evidence
            for evidence in evidence_refs
            if isinstance(evidence, dict)
            and evidence.get("owner") == source_owner
            and evidence.get("revision") == source_revision_block["revision"]
        ] if isinstance(evidence_refs, list) else []
        if len(matching_declarations) != 1:
            raise LivePacketError(
                "registry shadow contour lacks one exact owner source observation"
            )
        declaration = matching_declarations[0]
    if (
        declaration.get("owner") != source_owner
        or declaration.get("revision") != source_revision_block["revision"]
    ):
        raise LivePacketError(
            "registry declaration is not issued for the source revision"
        )
    declaration_ref = required_string(
        declaration.get("evidence_ref"),
        "declaration evidence_ref",
    )

    source_revision = "source:" + source_revision_block["revision"]
    package_revision = "package:" + service["package_digest"]
    deploy_revision = "deploy:" + deployment["manifest_id"]
    consumer_schema_revision = "consumer-schema:" + str(canary["server_schema_digest"])
    revision_map = {
        "source": source_revision,
        "package": package_revision,
        "deploy": deploy_revision,
        "consumer_schema": consumer_schema_revision,
    }
    maturity = {axis: {"state": "not_asserted"} for axis in MATURITY_AXES}
    evidence_times: list[datetime] = []

    declaration_time = parse_time(
        declaration.get("observed_at"),
        "declaration observed_at",
    )
    declaration_expiry = parse_time(
        declaration.get("expires_at"),
        "declaration expires_at",
    )
    maturity["declared"] = asserted_axis(
        observed_at=declaration_time,
        evidence_ref=declaration_ref,
        evidence_kind="source_declaration",
        revision=source_revision,
        expires_at=declaration_expiry,
    )
    evidence_times.append(declaration_time)

    deployment_ref = deployment_record_path.as_posix()
    for axis, evidence_kind in (
        ("packaged", "package_receipt"),
        ("exported", "export_receipt"),
        ("deployed", "deploy_receipt"),
    ):
        maturity[axis] = asserted_axis(
            observed_at=deployment_at,
            evidence_ref=deployment_ref,
            evidence_kind=evidence_kind,
            revision=(
                package_revision
                if axis in {"packaged", "exported"}
                else deploy_revision
            ),
            freshness_policy=(
                "content-addressed exact deployment receipt; current runtime "
                "state is evaluated independently"
            ),
        )
    evidence_times.append(deployment_at)

    process = subject.get("process")
    if not isinstance(process, dict):
        raise LivePacketError("runtime process observation is unavailable")
    process_evidence = process.get("evidence")
    if (
        process.get("active") is True
        and isinstance(process.get("process_identity"), str)
        and isinstance(process_evidence, dict)
        and process_evidence.get("state") == "exact"
        and isinstance(process_evidence.get("evidence_refs"), list)
        and process_evidence["evidence_refs"]
    ):
        process_time = parse_time(
            process_evidence.get("observed_at"),
            "process observed_at",
        )
        process_expiry = parse_time(
            process_evidence.get("expires_at"),
            "process expires_at",
        )
        process_ref = process_evidence["evidence_refs"][0]
        if not isinstance(process_ref, dict):
            raise LivePacketError("process evidence reference is invalid")
        process_ref_time = parse_time(
            process_ref.get("observed_at"),
            "process evidence ref observed_at",
        )
        process_ref_expiry = parse_time(
            process_ref.get("expires_at"),
            "process evidence ref expires_at",
        )
        process_ref_owner = required_string(
            process_ref.get("owner"),
            "process evidence owner",
            identifier=True,
        )
        process_ref_revision = required_string(
            process_ref.get("revision"),
            "process evidence revision",
        )
        process_ref_value = required_string(
            process_ref.get("evidence_ref"),
            "process evidence_ref",
        )
        effective_process_expiry = min(
            observation_expiry,
            process_expiry,
            process_ref_expiry,
        )
        if (
            process_ref_owner == "abyss-stack"
            and process_ref_revision == service.get("package_source_revision")
            and process_ref_time == process_time
            and effective_process_expiry > materialized_at
        ):
            maturity["process_alive"] = asserted_axis(
                observed_at=process_time,
                evidence_ref=process_ref_value,
                evidence_kind="process_observation",
                revision=deploy_revision,
                expires_at=effective_process_expiry,
            )
            evidence_times.append(process_time)

    registry_observed_ref = registry_path.absolute().as_posix() + "#" + registry_digest
    maturity["registry_indexed"] = asserted_axis(
        observed_at=materialized_at,
        evidence_ref=registry_observed_ref,
        evidence_kind="registry_observation",
        revision=deploy_revision,
        expires_at=registry_expiry,
    )
    evidence_times.append(materialized_at)

    canary_ref = canary_path.absolute().as_posix()
    maturity["endpoint_ready"] = asserted_axis(
        observed_at=canary_observed_at,
        evidence_ref=canary_ref + "#endpoint",
        evidence_kind="endpoint_probe",
        revision=deploy_revision,
        expires_at=canary_expiry,
    )
    maturity["schema_observed"] = asserted_axis(
        observed_at=canary_observed_at,
        evidence_ref=canary_ref + "#server-schema",
        evidence_kind="consumer_schema_observation",
        revision=consumer_schema_revision,
        expires_at=canary_expiry,
    )
    evidence_times.append(canary_observed_at)
    if canary.get("call_succeeded") is True:
        maturity["call_succeeded"] = asserted_axis(
            observed_at=canary_observed_at,
            evidence_ref=canary_ref + "#call",
            evidence_kind="call_receipt",
            revision=deploy_revision,
            expires_at=canary_expiry,
        )
    if review is not None and owner_review_path is not None:
        review_time = parse_time(
            review.get("reviewed_at"),
            "owner review reviewed_at",
        )
        review_expiry = parse_time(
            review.get("expires_at"),
            "owner review expires_at",
        )
        review_ref = owner_review_path.absolute().as_posix()
        if review["grounding_state"] == "grounded":
            maturity["result_grounded"] = asserted_axis(
                observed_at=review_time,
                evidence_ref=review_ref + "#grounding",
                evidence_kind="owner_grounding_review",
                revision=source_revision,
                expires_at=review_expiry,
            )
            evidence_times.append(review_time)
        if review["freshness_state"] == "exact":
            maturity["freshness_satisfied"] = asserted_axis(
                observed_at=review_time,
                evidence_ref=review_ref + "#freshness",
                evidence_kind="freshness_review",
                revision=deploy_revision,
                expires_at=review_expiry,
            )
            evidence_times.append(review_time)

    missing = [
        axis
        for axis in (
            "owner_reviewed",
            "consumer_registered",
            "result_grounded",
            "freshness_satisfied",
            "owner_accepted",
            "cross_organ_proven",
            "rollback_proven",
        )
        if maturity[axis]["state"] != "asserted"
    ]
    packet_body = {
        "schema_version": "organ_access_proof_packet_v1",
        "organ_id": organ_id,
        "capability_id": (
            str(review_capability["capability_id"])
            if review_capability is not None
            else str(canary["tool_name"])
        ),
        "policy_plane": "read",
        "protocol_pair": {
            "consumer": str(canary["consumer_id"]),
            "server": (
                str(canary["server_name"]) + "@" + str(canary["server_version"])
            ),
            "transport": "streamable-http",
        },
        "observation_window": {
            "started_at": timestamp(min(evidence_times)),
            "ended_at": timestamp(materialized_at),
        },
        "owners": {
            "source": source_owner,
            "access": required_string(
                owners.get("access_owner"),
                "registry access_owner",
                identifier=True,
            ),
            "control": control_owner,
            "runtime": required_string(
                owners.get("runtime_owner"),
                "registry runtime_owner",
                identifier=True,
            ),
            "proof": required_string(
                owners.get("proof_owner"),
                "registry proof_owner",
                identifier=True,
            ),
            "acceptance": required_string(
                owners.get("acceptance_owner"),
                "registry acceptance_owner",
                identifier=True,
            ),
        },
        "revisions": revision_map,
        "maturity": maturity,
        "result": {
            "verdict": "insufficient_evidence",
            "admission_change_authorized": False,
            "owner_acceptance_inferred": False,
            "higher_effect_authorized": False,
            "limitations": [
                (
                    "Local stack inputs pass bounded structural, content-address, "
                    "permission, and cross-input checks; those checks do not "
                    "authenticate the issuing owners."
                ),
                (
                    "Missing maturity axes remain not asserted: "
                    + ", ".join(missing)
                    + "."
                ),
                (
                    (
                        "The canary result contract matched, but "
                        if canary["result_contract_matched"]
                        else "The canary result contract did not match, and "
                    )
                    + "a call receipt does not prove owner grounding, "
                    "freshness, acceptance, admission, or rollback."
                ),
                (
                    "The bound owner review may assert only result grounding "
                    "and exact freshness; it does not assert owner acceptance, "
                    "central proof, admission, cross-organ proof, or rollback."
                    if review is not None
                    else (
                        "The private result artifact is preserved for owner "
                        "review but remains untrusted and does not assert a "
                        "maturity axis."
                        if result_artifact is not None
                        else "No successful canary result artifact is available."
                    )
                ),
            ],
        },
    }
    packet_id = (
        "live."
        + organ_id
        + "."
        + str(canary["tool_name"]).replace("_", "-")
        + "."
        + digest(packet_body).removeprefix("sha256:")[:16]
    )
    packet = {"packet_id": packet_id, **packet_body}
    issues = validate_packet(packet)
    if issues:
        raise LivePacketError(
            "materialized packet failed its source contract: " + ",".join(issues)
        )
    reject_secret_material(packet)
    return packet


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--organ", required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--deployment", type=Path, required=True)
    parser.add_argument("--observation", type=Path, required=True)
    parser.add_argument("--canary", type=Path, required=True)
    parser.add_argument("--result", type=Path)
    parser.add_argument("--owner-review", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--materialized-at")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        materialized_at = (
            parse_time(args.materialized_at, "materialized_at")
            if args.materialized_at
            else datetime.now(timezone.utc)
        )
        packet = materialize_packet(
            organ_id=args.organ,
            registry_path=args.registry,
            deployment_path=args.deployment,
            observation_path=args.observation,
            canary_path=args.canary,
            result_path=args.result,
            owner_review_path=args.owner_review,
            materialized_at=materialized_at,
        )
        write_private_json(args.output, packet)
    except LivePacketError as exc:
        print(
            f"aoa-organ-access live packet: {exc}",
            file=os.sys.stderr,
        )
        return 1
    asserted = sorted(
        axis
        for axis, evidence in packet["maturity"].items()
        if evidence["state"] == "asserted"
    )
    print(
        json.dumps(
            {
                "packet_id": packet["packet_id"],
                "organ_id": packet["organ_id"],
                "verdict": packet["result"]["verdict"],
                "asserted_axes": asserted,
                "output": args.output.as_posix(),
                "claim_limit": (
                    "Materialization and source-contract acceptance are not a "
                    "central proof verdict, owner grounding, acceptance, "
                    "admission, or rollback receipt."
                ),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
