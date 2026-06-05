from __future__ import annotations

import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validators import proof_object_route_paths as proof_object_paths_validator
from validators import proof_object_routes as proof_object_routes_validator
from validators import root_context
from validators import root_eval_guides as root_eval_guides_validator
from validators import root_release_guidance as root_release_guidance_validator
from validators import root_route_cards as root_route_cards_validator
from validators import root_topology as root_topology_validator
from validators import route_residue_active_mechanics as route_residue_active_mechanics_validator
from validators import route_residue_decisions as route_residue_decisions_validator
from validators import route_residue_mechanic_payload as route_residue_mechanic_payload_validator
from validators import route_residue_repo_config as route_residue_repo_config_validator
from validators import route_residue_root_authored as route_residue_root_authored_validator
from validators import route_residue_source_bundle as route_residue_source_bundle_validator


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


def copy_root_route_card_surface(repo_root: Path) -> None:
    for district_name, allowed_names in root_route_cards_validator.ROOT_ROUTE_CARD_ONLY_DISTRICTS.items():
        for allowed_name in allowed_names:
            copy_repo_text(repo_root, f"{district_name}/{allowed_name}")
    for path_name in (
        root_route_cards_validator.ROOT_ROUTE_CARD_GUARD_DECISION_NAME,
        "docs/decisions/README.md",
        root_context.PROOF_TOPOLOGY_NAME,
    ):
        copy_repo_text(repo_root, path_name)


def validate_root_route_card_districts(repo_root: Path):
    return root_route_cards_validator.validate_root_route_card_districts(
        repo_root,
        context=root_topology_validator.root_route_card_context(),
    )


def test_eval_philosophy_route_map_validates_current_route() -> None:
    assert root_eval_guides_validator.validate_eval_philosophy_route_map_surface(REPO_ROOT) == []


def test_eval_philosophy_route_map_rejects_flat_negative_slogan(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "docs/guides/EVAL_PHILOSOPHY.md")
    philosophy_path = tmp_path / "docs" / "guides" / "EVAL_PHILOSOPHY.md"
    philosophy_path.write_text(
        philosophy_path.read_text(encoding="utf-8")
        + "\nNeither fact alone proves quality.\n",
        encoding="utf-8",
    )

    issues = root_eval_guides_validator.validate_eval_philosophy_route_map_surface(tmp_path)

    assert any(
        issue.location == "docs/guides/EVAL_PHILOSOPHY.md"
        and "positive distinctions" in issue.message
        and "Neither fact alone proves quality." in issue.message
        for issue in issues
    )


def test_releasing_route_map_surface_validates_current_route() -> None:
    assert root_release_guidance_validator.validate_releasing_route_map_surface(REPO_ROOT) == []


def test_releasing_route_map_surface_rejects_status_ledger_wording(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, "docs/operations/RELEASING.md")
    releasing = tmp_path / "docs" / "operations" / "RELEASING.md"
    releasing.write_text(
        releasing.read_text(encoding="utf-8")
        + "\nThis readiness audit is not a branch, commit, push, PR, or tag.\n",
        encoding="utf-8",
    )

    issues = root_release_guidance_validator.validate_releasing_route_map_surface(tmp_path)

    assert any(
        issue.location == "docs/operations/RELEASING.md"
        and "live-status owners" in issue.message
        and "not a branch" in issue.message
        for issue in issues
    )


def test_proof_object_parts_route_validates_current_operating_card() -> None:
    assert proof_object_routes_validator.validate_proof_object_parts_route_surface(REPO_ROOT) == []


