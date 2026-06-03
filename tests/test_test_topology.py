from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = REPO_ROOT / "docs" / "testing" / "test_inventory.json"

ALLOWED_FAMILIES = {
    "source/proof-contract",
    "generated/read-model",
    "route-card/topology",
    "mechanics/package-topology",
    "mechanics/part-local",
    "boundary/sibling",
    "trace/eval-scenario",
    "audit/release-report",
    "validation-topology/authority",
}
ALLOWED_HOME_SCOPES = {"root", "mechanic-part", "agent-lane"}
ALLOWED_DISPOSITIONS = {"keep", "split", "fold", "add"}


def load_inventory() -> dict:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def inventory_entries() -> list[dict]:
    return load_inventory()["test_surfaces"]


def discovered_test_surfaces() -> set[str]:
    root_tests = {
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "tests").glob("test*.py")
        if path.is_file()
    }
    part_tests = {
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "mechanics").glob("*/parts/*/tests/test*.py")
        if path.is_file()
    }
    return root_tests | part_tests


class TestTopologyTests(unittest.TestCase):
    def test_test_inventory_covers_root_and_part_local_tests(self) -> None:
        inventory = load_inventory()
        paths = [entry["path"] for entry in inventory["test_surfaces"]]

        self.assertEqual("docs/testing/TEST_TOPOLOGY.md", inventory["owner"])
        self.assertEqual("docs/validation/validation_lanes.json", inventory["command_authority"])
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(discovered_test_surfaces(), set(paths))

    def test_test_inventory_entries_are_complete_and_owner_routed(self) -> None:
        required_fields = set(load_inventory()["required_fields"])

        for entry in inventory_entries():
            with self.subTest(path=entry.get("path")):
                self.assertEqual(required_fields, set(entry))
                self.assertTrue((REPO_ROOT / entry["path"]).is_file())
                self.assertTrue((REPO_ROOT / entry["owner_surface"]).exists())
                self.assertIn(entry["family"], ALLOWED_FAMILIES)
                self.assertIn(entry["home_scope"], ALLOWED_HOME_SCOPES)
                self.assertTrue(entry["coverage_authority"].startswith("validation_lanes."))
                self.assertTrue(entry["focused_target"])
                self.assertTrue(entry["failure_route"])
                self.assertIn(entry["disposition"], ALLOWED_DISPOSITIONS)

    def test_split_pressure_is_visible_for_root_validator_mesh(self) -> None:
        entries_by_path = {entry["path"]: entry for entry in inventory_entries()}

        self.assertEqual("split", entries_by_path["tests/test_validate_repo.py"]["disposition"])
        self.assertEqual(
            "validation-topology/authority",
            entries_by_path["tests/test_validation_topology.py"]["family"],
        )
        self.assertEqual(
            "validation-topology/authority",
            entries_by_path["tests/test_script_topology.py"]["family"],
        )
        self.assertEqual(
            "validation-topology/authority",
            entries_by_path["tests/test_test_topology.py"]["family"],
        )


if __name__ == "__main__":
    unittest.main()
