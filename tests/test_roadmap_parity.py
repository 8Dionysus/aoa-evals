from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


CURRENT_RELEASE_SURFACES = (
    "bundles/aoa-continuity-anchor-integrity/EVAL.md",
    "bundles/aoa-reflective-revision-boundedness/EVAL.md",
    "bundles/aoa-self-reanchor-correctness/EVAL.md",
    "bundles/aoa-candidate-lineage-integrity/EVAL.md",
    "bundles/aoa-diagnosis-cause-discipline/EVAL.md",
    "bundles/aoa-repair-boundedness/EVAL.md",
    "generated/eval_catalog.min.json",
    "generated/eval_capsules.json",
    "generated/eval_sections.full.json",
    "generated/runtime_candidate_template_index.min.json",
    "generated/runtime_candidate_intake.min.json",
    "generated/phase_alpha_eval_matrix.min.json",
    "docs/PROGRESSION_EVIDENCE_MODEL.md",
    "docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md",
    "docs/RECURRENCE_PROOF_PROGRAM.md",
    "docs/TRACE_EVAL_BRIDGE.md",
    "docs/EVAL_RESULT_RECEIPT_GUIDE.md",
    "docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
)


class RoadmapParityTestCase(unittest.TestCase):
    def test_roadmap_matches_current_v0_3_1_release_contour(self) -> None:
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        normalized_roadmap = " ".join(roadmap.split())

        self.assertIn("Current release: `v0.3.1`", readme)
        self.assertIn("## [0.3.1]", changelog)
        self.assertIn("`v0.3.1`", roadmap)
        self.assertIn("Current release contour", roadmap)
        self.assertIn("Roadmap drift", roadmap)
        self.assertIn("proves only bounded claims", normalized_roadmap)
        self.assertIn("not a claim that", roadmap)
        self.assertNotIn("grow from a strong public bootstrap", roadmap)

        for surface in CURRENT_RELEASE_SURFACES:
            with self.subTest(surface=surface):
                self.assertTrue((REPO_ROOT / surface).is_file())
                self.assertIn(surface, roadmap)


if __name__ == "__main__":
    unittest.main()
