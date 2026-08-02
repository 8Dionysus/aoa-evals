from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/architecture/aoa_evals_mcp_capabilities.v1.json"
SCHEMA = ROOT / "docs/architecture/aoa_evals_mcp_capabilities.schema.json"


def _payload(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_mcp_capability_contract_is_schema_valid_and_owner_bounded() -> None:
    contract = _payload(CONTRACT)
    Draft202012Validator(_payload(SCHEMA)).validate(contract)

    assert contract["organ_id"] == "aoa-evals"
    assert contract["source_owner"] == "aoa-evals"
    assert contract["proof_owner"] == "aoa-evals"
    assert contract["access_runtime_owner"] == "abyss-stack"
    assert contract["admission_owner"] == "aoa-sdk"
    assert contract["admission_asserted"] is False
    assert contract["owner_acceptance_asserted"] is False
    assert contract["proof_issuance_via_mcp_allowed"] is False
    assert contract["effect_activation_authorized"] is False
    assert all(value is False for value in contract["guardrails"].values())


def test_mcp_capability_contract_separates_discovery_request_and_proof_read() -> None:
    contract = _payload(CONTRACT)
    capabilities = {
        capability["capability_id"]: capability
        for capability in contract["capabilities"]
    }
    assert set(capabilities) == {
        "eval-discovery-read",
        "eval-request-prepare",
        "proof-result-read",
    }

    discovery = capabilities["eval-discovery-read"]
    request = capabilities["eval-request-prepare"]
    proof_read = capabilities["proof-result-read"]
    assert (discovery["policy_family"], discovery["credential_class"]) == (
        "read",
        "evals-read",
    )
    assert (request["policy_family"], request["credential_class"]) == (
        "candidate",
        "evals-candidate",
    )
    assert (proof_read["policy_family"], proof_read["credential_class"]) == (
        "read",
        "evals-read",
    )

    primitive_names = {
        capability_id: {
            primitive["mcp_name"] for primitive in capability["primitives"]
        }
        for capability_id, capability in capabilities.items()
    }
    assert primitive_names["eval-request-prepare"] == {
        "aoa_evals_prepare_request_candidate"
    }
    assert primitive_names["proof-result-read"] == {
        "aoa_evals_read_proof_result",
        "aoa-evals://proof-result/{report_id}",
    }
    assert primitive_names["eval-discovery-read"].isdisjoint(
        primitive_names["eval-request-prepare"]
    )
    assert primitive_names["eval-discovery-read"].isdisjoint(
        primitive_names["proof-result-read"]
    )


def test_mcp_capability_contract_cannot_issue_or_infer_proof() -> None:
    contract = _payload(CONTRACT)
    request = next(
        item
        for item in contract["capabilities"]
        if item["capability_id"] == "eval-request-prepare"
    )
    proof_read = next(
        item
        for item in contract["capabilities"]
        if item["capability_id"] == "proof-result-read"
    )

    assert all(
        primitive["effect_class"] == "prepare_candidate"
        for primitive in request["primitives"]
    )
    assert request["primitives"][0]["rollback_route"] == (
        "owner://aoa-evals/rollback/discard-unpersisted-request"
    )
    assert all(
        primitive["effect_class"] == "observe"
        for primitive in proof_read["primitives"]
    )
    assert "no verdict issuance" in proof_read["authority_ceiling"]
