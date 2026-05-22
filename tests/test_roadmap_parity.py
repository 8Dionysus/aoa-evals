from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


DIRECTION_ANCHORS = (
    "docs/AGENT_INDEX.md",
    "docs/PROOF_TOPOLOGY.md",
    "docs/LEGACY_NAMING.md",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json",
    "mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json",
    "mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json",
    "mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json",
    "mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json",
)


class RoadmapParityTestCase(unittest.TestCase):
    def test_roadmap_keeps_current_directional_public_contour(self) -> None:
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        normalized_roadmap = " ".join(roadmap.split())

        self.assertIn("Current release: `v0.3.3`", readme)
        self.assertIn("## [0.3.3]", changelog)
        self.assertIn("`v0.3.3`", roadmap)
        self.assertIn("Current Public Contour", roadmap)
        self.assertIn("Direction Anchors", roadmap)
        self.assertIn("release history: [CHANGELOG.md](CHANGELOG.md)", roadmap)
        self.assertIn("proves only bounded claims", normalized_roadmap)
        self.assertIn("Executable commands live in route cards", roadmap)
        self.assertNotIn("grow from a strong public bootstrap", roadmap)
        self.assertNotIn("Current Checked Contour", roadmap)
        self.assertNotIn("It is not the changelog", roadmap)

        for anchor in DIRECTION_ANCHORS:
            with self.subTest(anchor=anchor):
                self.assertTrue((REPO_ROOT / anchor).is_file())
                self.assertIn(anchor, roadmap)

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
