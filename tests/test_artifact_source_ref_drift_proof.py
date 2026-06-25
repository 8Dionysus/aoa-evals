from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def import_artifact_bundles() -> Any:
    candidates: list[Path] = []
    env_root = os.environ.get("ABYSS_MACHINE_REPO_ROOT")
    if env_root:
        candidates.append(Path(env_root))
    candidates.extend(
        [
            REPO_ROOT.parent / "abyss-machine",
            Path.home() / "src" / "abyss-machine",
            Path("/srv/AbyssOS/abyss-machine"),
        ]
    )
    for candidate in candidates:
        module_root = candidate.expanduser() / "src"
        if (module_root / "abyss_machine" / "artifact_bundles.py").is_file():
            sys.path.insert(0, str(module_root))
            return importlib.import_module("abyss_machine.artifact_bundles")
    pytest.skip("abyss-machine artifact_bundles module is unavailable")


def write_verified_registry_record(artifact_bundles: Any, registry: Path, *, evidence_refs: list[str]) -> None:
    record = {
        "schema": "abyss_machine_artifact_bundle_registry_record_v1",
        "record_id": "sha256:" + "a" * 64,
        "artifact_class": "aoa_sdk_python_distribution",
        "bundle_layout": "abyss_machine_artifact_bundle_v1",
        "bundle_ref": "aoa-sdk/dist/abyss-artifact-bundle",
        "bundle_manifest_ref": "sdk/distribution/manifests/python_distribution.bundle.json",
        "subject_digest": "sha256:" + "b" * 64,
        "lifecycle_state": "release-ready",
        "latest_eligible": True,
        "terminal_state": False,
        "verification_ok": True,
        "verification_errors": [],
        "verification_missing": [],
        "verification_warnings": [],
        "required_controls": ["abi_signature", "sbom", "slsa_in_toto"],
        "verified_controls": ["abi_signature", "sbom", "slsa_in_toto"],
        "present_controls": ["abi_signature", "sbom", "slsa_in_toto"],
        "source_repo": "aoa-sdk",
        "source_ref": "sdk/distribution/manifests/python_distribution.bundle.json",
        "source_refs": [
            "sdk/distribution/manifests/python_distribution.bundle.json",
            *evidence_refs,
        ],
        "producer": "aoa-sdk:release-audit-publish-helper@commit:current",
        "producer_command": "python mechanics/release-support/parts/release-audit-publish-helper/scripts/validate_abyss_machine_package_artifact_bundle.py --json",
        "trust_root_mode": "host_managed",
        "verifier_versions": {"aoa-evals": "source-ref-drift-proof"},
        "evidence_refs": evidence_refs,
        "created_at": "2026-06-21T00:00:00Z",
        "policy_ref": artifact_bundles.POLICY_REF,
        "abi_ref": artifact_bundles.ABI_REF,
    }
    records = registry / artifact_bundles.BUNDLE_REGISTRY_RECORDS_DIR
    records.mkdir(parents=True)
    (records / "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json").write_text(
        json.dumps(record, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def test_source_ref_drift_proof_distinguishes_promoted_and_unpromoted_refs(tmp_path: Path) -> None:
    artifact_bundles = import_artifact_bundles()
    promoted_registry = tmp_path / "promoted-registry"
    stale_registry = tmp_path / "stale-registry"
    changed_path = "sdk/distribution/manifests/python_distribution.bundle.json"

    write_verified_registry_record(artifact_bundles, promoted_registry, evidence_refs=["commit:current"])
    write_verified_registry_record(artifact_bundles, stale_registry, evidence_refs=["commit:previous"])

    promoted = artifact_bundles.artifact_affected(
        [changed_path],
        artifact_class="aoa_sdk_python_distribution",
        changed_source_repo="aoa-sdk",
        changed_source_ref="commit:current",
        registry_dir=promoted_registry,
    )
    stale = artifact_bundles.artifact_affected(
        [changed_path],
        artifact_class="aoa_sdk_python_distribution",
        changed_source_repo="aoa-sdk",
        changed_source_ref="commit:current",
        registry_dir=stale_registry,
    )

    promoted_row = promoted["rows"][0]
    stale_row = stale["rows"][0]

    assert promoted["summary"]["status_counts"] == {"fresh": 1}
    assert promoted_row["affected"] is False
    assert promoted_row["verdict"] == "fresh"
    assert promoted_row["source_ref_status"]["matched"] is True
    assert promoted_row["source_ref_status"]["matched_ref"] == "commit:current"
    assert promoted_row["drift"]["status"] == "fresh"
    assert promoted_row["drift"]["operationally_blocking"] is False
    assert promoted_row["drift"]["source_ref_state"] == "proved_current"
    assert promoted_row["trust_gate"]["verdict"] == "allow"

    assert stale["summary"]["status_counts"] == {"blocked_by_missing_sibling": 1}
    assert stale_row["affected"] is True
    assert stale_row["verdict"] == "blocked_by_missing_sibling"
    assert stale_row["source_ref_status"]["matched"] is False
    assert stale_row["source_ref_status"]["expected"] == "commit:current"
    assert stale_row["drift"]["status"] == "blocked_missing_sibling"
    assert stale_row["drift"]["operationally_blocking"] is True
    assert stale_row["drift"]["needs_rebuild"] is True
    assert stale_row["drift"]["source_ref_state"] == "missing_current_proof"
    assert stale_row["next_actions"][1] == "run the producer profile in owner repo aoa-sdk"
