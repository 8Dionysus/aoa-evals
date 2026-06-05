from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_repo
from validate_repo import run_validation
from validators import generated_route_surfaces
from validators.common import ValidationIssue
from validate_repo_fixtures import eval_dir_for_test, make_eval_bundle, write_catalogs


def copy_repo_text(repo_root: Path, relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)
    destination = repo_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def generated_parity_contracts(repo_root: Path) -> list[ValidationIssue]:
    return [
        ValidationIssue(location, message)
        for location, message in generated_route_surfaces.validate_generated_route_surfaces(repo_root)
    ]


def test_generated_parity_contracts_validate_current_readers() -> None:
    assert generated_parity_contracts(REPO_ROOT) == []


def test_generated_parity_contracts_reject_missing_check_command(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "generated/README.md")
    copy_repo_text(tmp_path, "generated/AGENTS.md")
    copy_repo_text(tmp_path, "docs/README.md")
    for path_name in (
        "docs/decisions/indexes/README.md",
        "docs/decisions/indexes/by-number.md",
        "docs/decisions/indexes/by-date.md",
        "docs/decisions/indexes/by-surface.md",
        "docs/decisions/indexes/by-mechanic.md",
        "docs/decisions/indexes/by-validation-guard.md",
    ):
        copy_repo_text(tmp_path, path_name)
    agents_path = tmp_path / "generated" / "AGENTS.md"
    agents_path.write_text(
        agents_path.read_text(encoding="utf-8").replace(
            "python scripts/generate_eval_report_index.py --check",
            "python scripts/generate_wrong_report_index.py --check",
            1,
        ),
        encoding="utf-8",
    )

    issues = generated_parity_contracts(tmp_path)

    assert any(
        issue.location == "generated/AGENTS.md"
        and "python scripts/generate_eval_report_index.py --check" in issue.message
        for issue in issues
    )


def test_validate_repo_missing_generated_catalogs_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-generated")

    issues = run_validation(tmp_path)

    assert any("file is missing" in issue.message for issue in issues if "generated/" in issue.location)


def test_validate_repo_missing_generated_capsules_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-capsules")
    write_catalogs(tmp_path)

    (tmp_path / "generated" / "eval_capsules.json").unlink()

    issues = run_validation(tmp_path)

    assert any(
        issue.location == "generated/eval_capsules.json" and "file is missing" in issue.message
        for issue in issues
    )


def test_validate_repo_stale_generated_catalogs_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-stale-generated")
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-stale-generated") / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(
        text.replace("Minimal summary for validation.", "Changed without rebuilding catalog.", 1),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "generated catalog is out of date; run 'python scripts/build_catalog.py'" in issue.message
        for issue in issues
    )


def test_validate_repo_stale_generated_capsules_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-stale-capsules")
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-stale-capsules") / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(
        text.replace(
            "under these conditions, the bounded claim holds on this surface.",
            "under these conditions, the bounded claim changed without rebuilding capsules.",
            1,
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "generated capsules are out of date; run 'python scripts/build_catalog.py'" in issue.message
        for issue in issues
    )


