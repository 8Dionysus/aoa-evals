from __future__ import annotations

import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_repo
from validators import mechanic_part_readme_contract as mechanic_parts_validator
from validators import mechanic_part_contract_common as mechanic_part_contract_common
from validators import mechanic_part_source_surfaces as mechanic_part_source_surfaces_validator


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


def eval_family_for_test(category: str = "workflow", baseline_mode: str = "none") -> Path:
    if baseline_mode == "fixed-baseline":
        return Path("comparison") / "fixed-baseline"
    if baseline_mode == "peer-compare":
        return Path("comparison") / "peer-compare"
    if baseline_mode == "longitudinal-window":
        return Path("comparison") / "longitudinal-window"
    return Path(category)


def eval_dir_for_test(
    repo_root: Path,
    name: str,
    *,
    category: str = "workflow",
    baseline_mode: str = "none",
) -> Path:
    matches = sorted((repo_root / "evals").glob(f"**/{name}/eval.yaml"))
    if matches:
        return matches[0].parent
    return repo_root / "evals" / eval_family_for_test(category, baseline_mode) / name


def write_agon_part_index(repo_root: Path, readme_name: str) -> None:
    write_text(
        repo_root / "mechanics" / "agon" / "PARTS.md",
        f"# Agon Parts\n\n- `{readme_name}`\n",
    )


def write_new_part_readme(
    repo_root: Path,
    body: str,
    *,
    readme_name: str = "mechanics/agon/parts/new-proof/README.md",
) -> str:
    write_text(repo_root / readme_name, body)
    return readme_name


def write_standard_new_part(
    repo_root: Path,
    *,
    readme_name: str = "mechanics/agon/parts/new-proof/README.md",
    inputs: str = "Local evidence.",
    outputs: str = "Local readout.",
    owner_split: str = "AoA keeps doctrine; aoa-evals keeps proof shape.",
    source_surfaces: str | None = None,
) -> str:
    write_agon_part_index(repo_root, readme_name)
    source_section = ""
    if source_surfaces is not None:
        source_section = f"""
        ## Source Surfaces

        {textwrap.indent(source_surfaces, "        ")}
        """
    return write_new_part_readme(
        repo_root,
        f"""
        # New Proof
        {source_section}
        ## Inputs

        {inputs}

        ## Outputs

        {outputs}

        ## Stronger Owner Split

        {owner_split}

        ## Stop-Lines

        | Pressure | Owner route |
        | --- | --- |
        | parent promotion pressure | `mechanics/agon/` parent route |

        ## Validation

        `python scripts/validate_repo.py`
        """,
        readme_name=readme_name,
    )


def test_mechanic_part_readme_contract_validates_current_routes() -> None:
    assert mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(REPO_ROOT) == []


def test_mechanic_part_readme_contract_rejects_heading_without_parent(
    tmp_path: Path,
) -> None:
    readme_name = "mechanics/proof-loop/parts/route-smoke/README.md"
    for path_name in (
        "mechanics/proof-loop/PARTS.md",
        readme_name,
        "mechanics/proof-loop/parts/route-smoke/VALIDATION.md",
    ):
        copy_repo_text(tmp_path, path_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "# Proof Loop / Route Smoke Part",
            "# Route Smoke Part",
            1,
        ),
        encoding="utf-8",
    )

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(tmp_path)

    assert any(
        issue.location == readme_name and "parent mechanic" in issue.message
        for issue in issues
    )


def test_mechanic_part_readme_contract_rejects_validation_heading_without_parent(
    tmp_path: Path,
) -> None:
    validation_name = "mechanics/proof-loop/parts/route-smoke/VALIDATION.md"
    for path_name in (
        "mechanics/proof-loop/PARTS.md",
        "mechanics/proof-loop/parts/route-smoke/README.md",
        validation_name,
    ):
        copy_repo_text(tmp_path, path_name)
    validation_path = tmp_path / validation_name
    validation_path.write_text(
        validation_path.read_text(encoding="utf-8").replace(
            "# Proof Loop / Route Smoke Validation",
            "# Route Smoke Validation",
            1,
        ),
        encoding="utf-8",
    )

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(tmp_path)

    assert any(
        issue.location == validation_name and "parent mechanic" in issue.message
        for issue in issues
    )


def test_mechanic_part_payload_inventory_validates_current_routes() -> None:
    assert mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(REPO_ROOT) == []


def test_mechanic_part_payload_inventory_rejects_active_decision_command_list(
    tmp_path: Path,
) -> None:
    copy_repo_text(
        tmp_path,
        mechanic_part_contract_common.MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME,
    )
    copy_repo_text(tmp_path, mechanic_part_contract_common.MECHANICS_AGENTS_NAME)
    decision_path = (
        tmp_path
        / mechanic_part_contract_common.MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME
    )
    decision_path.write_text(
        decision_path.read_text(encoding="utf-8").replace(
            "## Validation\n\nUse",
            "## Validation\n\n- python scripts/validate_repo.py\n\nUse",
            1,
        ),
        encoding="utf-8",
    )

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(
        tmp_path
    )

    assert any(
        issue.location == mechanic_part_contract_common.MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME
        and "mechanics/AGENTS.md#validation" in issue.message
        for issue in issues
    )


