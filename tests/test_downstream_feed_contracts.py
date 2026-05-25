from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
RUNTIME_CANDIDATE_READERS_SCRIPTS_DIR = (
    REPO_ROOT / "mechanics" / "audit" / "parts" / "candidate-readers" / "scripts"
)
PHASE_ALPHA_EVAL_MATRIX_SCRIPTS_DIR = (
    REPO_ROOT
    / "mechanics"
    / "boundary-bridge"
    / "parts"
    / "phase-alpha-eval-matrix"
    / "scripts"
)
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_repo import (
    build_catalog_payloads,
    build_comparison_spine_payload,
    collect_catalog_records,
)


def load_module(script_name: str):
    package_scripts = {
        "generate_runtime_candidate_template_index.py": RUNTIME_CANDIDATE_READERS_SCRIPTS_DIR / script_name,
        "generate_runtime_candidate_intake.py": RUNTIME_CANDIDATE_READERS_SCRIPTS_DIR / script_name,
        "generate_phase_alpha_eval_matrix.py": PHASE_ALPHA_EVAL_MATRIX_SCRIPTS_DIR / script_name,
    }
    path = package_scripts.get(script_name, SCRIPTS_DIR / script_name)
    spec = importlib.util.spec_from_file_location(script_name.replace(".py", ""), path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runtime_template_index_builder = load_module("generate_runtime_candidate_template_index.py")
runtime_candidate_intake_builder = load_module("generate_runtime_candidate_intake.py")
eval_report_index_builder = load_module("generate_eval_report_index.py")
phase_alpha_eval_matrix_builder = load_module("generate_phase_alpha_eval_matrix.py")


def load_json(relative_path: str) -> dict:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


class DownstreamFeedContractsTests(unittest.TestCase):
    def test_expected_downstream_feeds_exist(self) -> None:
        for relative_path in (
            "generated/eval_catalog.min.json",
            "generated/eval_capsules.json",
            "generated/eval_sections.full.json",
            "generated/comparison_spine.json",
            "generated/eval_report_index.min.json",
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
                "eval_manifest": "evals/**/eval.yaml",
                "eval_markdown": "evals/**/EVAL.md",
            },
        )
        self.assertEqual(
            capsules["source_of_truth"],
            {
                "eval_catalog": "generated/eval_catalog.json",
                "eval_markdown": "evals/**/EVAL.md",
            },
        )
        self.assertEqual(sections["source_of_truth"]["eval_markdown"], "evals/**/EVAL.md")
        self.assertIn("sections", sections["source_of_truth"])
        self.assertEqual(expected_names, [entry["name"] for entry in capsules["evals"]])
        self.assertEqual(expected_names, [entry["name"] for entry in sections["evals"]])
        first_catalog_entry = catalog["evals"][0]
        first_capsule_entry = capsules["evals"][0]
        for key in ("technique_refs", "skill_refs", "evidence_kinds", "proof_surface_kinds"):
            self.assertIn(key, first_catalog_entry)
            self.assertIn(key, first_capsule_entry)

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
                "eval_manifest": "evals/**/eval.yaml",
                "eval_markdown": "evals/**/EVAL.md",
            },
        )
        self.assertEqual(actual_names, expected_names)
        for entry in comparison_spine["evals"]:
            self.assertIn("comparison_surface", entry)
            self.assertIn("proof_artifacts", entry)
            self.assertIn("selection_summary", entry)
            self.assertIn("interpretation_boundary", entry)

    def test_generated_comparison_spine_is_generator_backed_and_keeps_public_reading_fields(self) -> None:
        issues, records = collect_catalog_records(REPO_ROOT)

        self.assertEqual(issues, [])
        full_catalog, _min_catalog = build_catalog_payloads(REPO_ROOT, records)
        expected = build_comparison_spine_payload(REPO_ROOT, records, full_catalog)
        current = load_json("generated/comparison_spine.json")

        self.assertEqual(current, expected)
        for entry in current["evals"]:
            self.assertTrue(entry["selection_summary"])
            self.assertTrue(entry["interpretation_boundary"])

    def test_runtime_candidate_template_index_is_generator_backed_and_complete(self) -> None:
        current = load_json("mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json")
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
        memo_writeback = by_name[("runtime_evidence_selection", "phase-alpha-memo-writeback-act-v1")]
        self.assertEqual(memo_writeback["eval_anchor"], "aoa-memo-writeback-act-integrity")
        self.assertEqual(
            memo_writeback["required_runtime_artifacts"],
            ["summary", "case-breakdown", "environment-note", "integrity-sidecar"],
        )
        chaos_window = by_name[("runtime_evidence_selection", "runtime-chaos-window")]
        self.assertEqual(chaos_window["eval_anchor"], "aoa-stress-recovery-window")
        self.assertEqual(
            chaos_window["required_runtime_artifacts"],
            ["summary", "case-breakdown", "environment-note", "integrity-sidecar"],
        )

        checkpoint_hook = by_name[("artifact_to_verdict_hook", "aoa-p-0006-approval-boundary-hook")]
        self.assertEqual(checkpoint_hook["playbook_id"], "AOA-P-0006")
        self.assertEqual(checkpoint_hook["eval_anchor"], "aoa-approval-boundary-adherence")
        self.assertTrue(checkpoint_hook["review_required"])
        chaos_hook = by_name[("artifact_to_verdict_hook", "trace-integrity-chaos")]
        self.assertEqual(chaos_hook["playbook_id"], "AOA-P-0032")
        self.assertEqual(chaos_hook["eval_anchor"], "aoa-witness-trace-integrity")
        self.assertTrue(chaos_hook["review_required"])
        for entry in current["templates"]:
            self.assertEqual(
                entry["required_runtime_artifacts"],
                list(dict.fromkeys(entry["required_runtime_artifacts"])),
            )
            self.assertTrue(
                entry["source_example_ref"].startswith(
                    (
                        "mechanics/audit/parts/",
                        "mechanics/checkpoint/parts/",
                    )
                )
            )
            self.assertTrue(
                all(
                    runtime_artifact
                    and runtime_artifact == runtime_artifact.lower()
                    and " " not in runtime_artifact
                    for runtime_artifact in entry["required_runtime_artifacts"]
                )
            )

    def test_runtime_candidate_intake_is_generator_backed_and_keeps_review_refs(self) -> None:
        current = load_json("mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json")
        expected = runtime_candidate_intake_builder.build_runtime_candidate_intake_payload()

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
        self.assertEqual(workhorse["review_guide_ref"], "mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md")
        self.assertEqual(
            workhorse["owner_review_refs"],
            [
                "mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
                "docs/guides/EVAL_REVIEW_GUIDE.md",
                "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.workhorse-local.example.json",
            ],
        )
        hook = by_name[("artifact_to_verdict_hook", "aoa-p-0006-approval-boundary-hook")]
        self.assertEqual(hook["review_guide_ref"], "mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md")
        self.assertEqual(hook["candidate_acceptance_posture"], "candidate_until_eval_review")
        memo_writeback = by_name[("runtime_evidence_selection", "phase-alpha-memo-writeback-act-v1")]
        self.assertEqual(memo_writeback["review_guide_ref"], "mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md")
        self.assertIn(
            "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.phase-alpha-memo-writeback-act.example.json",
            memo_writeback["owner_review_refs"],
        )
        chaos_window = by_name[("runtime_evidence_selection", "runtime-chaos-window")]
        self.assertIn(
            "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.runtime-chaos-window.example.json",
            chaos_window["owner_review_refs"],
        )
        chaos_hook = by_name[("artifact_to_verdict_hook", "trace-integrity-chaos")]
        self.assertEqual(chaos_hook["review_guide_ref"], "mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md")
        self.assertIn(
            "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.trace-integrity-chaos.example.json",
            chaos_hook["owner_review_refs"],
        )

    def test_eval_report_index_is_generator_backed_and_keeps_reports_subordinate(self) -> None:
        current = load_json("generated/eval_report_index.min.json")
        expected = eval_report_index_builder.build_eval_report_index_payload()

        self.assertEqual(current, expected)
        self.assertEqual(
            set(current.keys()),
            {"schema_version", "layer", "source_of_truth", "interpretation_boundary", "reports"},
        )
        self.assertEqual(current["schema_version"], 1)
        self.assertEqual(current["layer"], "aoa-evals")
        self.assertIn("not a receipt", current["interpretation_boundary"])
        self.assertIn("verdict authority", current["interpretation_boundary"])

        by_report = {
            (entry["eval_name"], entry["report_id"]): entry
            for entry in current["reports"]
        }
        local_report = by_report[
            ("aoa-verification-honesty", "aoa-evals-slice-19-lifecycle-contract")
        ]
        self.assertEqual(local_report["report_posture"], "bounded_report_output")
        self.assertEqual(local_report["receipt_status"], "not_a_receipt")
        self.assertIn("derived index only", local_report["authority_boundary"])
        self.assertEqual(
            local_report["source_report_path"],
            "evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json",
        )
        self.assertTrue(
            all(entry["source_report_path"].endswith(".report.json") for entry in current["reports"])
        )

    def test_phase_alpha_eval_matrix_is_generator_backed_and_tracks_required_evals(self) -> None:
        if not phase_alpha_eval_matrix_builder.PLAYBOOK_MATRIX_PATH.is_file():
            self.skipTest(
                f"aoa-playbooks phase alpha matrix is unavailable: "
                f"{phase_alpha_eval_matrix_builder.PLAYBOOK_MATRIX_PATH}"
            )
        current = load_json("mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/phase_alpha_eval_matrix.min.json")
        expected = phase_alpha_eval_matrix_builder.build_phase_alpha_eval_matrix_payload()

        self.assertEqual(current, expected)
        self.assertEqual(current["schema_version"], 1)
        self.assertEqual(current["layer"], "aoa-evals")
        self.assertEqual(current["phase"], "alpha")
        self.assertEqual(current["runtime_lanes"], {"primary": "llama.cpp", "control": "llama.cpp-second-pass"})

        by_run = {entry["run_id"]: entry for entry in current["runs"]}
        recall_rerun = by_run["alpha-06-validation-driven-remediation-recall-rerun"]
        self.assertEqual(recall_rerun["runtime_lane"], "primary")
        self.assertFalse(recall_rerun["optional_control_path_rerun"])
        self.assertEqual(
            [entry["eval_anchor"] for entry in recall_rerun["required_evals"]],
            [
                "aoa-memo-recall-integrity",
                "aoa-return-anchor-integrity",
                "aoa-verification-honesty",
            ],
        )
        memo_recall = recall_rerun["required_evals"][0]
        self.assertIn(
            "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.phase-alpha-memo-recall-rerun.example.json",
            memo_recall["evidence_refs"],
        )
        self.assertIn(
            "repo:aoa-memo/examples/recall/recall_contract.object.working.phase-alpha.json",
            memo_recall["evidence_refs"],
        )


if __name__ == "__main__":
    unittest.main()
