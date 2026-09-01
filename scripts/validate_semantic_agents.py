#!/usr/bin/env python3
"""Validate Pack 4 semantic-layer AGENTS.md guidance for aoa-evals."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
import re

REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class AgentsDocSpec:
    path: Path
    required_snippets: tuple[str, ...]


REQUIRED_DOCS: tuple[AgentsDocSpec, ...] = (
    AgentsDocSpec(
        Path('.aoa/live_receipts/AGENTS.md'),
        (
            'live receipt',
            'not new verdict authority',
            'object under evaluation',
            'public-safe',
            'the on-demand [VALIDATION.md](VALIDATION.md) route',
        ),
    ),
    AgentsDocSpec(
        Path('config/AGENTS.md'),
        (
            'compatibility route card',
            'Active root config payloads route to the operation that owns them',
            'mechanics/agon/parts',
            'draft',
            'bounded',
            'EVAL_SELECTION.md',
            'the on-demand [VALIDATION.md](VALIDATION.md) route',
        ),
    ),
    AgentsDocSpec(
        Path('docs/AGENTS.md'),
        (
            'eval philosophy',
            'EVAL.md',
            'eval.yaml',
            'anti-overread',
            'EVAL_SELECTION.md',
        ),
    ),
    AgentsDocSpec(
        Path('examples/AGENTS.md'),
        (
            'artifact-to-verdict',
            'public-safe',
            'proof limits',
            'schemas',
            'the on-demand [VALIDATION.md](VALIDATION.md) route',
        ),
    ),
    AgentsDocSpec(
        Path('manifests/AGENTS.md'),
        (
            'compatibility route card',
            'Active root manifest payloads route with the mechanic part',
            'mechanics/agon/parts',
            'mechanics/recurrence/parts/control-plane-integrity/manifests/',
            'the on-demand [VALIDATION.md](VALIDATION.md) route',
        ),
    ),
    AgentsDocSpec(
        Path('reports/AGENTS.md'),
        (
            'bounded outputs',
            'object under evaluation',
            'blind spots',
            'public-safe',
            'the on-demand [VALIDATION.md](VALIDATION.md) route',
        ),
    ),
    AgentsDocSpec(
        Path('schemas/AGENTS.md'),
        (
            'Schema edits are proof contract edits',
            '$schema',
            'verdict interpretation',
            'examples',
            'the on-demand [VALIDATION.md](VALIDATION.md) route',
        ),
    ),
    AgentsDocSpec(
        Path('scripts/AGENTS.md'),
        (
            'builders',
            'deterministic',
            'generated catalogs',
            'bounded proof posture',
            'the on-demand [VALIDATION.md](VALIDATION.md) route',
        ),
    ),
    AgentsDocSpec(
        Path('tests/AGENTS.md'),
        (
            'repo-wide eval contracts',
            'mechanic-owned tests',
            'anti-overread posture',
            'public-safe',
            'the on-demand [VALIDATION.md](VALIDATION.md) route',
            'semantic AGENTS validator',
        ),
    ),
)

RUNNABLE_AGENT_LINE_RE = re.compile(
    r"(?m)^\s*(?:\$\s*)?(?:python3?\s+|pytest(?:\s|$)|git\s+(?:check|diff|status|log|show|rev-parse|ls-files)\b)"
)
RUNNABLE_AGENT_INLINE_RE = re.compile(r"`(?:python3?\s+|pytest(?:\s|`)|git\s+(?:check|diff|status|log|show|rev-parse|ls-files)\b)")
STALE_EXECUTABLE_ROUTE_RE = re.compile(
    r"(?i)(?:AGENTS\.md#(?:validation|verify)|(?:executable|validation)\s+commands?[^\n]*\bAGENTS(?:\.md)?\b)"
)


def validate_all_agent_docs(repo_root: Path) -> list[str]:
    """Keep executable checks in local on-demand VALIDATION.md companions."""
    issues: list[str] = []
    for path in sorted(repo_root.rglob("AGENTS.md")):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if RUNNABLE_AGENT_LINE_RE.search(text) or RUNNABLE_AGENT_INLINE_RE.search(text):
            issues.append(f"{path.relative_to(repo_root).as_posix()}: executable command belongs in nearest VALIDATION.md")
        if STALE_EXECUTABLE_ROUTE_RE.search(text):
            issues.append(
                f"{path.relative_to(repo_root).as_posix()}: executable validation route belongs in nearest VALIDATION.md"
            )
        if "[VALIDATION.md](VALIDATION.md)" in text and not path.with_name("VALIDATION.md").is_file():
            issues.append(
                f"{path.relative_to(repo_root).as_posix()}: linked local VALIDATION.md companion is missing"
            )
        read_match = re.search(r"(?ms)^## Read [Bb]efore [Ee]diting\s*\n(.*?)(?=^## |\Z)", text)
        if read_match and re.search(r"(?m)^\s*(?:[-*]\s+|\d+[.)]\s+)", read_match.group(1)):
            issues.append(f"{path.relative_to(repo_root).as_posix()}: unconditional read inventory belongs in conditional route prose")
    return issues


def _display(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def validate(repo_root: Path = REPO_ROOT) -> list[str]:
    issues: list[str] = []
    for spec in REQUIRED_DOCS:
        path = repo_root / spec.path
        if not path.is_file():
            issues.append(f"{spec.path.as_posix()}: file is missing")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.strip().startswith("# AGENTS.md"):
            issues.append(f"{spec.path.as_posix()}: must start with '# AGENTS.md'")
        for snippet in spec.required_snippets:
            if snippet not in text:
                issues.append(
                    f"{spec.path.as_posix()}: missing required snippet {snippet!r}"
                )
    issues.extend(validate_all_agent_docs(repo_root))
    return issues


def main() -> int:
    issues = validate(REPO_ROOT)
    if issues:
        print("Pack 4 semantic AGENTS validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1
    print(f"[ok] Pack 4 semantic AGENTS docs are present and shaped: {len(REQUIRED_DOCS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
