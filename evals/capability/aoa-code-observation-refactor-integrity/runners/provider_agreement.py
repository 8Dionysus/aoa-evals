"""Validate bounded agreement between normalized code-observation providers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = BUNDLE_ROOT / "schemas" / "provider-agreement.schema.json"
REQUIRED_PROVIDERS = {"tree-sitter", "scip", "lsp"}
CLAIM_BOUNDARY = (
    "This exact-source-epoch comparison checks only agreement among supplied, "
    "unadmitted normalized observations; it is not provider correctness, machine "
    "admission, runtime health, KAG acceptance, proof promotion, or owner acceptance."
)


def _normalized_observation_issue(observation: Any) -> str | None:
    if not isinstance(observation, dict):
        return "not_object"
    if observation.get("capability_class") != "code-structure":
        return "capability_class"
    if observation.get("observation_kind") not in {"symbol", "relation"}:
        return "observation_kind"
    for field in ("observation_id", "semantic_key"):
        if not isinstance(observation.get(field), str) or not observation[field]:
            return field
    subject = observation.get("subject")
    if not isinstance(subject, dict) or any(
        not isinstance(subject.get(field), str) or not subject[field]
        for field in ("label", "qualified_name", "symbol_id", "symbol_kind")
    ):
        return "subject"
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
    relation = observation.get("relation")
    if observation["observation_kind"] == "symbol":
        if relation is not None:
            return "symbol_relation"
    elif (
        not isinstance(relation, dict)
        or relation.get("kind") not in {"references", "calls"}
        or not isinstance(relation.get("target_name"), str)
        or not relation["target_name"]
    ):
        return "relation"
    return None


def _load(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _source_path_is_safe(value: Any) -> bool:
    """Accept only a packet-local relative source path."""

    if not isinstance(value, str) or not value or "\x00" in value:
        return False
    posix_path = PurePosixPath(value)
    first_component = value.split("/", 1)[0]
    return not (
        posix_path.is_absolute()
        or ".." in posix_path.parts
        or "//" in value
        or "\\" in value
        or "://" in value
        or ":" in first_component
    )


def _packet_source_path(packet_path: Path, source_path: Any) -> Path | None:
    """Resolve a source witness without allowing a packet to escape its root."""

    if not _source_path_is_safe(source_path):
        return None
    packet_root = packet_path.parent.resolve()
    candidate = (packet_root / str(source_path)).resolve()
    try:
        candidate.relative_to(packet_root)
    except ValueError:
        return None
    return candidate if candidate.is_file() else None


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
    if schema_errors:
        return _result(payload, issues, {})

    if payload.get("claim_boundary") != CLAIM_BOUNDARY:
        issues.append("claim_boundary_mismatch")

    envelopes = payload["envelopes"]
    providers = [envelope["provider"]["id"] for envelope in envelopes]
    if len(providers) != len(set(providers)):
        issues.append("duplicate_provider")
    missing = sorted(REQUIRED_PROVIDERS - set(providers))
    if missing:
        issues.append("missing_providers:" + ",".join(missing))

    source_keys = {
        (
            envelope["source"]["repo"],
            envelope["source"]["path"],
            envelope["source"]["source_epoch"],
            envelope["source"]["content_digest"],
            envelope["source"]["language"],
        )
        for envelope in envelopes
    }
    if len(source_keys) != 1:
        issues.append("source_identity_mismatch")

    # Agreement on repeated metadata is not an independent source witness.
    # Read the referenced TypeScript bytes from the evidence packet and bind
    # the declared digest to that content before claiming exact-source-epoch
    # agreement.
    source = envelopes[0]["source"]
    source_file = _packet_source_path(path, source.get("path"))
    if source_file is None:
        issues.append("source_file_missing_or_unsafe")
    else:
        actual_digest = hashlib.sha256(source_file.read_bytes()).hexdigest()
        declared_digest = source["content_digest"].removeprefix("sha256:")
        if actual_digest != declared_digest:
            issues.append("source_content_digest_mismatch")

    facts: dict[str, set[str]] = {}
    for envelope in envelopes:
        provider_id = envelope["provider"]["id"]
        lane = envelope["provider"].get("lane", {})
        admission = envelope.get("qualification", {}).get("machine_admission", {})
        if (
            lane.get("status") != "supplied_unadmitted"
            or admission.get("state") != "not_admitted"
        ):
            issues.append(f"provider_not_bounded:{provider_id}")
        if envelope.get("parse_status") != "parsed":
            issues.append(f"provider_not_parsed:{provider_id}")

        provider_facts: set[str] = set()
        for observation_index, observation in enumerate(envelope["observations"]):
            observation_issue = _normalized_observation_issue(observation)
            if observation_issue is not None:
                issues.append(
                    f"invalid_normalized_observation:{provider_id}:{observation_index}:{observation_issue}"
                )
                continue
            label = str(observation.get("subject", {}).get("label", ""))
            if not label:
                continue
            if observation.get("observation_kind") == "symbol":
                provider_facts.add(f"definition:{label}")
            relation = observation.get("relation")
            if isinstance(relation, dict):
                target = str(relation.get("target_name") or label)
                provider_facts.add(f"{relation.get('kind', 'relation')}:{target}")
        facts[provider_id] = provider_facts

    for required_fact in payload["required_facts"]:
        missing_fact = sorted(
            provider
            for provider in REQUIRED_PROVIDERS
            if required_fact not in facts.get(provider, set())
        )
        if missing_fact:
            issues.append(f"fact_not_shared:{required_fact}:" + ",".join(missing_fact))
    return _result(payload, issues, facts)


def _result(
    payload: dict[str, Any], issues: list[str], facts: dict[str, set[str]]
) -> dict[str, Any]:
    return {
        "schema_version": "aoa_code_observation_provider_agreement_result_v1",
        "evidence_digest": _digest(payload),
        "provider_ids": sorted(facts),
        "shared_facts": sorted(set.intersection(*facts.values())) if facts else [],
        "issues": sorted(set(issues)),
        "verdict": (
            "supports bounded cross-provider agreement"
            if not issues
            else "does not support bounded cross-provider agreement"
        ),
        "claim_limit": CLAIM_BOUNDARY,
    }
