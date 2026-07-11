from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_eval_forge_readiness as forge_check


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def make_repo(workspace: Path, repo_id: str) -> Path:
    repo_root = workspace / repo_id
    write_text(repo_root / ".git" / "HEAD", "ref: refs/heads/main\n")
    return repo_root


def make_port(repo_root: Path) -> None:
    write_text(
        repo_root / "evals" / "PORT.yaml",
        f"""
        schema_version: local_eval_port_v1
        owner_repo: {repo_root.name}
        status: skeleton
        proof_owner_repo: aoa-evals
        default_intake_schema: eval_need_v1
        local_role: repo-local eval pressure, fixtures, suites, and reports
        central_boundary: no verdict, scoring, regression, or proof doctrine authority
        """,
    )
    write_text(
        repo_root / "evals" / "README.md",
        "`aoa-evals` owns verdict, scoring, regression, and proof doctrine authority.\n",
    )
    write_text(
        repo_root / "evals" / "AGENTS.md",
        "Route verdict, scoring, regression, and proof doctrine authority to `aoa-evals`.\n",
    )
    write_text(repo_root / "evals" / "intake" / "README.md", "# Intake\n")
    write_text(repo_root / "evals" / "suites" / "README.md", "# Suites\n")
    write_text(repo_root / "evals" / "reports" / "README.md", "# Reports\n")


def make_fake_stack(stack_root: Path) -> None:
    write_text(
        stack_root / "mcp/services/aoa-evals-mcp/src/aoa_evals_mcp/core.py",
        """
        LOCAL_WRITE_ALLOWED_GLOBS = (
            "evals/intake/*.eval_need.json",
            "evals/suites/*.suite.md",
            "evals/reports/*.report.md",
            "evals/PORT.yaml status skeleton-to-active activation with first pressure",
        )
        LOCAL_NOTE_CONFIG = {
            "suites": {"glob_suffix": ".suite.md"},
            "reports": {"glob_suffix": ".report.md"},
        }
        LOCAL_SUITE_EXECUTION_READ_GLOB = "evals/suites/*.suite.json"
        WRITE_RECEIPT = {
            "write_receipt": {
                "schema": "aoa_evals_local_write_receipt_v1",
                "allowed_relative_globs": ["evals/intake/*.eval_need.json"],
                "proof_authority": False,
                "promotion_allowed": False,
            }
        }
        """,
    )
    write_text(
        stack_root / "mcp/services/aoa-evals-mcp/tests/test_evals_mcp.py",
        """
        def test_write_receipt_shape():
            assert "aoa_evals_local_write_receipt_v1"
            assert "write_receipt"
        """,
    )


def test_eval_forge_readiness_check_builds_gate_packet(tmp_path: Path) -> None:
    workspace = tmp_path / "AbyssOS"
    repo_root = make_repo(workspace, "aoa-routing")
    make_port(repo_root)
    stack_root = tmp_path / "abyss-stack"
    make_fake_stack(stack_root)

    payload = forge_check.build_payload(
        evals_root=REPO_ROOT,
        workspace_root=workspace,
        aoa_root=tmp_path / ".aoa",
        skills_source_root=tmp_path / "aoa-skills",
        installed_skills_root=tmp_path / "skills",
        stack_root=stack_root,
        include_live_checks=False,
        live_timeout=1,
        max_generated_age_hours=999999,
    )

    assert payload["schema_version"] == forge_check.SCHEMA_VERSION
    gates = {item["id"]: item for item in payload["gates"]}
    assert gates["manual_session_mining_gate"]["status"] == "ok"
    assert gates["repo_local_forge_flow_gate"]["status"] == "ok"
    assert gates["local_suite_execution_gate"]["status"] == "ok"
    assert gates["local_suite_execution_gate"]["evidence"]["owner_apply_required"] is True
    assert gates["mcp_write_side_gate"]["status"] == "ok"
    assert gates["mcp_write_side_gate"]["evidence"]["suite_sidecar_read_marker_present"] is True
    assert gates["mcp_write_side_gate"]["evidence"]["suite_sidecar_write_allowed"] is False
    assert gates["support_classification_gate"]["status"] == "ok"
    assert gates["forge_front_door_surface_gate"]["status"] == "ok"
    assert gates["forge_front_door_surface_gate"]["evidence"]["proof_authority"] is False
    assert gates["forge_front_door_surface_gate"]["evidence"]["promotion_allowed"] is False
    assert gates["verification_shape_gate"]["status"] == "ok"
    assert payload["dashboard_summary"]["local_eval_ports"]["with_local_port"] == 1
    front_door = payload["dashboard_summary"]["eval_forge_front_door"]
    assert front_door["surface_refs"]["operating_path_ref"].endswith("EVAL_FORGE_OPERATING_PATH.md")
    assert front_door["surface_refs"]["worksheet_example_ref"].endswith("aoa_eval_criteria_before_mining.eval_design_worksheet.example.json")
    assert front_door["proof_authority"] is False
    assert front_door["promotion_allowed"] is False
    assert any("--write-worksheet" in item["command"] for item in front_door["exact_commands"])
    assert "python scripts/check_eval_forge_readiness.py --json" in payload["verification_commands"]

    json.dumps(payload)
