"""Regression tests for the bounded code-observation refactor contract."""

import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = (
    ROOT
    / "evals/capability/aoa-code-observation-refactor-integrity/runners/run_scenarios.py"
)
EXAMPLE = (
    ROOT
    / "evals/capability/aoa-code-observation-refactor-integrity/fixtures/observation-report.example.json"
)
sys.path.insert(0, str(RUNNER.parent))
import run_scenarios as runner  # noqa: E402
import provider_agreement  # noqa: E402
import adjacent_provider_evidence  # noqa: E402
import provider_execution  # noqa: E402


def run_runner(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RUNNER), *arguments],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def _agreement_envelope(provider_id: str, facts: list[str]) -> dict[str, object]:
    observations: list[dict[str, object]] = []
    for index, fact in enumerate(facts):
        kind, label = fact.split(":", 1)
        observations.append(
            {
                "capability_class": "code-structure",
                "observation_kind": "symbol" if kind == "definition" else "relation",
                "observation_id": f"{provider_id}:{index}",
                "semantic_key": f"typescript:{kind}:{label}",
                "subject": {
                    "label": label,
                    "qualified_name": label,
                    "symbol_id": f"typescript:{label}",
                    "symbol_kind": "function",
                },
                "occurrence": {
                    "start_line": 1,
                    "start_column": 1,
                    "end_line": 1,
                    "end_column": 6,
                },
                "confidence": {"evidence_class": "observed", "value": 1},
                "relation": None
                if kind == "definition"
                else {"kind": kind, "target_name": label},
            }
        )
    return {
        "schema_version": "aoa-code-observation-v1",
        "provider": {
            "id": provider_id,
            "version": "1.0.0",
            "config_digest": "0" * 64,
            "lane": {"status": "supplied_unadmitted"},
        },
        "source": {
            "repo": "fixture",
            "path": "src/render.ts",
            "source_epoch": "git:fixture",
            "content_digest": "1" * 64,
            "language": "typescript",
        },
        "parse_status": "parsed",
        "observations": observations,
        "qualification": {"machine_admission": {"state": "not_admitted"}},
    }


def test_typescript_provider_agreement_requires_shared_source_and_facts(
    tmp_path: Path,
) -> None:
    facts = ["definition:render"]
    payload = {
        "schema_version": "aoa_code_observation_provider_agreement_v1",
        "observed_at": "2026-08-29T00:00:00Z",
        "required_facts": facts,
        "claim_boundary": provider_agreement.CLAIM_BOUNDARY,
        "envelopes": [
            _agreement_envelope(provider_id, facts)
            for provider_id in ("tree-sitter", "scip", "lsp")
        ],
    }
    path = tmp_path / "agreement.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    result = provider_agreement.validate(path)
    assert result["issues"] == []
    assert result["verdict"] == "supports bounded cross-provider agreement"

    payload["envelopes"][2]["source"]["source_epoch"] = "git:other"
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "source_identity_mismatch" in provider_agreement.validate(path)["issues"]


def test_provider_agreement_rejects_claim_boundary_drift(tmp_path: Path) -> None:
    facts = ["definition:render"]
    payload = {
        "schema_version": "aoa_code_observation_provider_agreement_v1",
        "observed_at": "2026-08-29T00:00:00Z",
        "required_facts": facts,
        "claim_boundary": "This envelope proves provider correctness and admission.",
        "envelopes": [
            _agreement_envelope(provider_id, facts)
            for provider_id in ("tree-sitter", "scip", "lsp")
        ],
    }
    path = tmp_path / "agreement-boundary-drift.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = provider_agreement.validate(path)

    assert any("claim_boundary" in issue for issue in result["issues"])
    assert result["verdict"] == "does not support bounded cross-provider agreement"


