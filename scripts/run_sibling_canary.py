#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
from pathlib import Path
from typing import Any, Iterator, Sequence

import validate_repo


ROOT_VARIABLE_NAMES = {
    "AOA_TECHNIQUES_ROOT",
    "AOA_SKILLS_ROOT",
    "AOA_AGENTS_ROOT",
    "AOA_PLAYBOOKS_ROOT",
    "AOA_MEMO_ROOT",
    "AOA_STATS_ROOT",
    "ABYSS_STACK_ROOT",
}
ALLOWED_RESOLVERS = {"direct", "abyss-stack-source"}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the aoa-evals latest-sibling canary against an explicit matrix."
    )
    parser.add_argument("--repo-root", default=".", help="Path to the local aoa-evals checkout.")
    parser.add_argument(
        "--matrix",
        default="scripts/sibling_canary_matrix.json",
        help="Path to the sibling canary matrix JSON file.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args(argv)


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def resolve_path(repo_root: Path, raw_path: str) -> Path:
    candidate = Path(raw_path).expanduser()
    if not candidate.is_absolute():
        candidate = repo_root / candidate
    return candidate.resolve()


def normalized_entries(payload: dict[str, Any]) -> list[dict[str, Any]]:
    version = payload.get("matrix_version")
    if version != 1:
        raise ValueError("sibling canary matrix must declare matrix_version=1")

    entries = payload.get("entries")
    if not isinstance(entries, list) or not entries:
        raise ValueError("sibling canary matrix must define a non-empty 'entries' array")

    normalized: list[dict[str, Any]] = []
    seen_repos: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("sibling canary matrix entries must be objects")

        repo = entry.get("repo")
        if not isinstance(repo, str) or not repo:
            raise ValueError("each sibling canary matrix entry must declare a non-empty 'repo'")
        if repo in seen_repos:
            raise ValueError(f"duplicate sibling canary entry for repo {repo!r}")
        seen_repos.add(repo)

        root_variable = entry.get("root_variable")
        if not isinstance(root_variable, str) or root_variable not in ROOT_VARIABLE_NAMES:
            raise ValueError(
                f"sibling canary entry {repo!r} must declare a supported 'root_variable'"
            )

        path_value = entry.get("path")
        if not isinstance(path_value, str) or not path_value:
            raise ValueError(f"sibling canary entry {repo!r} must declare a non-empty 'path'")

        purpose = entry.get("purpose", "")
        if not isinstance(purpose, str) or not purpose:
            raise ValueError(f"sibling canary entry {repo!r} must declare a non-empty 'purpose'")

        resolver = entry.get("resolver", "direct")
        if not isinstance(resolver, str) or resolver not in ALLOWED_RESOLVERS:
            raise ValueError(
                f"sibling canary entry {repo!r} declares unsupported resolver {resolver!r}"
            )

        normalized.append(
            {
                "repo": repo,
                "root_variable": root_variable,
                "path": path_value,
                "purpose": purpose,
                "resolver": resolver,
            }
        )
    return normalized


def resolve_entry_path(repo_root: Path, entry: dict[str, Any]) -> Path:
    resolved = resolve_path(repo_root, str(entry["path"]))
    if entry["resolver"] == "abyss-stack-source":
        return validate_repo.resolve_abyss_stack_root(resolved)
    return resolved


def resolved_entries(repo_root: Path, entries: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    resolved_payload: list[dict[str, Any]] = []
    for entry in entries:
        resolved_path = resolve_entry_path(repo_root, entry)
        if not resolved_path.exists() or not resolved_path.is_dir():
            raise ValueError(
                f"sibling canary repo path does not exist for {entry['repo']}: {resolved_path}"
            )
        resolved_payload.append(
            {
                **entry,
                "resolved_path": resolved_path,
            }
        )
    return resolved_payload


@contextlib.contextmanager
def override_validate_repo_roots(
    repo_root: Path,
    entries: Sequence[dict[str, Any]],
) -> Iterator[None]:
    tracked_attributes = list(ROOT_VARIABLE_NAMES) + ["VISIBLE_ROOTS", "REPO_REF_ROOTS"]
    original_values = {
        name: getattr(validate_repo, name)
        for name in tracked_attributes
    }
    try:
        for entry in entries:
            setattr(validate_repo, str(entry["root_variable"]), Path(entry["resolved_path"]))
        validate_repo.VISIBLE_ROOTS = (
            repo_root,
            validate_repo.AOA_TECHNIQUES_ROOT,
            validate_repo.AOA_SKILLS_ROOT,
            validate_repo.AOA_AGENTS_ROOT,
            validate_repo.AOA_PLAYBOOKS_ROOT,
            validate_repo.AOA_MEMO_ROOT,
            validate_repo.ABYSS_STACK_ROOT,
        )
        validate_repo.REPO_REF_ROOTS = {
            "aoa-evals": repo_root,
            "aoa-techniques": validate_repo.AOA_TECHNIQUES_ROOT,
            "aoa-skills": validate_repo.AOA_SKILLS_ROOT,
            "aoa-agents": validate_repo.AOA_AGENTS_ROOT,
            "aoa-playbooks": validate_repo.AOA_PLAYBOOKS_ROOT,
            "aoa-memo": validate_repo.AOA_MEMO_ROOT,
            "abyss-stack": validate_repo.ABYSS_STACK_ROOT,
        }
        yield
    finally:
        for name, value in original_values.items():
            setattr(validate_repo, name, value)


def invoke_validator(repo_root: Path) -> tuple[int, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        exit_code = validate_repo.main(argv=[], repo_root=repo_root)
    combined = "\n".join(
        chunk.strip()
        for chunk in (stdout.getvalue(), stderr.getvalue())
        if chunk.strip()
    )
    return exit_code, combined


def build_summary(
    repo_root: Path,
    matrix_path: Path,
    entries: Sequence[dict[str, Any]],
    validator_exit_code: int,
    validator_output: str,
) -> dict[str, Any]:
    if validator_exit_code == 0:
        status = "ok"
    elif validator_exit_code == 1:
        status = "failed"
    else:
        status = "error"

    return {
        "matrix_path": matrix_path.as_posix(),
        "repo_root": repo_root.as_posix(),
        "status": status,
        "validator_exit_code": validator_exit_code,
        "entries": [
            {
                "repo": str(entry["repo"]),
                "root_variable": str(entry["root_variable"]),
                "path": str(entry["path"]),
                "purpose": str(entry["purpose"]),
                "resolver": str(entry["resolver"]),
                "resolved_path": Path(entry["resolved_path"]).as_posix(),
            }
            for entry in entries
        ],
        "validator_output": validator_output,
    }


def render_text(summary: dict[str, Any]) -> str:
    lines = [
        f"Sibling canary matrix: {summary['matrix_path']}",
        f"aoa-evals repo root: {summary['repo_root']}",
        f"validator status: {summary['status']}",
    ]
    for entry in summary["entries"]:
        lines.extend(
            [
                "",
                f"{entry['repo']}",
                f"- root variable: {entry['root_variable']}",
                f"- requested path: {entry['path']}",
                f"- resolved path: {entry['resolved_path']}",
                f"- resolver: {entry['resolver']}",
                f"- purpose: {entry['purpose']}",
            ]
        )
    if summary["validator_output"]:
        lines.extend(
            [
                "",
                "validator output:",
                summary["validator_output"],
            ]
        )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    matrix_path = (repo_root / args.matrix).resolve()

    try:
        payload = load_json(matrix_path)
        entries = normalized_entries(payload)
        resolved = resolved_entries(repo_root, entries)
        with override_validate_repo_roots(repo_root, resolved):
            validator_exit_code, validator_output = invoke_validator(repo_root)
        summary = build_summary(
            repo_root,
            matrix_path,
            resolved,
            validator_exit_code,
            validator_output,
        )
    except (FileNotFoundError, ValueError) as exc:
        if args.format == "json":
            print(json.dumps({"status": "error", "error": str(exc)}, indent=2) + "\n", end="")
        else:
            print(f"[error] {exc}")
        return 2

    if args.format == "json":
        print(json.dumps(summary, indent=2) + "\n", end="")
    else:
        print(render_text(summary))

    return validator_exit_code


if __name__ == "__main__":
    raise SystemExit(main())
