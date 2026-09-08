from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validators.validation_test_inventory import validate_test_inventory

INVENTORY_PATH = "docs/testing/test_inventory.json"
LANES_PATH = "docs/validation/validation_lanes.json"


class TestTopologyTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        owner = "docs/testing/TEST_TOPOLOGY.md"
        root_test = "tests/test_source.py"
        part_test = "mechanics/sample/parts/contracts/tests/test_contract.py"
        for relative_path in (owner, root_test, part_test):
            path = self.repo / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")
        self.entry = {
            "path": root_test,
            "family": "source/proof-contract",
            "home_scope": "root",
            "owner_surface": owner,
            "coverage_authority": "validation_lanes.source_fast",
            "focused_target": "source contract",
            "failure_route": "Return to the source owner.",
            "disposition": "keep",
        }
        # Independent small inputs, not a copy of the current repository inventory
        # or expected fields imported from the implementation under test.
        self.inventory = {
            "schema_version": 1,
            "owner": owner,
            "command_authority": LANES_PATH,
            "required_fields": [
                "path", "family", "home_scope", "owner_surface",
                "coverage_authority", "focused_target", "failure_route", "disposition",
            ],
            "test_surfaces": [
                self.entry,
                {**self.entry, "path": part_test, "home_scope": "mechanic-part"},
            ],
        }
        self.write_json(INVENTORY_PATH, self.inventory)
        # This checker resolves references; full lane definitions have their own validator.
        self.write_json(LANES_PATH, {"lanes": {"source_fast": {}}})

    def write_json(self, relative_path: str, payload: object) -> None:
        path = self.repo / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload), encoding="utf-8")

    def assert_rejected(self, fragment: str) -> None:
        issues = validate_test_inventory(self.repo)
        self.assertTrue(any(fragment in message for _, message in issues), issues)

    def test_accepts_complete_root_and_part_inventory(self) -> None:
        self.assertEqual([], validate_test_inventory(self.repo))

    def test_resolves_owner_declared_lane_without_requiring_execution(self) -> None:
        self.write_json(LANES_PATH, {"lanes": {"owner_review": {"posture": "non_blocking"}}})
        for entry in self.inventory["test_surfaces"]:
            entry["coverage_authority"] = "validation_lanes.owner_review"
        self.write_json(INVENTORY_PATH, self.inventory)

        self.assertEqual([], validate_test_inventory(self.repo))

    def test_rejects_dangling_or_malformed_lane_references(self) -> None:
        for reference in ("validation_lanes.unknown", "validation_lanes.", "source_fast", None):
            with self.subTest(reference=reference):
                self.entry["coverage_authority"] = reference
                self.write_json(INVENTORY_PATH, self.inventory)
                self.assert_rejected("coverage_authority")

    def test_rejects_unavailable_lane_authority(self) -> None:
        manifest_path = self.repo / LANES_PATH
        for content in (None, "{", "{}", '{"lanes": []}'):
            with self.subTest(content=content):
                if content is None:
                    manifest_path.unlink()
                else:
                    manifest_path.write_text(content, encoding="utf-8")
                issues = validate_test_inventory(self.repo)
                self.assertTrue(any(path == LANES_PATH for path, _ in issues), issues)

    def test_rejects_wrong_authority_and_field_contract(self) -> None:
        for field, value, fragment in (
            ("owner", "generated/INDEX.md", "owner"),
            ("command_authority", "tests/commands.json", "command authority"),
            ("required_fields", [], "required_fields"),
        ):
            with self.subTest(field=field):
                self.write_json(INVENTORY_PATH, {**self.inventory, field: value})
                self.assert_rejected(fragment)

    def test_rejects_unrouted_or_unclassified_entries(self) -> None:
        for field, value in (
            ("family", "unknown"),
            ("home_scope", "unknown"),
            ("disposition", "unknown"),
            ("owner_surface", "missing-owner.md"),
            ("focused_target", ""),
            ("failure_route", ""),
        ):
            with self.subTest(field=field):
                entries = [{**self.entry, field: value}, self.inventory["test_surfaces"][1]]
                self.write_json(INVENTORY_PATH, {**self.inventory, "test_surfaces": entries})
                self.assert_rejected(field)

    def test_rejects_incomplete_and_non_object_entries(self) -> None:
        for entry, fragment in (({}, "fields"), (None, "object")):
            with self.subTest(entry=entry):
                self.write_json(INVENTORY_PATH, {**self.inventory, "test_surfaces": [entry]})
                self.assert_rejected(fragment)

    def test_rejects_duplicate_and_missing_test_paths(self) -> None:
        self.inventory["test_surfaces"].append(self.entry)
        self.write_json(INVENTORY_PATH, self.inventory)
        self.assert_rejected("unique")

        self.inventory["test_surfaces"].pop()
        self.write_json(INVENTORY_PATH, self.inventory)
        (self.repo / self.entry["path"]).unlink()
        self.assert_rejected("path does not exist")

    def test_discovers_unclassified_root_and_part_tests(self) -> None:
        for relative_path in (
            "tests/test_unclassified.py",
            "mechanics/sample/parts/contracts/tests/test_unclassified.py",
        ):
            with self.subTest(path=relative_path):
                path = self.repo / relative_path
                path.write_text("", encoding="utf-8")
                issues = validate_test_inventory(self.repo)
                self.assertTrue(any(location == relative_path for location, _ in issues), issues)
                path.unlink()


if __name__ == "__main__":
    unittest.main()
