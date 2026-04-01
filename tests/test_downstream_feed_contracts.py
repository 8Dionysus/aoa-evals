from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module(script_name: str):
    path = REPO_ROOT / "scripts" / script_name
    spec = importlib.util.spec_from_file_location(script_name.replace(".py", ""), path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runtime_template_index_builder = load_module("generate_runtime_candidate_template_index.py")


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

    def test_runtime_candidate_template_index_is_generator_backed_and_complete(self) -> None:
        current = load_json("generated/runtime_candidate_template_index.min.json")
        expected = runtime_template_index_builder.build_runtime_candidate_template_index_payload()

        self.assertEqual(current, expected)
        self.assertEqual(
            set(current.keys()),
            {"schema_version", "layer", "source_of_truth", "templates"},
        )
        self.assertEqual(current["schema_version"], 1)
        self.assertEqual(current["layer"], "aoa-evals")

        by_name = {
            (entry["template_kind"], entry["template_name"]): entry
            for entry in current["templates"]
        }
        workhorse = by_name[("runtime_evidence_selection", "workhorse-q4-vs-q6-latency-tradeoff")]
        self.assertIsNone(workhorse["playbook_id"])
        self.assertIsNone(workhorse["eval_anchor"])
        self.assertIsNone(workhorse["verdict_bundle_ref"])
        self.assertEqual(
            workhorse["required_runtime_artifacts"],
            ["summary", "environment-note", "comparison-note"],
        )

        checkpoint_hook = by_name[("artifact_to_verdict_hook", "aoa-p-0006-approval-boundary-hook")]
        self.assertEqual(checkpoint_hook["playbook_id"], "AOA-P-0006")
        self.assertEqual(checkpoint_hook["eval_anchor"], "aoa-approval-boundary-adherence")
        self.assertTrue(checkpoint_hook["review_required"])
        for entry in current["templates"]:
            self.assertEqual(
                entry["required_runtime_artifacts"],
                list(dict.fromkeys(entry["required_runtime_artifacts"])),
            )
            self.assertTrue(entry["source_example_ref"].startswith("examples/"))
            self.assertTrue(
                all(
                    runtime_artifact
                    and runtime_artifact == runtime_artifact.lower()
                    and " " not in runtime_artifact
                    for runtime_artifact in entry["required_runtime_artifacts"]
                )
            )


if __name__ == "__main__":
    unittest.main()
