from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import run_sibling_canary  # noqa: E402


def write_matrix(path: Path, entries: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"matrix_version": 1, "entries": entries}, indent=2) + "\n", encoding="utf-8")


def test_sibling_canary_reports_success_with_resolved_roots(tmp_path: Path, monkeypatch) -> None:
    repo_root = tmp_path / "aoa-evals"
    repo_root.mkdir(parents=True)
    techniques_root = tmp_path / "aoa-techniques"
    skills_root = tmp_path / "aoa-skills"
    techniques_root.mkdir()
    skills_root.mkdir()

    matrix_path = repo_root / "scripts" / "sibling_canary_matrix.json"
    write_matrix(
        matrix_path,
        [
            {
                "repo": "aoa-techniques",
                "root_variable": "AOA_TECHNIQUES_ROOT",
                "path": "../aoa-techniques",
                "purpose": "fixture techniques check",
                "resolver": "direct",
            },
            {
                "repo": "aoa-skills",
                "root_variable": "AOA_SKILLS_ROOT",
                "path": "../aoa-skills",
                "purpose": "fixture skills check",
                "resolver": "direct",
            },
        ],
    )

    original_techniques_root = run_sibling_canary.validate_repo.AOA_TECHNIQUES_ROOT
    captured: dict[str, Path] = {}

    def fake_invoke(repo_root_arg: Path) -> tuple[int, str]:
        assert repo_root_arg == repo_root.resolve()
        captured["techniques"] = run_sibling_canary.validate_repo.AOA_TECHNIQUES_ROOT
        captured["skills"] = run_sibling_canary.validate_repo.AOA_SKILLS_ROOT
        return 0, "Validation passed for 0 eval bundles."

    monkeypatch.setattr(run_sibling_canary, "invoke_validator", fake_invoke)

    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exit_code = run_sibling_canary.main(
            [
                "--repo-root",
                str(repo_root),
                "--matrix",
                "scripts/sibling_canary_matrix.json",
            ]
        )

    assert exit_code == 0
    assert captured["techniques"] == techniques_root.resolve()
    assert captured["skills"] == skills_root.resolve()
    assert run_sibling_canary.validate_repo.AOA_TECHNIQUES_ROOT == original_techniques_root
    output = stdout.getvalue()
    assert "validator status: ok" in output
    assert "aoa-techniques" in output
    assert "aoa-skills" in output


def test_sibling_canary_prefers_source_checkout_for_abyss_stack(tmp_path: Path, monkeypatch) -> None:
    repo_root = tmp_path / "aoa-evals"
    repo_root.mkdir(parents=True)
    runtime_like_root = tmp_path / "abyss-stack"
    (runtime_like_root / "Configs").mkdir(parents=True)

    home_root = tmp_path / "home" / "dionysus"
    source_root = home_root / "src" / "abyss-stack"
    (source_root / "scripts").mkdir(parents=True)
    (source_root / "schemas").mkdir(parents=True)
    (source_root / "README.md").write_text("# abyss-stack\n", encoding="utf-8")
    (source_root / "scripts" / "validate_stack.py").write_text("print('ok')\n", encoding="utf-8")
    (source_root / "schemas" / "runtime-return-event.schema.json").write_text("{}\n", encoding="utf-8")
    monkeypatch.setenv("HOME", str(home_root))
    monkeypatch.delenv("ABYSS_STACK_ROOT", raising=False)

    matrix_path = repo_root / "scripts" / "sibling_canary_matrix.json"
    write_matrix(
        matrix_path,
        [
            {
                "repo": "abyss-stack",
                "root_variable": "ABYSS_STACK_ROOT",
                "path": "../abyss-stack",
                "purpose": "fixture abyss-stack check",
                "resolver": "abyss-stack-source",
            }
        ],
    )

    captured: dict[str, Path] = {}

    def fake_invoke(repo_root_arg: Path) -> tuple[int, str]:
        assert repo_root_arg == repo_root.resolve()
        captured["abyss_stack"] = run_sibling_canary.validate_repo.ABYSS_STACK_ROOT
        return 0, "Validation passed for 0 eval bundles."

    monkeypatch.setattr(run_sibling_canary, "invoke_validator", fake_invoke)

    exit_code = run_sibling_canary.main(
        [
            "--repo-root",
            str(repo_root),
            "--matrix",
            "scripts/sibling_canary_matrix.json",
        ]
    )

    assert exit_code == 0
    assert captured["abyss_stack"] == source_root.resolve()


def test_sibling_canary_reports_missing_repo_path(tmp_path: Path) -> None:
    repo_root = tmp_path / "aoa-evals"
    repo_root.mkdir(parents=True)
    matrix_path = repo_root / "scripts" / "sibling_canary_matrix.json"
    write_matrix(
        matrix_path,
        [
            {
                "repo": "aoa-techniques",
                "root_variable": "AOA_TECHNIQUES_ROOT",
                "path": "../aoa-techniques",
                "purpose": "fixture techniques check",
                "resolver": "direct",
            }
        ],
    )

    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exit_code = run_sibling_canary.main(
            [
                "--repo-root",
                str(repo_root),
                "--matrix",
                "scripts/sibling_canary_matrix.json",
            ]
        )

    assert exit_code == 2
    assert "does not exist" in stdout.getvalue()


def test_sibling_canary_reports_validator_failure(tmp_path: Path, monkeypatch) -> None:
    repo_root = tmp_path / "aoa-evals"
    repo_root.mkdir(parents=True)
    techniques_root = tmp_path / "aoa-techniques"
    techniques_root.mkdir()

    matrix_path = repo_root / "scripts" / "sibling_canary_matrix.json"
    write_matrix(
        matrix_path,
        [
            {
                "repo": "aoa-techniques",
                "root_variable": "AOA_TECHNIQUES_ROOT",
                "path": "../aoa-techniques",
                "purpose": "fixture techniques check",
                "resolver": "direct",
            }
        ],
    )

    monkeypatch.setattr(
        run_sibling_canary,
        "invoke_validator",
        lambda repo_root_arg: (1, "Validation failed for repository."),
    )

    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exit_code = run_sibling_canary.main(
            [
                "--repo-root",
                str(repo_root),
                "--matrix",
                "scripts/sibling_canary_matrix.json",
            ]
        )

    assert exit_code == 1
    assert "validator status: failed" in stdout.getvalue()
    assert "Validation failed for repository." in stdout.getvalue()
