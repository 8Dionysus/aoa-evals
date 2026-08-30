"""Validate exact adjacent-provider evidence without promoting admission."""

from __future__ import annotations

import hashlib
import json
import re
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
CLAIM_LIMITS = [
    "Actual provider execution and common-envelope normalization are shown.",
    "Candidate execution does not establish artifact admission or deployed runtime availability.",
    "The packet does not establish scanner completeness, SBOM completeness, document fidelity, semantic proof, landing, or owner acceptance.",
]
RAW_EVIDENCE_KEYS = {
    "static_security": "sarif",
    "software_components": "sbom",
    "artifact_provenance": "in_toto",
    "document_structure": "document_markdown",
}
EXPECTED_PROVIDER_IDS = {provider_id for provider_id, _ in EXPECTED.values()}
# Adjacent batches predate the envelope's ``sha256:``-qualified artifact
# references and carry their provider configuration digest as raw hex.  Keep
# accepting both representations while requiring a complete cryptographic
# digest rather than an arbitrary non-empty token.
_DIGEST_RE = re.compile(r"^(?:sha256:)?[0-9a-f]{64}$")
_RAW_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
# Adjacent evidence is normally staged beside the packet.  The supplied
# AbyssOS packet also points at a host-managed artifact bundle for its in-toto
# output; keep that explicit store as the only permitted external root.
_HOST_ARTIFACT_ROOT = Path("/srv/abyss-machine/artifacts")


def _raw_evidence_path(packet_path: Path, declared_path: Any) -> tuple[Path | None, str | None]:
    """Resolve one raw ref without allowing arbitrary host-file claims."""

    if (
        not isinstance(declared_path, str)
        or not declared_path.strip()
        or "\x00" in declared_path
        or "://" in declared_path
    ):
        return None, "path_unsafe"
    try:
        candidate = Path(declared_path)
        resolved = (
            candidate if candidate.is_absolute() else packet_path.parent / candidate
        ).resolve(strict=False)
        packet_root = packet_path.parent.resolve(strict=False)
        allowed_roots = [packet_root]
        if _HOST_ARTIFACT_ROOT.exists():
            allowed_roots.append(_HOST_ARTIFACT_ROOT.resolve(strict=False))
        if not any(
            resolved == root or root in resolved.parents for root in allowed_roots
        ):
            return None, "path_unsafe"
    except (OSError, RuntimeError, TypeError, ValueError):
        return None, "path_unsafe"
    if not resolved.is_file():
        return None, "file_missing"
    return resolved, None


def _raw_evidence_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _provider_execution_issues(
    key: str,
    batch: dict[str, Any],
    providers: Any,
    raw_evidence: Any,
    packet_path: Path,
) -> list[str]:
    """Require provenance that the advertised provider output really exists.

    The batch itself carries the normalized observation, but a positive
    adjacent-provider result also claims actual candidate output.  Keep that
    claim bound to a provider version/configuration, parser provenance, and a
    digest-bearing raw output reference.  An empty top-level provider map must
    therefore never be enough for a positive result.
    """

    provider_id, _capability_class = EXPECTED[key]
    issues: list[str] = []
    provider = batch.get("provider", {})
    provider_meta = providers.get(provider_id) if isinstance(providers, dict) else None
    if not isinstance(provider_meta, dict):
        issues.append(f"provider_provenance_missing:{provider_id}")
    else:
        runtime_version = provider_meta.get("version")
        batch_version = provider.get("version")
        if not isinstance(runtime_version, str) or not runtime_version.strip():
            issues.append(f"provider_version_missing:{provider_id}")
        elif not isinstance(batch_version, str) or not batch_version.strip():
            issues.append(f"provider_version_missing:{provider_id}")
        elif runtime_version not in batch_version and batch_version not in runtime_version:
            issues.append(f"provider_version_mismatch:{provider_id}")
        if not isinstance(provider_meta.get("runtime_posture"), str) or not provider_meta[
            "runtime_posture"
        ].strip():
            issues.append(f"provider_runtime_posture_missing:{provider_id}")

    config_digest = provider.get("config_digest")
    if not isinstance(config_digest, str) or _DIGEST_RE.fullmatch(config_digest) is None:
        issues.append(f"provider_config_missing:{provider_id}")
    lane = provider.get("lane")
    if not isinstance(lane, dict) or lane.get("id") != provider_id:
        issues.append(f"provider_lane_identity_missing:{provider_id}")
    currentness = batch.get("currentness")
    if not isinstance(currentness, dict) or currentness.get("provider") != {
        "id": provider_id,
        "version": provider.get("version"),
        "config_digest": config_digest,
    }:
        issues.append(f"provider_currentness_mismatch:{provider_id}")

    provenance = batch.get("provenance")
    if not isinstance(provenance, dict):
        issues.append(f"provider_execution_provenance_missing:{provider_id}")
    else:
        for field in ("extractor_ref", "parser_ref"):
            value = provenance.get(field)
            if not isinstance(value, str) or not value.strip():
                issues.append(f"provider_execution_{field}_missing:{provider_id}")
        source_refs = provenance.get("source_refs")
        if not isinstance(source_refs, list) or not source_refs:
            issues.append(f"provider_execution_source_refs_missing:{provider_id}")

    raw_key = RAW_EVIDENCE_KEYS[key]
    raw_ref = raw_evidence.get(raw_key) if isinstance(raw_evidence, dict) else None
    if not isinstance(raw_ref, dict):
        issues.append(f"raw_evidence_missing:{raw_key}")
    else:
        declared_path = raw_ref.get("path")
        raw_path, path_issue = _raw_evidence_path(packet_path, declared_path)
        if path_issue == "path_unsafe":
            issues.append(f"raw_evidence_path_unsafe:{raw_key}")
        elif path_issue == "file_missing":
            issues.append(f"raw_evidence_file_missing:{raw_key}")
        if _RAW_DIGEST_RE.fullmatch(str(raw_ref.get("sha256", ""))) is None:
            issues.append(f"raw_evidence_digest_missing:{raw_key}")
        elif raw_path is not None:
            try:
                if _raw_evidence_digest(raw_path) != raw_ref["sha256"]:
                    issues.append(f"raw_evidence_digest_mismatch:{raw_key}")
            except OSError:
                issues.append(f"raw_evidence_file_unreadable:{raw_key}")
    return issues


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
        if payload.get("claim_limits") != CLAIM_LIMITS:
            issues.append("claim_limits_mismatch")
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
            issues.extend(
                _provider_execution_issues(
                    key,
                    batch,
                    payload.get("providers"),
                    payload.get("raw_evidence"),
                    path,
                )
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
