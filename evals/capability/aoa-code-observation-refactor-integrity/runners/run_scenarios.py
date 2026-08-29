#!/usr/bin/env python3
"""Validate and summarize the bounded refactor-torture observation contract."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
import platform
import sys
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BUNDLE_ROOT.parents[2]
FIXTURE_PATH = (
    REPO_ROOT
    / "mechanics"
    / "proof-infra"
    / "parts"
    / "fixture-families"
    / "fixtures"
    / "refactor-torture-v1"
    / "cases.json"
)
FIXTURE_CONTRACT_PATH = BUNDLE_ROOT / "fixtures" / "contract.json"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "schemas" / "refactor-observation-report.schema.json"
PROVIDER_EXECUTION_SCHEMA_PATH = BUNDLE_ROOT / "schemas" / "provider-execution.schema.json"
PROVIDER_EVIDENCE_SCHEMA_PATH = BUNDLE_ROOT / "schemas" / "provider-observation-evidence.schema.json"
PROVIDER_EXECUTION_FIXTURE_PATH = (
    BUNDLE_ROOT / "fixtures" / "provider-execution" / "manifest.json"
)
PROVIDER_EXECUTION_FIXTURE_SCHEMA_PATH = (
    BUNDLE_ROOT / "schemas" / "provider-execution-fixture.schema.json"
)
SUMMARY_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "summary.schema.json"
EXAMPLE_REPORT_PATH = BUNDLE_ROOT / "fixtures" / "observation-report.example.json"
AFFECTED_TEST_ORACLE_PATH = FIXTURE_PATH.parent / "oracles" / "affected-tests.json"
AFFECTED_TEST_ORACLE_REPO_PATH = (
    AFFECTED_TEST_ORACLE_PATH.relative_to(REPO_ROOT).as_posix()
)
AFFECTED_TEST_ORACLE_MANIFEST_PATH = "oracles/affected-tests.json"

MACHINE_CONTRACT_SCHEMA = "abyss_machine_code_intelligence_config_v1"
MACHINE_CONTRACT_REF = "config-templates/etc/abyss-machine/code-intelligence.json"
MACHINE_CONTRACT_DIGEST = "sha256:6a5b5a78e1a3abe963764ab45fc3df96b8f24929a9fb95742c58328de670b7ba"
MACHINE_CONTRACT_DIGEST_KIND = "sha256-raw-file-bytes"
MACHINE_CONTRACT_SNAPSHOT_EPOCH = "59be4462e5cbed389ab8906c26524ed6338f1eb2"
MACHINE_WORKSPACE_MANIFEST_DIGEST = "sha256:3da4c03be2d8ca518012e1228d17a4ca0018d6d3b0ad3d871fed03768489622b"
MACHINE_PROVIDER_ID = "python-ast-bootstrap"
OWNER_BINDINGS = {
    "host_install_and_trust_owner": "abyss-machine",
    "provider_lifecycle_owner": "abyss-stack",
    "normalized_observation_consumer": "aoa-kag",
    "semantic_proof_owner": "aoa-evals",
}

SUMMARY_LIMITATIONS = [
    "synthetic cases do not establish provider correctness or production performance",
    "live and indexed labels are declared evidence planes, not canonical owner truth",
    "a green contract run is not an aoa-evals proof verdict or owner acceptance",
]


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def stable_provider_state_digest(value: Any) -> str:
    """Digest provider state while ignoring observation timestamps."""

    def strip_timestamps(item: Any) -> Any:
        if isinstance(item, dict):
            return {
                key: strip_timestamps(value_item)
                for key, value_item in item.items()
                if key != "observed_at"
            }
        if isinstance(item, list):
            return [strip_timestamps(value_item) for value_item in item]
        return item

    return canonical_digest(strip_timestamps(value))


def source_tree_text(tree: dict[str, list[str]]) -> dict[str, str]:
    """Materialize the public-safe execution fixture without touching disk."""

    return {
        path: "\n".join(lines) + "\n"
        for path, lines in sorted(tree.items())
    }


def source_snapshot_digest(tree: dict[str, list[str]]) -> str:
    files = source_tree_text(tree)
    records = [
        {
            "path": path,
            "sha256": "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest(),
        }
        for path, content in sorted(files.items())
    ]
    return canonical_digest(records)


def changed_source_paths(
    before: dict[str, list[str]], after: dict[str, list[str]]
) -> tuple[list[str], list[str], list[str]]:
    before_paths = set(before)
    after_paths = set(after)
    changed = sorted(
        path for path in before_paths & after_paths if before[path] != after[path]
    )
    added = sorted(after_paths - before_paths)
    deleted = sorted(before_paths - after_paths)
    return changed, added, deleted


def source_import_modules(path: str, source: str) -> set[str]:
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError:
        return set()
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            modules.add(node.module.split(".")[0])
    return modules


def dependency_impacted_paths(
    before: dict[str, list[str]],
    after: dict[str, list[str]],
    changed: list[str],
    added: list[str],
    deleted: list[str],
) -> list[str]:
    target_modules: set[str] = set()
    for path in [*changed, *added, *deleted]:
        pure = PurePosixPath(path)
        target_modules.add(pure.stem)
        target_modules.add(".".join(pure.with_suffix("").parts))

    impacted: set[str] = set()
    for path, source in {**source_tree_text(before), **source_tree_text(after)}.items():
        if path in changed:
            continue
        if source_import_modules(path, source) & target_modules:
            impacted.add(path)
    return sorted(impacted)


def _normalized_ast_dump(node: ast.AST, *, body_only: bool) -> str:
    normalized = copy.deepcopy(node)
    if isinstance(normalized, (ast.AsyncFunctionDef, ast.FunctionDef, ast.ClassDef)):
        normalized.name = ""
    if body_only and isinstance(normalized, (ast.AsyncFunctionDef, ast.FunctionDef)):
        normalized = ast.Module(body=normalized.body, type_ignores=[])
    return ast.dump(normalized, annotate_fields=True, include_attributes=False)


class _LineageShapeNormalizer(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        normalized = ast.Constant(value=type(node.value).__name__)
        return ast.copy_location(normalized, node)


def _lineage_shape_dump(node: ast.AST, *, kind: str) -> str:
    normalized = copy.deepcopy(node)
    if isinstance(normalized, (ast.AsyncFunctionDef, ast.FunctionDef, ast.ClassDef)):
        normalized.name = ""
    if kind == "function" and isinstance(normalized, (ast.AsyncFunctionDef, ast.FunctionDef)):
        normalized = ast.Module(body=normalized.body, type_ignores=[])
    normalized = _LineageShapeNormalizer().visit(normalized)
    return ast.dump(normalized, annotate_fields=True, include_attributes=False)


def ast_symbol_records(tree: dict[str, list[str]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path, source in source_tree_text(tree).items():
        parsed = ast.parse(source, filename=path)
        for node in ast.walk(parsed):
            if isinstance(node, ast.ClassDef):
                kind = "class"
            elif isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
                kind = "function"
            else:
                continue
            identity = _normalized_ast_dump(node, body_only=False)
            body = _normalized_ast_dump(node, body_only=True)
            body_digest = canonical_digest({"kind": kind, "body": body})
            lineage_digest = canonical_digest(
                {"kind": kind, "shape": _lineage_shape_dump(node, kind=kind)}
            )
            records.append(
                {
                    "name": node.name,
                    "kind": kind,
                    "path": path,
                    "start_line": node.lineno,
                    "end_line": getattr(node, "end_lineno", node.lineno),
                    "fingerprint": canonical_digest({"kind": kind, "identity": identity}),
                    "body_fingerprint": body_digest,
                    "lineage_id": f"lineage:{lineage_digest.removeprefix('sha256:')}",
                }
            )
    return sorted(records, key=lambda item: (item["path"], item["start_line"], item["name"]))


def provider_execution_fixture_errors() -> tuple[dict[str, Any], list[str]]:
    try:
        manifest = load_json(PROVIDER_EXECUTION_FIXTURE_PATH)
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"provider-fixture:load:{exc}"]
    errors = schema_errors(
        manifest,
        load_json(PROVIDER_EXECUTION_FIXTURE_SCHEMA_PATH),
        "provider-fixture",
    )
    cases = manifest.get("cases", [])
    fixture = load_json(FIXTURE_PATH)
    expected_ids = [case["case_id"] for case in fixture.get("cases", [])]
    actual_ids = [case.get("case_id") for case in cases if isinstance(case, dict)]
    if actual_ids != expected_ids:
        errors.append(issue("provider-fixture:case_order", "execution fixture must match refactor fixture order"))
    if len(actual_ids) != len(set(actual_ids)):
        errors.append(issue("provider-fixture:duplicate_case", "duplicate execution fixture case id"))
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            continue
        for label in ("before", "after"):
            tree = case.get(label, {})
            for path, lines in tree.items():
                if local_path_error(path) or not path.endswith(".py"):
                    errors.append(issue("provider-fixture:unsafe_path", f"cases[{index}].{label}:{path}"))
                if not isinstance(lines, list) or any(not isinstance(line, str) for line in lines):
                    errors.append(issue("provider-fixture:source_lines", f"cases[{index}].{label}:{path}"))
                else:
                    try:
                        ast.parse("\n".join(lines) + "\n", filename=path)
                    except SyntaxError as exc:
                        errors.append(issue("provider-fixture:syntax", f"{path}:{exc.msg}"))
        dependencies = case.get("test_dependencies", {})
        for source_path, test_paths in dependencies.items():
            if local_path_error(source_path) or any(
                local_path_error(test_path) or not test_path.startswith("tests/")
                for test_path in test_paths
            ):
                errors.append(issue("provider-fixture:test_path", source_path))
    return manifest, errors


def _symbol_key(symbol: dict[str, Any]) -> tuple[str, str, str]:
    return (symbol["path"], symbol["name"], symbol["kind"])


def _body_groups(symbols: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for symbol in symbols:
        groups.setdefault(symbol["body_fingerprint"], []).append(symbol)
    return groups


def _lineage_groups(symbols: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for symbol in symbols:
        groups.setdefault(symbol["lineage_id"], []).append(symbol)
    return groups


def _expected_execution_tests(
    scenario: dict[str, Any],
    changed: list[str],
    added: list[str],
    deleted: list[str],
    dependency_impacted: list[str],
) -> list[str]:
    selected: set[str] = set()
    dependencies = scenario.get("test_dependencies", {})
    for path in [*changed, *added, *deleted, *dependency_impacted]:
        selected.update(dependencies.get(path, []))
    return sorted(selected)


def provider_case_observation_errors(
    execution: dict[str, Any],
    fixture_case: dict[str, Any],
    scenario: dict[str, Any],
) -> list[str]:
    case_id = fixture_case["case_id"]
    observation = execution.get("observation")
    if not isinstance(observation, dict):
        return [issue("case_observation_missing", case_id)]

    before = scenario["before"]
    after = scenario["after"]
    changed, added, deleted = changed_source_paths(before, after)
    dependency_impacted = dependency_impacted_paths(before, after, changed, added, deleted)
    before_epoch = source_snapshot_digest(before)
    after_epoch = source_snapshot_digest(after)
    before_symbols = ast_symbol_records(before)
    after_symbols = ast_symbol_records(after)
    before_keys = {_symbol_key(symbol) for symbol in before_symbols}
    after_keys = {_symbol_key(symbol) for symbol in after_symbols}
    expected_added_symbols = sorted(after_keys - before_keys)
    expected_deleted_symbols = sorted(before_keys - after_keys)

    if observation.get("operation") != fixture_case["operation"]:
        errors = [issue("case_operation", f"{case_id}:{fixture_case['operation']}")]
    else:
        errors = []
    if execution.get("source_epoch") != after_epoch:
        errors.append(issue("case_source_epoch", case_id))
    if observation.get("source_epoch") != after_epoch:
        errors.append(issue("case_observation_source_epoch", case_id))
    if observation.get("before_snapshot_digest") != before_epoch:
        errors.append(issue("case_before_snapshot", case_id))
    if observation.get("after_snapshot_digest") != after_epoch:
        errors.append(issue("case_after_snapshot", case_id))
    if observation.get("changed_paths") != changed:
        errors.append(issue("case_changed_paths", case_id))
    if observation.get("added_paths") != added:
        errors.append(issue("case_added_paths", case_id))
    if observation.get("deleted_paths") != deleted:
        errors.append(issue("case_deleted_paths", case_id))
    if observation.get("dependency_impacted_paths") != dependency_impacted:
        errors.append(issue("case_dependency_impacted_paths", case_id))

    def projected(symbols: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                key: symbol[key]
                for key in (
                    "name",
                    "kind",
                    "path",
                    "start_line",
                    "end_line",
                    "fingerprint",
                    "body_fingerprint",
                    "lineage_id",
                )
            }
            for symbol in symbols
        ]

    if observation.get("before_symbols") != projected(before_symbols):
        errors.append(issue("case_before_symbols", case_id))
    if observation.get("after_symbols") != projected(after_symbols):
        errors.append(issue("case_after_symbols", case_id))
    actual_added_symbols = sorted(
        _symbol_key(symbol) for symbol in observation.get("added_symbols", [])
    )
    actual_deleted_symbols = sorted(
        _symbol_key(symbol) for symbol in observation.get("deleted_symbols", [])
    )
    if actual_added_symbols != expected_added_symbols:
        errors.append(issue("case_added_symbols", case_id))
    if actual_deleted_symbols != expected_deleted_symbols:
        errors.append(issue("case_deleted_symbols", case_id))

    lineage = observation.get("lineage", {})
    before_body_groups = _body_groups(before_symbols)
    after_body_groups = _body_groups(after_symbols)
    before_groups = _lineage_groups(before_symbols)
    after_groups = _lineage_groups(after_symbols)
    common_groups = sorted(set(before_groups) & set(after_groups))
    common_lineage_ids = common_groups
    expected_lineage = fixture_case["expected_lineage"]
    if lineage.get("posture") != expected_lineage:
        errors.append(issue("case_lineage_posture", case_id))
    if expected_lineage == "preserve":
        if lineage.get("stable_ids") != common_lineage_ids:
            errors.append(issue("case_lineage_stability", case_id))
        if lineage.get("alternatives") != 0 or lineage.get("confidence") != 1:
            errors.append(issue("case_lineage_confidence", case_id))
    elif expected_lineage == "branched":
        branch_count = max(
            [
                max(len(before_groups[lineage_id]), len(after_groups[lineage_id]))
                for lineage_id in common_groups
            ]
            or [0]
        )
        if lineage.get("stable_ids") != common_lineage_ids:
            errors.append(issue("case_lineage_stability", case_id))
        if lineage.get("alternatives", 0) < branch_count:
            errors.append(issue("case_lineage_alternatives", case_id))
        confidence = lineage.get("confidence", 1)
        if not isinstance(confidence, (int, float)) or not 0 < confidence < 1:
            errors.append(issue("case_lineage_confidence", case_id))
    elif lineage.get("stable_ids"):
        errors.append(issue("case_lineage_not_applicable", case_id))

    freshness = observation.get("freshness", {})
    if freshness.get("observed_source_epoch") != after_epoch:
        errors.append(issue("case_freshness_observed_epoch", case_id))
    expected_index_epoch = before_epoch if case_id == "stale-index" else after_epoch
    if freshness.get("indexed_source_epoch") != expected_index_epoch:
        errors.append(issue("case_freshness_index_epoch", case_id))
    expected_freshness = "stale" if case_id == "stale-index" else "exact"
    if freshness.get("status") != expected_freshness:
        errors.append(issue("case_freshness_status", case_id))

    deletion = observation.get("deletion", {})
    if case_id == "delete-entity":
        if deletion.get("status") != "confirmed":
            errors.append(issue("deletion_semantics", case_id))
        if deletion.get("before_present") != deleted:
            errors.append(issue("deletion_before_presence", case_id))
        if deletion.get("after_absent") != deleted:
            errors.append(issue("deletion_after_absence", case_id))
    elif deletion.get("status") != "not-applicable":
        errors.append(issue("deletion_semantics", case_id))

    affected_tests = observation.get("affected_tests", {})
    expected_tests = _expected_execution_tests(
        scenario, changed, added, deleted, dependency_impacted
    )
    if affected_tests.get("selected") != expected_tests:
        errors.append(issue("execution_affected_tests", case_id))
    expected_test_status = "selected" if expected_tests else "empty"
    if affected_tests.get("status") != expected_test_status:
        errors.append(issue("execution_affected_tests_status", case_id))
    expected_oracle = affected_test_oracle_ref(case_id)
    if affected_tests.get("oracle_ref") != expected_oracle:
        errors.append(issue("execution_affected_tests_oracle", case_id))
    try:
        canonical_tests = affected_test_oracle_selections().get(case_id)
    except (OSError, TypeError, AttributeError, KeyError, json.JSONDecodeError):
        canonical_tests = None
    if canonical_tests is None or affected_tests.get("selected") != canonical_tests:
        errors.append(issue("execution_affected_tests_oracle_selection", case_id))

    parity = observation.get("parity", {})
    if case_id == "delta-full-parity":
        if parity.get("status") != "equal":
            errors.append(issue("execution_parity", case_id))
        if not parity.get("full_projection_digest") or (
            parity.get("full_projection_digest") != parity.get("delta_projection_digest")
        ):
            errors.append(issue("execution_parity_digest", case_id))
    elif parity.get("status") != "not-run":
        errors.append(issue("execution_parity", case_id))

    operation = fixture_case["operation"]
    if operation == "rename":
        rename_match = any(
            before_symbol["body_fingerprint"] == after_symbol["body_fingerprint"]
            and before_symbol["path"] == after_symbol["path"]
            and before_symbol["name"] != after_symbol["name"]
            for before_symbol in before_symbols
            for after_symbol in after_symbols
        )
        if not rename_match or changed != ["src/alpha.py"]:
            errors.append(issue("execution_rename", case_id))
    elif operation == "move":
        move_match = any(
            before_symbol["body_fingerprint"] == after_symbol["body_fingerprint"]
            and before_symbol["name"] == after_symbol["name"]
            and before_symbol["path"] != after_symbol["path"]
            for before_symbol in before_symbols
            for after_symbol in after_symbols
        )
        if not move_match or not added or not deleted:
            errors.append(issue("execution_move", case_id))
    elif operation == "signature-change":
        signature_match = any(
            before_symbol["body_fingerprint"] == after_symbol["body_fingerprint"]
            and before_symbol["fingerprint"] != after_symbol["fingerprint"]
            for before_symbol in before_symbols
            for after_symbol in after_symbols
        )
        if not signature_match:
            errors.append(issue("execution_signature", case_id))
    elif operation == "add" and not expected_added_symbols:
        errors.append(issue("execution_add", case_id))
    elif operation == "delete" and not deleted:
        errors.append(issue("execution_delete", case_id))
    elif operation == "imports":
        if not any(
            source_import_modules(path, source_tree_text(before)[path])
            != source_import_modules(path, source_tree_text(after)[path])
            for path in changed
        ):
            errors.append(issue("execution_imports", case_id))
    elif operation == "multi-file-impact" and len(changed) < 2:
        errors.append(issue("execution_multi_file", case_id))
    elif operation == "split" and not any(
        len(before_body_groups[fingerprint]) == 1
        and len(after_body_groups[fingerprint]) >= 2
        for fingerprint in sorted(set(before_body_groups) & set(after_body_groups))
    ):
        errors.append(issue("execution_split", case_id))
    elif operation == "merge" and not any(
        len(before_body_groups[fingerprint]) >= 2
        and len(after_body_groups[fingerprint]) == 1
        for fingerprint in sorted(set(before_body_groups) & set(after_body_groups))
    ):
        errors.append(issue("execution_merge", case_id))
    elif operation == "freshness-drift":
        if execution.get("status") != "degraded":
            errors.append(issue("execution_stale_status", case_id))
    return errors


def local_path_error(path: str) -> bool:
    """Return whether a provider path escapes the declared local universe."""

    if not isinstance(path, str) or not path or "\x00" in path:
        return True
    posix_path = PurePosixPath(path)
    first_component = path.split("/", 1)[0]
    return (
        posix_path.is_absolute()
        or ".." in posix_path.parts
        or "//" in path
        or "\\" in path
        or "://" in path
        or ":" in first_component
    )


def provider_execution_errors(
    envelope: dict[str, Any],
) -> tuple[list[str], list[str]]:
    """Validate actual provider state binding without issuing a proof verdict."""

    errors = schema_errors(
        envelope,
        load_json(PROVIDER_EXECUTION_SCHEMA_PATH),
        "provider-execution",
    )
    if errors:
        return errors, []

    manifest, fixture_errors_found = validate_manifest()
    errors.extend(f"fixture:{error}" for error in fixture_errors_found)
    execution_fixture, execution_fixture_errors = provider_execution_fixture_errors()
    errors.extend(execution_fixture_errors)
    known_case_order = [
        case["case_id"]
        for case in manifest.get("cases", [])
        if isinstance(case, dict) and isinstance(case.get("case_id"), str)
    ]
    known_case_ids = set(known_case_order)

    binding = envelope["machine_binding"]
    if binding["contract_schema"] != MACHINE_CONTRACT_SCHEMA:
        errors.append(issue("machine_contract_schema", MACHINE_CONTRACT_SCHEMA))
    if binding["contract_ref"] != MACHINE_CONTRACT_REF:
        errors.append(issue("machine_contract_ref", MACHINE_CONTRACT_REF))
    if binding["contract_digest"] != MACHINE_CONTRACT_DIGEST:
        errors.append(issue("machine_contract_digest", MACHINE_CONTRACT_DIGEST))
    if binding["contract_digest_kind"] != MACHINE_CONTRACT_DIGEST_KIND:
        errors.append(issue("machine_contract_digest_kind", MACHINE_CONTRACT_DIGEST_KIND))
    if binding["contract_snapshot_epoch"] != MACHINE_CONTRACT_SNAPSHOT_EPOCH:
        errors.append(issue("machine_contract_snapshot_epoch", MACHINE_CONTRACT_SNAPSHOT_EPOCH))
    if binding["workspace_manifest_digest"] != MACHINE_WORKSPACE_MANIFEST_DIGEST:
        errors.append(issue("machine_workspace_manifest_digest", MACHINE_WORKSPACE_MANIFEST_DIGEST))
    if binding["provider_id"] != MACHINE_PROVIDER_ID:
        errors.append(issue("machine_provider_id", MACHINE_PROVIDER_ID))
    if binding["owner_bindings"] != OWNER_BINDINGS:
        errors.append(issue("owner_bindings", "owner split differs from the machine contract"))
    if binding["admission_state"] == "admitted" and not binding["admission_receipt_ref"]:
        errors.append(issue("admission_receipt", "admitted state requires a receipt reference"))

    current_contract_digest = binding.get("current_contract_digest")
    snapshot_currentness = binding.get("snapshot_currentness")
    if snapshot_currentness == "unobserved":
        if current_contract_digest is not None:
            errors.append(
                issue(
                    "snapshot_currentness",
                    "unobserved cannot be paired with a current digest",
                )
            )
    elif current_contract_digest is None:
        if snapshot_currentness is not None:
            errors.append(
                issue(
                    "snapshot_currentness",
                    "a currentness classification requires current_contract_digest",
                )
            )
    else:
        if current_contract_digest == MACHINE_CONTRACT_DIGEST:
            if snapshot_currentness != "matches_reviewed_snapshot":
                errors.append(
                    issue(
                        "snapshot_currentness",
                        "matching current digest requires matches_reviewed_snapshot",
                    )
                )
        elif snapshot_currentness != "drifted":
            errors.append(
                issue(
                    "snapshot_currentness",
                    "a different current digest requires drifted",
                )
            )
        if binding["admission_state"] == "admitted" and snapshot_currentness == "drifted":
            errors.append(
                issue(
                    "admission_snapshot_drift",
                    "admitted state cannot be claimed against a drifted snapshot",
                )
            )

    provider = envelope["provider"]
    if provider["id"] != binding["provider_id"]:
        errors.append(issue("provider_id", "provider and machine binding differ"))

    run = envelope["run"]
    seen_case_ids: set[str] = set()
    observed_case_order: list[str] = []
    coverage = envelope.get("coverage")
    complete_coverage = isinstance(coverage, dict) and coverage.get("mode") == "complete"
    execution_cases = {
        case["case_id"]: case
        for case in execution_fixture.get("cases", [])
        if isinstance(case, dict) and isinstance(case.get("case_id"), str)
    }
    fixture_cases = {
        case["case_id"]: case
        for case in manifest.get("cases", [])
        if isinstance(case, dict) and isinstance(case.get("case_id"), str)
    }
    if complete_coverage:
        if envelope.get("execution_posture") != "source-bound-provider-candidate":
            errors.append(issue("execution_posture", "complete coverage requires source-bound posture"))
        provider = envelope.get("provider", {})
        expected_provider = execution_fixture.get("provider", {})
        if provider.get("id") != expected_provider.get("id"):
            errors.append(issue("execution_provider_id", "provider execution fixture identity differs"))
        if provider.get("version") != expected_provider.get("version"):
            errors.append(issue("execution_provider_version", "provider execution fixture version differs"))
    for index, execution in enumerate(envelope["executions"]):
        location = f"execution[{index}]"
        case_id = execution["case_id"]
        observed_case_order.append(case_id)
        if case_id not in known_case_ids:
            errors.append(issue("unknown_case", f"{location}:{case_id}"))
        if case_id in seen_case_ids:
            errors.append(issue("duplicate_case", case_id))
        seen_case_ids.add(case_id)

        if execution["environment_digest"] != run["environment_digest"]:
            errors.append(issue("environment_digest", location))
        if not math.isfinite(execution["latency_ms"]):
            errors.append(issue("latency", f"{location}:not-finite"))
        state = execution["provider_state"]
        state_provider = state["provider"]
        state_source = state["source"]
        state_config = state["config"]
        state_invalidation = state["invalidation"]
        state_freshness = state["freshness"]
        state_provenance = state["provenance"]

        if state_provider.get("id") != provider["id"]:
            errors.append(issue("state_provider_id", location))
        if state_provider.get("version") != provider["version"]:
            errors.append(issue("state_provider_version", location))
        if state_config.get("digest") != provider["config_digest"]:
            errors.append(issue("state_config_digest", location))
        if state_source.get("source_epoch") != execution["source_epoch"]:
            errors.append(issue("state_source_epoch", location))
        if state_freshness.get("source_epoch") != execution["source_epoch"]:
            errors.append(issue("freshness_source_epoch", location))
        freshness_provider = state_freshness.get("provider")
        if not isinstance(freshness_provider, dict) or freshness_provider != state_provider:
            errors.append(issue("freshness_provider", location))
        if state_provenance.get("runtime_owner") != "abyss-stack":
            errors.append(issue("runtime_owner", location))
        if state_provenance.get("observation_meaning_owner") != "aoa-kag":
            errors.append(issue("observation_meaning_owner", location))
        if state_provenance.get("proof_owner") != "aoa-evals":
            errors.append(issue("proof_owner", location))
        if state_provenance.get("full_rebuild") != state_invalidation.get("full_rebuild"):
            errors.append(issue("full_rebuild_provenance", location))
        if execution["mode"] == "full" and not state_invalidation["full_rebuild"]:
            errors.append(issue("full_mode", f"{location}:state is incremental"))
        if execution["mode"] == "delta" and state_invalidation["full_rebuild"]:
            errors.append(issue("delta_mode", f"{location}:state is a full rebuild"))
        if execution["status"] == "completed" and state["status"] != "current":
            errors.append(issue("execution_status", location))
        if execution["status"] == "degraded" and state["status"] != "degraded":
            errors.append(issue("execution_status", location))

        invalidated = set(state_invalidation["invalidated_paths"])
        deleted = set(state_invalidation["deleted_paths"])
        dependency_impacted = set(state_invalidation["dependency_impacted_paths"])
        reused = set(state_invalidation["reused_paths"])
        universe = state_invalidation["blast_radius_universe"]
        universe_paths = set(universe["paths"])

        path_fields = (
            "changed_paths",
            "added_paths",
            "deleted_paths",
            "dependency_impacted_paths",
            "invalidated_paths",
            "reused_paths",
        )
        for field in path_fields:
            values = state_invalidation[field]
            for path in values:
                if local_path_error(path):
                    errors.append(issue("unsafe_path", f"{location}:{field}:{path}"))
            if not set(values).issubset(universe_paths):
                errors.append(issue("path_outside_universe", f"{location}:{field}"))
        for path in universe["paths"]:
            if local_path_error(path):
                errors.append(issue("unsafe_path", f"{location}:blast_radius_universe:{path}"))

        if universe["count"] < 1:
            errors.append(issue("blast_radius_universe_empty", location))
        if case_id == "delete-entity" and not deleted:
            errors.append(issue("deletion_event_missing", location))
        if not (set(state_invalidation["changed_paths"]) | set(state_invalidation["added_paths"]) | deleted).issubset(invalidated):
            errors.append(issue("invalidation_event_not_invalidated", location))
        if not deleted.issubset(invalidated):
            errors.append(issue("deleted_not_invalidated", location))
        if not dependency_impacted.issubset(invalidated):
            errors.append(issue("dependency_not_invalidated", location))
        if invalidated.intersection(reused):
            errors.append(issue("invalidated_reused_overlap", location))
        if universe["count"] != len(universe["paths"]):
            errors.append(issue("blast_radius_universe_count", location))
        if not invalidated.issubset(universe_paths):
            errors.append(issue("blast_radius_universe_membership", location))
        expected_blast_radius = round(
            len(invalidated) / universe["count"], 6
        ) if universe["count"] else 0.0
        if state_invalidation["blast_radius"] != expected_blast_radius:
            errors.append(issue("blast_radius_denominator", location))

        if execution["state_digest"] != canonical_digest(state):
            errors.append(issue("state_digest", location))
        if run["reproducibility_state"] == "deterministic":
            repeated_digest = execution["repeated_state_digest"]
            if repeated_digest != stable_provider_state_digest(state):
                errors.append(issue("reproducibility", location))
        full_projection = execution["full_state_projection_digest"]
        delta_projection = execution["delta_state_projection_digest"]
        if (full_projection is None) != (delta_projection is None):
            errors.append(issue("parity_projection", location))
        if full_projection is not None and full_projection != delta_projection:
            errors.append(issue("parity_projection", f"{location}:different"))

        if complete_coverage:
            if not invalidated:
                errors.append(issue("complete_invalidation", location))
            if state_invalidation["full_rebuild"]:
                if invalidated != universe_paths:
                    errors.append(issue("full_rebuild_universe", location))
                if reused:
                    errors.append(issue("full_rebuild_reused_paths", location))
            if execution["repeated_state_digest"] is None:
                errors.append(issue("reproducibility_required", location))
            if case_id == "delta-full-parity":
                if full_projection is None or delta_projection is None:
                    errors.append(issue("parity_required", location))

            scenario = execution_cases.get(case_id)
            fixture_case = fixture_cases.get(case_id)
            if scenario is None or fixture_case is None:
                errors.append(issue("case_observation_fixture_missing", location))
            else:
                errors.extend(
                    f"{location}:{error}"
                    for error in provider_case_observation_errors(
                        execution, fixture_case, scenario
                    )
                )
                changed, added, deleted = changed_source_paths(
                    scenario["before"], scenario["after"]
                )
                dependency_impacted = dependency_impacted_paths(
                    scenario["before"], scenario["after"], changed, added, deleted
                )
                expected_invalidated = set(
                    [*changed, *added, *deleted, *dependency_impacted]
                )
                expected_universe = set(scenario["before"]) | set(scenario["after"])
                expected_full_rebuild = case_id == "delta-full-parity"
                expected_reused = (
                    set() if expected_full_rebuild else expected_universe - expected_invalidated
                )
                for field, expected in (
                    ("changed_paths", changed),
                    ("added_paths", added),
                    ("deleted_paths", deleted),
                    ("dependency_impacted_paths", dependency_impacted),
                    ("invalidated_paths", sorted(expected_invalidated)),
                    ("reused_paths", sorted(expected_reused)),
                ):
                    if state_invalidation.get(field) != expected:
                        errors.append(issue("execution_invalidation", f"{location}:{field}"))
                if state_invalidation.get("full_rebuild") != expected_full_rebuild:
                    errors.append(issue("execution_rebuild_mode", location))
                if state_invalidation.get("blast_radius_universe", {}).get("paths") != sorted(expected_universe):
                    errors.append(issue("execution_invalidation_universe", location))

    if coverage is not None:
        declared_case_order = coverage["case_ids"]
        if declared_case_order != observed_case_order:
            errors.append(issue("coverage_case_ids", "declaration differs from executions"))
        if coverage["mode"] == "complete":
            if declared_case_order != known_case_order:
                errors.append(issue("coverage_complete", "complete coverage must match the fixture order"))
            if observed_case_order != known_case_order:
                errors.append(issue("coverage_complete", "complete coverage must execute every fixture case once"))
            if run["reproducibility_state"] != "deterministic":
                errors.append(issue("reproducibility_required", "complete coverage requires deterministic runs"))

    return errors, sorted(seen_case_ids)


def schema_errors(instance: Any, schema: dict[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "$"
        errors.append(f"{label}:{location}: {error.message}")
    return errors


def fixture_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != "aoa_refactor_torture_fixture_v1":
        errors.append("fixture:$: unexpected schema_version")
    if manifest.get("family_id") != "refactor-torture-v1":
        errors.append("fixture:family_id: expected refactor-torture-v1")
    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        return errors + ["fixture:cases: expected a non-empty list"]
    case_ids = [case.get("case_id") for case in cases if isinstance(case, dict)]
    if len(case_ids) != len(set(case_ids)):
        errors.append("fixture:cases: duplicate case_id")
    required = {
        "case_id",
        "operation",
        "expected_lineage",
        "expected_freshness",
        "expected_invalidation_scope",
        "required_planes",
        "required_metrics",
    }
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or not required.issubset(case):
            errors.append(f"fixture:cases[{index}]: missing case contract field")
    errors.extend(affected_test_oracle_errors(manifest, case_ids))
    return errors


def issue(code: str, detail: str) -> str:
    return f"{code}:{detail}"


def affected_test_oracle_ref(case_id: str) -> str:
    return f"{AFFECTED_TEST_ORACLE_REPO_PATH}#{case_id}"


def affected_test_oracle_selections() -> dict[str, list[str]]:
    """Return the canonical checked-in selection for each fixture case."""

    oracle = load_json(AFFECTED_TEST_ORACLE_PATH)
    return {
        case["case_id"]: case["selected"]
        for case in oracle.get("cases", [])
        if isinstance(case, dict)
        and isinstance(case.get("case_id"), str)
        and isinstance(case.get("selected"), list)
    }


def affected_test_oracle_errors(
    manifest: dict[str, Any], case_ids: list[str | None]
) -> list[str]:
    errors: list[str] = []
    if manifest.get("affected_test_oracle_path") != AFFECTED_TEST_ORACLE_MANIFEST_PATH:
        errors.append(
            issue(
                "fixture:affected_test_oracle_path",
                f"expected {AFFECTED_TEST_ORACLE_MANIFEST_PATH}",
            )
        )
    try:
        oracle = load_json(AFFECTED_TEST_ORACLE_PATH)
    except (OSError, json.JSONDecodeError) as exc:
        return errors + [issue("fixture:affected_test_oracle", str(exc))]

    if manifest.get("affected_test_oracle_digest") != canonical_digest(oracle):
        errors.append(issue("fixture:affected_test_oracle_digest", "digest mismatch"))
    if not isinstance(oracle, dict):
        return errors + [issue("fixture:affected_test_oracle", "expected an object")]
    if oracle.get("schema_version") != "aoa_refactor_torture_affected_test_oracle_v1":
        errors.append(issue("fixture:affected_test_oracle", "unexpected schema_version"))
    if oracle.get("family_id") != manifest.get("family_id"):
        errors.append(issue("fixture:affected_test_oracle", "family_id mismatch"))

    oracle_cases = oracle.get("cases")
    if not isinstance(oracle_cases, list) or not oracle_cases:
        return errors + [issue("fixture:affected_test_oracle", "expected a non-empty list")]
    oracle_ids = [
        case.get("case_id") for case in oracle_cases if isinstance(case, dict)
    ]
    if len(oracle_ids) != len(set(oracle_ids)):
        errors.append(issue("fixture:affected_test_oracle", "duplicate case_id"))
    if set(oracle_ids) != set(case_ids):
        errors.append(issue("fixture:affected_test_oracle", "case coverage mismatch"))
    for index, case in enumerate(oracle_cases):
        if not isinstance(case, dict):
            errors.append(issue("fixture:affected_test_oracle", f"cases[{index}] is not an object"))
            continue
        selected = case.get("selected")
        if not isinstance(selected, list) or any(
            not isinstance(path, str) or not path for path in selected
        ):
            errors.append(
                issue(
                    "fixture:affected_test_oracle",
                    f"cases[{index}].selected must be a list of non-empty paths",
                )
            )
            continue
        if len(selected) != len(set(selected)):
            errors.append(
                issue(
                    "fixture:affected_test_oracle",
                    f"cases[{index}].selected contains duplicates",
                )
            )
        for path in selected:
            posix_path = PurePosixPath(path)
            if (
                posix_path.is_absolute()
                or ".." in posix_path.parts
                or not path.startswith("tests/")
                or "://" in path
            ):
                errors.append(
                    issue(
                        "fixture:affected_test_oracle",
                        f"cases[{index}].selected path is not local: {path}",
                    )
                )
    return errors


def semantic_case_issues(
    observation: dict[str, Any],
    case: dict[str, Any],
    report: dict[str, Any],
    affected_test_oracles: dict[str, dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    case_id = case["case_id"]
    if observation.get("operation") != case["operation"]:
        errors.append(issue("operation_mismatch", f"{case_id} declares {case['operation']}"))

    observed_planes = set(observation.get("planes", []))
    required_planes = set(case["required_planes"])
    if not required_planes.issubset(observed_planes):
        errors.append(issue("missing_plane", f"{case_id} requires {sorted(required_planes)}"))

    lineage = observation.get("lineage", {})
    if lineage.get("posture") != case["expected_lineage"]:
        errors.append(issue("lineage_posture_mismatch", f"{case_id} expects {case['expected_lineage']}"))
    if case["expected_lineage"] == "branched":
        if lineage.get("alternatives", 0) < 1 or lineage.get("confidence", 1) >= 1:
            errors.append(issue("ambiguity_not_exposed", f"{case_id} requires alternatives and sub-certainty"))

    freshness = observation.get("freshness", {})
    if freshness.get("status") != case["expected_freshness"]:
        errors.append(issue("freshness_mismatch", f"{case_id} expects {case['expected_freshness']}"))
    if case["expected_freshness"] == "stale" and observation.get("evidence_state") != "stale":
        errors.append(issue("stale_state_missing", f"{case_id} must disclose stale evidence"))

    invalidation = observation.get("invalidation", {})
    if invalidation.get("scope") != case["expected_invalidation_scope"]:
        errors.append(
            issue(
                "invalidation_scope_mismatch",
                f"{case_id} expects {case['expected_invalidation_scope']}",
            )
        )
    if case["expected_invalidation_scope"] != "full" and invalidation.get("scope") == "full":
        errors.append(issue("ordinary_case_full_rebuild", f"{case_id} hides bounded invalidation"))

    metric_map = {metric.get("metric_id"): metric for metric in observation.get("metrics", [])}
    for metric_id in case["required_metrics"]:
        metric = metric_map.get(metric_id)
        if metric is None:
            errors.append(issue("missing_metric", f"{case_id}:{metric_id}"))
        elif metric.get("value") is None or metric.get("status") != "observed":
            errors.append(issue("metric_not_observed", f"{case_id}:{metric_id}"))

    provenance = observation.get("provenance", {})
    provider = report["provider"]
    source_epoch = report["source_epoch"]
    if provenance.get("provider_ref") != provider["id"]:
        errors.append(issue("provider_provenance_mismatch", case_id))
    if provenance.get("config_ref") != provider["config_digest"]:
        errors.append(issue("config_provenance_mismatch", case_id))
    if provenance.get("source_epoch_ref") != source_epoch["revision"]:
        errors.append(issue("source_epoch_provenance_mismatch", case_id))
    if freshness.get("source_epoch_ref") != source_epoch["revision"]:
        errors.append(issue("freshness_epoch_mismatch", case_id))

    if case_id in {"split-symbol", "merge-symbol"} and observation.get("evidence_state") != "ambiguous":
        errors.append(issue("ambiguity_state_missing", case_id))

    if case_id == "delta-full-parity":
        if invalidation.get("delta_full_parity") != "equal":
            errors.append(issue("delta_full_parity_failed", case_id))
        reproducibility = report["run"]["reproducibility"]
        if reproducibility.get("state") != "deterministic":
            errors.append(issue("reproducibility_not_deterministic", case_id))

    if "affected_tests" in case["required_metrics"]:
        affected_tests = observation.get("affected_tests", {})
        if affected_tests.get("status") not in {"selected", "empty"}:
            errors.append(issue("affected_tests_not_classified", case_id))
        oracle = affected_test_oracles.get(case_id)
        oracle_ref = affected_tests.get("oracle_ref")
        if not oracle_ref:
            errors.append(issue("affected_tests_oracle_missing", case_id))
        elif oracle_ref != affected_test_oracle_ref(case_id):
            errors.append(
                issue(
                    "affected_tests_oracle_mismatch",
                    f"{case_id} must use {affected_test_oracle_ref(case_id)}",
                )
            )
        if oracle is None:
            errors.append(issue("affected_tests_oracle_unavailable", case_id))
        elif affected_tests.get("selected") != oracle.get("selected"):
            errors.append(issue("affected_tests_selection_mismatch", case_id))

    return errors


def validate_manifest() -> tuple[dict[str, Any], list[str]]:
    manifest = load_json(FIXTURE_PATH)
    errors = fixture_errors(manifest)
    return manifest, errors


def validate_report(report_path: Path) -> tuple[dict[str, Any], list[str], dict[str, list[str]]]:
    manifest, errors = validate_manifest()
    report = load_json(report_path)
    errors.extend(schema_errors(report, load_json(REPORT_SCHEMA_PATH), "report"))
    breakdown: dict[str, list[str]] = {}
    if errors:
        return report, errors, breakdown

    expected_digest = canonical_digest(manifest)
    if report["run"]["fixture_digest"] != expected_digest:
        errors.append(issue("fixture_digest_mismatch", expected_digest))
    if not {"live", "indexed"}.issubset(set(report["run"]["planes"])):
        errors.append(issue("overall_plane_coverage_missing", "report requires live and indexed"))

    cases = manifest["cases"]
    cases_by_id = {case["case_id"]: case for case in cases}
    affected_test_oracle = load_json(AFFECTED_TEST_ORACLE_PATH)
    affected_test_oracles = {
        case["case_id"]: case for case in affected_test_oracle["cases"]
    }
    observations = report["observations"]
    observations_by_id: dict[str, dict[str, Any]] = {}
    occurrence_counts: dict[str, int] = {}
    for index, observation in enumerate(observations):
        case_id = observation["case_id"]
        occurrence = occurrence_counts.get(case_id, 0)
        occurrence_counts[case_id] = occurrence + 1
        if occurrence == 0:
            observations_by_id[case_id] = observation

        observation_errors: list[str] = []
        if occurrence > 0:
            observation_errors.append(issue("duplicate_case", case_id))
        if case_id not in cases_by_id:
            observation_errors.append(issue("unexpected_case", case_id))
        if observation_errors:
            extra_key = f"observation-{index}-{case_id}"
            breakdown[extra_key] = observation_errors
            errors.extend(observation_errors)

    for case in cases:
        case_id = case["case_id"]
        observation = observations_by_id.get(case_id)
        if observation is None:
            breakdown[case_id] = [issue("missing_case", case_id)]
            errors.extend(breakdown[case_id])
            continue
        case_errors = semantic_case_issues(
            observation, case, report, affected_test_oracles
        )
        breakdown[case_id] = case_errors
        errors.extend(case_errors)

    return report, errors, breakdown


def build_summary(report: dict[str, Any], errors: list[str], breakdown: dict[str, list[str]]) -> dict[str, Any]:
    cases = load_json(FIXTURE_PATH)["cases"]
    known_case_ids = {case["case_id"] for case in cases}
    per_case: list[dict[str, Any]] = []
    for case in cases:
        case_id = case["case_id"]
        if case_id in breakdown:
            case_errors = breakdown[case_id]
        elif errors:
            case_errors = [issue("report_unavailable", case_id)]
        else:
            case_errors = [issue("missing_case", case_id)]
        passed = not case_errors
        per_case.append(
            {
                "case_id": case_id,
                "expected": "pass",
                "observed": "pass" if passed else "reject",
                "issue_codes": sorted(case_errors),
                "outcome": "pass" if passed else "fail",
            }
        )

    represented_errors = {
        error for case_errors in breakdown.values() for error in case_errors
    }
    global_errors = sorted(set(errors) - represented_errors)
    if global_errors and breakdown:
        per_case.append(
            {
                "case_id": "report-contract",
                "expected": "reject",
                "observed": "reject",
                "issue_codes": global_errors,
                "outcome": "fail",
            }
        )

    for extra_case_id, case_errors in breakdown.items():
        if extra_case_id in known_case_ids:
            continue
        per_case.append(
            {
                "case_id": extra_case_id,
                "expected": "reject",
                "observed": "reject",
                "issue_codes": sorted(case_errors),
                "outcome": "fail",
            }
        )

    passed_count = sum(item["outcome"] == "pass" for item in per_case)
    failed_count = len(per_case) - passed_count
    return {
        "eval_name": "aoa-code-observation-refactor-integrity",
        "bundle_status": "draft",
        "object_under_evaluation": "provider-neutral code-observation envelope under controlled refactor cases",
        "verdict": "supports bounded contract" if not errors else "does not support bounded contract",
        "claim_boundary": "A positive result supports only internal completeness and coherence of the supplied synthetic observation envelope; it is not provider correctness, canonical owner truth, or proof acceptance.",
        "limitations": SUMMARY_LIMITATIONS,
        "scenario_count": len(per_case),
        "passed_count": passed_count,
        "failed_count": failed_count,
        "per_scenario_breakdown": per_case,
    }


def command_validate_fixture() -> int:
    manifest, errors = validate_manifest()
    execution_fixture, execution_fixture_errors = provider_execution_fixture_errors()
    errors.extend(execution_fixture_errors)
    result = {
        "valid": not errors,
        "family_id": manifest.get("family_id"),
        "case_count": len(manifest.get("cases", [])),
        "fixture_digest": canonical_digest(manifest),
        "affected_test_oracle_path": manifest.get("affected_test_oracle_path"),
        "affected_test_oracle_digest": manifest.get("affected_test_oracle_digest"),
        "provider_execution_fixture_case_count": len(execution_fixture.get("cases", [])),
        "provider_execution_fixture_digest": canonical_digest(execution_fixture)
        if execution_fixture
        else None,
        "errors": errors,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


def command_validate_report(report_path: Path) -> int:
    _report, errors, _breakdown = validate_report(report_path)
    result = {"valid": not errors, "report": str(report_path), "errors": errors}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


def command_validate_provider_execution(execution_path: Path) -> int:
    envelope = load_json(execution_path)
    errors, case_ids = provider_execution_errors(envelope)
    machine_binding = envelope.get("machine_binding")
    if not isinstance(machine_binding, dict):
        machine_binding = {}
    provider = envelope.get("provider")
    if not isinstance(provider, dict):
        provider = {}
    coverage = envelope.get("coverage")
    if not isinstance(coverage, dict):
        coverage = {}
    result = {
        "valid": not errors,
        "execution": str(execution_path),
        "provider_id": provider.get("id"),
        "machine_contract_ref": machine_binding.get("contract_ref"),
        "machine_contract_digest": machine_binding.get("contract_digest"),
        "machine_contract_digest_kind": machine_binding.get("contract_digest_kind"),
        "machine_contract_snapshot_epoch": machine_binding.get("contract_snapshot_epoch"),
        "machine_workspace_manifest_digest": machine_binding.get("workspace_manifest_digest"),
        "admission_state": machine_binding.get("admission_state"),
        "snapshot_currentness": machine_binding.get("snapshot_currentness"),
        "coverage_mode": coverage.get("mode"),
        "coverage_case_count": len(coverage.get("case_ids", [])),
        "case_ids": case_ids,
        "claim_boundary": (
            "Provider state is bound to the reviewed machine contract and the "
            "refactor fixture case IDs; this is not admission, a proof verdict, "
            "or owner acceptance."
        ),
        "errors": errors,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


def command_collect_provider_evidence() -> int:
    import provider_evidence

    evidence = provider_evidence.collect_evidence()
    errors = provider_evidence.schema_errors(evidence)
    if not errors:
        errors.extend(provider_evidence.semantic_errors(evidence))
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0 if not errors else 1


def command_execute_provider() -> int:
    import provider_execution

    try:
        envelope = provider_execution.execute()
    except (OSError, ValueError, RuntimeError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1
    errors, _case_ids = provider_execution_errors(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0 if not errors else 1


def command_validate_provider_evidence(evidence_path: Path) -> int:
    import provider_evidence

    evidence, errors = provider_evidence.validate_evidence(evidence_path)
    evidence_object = evidence if isinstance(evidence, dict) else {}
    raw_providers = evidence_object.get("providers", [])
    if not isinstance(raw_providers, list):
        raw_providers = []
    providers = [
        {
            "id": provider.get("id"),
            "availability": provider.get("availability"),
            "admission_state": provider.get("admission_state"),
            "case_count": len(provider.get("case_ids", [])),
            "observed_count": sum(
                observation.get("status") == "observed"
                for observation in provider.get("observations", [])
            ),
        }
        for provider in raw_providers
        if isinstance(provider, dict)
    ]
    result = {
        "valid": not errors,
        "evidence": str(evidence_path),
        "family_id": evidence_object.get("family_id"),
        "providers": providers,
        "claim_boundary": provider_evidence.CLAIM_BOUNDARY,
        "errors": errors,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


def command_run_scenarios(report_path: Path) -> int:
    report, errors, breakdown = validate_report(report_path)
    summary = build_summary(report, errors, breakdown)
    summary_errors = schema_errors(
        summary, load_json(SUMMARY_SCHEMA_PATH), "summary"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    if summary_errors:
        print("summary validation failed:", file=sys.stderr)
        print("\n".join(summary_errors), file=sys.stderr)
    return 0 if not errors and not summary_errors else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate-fixture")

    validate_report_parser = subparsers.add_parser("validate-report")
    validate_report_parser.add_argument("report", nargs="?", type=Path, default=EXAMPLE_REPORT_PATH)

    provider_execution_parser = subparsers.add_parser("validate-provider-execution")
    provider_execution_parser.add_argument("execution", type=Path)

    subparsers.add_parser("collect-provider-evidence")
    subparsers.add_parser("execute-provider")

    provider_evidence_parser = subparsers.add_parser("validate-provider-evidence")
    provider_evidence_parser.add_argument("evidence", type=Path)

    run_parser = subparsers.add_parser("run-scenarios")
    run_parser.add_argument("report", nargs="?", type=Path, default=EXAMPLE_REPORT_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "validate-fixture":
        return command_validate_fixture()
    if args.command == "validate-report":
        return command_validate_report(args.report)
    if args.command == "validate-provider-execution":
        return command_validate_provider_execution(args.execution)
    if args.command == "collect-provider-evidence":
        return command_collect_provider_evidence()
    if args.command == "execute-provider":
        return command_execute_provider()
    if args.command == "validate-provider-evidence":
        return command_validate_provider_evidence(args.evidence)
    if args.command == "run-scenarios":
        return command_run_scenarios(args.report)
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    sys.exit(main())
