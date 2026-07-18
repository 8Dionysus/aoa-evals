#!/usr/bin/env python3
"""Validate sibling-repo local eval ports."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Sequence
from urllib.parse import urlparse

import yaml
from jsonschema import Draft202012Validator


CONTRACT_ROOT = Path(__file__).resolve().parents[1]
EVAL_NEED_SCHEMA = (
    CONTRACT_ROOT
    / "mechanics"
    / "proof-object"
    / "parts"
    / "eval-authoring"
    / "schemas"
    / "eval-need.schema.json"
)
LOCAL_SUITE_EXECUTION_SCHEMA = (
    CONTRACT_ROOT
    / "mechanics"
    / "proof-object"
    / "parts"
    / "eval-authoring"
    / "schemas"
    / "local-eval-suite-execution.schema.json"
)

REQUIRED_PORT_FILES = (
    "AGENTS.md",
    "README.md",
    "PORT.yaml",
    "intake/README.md",
    "suites/README.md",
    "reports/README.md",
)
REQUIRED_PORT_FIELDS = (
    "schema_version",
    "owner_repo",
    "status",
    "proof_owner_repo",
    "default_intake_schema",
    "local_role",
    "central_boundary",
)
VALID_STATUSES = {"skeleton", "active"}
AUTHORITY_BOUNDARY_TOKENS = ("verdict", "scoring", "regression", "proof doctrine")
AUTHORITY_CLAUSE_SPLIT_RE = re.compile(
    r"[.;:\n]+|\b(?:but|while|whereas)\b"
)
AUTHORITY_DENIAL_RE = re.compile(r"\b(no|without)\b")
LOCAL_STAY_GRANT_RE = re.compile(r"\b(stay|stays|remain|remains)\s+local\b")
AUTHORITY_GRANT_RE = re.compile(r"\b(authority|control|ownership|own|owns|owned)\b")
LOCAL_SUBJECT_GRANT_RE = re.compile(
    r"\blocal\b.*\b(has|have|had|hold|holds|held|keep|keeps|kept|"
    r"retain|retains|retained|own|owns|owned|control|controls|controlled)\b"
)
AUTHORITY_STAYS_LOCAL_RE = re.compile(
    r"\bauthority\s+(stay|stays|remain|remains)\s+local\b"
)
AUTHORITY_IS_LOCAL_RE = re.compile(
    r"\bauthority\s+(is|are|stay|stays|remain|remains)\s+local\b"
)
AOA_EVALS_ROUTE_RE = re.compile(
    r"\b(route|routes|routed|routing|to|toward|towards|downstream)\b.*?\baoa-evals\b"
)
AUTHORITY_ROUTE_NEGATION_PREFIX_RE = re.compile(
    r"\b(?:not|never)\s+(?:be\s+|being\s+|been\s+)?$"
)
AUTHORITY_ROUTE_ABSENCE_PREFIX_RE = re.compile(
    r"\b(?:no|without)\s+(?:a\s+|any\s+)?$"
)
AUTHORITY_ROUTE_TAIL_STOP_RE = re.compile(
    r"[.;:\n]+|\b(?:but|while|whereas)\b"
)
AUTHORITY_ROUTE_SUBJECT_PREFIX_RE = re.compile(
    r"\bauthority(?:\s+(?:(?:is|are|be|being|been)|"
    r"(?:must|should|shall|will|can|could|may|might)(?:\s+be)?))?\s*$"
)
CLAIM_FAMILIES = {
    "artifact",
    "boundary",
    "capability",
    "comparative",
    "longitudinal",
    "regression",
    "stress",
    "workflow",
}
LOCAL_NOTE_BOUNDARY_TOKENS = ("verdict", "scoring", "regression", "proof doctrine")
LOCAL_NOTE_CONFIG = {
    "suites": {
        "glob": "*.suite.md",
        "schema_version": "local_eval_suite_note_v1",
        "label": "local suite note",
    },
    "reports": {
        "glob": "*.report.md",
        "schema_version": "local_eval_report_note_v1",
        "label": "local report note",
    },
}
LOCAL_SUITE_AUTHORITY_BOUNDARY = (
    "owner-local execution support only; no verdict, scoring, regression, "
    "proof doctrine, proof acceptance, or promotion authority"
)
LOCAL_SUITE_EXECUTION_STATES = ("absent", "invalid", "stale", "ready")
LOCAL_SUITE_EXECUTION_AGGREGATE_PRIORITY = ("invalid", "stale", "ready", "absent")
LOCAL_SUITE_READY_SCOPE = "source-contract-ready"
LOCAL_SUITE_RUNTIME_BOUNDARY = (
    "ready validates the reviewed source contract only; it does not prove a pinned "
    "interpreter, dependency environment, or reproducible runtime"
)
LOCAL_SUITE_JIT_HANDOFF = (
    "owner/apply must revalidate the sidecar and tracked hashes immediately before "
    "execution, then capture the environment and an execution receipt"
)
SHELL_EXECUTABLES = {
    "ash",
    "bash",
    "cmd",
    "cmd.exe",
    "dash",
    "fish",
    "ksh",
    "powershell",
    "powershell.exe",
    "pwsh",
    "sh",
    "zsh",
}
SHELL_WRAPPER_EXECUTABLES = {"command", "env"}
BUSYBOX_EXECUTABLES = {"busybox"}
SHELL_METACHARACTER_RE = re.compile(r"[;&|<>`$\r\n\x00]")
WINDOWS_ABSOLUTE_PATH_RE = re.compile(r"^[A-Za-z]:[\\/]")
PORTABLE_OWNER_DECLARATIONS = (
    ("evals/PORT.yaml", "local_eval_port_v1"),
    ("capabilities/port.manifest.json", "aoa_capability_home_port_v1"),
    ("skills/port.manifest.json", "aoa_skill_home_port_v2"),
)
PORTABLE_OWNER_MIN_AGREEMENTS = 2
PYTHON_PYTEST_EXECUTABLES = {"python", "python3"}
PYTHON_PYTEST_FLAGS = {
    "-q",
    "--quiet",
    "-x",
    "--exitfirst",
    "--strict-markers",
    "--strict-config",
    "--disable-warnings",
}
PYTHON_PYTEST_VALUE_FLAG_RE = re.compile(
    r"^(?:--maxfail=[1-9][0-9]{0,2}|--tb=(?:auto|long|short|line|native|no)|"
    r"--color=(?:yes|no|auto)|-r[a-zA-Z]+)$"
)


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


@dataclass(frozen=True)
class RepoIdentity:
    owner_repo: str
    sources: tuple[str, ...]
    common_dir: str | None
    common_dir_owner: str | None
    origin_owner: str | None
    issues: tuple[str, ...]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target-root",
        default=".",
        help="Repository root that should contain the local eval port.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a JSON result instead of human-readable issues.",
    )
    return parser.parse_args(argv)


def relative_location(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def git_dir_from_marker(repo_root: Path) -> Path | None:
    marker = repo_root / ".git"
    if marker.is_dir():
        return marker.resolve()
    if not marker.is_file():
        return None
    try:
        first_line = marker.read_text(encoding="utf-8").splitlines()[0]
    except (IndexError, OSError, UnicodeDecodeError):
        return None
    if not first_line.startswith("gitdir:"):
        return None
    raw_path = first_line.removeprefix("gitdir:").strip()
    if not raw_path:
        return None
    git_dir = Path(raw_path)
    if not git_dir.is_absolute():
        git_dir = repo_root / git_dir
    return git_dir.resolve(strict=False)


def git_common_dir(git_dir: Path) -> Path:
    commondir_path = git_dir / "commondir"
    try:
        raw_path = commondir_path.read_text(encoding="utf-8").splitlines()[0].strip()
    except (FileNotFoundError, IndexError, OSError, UnicodeDecodeError):
        return git_dir
    common_dir = Path(raw_path)
    if not common_dir.is_absolute():
        common_dir = git_dir / common_dir
    return common_dir.resolve(strict=False)


def repo_name_from_git_remote(url: str) -> str | None:
    value = url.strip().rstrip("/")
    if not value:
        return None
    if "://" in value:
        path_text = urlparse(value).path
    elif ":" in value and not WINDOWS_ABSOLUTE_PATH_RE.match(value):
        path_text = value.rsplit(":", 1)[1]
    else:
        path_text = value
    name = PurePosixPath(path_text.replace("\\", "/")).name
    if name.endswith(".git"):
        name = name[:-4]
    return name or None


def origin_owner_from_config(common_dir: Path) -> str | None:
    try:
        text = (common_dir / "config").read_text(encoding="utf-8")
    except (FileNotFoundError, OSError, UnicodeDecodeError):
        return None
    match = re.search(
        r'^\s*\[remote\s+"origin"\]\s*$'
        r"(?P<body>.*?)(?=^\s*\[|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        return None
    url_match = re.search(r"^\s*url\s*=\s*(?P<url>.+?)\s*$", match.group("body"), re.MULTILINE)
    return repo_name_from_git_remote(url_match.group("url")) if url_match else None


def portable_owner_declarations(repo_root: Path) -> list[tuple[str, str]]:
    declarations: list[tuple[str, str]] = []
    for relative_path, schema_version in PORTABLE_OWNER_DECLARATIONS:
        path = repo_root / relative_path
        if (
            first_symlink_component(
                repo_root,
                PurePosixPath(relative_path).parts,
            )
            is not None
            or not path.is_file()
        ):
            continue
        try:
            if path.suffix == ".json":
                payload = json.loads(path.read_text(encoding="utf-8"))
            else:
                payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, yaml.YAMLError):
            continue
        if not isinstance(payload, dict) or payload.get("schema_version") != schema_version:
            continue
        owner_repo = payload.get("owner_repo")
        if isinstance(owner_repo, str) and owner_repo.strip():
            declarations.append((relative_path, owner_repo.strip()))
    return declarations


def resolve_repo_identity(repo_root: Path) -> RepoIdentity:
    repo_root = repo_root.resolve()
    git_dir = git_dir_from_marker(repo_root)
    if git_dir is None:
        declarations = portable_owner_declarations(repo_root)
        if len(declarations) >= PORTABLE_OWNER_MIN_AGREEMENTS:
            owners = sorted({owner for _, owner in declarations})
            sources = tuple(f"portable_manifest:{path}" for path, _ in declarations)
            if len(owners) == 1:
                return RepoIdentity(
                    owner_repo=owners[0],
                    sources=sources,
                    common_dir=None,
                    common_dir_owner=None,
                    origin_owner=None,
                    issues=(),
                )
            rendered = ", ".join(
                f"{path}={owner}" for path, owner in declarations
            )
            return RepoIdentity(
                owner_repo=repo_root.name,
                sources=sources,
                common_dir=None,
                common_dir_owner=None,
                origin_owner=None,
                issues=(
                    "portable owner declarations conflict: " + rendered,
                ),
            )
        return RepoIdentity(
            owner_repo=repo_root.name,
            sources=("fallback_basename_nongit",),
            common_dir=None,
            common_dir_owner=None,
            origin_owner=None,
            issues=(),
        )

    common_dir = git_common_dir(git_dir)
    common_owner = common_dir.parent.name if common_dir.name == ".git" else None
    origin_owner = origin_owner_from_config(common_dir)
    sources: list[str] = []
    if common_owner:
        sources.append("git_common_dir")
    if origin_owner:
        sources.append("git_origin")
    if not sources:
        sources.append("fallback_basename_unidentified_git")

    identity_issues: list[str] = []
    if common_owner and origin_owner and common_owner != origin_owner:
        identity_issues.append(
            "Git common-dir owner "
            f"'{common_owner}' conflicts with origin owner '{origin_owner}'"
        )
    resolved_owner = origin_owner or common_owner or repo_root.name
    return RepoIdentity(
        owner_repo=resolved_owner,
        sources=tuple(sources),
        common_dir=common_dir.as_posix(),
        common_dir_owner=common_owner,
        origin_owner=origin_owner,
        issues=tuple(identity_issues),
    )


def load_yaml_payload(path: Path, root: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
    except yaml.YAMLError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid YAML: {exc}"))
    return None


def load_json_payload(path: Path, root: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid JSON: {exc}"))
    except UnicodeDecodeError as exc:
        issues.append(
            ValidationIssue(
                relative_location(path, root),
                f"invalid JSON: file must be UTF-8 text ({exc})",
            )
        )
    except OSError as exc:
        issues.append(
            ValidationIssue(
                relative_location(path, root),
                f"invalid JSON sidecar: cannot read regular file ({exc})",
            )
        )
    return None


def load_markdown_frontmatter(path: Path, root: Path, issues: list[ValidationIssue]) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return None
    if not text.startswith("---\n"):
        issues.append(ValidationIssue(relative_location(path, root), "missing YAML frontmatter"))
        return None
    try:
        _, frontmatter, _ = text.split("---\n", 2)
    except ValueError:
        issues.append(ValidationIssue(relative_location(path, root), "unterminated YAML frontmatter"))
        return None
    try:
        payload = yaml.safe_load(frontmatter)
    except yaml.YAMLError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid frontmatter YAML: {exc}"))
        return None
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(relative_location(path, root), "frontmatter must contain a mapping"))
        return None
    return payload


def format_schema_path(path_parts: Sequence[Any]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            if parts:
                parts[-1] = f"{parts[-1]}[{part}]"
            else:
                parts.append(f"[{part}]")
        else:
            parts.append(str(part))
    return ".".join(parts)


def eval_need_validator() -> Draft202012Validator:
    schema = json.loads(EVAL_NEED_SCHEMA.read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def local_suite_execution_validator() -> Draft202012Validator:
    schema = json.loads(LOCAL_SUITE_EXECUTION_SCHEMA.read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def compute_file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compute_tree_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    for child in sorted(path.rglob("*"), key=lambda item: item.relative_to(path).as_posix()):
        relative = child.relative_to(path).as_posix()
        if child.is_symlink():
            raise ValueError(f"tracked tree contains symlink: {relative}")
        if child.is_dir():
            digest.update(f"dir\0{relative}\n".encode("utf-8"))
            continue
        if not child.is_file():
            raise ValueError(f"tracked tree contains non-regular path: {relative}")
        child_digest = compute_file_sha256(child)
        digest.update(f"file\0{relative}\0{child_digest}\n".encode("utf-8"))
    return digest.hexdigest()


def compute_tracked_source_sha256(path: Path, kind: str) -> str:
    if kind == "file":
        return compute_file_sha256(path)
    if kind == "tree":
        return compute_tree_sha256(path)
    raise ValueError(f"unsupported tracked source kind: {kind}")


def repo_relative_contract_path(
    repo_root: Path,
    value: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
    allow_repo_root: bool = False,
) -> Path | None:
    if not isinstance(value, str) or not value:
        issues.append(ValidationIssue(location, "path must be a non-empty repo-relative string"))
        return None
    if "\\" in value or value.startswith("~"):
        issues.append(ValidationIssue(location, "path must use a repo-relative POSIX form"))
        return None
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts:
        issues.append(ValidationIssue(location, "path traversal is forbidden; use a repo-relative path"))
        return None
    if value != "." and any(part in {"", "."} for part in pure.parts):
        issues.append(ValidationIssue(location, "path must use a normalized repo-relative form"))
        return None
    if value == "." and not allow_repo_root:
        issues.append(ValidationIssue(location, "path must name a repo-relative surface, not the repo root"))
        return None

    candidate = repo_root if value == "." else repo_root.joinpath(*pure.parts)
    symlink_component = first_symlink_component(repo_root, pure.parts)
    if symlink_component is not None:
        issues.append(ValidationIssue(location, f"symlink path components are forbidden: {symlink_component}"))
        return None
    try:
        candidate.resolve(strict=False).relative_to(repo_root.resolve())
    except ValueError:
        issues.append(ValidationIssue(location, "path traversal is forbidden; target escapes repo root"))
        return None
    return candidate


def first_symlink_component(repo_root: Path, parts: Sequence[str]) -> str | None:
    cursor = repo_root
    for part in parts:
        cursor = cursor / part
        if cursor.is_symlink():
            try:
                return cursor.relative_to(repo_root).as_posix()
            except ValueError:
                return cursor.as_posix()
    return None


def validate_shell_free_argv(
    argv: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(argv, list) or not argv:
        return
    if not all(isinstance(item, str) and item for item in argv):
        return
    executable = Path(argv[0]).name.lower()
    if executable in SHELL_EXECUTABLES:
        issues.append(ValidationIssue(location, "runner.argv must be shell-free; shell executables are forbidden"))
    if executable.startswith("python") and len(argv) > 1 and argv[1] == "-c":
        issues.append(ValidationIssue(location, "runner.argv must be shell-free; inline interpreter code is forbidden"))
    if executable in SHELL_WRAPPER_EXECUTABLES:
        issues.append(ValidationIssue(location, "runner.argv must be shell-free; shell-dispatch wrappers are forbidden"))
    if executable in BUSYBOX_EXECUTABLES:
        issues.append(ValidationIssue(location, "runner.argv must be shell-free; busybox dispatch is forbidden"))
    for index, item in enumerate(argv):
        if SHELL_METACHARACTER_RE.search(item):
            issues.append(
                ValidationIssue(
                    f"{location}[{index}]",
                    "runner.argv must be shell-free; shell metacharacters are forbidden",
                )
            )


def validate_python_pytest_runner(
    runner: Any,
    entrypoint_arg: str,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(runner, dict) or runner.get("kind") != "python_pytest":
        return
    argv = runner.get("argv")
    if not isinstance(argv, list) or not all(isinstance(item, str) for item in argv):
        return
    if len(argv) < 4:
        issues.append(
            ValidationIssue(
                location,
                "python_pytest runner argv must be <python|python3> [-B] -m pytest [allowed flags] <entrypoint_ref>",
            )
        )
        return
    module_index = 2 if len(argv) > 1 and argv[1] == "-B" else 1
    flags_start = module_index + 2
    if (
        argv[0] not in PYTHON_PYTEST_EXECUTABLES
        or argv[module_index:flags_start] != ["-m", "pytest"]
    ):
        issues.append(
            ValidationIssue(
                location,
                "python_pytest runner permits only exact executable/module prefix: python or python3, optional -B, then -m pytest",
            )
        )
    if argv[-1] != entrypoint_arg:
        issues.append(
            ValidationIssue(
                location,
                "python_pytest runner must place the runner.cwd-relative entrypoint argument exactly once as the final argv token",
            )
        )
    if argv.count(entrypoint_arg) != 1:
        issues.append(
            ValidationIssue(
                location,
                "python_pytest runner must contain the runner.cwd-relative entrypoint argument exactly once",
            )
        )
    index = flags_start
    while index < len(argv) - 1:
        flag = argv[index]
        if flag == "-p" and index + 1 < len(argv) - 1:
            if argv[index + 1] == "no:cacheprovider":
                index += 2
                continue
            issues.append(
                ValidationIssue(
                    f"{location}.argv[{index}]",
                    "python_pytest runner permits only the fixed plugin pair -p no:cacheprovider",
                )
            )
            index += 2
            continue
        if flag in PYTHON_PYTEST_FLAGS or PYTHON_PYTEST_VALUE_FLAG_RE.fullmatch(flag):
            index += 1
            continue
        issues.append(
            ValidationIssue(
                f"{location}.argv[{index}]",
                f"python_pytest runner flag is outside the reviewed allowlist: {flag}",
            )
        )
        index += 1


def validate_runner_argv_paths_and_entrypoint(
    argv: Any,
    entrypoint_arg: str,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(argv, list) or not all(isinstance(item, str) for item in argv):
        return
    if entrypoint_arg not in argv:
        issues.append(
            ValidationIssue(
                location,
                "runner.argv must contain the runner.cwd-relative entrypoint argument exactly so owner/apply invocation resolves to the reviewed entrypoint_ref",
            )
        )
    for index, item in enumerate(argv[1:], start=1):
        if item.startswith("-"):
            continue
        pure = PurePosixPath(item)
        if pure.is_absolute() or ".." in pure.parts or WINDOWS_ABSOLUTE_PATH_RE.match(item):
            issues.append(
                ValidationIssue(
                    f"{location}[{index}]",
                    "runner.argv path-like values must use normalized repo-relative path arguments without traversal",
                )
            )


def tracked_source_covers_entrypoint(
    entrypoint_ref: str,
    tracked_path: str,
    kind: str,
) -> bool:
    entrypoint = PurePosixPath(entrypoint_ref)
    tracked = PurePosixPath(tracked_path)
    if kind == "file":
        return entrypoint == tracked
    return entrypoint == tracked or tracked in entrypoint.parents


def evaluate_local_suite_contract(
    repo_root: Path,
    path: Path,
    *,
    repo_identity: RepoIdentity | None = None,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    repo_identity = repo_identity or resolve_repo_identity(repo_root)
    location = relative_location(path, repo_root)
    issues: list[ValidationIssue] = []
    stale_sources: list[dict[str, str]] = []
    for identity_issue in repo_identity.issues:
        issues.append(ValidationIssue(location, identity_issue))
    try:
        lexical_relative = path.absolute().relative_to(repo_root)
    except ValueError:
        issues.append(ValidationIssue(location, "suite execution sidecar must stay inside the repo root"))
        lexical_relative = None
    if lexical_relative is not None:
        symlink_component = first_symlink_component(repo_root, lexical_relative.parts)
        if symlink_component is not None:
            issues.append(
                ValidationIssue(
                    location,
                    f"suite execution sidecar path must not contain a symlink: {symlink_component}",
                )
            )
    if issues:
        payload: Any = None
    elif path.is_symlink():
        issues.append(ValidationIssue(location, "suite execution sidecar must not be a symlink"))
        payload = None
    elif not path.is_file():
        issues.append(
            ValidationIssue(location, "suite execution sidecar must be a regular file")
        )
        payload = None
    else:
        payload = load_json_payload(path, repo_root, issues)

    if isinstance(payload, dict):
        validator = local_suite_execution_validator()
        errors = sorted(
            validator.iter_errors(payload),
            key=lambda error: (list(error.absolute_path), error.message),
        )
        for error in errors:
            error_path = format_schema_path(error.absolute_path)
            message = f"schema violation at '{error_path}': {error.message}" if error_path else f"schema violation: {error.message}"
            issues.append(ValidationIssue(location, message))
    elif payload is not None:
        issues.append(ValidationIssue(location, "suite execution sidecar must contain a JSON object"))

    if not isinstance(payload, dict) or issues:
        return {
            "path": location,
            "suite_id": payload.get("suite_id") if isinstance(payload, dict) else None,
            "state": "invalid",
            "readiness_scope": LOCAL_SUITE_READY_SCOPE,
            "runtime_reproducibility_proven": False,
            "runtime_boundary": LOCAL_SUITE_RUNTIME_BOUNDARY,
            "jit_revalidation_required": True,
            "execution_receipt_required": True,
            "environment_capture_required": True,
            "execution_handoff": LOCAL_SUITE_JIT_HANDOFF,
            "runner": payload.get("runner") if isinstance(payload, dict) else None,
            "issues": [{"location": issue.location, "message": issue.message} for issue in issues],
            "stale_sources": [],
        }

    suite_id = str(payload["suite_id"])
    expected_name = f"{suite_id}.suite.json"
    if path.name != expected_name:
        issues.append(ValidationIssue(location, f"filename must be '{expected_name}'"))
    expected_note_ref = f"evals/suites/{suite_id}.suite.md"
    if payload["suite_note_ref"] != expected_note_ref:
        issues.append(ValidationIssue(location, f"suite_note_ref must be '{expected_note_ref}'"))
    if payload["owner_repo"] != repo_identity.owner_repo:
        issues.append(
            ValidationIssue(
                location,
                "owner_repo must match canonical repo identity "
                f"'{repo_identity.owner_repo}', not worktree basename '{repo_root.name}'",
            )
        )
    if payload["authority_boundary"] != LOCAL_SUITE_AUTHORITY_BOUNDARY:
        issues.append(ValidationIssue(location, "authority_boundary must preserve the owner-local non-proof boundary"))

    suite_note_path = repo_relative_contract_path(
        repo_root,
        payload["suite_note_ref"],
        location=f"{location}:suite_note_ref",
        issues=issues,
    )
    if suite_note_path is not None and not suite_note_path.is_file():
        issues.append(ValidationIssue(f"{location}:suite_note_ref", "referenced suite note is missing"))

    runner = payload["runner"]
    validate_shell_free_argv(runner["argv"], location=f"{location}:runner.argv", issues=issues)
    cwd_path = repo_relative_contract_path(
        repo_root,
        runner["cwd"],
        location=f"{location}:runner.cwd",
        issues=issues,
        allow_repo_root=True,
    )
    if cwd_path is not None and not cwd_path.is_dir():
        issues.append(ValidationIssue(f"{location}:runner.cwd", "runner cwd must be an existing directory"))

    entrypoint_ref = str(payload["entrypoint_ref"])
    entrypoint_path = repo_relative_contract_path(
        repo_root,
        entrypoint_ref,
        location=f"{location}:entrypoint_ref",
        issues=issues,
    )
    if entrypoint_path is not None and not entrypoint_path.is_file():
        issues.append(ValidationIssue(f"{location}:entrypoint_ref", "entrypoint_ref must name an existing file"))

    entrypoint_arg: str | None = None
    if cwd_path is not None and entrypoint_path is not None:
        try:
            entrypoint_arg = entrypoint_path.relative_to(cwd_path).as_posix()
        except ValueError:
            issues.append(
                ValidationIssue(
                    f"{location}:runner.cwd",
                    "entrypoint_ref must resolve beneath runner.cwd so argv can name it without traversal",
                )
            )
        if entrypoint_arg in {"", "."}:
            issues.append(
                ValidationIssue(
                    f"{location}:entrypoint_ref",
                    "entrypoint_ref must resolve to a file below runner.cwd",
                )
            )
            entrypoint_arg = None
    if entrypoint_arg is not None:
        validate_python_pytest_runner(
            runner,
            entrypoint_arg,
            location=f"{location}:runner",
            issues=issues,
        )
        validate_runner_argv_paths_and_entrypoint(
            runner["argv"],
            entrypoint_arg,
            location=f"{location}:runner.argv",
            issues=issues,
        )

    tracked_paths: set[str] = set()
    entrypoint_covered = False
    for index, source in enumerate(payload["tracked_sources"]):
        source_location = f"{location}:tracked_sources[{index}]"
        source_ref = str(source["path"])
        kind = str(source["kind"])
        if source_ref in tracked_paths:
            issues.append(ValidationIssue(source_location, f"duplicate tracked source path: {source_ref}"))
            continue
        tracked_paths.add(source_ref)
        source_path = repo_relative_contract_path(
            repo_root,
            source_ref,
            location=f"{source_location}.path",
            issues=issues,
        )
        if source_path is None:
            continue
        if kind == "file" and not source_path.is_file():
            issues.append(ValidationIssue(source_location, "tracked file source is missing or not a file"))
            continue
        if kind == "tree" and not source_path.is_dir():
            issues.append(ValidationIssue(source_location, "tracked tree source is missing or not a directory"))
            continue
        try:
            actual_sha256 = compute_tracked_source_sha256(source_path, kind)
        except (OSError, ValueError) as exc:
            issues.append(ValidationIssue(source_location, str(exc)))
            continue
        if actual_sha256 != source["sha256"]:
            stale_sources.append(
                {
                    "path": source_ref,
                    "kind": kind,
                    "expected_sha256": str(source["sha256"]),
                    "actual_sha256": actual_sha256,
                }
            )
        entrypoint_covered = entrypoint_covered or tracked_source_covers_entrypoint(
            entrypoint_ref,
            source_ref,
            kind,
        )
    if not entrypoint_covered:
        issues.append(ValidationIssue(location, "entrypoint_ref must be covered by tracked_sources"))

    state = "invalid" if issues else ("stale" if stale_sources else "ready")
    return {
        "path": location,
        "suite_id": suite_id,
        "state": state,
        "runner": runner,
        "entrypoint_ref": entrypoint_ref,
        "entrypoint_arg": entrypoint_arg,
        "timeout_seconds": payload["timeout_seconds"],
        "success_exit_codes": payload["success_exit_codes"],
        "auto_run_allowed": False,
        "proof_authority": False,
        "promotion_allowed": False,
        "readiness_scope": LOCAL_SUITE_READY_SCOPE,
        "runtime_reproducibility_proven": False,
        "runtime_boundary": LOCAL_SUITE_RUNTIME_BOUNDARY,
        "jit_revalidation_required": True,
        "execution_receipt_required": True,
        "environment_capture_required": True,
        "execution_handoff": LOCAL_SUITE_JIT_HANDOFF,
        "authority_boundary": payload["authority_boundary"],
        "issues": [{"location": issue.location, "message": issue.message} for issue in issues],
        "stale_sources": stale_sources,
    }


def evaluate_local_suite_execution(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    repo_identity = resolve_repo_identity(repo_root)
    evals_dir = repo_root / "evals"
    suite_dir = evals_dir / "suites"
    parent_issues = [
        {
            "location": location,
            "message": "suite execution discovery path must not contain a symlink",
        }
        for parent, location in ((evals_dir, "evals"), (suite_dir, "evals/suites"))
        if parent.is_symlink()
    ]
    if parent_issues:
        return {
            "schema_version": "local_eval_suite_execution_inventory_v1",
            "state": "invalid",
            "canonical_owner_repo": repo_identity.owner_repo,
            "owner_identity_sources": list(repo_identity.sources),
            "state_vocabulary": list(LOCAL_SUITE_EXECUTION_STATES),
            "aggregate_priority": list(LOCAL_SUITE_EXECUTION_AGGREGATE_PRIORITY),
            "suite_count": 0,
            "invalid_count": 1,
            "stale_count": 0,
            "ready_count": 0,
            "auto_run_allowed": False,
            "inventory_executed_runner": False,
            "proof_authority": False,
            "promotion_allowed": False,
            "readiness_scope": LOCAL_SUITE_READY_SCOPE,
            "runtime_reproducibility_proven": False,
            "runtime_boundary": LOCAL_SUITE_RUNTIME_BOUNDARY,
            "jit_revalidation_required": True,
            "execution_receipt_required": True,
            "environment_capture_required": True,
            "execution_handoff": LOCAL_SUITE_JIT_HANDOFF,
            "issues": parent_issues,
            "suites": [],
        }
    paths = sorted(suite_dir.glob("*.suite.json")) if suite_dir.is_dir() else []
    suites = [
        evaluate_local_suite_contract(repo_root, path, repo_identity=repo_identity)
        for path in paths
    ]
    states = {str(suite["state"]) for suite in suites}
    aggregate_state = next(
        (state for state in LOCAL_SUITE_EXECUTION_AGGREGATE_PRIORITY if state in states),
        "absent",
    )
    issues = [issue for suite in suites for issue in suite.get("issues", [])]
    return {
        "schema_version": "local_eval_suite_execution_inventory_v1",
        "state": aggregate_state,
        "canonical_owner_repo": repo_identity.owner_repo,
        "owner_identity_sources": list(repo_identity.sources),
        "state_vocabulary": list(LOCAL_SUITE_EXECUTION_STATES),
        "aggregate_priority": list(LOCAL_SUITE_EXECUTION_AGGREGATE_PRIORITY),
        "suite_count": len(suites),
        "invalid_count": sum(1 for suite in suites if suite["state"] == "invalid"),
        "stale_count": sum(1 for suite in suites if suite["state"] == "stale"),
        "ready_count": sum(1 for suite in suites if suite["state"] == "ready"),
        "auto_run_allowed": False,
        "inventory_executed_runner": False,
        "proof_authority": False,
        "promotion_allowed": False,
        "readiness_scope": LOCAL_SUITE_READY_SCOPE,
        "runtime_reproducibility_proven": False,
        "runtime_boundary": LOCAL_SUITE_RUNTIME_BOUNDARY,
        "jit_revalidation_required": True,
        "execution_receipt_required": True,
        "environment_capture_required": True,
        "execution_handoff": LOCAL_SUITE_JIT_HANDOFF,
        "issues": issues,
        "suites": suites,
    }


def authority_boundary_clauses(text: str) -> list[str]:
    return [
        clause.strip()
        for clause in AUTHORITY_CLAUSE_SPLIT_RE.split(text)
        if clause.strip()
    ]


def authority_boundary_clause_denies_term(clause: str, token: str) -> bool:
    return (
        token in clause
        and "authority" in clause
        and bool(AUTHORITY_DENIAL_RE.search(clause))
        and not authority_boundary_clause_negates_route(clause)
    )


def authority_route_match_is_negated(clause: str, match: re.Match[str]) -> bool:
        prefix = clause[max(0, match.start() - 40) : match.start()]
        return bool(
            AUTHORITY_ROUTE_NEGATION_PREFIX_RE.search(prefix)
            or AUTHORITY_ROUTE_ABSENCE_PREFIX_RE.search(prefix)
        )


def authority_boundary_clause_negates_route(clause: str) -> bool:
    return any(
        authority_route_match_is_negated(clause, match)
        for match in AOA_EVALS_ROUTE_RE.finditer(clause)
    )


def authority_route_target_tail(clause: str, start: int) -> str:
    tail = clause[start:].lstrip()
    if not tail or tail[0] in ",)]}":
        return ""
    return AUTHORITY_ROUTE_TAIL_STOP_RE.split(tail, maxsplit=1)[0]


def authority_terms_in_text(text: str) -> set[str]:
    return {token for token in AUTHORITY_BOUNDARY_TOKENS if token in text}


def local_subject_authority_grant_terms(clause: str) -> set[str]:
    if AUTHORITY_DENIAL_RE.search(clause):
        return set()

    granted: set[str] = set()
    for match in LOCAL_SUBJECT_GRANT_RE.finditer(clause):
        object_text = clause[match.end() :]
        authority_index = object_text.find("authority")
        if authority_index < 0:
            continue
        object_before_authority = object_text[:authority_index]
        positions = [
            object_before_authority.find(token)
            for token in AUTHORITY_BOUNDARY_TOKENS
            if token in object_before_authority
        ]
        if not positions:
            continue
        leading_object = object_before_authority[: min(positions)]
        if re.search(r"[a-z0-9]", leading_object):
            continue
        granted.update(authority_terms_in_text(object_before_authority))
    return granted


def routed_authority_terms(clause: str) -> set[str]:
    if "authority" not in clause:
        return set()

    routed: set[str] = set()
    for match in AOA_EVALS_ROUTE_RE.finditer(clause):
        if authority_route_match_is_negated(clause, match):
            continue

        prefix = clause[: match.start()]
        if AUTHORITY_ROUTE_SUBJECT_PREFIX_RE.search(prefix):
            routed.update(authority_terms_in_text(prefix))

        match_text = match.group(0)
        if "authority" in match_text:
            routed.update(authority_terms_in_text(match_text))

        tail = authority_route_target_tail(clause, match.end())
        if "authority" in tail:
            routed.update(authority_terms_in_text(tail))

    return routed


def authority_boundary_clause_routes_term(clause: str, token: str) -> bool:
    return token in routed_authority_terms(clause)


def protected_authority_terms(text: str) -> set[str]:
    protected: set[str] = set()
    for clause in authority_boundary_clauses(text):
        for token in AUTHORITY_BOUNDARY_TOKENS:
            if authority_boundary_clause_denies_term(
                clause, token
            ) or authority_boundary_clause_routes_term(clause, token):
                protected.add(token)
    return protected


def local_authority_grant_terms(text: str) -> set[str]:
    granted: set[str] = set()
    for clause in authority_boundary_clauses(text):
        for token in AUTHORITY_BOUNDARY_TOKENS:
            if token not in clause:
                continue
            term = re.escape(token)
            denied_authority_stays_local = bool(
                AUTHORITY_DENIAL_RE.search(clause)
                and AUTHORITY_STAYS_LOCAL_RE.search(clause)
            )
            stay_local_grant = bool(
                not denied_authority_stays_local
                and re.search(rf"\b{term}\b.*{LOCAL_STAY_GRANT_RE.pattern}", clause)
            )
            local_authority_grant = (
                not AUTHORITY_DENIAL_RE.search(clause)
                and bool(re.search(rf"\blocal\s+{term}\b", clause))
                and bool(AUTHORITY_GRANT_RE.search(clause))
            )
            local_subject_grant = (
                token in local_subject_authority_grant_terms(clause)
            )
            authority_is_local_grant = (
                not AUTHORITY_DENIAL_RE.search(clause)
                and bool(AUTHORITY_IS_LOCAL_RE.search(clause))
            )
            if (
                stay_local_grant
                or local_authority_grant
                or local_subject_grant
                or authority_is_local_grant
            ):
                granted.add(token)
    return granted


def validate_port_file(
    repo_root: Path,
    evals_dir: Path,
    repo_identity: RepoIdentity,
    issues: list[ValidationIssue],
) -> dict[str, Any] | None:
    port_path = evals_dir / "PORT.yaml"
    payload = load_yaml_payload(port_path, repo_root, issues)
    if payload is None:
        return None
    location = relative_location(port_path, repo_root)
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(location, "PORT.yaml must contain a mapping"))
        return None

    for field in REQUIRED_PORT_FIELDS:
        if field not in payload:
            issues.append(ValidationIssue(location, f"missing required field '{field}'"))

    if payload.get("schema_version") != "local_eval_port_v1":
        issues.append(
            ValidationIssue(location, "schema_version must be 'local_eval_port_v1'")
        )
    for identity_issue in repo_identity.issues:
        issues.append(ValidationIssue(location, identity_issue))
    if payload.get("owner_repo") != repo_identity.owner_repo:
        issues.append(
            ValidationIssue(
                location,
                "owner_repo must match canonical repo identity "
                f"'{repo_identity.owner_repo}', not worktree basename '{repo_root.name}'",
            )
        )
    if payload.get("status") not in VALID_STATUSES:
        issues.append(ValidationIssue(location, "status must be 'skeleton' or 'active'"))
    if payload.get("proof_owner_repo") != "aoa-evals":
        issues.append(ValidationIssue(location, "proof_owner_repo must be 'aoa-evals'"))
    if payload.get("default_intake_schema") != "eval_need_v1":
        issues.append(ValidationIssue(location, "default_intake_schema must be 'eval_need_v1'"))

    central_boundary = payload.get("central_boundary")
    if not isinstance(central_boundary, str) or not central_boundary.strip():
        issues.append(ValidationIssue(location, "central_boundary must be a non-empty string"))
    else:
        lowered = central_boundary.lower()
        missing = [token for token in AUTHORITY_BOUNDARY_TOKENS if token not in lowered]
        if missing:
            issues.append(
                ValidationIssue(
                    location,
                    "central_boundary must name no verdict, scoring, regression, "
                    "or proof doctrine authority",
                )
            )
        else:
            granted = sorted(local_authority_grant_terms(lowered))
            protected = protected_authority_terms(lowered)
            missing_denial = [
                token for token in AUTHORITY_BOUNDARY_TOKENS if token not in protected
            ]
            if granted:
                issues.append(
                    ValidationIssue(
                        location,
                        "central_boundary must not grant local "
                        f"{', '.join(granted)} authority",
                    )
                )
            elif missing_denial:
                issues.append(
                    ValidationIssue(
                        location,
                        "central_boundary must explicitly deny local "
                        f"{', '.join(missing_denial)} authority",
                    )
                )

    local_role = payload.get("local_role")
    if not isinstance(local_role, str) or not local_role.strip():
        issues.append(ValidationIssue(location, "local_role must be a non-empty string"))

    return payload


def validate_required_shape(repo_root: Path, evals_dir: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if evals_dir.is_symlink():
        issues.append(ValidationIssue("evals", "local eval port directory must not be a symlink"))
        return issues
    if not evals_dir.is_dir():
        issues.append(ValidationIssue("evals", "local eval port directory is missing"))
        return issues
    for relative_path in REQUIRED_PORT_FILES:
        path = evals_dir / relative_path
        symlink_component = first_symlink_component(
            repo_root,
            Path("evals", relative_path).parts,
        )
        if symlink_component is not None:
            issues.append(
                ValidationIssue(
                    relative_location(path, repo_root),
                    f"local eval port path components must not be symlinks: {symlink_component}",
                )
            )
            continue
        if not path.is_file():
            issues.append(ValidationIssue(relative_location(path, repo_root), "file is missing"))
    return issues


def validate_port_docs(repo_root: Path, evals_dir: Path, issues: list[ValidationIssue]) -> None:
    for relative_path in ("README.md", "AGENTS.md"):
        path = evals_dir / relative_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8").lower()
        missing = [
            token
            for token in ("aoa-evals", "verdict", "scoring", "regression", "proof doctrine")
            if token not in text
        ]
        if missing:
            issues.append(
                ValidationIssue(
                    relative_location(path, repo_root),
                    "local eval port docs must name aoa-evals and the central "
                    "verdict/scoring/regression/proof doctrine boundary",
                )
            )


def validate_intake_payloads(
    repo_root: Path,
    evals_dir: Path,
    issues: list[ValidationIssue],
) -> int:
    intake_dir = evals_dir / "intake"
    if not intake_dir.is_dir():
        return 0

    validator = eval_need_validator()
    intake_count = 0
    for path in sorted(intake_dir.glob("*.eval_need.json")):
        intake_count += 1
        payload = load_json_payload(path, repo_root, issues)
        if payload is None:
            continue
        errors = sorted(
            validator.iter_errors(payload),
            key=lambda error: (list(error.absolute_path), error.message),
        )
        for error in errors:
            error_path = format_schema_path(error.absolute_path)
            if error_path:
                message = f"schema violation at '{error_path}': {error.message}"
            else:
                message = f"schema violation: {error.message}"
            issues.append(ValidationIssue(relative_location(path, repo_root), message))
    return intake_count


def expected_family(manifest: dict[str, Any]) -> Path | None:
    baseline_mode = manifest.get("baseline_mode", "none")
    category = manifest.get("category")
    if baseline_mode != "none":
        if not isinstance(baseline_mode, str) or not baseline_mode:
            return None
        family = "fixed-baseline" if baseline_mode == "previous-version" else baseline_mode
        return Path("comparison") / family
    if not isinstance(category, str) or category not in CLAIM_FAMILIES:
        return None
    return Path(category)


def validate_local_bundles(
    repo_root: Path,
    evals_dir: Path,
    issues: list[ValidationIssue],
) -> int:
    bundle_count = 0
    for manifest_path in sorted(evals_dir.glob("**/eval.yaml")):
        bundle_count += 1
        bundle_dir = manifest_path.parent
        eval_md_path = bundle_dir / "EVAL.md"
        if not eval_md_path.is_file():
            issues.append(ValidationIssue(relative_location(eval_md_path, repo_root), "file is missing"))

        manifest = load_yaml_payload(manifest_path, repo_root, issues)
        if not isinstance(manifest, dict):
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    "eval.yaml must contain a mapping",
                )
            )
            continue

        name = manifest.get("name")
        if not isinstance(name, str) or not name:
            issues.append(ValidationIssue(relative_location(manifest_path, repo_root), "missing string 'name'"))
        elif name != bundle_dir.name:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    f"name '{name}' must match bundle directory '{bundle_dir.name}'",
                )
            )

        family = expected_family(manifest)
        if family is None:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    "manifest must expose a valid category and baseline_mode",
                )
            )
            continue
        try:
            bundle_relative = bundle_dir.relative_to(evals_dir)
        except ValueError:
            continue
        family_relative = Path(*bundle_relative.parts[:-1])
        if family_relative != family:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    f"bundle must live under evals/{family.as_posix()}/",
                )
            )
    return bundle_count


def validate_local_note_dir(
    repo_root: Path,
    evals_dir: Path,
    directory_name: str,
    canonical_owner_repo: str,
    issues: list[ValidationIssue],
) -> int:
    config = LOCAL_NOTE_CONFIG[directory_name]
    directory = evals_dir / directory_name
    if not directory.is_dir():
        return 0

    note_count = 0
    for path in sorted(directory.glob("*.md")):
        if path.name == "README.md":
            continue
        note_count += 1
        if not path.match(config["glob"]):
            issues.append(
                ValidationIssue(
                    relative_location(path, repo_root),
                    f"{config['label']} filename must match {config['glob']}",
                )
            )
            continue

        payload = load_markdown_frontmatter(path, repo_root, issues)
        if payload is None:
            continue
        location = relative_location(path, repo_root)
        if payload.get("schema_version") != config["schema_version"]:
            issues.append(
                ValidationIssue(
                    location,
                    f"schema_version must be '{config['schema_version']}'",
                )
            )
        if payload.get("owner_repo") != canonical_owner_repo:
            issues.append(
                ValidationIssue(
                    location,
                    f"owner_repo must match canonical repo identity '{canonical_owner_repo}'",
                )
            )
        if payload.get("status") not in {"draft", "reviewed"}:
            issues.append(ValidationIssue(location, "status must be 'draft' or 'reviewed'"))
        boundary = payload.get("authority_boundary")
        if not isinstance(boundary, str) or not boundary.strip():
            issues.append(ValidationIssue(location, "authority_boundary must be a non-empty string"))
        else:
            lowered = boundary.lower()
            missing = [token for token in LOCAL_NOTE_BOUNDARY_TOKENS if token not in lowered]
            if missing:
                issues.append(
                    ValidationIssue(
                        location,
                        "authority_boundary must name no verdict, scoring, regression, or proof doctrine authority",
                    )
                )
    return note_count


def validate_status(
    repo_root: Path,
    evals_dir: Path,
    port_payload: dict[str, Any] | None,
    *,
    intake_count: int,
    bundle_count: int,
    suite_count: int,
    suite_execution_contract_count: int,
    report_count: int,
    issues: list[ValidationIssue],
) -> None:
    if not port_payload:
        return
    location = relative_location(evals_dir / "PORT.yaml", repo_root)
    status = port_payload.get("status")
    active_count = (
        intake_count
        + bundle_count
        + suite_count
        + suite_execution_contract_count
        + report_count
    )
    if status == "active" and active_count == 0:
        issues.append(
            ValidationIssue(
                location,
                "active local eval port must contain at least one intake packet, local bundle, suite note, or report note",
            )
        )
    if status == "skeleton" and active_count > 0:
        issues.append(
            ValidationIssue(
                location,
                "skeleton local eval port must not contain active intake packets, bundles, suite notes, or report notes",
            )
        )


def validate_local_eval_port(repo_root: Path) -> list[ValidationIssue]:
    repo_root = repo_root.resolve()
    repo_identity = resolve_repo_identity(repo_root)
    evals_dir = repo_root / "evals"
    issues = validate_required_shape(repo_root, evals_dir)
    if evals_dir.is_symlink() or (evals_dir / "suites").is_symlink():
        return issues
    if not evals_dir.is_dir():
        return issues

    port_payload = validate_port_file(repo_root, evals_dir, repo_identity, issues)
    validate_port_docs(repo_root, evals_dir, issues)
    intake_count = validate_intake_payloads(repo_root, evals_dir, issues)
    bundle_count = validate_local_bundles(repo_root, evals_dir, issues)
    suite_count = validate_local_note_dir(
        repo_root,
        evals_dir,
        "suites",
        repo_identity.owner_repo,
        issues,
    )
    report_count = validate_local_note_dir(
        repo_root,
        evals_dir,
        "reports",
        repo_identity.owner_repo,
        issues,
    )
    suite_execution = evaluate_local_suite_execution(repo_root)
    for issue in suite_execution["issues"]:
        issues.append(ValidationIssue(str(issue["location"]), str(issue["message"])))
    validate_status(
        repo_root,
        evals_dir,
        port_payload,
        intake_count=intake_count,
        bundle_count=bundle_count,
        suite_count=suite_count,
        suite_execution_contract_count=int(suite_execution["suite_count"]),
        report_count=report_count,
        issues=issues,
    )
    return issues


def format_issues(issues: Sequence[ValidationIssue]) -> str:
    return "\n".join(f"- {issue.location}: {issue.message}" for issue in issues)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    target_root = Path(args.target_root)
    issues = validate_local_eval_port(target_root)
    suite_execution = evaluate_local_suite_execution(target_root)
    suite_execution_blocked = suite_execution["state"] in {"invalid", "stale"}
    if args.json:
        print(
            json.dumps(
                {
                    "schema": "local_eval_port_validation_v1",
                    "target_root": str(target_root.resolve()),
                    "ok": not issues and not suite_execution_blocked,
                    "suite_execution": suite_execution,
                    "issues": [
                        {"location": issue.location, "message": issue.message}
                        for issue in issues
                    ],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif issues or suite_execution_blocked:
        print("Local eval port validation failed:")
        if issues:
            print(format_issues(issues))
        if suite_execution["state"] == "stale":
            print("- evals/suites: one or more suite execution contracts have stale tracked-source hashes")
    else:
        print("Local eval port validation passed.")
    return 1 if issues or suite_execution_blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
