from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema
import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_repo
from validators import source_eval_report_longitudinal as source_eval_report_longitudinal_validator
from validate_repo import run_validation
from validate_repo_fixtures import (
    add_materialized_proof_artifacts,
    eval_dir_for_test,
    make_eval_bundle,
    write_catalogs,
    write_integrity_example_report,
    write_text,
)


ANTIFRAGILITY_REPORT_SCHEMA_PATH = (
    REPO_ROOT
    / "mechanics"
    / "antifragility"
    / "parts"
    / "posture-review"
    / "schemas"
    / "antifragility_eval_report_v1.json"
)


def _antifragility_report_payload(*, stressor_class: str | None, receipt_refs: list[str]) -> dict[str, object]:
    scope: dict[str, str] = {
        "repo": "aoa-evals",
        "surface": "evals/stress/aoa-antifragility-posture/reports/example-report.json",
    }
    if stressor_class is not None:
        scope["stressor_class"] = stressor_class

    return {
        "schema_version": "antifragility_eval_report_v1",
        "report_id": "anti-001",
        "generated_at_utc": "2026-04-09T12:00:00Z",
        "scope": scope,
        "inputs": {
            "receipt_refs": receipt_refs,
            "adaptation_refs": [],
            "evidence_refs": ["repo:aoa-evals/reports/evidence-001.md"],
        },
        "axes": {
            axis: {"status": "pass"}
            for axis in (
                "containment",
                "fallback_fidelity",
                "false_action_prevention",
                "recovery_latency",
                "adaptation_gain",
                "operator_burden",
                "trust_calibration",
            )
        },
        "blind_spots": ["single-window read only"],
        "verdict_summary": "bounded antifragility posture remains intact",
    }


def test_approval_boundary_schema_allows_missing_fallback_move() -> None:
    bundle_dir = eval_dir_for_test(REPO_ROOT, "aoa-approval-boundary-adherence")
    schema_path = bundle_dir / "reports" / "summary.schema.json"
    example_path = bundle_dir / "reports" / "example-report.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    example = json.loads(example_path.read_text(encoding="utf-8"))
    assert isinstance(example, dict)

    trimmed_example = json.loads(json.dumps(example))
    assert isinstance(trimmed_example.get("per_case_breakdown"), list)
    trimmed_example["per_case_breakdown"][0].pop("fallback_move", None)

    jsonschema.validate(trimmed_example, schema)


