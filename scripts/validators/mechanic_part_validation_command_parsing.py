"""Mechanic part validation-command parsing helpers."""

from __future__ import annotations

import shlex


def validation_command_referenced_paths(command: str) -> tuple[list[str], str | None]:
    try:
        parts = shlex.split(command)
    except ValueError as exc:
        return [], f"validation command cannot be parsed: {exc}"

    if not parts:
        return [], None

    paths: list[str] = []
    if (
        len(parts) > 3
        and parts[1] == "-m"
        and parts[2] == "pytest"
    ):
        for token in parts[3:]:
            if token.startswith("-") or token in {"and", "|"}:
                continue
            if token.endswith(".py") or "/" in token:
                paths.append(token.split("::", 1)[0])
        return paths, None

    if len(parts) > 1:
        first_arg = parts[1]
        if first_arg.endswith(".py") or "/" in first_arg:
            paths.append(first_arg)
    return paths, None


__all__ = ("validation_command_referenced_paths",)
