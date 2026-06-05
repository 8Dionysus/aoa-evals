"""Shared runtime audit validation context."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping


@dataclass(frozen=True)
class RuntimeAuditContext:
    agents_of_abyss_root: Path
    abyss_stack_root: Path
    aoa_playbooks_root: Path
    repo_ref_roots: Mapping[str, Path]
    strict_sibling_compat_checks_enabled: Callable[[], bool]
    parse_repo_ref: Callable[..., tuple[str, Path, str | None] | None]
    parse_named_surface_ref: Callable[..., tuple[Path, str | None] | None]
    validate_abyss_stack_ref: Callable[..., Any]
