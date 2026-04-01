from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> dict:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


class DownstreamFeedContractsTests(unittest.TestCase):
    def test_expected_downstream_feeds_exist(self) -> None:
        for relative_path in (
            "generated/eval_catalog.min.json",
            "generated/eval_capsules.json",
            "generated/eval_sections.full.json",
            "generated/comparison_spine.json",
        ):
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())

    def test_catalog_capsules_and_sections_share_eval_names(self) -> None:
        catalog = load_json("generated/eval_catalog.min.json")
        capsules = load_json("generated/eval_capsules.json")
        sections = load_json("generated/eval_sections.full.json")

        expected_names = [entry["name"] for entry in catalog["evals"]]

        self.assertEqual(catalog["catalog_version"], 1)
        self.assertEqual(capsules["capsule_version"], 1)
        self.assertEqual(sections["section_version"], 1)
        self.assertEqual(
            catalog["source_of_truth"],
            {
                "eval_manifest": "bundles/*/eval.yaml",
                "eval_markdown": "bundles/*/EVAL.md",
            },
        )
        self.assertEqual(
            capsules["source_of_truth"],
            {
                "eval_catalog": "generated/eval_catalog.json",
                "eval_markdown": "bundles/*/EVAL.md",
            },
        )
        self.assertEqual(sections["source_of_truth"]["eval_markdown"], "bundles/*/EVAL.md")
        self.assertIn("sections", sections["source_of_truth"])
        self.assertEqual(expected_names, [entry["name"] for entry in capsules["evals"]])
        self.assertEqual(expected_names, [entry["name"] for entry in sections["evals"]])

    def test_comparison_spine_tracks_only_non_none_baseline_evals(self) -> None:
        catalog = load_json("generated/eval_catalog.min.json")
        comparison_spine = load_json("generated/comparison_spine.json")

        expected_names = sorted(
            entry["name"] for entry in catalog["evals"] if entry["baseline_mode"] != "none"
        )
        actual_names = sorted(entry["name"] for entry in comparison_spine["evals"])

        self.assertEqual(comparison_spine["comparison_spine_version"], 1)
        self.assertEqual(
            comparison_spine["source_of_truth"],
            {
                "eval_catalog": "generated/eval_catalog.json",
                "eval_manifest": "bundles/*/eval.yaml",
                "eval_markdown": "bundles/*/EVAL.md",
            },
        )
        self.assertEqual(actual_names, expected_names)
        for entry in comparison_spine["evals"]:
            self.assertIn("comparison_surface", entry)
            self.assertIn("proof_artifacts", entry)
            self.assertIn("selection_summary", entry)


if __name__ == "__main__":
    unittest.main()
