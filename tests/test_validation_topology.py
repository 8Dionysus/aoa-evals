from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validation_lanes
import ci_gate
import validate_abyss_machine_report_index_bundle
from validators import (
    validation_lane_manifest,
    validation_script_inventory,
    validation_test_inventory,
    validation_topology_common,
    validation_topology_docs,
    validation_validator_inventory,
)

LANE_MANIFEST_PATH = REPO_ROOT / "docs" / "validation" / "validation_lanes.json"
VALIDATOR_INVENTORY_PATH = REPO_ROOT / "docs" / "validation" / "validator_inventory.json"
TOPOLOGY_PATH = REPO_ROOT / "docs" / "validation" / "VALIDATOR_TOPOLOGY.md"
COMMAND_AUTHORITY_PATH = REPO_ROOT / "docs" / "validation" / "COMMAND_AUTHORITY.md"
SKILL_PORT_MANIFEST_PATH = REPO_ROOT / "skills" / "port.manifest.json"
PRIMARY_COMMAND_DOCS = frozenset(
    {
        "docs/validation/COMMAND_AUTHORITY.md",
        "docs/operations/RELEASING.md",
        "docs/guides/EVAL_FORGE_READINESS_LAYER.md",
        "docs/guides/LOCAL_EVAL_PORT_STANDARD.md",
        (
            "mechanics/proof-object/parts/eval-authoring/docs/"
            "EVAL_FORGE_OPERATING_PATH.md"
        ),
    }
)
SHELL_FENCE_PATTERN = re.compile(
    r"^ {0,3}```(?:bash|console|sh|shell)(?:\s+.*)?$",
    re.IGNORECASE | re.MULTILINE,
)
REPO_COMMAND_LINE_PATTERN = re.compile(
    r"^[ \t]*(?:[-*][ \t]+)?`?(?:"
    r"python(?:[ \t]+-m)?[ \t]+|pytest(?=[ \t])|"
    r"uv[ \t]+run[ \t]+pytest\b|git[ \t]+(?:status|diff)\b)",
    re.IGNORECASE | re.MULTILINE,
)
INLINE_REPO_COMMAND_PATTERN = re.compile(
    r"`(?:python(?:\s+-m)?\s+|pytest(?=\s)|git\s+(?:status|diff)\b)[^`]+`",
    re.IGNORECASE,
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def tracked_markdown_paths() -> tuple[Path, ...]:
    result = subprocess.run(
        ("git", "ls-files", "--", "*.md"),
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return tuple(Path(line) for line in result.stdout.splitlines() if line)


def admitted_owner_skill_roots() -> tuple[Path, ...]:
    payload = load_json(SKILL_PORT_MANIFEST_PATH)
    roots: list[Path] = []
    for bundle in payload.get("bundles", []):
        path = bundle.get("path") if isinstance(bundle, dict) else None
        if isinstance(path, str) and path:
            roots.append(Path(path))
    return tuple(roots)


def is_owner_skill_command_doc(relative_path: Path) -> bool:
    return any(
        relative_path == root or root in relative_path.parents
        for root in admitted_owner_skill_roots()
    )


def markdown_command_violations(content: str) -> set[str]:
    violations: set[str] = set()
    if SHELL_FENCE_PATTERN.search(content):
        violations.add("shell command block")
    if REPO_COMMAND_LINE_PATTERN.search(content):
        violations.add("repo command line")
    if INLINE_REPO_COMMAND_PATTERN.search(content):
        violations.add("inline repo command")
    return violations


def command_script_paths(commands: tuple[tuple[str, ...], ...]) -> set[str]:
    paths: set[str] = set()
    for command in commands:
        for part in command:
            if part.endswith(".py") and (
                part.startswith("scripts/") or "/scripts/" in part
            ):
                paths.add(part)
    return paths


def validate_validation_topology(repo_root: Path) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    issues.extend(validation_topology_docs.validate_validation_topology_docs(repo_root))
    issues.extend(validation_lane_manifest.validate_validation_lane_manifest(repo_root))
    issues.extend(validation_validator_inventory.validate_validator_inventory(repo_root))
    issues.extend(validation_script_inventory.validate_script_inventory(repo_root))
    issues.extend(validation_test_inventory.validate_test_inventory(repo_root))
    return issues


class ValidationTopologyTests(unittest.TestCase):
    def test_non_owner_markdown_routes_runnable_commands_to_command_owners(self) -> None:
        offenders: list[str] = []
        for relative_path in tracked_markdown_paths():
            route = relative_path.as_posix()
            if route.startswith(".agents/skills/"):
                continue
            if relative_path.name in {"AGENTS.md", "VALIDATION.md"}:
                continue
            if is_owner_skill_command_doc(relative_path):
                continue
            if route in PRIMARY_COMMAND_DOCS:
                continue
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for violation in sorted(markdown_command_violations(content)):
                offenders.append(f"{route}: {violation}")

        self.assertEqual([], offenders)

    def test_markdown_command_guard_rejects_scattered_command_forms(self) -> None:
        content = """# Drift

```bash
python scripts/validate_repo.py
```

- `python -m pytest -q`
"""

        self.assertEqual(
            {"inline repo command", "repo command line", "shell command block"},
            markdown_command_violations(content),
        )

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
        stats_command = ("python", "scripts/validate_local_stats_port.py")
        self.assertEqual(stats_command, validation_lanes.LATEST_SIBLING_COMMAND_SEQUENCE[0])
        self.assertIn(stats_command, validation_lanes.NIGHTLY_COMMAND_SEQUENCE)
        self.assertNotIn(stats_command, validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE)

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

    def test_report_index_bundle_validator_uses_temporary_paths_by_default(self) -> None:
        captured: dict[str, Path] = {}

        def fake_validate(
            manifest: Path,
            subject: Path,
            bundle_dir: Path,
            registry_dir: Path,
            subject_store_root: Path,
            *,
            clean: bool,
        ) -> dict:
            captured.update(
                {
                    "bundle_dir": bundle_dir,
                    "registry_dir": registry_dir,
                    "subject_store_root": subject_store_root,
                }
            )
            return {"ok": True, "bundle_dir": str(bundle_dir), "registry_dir": str(registry_dir)}

        with patch.object(
            validate_abyss_machine_report_index_bundle,
            "_validate_in_bundle_dir",
            side_effect=fake_validate,
        ):
            payload = validate_abyss_machine_report_index_bundle.validate_bundle(
                validate_abyss_machine_report_index_bundle.DEFAULT_MANIFEST,
                validate_abyss_machine_report_index_bundle.DEFAULT_SUBJECT,
                None,
                None,
                None,
                clean=True,
            )

        self.assertTrue(payload["ok"])
        self.assertNotEqual(
            captured["bundle_dir"],
            validate_abyss_machine_report_index_bundle.DEFAULT_BUNDLE_DIR,
        )
        self.assertNotEqual(
            captured["registry_dir"],
            validate_abyss_machine_report_index_bundle.DEFAULT_REGISTRY_DIR,
        )
        self.assertNotEqual(
            captured["subject_store_root"],
            validate_abyss_machine_report_index_bundle.DEFAULT_SUBJECT_STORE_ROOT,
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
        self.assertEqual([], validate_validation_topology(REPO_ROOT))

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

            issues = validate_validation_topology(tmp_path)

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

            issues = validate_validation_topology(tmp_path)

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

            issues = validate_validation_topology(tmp_path)

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

            discovered = validation_topology_common._discovered_script_surfaces(tmp_path)

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