def test_targeted_validation_catches_stale_generated_catalog_for_selected_eval(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-stale-generated")
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-targeted-stale-generated") / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(
        text.replace("Minimal summary for validation.", "Changed without rebuilding catalog.", 1),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path, eval_name="aoa-targeted-stale-generated")

    assert any(
        "generated catalog entry for 'aoa-targeted-stale-generated' is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )
    assert any(
        "generated min catalog entry for 'aoa-targeted-stale-generated' is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_targeted_validation_catches_stale_generated_capsule_for_selected_eval(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-stale-capsule")
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-targeted-stale-capsule") / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(
        text.replace(
            "under these conditions, the bounded claim holds on this surface.",
            "under these conditions, the bounded claim drifted after generation.",
            1,
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path, eval_name="aoa-targeted-stale-capsule")

    assert any(
        "generated capsule entry for 'aoa-targeted-stale-capsule' is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_targeted_validation_catches_stale_catalog_metadata(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-metadata-drift")
    write_catalogs(tmp_path)

    full_path = tmp_path / "generated" / "eval_catalog.json"
    min_path = tmp_path / "generated" / "eval_catalog.min.json"
    full_catalog = json.loads(full_path.read_text(encoding="utf-8"))
    min_catalog = json.loads(min_path.read_text(encoding="utf-8"))
    full_catalog["catalog_version"] = 999
    min_catalog["source_of_truth"] = {"broken": True}
    full_path.write_text(json.dumps(full_catalog), encoding="utf-8")
    min_path.write_text(json.dumps(min_catalog), encoding="utf-8")

    issues = run_validation(tmp_path, eval_name="aoa-targeted-metadata-drift")

    assert any(
        "generated catalog metadata is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )
    assert any(
        "generated min catalog metadata is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_capsule_source_section_without_derivable_content(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-capsule-source",
        section_overrides={"Interpretation guidance": ""},
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any(
        "missing capsule source section 'Interpretation guidance'" in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_capsule_catalog_alignment_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-capsule-alignment-drift")
    write_catalogs(tmp_path)

    capsule_path = tmp_path / "generated" / "eval_capsules.json"
    capsules = json.loads(capsule_path.read_text(encoding="utf-8"))
    capsules["evals"] = []
    capsule_path.write_text(json.dumps(capsules), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "capsules are missing eval 'aoa-capsule-alignment-drift' from generated/eval_catalog.json"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_missing_generated_sections(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-sections-surface")
    write_catalogs(tmp_path)
    (tmp_path / "generated" / "eval_sections.full.json").unlink()

    issues = run_validation(tmp_path)

    assert any("file is missing" in issue.message for issue in issues if issue.location.endswith("eval_sections.full.json"))


def test_validate_repo_rejects_stale_generated_sections(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-stale-sections-surface")
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-stale-sections-surface") / "EVAL.md"
    eval_md_path.write_text(
        eval_md_path.read_text(encoding="utf-8").replace(
            "## Adaptation points\n- point\n",
            "## Adaptation points\n- point\n- another point\n",
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "generated sections are out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_section_catalog_alignment_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-section-alignment-drift")
    write_catalogs(tmp_path)

    sections_path = tmp_path / "generated" / "eval_sections.full.json"
    sections = json.loads(sections_path.read_text(encoding="utf-8"))
    sections["evals"][0]["status"] = "promoted"
    sections_path.write_text(json.dumps(sections), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "generated section entry for 'aoa-section-alignment-drift' must align with full catalog field 'status'"
        in issue.message
        for issue in issues
    )


def test_targeted_validation_catches_stale_generated_section_for_selected_eval(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-stale-sections")
    write_catalogs(tmp_path)

    eval_md_path = eval_dir_for_test(tmp_path, "aoa-targeted-stale-sections") / "EVAL.md"
    eval_md_path.write_text(
        eval_md_path.read_text(encoding="utf-8").replace(
            "## Adaptation points\n- point\n",
            "## Adaptation points\n- point\n- another point\n",
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path, eval_name="aoa-targeted-stale-sections")

    assert any(
        "generated section entry for 'aoa-targeted-stale-sections' is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_min_projection_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-min-projection-drift")
    write_catalogs(tmp_path)

    min_path = tmp_path / "generated" / "eval_catalog.min.json"
    min_catalog = json.loads(min_path.read_text(encoding="utf-8"))
    min_catalog["evals"][0]["summary"] = "tampered"
    min_path.write_text(json.dumps(min_catalog), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "min catalog must stay a projection of the full catalog" in issue.message
        for issue in issues
    )


def test_validate_repo_reports_malformed_full_catalog_projection_error(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-malformed-full-catalog")
    write_catalogs(tmp_path)

    full_path = tmp_path / "generated" / "eval_catalog.json"
    full_catalog = json.loads(full_path.read_text(encoding="utf-8"))
    del full_catalog["evals"]
    full_path.write_text(json.dumps(full_catalog), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "generated catalog is malformed; min projection could not be computed" in issue.message
        for issue in issues
    )
