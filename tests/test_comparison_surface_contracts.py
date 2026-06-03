from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_repo import run_validation
from validate_repo_fixtures import (
    add_fixed_baseline_proof_artifacts,
    add_longitudinal_proof_artifacts,
    add_peer_compare_proof_artifacts,
    eval_dir_for_test,
    make_eval_bundle,
    write_catalogs,
    write_text,
)


def test_validate_repo_requires_support_note_for_comparative_summary(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-comparison-contract",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("report_format 'comparative-summary' requires an evidence entry with kind 'support_note'" in issue.message for issue in issues)


def test_validate_repo_requires_fixed_baseline_contract_phrases(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-weak-fixed-baseline-contract",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nbaseline target only\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any(
        "must state the baseline target, noisy variation, and style-only overread limits in a support note"
        in issue.message
        for issue in issues
    )


def test_validate_repo_requires_materialized_report_artifacts_for_fixed_baseline(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-fixed-baseline-report-artifacts",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nbaseline target\nnoisy variation\nstyle-only overread\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("reports/summary.schema.json" in issue.message for issue in issues)
    assert any("reports/example-report.json" in issue.message for issue in issues)


def test_validate_repo_requires_runner_contract_for_fixed_baseline(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-fixed-baseline-runner",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nbaseline target\nnoisy variation\nstyle-only overread\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    add_fixed_baseline_proof_artifacts(
        tmp_path,
        bundle_name="aoa-missing-fixed-baseline-runner",
        include_runner_contract=False,
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("runners/contract.json" in issue.message for issue in issues)


def test_validate_repo_requires_peer_compare_contract_phrases(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-weak-peer-compare-contract",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nmatched conditions only\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any(
        "must state matched conditions and side-by-side interpretation limits in a support note"
        in issue.message
        for issue in issues
    )


def test_validate_repo_accepts_valid_fixed_baseline_comparison_surface(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-fixed-baseline",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_fixed_baseline_proof_artifacts(tmp_path, bundle_name="aoa-valid-fixed-baseline")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-valid-fixed-baseline")

    assert issues == []


def test_validate_repo_accepts_valid_peer_compare_comparison_surface(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-peer-compare",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_peer_compare_proof_artifacts(tmp_path, bundle_name="aoa-valid-peer-compare")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-valid-peer-compare")

    assert issues == []


def test_validate_repo_accepts_valid_longitudinal_comparison_surface(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-longitudinal-window",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(tmp_path, bundle_name="aoa-valid-longitudinal-window")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-valid-longitudinal-window")

    assert issues == []


def test_validate_repo_requires_comparison_surface_for_non_none_baseline(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-comparison-surface",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    manifest_path = eval_dir_for_test(tmp_path, "aoa-missing-comparison-surface") / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest.pop("comparison_surface", None)
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("comparison_surface" in issue.message for issue in issues)


def test_validate_repo_requires_comparison_mode_in_comparative_report_artifacts(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-comparison-mode",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_fixed_baseline_proof_artifacts(tmp_path, bundle_name="aoa-missing-comparison-mode")
    schema_path = eval_dir_for_test(tmp_path, "aoa-missing-comparison-mode") / "reports" / "summary.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["required"] = [item for item in schema["required"] if item != "comparison_mode"]
    schema["properties"].pop("comparison_mode", None)
    schema_path.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    example_path = eval_dir_for_test(tmp_path, "aoa-missing-comparison-mode") / "reports" / "example-report.json"
    example = json.loads(example_path.read_text(encoding="utf-8"))
    example.pop("comparison_mode", None)
    example_path.write_text(json.dumps(example, indent=2), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("comparison_mode" in issue.message for issue in issues)


def test_validate_repo_rejects_peer_compare_with_wrong_peer_surface_count(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-invalid-peer-surface-count",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    manifest_path = eval_dir_for_test(tmp_path, "aoa-invalid-peer-surface-count") / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["comparison_surface"]["peer_surfaces"] = ["aoa-peer-left"]
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("peer_surfaces" in issue.location or "peer_surfaces" in issue.message for issue in issues)


def test_validate_repo_rejects_mismatched_comparison_surface_shared_family_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-mismatched-shared-family",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_fixed_baseline_proof_artifacts(tmp_path, bundle_name="aoa-mismatched-shared-family")
    write_text(tmp_path / "fixtures" / "alt-family" / "README.md", "# Shared Fixture Family\n")
    manifest_path = eval_dir_for_test(tmp_path, "aoa-mismatched-shared-family") / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["comparison_surface"]["shared_family_path"] = "fixtures/alt-family/README.md"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("shared_family_path must match fixtures/contract.json" in issue.message for issue in issues)


def test_validate_repo_rejects_mismatched_comparison_surface_paired_readout_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-mismatched-paired-readout",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(tmp_path, bundle_name="aoa-mismatched-paired-readout")
    write_text(tmp_path / "reports" / "alt-proof-flow.md", "# Paired Proof\n")
    manifest_path = eval_dir_for_test(tmp_path, "aoa-mismatched-paired-readout") / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["comparison_surface"]["paired_readout_path"] = "reports/alt-proof-flow.md"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("paired_readout_path must match runners/contract.json" in issue.message for issue in issues)


def test_validate_repo_rejects_invalid_additional_fixture_family_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-output-vs-process-gap",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_peer_compare_proof_artifacts(tmp_path, bundle_name="aoa-output-vs-process-gap")
    contract_path = eval_dir_for_test(tmp_path, "aoa-output-vs-process-gap") / "fixtures" / "contract.json"
    payload = json.loads(contract_path.read_text(encoding="utf-8"))
    payload["additional_shared_fixture_family_paths"] = ["fixtures/missing-v2/README.md"]
    contract_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-output-vs-process-gap")

    assert any("additional_shared_fixture_family_paths" in issue.location for issue in issues)


def test_validate_repo_rejects_blank_shared_fixture_family_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-output-vs-process-gap",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_peer_compare_proof_artifacts(tmp_path, bundle_name="aoa-output-vs-process-gap")
    contract_path = eval_dir_for_test(tmp_path, "aoa-output-vs-process-gap") / "fixtures" / "contract.json"
    payload = json.loads(contract_path.read_text(encoding="utf-8"))
    payload["shared_fixture_family_path"] = "   "
    contract_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-output-vs-process-gap")

    assert any(
        issue.location.endswith(".shared_fixture_family_path")
        and "path must be a non-empty string" in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_blank_additional_paired_readout_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-output-vs-process-gap",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_peer_compare_proof_artifacts(tmp_path, bundle_name="aoa-output-vs-process-gap")
    contract_path = eval_dir_for_test(tmp_path, "aoa-output-vs-process-gap") / "runners" / "contract.json"
    payload = json.loads(contract_path.read_text(encoding="utf-8"))
    payload["additional_paired_readout_paths"] = ["   "]
    contract_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-output-vs-process-gap")

    assert any(
        issue.location.endswith(".additional_paired_readout_paths[0]")
        and "path must be a non-empty string" in issue.message
        for issue in issues
    )


def test_validate_repo_requires_comparison_doctrine_selection_parity(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-selection-drift",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_fixed_baseline_proof_artifacts(tmp_path, bundle_name="aoa-selection-drift")
    write_catalogs(tmp_path)
    write_text(
        tmp_path / "EVAL_SELECTION.md",
        """
        # Eval Bundle Selection Chooser

        This file is the repository-wide chooser for public eval bundles.

        Current starter posture:
        - `aoa-selection-drift`
        """,
    )

    issues = run_validation(tmp_path)

    assert any("Pick Comparison Surface" in issue.message or "comparison selector question" in issue.message for issue in issues)


def test_validate_repo_requires_fixture_contract_for_longitudinal_window(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-longitudinal-fixture",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/window-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/window-contract.md": "# Window Contract\nordered window\nanchor workflow surface\nno clear directional movement\nmixed or unstable movement\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-missing-longitudinal-fixture",
        include_fixture_contract=False,
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("fixtures/contract.json" in issue.message for issue in issues)


def test_validate_repo_rejects_missing_shared_fixture_family_path(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-shared-fixture")
    write_catalogs(tmp_path)
    write_text(
        eval_dir_for_test(tmp_path, "aoa-missing-shared-fixture") / "fixtures" / "contract.json",
        json.dumps(
            {
                "contract_version": 1,
                "shared_fixture_family_path": "fixtures/does-not-exist/README.md",
                "shared_case_surface": "shared bounded case family for validation",
                "bounded_replacement_rule": "replace only with the same bounded case class and public-safe evidence surface",
                "public_safe_requirements": ["outside reviewers can inspect the surface"],
            },
            indent=2,
        ),
    )

    issues = run_validation(tmp_path)

    assert any("shared_fixture_family_path" in issue.location and "does not exist" in issue.message for issue in issues)


def test_validate_repo_allows_missing_initial_longitudinal_transition_note(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-longitudinal-growth-snapshot",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-longitudinal-growth-snapshot",
        report_example_override={
            "windows": [
                {
                    "window_id": "LG-01",
                    "window_order": 1,
                    "workflow_note": "workflow note",
                    "movement_reading": "no clear directional movement",
                    "context_note": "context note",
                },
                {
                    "window_id": "LG-02",
                    "window_order": 2,
                    "workflow_note": "workflow note later",
                    "movement_reading": "bounded improvement signal",
                    "context_note": "context note later",
                    "transition_note": "follow-up transition note",
                },
            ]
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-longitudinal-growth-snapshot")

    assert not any("transition_note" in issue.location for issue in issues)


def test_validate_repo_requires_longitudinal_transition_note(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-longitudinal-growth-snapshot",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-longitudinal-growth-snapshot",
        report_example_override={
            "windows": [
                {
                    "window_id": "LG-01",
                    "window_order": 1,
                    "workflow_note": "workflow note",
                    "movement_reading": "no clear directional movement",
                    "context_note": "context note",
                },
                {
                    "window_id": "LG-02",
                    "window_order": 2,
                    "workflow_note": "workflow note later",
                    "movement_reading": "bounded improvement signal",
                    "context_note": "context note later",
                },
            ]
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-longitudinal-growth-snapshot")

    assert any("transition_note" in issue.message or "transition_note" in issue.location for issue in issues)


def test_validate_repo_allows_negated_longitudinal_growth_disclaimer_in_claim_boundary(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-longitudinal-growth-snapshot",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-longitudinal-growth-snapshot",
        report_example_override={
            "claim_boundary": (
                "This bounded report does not prove general capability growth beyond "
                "this anchored surface."
            ),
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-longitudinal-growth-snapshot")

    assert not any(
        "claim_boundary must stay weaker than broad or general capability growth" in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_longitudinal_report_with_duplicate_window_id(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-duplicate-longitudinal-window",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-duplicate-longitudinal-window",
        report_example_override={
            "windows": [
                {
                    "window_id": "LG-01",
                    "window_order": 1,
                    "workflow_note": "workflow note",
                    "movement_reading": "no clear directional movement",
                    "context_note": "context note",
                    "transition_note": "initial transition note",
                },
                {
                    "window_id": "LG-01",
                    "window_order": 2,
                    "workflow_note": "workflow note later",
                    "movement_reading": "bounded improvement signal",
                    "context_note": "context note later",
                    "transition_note": "duplicate id transition note",
                },
            ]
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("window_id 'LG-01' must be unique" in issue.message for issue in issues)


def test_validate_repo_rejects_longitudinal_report_with_non_increasing_window_order(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-out-of-order-longitudinal-window",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-out-of-order-longitudinal-window",
        report_example_override={
            "windows": [
                {
                    "window_id": "LG-01",
                    "window_order": 2,
                    "workflow_note": "workflow note",
                    "movement_reading": "no clear directional movement",
                    "context_note": "context note",
                    "transition_note": "out-of-order transition note",
                },
                {
                    "window_id": "LG-02",
                    "window_order": 2,
                    "workflow_note": "workflow note later",
                    "movement_reading": "bounded improvement signal",
                    "context_note": "context note later",
                    "transition_note": "second out-of-order transition note",
                },
            ]
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("window_order values must be strictly increasing" in issue.message for issue in issues)