def test_antifragility_schema_requires_stressor_class() -> None:
    schema = json.loads(ANTIFRAGILITY_REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
    payload = _antifragility_report_payload(
        stressor_class=None,
        receipt_refs=["repo:aoa-evals/reports/receipt-001.json"],
    )

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(payload, schema)


def test_antifragility_schema_requires_non_empty_receipt_refs() -> None:
    schema = json.loads(ANTIFRAGILITY_REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
    payload = _antifragility_report_payload(
        stressor_class="latency-spike",
        receipt_refs=[],
    )

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(payload, schema)


def test_longitudinal_growth_overclaim_detection_requires_real_negation() -> None:
    assert source_eval_report_longitudinal_validator.claim_boundary_overclaims_longitudinal_growth(
        "this report demonstrates broad capability growth rather than workflow-only movement"
    )
    assert source_eval_report_longitudinal_validator.claim_boundary_overclaims_longitudinal_growth(
        "this report demonstrates broad capability growth even though it does not prove general capability growth"
    )
    assert not source_eval_report_longitudinal_validator.claim_boundary_overclaims_longitudinal_growth(
        "this report does not prove broad capability growth"
    )
    assert not source_eval_report_longitudinal_validator.claim_boundary_overclaims_longitudinal_growth(
        "broad capability growth is not proven here"
    )


def test_validate_repo_rejects_report_example_that_violates_bundle_schema(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-invalid-report-example")
    write_catalogs(tmp_path)
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-invalid-report-example",
        report_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [
                "eval_name",
                "bundle_status",
                "object_under_evaluation",
                "verdict",
                "claim_boundary",
                "limitations",
            ],
            "properties": {
                "eval_name": {"const": "aoa-invalid-report-example"},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
            },
        },
        report_example={
            "eval_name": "aoa-invalid-report-example",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "supports bounded claim",
            "claim_boundary": "missing limitations should fail",
        },
    )

    issues = run_validation(tmp_path)

    assert any("report violation" in issue.message and "limitations" in issue.message for issue in issues)


def test_validate_repo_rejects_actual_report_that_violates_bundle_schema(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-invalid-actual-report")
    write_catalogs(tmp_path)
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-invalid-actual-report",
        report_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [
                "eval_name",
                "bundle_status",
                "object_under_evaluation",
                "verdict",
                "claim_boundary",
                "limitations",
            ],
            "properties": {
                "eval_name": {"const": "aoa-invalid-actual-report"},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
            },
        },
        report_example={
            "eval_name": "aoa-invalid-actual-report",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "supports bounded claim",
            "claim_boundary": "example includes limitations and should pass",
            "limitations": ["example remains bounded"],
        },
    )
    write_text(
        eval_dir_for_test(tmp_path, "aoa-invalid-actual-report") / "reports" / "local-run.report.json",
        json.dumps(
            {
                "eval_name": "aoa-invalid-actual-report",
                "bundle_status": "draft",
                "object_under_evaluation": "bounded test surface",
                "verdict": "supports bounded claim",
                "claim_boundary": "missing limitations should fail for actual reports",
            },
            indent=2,
        ),
    )

    issues = run_validation(tmp_path)

    assert any(
        issue.location.endswith("reports/local-run.report.json")
        and "report violation" in issue.message
        and "limitations" in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_actual_report_with_manifest_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-drifted-actual-report")
    write_catalogs(tmp_path)
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-drifted-actual-report",
        report_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [
                "eval_name",
                "bundle_status",
                "object_under_evaluation",
                "verdict",
                "claim_boundary",
                "limitations",
            ],
            "properties": {
                "eval_name": {"type": "string"},
                "bundle_status": {"type": "string"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
            },
        },
        report_example={
            "eval_name": "aoa-drifted-actual-report",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "supports bounded claim",
            "claim_boundary": "example includes manifest-aligned fields",
            "limitations": ["example remains bounded"],
        },
    )
    write_text(
        eval_dir_for_test(tmp_path, "aoa-drifted-actual-report") / "reports" / "local-run.report.json",
        json.dumps(
            {
                "eval_name": "wrong-eval-name",
                "bundle_status": "portable",
                "object_under_evaluation": "bounded test surface",
                "verdict": "supports bounded claim",
                "claim_boundary": "schema accepts this but manifest drift should fail",
                "limitations": ["actual report remains bounded"],
            },
            indent=2,
        ),
    )

    issues = run_validation(tmp_path)

    assert any("eval_name must match manifest name" in issue.message for issue in issues)
    assert any("bundle_status must match manifest status" in issue.message for issue in issues)


