#!/usr/bin/env python3
"""Build a read-only OS Abyss local eval-port inventory."""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

import yaml

import validate_local_eval_port


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = Path("docs/architecture/local_eval_port_inventory.contract.v1.json")
DEFAULT_WORKSPACE_ROOT = Path("/srv/AbyssOS")
DEFAULT_MAX_DEPTH = 4
SCHEMA_VERSION = "os_abyss_local_eval_port_inventory_v1"
PROOF_OWNER_REPO = "aoa-evals"
AUTHORITY_BOUNDARY = (
    "Repo-local eval ports carry intake, suites, reports, and pressure evidence "
    "only. Central verdict, scoring, regression, proof doctrine, and central "
    "bundle adoption remain in aoa-evals."
)
SOURCE_OF_TRUTH = {
    "local_port_standard": "docs/guides/LOCAL_EVAL_PORT_STANDARD.md",
    "local_port_validator": "scripts/validate_local_eval_port.py",
    "central_eval_catalog": "generated/eval_catalog.min.json",
    "mcp_contract": "docs/architecture/AOA_EVALS_MCP_CONTRACT.md",
    "inventory_contract": CONTRACT_PATH.as_posix(),
}
IGNORED_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".aoa",
    ".codex",
    ".worktrees",
    ".tox",
    ".venv",
    "__pycache__",
    "node_modules",
}
IGNORED_RELATIVE_PREFIXES = (
    ".worktrees",
    ".codex",
    "abyss-stack/Logs",
    "abyss-stack/Models",
    "abyss-stack/Services",
    "bundles",
)


@dataclass(frozen=True)
class PressureCounts:
    intake_packets: int
    suite_notes: int
    report_notes: int
    local_bundles: int

    @property
    def active_total(self) -> int:
        return self.intake_packets + self.suite_notes + self.report_notes + self.local_bundles


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace-root",
        default=str(DEFAULT_WORKSPACE_ROOT),
        help="Workspace root containing OS Abyss repositories.",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=DEFAULT_MAX_DEPTH,
        help="Maximum relative directory depth to inspect for git repositories.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON inventory to stdout instead of Markdown.",
    )
    parser.add_argument(
        "--json-output",
        help="Optional path to write the machine-readable inventory JSON.",
    )
    parser.add_argument(
        "--markdown-output",
        help="Optional path to write the human-readable inventory report.",
    )
    return parser.parse_args(argv)


def repo_relative(path: Path, root: Path) -> str:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return path.as_posix()
    return "." if str(relative) == "." else relative.as_posix()


def local_repo_id(path: Path, root: Path) -> str:
    relative = repo_relative(path, root)
    return path.name if relative == "." else relative


def is_ignored_path(path: Path, workspace_root: Path) -> bool:
    relative = repo_relative(path, workspace_root)
    if relative == ".":
        return False
    return any(relative == prefix or relative.startswith(f"{prefix}/") for prefix in IGNORED_RELATIVE_PREFIXES)


def relative_depth(path: Path, workspace_root: Path) -> int:
    relative = repo_relative(path, workspace_root)
    if relative == ".":
        return 0
    return len(Path(relative).parts)


def has_valid_git_marker(path: Path) -> bool:
    git_marker = path / ".git"
    if git_marker.is_dir():
        return (git_marker / "HEAD").is_file()
    if not git_marker.is_file():
        return False
    try:
        first_line = git_marker.read_text(encoding="utf-8").splitlines()[0]
    except (IndexError, OSError, UnicodeDecodeError):
        return False
    return first_line.startswith("gitdir:")


def discover_repo_roots(workspace_root: Path, *, max_depth: int) -> list[Path]:
    workspace_root = workspace_root.resolve()
    repo_roots: list[Path] = []
    for current, dirnames, _filenames in os.walk(workspace_root):
        current_path = Path(current)
        if is_ignored_path(current_path, workspace_root):
            dirnames[:] = []
            continue
        if relative_depth(current_path, workspace_root) > max_depth:
            dirnames[:] = []
            continue

        dirnames[:] = sorted(
            name
            for name in dirnames
            if name not in IGNORED_DIR_NAMES
            and not name.startswith(".")
            and not is_ignored_path(current_path / name, workspace_root)
        )

        if has_valid_git_marker(current_path):
            repo_roots.append(current_path)
    return sorted(set(repo_roots), key=lambda path: repo_relative(path, workspace_root))


def excluded_repo_reason(repo_root: Path) -> str | None:
    if repo_root.name == PROOF_OWNER_REPO:
        return "central_proof_owner_not_repo_local_port"
    return None