def test_proof_object_parts_route_rejects_stale_negative_boundary_scaffold(
    tmp_path: Path,
) -> None:
    copy_repo_text(tmp_path, proof_object_paths_validator.PROOF_OBJECT_PARTS_README_NAME)
    parts_path = tmp_path / proof_object_paths_validator.PROOF_OBJECT_PARTS_README_NAME
    parts_path.write_text(
        parts_path.read_text(encoding="utf-8")
        + "\nThey do not own source eval meaning and do not replace generated readers.\n",
        encoding="utf-8",
    )

    issues = proof_object_routes_validator.validate_proof_object_parts_route_surface(tmp_path)

    assert any(
        issue.location == proof_object_paths_validator.PROOF_OBJECT_PARTS_README_NAME
        and "positive operating card" in issue.message
        for issue in issues
    )


def test_root_route_card_districts_validate_current_routes() -> None:
    assert validate_root_route_card_districts(REPO_ROOT) == []


def test_root_route_card_districts_cover_expected_roots() -> None:
    assert set(root_route_cards_validator.ROOT_ROUTE_CARD_ONLY_DISTRICTS) == {
        "config",
        "examples",
        "fixtures",
        "manifests",
        "reports",
        "runners",
        "schemas",
        "scorers",
        "templates",
    }


def test_root_route_card_districts_reject_active_payload(tmp_path: Path) -> None:
    copy_root_route_card_surface(tmp_path)
    for district_name in root_route_cards_validator.ROOT_ROUTE_CARD_ONLY_DISTRICTS:
        write_text(tmp_path / district_name / "stray" / "payload.txt", "stray\n")

    issues = validate_root_route_card_districts(tmp_path)

    for district_name in root_route_cards_validator.ROOT_ROUTE_CARD_ONLY_DISTRICTS:
        assert any(
            issue.location == f"{district_name}/stray/payload.txt"
            and "route-card-only root district" in issue.message
            for issue in issues
        )


def test_root_route_card_districts_reject_stray_empty_directory(
    tmp_path: Path,
) -> None:
    copy_root_route_card_surface(tmp_path)
    stray_path = tmp_path / "manifests" / "recurrence" / "hooks"
    stray_path.mkdir(parents=True)

    issues = validate_root_route_card_districts(tmp_path)

    assert any(
        issue.location == "manifests/recurrence"
        and "stray directory" in issue.message
        for issue in issues
    )