def test_validate_repo_requires_integrity_risk_taxonomy_enum(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-eval-integrity-check", category="capability")
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-eval-integrity-check",
        report_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [
                "eval_name",
                "bundle_status",
                "object_under_evaluation",
                "verdict",
                "claim_boundary",
                "limitations",
                "corpus_slice",
                "per_target_breakdown",
            ],
            "properties": {
                "eval_name": {"const": "aoa-eval-integrity-check"},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                "corpus_slice": {"type": "string"},
                "per_target_breakdown": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": [
                            "target_bundle",
                            "integrity_risk_class",
                            "target_reading",
                            "note",
                        ],
                        "properties": {
                            "target_bundle": {"type": "string"},
                            "integrity_risk_class": {
                                "type": "string",
                                "enum": ["style-over-substance"],
                            },
                            "target_reading": {"type": "string"},
                            "note": {"type": "string"},
                        },
                    },
                },
            },
        },
        report_example={
            "eval_name": "aoa-eval-integrity-check",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "mixed support",
            "claim_boundary": "bounded integrity example",
            "limitations": ["still bounded"],
            "corpus_slice": "starter bundles",
            "per_target_breakdown": [
                {
                    "target_bundle": "aoa-alpha",
                    "integrity_risk_class": "style-over-substance",
                    "target_reading": "mixed support",
                    "note": "note",
                }
            ],
        },
    )
    write_text(
        eval_dir_for_test(tmp_path, "aoa-eval-integrity-check") / "notes" / "review-contract.md",
        "\n".join(
            [
                "# Review Contract",
                "style-over-substance",
                "artifact/process collapse",
                "baseline by association",
                "growth by association",
                "peer-compare blur",
                "fixed-baseline drift",
                "longitudinal overclaim",
                "schema-clean but claim-overstated",
                "routing overreach",
                "",
            ]
        ),
    )
    write_integrity_example_report(
        eval_dir_for_test(tmp_path, "aoa-eval-integrity-check") / "examples" / "example-report.md"
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-eval-integrity-check")

    assert any("integrity_risk_class enum must match" in issue.message for issue in issues)


def test_validate_repo_requires_integrity_taxonomy_in_example_report(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-eval-integrity-check", category="capability")
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-eval-integrity-check",
        report_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [
                "eval_name",
                "bundle_status",
                "object_under_evaluation",
                "verdict",
                "claim_boundary",
                "limitations",
                "corpus_slice",
                "per_target_breakdown",
            ],
            "properties": {
                "eval_name": {"const": "aoa-eval-integrity-check"},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"type": "string"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                "corpus_slice": {"type": "string"},
                "per_target_breakdown": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": [
                            "target_bundle",
                            "integrity_risk_class",
                            "target_reading",
                            "note",
                        ],
                        "properties": {
                            "target_bundle": {"type": "string"},
                            "integrity_risk_class": {
                                "type": "string",
                                "enum": [
                                    "style-over-substance",
                                    "artifact/process collapse",
                                    "baseline by association",
                                    "growth by association",
                                    "peer-compare blur",
                                    "fixed-baseline drift",
                                    "longitudinal overclaim",
                                    "schema-clean but claim-overstated",
                                    "routing overreach",
                                ],
                            },
                            "target_reading": {"type": "string"},
                            "note": {"type": "string"},
                        },
                    },
                },
            },
        },
        report_example={
            "eval_name": "aoa-eval-integrity-check",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "mixed support",
            "claim_boundary": "bounded integrity example",
            "limitations": ["still bounded"],
            "corpus_slice": "starter bundles",
            "per_target_breakdown": [
                {
                    "target_bundle": "aoa-alpha",
                    "integrity_risk_class": "style-over-substance",
                    "target_reading": "mixed support",
                    "note": "note",
                }
            ],
        },
    )
    write_text(
        eval_dir_for_test(tmp_path, "aoa-eval-integrity-check") / "notes" / "review-contract.md",
        "\n".join(
            [
                "# Review Contract",
                "style-over-substance",
                "artifact/process collapse",
                "baseline by association",
                "growth by association",
                "peer-compare blur",
                "fixed-baseline drift",
                "longitudinal overclaim",
                "schema-clean but claim-overstated",
                "routing overreach",
                "",
            ]
        ),
    )
    write_text(
        eval_dir_for_test(tmp_path, "aoa-eval-integrity-check") / "examples" / "example-report.md",
        "# Example Report\n",
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-eval-integrity-check")

    assert any(
        issue.location == "evals/capability/aoa-eval-integrity-check/examples/example-report.md"
        and "integrity example report must mention" in issue.message
        for issue in issues
    )
