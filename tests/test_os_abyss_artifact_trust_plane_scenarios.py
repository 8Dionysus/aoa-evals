from __future__ import annotations

import importlib.util
import os
import sys
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


KNOWN_DRIFT_STATUSES = [
    "fresh",
    "missing_durable_evidence",
    "rebuild_required",
    "reverify_required",
    "blocked_missing_sibling",
    "accepted_lag",
    "manual_review_required",
]


def drift_state(
    status: str,
    *,
    operationally_blocking: bool,
    needs_rebuild: bool = False,
    needs_reverify: bool = False,
    accepted_lag: bool = False,
    lag_policy: str = "not_accepted",
    source_ref_state: str = "not_requested",
) -> dict[str, Any]:
    return {
        "status": status,
        "known_statuses": KNOWN_DRIFT_STATUSES,
        "operationally_blocking": operationally_blocking,
        "needs_rebuild": needs_rebuild,
        "needs_reverify": needs_reverify,
        "accepted_lag": accepted_lag,
        "lag_policy": lag_policy,
        "source_ref_state": source_ref_state,
        "evidence_state": "durable_latest_present",
        "reason_count": 1,
        "explanation": f"{status} fixture",
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


def public_media_c2pa_real_blocker_row(*, durable_only: bool = False) -> dict[str, Any]:
    return {
        "artifact_class": "public_media_export",
        "status": "DEFERRED_WITH_REAL_BLOCKER",
        "remaining_blocker": (
            "Public media export has release evidence and valid C2PA asset binding, "
            "but the C2PA signing credential is not production trust-list trusted."
        ),
        "required_controls": ["c2pa"],
        "manual_positive_evidence": [] if durable_only else ["public_media_export/positive.json"],
        "manual_negative_evidence": [] if durable_only else ["public_media_export/negative.json"],
        "installed_verification": {
            "latest_record_verification_ok": True,
            "verified_controls": ["c2pa"],
            "manual_positive_evidence_count": 0 if durable_only else 1,
            "manual_negative_evidence_count": 0 if durable_only else 1,
            "trust_gate_ok": True,
            "trust_gate_verdict": "warn",
        },
        "source_freshness": {"freshness": "fresh"},
        "persistent_registry_status": {
            "has_latest": True,
            "latest_eligible": True,
            "verification_missing": [],
            "verification_errors": [],
            "trust_gate_verdict": "warn",
        },
    }


def replace_coverage_row(payload: dict[str, Any], replacement: dict[str, Any]) -> None:
    artifact_class = replacement["artifact_class"]
    payload["rows"] = [
        replacement if row["artifact_class"] == artifact_class else row
        for row in payload["rows"]
    ]


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
            "known_drift_statuses": sorted(validator.KNOWN_DRIFT_STATUSES),
            "summary": {
                "artifact_classes": len(artifact_classes),
                "status_counts": {"needs_reverify": len(artifact_classes)},
                "operationally_blocking": len(artifact_classes),
                "accepted_lag": 0,
            },
            "rows": [
                {
                    "artifact_class": artifact_class,
                    "verdict": "needs_reverify",
                    "source_ref_status": {"required": False, "matched": None},
                    "drift": drift_state(
                        "reverify_required",
                        operationally_blocking=True,
                        needs_reverify=True,
                    ),
                }
                for artifact_class in artifact_classes
            ],
        },
        "sibling_blocked": {
            "rows": [
                {
                    "artifact_class": "aoa_sdk_python_distribution",
                    "verdict": "blocked_by_missing_sibling",
                    "source_ref_status": {"matched": False},
                    "drift": drift_state(
                        "blocked_missing_sibling",
                        operationally_blocking=True,
                        needs_rebuild=True,
                        lag_policy="blocked",
                        source_ref_state="missing_current_proof",
                    ),
                }
            ]
        },
        "sibling_accepted_lag": {
            "rows": [
                {
                    "artifact_class": "aoa_sdk_python_distribution",
                    "verdict": "accepted_lag",
                    "source_ref_status": {"matched": False},
                    "drift": drift_state(
                        "accepted_lag",
                        operationally_blocking=False,
                        accepted_lag=True,
                        lag_policy="accepted",
                        source_ref_state="missing_current_proof",
                    ),
                }
            ]
        },
    }


def test_os_artifact_trust_plane_validator_accepts_full_durable_and_drift_scenarios() -> None:
    validator = load_validator_module()

    result = validator.validate_payloads(make_payloads())

    assert result["ok"] is True
    assert result["issues"] == []
    assert any("durable-only pass must stay weaker than FULLY_COVERED" in item for item in result["claim_limits"])
    assert "aoa_sdk_python_distribution" in result["checked"]["requirements"]["artifact_classes"]
    assert "aoa-sdk" in result["checked"]["producer_profiles"]["owner_repos"]
    assert result["checked"]["drift"]["policy_drift_statuses"] == ["reverify_required"]
    assert result["checked"]["drift"]["sibling_blocked_verdict"] == "blocked_by_missing_sibling"
    assert result["checked"]["drift"]["sibling_blocked_drift_status"] == "blocked_missing_sibling"
    assert result["checked"]["drift"]["sibling_blocked_operationally_blocking"] is True
    assert result["checked"]["drift"]["sibling_accepted_lag_verdict"] == "accepted_lag"
    assert result["checked"]["drift"]["sibling_accepted_lag_drift_status"] == "accepted_lag"
    assert result["checked"]["drift"]["sibling_accepted_lag_operationally_blocking"] is False


