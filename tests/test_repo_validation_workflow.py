from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validators import boundary_bridge_canary as boundary_bridge_canary_validator
from validators import boundary_bridge_workflow as boundary_bridge_workflow_validator


def copy_repo_text(repo_root: Path, relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)
    destination = repo_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def test_repo_validation_workflow_surface_validates_current_pin() -> None:
    assert boundary_bridge_workflow_validator.validate_repo_validation_workflow_surface(REPO_ROOT) == []


def test_repo_validation_workflow_rejects_sibling_checkout(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, ".github/workflows/repo-validation.yml")
    workflow_path = tmp_path / ".github" / "workflows" / "repo-validation.yml"
    workflow_text = workflow_path.read_text(encoding="utf-8")
    workflow_text = workflow_text.replace(
        "      - name: Setup Python",
        """      - name: Checkout aoa-memo
        uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd
        with:
          repository: 8Dionysus/aoa-memo
          ref: 97f19698c94ebbebabe8b1b6f22e5ccff3bc5f1f
          path: .deps/aoa-memo

      - name: Setup Python""",
    )
    workflow_path.write_text(workflow_text, encoding="utf-8")

    issues = boundary_bridge_workflow_validator.validate_repo_validation_workflow_surface(tmp_path)

    assert any(
        issue.location == ".github/workflows/repo-validation.yml"
        and "must not checkout or pin sibling repositories" in issue.message
        for issue in issues
    )


def test_repo_validation_workflow_rejects_sibling_root_env(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, ".github/workflows/repo-validation.yml")
    workflow_path = tmp_path / ".github" / "workflows" / "repo-validation.yml"
    workflow_text = workflow_path.read_text(encoding="utf-8")
    workflow_text = workflow_text.replace(
        "    steps:",
        "    env:\n      AOA_PLAYBOOKS_ROOT: ${{ github.workspace }}/.deps/aoa-playbooks\n    steps:",
    )
    workflow_path.write_text(workflow_text, encoding="utf-8")

    issues = boundary_bridge_workflow_validator.validate_repo_validation_workflow_surface(tmp_path)

    assert any(
        issue.location == ".github/workflows/repo-validation.yml"
        and "must not checkout or pin sibling repositories" in issue.message
        for issue in issues
    )


def test_sibling_canary_matrix_surface_validates_current_entries() -> None:
    assert boundary_bridge_canary_validator.validate_sibling_canary_matrix_surface(REPO_ROOT) == []


def test_sibling_canary_matrix_rejects_missing_expected_repo(tmp_path: Path) -> None:
    copy_repo_text(tmp_path, boundary_bridge_canary_validator.SIBLING_CANARY_MATRIX_NAME)
    matrix_path = tmp_path / boundary_bridge_canary_validator.SIBLING_CANARY_MATRIX_NAME
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    matrix["entries"] = [
        entry
        for entry in matrix["entries"]
        if entry.get("repo") != "aoa-memo"
    ]
    matrix_path.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")

    issues = boundary_bridge_canary_validator.validate_sibling_canary_matrix_surface(tmp_path)

    assert any(
        issue.location == boundary_bridge_canary_validator.SIBLING_CANARY_MATRIX_NAME
        and "missing sibling canary entry for aoa-memo" in issue.message
        for issue in issues
    )


def test_sibling_canary_matrix_rejects_abyss_stack_direct_resolver(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, boundary_bridge_canary_validator.SIBLING_CANARY_MATRIX_NAME)
    matrix_path = tmp_path / boundary_bridge_canary_validator.SIBLING_CANARY_MATRIX_NAME
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    for entry in matrix["entries"]:
        if entry.get("repo") == "abyss-stack":
            entry["resolver"] = "direct"
    matrix_path.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")

    issues = boundary_bridge_canary_validator.validate_sibling_canary_matrix_surface(tmp_path)

    assert any(
        issue.location == boundary_bridge_canary_validator.SIBLING_CANARY_MATRIX_NAME
        and "abyss-stack-source" in issue.message
        for issue in issues
    )
