from __future__ import annotations

import importlib.util
from copy import deepcopy
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_os_abyss_artifact_trust_plane.py"


def load_validator_module() -> Any:
    spec = importlib.util.spec_from_file_location("os_trust_plane_validator", VALIDATOR_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


OWNER_CLASS_BY_REPO = {
    "abyss-machine": "bootstrap_install_bundle",
    "abyss-stack": "abyss_stack_runtime_config_bundle",
    "Tree-of-Sophia": "tree_of_sophia_generated_readmodel_bundle",
    "Dionysus": "dionysus_seed_route_readmodel_bundle",
    "aoa-agents": "role_contract_registry",
    "aoa-evals": "aoa_evals_generated_report_index_bundle",
    "aoa-kag": "derived_kag_registry_readmodel_bundle",
    "aoa-memo": "derived_memory_object_readmodel_family",
    "aoa-playbooks": "playbook_registry_bundle",
    "aoa-routing": "thin_routing_readmodel_bundle",
    "aoa-sdk": "aoa_sdk_python_distribution",
    "aoa-session-memory": "aoa_session_memory_portable_bundle",
    "aoa-skills": "aoa_skills_release_manifest",
    "aoa-stats": "derived_observability_readmodel_catalog",
    "aoa-techniques": "source_owned_kag_export_capsule",
}


def requirement_row(artifact_class: str, owner: str) -> dict[str, Any]:
    return {
        "artifact_class": artifact_class,
        "owner_repo": owner,
        "controls": {"required": ["abi_signature"]},
        "producer_profile": {"producer": f"{owner} producer"},
        "trust_gate_status": {"checked": True, "verdict": "allow"},
        "consumer": {"trust_gate": f"abyss-machine artifacts trust-gate --artifact-class {artifact_class} --json"},
        "agent_loop": {
            "requirements": "requirements",
            "producer_profiles": "producer-profiles",
            "affected": "affected",
            "build_sidecars": "build-sidecars",
            "evidence_promote": "evidence-promote",
            "trust_gate": "trust-gate",
        },
    }


def coverage_row(artifact_class: str, *, durable_only: bool = False) -> dict[str, Any]:
    return {
        "artifact_class": artifact_class,
        "status": "DURABLE_GATE_COVERED" if durable_only else "FULLY_COVERED",
        "manual_positive_evidence": [] if durable_only else [f"{artifact_class}/positive.json"],
        "manual_negative_evidence": [] if durable_only else [f"{artifact_class}/negative.json"],
        "installed_verification": {"trust_gate_verdict": "allow"},
    }


def make_payloads() -> dict[str, dict[str, Any]]:
    validator = load_validator_module()
    class_owner = {artifact_class: owner for owner, artifact_class in OWNER_CLASS_BY_REPO.items()}
    for artifact_class in validator.REQUIRED_SCENARIO_CLASSES:
        class_owner.setdefault(artifact_class, "abyss-machine")
    artifact_classes = sorted(class_owner)
    requirements_rows = [
        requirement_row(artifact_class, owner)
        for artifact_class, owner in sorted(class_owner.items())
    ]
    full_rows = [coverage_row(artifact_class) for artifact_class in artifact_classes]
    durable_rows = [coverage_row(artifact_class, durable_only=True) for artifact_class in artifact_classes]
    producer_profile_rows = [
        {
            "profile_id": owner,
            "owner_repo": owner,
            "artifact_classes": [artifact_class],
            "owner_route_refs": ["AGENTS.md"],
            "validator_commands": ["python scripts/release_check.py"],
            "produced_sidecars": ["artifact.identity.json"],
            "consumer_expectations": ["consume only after trust-gate verdict"],
            "owner_boundaries": ["source owner remains stronger than read-model"],
            "trust_root_modes": ["local_dev", "github_oidc"],
        }
        for owner, artifact_class in sorted(OWNER_CLASS_BY_REPO.items())
    ]
    for row in producer_profile_rows:
        if row["owner_repo"] == "abyss-machine":
            row["artifact_classes"].extend(
                [
                    "runtime_or_container_artifact",
                    "ai_model_or_runtime_bundle",
                    "public_source_seed",
                    "public_media_export",
                    "browser_extension_package",
                    "host_local_evidence",
                ]
            )
    return {
        "requirements": {
            "ok": True,
            "summary": {"artifact_classes": len(requirements_rows), "missing_artifact_classes": []},
            "rows": requirements_rows,
        },
        "producer_profiles": {
            "ok": True,
            "summary": {
                "profiles": len(producer_profile_rows),
                "owner_repos": sorted(OWNER_CLASS_BY_REPO),
                "artifact_classes": artifact_classes,
                "artifact_class_count": len(artifact_classes),
            },
            "rows": producer_profile_rows,
            "agent_loop": {
                "producer_profiles": "abyss-machine artifacts producer-profiles --artifact-class ARTIFACT_CLASS --json",
                "trust_gate": "abyss-machine artifacts trust-gate --artifact-class ARTIFACT_CLASS --json",
            },
            "claim_limits": ["Producer profiles are read-models, not enforcement."],
        },
        "trust_coverage": {
            "ok": True,
            "summary": {
                "artifact_classes": len(full_rows),
                "fully_covered": len(full_rows),
                "trust_tools_status": "ready",
            },
            "rows": full_rows,
        },
        "durable_trust_coverage": {
            "ok": True,
            "summary": {
                "artifact_classes": len(durable_rows),
                "fully_covered": 0,
                "durable_gate_covered": len(durable_rows),
            },
            "manual_evidence_roots": [],
            "rows": durable_rows,
        },
        "policy_drift": {
            "known_verdicts": sorted(validator.KNOWN_AFFECTED_VERDICTS),
            "summary": {"artifact_classes": len(artifact_classes), "status_counts": {"needs_reverify": len(artifact_classes)}},
            "rows": [],
        },
        "sibling_blocked": {
            "rows": [
                {
                    "artifact_class": "aoa_sdk_python_distribution",
                    "verdict": "blocked_by_missing_sibling",
                    "source_ref_status": {"matched": False},
                }
            ]
        },
        "sibling_accepted_lag": {
            "rows": [
                {
                    "artifact_class": "aoa_sdk_python_distribution",
                    "verdict": "accepted_lag",
                    "source_ref_status": {"matched": False},
                }
            ]
        },
    }


def test_os_artifact_trust_plane_validator_accepts_full_durable_and_drift_scenarios() -> None:
    validator = load_validator_module()

    result = validator.validate_payloads(make_payloads())

    assert result["ok"] is True
    assert result["issues"] == []
    assert "durable-only pass must stay weaker than FULLY_COVERED" in result["claim_limits"][2]
    assert "aoa_sdk_python_distribution" in result["checked"]["requirements"]["artifact_classes"]
    assert "aoa-sdk" in result["checked"]["producer_profiles"]["owner_repos"]
    assert result["checked"]["drift"]["sibling_blocked_verdict"] == "blocked_by_missing_sibling"
    assert result["checked"]["drift"]["sibling_accepted_lag_verdict"] == "accepted_lag"


def test_os_artifact_trust_plane_validator_rejects_missing_manual_negative_evidence() -> None:
    validator = load_validator_module()
    payloads = make_payloads()
    payloads["trust_coverage"]["rows"][0]["manual_negative_evidence"] = []

    result = validator.validate_payloads(payloads)

    assert result["ok"] is False
    assert any(issue["check"] == "trust_coverage.manual_negative" for issue in result["issues"])


def test_os_artifact_trust_plane_validator_rejects_durable_only_full_claim() -> None:
    validator = load_validator_module()
    payloads = make_payloads()
    payloads["durable_trust_coverage"]["summary"]["fully_covered"] = 1
    payloads["durable_trust_coverage"]["rows"][0]["manual_positive_evidence"] = ["tmp/manual-positive.json"]

    result = validator.validate_payloads(payloads)

    assert result["ok"] is False
    assert any(issue["check"] == "durable_trust_coverage.claim_level" for issue in result["issues"])
    assert any(issue["check"] == "durable_trust_coverage.manual_evidence" for issue in result["issues"])


def test_os_artifact_trust_plane_validator_rejects_unaccepted_sibling_drift_claim() -> None:
    validator = load_validator_module()
    payloads = deepcopy(make_payloads())
    payloads["sibling_accepted_lag"]["rows"][0]["verdict"] = "blocked_by_missing_sibling"

    result = validator.validate_payloads(payloads)

    assert result["ok"] is False
    assert any(issue["check"] == "affected.accepted_lag" for issue in result["issues"])


def test_os_artifact_trust_plane_validator_rejects_missing_producer_profile_owner() -> None:
    validator = load_validator_module()
    payloads = deepcopy(make_payloads())
    payloads["producer_profiles"]["rows"] = [
        row for row in payloads["producer_profiles"]["rows"] if row["owner_repo"] != "Tree-of-Sophia"
    ]

    result = validator.validate_payloads(payloads)

    assert result["ok"] is False
    assert any(issue["check"] == "producer_profiles.owner_repos" for issue in result["issues"])