def test_os_artifact_trust_plane_validator_accepts_declared_public_media_c2pa_real_blocker() -> None:
    validator = load_validator_module()
    payloads = make_payloads()
    replace_coverage_row(payloads["trust_coverage"], public_media_c2pa_real_blocker_row())
    replace_coverage_row(payloads["durable_trust_coverage"], public_media_c2pa_real_blocker_row(durable_only=True))
    payloads["trust_coverage"]["summary"]["fully_covered"] -= 1
    payloads["trust_coverage"]["summary"]["deferred_with_real_blocker"] = 1
    payloads["durable_trust_coverage"]["summary"]["durable_gate_covered"] -= 1
    payloads["durable_trust_coverage"]["summary"]["deferred_with_real_blocker"] = 1

    result = validator.validate_payloads(payloads)

    assert result["ok"] is True
    assert result["checked"]["trust_coverage"]["accepted_real_blockers"] == ["public_media_export"]
    assert result["checked"]["durable_trust_coverage"]["accepted_real_blockers"] == ["public_media_export"]


def test_os_artifact_trust_plane_validator_rejects_undeclared_real_blocker() -> None:
    validator = load_validator_module()
    payloads = make_payloads()
    row = public_media_c2pa_real_blocker_row()
    row["artifact_class"] = "public_source_seed"
    replace_coverage_row(payloads["trust_coverage"], row)
    payloads["trust_coverage"]["summary"]["fully_covered"] -= 1
    payloads["trust_coverage"]["summary"]["deferred_with_real_blocker"] = 1

    result = validator.validate_payloads(payloads)

    assert result["ok"] is False
    assert any(issue["check"] == "trust_coverage.accepted_real_blocker" for issue in result["issues"])


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


def test_os_artifact_trust_plane_validator_rejects_accepted_lag_without_nonblocking_drift() -> None:
    validator = load_validator_module()
    payloads = deepcopy(make_payloads())
    payloads["sibling_accepted_lag"]["rows"][0]["drift"]["operationally_blocking"] = True

    result = validator.validate_payloads(payloads)

    assert result["ok"] is False
    assert any(issue["check"] == "affected.accepted_lag_blocking" for issue in result["issues"])


def test_os_artifact_trust_plane_validator_rejects_missing_producer_profile_owner() -> None:
    validator = load_validator_module()
    payloads = deepcopy(make_payloads())
    payloads["producer_profiles"]["rows"] = [
        row for row in payloads["producer_profiles"]["rows"] if row["owner_repo"] != "Tree-of-Sophia"
    ]

    result = validator.validate_payloads(payloads)

    assert result["ok"] is False
    assert any(issue["check"] == "producer_profiles.owner_repos" for issue in result["issues"])


def test_artifact_trust_plane_command_prefers_installed_cli_over_implicit_checkout(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    validator = load_validator_module()
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_cli = fake_bin / "abyss-machine"
    fake_cli.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    fake_cli.chmod(0o755)
    monkeypatch.delenv("ABYSS_MACHINE_REPO_ROOT", raising=False)
    monkeypatch.setenv("PATH", str(fake_bin))

    command, env = validator._resolve_artifacts_command(["trust-coverage"], repo_root=REPO_ROOT)

    assert command == [str(fake_cli), "artifacts", "trust-coverage", "--json"]
    assert env.get("PYTHONPATH", "").split(os.pathsep)[0] != str(Path.home() / "src" / "abyss-machine" / "src")


def test_artifact_trust_plane_command_honors_explicit_source_root(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    validator = load_validator_module()
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_cli = fake_bin / "abyss-machine"
    fake_cli.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    fake_cli.chmod(0o755)
    source_root = tmp_path / "abyss-machine"
    module_root = source_root / "src"
    package_root = module_root / "abyss_machine"
    package_root.mkdir(parents=True)
    (package_root / "cli.py").write_text("def main():\n    return 0\n", encoding="utf-8")
    monkeypatch.setenv("PATH", str(fake_bin))
    monkeypatch.setenv("ABYSS_MACHINE_REPO_ROOT", str(source_root))

    command, env = validator._resolve_artifacts_command(["trust-coverage"], repo_root=REPO_ROOT)

    assert command == [
        sys.executable,
        "-m",
        "abyss_machine.cli",
        "artifacts",
        "trust-coverage",
        "--json",
    ]
    assert env["PYTHONPATH"].split(os.pathsep)[0] == str(module_root)
