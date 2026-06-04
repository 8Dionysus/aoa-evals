from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_repo
from validate_repo import run_validation
from validators import eval_bundles as eval_bundles_validator
from validate_repo_fixtures import make_eval_bundle, make_index, make_roadmap, make_selection, write_catalogs


DIRECTION_ANCHORS = (
    "docs/architecture/AGENT_INDEX.md",
    "docs/architecture/PROOF_TOPOLOGY.md",
    "docs/architecture/LEGACY_NAMING.md",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "mechanics/proof-loop/README.md",
    "generated/README.md",
    "mechanics/publication-receipts/README.md",
    "mechanics/release-support/README.md",
)


DETAILED_EVIDENCE_ANCHORS = (
    "evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json",
    "mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json",
    "mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json",
    "mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json",
    "mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json",
)

DOCS_ROUTE_TOKENS = (
    "architecture/AGENT_INDEX.md",
    "architecture/PROOF_TOPOLOGY.md",
    "architecture/ROUTE_RESIDUE_GUARDS.md",
    "guides/EVAL_REVIEW_GUIDE.md",
    "operations/RELEASING.md",
    "decisions/README.md",
    "generated/eval_report_index.min.json",
    "generated/comparison_spine.json",
)


def test_validate_repo_requires_roadmap_current_public_surface_to_be_a_starter_bundle(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-alpha")
    make_eval_bundle(tmp_path, name="aoa-beta")
    make_index(tmp_path, "aoa-alpha", "workflow")
    make_selection(tmp_path, ["aoa-alpha"])
    make_roadmap(tmp_path, ["aoa-beta"])
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("roadmap 'Current public surface' eval 'aoa-beta' must appear in EVAL_INDEX.md starter bundles" in issue.message for issue in issues)


def test_validate_roadmap_parity_rejects_generic_heading(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    roadmap_path = tmp_path / "ROADMAP.md"
    roadmap_path.write_text(
        roadmap_path.read_text(encoding="utf-8").replace(
            "# Proof Direction Roadmap",
            "# Roadmap",
            1,
        ),
        encoding="utf-8",
    )
    write_catalogs(tmp_path)

    issues = eval_bundles_validator.validate_roadmap_parity(
        tmp_path,
        starter_names=["aoa-starter-alpha"],
    )

    assert any(
        issue.location == "ROADMAP.md"
        and "# Proof Direction Roadmap" in issue.message
        for issue in issues
    )


def test_validate_roadmap_parity_rejects_missing_update_rule(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    roadmap_path = tmp_path / "ROADMAP.md"
    roadmap_path.write_text(
        roadmap_path.read_text(encoding="utf-8").replace(
            "## Update Rule",
            "## Local Log",
            1,
        ),
        encoding="utf-8",
    )
    write_catalogs(tmp_path)

    issues = eval_bundles_validator.validate_roadmap_parity(
        tmp_path,
        starter_names=["aoa-starter-alpha"],
    )

    assert any(
        issue.location == "ROADMAP.md"
        and "## Update Rule" in issue.message
        for issue in issues
    )


def test_validate_roadmap_parity_rejects_old_negative_route_scaffold(
    tmp_path: Path,
) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    roadmap_path = tmp_path / "ROADMAP.md"
    roadmap_path.write_text(
        roadmap_path.read_text(encoding="utf-8")
        + "\nkeep the agent index chain visible without making the roadmap an index\n"
        + "grow the active proof loop without strengthening the bounded claim\n",
        encoding="utf-8",
    )

    issues = eval_bundles_validator.validate_roadmap_parity(
        tmp_path,
        ["aoa-starter-alpha"],
    )

    assert any(
        issue.location == "ROADMAP.md"
        and "direction owner routes" in issue.message
        and "without making the roadmap an index" in issue.message
        for issue in issues
    )
    assert any(
        issue.location == "ROADMAP.md"
        and "direction owner routes" in issue.message
        and "without strengthening the bounded claim" in issue.message
        for issue in issues
    )


def test_validate_repo_allows_public_bundle_outside_starter_surface(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_eval_bundle(tmp_path, name="aoa-public-draft")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-starter-alpha") == []
    assert run_validation(tmp_path, eval_name="aoa-public-draft") == []


def test_validate_repo_allows_targeted_non_starter_bundle_validation(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_eval_bundle(tmp_path, name="aoa-public-draft")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-public-draft") == []


def test_validate_eval_index_allows_targeted_non_starter_bundle_selection(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_eval_bundle(tmp_path, name="aoa-public-draft")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    write_catalogs(tmp_path)

    issues = eval_bundles_validator.validate_eval_index(
        tmp_path,
        starter_names=["aoa-starter-alpha"],
        selected_evals={"aoa-public-draft"},
    )

    assert issues == []


def test_validate_repo_requires_absence_note_sync_between_roadmap_and_index(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-absence-note-drift")
    make_roadmap(tmp_path, ["aoa-absence-note-drift"], include_absence_note=False)
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("absence note" in issue.message for issue in issues)


class RoadmapParityTestCase(unittest.TestCase):
    def test_roadmap_keeps_current_directional_public_contour(self) -> None:
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        normalized_readme = " ".join(readme.split())
        normalized_roadmap = " ".join(roadmap.split())

        self.assertIn("Current release: `v0.4.0`", readme)
        self.assertIn("## [0.4.0]", changelog)
        self.assertIn("`v0.4.0`", roadmap)
        self.assertIn("Current Public Contour", roadmap)
        self.assertIn("Direction Anchors", roadmap)
        self.assertIn("release history: [CHANGELOG.md](CHANGELOG.md)", roadmap)
        self.assertIn("source eval bundle corpus", normalized_readme)
        self.assertIn("source eval bundle corpus", normalized_roadmap)
        self.assertIn("proves only bounded claims", normalized_roadmap)
        self.assertIn("Executable commands live in route cards", roadmap)
        self.assertNotRegex(normalized_readme, r"carries \d+ source eval bundles")
        self.assertNotRegex(normalized_roadmap, r"carries \d+ eval bundles")
        self.assertNotIn("grow from a strong public bootstrap", roadmap)
        self.assertNotIn("Current Checked Contour", roadmap)
        self.assertNotIn("It is not the changelog", roadmap)

        for anchor in DIRECTION_ANCHORS:
            with self.subTest(anchor=anchor):
                self.assertTrue((REPO_ROOT / anchor).is_file())
                self.assertIn(anchor, roadmap)

        docs_readme = (REPO_ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        for token in DOCS_ROUTE_TOKENS:
            with self.subTest(docs_route_token=token):
                self.assertIn(token, docs_readme)
        for anchor in DETAILED_EVIDENCE_ANCHORS:
            with self.subTest(detailed_anchor=anchor):
                self.assertTrue((REPO_ROOT / anchor).is_file())

    def test_memo_pilot_surfaces_do_not_overclaim_memory_readiness(self) -> None:
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        eval_index = (REPO_ROOT / "EVAL_INDEX.md").read_text(encoding="utf-8")
        eval_selection = (REPO_ROOT / "EVAL_SELECTION.md").read_text(encoding="utf-8")

        for text in (roadmap, eval_index, eval_selection):
            with self.subTest(surface=text[:20]):
                self.assertIn("future scar", text)
                self.assertIn("retention", text)
                self.assertIn("live memory-ledger readiness", text)

        for relative_path in (
            "evals/workflow/aoa-memo-recall-integrity/EVAL.md",
            "evals/workflow/aoa-memo-contradiction-integrity/EVAL.md",
            "evals/workflow/aoa-memo-writeback-act-integrity/EVAL.md",
        ):
            bundle_text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(bundle=relative_path):
                self.assertIn("future scar or retention readiness", bundle_text)
                self.assertIn("live memory-ledger behavior", bundle_text)


if __name__ == "__main__":
    unittest.main()