def test_adjacent_provider_evidence_requires_all_unadmitted_classes(
    tmp_path: Path,
) -> None:
    source_epoch = "commit:" + "a" * 40
    specs = {
        "static_security": ("semgrep", "static-security"),
        "software_components": ("syft", "software-components"),
        "artifact_provenance": ("in-toto", "artifact-provenance"),
        "document_structure": ("markitdown", "document-structure"),
    }
    batches = {}
    observation_specs = {
        "static_security": ("security_finding", "sarif:"),
        "software_components": ("software_component", "component:"),
        "artifact_provenance": ("artifact_subject", "provenance:"),
        "document_structure": ("heading", "document:"),
    }
    for key, (provider_id, capability) in specs.items():
        symbol_kind, semantic_prefix = observation_specs[key]
        batches[key] = {
            "schema_version": "aoa-code-observation-v1",
            "capability_class": capability,
            "provider": {"id": provider_id, "lane": {"status": "supplied_unadmitted"}},
            "source": {"source_epoch": source_epoch},
            "parse_status": "parsed",
            "observations": [
                {
                    "capability_class": capability,
                    "observation_kind": "symbol",
                    "observation_id": f"{provider_id}:0",
                    "semantic_key": semantic_prefix + "fixture",
                    "subject": {
                        "label": "fixture",
                        "qualified_name": "fixture",
                        "symbol_id": semantic_prefix + "fixture",
                        "symbol_kind": symbol_kind,
                    },
                    "occurrence": {
                        "start_line": 1,
                        "start_column": 1,
                        "end_line": 1,
                        "end_column": 1,
                    },
                    "confidence": {"evidence_class": "observed", "value": 1},
                    "relation": None,
                }
            ],
            "qualification": {"machine_admission": {"state": "not_admitted"}},
        }
    payload = {
        "schema": "abyssos_adjacent_provider_evidence_v1",
        "goal_id": "fixture",
        "observed_at": "2026-08-29T00:00:00Z",
        "source_epoch": source_epoch,
        "artifact": {
            "sha256": "sha256:" + "1" * 64,
            "subject_digest": "sha256:" + "2" * 64,
            "signature_status": "missing",
            "admission_status": "not_admitted",
        },
        "providers": {},
        "batches": batches,
        "summary": {"all_provider_lanes_unadmitted": True},
        "claim_limits": adjacent_provider_evidence.CLAIM_LIMITS,
    }
    path = tmp_path / "adjacent.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    result = adjacent_provider_evidence.validate(path)
    assert result["issues"] == []
    assert result["verdict"] == "supports bounded adjacent-provider envelope evidence"

    payload["claim_limits"] = ["This packet proves provider correctness."] * 3
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert any(
        "claim_limits" in issue
        for issue in adjacent_provider_evidence.validate(path)["issues"]
    )

    payload["claim_limits"] = adjacent_provider_evidence.CLAIM_LIMITS
    payload["batches"]["static_security"]["qualification"]["machine_admission"][
        "state"
    ] = "admitted"
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert (
        "provider_not_bounded:semgrep"
        in adjacent_provider_evidence.validate(path)["issues"]
    )


def test_example_observation_report_supports_all_cases() -> None:
    result = run_runner("run-scenarios")
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["scenario_count"] == 12
    assert summary["passed_count"] == 12
    assert summary["failed_count"] == 0
    assert summary["verdict"] == "supports bounded contract"


def test_operation_drift_is_rejected(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["observations"][0]["operation"] = "delete"
    mutated = tmp_path / "operation-drift.json"
    mutated.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(mutated))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any(
        "operation_mismatch:rename-symbol" in error for error in payload["errors"]
    )


def test_fixture_manifest_is_digest_bound() -> None:
    result = run_runner("validate-fixture")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["family_id"] == "refactor-torture-v1"
    assert payload["case_count"] == 12
    assert payload["fixture_digest"].startswith("sha256:")


