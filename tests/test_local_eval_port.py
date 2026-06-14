from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_local_eval_port


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def make_port(repo_root: Path, *, status: str = "skeleton", boundary: str | None = None) -> None:
    boundary = boundary or "no verdict, scoring, regression, or proof doctrine authority"
    write_text(
        repo_root / "evals" / "PORT.yaml",
        f"""
        schema_version: local_eval_port_v1
        owner_repo: {repo_root.name}
        status: {status}
        proof_owner_repo: aoa-evals
        default_intake_schema: eval_need_v1
        local_role: repo-local eval pressure, fixtures, suites, and reports
        central_boundary: {boundary}
        """,
    )
    write_text(
        repo_root / "evals" / "README.md",
        """
        # Local Eval Port

        This local port preserves repo-local eval pressure. `aoa-evals` owns
        central verdict, scoring, regression, and proof doctrine authority.
        """,
    )
    write_text(
        repo_root / "evals" / "AGENTS.md",
        """
        # AGENTS.md

        Local eval pressure may be captured here. Route verdict, scoring,
        regression, and proof doctrine authority to `aoa-evals`.
        """,
    )
    write_text(repo_root / "evals" / "intake" / "README.md", "# Intake\n")
    write_text(repo_root / "evals" / "suites" / "README.md", "# Suites\n")
    write_text(repo_root / "evals" / "reports" / "README.md", "# Reports\n")


def write_valid_intake(repo_root: Path) -> None:
    payload = {
        "schema_version": "eval_need_v1",
        "name": "aoa-memory-guardrail-pressure",
        "proof_question": "Does memory guardrail pressure route to bounded proof review?",
        "origin_need": "A local memory handoff needs a route before central proof adoption.",
        "summary": "Checks whether memory guardrail pressure stays below proof authority.",
        "object_under_evaluation": "memory guardrail handoff",
        "category": "boundary",
        "claim_type": "bounded",
        "baseline_mode": "none",
        "report_format": "summary-with-breakdown",
        "verdict_shape": "categorical",
        "authoring_route": "candidate_evidence_packet",
        "expected_use_when": ["memory guardrail pressure appears locally"],
        "blind_spot_notes": ["does not accept a central proof verdict"],
        "candidate_evidence_refs": [
            "mechanics/consumer-handoff/parts/eval-guardrail-handoff/"
        ],
        "source_refs": ["evals/README.md"],
    }
    write_text(
        repo_root / "evals" / "intake" / "memory-guardrail.eval_need.json",
        json.dumps(payload, indent=2) + "\n",
    )


def write_valid_suite_note(repo_root: Path) -> None:
    write_text(
        repo_root / "evals" / "suites" / "memory-guardrail.suite.md",
        f"""
        ---
        schema_version: local_eval_suite_note_v1
        owner_repo: {repo_root.name}
        status: draft
        authority_boundary: no verdict, scoring, regression, or proof doctrine authority
        ---

        # Memory Guardrail Suite

        Local suite shape for memo-side guardrail pressure.
        """,
    )


def write_valid_report_note(repo_root: Path) -> None:
    write_text(
        repo_root / "evals" / "reports" / "memory-guardrail.report.md",
        f"""
        ---
        schema_version: local_eval_report_note_v1
        owner_repo: {repo_root.name}
        status: draft
        authority_boundary: no verdict, scoring, regression, or proof doctrine authority
        ---

        # Memory Guardrail Report

        Local report shell for memo-side guardrail pressure.
        """,
    )


