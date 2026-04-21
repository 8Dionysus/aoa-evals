from __future__ import annotations
import json, subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RecurrenceControlPlaneIntegritySeedTest(unittest.TestCase):
    def load_case(self, name):
        return json.loads(
            (
                ROOT
                / "fixtures"
                / "recurrence-control-plane-integrity-v1"
                / "cases"
                / name
            ).read_text(encoding="utf-8")
        )

    def test_positive_cases_match_expected_axes(self):
        from scorers.recurrence_control_plane_integrity import (
            evaluate_dossier,
            compare_expected,
        )

        for name in [
            "RCPI-001.registry-mixed-manifests.json",
            "RCPI-002.graph-closure-cycle-aware.json",
            "RCPI-003.hook-no-mutation.json",
            "RCPI-004.beacon-review-boundary.json",
            "RCPI-005.downstream-thinness.json",
            "RCPI-006.agon-stop-lines.json",
        ]:
            case = self.load_case(name)
            report = evaluate_dossier(case)
            self.assertEqual(compare_expected(report, case["expected_axis_status"]), [])
            self.assertIn(
                report["verdict"], {"supports bounded claim", "mixed support"}
            )

    def test_negative_overclaim_degrades(self):
        from scorers.recurrence_control_plane_integrity import (
            evaluate_dossier,
            compare_expected,
        )

        case = self.load_case("RCPI-007.negative-overclaim.json")
        report = evaluate_dossier(case)
        self.assertEqual(compare_expected(report, case["expected_axis_status"]), [])
        self.assertEqual(report["verdict"], "does not support bounded claim")

    def test_runner_check_expected_passes(self):
        case = (
            ROOT
            / "fixtures"
            / "recurrence-control-plane-integrity-v1"
            / "cases"
            / "RCPI-001.registry-mixed-manifests.json"
        )
        proc = subprocess.run(
            [
                sys.executable,
                "scripts/run_recurrence_control_plane_integrity_eval.py",
                "--case",
                str(case),
                "--check-expected",
                "--json",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(
            json.loads(proc.stdout)["eval_name"],
            "aoa-recurrence-control-plane-integrity",
        )

    def test_report_schema_and_example_are_present(self):
        schema = json.loads(
            (
                ROOT
                / "bundles"
                / "aoa-recurrence-control-plane-integrity"
                / "reports"
                / "summary.schema.json"
            ).read_text()
        )
        example = json.loads(
            (
                ROOT
                / "bundles"
                / "aoa-recurrence-control-plane-integrity"
                / "reports"
                / "example-report.json"
            ).read_text()
        )
        self.assertEqual(schema["title"], "Recurrence Control Plane Integrity Summary")
        self.assertEqual(example["eval_name"], "aoa-recurrence-control-plane-integrity")


if __name__ == "__main__":
    unittest.main()
