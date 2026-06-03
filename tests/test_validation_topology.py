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

import validation_lanes
import ci_gate
from validators import validation_topology

LANE_MANIFEST_PATH = REPO_ROOT / "docs" / "validation" / "validation_lanes.json"
VALIDATOR_INVENTORY_PATH = REPO_ROOT / "docs" / "validation" / "validator_inventory.json"
TOPOLOGY_PATH = REPO_ROOT / "docs" / "validation" / "VALIDATOR_TOPOLOGY.md"
COMMAND_AUTHORITY_PATH = REPO_ROOT / "docs" / "validation" / "COMMAND_AUTHORITY.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def command_script_paths(commands: tuple[tuple[str, ...], ...]) -> set[str]:
    paths: set[str] = set()
    for command in commands:
        for part in command:
            if part.endswith(".py") and (
                part.startswith("scripts/") or "/scripts/" in part
            ):
                paths.add(part)
    return paths


class ValidationTopologyTests(unittest.TestCase):
    def test_topology_docs_name_agentic_proof_lanes(self) -> None:
        topology = TOPOLOGY_PATH.read_text(encoding="utf-8")
        command_authority = COMMAND_AUTHORITY_PATH.read_text(encoding="utf-8")

        for required in (
            "source-fast",
            "generated",
            "mechanics/part-local",
            "pinned-sibling",
            "latest-sibling",
            "trace/eval",
            "audit",
            "release",
            "nightly",
            "advisory",
            "Generated validators",
            "Memory/context validators",
            "Security/adversarial validators",
        ):
            self.assertIn(required, topology)

        self.assertIn("docs/validation/validation_lanes.json", command_authority)
        self.assertIn("config/` is currently a route-card-only", command_authority)

    def test_lane_manifest_is_loader_authority(self) -> None:
        manifest = load_json(LANE_MANIFEST_PATH)

        self.assertEqual(LANE_MANIFEST_PATH, validation_lanes.VALIDATION_LANES_PATH)
        self.assertEqual(manifest["command_authority"], "docs/validation/validation_lanes.json")
        self.assertEqual(
            tuple(tuple(command) for command in manifest["command_sequences"]["source_fast"]),
            validation_lanes.SOURCE_FAST_COMMAND_SEQUENCE,
        )
        self.assertEqual(
            tuple(tuple(command) for command in manifest["command_sequences"]["generated_check"]),
            validation_lanes.GENERATED_CHECK_COMMAND_SEQUENCE,
        )
        self.assertEqual(
            validation_lanes.GENERATED_CHECK_COMMAND_SEQUENCE,
            validation_lanes.GENERATED_CHECK_COMMAND_SEQUENCE_FROM_GROUPS,
        )
        self.assertIn(
            (
                "python",
                "mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py",
                "--check",
            ),
            validation_lanes.GENERATED_CHECK_COMMAND_SEQUENCE,
        )
        self.assertEqual(
            tuple(tuple(command) for command in manifest["command_sequences"]["release_check"]),
            validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE,
        )

        release_text = (REPO_ROOT / "scripts" / "release_check.py").read_text(encoding="utf-8")
        self.assertIn("validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE", release_text)
        self.assertIn("validation_lanes.command_for_runtime", release_text)
        self.assertNotIn("COMMANDS = [", release_text)

    def test_lane_runtime_command_uses_current_python_interpreter(self) -> None:
        self.assertEqual(
            (sys.executable, "scripts/validate_repo.py"),
            validation_lanes.command_for_runtime(("python", "scripts/validate_repo.py")),
        )
        self.assertEqual(
            ("node", "--version"),
            validation_lanes.command_for_runtime(("node", "--version")),
        )

    def test_validator_inventory_entries_are_complete_and_owner_routed(self) -> None:
        inventory = load_json(VALIDATOR_INVENTORY_PATH)
        required_fields = set(inventory["required_fields"])
        entries = inventory["entries"]
        paths = [entry["path"] for entry in entries]

        self.assertEqual("docs/validation/VALIDATOR_TOPOLOGY.md", inventory["owner"])
        self.assertEqual("docs/validation/validation_lanes.json", inventory["command_authority"])
        self.assertEqual(len(paths), len(set(paths)))
        self.assertGreaterEqual(len(entries), 10)

        for entry in entries:
            with self.subTest(path=entry.get("path")):
                self.assertEqual(required_fields, set(entry))
                self.assertTrue((REPO_ROOT / entry["path"]).exists())
                self.assertTrue((REPO_ROOT / entry["owner_surface"]).exists())
                self.assertTrue(entry["source_truth"])
                self.assertTrue(entry["input"])
                self.assertTrue(entry["output"])
                self.assertTrue(entry["command_sequences"])
                self.assertTrue(entry["failure_route"])
                self.assertIn(entry["disposition"], {"keep", "split", "fold", "add"})

    def test_validation_topology_validator_accepts_current_surfaces(self) -> None:
        self.assertEqual([], validation_topology.validate_validation_topology(REPO_ROOT))

    def test_validation_topology_validator_rejects_unclassified_validator_module(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            for relative_path in (
                "docs/validation/VALIDATOR_TOPOLOGY.md",
                "docs/validation/COMMAND_AUTHORITY.md",
                "docs/validation/validation_lanes.json",
                "docs/validation/validator_inventory.json",
                "docs/validation/script_inventory.json",
                "docs/testing/test_inventory.json",
                "docs/testing/TEST_TOPOLOGY.md",
            ):
                source = REPO_ROOT / relative_path
                target = tmp_path / relative_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            module_path = tmp_path / "scripts" / "validators" / "unclassified.py"
            module_path.parent.mkdir(parents=True, exist_ok=True)
            module_path.write_text("# unclassified validator\n", encoding="utf-8")

            issues = validation_topology.validate_validation_topology(tmp_path)

        self.assertTrue(
            any(
                location == "scripts/validators/unclassified.py"
                and "validator inventory must classify" in message
                for location, message in issues
            )
        )

    def test_validation_topology_validator_rejects_generated_group_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            for relative_path in (
                "docs/validation/VALIDATOR_TOPOLOGY.md",
                "docs/validation/COMMAND_AUTHORITY.md",
                "docs/validation/validation_lanes.json",
                "docs/validation/validator_inventory.json",
                "docs/validation/script_inventory.json",
                "docs/testing/test_inventory.json",
                "docs/testing/TEST_TOPOLOGY.md",
            ):
                source = REPO_ROOT / relative_path
                target = tmp_path / relative_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            manifest_path = tmp_path / "docs" / "validation" / "validation_lanes.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["command_sequences"]["generated_check"] = [
                ["python", "scripts/build_catalog.py", "--check"]
            ]
            manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

            issues = validation_topology.validate_validation_topology(tmp_path)

        self.assertTrue(
            any(
                location == "docs/validation/validation_lanes.json"
                and "generated command group must flatten" in message
                for location, message in issues
            )
        )

    def test_validation_topology_validator_requires_generated_group(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            for relative_path in (
                "docs/validation/VALIDATOR_TOPOLOGY.md",
                "docs/validation/COMMAND_AUTHORITY.md",
                "docs/validation/validation_lanes.json",
                "docs/validation/validator_inventory.json",
                "docs/validation/script_inventory.json",
                "docs/testing/test_inventory.json",
                "docs/testing/TEST_TOPOLOGY.md",
            ):
                source = REPO_ROOT / relative_path
                target = tmp_path / relative_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            manifest_path = tmp_path / "docs" / "validation" / "validation_lanes.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            del manifest["command_groups"]["generated_check"]
            manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

            issues = validation_topology.validate_validation_topology(tmp_path)

        self.assertTrue(
            any(
                location == "docs/validation/validation_lanes.json"
                and "command_groups.generated_check must be a non-empty list" in message
                for location, message in issues
            )
        )

    def test_lane_command_scripts_are_in_script_inventory(self) -> None:
        script_inventory = load_json(REPO_ROOT / "docs" / "validation" / "script_inventory.json")
        inventory_paths = {entry["path"] for entry in script_inventory["script_surfaces"]}
        lane_script_paths = set()

        for lane_id, lane in validation_lanes.LANE_DEFINITIONS.items():
            if not lane.get("command_sequence"):
                continue
            lane_script_paths.update(command_script_paths(validation_lanes.command_sequence_for_lane(lane_id)))

        self.assertTrue(lane_script_paths)
        self.assertEqual([], sorted(lane_script_paths - inventory_paths))

    def test_script_discovery_ignores_dependency_checkouts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            owned_script = tmp_path / "scripts" / "owned.py"
            dependency_script = tmp_path / ".deps" / "aoa-playbooks" / "scripts" / "external.py"
            owned_script.parent.mkdir(parents=True, exist_ok=True)
            dependency_script.parent.mkdir(parents=True, exist_ok=True)
            owned_script.write_text("# owned\n", encoding="utf-8")
            dependency_script.write_text("# dependency\n", encoding="utf-8")

            discovered = validation_topology._discovered_script_surfaces(tmp_path)

        self.assertIn("scripts/owned.py", discovered)
        self.assertNotIn(".deps/aoa-playbooks/scripts/external.py", discovered)

    def test_ci_gate_expands_manifest_path_globs_without_shell(self) -> None:
        command = ("python", "-m", "pytest", "-q", "mechanics/*/parts/*/tests/test*.py")

        expanded = ci_gate.expand_command_globs(command)

        self.assertNotIn("mechanics/*/parts/*/tests/test*.py", expanded)
        self.assertIn("python", expanded)
        self.assertTrue(
            any(part.startswith("mechanics/") and part.endswith(".py") for part in expanded)
        )
        self.assertFalse(any("*" in part for part in expanded))


if __name__ == "__main__":
    unittest.main()
