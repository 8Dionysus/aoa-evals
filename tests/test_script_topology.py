from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validation_lanes

INVENTORY_PATH = REPO_ROOT / "docs" / "validation" / "script_inventory.json"

ALLOWED_ORGAN_LANES = {
    "source/topology",
    "projection/generated",
    "capability/runtime-policy route",
    "mechanics/part-local",
    "runtime-policy route",
    "trace/eval route",
    "observability/audit",
    "security/adversarial",
    "release/nightly",
    "compatibility adapter",
}
ALLOWED_VALIDATION_LANES = {
    "source_fast",
    "generated",
    "mechanics_part_local",
    "pinned_sibling",
    "latest_sibling",
    "release",
    "nightly",
    "advisory",
}
REQUIRED_ENTRY_FIELDS = {
    "path",
    "family",
    "organ_lane",
    "owner_surface",
    "source_truth",
    "reads",
    "writes",
    "side_effects",
    "validation_lane",
    "ci_inclusion",
    "test_target",
    "disposition",
}


def load_inventory() -> dict:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def inventory_entries() -> list[dict]:
    return load_inventory()["script_surfaces"]


def inventory_paths() -> set[str]:
    return {entry["path"] for entry in inventory_entries()}


def discovered_script_surfaces() -> set[str]:
    return {
        path.relative_to(REPO_ROOT).as_posix()
        for path in REPO_ROOT.rglob("*")
        if path.is_file()
        and "/scripts/" in f"/{path.relative_to(REPO_ROOT).as_posix()}"
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    }


def command_script_paths(commands: tuple[tuple[str, ...], ...]) -> set[str]:
    paths: set[str] = set()
    for command in commands:
        for part in command:
            if part.endswith(".py") and (
                part.startswith("scripts/") or "/scripts/" in part
            ):
                paths.add(part)
    return paths


def all_lane_command_script_paths() -> set[str]:
    paths: set[str] = set()
    for lane_id, lane in validation_lanes.LANE_DEFINITIONS.items():
        if not lane.get("command_sequence"):
            continue
        paths.update(command_script_paths(validation_lanes.command_sequence_for_lane(lane_id)))
    return paths


class ScriptTopologyTests(unittest.TestCase):
    def test_script_inventory_covers_every_active_script_surface(self) -> None:
        inventory = load_inventory()
        paths = [entry["path"] for entry in inventory["script_surfaces"]]

        self.assertEqual("docs/validation/SCRIPT_TOPOLOGY.md", inventory["owner"])
        self.assertEqual("docs/validation/validation_lanes.json", inventory["command_authority"])
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(discovered_script_surfaces(), set(paths))

    def test_script_inventory_entries_are_complete_and_owner_routed(self) -> None:
        for entry in inventory_entries():
            with self.subTest(path=entry.get("path")):
                self.assertEqual(REQUIRED_ENTRY_FIELDS, set(entry))
                self.assertIn(entry["organ_lane"], ALLOWED_ORGAN_LANES)
                self.assertIn(entry["validation_lane"], ALLOWED_VALIDATION_LANES)
                self.assertIn(entry["disposition"], {"keep", "split", "add"})
                self.assertTrue((REPO_ROOT / entry["path"]).is_file())
                self.assertTrue((REPO_ROOT / entry["owner_surface"]).exists())
                self.assertTrue((REPO_ROOT / entry["test_target"]).exists())
                self.assertIsInstance(entry["source_truth"], list)
                self.assertTrue(entry["source_truth"])
                self.assertIsInstance(entry["reads"], list)
                self.assertTrue(entry["reads"])
                self.assertIsInstance(entry["writes"], list)
                self.assertTrue(entry["side_effects"])
                self.assertTrue(entry["ci_inclusion"])

    def test_lane_commands_reference_inventoried_scripts(self) -> None:
        command_paths = all_lane_command_script_paths()

        self.assertTrue(command_paths)
        self.assertTrue(command_paths <= inventory_paths())
        self.assertNotIn("scripts/release_check.py", command_script_paths(validation_lanes.SOURCE_FAST_COMMAND_SEQUENCE))
        self.assertFalse(
            {
                path
                for path in command_script_paths(validation_lanes.SOURCE_FAST_COMMAND_SEQUENCE)
                if Path(path).name.startswith(("build_", "generate_"))
            }
        )

    def test_advisory_skill_helpers_are_not_hidden_hard_gates(self) -> None:
        hard_gate_paths = all_lane_command_script_paths()

        for entry in inventory_entries():
            path = entry["path"]
            with self.subTest(path=path):
                if path.startswith(".agents/skills/"):
                    self.assertEqual("advisory", entry["validation_lane"])
                    self.assertEqual([], entry["writes"])
                    self.assertNotIn(path, hard_gate_paths)
                if path.endswith("publish_live_receipts.py"):
                    self.assertEqual("advisory", entry["validation_lane"])
                    self.assertIn("appends", entry["side_effects"])

    def test_tracked_python_cache_residue_stays_out_of_scripts(self) -> None:
        completed = subprocess.run(
            ["git", "ls-files", "**/__pycache__/**", "*.pyc"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            check=False,
        )
        tracked_cache = [line for line in completed.stdout.splitlines() if line]
        self.assertEqual([], tracked_cache)


if __name__ == "__main__":
    unittest.main()
