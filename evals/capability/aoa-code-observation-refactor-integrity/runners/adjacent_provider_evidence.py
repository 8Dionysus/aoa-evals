"""Validate exact adjacent-provider evidence without promoting admission."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = BUNDLE_ROOT / "schemas/adjacent-provider-evidence.schema.json"
EXPECTED = {
    "static_security": ("semgrep", "static-security"),
    "software_components": ("syft", "software-components"),
    "artifact_provenance": ("in-toto", "artifact-provenance"),
    "document_structure": ("markitdown", "document-structure"),
}
OBSERVATION_CONTRACT = {
    "static_security": ("static-security", {"security_finding"}, "sarif:"),
    "software_components": (
        "software-components",
        {"software_component"},
        "component:",
    ),
    "artifact_provenance": ("artifact-provenance", {"artifact_subject"}, "provenance:"),
    "document_structure": (
        "document-structure",
        {"heading", "paragraph", "table", "list", "document_element"},
        "document:",
    ),
}


def _observation_issue(key: str, observation: Any) -> str | None:
    if not isinstance(observation, dict):
        return "not_object"
    capability_class, symbol_kinds, semantic_prefix = OBSERVATION_CONTRACT[key]
    if observation.get("capability_class") != capability_class:
        return "capability_class"
    if (
        observation.get("observation_kind") != "symbol"
        or observation.get("relation") is not None
    ):
        return "observation_kind"
    if (
        not isinstance(observation.get("observation_id"), str)
        or not observation["observation_id"]
    ):
        return "observation_id"
    semantic_key = observation.get("semantic_key")
    if not isinstance(semantic_key, str) or not semantic_key.startswith(
        semantic_prefix
    ):
        return "semantic_key"
    subject = observation.get("subject")
    if not isinstance(subject, dict) or any(
        not isinstance(subject.get(field), str) or not subject[field]
        for field in ("label", "qualified_name", "symbol_id", "symbol_kind")
    ):
        return "subject"
    if subject["symbol_kind"] not in symbol_kinds:
        return "subject_kind"
    occurrence = observation.get("occurrence")
    coordinate_fields = ("start_line", "start_column", "end_line", "end_column")
    if not isinstance(occurrence, dict) or any(
        not isinstance(occurrence.get(field), int) or occurrence[field] < 1
        for field in coordinate_fields
    ):
        return "occurrence"
    if (occurrence["end_line"], occurrence["end_column"]) < (
        occurrence["start_line"],
        occurrence["start_column"],
    ):
        return "occurrence_order"
    confidence = observation.get("confidence")
    value = confidence.get("value") if isinstance(confidence, dict) else None
    if (
        not isinstance(confidence, dict)
        or confidence.get("evidence_class") != "observed"
        or isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not 0 < value <= 1
    ):
        return "confidence"
    return None


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def validate(path: Path) -> dict[str, Any]:
    payload = _load(path)
    schema_errors = sorted(
        Draft202012Validator(
            _load(SCHEMA_PATH), format_checker=FormatChecker()
        ).iter_errors(payload),
        key=lambda error: list(error.absolute_path),
    )
    issues = [
        "schema:"
        + "/".join(str(part) for part in error.absolute_path)
        + ":"
        + error.message
        for error in schema_errors
    ]
    evidence: dict[str, Any] = {}
    if not schema_errors:
        for key, (provider_id, capability_class) in EXPECTED.items():
            batch = payload["batches"][key]
            provider = batch.get("provider", {})
            source = batch.get("source", {})
            qualification = batch.get("qualification", {})
            admission = qualification.get("machine_admission", {})
            if provider.get("id") != provider_id:
                issues.append(f"provider_identity_mismatch:{key}")
            if batch.get("capability_class") != capability_class:
                issues.append(f"capability_class_mismatch:{key}")
            if (
                provider.get("lane", {}).get("status") != "supplied_unadmitted"
                or admission.get("state") != "not_admitted"
            ):
                issues.append(f"provider_not_bounded:{provider_id}")
            if source.get("source_epoch") != payload.get("source_epoch"):
                issues.append(f"source_epoch_mismatch:{provider_id}")
            count = len(batch.get("observations", []))
            if count < 1:
                issues.append(f"observation_missing:{provider_id}")
            for observation_index, observation in enumerate(
                batch.get("observations", [])
            ):
                observation_issue = _observation_issue(key, observation)
                if observation_issue is not None:
                    issues.append(
                        f"invalid_observation:{provider_id}:{observation_index}:{observation_issue}"
                    )
            evidence[key] = {
                "provider_id": provider_id,
                "capability_class": capability_class,
                "observation_count": count,
            }
        summary = payload.get("summary", {})
        if summary.get("all_provider_lanes_unadmitted") is not True:
            issues.append("summary_admission_posture_mismatch")
        if payload.get("artifact", {}).get("admission_status") != "not_admitted":
            issues.append("artifact_admission_overclaim")
    issues = sorted(set(issues))
    return {
        "schema_version": "aoa_adjacent_provider_envelope_evidence_result_v1",
        "evidence_digest": _digest(payload),
        "evidence": evidence,
        "issues": issues,
        "verdict": (
            "supports bounded adjacent-provider envelope evidence"
            if not issues
            else "does not support bounded adjacent-provider envelope evidence"
        ),
        "claim_limit": (
            "The result supports actual output presence and common-envelope integrity for the supplied exact packet only; "
            "it is not artifact admission, deployed runtime health, provider completeness, landing, or owner acceptance."
        ),
    }
