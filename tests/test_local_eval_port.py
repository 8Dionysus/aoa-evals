from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_local_eval_port


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def make_port(
    repo_root: Path,
    *,
    status: str = "skeleton",
    boundary: str | None = None,
    owner_repo: str | None = None,
) -> None:
    boundary = boundary or "no verdict, scoring, regression, or proof doctrine authority"
    owner_repo = owner_repo or repo_root.name
    write_text(
        repo_root / "evals" / "PORT.yaml",
        f"""
        schema_version: local_eval_port_v1
        owner_repo: {owner_repo}
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


def write_valid_suite_note(repo_root: Path, *, owner_repo: str | None = None) -> None:
    owner_repo = owner_repo or repo_root.name
    write_text(
        repo_root / "evals" / "suites" / "memory-guardrail.suite.md",
        f"""
        ---
        schema_version: local_eval_suite_note_v1
        owner_repo: {owner_repo}
        status: draft
        authority_boundary: no verdict, scoring, regression, or proof doctrine authority
        ---

        # Memory Guardrail Suite

        Local suite shape for memo-side guardrail pressure.
        """,
    )


def write_valid_report_note(repo_root: Path, *, owner_repo: str | None = None) -> None:
    owner_repo = owner_repo or repo_root.name
    write_text(
        repo_root / "evals" / "reports" / "memory-guardrail.report.md",
        f"""
        ---
        schema_version: local_eval_report_note_v1
        owner_repo: {owner_repo}
        status: draft
        authority_boundary: no verdict, scoring, regression, or proof doctrine authority
        ---

        # Memory Guardrail Report

        Local report shell for memo-side guardrail pressure.
        """,
    )


def write_suite_execution_contract(
    repo_root: Path,
    *,
    slug: str = "memory-guardrail",
    source_rel: str = "tests/memory_guardrail.py",
    source_kind: str = "file",
    source_sha256: str | None = None,
    source_content: str = "def test_guardrail():\n    assert True\n",
    owner_repo: str | None = None,
    overrides: dict[str, object] | None = None,
) -> Path:
    owner_repo = owner_repo or repo_root.name
    source_path = repo_root / source_rel
    if source_kind == "tree":
        source_path.mkdir(parents=True, exist_ok=True)
        write_text(source_path / "test_guardrail.py", source_content)
        entrypoint_ref = f"{source_rel}/test_guardrail.py"
    else:
        write_text(source_path, source_content)
        entrypoint_ref = source_rel
    if source_sha256 is None:
        source_sha256 = validate_local_eval_port.compute_tracked_source_sha256(
            source_path,
            source_kind,
        )
    payload: dict[str, object] = {
        "schema_version": "local_eval_suite_execution_v1",
        "suite_id": slug,
        "owner_repo": owner_repo,
        "suite_note_ref": f"evals/suites/{slug}.suite.md",
        "runner": {
            "kind": "python_pytest",
            "argv": ["python", "-m", "pytest", "-q", entrypoint_ref],
            "cwd": ".",
        },
        "entrypoint_ref": entrypoint_ref,
        "timeout_seconds": 120,
        "success_exit_codes": [0],
        "tracked_sources": [
            {
                "path": source_rel,
                "kind": source_kind,
                "sha256": source_sha256,
            }
        ],
        "auto_run_allowed": False,
        "proof_authority": False,
        "promotion_allowed": False,
        "readiness_scope": "source-contract-ready",
        "runtime_reproducibility_proven": False,
        "jit_revalidation_required": True,
        "execution_receipt_required": True,
        "environment_capture_required": True,
        "authority_boundary": validate_local_eval_port.LOCAL_SUITE_AUTHORITY_BOUNDARY,
    }
    if overrides:
        payload.update(overrides)
    path = repo_root / "evals" / "suites" / f"{slug}.suite.json"
    write_text(path, json.dumps(payload, indent=2) + "\n")
    return path


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


def test_suite_note_alone_is_not_runnable(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "absent"
    assert execution["suite_count"] == 0
    assert execution["ready_count"] == 0


def test_valid_suite_execution_contract_is_ready_without_running_it(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)
    marker = repo_root / "executed.marker"
    write_suite_execution_contract(
        repo_root,
        source_content="from pathlib import Path\nPath('executed.marker').write_text('ran')\n",
    )

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "ready"
    assert execution["ready_count"] == 1
    assert execution["readiness_scope"] == "source-contract-ready"
    assert execution["runtime_reproducibility_proven"] is False
    assert execution["jit_revalidation_required"] is True
    assert execution["execution_receipt_required"] is True
    assert execution["environment_capture_required"] is True
    assert execution["suites"][0]["runner"]["argv"][-1] == "tests/memory_guardrail.py"
    assert not marker.exists()


def test_python_pytest_runner_allows_bytecode_off_and_cacheprovider_disable(
    tmp_path: Path,
) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)
    write_suite_execution_contract(
        repo_root,
        overrides={
            "runner": {
                "kind": "python_pytest",
                "argv": [
                    "python",
                    "-B",
                    "-m",
                    "pytest",
                    "-q",
                    "-p",
                    "no:cacheprovider",
                    "tests/memory_guardrail.py",
                ],
                "cwd": ".",
            }
        },
    )

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "ready"


def test_runner_entrypoint_argument_must_resolve_from_runner_cwd(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)
    write_suite_execution_contract(
        repo_root,
        overrides={
            "runner": {
                "kind": "python_pytest",
                "argv": ["python", "-m", "pytest", "tests/memory_guardrail.py"],
                "cwd": "tests",
            }
        },
    )

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "invalid"
    assert any("runner.cwd" in issue["message"] for issue in execution["issues"])


def test_runner_entrypoint_argument_may_be_cwd_relative(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)
    write_suite_execution_contract(
        repo_root,
        overrides={
            "runner": {
                "kind": "python_pytest",
                "argv": ["python", "-m", "pytest", "memory_guardrail.py"],
                "cwd": "tests",
            }
        },
    )

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "ready"


def test_named_git_worktree_uses_canonical_common_dir_and_origin_owner(
    tmp_path: Path,
) -> None:
    canonical_root = tmp_path / "aoa-skills"
    worktree_root = tmp_path / "aoa-skills-executable-eval-pilot-20260710"
    subprocess.run(["git", "init", "-q", canonical_root], check=True)
    write_text(canonical_root / "README.md", "# aoa-skills\n")
    subprocess.run(["git", "-C", canonical_root, "add", "README.md"], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            canonical_root,
            "-c",
            "user.name=AoA Test",
            "-c",
            "user.email=aoa-test@example.invalid",
            "commit",
            "-qm",
            "initial",
        ],
        check=True,
    )
    subprocess.run(
        [
            "git",
            "-C",
            canonical_root,
            "remote",
            "add",
            "origin",
            "https://github.com/Agents-of-Abyss/aoa-skills.git",
        ],
        check=True,
    )
    subprocess.run(
        ["git", "-C", canonical_root, "worktree", "add", "-qb", "pilot", worktree_root],
        check=True,
    )
    assert (worktree_root / ".git").is_file()
    make_port(worktree_root, status="active", owner_repo="aoa-skills")
    write_valid_suite_note(worktree_root, owner_repo="aoa-skills")
    write_valid_report_note(worktree_root, owner_repo="aoa-skills")
    write_suite_execution_contract(worktree_root, owner_repo="aoa-skills")

    issues = validate_local_eval_port.validate_local_eval_port(worktree_root)
    execution = validate_local_eval_port.evaluate_local_suite_execution(worktree_root)

    assert issues == []
    assert execution["state"] == "ready"
    assert execution["canonical_owner_repo"] == "aoa-skills"
    assert execution["owner_identity_sources"] == ["git_common_dir", "git_origin"]


def test_git_common_dir_origin_identity_conflict_invalidates_suite(tmp_path: Path) -> None:
    repo_root = tmp_path / "spoof-repo"
    write_text(repo_root / ".git" / "HEAD", "ref: refs/heads/main\n")
    write_text(
        repo_root / ".git" / "config",
        """
        [remote "origin"]
            url = https://github.com/Agents-of-Abyss/aoa-evals.git
        """,
    )
    make_port(repo_root, status="active", owner_repo="aoa-evals")
    write_valid_suite_note(repo_root, owner_repo="aoa-evals")
    write_suite_execution_contract(repo_root, owner_repo="aoa-evals")

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "invalid"
    assert any("conflicts with origin owner" in issue["message"] for issue in execution["issues"])


def test_suite_execution_contract_becomes_stale_when_tracked_source_changes(
    tmp_path: Path,
) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)
    write_suite_execution_contract(repo_root)
    write_text(repo_root / "tests" / "memory_guardrail.py", "CHANGED = True\n")

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "stale"
    assert execution["stale_count"] == 1
    assert execution["suites"][0]["stale_sources"][0]["path"] == "tests/memory_guardrail.py"


def test_suite_execution_tree_hash_detects_nested_change(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)
    write_suite_execution_contract(
        repo_root,
        source_rel="tests/guardrail_suite",
        source_kind="tree",
    )
    write_text(repo_root / "tests" / "guardrail_suite" / "nested.py", "CHANGED = True\n")

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "stale"


def test_suite_execution_aggregate_priority_is_invalid_stale_ready_absent(
    tmp_path: Path,
) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)
    write_suite_execution_contract(repo_root, slug="memory-guardrail")
    write_valid_suite_note_for_slug(repo_root, "stale-guardrail")
    write_suite_execution_contract(repo_root, slug="stale-guardrail", source_rel="tests/stale.py")
    write_text(repo_root / "tests" / "stale.py", "CHANGED = True\n")

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)
    assert execution["state"] == "stale"

    write_text(repo_root / "evals" / "suites" / "invalid.suite.json", "{}\n")
    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)
    assert execution["state"] == "invalid"


def write_valid_suite_note_for_slug(repo_root: Path, slug: str) -> None:
    write_text(
        repo_root / "evals" / "suites" / f"{slug}.suite.md",
        f"""
        ---
        schema_version: local_eval_suite_note_v1
        owner_repo: {repo_root.name}
        status: draft
        authority_boundary: no verdict, scoring, regression, or proof doctrine authority
        ---

        # {slug}
        """,
    )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("suite_note_ref", "../outside.suite.md"),
        ("entrypoint_ref", "../outside.py"),
        (
            "runner",
            {
                "kind": "python_pytest",
                "argv": ["python", "-m", "pytest", "tests/memory_guardrail.py"],
                "cwd": "../outside",
            },
        ),
        (
            "tracked_sources",
            [{"path": "../outside.py", "kind": "file", "sha256": "0" * 64}],
        ),
    ],
)
def test_suite_execution_rejects_path_traversal(
    tmp_path: Path,
    field: str,
    value: object,
) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)
    write_suite_execution_contract(repo_root, overrides={field: value})

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "invalid"
    assert any(
        "repo-relative" in issue["message"]
        or "traversal" in issue["message"]
        or "schema violation" in issue["message"]
        for issue in execution["issues"]
    )


def test_suite_execution_rejects_symlinked_tracked_source(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)
    real_source = repo_root / "real.py"
    write_text(real_source, "VALUE = 1\n")
    linked_source = repo_root / "tests" / "memory_guardrail.py"
    linked_source.parent.mkdir(parents=True, exist_ok=True)
    linked_source.symlink_to(real_source)
    digest = validate_local_eval_port.compute_file_sha256(real_source)
    write_suite_execution_contract(repo_root, source_sha256=digest)
    linked_source.unlink()
    linked_source.symlink_to(real_source)

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "invalid"
    assert any("symlink" in issue["message"] for issue in execution["issues"])


def test_suite_execution_rejects_directory_named_as_json_sidecar(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)
    (repo_root / "evals" / "suites" / "bad.suite.json").mkdir()

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "invalid"
    assert any("regular file" in issue["message"] for issue in execution["issues"])


def test_suite_execution_rejects_non_utf8_json_sidecar(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)
    path = repo_root / "evals" / "suites" / "bad.suite.json"
    path.write_bytes(b"\xff\xfe\x00")

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "invalid"
    assert any("UTF-8" in issue["message"] for issue in execution["issues"])


@pytest.mark.parametrize("symlink_level", ["evals", "suites"])
def test_suite_execution_rejects_symlinked_parent_directory_before_glob_or_read(
    tmp_path: Path,
    symlink_level: str,
) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    external = tmp_path / f"external-{symlink_level}"
    if symlink_level == "evals":
        (repo_root / "evals").rename(external)
        (repo_root / "evals").symlink_to(external, target_is_directory=True)
    else:
        (repo_root / "evals" / "suites").rename(external)
        (repo_root / "evals" / "suites").symlink_to(external, target_is_directory=True)

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)
    port_issues = validate_local_eval_port.validate_local_eval_port(repo_root)

    assert execution["state"] == "invalid"
    assert any("symlink" in issue["message"] for issue in execution["issues"])
    assert any("symlink" in issue.message for issue in port_issues)


@pytest.mark.parametrize(
    "argv",
    [
        ["bash", "-c", "pytest -q"],
        ["env", "bash", "-c", "pytest -q"],
        ["/usr/bin/env", "zsh", "-c", "pytest -q"],
        ["command", "sh", "-c", "pytest -q"],
        ["busybox", "sh", "-c", "pytest -q"],
        ["python", "-c", "print('unsafe')"],
        ["python", "-m", "pytest", "tests/test_guardrail.py;touch", "marker"],
        ["python", "-m", "pytest", "$(touch marker)"],
        ["python", "-m", "pytest", "tests/test_guardrail.py", "&&", "touch"],
    ],
)
def test_suite_execution_rejects_shell_or_metacharacter_argv(
    tmp_path: Path,
    argv: list[str],
) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)
    write_suite_execution_contract(
        repo_root,
        overrides={"runner": {"kind": "python_pytest", "argv": argv, "cwd": "."}},
    )

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "invalid"
    assert any("shell-free" in issue["message"] for issue in execution["issues"])


@pytest.mark.parametrize(
    "argv",
    [
        ["python", "-m", "pytest", "tests/other.py"],
        ["python", "-m", "pytest", "/tmp/tests/memory_guardrail.py"],
        ["python", "-m", "pytest", "../tests/memory_guardrail.py"],
        ["python", "-m", "pytest", "tests/../tests/memory_guardrail.py"],
    ],
)
def test_suite_execution_binds_argv_to_entrypoint_and_rejects_escaping_path_args(
    tmp_path: Path,
    argv: list[str],
) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)
    write_suite_execution_contract(
        repo_root,
        overrides={"runner": {"kind": "python_pytest", "argv": argv, "cwd": "."}},
    )

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "invalid"
    assert any(
        "entrypoint_ref" in issue["message"]
        or "repo-relative path arguments" in issue["message"]
        for issue in execution["issues"]
    )


@pytest.mark.parametrize(
    "argv",
    [
        ["python", "-B", "-c", "print('unsafe')", "tests/memory_guardrail.py"],
        ["/tmp/unreviewed-runner", "tests/memory_guardrail.py"],
        ["node", "-e", "require('child_process')", "tests/memory_guardrail.py"],
        ["python", "-m", "pip", "tests/memory_guardrail.py"],
        ["python", "-m", "pytest", "-p", "unreviewed_plugin", "tests/memory_guardrail.py"],
        ["python", "-m", "pytest", "--rootdir=/tmp", "tests/memory_guardrail.py"],
    ],
)
def test_python_pytest_runner_rejects_semantic_dispatch_bypasses(
    tmp_path: Path,
    argv: list[str],
) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)
    write_suite_execution_contract(
        repo_root,
        overrides={
            "runner": {
                "kind": "python_pytest",
                "argv": argv,
                "cwd": ".",
            }
        },
    )

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "invalid"
    assert any("python_pytest" in issue["message"] for issue in execution["issues"])


@pytest.mark.parametrize("flag", ["auto_run_allowed", "proof_authority", "promotion_allowed"])
def test_suite_execution_rejects_authority_or_automatic_execution_flags(
    tmp_path: Path,
    flag: str,
) -> None:
    repo_root = tmp_path / "aoa-memo"
    make_port(repo_root, status="active")
    write_valid_suite_note(repo_root)
    write_suite_execution_contract(repo_root, overrides={flag: True})

    execution = validate_local_eval_port.evaluate_local_suite_execution(repo_root)

    assert execution["state"] == "invalid"


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


def test_port_boundary_accepts_modal_route_to_aoa_evals_authority(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "verdict, scoring, regression, and proof doctrine authority must "
            "be routed to aoa-evals"
        ),
    )

    assert validate_local_eval_port.validate_local_eval_port(repo_root) == []


def test_port_boundary_accepts_modal_active_route_to_aoa_evals_authority(
    tmp_path: Path,
) -> None:
    repo_root = tmp_path / "aoa-routing"
    make_port(
        repo_root,
        boundary=(
            "verdict, scoring, regression, and proof doctrine authority must "
            "route to aoa-evals"
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
