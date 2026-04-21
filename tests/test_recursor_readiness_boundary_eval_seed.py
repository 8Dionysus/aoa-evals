from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_scorer():
    path = ROOT / "scorers" / "recursor_readiness_boundary.py"
    spec = importlib.util.spec_from_file_location("recursor_readiness_boundary_test", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RecursorReadinessBoundaryEvalSeedTest(unittest.TestCase):
    def test_all_fixture_expectations_hold(self):
        scorer = load_scorer()
        cases_dir = ROOT / "fixtures" / "recursor-readiness-boundary-v1" / "cases"
        for path in sorted(cases_dir.glob("*.json")):
            case = json.loads(path.read_text(encoding="utf-8"))
            result = scorer.score(case["input"])
            ok, errors = scorer.check_expected(result, case["expected"])
            self.assertTrue(ok, f"{path.name}: {errors}")

    def test_positive_case_passes(self):
        scorer = load_scorer()
        case = json.loads((ROOT / "fixtures" / "recursor-readiness-boundary-v1" / "cases" / "RRB-001.no-spawn-readiness.json").read_text(encoding="utf-8"))
        result = scorer.score(case["input"])
        self.assertEqual(result["verdict"], "pass")
        self.assertFalse(result["failed_axes"])

    def test_projection_install_by_default_fails(self):
        scorer = load_scorer()
        case = json.loads((ROOT / "fixtures" / "recursor-readiness-boundary-v1" / "cases" / "RRB-002.projection-install-by-default-negative.json").read_text(encoding="utf-8"))
        result = scorer.score(case["input"])
        self.assertEqual(result["verdict"], "fail")
        self.assertIn("candidate_only_projection", result["failed_axes"])


if __name__ == "__main__":
    unittest.main()
