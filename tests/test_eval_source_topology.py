from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_repo
from validate_repo import run_validation
from validate_repo_fixtures import eval_dir_for_test, make_eval_bundle, write_catalogs


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def copy_repo_text(repo_root: Path, relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)
    destination = repo_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def test_eval_source_entry_operating_cards_validate_current_routes() -> None:
    assert validate_repo.validate_eval_source_entry_operating_cards(REPO_ROOT) == []


def test_eval_source_entry_operating_cards_reject_missing_selection_card(
    tmp_path: Path,
) -> None:
    for path_name in validate_repo.EVAL_SOURCE_ENTRY_OPERATING_CARD_REQUIRED_TOKENS:
        copy_repo_text(tmp_path, path_name)
    selection_path = tmp_path / validate_repo.EVAL_SELECTION_NAME
    selection_path.write_text(
        selection_path.read_text(encoding="utf-8").replace(
            "## Operating Card",
            "## Route Notes",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_eval_source_entry_operating_cards(tmp_path)

    assert any(
        issue.location == validate_repo.EVAL_SELECTION_NAME
        and "## Operating Card" in issue.message
        for issue in issues
    )


def test_eval_source_entry_operating_cards_reject_missing_source_index_card(
    tmp_path: Path,
) -> None:
    for path_name in validate_repo.EVAL_SOURCE_ENTRY_OPERATING_CARD_REQUIRED_TOKENS:
        copy_repo_text(tmp_path, path_name)
    source_index_path = tmp_path / "evals" / "README.md"
    source_index_path.write_text(
        source_index_path.read_text(encoding="utf-8").replace(
            "## Operating Card",
            "## Route Notes",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_eval_source_entry_operating_cards(tmp_path)

    assert any(
        issue.location == "evals/README.md"
        and "## Operating Card" in issue.message
        for issue in issues
    )


def test_source_eval_tree_topology_validates_current_route() -> None:
    assert validate_repo.validate_source_eval_tree_topology_surfaces(REPO_ROOT) == []


def test_source_eval_tree_topology_rejects_decision_command_list(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, validate_repo.SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME)
    copy_repo_text(tmp_path, validate_repo.EVALS_AGENTS_NAME)
    copy_repo_text(tmp_path, "docs/decisions/README.md")
    decision_path = tmp_path / validate_repo.SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME
    decision_path.write_text(
        decision_path.read_text(encoding="utf-8").replace(
            "Validation routes through",
            "Run:\n\n- `python scripts/validate_repo.py`\n\nValidation routes through",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_source_eval_tree_topology_surfaces(tmp_path)

    assert any(
        issue.location == validate_repo.SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME
        and "evals/AGENTS.md#validation" in issue.message
        for issue in issues
    )


def test_source_eval_tree_topology_requires_agents_command_route(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, validate_repo.SOURCE_EVAL_TREE_TOPOLOGY_DECISION_NAME)
    copy_repo_text(tmp_path, validate_repo.EVALS_AGENTS_NAME)
    copy_repo_text(tmp_path, "docs/decisions/README.md")
    agents_path = tmp_path / validate_repo.EVALS_AGENTS_NAME
    agents_path.write_text(
        agents_path.read_text(encoding="utf-8").replace(
            "python scripts/build_catalog.py --check",
            "python scripts/build_wrong_catalog.py --check",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo.validate_source_eval_tree_topology_surfaces(tmp_path)

    assert any(
        issue.location == validate_repo.EVALS_AGENTS_NAME
        and "python scripts/build_catalog.py --check" in issue.message
        for issue in issues
    )


def test_eval_bundle_topology_contracts_validate_current_tree() -> None:
    assert validate_repo.validate_eval_bundle_topology_contracts(REPO_ROOT) == []


def test_eval_bundle_topology_contracts_reject_flat_manifest(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "evals/README.md")
    copy_repo_text(tmp_path, validate_repo.EVALS_AGENTS_NAME)
    write_text(
        tmp_path / "evals" / "aoa-flat" / "EVAL.md",
        "# Flat Eval\n",
    )
    write_text(
        tmp_path / "evals" / "aoa-flat" / "eval.yaml",
        """
        name: aoa-flat
        category: workflow
        baseline_mode: none
        """,
    )

    issues = validate_repo.validate_eval_bundle_topology_contracts(tmp_path)

    assert any(
        issue.location == "evals/aoa-flat/eval.yaml"
        and "evals/<claim-family>/<eval-name>" in issue.message
        for issue in issues
    )


def test_source_eval_command_ownership_validates_current_routes() -> None:
    source_issues, records = validate_repo.collect_catalog_records(REPO_ROOT)

    assert source_issues == []
    assert validate_repo.validate_source_eval_command_ownership(
        REPO_ROOT, records
    ) == []


def test_source_eval_command_ownership_rejects_eval_command_block(
    tmp_path: Path,
) -> None:
    eval_path = (
        tmp_path / "evals" / "boundary" / "sample-command-owner" / "EVAL.md"
    )
    write_text(
        eval_path,
        """
        # Sample Eval

        ## Verification

        ```bash
        python scripts/validate_repo.py --eval sample-command-owner
        ```
        """,
    )
    record = validate_repo.EvalBundleRecord(
        name="sample-command-owner",
        bundle_dir=eval_path.parent,
        eval_md_path=eval_path,
        eval_yaml_path=eval_path.parent / "eval.yaml",
        metadata={},
        manifest={},
        sections={},
    )

    issues = validate_repo.validate_source_eval_command_ownership(tmp_path, [record])

    assert any(
        issue.location == "evals/boundary/sample-command-owner/EVAL.md"
        and "route executable validation commands to evals/AGENTS.md" in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_mirrored_field_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-field-drift")
    write_catalogs(tmp_path)

    manifest_path = eval_dir_for_test(tmp_path, "aoa-field-drift") / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["category"] = "artifact"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("field 'category' does not match" in issue.message for issue in issues)


def test_validate_repo_rejects_technique_dependency_order_mismatch(tmp_path: Path) -> None:
    technique_dependencies = [
        {
            "id": "AOA-T-0001",
            "repo": "8Dionysus/aoa-techniques",
            "path": "techniques/execution/agent-workflows-core/plan-diff-apply-verify-report/TECHNIQUE.md",
        },
        {
            "id": "AOA-T-0002",
            "repo": "aoa-techniques",
            "path": "techniques/docs/source-of-truth-layout/TECHNIQUE.md",
        },
    ]
    make_eval_bundle(
        tmp_path,
        name="aoa-technique-order-drift",
        technique_dependencies=technique_dependencies,
    )
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-technique-order-drift") / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    _opening, frontmatter_text, body = text.split("---", 2)
    frontmatter = yaml.safe_load(frontmatter_text)
    frontmatter["technique_dependencies"] = list(reversed(frontmatter["technique_dependencies"]))
    eval_md_path.write_text(
        f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---{body}",
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "ordered technique refs do not match"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_skill_dependency_order_mismatch(tmp_path: Path) -> None:
    skill_dependencies = [
        {
            "name": "aoa-change-protocol",
            "repo": "8Dionysus/aoa-skills",
            "path": "skills/core/engineering/aoa-change-protocol/SKILL.md",
        },
        {
            "name": "aoa-approval-gate-check",
            "repo": "aoa-skills",
            "path": "skills/aoa-approval-gate-check/SKILL.md",
        },
    ]
    make_eval_bundle(
        tmp_path,
        name="aoa-skill-order-drift",
        skill_dependencies=skill_dependencies,
    )
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-skill-order-drift") / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    _opening, frontmatter_text, body = text.split("---", 2)
    frontmatter = yaml.safe_load(frontmatter_text)
    frontmatter["skill_dependencies"] = list(reversed(frontmatter["skill_dependencies"]))
    eval_md_path.write_text(
        f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---{body}",
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "ordered skill refs do not match"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_repo_mismatch(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-repo-mismatch")
    write_catalogs(tmp_path)

    manifest_path = eval_dir_for_test(tmp_path, "aoa-repo-mismatch") / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["technique_dependencies"][0]["repo"] = "example/other-repo"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("repo must resolve to 'aoa-techniques'" in issue.message for issue in issues)


def test_validate_repo_rejects_non_repo_relative_dependency_path(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-path-mismatch")
    write_catalogs(tmp_path)

    manifest_path = eval_dir_for_test(tmp_path, "aoa-path-mismatch") / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["technique_dependencies"][0]["path"] = "../techniques/test/TECHNIQUE.md"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("path must be a concrete repo-relative path" in issue.message for issue in issues)


def test_validate_repo_accepts_dependency_targets_when_roots_exist(
    tmp_path: Path,
    monkeypatch,
) -> None:
    make_eval_bundle(tmp_path, name="aoa-valid-dependency-targets")
    write_catalogs(tmp_path)

    techniques_root = tmp_path / ".deps" / "aoa-techniques"
    skills_root = tmp_path / ".deps" / "aoa-skills"
    write_text(
        techniques_root
        / "techniques"
        / "execution"
        / "agent-workflows-core"
        / "plan-diff-apply-verify-report"
        / "TECHNIQUE.md",
        "# Technique\n",
    )
    write_text(
        skills_root / "skills" / "core" / "engineering" / "aoa-change-protocol" / "SKILL.md",
        "# Skill\n",
    )

    monkeypatch.setattr(validate_repo, "AOA_TECHNIQUES_ROOT", techniques_root)
    monkeypatch.setattr(validate_repo, "AOA_SKILLS_ROOT", skills_root)

    assert run_validation(tmp_path, eval_name="aoa-valid-dependency-targets") == []


def test_validate_repo_rejects_missing_dependency_target_when_root_exists(
    tmp_path: Path,
    monkeypatch,
) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-dependency-target")
    write_catalogs(tmp_path)

    techniques_root = tmp_path / ".deps" / "aoa-techniques"
    skills_root = tmp_path / ".deps" / "aoa-skills"
    write_text(techniques_root / "README.md", "# Technique Repo\n")
    write_text(
        skills_root / "skills" / "aoa-change-protocol" / "SKILL.md",
        "# Skill\n",
    )

    monkeypatch.setattr(validate_repo, "AOA_TECHNIQUES_ROOT", techniques_root)
    monkeypatch.setattr(validate_repo, "AOA_SKILLS_ROOT", skills_root)

    issues = run_validation(tmp_path, eval_name="aoa-missing-dependency-target")

    assert any(
        "dependency target does not exist: aoa-techniques/techniques/execution/agent-workflows-core/plan-diff-apply-verify-report/TECHNIQUE.md"
        in issue.message
        for issue in issues
    )