def test_unexpected_case_is_counted_and_summary_remains_schema_valid(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    unexpected = copy.deepcopy(report["observations"][0])
    unexpected["case_id"] = "unexpected-thirteenth-case"
    report["observations"].append(unexpected)
    mutated = tmp_path / "unexpected-case.json"
    mutated.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("run-scenarios", str(mutated))

    assert result.returncode == 1
    assert "summary validation failed" not in result.stderr
    summary = json.loads(result.stdout)
    assert summary["scenario_count"] == 13
    assert summary["passed_count"] == 12
    assert summary["failed_count"] == 1
    unexpected_summary = next(
        item
        for item in summary["per_scenario_breakdown"]
        if item["case_id"] == "observation-12-unexpected-thirteenth-case"
    )
    assert unexpected_summary["expected"] == "reject"
    assert unexpected_summary["observed"] == "reject"
    assert unexpected_summary["outcome"] == "fail"
    assert any(
        "unexpected_case:unexpected-thirteenth-case" in code
        for code in unexpected_summary["issue_codes"]
    )


def test_affected_test_selection_must_match_fixture_oracle(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["observations"][0]["affected_tests"]["selected"] = [
        "tests/not-the-alpha-test.py"
    ]
    mutated = tmp_path / "affected-test-selection-drift.json"
    mutated.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(mutated))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any(
        "affected_tests_selection_mismatch:rename-symbol" in error
        for error in payload["errors"]
    )


def test_affected_test_oracle_must_be_repo_local(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["observations"][0]["affected_tests"]["oracle_ref"] = (
        "https://example.invalid/oracle"
    )
    mutated = tmp_path / "nonlocal-affected-test-oracle.json"
    mutated.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(mutated))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any(
        "affected_tests_oracle_mismatch:rename-symbol" in error
        for error in payload["errors"]
    )


def test_report_rejects_partial_evidence_and_uncertain_preserved_lineage(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    observation = report["observations"][0]
    observation["evidence_state"] = "partial"
    observation["lineage"]["confidence"] = 0.2
    observation["lineage"]["alternatives"] = 1
    path = tmp_path / "partial-lineage.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any("evidence_state_mismatch:rename-symbol" in error for error in errors)
    assert any(
        "preserved_lineage_not_certain:rename-symbol" in error for error in errors
    )


def test_report_binds_semantic_identity_to_unique_local_case_paths(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    first = report["observations"][0]["semantic_identity"]["entities"][0]
    first["occurrences"][0].update(
        {"path": "../outside.py", "start_line": 8, "end_line": 2}
    )
    report["observations"][1]["semantic_identity"]["entities"][0]["semantic_id"] = (
        first["semantic_id"]
    )
    report["observations"][2]["semantic_identity"]["entities"][0]["occurrences"][0][
        "end_line"
    ] = 1
    path = tmp_path / "identity-drift.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any("semantic_identity_path:rename-symbol" in error for error in errors)
    assert any("semantic_identity_range:rename-symbol" in error for error in errors)
    assert any("semantic_identity_mismatch:move-symbol" in error for error in errors)
    assert any("semantic_identity_duplicate:move-symbol" in error for error in errors)
    assert any(
        "semantic_identity_occurrence:signature-change" in error for error in errors
    )


def test_report_rejects_invented_relation_identity(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    relation = report["observations"][6]["semantic_identity"]["entities"][0][
        "relations"
    ][0]
    relation["target"] = "fixture:invented-target"
    path = tmp_path / "relation-drift.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    assert any(
        "semantic_relation_mismatch:multi-file-impact:fixture:eta.symbol" in error
        for error in json.loads(result.stdout)["errors"]
    )


def test_report_rejects_duplicate_metric_declarations(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["observations"][0]["metrics"].append(
        copy.deepcopy(report["observations"][0]["metrics"][0])
    )
    path = tmp_path / "duplicate-metric.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    assert any(
        "duplicate_metric:rename-symbol:definitions_references" in error
        for error in json.loads(result.stdout)["errors"]
    )


def test_report_rejects_source_provenance_drift(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["observations"][0]["provenance"]["source_ref"] = (
        "fixture://unrelated-source"
    )
    path = tmp_path / "source-provenance-drift.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    assert any(
        "source_provenance_mismatch:rename-symbol" in error
        for error in json.loads(result.stdout)["errors"]
    )


def test_report_rejects_inflated_branch_count_and_inconsistent_confidence(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    lineage = report["observations"][7]["lineage"]
    lineage["alternatives"] = 100
    lineage["confidence"] = 0.01
    path = tmp_path / "inflated-lineage.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    assert any(
        "lineage_ambiguity_mismatch:split-symbol" in error
        for error in json.loads(result.stdout)["errors"]
    )


def test_report_rejects_unbounded_invalidation_and_metric_drift(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    observation = report["observations"][0]
    observation["invalidation"]["affected_paths"] = ["src/alpha.py", "../outside.py"]
    observation["invalidation"]["recomputed_paths"] = ["src/not-alpha.py"]
    observation["metrics"][0]["unit"] = "ratio"
    observation["metrics"][0]["value"] = -1
    path = tmp_path / "invalidation-metric-drift.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any("invalidation_path:rename-symbol" in error for error in errors)
    assert any(
        "invalidation_recompute_scope:rename-symbol" in error for error in errors
    )
    assert any(
        "metric_unit:rename-symbol:definitions_references" in error for error in errors
    )
    assert any(
        "metric_range:rename-symbol:definitions_references" in error for error in errors
    )


def test_report_rejects_affected_test_status_and_count_contradiction(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    observation = report["observations"][0]
    observation["affected_tests"]["status"] = "empty"
    next(
        metric
        for metric in observation["metrics"]
        if metric["metric_id"] == "affected_tests"
    )["value"] = 0
    path = tmp_path / "affected-test-contradiction.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any(
        "affected_tests_status_mismatch:rename-symbol" in error for error in errors
    )
    assert any(
        "affected_tests_metric_mismatch:rename-symbol" in error for error in errors
    )


def test_schema_errors_remain_visible_in_summary(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["provider"].pop("id")
    path = tmp_path / "schema-invalid.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("run-scenarios", str(path))

    assert result.returncode == 1
    summary = json.loads(result.stdout)
    contract = next(
        item
        for item in summary["per_scenario_breakdown"]
        if item["case_id"] == "report-contract"
    )
    assert any(code.startswith("report:provider:") for code in contract["issue_codes"])


def provider_execution_payload() -> dict[str, object]:
    provider = {
        "id": "python-ast-bootstrap",
        "version": "1.0.0",
    }
    source_epoch = "sha256:" + ("1" * 64)
    state = {
        "schema_version": "abyss-stack-live-code-intelligence-state-v1",
        "status": "current",
        "provider": provider,
        "config": {"digest": "sha256:" + ("2" * 64)},
        "source": {"source_epoch": source_epoch},
        "invalidation": {
            "changed_paths": ["consumer.py"],
            "added_paths": [],
            "deleted_paths": [],
            "dependency_impacted_paths": ["consumer.py"],
            "invalidated_paths": ["consumer.py"],
            "reused_paths": ["other.py"],
            "full_rebuild": False,
            "blast_radius_universe": {
                "kind": "previous-and-current-source-files",
                "count": 2,
                "paths": ["consumer.py", "other.py"],
            },
            "blast_radius": 0.5,
        },
        "freshness": {
            "layer": "LIVE",
            "source_epoch": source_epoch,
            "provider": provider,
            "confidence": "observed",
        },
        "provenance": {
            "runtime_owner": "abyss-stack",
            "observation_meaning_owner": "aoa-kag",
            "proof_owner": "aoa-evals",
            "source_kind": "working_tree",
            "full_rebuild": False,
        },
    }
    environment_digest = "sha256:" + ("3" * 64)
    execution = {
        "case_id": "delta-full-parity",
        "mode": "delta",
        "status": "completed",
        "source_epoch": source_epoch,
        "observed_at": "2026-08-25T12:00:01Z",
        "command_ref": "test://provider-execution",
        "environment_digest": environment_digest,
        "latency_ms": 1.5,
        "resource_peak_bytes": 4096,
        "state_digest": runner.canonical_digest(state),
        "repeated_state_digest": runner.stable_provider_state_digest(state),
        "full_state_projection_digest": "sha256:" + ("4" * 64),
        "delta_state_projection_digest": "sha256:" + ("4" * 64),
        "provider_state": state,
    }
    return {
        "schema_version": "aoa_code_observation_provider_execution_v1",
        "machine_binding": {
            "contract_schema": "abyss_machine_code_intelligence_config_v1",
            "contract_ref": "config-templates/etc/abyss-machine/code-intelligence.json",
            "contract_digest": runner.MACHINE_CONTRACT_DIGEST,
            "contract_digest_kind": runner.MACHINE_CONTRACT_DIGEST_KIND,
            "contract_snapshot_epoch": runner.MACHINE_CONTRACT_SNAPSHOT_EPOCH,
            "workspace_manifest_digest": runner.MACHINE_WORKSPACE_MANIFEST_DIGEST,
            "provider_id": "python-ast-bootstrap",
            "admission_state": "not_admitted",
            "admission_receipt_ref": None,
            "owner_bindings": runner.OWNER_BINDINGS,
            "claim_limits": runner.PROVIDER_EXECUTION_CLAIM_LIMITS,
        },
        "provider": {
            "id": provider["id"],
            "version": provider["version"],
            "observation_schema": "abyss-stack-code-observation-v1",
            "state_schema": "abyss-stack-live-code-intelligence-state-v1",
            "config_digest": state["config"]["digest"],
        },
        "run": {
            "execution_id": "test-execution",
            "observed_at": "2026-08-25T12:00:00Z",
            "command_ref": "test://provider-execution",
            "environment_digest": environment_digest,
            "reproducibility_state": "deterministic",
        },
        "executions": [execution],
    }


def complete_provider_execution_payload() -> dict[str, object]:
    import provider_execution

    return provider_execution.execute()


def test_provider_execution_runs_all_twelve_cases() -> None:
    result = run_runner("execute-provider")

    assert result.returncode == 0, result.stderr
    envelope = json.loads(result.stdout)
    assert envelope["execution_posture"] == "source-bound-provider-candidate"
    assert envelope["machine_binding"]["admission_state"] == "not_admitted"
    assert envelope["coverage"]["mode"] == "complete"
    assert len(envelope["executions"]) == 12
    assert envelope["executions"][4]["observation"]["deletion"]["status"] == "confirmed"
    assert envelope["executions"][7]["observation"]["lineage"]["alternatives"] >= 2
    assert envelope["executions"][8]["observation"]["lineage"]["confidence"] < 1
    assert envelope["executions"][9]["observation"]["freshness"]["status"] == "stale"
    assert envelope["executions"][10]["observation"]["parity"]["status"] == "equal"


def test_provider_execution_binds_state_to_machine_contract(tmp_path: Path) -> None:
    execution_path = tmp_path / "provider-execution.json"
    execution_path.write_text(
        json.dumps(provider_execution_payload()), encoding="utf-8"
    )

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["valid"] is True
    assert payload["admission_state"] == "not_admitted"
    assert payload["case_ids"] == ["delta-full-parity"]


def test_provider_execution_rejects_claim_limit_drift(tmp_path: Path) -> None:
    envelope = provider_execution_payload()
    envelope["machine_binding"]["claim_limits"] = [  # type: ignore[index]
        "This provider proves runtime health and proof acceptance."
    ]
    execution_path = tmp_path / "claim-limit-drift.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    assert any(
        "claim_limits" in error for error in json.loads(result.stdout)["errors"]
    )


def test_provider_execution_rejects_state_digest_drift(tmp_path: Path) -> None:
    envelope = provider_execution_payload()
    envelope["executions"][0]["provider_state"]["status"] = "degraded"  # type: ignore[index]
    execution_path = tmp_path / "state-drift.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("state_digest:execution[0]" in error for error in payload["errors"])


def test_provider_execution_rejects_unbounded_blast_radius(tmp_path: Path) -> None:
    envelope = provider_execution_payload()
    state = envelope["executions"][0]["provider_state"]  # type: ignore[index]
    state["invalidation"]["blast_radius"] = 0.0  # type: ignore[index]
    execution_path = tmp_path / "blast-radius-drift.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any(
        "blast_radius_denominator:execution[0]" in error for error in payload["errors"]
    )


def test_provider_execution_rejects_delete_without_deletion_event(
    tmp_path: Path,
) -> None:
    envelope = provider_execution_payload()
    envelope["executions"][0]["case_id"] = "delete-entity"  # type: ignore[index]
    execution_path = tmp_path / "missing-delete-event.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any(
        "deletion_event_missing:execution[0]" in error for error in payload["errors"]
    )


def test_provider_execution_rejects_admitted_without_receipt(tmp_path: Path) -> None:
    envelope = provider_execution_payload()
    envelope["machine_binding"]["admission_state"] = "admitted"  # type: ignore[index]
    execution_path = tmp_path / "unreceipted-admission.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("admission_receipt" in error for error in payload["errors"])


def test_complete_provider_execution_covers_the_whole_fixture_family(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    execution_path = tmp_path / "complete-provider-execution.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["valid"] is True
    assert payload["case_ids"] == sorted(envelope["coverage"]["case_ids"])  # type: ignore[index]


def test_complete_provider_execution_rejects_incomplete_coverage(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["coverage"]["case_ids"] = envelope["coverage"]["case_ids"][:-1]  # type: ignore[index]
    execution_path = tmp_path / "incomplete-provider-execution.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("coverage_complete" in error for error in payload["errors"])


def test_complete_provider_candidate_cannot_self_claim_admission(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["machine_binding"]["admission_state"] = "admitted"  # type: ignore[index]
    envelope["machine_binding"]["admission_receipt_ref"] = "receipt://self-claimed"  # type: ignore[index]
    path = tmp_path / "complete-admitted.json"
    path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any("complete_candidate_admission" in error for error in errors)
    assert any("complete_candidate_receipt" in error for error in errors)


def test_complete_provider_execution_rejects_freshness_confidence_drift(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    execution = envelope["executions"][0]  # type: ignore[index]
    state = execution["provider_state"]
    state["freshness"]["confidence"] = "degraded"
    execution["state_digest"] = runner.canonical_digest(state)
    execution["repeated_state_digest"] = runner.stable_provider_state_digest(state)
    path = tmp_path / "freshness-confidence-drift.json"
    path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(path))

    assert result.returncode == 1
    assert any(
        "freshness_confidence:execution[0]" in error
        for error in json.loads(result.stdout)["errors"]
    )


def test_delta_projection_uses_incremental_reuse_and_matches_full_projection() -> None:
    before = {
        "src/changed.py": ["def value():", "    return 1"],
        "src/reused.py": ["def reused():", "    return 2"],
    }
    after = {
        "src/changed.py": ["def value():", "    return 3"],
        "src/reused.py": ["def reused():", "    return 2"],
    }

    delta = provider_execution.delta_source_index(before, after, ["src/changed.py"])

    assert delta == provider_execution.source_index(after)
    assert delta is not provider_execution.source_index(after)


def test_complete_provider_execution_binds_affected_test_oracle(
    tmp_path: Path, monkeypatch
) -> None:
    envelope = complete_provider_execution_payload()
    oracle = json.loads(runner.AFFECTED_TEST_ORACLE_PATH.read_text(encoding="utf-8"))
    oracle["cases"][0]["selected"] = []
    oracle_path = tmp_path / "drifted-affected-tests.json"
    oracle_path.write_text(json.dumps(oracle), encoding="utf-8")
    monkeypatch.setattr(runner, "AFFECTED_TEST_ORACLE_PATH", oracle_path)

    errors, _case_ids = runner.provider_execution_errors(envelope)
    assert any(
        "execution_affected_tests_oracle_selection:rename-symbol" in error
        for error in errors
    )


def test_complete_provider_execution_requires_reproducibility_digest(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["executions"][0]["repeated_state_digest"] = None  # type: ignore[index]
    execution_path = tmp_path / "non-reproducible-provider-execution.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("reproducibility_required" in error for error in payload["errors"])


def test_complete_provider_execution_requires_delta_full_projections(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["executions"][10]["full_state_projection_digest"] = None  # type: ignore[index]
    execution_path = tmp_path / "missing-parity-projection.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("parity_required:execution[10]" in error for error in payload["errors"])


def test_complete_provider_execution_rejects_forged_deletion_semantics(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["executions"][4]["observation"]["deletion"]["after_absent"] = []  # type: ignore[index]
    execution_path = tmp_path / "forged-delete.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any(
        "execution[4]:deletion_after_absence" in error for error in payload["errors"]
    )


def test_complete_provider_execution_rejects_overconfident_split_lineage(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["executions"][7]["observation"]["lineage"]["confidence"] = 1  # type: ignore[index]
    execution_path = tmp_path / "overconfident-split.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any(
        "execution[7]:case_lineage_confidence" in error for error in payload["errors"]
    )


def test_complete_provider_execution_rejects_inflated_split_lineage(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    lineage = envelope["executions"][7]["observation"]["lineage"]  # type: ignore[index]
    lineage["alternatives"] = 100
    lineage["confidence"] = 0.01
    execution_path = tmp_path / "inflated-split-lineage.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any(
        "execution[7]:case_lineage_alternatives" in error for error in errors
    )
    assert any(
        "execution[7]:case_lineage_confidence" in error for error in errors
    )


def test_complete_provider_execution_binds_all_parity_digests(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    execution = envelope["executions"][10]  # type: ignore[index]
    forged_top_level = "sha256:" + ("f" * 64)
    forged_observation = "sha256:" + ("e" * 64)
    execution["full_state_projection_digest"] = forged_top_level
    execution["delta_state_projection_digest"] = forged_top_level
    parity = execution["observation"]["parity"]
    parity["full_projection_digest"] = forged_observation
    parity["delta_projection_digest"] = forged_observation
    execution["provider_state"]["source"]["projection_digest"] = forged_top_level
    state = execution["provider_state"]
    execution["state_digest"] = runner.canonical_digest(state)
    execution["repeated_state_digest"] = runner.stable_provider_state_digest(state)
    execution_path = tmp_path / "forged-parity-digests.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any("execution_projection_digest:execution[10]" in error for error in errors)
    assert any(
        "execution_parity_projection:execution[10]:full" in error
        for error in errors
    )
    assert any(
        "execution_parity_projection:execution[10]:delta" in error
        for error in errors
    )
    assert any(
        "execution_parity_observation:execution[10]:full" in error
        for error in errors
    )
    assert any(
        "execution_parity_observation:execution[10]:delta" in error
        for error in errors
    )


def test_complete_provider_execution_rejects_provider_fixture_version_drift(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["provider"]["version"] = "self-asserted"  # type: ignore[index]
    execution_path = tmp_path / "provider-version-drift.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("execution_provider_version" in error for error in payload["errors"])


def test_provider_execution_requires_explicit_snapshot_drift(tmp_path: Path) -> None:
    envelope = provider_execution_payload()
    envelope["machine_binding"]["current_contract_digest"] = "sha256:" + ("9" * 64)  # type: ignore[index]
    execution_path = tmp_path / "implicit-snapshot-drift.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("snapshot_currentness" in error for error in payload["errors"])


def test_provider_execution_allows_explicit_unobserved_currentness(
    tmp_path: Path,
) -> None:
    envelope = provider_execution_payload()
    envelope["machine_binding"]["snapshot_currentness"] = "unobserved"  # type: ignore[index]
    execution_path = tmp_path / "unobserved-snapshot-currentness.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["valid"] is True


def test_provider_execution_rejects_unsafe_invalidation_path(tmp_path: Path) -> None:
    envelope = provider_execution_payload()
    envelope["executions"][0]["provider_state"]["invalidation"][
        "blast_radius_universe"
    ]["paths"] = [  # type: ignore[index]
        "consumer.py",
        "../outside.py",
    ]
    execution_path = tmp_path / "unsafe-invalidation-path.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("unsafe_path:execution[0]" in error for error in payload["errors"])


def test_provider_execution_rejects_non_positive_latency(tmp_path: Path) -> None:
    envelope = provider_execution_payload()
    envelope["executions"][0]["latency_ms"] = 0  # type: ignore[index]
    execution_path = tmp_path / "zero-latency.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("latency_ms" in error for error in payload["errors"])


def test_provider_evidence_collects_and_validates_real_local_observations(
    tmp_path: Path,
) -> None:
    result = run_runner("collect-provider-evidence")

    assert result.returncode == 0, result.stderr
    evidence = json.loads(result.stdout)
    assert evidence["family_id"] == "refactor-torture-v1"
    assert {provider["id"] for provider in evidence["providers"]} == {
        "python-ast",
        "ctags-host",
    }
    for provider in evidence["providers"]:
        assert provider["admission_state"] == "not_admitted"
        if provider["availability"] == "available":
            assert len(provider["case_ids"]) == 12
            assert (
                sum(item["status"] == "observed" for item in provider["observations"])
                == 12
            )
    ctags_provider = next(
        provider for provider in evidence["providers"] if provider["id"] == "ctags-host"
    )
    if shutil.which("ctags"):
        assert ctags_provider["availability"] == "available"
    else:
        assert ctags_provider["availability"] == "not_available"

    evidence_path = tmp_path / "provider-evidence.json"
    evidence_path.write_text(result.stdout, encoding="utf-8")
    validation = run_runner("validate-provider-evidence", str(evidence_path))
    assert validation.returncode == 0, validation.stderr
    assert json.loads(validation.stdout)["valid"] is True


def test_provider_evidence_cannot_claim_admission(tmp_path: Path) -> None:
    evidence = json.loads(run_runner("collect-provider-evidence").stdout)
    evidence["providers"][0]["admission_state"] = "admitted"
    evidence_path = tmp_path / "admitted-provider-evidence.json"
    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")

    result = run_runner("validate-provider-evidence", str(evidence_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("admission_state" in error for error in payload["errors"])


def test_provider_evidence_rejects_claim_boundary_and_occurrence_drift(
    tmp_path: Path,
) -> None:
    evidence = json.loads(run_runner("collect-provider-evidence").stdout)
    evidence["claim_boundary"] = evidence["claim_boundary"].replace(
        "These observations", "The observations"
    )
    symbol = evidence["providers"][0]["observations"][0]["symbols"][0]
    symbol["start_line"] += 10
    symbol["end_line"] += 10
    path = tmp_path / "provider-evidence-drift.json"
    path.write_text(json.dumps(evidence), encoding="utf-8")

    result = run_runner("validate-provider-evidence", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any("claim_boundary" in error for error in errors)
    assert any(
        "symbol occurrence does not match independent provider output" in error
        for error in errors
    )


def test_provider_agreement_rejects_placeholder_observation(tmp_path: Path) -> None:
    facts = ["definition:render"]
    payload = {
        "schema_version": "aoa_code_observation_provider_agreement_v1",
        "observed_at": "2026-08-29T00:00:00Z",
        "required_facts": facts,
        "claim_boundary": provider_agreement.CLAIM_BOUNDARY,
        "envelopes": [
            _agreement_envelope(provider_id, facts)
            for provider_id in ("tree-sitter", "scip", "lsp")
        ],
    }
    payload["envelopes"][0]["observations"] = [{}]
    path = tmp_path / "placeholder-agreement.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = provider_agreement.validate(path)

    assert any(
        issue.startswith("invalid_normalized_observation:tree-sitter:0")
        for issue in result["issues"]
    )


def test_adjacent_provider_evidence_rejects_placeholder_observation(
    tmp_path: Path,
) -> None:
    source_epoch = "commit:" + "a" * 40
    specs = {
        "static_security": ("semgrep", "static-security"),
        "software_components": ("syft", "software-components"),
        "artifact_provenance": ("in-toto", "artifact-provenance"),
        "document_structure": ("markitdown", "document-structure"),
    }
    batches = {
        key: {
            "schema_version": "aoa-code-observation-v1",
            "capability_class": capability,
            "provider": {"id": provider_id, "lane": {"status": "supplied_unadmitted"}},
            "source": {"source_epoch": source_epoch},
            "parse_status": "parsed",
            "observations": [{}],
            "qualification": {"machine_admission": {"state": "not_admitted"}},
        }
        for key, (provider_id, capability) in specs.items()
    }
    payload = {
        "schema": "abyssos_adjacent_provider_evidence_v1",
        "goal_id": "fixture",
        "observed_at": "2026-08-29T00:00:00Z",
        "source_epoch": source_epoch,
        "artifact": {
            "sha256": "sha256:" + "1" * 64,
            "subject_digest": "sha256:" + "2" * 64,
            "signature_status": "missing",
            "admission_status": "not_admitted",
        },
        "providers": {},
        "batches": batches,
        "summary": {"all_provider_lanes_unadmitted": True},
        "claim_limits": adjacent_provider_evidence.CLAIM_LIMITS,
    }
    path = tmp_path / "placeholder-adjacent.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = adjacent_provider_evidence.validate(path)

    assert any(
        issue.startswith("invalid_observation:semgrep:0") for issue in result["issues"]
    )