def test_root_route_card_districts_reject_unclear_readme_heading(
    tmp_path: Path,
) -> None:
    copy_root_route_card_surface(tmp_path)
    fixtures_readme = tmp_path / "fixtures" / "README.md"
    fixtures_readme.write_text(
        fixtures_readme.read_text(encoding="utf-8").replace(
            "# Fixtures Route",
            "# Shared Fixtures",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_root_route_card_districts(tmp_path)

    assert any(
        issue.location == "fixtures/README.md"
        and "must name itself as a Route surface" in issue.message
        for issue in issues
    )


def test_root_route_card_districts_reject_readme_operational_discipline(
    tmp_path: Path,
) -> None:
    copy_root_route_card_surface(tmp_path)
    runners_readme = tmp_path / "runners" / "README.md"
    runners_readme.write_text(
        runners_readme.read_text(encoding="utf-8")
        + "\nDo not recreate active root runner payloads here.\n",
        encoding="utf-8",
    )

    issues = validate_root_route_card_districts(tmp_path)

    assert any(
        issue.location == "runners/README.md"
        and "operational discipline in AGENTS.md" in issue.message
        for issue in issues
    )


def test_reports_route_card_requires_source_strength_route(
    tmp_path: Path,
) -> None:
    copy_root_route_card_surface(tmp_path)
    reports_readme = tmp_path / "reports" / "README.md"
    reports_readme.write_text(
        reports_readme.read_text(encoding="utf-8").replace(
            "eval-claim strength stays with source bundles and reviewed reports",
            "handoff route is unclear",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_root_route_card_districts(tmp_path)

    assert any(
        issue.location == "reports/README.md"
        and "eval-claim strength stays with source bundles and reviewed reports"
        in issue.message
        for issue in issues
    )


def test_active_mechanic_route_residue_validates_current_route_cards() -> None:
    assert route_residue_active_mechanics_validator.validate_active_mechanic_route_residue(REPO_ROOT) == []


def test_active_mechanic_route_residue_rejects_root_payload_reference(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / "mechanics" / "proof-infra" / "README.md",
        "# Proof Infra\n\nUse `fixtures/old-family/README.md` as active input.\n",
    )

    issues = route_residue_active_mechanics_validator.validate_active_mechanic_route_residue(tmp_path)

    assert any(
        issue.location == "mechanics/proof-infra/README.md:3"
        and "route-card-only root district payload 'fixtures/old-family/README.md'"
        in issue.message
        for issue in issues
    )


def test_active_mechanic_route_residue_allows_root_route_card_reference(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / "mechanics" / "proof-infra" / "README.md",
        "# Proof Infra\n\nSee root route card `fixtures/README.md`.\n",
    )

    assert route_residue_active_mechanics_validator.validate_active_mechanic_route_residue(tmp_path) == []


def test_active_mechanic_route_residue_allows_same_part_root_reference(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path
        / "mechanics"
        / "audit"
        / "parts"
        / "artifact-verdict-hooks"
        / "examples"
        / "hook.example.json",
        "{}",
    )
    write_text(
        tmp_path
        / "mechanics"
        / "audit"
        / "parts"
        / "artifact-verdict-hooks"
        / "README.md",
        "# Artifact Verdict Hooks\n\nUse `examples/hook.example.json` locally.\n",
    )

    assert route_residue_active_mechanics_validator.validate_active_mechanic_route_residue(tmp_path) == []


def test_active_mechanic_route_residue_rejects_legacy_parent_route(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / "mechanics" / "titan" / "README.md",
        "# Titan\n\nDo not route through `mechanics/titan-canaries/README.md`.\n",
    )

    issues = route_residue_active_mechanics_validator.validate_active_mechanic_route_residue(tmp_path)

    assert any(
        issue.location == "mechanics/titan/README.md:3"
        and "not legacy parent route `mechanics/titan-canaries/`" in issue.message
        for issue in issues
    )


def test_root_authored_route_residue_validates_current_route_cards() -> None:
    assert route_residue_root_authored_validator.validate_root_authored_route_residue(REPO_ROOT) == []


def test_root_authored_route_residue_rejects_root_payload_reference(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / "AUDIT.md",
        "# Audit\n\nRead `reports/summary.schema.json` before review.\n",
    )

    issues = route_residue_root_authored_validator.validate_root_authored_route_residue(tmp_path)

    assert any(
        issue.location == "AUDIT.md:3"
        and "route-card-only root district payload 'reports/summary.schema.json'"
        in issue.message
        for issue in issues
    )


def test_root_authored_route_residue_allows_bundle_local_reference(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / "AUDIT.md",
        "# Audit\n\nRead `evals/workflow/aoa-demo/reports/summary.schema.json`.\n",
    )

    assert route_residue_root_authored_validator.validate_root_authored_route_residue(tmp_path) == []


def test_root_authored_route_residue_allows_root_route_card_reference(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / "docs" / "operations" / "RELEASING.md",
        "# Releasing\n\nRead route card `reports/README.md`.\n",
    )

    assert route_residue_root_authored_validator.validate_root_authored_route_residue(tmp_path) == []


def test_root_authored_route_residue_allows_historical_context(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / "docs" / "architecture" / "LEGACY_NAMING.md",
        "# Legacy\n\nFormer root paths `reports/old.json` are mapped through provenance.\n",
    )

    assert route_residue_root_authored_validator.validate_root_authored_route_residue(tmp_path) == []


def test_decision_route_residue_validates_current_decisions() -> None:
    assert route_residue_decisions_validator.validate_decision_route_residue(REPO_ROOT) == []


def test_decision_route_residue_rejects_unmarked_root_payload_reference(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / "docs" / "decisions" / "AOA-EV-D-0099-bad-route.md",
        "# Bad Route\n\nUse `reports/summary.schema.json` as the active schema.\n",
    )

    issues = route_residue_decisions_validator.validate_decision_route_residue(tmp_path)

    assert any(
        issue.location == "docs/decisions/AOA-EV-D-0099-bad-route.md:3"
        and "route-card-only root district payload 'reports/summary.schema.json'"
        in issue.message
        for issue in issues
    )


def test_decision_route_residue_allows_historical_root_payload_reference(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / "docs" / "decisions" / "AOA-EV-D-0099-former-route.md",
        "# Former Route\n\nFormer root `reports/summary.schema.json` moved behind provenance.\n",
    )

    assert route_residue_decisions_validator.validate_decision_route_residue(tmp_path) == []


def test_decision_route_residue_allows_bundle_local_reference(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / "docs" / "decisions" / "0099-bundle-route.md",
        "# Bundle Route\n\nUse `evals/workflow/aoa-demo/reports/summary.schema.json`.\n",
    )

    assert route_residue_decisions_validator.validate_decision_route_residue(tmp_path) == []


def test_decision_route_residue_allows_root_route_card_reference(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / "docs" / "decisions" / "0099-route-card.md",
        "# Route Card\n\nRead route card `reports/README.md`.\n",
    )

    assert route_residue_decisions_validator.validate_decision_route_residue(tmp_path) == []


def test_repo_config_route_residue_validates_current_config() -> None:
    assert route_residue_repo_config_validator.validate_repo_config_route_residue(REPO_ROOT) == []


def test_repo_config_route_residue_rejects_legacy_parent_reference(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / ".gitignore",
        "seeds/\n!mechanics/titan-canaries/seeds/\n",
    )

    issues = route_residue_repo_config_validator.validate_repo_config_route_residue(tmp_path)

    assert any(
        issue.location == ".gitignore:2"
        and "legacy mechanic parent `mechanics/titan-canaries/`" in issue.message
        for issue in issues
    )


def test_repo_config_route_residue_rejects_root_payload_reference(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / ".github" / "workflows" / "bad.yml",
        "name: bad\n# uses reports/summary.schema.json\n",
    )

    issues = route_residue_repo_config_validator.validate_repo_config_route_residue(tmp_path)

    assert any(
        issue.location == ".github/workflows/bad.yml:2"
        and "route-card-only root district payload 'reports/summary.schema.json'"
        in issue.message
        for issue in issues
    )


def test_repo_config_route_residue_allows_current_seed_boundary_unignore(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path / ".gitignore",
        "seeds/\n!mechanics/titan/parts/seed-boundary/seeds/\n",
    )

    assert route_residue_repo_config_validator.validate_repo_config_route_residue(tmp_path) == []


def test_source_bundle_route_residue_validates_current_bundles() -> None:
    assert route_residue_source_bundle_validator.validate_source_bundle_route_residue(REPO_ROOT) == []


def test_source_bundle_route_residue_rejects_unqualified_external_path(
    tmp_path: Path,
) -> None:
    write_text(
        eval_dir_for_test(tmp_path, "aoa-demo") / "EVAL.md",
        "# Demo\n\nRead `examples/a2a/external.fixture.json` from aoa-sdk.\n",
    )

    issues = route_residue_source_bundle_validator.validate_source_bundle_route_residue(tmp_path)

    assert any(
        issue.location == "evals/workflow/aoa-demo/EVAL.md:3"
        and "route-card-only root district payload 'examples/a2a/external.fixture.json'"
        in issue.message
        for issue in issues
    )


def test_source_bundle_route_residue_rejects_legacy_parent_reference(
    tmp_path: Path,
) -> None:
    write_text(
        eval_dir_for_test(tmp_path, "aoa-demo") / "EVAL.md",
        "# Demo\n\nUse `mechanics/agon-proof/README.md` as the owner.\n",
    )

    issues = route_residue_source_bundle_validator.validate_source_bundle_route_residue(tmp_path)

    assert any(
        issue.location == "evals/workflow/aoa-demo/EVAL.md:3"
        and "legacy mechanic parent `mechanics/agon-proof/`" in issue.message
        for issue in issues
    )


def test_source_bundle_route_residue_allows_bundle_local_path(
    tmp_path: Path,
) -> None:
    write_text(
        eval_dir_for_test(tmp_path, "aoa-demo") / "fixtures" / "contract.json",
        "{}",
    )
    write_text(
        eval_dir_for_test(tmp_path, "aoa-demo") / "EVAL.md",
        "# Demo\n\nUse `fixtures/contract.json` as this bundle's local fixture contract.\n",
    )

    assert route_residue_source_bundle_validator.validate_source_bundle_route_residue(tmp_path) == []


def test_source_bundle_route_residue_allows_repo_qualified_sibling_path(
    tmp_path: Path,
) -> None:
    write_text(
        eval_dir_for_test(tmp_path, "aoa-demo") / "EVAL.md",
        "# Demo\n\nUse `repo:aoa-sdk/examples/a2a/external.fixture.json` as sibling evidence.\n",
    )

    assert route_residue_source_bundle_validator.validate_source_bundle_route_residue(tmp_path) == []


def test_mechanic_payload_route_residue_validates_current_payloads() -> None:
    assert route_residue_mechanic_payload_validator.validate_mechanic_payload_route_residue(REPO_ROOT) == []


def test_mechanic_payload_route_residue_rejects_unqualified_external_path(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path
        / "mechanics"
        / "recurrence"
        / "parts"
        / "recursor-boundary"
        / "fixtures"
        / "case.json",
        '{\n  "must_not_modify": [\n    "config/codex_subagent_wiring.v2.json"\n  ]\n}\n',
    )

    issues = route_residue_mechanic_payload_validator.validate_mechanic_payload_route_residue(tmp_path)

    assert any(
        issue.location
        == "mechanics/recurrence/parts/recursor-boundary/fixtures/case.json:3"
        and "route-card-only root district payload 'config/codex_subagent_wiring.v2.json'"
        in issue.message
        for issue in issues
    )


def test_mechanic_payload_route_residue_allows_part_local_path(
    tmp_path: Path,
) -> None:
    part_root = (
        tmp_path / "mechanics" / "recurrence" / "parts" / "recursor-boundary"
    )
    write_text(part_root / "config" / "local.json", "{}")
    write_text(
        part_root / "fixtures" / "case.json",
        '{\n  "local_config": "config/local.json"\n}\n',
    )

    assert route_residue_mechanic_payload_validator.validate_mechanic_payload_route_residue(tmp_path) == []


def test_mechanic_payload_route_residue_allows_repo_qualified_sibling_path(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path
        / "mechanics"
        / "recurrence"
        / "parts"
        / "recursor-boundary"
        / "fixtures"
        / "case.json",
        '{\n  "source": "repo:aoa-agents/config/codex_subagent_wiring.v2.json"\n}\n',
    )

    assert route_residue_mechanic_payload_validator.validate_mechanic_payload_route_residue(tmp_path) == []


def test_mechanic_payload_route_residue_rejects_legacy_parent_route(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path
        / "mechanics"
        / "recurrence"
        / "parts"
        / "recursor-boundary"
        / "fixtures"
        / "case.json",
        '{\n  "owner": "mechanics/titan-canaries/seeds/titan_runtime_roster_canary.yaml"\n}\n',
    )

    issues = route_residue_mechanic_payload_validator.validate_mechanic_payload_route_residue(tmp_path)

    assert any(
        issue.location
        == "mechanics/recurrence/parts/recursor-boundary/fixtures/case.json:2"
        and "legacy mechanic parent `mechanics/titan-canaries/`" in issue.message
        for issue in issues
    )