def read_yaml_mapping(path: Path) -> dict[str, Any]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, yaml.YAMLError):
        return {}
    return payload if isinstance(payload, dict) else {}


def read_json_mapping(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def load_inventory_contract(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    return read_json_mapping(repo_root / CONTRACT_PATH)


def contract_route_recommendation(route_key: str) -> dict[str, str]:
    contract = load_inventory_contract()
    routes = contract.get("route_recommendations")
    if isinstance(routes, list):
        for route in routes:
            if isinstance(route, dict) and route.get("route_key") == route_key:
                return {str(key): str(value) for key, value in route.items()}
    raise RuntimeError(f"inventory contract missing route recommendation: {route_key}")


def load_central_eval_names(repo_root: Path = REPO_ROOT) -> set[str]:
    catalog = read_json_mapping(repo_root / "generated" / "eval_catalog.min.json")
    evals = catalog.get("evals")
    if not isinstance(evals, list):
        return set()
    names: set[str] = set()
    for record in evals:
        if not isinstance(record, dict):
            continue
        name = record.get("name")
        if isinstance(name, str) and name:
            names.add(name)
    return names


def count_matching_files(directory: Path, pattern: str, *, excluded_names: Iterable[str] = ()) -> int:
    if not directory.is_dir():
        return 0
    excluded = set(excluded_names)
    return sum(1 for path in directory.glob(pattern) if path.is_file() and path.name not in excluded)


def count_local_bundles(evals_dir: Path) -> int:
    if not evals_dir.is_dir():
        return 0
    return sum(1 for path in evals_dir.glob("**/eval.yaml") if path.is_file())


def collect_pressure_counts(evals_dir: Path) -> PressureCounts:
    return PressureCounts(
        intake_packets=count_matching_files(evals_dir / "intake", "*.eval_need.json"),
        suite_notes=count_matching_files(evals_dir / "suites", "*.suite.md", excluded_names={"README.md"}),
        report_notes=count_matching_files(evals_dir / "reports", "*.report.md", excluded_names={"README.md"}),
        local_bundles=count_local_bundles(evals_dir),
    )


def local_eval_names(evals_dir: Path) -> set[str]:
    names: set[str] = set()
    if not evals_dir.is_dir():
        return names

    for manifest_path in sorted(evals_dir.glob("**/eval.yaml")):
        payload = read_yaml_mapping(manifest_path)
        name = payload.get("name")
        if isinstance(name, str) and name:
            names.add(name)

    for intake_path in sorted((evals_dir / "intake").glob("*.eval_need.json")):
        payload = read_json_mapping(intake_path)
        name = payload.get("name")
        if isinstance(name, str) and name:
            names.add(name)
    return names


def validation_issues(repo_root: Path) -> list[dict[str, str]]:
    return [
        {"location": issue.location, "message": issue.message}
        for issue in validate_local_eval_port.validate_local_eval_port(repo_root)
    ]


def central_boundary_ok(port_payload: dict[str, Any], issues: list[dict[str, str]]) -> bool:
    if port_payload.get("proof_owner_repo") != PROOF_OWNER_REPO:
        return False
    for issue in issues:
        if issue["location"] != "evals/PORT.yaml":
            continue
        message = issue["message"]
        if "proof_owner_repo" in message or "central_boundary" in message:
            return False
    return True


def inventory_status(
    *,
    evals_dir: Path,
    port_path: Path,
    issues: list[dict[str, str]],
    declared_status: str | None,
) -> str:
    if not port_path.is_file():
        if evals_dir.exists():
            return "stale_candidate"
        return "missing"
    if issues:
        return "invalid"
    if declared_status in {"skeleton", "active"}:
        return declared_status
    return "invalid"


def route_recommendation(
    *,
    status: str,
    declared_status: str | None,
    counts: PressureCounts,
    central_matches: list[str],
) -> dict[str, str]:
    if status == "missing":
        return contract_route_recommendation("missing_no_pressure")
    if status == "stale_candidate":
        return contract_route_recommendation("stale_local_eval_surface_review")
    if status == "invalid":
        return contract_route_recommendation(
            "invalid_active_repair" if declared_status == "active" else "invalid_port_repair"
        )
    if central_matches:
        return contract_route_recommendation("central_overlap_apply_existing_first")
    if status == "skeleton":
        return contract_route_recommendation("valid_skeleton_keep_dormant")
    if counts.local_bundles:
        return contract_route_recommendation("local_bundle_central_review_candidate")
    if counts.suite_notes:
        return contract_route_recommendation("active_suite_apply_or_regression_check")
    if counts.intake_packets:
        return contract_route_recommendation("active_intake_select_then_apply_or_design")
    if counts.report_notes:
        return contract_route_recommendation("active_reports_only_suite_extraction_or_review")
    return contract_route_recommendation("active_without_detected_pressure")


def build_repo_entry(repo_root: Path, workspace_root: Path, central_eval_names: set[str]) -> dict[str, Any]:
    evals_dir = repo_root / "evals"
    port_path = evals_dir / "PORT.yaml"
    port_payload = read_yaml_mapping(port_path)
    issues = validation_issues(repo_root) if evals_dir.exists() or port_path.exists() else []
    counts = collect_pressure_counts(evals_dir)
    declared_status = port_payload.get("status") if isinstance(port_payload.get("status"), str) else None
    status = inventory_status(
        evals_dir=evals_dir,
        port_path=port_path,
        issues=issues,
        declared_status=declared_status,
    )
    central_matches = sorted(local_eval_names(evals_dir) & central_eval_names)

    entry = {
        "repo": repo_root.name,
        "repo_path": repo_relative(repo_root, workspace_root),
        "repo_id": local_repo_id(repo_root, workspace_root),
        "root": repo_root.as_posix(),
        "port_path": repo_relative(port_path, repo_root),
        "inventory_status": status,
        "validator_ok": not issues and status not in {"missing", "stale_candidate"},
        "declared_status": declared_status,
        "pressure_counts": {
            "intake_packets": counts.intake_packets,
            "suite_notes": counts.suite_notes,
            "report_notes": counts.report_notes,
            "local_bundles": counts.local_bundles,
            "active_total": counts.active_total,
        },
        "owner_boundary": {
            "schema_version": port_payload.get("schema_version"),
            "owner_repo": port_payload.get("owner_repo"),
            "proof_owner_repo": port_payload.get("proof_owner_repo"),
            "default_intake_schema": port_payload.get("default_intake_schema"),
            "local_role": port_payload.get("local_role"),
            "central_boundary": port_payload.get("central_boundary"),
            "central_proof_boundary_ok": central_boundary_ok(port_payload, issues),
        },
        "central_eval_name_matches": central_matches,
        "validation_issues": issues,
    }
    entry["route_recommendation"] = route_recommendation(
        status=status,
        declared_status=declared_status,
        counts=counts,
        central_matches=central_matches,
    )
    return entry


def build_summary(entries: list[dict[str, Any]]) -> dict[str, int]:
    summary: dict[str, int] = {
        "repos": len(entries),
        "validator_ok": sum(1 for entry in entries if entry["validator_ok"]),
        "validator_failed": sum(1 for entry in entries if entry["validation_issues"]),
        "with_local_port": sum(1 for entry in entries if entry["inventory_status"] not in {"missing", "stale_candidate"}),
        "with_detected_pressure": sum(
            1 for entry in entries if entry["pressure_counts"]["active_total"] > 0
        ),
    }
    for status in ("missing", "stale_candidate", "invalid", "skeleton", "active"):
        summary[status] = sum(1 for entry in entries if entry["inventory_status"] == status)
    return summary


def build_inventory_payload(workspace_root: Path, *, max_depth: int = DEFAULT_MAX_DEPTH) -> dict[str, Any]:
    workspace_root = workspace_root.resolve()
    central_eval_names = load_central_eval_names()
    repo_roots = discover_repo_roots(workspace_root, max_depth=max_depth)
    excluded_repos = [
        {
            "repo": path.name,
            "repo_path": repo_relative(path, workspace_root),
            "repo_id": local_repo_id(path, workspace_root),
            "reason": reason,
        }
        for path in repo_roots
        for reason in [excluded_repo_reason(path)]
        if reason is not None
    ]
    entries = [
        build_repo_entry(path, workspace_root, central_eval_names)
        for path in repo_roots
        if excluded_repo_reason(path) is None
    ]
    entries.sort(key=lambda entry: str(entry["repo_id"]))
    excluded_repos.sort(key=lambda entry: str(entry["repo_id"]))
    summary = build_summary(entries)
    summary["excluded_repos"] = len(excluded_repos)
    return {
        "contract_schema_version": load_inventory_contract().get("schema_version"),
        "contract_ref": CONTRACT_PATH.as_posix(),
        "schema_version": SCHEMA_VERSION,
        "layer": "aoa-evals-local-port-inventory",
        "workspace_root": workspace_root.as_posix(),
        "proof_owner_repo": PROOF_OWNER_REPO,
        "authority_boundary": AUTHORITY_BOUNDARY,
        "source_of_truth": SOURCE_OF_TRUTH,
        "summary": summary,
        "excluded_repos": excluded_repos,
        "repos": entries,
    }


def markdown_table_row(values: Sequence[str]) -> str:
    return "| " + " | ".join(value.replace("\n", " ") for value in values) + " |"


def build_markdown_report(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# OS Abyss Local Eval-Port Inventory",
        "",
        "This read-model is generated from repo-local `evals/` ports and the",
        "`aoa-evals` local-port validator. It is routing evidence, not central",
        "proof acceptance.",
        "",
        "## Boundary",
        "",
        str(payload["authority_boundary"]),
        "",
        "## Summary",
        "",
        f"- Workspace root: `{payload['workspace_root']}`",
        f"- Repositories scanned: {summary['repos']}",
        f"- Valid local ports: {summary['validator_ok']}",
        f"- Invalid local ports: {summary['validator_failed']}",
        f"- Missing ports: {summary['missing']}",
        f"- Skeleton ports: {summary['skeleton']}",
        f"- Active ports: {summary['active']}",
        f"- Stale candidates: {summary['stale_candidate']}",
        f"- Excluded central proof owners: {summary['excluded_repos']}",
        f"- Repos with detected pressure: {summary['with_detected_pressure']}",
        "",
        "## Route Table",
        "",
        markdown_table_row(
            [
                "Repo",
                "Status",
                "Validator",
                "Intake",
                "Suites",
                "Reports",
                "Bundles",
                "Route",
            ]
        ),
        markdown_table_row(["---", "---", "---", "---:", "---:", "---:", "---:", "---"]),
    ]
    for entry in payload["repos"]:
        counts = entry["pressure_counts"]
        route = entry["route_recommendation"]
        validator = "ok" if entry["validator_ok"] else f"{len(entry['validation_issues'])} issue(s)"
        lines.append(
            markdown_table_row(
                [
                    f"`{entry['repo_id']}`",
                    str(entry["inventory_status"]),
                    validator,
                    str(counts["intake_packets"]),
                    str(counts["suite_notes"]),
                    str(counts["report_notes"]),
                    str(counts["local_bundles"]),
                    str(route["route_key"]),
                ]
            )
        )

    invalid_entries = [entry for entry in payload["repos"] if entry["validation_issues"]]
    if invalid_entries:
        lines.extend(["", "## Validator Issues", ""])
        for entry in invalid_entries:
            lines.append(f"### `{entry['repo_id']}`")
            lines.append("")
            for issue in entry["validation_issues"]:
                lines.append(f"- `{issue['location']}`: {issue['message']}")
            lines.append("")

    excluded_entries = payload.get("excluded_repos")
    if isinstance(excluded_entries, list) and excluded_entries:
        lines.extend(["", "## Excluded Repositories", ""])
        for entry in excluded_entries:
            if not isinstance(entry, dict):
                continue
            lines.append(
                f"- `{entry.get('repo_id')}`: {entry.get('reason')}"
            )
        lines.append("")

    lines.extend(
        [
            "## Route Semantics",
            "",
            "- `missing_no_pressure`: no mutation unless current repo work creates real eval pressure.",
            "- `valid_skeleton_keep_dormant`: valid dormant port; stop unless pressure appears.",
            "- `active_intake_select_then_apply_or_design`: inspect local and central routes before applying or designing.",
            "- `active_suite_apply_or_regression_check`: local suite may drive deterministic checks; central proof stays in `aoa-evals`.",
            "- `active_reports_only_suite_extraction_or_review`: reports-only pressure may need suite extraction or central review.",
            "- `invalid_active_repair` / `invalid_port_repair`: repair port shape before eval adoption.",
            "- `central_overlap_apply_existing_first`: apply or inspect existing central route before local duplication.",
            "",
        ]
    )
    return "\n".join(lines)


def write_text_output(path_text: str | None, content: str) -> None:
    if not path_text:
        return
    path = Path(path_text)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    payload = build_inventory_payload(Path(args.workspace_root), max_depth=args.max_depth)
    json_text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    markdown_text = build_markdown_report(payload) + "\n"

    write_text_output(args.json_output, json_text)
    write_text_output(args.markdown_output, markdown_text)
    print(json_text if args.json else markdown_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
