"""Validate bounded agreement between normalized code-observation providers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = BUNDLE_ROOT / "schemas" / "provider-agreement.schema.json"
REQUIRED_PROVIDERS = {"tree-sitter", "scip", "lsp"}


def _load(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


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
        "schema:" + "/".join(str(part) for part in error.absolute_path) + ":" + error.message
        for error in schema_errors
    ]
    if schema_errors:
        return _result(payload, issues, {})

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

    facts: dict[str, set[str]] = {}
    for envelope in envelopes:
        provider_id = envelope["provider"]["id"]
        lane = envelope["provider"].get("lane", {})
        admission = envelope.get("qualification", {}).get("machine_admission", {})
        if lane.get("status") != "supplied_unadmitted" or admission.get("state") != "not_admitted":
            issues.append(f"provider_not_bounded:{provider_id}")
        if envelope.get("parse_status") != "parsed":
            issues.append(f"provider_not_parsed:{provider_id}")

        provider_facts: set[str] = set()
        for observation in envelope["observations"]:
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
            provider for provider in REQUIRED_PROVIDERS
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
        "claim_limit": (
            "Agreement is limited to supplied normalized observations at one exact "
            "source epoch; it is not provider correctness, admission, runtime health, "
            "KAG acceptance, or owner acceptance."
        ),
    }
