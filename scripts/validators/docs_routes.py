"""Docs route-map contracts for agent-operable documentation."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote


DOCS_README = Path("docs/README.md")
DOCS_DIR = Path("docs")
README_ROUTE_FIELDS = (
    "role",
    "entry",
    "input",
    "output",
    "owner",
    "next route",
    "validation",
)
README_REQUIRED_HEADINGS = (
    "Operating Card",
    "First Route",
    "Folder Map",
    "Recommended Reading Paths",
    "Validation Route",
)
README_FOLDER_ROUTES = (
    "docs/architecture/",
    "docs/guides/",
    "docs/operations/",
    "docs/validation/",
    "docs/testing/",
    "docs/decisions/",
)
RELATIVE_LINK_RE = re.compile(r"!?\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def _heading_offset(text: str, heading: str) -> int:
    match = re.search(rf"^## {re.escape(heading)}\s*$", text, re.MULTILINE)
    return -1 if match is None else match.start()


def _has_fenced_python_command(text: str) -> bool:
    in_fence = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence and line.startswith("python "):
            return True
    return False


def _relative_markdown_links(text: str) -> list[str]:
    links: list[str] = []
    for match in RELATIVE_LINK_RE.finditer(text):
        target = match.group(1).strip()
        if (
            not target
            or target.startswith("#")
            or target.startswith(("http://", "https://", "mailto:"))
            or ":" in target.split("#", 1)[0]
        ):
            continue
        links.append(unquote(target.split("#", 1)[0]))
    return links


def _validate_docs_markdown_links(repo_root: Path) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    docs_root = repo_root / DOCS_DIR
    if not docs_root.is_dir():
        return [(DOCS_DIR.as_posix(), "docs directory is missing")]

    for markdown_path in sorted(docs_root.rglob("*.md")):
        relative_path = markdown_path.relative_to(repo_root)
        text = markdown_path.read_text(encoding="utf-8")
        for target in _relative_markdown_links(text):
            resolved = (markdown_path.parent / target).resolve()
            if not resolved.exists():
                issues.append(
                    (
                        relative_path.as_posix(),
                        f"relative docs link target is missing: {target}",
                    )
                )
    return issues


def validate_docs_routes(repo_root: Path) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    readme_path = repo_root / DOCS_README
    if not readme_path.is_file():
        return [(DOCS_README.as_posix(), "docs route chooser is missing")]

    text = readme_path.read_text(encoding="utf-8")
    for heading in README_REQUIRED_HEADINGS:
        if _heading_offset(text, heading) == -1:
            issues.append((DOCS_README.as_posix(), f"docs route chooser must contain ## {heading}"))

    for field in README_ROUTE_FIELDS:
        if f"| {field} |" not in text:
            issues.append((DOCS_README.as_posix(), f"docs operating card must define {field!r}"))

    for folder_route in README_FOLDER_ROUTES:
        if folder_route not in text:
            issues.append((DOCS_README.as_posix(), f"docs route chooser must route {folder_route}"))

    recommended_offset = _heading_offset(text, "Recommended Reading Paths")
    validation_offset = _heading_offset(text, "Validation Route")
    if recommended_offset != -1 and validation_offset != -1 and validation_offset < recommended_offset:
        issues.append(
            (
                DOCS_README.as_posix(),
                "docs validation route must follow recommended reading paths",
            )
        )

    if _has_fenced_python_command(text):
        issues.append(
            (
                DOCS_README.as_posix(),
                "docs route chooser must link validation routes instead of owning python command blocks",
            )
        )

    issues.extend(_validate_docs_markdown_links(repo_root))
    return issues
