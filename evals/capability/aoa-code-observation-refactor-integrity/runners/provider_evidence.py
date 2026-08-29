"""Collect and validate bounded local Python-AST and Ctags evidence."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import platform
import shutil
import subprocess
from datetime import datetime, timezone
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
SOURCE_MANIFEST_PATH = BUNDLE_ROOT / "fixtures" / "provider-evidence" / "manifest.json"
SOURCE_ROOT = BUNDLE_ROOT / "fixtures" / "provider-evidence" / "source"
SCHEMA_PATH = BUNDLE_ROOT / "schemas" / "provider-observation-evidence.schema.json"

FAMILY_ID = "refactor-torture-v1"
EVIDENCE_SCHEMA_VERSION = "aoa_code_observation_provider_evidence_v1"
SOURCE_MANIFEST_SCHEMA_VERSION = "aoa_code_observation_provider_source_manifest_v1"
CLAIM_BOUNDARY = (
    "These observations expose symbols in a checked-in synthetic source snapshot; "
    "they do not establish provider correctness, refactor truth, currentness "
    "outside the snapshot, installation, trust, admission, KAG meaning, proof, "
    "or owner acceptance."
)
CLAIM_LIMITS = [
    "synthetic source visibility only; not provider correctness or refactor proof",
    "not admitted and not canonical owner truth",
    "source snapshot and host-tool observations are not production runtime evidence",
]


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def raw_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def source_files() -> list[Path]:
    return sorted(path for path in SOURCE_ROOT.rglob("*.py") if path.is_file())


def source_root_digest() -> str:
    records = [
        {"path": path.relative_to(SOURCE_ROOT).as_posix(), "sha256": raw_digest(path)}
        for path in source_files()
    ]
    return canonical_digest(records)


def expected_cases() -> tuple[dict[str, Any], dict[str, Any]]:
    fixture = load_json(FIXTURE_PATH)
    source_manifest = load_json(SOURCE_MANIFEST_PATH)
    if fixture.get("family_id") != FAMILY_ID:
        raise ValueError("refactor-torture fixture family id drifted")
    if source_manifest.get("schema_version") != SOURCE_MANIFEST_SCHEMA_VERSION:
        raise ValueError("provider source manifest schema version drifted")
    if source_manifest.get("family_id") != FAMILY_ID:
        raise ValueError("provider source manifest family id drifted")
    fixture_ids = [case["case_id"] for case in fixture["cases"]]
    source_ids = [case["case_id"] for case in source_manifest["cases"]]
    if len(fixture_ids) != len(set(fixture_ids)) or len(source_ids) != len(set(source_ids)):
        raise ValueError("duplicate provider evidence case id")
    if fixture_ids != source_ids:
        raise ValueError("provider source manifest does not cover fixture cases in order")
    if source_manifest.get("source_root") != "source":
        raise ValueError("provider source manifest must use its local source root")
    files = source_files()
    if not files:
        raise ValueError("provider evidence source root is empty")
    return fixture, source_manifest


def observation_paths() -> list[str]:
    return [path.relative_to(SOURCE_ROOT).as_posix() for path in source_files()]


def python_symbols() -> dict[tuple[str, str], dict[str, Any]]:
    found: dict[tuple[str, str], dict[str, Any]] = {}
    for path in source_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        relative_path = path.relative_to(SOURCE_ROOT).as_posix()
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                kind = "class"
            elif isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
                kind = "function"
            else:
                continue
            end_line = getattr(node, "end_lineno", node.lineno)
            found[(node.name, kind)] = {
                "name": node.name,
                "kind": kind,
                "source_path": relative_path,
                "start_line": node.lineno,
                "end_line": end_line,
            }
    return found


def ctags_version(ctags_path: str) -> str:
    result = subprocess.run(
        [ctags_path, "--version"],
        check=False,
        capture_output=True,
        text=True,
    )
    first_line = (result.stdout or result.stderr).splitlines()
    return first_line[0].strip() if first_line else "unknown"


def ctags_symbols(ctags_path: str) -> dict[tuple[str, str], dict[str, Any]]:
    paths = [path.relative_to(SOURCE_ROOT).as_posix() for path in source_files()]
    result = subprocess.run(
        [
            ctags_path,
            "--output-format=json",
            "--languages=Python",
            "--fields=+nKz",
            "-o",
            "-",
            *paths,
        ],
        cwd=SOURCE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip() or "ctags returned non-zero"
        raise RuntimeError(detail)

    found: dict[tuple[str, str], dict[str, Any]] = {}
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        tag = json.loads(line)
        if tag.get("_type") != "tag":
            continue
        kind = tag.get("kind")
        if kind not in {"class", "function"}:
            continue
        source_path = PurePosixPath(str(tag.get("path", ""))).as_posix()
        line_number = tag.get("line")
        if not isinstance(line_number, int) or line_number < 1:
            continue
        found.setdefault(
            (str(tag.get("name", "")), kind),
            {
                "name": str(tag.get("name", "")),
                "kind": kind,
                "source_path": source_path,
                "start_line": line_number,
                "end_line": line_number,
            },
        )
    return found


def case_observations(
    source_manifest: dict[str, Any],
    symbols: dict[tuple[str, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    paths = observation_paths()
    observations: list[dict[str, Any]] = []
    for case in source_manifest["cases"]:
        expected = [
            (symbol["name"], symbol["kind"])
            for symbol in case["symbols"]
        ]
        matched = [symbols[key] for key in expected if key in symbols]
        observations.append(
            {
                "case_id": case["case_id"],
                "status": "observed" if len(matched) == len(expected) else "failed",
                "source_paths": paths,
                "symbols": matched,
                **(
                    {}
                    if len(matched) == len(expected)
                    else {"error": "one or more declared symbols were not observed"}
                ),
            }
        )
    return observations


def provider_record(
    *,
    provider_id: str,
    kind: str,
    version: str,
    command_ref: str,
    availability: str,
    source_manifest: dict[str, Any],
    observations: list[dict[str, Any]],
    case_ids: list[str],
) -> dict[str, Any]:
    config = {
        "command_ref": command_ref,
        "kind": kind,
        "source_manifest_digest": canonical_digest(source_manifest),
    }
    return {
        "id": provider_id,
        "kind": kind,
        "version": version,
        "config_digest": canonical_digest(config),
        "command_ref": command_ref,
        "availability": availability,
        "admission_state": "not_admitted",
        "source_root": {
            "path": repo_relative(SOURCE_ROOT),
            "digest": source_root_digest(),
        },
        "case_ids": case_ids,
        "observations": observations,
        "claim_limits": CLAIM_LIMITS,
    }


def collect_evidence() -> dict[str, Any]:
    _fixture, source_manifest = expected_cases()
    case_ids = [case["case_id"] for case in source_manifest["cases"]]
    ast_observations = case_observations(source_manifest, python_symbols())
    providers = [
        provider_record(
            provider_id="python-ast",
            kind="python-ast",
            version=platform.python_version(),
            command_ref="python3:ast.parse",
            availability="available",
            source_manifest=source_manifest,
            observations=ast_observations,
            case_ids=case_ids,
        )
    ]

    ctags_path = shutil.which("ctags")
    if ctags_path is None:
        providers.append(
            provider_record(
                provider_id="ctags-host",
                kind="ctags",
                version="unavailable",
                command_ref="ctags:unavailable",
                availability="not_available",
                source_manifest=source_manifest,
                observations=[],
                case_ids=[],
            )
        )
    else:
        try:
            ctags_observations = case_observations(
                source_manifest, ctags_symbols(ctags_path)
            )
            providers.append(
                provider_record(
                    provider_id="ctags-host",
                    kind="ctags",
                    version=ctags_version(ctags_path),
                    command_ref=f"ctags:{ctags_path}",
                    availability="available",
                    source_manifest=source_manifest,
                    observations=ctags_observations,
                    case_ids=case_ids,
                )
            )
        except (OSError, RuntimeError, json.JSONDecodeError) as exc:
            providers.append(
                provider_record(
                    provider_id="ctags-host",
                    kind="ctags",
                    version=ctags_version(ctags_path),
                    command_ref=f"ctags:{ctags_path}",
                    availability="available",
                    source_manifest=source_manifest,
                    observations=[
                        {
                            "case_id": case_ids[0],
                            "status": "failed",
                            "source_paths": observation_paths(),
                            "symbols": [],
                            "error": f"ctags observation failed: {exc}",
                        }
                    ],
                    case_ids=case_ids,
                )
            )

    return {
        "schema_version": EVIDENCE_SCHEMA_VERSION,
        "family_id": FAMILY_ID,
        "fixture_manifest_digest": canonical_digest(load_json(FIXTURE_PATH)),
        "source_manifest_digest": canonical_digest(source_manifest),
        "observed_at": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "providers": providers,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def schema_errors(instance: Any) -> list[str]:
    validator = Draft202012Validator(load_json(SCHEMA_PATH), format_checker=FormatChecker())
    return [
        f"{'.'.join(str(part) for part in error.path) or '$'}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


def local_path_error(path: str) -> bool:
    posix_path = PurePosixPath(path)
    return (
        posix_path.is_absolute()
        or ".." in posix_path.parts
        or "://" in path
        or not path
    )


def semantic_errors(evidence: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        fixture, source_manifest = expected_cases()
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return [f"source-manifest: {exc}"]

    expected_case_ids = [case["case_id"] for case in fixture["cases"]]
    expected_source_cases = {
        case["case_id"]: case for case in source_manifest["cases"]
    }
    expected_paths = set(observation_paths())
    if evidence.get("family_id") != FAMILY_ID:
        errors.append("family_id: expected refactor-torture-v1")
    if evidence.get("fixture_manifest_digest") != canonical_digest(fixture):
        errors.append("fixture_manifest_digest: digest mismatch")
    if evidence.get("source_manifest_digest") != canonical_digest(source_manifest):
        errors.append("source_manifest_digest: digest mismatch")

    providers = evidence.get("providers", [])
    provider_ids: list[str] = []
    for index, provider in enumerate(providers):
        location = f"provider[{index}]"
        provider_id = provider["id"]
        provider_ids.append(provider_id)
        if provider_id == "python-ast" and provider["kind"] != "python-ast":
            errors.append(f"{location}: python-ast kind mismatch")
        if provider_id == "ctags-host" and provider["kind"] != "ctags":
            errors.append(f"{location}: ctags-host kind mismatch")
        limits = " ".join(provider["claim_limits"]).lower()
        if "not admitted" not in limits or "not provider correctness" not in limits:
            errors.append(f"{location}: claim limits must preserve non-admission and correctness bounds")
        if provider["source_root"]["path"] != repo_relative(SOURCE_ROOT):
            errors.append(f"{location}: source root path drift")
        if provider["source_root"]["digest"] != source_root_digest():
            errors.append(f"{location}: source root digest mismatch")

        if provider["availability"] == "not_available":
            if provider_id != "ctags-host":
                errors.append(f"{location}: only optional Ctags may be unavailable")
            if provider["case_ids"] or provider["observations"]:
                errors.append(f"{location}: unavailable provider must not carry observations")
            continue

        case_ids = provider["case_ids"]
        if case_ids != expected_case_ids:
            errors.append(f"{location}: available provider case coverage is not the complete family")
        observations = provider["observations"]
        observation_ids = [observation["case_id"] for observation in observations]
        if observation_ids != expected_case_ids:
            errors.append(f"{location}: available provider observations are not one-per-case")
        if len(observation_ids) != len(set(observation_ids)):
            errors.append(f"{location}: duplicate observation case id")

        observations_by_id = {observation["case_id"]: observation for observation in observations}
        for case_id in expected_case_ids:
            observation = observations_by_id.get(case_id)
            if observation is None:
                continue
            if observation["status"] != "observed":
                errors.append(f"{location}:{case_id}: provider observation failed")
                continue
            if set(observation["source_paths"]) != expected_paths:
                errors.append(f"{location}:{case_id}: source path coverage mismatch")
            expected_symbols = {
                (symbol["name"], symbol["kind"])
                for symbol in expected_source_cases[case_id]["symbols"]
            }
            actual_symbols = {
                (symbol["name"], symbol["kind"])
                for symbol in observation["symbols"]
            }
            if actual_symbols != expected_symbols:
                errors.append(f"{location}:{case_id}: declared symbol evidence mismatch")
            for symbol in observation["symbols"]:
                if local_path_error(symbol["source_path"]):
                    errors.append(f"{location}:{case_id}: unsafe symbol source path")
                if symbol["source_path"] not in expected_paths:
                    errors.append(f"{location}:{case_id}: symbol source path is outside source root")
                if symbol["end_line"] < symbol["start_line"]:
                    errors.append(f"{location}:{case_id}: symbol line span is reversed")

    if len(provider_ids) != len(set(provider_ids)):
        errors.append("providers: duplicate provider id")
    if "python-ast" not in provider_ids:
        errors.append("providers: Python-AST evidence is required")
    return errors


def validate_evidence(path: Path) -> tuple[dict[str, Any], list[str]]:
    evidence = load_json(path)
    errors = schema_errors(evidence)
    if not errors:
        errors.extend(semantic_errors(evidence))
    return evidence, errors


def command_collect() -> int:
    evidence = collect_evidence()
    errors = schema_errors(evidence) + semantic_errors(evidence)
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0 if not errors else 1


def command_validate(path: Path) -> int:
    evidence, errors = validate_evidence(path)
    providers = [
        {
            "id": provider.get("id"),
            "availability": provider.get("availability"),
            "case_count": len(provider.get("case_ids", [])),
            "observed_count": sum(
                observation.get("status") == "observed"
                for observation in provider.get("observations", [])
            ),
        }
        for provider in evidence.get("providers", [])
    ]
    result = {
        "valid": not errors,
        "evidence": str(path),
        "family_id": evidence.get("family_id"),
        "providers": providers,
        "claim_boundary": CLAIM_BOUNDARY,
        "errors": errors,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("collect")
    validate = subparsers.add_parser("validate")
    validate.add_argument("evidence", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "collect":
        return command_collect()
    return command_validate(args.evidence)


if __name__ == "__main__":
    raise SystemExit(main())