def test_mechanic_part_payload_inventory_requires_superseded_command_string(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, mechanic_part_contract_common.MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME)
    copy_repo_text(tmp_path, mechanic_part_contract_common.MECHANICS_AGENTS_NAME)
    decision_path = tmp_path / mechanic_part_contract_common.MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME
    decision_path.write_text(
        decision_path.read_text(encoding="utf-8").replace(
            mechanic_part_contract_common.MECHANIC_PART_PAYLOAD_INVENTORY_SUPERSEDED_COMMAND,
            "python -m pytest -q tests/test_mechanic_part_contracts.py -k changed_guard",
            1,
        ),
        encoding="utf-8",
    )

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(tmp_path)

    assert any(
        issue.location == mechanic_part_contract_common.MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME
        and mechanic_part_contract_common.MECHANIC_PART_PAYLOAD_INVENTORY_SUPERSEDED_COMMAND in issue.message
        for issue in issues
    )


def test_mechanic_part_source_surface_refs_validate_current_routes() -> None:
    assert mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(REPO_ROOT) == []


def test_mechanic_part_source_surfaces_section_validates_current_routes() -> None:
    assert mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(REPO_ROOT) == []


def test_mechanic_part_source_surfaces_section_rejects_singular_heading(
    tmp_path: Path,
) -> None:
    readme_name = "mechanics/proof-loop/parts/route-smoke/README.md"
    copy_repo_text(tmp_path, "mechanics/proof-loop/PARTS.md")
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "## Source Surfaces",
            "## Source Surface",
            1,
        ),
        encoding="utf-8",
    )

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(tmp_path)

    assert any(
        issue.location == readme_name and "## Source Surfaces" in issue.message
        for issue in issues
    )


def test_mechanic_part_source_surfaces_section_rejects_empty_section(
    tmp_path: Path,
) -> None:
    readme_name = "mechanics/proof-loop/parts/route-smoke/README.md"
    copy_repo_text(tmp_path, "mechanics/proof-loop/PARTS.md")
    copy_repo_text(tmp_path, readme_name)
    readme_path = tmp_path / readme_name
    text = readme_path.read_text(encoding="utf-8")
    text = text.replace(
        "## Source Surfaces\n\n- `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md`\n\n",
        "## Source Surfaces\n\n",
        1,
    )
    readme_path.write_text(text, encoding="utf-8")

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "at least one path-like source ref" in issue.message
        for issue in issues
    )


def test_mechanic_part_source_surface_refs_reject_stale_path(
    tmp_path: Path,
) -> None:
    readme_name = write_standard_new_part(
        tmp_path,
        source_surfaces="- `mechanics/agon/parts/new-proof/docs/missing.md`\n",
    )

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "stale source surface ref" in issue.message
        and "mechanics/agon/parts/new-proof/docs/missing.md" in issue.message
        for issue in issues
    )


def test_mechanic_part_source_surface_refs_allow_explicit_nonlocal_routes(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / "mechanics" / "agon" / "parts" / "new-proof" / "docs" / "note.md",
        "# Note\n",
    )

    assert (
        mechanic_part_source_surfaces_validator.source_surface_ref_resolution_issue(
            tmp_path,
            "mechanics/agon/parts/new-proof/docs/*.md",
        )
        is None
    )
    assert (
        mechanic_part_source_surfaces_validator.source_surface_ref_resolution_issue(
            tmp_path,
            "repo:aoa-playbooks/generated/phase_alpha_run_matrix.min.json",
        )
        is None
    )
    assert (
        mechanic_part_source_surfaces_validator.source_surface_ref_resolution_issue(
            tmp_path,
            "quests/<lane>/<state>/AOA-EV-Q-*.yaml",
        )
        is None
    )


def test_mechanic_part_readme_contract_rejects_unrouted_part(tmp_path: Path) -> None:
    write_text(
        tmp_path / "mechanics" / "agon" / "PARTS.md",
        "# Agon Parts\n\nNo concrete part route is listed here.\n",
    )
    readme_name = write_new_part_readme(
        tmp_path,
        """
        # New Proof

        ## Inputs

        Local evidence.

        ## Outputs

        Local readout.

        ## Stronger Owner Split

        AoA keeps doctrine; aoa-evals keeps proof shape.

        ## Stop-Lines

        No parent promotion.

        ## Validation

        `python scripts/validate_repo.py`
        """,
    )

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(tmp_path)

    assert any(
        issue.location == "mechanics/agon/PARTS.md"
        and readme_name in issue.message
        for issue in issues
    )


