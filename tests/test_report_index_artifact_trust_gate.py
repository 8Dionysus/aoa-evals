from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_abyss_machine_report_index_bundle.py"
MANIFEST_PATH = (
    REPO_ROOT
    / "mechanics"
    / "release-support"
    / "parts"
    / "artifact-bundles"
    / "manifests"
    / "report_index.bundle.json"
)
VALIDATOR_INVENTORY_PATH = REPO_ROOT / "docs" / "validation" / "validator_inventory.json"
PART_README_PATH = REPO_ROOT / "mechanics" / "release-support" / "parts" / "artifact-bundles" / "README.md"


def load_validator_module() -> Any:
    spec = importlib.util.spec_from_file_location("report_index_bundle_validator", VALIDATOR_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeArtifactBundles:
    def __init__(self, trust_gate_response: dict[str, Any]) -> None:
        self.trust_gate_response = trust_gate_response
        self.trust_gate_calls: list[dict[str, Any]] = []
        self.materialize_calls: list[dict[str, Any]] = []
        self.records: list[dict[str, Any]] = []

    def trust_gate(self, registry_dir: Path, **kwargs: Any) -> dict[str, Any]:
        self.trust_gate_calls.append({"registry_dir": registry_dir, **kwargs})
        return self.trust_gate_response

    def write_bundle_registry_record(self, bundle_dir: Path, registry_dir: Path, **kwargs: Any) -> dict[str, Any]:
        state = str(kwargs.get("lifecycle_state") or "")
        record = {
            "record_id": f"record-{len(self.records) + 1}",
            "subject_digest": "sha256:" + "1" * 64,
            "lifecycle_state": state,
        }
        self.records.append(record)
        return {"ok": True, "record": record}

    def promote_bundle_evidence(self, bundle_dir: Path, registry_dir: Path, **kwargs: Any) -> dict[str, Any]:
        registered = self.write_bundle_registry_record(bundle_dir, registry_dir, **kwargs)
        return {
            "ok": registered["ok"],
            "promotion": {"record_id": registered["record"]["record_id"]},
            "record": registered["record"],
        }

    def read_bundle_registry(self, registry_dir: Path, *, artifact_class: str) -> dict[str, Any]:
        release_ready = [record for record in self.records if record.get("lifecycle_state") == "release-ready"]
        latest_record = release_ready[-1] if release_ready else None
        if self.records and self.records[-1].get("lifecycle_state") == "revoked":
            latest_record = None
        if latest_record and os.environ.get("ABYSS_MACHINE_ARTIFACT_SUBJECT_STORE_ROOT"):
            latest_record["artifact_subject_store"] = {"ok": True}
        return {"latest_by_artifact_class": {artifact_class: latest_record} if latest_record else {}}

    def materialize_artifact_subjects(
        self,
        bundle_dir: Path,
        *,
        store_root: Path,
        registry_dir: Path,
        manifest_ref: Path,
        consumer_intent: str,
        expected_source_repo: str,
        expected_trust_root_mode: str,
        repo_root: Path,
    ) -> dict[str, Any]:
        self.materialize_calls.append(
            {
                "bundle_dir": bundle_dir,
                "store_root": store_root,
                "registry_dir": registry_dir,
                "manifest_ref": manifest_ref,
                "consumer_intent": consumer_intent,
                "expected_source_repo": expected_source_repo,
                "expected_trust_root_mode": expected_trust_root_mode,
                "repo_root": repo_root,
            }
        )
        return {"ok": True, "aggregate_digest": "sha256:" + "3" * 64}


def allow_gate_response() -> dict[str, Any]:
    return {
        "ok": True,
        "verdict": "allow",
        "decision": {"model": "fail_closed_consumer_admission", "allow": True},
        "inspected_claims": {
            "registry_latest": {"selected_record_is_latest": True},
            "controls": {"required_controls_missing": []},
            "source": {"source_repo_matched": True},
            "trust_root": {"trust_root_mode_matched": True},
            "artifact_subject_store": {"ok": True},
        },
    }


def deny_terminal_gate_response() -> dict[str, Any]:
    return {
        "ok": True,
        "verdict": "deny",
        "decision": {"model": "fail_closed_consumer_admission", "allow": False},
        "inspected_claims": {"lifecycle": {"terminal_state": True}},
    }


def test_report_index_manifest_and_inventory_keep_consumer_trust_gate_contract() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    inventory = json.loads(VALIDATOR_INVENTORY_PATH.read_text(encoding="utf-8"))
    part_readme = PART_README_PATH.read_text(encoding="utf-8")

    consumer_contract = manifest["consumer_contract"]
    consumer_commands = "\n".join(manifest["consumer_command"])
    report_index_entry = next(
        entry
        for entry in inventory["entries"]
        if entry["path"] == "scripts/validate_abyss_machine_report_index_bundle.py"
    )

    assert "trust-gate" in consumer_contract["stable_interface"]
    assert "trust-gate allow/warn" in consumer_contract["consumer_expectation"]
    assert "abyss-machine artifacts evidence-promote" in consumer_commands
    assert "abyss-machine artifacts materialize-subjects" in consumer_commands
    assert "abyss-machine artifacts trust-gate" in consumer_commands
    assert "abyss-machine artifacts registry-latest" in consumer_commands
    assert "--consumer-ref aoa-evals:generated-report-index" in consumer_commands
    assert "--source-repo aoa-evals" in consumer_commands
    assert "--trust-root-mode host_managed" in consumer_commands
    assert consumer_contract["subject_store_required"] is True
    assert consumer_contract["admission_gate"] == "fail_closed_consumer_admission"
    assert "consumer trust-gate allow/deny readout" in report_index_entry["output"]
    assert "materialized subject-store readout" in report_index_entry["output"]
    assert "materializes the" in part_readme
    assert "report-index subject store" in part_readme
    assert "revoked-record `trust-gate` denial" in part_readme


def test_trust_gate_allow_latest_requires_fail_closed_latest_controls_and_source(tmp_path: Path) -> None:
    validator = load_validator_module()
    fake = FakeArtifactBundles(allow_gate_response())
    registry_roundtrip = {"promoted": {"record": {"subject_digest": "sha256:" + "2" * 64}}}

    result = validator._trust_gate_allow_latest(fake, tmp_path, registry_roundtrip)

    assert result["ok"] is True
    assert fake.trust_gate_calls == [
        {
            "registry_dir": tmp_path,
            "artifact_class": "aoa_evals_generated_report_index_bundle",
            "subject_digest": "sha256:" + "2" * 64,
            "consumer_intent": "agent",
            "expected_source_repo": "aoa-evals",
            "expected_trust_root_mode": "host_managed",
        }
    ]

    for mutated_claim in (
        {"decision": {"model": "shape_only", "allow": True}},
        {"inspected_claims": {"registry_latest": {"selected_record_is_latest": False}}},
        {"inspected_claims": {"controls": {"required_controls_missing": ["sbom"]}}},
        {"inspected_claims": {"source": {"source_repo_matched": False}}},
        {"inspected_claims": {"trust_root": {"trust_root_mode_matched": False}}},
        {"inspected_claims": {"artifact_subject_store": {"ok": False}}},
    ):
        response = allow_gate_response()
        for key, value in mutated_claim.items():
            if key == "inspected_claims":
                response[key].update(value)
            else:
                response[key] = value
        assert validator._trust_gate_allow_latest(FakeArtifactBundles(response), tmp_path, registry_roundtrip)["ok"] is False


def test_terminal_registry_state_requires_revoked_record_trust_gate_deny(tmp_path: Path) -> None:
    validator = load_validator_module()

    denied = validator._verify_terminal_registry_state(
        FakeArtifactBundles(deny_terminal_gate_response()),
        tmp_path,
        tmp_path,
        MANIFEST_PATH,
        tmp_path,
    )
    assert denied["ok"] is True
    assert denied["revoked_trust_gate"]["verdict"] == "deny"

    allowed = validator._verify_terminal_registry_state(
        FakeArtifactBundles(allow_gate_response()),
        tmp_path,
        tmp_path,
        MANIFEST_PATH,
        tmp_path,
    )
    assert allowed["ok"] is False
    assert allowed["revoked_trust_gate"]["verdict"] == "allow"


def test_materialized_subject_store_requires_trusted_source_scoped_subject(tmp_path: Path) -> None:
    validator = load_validator_module()
    fake = FakeArtifactBundles(allow_gate_response())

    result = validator._verify_materialized_subject_store(
        fake,
        MANIFEST_PATH,
        tmp_path,
        tmp_path / "registry",
        tmp_path,
        tmp_path,
    )

    assert result["ok"] is True
    assert fake.materialize_calls == [
        {
            "bundle_dir": tmp_path,
            "store_root": tmp_path / "subject-store",
            "registry_dir": tmp_path / "registry",
            "manifest_ref": MANIFEST_PATH,
            "consumer_intent": "agent",
            "expected_source_repo": "aoa-evals",
            "expected_trust_root_mode": "host_managed",
            "repo_root": tmp_path,
        }
    ]
    assert fake.trust_gate_calls[-1] == {
        "registry_dir": tmp_path / "registry",
        "artifact_class": "aoa_evals_generated_report_index_bundle",
        "subject_digest": "sha256:" + "3" * 64,
        "consumer_intent": "agent",
        "expected_source_repo": "aoa-evals",
        "expected_trust_root_mode": "host_managed",
    }

    fake = FakeArtifactBundles({**allow_gate_response(), "verdict": "warn"})
    assert (
        validator._verify_materialized_subject_store(
            fake,
            MANIFEST_PATH,
            tmp_path,
            tmp_path / "registry",
            tmp_path,
            tmp_path,
        )["ok"]
        is True
    )

    response = allow_gate_response()
    response["inspected_claims"]["artifact_subject_store"] = {"ok": False}
    fake = FakeArtifactBundles(response)
    assert (
        validator._verify_materialized_subject_store(
            fake,
            MANIFEST_PATH,
            tmp_path,
            tmp_path / "registry",
            tmp_path,
            tmp_path,
        )["ok"]
        is False
    )