def test_valid_skeleton_port_passes(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(repo_root)

    assert validate_local_eval_port.validate_local_eval_port(repo_root) == []


def test_missing_port_yaml_fails(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(repo_root)
    (repo_root / "evals" / "PORT.yaml").unlink()

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any(issue.location == "evals/PORT.yaml" for issue in issues)


def test_active_port_requires_intake_or_bundle(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("active local eval port" in issue.message for issue in issues)


def test_valid_active_suite_note_passes(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)

    assert validate_local_eval_port.validate_local_eval_port(repo_root) == []


def test_valid_active_report_note_passes(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_report_note(repo_root)

    assert validate_local_eval_port.validate_local_eval_port(repo_root) == []


def test_skeleton_port_rejects_suite_or_report_pressure(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(repo_root, status="skeleton")
    write_valid_suite_note(repo_root)

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("skeleton local eval port" in issue.message for issue in issues)


def test_local_note_frontmatter_boundary_is_required(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_text(
        repo_root / "evals" / "reports" / "bad.report.md",
        f"""
        ---
        schema_version: local_eval_report_note_v1
        owner_repo: {repo_root.name}
        status: draft
        authority_boundary: local proof
        ---

        # Bad Report
        """,
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("authority_boundary" in issue.message for issue in issues)


def test_local_note_filename_shape_is_required(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_text(
        repo_root / "evals" / "suites" / "bad.md",
        """
        ---
        schema_version: local_eval_suite_note_v1
        owner_repo: aoa-memo
        status: draft
        authority_boundary: no verdict, scoring, regression, or proof doctrine authority
        ---

        # Bad Suite
        """,
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("filename must match" in issue.message for issue in issues)


def test_valid_active_intake_passes(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_intake(repo_root)

    assert validate_local_eval_port.validate_local_eval_port(repo_root) == []


def test_invalid_intake_schema_fails(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_text(
        repo_root / "evals" / "intake" / "bad.eval_need.json",
        '{"schema_version": "eval_need_v1"}\n',
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("schema violation" in issue.message for issue in issues)


def test_local_bundle_requires_eval_markdown(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_text(
        repo_root / "evals" / "boundary" / "aoa-memory-local-proof" / "eval.yaml",
        """
        name: aoa-memory-local-proof
        category: boundary
        baseline_mode: none
        """,
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any(issue.location.endswith("/EVAL.md") for issue in issues)


def test_port_boundary_must_keep_central_authority_visible(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-kag"
    make_port(repo_root, boundary="local proof workspace")

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("central_boundary" in issue.message for issue in issues)


def test_port_boundary_rejects_local_authority_affirmation(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary="local verdict, scoring, regression, and proof doctrine authority",
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("central_boundary" in issue.message for issue in issues)


def test_port_boundary_rejects_split_denial_then_local_authority(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "no central authority; local verdict, scoring, regression, "
            "and proof doctrine authority"
        ),
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("central_boundary" in issue.message for issue in issues)


def test_port_boundary_requires_denial_for_each_authority_term(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "no local verdict authority; scoring, regression, "
            "and proof doctrine stay local"
        ),
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("central_boundary" in issue.message for issue in issues)


def test_port_boundary_rejects_comma_grant_after_partial_denial(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "no local verdict authority, scoring, regression, "
            "and proof doctrine stay local"
        ),
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("central_boundary" in issue.message for issue in issues)


def test_port_boundary_accepts_split_denial_for_each_authority_term(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "no verdict authority; no scoring authority; "
            "no regression authority; no proof doctrine authority"
        ),
    )

    assert validate_local_eval_port.validate_local_eval_port(repo_root) == []


def test_port_boundary_accepts_route_to_aoa_evals_authority(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "local intake routes downstream to aoa-evals verdict, scoring, "
            "regression, and proof doctrine authority"
        ),
    )

    assert validate_local_eval_port.validate_local_eval_port(repo_root) == []


def test_port_boundary_rejects_route_for_only_one_authority_term(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "verdict authority routes to aoa-evals, while scoring, regression, "
            "and proof doctrine authority are undecided"
        ),
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("central_boundary" in issue.message for issue in issues)


def test_port_boundary_rejects_route_followed_by_negated_route(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "verdict authority routes to aoa-evals, and scoring, regression, "
            "and proof doctrine authority is not routed to aoa-evals"
        ),
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("central_boundary" in issue.message for issue in issues)


def test_port_boundary_rejects_unrelated_report_route(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "verdict, scoring, regression, and proof doctrine authority are "
            "undecided, and reports route to aoa-evals"
        ),
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("central_boundary" in issue.message for issue in issues)


def test_port_boundary_rejects_negated_route_to_aoa_evals_authority(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "verdict, scoring, regression, and proof doctrine authority is not "
            "routed to aoa-evals"
        ),
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("central_boundary" in issue.message for issue in issues)


def test_port_boundary_rejects_absent_route_to_aoa_evals_authority(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "verdict, scoring, regression, and proof doctrine authority has no "
            "route to aoa-evals"
        ),
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("central_boundary" in issue.message for issue in issues)


def test_port_boundary_rejects_stays_local_after_partial_denial(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "no local verdict authority, but scoring, regression, and proof "
            "doctrine authority stays local"
        ),
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("central_boundary" in issue.message for issue in issues)


def test_port_boundary_accepts_local_fixture_custody_with_authority_route(
    tmp_path: Path,
) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "local port keeps fixtures, and verdict, scoring, regression, "
            "and proof doctrine authority routes to aoa-evals"
        ),
    )

    assert validate_local_eval_port.validate_local_eval_port(repo_root) == []


def test_port_boundary_rejects_local_grant_with_aoa_evals_route(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "local verdict, scoring, regression, and proof doctrine authority, "
            "with reports routed downstream to aoa-evals"
        ),
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("central_boundary" in issue.message for issue in issues)


def test_port_boundary_rejects_local_subject_owning_authority_with_route(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "local port owns verdict, scoring, regression, and proof doctrine authority, "
            "with reports routed downstream to aoa-evals"
        ),
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("central_boundary" in issue.message for issue in issues)


def test_port_boundary_rejects_local_subject_having_authority_with_route(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "local port has verdict, scoring, regression, and proof doctrine authority, "
            "with reports routed downstream to aoa-evals"
        ),
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("central_boundary" in issue.message for issue in issues)


def test_port_boundary_accepts_denial_that_authority_stays_local(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary="no verdict, scoring, regression, or proof doctrine authority stays local",
    )

    assert validate_local_eval_port.validate_local_eval_port(repo_root) == []


def test_port_boundary_rejects_authority_is_local_with_route(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "reports route to aoa-evals, but verdict, scoring, regression, "
            "and proof doctrine authority is local"
        ),
    )

    issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert any("central_boundary" in issue.message for issue in issues)