def test_mechanic_part_readme_contract_rejects_missing_owner_split(
    tmp_path: Path,
) -> None:
    readme_name = "mechanics/agon/parts/new-proof/README.md"
    write_agon_part_index(tmp_path, readme_name)
    write_new_part_readme(
        tmp_path,
        """
        # New Proof

        ## Inputs

        Local evidence.

        ## Outputs

        Local readout.

        ## Owner Split

        Too soft.

        ## Stop-Lines

        No parent promotion.

        ## Validation

        `python scripts/validate_repo.py`
        """,
        readme_name=readme_name,
    )

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(tmp_path)

    assert any(
        issue.location == readme_name and "## Stronger Owner Split" in issue.message
        for issue in issues
    )


def test_mechanic_part_readme_contract_rejects_stop_lines_without_route_table(
    tmp_path: Path,
) -> None:
    readme_name = write_standard_new_part(
        tmp_path,
        source_surfaces="- `mechanics/agon/parts/new-proof/README.md`",
    )
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            """| Pressure | Owner route |
| --- | --- |
| parent promotion pressure | `mechanics/agon/` parent route |""",
            "No parent promotion.",
        ),
        encoding="utf-8",
    )

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "Stop-Lines" in issue.message
        and "pressure-to-owner route table" in issue.message
        for issue in issues
    )


def test_mechanic_part_readme_contract_rejects_stop_lines_with_empty_route_cells(
    tmp_path: Path,
) -> None:
    readme_name = write_standard_new_part(
        tmp_path,
        source_surfaces="- `mechanics/agon/parts/new-proof/README.md`",
    )
    readme_path = tmp_path / readme_name
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace(
            "| parent promotion pressure | `mechanics/agon/` parent route |",
            "| parent promotion pressure | |",
        ),
        encoding="utf-8",
    )

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "Stop-Lines" in issue.message
        and "pressure-to-owner route table" in issue.message
        for issue in issues
    )


def test_mechanic_part_payload_inventory_rejects_unmentioned_payload_dir(
    tmp_path: Path,
) -> None:
    readme_name = write_standard_new_part(tmp_path)
    write_text(
        tmp_path / "mechanics" / "agon" / "parts" / "new-proof" / "fixtures" / "case.json",
        "{}\n",
    )

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "payload subdirectory `fixtures/`" in issue.message
        for issue in issues
    )


def test_mechanic_part_payload_inventory_rejects_unknown_payload_class(
    tmp_path: Path,
) -> None:
    write_standard_new_part(tmp_path, inputs="Local evidence from `mystery/`.")
    write_text(
        tmp_path / "mechanics" / "agon" / "parts" / "new-proof" / "mystery" / "case.json",
        "{}\n",
    )

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(tmp_path)

    assert any(
        issue.location == "mechanics/agon/parts/new-proof/mystery"
        and "unexpected payload class" in issue.message
        for issue in issues
    )


def test_mechanic_part_payload_inventory_rejects_unexpected_part_root_file(
    tmp_path: Path,
) -> None:
    write_standard_new_part(tmp_path)
    write_text(
        tmp_path / "mechanics" / "agon" / "parts" / "new-proof" / "payload.json",
        "{}\n",
    )

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(tmp_path)

    assert any(
        issue.location == "mechanics/agon/parts/new-proof/payload.json"
        and "unexpected part-root file" in issue.message
        for issue in issues
    )


def test_mechanic_part_payload_inventory_rejects_empty_payload_dir(
    tmp_path: Path,
) -> None:
    write_standard_new_part(tmp_path, inputs="Local evidence from `fixtures/`.")
    (tmp_path / "mechanics" / "agon" / "parts" / "new-proof" / "fixtures").mkdir(
        parents=True
    )

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(tmp_path)

    assert any(
        issue.location == "mechanics/agon/parts/new-proof/fixtures"
        and "empty payload subdirectory" in issue.message
        for issue in issues
    )


def test_mechanic_part_payload_inventory_rejects_unexplained_thin_part(
    tmp_path: Path,
) -> None:
    write_text(eval_dir_for_test(tmp_path, "aoa-demo") / "EVAL.md", "# Demo\n")
    readme_name = write_standard_new_part(
        tmp_path,
        source_surfaces="- `evals/workflow/aoa-demo/EVAL.md`\n",
        inputs="Bundle-local evidence.",
        outputs="Bundle-local readout.",
        owner_split="Bundles keep source proof meaning; mechanics keeps route support.",
    )

    issues = mechanic_parts_validator.validate_mechanic_part_readme_contract_surfaces(tmp_path)

    assert any(
        issue.location == readme_name
        and "eval-backed thin support route" in issue.message
        for issue in issues
    )
