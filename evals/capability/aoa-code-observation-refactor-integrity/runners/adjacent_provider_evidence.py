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


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def validate(path: Path) -> dict[str, Any]:
    payload = _load(path)
    schema_errors = sorted(
        Draft202012Validator(_load(SCHEMA_PATH), format_checker=FormatChecker()).iter_errors(payload),
        key=lambda error: list(error.absolute_path),
    )
    issues = [
        "schema:" + "/".join(str(part) for part in error.absolute_path) + ":" + error.message
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
            if provider.get("lane", {}).get("status") != "supplied_unadmitted" or admission.get("state") != "not_admitted":
                issues.append(f"provider_not_bounded:{provider_id}")
            if source.get("source_epoch") != payload.get("source_epoch"):
                issues.append(f"source_epoch_mismatch:{provider_id}")
            count = len(batch.get("observations", []))
            if count < 1:
                issues.append(f"observation_missing:{provider_id}")
            evidence[key] = {"provider_id": provider_id, "capability_class": capability_class, "observation_count": count}
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
            if not issues else "does not support bounded adjacent-provider envelope evidence"
        ),
        "claim_limit": (
            "The result supports actual output presence and common-envelope integrity for the supplied exact packet only; "
            "it is not artifact admission, deployed runtime health, provider completeness, landing, or owner acceptance."
        ),
    }
